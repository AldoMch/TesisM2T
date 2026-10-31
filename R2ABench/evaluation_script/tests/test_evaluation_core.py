import csv
import errno
import io
import json
import os
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest.mock import patch

from evaluation_script import evaluate as evaluate_cli
from evaluation_script import l1_structural
from evaluation_script import l0_syntax
from evaluation_script.l2_semantic import L2JudgeConfig, _flatten_l2, empty_l2_result
from evaluation_script.l0_syntax import _plantuml_command, evaluate_l0
from evaluation_script.l1_structural import L1AlignmentConfig, evaluate_l1
from evaluation_script.pipeline import (
    evaluate_files,
    evaluate_pair,
    load_resume_rows,
    write_csv,
)
from evaluation_script.plantuml_parser import PlantUMLParser


VALID_PUML = """@startuml
package "Backend" {
  [API Service] as API
}
database "Main DB" as DB
API --> DB : reads/writes
@enduml
"""


def _seal_fixture_cache(path):
    """Attach actual fixture input/prompt provenance; no validation is bypassed."""
    path = Path(path)
    root = next(parent for parent in path.parents if parent.name.startswith("tmp"))
    predictions = list(path.parent.glob("*.puml"))
    pred = next(p for p in predictions if p.name in {"predicted.puml", "pred.puml"})
    reference = next(
        p
        for p in root.rglob("*.puml")
        if p != pred and p.name in {"ad.puml", "gt.puml"}
    )
    reqs = list(root.rglob("checked_srs.md"))
    requirements = reqs[0].read_text(encoding="utf-8") if reqs else ""
    data = json.loads(path.read_text(encoding="utf-8"))
    prefix = "judge_alignment_v2_"
    model = path.stem[len(prefix) :] if path.stem.startswith(prefix) else None
    parser = PlantUMLParser()
    data["_provenance"] = dict(
        model=model,
        fingerprint=l1_structural._alignment_fingerprint(
            requirements,
            parser.parse(reference.read_text(encoding="utf-8")),
            parser.parse(pred.read_text(encoding="utf-8")),
        ),
    )
    path.write_text(json.dumps(data), encoding="utf-8")


