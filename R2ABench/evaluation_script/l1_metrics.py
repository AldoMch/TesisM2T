"""L1 v2: validated semantic correspondence and deterministic graph diagnostics."""

from __future__ import annotations
import copy

VERSION = "l1-correspondence-v2"


def validate_alignment(data, reference_nodes, predicted_nodes):
    """Require a complete independent census and disjoint 1:1/1:N/N:1 groups.

    Never derive missing semantic judgments from group membership. Legacy JSON
    field names are retained for compatibility with the existing judge client;
    ``grounded`` means reference correspondence, not factual correctness.
    """
    if not isinstance(data, dict):
        raise ValueError("alignment must be a JSON object")
    data = copy.deepcopy(data)
    r, p = set(reference_nodes), set(predicted_nodes)
    for field, node_key, flag, support, expected, opposite in [
        (
            "reference_node_coverage",
            "gt_node",
            "covered",
            "covering_predicted_nodes",
            r,
            p,
        ),
        (
            "predicted_node_grounding",
            "predicted_node",
            "grounded",
            "reference_nodes",
            p,
            r,
        ),
    ]:
        scan = data.get(field)
        if not isinstance(scan, list):
            raise ValueError(f"{field}: complete independent scan required")
        seen = set()
        for item in scan:
            if not isinstance(item, dict):
                raise ValueError(f"{field}: expected object")
            name = item.get(node_key)
            if name not in expected or name in seen:
                raise ValueError(f"{field}: unknown or duplicate node {name!r}")
            seen.add(name)
            if type(item.get(flag)) is not bool:
                raise ValueError(f"{field}: {flag} must be boolean")
            refs = item.get(support)
            if (
                not isinstance(refs, list)
                or any(n not in opposite for n in refs)
                or len(set(refs)) != len(refs)
            ):
                raise ValueError(f"{field}: invalid supporting nodes for {name!r}")
            if item[flag] and not refs:
                raise ValueError(
                    f"{field}: positive judgment has no support for {name!r}"
                )
        if seen != expected:
            raise ValueError(f"{field}: missing nodes {sorted(expected-seen)!r}")
    groups = data.get("matched_pairs")
    if not isinstance(groups, list):
        raise ValueError("matched_pairs: list required")
    used_r, used_p = set(), set()
    for group in groups:
        if not isinstance(group, dict):
            raise ValueError("matched_pairs: expected object")
        a, b = group.get("gt_nodes"), group.get("predicted_nodes")
        if not isinstance(a, list) or not isinstance(b, list) or not a or not b:
            raise ValueError("matched group must have both sides")
        if any(n not in r for n in a) or any(n not in p for n in b):
            raise ValueError("matched group contains unknown nodes")
        if len(set(a)) != len(a) or len(set(b)) != len(b):
            raise ValueError("duplicate node within matched group")
        if len(a) > 1 and len(b) > 1:
            raise ValueError(
                "many-to-many group is not supported; use disjoint 1:1, 1:N, or N:1 groups"
            )
        if used_r.intersection(a) or used_p.intersection(b):
            raise ValueError(
                "overlapping matched groups; every node may appear in at most one group"
            )
        if type(group.get("is_boundary_correct")) is not bool:
            raise ValueError("matched group requires a boolean boundary judgment")
        used_r.update(a)
        used_p.update(b)
        group["match_type"] = (
            "1:1" if len(a) == len(b) == 1 else ("1:N" if len(a) == 1 else "N:1")
        )
    # Complements are deterministic, not a second source of truth supplied by a model.
    data["unmatched_gt_nodes"] = sorted(r - used_r)
    data["unmatched_predicted_nodes"] = sorted(p - used_p)
    return data


def _ratio(n, d):
    return n / d if d else None


def edge_report(data, gt_edges, pred_edges):
    r_group, p_group = {}, {}
    split_merge = set()
    for i, g in enumerate(data["matched_pairs"]):
        r_group.update((n, i) for n in g["gt_nodes"])
        p_group.update((n, i) for n in g["predicted_nodes"])
        if len(g["gt_nodes"]) > 1 or len(g["predicted_nodes"]) > 1:
            split_merge.add(i)

    def partition(edges, mapping):
        internal, comparable = set(), set()
        for a, b in set(edges):
            # Explicit self-relations remain comparable. Only relations between
            # distinct members of an accepted split/merge group are excluded.
            if (
                a != b
                and a in mapping
                and b in mapping
                and mapping[a] == mapping[b]
                and mapping[a] in split_merge
            ):
                internal.add((a, b))
            else:
                comparable.add((a, b))
        return comparable, internal

    r, ri = partition(gt_edges, r_group)
    p, pi = partition(pred_edges, p_group)

    def keys(edges, mapping):
        return {
            (mapping[a], mapping[b]) for a, b in edges if a in mapping and b in mapping
        }

    rk, pk = keys(r, r_group), keys(p, p_group)
    rh = {
        e
        for e in r
        if e[0] in r_group and e[1] in r_group and (r_group[e[0]], r_group[e[1]]) in pk
    }
    ph = {
        e
        for e in p
        if e[0] in p_group and e[1] in p_group and (p_group[e[0]], p_group[e[1]]) in rk
    }
    precision, recall = _ratio(len(ph), len(p)), _ratio(len(rh), len(r))
    f1 = (
        None
        if not p and not r
        else (
            2 * precision * recall / (precision + recall)
            if precision and recall
            else 0.0
        )
    )
    return dict(
        precision=precision,
        recall=recall,
        f1=f1,
        reference_edges=sorted(r),
        predicted_edges=sorted(p),
        covered_reference_edges=sorted(rh),
        supported_predicted_edges=sorted(ph),
        unmatched_reference_edges=sorted(r - rh),
        unmatched_predicted_edges=sorted(p - ph),
        internal_reference_edges=sorted(ri),
        internal_predicted_edges=sorted(pi),
    )


