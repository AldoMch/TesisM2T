#!/usr/bin/env python3
from __future__ import annotations

import argparse
import asyncio
import json
import os
import re
import sys
from pathlib import Path
from typing import Awaitable, Callable


DEFAULT_OUTPUT_DIR = Path("runs") / "E-R2A" / "metagpt-custom"


def sanitize_for_path(value: str) -> str:
    safe = re.sub(r'[<>:"/\\|?*\s]+', "_", value.strip())
    safe = safe.strip("._")
    return safe or "metagpt_custom"


def ensure_plantuml_markers(content: str) -> str:
    puml = content.strip()
    if not puml:
        return ""
    if not re.search(r"^\s*@startuml\b", puml, re.IGNORECASE):
        puml = "@startuml\n" + puml
    if not re.search(r"@enduml\s*$", puml, re.IGNORECASE):
        puml = puml + "\n@enduml"
    return puml.strip()


def extract_plantuml(text: str) -> str:
    fenced = re.search(r"```(?:plantuml|puml|uml)\s*(.*?)\s*```", text, re.DOTALL | re.IGNORECASE)
    if fenced:
        return ensure_plantuml_markers(fenced.group(1))

    embedded = re.search(r"(?ms)^\s*(@startuml\b.*?^\s*@enduml\b\s*)$", text, re.IGNORECASE)
    if embedded:
        return embedded.group(1).strip()

    return ""


def build_stage_prompts(
    prd_text: str,
    *,
    plan: str = "",
    draft_puml: str = "",
    review: str = "",
) -> dict[str, str]:
    return {
        "analyze": f"""You are a PRD Analyst. Read the following PRD/SRS and extract a structured architecture plan.

Output Markdown with exactly these sections:
## System Scope
(one sentence)

## Layers
- Layer name: description

## Core Components
- ComponentName (layer): responsibility

## Key Dependencies
- ComponentA -> ComponentB: reason

## External Systems
- system name

Use only facts from the PRD/SRS and clearly mark necessary architecture inferences as inferred.

PRD/SRS:
{prd_text}
""",
        "draft": f"""You are a Software Architect. Using the architecture plan below, generate a layered PlantUML component/deployment diagram.

Rules:
1. Use ONLY PlantUML component/deployment syntax: package, component, node, database, cloud, interface, and arrows.
2. Do NOT write implementation code, source files, APIs, tests, Mermaid, sequence diagrams, use-case diagrams, or class diagrams.
3. Group components into architecture layers using package or node blocks.
4. Keep the diagram architecture-level: components, services, stores, gateways, external systems, and major dependencies.
5. Output ONLY PlantUML inside ```plantuml ... ``` with @startuml and @enduml.

Architecture Plan:
{plan or prd_text}
""",
        "review": f"""You are an Architecture Reviewer. Review the draft PlantUML diagram against the original PRD/SRS.

List concrete issues in these categories:
- MISSING: components/layers present in PRD/SRS but absent in diagram
- HALLUCINATED: components in diagram not supported by PRD/SRS
- DEPENDENCY_ERROR: wrong or missing connections
- SYNTAX_ISSUE: PlantUML syntax problems

If no issues, write LGTM.

PRD/SRS:
{prd_text}

Draft PlantUML:
{draft_puml}
""",
        "refine": f"""You are an Architecture Refiner. Apply the reviewer's feedback to fix the draft PlantUML diagram.

Rules:
1. Use ONLY PlantUML component/deployment syntax.
2. Do NOT write implementation code, source files, APIs, tests, Mermaid, sequence diagrams, use-case diagrams, or class diagrams.
3. Output ONLY the final PlantUML inside ```plantuml ... ```.
4. Must include @startuml and @enduml.

Draft PlantUML:
{draft_puml}

Reviewer Feedback:
{review}
""",
        "direct": f"""You are an experienced software architect.
Generate a layered PlantUML component/deployment diagram directly from the PRD/SRS.

Rules:
1. Use ONLY PlantUML component/deployment syntax: package, component, node, database, cloud, interface, and arrows.
2. Do NOT write implementation code, source files, APIs, tests, Mermaid, sequence diagrams, use-case diagrams, or class diagrams.
3. Output ONLY PlantUML inside ```plantuml ... ```.
4. Must include @startuml and @enduml.

PRD/SRS:
{prd_text}
""",
    }


async def ask_with_retry(
    step_name: str,
    ask_fn: Callable[[], Awaitable[str]],
    retries: int,
) -> str:
    for idx in range(retries):
        try:
            output = await ask_fn()
        except Exception as exc:
            print(f"    [{step_name}] exception: {exc}", flush=True)
            output = ""
        if output and output.strip():
            return output
        if idx < retries - 1:
            print(f"    [{step_name}] empty output, retry {idx + 2}/{retries}...", flush=True)
    return ""


