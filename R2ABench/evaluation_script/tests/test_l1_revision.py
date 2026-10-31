import unittest, copy, json, tempfile
from pathlib import Path
from evaluation_script.plantuml_parser import PlantUMLParser
from evaluation_script.l1_metrics import (
    validate_alignment,
    edge_report,
    calculate_metrics,
)
from evaluation_script.l1_structural import (
    evaluate_l1,
    L1AlignmentError,
    L1AlignmentConfig,
    _resolve_alignment_data,
    _alignment_fingerprint,
)
from evaluation_script.l0_syntax import evaluate_l0


def graph(nodes, edges=()):
    return (
        "@startuml\n"
        + "\n".join("component " + n for n in nodes)
        + "\n"
        + "\n".join(a + " --> " + b for a, b in edges)
        + "\n@enduml"
    )


def alignment(r, p, groups):
    groups = [
        dict(
            gt_nodes=["Global::" + n for n in a],
            predicted_nodes=["Global::" + n for n in b],
            is_boundary_correct=layer,
        )
        for a, b, layer in groups
    ]
    data = dict(
        matched_pairs=groups, reference_node_coverage=[], predicted_node_grounding=[]
    )
    for side, nodes in [("reference", r), ("predicted", p)]:
        for n in nodes:
            own = "gt_nodes" if side == "reference" else "predicted_nodes"
            other = "predicted_nodes" if side == "reference" else "gt_nodes"
            support = [v for g in groups if "Global::" + n in g[own] for v in g[other]]
            if side == "reference":
                data["reference_node_coverage"].append(
                    dict(
                        gt_node="Global::" + n,
                        covered=bool(support),
                        covering_predicted_nodes=support,
                    )
                )
            else:
                data["predicted_node_grounding"].append(
                    dict(
                        predicted_node="Global::" + n,
                        grounded=bool(support),
                        reference_nodes=support,
                    )
                )
    return data


