from __future__ import annotations

import csv
import errno
import os
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Dict, Iterable, List, Optional

from .l0_syntax import evaluate_l0
from .l1_metrics import VERSION
from .l1_structural import L1AlignmentConfig, L1AlignmentError, evaluate_l1
from .l2_semantic import L2JudgeConfig, empty_l2_result, evaluate_l2, l2_resume_is_current


INTERNAL_OUTPUT_COLUMNS = {"pred_path", "gt_path", "requirements_path"}
RETIRED_OUTPUT_COLUMNS = {"l1_orphan_ratio"}
ProgressLogger = Callable[[str], None]
CSV_WRITE_MAX_ATTEMPTS = 5
CSV_WRITE_RETRY_DELAY_SECONDS = 0.2
CSV_WRITE_RETRY_ERRNOS = {errno.EINVAL, errno.EACCES, errno.EPERM}

CSV_COLUMNS = [
    "sample_id",
    "candidate_id",
    "workflow",
    "model_id",
    "project_language",
    "stage_status",
    "l0_valid",
    "l0_errors",
    "l0_warnings",
    "l0_node_count",
    "l0_edge_count",
    "l1_status",
    "l1_error",
    "l1_predicted_node_count",
    "l1_predicted_edge_count",
    "l1_reference_node_count",
    "l1_reference_edge_count",
    "l1_node_coverage",
    "l1_gen_precision",
    "l1_edge_precision",
    "l1_edge_recall",
    "l1_edge_f1",
    "l1_boundary_accuracy",
    "l1_structural_similarity",
    "l1_structural_discrepancy",
    "l1_structural_denominator",
    "l1_metric_version",
    "l1_god_ratio",
    "l1_matched_node_count",
    "l1_unmatched_predicted_node_count",
    "l1_unmatched_reference_node_count",
    "l2_status",
    "l2_completeness_score",
    "l2_faithfulness_score",
    "l2_architectural_rationality_score",
    "l2_traceability_score",
    "l2_readability_score",
    "l2_requirement_coverage",
    "l2_requirement_coverage_percent",
    "l2_requirement_coverage_status",
    "l2_requirement_coverage_error",
    "l2_requirement_coverage_version",
    "l2_requirement_count",
    "l2_covered_requirement_count",
    "l2_requirement_assessments_json",
    "l2_requirement_coverage_raw_response",
    "l2_input_signature",
    "l2_asr_coverage",
    "l2_unsupported_inference_rate",
    "l2_completeness_reasoning",
    "l2_faithfulness_reasoning",
    "l2_architectural_rationality_reasoning",
    "l2_traceability_reasoning",
    "l2_readability_reasoning",
    "l2_raw_json",
    "l2_raw_response",
    "l2_normalized_json",
    "l2_format_repaired",
    "l2_error",
]


@dataclass(frozen=True)
class DatasetSample:
    sample_id: str
    language: str
    project_dir: Path
    reference_path: Optional[Path]
    requirements_path: Optional[Path]
    reqcov_requirements_path: Optional[Path] = None


