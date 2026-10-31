#!/usr/bin/env bash
set -euo pipefail

#
# Typical usage:
#   DATASET=E-R2A bash generation/openhands.sh
#   DATASET=G-R2A FORCE=1 bash generation/openhands.sh
#
# Optional overrides:
#   MODELS_OVERRIDE="gpt-5 qwen3-coder-480b-a35b-instruct"
#   SAMPLES_OVERRIDE="asp deepcode"
#   OPENHANDS_BIN=openhands
#   MODEL_PROVIDER_PREFIX=openai
#   STOP_ON_ERROR=1

ROOT="${ROOT:-$(cd "$(dirname "$0")/.." && pwd)}"
DATASET="${DATASET:-E-R2A}"
INPUT="${INPUT:-$ROOT/Dataset/$DATASET}"
OUTROOT="${OUTROOT:-$ROOT/runs/$DATASET/openhands}"
OPENHANDS_BIN="${OPENHANDS_BIN:-openhands}"
MODEL_PROVIDER_PREFIX="${MODEL_PROVIDER_PREFIX:-openai}"
PYTHON_BIN="${PYTHON_BIN:-python3}"
FORCE="${FORCE:-0}"
DRY_RUN="${DRY_RUN:-0}"
STOP_ON_ERROR="${STOP_ON_ERROR:-1}"

if [[ -n "${MODELS_OVERRIDE:-}" ]]; then
  # Space-separated list, for example:
  # MODELS_OVERRIDE="gpt-5 qwen3-coder-480b-a35b-instruct"
  read -r -a MODELS <<< "$MODELS_OVERRIDE"
else
  MODELS=(
    "claude-sonnet-4-6"
    "deepseek-v3.2"
    "deepseek-v4.1-flash"
    "gpt-5"
    "qwen3-coder-480b-a35b-instruct"
  )
fi

if [[ -n "${SAMPLES_OVERRIDE:-}" ]]; then
  read -r -a SELECTED_SAMPLES <<< "$SAMPLES_OVERRIDE"
else
  SELECTED_SAMPLES=()
fi

if [[ ! -d "$INPUT" ]]; then
  echo "Input directory not found: $INPUT" >&2
  exit 1
fi

if [[ "$DRY_RUN" != "1" ]] && ! command -v "$OPENHANDS_BIN" >/dev/null 2>&1; then
  echo "OpenHands executable not found: $OPENHANDS_BIN" >&2
  exit 1
fi

if [[ "$DRY_RUN" != "1" && -z "${LLM_API_KEY:-}" ]]; then
  if [[ -n "${OPENAI_API_KEY:-}" ]]; then
    export LLM_API_KEY="$OPENAI_API_KEY"
  else
    echo "LLM_API_KEY or OPENAI_API_KEY must be set before running OpenHands." >&2
    exit 1
  fi
fi

# OpenHands reads LLM_* env vars when --override-with-envs is used. Keep the
# OpenAI-compatible base URL in the same namespace when the experiment uses one.
if [[ -z "${LLM_BASE_URL:-}" && -n "${OPENAI_BASE_URL:-}" ]]; then
  export LLM_BASE_URL="$OPENAI_BASE_URL"
fi

# OpenHands' interactive Settings/Command Palette can persist the chosen model
# under ~/.openhands, e.g. agent_settings.json. Isolate persistent state so that
# an old UI selection such as openai/gpt-5 cannot silently leak into this
# benchmark run. Override this env var only if you intentionally want to reuse a
# known OpenHands settings directory.
export OH_PERSISTENCE_DIR="${OH_PERSISTENCE_DIR:-$ROOT/tmp/openhands_r2a_state}"

safe_path_segment() {
  printf '%s' "$1" |
    sed -E 's#[<>:"/\\|?*[:space:]]+#_#g; s#^_+##; s#_+$##'
}

