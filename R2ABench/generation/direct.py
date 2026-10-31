#!/usr/bin/env python3
from __future__ import annotations

import argparse
import http.client
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Callable


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT_DIR = PROJECT_ROOT / "Dataset"
DEFAULT_LLM_MODEL = "deepseek-v4.1-flash"
DEFAULT_OUTPUT_ROOT = PROJECT_ROOT / "runs" / "direct"
API_KEY = ""
DEFAULT_LLM_API_URL = ""
SUPPORTED_DATASETS = ("G-R2A", "E-R2A")

LlmClient = Callable[..., str]


@dataclass(frozen=True)
class CheckedSrsSample:
    project_name: str
    srs_path: Path
    dataset_name: str = ""


@dataclass(frozen=True)
class GenerationResult:
    project_name: str
    status: str
    output_dir: Path
    predicted_path: Path
    message: str = ""


def sanitize_for_path(value: str) -> str:
    sanitized = re.sub(r'[<>:"/\\|?*\s]+', "_", value.strip())
    sanitized = sanitized.strip("._")
    return sanitized or "model"


def normalize_chat_completions_url(api_url: str) -> str:
    stripped = api_url.rstrip("/")
    if stripped.endswith("/chat/completions"):
        return stripped
    return f"{stripped}/chat/completions"


class NoRedirectHandler(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def open_llm_request(request: urllib.request.Request, timeout: int | None):
    opener = urllib.request.build_opener(NoRedirectHandler())
    return opener.open(request, timeout=timeout)


def normalize_timeout(timeout: int) -> int | None:
    return None if timeout <= 0 else timeout


def discover_checked_srs(root_dir: Path, sample_names: list[str] | None = None) -> list[CheckedSrsSample]:
    if not root_dir.exists():
        raise FileNotFoundError(f"Input directory not found: {root_dir}")

    allowed = set(sample_names or [])
    samples: list[CheckedSrsSample] = []
    for srs_path in sorted(root_dir.rglob("checked_srs.md"), key=lambda path: str(path).lower()):
        project_name = srs_path.parent.name
        if allowed and project_name not in allowed:
            continue
        samples.append(
            CheckedSrsSample(
                project_name=project_name,
                srs_path=srs_path,
                dataset_name=infer_dataset_name(root_dir, srs_path),
            )
        )
    return samples


def infer_dataset_name(root_dir: Path, srs_path: Path) -> str:
    if root_dir.name in SUPPORTED_DATASETS:
        return root_dir.name
    try:
        relative_parts = srs_path.relative_to(root_dir).parts
    except ValueError:
        return ""
    if relative_parts and relative_parts[0] in SUPPORTED_DATASETS:
        return relative_parts[0]
    return ""


def discover_dataset_samples(
    input_dir: Path,
    dataset_names: list[str] | None = None,
    sample_names: list[str] | None = None,
) -> list[CheckedSrsSample]:
    selected = dataset_names or []
    if not selected:
        return discover_checked_srs(input_dir, sample_names)

    samples: list[CheckedSrsSample] = []
    for dataset_name in selected:
        dataset_dir = input_dir / dataset_name
        for sample in discover_checked_srs(dataset_dir, sample_names):
            samples.append(
                CheckedSrsSample(
                    project_name=sample.project_name,
                    srs_path=sample.srs_path,
                    dataset_name=dataset_name,
                )
            )
    return samples


def build_prompt(srs_text: str) -> str:
    return f"""You are an experienced software architect.

Task: Generate a system architecture diagram directly from the provided Software Requirements Specification (SRS).

Return ONLY PlantUML source. Begin with @startuml and end with @enduml. Do not wrap the answer in Markdown fences and do not add explanations. Do not generate sequence, class, or use-case diagrams.

SRS:

{srs_text.strip()}
"""


def extract_plantuml(raw_response: str) -> str:
    fenced = re.search(r"```(?:plantuml|puml|uml)?\s*(.*?)\s*```", raw_response, re.DOTALL | re.IGNORECASE)
    if fenced:
        return ensure_plantuml_markers(fenced.group(1))

    embedded = re.search(r"(@startuml.*?@enduml)", raw_response, re.DOTALL | re.IGNORECASE)
    if embedded:
        return embedded.group(1).strip()

    return ""


def ensure_plantuml_markers(content: str) -> str:
    puml = content.strip()
    if not puml:
        return ""
    if not re.search(r"^\s*@startuml\b", puml, re.IGNORECASE):
        puml = "@startuml\n" + puml
    if not re.search(r"@enduml\s*$", puml, re.IGNORECASE):
        puml = puml + "\n@enduml"
    return puml.strip()


def call_openai_chat(
    prompt: str,
    *,
    api_key: str,
    model: str,
    api_url: str,
    temperature: float,
    timeout: int,
    retries: int,
    retry_backoff: float,
) -> str:
    endpoint = normalize_chat_completions_url(api_url)
    payload = {
        "model": model,
        "temperature": temperature,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You generate PlantUML software architecture diagrams from requirements. "
                    "Return only PlantUML source."
                ),
            },
            {"role": "user", "content": prompt},
        ],
    }
    request = urllib.request.Request(
        endpoint,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "User-Agent": "r2abench-checked-srs-baseline",
        },
        method="POST",
    )

    raw = ""
    for attempt in range(retries + 1):
        try:
            with open_llm_request(request, timeout=normalize_timeout(timeout)) as response:
                raw = response.read().decode("utf-8", errors="replace")
            break
        except Exception as exc:
            if attempt >= retries or not is_retryable_llm_error(exc):
                raise RuntimeError(format_llm_error(exc, endpoint)) from exc
            delay = retry_backoff * (attempt + 1)
            print(
                f"LLM request failed ({retry_error_summary(exc)}); "
                f"retrying {attempt + 2}/{retries + 1} in {delay:.1f}s.",
                file=sys.stderr,
                flush=True,
            )
            if delay > 0:
                time.sleep(delay)

    response_data = json.loads(raw)
    return str(response_data["choices"][0]["message"]["content"]).strip()