def evaluate_pair(
    pred_path: Path,
    gt_path: Optional[Path] = None,
    requirements_path: Optional[Path] = None,
    l2_config: Optional[L2JudgeConfig] = None,
    l1_config: Optional[L1AlignmentConfig] = None,
    *,
    reqcov_requirements_path: Optional[Path] = None,
    sample_id: Optional[str] = None,
    candidate_id: Optional[str] = None,
    workflow: Optional[str] = None,
    model_id: Optional[str] = None,
    project_language: Optional[str] = None,
    alignment_cache_path: Optional[Path] = None,
    progress_logger: Optional[ProgressLogger] = None,
    progress_index: Optional[int] = None,
    progress_total: Optional[int] = None,
) -> Dict[str, object]:
    pred_path = Path(pred_path)
    predicted_puml = pred_path.read_text(encoding="utf-8")
    row: Dict[str, object] = {
        "sample_id": sample_id or pred_path.stem,
        "candidate_id": candidate_id or (pred_path.parent.name if pred_path.parent.name else "candidate"),
        "workflow": workflow,
        "model_id": model_id,
        "project_language": project_language,
    }

    _log_progress(progress_logger, row, "sample", "start", progress_index, progress_total)
    _log_progress(progress_logger, row, "L0", "start", progress_index, progress_total)
    l0 = evaluate_l0(predicted_puml)
    row.update(
        {
            "l0_valid": l0.passed,
            "l0_errors": " | ".join(l0.errors),
            "l0_warnings": " | ".join(l0.warnings),
            "l0_node_count": l0.node_count,
            "l0_edge_count": l0.edge_count,
        }
    )
    if not l0.passed:
        row["stage_status"] = "failed_l0"
        row.update(_empty_l1_for_short_circuit())
        row.update(empty_l2_result("skipped_l0_failed"))
        _log_progress(
            progress_logger,
            row,
            "L0",
            "failed",
            progress_index,
            progress_total,
            detail=row["l0_errors"],
        )
        _log_progress(progress_logger, row, "sample", "failed_l0", progress_index, progress_total)
        return _ordered_row(row)

    _log_progress(
        progress_logger,
        row,
        "L0",
        "passed",
        progress_index,
        progress_total,
        detail=f"nodes={l0.node_count} edges={l0.edge_count}",
    )

    gt_text = Path(gt_path).read_text(encoding="utf-8") if gt_path else None
    requirements_text = Path(requirements_path).read_text(encoding="utf-8") if requirements_path else None
    l1_failed = False
    _log_progress(progress_logger, row, "L1", "start", progress_index, progress_total)
    try:
        row.update(
            evaluate_l1(
                predicted_puml,
                gt_text,
                requirements_text=requirements_text,
                alignment_config=l1_config,
                alignment_cache_path=alignment_cache_path,
            )
        )
        _log_progress(
            progress_logger,
            row,
            "L1",
            str(row.get("l1_status") or "completed"),
            progress_index,
            progress_total,
        )
    except L1AlignmentError as exc:
        _log_progress(progress_logger, row, "L1", "failed", progress_index, progress_total, detail=str(exc))
        if not (l1_config and l1_config.enabled):
            raise
        l1_failed = True
        row.update(_failed_l1_result(str(exc)))

    _log_progress(progress_logger, row, "L2", "start", progress_index, progress_total)
    if reqcov_requirements_path is None and requirements_path is not None:
        reqcov_requirements_path = Path(requirements_path).with_name("req_final.jsonl")
    row.update(evaluate_l2(
        requirements_text, predicted_puml, l2_config or L2JudgeConfig(),
        reqcov_requirements_path=reqcov_requirements_path,
    ))
    _log_progress(
        progress_logger,
        row,
        "L2",
        str(row.get("l2_status") or "completed"),
        progress_index,
        progress_total,
        detail=row.get("l2_error") or row.get("l2_requirement_coverage_error"),
    )
    row["stage_status"] = _completion_status(row, l1_failed)
    _log_progress(progress_logger, row, "sample", str(row["stage_status"]), progress_index, progress_total)
    return _ordered_row(row)


def _completion_status(row: Dict[str, object], l1_failed: bool) -> str:
    l2_failed = row.get("l2_status") in {"failed", "completed_with_reqcov_error"}
    if l1_failed and l2_failed:
        return "completed_with_l1_and_l2_error"
    if l1_failed:
        return "completed_with_l1_error"
    return "completed_with_l2_error" if l2_failed else "completed"


