# Evaluation implementation

The paired statistical analysis of the saved paper results runs offline with:

```bash
python -B analysis/paired_tests/analyze.py
```

`l0_syntax.py` performs renderer/parser checks. `plantuml_parser.py` extracts
component-style PlantUML. `l1_structural.py` obtains semantic alignment using the
`l1-correspondence-v2` protocol; `l1_metrics.py` implements entity metrics.
`l1_hierarchy.py` computes the hierarchy-aware relation correspondence used in
the released results. Frozen v2 caches are included alongside valid views.

`Results/l1.csv` contains the saved hierarchy-aware L1 metrics.

`l2_semantic.py` contains the five-dimensional rubric. `reqcov.py` implements
curated requirement coverage and validates evidence. The prompt texts are
`prompts/semantic_frozen.txt` and `reqcov_prompt.txt`, respectively.
Historical inference-rate/ASR fields are supplementary.

For a new evaluation, inspect `python -m evaluation_script.evaluate --help`.
This general-purpose batch entry point uses the v2 alignment/metric pipeline;
the paper's hierarchy-aware edge metrics are the subsequent offline
`evaluate_hierarchy` step, not the unmodified batch v2 edge scores. New model
judgments require an explicitly configured OpenAI-compatible provider:

```bash
export OPENAI_API_KEY="YOUR_API_KEY"
export OPENAI_BASE_URL="YOUR_PROVIDER_BASE_URL"
export OPENAI_MODEL="YOUR_JUDGE_MODEL"
```

Configure PlantUML through `PLANTUML_CMD` or `PLANTUML_JAR` when rendering fresh
outputs. The released offline analyses do not require a renderer or API key.

Reference mismatches do not independently establish design errors. L2 support
is assessed against the SRS. The five-point scores are not probabilities.