def generate_one(
    *,
    sample: CheckedSrsSample,
    output_base_dir: Path,
    client: LlmClient,
    api_key: str,
    model: str,
    api_url: str,
    temperature: float,
    timeout: int,
    retries: int,
    retry_backoff: float,
    force: bool,
    include_dataset_in_output: bool = False,
) -> GenerationResult:
    output_dir = output_base_dir
    if include_dataset_in_output and sample.dataset_name:
        output_dir = output_dir / sample.dataset_name
    output_dir = output_dir / sample.project_name
    predicted_path = output_dir / "predicted.puml"
    if predicted_path.exists() and not force:
        return GenerationResult(
            project_name=sample.project_name,
            status="skipped",
            output_dir=output_dir,
            predicted_path=predicted_path,
            message="predicted.puml already exists",
        )

    srs_text = sample.srs_path.read_text(encoding="utf-8")
    prompt = build_prompt(srs_text)
    raw_response = client(
        prompt,
        api_key=api_key,
        model=model,
        api_url=api_url,
        temperature=temperature,
        timeout=timeout,
        retries=retries,
        retry_backoff=retry_backoff,
    )

    puml = extract_plantuml(raw_response)
    if not puml:
        raise RuntimeError(f"No PlantUML block found in model response for {sample.project_name}.")

    output_dir.mkdir(parents=True, exist_ok=True)
    predicted_path.write_text(puml.rstrip() + "\n", encoding="utf-8")
    return GenerationResult(
        project_name=sample.project_name,
        status="generated",
        output_dir=output_dir,
        predicted_path=predicted_path,
    )


def require_llm_config(api_key: str, model: str, api_url: str) -> None:
    missing = []
    if not api_key:
        missing.append("API_KEY, OPENAI_API_KEY, or --llm-api-key")
    if not model:
        missing.append("OPENAI_MODEL or --llm-model")
    if not api_url:
        missing.append("OPENAI_API_URL or --llm-api-url")
    if missing:
        raise RuntimeError("Missing LLM configuration: " + ", ".join(missing))


def resolve_llm_config(args: argparse.Namespace) -> tuple[str, str]:
    api_key = API_KEY or args.llm_api_key or os.getenv("OPENAI_API_KEY", "")
    model = args.llm_model or os.getenv("OPENAI_MODEL", DEFAULT_LLM_MODEL)
    return api_key, model


def read_http_error_body(exc: urllib.error.HTTPError, max_chars: int = 500) -> str:
    if not exc.fp:
        return ""
    raw = exc.fp.read(max_chars + 1)
    text = raw.decode("utf-8", errors="replace") if isinstance(raw, bytes) else str(raw)
    text = " ".join(text.split())
    if len(text) > max_chars:
        return text[:max_chars].rstrip() + "..."
    return text


def format_llm_error(exc: Exception, api_url: str) -> str:
    if isinstance(exc, urllib.error.HTTPError):
        status = f"HTTP {exc.code} {exc.msg}".strip()
        parts = [f"LLM API request failed: {status} for {api_url}."]
        location = exc.headers.get("Location") if exc.headers else ""
        if 300 <= exc.code < 400:
            parts.append(f"The endpoint redirected to {location or 'another URL'}.")
        elif exc.code == 405:
            parts.append("The endpoint does not accept POST requests.")
        body = read_http_error_body(exc)
        if body:
            parts.append(f"Response body: {body}")
        return " ".join(parts)
    return f"LLM API request failed for {api_url}: {exc}"


