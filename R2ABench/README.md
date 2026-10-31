# R2ABench

R2ABench evaluates requirements-to-architecture generation using software
requirements specifications (SRSs), reference architecture views, generated
PlantUML views, and complementary structural and semantic assessments.

This release contains **68 projects, five models and four generation settings**:
**1,360 generation cases**. The package provides **1,128 valid architecture views**
and the recorded evaluation outcomes. It incorporates the completed ASP
rerun and the subsequent paired statistical analysis. It does not merge the
unfinished L0-feedback experiment into the main results.

## Released artifacts

| Artifact | Location |
| --- | --- |
| 17 project-document examples | [Dataset/E-R2A](Dataset/E-R2A) |
| 51 GitHub-derived examples | [Dataset/G-R2A](Dataset/G-R2A) |
| Inputs, hashes, paths and stable output IDs | [Results/manifest.csv](Results/manifest.csv) |
| Complete frozen score tables | [Results](Results/README.md) |
| Generated views | [Output/E-R2A](Output/E-R2A), [Output/G-R2A-52](Output/G-R2A-52) |
| Compatible compact result tables | [E-R2A](Output/results_e_r2a.csv), [G-R2A](Output/results_g_r2a.csv) |
| Cached semantic alignments | Alongside each L0-valid generated view |
| Edge correspondence witnesses | [Results/edge_audits](Results/edge_audits) |
| Descriptive RQ1--RQ3 results and figures | [analysis/descriptive](analysis/descriptive) |
| 165 paired comparisons and sensitivity analyses | [analysis/paired_tests](analysis/paired_tests) |
| Generation entry points | [generation](generation/README.md) |
| SRS review agreement | [Dataset/G-R2A/_agreement](Dataset/G-R2A/_agreement) |

The historical output folder name `G-R2A-52` is retained to preserve links;
it contains **51** main-study projects. Local research labels `C-R2A-17` and
`G-R2A-52` map to the released dataset names `E-R2A` and `G-R2A`.

## Study configuration

Models: GPT-5, Claude Sonnet 4.6, DeepSeek V3.2, DeepSeek V4.1 Flash, and
Qwen3-Coder 480B-A35B.

Settings: direct LLM use (`direct`), a MetaGPT-based R2A workflow
(`metagpt-custom`), Mini-SWE-Agent (`mini-swe-agent`), and OpenHands (`openhands`).
The MetaGPT workflow decomposes the task into analyst, architect, reviewer and
refiner stages; its reviewer is a model-driven stage, not a human rating.

Each dataset project includes `checked_srs.md`, its reference view, and
`req_final.jsonl`. Across the 68 projects, the curated lists contain 480
requirements. See [the data format and provenance notes](Dataset/README.md).

## Reproduce the paired statistical analysis

Use Python 3.12. The reference environment used Python 3.12.4, NumPy 1.26.4,
pandas 2.2.2, SciPy 1.13.1 and statsmodels 0.14.2.

```bash
python -m pip install -r requirements-analysis.txt
python -B analysis/paired_tests/analyze.py
python -B -m unittest discover -s evaluation_script/tests -q
python -B generation/tests/test_launchers.py
```

The paired analysis reads the saved scores in `Results/`. Descriptive tables
and figures are provided in `analysis/descriptive/`. These commands run locally
without model calls or architecture-view generation.

The paired analysis uses all 68 projects for exact two-sided McNemar tests of L0.
L1/L2 comparisons use jointly L0-valid project pairs and exact conditional
Wilcoxon signed-rank tests, excluding zero differences and averaging tied ranks.
Holm correction is applied to all 165 comparisons as one family. The stored
results show **0 significant improvements, 15 significant decreases (all L2),
and 150 nonsignificant comparisons**. Exact sign tests preserve these
significance classifications.
Nonsignificance is not evidence of equivalence.

## Evaluation interpretation

- **L0:** syntax and representation validity.
- **L1:** correspondence to a reference view, including hierarchy-aware relation
  matching using frozen semantic alignments. It is not a proof of design
  correctness. Structural similarity is not an optimized graph edit distance.
- **L2:** completeness, faithfulness, architectural rationality, traceability,
  and readability on five-point scales, interpreted relative to the available
  SRS. Reasonable additions to underspecified requirements may receive low
  evidence-related ratings.
- **ReqCov:** binary coverage judgments for each curated requirement, aggregated
  within an output. Aggregate tables average output-level percentages.

Historical auxiliary ASR and inference-rate columns are
retained in the detailed L2 records but are not part of the eleven-metric paired
analysis.

## Scope and provenance

The original generated text and numerical judgments are preserved; published
text files use UTF-8/LF and repository-relative paths. Released digests therefore
can differ from source-file digests; both are recorded in the manifest.

Old human ratings of generated architectures and their agreement summaries are
not included. **SRS construction review records are retained**: 340 issues,
89.80% mean pairwise agreement, and Fleiss' kappa 0.7630. Those statistics concern
issue decisions, not architecture-score agreement or per-edge SRS/reference
support. The construction protocol also included a manual scope and key
responsibility/dependency support check; no additional per-edge agreement
statistic is claimed.

Source repositories and original reference artifacts retain their existing
attribution and licensing information. Do not infer a new blanket license for
third-party artifacts from this update. Citation metadata will be added when the
associated paper's publication details are final.
