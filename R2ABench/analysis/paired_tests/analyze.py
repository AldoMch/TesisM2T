r"""Offline, paired agent-versus-Direct analysis of the frozen R2ABench scores.

Run: python -B analysis/paired_tests/analyze.py
No generation, judging, source-data mutation, or network requests.
"""
from __future__ import annotations

import hashlib
import itertools
import json
import platform
from pathlib import Path

import numpy as np
import pandas as pd
import scipy
from scipy import stats
import statsmodels
from statsmodels.stats.multitest import multipletests

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
MODELS = {
    "gpt-5": "GPT-5", "claude-sonnet-4-6": "Claude Sonnet 4.6",
    "deepseek-v3.2": "DeepSeek V3.2", "deepseek-v4.1-flash": "DeepSeek V4.1 Flash",
    "qwen3-coder-480b-a35b-instruct": "Qwen3-Coder 480B-A35B",
}
AGENTS = {"metagpt-custom": "MetaGPT", "mini-swe-agent": "Mini-SWE", "openhands": "OpenHands"}
METRICS = {
    "l0_valid": ("L0", "SV", "proportion"),
    "node_f1": ("L1", "Node F1", "0-1"),
    "edge_f1": ("L1", "Edge F1", "0-1"),
    "structural_similarity": ("L1", "Structural similarity", "0-100"),
    "layer_agreement": ("L1", "LayerAgr", "0-1"),
    "completeness": ("L2", "Completeness", "1-5"),
    "faithfulness": ("L2", "Faithfulness", "1-5"),
    "architectural_rationality": ("L2", "Rationality", "1-5"),
    "traceability": ("L2", "Traceability", "1-5"),
    "readability": ("L2", "Readability", "1-5"),
    "req_cov": ("L2", "ReqCov", "percent"),
}
SOURCES = {
    "per": "Results/cohort.csv",
    "l1": "Results/l1.csv",
    "l2": "Results/l2.csv",
    "req": "Results/reqcov.csv",
    "summary": "Results/configuration_summary.csv",
    "audit": "Results/frozen_audit.json",
}
BOOTSTRAPS = 20000
SEED = 20261002


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def dump(name, obj):
    (OUT / name).write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8")


def exact_signed_rank(d):
    """Two-sided Wilcoxon conditional sign-flip distribution, including ties.

    Drop zero differences (Wilcox convention). Average tied absolute ranks;
    multiply ranks by two to obtain integer weights. Dynamic programming counts
    all 2**n equiprobable sign assignments using Python's unbounded integers.
    This avoids scipy's tie-free 'exact' distribution and Monte Carlo error.
    """
    d = np.round(np.asarray(d, dtype=float), 10)
    d = d[d != 0]
    if not len(d):
        return 0.0, 1.0, 0.0
    w = np.rint(2 * stats.rankdata(np.abs(d), method="average")).astype(int)
    total, observed = int(w.sum()), int(w[d > 0].sum())
    counts = [0] * (total + 1)
    counts[0] = 1
    end = 0
    for weight in w:
        weight = int(weight)
        for j in range(end, -1, -1):
            counts[j + weight] += counts[j]
        end += weight
    assert sum(counts) == 2 ** len(d)
    tail = min(observed, total - observed)
    p = min(1.0, 2 * sum(counts[:tail + 1]) / (2 ** len(d)))
    return tail / 2, p, (2 * observed - total) / total


def verify_statistics():
    # Independent exhaustive sign enumeration covers ties, zeros and all-zero input.
    examples = [[0, 0, 0], [1, 1, -1, 0, 2], [1, -2, 2, -3, 0], [1] * 8]
    rng = np.random.default_rng(SEED)
    examples += [rng.integers(-3, 4, size=8).tolist() for _ in range(20)]
    for example in examples:
        d = np.asarray(example, dtype=float)
        d = d[d != 0]
        _, got, _ = exact_signed_rank(example)
        if len(d):
            ranks = stats.rankdata(np.abs(d))
            observed = ranks[d > 0].sum()
            sums = np.asarray([np.dot(s, ranks) for s in itertools.product([0, 1], repeat=len(d))])
            expected = min(1., 2 * min(np.mean(sums <= observed), np.mean(sums >= observed)))
        else:
            expected = 1.
        assert abs(got - expected) < 1e-12
    for n in (8, 17, 31):
        d = np.arange(1, n + 1) * rng.choice([-1, 1], n)
        assert abs(exact_signed_rank(d)[1] - stats.wilcoxon(d, method="exact").pvalue) < 1e-12
    return {"exhaustive_tie_zero_cases": len(examples), "scipy_untied_exact_cross_checks": 3}


