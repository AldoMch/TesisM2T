# Frozen scores and provenance

`manifest.csv` defines the main cohort. Join tables by `id`; do not discover
experiments by recursively counting every output file.

| File | Content |
| --- | --- |
| `cohort.csv` | Main-study IDs, recorded validity and derived structural metrics |
| `l1.csv` | Frozen L0/L1 results, hierarchy-aware metrics and alignment paths |
| `l2.csv` | Saved five-dimensional semantic scores and explanations |
| `reqcov.csv` | Curated per-requirement judgments, evidence and coverage counts |
| `configuration_summary.csv` | 20 configurations, separately by source and pooled |
| `source_summary.csv` | E-R2A, G-R2A and pooled descriptive results |
| `frozen_audit.json` | Release-table digests and original source digests |
| `edge_audits/` | Saved per-edge correspondence witnesses |

All four main tables contain the same 1,360 evaluation-case IDs.
`output_released` identifies the 1,128 published views; remaining cases retain
validity outcomes for the statistical analyses. Quality summaries use valid cases.

`requirements_path` records the L1 input path.
`current_srs_path` identifies the current public SRS. ReqCov's own table identifies
its SRS input.

Paths and text serialization were made portable. In CSV tables,
`source_*_sha256` records original digests; unprefixed digests
describe released files. The historical edge-audit JSON headers retain the
source-run input/cache hashes; these correspond to the manifest's source digests.
L1 scores use the cached semantic alignments.
The current curated requirement file is identified by
`categorized_requirements_path`; ReqCov records use its stable requirement IDs.
Composite `*_input_signature` fields retain historical judge signatures; they
are not newly computed signatures for the normalized release files.

`l2_requirement_coverage` in the detailed and compact tables is a fraction
from 0 to 1. Analysis tables express ReqCov as a percentage from 0 to 100.

Ten recorded ReqCov responses use `source-line-ids-v1`: the judge cited source
line numbers, which were resolved to exact PlantUML excerpts before scoring.
`evaluation_script/reqcov_citations.py` preserves that prompt override and
decoder for resolving the recorded evidence to diagram excerpts.
