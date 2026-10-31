import copy
import unittest

from evaluation_script.plantuml_parser import PlantUMLParser
from evaluation_script.l1_hierarchy import evaluate_hierarchy, endpoint_anchors
from evaluation_script.l1_metrics import calculate_metrics, validate_alignment


def parse(text):
    return PlantUMLParser().parse("@startuml\n" + text + "\n@enduml")


def alignment(gt, pred, pairs):
    groups = [dict(gt_nodes=r, predicted_nodes=p, is_boundary_correct=True) for r, p in pairs]
    data = dict(matched_pairs=groups, reference_node_coverage=[], predicted_node_grounding=[])
    for node in gt.entity_nodes:
        support = [n for g in groups if node in g["gt_nodes"] for n in g["predicted_nodes"]]
        data["reference_node_coverage"].append(dict(gt_node=node, covered=bool(support), covering_predicted_nodes=support))
    for node in pred.entity_nodes:
        support = [n for g in groups if node in g["predicted_nodes"] for n in g["gt_nodes"]]
        data["predicted_node_grounding"].append(dict(predicted_node=node, grounded=bool(support), reference_nodes=support))
    return validate_alignment(data, gt.entity_nodes, pred.entity_nodes)


REF = 'package Business {\ncomponent Orders as O\ncomponent Users as U\n}\npackage Data {\ndatabase OrdersDB as D1\ndatabase UsersDB as D2\n}\nBusiness --> Data'
PRED = 'component OrderSvc as O\ncomponent UserSvc as U\ndatabase OrderStore as D1\ndatabase UserStore as D2\nO --> D1\nU --> D2'
PAIRS = [(["Business::Orders"], ["Global::OrderSvc"]), (["Business::Users"], ["Global::UserSvc"]),
         (["Data::OrdersDB"], ["Global::OrderStore"]), (["Data::UsersDB"], ["Global::UserStore"])]