def evaluate_files(
    pred_paths: Iterable[Path],
    gt_dir: Optional[Path] = None,
    requirements_dir: Optional[Path] = None,
    l2_config: Optional[L2JudgeConfig] = None,
    l1_config: Optional[L1AlignmentConfig] = None,
    pred_root: Optional[Path] = None,
    dataset_dir: Optional[Path] = None,
    resume_rows: Optional[Iterable[Dict[str, object]]] = None,
    checkpoint_path: Optional[Path] = None,
    progress_logger: Optional[ProgressLogger] = None,
) -> List[Dict[str, object]]:
    rows = []
    gt_dir = Path(gt_dir) if gt_dir else None
    requirements_dir = Path(requirements_dir) if requirements_dir else None
    pred_root = Path(pred_root) if pred_root else None
    dataset_dir = Path(dataset_dir) if dataset_dir else None
    dataset_index = build_dataset_index(dataset_dir) if dataset_dir else {}
    pred_paths = list(pred_paths)
    total = len(pred_paths)
    resume_rows = list(resume_rows) if resume_rows else []
    resume_index = _build_l0_valid_resume_index(resume_rows)

    for index, pred_path in enumerate(pred_paths, start=1):
        metadata = infer_prediction_metadata(pred_path, pred_root)
        dataset_sample = dataset_index.get(_project_key(metadata["sample_id"]))

        if dataset_sample:
            gt_path = dataset_sample.reference_path
            req_path = dataset_sample.requirements_path
            reqcov_path = dataset_sample.reqcov_requirements_path
            project_language = dataset_sample.language
        else:
            gt_path = (
                _find_matching_file(gt_dir, pred_path, [".puml", ".plantuml", ".wsd"], metadata["sample_id"])
                if gt_dir
                else None
            )
            req_path = (
                _find_matching_file(requirements_dir, pred_path, [".md", ".txt", ".json"], metadata["sample_id"])
                if requirements_dir
                else None
            )
            project_language = None
            reqcov_path = req_path.with_name("req_final.jsonl") if req_path else None

        resume_row = _find_l0_valid_resume_row(
            resume_index,
            sample_id=metadata["sample_id"],
            candidate_id=metadata["candidate_id"],
        )
        if resume_row and resume_row.get("l1_metric_version") == VERSION:
            resume_row = dict(resume_row)
            for column in RETIRED_OUTPUT_COLUMNS:
                resume_row.pop(column, None)
            resume_row.update(
                {
                    "workflow": metadata["workflow"],
                    "model_id": metadata["model_id"],
                    "project_language": project_language,
                }
            )
            refreshed_l2 = False
            if l2_config and l2_config.enabled:
                requirements_text = req_path.read_text(encoding="utf-8") if req_path else None
                predicted_puml = Path(pred_path).read_text(encoding="utf-8")
                if not l2_resume_is_current(
                    resume_row, requirements_text, predicted_puml, l2_config, reqcov_path,
                ):
                    _log_progress(progress_logger, resume_row, "L2", "start", index, total,
                                  detail="refreshing legacy, failed, or changed-input L2 result")
                    resume_row.update(evaluate_l2(
                        requirements_text, predicted_puml, l2_config,
                        reqcov_requirements_path=reqcov_path,
                    ))
                    resume_row["stage_status"] = _completion_status(
                        resume_row, resume_row.get("l1_status") == "failed",
                    )
                    refreshed_l2 = True
                    _log_progress(progress_logger, resume_row, "L2", str(resume_row["l2_status"]),
                                  index, total, detail=resume_row.get("l2_error")
                                  or resume_row.get("l2_requirement_coverage_error"))
            _log_progress(
                progress_logger,
                resume_row,
                "sample",
                "reused",
                index,
                total,
                detail=("reused L0/L1; refreshed L2" if refreshed_l2 else
                        "matched candidate, sample, and l0_valid=True in resume CSV"),
            )
            rows.append(_ordered_row(dict(resume_row)))
            _write_checkpoint(rows, checkpoint_path)
            continue

        rows.append(
            evaluate_pair(
                pred_path,
                gt_path,
                req_path,
                l2_config,
                l1_config,
                reqcov_requirements_path=reqcov_path,
                sample_id=metadata["sample_id"],
                candidate_id=metadata["candidate_id"],
                workflow=metadata["workflow"],
                model_id=metadata["model_id"],
                project_language=project_language,
                alignment_cache_path=_alignment_cache_path(pred_path, l1_config),
                progress_logger=progress_logger,
                progress_index=index,
                progress_total=total,
            )
        )
        _write_checkpoint(rows, checkpoint_path)
    return rows


