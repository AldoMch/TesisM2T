from __future__ import annotations

import hashlib
import json
import math
import os
import re
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Optional

from .reqcov import (
    REQCOV_VERSION,
    build_reqcov_prompt,
    empty_reqcov_result,
    load_curated_requirements,
    validate_reqcov_assessments,
)


L2_DIMENSIONS = [
    "completeness",
    "faithfulness",
    "architectural_rationality",
    "traceability",
    "readability",
]


@dataclass
class L2JudgeConfig:
    enabled: bool = False
    model: str = "gemini-2.5-pro"
    base_url: str = ""
    api_key: Optional[str] = None
    timeout_seconds: int = 600

    @classmethod
    def from_env(
        cls,
        enabled: bool = False,
        model: Optional[str] = None,
        base_url: Optional[str] = None,
        api_key_env: str = "OPENAI_API_KEY",
    ) -> "L2JudgeConfig":
        return cls(
            enabled=enabled,
            model=model or os.environ.get("OPENAI_MODEL", "gemini-2.5-pro"),
            base_url=(base_url or os.environ.get("OPENAI_BASE_URL", "")).rstrip("/"),
            api_key=os.environ.get(api_key_env),
        )


def empty_l2_result(status: str) -> Dict[str, object]:
    result: Dict[str, object] = {"l2_status": status}
    for dimension in L2_DIMENSIONS:
        result[f"l2_{dimension}_score"] = None
        result[f"l2_{dimension}_reasoning"] = None
    result.update(
        {
            "l2_asr_coverage": None,
            "l2_unsupported_inference_rate": None,
            "l2_raw_json": None,
            "l2_raw_response": None,
            "l2_normalized_json": None,
            "l2_format_repaired": False,
            "l2_error": None,
        }
    )
    result.update(empty_reqcov_result(status))
    return result


def evaluate_l2(
    requirements_text: Optional[str], predicted_puml: str, config: L2JudgeConfig,
    *, reqcov_requirements_path: Optional[Path] = None,
) -> Dict[str, object]:
    if not config.enabled:
        return empty_l2_result("skipped_disabled")
    if not config.api_key:
        return empty_l2_result("skipped_missing_api_key")
    if not requirements_text:
        return empty_l2_result("skipped_missing_requirements")

    prompt = _build_prompt(requirements_text, predicted_puml)
    raw = None
    try:
        raw = _chat_completion(prompt, config)
        parsed = _parse_json(raw)
        if not isinstance(parsed, dict):
            raise ValueError("L2 response must be a JSON object")
        result = _flatten_l2(parsed)
    except Exception as exc:  # noqa: BLE001 - surfaced in CSV for batch runs.
        result = empty_l2_result("failed")
        result["l2_error"] = str(exc)
    result["l2_raw_response"] = raw

    # ReqCov uses its own prompt so holistic scoring/traceability rules cannot
    # silently redefine the curated coverage units or the coverage criterion.
    coverage = _evaluate_reqcov(requirements_text, predicted_puml, config, reqcov_requirements_path)
    result.update(coverage)
    if result["l2_status"] == "completed" and coverage["l2_requirement_coverage_status"] != "completed":
        result["l2_status"] = "completed_with_reqcov_error"
    return result


def _evaluate_reqcov(requirements_text, predicted_puml, config, path):
    result = empty_reqcov_result("failed_invalid_req_final")
    try:
        items = load_curated_requirements(path)
    except FileNotFoundError as exc:
        result["l2_requirement_coverage_status"] = "skipped_missing_req_final"
        result["l2_requirement_coverage_error"] = str(exc)
        return result
    except (OSError, ValueError) as exc:
        result["l2_requirement_coverage_error"] = str(exc)
        return result

    result["l2_requirement_count"] = len(items)
    try:
        prompt = build_reqcov_prompt(items, predicted_puml, requirements_text)
        result["l2_input_signature"] = _input_signature(requirements_text, predicted_puml, items, config)
        raw = _chat_completion(prompt, config)
    except Exception as exc:  # noqa: BLE001 - preserve holistic scores on coverage failure.
        result["l2_requirement_coverage_status"] = "failed_judge"
        result["l2_requirement_coverage_error"] = str(exc)
        return result
    result["l2_requirement_coverage_raw_response"] = raw
    try:
        parsed = _parse_json(raw)
        result.update(validate_reqcov_assessments(parsed, items, predicted_puml))
    except ValueError as exc:
        result["l2_requirement_coverage_status"] = "failed_validation"
        result["l2_requirement_coverage_error"] = str(exc)
    return result


def _input_signature(requirements_text, predicted_puml, items, config):
    payload = {
        "reqcov_version": REQCOV_VERSION,
        "model": config.model,
        "base_url": config.base_url.rstrip("/"),
        "semantic_prompt": _build_prompt(requirements_text, predicted_puml),
        "reqcov_prompt": build_reqcov_prompt(items, predicted_puml, requirements_text),
    }
    return hashlib.sha256(json.dumps(payload, ensure_ascii=False, sort_keys=True).encode("utf-8")).hexdigest()