async def run_pipeline(prd_text: str, retries: int) -> dict[str, str]:
    from metagpt.actions import Action

    class PromptAction(Action):
        name: str = "R2APromptAction"

        async def run(self, prompt: str) -> str:
            return await self.llm.aask(prompt, stream=False)

    prompts = build_stage_prompts(prd_text)

    print("    [1/4] PRDAnalyst analyzing PRD/SRS...", flush=True)
    plan = await ask_with_retry("PRDAnalyst", lambda: PromptAction().run(prompts["analyze"]), retries)

    print("    [2/4] Architect drafting PlantUML...", flush=True)
    draft_prompt = build_stage_prompts(prd_text, plan=plan)["draft"]
    draft = await ask_with_retry("Architect", lambda: PromptAction().run(draft_prompt), retries)
    draft_code = extract_plantuml(draft)

    if not draft_code:
        print("    [2.1/4] Draft had no PlantUML; using direct generation fallback...", flush=True)
        direct_prompt = build_stage_prompts(prd_text)["direct"]
        draft = await ask_with_retry("DirectDraft", lambda: PromptAction().run(direct_prompt), retries)
        draft_code = extract_plantuml(draft)

    print("    [3/4] Reviewer checking draft...", flush=True)
    if draft_code:
        review_prompt = build_stage_prompts(prd_text, draft_puml=draft_code)["review"]
        review = await ask_with_retry("Reviewer", lambda: PromptAction().run(review_prompt), retries)
    else:
        review = (
            "SYNTAX_ISSUE:\n"
            "- Draft is empty or invalid PlantUML. Regenerate a complete PlantUML architecture diagram."
        )

    print("    [4/4] Refiner producing final PlantUML...", flush=True)
    refine_prompt = build_stage_prompts(prd_text, draft_puml=draft_code or draft, review=review)["refine"]
    final = await ask_with_retry("Refiner", lambda: PromptAction().run(refine_prompt), retries)
    final_code = extract_plantuml(final)

    if not final_code and draft_code:
        print("    [4.1/4] Refiner had no PlantUML; falling back to Architect draft.", flush=True)
        final = draft
        final_code = draft_code

    if not final_code:
        print("    [4.2/4] Running final direct fallback...", flush=True)
        direct_prompt = build_stage_prompts(prd_text)["direct"]
        final = await ask_with_retry("DirectFinal", lambda: PromptAction().run(direct_prompt), retries)

    return {
        "plan": plan,
        "draft": draft,
        "review": review,
        "final": final,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run a customized MetaGPT Action-based R2A pipeline and save predicted.puml."
    )
    parser.add_argument("--srs", type=Path, required=True, help="Path to checked_srs.md or PRD/SRS markdown.")
    parser.add_argument("--output-dir", type=Path, default=None, help="Directory for raw_response.txt and predicted.puml.")
    parser.add_argument("--model-label", default="metagpt-custom", help="Label used in the default output path.")
    parser.add_argument("--setting-name", default="Setting_CustomMetaGPT", help="Recorded setting name.")
    parser.add_argument("--retries", type=int, default=3, help="Retries per stage when the model returns empty output.")
    parser.add_argument("--force", action="store_true", help="Overwrite an existing predicted.puml.")
    parser.add_argument("--dry-run", action="store_true", help="Write task/prompts metadata without calling MetaGPT.")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    srs_path = args.srs.resolve()
    if not srs_path.exists():
        raise FileNotFoundError(f"SRS file not found: {srs_path}")

    sample_name = srs_path.parent.name
    output_dir = args.output_dir
    if output_dir is None:
        output_dir = DEFAULT_OUTPUT_DIR / sanitize_for_path(args.model_label) / sample_name
    output_dir = output_dir.resolve()
    predicted_path = output_dir / "predicted.puml"
    raw_path = output_dir / "raw_response.txt"
    metadata_path = output_dir / "run_metadata.json"
    prompts_path = output_dir / "stage_prompts.json"

    if predicted_path.exists() and not args.force and not args.dry_run:
        print(f"skipped: {predicted_path} already exists")
        return 0

    output_dir.mkdir(parents=True, exist_ok=True)
    prd_text = srs_path.read_text(encoding="utf-8")
    prompts_path.write_text(json.dumps(build_stage_prompts(prd_text), indent=2, ensure_ascii=False), encoding="utf-8")

    metadata = {
        "sample_name": sample_name,
        "srs_path": str(srs_path),
        "output_dir": str(output_dir),
        "predicted_path": str(predicted_path),
        "model_label": args.model_label,
        "setting_name": args.setting_name,
        "pipeline": "MetaGPT Action pipeline: PRDAnalyst -> Architect -> Reviewer -> Refiner",
        "retries": args.retries,
        "dry_run": args.dry_run,
    }

    if args.dry_run:
        metadata_path.write_text(json.dumps(metadata, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"dry-run: wrote {prompts_path}")
        return 0

    print(f"[MetaGPT-custom] {sample_name}: PRDAnalyst -> Architect -> Reviewer -> Refiner", flush=True)
    stage_outputs = asyncio.run(run_pipeline(prd_text, retries=args.retries))
    raw_output = (
        "===== STAGE: PLAN =====\n"
        f"{stage_outputs.get('plan', '')}\n\n"
        "===== STAGE: DRAFT =====\n"
        f"{stage_outputs.get('draft', '')}\n\n"
        "===== STAGE: REVIEW =====\n"
        f"{stage_outputs.get('review', '')}\n\n"
        "===== STAGE: FINAL =====\n"
        f"{stage_outputs.get('final', '')}\n"
    )
    raw_path.write_text(raw_output, encoding="utf-8")

    final_puml = extract_plantuml(stage_outputs.get("final", ""))
    if not final_puml:
        final_puml = extract_plantuml(stage_outputs.get("draft", ""))

    metadata["plantuml_extracted"] = bool(final_puml.strip())
    metadata_path.write_text(json.dumps(metadata, indent=2, ensure_ascii=False), encoding="utf-8")

    if not final_puml.strip():
        print(f"failed: no valid PlantUML extracted. See {raw_path}", file=sys.stderr)
        return 1

    predicted_path.write_text(final_puml.rstrip() + "\n", encoding="utf-8")
    print(f"generated: {predicted_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