def discover_plantuml_files(path: Path) -> List[Path]:
    path = Path(path)
    if path.is_file():
        return [path]
    patterns = ["*.puml", "*.plantuml", "*.wsd"]
    files: List[Path] = []
    for pattern in patterns:
        files.extend(path.rglob(pattern))
    return sorted(files)


def build_dataset_index(dataset_dir: Path) -> Dict[str, DatasetSample]:
    dataset_dir = Path(dataset_dir)
    index: Dict[str, DatasetSample] = {}
    if not dataset_dir.exists():
        return index

    direct_samples = [
        sample
        for project_dir in sorted(path for path in dataset_dir.iterdir() if _is_indexable_dir(path))
        if (sample := _dataset_sample_from_project_dir(project_dir, dataset_dir.name)) is not None
    ]
    if direct_samples:
        for sample in direct_samples:
            index[_project_key(sample.sample_id)] = sample
        return index

    for language_dir in sorted(path for path in dataset_dir.iterdir() if path.is_dir()):
        if not _is_indexable_dir(language_dir):
            continue
        for project_dir in sorted(path for path in language_dir.iterdir() if _is_indexable_dir(path)):
            sample = _dataset_sample_from_project_dir(project_dir, language_dir.name)
            if sample is None:
                continue
            index[_project_key(project_dir.name)] = sample
    return index


def _is_indexable_dir(path: Path) -> bool:
    return path.is_dir() and path.name.casefold() != "invalid"


def _dataset_sample_from_project_dir(project_dir: Path, language: str) -> Optional[DatasetSample]:
    reference_path = _find_reference_diagram(project_dir)
    requirements_path = _find_requirements_document(project_dir)
    reqcov_path = project_dir / "req_final.jsonl"
    if not reference_path and not requirements_path and not reqcov_path.is_file():
        return None
    return DatasetSample(
        sample_id=project_dir.name,
        language=language,
        project_dir=project_dir,
        reference_path=reference_path,
        requirements_path=requirements_path,
        reqcov_requirements_path=reqcov_path,
    )


def infer_prediction_metadata(pred_path: Path, pred_root: Optional[Path] = None) -> Dict[str, Optional[str]]:
    pred_path = Path(pred_path)
    sample_id = pred_path.stem
    candidate_id = pred_path.parent.name if pred_path.parent.name else "candidate"
    workflow: Optional[str] = None
    model_id: Optional[str] = None

    relative_parts: List[str] = []
    if pred_root:
        try:
            relative = pred_path.resolve().relative_to(Path(pred_root).resolve())
            relative_parts = list(relative.parts)
        except ValueError:
            relative_parts = []

    if len(relative_parts) >= 4:
        workflow = relative_parts[0]
        model_id = relative_parts[1]
        sample_id = relative_parts[-2]
        candidate_id = "/".join(relative_parts[:-2])
    elif len(relative_parts) >= 3:
        model_id = relative_parts[0]
        sample_id = relative_parts[-2]
        candidate_id = "/".join(relative_parts[:-2])
    elif _is_generic_prediction_name(pred_path.stem) and pred_path.parent.name:
        sample_id = pred_path.parent.name

    return {
        "sample_id": sample_id,
        "candidate_id": candidate_id,
        "workflow": workflow,
        "model_id": model_id,
    }


def _alignment_cache_path(pred_path: Path, l1_config: Optional[L1AlignmentConfig]) -> Optional[Path]:
    parent = Path(pred_path).parent
    model = l1_config.model if l1_config else None
    if not model:
        return None
    existing = _find_alignment_cache_file(parent, model)
    if existing:
        return existing
    return parent / f"judge_alignment_v2_{_safe_filename(model)}.json"


