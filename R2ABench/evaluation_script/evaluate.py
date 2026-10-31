from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .l1_structural import L1AlignmentConfig
from .l2_semantic import L2JudgeConfig
from .pipeline import discover_plantuml_files, evaluate_files, infer_prediction_metadata, load_resume_rows, write_csv


def _project_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _default_pred_root() -> Path:
    return _project_root() / "Outputs" / "RQ1" / "C-R2A-17"


def _default_dataset_dir() -> Path:
    return _project_root() / "Dataset" / "C-R2A-17"


def _print_progress(message: str) -> None:
    print(message, file=sys.stderr, flush=True)


def main() -> None:
    parser = argparse.ArgumentParser(description="Run MA4SA/R2ABench+ evaluation over generated PlantUML files.")
    parser.add_argument("--pred", type=Path, help="Generated PlantUML file or directory.")
    parser.add_argument("--pred-dir", type=Path, help="Generated PlantUML directory. Alias for --pred.")
    parser.add_argument(
        "--pred-root",
        type=Path,
        default=None,
        help="Metadata root used to infer workflow/model/sample when --pred targets a subdirectory.",
    )
    parser.add_argument(
        "--dataset-dir",
        type=Path,
        default=None,
        help="Dataset root with project AD/ad.puml, checked_srs.md, and req_final.jsonl (required for ReqCov).",
    )
    parser.add_argument("--gt-dir", type=Path, default=None, help="Optional reference PlantUML directory.")
    parser.add_argument("--requirements-dir", type=Path, default=None, help="Optional SRS directory; ReqCov reads req_final.jsonl beside each matched SRS.")
    parser.add_argument("--out", type=Path, default=Path("evaluation/results.csv"), help="Output CSV path.")
    parser.add_argument(
        "--resume-from",
        type=Path,
        default=None,
        help=(
            "Reuse current L0/L1 rows from an evaluation CSV. When L2 is enabled, refresh legacy or changed-input L2 results."
        ),
    )
    parser.add_argument(
        "--only-resume-rows",
        action="store_true",
        help="With --resume-from, only evaluate predictions whose candidate/sample key exists in the resume CSV.",
    )
    parser.add_argument(
        "--enable-l1-judge",
        action="store_true",
        help="Call an OpenAI-compatible judge for R2ABench-style semantic node alignment.",
    )
    parser.add_argument(
        "--l1-judge-model",
        default=None,
        help="L1 node-alignment judge model name. Defaults to --llm-model when provided.",
    )
    parser.add_argument("--enable-l2-judge", action="store_true", help="Call a judge for L2 dimensions and separately for curated item-level ReqCov.")
    parser.add_argument("--llm-model", default=None, help="Judge model name.")
    parser.add_argument("--llm-base-url", default=None, help="OpenAI-compatible base URL.")
    parser.add_argument("--llm-api-key-env", default="OPENAI_API_KEY", help="Environment variable containing API key.")
    args = parser.parse_args()

    pred_root = args.pred or args.pred_dir
    if not pred_root:
        default_pred_root = _default_pred_root()
        if default_pred_root.exists():
            pred_root = default_pred_root
        else:
            parser.error("Provide --pred or --pred-dir.")
    metadata_root = args.pred_root or pred_root

    dataset_dir = args.dataset_dir
    if dataset_dir is None:
        default_dataset_dir = _default_dataset_dir()
        try:
            uses_default_pred = Path(metadata_root).resolve() == _default_pred_root().resolve()
        except OSError:
            uses_default_pred = False
        if uses_default_pred and default_dataset_dir.exists():
            dataset_dir = default_dataset_dir

    pred_paths = discover_plantuml_files(pred_root)
    if not pred_paths:
        parser.error(f"No PlantUML files found under {pred_root}")
    resume_rows = load_resume_rows(args.resume_from) if args.resume_from else None
    if args.only_resume_rows:
        if resume_rows is None:
            parser.error("--only-resume-rows requires --resume-from.")
        resume_keys = {
            (str(row.get("candidate_id")), str(row.get("sample_id")))
            for row in resume_rows
            if row.get("candidate_id") and row.get("sample_id")
        }
        before_count = len(pred_paths)
        pred_paths = [
            path
            for path in pred_paths
            if (
                infer_prediction_metadata(path, metadata_root)["candidate_id"],
                infer_prediction_metadata(path, metadata_root)["sample_id"],
            )
            in resume_keys
        ]
        _print_progress(f"Filtered predictions by resume CSV: {len(pred_paths)}/{before_count} files kept.")
        if not pred_paths:
            parser.error("No PlantUML files matched --resume-from keys.")

    l1_config = L1AlignmentConfig.from_env(
        enabled=args.enable_l1_judge,
        model=args.l1_judge_model or args.llm_model,
        base_url=args.llm_base_url,
        api_key_env=args.llm_api_key_env,
    )
    l2_config = L2JudgeConfig.from_env(
        enabled=args.enable_l2_judge,
        model=args.llm_model,
        base_url=args.llm_base_url,
        api_key_env=args.llm_api_key_env,
    )
    rows = evaluate_files(
        pred_paths,
        args.gt_dir,
        args.requirements_dir,
        l2_config,
        l1_config,
        pred_root=metadata_root,
        dataset_dir=dataset_dir,
        resume_rows=resume_rows,
        checkpoint_path=args.out,
        progress_logger=_print_progress,
    )
    write_csv(rows, args.out)
    print(f"Wrote {len(rows)} evaluation rows to {args.out}")


if __name__ == "__main__":
    main()