def entity_edges(parsed):
    entities = set(parsed.entity_nodes)
    return [e for e in parsed.edges if e[0] in entities and e[1] in entities]


def calculate_metrics(gt, pred, data):
    r, p = gt.entity_nodes, pred.entity_nodes
    edges = edge_report(data, entity_edges(gt), entity_edges(pred))
    groups = data["matched_pairs"]
    m = len(groups)
    nr, np = len(data["unmatched_gt_nodes"]), len(data["unmatched_predicted_nodes"])
    er, ep = len(edges["unmatched_reference_edges"]), len(
        edges["unmatched_predicted_edges"]
    )
    b = sum(not g["is_boundary_correct"] for g in groups)
    d = nr + np + er + ep + b
    z = (
        len(r)
        + len(p)
        + len(edges["reference_edges"])
        + len(edges["predicted_edges"])
        + m
    )
    values = dict(
        l1_metric_version=VERSION,
        l1_status="completed",
        l1_reference_node_count=len(r),
        l1_predicted_node_count=len(p),
        l1_reference_edge_count=len(entity_edges(gt)),
        l1_predicted_edge_count=len(entity_edges(pred)),
        l1_node_coverage=_ratio(
            sum(i["covered"] for i in data["reference_node_coverage"]), len(r)
        ),
        l1_gen_precision=_ratio(
            sum(i["grounded"] for i in data["predicted_node_grounding"]), len(p)
        ),
        l1_edge_precision=edges["precision"],
        l1_edge_recall=edges["recall"],
        l1_edge_f1=edges["f1"],
        l1_boundary_accuracy=_ratio(m - b, m),
        l1_matched_group_count=m,
        l1_structural_similarity=100 * (1 - d / z) if z else None,
        l1_structural_discrepancy=d,
        l1_structural_denominator=z,
        l1_unmatched_reference_node_count=nr,
        l1_unmatched_predicted_node_count=np,
        l1_matched_node_count=len(p) - np,
        l1_layer_disagreement_count=b,
        l1_unmatched_reference_edge_count=er,
        l1_unmatched_predicted_edge_count=ep,
        l1_comparable_reference_edge_count=len(edges["reference_edges"]),
        l1_comparable_predicted_edge_count=len(edges["predicted_edges"]),
        l1_covered_reference_edge_count=len(edges["covered_reference_edges"]),
        l1_supported_predicted_edge_count=len(edges["supported_predicted_edges"]),
        l1_excluded_internal_reference_edge_count=len(
            edges["internal_reference_edges"]
        ),
        l1_excluded_internal_predicted_edge_count=len(
            edges["internal_predicted_edges"]
        ),
    )
    for label, graph in [("reference", gt), ("predicted", pred)]:
        values[f"l1_{label}_grouping_node_count"] = len(graph.grouping_nodes)
        values[f"l1_{label}_container_edge_count"] = len(graph.edges) - len(
            entity_edges(graph)
        )
        values[f"l1_{label}_undirected_edge_count"] = len(graph.undirected_edges)
        values[f"l1_{label}_duplicate_edge_count"] = graph.duplicate_edge_count
        values[f"l1_{label}_layout_edge_count"] = graph.layout_edge_count
    return {k: round(v, 6) if isinstance(v, float) else v for k, v in values.items()}


def intrinsic_metrics(parsed):
    degree = dict.fromkeys(parsed.entity_nodes, 0)
    for a, b in entity_edges(parsed):
        degree[a] += 1
        degree[b] += 1
    vals = list(degree.values())
    mean = sum(vals) / len(vals) if vals else 0
    sd = (sum((v - mean) ** 2 for v in vals) / len(vals)) ** 0.5 if vals else 0
    return dict(
        l1_predicted_node_count=len(degree),
        l1_predicted_edge_count=len(entity_edges(parsed)),
        l1_god_ratio=_ratio(sum(v > mean + 2 * sd and v > 2 for v in vals), len(vals)),
    )
