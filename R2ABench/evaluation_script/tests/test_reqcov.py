import copy
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from evaluation_script.l0_syntax import evaluate_l0
from evaluation_script.l1_metrics import VERSION
from evaluation_script.l2_semantic import L2_DIMENSIONS, L2JudgeConfig, evaluate_l2, l2_resume_is_current
from evaluation_script.pipeline import build_dataset_index, evaluate_files, evaluate_pair, load_resume_rows, write_csv
from evaluation_script.reqcov import REQCOV_VERSION, build_reqcov_prompt, load_curated_requirements, validate_reqcov_assessments


PUML = '@startuml\ncomponent "Game Save Manager" as Saves\ndatabase "Save Store" as DB\nSaves --> DB : stores saves\n@enduml\n'
SRS = "The system shall manage saves and user accounts."
ITEMS = [
    {"req_id": "demo-R1", "requirement": "Create, list, delete and continue game saves.",
     "source": {"file": "checked_srs.md", "ids": ["FR-1"], "lines": [10]}},
    {"req_id": "demo-R2", "requirement": "Manage user accounts."},
]
ASSESSMENTS = [
    {"req_id": "demo-R1", "main_responsibility": "Game save management", "covered": 1,
     "evidence": ['component "Game Save Manager" as Saves'],
     "reason": "The component explicitly represents save management."},
    {"req_id": "demo-R2", "main_responsibility": "User account management", "covered": 0,
     "evidence": [], "reason": "No account-management responsibility is shown."},
]
HOLISTIC = {"scores": {dimension: {"score": 4, "reasoning": "One capability omitted."} for dimension in L2_DIMENSIONS},
            "metrics": {"requirement_coverage": 0.99, "asr_coverage": 0.7}}


class ReqCovTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.req = self.root / "req_final.jsonl"
        self.write_items()
        self.config = L2JudgeConfig(enabled=True, api_key="test-only", model="mock-judge")

    def write_items(self, items=None):
        self.req.write_text("\n".join(json.dumps(item) for item in (ITEMS if items is None else items)), encoding="utf-8")

    def responses(self, assessments=None):
        return [json.dumps(HOLISTIC), json.dumps({"requirement_assessments": ASSESSMENTS if assessments is None else assessments})]

    def run_judge(self, responses=None, path=None):
        with patch("evaluation_script.l2_semantic._chat_completion", side_effect=self.responses() if responses is None else responses) as call:
            result = evaluate_l2(SRS, PUML, self.config, reqcov_requirements_path=self.req if path is None else path)
        return result, call

    def test_loads_bom_blank_lines_and_preserves_all_metadata(self):
        self.req.write_text("\n" + "\n\n".join(json.dumps(i) for i in ITEMS) + "\n", encoding="utf-8-sig")
        self.assertEqual(load_curated_requirements(self.req), ITEMS)

    def test_rejects_empty_malformed_duplicate_and_invalid_items(self):
        invalid = ["", "\n ", "not json", "[]", "null", '{}',
                   '{"req_id":1,"requirement":"x"}',
                   '{"req_id":"R1","requirement":" "}',
                   '{"req_id":"R1","req_id":"R2","requirement":"x"}',
                   "\n".join([json.dumps(ITEMS[0])] * 2)]
        for value in invalid:
            with self.subTest(value=value):
                self.req.write_text(value, encoding="utf-8")
                with self.assertRaises(ValueError):
                    load_curated_requirements(self.req)

    def test_does_not_fallback_to_req_jsonl(self):
        self.req.rename(self.root / "Req.jsonl")
        result, call = self.run_judge(responses=[json.dumps(HOLISTIC)])
        self.assertEqual(call.call_count, 1)
        self.assertEqual(result["l2_requirement_coverage_status"], "skipped_missing_req_final")
        self.assertEqual(result["l2_status"], "completed_with_reqcov_error")
        self.assertIsNone(result["l2_requirement_coverage"])
        self.assertIsNone(result["l2_requirement_coverage_percent"])
        self.assertEqual(result["l2_completeness_score"], 4)

    def test_invalid_file_preserves_holistic_scores_and_does_not_call_coverage_judge(self):
        self.req.write_text("{broken", encoding="utf-8")
        result, call = self.run_judge(responses=[json.dumps(HOLISTIC)])
        self.assertEqual(call.call_count, 1)
        self.assertEqual(result["l2_requirement_coverage_status"], "failed_invalid_req_final")
        self.assertIn("line 1", result["l2_requirement_coverage_error"])
        self.assertIsNone(result["l2_requirement_count"])
        self.assertIsNone(result["l2_requirement_coverage"])

    def test_request_uses_exact_curated_set_and_calculates_coverage_locally(self):
        result, call = self.run_judge()
        self.assertEqual(result["l2_status"], "completed")
        self.assertEqual(result["l2_requirement_coverage"], 0.5)
        self.assertEqual(result["l2_requirement_coverage_percent"], 50.0)
        self.assertEqual(result["l2_requirement_count"], 2)
        self.assertEqual(result["l2_covered_requirement_count"], 1)
        self.assertEqual(result["l2_requirement_coverage_version"], REQCOV_VERSION)
        self.assertEqual(json.loads(result["l2_requirement_assessments_json"]), ASSESSMENTS)
        prompt = call.call_args_list[1].args[0]
        payload = prompt.split("<REQ_FINAL_JSONL>\n", 1)[1].split("\n</REQ_FINAL_JSONL>", 1)[0]
        self.assertEqual([json.loads(line) for line in payload.splitlines()], ITEMS)
        self.assertIn(PUML, prompt)
        self.assertIn(SRS, prompt)
        self.assertNotIn('"requirement_coverage":', call.call_args_list[0].args[0])

    def test_zero_and_full_coverage_are_valid_results(self):
        for covered in (0, 1):
            with self.subTest(covered=covered):
                assessments = copy.deepcopy(ASSESSMENTS)
                for item in assessments:
                    item["covered"] = covered
                    item["evidence"] = ['component "Game Save Manager" as Saves'] if covered else []
                result = validate_reqcov_assessments({"requirement_assessments": assessments}, ITEMS, PUML)
                self.assertEqual(result["l2_requirement_coverage_percent"], 100 * covered)
                self.assertEqual(result["l2_requirement_coverage_status"], "completed")

    def test_invalid_assessments_never_become_zero_coverage(self):
        cases = []
        cases.append({"requirement_assessments": ASSESSMENTS[:1]})
        cases.append({"requirement_assessments": [ASSESSMENTS[0], ASSESSMENTS[0]]})
        for field, value in [("req_id", "unknown"), ("req_id", None), ("covered", True),
                             ("covered", "1"), ("covered", 0.5), ("covered", 2),
                             ("evidence", []), ("evidence", ["invented component"]),
                             ("evidence", [ITEMS[0]["requirement"]]), ("evidence", [1]),
                             ("evidence", "Game Save Manager"), ("reason", ""),
                             ("main_responsibility", None)]:
            assessments = copy.deepcopy(ASSESSMENTS)
            assessments[0][field] = value
            cases.append({"requirement_assessments": assessments})
        cases.extend([[], {}, {"requirement_assessments": [None, None]}])
        for payload in cases:
            with self.subTest(payload=payload):
                result, _ = self.run_judge([json.dumps(HOLISTIC), json.dumps(payload)])
                self.assertEqual(result["l2_requirement_coverage_status"], "failed_validation")
                self.assertIsNone(result["l2_requirement_coverage"])
                self.assertIsNone(result["l2_requirement_coverage_percent"])
                self.assertEqual(result["l2_requirement_count"], 2)
                self.assertEqual(result["l2_requirement_coverage_raw_response"], json.dumps(payload))

    def test_malformed_json_and_request_failure_are_distinct(self):
        for response, status in [("{broken", "failed_validation"), (None, "failed_validation"), (RuntimeError("timeout"), "failed_judge")]:
            with self.subTest(status=status):
                result, _ = self.run_judge([json.dumps(HOLISTIC), response])
                self.assertEqual(result["l2_requirement_coverage_status"], status)
                self.assertIsNone(result["l2_requirement_coverage"])

    def test_quote_validation_accepts_newline_conventions_and_preserves_input_order(self):
        assessments = copy.deepcopy(ASSESSMENTS)
        assessments[0]["evidence"] = ['component "Game Save Manager" as Saves\ndatabase "Save Store" as DB']
        result = validate_reqcov_assessments({"requirement_assessments": list(reversed(assessments))}, ITEMS, PUML.replace("\n", "\r\n"))
        self.assertEqual(json.loads(result["l2_requirement_assessments_json"]), assessments)

    def test_disabled_or_missing_context_never_calls_judge(self):
        for config, text, status in [(L2JudgeConfig(), SRS, "skipped_disabled"),
                                     (L2JudgeConfig(enabled=True), SRS, "skipped_missing_api_key"),
                                     (self.config, None, "skipped_missing_requirements")]:
            with self.subTest(status=status), patch("evaluation_script.l2_semantic._chat_completion") as call:
                result = evaluate_l2(text, PUML, config, reqcov_requirements_path=self.req)
                call.assert_not_called()
                self.assertEqual(result["l2_requirement_coverage_status"], status)
                self.assertIsNone(result["l2_requirement_coverage"])

    def test_coverage_can_complete_when_holistic_request_fails(self):
        result, _ = self.run_judge([RuntimeError("holistic failed"), self.responses()[1]])
        self.assertEqual(result["l2_status"], "failed")
        self.assertEqual(result["l2_requirement_coverage_status"], "completed")
        self.assertEqual(result["l2_requirement_coverage_percent"], 50.0)

    def test_resume_signature_detects_file_view_srs_model_prompt_and_version_changes(self):
        row, _ = self.run_judge()
        self.assertTrue(l2_resume_is_current(row, SRS, PUML, self.config, self.req))
        self.assertFalse(l2_resume_is_current(row, SRS + " changed", PUML, self.config, self.req))
        self.assertFalse(l2_resume_is_current(row, SRS, PUML + " changed", self.config, self.req))
        self.assertFalse(l2_resume_is_current(row, SRS, PUML, L2JudgeConfig(model="other"), self.req))
        with patch("evaluation_script.l2_semantic.build_reqcov_prompt", return_value="changed rubric"):
            self.assertFalse(l2_resume_is_current(row, SRS, PUML, self.config, self.req))
        self.assertFalse(l2_resume_is_current(dict(row, l2_requirement_coverage_version="old"), SRS, PUML, self.config, self.req))
        self.assertFalse(l2_resume_is_current(dict(row, l2_requirement_coverage_status="failed_validation"), SRS, PUML, self.config, self.req))
        changed = copy.deepcopy(ITEMS)
        changed[0]["requirement"] += " Updated intent."
        self.write_items(changed)
        self.assertFalse(l2_resume_is_current(row, SRS, PUML, self.config, self.req))
        self.req.write_text("{bad", encoding="utf-8")
        self.assertFalse(l2_resume_is_current(row, SRS, PUML, self.config, self.req))

    def make_project(self):
        dataset = self.root / "dataset"
        project = dataset / "JAVA" / "demo"
        project.mkdir(parents=True)
        (project / "checked_srs.md").write_text(SRS, encoding="utf-8")
        (project / "req_final.jsonl").write_bytes(self.req.read_bytes())
        pred_root = self.root / "predictions"
        pred = pred_root / "direct" / "mock" / "demo" / "predicted.puml"
        pred.parent.mkdir(parents=True)
        pred.write_text(PUML, encoding="utf-8")
        return dataset, project, pred_root, pred

    def test_pipeline_selects_req_final_from_matched_project_and_roundtrips_csv(self):
        dataset, project, pred_root, pred = self.make_project()
        other = dataset / "JAVA" / "other"
        other.mkdir()
        (other / "checked_srs.md").write_text("Other project", encoding="utf-8")
        (other / "req_final.jsonl").write_text('{"req_id":"wrong","requirement":"wrong"}', encoding="utf-8")
        self.assertEqual(build_dataset_index(dataset)["demo"].reqcov_requirements_path, project / "req_final.jsonl")
        with patch("evaluation_script.pipeline.evaluate_l0", side_effect=lambda p: evaluate_l0(p, syntax_checker=lambda _: (True, ""))), \
             patch("evaluation_script.pipeline.evaluate_l1", return_value={"l1_status": "completed", "l1_metric_version": VERSION}), \
             patch("evaluation_script.l2_semantic._chat_completion", side_effect=self.responses()) as call:
            rows = evaluate_files([pred], dataset_dir=dataset, pred_root=pred_root, l2_config=self.config)
        self.assertEqual(rows[0]["l2_requirement_coverage_percent"], 50.0)
        self.assertNotIn('"req_id": "wrong"', call.call_args_list[1].args[0])
        out = self.root / "result.csv"
        write_csv(rows, out)
        restored = load_resume_rows(out)[0]
        self.assertEqual(json.loads(restored["l2_requirement_assessments_json"]), ASSESSMENTS)
        with patch("evaluation_script.pipeline.evaluate_l0") as l0, patch("evaluation_script.l2_semantic._chat_completion") as chat:
            resumed = evaluate_files([pred], dataset_dir=dataset, pred_root=pred_root, l2_config=self.config, resume_rows=[restored])
            l0.assert_not_called()
            chat.assert_not_called()
        self.assertEqual(float(resumed[0]["l2_requirement_coverage_percent"]), 50.0)

    def test_resume_refreshes_legacy_l2_only_and_preserves_l1_results(self):
        dataset, project, pred_root, pred = self.make_project()
        legacy = {"sample_id": "demo", "candidate_id": "direct/mock", "l0_valid": True,
                  "l1_metric_version": VERSION, "l1_status": "completed", "l1_edge_f1": 0.37,
                  "l2_status": "completed", "l2_requirement_coverage": 0.99}
        with patch("evaluation_script.pipeline.evaluate_l0") as l0, patch("evaluation_script.pipeline.evaluate_l1") as l1, \
             patch("evaluation_script.l2_semantic._chat_completion", side_effect=self.responses()):
            result = evaluate_files([pred], dataset_dir=dataset, pred_root=pred_root, l2_config=self.config, resume_rows=[legacy])[0]
            l0.assert_not_called()
            l1.assert_not_called()
        self.assertEqual(result["l2_requirement_coverage_percent"], 50.0)
        self.assertEqual(result["l1_edge_f1"], 0.37)
        (project / "req_final.jsonl").write_text("{invalid", encoding="utf-8")
        with patch("evaluation_script.l2_semantic._chat_completion", side_effect=[json.dumps(HOLISTIC)]):
            failed = evaluate_files([pred], dataset_dir=dataset, pred_root=pred_root, l2_config=self.config, resume_rows=[result])[0]
        self.assertIsNone(failed["l2_requirement_coverage"])
        self.assertIsNone(failed["l2_requirement_assessments_json"])
        self.assertEqual(failed["stage_status"], "completed_with_l2_error")
        self.assertEqual(failed["l1_edge_f1"], 0.37)

    def test_direct_pair_resolves_req_final_beside_srs(self):
        srs = self.root / "checked_srs.md"
        pred = self.root / "predicted.puml"
        srs.write_text(SRS, encoding="utf-8")
        pred.write_text(PUML, encoding="utf-8")
        with patch("evaluation_script.pipeline.evaluate_l0", side_effect=lambda p: evaluate_l0(p, syntax_checker=lambda _: (True, ""))), \
             patch("evaluation_script.l2_semantic._chat_completion", side_effect=self.responses()):
            row = evaluate_pair(pred, requirements_path=srs, l2_config=self.config)
        self.assertEqual(row["l2_requirement_coverage_percent"], 50.0)


if __name__ == "__main__":
    unittest.main()
