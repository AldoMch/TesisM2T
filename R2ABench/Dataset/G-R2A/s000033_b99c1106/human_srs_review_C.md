<!-- human_srs_review_A.md 由审阅者 A 生成。保留原始 human_srs_review.md。所有人类的判断都是英语的。 -->

# 人类 SRS 审查表

## 元数据

- 示例目录：`s000033_b99c1106`
- 生成SRS：`final_srs.md`
- 证据包：`evidence_pack.json`
- 评测型号：`claude-opus-4-8`
- 生成于：`2026-06-05T15:43:09.391137Z`
- 原始模型响应：`model_srs_review_raw.md`
- 解析状态：`parsed`

## 总体模型意见

- 推荐：`revise`
- 置信度：`0.78`
- 理由：SRS 内部一致，并且可以很好地追踪到小型证据包，但它大大夸大了存储库范围。该存储库是一个 Airflow+Spark 集成环境（deployment_config、文档、测试、架构图），但 SRS 几乎所有需求都来自通用上游 Spark README 和捆绑的 Spark 示例文件。最独特的产品行为（Airflow 编排 Spark 作业、Docker Compose 部署）的代表性不足，而通用 Spark 功能则过高地满足了产品要求。

## 人类整体决策

- [ ] 接受
- [ ] 拒绝
- [x] 部分接受

原因：
> ACCEPT=3，PARTIAL_ACCEPT=2，REJECT=0，PARTIAL_ACCEPT=0。

## 积极的观察

- 每个功能和非功能需求都带有证据ID，并且可追溯性矩阵与引用的块一致。
- NFR-002 中的依赖版本是从 E002 准确转录的（celery==4.1.1、kombu==4.2.0、tornado==5.1.1、werkzeug==0.16.0、SQLAlchemy==1.3.15、pyspark）。
- SRS 正确地捕获了 requirements.txt 注释中的关键原理，即 Airflow 机器内的 Spark 提交需要 pyspark（FR-004、C-002）。
- FR-001（返回 1000）和 NFR-001/002（版本/固定部门检查）的验收标准是具体且可验证的。
- 该文档在限制对已证实的执行目标的声明方面相当保守，而不是发明额外的 Spark 功能。

## 候选人问题

### R001：范围

- 严重性：`major`
- 建议采取的措施：`partial_accept_as_issue`
- SRS 位置：第1节产品范围；第 4 节 功能要求（FR-001、FR-002、FR-005）
- 证据 IDs：E001、E002

**索赔或差距**

SRS 将通用上游 Spark 功能（`./bin/pyspark`、`./bin/run-example`、libsvm 示例加载）视为核心产品要求，而存储库的实际产品是 Airflow+Spark 与 Docker Compose 部署和基于 DAG 的编排的集成。

**模型意见**

FR-001、FR-002 和 FR-005 源自供应商的 Spark 发行版的库存 README 和 Apache 示例源。这些描述了 Apache Spark 本身，而不是 cordon-thiago/airflow-spark 的差异化行为。证据包报告类别部署（91 次点击）和功能（123 次点击）以及包括部署配置和测试在内的文档类型，以及架构图，但这些都没有反映在功能需求中。 SRS 低估了集成/编排范围并夸大了通用 Spark 功能。

**推荐人工检查**

检查 docker-compose.yml、dags/ 目录和架构图 (doc/architecture.png) 以确认 Airflow-orchestrates-Spark 行为和 Docker Compose 多服务部署，然后添加相应的要求。

**型号建议更改 SRS**

在第 1 节“产品范围”中，添加一句话，阐明该产品是一个集成的 Airflow+Spark Docker 环境，用于从 Airflow DAGs 编排 Spark 作业。添加新的 FR（e.g.、FR-006），涵盖 Airflow DAG 驱动的 Spark 作业提交，以确认 dags/ 和 docker-compose 证据为条件；降级 FR-002/FR-005 优先级或将它们标记为继承的 Spark 分发行为。

可选的人工修订修复：
> 改 final_srs.md (line 8) 产品范围、final_srs.md (line 32) 功能概述、final_srs.md (line 84) 功能需求。应补充“Airflow DAG 驱动 Spark 作业提交到 Spark standalone 集群”的产品核心行为；同时把 FR-001/FR-002/FR-005 标注为“继承的 Spark 发行版能力”，不要继续当成最核心产品差异。

**人为决定**

- [ ] 接受
- [ ] 拒绝
- [x] 部分接受（`PARTIAL_ACCEPT`：混合声明；有些有效，有些无效）