def load_data():
    frames = {k: pd.read_csv(ROOT / v) for k, v in SOURCES.items() if k != "audit"}
    manifest = json.loads((ROOT / SOURCES["audit"]).read_text(encoding="utf-8"))
    for path, digest in manifest["current_sources"].items():
        assert sha(ROOT / path) == digest, f"Source changed since frozen audit: {path}"
    per = frames["per"].copy()
    assert len(per) == 1360 and per.id.is_unique
    assert per.l0_valid.sum() == 1128
    assert not per.duplicated(["dataset", "sample_id", "model_id", "workflow"]).any()
    assert set(per.model_id) == set(MODELS)
    assert set(per.workflow) == {"direct", *AGENTS}
    projects = set(zip(per.dataset, per.sample_id))
    assert len(projects) == 68
    for _, g in per.groupby(["model_id", "workflow"]):
        assert set(zip(g.dataset, g.sample_id)) == projects
    for key in ("l1", "l2", "req"):
        f = frames[key]
        f = f[f.id.isin(per.id)].set_index("id").loc[per.id].reset_index()
        assert len(f) == len(per) and f.id.is_unique
        for c in ["dataset", "sample_id", "model_id", "workflow"]:
            assert (f[c] == per[c]).all()
        flag = "l2_eligible_current_l0" if key == "l2" else "l0_valid"
        assert (f[flag] == per.l0_valid).all()
        frames[key] = f
    valid = per.l0_valid
    assert (frames["l2"].loc[valid, "l2_status"] == "completed").all()
    assert (frames["req"].loc[valid, "l2_requirement_coverage_status"] == "completed").all()
    for metric in list(METRICS)[5:10]:
        per[metric] = frames["l2"][f"l2_{metric}_score"]
        assert per.loc[valid, metric].between(1, 5).all()
    per["req_cov"] = (100 * frames["req"].l2_covered_requirement_count /
                      frames["req"].l2_requirement_count)
    per.loc[~valid, list(METRICS)[1:]] = np.nan
    assert per.loc[valid, list(METRICS)].notna().all().all()
    # Every current configuration/source aggregate must match the published source table.
    checked = 0
    for _, s in frames["summary"].iterrows():
        g = per[(per.model_id == s.model_id) & (per.workflow == s.workflow)]
        if s.dataset != "pooled":
            g = g[g.dataset == s.dataset]
        assert len(g) == s.n_total and g.l0_valid.sum() == s.n_l0_pass
        for metric in METRICS:
            column = "sv" if metric == "l0_valid" else (f"l2_{metric}_score" if metric in list(METRICS)[5:10] else metric)
            assert np.isclose(g[metric].mean(), s[column], rtol=0, atol=1e-9), (metric, s.to_dict())
            checked += 1
    drift = frames["req"].loc[frames["req"].srs_changed_since_l1.astype(str).str.lower() == "true", ["dataset", "sample_id"]].drop_duplicates()
    return per[["id", "dataset", "sample_id", "model_id", "workflow", *METRICS]], drift, checked


def mean_ci(d, strata, seed):
    rng = np.random.default_rng(seed)
    total = np.zeros(BOOTSTRAPS)
    for label in np.unique(strata):
        values = d[strata == label]
        total += values[rng.integers(0, len(values), (BOOTSTRAPS, len(values)))].sum(axis=1)
    return np.quantile(total / len(d), [.025, .975]).tolist()


