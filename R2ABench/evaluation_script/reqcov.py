"""Curated requirement loading and deterministic validation of ReqCov judgments."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List, Optional


REQCOV_VERSION = "reqcov-main-responsibility-v1"
PROMPT_PATH = Path(__file__).with_name("reqcov_prompt.txt")


def empty_reqcov_result(status: str) -> Dict[str, object]:
    return {
        "l2_requirement_coverage": None,
        "l2_requirement_coverage_percent": None,
        "l2_requirement_coverage_status": status,
        "l2_requirement_coverage_error": None,
        "l2_requirement_coverage_version": REQCOV_VERSION,
        "l2_requirement_count": None,
        "l2_covered_requirement_count": None,
        "l2_requirement_assessments_json": None,
        "l2_requirement_coverage_raw_response": None,
        "l2_input_signature": None,
    }


def _unique_json_keys(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def load_curated_requirements(path: Optional[Path]) -> List[Dict[str, object]]:
    """Every nonblank JSONL record is one evaluation unit; never infer/filter items."""
    if path is None:
        raise FileNotFoundError("No project req_final.jsonl path was resolved")
    text = Path(path).read_text(encoding="utf-8-sig")
    items: List[Dict[str, object]] = []
    seen = set()
    for line_number, line in enumerate(text.splitlines(), start=1):
        if not line.strip():
            continue
        try:
            item = json.loads(line, object_pairs_hook=_unique_json_keys)
        except ValueError as exc:
            raise ValueError(f"req_final.jsonl line {line_number}: {exc}") from exc
        if not isinstance(item, dict):
            raise ValueError(f"req_final.jsonl line {line_number}: expected an object")
        for field in ("req_id", "requirement"):
            if not isinstance(item.get(field), str) or not item[field].strip():
                raise ValueError(f"req_final.jsonl line {line_number}: {field} must be a nonempty string")
        if item["req_id"] in seen:
            raise ValueError(f"req_final.jsonl line {line_number}: duplicate req_id {item['req_id']}")
        seen.add(item["req_id"])
        items.append(item)
    if not items:
        raise ValueError("req_final.jsonl contains no requirement items")
    return items


def build_reqcov_prompt(
    items: List[Dict[str, object]], predicted_puml: str, requirements_text: str,
) -> str:
    instructions = PROMPT_PATH.read_text(encoding="utf-8")
    jsonl = "\n".join(json.dumps(item, ensure_ascii=False) for item in items)
    return (
        instructions
        + f"\n\n<REQ_FINAL_JSONL>\n{jsonl}\n</REQ_FINAL_JSONL>"
        + f"\n\n<GENERATED_PLANTUML>\n{predicted_puml}\n</GENERATED_PLANTUML>"
        + f"\n\n<SRS_CONTEXT>\n{requirements_text}\n</SRS_CONTEXT>\n"
    )


def validate_reqcov_assessments(
    parsed: object, items: List[Dict[str, object]], predicted_puml: str,
) -> Dict[str, object]:
    """Validate identities and quoted evidence, then calculate both ratio and percent.

    Evidence validation checks quote provenance, not semantic correctness; the
    latter remains a judge decision requiring calibration.
    """
    if not isinstance(parsed, dict) or not isinstance(parsed.get("requirement_assessments"), list):
        raise ValueError("Expected a requirement_assessments array")
    assessments = parsed["requirement_assessments"]
    expected_ids = [item["req_id"] for item in items]
    if not expected_ids or len(set(expected_ids)) != len(expected_ids):
        raise ValueError("Expected a nonempty curated set with unique req_id values")
    if len(assessments) != len(expected_ids):
        raise ValueError(f"Expected {len(expected_ids)} assessments, received {len(assessments)}")
    expected = set(expected_ids)
    by_id = {}
    normalized_puml = predicted_puml.replace("\r\n", "\n").replace("\r", "\n")
    for assessment in assessments:
        if not isinstance(assessment, dict):
            raise ValueError("Every assessment must be an object")
        req_id = assessment.get("req_id")
        if not isinstance(req_id, str) or req_id not in expected:
            raise ValueError(f"Unknown req_id: {req_id!r}")
        if req_id in by_id:
            raise ValueError(f"Duplicate assessment for {req_id}")
        covered = assessment.get("covered")
        if type(covered) is not int or covered not in (0, 1):
            raise ValueError(f"{req_id}: covered must be integer 0 or 1")
        for field in ("main_responsibility", "reason"):
            if not isinstance(assessment.get(field), str) or not assessment[field].strip():
                raise ValueError(f"{req_id}: {field} must be a nonempty string")
        evidence = assessment.get("evidence")
        if not isinstance(evidence, list) or (covered == 1 and not evidence):
            raise ValueError(f"{req_id}: evidence must be an array, nonempty for covered=1")
        for quote in evidence:
            if not isinstance(quote, str) or not quote.strip():
                raise ValueError(f"{req_id}: evidence excerpts must be nonempty strings")
            normalized_quote = quote.replace("\r\n", "\n").replace("\r", "\n")
            if normalized_quote not in normalized_puml:
                raise ValueError(f"{req_id}: evidence excerpt not found in generated PlantUML")
        by_id[req_id] = {
            "req_id": req_id,
            "main_responsibility": assessment["main_responsibility"],
            "covered": covered,
            "evidence": evidence,
            "reason": assessment["reason"],
        }
    ordered = [by_id[req_id] for req_id in expected_ids]
    count = sum(item["covered"] for item in ordered)
    return {
        "l2_requirement_coverage_status": "completed",
        "l2_requirement_coverage": count / len(items),
        "l2_requirement_coverage_percent": 100.0 * count / len(items),
        "l2_requirement_count": len(items),
        "l2_covered_requirement_count": count,
        "l2_requirement_assessments_json": json.dumps(ordered, ensure_ascii=False),
    }