def _find_alignment_cache_file(directory: Path, model: str) -> Optional[Path]:
    candidate = directory / f"judge_alignment_v2_{_safe_filename(model)}.json"
    return candidate if candidate.exists() else None


def _safe_filename(value: str) -> str:
    return "".join(char if char.isalnum() or char in {"-", "_", "."} else "_" for char in value)


def write_csv(rows: List[Dict[str, object]], out_path: Path) -> None:
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    columns = list(CSV_COLUMNS)
    extras = sorted({key for row in rows for key in row if key not in columns and key not in INTERNAL_OUTPUT_COLUMNS and key not in RETIRED_OUTPUT_COLUMNS})
    columns.extend(extras)
    _write_csv_atomic(rows, out_path, columns)


def _write_csv_atomic(rows: List[Dict[str, object]], out_path: Path, columns: List[str]) -> None:
    last_error: Optional[OSError] = None
    for attempt in range(1, CSV_WRITE_MAX_ATTEMPTS + 1):
        tmp_path = out_path.with_name(f".{out_path.name}.{os.getpid()}.{attempt}.tmp")
        try:
            with tmp_path.open("w", encoding="utf-8-sig", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=columns)
                writer.writeheader()
                for row in rows:
                    writer.writerow({column: row.get(column) for column in columns})
            os.replace(tmp_path, out_path)
            return
        except OSError as exc:
            last_error = exc
            _unlink_if_exists(tmp_path)
            if not _is_retryable_csv_write_error(exc) or attempt == CSV_WRITE_MAX_ATTEMPTS:
                raise
            time.sleep(CSV_WRITE_RETRY_DELAY_SECONDS * attempt)

    if last_error:
        raise last_error


def _is_retryable_csv_write_error(exc: OSError) -> bool:
    return exc.errno in CSV_WRITE_RETRY_ERRNOS


def _unlink_if_exists(path: Path) -> None:
    try:
        path.unlink()
    except FileNotFoundError:
        return


def load_resume_rows(path: Path) -> List[Dict[str, object]]:
    with Path(path).open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def _write_checkpoint(rows: List[Dict[str, object]], checkpoint_path: Optional[Path]) -> None:
    if checkpoint_path:
        write_csv(rows, checkpoint_path)


def _find_matching_file(
    base_dir: Path,
    pred_path: Path,
    suffixes: List[str],
    sample_id: Optional[str] = None,
) -> Optional[Path]:
    sample_id = sample_id or pred_path.stem
    candidates = []
    for suffix in suffixes:
        candidates.append(base_dir / f"{pred_path.stem}{suffix}")
        candidates.append(base_dir / pred_path.parent.name / f"{pred_path.stem}{suffix}")
        candidates.append(base_dir / f"{sample_id}{suffix}")
        candidates.append(base_dir / sample_id / f"{sample_id}{suffix}")
    for candidate in candidates:
        if candidate.exists():
            return candidate
    matches = [path for path in base_dir.rglob(f"{sample_id}.*") if path.suffix.lower() in suffixes]
    if matches:
        return sorted(matches)[0]
    matches = [path for path in base_dir.rglob(f"{pred_path.stem}.*") if path.suffix.lower() in suffixes]
    return sorted(matches)[0] if matches else None


def _find_reference_diagram(project_dir: Path) -> Optional[Path]:
    candidates = [
        project_dir / "AD" / "ad.puml",
        project_dir / "AD" / "ad.plantuml",
        project_dir / "AD" / "ad.wsd",
        project_dir / "ad.puml",
        project_dir / "ad.plantuml",
        project_dir / "ad.wsd",
    ]
    return _first_existing(candidates)


def _find_requirements_document(project_dir: Path) -> Optional[Path]:
    candidates = [
        project_dir / "checked_srs.md",
        project_dir / f"{project_dir.name}_review_checklist_srs.md",
    ]
    direct_match = _first_existing(candidates)
    if direct_match:
        return direct_match

    for pattern in ["*_review_checklist_srs.md", "*_srs.md", "*SRS*.md", "*srs*.md"]:
        matches = sorted(project_dir.glob(pattern))
        if matches:
            return matches[0]
    return None


