# L1 hierarchy-aware offline recomputation

Version: `l1-hierarchy-offline-v1`. Alignment protocol: unchanged `l1-correspondence-v2`.

This entry point implements the agreed minimal revision: retain directed container relations and match edge endpoints through hierarchy paths using the existing GPT-5.4-mini alignment. It does not edit PlantUML sources, rerun a judge, merge historical judge outputs, or change the frozen entity/layer judgments. The original v2 entry points remain available for reproducibility.

## Representation and matching

`V` contains all parsed nodes, including package/folder/frame endpoints. `A` is the original v2 entity set for which semantic judgments were cached. Node coverage, generation precision and layer agreement remain defined over `A` and the existing groups, not over newly admitted container endpoints.

For node `x`, define `I(x)` as the IDs of existing matched groups having a member equal to `x` or an explicit descendant of `x`, based on complete path segments. The synthetic `Global` prefix is not a shared system node. Anchors flow from aligned descendants to their explicit ancestors; a child does not borrow anchors from siblings or an ancestor merely because their names share a prefix. No new name-based semantic alignment is inferred.

Reference edge `(a,b)` and generated edge `(u,v)` correspond iff `I(a)` intersects `I(u)` and `I(b)` intersects `I(v)`. Direction is preserved. Each original edge is counted at most once on its own side, with no one-to-one restriction across sides. This is deliberately permissive: different descendants can supply the source and target anchors; a container match does not verify the finer dependency. No transitive dependency paths or Cartesian expansions of container edges are created.

All deduplicated directed edges participate, including container edges. The existing exclusion for edges between distinct members of a directly aligned split/merge group is retained. It is not extended to edges whose inferred container anchor sets happen to overlap. Explicit self-edges remain comparable. Annotation/layout links and undirected links retain the parser's previous treatment; labels do not affect correspondence. Newly retained endpoints without a cached self/descendant anchor remain unmatched and are separately counted as unanchored.

## Metrics

- `l1_node_coverage`, `l1_gen_precision`, `l1_boundary_accuracy`, node counts and unmatched-node counts remain unchanged.
- `l1_edge_precision` uses supported generated edges divided by comparable generated edges.
- `l1_edge_recall` uses recovered reference edges divided by comparable reference edges. The two numerators may differ.
- `l1_edge_f1` is their harmonic mean, with the existing empty-set conventions: both edge sets empty gives undefined; exactly one empty gives F1 zero. A zero denominator gives an undefined directional ratio.
- `l1_structural_similarity` is recomputed as `100*(1-D/Z)` using the same unit-cost formula, frozen entity terms, new comparable edge terms and old layer judgments. It is not optimized GED or architectural accuracy.
- `l1_god_ratio` uses the original entity denominator and counts actual incidence of all directed edges, including entity-to-container links. Parent edges are never inherited by descendants.
- `l1_*_graph_node_count` includes container nodes; `l1_*_node_count` is the original semantic entity count.
- `l1_*_container_edge_count` and `l1_*_included_container_edge_count` count retained container-related edges; these are no longer exclusions in this protocol.
- `l1_*_unanchored_edge_count` counts comparable edges with at least one endpoint lacking an alignment anchor. They remain in the denominator and unmatched.

New edge scores measure broad reference correspondence. Neither an unmatched edge nor an unmatched node by itself proves that the generated design is wrong. The cached mappings may themselves be coarse or imperfect; this offline revision does not correct their semantics. Labels such as prohibitions remain a limitation of the label-insensitive extraction convention.

## Released results

`Results/manifest.csv` defines the study cohort, and `Results/l1.csv` contains
the hierarchy-aware metrics. The cohort contains 1,128 L0-valid outputs and
232 failures. Per-edge correspondence witnesses are stored under
`Results/edge_audits/`.

## Verification

```powershell
python -B -m unittest evaluation_script.tests.test_evaluation_core evaluation_script.tests.test_l1_revision evaluation_script.tests.test_l1_hierarchy -q
```

Tests cover asymmetric edge counts, reverse directions, exact path segments, unanchored empty containers, no sibling/global fallback, no multi-hop substitution, declaration variants, duplicate edges, internal split/merge exclusions, unchanged semantic judgments, and stale-cache rejection.
