import copy
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from evaluation_script.l2_semantic import (
    L2_DIMENSIONS, L2JudgeConfig, _flatten_l2, _normalize_l2_response,
    _parse_json, evaluate_l2, l2_resume_is_current,
)
from evaluation_script.pipeline import load_resume_rows, write_csv


def response():
    return {
        "scores": {dimension: {"score": score, "reasoning": f"Evidence for {dimension}."}
                   for dimension, score in zip(L2_DIMENSIONS, [3, 2, 3, 2, 4])},
        "metrics": {"asr_coverage": 0.6, "unsupported_inference_rate": 0.2},
    }


def nested_response():
    canonical = response()
    result = {"scores": {}}
    target = result["scores"]
    for dimension in L2_DIMENSIONS:
        target[dimension] = dict(canonical["scores"][dimension])
        target = target[dimension]
    target["metrics"] = canonical["metrics"]
    return result


class L2FormatTests(unittest.TestCase):
    def test_recovers_root_dimensions_without_mutating_original(self):
        raw = response()
        for dimension in L2_DIMENSIONS[1:]:
            raw[dimension] = raw["scores"].pop(dimension)
        before = copy.deepcopy(raw)
        result = _flatten_l2(raw)
        self.assertEqual(raw, before)
        self.assertEqual(result["l2_status"], "completed")
        self.assertTrue(result["l2_format_repaired"])
        self.assertEqual(json.loads(result["l2_raw_json"]), before)
        self.assertEqual(json.loads(result["l2_normalized_json"]), response())

    def test_recovers_nested_dimensions_and_metrics(self):
        result = _flatten_l2(nested_response())
        self.assertEqual(result["l2_status"], "completed")
        self.assertEqual([result[f"l2_{d}_score"] for d in L2_DIMENSIONS], [3, 2, 3, 2, 4])
        self.assertEqual(result["l2_asr_coverage"], 0.6)
        self.assertEqual(result["l2_unsupported_inference_rate"], 0.2)
        self.assertEqual(json.loads(result["l2_normalized_json"]), response())

    def test_canonical_response_is_unchanged_and_normalization_is_idempotent(self):
        result = _flatten_l2(response())
        self.assertFalse(result["l2_format_repaired"])
        normalized = _normalize_l2_response(nested_response())
        self.assertEqual(_normalize_l2_response(normalized), normalized)

    def test_recovers_metrics_inside_scores_without_changing_dimension_scores(self):
        raw = response()
        raw["scores"]["metrics"] = raw.pop("metrics")
        result = _flatten_l2(raw)
        self.assertTrue(result["l2_format_repaired"])
        self.assertEqual(result["l2_asr_coverage"], 0.6)
        self.assertEqual(json.loads(result["l2_normalized_json"]), response())

    def test_missing_dimensions_never_report_completed(self):
        raw = response()
        del raw["scores"]["readability"]
        result = _flatten_l2(raw)
        self.assertEqual(result["l2_status"], "failed")
        self.assertIn("Missing dimension readability", result["l2_error"])
        self.assertEqual(result["l2_completeness_score"], 3)
        self.assertIsNone(result["l2_readability_score"])

    def test_missing_reasoning_is_not_invented(self):
        raw = response()
        raw["scores"]["faithfulness"]["reasoning"] = ""
        result = _flatten_l2(raw)
        self.assertEqual(result["l2_status"], "failed")
        self.assertEqual(result["l2_faithfulness_reasoning"], "")
        self.assertIn("Missing reasoning for faithfulness", result["l2_error"])

    def test_unambiguous_numeric_scores_are_normalized_but_invalid_values_rejected(self):
        for value in (3, 3.0, "3", "3.0", " 3 "):
            raw = response()
            raw["scores"]["completeness"]["score"] = value
            self.assertEqual(_flatten_l2(raw)["l2_completeness_score"], 3)
        for value in (True, None, 0, 6, 2.5, "3/5", "three", float("nan"), float("inf")):
            with self.subTest(value=value):
                raw = response()
                raw["scores"]["completeness"]["score"] = value
                with self.assertRaises(ValueError):
                    _flatten_l2(raw)

    def test_conflicting_occurrences_are_rejected(self):
        raw = response()
        raw["faithfulness"] = {"score": 5, "reasoning": "Different judgment."}
        with self.assertRaisesRegex(ValueError, "Conflicting L2 values"):
            _flatten_l2(raw)

    def test_does_not_use_dimensions_inside_unrelated_metadata(self):
        raw = response()
        raw["example"] = {"readability": raw["scores"].pop("readability")}
        self.assertEqual(_flatten_l2(raw)["l2_status"], "failed")

    def test_json_fences_bom_and_duplicate_key_detection(self):
        raw = json.dumps(response())
        for text in (raw, "\ufeff" + raw, "```json\n" + raw + "\n```"):
            self.assertEqual(_parse_json(text), response())
        with self.assertRaisesRegex(ValueError, "Duplicate JSON key"):
            _parse_json('{"scores": {}, "scores": {}}')
        with self.assertRaises(ValueError):
            _parse_json('{"scores":')

    def test_failed_live_response_is_retained_even_when_json_is_invalid(self):
        config = L2JudgeConfig(enabled=True, api_key="test-only")
        for raw in ('{"scores":', json.dumps({"scores": {}})):
            with patch("evaluation_script.l2_semantic._chat_completion", return_value=raw), \
                 patch("evaluation_script.l2_semantic._evaluate_reqcov", return_value={}):
                result = evaluate_l2("Requirements", "@startuml\n@enduml", config)
            self.assertEqual(result["l2_status"], "failed")
            self.assertEqual(result["l2_raw_response"], raw)

    def test_csv_retains_original_and_normalized_response(self):
        row = _flatten_l2(nested_response())
        row["l2_raw_response"] = json.dumps(nested_response())
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "scores.csv"
            write_csv([row], path)
            loaded = load_resume_rows(path)[0]
        for field in ("l2_raw_json", "l2_normalized_json", "l2_raw_response"):
            self.assertEqual(loaded[field], row[field])

    def test_resume_rejects_completed_row_with_missing_score(self):
        row = _flatten_l2(response())
        row.update(l2_status="completed", l2_readability_score=None,
                   l2_requirement_coverage_status="completed")
        from evaluation_script.reqcov import REQCOV_VERSION
        row["l2_requirement_coverage_version"] = REQCOV_VERSION
        with patch("evaluation_script.l2_semantic.load_curated_requirements") as load:
            self.assertFalse(l2_resume_is_current(row, "SRS", "PUML", L2JudgeConfig(), Path("absent")))
            load.assert_not_called()


if __name__ == "__main__":
    unittest.main()