def _first_existing(candidates: List[Path]) -> Optional[Path]:
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return None


def _build_l0_valid_resume_index(
    resume_rows: Optional[Iterable[Dict[str, object]]],
) -> Dict[tuple[str, str], Dict[str, object]]:
    index: Dict[tuple[str, str], Dict[str, object]] = {}
    if not resume_rows:
        return index
    for row in resume_rows:
        candidate_id = row.get("candidate_id")
        sample_id = row.get("sample_id")
        if not candidate_id or not sample_id:
            continue
        if not _csv_truthy(row.get("l0_valid")):
            continue
        index[(str(candidate_id), str(sample_id))] = row
    return index


def _find_l0_valid_resume_row(
    index: Dict[tuple[str, str], Dict[str, object]],
    *,
    sample_id: str,
    candidate_id: str,
) -> Optional[Dict[str, object]]:
    return index.get((candidate_id, sample_id))


def _csv_truthy(value: object) -> bool:
    if isinstance(value, bool):
        return value
    if value is None:
        return False
    return str(value).strip().casefold() in {"1", "true", "t", "yes", "y"}


def _is_generic_prediction_name(stem: str) -> bool:
    return stem.lower() in {"predicted", "prediction", "candidate", "output", "generated", "architecture"}


def _project_key(value: str) -> str:
    return value.casefold()


def _empty_l1_for_short_circuit() -> Dict[str, object]:
    return {
        "l1_status": None,
        "l1_error": None,
        "l1_predicted_node_count": None,
        "l1_predicted_edge_count": None,
        "l1_reference_node_count": None,
        "l1_reference_edge_count": None,
        "l1_node_coverage": None,
        "l1_gen_precision": None,
        "l1_edge_precision": None,
        "l1_edge_recall": None,
        "l1_edge_f1": None,
        "l1_boundary_accuracy": None,
        "l1_structural_similarity": None,
        "l1_structural_discrepancy": None,
        "l1_structural_denominator": None,
        "l1_metric_version": VERSION,
        "l1_god_ratio": None,
        "l1_matched_node_count": None,
        "l1_unmatched_predicted_node_count": None,
        "l1_unmatched_reference_node_count": None,
    }


def _failed_l1_result(error: str) -> Dict[str, object]:
    result = _empty_l1_for_short_circuit()
    result["l1_status"] = "failed"
    result["l1_error"] = error
    return result


def _log_progress(
    logger: Optional[ProgressLogger],
    row: Dict[str, object],
    stage: str,
    status: str,
    index: Optional[int],
    total: Optional[int],
    *,
    detail: object = None,
) -> None:
    if not logger:
        return

    position = f" {index}/{total}" if index is not None and total is not None else ""
    parts = [
        f"[eval{position}]",
        f"sample={_log_value(row.get('sample_id'))}",
        f"candidate={_log_value(row.get('candidate_id'))}",
    ]
    if row.get("workflow"):
        parts.append(f"workflow={_log_value(row.get('workflow'))}")
    if row.get("model_id"):
        parts.append(f"model={_log_value(row.get('model_id'))}")
    if row.get("project_language"):
        parts.append(f"language={_log_value(row.get('project_language'))}")
    parts.append(f"stage={stage}")
    parts.append(f"status={status}")
    if detail:
        parts.append(f"detail={_log_value(detail, max_length=240)}")
    logger(" ".join(parts))


def _log_value(value: object, *, max_length: int = 120) -> str:
    text = "-" if value is None else str(value)
    text = " ".join(text.split())
    if len(text) > max_length:
        return f"{text[: max_length - 3]}..."
    return text


def _ordered_row(row: Dict[str, object]) -> Dict[str, object]:
    ordered = {column: row.get(column) for column in CSV_COLUMNS}
    for key, value in row.items():
        if key not in ordered and key not in INTERNAL_OUTPUT_COLUMNS:
            ordered[key] = value
    return ordered