def l2_resume_is_current(row, requirements_text, predicted_puml, config, reqcov_requirements_path):
    """Never reuse legacy estimates, failed judgments, or results for changed inputs."""
    if (
        row.get("l2_status") != "completed"
        or row.get("l2_requirement_coverage_status") != "completed"
        or row.get("l2_requirement_coverage_version") != REQCOV_VERSION
        or not requirements_text
    ):
        return False
    try:
        _validate_l2_scores({"scores": {
            dimension: {"score": row.get(f"l2_{dimension}_score"),
                        "reasoning": row.get(f"l2_{dimension}_reasoning")}
            for dimension in L2_DIMENSIONS
        }})
        items = load_curated_requirements(reqcov_requirements_path)
        return row.get("l2_input_signature") == _input_signature(requirements_text, predicted_puml, items, config)
    except (OSError, ValueError):
        return False


def _build_prompt(requirements_text: str, predicted_puml: str) -> str:
    return f"""You are a senior software architect and an impartial evaluator.

Evaluate the generated architecture diagram using an ATAM-inspired protocol.
Focus on requirements-to-architecture reasoning, ASR coverage, traceability,
and unsupported inferences. Do not reward visual similarity to a reference
diagram.
Before scoring, list concrete defects in the relevant reasoning fields. If no
concrete evidence supports an architectural element, penalize faithfulness and
traceability.

Return strict JSON only, with this schema:
{{
  "scores": {{
    "completeness": {{"score": 1, "reasoning": "..."}},
    "faithfulness": {{"score": 1, "reasoning": "..."}},
    "architectural_rationality": {{"score": 1, "reasoning": "..."}},
    "traceability": {{"score": 1, "reasoning": "..."}},
    "readability": {{"score": 1, "reasoning": "..."}}
  }},
  "metrics": {{
    "asr_coverage": 0.0,
    "unsupported_inference_rate": 0.0
  }}
}}

Do not estimate or return requirement_coverage. ReqCov is calculated separately
from item-level judgments over the project's curated req_final.jsonl. The rules
below apply to the holistic dimensions, not to that separate coverage decision.

Use the full 1--5 scale strictly. Scores must be integers. Before assigning
each score, identify concrete defects in that dimension; if the reasoning
does not name specific evidence from the requirements and diagram, do not
assign a 5.

General scoring rubric for every dimension:
- 5: Strong. No major missing requirements, no incorrect architectural
  boundaries, no unsupported components or relations, and trace IDs/evidence
  links are all verifiable against the requirements.
- 4: Good. Only minor omissions, minor ambiguity, or a small number of
  unsupported inferences; the main architecture remains evidence-supported.
- 3: Partially acceptable. The diagram covers the main requirements, but has
  clear omissions, boundary mistakes, weak traceability, or several unsupported
  assumptions.
- 2: Weak. Multiple important requirements are missing, architectural
  relations or deployment/runtime boundaries are often wrong, or many elements
  are unsupported by the requirements.
- 1: Poor. The diagram is largely inconsistent with the requirements, models a
  different system, or provides little usable requirements-to-architecture
  reasoning.

Apply these additional dimension-specific checks:
- Completeness: penalize missing functional requirements, quality drivers,
  ASRs, external systems, data stores, or deployment/runtime concerns that are
  explicit in the requirements.
- Faithfulness: penalize components, technologies, relations, protocols,
  constraints, or assumptions that are not supported by the requirements, even
  if they look plausible.
- Architectural rationality: penalize incorrect abstraction level, misplaced
  responsibilities, wrong dependencies, poor separation of concerns, or
  architecture decisions that do not address quality attributes.
- Traceability: verify that cited requirement IDs actually exist and support
  the linked element. Penalize hallucinated IDs, vague trace labels, and
  elements without evidence.
- Readability: penalize clutter, misleading grouping, inconsistent notation,
  ambiguous labels, overly flat diagrams, and diagrams that are syntactically
  valid but hard to audit.

<REQUIREMENTS>
{requirements_text}
</REQUIREMENTS>

<PREDICTED_PLANTUML>
{predicted_puml}
</PREDICTED_PLANTUML>
"""


def _chat_completion(prompt: str, config: L2JudgeConfig) -> str:
    if not config.base_url:
        raise ValueError("Missing judge endpoint: configure OPENAI_BASE_URL or base_url")
    payload = {
        "model": config.model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0,
        "max_tokens": 16000,
        "response_format": {"type": "json_object"},
    }
    # The Momenta gateway supports GLM's explicit thinking control. Keep the
    # request focused on the JSON judgment so hidden reasoning is not returned
    # in the model content or charged as part of the visible result.
    if os.environ.get("L2_DISABLE_THINKING", "1").strip().lower() not in {"0", "false", "no", "off"}:
        payload["thinking"] = {"type": "disabled"}
    data = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        f"{config.base_url}/chat/completions",
        data=data,
        headers={
            "Authorization": f"Bearer {config.api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=config.timeout_seconds) as response:
            body = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"judge request failed: {exc.code} {detail}") from exc
    return body["choices"][0]["message"]["content"]