可选的人工注释：
> 模型意见成立：当前 SRS 的范围偏向“原生 Spark 发行版”，而不是这个仓库真正提供的 Airflow-Spark 编排环境。

### R002：缺少需求

- 严重性：`major`
- 建议采取的措施：`accept_as_issue`
- SRS 位置：第 2 节 运行环境；第 3 节 外部接口；第 7 节 限制
- 证据 IDs：无

**索赔或差距**

尽管部署是最大的证据类别，但没有要求描述 Docker Compose 部署拓扑（Airflow Web 服务器/调度程序、Spark master/workers、数据库）。

**模型意见**

证据包显示document_types包括deployment_config和category_hitsdeployment=91，是功能之后的最高值。存储库名称和 architecture.png 强烈暗示多容器部署。 SRS 仅模糊地引用了“Dockerized Airflow 环境”，没有服务组合、端口或启动要求。对于集成产品来说，这是一个巨大的差距。

**推荐人工检查**

打开docker-compose.yml / Dockerfile(s)和architecture.png枚举服务、暴露的端口以及服务间依赖关系；相应地添加部署要求。

**型号建议更改 SRS**

添加部署要求小节（或 DR/NFR 条目），指定 Docker Compose 服务集及其从 docker-compose.yml 确认后的关系。条件编辑：验证 compose 文件后，“系统应可通过包含 <services> 和 <ports> 的 Docker Compose 进行部署”。

可选的人工修订修复：
> 推荐新增部署要求：
> DEP-001: The system shall be deployable through Docker Compose with the following services:
> - `postgres`, using PostgreSQL 9.6 and exposing port 5432.
> - `airflow-webserver`, exposing Airflow on port 8282 and depending on Postgres.
> - `spark`, acting as Spark standalone master and exposing web UI port 8181 and cluster port 7077.
> - `spark-worker-1`, `spark-worker-2`, and `spark-worker-3`, each connected to `spark://spark:7077`.
> - `jupyter-spark`, exposing Jupyter on port 8888 and Spark application UI ports 4040-4080.
> DEP-002: The Airflow, Spark, and Jupyter services shall share mounted directories for DAGs, Spark applications, notebooks, and input data so that submitted jobs can access the same application and resource files.



**人为决定**

- [x] 接受
- [ ] 拒绝
- [ ] 部分接受（`PARTIAL_ACCEPT`：混合声明；有些有效，有些无效）

可选的人工注释：
> 这个 issue 很重要。SRS 缺少 Docker Compose 部署拓扑要求，但源码里 docker-compose.yml 明确给出了产品运行结构。

### R003：可追溯性

- 严重性：`minor`
- 建议采取的措施：`partial_accept_as_issue`
- SRS 位置：第 9 节可追溯性矩阵与第 5 节 NFR-003 / 第 1 节参考
- 证据IDs：E001

**索赔或差距**

NFR-003 置信度在可追溯性矩阵中被列为“高”，但派生的“至少五种形式”声称它解释单个 README 句子；参考文献仅列出了 4 个证据 IDs，而包装中包含未使用的 E003/E004。

**模型意见**

“至少五个执行目标表单”要求是对 E001 的合理解读，但它是通用 Spark 功能，而不是特定于产品的要求；将其标记为高可信度产品 NFR 夸大了其相关性。此外，E003 (JavaPageRank) 和 E004 (conf.py) 出现在包中，但未引用 - 可以接受，但参考文献部分可以注明已考虑但为了透明度而排除的证据。

**推荐人工检查**

确认“五个执行目标”是有意义的产品需求还是仅仅继承了 Spark 行为；相应地调整置信度/优先级。

**型号建议更改 SRS**

在第 9 节中，将 NFR-003 置信度从“高”更改为“中”，并将其注释为继承的 Spark 分发功能而不是特定于产品。

可选的人工修订修复：
> 建议在 NFR-003 traceability (line 143) 修改为：
> NFR-003: The system should preserve compatibility with Spark-supported master URL formats where the bundled Spark distribution supports them. In this project, the directly configured and deployable cluster target is `spark://spark:7077`; other master URL forms are inherited Spark capabilities and are not independently deployed by this repository.
> Confidence: Medium
> Rationale: The evidence supports Spark-level syntax compatibility, while the project-specific Docker Compose topology validates only the standalone Spark master configuration.

**人为决定**

- [ ] 接受
- [ ] 拒绝
- [x] 部分接受（`PARTIAL_ACCEPT`：混合声明；有些有效，有些无效）