model_call_name() {
  local model_label="$1"
  if [[ -z "$MODEL_PROVIDER_PREFIX" || "$model_label" == */* ]]; then
    printf '%s' "$model_label"
  else
    printf '%s/%s' "$MODEL_PROVIDER_PREFIX" "$model_label"
  fi
}

normalize_model_name() {
  printf '%s' "$1" | tr '[:upper:]' '[:lower:]' | tr -d '[:space:]'
}

strip_ansi() {
  sed -E 's/\x1B\[[0-9;]*[[:alpha:]]//g'
}

extract_actual_model() {
  local log_path="$1"
  if [[ ! -f "$log_path" ]]; then
    return 0
  fi
  strip_ansi < "$log_path" |
    sed -n 's/.*Agent initialized with model: //p' |
    head -n 1 |
    tr -d '\r' |
    sed -E 's/[[:space:]]+$//'
}

has_valid_plantuml_markers() {
  local puml_path="$1"
  [[ -f "$puml_path" ]] &&
    grep -qiE '^[[:space:]]*@startuml\b' "$puml_path" &&
    grep -qi '@enduml' "$puml_path"
}

sample_allowed() {
  local sample="$1"
  if [[ "${#SELECTED_SAMPLES[@]}" -eq 0 ]]; then
    return 0
  fi
  local selected
  for selected in "${SELECTED_SAMPLES[@]}"; do
    if [[ "$sample" == "$selected" ]]; then
      return 0
    fi
  done
  return 1
}

write_metadata() {
  local metadata_path="$1"
  local status="$2"
  local error_message="${3:-}"

  DATASET="$DATASET" \
  SAMPLE="$SAMPLE" \
  MODEL_LABEL="$MODEL_LABEL" \
  MODEL_CALL="$MODEL_CALL" \
  ACTUAL_MODEL="$ACTUAL_MODEL" \
  STATUS="$status" \
  ERROR_MESSAGE="$error_message" \
  SRS="$SRS" \
  OUTDIR="$OUTDIR" \
  PRED="$PRED" \
  TASK="$TASK" \
  LOG="$LOG" \
  ROOT="$ROOT" \
  OPENHANDS_BIN="$OPENHANDS_BIN" \
  OH_PERSISTENCE_DIR="$OH_PERSISTENCE_DIR" \
  "$PYTHON_BIN" - <<'PY' > "$metadata_path"
import datetime
import json
import os

payload = {
    "timestamp_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "dataset": os.environ["DATASET"],
    "sample": os.environ["SAMPLE"],
    "model_label": os.environ["MODEL_LABEL"],
    "requested_model": os.environ["MODEL_CALL"],
    "actual_model_from_openhands_log": os.environ.get("ACTUAL_MODEL", ""),
    "status": os.environ["STATUS"],
    "error": os.environ.get("ERROR_MESSAGE", ""),
    "root": os.environ["ROOT"],
    "srs_path": os.environ["SRS"],
    "output_dir": os.environ["OUTDIR"],
    "predicted_path": os.environ["PRED"],
    "task_path": os.environ["TASK"],
    "openhands_log_path": os.environ["LOG"],
    "openhands_bin": os.environ["OPENHANDS_BIN"],
    "openhands_persistence_dir": os.environ["OH_PERSISTENCE_DIR"],
    "command": [
        os.environ["OPENHANDS_BIN"],
        "--override-with-envs",
        "--headless",
        "--json",
        "-f",
        os.environ["TASK"],
    ],
    "llm_env": {
        "LLM_MODEL": os.environ["MODEL_CALL"],
        "LLM_BASE_URL": os.environ.get("LLM_BASE_URL", ""),
        "LLM_API_KEY_set": bool(os.environ.get("LLM_API_KEY", "")),
    },
}
print(json.dumps(payload, ensure_ascii=False, indent=2))
PY
}

failures=0

record_failure() {
  local message="$1"
  failures=$((failures + 1))
  echo "  failed: $message" >&2
  write_metadata "$METADATA" "failed" "$message" || true
  if [[ "$STOP_ON_ERROR" == "1" ]]; then
    exit 1
  fi
}

echo "Root: $ROOT"
echo "Dataset: $DATASET"
echo "Input: $INPUT"
echo "Output: $OUTROOT"
echo "Models: ${MODELS[*]}"
if [[ "${#SELECTED_SAMPLES[@]}" -gt 0 ]]; then
  echo "Selected samples: ${SELECTED_SAMPLES[*]}"
fi
echo "OpenHands state: $OH_PERSISTENCE_DIR"

total_samples=$(
  while IFS= read -r candidate_srs; do
    candidate_sample="$(basename "$(dirname "$candidate_srs")")"
    if sample_allowed "$candidate_sample"; then
      printf '.'
    fi
  done < <(find "$INPUT" -name checked_srs.md | sort) | wc -c | tr -d '[:space:]'
)
echo "Samples: $total_samples"

for MODEL_LABEL in "${MODELS[@]}"; do
  MODEL_DIR="$(safe_path_segment "$MODEL_LABEL")"
  if [[ -z "$MODEL_DIR" ]]; then
    MODEL_DIR="model"
  fi
  MODEL_CALL="$(model_call_name "$MODEL_LABEL")"
  expected_norm="$(normalize_model_name "$MODEL_CALL")"

  while IFS= read -r SRS; do
    SAMPLE="$(basename "$(dirname "$SRS")")"
    if ! sample_allowed "$SAMPLE"; then
      continue
    fi
    OUTDIR="$OUTROOT/$MODEL_DIR/$SAMPLE"
    PRED="$OUTDIR/predicted.puml"
    TASK="$OUTDIR/task.txt"
    LOG="$OUTDIR/openhands.jsonl"
    METADATA="$OUTDIR/run_metadata.json"

    echo "running: $MODEL_LABEL :: $SAMPLE"

    if [[ -f "$PRED" && "$FORCE" != "1" ]]; then
      ACTUAL_MODEL="$(extract_actual_model "$LOG")"
      actual_norm="$(normalize_model_name "$ACTUAL_MODEL")"
      if has_valid_plantuml_markers "$PRED" && [[ -n "$ACTUAL_MODEL" && "$actual_norm" == "$expected_norm" ]]; then
        echo "  skipped: existing output verified with actual model $ACTUAL_MODEL"
        continue
      fi
      record_failure "existing output is not verifiably from $MODEL_CALL; actual log model is '${ACTUAL_MODEL:-missing}'. Re-run with FORCE=1 after deciding whether to overwrite it."
      continue
    fi

    if [[ "$DRY_RUN" == "1" ]]; then
      echo "  dry-run: LLM_MODEL=$MODEL_CALL $OPENHANDS_BIN --override-with-envs --headless --json -f $TASK"
      continue
    fi

    mkdir -p "$OUTDIR"
    if [[ -f "$PRED" ]]; then
      BACKUP="$(mktemp "$OUTDIR/predicted.previous.XXXXXXXX.puml")"
      mv -- "$PRED" "$BACKUP"
      echo "  previous prediction preserved: $BACKUP"
    fi

    cat > "$TASK" <<EOF
Run the following architecture-generation prompt. Save the PlantUML source ONLY to:
$PRED

Do not edit files outside:
$OUTDIR

Prompt:

You are an experienced software architect.

Task: Generate a system architecture diagram directly from the provided Software Requirements Specification (SRS).

Return ONLY PlantUML source. Begin with @startuml and end with @enduml. Do not wrap the answer in Markdown fences and do not add explanations. Do not generate sequence, class, or use-case diagrams.

SRS:

EOF
    cat "$SRS" >> "$TASK"

    export LLM_MODEL="$MODEL_CALL"
    ACTUAL_MODEL=""
    write_metadata "$METADATA" "started"

    set +e
    "$OPENHANDS_BIN" --override-with-envs --headless --json -f "$TASK" > "$LOG" 2>&1
    exit_code=$?
    set -e

    if [[ "$exit_code" -ne 0 ]]; then
      ACTUAL_MODEL="$(extract_actual_model "$LOG")"
      record_failure "OpenHands exited with code $exit_code"
      continue
    fi

    ACTUAL_MODEL="$(extract_actual_model "$LOG")"
    actual_norm="$(normalize_model_name "$ACTUAL_MODEL")"
    if [[ -z "$ACTUAL_MODEL" ]]; then
      record_failure "OpenHands log does not contain an 'Agent initialized with model' line."
      continue
    fi
    if [[ "$actual_norm" != "$expected_norm" ]]; then
      record_failure "model mismatch: requested $MODEL_CALL but OpenHands initialized $ACTUAL_MODEL"
      continue
    fi
    if ! has_valid_plantuml_markers "$PRED"; then
      record_failure "predicted.puml is missing or does not contain @startuml/@enduml markers."
      continue
    fi

    write_metadata "$METADATA" "completed"
    echo "  generated: $PRED"
  done < <(find "$INPUT" -name checked_srs.md | sort)
done

if [[ "$failures" -gt 0 ]]; then
  echo "Completed with $failures failure(s)." >&2
  exit 1
fi

echo "Completed successfully."
