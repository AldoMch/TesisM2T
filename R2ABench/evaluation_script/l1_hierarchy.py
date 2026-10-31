"""Offline hierarchy-aware edge correspondence using frozen v2 alignments.

The semantic node universe is unchanged. All explicit directed relations are
eligible, including relations incident to package/folder/frame nodes. A node's
edge-matching anchors are the existing matched groups of itself or descendants.
No semantic mapping, relation, or alignment judgment is generated here.
"""
from __future__ import annotations

from collections import defaultdict

from .l1_metrics import calculate_metrics, edge_report, validate_alignment

VERSION = "l1-hierarchy-offline-v1"


def _path(node):
    """Use path segments; Global is the parser's synthetic top-level prefix."""
    parts = tuple(node.split("::"))
    return parts[1:] if parts[0] == "Global" else parts


def endpoint_anchors(graph, data, side):
    """Groups with a member at or below this actual graph node.

    This lifts existing alignments to explicit ancestors. It does not pass an
    ancestor's anchors down to unrelated/unmatched children or introduce a
    universal Global node that would make all endpoints match.
    """
    field = "gt_nodes" if side == "reference" else "predicted_nodes"
    members = [(i, _path(n)) for i, g in enumerate(data["matched_pairs"]) for n in g[field]]
    anchors = {}
    for node in graph.nodes:
        path = _path(node)
        anchors[node] = frozenset(i for i, member in members if member[:len(path)] == path)
    return anchors


def hierarchical_edge_report(gt, pred, data):
    """Match edges by a shared source anchor and a shared target anchor."""
    # Preserve the prior narrow internal split/merge exclusion. Inferred
    # container anchors never cause an additional internal-edge exclusion.
    base = edge_report(data, gt.edges, pred.edges)
    r, p = base["reference_edges"], base["predicted_edges"]
    ra = endpoint_anchors(gt, data, "reference")
    pa = endpoint_anchors(pred, data, "predicted")

    def index(edges, anchors):
        keys = []
        inverse = defaultdict(list)
        for i, (a, b) in enumerate(edges):
            pairs = {(x, y) for x in anchors[a] for y in anchors[b]}
            keys.append(pairs)
            for pair in sorted(pairs):
                inverse[pair].append(i)
        return keys, inverse

    rk, ri = index(r, ra)
    pk, pi = index(p, pa)

    def hits(keys, opposite):
        witnesses = []
        for i, candidates in enumerate(keys):
            common = candidates.intersection(opposite)
            if common:
                source, target = min(common)
                witnesses.append({"edge_index": i, "counterpart_index": opposite[(source, target)][0],
                                  "source_group": source, "target_group": target})
        return witnesses

    rw, pw = hits(rk, pi), hits(pk, ri)
    rh = {w["edge_index"] for w in rw}
    ph = {w["edge_index"] for w in pw}
    precision = len(ph) / len(p) if p else None
    recall = len(rh) / len(r) if r else None
    f1 = None if not p and not r else (
        2 * precision * recall / (precision + recall) if precision and recall else 0.0)
    return dict(
        precision=precision, recall=recall, f1=f1,
        reference_edges=r, predicted_edges=p,
        covered_reference_edges=[e for i, e in enumerate(r) if i in rh],
        supported_predicted_edges=[e for i, e in enumerate(p) if i in ph],
        unmatched_reference_edges=[e for i, e in enumerate(r) if i not in rh],
        unmatched_predicted_edges=[e for i, e in enumerate(p) if i not in ph],
        internal_reference_edges=base["internal_reference_edges"],
        internal_predicted_edges=base["internal_predicted_edges"],
        reference_witnesses=rw, predicted_witnesses=pw,
        reference_endpoint_anchors={n: sorted(v) for n, v in ra.items()},
        predicted_endpoint_anchors={n: sorted(v) for n, v in pa.items()},
        reference_unanchored_edges=[e for e in r if not ra[e[0]] or not ra[e[1]]],
        predicted_unanchored_edges=[e for e in p if not pa[e[0]] or not pa[e[1]]],
    )


def evaluate_hierarchy(gt, pred, alignment):
    """Return metrics and an auditable edge report, without any judge calls."""
    if gt.parse_errors or pred.parse_errors:
        raise ValueError("Graph parsing failed: " + " | ".join(gt.parse_errors + pred.parse_errors))
    data = validate_alignment(alignment, gt.entity_nodes, pred.entity_nodes)
    values = calculate_metrics(gt, pred, data)
    edges = hierarchical_edge_report(gt, pred, data)
    nr, np = len(data["unmatched_gt_nodes"]), len(data["unmatched_predicted_nodes"])
    er, ep = len(edges["unmatched_reference_edges"]), len(edges["unmatched_predicted_edges"])
    m = len(data["matched_pairs"])
    b = sum(not g["is_boundary_correct"] for g in data["matched_pairs"])
    d = nr + np + er + ep + b
    z = len(gt.entity_nodes) + len(pred.entity_nodes) + len(edges["reference_edges"]) + len(edges["predicted_edges"]) + m
    values.update(
        l1_metric_version=VERSION,
        l1_alignment_metric_version="l1-correspondence-v2",
        l1_edge_precision=edges["precision"], l1_edge_recall=edges["recall"], l1_edge_f1=edges["f1"],
        l1_structural_similarity=100 * (1 - d / z) if z else None,
        l1_structural_discrepancy=d, l1_structural_denominator=z,
    )
    for side, graph, hit in [("reference", gt, "covered"), ("predicted", pred, "supported")]:
        values.update({
            f"l1_{side}_graph_node_count": len(graph.nodes),
            f"l1_{side}_edge_count": len(graph.edges),
            f"l1_comparable_{side}_edge_count": len(edges[f"{side}_edges"]),
            f"l1_{hit}_{side}_edge_count": len(edges[f"{hit}_{side}_edges"]),
            f"l1_unmatched_{side}_edge_count": len(edges[f"unmatched_{side}_edges"]),
            f"l1_excluded_internal_{side}_edge_count": len(edges[f"internal_{side}_edges"]),
            f"l1_{side}_unanchored_edge_count": len(edges[f"{side}_unanchored_edges"]),
            f"l1_{side}_included_container_edge_count": values[f"l1_{side}_container_edge_count"],
        })
    # Count only actual incidence. A relation on a parent does not give every
    # descendant an invented connection. The node denominator stays frozen.
    degree = dict.fromkeys(pred.entity_nodes, 0)
    for a, b in pred.edges:
        if a in degree:
            degree[a] += 1
        if b in degree:
            degree[b] += 1
    degrees = list(degree.values())
    mean = sum(degrees) / len(degrees) if degrees else 0
    sd = (sum((v - mean) ** 2 for v in degrees) / len(degrees)) ** 0.5 if degrees else 0
    values["l1_god_ratio"] = sum(v > mean + 2 * sd and v > 2 for v in degrees) / len(degrees) if degrees else None
    return {k: round(v, 6) if isinstance(v, float) else v for k, v in values.items()}, edges