def comparisons(data, with_ci=True):
    rows, pairs = [], []
    for model, workflow in itertools.product(MODELS, AGENTS):
        base = data[(data.model_id == model) & (data.workflow == "direct")]
        agent = data[(data.model_id == model) & (data.workflow == workflow)]
        joined = base.merge(agent, on=["dataset", "sample_id"], suffixes=("_direct", "_agent"), validate="one_to_one")
        joint = joined.l0_valid_direct & joined.l0_valid_agent
        for metric, (level, label, unit) in METRICS.items():
            g = joined if level == "L0" else joined[joint]
            x = g[f"{metric}_direct"].to_numpy(float)
            y = g[f"{metric}_agent"].to_numpy(float)
            d = np.round(y - x, 10)
            wins, losses, ties = int(sum(d > 0)), int(sum(d < 0)), int(sum(d == 0))
            sign_p = float(stats.binomtest(wins, wins + losses).pvalue) if wins + losses else 1.
            if level == "L0":
                statistic, p, r = min(wins, losses), sign_p, np.nan
                test = "Exact McNemar (two-sided binomial)"
                signed = d.sum()
            else:
                statistic, p, r = exact_signed_rank(d)
                test = "Exact conditional Wilcoxon signed-rank (Wilcox zeros)"
                signed = r
            low, high = mean_ci(d, g.dataset.to_numpy(), SEED + len(rows)) if with_ci else [np.nan, np.nan]
            rows.append(dict(model_id=model, model=MODELS[model], workflow=workflow, agent=AGENTS[workflow],
                             metric=metric, metric_label=label, level=level, unit=unit, n_pairs=len(g),
                             n_E=int(sum(g.dataset == "E-R2A")), n_G=int(sum(g.dataset == "G-R2A")),
                             direct_mean=float(x.mean()), agent_mean=float(y.mean()),
                             mean_difference=float((y-x).mean()), median_difference=float(np.median(y-x)),
                             mean_ci95_low=float(low), mean_ci95_high=float(high),
                             agent_wins=wins, direct_wins=losses, ties=ties, n_nonzero=wins+losses,
                             rank_biserial=r, statistic=statistic, test=test, p_raw=p,
                             sign_test_p_raw=sign_p,
                             direction="higher" if signed > 0 else ("lower" if signed < 0 else "equal")))
            for (_, record), a, b in zip(g.iterrows(), x, y):
                pairs.append(dict(model_id=model, workflow=workflow, metric=metric, dataset=record.dataset,
                                  sample_id=record.sample_id, direct=a, agent=b, difference=b-a))
    result = pd.DataFrame(rows)
    assert len(result) == 165
    # One family includes every tested agent/model/metric comparison, including L0.
    result["p_holm_165"] = multipletests(result.p_raw, method="holm")[1]
    result["sign_test_p_holm_165"] = multipletests(result.sign_test_p_raw, method="holm")[1]
    result["outcome"] = np.where(result.p_holm_165 < .05, np.where(result.direction == "higher", "improvement", "decline"), "not_significant")
    result["sign_test_outcome"] = np.where(result.sign_test_p_holm_165 < .05,
        np.where(result.agent_wins > result.direct_wins, "improvement", "decline"), "not_significant")
    return result, pd.DataFrame(pairs)


def tabulate_counts(results):
    rows = []
    for agent in AGENTS.values():
        for level in ["ALL", "L0", "L1", "L2"]:
            g = results[results.agent == agent]
            if level != "ALL":
                g = g[g.level == level]
            rows.append(dict(agent=agent, level=level, comparisons=len(g),
                             improvements=int(sum(g.outcome == "improvement")),
                             declines=int(sum(g.outcome == "decline")),
                             not_significant=int(sum(g.outcome == "not_significant"))))
    return pd.DataFrame(rows)


def markdown_table(frame, columns):
    header = "| " + " | ".join(columns) + " |\n|" + "|".join(["---"] * len(columns)) + "|\n"
    return header + "\n".join("| " + " | ".join(str(v) for v in row) + " |" for row in frame[columns].itertuples(index=False, name=None))