class HierarchyTests(unittest.TestCase):
    def setUp(self):
        self.gt, self.pred = parse(REF), parse(PRED)
        self.data = alignment(self.gt, self.pred, PAIRS)

    def test_parent_relation_matches_two_fine_edges_without_expansion(self):
        score, audit = evaluate_hierarchy(self.gt, self.pred, self.data)
        self.assertEqual(score["l1_edge_f1"], 1)
        self.assertEqual(score["l1_covered_reference_edge_count"], 1)
        self.assertEqual(score["l1_supported_predicted_edge_count"], 2)
        self.assertEqual(len(audit["reference_edges"]), 1)
        self.assertEqual(len(audit["predicted_edges"]), 2)
        self.assertEqual(score["l1_reference_included_container_edge_count"], 1)
        self.assertEqual(score["l1_structural_similarity"], 100)

    def test_reverse_views_preserve_two_sided_existence(self):
        data = alignment(self.pred, self.gt, [(p, r) for r, p in PAIRS])
        score, _ = evaluate_hierarchy(self.pred, self.gt, data)
        self.assertEqual(score["l1_edge_f1"], 1)
        self.assertEqual(score["l1_covered_reference_edge_count"], 2)
        self.assertEqual(score["l1_supported_predicted_edge_count"], 1)

    def test_swapping_direction_does_not_match(self):
        pred = parse(PRED.replace("O --> D1", "D1 --> O").replace("U --> D2", "D2 --> U"))
        score, _ = evaluate_hierarchy(self.gt, pred, self.data)
        self.assertEqual(score["l1_edge_f1"], 0)

    def test_unmatched_sibling_cannot_borrow_ancestor_support(self):
        pred = parse(PRED + '\npackage Other {\ncomponent Unknown as X\n}\nX --> D1')
        data = alignment(self.gt, pred, PAIRS)
        score, audit = evaluate_hierarchy(self.gt, pred, data)
        self.assertAlmostEqual(score["l1_edge_precision"], 2 / 3, places=6)
        self.assertEqual(len(audit["predicted_unanchored_edges"]), 1)

    def test_empty_container_without_cache_anchor_is_retained_but_unmatched(self):
        pred = parse(PRED + '\npackage Control as C\nC --> D1')
        score, audit = evaluate_hierarchy(self.gt, pred, self.data)
        self.assertEqual(score["l1_predicted_edge_count"], 3)
        self.assertEqual(audit["predicted_endpoint_anchors"]["Global::Control"], [])
        self.assertEqual(score["l1_predicted_unanchored_edge_count"], 1)

    def test_path_segments_do_not_confuse_prefixes_or_global(self):
        pred = parse('package A {\ncomponent Unmatched\n}\npackage AB {\ncomponent OrderSvc as O\n}\ncomponent UserSvc\ndatabase OrderStore\ndatabase UserStore')
        pairs = copy.deepcopy(PAIRS)
        pairs[0] = (pairs[0][0], ["AB::OrderSvc"])
        data = alignment(self.gt, pred, pairs)
        anchors = endpoint_anchors(pred, data, "predicted")
        self.assertEqual(anchors["Global::A"], set())
        self.assertEqual(anchors["Global::AB"], {0})
        self.assertNotIn("Global", anchors)

    def test_no_transitive_dependency_matching(self):
        pred = parse(PRED.replace("O --> D1", "O --> Q\nQ --> D1").replace("U --> D2", "") + '\ncomponent Q')
        data = alignment(self.gt, pred, PAIRS)
        score, _ = evaluate_hierarchy(self.gt, pred, data)
        self.assertEqual(score["l1_edge_f1"], 0)

    def test_container_keyword_variants_preserve_edge_results(self):
        for keyword in ["folder", "frame", "rectangle"]:
            gt = parse(REF.replace("package", keyword))
            # Only the original matched entities supply anchors in all cases;
            # rectangle adds unjudged nodes to this synthetic scan as negatives.
            data = alignment(gt, self.pred, PAIRS)
            score, _ = evaluate_hierarchy(gt, self.pred, data)
            self.assertEqual(score["l1_edge_f1"], 1)
            self.assertEqual(score["l1_reference_edge_count"], 1)

    def test_duplicate_arrows_and_labels_do_not_change_scores(self):
        pred = parse(PRED + '\nO --> D1 : another label\nD2 <-- U')
        score, _ = evaluate_hierarchy(self.gt, pred, self.data)
        self.assertEqual(score["l1_predicted_edge_count"], 2)
        self.assertEqual(score["l1_predicted_duplicate_edge_count"], 2)

    def test_internal_split_edges_excluded_but_self_edges_retained(self):
        gt = parse('component A\ncomponent B\nA --> B\nA --> A')
        pred = parse('component X\nX --> X')
        data = alignment(gt, pred, [(["Global::A", "Global::B"], ["Global::X"])])
        score, audit = evaluate_hierarchy(gt, pred, data)
        self.assertEqual(score["l1_excluded_internal_reference_edge_count"], 1)
        self.assertEqual(audit["reference_edges"], [("Global::A", "Global::A")])
        self.assertEqual(score["l1_edge_f1"], 1)

    def test_preserves_node_scans_and_layer_flags(self):
        data = copy.deepcopy(self.data)
        data["reference_node_coverage"][0]["covered"] = False
        data["matched_pairs"][0]["is_boundary_correct"] = False
        before = calculate_metrics(self.gt, self.pred, data)
        after, _ = evaluate_hierarchy(self.gt, self.pred, data)
        for k in ["l1_node_coverage", "l1_gen_precision", "l1_boundary_accuracy"]:
            self.assertEqual(before[k], after[k])

    def test_empty_edge_sets_undefined_and_one_empty_zero(self):
        gt = parse(REF.replace("Business --> Data", ""))
        pred = parse(PRED.replace("O --> D1", "").replace("U --> D2", ""))
        score, _ = evaluate_hierarchy(gt, pred, self.data)
        self.assertIsNone(score["l1_edge_f1"])
        score, _ = evaluate_hierarchy(gt, self.pred, self.data)
        self.assertEqual(score["l1_edge_f1"], 0)
        self.assertIsNone(score["l1_edge_recall"])

    def test_invalid_alignment_is_not_silently_repaired(self):
        data = copy.deepcopy(self.data)
        data["matched_pairs"][0]["predicted_nodes"] = ["unknown"]
        with self.assertRaises(ValueError):
            evaluate_hierarchy(self.gt, self.pred, data)


if __name__ == "__main__":
    unittest.main()
