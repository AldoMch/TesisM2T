# Agent 相对于 Direct 的配对显著性检验

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

| agent | level | comparisons | improvements | declines | not_significant |
|---|---|---|---|---|---|
| MetaGPT | ALL | 55 | 0 | 11 | 44 |
| MetaGPT | L0 | 5 | 0 | 0 | 5 |
| MetaGPT | L1 | 20 | 0 | 0 | 20 |
| MetaGPT | L2 | 30 | 0 | 11 | 19 |
| Mini-SWE | ALL | 55 | 0 | 3 | 52 |
| Mini-SWE | L0 | 5 | 0 | 0 | 5 |
| Mini-SWE | L1 | 20 | 0 | 0 | 20 |
| Mini-SWE | L2 | 30 | 0 | 3 | 27 |
| OpenHands | ALL | 55 | 0 | 1 | 54 |
| OpenHands | L0 | 5 | 0 | 0 | 5 |
| OpenHands | L1 | 20 | 0 | 0 | 20 |
| OpenHands | L2 | 30 | 0 | 1 | 29 |

## 校正后显著的比较

| model | agent | metric_label | n_pairs | mean_difference | rank_biserial | p_holm_165 | outcome |
|---|---|---|---|---|---|---|---|
| GPT-5 | MetaGPT | Completeness | 58 | -0.5517 | -0.8891 | 1.0161e-05 | decline |
| GPT-5 | MetaGPT | Faithfulness | 58 | -0.4828 | -0.8750 | 7.0893e-05 | decline |
| GPT-5 | MetaGPT | Rationality | 58 | -0.3621 | -0.8406 | 0.0088501 | decline |
| GPT-5 | MetaGPT | Traceability | 58 | -0.4483 | -0.9286 | 6.5982e-05 | decline |
| GPT-5 | Mini-SWE | Completeness | 49 | -0.4286 | -0.7785 | 0.018921 | decline |
| GPT-5 | Mini-SWE | Traceability | 49 | -0.4082 | -0.8333 | 0.0096667 | decline |
| GPT-5 | OpenHands | ReqCov | 56 | -4.7151 | -1.0000 | 0.0096667 | decline |
| Claude Sonnet 4.6 | Mini-SWE | ReqCov | 57 | -4.6418 | -1.0000 | 0.037109 | decline |
| DeepSeek V3.2 | MetaGPT | Completeness | 37 | -0.5676 | -1.0000 | 0.001236 | decline |
| DeepSeek V3.2 | MetaGPT | Rationality | 37 | -0.4324 | -1.0000 | 0.0096667 | decline |
| DeepSeek V3.2 | MetaGPT | Readability | 37 | -0.4865 | -0.9000 | 0.011307 | decline |
| DeepSeek V4.1 Flash | MetaGPT | Traceability | 66 | -0.3333 | -0.7354 | 0.029698 | decline |
| DeepSeek V4.1 Flash | MetaGPT | Readability | 66 | -0.3333 | -0.8462 | 0.001689 | decline |
| Qwen3-Coder 480B-A35B | MetaGPT | Rationality | 28 | -0.5000 | -1.0000 | 0.018921 | decline |
| Qwen3-Coder 480B-A35B | MetaGPT | Readability | 28 | -0.5357 | -0.8824 | 0.041473 | decline |

## 解释范围与数据限制

- 连续/等级评分的共同有效配对数为 22–66；其均值可能与论文各自有效集的均值不同。条件质量结果不衡量无效输出的损失，应结合 L0 阅读。
- 单次保存输出支持跨项目的配对比较，无法量化重复生成的随机性；不同工作流的预算和工具配置也限制因果归因。
- L1 衡量对参考图的对应程度，显著变化不直接等于架构正确性的变化。ReqCov 是逐输出覆盖比例的配对分析，不把每条重复需求判断当作独立样本。
- 已有数据记录 G-R2A 项目 s000001_3c90b51c 的当前 SRS 与历史 L1 输入不一致；历史 L2 输入哈希也不完全可追溯。本分析复用保存评分，未重新生成或评判。剔除此已知漂移项目的结果另存。
- 用精确符号检验替代 Wilcoxon 后，165 项结论中 0 项发生显著性分类变化；剔除已知 SRS 漂移项目后 0 项变化。变化明细见 sensitivity_comparison.csv。

## 方法资料

- [SciPy Wilcoxon 文档](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.wilcoxon.html)：配对设计、零差值、并列值与符号置换。
- [statsmodels McNemar 文档](https://www.statsmodels.org/stable/generated/statsmodels.stats.contingency_tables.mcnemar.html)：精确二项形式。
- [statsmodels 多重检验文档](https://www.statsmodels.org/stable/generated/statsmodels.stats.multitest.multipletests.html)：Holm 校正。


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

## 复现

`python -B analysis/paired_tests/analyze.py`

主文件 paired_tests.csv 包含全部 165 项的原始/校正 p 值、配对数、胜/负/平计数、效应量和区间；analysis_data.csv 为冻结的最小分析数据；paired_observations.csv 为实际配对观察；audit.json 保存来源哈希、版本和核验结果。源 CSV 未改动。