class RevisionTests(unittest.TestCase):
    def test_arrow_direction_bidirectional_and_deduplication(self):
        p = PlantUMLParser()
        for link in [
            "A --> B",
            "B <-- A",
            "A->B",
            "B<-A",
            "A -right-> B",
            "A -[#red]-> B",
        ]:
            self.assertEqual(
                p.parse(graph(["A", "B"]) + "\n" + link).edges,
                [("Global::A", "Global::B")],
                link,
            )
        parsed = p.parse(
            graph(["A", "B"])
            + "\nA<-->B\nA --> B : second label\nA -- B\nA -[hidden]-> B"
        )
        self.assertEqual(len(parsed.edges), 2)
        self.assertEqual(parsed.duplicate_edge_count, 1)
        self.assertEqual(len(parsed.undirected_edges), 1)
        self.assertEqual(parsed.layout_edge_count, 1)

    def test_multiline_labels_preserve_parentheses(self):
        p = PlantUMLParser().parse(
            '@startuml\npackage "Backend" {\ncomponent "Auth (v2)" as A\n[DB\n(MySQL)] as B\nA --> B\n}\n@enduml'
        )
        self.assertFalse(p.parse_errors)
        self.assertIn("Backend::Auth (v2)", p.entity_nodes)
        self.assertIn("Backend::DB\\n(MySQL)", p.entity_nodes)

    def test_split_and_merge_have_two_sided_full_coverage(self):
        r, p = ["A1", "A2", "B"], ["A", "B"]
        data = alignment(r, p, [(["A1", "A2"], ["A"], True), (["B"], ["B"], True)])
        scored = evaluate_l1(
            graph(p, [("A", "B")]),
            graph(r, [("A1", "B"), ("A2", "B")]),
            alignment_data=data,
        )
        self.assertEqual(scored["l1_edge_f1"], 1)
        self.assertEqual(scored["l1_structural_similarity"], 100)
        self.assertEqual(scored["l1_covered_reference_edge_count"], 2)
        self.assertEqual(scored["l1_supported_predicted_edge_count"], 1)
        inverse = alignment(p, r, [(["A"], ["A1", "A2"], True), (["B"], ["B"], True)])
        reversed_score = evaluate_l1(
            graph(r, [("A1", "B"), ("A2", "B")]),
            graph(p, [("A", "B")]),
            alignment_data=inverse,
        )
        self.assertEqual(reversed_score["l1_edge_f1"], 1)

    def test_internal_edges_excluded_on_both_sides_without_perfect_empty_score(self):
        d = alignment(["A1", "A2"], ["A"], [(["A1", "A2"], ["A"], True)])
        score = evaluate_l1(
            graph(["A"]), graph(["A1", "A2"], [("A1", "A2")]), alignment_data=d
        )
        self.assertIsNone(score["l1_edge_f1"])
        self.assertEqual(score["l1_excluded_internal_reference_edge_count"], 1)
        self.assertEqual(score["l1_structural_similarity"], 100)

    def test_self_edges_are_compared(self):
        d = alignment(["A"], ["B"], [(["A"], ["B"], True)])
        score = evaluate_l1(graph(["B"]), graph(["A"], [("A", "A")]), alignment_data=d)
        self.assertEqual(score["l1_comparable_reference_edge_count"], 1)
        self.assertEqual(score["l1_edge_f1"], 0)
        self.assertIsNone(score["l1_edge_precision"])
        self.assertEqual(score["l1_edge_recall"], 0)

    def test_no_match_even_with_identical_labels_is_zero(self):
        d = alignment(["A", "B"], ["A", "B"], [])
        score = evaluate_l1(
            graph(["A", "B"], [("A", "B")]),
            graph(["A", "B"], [("A", "B")]),
            alignment_data=d,
        )
        self.assertEqual(score["l1_structural_similarity"], 0)
        self.assertEqual(score["l1_edge_f1"], 0)
        self.assertIsNone(score["l1_boundary_accuracy"])

    def test_no_reachability_substitution(self):
        d = alignment(
            ["A", "B"], ["A", "Q", "B"], [(["A"], ["A"], True), (["B"], ["B"], True)]
        )
        score = evaluate_l1(
            graph(["A", "Q", "B"], [("A", "Q"), ("Q", "B")]),
            graph(["A", "B"], [("A", "B")]),
            alignment_data=d,
        )
        self.assertEqual(score["l1_edge_f1"], 0)

    def test_package_not_entity_but_composite_database_is(self):
        parsed = PlantUMLParser().parse(
            '@startuml\npackage "Backend" {\ndatabase "DB" {\ncomponent Table\n}\n}\n@enduml'
        )
        self.assertNotIn("Global::Backend", parsed.entity_nodes)
        self.assertIn("Backend::DB", parsed.entity_nodes)
        self.assertIn("Backend::DB::Table", parsed.entity_nodes)

    def test_node_scans_are_independent_of_groups(self):
        d = alignment(["A"], ["B"], [(["A"], ["B"], True)])
        d["reference_node_coverage"][0]["covered"] = False
        score = evaluate_l1(graph(["B"]), graph(["A"]), alignment_data=d)
        self.assertEqual(score["l1_node_coverage"], 0)
        self.assertEqual(score["l1_gen_precision"], 1)
        self.assertEqual(score["l1_structural_similarity"], 100)

    def test_invalid_censuses_and_overlaps_are_rejected(self):
        base = alignment(
            ["A", "B"], ["C", "D"], [(["A"], ["C"], True), (["B"], ["D"], True)]
        )
        bad = []
        d = copy.deepcopy(base)
        d["reference_node_coverage"].pop()
        bad.append(d)
        d = copy.deepcopy(base)
        d["reference_node_coverage"].append(d["reference_node_coverage"][0])
        bad.append(d)
        d = copy.deepcopy(base)
        d["reference_node_coverage"][0]["covered"] = "false"
        bad.append(d)
        d = copy.deepcopy(base)
        d["reference_node_coverage"][0]["covering_predicted_nodes"] = ["unknown"]
        bad.append(d)
        d = copy.deepcopy(base)
        d["matched_pairs"][1]["predicted_nodes"] = ["Global::C"]
        bad.append(d)
        d = copy.deepcopy(base)
        d.pop("reference_node_coverage")
        bad.append(d)
        for d in bad:
            with self.assertRaises(L1AlignmentError):
                evaluate_l1(graph(["C", "D"]), graph(["A", "B"]), alignment_data=d)

    def test_boundary_disagreement_counts_group_once(self):
        d = alignment(["A", "B"], ["C"], [(["A", "B"], ["C"], False)])
        score = evaluate_l1(graph(["C"]), graph(["A", "B"]), alignment_data=d)
        self.assertEqual(score["l1_layer_disagreement_count"], 1)
        self.assertEqual(score["l1_structural_similarity"], 75)
        self.assertNotIn("l1_ged_accuracy", score)

    def test_notes_and_together_are_not_entities(self):
        parsed = PlantUMLParser().parse(
            "@startuml\ntogether {\ncomponent A\n}\nnote as Note\nA --> fake\nend note\nA .. Note\n@enduml"
        )
        self.assertFalse(parsed.parse_errors)
        self.assertEqual(parsed.entity_nodes, ["Global::A"])
        self.assertFalse(parsed.edges)

    def test_l0_fails_unparsed_structure(self):
        result = evaluate_l0(
            "@startuml\ncomponent A\nA --> unsupported bare label\n@enduml",
            syntax_checker=lambda _: (True, ""),
        )
        self.assertFalse(result.passed)

    def test_fingerprint_changes_when_candidates_or_requirements_change(self):
        p = PlantUMLParser()
        a = p.parse(graph(["A"]))
        b = p.parse(graph(["B"]))
        self.assertNotEqual(
            _alignment_fingerprint("x", a, b), _alignment_fingerprint("y", a, b)
        )
        self.assertNotEqual(
            _alignment_fingerprint("x", a, b), _alignment_fingerprint("x", a, a)
        )

    def test_parent_relation_does_not_support_child_relation(self):
        ref = "@startuml\npackage Parent {\ncomponent A\n}\ncomponent B\nParent --> B\n@enduml"
        pred = graph(["A", "B"], [("A", "B")])
        d = alignment(
            ["A", "B"], ["A", "B"], [(["A"], ["A"], True), (["B"], ["B"], True)]
        )
        d["reference_node_coverage"][0]["gt_node"] = "Parent::A"
        d["predicted_node_grounding"][0]["reference_nodes"] = ["Parent::A"]
        d["matched_pairs"][0]["gt_nodes"] = ["Parent::A"]
        scored = evaluate_l1(pred, ref, alignment_data=d)
        self.assertEqual(scored["l1_reference_container_edge_count"], 1)
        self.assertEqual(scored["l1_supported_predicted_edge_count"], 0)
        self.assertEqual(scored["l1_edge_f1"], 0)

    def test_duplicate_relations_do_not_change_correspondence(self):
        d = alignment(
            ["A", "B"], ["A", "B"], [(["A"], ["A"], True), (["B"], ["B"], True)]
        )
        ref = graph(["A", "B"], [("A", "B")])
        score = evaluate_l1(ref + "\nA --> B : another label", ref, alignment_data=d)
        self.assertEqual(score["l1_structural_similarity"], 100)
        self.assertEqual(score["l1_edge_f1"], 1)
        self.assertEqual(score["l1_predicted_duplicate_edge_count"], 1)

    def test_model_split_merge_proposals_are_consolidated_without_many_to_many(self):
        from evaluation_script.l1_structural import _consolidate_compatible_groups

        d = {
            "matched_pairs": [
                {
                    "gt_nodes": ["A"],
                    "predicted_nodes": ["P"],
                    "is_boundary_correct": True,
                },
                {
                    "gt_nodes": ["B"],
                    "predicted_nodes": ["P"],
                    "is_boundary_correct": False,
                },
            ]
        }
        groups = _consolidate_compatible_groups(d)["matched_pairs"]
        self.assertEqual(len(groups), 1)
        self.assertEqual(groups[0]["gt_nodes"], ["A", "B"])
        self.assertFalse(groups[0]["is_boundary_correct"])

    def test_conflict_ownership_preserves_independent_node_scans(self):
        from unittest.mock import patch, MagicMock
        from evaluation_script.l1_structural import _repair_group_ownership

        d = alignment(
            ["A", "B"], ["X", "Y"], [(["A"], ["X", "Y"], True), (["B"], ["Y"], True)]
        )
        response = MagicMock()
        response.__enter__.return_value.read.return_value = json.dumps(
            {
                "choices": [
                    {
                        "message": {
                            "content": json.dumps(
                                {
                                    "owners": {"p2": "g1"},
                                    "layer_flags": {"g0": True, "g1": False},
                                }
                            )
                        }
                    }
                ],
                "model": "test",
            }
        ).encode()
        with patch(
            "evaluation_script.l1_structural.urllib.request.urlopen",
            return_value=response,
        ):
            repaired = _repair_group_ownership(
                d,
                ["Global::A", "Global::B"],
                ["Global::X", "Global::Y"],
                L1AlignmentConfig(
                    model="test", api_key="test", base_url="https://example.invalid"
                ),
            )
        validated = validate_alignment(
            repaired, ["Global::A", "Global::B"], ["Global::X", "Global::Y"]
        )
        self.assertEqual(
            validated["matched_pairs"][0]["predicted_nodes"], ["Global::X"]
        )
        self.assertEqual(
            validated["matched_pairs"][1]["predicted_nodes"], ["Global::Y"]
        )
        self.assertFalse(validated["matched_pairs"][1]["is_boundary_correct"])
        self.assertEqual(
            validated["reference_node_coverage"], d["reference_node_coverage"]
        )
        self.assertEqual(
            validated["predicted_node_grounding"], d["predicted_node_grounding"]
        )

    def test_legacy_resume_row_cannot_skip_new_l1_evaluation(self):
        from unittest.mock import patch
        from evaluation_script.pipeline import evaluate_files, infer_prediction_metadata

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            pred = root / "demo.puml"
            pred.write_text(graph(["A"]))
            metadata = infer_prediction_metadata(pred, pred_root=root)
            old = dict(metadata, l0_valid=True, l1_ged_accuracy=90, stage_status="old")
            with patch(
                "evaluation_script.pipeline.evaluate_pair",
                return_value={"stage_status": "fresh"},
            ) as evaluate:
                rows = evaluate_files([pred], pred_root=root, resume_rows=[old])
            evaluate.assert_called_once()
            self.assertEqual(rows[0]["stage_status"], "fresh")

    def test_legend_endlegend_preserves_following_entities(self):
        parsed = PlantUMLParser().parse(
            "@startuml\nlegend right\nExplanatory text\nendlegend\ncomponent A\n@enduml"
        )
        self.assertEqual(parsed.entity_nodes, ["Global::A"])

    def test_stale_cache_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            cache = Path(tmp) / "cache.json"
            cache.write_text(
                json.dumps(alignment(["A"], ["A"], [(["A"], ["A"], True)]))
            )
            p = PlantUMLParser().parse(graph(["A"]))
            with self.assertRaises(L1AlignmentError):
                _resolve_alignment_data(
                    requirements_text="",
                    gt=p,
                    pred=p,
                    config=L1AlignmentConfig(),
                    cache_path=cache,
                )


if __name__ == "__main__":
    unittest.main()