def is_retryable_llm_error(exc: Exception) -> bool:
    if isinstance(exc, urllib.error.HTTPError):
        return exc.code in {408, 409, 425, 429, 500, 502, 503, 504} or 520 <= exc.code <= 599
    if isinstance(exc, http.client.RemoteDisconnected):
        return True
    if isinstance(exc, (TimeoutError, urllib.error.URLError)):
        return True
    message = str(exc).lower()
    return (
        "timeout" in message
        or "temporarily unavailable" in message
        or "remote end closed connection" in message
    )


def retry_error_summary(exc: Exception) -> str:
    if isinstance(exc, urllib.error.HTTPError):
        summary = f"HTTP {exc.code} {exc.msg}".strip()
        location = exc.headers.get("Location") if exc.headers else ""
        if location:
            summary = f"{summary}, Location={location}"
        return summary
    return f"{type(exc).__name__}: {exc}"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run a direct checked_srs.md -> PlantUML architecture baseline over R2ABench-style folders."
    )
    parser.add_argument(
        "--input-dir",
        type=Path,
        default=DEFAULT_INPUT_DIR,
        help="Directory to scan recursively for checked_srs.md files.",
    )
    parser.add_argument(
        "--output-root",
        type=Path,
        default=None,
        help="Root directory for baseline outputs. Defaults to runs/direct/<model>.",
    )
    parser.add_argument(
        "--run-name",
        default="",
        help="Optional output run folder name under the model directory. Defaults to no extra run folder.",
    )
    parser.add_argument(
        "--dataset",
        action="append",
        choices=SUPPORTED_DATASETS,
        default=[],
        help="Dataset collection to generate. Use G-R2A or E-R2A. Can be passed more than once. Defaults to all.",
    )
    parser.add_argument(
        "--sample",
        action="append",
        default=[],
        help="Project/sample folder name to run. Can be passed multiple times. Defaults to all.",
    )
    parser.add_argument("--force", action="store_true", help="Overwrite existing predicted.puml files.")
    parser.add_argument("--dry-run", action="store_true", help="List discovered samples and target paths without calling the LLM.")
    parser.add_argument("--stop-on-error", action="store_true", help="Stop at the first failed sample.")
    parser.add_argument("--llm-api-key", default="", help="LLM API key. Defaults to API_KEY, then OPENAI_API_KEY.")
    parser.add_argument("--llm-model", default="", help=f"LLM model. Defaults to OPENAI_MODEL or {DEFAULT_LLM_MODEL}.")
    parser.add_argument(
        "--llm-api-url",
        default=os.getenv("OPENAI_API_URL", DEFAULT_LLM_API_URL),
        help="OpenAI-compatible base URL or chat completions endpoint.",
    )
    parser.add_argument("--temperature", type=float, default=0.0, help="LLM temperature.")
    parser.add_argument("--timeout", type=int, default=600, help="Network timeout in seconds. Use 0 to wait indefinitely.")
    parser.add_argument("--retries", type=int, default=3, help="Retry count for transient LLM API errors.")
    parser.add_argument("--retry-backoff", type=float, default=8.0, help="Retry backoff seconds multiplied by attempt.")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    api_key, model = resolve_llm_config(args)
    dataset_names = list(dict.fromkeys(args.dataset))
    output_root = args.output_root or (DEFAULT_OUTPUT_ROOT / sanitize_for_path(model))
    output_base_dir = output_root / args.run_name if args.run_name else output_root
    samples = discover_dataset_samples(args.input_dir, dataset_names=dataset_names, sample_names=args.sample)
    include_dataset_in_output = len(dataset_names) != 1

    if not samples:
        selection = ", ".join(dataset_names) if dataset_names else "all datasets"
        raise RuntimeError(f"No checked_srs.md files found in {args.input_dir} for {selection}.")

    if args.dry_run:
        for sample in samples:
            target_dir = output_base_dir
            if include_dataset_in_output and sample.dataset_name:
                target_dir = target_dir / sample.dataset_name
            target_path = target_dir / sample.project_name / "predicted.puml"
            print(f"{sample.dataset_name or '-'}\t{sample.project_name}\t{sample.srs_path}\t{target_path}")
        return 0

    require_llm_config(api_key, model, args.llm_api_url)

    failures = 0
    for index, sample in enumerate(samples, start=1):
        print(f"[{index}/{len(samples)}] {sample.project_name}")
        try:
            result = generate_one(
                sample=sample,
                output_base_dir=output_base_dir,
                client=call_openai_chat,
                api_key=api_key,
                model=model,
                api_url=args.llm_api_url,
                temperature=args.temperature,
                timeout=args.timeout,
                retries=args.retries,
                retry_backoff=args.retry_backoff,
                force=args.force,
                include_dataset_in_output=include_dataset_in_output,
            )
            print(f"  {result.status}: {result.predicted_path}")
        except Exception as exc:
            failures += 1
            print(f"  failed: {exc}", file=sys.stderr)
            if args.stop_on_error:
                break

    if failures:
        print(f"Completed with {failures} failed sample(s).", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except RuntimeError as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise SystemExit(2)