class EvaluationCoreTests(unittest.TestCase):
    def test_l0_rejects_failed_plantuml_render(self):
        def syntax_checker(_puml_code):
            return False, "PlantUML render failed: missing @enduml"

        result = evaluate_l0("@startuml\n[A] --> [B]\n", syntax_checker=syntax_checker)

        self.assertFalse(result.passed)
        self.assertEqual(result.errors, ["PlantUML render failed: missing @enduml"])

    def test_l0_allows_renderable_non_component_keywords(self):
        puml = """@startuml
class UserService
class UserRepository
UserService --> UserRepository
@enduml
"""

        result = evaluate_l0(puml, syntax_checker=lambda _puml_code: (True, ""))

        self.assertTrue(result.passed)
        self.assertEqual(result.errors, [])
        self.assertFalse(hasattr(result, "diagram_type"))
        self.assertEqual(result.node_count, 2)
        self.assertEqual(result.edge_count, 1)

    def test_l0_plantuml_command_strips_quotes_from_windows_paths(self):
        with tempfile.TemporaryDirectory() as tmp:
            jar = str(Path(tmp) / "directory with spaces" / "plantuml.jar")
            with patch.dict("os.environ", {"PLANTUML_CMD": f'java -jar "{jar}"'}, clear=True):
                command = _plantuml_command()
            self.assertEqual(command, ["java", "-jar", jar])

    def test_l0_main_reports_result_for_path(self):
        with tempfile.TemporaryDirectory() as tmp:
            puml_path = Path(tmp) / "candidate.puml"
            puml_path.write_text(VALID_PUML, encoding="utf-8")
            output = io.StringIO()

            with patch(
                "evaluation_script.l0_syntax.check_plantuml_renderable",
                return_value=(True, ""),
            ):
                with redirect_stdout(output):
                    exit_code = l0_syntax.main([str(puml_path)])

        self.assertEqual(exit_code, 0)
        text = output.getvalue()
        self.assertIn("passed: True", text)
        self.assertNotIn("diagram_type", text)
        self.assertIn("node_count: 3", text)
        self.assertIn("edge_count: 1", text)

    def test_l0_script_can_run_directly(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            puml_path = tmp_path / "candidate.puml"
            puml_path.write_text(VALID_PUML, encoding="utf-8")
            fake_plantuml = tmp_path / "fake_plantuml.py"
            fake_plantuml.write_text(
                "from pathlib import Path\n"
                "import sys\n"
                "out_dir = Path(sys.argv[sys.argv.index('-o') + 1])\n"
                "out_dir.mkdir(exist_ok=True)\n"
                "(out_dir / 'candidate.svg').write_text('<svg/>', encoding='utf-8')\n",
                encoding="utf-8",
            )
            script_path = Path(__file__).resolve().parents[1] / "l0_syntax.py"
            env = os.environ.copy()
            env["PLANTUML_CMD"] = f'"{sys.executable}" "{fake_plantuml}"'
            env.pop("PLANTUML_JAR", None)

            completed = subprocess.run(
                [sys.executable, str(script_path), str(puml_path)],
                cwd=script_path.parents[1],
                env=env,
                capture_output=True,
                text=True,
                check=False,
            )

        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertIn("passed: True", completed.stdout)
        self.assertIn("edge_count: 1", completed.stdout)

    def test_l1_scores_identical_diagrams_as_perfect_alignment(self):
        alignment_data = {
            "matched_pairs": [
                {
                    "gt_nodes": ["Backend::API Service"],
                    "predicted_nodes": ["Backend::API Service"],
                    "match_type": "1:1",
                    "is_boundary_correct": True,
                },
                {
                    "gt_nodes": ["Global::Main DB"],
                    "predicted_nodes": ["Global::Main DB"],
                    "match_type": "1:1",
                    "is_boundary_correct": True,
                },
            ],
            "unmatched_gt_nodes": [],
            "unmatched_predicted_nodes": [],
            "reference_node_coverage": [
                {
                    "gt_node": "Backend::API Service",
                    "covered": True,
                    "covering_predicted_nodes": ["Backend::API Service"],
                },
                {
                    "gt_node": "Global::Main DB",
                    "covered": True,
                    "covering_predicted_nodes": ["Global::Main DB"],
                },
            ],
            "predicted_node_grounding": [
                {
                    "predicted_node": "Backend::API Service",
                    "grounded": True,
                    "reference_nodes": ["Backend::API Service"],
                },
                {
                    "predicted_node": "Global::Main DB",
                    "grounded": True,
                    "reference_nodes": ["Global::Main DB"],
                },
            ],
        }

        result = evaluate_l1(VALID_PUML, VALID_PUML, alignment_data=alignment_data)

        self.assertEqual(result["l1_gen_precision"], 1.0)
        self.assertEqual(result["l1_node_coverage"], 1.0)
        self.assertNotIn("l1_node_f1", result)
        self.assertEqual(result["l1_edge_precision"], 1.0)
        self.assertEqual(result["l1_edge_recall"], 1.0)
        self.assertEqual(result["l1_edge_f1"], 1.0)
        self.assertEqual(result["l1_boundary_accuracy"], 1.0)

    def test_l1_reports_reference_coverage_and_generated_precision_independently(self):
        gt = """@startuml
[Login Service] as Login
[Register Service] as Register
[Payment Service] as Payment
[Audit Service] as Audit
@enduml
"""
        pred = """@startuml
[Auth Service] as Auth
[Alipay Service] as Alipay
[WeChat Service] as WeChat
[Kafka] as Kafka
[Redis] as Redis
@enduml
"""
        alignment_data = {
            "matched_pairs": [
                {
                    "gt_nodes": ["Global::Login Service", "Global::Register Service"],
                    "predicted_nodes": ["Global::Auth Service"],
                    "match_type": "N:1",
                    "is_boundary_correct": True,
                },
                {
                    "gt_nodes": ["Global::Payment Service"],
                    "predicted_nodes": [
                        "Global::Alipay Service",
                        "Global::WeChat Service",
                    ],
                    "match_type": "1:N",
                    "is_boundary_correct": True,
                },
            ],
            "unmatched_gt_nodes": ["Global::Audit Service"],
            "unmatched_predicted_nodes": ["Global::Kafka", "Global::Redis"],
            "reference_node_coverage": [
                {
                    "gt_node": "Global::Audit Service",
                    "covered": False,
                    "covering_predicted_nodes": [],
                },
                {
                    "gt_node": "Global::Login Service",
                    "covered": True,
                    "covering_predicted_nodes": ["Global::Auth Service"],
                },
                {
                    "gt_node": "Global::Payment Service",
                    "covered": True,
                    "covering_predicted_nodes": [
                        "Global::Alipay Service",
                        "Global::WeChat Service",
                    ],
                },
                {
                    "gt_node": "Global::Register Service",
                    "covered": True,
                    "covering_predicted_nodes": ["Global::Auth Service"],
                },
            ],
            "predicted_node_grounding": [
                {
                    "predicted_node": "Global::Alipay Service",
                    "grounded": True,
                    "reference_nodes": ["Global::Payment Service"],
                },
                {
                    "predicted_node": "Global::Auth Service",
                    "grounded": True,
                    "reference_nodes": [
                        "Global::Login Service",
                        "Global::Register Service",
                    ],
                },
                {
                    "predicted_node": "Global::Kafka",
                    "grounded": False,
                    "reference_nodes": [],
                },
                {
                    "predicted_node": "Global::Redis",
                    "grounded": False,
                    "reference_nodes": [],
                },
                {
                    "predicted_node": "Global::WeChat Service",
                    "grounded": True,
                    "reference_nodes": ["Global::Payment Service"],
                },
            ],
        }

        result = evaluate_l1(pred, gt, alignment_data=alignment_data)

        self.assertEqual(result["l1_node_coverage"], 0.75)
        self.assertEqual(result["l1_gen_precision"], 0.6)
        self.assertNotIn("l1_node_f1", result)

    def test_l1_requires_alignment_data_cache_or_judge(self):
        with self.assertRaises(l1_structural.L1AlignmentError):
            evaluate_l1(VALID_PUML, VALID_PUML)

    def test_l1_does_not_fallback_to_heuristic_when_judge_key_is_missing(self):
        config = L1AlignmentConfig(enabled=True, model="gpt-4o-mini")

        with self.assertRaises(l1_structural.L1AlignmentError):
            evaluate_l1(VALID_PUML, VALID_PUML, alignment_config=config)

    def test_l1_alignment_prompt_includes_split_merge_example(self):
        prompt = l1_structural._build_alignment_prompt(
            "Demo PRD",
            ["Data Layer::User DB"],
            ["Database::MySQL_User", "Database::Redis_User"],
        )

        self.assertIn('"gt_node": "r1"', prompt)
        self.assertIn('"r1": "Data Layer::User DB"', prompt)
        self.assertIn('"p1": "Database::MySQL_User"', prompt)
        self.assertIn("split into finer components", prompt)

    def test_l1_main_outputs_json_metrics(self):
        alignment_data = {
            "matched_pairs": [
                {
                    "gt_nodes": ["Backend::API Service"],
                    "predicted_nodes": ["Backend::API Service"],
                    "match_type": "1:1",
                    "is_boundary_correct": True,
                },
                {
                    "gt_nodes": ["Global::Main DB"],
                    "predicted_nodes": ["Global::Main DB"],
                    "match_type": "1:1",
                    "is_boundary_correct": True,
                },
            ],
            "unmatched_gt_nodes": [],
            "unmatched_predicted_nodes": [],
            "reference_node_coverage": [
                {
                    "gt_node": "Backend::API Service",
                    "covered": True,
                    "covering_predicted_nodes": ["Backend::API Service"],
                },
                {
                    "gt_node": "Global::Main DB",
                    "covered": True,
                    "covering_predicted_nodes": ["Global::Main DB"],
                },
            ],
            "predicted_node_grounding": [
                {
                    "predicted_node": "Backend::API Service",
                    "grounded": True,
                    "reference_nodes": ["Backend::API Service"],
                },
                {
                    "predicted_node": "Global::Main DB",
                    "grounded": True,
                    "reference_nodes": ["Global::Main DB"],
                },
            ],
        }
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            pred = root / "predicted.puml"
            gt = root / "ad.puml"
            alignment_cache = root / "alignment.json"
            pred.write_text(VALID_PUML, encoding="utf-8")
            gt.write_text(VALID_PUML, encoding="utf-8")
            alignment_cache.write_text(json.dumps(alignment_data), encoding="utf-8")
            _seal_fixture_cache(alignment_cache)
            output = io.StringIO()

            with redirect_stdout(output):
                exit_code = l1_structural.main(
                    [
                        "--pred",
                        str(pred),
                        "--gt",
                        str(gt),
                        "--alignment-cache",
                        str(alignment_cache),
                    ]
                )

        result = json.loads(output.getvalue())
        self.assertEqual(exit_code, 0)
        self.assertEqual(result["l1_status"], "completed")
        self.assertEqual(result["l1_node_coverage"], 1.0)
        self.assertEqual(result["l1_gen_precision"], 1.0)
        self.assertEqual(result["l1_edge_f1"], 1.0)

    def test_l1_main_returns_error_when_alignment_is_unavailable(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            pred = root / "predicted.puml"
            gt = root / "ad.puml"
            pred.write_text(VALID_PUML, encoding="utf-8")
            gt.write_text(VALID_PUML, encoding="utf-8")
            output = io.StringIO()
            error = io.StringIO()

            with redirect_stdout(output), redirect_stderr(error):
                exit_code = l1_structural.main(["--pred", str(pred), "--gt", str(gt)])

        self.assertEqual(exit_code, 2)
        self.assertEqual(output.getvalue(), "")
        self.assertIn("L1 alignment required", error.getvalue())

    def test_l1_structural_treats_all_split_predicted_nodes_as_mapped(self):
        gt = """@startuml
database "User DB" as UDB
@enduml
"""
        pred = """@startuml
database "MySQL_User" as MYSQL
database "Redis_User" as REDIS
@enduml
"""
        alignment_data = {
            "matched_pairs": [
                {
                    "gt_nodes": ["Global::User DB"],
                    "predicted_nodes": ["Global::MySQL_User", "Global::Redis_User"],
                    "match_type": "1:N",
                    "is_boundary_correct": True,
                }
            ],
            "unmatched_gt_nodes": [],
            "unmatched_predicted_nodes": [],
            "reference_node_coverage": [
                {
                    "gt_node": "Global::User DB",
                    "covered": True,
                    "covering_predicted_nodes": [
                        "Global::MySQL_User",
                        "Global::Redis_User",
                    ],
                }
            ],
            "predicted_node_grounding": [
                {
                    "predicted_node": "Global::MySQL_User",
                    "grounded": True,
                    "reference_nodes": ["Global::User DB"],
                },
                {
                    "predicted_node": "Global::Redis_User",
                    "grounded": True,
                    "reference_nodes": ["Global::User DB"],
                },
            ],
        }

        result = evaluate_l1(pred, gt, alignment_data=alignment_data)

        self.assertEqual(result["l1_structural_similarity"], 100.0)
        self.assertEqual(result["l1_structural_discrepancy"], 0.0)
        self.assertEqual(result["l1_unmatched_predicted_node_count"], 0)

    def test_l1_outputs_structural_error_breakdown(self):
        gt = """@startuml
[A] as A
[B] as B
A --> B
@enduml
"""
        pred = """@startuml
[A] as A
[Extra] as Extra
A --> Extra
@enduml
"""
        alignment_data = {
            "matched_pairs": [
                {
                    "gt_nodes": ["Global::A"],
                    "predicted_nodes": ["Global::A"],
                    "match_type": "1:1",
                    "is_boundary_correct": True,
                }
            ],
            "unmatched_gt_nodes": ["Global::B"],
            "unmatched_predicted_nodes": ["Global::Extra"],
            "reference_node_coverage": [
                {
                    "gt_node": "Global::A",
                    "covered": True,
                    "covering_predicted_nodes": ["Global::A"],
                },
                {
                    "gt_node": "Global::B",
                    "covered": False,
                    "covering_predicted_nodes": [],
                },
            ],
            "predicted_node_grounding": [
                {
                    "predicted_node": "Global::A",
                    "grounded": True,
                    "reference_nodes": ["Global::A"],
                },
                {
                    "predicted_node": "Global::Extra",
                    "grounded": False,
                    "reference_nodes": [],
                },
            ],
        }

        result = evaluate_l1(pred, gt, alignment_data=alignment_data)

        self.assertEqual(result["l1_unmatched_reference_node_count"], 1)
        self.assertEqual(result["l1_unmatched_predicted_node_count"], 1)
        self.assertEqual(result["l1_unmatched_reference_edge_count"], 1)
        self.assertEqual(result["l1_unmatched_predicted_edge_count"], 1)

    def test_l1_judge_candidates_include_component_containers_but_not_pure_packages(
        self,
    ):
        gt = """@startuml
database "User DB" {
  component "MySQL" as MYSQL
}
package "Backend" {
  component "API" as API
}
@enduml
"""
        pred = """@startuml
database "MySQL_User" as MYSQL
component "API Service" as API
@enduml
"""
        captured = {}

        def fake_judge(**kwargs):
            captured["gt_nodes"] = kwargs["gt_nodes"]
            captured["predicted_nodes"] = kwargs["predicted_nodes"]
            return {
                "reference_node_coverage": [
                    dict(gt_node=n, covered=False, covering_predicted_nodes=[])
                    for n in kwargs["gt_nodes"]
                ],
                "predicted_node_grounding": [
                    dict(predicted_node=n, grounded=False, reference_nodes=[])
                    for n in kwargs["predicted_nodes"]
                ],
                "matched_pairs": [],
                "unmatched_gt_nodes": kwargs["gt_nodes"],
                "unmatched_predicted_nodes": kwargs["predicted_nodes"],
            }

        parser = PlantUMLParser()
        with patch(
            "evaluation_script.l1_structural._call_alignment_judge",
            side_effect=fake_judge,
        ):
            l1_structural._resolve_alignment_data(
                requirements_text="",
                gt=parser.parse(gt),
                pred=parser.parse(pred),
                config=L1AlignmentConfig(
                    enabled=True, model="gpt-4o-mini", api_key="test-key"
                ),
                cache_path=None,
            )

        self.assertIn("Global::User DB", captured["gt_nodes"])
        self.assertIn("User DB::MySQL", captured["gt_nodes"])
        self.assertIn("Backend::API", captured["gt_nodes"])
        self.assertNotIn("Global::Backend", captured["gt_nodes"])

    def test_parser_treats_database_and_interface_blocks_as_boundaries(self):
        puml = """@startuml
database "Database" {
  component "MySQL" as MYSQL
}
interface "API Boundary" {
  component "REST API" as API
}
@enduml
"""

        parsed = PlantUMLParser().parse(puml)

        self.assertIn("Global::Database", parsed.nodes)
        self.assertIn("Database::MySQL", parsed.nodes)
        self.assertIn("Global::API Boundary", parsed.nodes)
        self.assertIn("API Boundary::REST API", parsed.nodes)

    def test_l1_main_writes_model_named_alignment_cache_next_to_prediction(self):
        gt = """@startuml
package "Backend" {
  [Authentication Service] as Auth
}
@enduml
"""
        pred_text = """@startuml
package "Services" {
  [Login API] as Login
}
@enduml
"""
        alignment_data = {
            "matched_pairs": [
                {
                    "gt_nodes": ["Backend::Authentication Service"],
                    "predicted_nodes": ["Services::Login API"],
                    "match_type": "1:1",
                    "is_boundary_correct": True,
                }
            ],
            "unmatched_gt_nodes": [],
            "unmatched_predicted_nodes": [],
            "reference_node_coverage": [
                {
                    "gt_node": "Backend::Authentication Service",
                    "covered": True,
                    "covering_predicted_nodes": ["Services::Login API"],
                }
            ],
            "predicted_node_grounding": [
                {
                    "predicted_node": "Services::Login API",
                    "grounded": True,
                    "reference_nodes": ["Backend::Authentication Service"],
                }
            ],
        }
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            pred = root / "sample" / "predicted.puml"
            gt_path = root / "ad.puml"
            pred.parent.mkdir()
            pred.write_text(pred_text, encoding="utf-8")
            gt_path.write_text(gt, encoding="utf-8")
            output = io.StringIO()

            with patch.dict(os.environ, {"TEST_OPENAI_KEY": "test-key"}):
                with patch(
                    "evaluation_script.l1_structural._call_alignment_judge",
                    return_value=alignment_data,
                ):
                    with redirect_stdout(output):
                        exit_code = l1_structural.main(
                            [
                                "--pred",
                                str(pred),
                                "--gt",
                                str(gt_path),
                                "--enable-judge",
                                "--llm-model",
                                "gpt-4o-mini",
                                "--llm-api-key-env",
                                "TEST_OPENAI_KEY",
                            ]
                        )

            cache_path = pred.parent / "judge_alignment_v2_gpt-4o-mini.json"
            cache_exists = cache_path.exists()
            o3_cache_exists = (pred.parent / "judge_alignment_v2_o3.json").exists()

        result = json.loads(output.getvalue())
        self.assertEqual(exit_code, 0)
        self.assertNotIn("l1_alignment_source", result)
        self.assertNotIn("l1_alignment_error", result)
        self.assertEqual(result["l1_node_coverage"], 1.0)
        self.assertEqual(result["l1_gen_precision"], 1.0)
        self.assertTrue(cache_exists)
        self.assertFalse(o3_cache_exists)

    def test_l1_uses_r2abench_alignment_data_for_semantic_matches(self):
        gt = """@startuml
package "Backend" {
  [Authentication Service] as Auth
  [Billing Service] as Billing
}
Auth --> Billing : validates account
@enduml
"""
        pred = """@startuml
package "Services" {
  [Login API] as Login
  [Payment Module] as Payment
}
Login --> Payment : validates account
@enduml
"""
        alignment_data = {
            "matched_pairs": [
                {
                    "gt_nodes": ["Backend::Authentication Service"],
                    "predicted_nodes": ["Services::Login API"],
                    "match_type": "1:1",
                    "is_boundary_correct": False,
                },
                {
                    "gt_nodes": ["Backend::Billing Service"],
                    "predicted_nodes": ["Services::Payment Module"],
                    "match_type": "1:1",
                    "is_boundary_correct": True,
                },
            ],
            "unmatched_gt_nodes": [],
            "unmatched_predicted_nodes": [],
            "reference_node_coverage": [
                {
                    "gt_node": "Backend::Authentication Service",
                    "covered": True,
                    "covering_predicted_nodes": ["Services::Login API"],
                },
                {
                    "gt_node": "Backend::Billing Service",
                    "covered": True,
                    "covering_predicted_nodes": ["Services::Payment Module"],
                },
            ],
            "predicted_node_grounding": [
                {
                    "predicted_node": "Services::Login API",
                    "grounded": True,
                    "reference_nodes": ["Backend::Authentication Service"],
                },
                {
                    "predicted_node": "Services::Payment Module",
                    "grounded": True,
                    "reference_nodes": ["Backend::Billing Service"],
                },
            ],
        }

        result = evaluate_l1(pred, gt, alignment_data=alignment_data)

        self.assertEqual(result["l1_gen_precision"], 1.0)
        self.assertEqual(result["l1_node_coverage"], 1.0)
        self.assertEqual(result["l1_edge_precision"], 1.0)
        self.assertEqual(result["l1_edge_recall"], 1.0)
        self.assertEqual(result["l1_boundary_accuracy"], 0.5)
        self.assertEqual(result["l1_structural_similarity"], 87.5)
        self.assertEqual(result["l1_matched_node_count"], 2)
        self.assertEqual(result["l1_unmatched_predicted_node_count"], 0)
        self.assertEqual(result["l1_unmatched_reference_node_count"], 0)

    def test_pipeline_short_circuits_when_l0_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            pred = Path(tmp) / "bad.puml"
            pred.write_text("@startuml\n[A] --> [B]\n", encoding="utf-8")

            with patch(
                "evaluation_script.pipeline.evaluate_l0",
                side_effect=lambda puml: evaluate_l0(
                    puml,
                    syntax_checker=lambda _puml_code: (
                        False,
                        "PlantUML render failed: missing @enduml",
                    ),
                ),
            ):
                row = evaluate_pair(
                    pred_path=pred, gt_path=None, requirements_path=None
                )

            self.assertFalse(row["l0_valid"])
            self.assertEqual(row["stage_status"], "failed_l0")
            self.assertIsNone(row["l1_node_coverage"])
            self.assertIsNone(row["l1_gen_precision"])
            self.assertIsNone(row["l2_completeness_score"])
            self.assertNotIn("l3_scenario_support_score", row)

    def test_pipeline_records_l1_failure_and_still_runs_l2(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            pred = root / "predicted.puml"
            gt = root / "gt.puml"
            requirements = root / "checked_srs.md"
            pred.write_text(VALID_PUML, encoding="utf-8")
            gt.write_text(VALID_PUML, encoding="utf-8")
            requirements.write_text(
                "# Demo SRS\n\nThe system should remain secure.", encoding="utf-8"
            )

            with patch(
                "evaluation_script.pipeline.evaluate_l0",
                side_effect=lambda puml: evaluate_l0(
                    puml, syntax_checker=lambda _puml_code: (True, "")
                ),
            ):
                with patch(
                    "evaluation_script.pipeline.evaluate_l1",
                    side_effect=l1_structural.L1AlignmentError(
                        "judge_failed: The read operation timed out"
                    ),
                ):
                    with patch(
                        "evaluation_script.pipeline.evaluate_l2",
                        return_value={
                            "l2_status": "completed",
                            "l2_completeness_score": 4,
                        },
                    ):
                        row = evaluate_pair(
                            pred_path=pred,
                            gt_path=gt,
                            requirements_path=requirements,
                            l1_config=L1AlignmentConfig(
                                enabled=True, model="gemini-2.5-pro", api_key="key"
                            ),
                        )

        self.assertEqual(row["stage_status"], "completed_with_l1_error")
        self.assertEqual(row["l1_status"], "failed")
        self.assertIn("read operation timed out", row["l1_error"])
        self.assertEqual(row["l2_status"], "completed")
        self.assertEqual(row["l2_completeness_score"], 4)

    def test_evaluate_files_logs_project_and_stage_progress(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            dataset = root / "Dataset" / "C-R2A-17"
            project = dataset / "Python" / "demo"
            reference = project / "AD" / "ad.puml"
            requirements = project / "checked_srs.md"
            reference.parent.mkdir(parents=True)
            reference.write_text(VALID_PUML, encoding="utf-8")
            requirements.write_text(
                "# Demo SRS\n\nThe system should remain secure.", encoding="utf-8"
            )

            pred_root = root / "Outputs" / "RQ1" / "C-R2A-17"
            pred = pred_root / "direct" / "gpt-5" / "demo" / "predicted.puml"
            pred.parent.mkdir(parents=True)
            pred.write_text(VALID_PUML, encoding="utf-8")
            (pred.parent / "judge_alignment_v2_gpt-5.json").write_text(
                json.dumps(
                    {
                        "matched_pairs": [
                            {
                                "gt_nodes": ["Backend::API Service"],
                                "predicted_nodes": ["Backend::API Service"],
                                "match_type": "1:1",
                                "is_boundary_correct": True,
                            },
                            {
                                "gt_nodes": ["Global::Main DB"],
                                "predicted_nodes": ["Global::Main DB"],
                                "match_type": "1:1",
                                "is_boundary_correct": True,
                            },
                        ],
                        "unmatched_gt_nodes": [],
                        "unmatched_predicted_nodes": [],
                        "reference_node_coverage": [
                            {
                                "gt_node": "Backend::API Service",
                                "covered": True,
                                "covering_predicted_nodes": ["Backend::API Service"],
                            },
                            {
                                "gt_node": "Global::Main DB",
                                "covered": True,
                                "covering_predicted_nodes": ["Global::Main DB"],
                            },
                        ],
                        "predicted_node_grounding": [
                            {
                                "predicted_node": "Backend::API Service",
                                "grounded": True,
                                "reference_nodes": ["Backend::API Service"],
                            },
                            {
                                "predicted_node": "Global::Main DB",
                                "grounded": True,
                                "reference_nodes": ["Global::Main DB"],
                            },
                        ],
                    }
                ),
                encoding="utf-8",
            )
            _seal_fixture_cache(pred.parent / "judge_alignment_v2_gpt-5.json")
            logs = []

            with patch(
                "evaluation_script.pipeline.evaluate_l0",
                side_effect=lambda puml: evaluate_l0(
                    puml, syntax_checker=lambda _puml_code: (True, "")
                ),
            ):
                evaluate_files(
                    [pred],
                    dataset_dir=dataset,
                    l1_config=L1AlignmentConfig(model="gpt-5"),
                    pred_root=pred_root,
                    progress_logger=logs.append,
                )

        joined = "\n".join(logs)
        self.assertIn("[eval 1/1]", joined)
        self.assertIn("sample=demo", joined)
        self.assertIn("candidate=direct/gpt-5", joined)
        self.assertIn("workflow=direct", joined)
        self.assertIn("model=gpt-5", joined)
        self.assertIn("language=Python", joined)
        self.assertIn("stage=L0 status=start", joined)
        self.assertIn("stage=L1 status=start", joined)
        self.assertIn("stage=L2 status=start", joined)
        self.assertIn("stage=sample status=completed", joined)

    def test_evaluate_files_reuses_resume_row_when_l0_already_valid(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            pred_root = root / "Outputs" / "RQ1" / "C-R2A-17"
            pred = pred_root / "direct" / "gpt-5" / "demo" / "predicted.puml"
            pred.parent.mkdir(parents=True)
            pred.write_text(VALID_PUML, encoding="utf-8")
            resume_csv = root / "results.csv"
            write_csv(
                [
                    {
                        "sample_id": "demo",
                        "candidate_id": "direct/gpt-5",
                        "l0_valid": True,
                        "l1_metric_version": "l1-correspondence-v2",
                        "stage_status": "completed",
                        "l2_status": "completed",
                    }
                ],
                resume_csv,
            )

            with patch(
                "evaluation_script.pipeline.evaluate_l0",
                side_effect=AssertionError(
                    "L0 should not run when resume row is already L0-valid"
                ),
            ):
                resumed_rows = evaluate_files(
                    [pred],
                    pred_root=pred_root,
                    resume_rows=load_resume_rows(resume_csv),
                )

        self.assertEqual(resumed_rows[0]["sample_id"], "demo")
        self.assertEqual(resumed_rows[0]["candidate_id"], "direct/gpt-5")
        self.assertTrue(resumed_rows[0]["l0_valid"])
        self.assertEqual(resumed_rows[0]["l2_status"], "completed")

    def test_evaluate_files_reruns_when_resume_row_failed_l0(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            pred_root = root / "Outputs" / "RQ1" / "C-R2A-17"
            pred = pred_root / "direct" / "gpt-5" / "demo" / "predicted.puml"
            pred.parent.mkdir(parents=True)
            pred.write_text(VALID_PUML, encoding="utf-8")
            resume_csv = root / "results.csv"
            write_csv(
                [
                    {
                        "sample_id": "demo",
                        "candidate_id": "direct/gpt-5",
                        "l0_valid": False,
                        "stage_status": "failed_l0",
                        "l2_status": "skipped_l0_failed",
                    }
                ],
                resume_csv,
            )
            l0_calls = []

            def fake_l0(puml):
                l0_calls.append(puml)
                return evaluate_l0(puml, syntax_checker=lambda _puml_code: (True, ""))

            with patch("evaluation_script.pipeline.evaluate_l0", side_effect=fake_l0):
                rows = evaluate_files(
                    [pred],
                    pred_root=pred_root,
                    resume_rows=load_resume_rows(resume_csv),
                )

        self.assertEqual(len(l0_calls), 1)
        self.assertEqual(rows[0]["stage_status"], "completed")

    def test_l2_empty_result_only_exposes_selected_secondary_metrics(self):
        result = empty_l2_result("skipped_disabled")

        self.assertIn("l2_requirement_coverage", result)
        self.assertIn("l2_asr_coverage", result)
        self.assertIn("l2_unsupported_inference_rate", result)
        self.assertNotIn("l2_quality_scenario_support", result)
        self.assertNotIn("l2_risks", result)
        self.assertNotIn("l2_sensitivity_points", result)
        self.assertNotIn("l2_tradeoff_points", result)

    def test_l2_flatten_ignores_removed_metrics_and_unvalidated_reqcov(self):
        parsed = {
            "scores": {
                "completeness": {"score": 4, "reasoning": "Covers major flows."},
                "faithfulness": {
                    "score": 3,
                    "reasoning": "One relation is weakly supported.",
                },
            },
            "metrics": {
                "requirement_coverage": 0.8,
                "asr_coverage": 0.6,
                "quality_scenario_support": 0.7,
                "unsupported_inference_rate": 0.2,
            },
            "risks": ["Session storage is unspecified."],
            "sensitivity_points": ["Token lifetime"],
            "tradeoff_points": ["Security vs usability"],
        }

        result = _flatten_l2(parsed)

        self.assertIsNone(result["l2_requirement_coverage"])
        self.assertEqual(result["l2_asr_coverage"], 0.6)
        self.assertEqual(result["l2_unsupported_inference_rate"], 0.2)
        self.assertNotIn("l2_quality_scenario_support", result)
        self.assertNotIn("l2_risks", result)
        self.assertNotIn("l2_sensitivity_points", result)
        self.assertNotIn("l2_tradeoff_points", result)



    def test_evaluate_files_matches_c_r2a_17_layout(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            dataset = root / "Dataset" / "C-R2A-17"
            project = dataset / "Python" / "demo"
            reference = project / "AD" / "ad.puml"
            requirements = project / "checked_srs.md"
            reference.parent.mkdir(parents=True)
            reference.write_text(VALID_PUML, encoding="utf-8")
            requirements.write_text(
                "# Demo SRS\n\nFunctional requirement.", encoding="utf-8"
            )

            pred_root = root / "Outputs" / "RQ1" / "C-R2A-17"
            pred = pred_root / "direct" / "gpt-5" / "demo" / "predicted.puml"
            pred.parent.mkdir(parents=True)
            pred.write_text(VALID_PUML, encoding="utf-8")
            alignment_data = {
                "matched_pairs": [
                    {
                        "gt_nodes": ["Backend::API Service"],
                        "predicted_nodes": ["Backend::API Service"],
                        "match_type": "1:1",
                        "is_boundary_correct": True,
                    },
                    {
                        "gt_nodes": ["Global::Main DB"],
                        "predicted_nodes": ["Global::Main DB"],
                        "match_type": "1:1",
                        "is_boundary_correct": True,
                    },
                ],
                "unmatched_gt_nodes": [],
                "unmatched_predicted_nodes": [],
                "reference_node_coverage": [
                    {
                        "gt_node": "Backend::API Service",
                        "covered": True,
                        "covering_predicted_nodes": ["Backend::API Service"],
                    },
                    {
                        "gt_node": "Global::Main DB",
                        "covered": True,
                        "covering_predicted_nodes": ["Global::Main DB"],
                    },
                ],
                "predicted_node_grounding": [
                    {
                        "predicted_node": "Backend::API Service",
                        "grounded": True,
                        "reference_nodes": ["Backend::API Service"],
                    },
                    {
                        "predicted_node": "Global::Main DB",
                        "grounded": True,
                        "reference_nodes": ["Global::Main DB"],
                    },
                ],
            }
            (pred.parent / "judge_alignment_v2_gpt-5.json").write_text(
                json.dumps(alignment_data),
                encoding="utf-8",
            )
            _seal_fixture_cache(pred.parent / "judge_alignment_v2_gpt-5.json")
            l1_config = L1AlignmentConfig(model="gpt-5")

            with patch(
                "evaluation_script.pipeline.evaluate_l0",
                side_effect=lambda puml: evaluate_l0(
                    puml, syntax_checker=lambda _puml_code: (True, "")
                ),
            ):
                rows = evaluate_files(
                    [pred],
                    dataset_dir=dataset,
                    l1_config=l1_config,
                    pred_root=pred_root,
                )

        self.assertEqual(len(rows), 1)
        row = rows[0]
        self.assertEqual(row["sample_id"], "demo")
        self.assertEqual(row["candidate_id"], "direct/gpt-5")
        self.assertEqual(row["workflow"], "direct")
        self.assertEqual(row["model_id"], "gpt-5")
        self.assertEqual(row["project_language"], "Python")
        self.assertNotIn("pred_path", row)
        self.assertNotIn("gt_path", row)
        self.assertNotIn("requirements_path", row)
        self.assertNotIn("l0_diagram_type", row)
        self.assertNotIn("l1_alignment_source", row)
        self.assertNotIn("l1_alignment_error", row)
        self.assertEqual(row["l1_status"], "completed")

    def test_evaluate_files_matches_g_r2a_52_flat_layout(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            dataset = root / "Dataset" / "G-R2A-52"
            project = dataset / "s000001_3c90b51c"
            reference = project / "AD" / "ad.puml"
            requirements = project / "checked_srs.md"
            reference.parent.mkdir(parents=True)
            reference.write_text(VALID_PUML, encoding="utf-8")
            requirements.write_text(
                "# Demo SRS\n\nFunctional requirement.", encoding="utf-8"
            )

            invalid_project = dataset / "invalid" / "s000041_4e10c941"
            invalid_project.mkdir(parents=True)
            (invalid_project / "checked_srs.md").write_text(
                "# Invalid SRS", encoding="utf-8"
            )

            pred_root = root / "Outputs" / "RQ1" / "G-R2A-52"
            pred = (
                pred_root / "direct" / "gpt-5" / "s000001_3c90b51c" / "predicted.puml"
            )
            pred.parent.mkdir(parents=True)
            pred.write_text(VALID_PUML, encoding="utf-8")
            alignment_data = {
                "matched_pairs": [
                    {
                        "gt_nodes": ["Backend::API Service"],
                        "predicted_nodes": ["Backend::API Service"],
                        "match_type": "1:1",
                        "is_boundary_correct": True,
                    },
                    {
                        "gt_nodes": ["Global::Main DB"],
                        "predicted_nodes": ["Global::Main DB"],
                        "match_type": "1:1",
                        "is_boundary_correct": True,
                    },
                ],
                "unmatched_gt_nodes": [],
                "unmatched_predicted_nodes": [],
                "reference_node_coverage": [
                    {
                        "gt_node": "Backend::API Service",
                        "covered": True,
                        "covering_predicted_nodes": ["Backend::API Service"],
                    },
                    {
                        "gt_node": "Global::Main DB",
                        "covered": True,
                        "covering_predicted_nodes": ["Global::Main DB"],
                    },
                ],
                "predicted_node_grounding": [
                    {
                        "predicted_node": "Backend::API Service",
                        "grounded": True,
                        "reference_nodes": ["Backend::API Service"],
                    },
                    {
                        "predicted_node": "Global::Main DB",
                        "grounded": True,
                        "reference_nodes": ["Global::Main DB"],
                    },
                ],
            }
            (pred.parent / "judge_alignment_v2_gpt-5.json").write_text(
                json.dumps(alignment_data),
                encoding="utf-8",
            )
            _seal_fixture_cache(pred.parent / "judge_alignment_v2_gpt-5.json")
            l1_config = L1AlignmentConfig(model="gpt-5")

            with patch(
                "evaluation_script.pipeline.evaluate_l0",
                side_effect=lambda puml: evaluate_l0(
                    puml, syntax_checker=lambda _puml_code: (True, "")
                ),
            ):
                rows = evaluate_files(
                    [pred],
                    dataset_dir=dataset,
                    l1_config=l1_config,
                    pred_root=pred_root,
                )

        self.assertEqual(len(rows), 1)
        row = rows[0]
        self.assertEqual(row["sample_id"], "s000001_3c90b51c")
        self.assertEqual(row["candidate_id"], "direct/gpt-5")
        self.assertEqual(row["workflow"], "direct")
        self.assertEqual(row["model_id"], "gpt-5")
        self.assertEqual(row["project_language"], "G-R2A-52")
        self.assertEqual(row["l1_status"], "completed")
        self.assertNotIn("invalid", str(row.get("requirements_path", "")))

    def test_evaluate_files_does_not_call_l3_or_emit_l3_columns(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            dataset = root / "Dataset" / "C-R2A-17"
            project = dataset / "Python" / "demo"
            reference = project / "AD" / "ad.puml"
            requirements = project / "checked_srs.md"
            reference.parent.mkdir(parents=True)
            reference.write_text(VALID_PUML, encoding="utf-8")
            requirements.write_text(
                "# Demo SRS\n\nThe system should remain secure.", encoding="utf-8"
            )

            pred_root = root / "Outputs" / "RQ1" / "C-R2A-17"
            pred = pred_root / "direct" / "gpt-5" / "demo" / "predicted.puml"
            pred.parent.mkdir(parents=True)
            pred.write_text(VALID_PUML, encoding="utf-8")
            alignment_data = {
                "matched_pairs": [
                    {
                        "gt_nodes": ["Backend::API Service"],
                        "predicted_nodes": ["Backend::API Service"],
                        "match_type": "1:1",
                        "is_boundary_correct": True,
                    },
                    {
                        "gt_nodes": ["Global::Main DB"],
                        "predicted_nodes": ["Global::Main DB"],
                        "match_type": "1:1",
                        "is_boundary_correct": True,
                    },
                ],
                "unmatched_gt_nodes": [],
                "unmatched_predicted_nodes": [],
                "reference_node_coverage": [
                    {
                        "gt_node": "Backend::API Service",
                        "covered": True,
                        "covering_predicted_nodes": ["Backend::API Service"],
                    },
                    {
                        "gt_node": "Global::Main DB",
                        "covered": True,
                        "covering_predicted_nodes": ["Global::Main DB"],
                    },
                ],
                "predicted_node_grounding": [
                    {
                        "predicted_node": "Backend::API Service",
                        "grounded": True,
                        "reference_nodes": ["Backend::API Service"],
                    },
                    {
                        "predicted_node": "Global::Main DB",
                        "grounded": True,
                        "reference_nodes": ["Global::Main DB"],
                    },
                ],
            }
            (pred.parent / "judge_alignment_v2_gpt-5.json").write_text(
                json.dumps(alignment_data),
                encoding="utf-8",
            )
            _seal_fixture_cache(pred.parent / "judge_alignment_v2_gpt-5.json")
            l1_config = L1AlignmentConfig(model="gpt-5")

            with patch(
                "evaluation_script.pipeline.evaluate_l0",
                side_effect=lambda puml: evaluate_l0(
                    puml, syntax_checker=lambda _puml_code: (True, "")
                ),
            ):
                rows = evaluate_files(
                    [pred],
                    dataset_dir=dataset,
                    l1_config=l1_config,
                    pred_root=pred_root,
                )
            scenario_cache_exists = (project / "l3_scenario_gpt-5.json").exists()

        self.assertFalse(any(key.startswith("l3_") for key in rows[0]))
        self.assertFalse(scenario_cache_exists)

    def test_evaluate_files_uses_cached_alignment_for_requested_model(self):
        gt = """@startuml
package "Backend" {
  [Authentication Service] as Auth
  [Billing Service] as Billing
}
Auth --> Billing
@enduml
"""
        pred_text = """@startuml
package "Services" {
  [Login API] as Login
  [Payment Module] as Payment
}
Login --> Payment
@enduml
"""
        alignment_data = {
            "matched_pairs": [
                {
                    "gt_nodes": ["Backend::Authentication Service"],
                    "predicted_nodes": ["Services::Login API"],
                    "match_type": "1:1",
                    "is_boundary_correct": False,
                },
                {
                    "gt_nodes": ["Backend::Billing Service"],
                    "predicted_nodes": ["Services::Payment Module"],
                    "match_type": "1:1",
                    "is_boundary_correct": True,
                },
            ],
            "unmatched_gt_nodes": [],
            "unmatched_predicted_nodes": [],
            "reference_node_coverage": [
                {
                    "gt_node": "Backend::Authentication Service",
                    "covered": True,
                    "covering_predicted_nodes": ["Services::Login API"],
                },
                {
                    "gt_node": "Backend::Billing Service",
                    "covered": True,
                    "covering_predicted_nodes": ["Services::Payment Module"],
                },
            ],
            "predicted_node_grounding": [
                {
                    "predicted_node": "Services::Login API",
                    "grounded": True,
                    "reference_nodes": ["Backend::Authentication Service"],
                },
                {
                    "predicted_node": "Services::Payment Module",
                    "grounded": True,
                    "reference_nodes": ["Backend::Billing Service"],
                },
            ],
        }
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            dataset = root / "Dataset" / "C-R2A-17"
            project = dataset / "Python" / "demo"
            reference = project / "AD" / "ad.puml"
            requirements = project / "checked_srs.md"
            reference.parent.mkdir(parents=True)
            reference.write_text(gt, encoding="utf-8")
            requirements.write_text("# Demo SRS", encoding="utf-8")

            pred_root = root / "Outputs" / "RQ1" / "C-R2A-17"
            pred = pred_root / "direct" / "gpt-5" / "demo" / "predicted.puml"
            pred.parent.mkdir(parents=True)
            pred.write_text(pred_text, encoding="utf-8")
            l1_config = L1AlignmentConfig(model="gpt-5")
            (pred.parent / "judge_alignment_v2_gpt-5.json").write_text(
                json.dumps(alignment_data),
                encoding="utf-8",
            )
            _seal_fixture_cache(pred.parent / "judge_alignment_v2_gpt-5.json")

            with patch(
                "evaluation_script.pipeline.evaluate_l0",
                side_effect=lambda puml: evaluate_l0(
                    puml, syntax_checker=lambda _puml_code: (True, "")
                ),
            ):
                rows = evaluate_files(
                    [pred],
                    dataset_dir=dataset,
                    l1_config=l1_config,
                    pred_root=pred_root,
                )

        self.assertEqual(rows[0]["l1_node_coverage"], 1.0)
        self.assertEqual(rows[0]["l1_gen_precision"], 1.0)
        self.assertEqual(rows[0]["l1_edge_f1"], 1.0)
        self.assertEqual(rows[0]["l1_boundary_accuracy"], 0.5)

    def test_evaluate_files_ignores_o3_alignment_when_another_model_is_requested(self):
        gt = """@startuml
package "Backend" {
  [Authentication Service] as Auth
}
@enduml
"""
        pred_text = """@startuml
package "Services" {
  [Login API] as Login
}
@enduml
"""
        alignment_data = {
            "matched_pairs": [
                {
                    "gt_nodes": ["Backend::Authentication Service"],
                    "predicted_nodes": ["Services::Login API"],
                    "match_type": "1:1",
                    "is_boundary_correct": True,
                }
            ],
            "unmatched_gt_nodes": [],
            "unmatched_predicted_nodes": [],
            "reference_node_coverage": [
                {
                    "gt_node": "Backend::Authentication Service",
                    "covered": True,
                    "covering_predicted_nodes": ["Services::Login API"],
                }
            ],
            "predicted_node_grounding": [
                {
                    "predicted_node": "Services::Login API",
                    "grounded": True,
                    "reference_nodes": ["Backend::Authentication Service"],
                }
            ],
        }
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            gt_dir = root / "gt"
            gt_dir.mkdir()
            (gt_dir / "demo.puml").write_text(gt, encoding="utf-8")

            pred_root = root / "predictions"
            pred = pred_root / "demo" / "predicted.puml"
            pred.parent.mkdir(parents=True)
            pred.write_text(pred_text, encoding="utf-8")
            (pred.parent / "judge_alignment_v2_o3.json").write_text(
                json.dumps(alignment_data),
                encoding="utf-8",
            )
            l1_config = L1AlignmentConfig(model="gpt-4o-mini")

            with patch(
                "evaluation_script.pipeline.evaluate_l0",
                side_effect=lambda puml: evaluate_l0(
                    puml, syntax_checker=lambda _puml_code: (True, "")
                ),
            ):
                with self.assertRaises(l1_structural.L1AlignmentError):
                    evaluate_files(
                        [pred], gt_dir=gt_dir, l1_config=l1_config, pred_root=pred_root
                    )

        self.assertFalse((pred.parent / "judge_alignment_v2_gpt-4o-mini.json").exists())

    def test_evaluate_files_does_not_use_o3_alignment_without_requested_model(self):
        gt = """@startuml
package "Backend" {
  [Authentication Service] as Auth
}
@enduml
"""
        pred_text = """@startuml
package "Services" {
  [Login API] as Login
}
@enduml
"""
        alignment_data = {
            "matched_pairs": [
                {
                    "gt_nodes": ["Backend::Authentication Service"],
                    "predicted_nodes": ["Services::Login API"],
                    "match_type": "1:1",
                    "is_boundary_correct": True,
                }
            ],
            "unmatched_gt_nodes": [],
            "unmatched_predicted_nodes": [],
            "reference_node_coverage": [
                {
                    "gt_node": "Backend::Authentication Service",
                    "covered": True,
                    "covering_predicted_nodes": ["Services::Login API"],
                }
            ],
            "predicted_node_grounding": [
                {
                    "predicted_node": "Services::Login API",
                    "grounded": True,
                    "reference_nodes": ["Backend::Authentication Service"],
                }
            ],
        }
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            gt_dir = root / "gt"
            gt_dir.mkdir()
            (gt_dir / "demo.puml").write_text(gt, encoding="utf-8")

            pred_root = root / "predictions"
            pred = pred_root / "demo" / "predicted.puml"
            pred.parent.mkdir(parents=True)
            pred.write_text(pred_text, encoding="utf-8")
            (pred.parent / "judge_alignment_v2_o3.json").write_text(
                json.dumps(alignment_data),
                encoding="utf-8",
            )

            with patch(
                "evaluation_script.pipeline.evaluate_l0",
                side_effect=lambda puml: evaluate_l0(
                    puml, syntax_checker=lambda _puml_code: (True, "")
                ),
            ):
                with self.assertRaises(l1_structural.L1AlignmentError):
                    evaluate_files([pred], gt_dir=gt_dir, pred_root=pred_root)

        self.assertFalse((pred.parent / "judge_alignment_v2_o3.json").exists())

    def test_l1_config_has_no_o3_default_without_model(self):
        with patch.dict(os.environ, {}, clear=True):
            config = L1AlignmentConfig.from_env(enabled=True)

        self.assertIsNone(config.model)
        self.assertEqual(config.base_url, "")

    def test_judge_configs_default_to_at_least_600_seconds(self):
        with patch.dict(os.environ, {}, clear=True):
            configs = [
                L1AlignmentConfig.from_env(enabled=True),
                L2JudgeConfig.from_env(enabled=True),
            ]

        for config in configs:
            self.assertGreaterEqual(config.timeout_seconds, 600)

    def test_evaluate_files_ignores_alignment_outside_prediction_directory(self):
        gt = """@startuml
package "Backend" {
  [Authentication Service] as Auth
  [Billing Service] as Billing
}
Auth --> Billing
@enduml
"""
        pred_text = """@startuml
package "Services" {
  [Login API] as Login
  [Payment Module] as Payment
}
Login --> Payment
@enduml
"""
        alignment_data = {
            "matched_pairs": [
                {
                    "gt_nodes": ["Backend::Authentication Service"],
                    "predicted_nodes": ["Services::Login API"],
                    "match_type": "1:1",
                    "is_boundary_correct": False,
                },
                {
                    "gt_nodes": ["Backend::Billing Service"],
                    "predicted_nodes": ["Services::Payment Module"],
                    "match_type": "1:1",
                    "is_boundary_correct": True,
                },
            ],
            "unmatched_gt_nodes": [],
            "unmatched_predicted_nodes": [],
            "reference_node_coverage": [
                {
                    "gt_node": "Backend::Authentication Service",
                    "covered": True,
                    "covering_predicted_nodes": ["Services::Login API"],
                },
                {
                    "gt_node": "Backend::Billing Service",
                    "covered": True,
                    "covering_predicted_nodes": ["Services::Payment Module"],
                },
            ],
            "predicted_node_grounding": [
                {
                    "predicted_node": "Services::Login API",
                    "grounded": True,
                    "reference_nodes": ["Backend::Authentication Service"],
                },
                {
                    "predicted_node": "Services::Payment Module",
                    "grounded": True,
                    "reference_nodes": ["Backend::Billing Service"],
                },
            ],
        }
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            gt_dir = root / "gt"
            gt_dir.mkdir()
            (gt_dir / "demo.puml").write_text(gt, encoding="utf-8")

            pred_root = root / "predictions"
            pred = pred_root / "demo" / "predicted.puml"
            pred.parent.mkdir(parents=True)
            pred.write_text(pred_text, encoding="utf-8")
            (pred_root / "judge_alignment_v2_gpt-4o-mini.json").write_text(
                json.dumps(alignment_data),
                encoding="utf-8",
            )
            l1_config = L1AlignmentConfig(model="gpt-4o-mini")

            with patch(
                "evaluation_script.pipeline.evaluate_l0",
                side_effect=lambda puml: evaluate_l0(
                    puml, syntax_checker=lambda _puml_code: (True, "")
                ),
            ):
                with self.assertRaises(l1_structural.L1AlignmentError):
                    evaluate_files(
                        [pred], gt_dir=gt_dir, l1_config=l1_config, pred_root=pred_root
                    )

        self.assertFalse((pred.parent / "judge_alignment_v2_gpt-4o-mini.json").exists())

    def test_evaluate_files_writes_generated_alignment_next_to_prediction_file(self):
        gt = """@startuml
package "Backend" {
  [Authentication Service] as Auth
}
@enduml
"""
        pred_text = """@startuml
package "Services" {
  [Login API] as Login
}
@enduml
"""
        alignment_data = {
            "matched_pairs": [
                {
                    "gt_nodes": ["Backend::Authentication Service"],
                    "predicted_nodes": ["Services::Login API"],
                    "match_type": "1:1",
                    "is_boundary_correct": True,
                }
            ],
            "unmatched_gt_nodes": [],
            "unmatched_predicted_nodes": [],
            "reference_node_coverage": [
                {
                    "gt_node": "Backend::Authentication Service",
                    "covered": True,
                    "covering_predicted_nodes": ["Services::Login API"],
                }
            ],
            "predicted_node_grounding": [
                {
                    "predicted_node": "Services::Login API",
                    "grounded": True,
                    "reference_nodes": ["Backend::Authentication Service"],
                }
            ],
        }
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            gt_dir = root / "gt"
            gt_dir.mkdir()
            (gt_dir / "demo.puml").write_text(gt, encoding="utf-8")

            pred_root = root / "predictions"
            pred = pred_root / "demo" / "predicted.puml"
            pred.parent.mkdir(parents=True)
            pred.write_text(pred_text, encoding="utf-8")
            l1_config = L1AlignmentConfig(
                enabled=True, model="gpt-4o-mini", api_key="test-key"
            )

            with patch(
                "evaluation_script.pipeline.evaluate_l0",
                side_effect=lambda puml: evaluate_l0(
                    puml, syntax_checker=lambda _puml_code: (True, "")
                ),
            ):
                with patch(
                    "evaluation_script.l1_structural._call_alignment_judge",
                    return_value=alignment_data,
                ):
                    rows = evaluate_files(
                        [pred], gt_dir=gt_dir, l1_config=l1_config, pred_root=pred_root
                    )

            root_alignment = pred_root / "judge_alignment_v2_o3.json"
            sample_alignment = pred.parent / "judge_alignment_v2_gpt-4o-mini.json"
            o3_sample_alignment = pred.parent / "judge_alignment_v2_o3.json"
            root_alignment_exists = root_alignment.exists()
            sample_alignment_exists = sample_alignment.exists()
            o3_sample_alignment_exists = o3_sample_alignment.exists()

        self.assertNotIn("l1_alignment_source", rows[0])
        self.assertNotIn("l1_alignment_error", rows[0])
        self.assertEqual(rows[0]["l1_node_coverage"], 1.0)
        self.assertEqual(rows[0]["l1_gen_precision"], 1.0)
        self.assertFalse(root_alignment_exists)
        self.assertTrue(sample_alignment_exists)
        self.assertFalse(o3_sample_alignment_exists)

    def test_cli_uses_llm_model_for_l1_when_l1_model_is_not_set(self):
        with tempfile.TemporaryDirectory() as tmp:
            pred = Path(tmp) / "predicted.puml"
            pred.write_text(VALID_PUML, encoding="utf-8")
            captured = {}

            def fake_evaluate_files(
                _pred_paths,
                _gt_dir,
                _requirements_dir,
                _l2_config,
                l1_config,
                **_kwargs,
            ):
                captured["l1_model"] = l1_config.model
                return [{"sample_id": "demo"}]

            with patch.object(
                sys,
                "argv",
                [
                    "evaluate.py",
                    "--pred",
                    str(pred),
                    "--llm-model",
                    "gpt-4o-mini",
                ],
            ):
                with patch(
                    "evaluation_script.evaluate.discover_plantuml_files",
                    return_value=[pred],
                ):
                    with patch(
                        "evaluation_script.evaluate.evaluate_files",
                        side_effect=fake_evaluate_files,
                    ):
                        with patch("evaluation_script.evaluate.write_csv"):
                            with redirect_stdout(io.StringIO()):
                                evaluate_cli.main()

        self.assertEqual(captured["l1_model"], "gpt-4o-mini")

    def test_cli_passes_resume_rows_to_pipeline(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            pred = root / "predicted.puml"
            pred.write_text(VALID_PUML, encoding="utf-8")
            resume_csv = root / "results.csv"
            resume_csv.write_text(
                "sample_id,candidate_id,l0_valid,stage_status\n"
                "demo,direct/gpt-5,TRUE,completed\n",
                encoding="utf-8-sig",
            )
            captured = {}

            def fake_evaluate_files(
                _pred_paths,
                _gt_dir,
                _requirements_dir,
                _l2_config,
                _l1_config,
                **kwargs,
            ):
                captured["resume_rows"] = kwargs["resume_rows"]
                return [{"sample_id": "demo"}]

            with patch.object(
                sys,
                "argv",
                [
                    "evaluate.py",
                    "--pred",
                    str(pred),
                    "--resume-from",
                    str(resume_csv),
                ],
            ):
                with patch(
                    "evaluation_script.evaluate.discover_plantuml_files",
                    return_value=[pred],
                ):
                    with patch(
                        "evaluation_script.evaluate.evaluate_files",
                        side_effect=fake_evaluate_files,
                    ):
                        with patch("evaluation_script.evaluate.write_csv"):
                            with redirect_stdout(io.StringIO()):
                                evaluate_cli.main()

        self.assertEqual(captured["resume_rows"][0]["sample_id"], "demo")
        self.assertEqual(captured["resume_rows"][0]["l0_valid"], "TRUE")

    def test_cli_can_filter_predictions_to_resume_rows(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            pred_root = root / "Outputs" / "RQ1" / "C-R2A-17"
            kept = pred_root / "direct" / "gpt-5" / "demo" / "predicted.puml"
            skipped = pred_root / "direct" / "gpt-5" / "extra" / "predicted.puml"
            kept.parent.mkdir(parents=True)
            skipped.parent.mkdir(parents=True)
            kept.write_text(VALID_PUML, encoding="utf-8")
            skipped.write_text(VALID_PUML, encoding="utf-8")
            resume_csv = root / "results.csv"
            resume_csv.write_text(
                "sample_id,candidate_id,l0_valid,stage_status\n"
                "demo,direct/gpt-5,TRUE,completed\n",
                encoding="utf-8-sig",
            )
            captured = {}

            def fake_evaluate_files(
                pred_paths, _gt_dir, _requirements_dir, _l2_config, _l1_config, **kwargs
            ):
                captured["pred_paths"] = list(pred_paths)
                captured["resume_rows"] = kwargs["resume_rows"]
                return [{"sample_id": "demo"}]

            with patch.object(
                sys,
                "argv",
                [
                    "evaluate.py",
                    "--pred",
                    str(pred_root),
                    "--resume-from",
                    str(resume_csv),
                    "--only-resume-rows",
                ],
            ):
                with patch(
                    "evaluation_script.evaluate.discover_plantuml_files",
                    return_value=[kept, skipped],
                ):
                    with patch(
                        "evaluation_script.evaluate.evaluate_files",
                        side_effect=fake_evaluate_files,
                    ):
                        with patch("evaluation_script.evaluate.write_csv"):
                            with redirect_stdout(io.StringIO()):
                                evaluate_cli.main()

        self.assertEqual(captured["pred_paths"], [kept])
        self.assertEqual(captured["resume_rows"][0]["sample_id"], "demo")

    def test_cli_accepts_metadata_root_for_targeted_subdirectory(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            metadata_root = root / "Outputs" / "RQ1" / "C-R2A-17"
            target_dir = metadata_root / "openhands" / "qwen3-coder-480b-a35b-instruct"
            pred = target_dir / "demo" / "predicted.puml"
            pred.parent.mkdir(parents=True)
            pred.write_text(VALID_PUML, encoding="utf-8")
            captured = {}

            def fake_evaluate_files(
                pred_paths, _gt_dir, _requirements_dir, _l2_config, _l1_config, **kwargs
            ):
                captured["pred_paths"] = list(pred_paths)
                captured["pred_root"] = kwargs["pred_root"]
                return [{"sample_id": "demo"}]

            with patch.object(
                sys,
                "argv",
                [
                    "evaluate.py",
                    "--pred",
                    str(target_dir),
                    "--pred-root",
                    str(metadata_root),
                ],
            ):
                with patch(
                    "evaluation_script.evaluate.discover_plantuml_files",
                    return_value=[pred],
                ):
                    with patch(
                        "evaluation_script.evaluate.evaluate_files",
                        side_effect=fake_evaluate_files,
                    ):
                        with patch("evaluation_script.evaluate.write_csv"):
                            with redirect_stdout(io.StringIO()):
                                evaluate_cli.main()

        self.assertEqual(captured["pred_paths"], [pred])
        self.assertEqual(captured["pred_root"], metadata_root)

    def test_write_csv_omits_internal_path_columns(self):
        rows = [
            {
                "sample_id": "demo",
                "candidate_id": "model-a",
                "pred_path": "predicted.puml",
                "gt_path": "ad.puml",
                "requirements_path": "checked_srs.md",
                "l0_valid": True,
                "l1_metric_version": "l1-correspondence-v2",
                "stage_status": "completed",
            }
        ]
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "results.csv"
            write_csv(rows, out)

            with out.open("r", encoding="utf-8-sig", newline="") as f:
                header = next(csv.reader(f))

        self.assertNotIn("pred_path", header)
        self.assertNotIn("gt_path", header)
        self.assertNotIn("requirements_path", header)
        self.assertNotIn("l1_alignment_source", header)
        self.assertNotIn("l1_alignment_error", header)
        self.assertNotIn("l2_quality_scenario_support", header)
        self.assertNotIn("l2_risks", header)
        self.assertNotIn("l2_sensitivity_points", header)
        self.assertNotIn("l2_tradeoff_points", header)

    def test_write_csv_outputs_flat_rows(self):
        rows = [
            {
                "sample_id": "demo",
                "candidate_id": "model-a",
                "l0_valid": True,
                "l1_metric_version": "l1-correspondence-v2",
                "stage_status": "completed",
                "l1_node_coverage": 1.0,
                "l1_gen_precision": 1.0,
            }
        ]
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "results.csv"
            write_csv(rows, out)

            with out.open("r", encoding="utf-8-sig", newline="") as f:
                loaded = list(csv.DictReader(f))

        self.assertEqual(loaded[0]["sample_id"], "demo")
        self.assertEqual(loaded[0]["l1_node_coverage"], "1.0")
        self.assertEqual(loaded[0]["l1_gen_precision"], "1.0")

    def test_write_csv_retries_transient_windows_open_failure(self):
        rows = [{"sample_id": "demo", "candidate_id": "model-a", "l0_valid": True}]
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "results.csv"
            original_open = Path.open
            failed_paths = []

            def flaky_open(path, *args, **kwargs):
                mode = args[0] if args else kwargs.get("mode", "r")
                if "w" in mode and not failed_paths:
                    failed_paths.append(path)
                    raise OSError(errno.EINVAL, "Invalid argument", str(path))
                return original_open(path, *args, **kwargs)

            with patch("pathlib.Path.open", new=flaky_open):
                write_csv(rows, out)

            with out.open("r", encoding="utf-8-sig", newline="") as f:
                loaded = list(csv.DictReader(f))

        self.assertEqual(len(failed_paths), 1)
        self.assertEqual(loaded[0]["sample_id"], "demo")


if __name__ == "__main__":
    unittest.main()