可选的人工注释：
> 模型对 NFR-003 的质疑成立，但不应简单删除。当前 NFR-003 (line 100) 把“支持五种 master URL 形式”写得像产品级质量需求，置信度还偏高。实际它更多来自 Spark upstream 文档，是继承能力，不是此 Compose 项目专门实现的架构能力。

### R004：不可验证

- 严重性：`minor`
- 建议采取的措施：`accept_as_issue`
- SRS 位置：第 8 部分，FR-003 验收标准
- 证据IDs：E001

**索赔或差距**

FR-003 接受标准“导致提交使用该目标语法而不拒绝接口”是模糊的并且无法清楚地观察到。

**模型意见**

该标准未定义可观察到的通过/失败信号（e.g.、作业到达指定的主节点，或 Spark-submit 记录主节点 URL）。 “没有接口拒绝”是不明确的。由于只有 local/SparkPi 被证明在 README 中实际可运行，因此在此存储库中测试 mesos/yarn/standalone 端到端可能不可行。

**推荐人工检查**

确定非本地主控是否在存储库中实际配置/可用；如果不是，则将可验证的验收标准限制为本地模式。

**型号建议更改 SRS**

将FR-003验收标准修改为：'对于本地和本地[N]，`./bin/run-example SparkPi`在设置的MASTER下运行完成；对于 mesos/spark/yarn 表单，验证仅限于确认 MASTER 值已传递给 Spark-submit（语法接受）。

可选的人工修订修复：
> 本仓库真实配置的 standalone Spark 要做端到端验证；其他 upstream Spark master 形式只作为语法兼容或继承能力说明。
> Acceptance criteria for FR-003:
> - For the configured Docker Compose deployment, Airflow shall submit a Spark job to `spark://spark:7077` through the `spark_default` connection, and the run shall be observable in Airflow task logs and the Spark master UI.
> - For local Spark execution, `local` or `local[N]` shall be accepted by Spark commands using the bundled Spark distribution.
> - Mesos, YARN, and other Spark-supported master URL formats shall be documented as inherited Spark capabilities unless this repository provides deployment configuration and an executable verification path for them.

**人为决定**

- [x] 接受
- [ ] 拒绝
- [ ] 部分接受（`PARTIAL_ACCEPT`：混合声明；有些有效，有些无效）

可选的人工注释：
> 当前 FR-003 的验收标准 (line 125) 写成“uses corresponding target syntax and interface does not reject”太弱，不可验证。

### R005：架构_详细信息

- 严重性：`minor`
- 建议采取的措施：`accept_as_issue`
- SRS 位置：第二节 产品视角/运行环境
- 证据 IDs：无

**索赔或差距**

候选元数据中引用了架构图 (doc/architecture.png)，但其内容未反映在 SRS 中的任何位置。

**模型意见**

真实情况中存在架构图，但 SRS 除了“Dockerized Airflow 环境”之外不包含任何架构描述。这是在权威图表中错过了展示产品视角的机会，并且可能表明 SRS 缺少显示的组件（e.g.、PostgreSQL、Spark master/worker、Jupyter）。

**推荐人工检查**

查看 doc/architecture.png 并将所描述的组件与第 2 部分进行协调；添加 SRS 中显示但不存在的任何组件。

**型号建议更改 SRS**

在第 2 节产品视角中添加一个简短的架构段落，枚举审核后 doc/architecture.png 中显示的组件（以图表内容为条件）。

可选的人工修订修复：
> 建议在 Product Perspective (line 29) 或 Operating Environment (line 45) 增加架构说明。Architecture context: The system is deployed as a Docker Compose environment containing Airflow, Postgres, a Spark standalone cluster, and Jupyter/PySpark. Users can schedule Spark jobs through Airflow or run interactive workloads through Jupyter. Airflow stores metadata in Postgres and submits configured Spark applications to the Spark standalone cluster, which executes the workloads through its worker services. Shared mounted directories provide access to DAGs, Spark applications, notebooks, and data resources.

**人为决定**

- [x] 接受
- [ ] 拒绝
- [ ] 部分接受（`PARTIAL_ACCEPT`：混合声明；有些有效，有些无效）

可选的人工注释：
> 地架构图明确展示了 Data Engineer、Postgres、Airflow/Spark Driver、Jupyter Notebook、Spark Cluster Manager 和多个 Worker 的关系。SRS 当前只写命令行和 Spark 能力，会漏掉实际系统的组件协作方式。