def _parse_json(raw: str) -> Dict[str, object]:
    if not isinstance(raw, str):
        raise ValueError("Judge response content must be a JSON string")
    match = re.search(r"```(?:json)?\s*(.*?)\s*```", raw, flags=re.DOTALL | re.IGNORECASE)
    text = (match.group(1) if match else raw).lstrip("\ufeff").strip()

    def unique_keys(pairs):
        result = {}
        for name, value in pairs:
            if name in result:
                raise ValueError(f"Duplicate JSON key: {name}")
            result[name] = value
        return result

    return json.loads(text, object_pairs_hook=unique_keys)


def _score_integer(value):
    """Convert an unambiguous 1--5 numeric representation; never round a score."""
    if isinstance(value, str) and re.fullmatch(r"[1-5](?:\.0+)?", value.strip()):
        return int(float(value))
    if type(value) in (int, float) and math.isfinite(value) and value == int(value) and 1 <= value <= 5:
        return int(value)
    raise ValueError("score must be an integer from 1 through 5")


def _normalize_l2_response(parsed):
    """Recover known dimensions misplaced at the root or inside other dimensions.

    Only traverse rubric fields, not arbitrary objects such as examples or risks.
    Conflicting occurrences are ambiguous and must never be selected silently.
    """
    if not isinstance(parsed, dict):
        raise ValueError("L2 response must be a JSON object")
    scores, metrics = {}, {}

    def remember(target, name, value):
        if name in target and target[name] != value:
            raise ValueError(f"Conflicting L2 values for {name}")
        target[name] = value

    def visit(node, depth=0):
        if depth > 20:
            raise ValueError("L2 response nesting is too deep")
        for name, value in node.items():
            if name == "scores":
                if not isinstance(value, dict):
                    raise ValueError("L2 scores must be an object")
                visit(value, depth + 1)
            elif name in L2_DIMENSIONS:
                if not isinstance(value, dict):
                    raise ValueError(f"L2 {name} must be an object")
                item = {k: v for k, v in value.items() if k not in {*L2_DIMENSIONS, "scores", "metrics"}}
                if "score" in item:
                    try:
                        item["score"] = _score_integer(item["score"])
                    except ValueError as exc:
                        raise ValueError(f"{name}: {exc}") from exc
                remember(scores, name, item)
                visit(value, depth + 1)
            elif name == "metrics":
                if not isinstance(value, dict):
                    raise ValueError("L2 metrics must be an object")
                for metric, number in value.items():
                    remember(metrics, metric, number)

    visit(parsed)
    normalized = {k: v for k, v in parsed.items() if k not in {*L2_DIMENSIONS, "scores", "metrics"}}
    normalized["scores"] = scores
    if metrics:
        normalized["metrics"] = metrics
    return normalized


def _validate_l2_scores(parsed):
    """Require every dimension and its evidence before reporting completion."""
    scores = parsed.get("scores", {})
    errors = []
    for dimension in L2_DIMENSIONS:
        item = scores.get(dimension) if isinstance(scores, dict) else None
        if not isinstance(item, dict):
            errors.append(f"Missing dimension {dimension}")
            continue
        try:
            _score_integer(item.get("score"))
        except ValueError:
            errors.append(f"Invalid score for {dimension}")
        if not isinstance(item.get("reasoning"), str) or not item["reasoning"].strip():
            errors.append(f"Missing reasoning for {dimension}")
    if errors:
        raise ValueError("; ".join(errors))


def _flatten_l2(parsed: Dict[str, object]) -> Dict[str, object]:
    normalized = _normalize_l2_response(parsed)
    result = empty_l2_result("completed")
    scores = normalized["scores"]
    for dimension in L2_DIMENSIONS:
        item = scores.get(dimension, {}) if isinstance(scores, dict) else {}
        if isinstance(item, dict):
            result[f"l2_{dimension}_score"] = item.get("score")
            result[f"l2_{dimension}_reasoning"] = item.get("reasoning")

    metrics = normalized.get("metrics", {})
    if isinstance(metrics, dict):
        result["l2_asr_coverage"] = metrics.get("asr_coverage")
        result["l2_unsupported_inference_rate"] = metrics.get("unsupported_inference_rate")

    result["l2_raw_json"] = json.dumps(parsed, ensure_ascii=False)
    result["l2_normalized_json"] = json.dumps(normalized, ensure_ascii=False)
    result["l2_format_repaired"] = normalized != parsed
    try:
        _validate_l2_scores(normalized)
    except ValueError as exc:
        result["l2_status"] = "failed"
        result["l2_error"] = str(exc)
    return result