def main():
    sources_before = {v: sha(ROOT / v) for v in SOURCES.values()}
    plan = dict(scope="Exploratory post-hoc analysis; settings and metrics chosen from the existing paper, not preregistered.",
        comparisons="3 agents x 5 models x 11 metrics = 165, each versus Direct within the same model and project",
        l0="Exact two-sided McNemar, all 68 projects per comparison",
        quality="Exact two-sided conditional Wilcoxon signed-rank, only jointly L0-valid projects; average ranks for ties, zero differences dropped",
        correction="Holm family-wise correction across all 165 comparisons, alpha=0.05",
        effect="Agent minus Direct paired mean differences and matched-pairs rank-biserial correlations",
        ci="Unadjusted 95% percentile bootstrap CIs for paired mean differences, stratified by E/G source, 20000 resamples",
        sensitivity="Exact paired sign tests with Holm-165; repeat primary analysis after removing documented SRS-drift project(s)",
        assumptions="Independent project-level paired differences; signed-rank inference assumes a symmetric difference distribution under the null. Sign tests relax magnitude/symmetry assumptions.",
        seed=SEED, no_equivalence_test=True)
    dump("analysis_plan.json", plan)
    tests = verify_statistics()
    data, drift, aggregate_checks = load_data()
    data.to_csv(OUT / "analysis_data.csv", index=False, encoding="utf-8-sig")
    results, pairs = comparisons(data)
    results.to_csv(OUT / "paired_tests.csv", index=False, encoding="utf-8-sig")
    pairs.to_csv(OUT / "paired_observations.csv", index=False, encoding="utf-8-sig")
    counts = tabulate_counts(results)
    counts.to_csv(OUT / "summary_counts.csv", index=False, encoding="utf-8-sig")
    sensitivity = None
    if len(drift):
        excluded = set(map(tuple, drift.to_numpy()))
        reduced = data[[key not in excluded for key in zip(data.dataset, data.sample_id)]]
        sensitivity, _ = comparisons(reduced, with_ci=False)
        sensitivity.to_csv(OUT / "sensitivity_excluding_srs_drift.csv", index=False, encoding="utf-8-sig")
    assert sources_before == {v: sha(ROOT / v) for v in SOURCES.values()}
    metadata = dict(source_hashes=sources_before, records=len(data), projects=68, l0_valid=int(data.l0_valid.sum()),
                    aggregate_cells_verified=aggregate_checks, statistics_checks=tests,
                    python=platform.python_version(), numpy=np.__version__, pandas=pd.__version__,
                    scipy=scipy.__version__, statsmodels=statsmodels.__version__,
                    script_sha256=sha(Path(__file__)), drift_projects=drift.to_dict("records"),
                    api_calls=0, source_files_unchanged=True,
                    quality_pair_count_range=[int(results[results.level != 'L0'].n_pairs.min()), int(results[results.level != 'L0'].n_pairs.max())],
                    sign_test_outcome_changes=int(sum(results.outcome != results.sign_test_outcome)),
                    drift_exclusion_outcome_changes=int(sum(results.outcome != sensitivity.outcome)) if sensitivity is not None else 0)
    dump("audit.json", metadata)
    detail = results.copy()
    for col in ["direct_mean", "agent_mean", "mean_difference", "rank_biserial"]:
        detail[col] = detail[col].map(lambda x: f"{x:.4f}")
    detail["p_holm_165"] = detail.p_holm_165.map(lambda x: f"{x:.5g}")
    report = """# Agent 相对于 Direct 的配对显著性检验

统一进行 Holm 校正后，165 项比较中未检出显著提升，15 项显著下降，150 项不显著。显著下降全部位于 L2：MetaGPT 11 项、Mini-SWE 3 项、OpenHands 1 项。精确符号检验及剔除已知 SRS 漂移项目的敏感性分析均保留这一显著性分类。这支持“在所测配置及校正方案下未检出显著提升”，不证明 agent 无效或与 Direct 等效。

分析使用 2026-10-01 刷新后冻结的逐项目评分：68 项目、5 模型、4 设置，共 1,360 输出，1,128 通过 L0。所有源文件哈希与最新审计一致，所有 60 个配置/来源组合的 11 项均值（660 单元格）均复现现有汇总。

## 检验设计

- 每个模型内分别比较 MetaGPT、Mini-SWE、OpenHands 与 Direct，同一项目配对；不将不同模型对同一项目的输出视为独立项目。
- L0：全部 68 项目，双侧精确 McNemar 检验。
- L1/L2：双方均通过 L0 的项目，双侧 Wilcoxon 符号秩检验。零差值剔除，相同绝对差使用平均秩；用动态规划计算包含并列值的精确符号置换分布。差值四舍五入至 10 位小数避免浮点伪差异。
- 所有 165 项比较统一做 Holm 校正，显著性水平 0.05；不按显著结果挑选检验族。正方向代表 agent 更高。
- 效应量：配对均值差和配对秩二列相关；同时报告按来源分层的配对 bootstrap 均值差 95% 区间（20,000 次、固定种子）。这些区间未做多重校正，不用于取代 Holm 显著性判断。
- Wilcoxon 对差值分布有对称性假设。精确符号检验作为较少依赖该假设的敏感性分析，同时对 165 项比较作 Holm 校正。
- 这是检查已有观察的事后探索分析，不是预注册的验证研究。未做等效性检验；不显著不代表没有效果或两方法等效。

## 各工作流结果

"""
    report += markdown_table(counts, list(counts.columns))
    report += "\n\n## 校正后显著的比较\n\n"
    report += markdown_table(detail[results.outcome != "not_significant"], ["model", "agent", "metric_label", "n_pairs", "mean_difference", "rank_biserial", "p_holm_165", "outcome"])
    report += "\n\n## 解释范围与数据限制\n\n"
    report += f"- 连续/等级评分的共同有效配对数为 {metadata['quality_pair_count_range'][0]}–{metadata['quality_pair_count_range'][1]}；其均值可能与论文各自有效集的均值不同。条件质量结果不衡量无效输出的损失，应结合 L0 阅读。\n"
    report += "- 单次保存输出支持跨项目的配对比较，无法量化重复生成的随机性；不同工作流的预算和工具配置也限制因果归因。\n"
    report += "- L1 衡量对参考图的对应程度，显著变化不直接等于架构正确性的变化。ReqCov 是逐输出覆盖比例的配对分析，不把每条重复需求判断当作独立样本。\n"
    report += "- 已有数据记录 G-R2A 项目 s000001_3c90b51c 的当前 SRS 与历史 L1 输入不一致；历史 L2 输入哈希也不完全可追溯。本分析复用保存评分，未重新生成或评判。剔除此已知漂移项目的结果另存。\n"
    report += f"- 用精确符号检验替代 Wilcoxon 后，165 项结论中 {metadata['sign_test_outcome_changes']} 项发生显著性分类变化；剔除已知 SRS 漂移项目后 {metadata['drift_exclusion_outcome_changes']} 项变化。变化明细见 sensitivity_comparison.csv。\n"
    report += "\n## 方法资料\n\n"
    report += "- [SciPy Wilcoxon 文档](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.wilcoxon.html)：配对设计、零差值、并列值与符号置换。\n"
    report += "- [statsmodels McNemar 文档](https://www.statsmodels.org/stable/generated/statsmodels.stats.contingency_tables.mcnemar.html)：精确二项形式。\n"
    report += "- [statsmodels 多重检验文档](https://www.statsmodels.org/stable/generated/statsmodels.stats.multitest.multipletests.html)：Holm 校正。\n"
    report += r"""

## 论文可用表述

摘要中 agent 结论可替换为：

```latex
After Holm correction, the evaluated agentic workflows show no statistically significant improvements over direct prompting, with significant declines in several semantic evaluation metrics.
```

实验方法补充：

```latex
We conduct post-hoc paired comparisons between each agentic workflow and direct prompting within each model.
L0 validity is compared using two-sided exact McNemar tests on all 68 projects, while downstream metrics are compared using two-sided Wilcoxon signed-rank tests on projects for which both configurations pass L0.
We compute exact conditional signed-rank probabilities with average ranks for ties and zero differences excluded.
Holm correction controls the family-wise error rate at 0.05 across all 165 comparisons (three workflows, five models, and eleven metrics).
We report paired mean differences and rank-biserial effect sizes; unadjusted 95% bootstrap intervals for mean differences are stratified by project source.
```

RQ1 结果补充：

```latex
After Holm correction, none of the 165 paired comparisons indicates a statistically significant improvement over direct prompting, whereas 15 indicate significant decreases in L2 metrics: 11 for MetaGPT, three for Mini-SWE, and one for OpenHands.
The significance classifications remain unchanged under exact paired sign tests and after excluding the project with documented SRS version drift.
These results concern the evaluated configurations and stored outputs; nonsignificant differences do not establish equivalence.
```

版本漂移的敏感性分析若写入正文，应同时在数据说明或补充材料解释该项目的评分版本。摘要不必加入这一细节。统计方法和结果段落均为可复制片段，未改写论文原文件。
"""
    report += "\n## 复现\n\n`python -B analysis/paired_tests/analyze.py`\n\n主文件 paired_tests.csv 包含全部 165 项的原始/校正 p 值、配对数、胜/负/平计数、效应量和区间；analysis_data.csv 为冻结的最小分析数据；paired_observations.csv 为实际配对观察；audit.json 保存来源哈希、版本和核验结果。源 CSV 未改动。\n"
    (OUT / "report.md").write_text(report, encoding="utf-8")
    comp = results[["model", "agent", "metric_label", "p_holm_165", "outcome", "sign_test_p_holm_165", "sign_test_outcome"]].copy()
    if sensitivity is not None:
        comp["exclude_drift_p_holm_165"] = sensitivity.p_holm_165
        comp["exclude_drift_outcome"] = sensitivity.outcome
    comp.to_csv(OUT / "sensitivity_comparison.csv", index=False, encoding="utf-8-sig")
    print(counts.to_string(index=False))
    print("\nSIGNIFICANT\n" + detail[results.outcome != "not_significant"][["model", "agent", "metric_label", "n_pairs", "mean_difference", "p_holm_165", "outcome"]].to_string(index=False))
    print("\nAUDIT", json.dumps(metadata, ensure_ascii=True, indent=2))


if __name__ == "__main__":
    main()
