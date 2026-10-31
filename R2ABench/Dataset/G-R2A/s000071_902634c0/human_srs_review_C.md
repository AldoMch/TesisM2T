<!-- human_srs_review_A.md 由审阅者 A 生成。保留原始 human_srs_review.md。所有人类的判断都是英语的。 -->

# 人类 SRS 审查表

## 元数据

- 示例目录：`s000071_902634c0`
- 生成SRS：`final_srs.md`
- 证据包：`evidence_pack.json`
- 评测型号：`claude-opus-4-8`
- 生成于：`2026-06-05T16:03:21.681103Z`
- 原始模型响应：`model_srs_review_raw.md`
- 解析状态：`parsed`

## 总体模型意见

- 推荐：`revise`
- 置信度：`0.82`
- 理由：SRS 在证据包中基本有充分依据，并且可追溯性总体上是健全的。然而，存在一个明显的内部矛盾（FR-004/NFR-001 规定了 2 秒默认值，而产品功能摘要模糊地描述了报告周期）以及描述行为的几项要求（e.g.、标准输出的捕获/日志、ping 连接），这些要求是超出字面配置证据推断的。 README 证据 (E001) 被截断，并且架构图不在证据包中，因此 Kubernetes-flow 声明和架构细节需要人工确认。

## 人类整体决策

- [ ] 接受
- [ ] 拒绝
- [x] 部分接受

原因：
> ACCEPT=4，PARTIAL_ACCEPT=1，REJECT=2，PARTIAL_ACCEPT=0。

## 积极的观察

- 强大的可追溯性规则：每个 FR/NFR 都引用具体证据 IDs，并且大多数直接映射到可验证的配置值 (E002) 或代码结构 (E003-E006)。
- 数值遥测默认值（report_period_sec: 2、ping_period_sec: 30）和 report_global_mem_used 语义是从 E002 中准确提取的。
- SRS 适当地将 GUI/CLI、存储和隐私要求的缺失标记为不受支持，而不是发明它们。
- 服务版本标记（v2.4 模型、v2.5 事件）正确绑定到 E004/E005 中的 NFR-003 和 C-004。

## 候选人问题

### R001：矛盾

- 严重性：`minor`
- 建议采取的措施：`probably_ignore`
- SRS 位置：第二部分 产品功能总结 对比 FR-004/NFR-001
- 证据IDs：E002

**索赔或差距**

产品功能摘要引用 E002 表示“定期报告工作人员状态”，但未说明该值，而 FR-004 规定默认值为 2 秒，FR-005/NFR-001 规定 30 秒 ping。证据 (E002) 显示 report_period_sec: 2 和 ping_period_sec: 30，因此数字要求是正确的，但 E002 下的“ping 服务器”摘要分组是一致的。价值观上没有严重矛盾，但摘要缺乏下游的数字细节。

**模型意见**

这是一致性/完整性问题，而不是真正的矛盾。 FR-004 (2s) 和 FR-005 (30s) 中的值与 E002 匹配。值得调整摘要，但风险较低。

**推荐人工检查**

确认 E002 确实显示了 report_period_sec: 2 和 ping_period_sec: 30（确实如此），并确定摘要是否需要显式值。

**型号建议更改 SRS**

在第二节产品功能汇总中，将“定期上报worker状态并ping服务器（E002）”修改为“定期上报worker状态（默认每2s）并ping服务器（默认每30s）（E002）”。

可选的人工修订修复：
> 

**人为决定**

- [ ] 接受
- [x] 拒绝
- [ ] 部分接受（`PARTIAL_ACCEPT`：混合声明；有些有效，有些无效）

可选的人工注释：
> sdk.conf 中确实是 report_period_sec: 2、ping_period_sec: 30，SRS 的 FR-004/FR-005/NFR-001 与证据一致；Product summary 只是没写默认值，不构成矛盾。

### R002：不支持的声明

- 严重性：`major`
- 建议采取的措施：`accept_as_issue`
- SRS 位置：FR-006，第 2 节产品功能（“可选择记录 stdout 和 stderr”）
- 证据IDs：E002

**索赔或差距**

FR-006 将 stdout/stderr 日志记录设置为条件（“当启用 stdout/stderr 日志记录时”）并将 log_stdout 引用为启用标志。 E002 显示“log_stdout：true”，并带有注释“记录所有 stdout 和 stderr”，i.e.，默认启用，并且证据不显示运行时捕获/禁用行为或它是“可选”。推断“启用/禁用”语义。

**模型意见**

配置键存在且默认为 true，但证据并未展示切换行为或实际捕获管道。将其表述为可配置的启用/禁用是一个合理的推论，但稍微超出了字面证据。应标记为推断或软化。

**推荐人工检查**

检查 log_stdout 是否实际上被用作代理代码中的布尔切换，当 false 时禁用日志记录；使用 sdk.conf 之外的代码进行验证。

**型号建议更改 SRS**

将 FR-006 修改为：“工作线程应记录执行中的 stdout 和 stderr，由 log_stdout 配置标志（默认 true）控制。”将证据置信度设置为“中”，并注意切换语义是从配置默认待处理代码确认中推断出来的。

可选的人工修订修复：
> 在 FR-006 中改为：“系统默认 worker 配置应启用 stdout/stderr 日志记录（log_stdout=true）；当前证据仅支持默认启用，不单独规定运行时禁用语义。”
同时把该条的信心从 High 调为 Medium 更稳妥。

**人为决定**

- [x] 接受
- [ ] 拒绝
- [ ] 部分接受（`PARTIAL_ACCEPT`：混合声明；有些有效，有些无效）

可选的人工注释：
> 证据只明确显示默认配置 log_stdout: true 和注释“Log all stdout & stderr”，但我没有在源码中找到直接消费 log_stdout 的逻辑，因此不能强写成完整的“可配置启用/禁用行为”。

### R003：可追溯性

- 严重性：`major`
- 建议采取的措施：`partial_accept_as_issue`
- SRS位置：FR-001、FR-002（来源证据E001）
- 证据IDs：E001

**索赔或差距**

证据包中的 E001 被截断（“...旋转和监视...”）。 SRS 对从队列中提取作业、从 YAML 模板准备 K8s 作业以及 Pod 内环境安装和 Docker 监控做出了自信的声明（高置信度、演示）。截断的文本支持队列/模板声明，但在完全确认“监视 Docker 执行”细节之前被截断。

**模型意见**

可见的 E001 文本支持队列拉取和 YAML 模板声明。 “旋转并监视用户代码的 Docker 执行”(FR-002) 依赖于截断的尾部。对于监控部分，标记为“高”的置信度可能稍微被夸大了。

**推荐人工检查**

阅读完整的 README 部分，以确认代理“旋转并监视”Pod 内的 Docker 执行；确保 FR-002 措辞匹配。

**型号建议更改 SRS**

如果完整的 README 确认监控，请保持 FR-002 不变。如果未完全确认，请将 FR-002 可追溯性信心降级为“中”，并改写为“安装实验环境并在 Docker 中运行用户代码”，而不断言监控。

可选的人工修订修复：
> 在 FR-002 中把：“spin and monitor a Docker execution for the user code” 改为：“在 pod 内安装实验环境，并启动、监控实验进程。”
Docker socket / sibling Docker 管理保留在 FR-003 即可。

**人为决定**

- [ ] 接受
- [ ] 拒绝
- [x] 部分接受（`PARTIAL_ACCEPT`：混合声明；有些有效，有些无效）

可选的人工注释：
> 完整 README 证实 Kubernetes Glue 会从队列拉取 job、基于 YAML template 准备 K8s job，并在 pod 内安装环境、启动并监控实验进程；但 SRS 中“Docker execution for user code”比证据更具体。

### R004：不可验证

- 严重性：`minor`
- 建议采取的措施：`accept_as_issue`
- SRS 位置：FR-007 / FR-007 的第 8 节验收
- 证据IDs：E003

**索赔或差距**

FR-007 断言 get_all/get_all_ex 返回“表样式响应”，而 create 返回“实体引用”。 E003 显示代码分支（创建、获取、get_all/get_all_ex 返回 TableResponse），但接受标准“返回预期的映射实体或集合响应表单”定义松散，并且依赖于实时服务器，因此很难纯粹从存储库进行验证。

**模型意见**

操作集 (create/get/get_all/get_all_ex) 和 TableResponse 映射在 E003 中得到证实。接受措辞有些通用；验证可能需要会话模拟。收紧验收标准以使其可观察。

**推荐人工检查**

在 E003 中确认 'create' 返回一个带有 id 的实体，并且 get_all/get_all_ex 返回 TableResponse；细化接受以引用这些具体的返回类型。

**型号建议更改 SRS**

将 FR-007 接受细化为：“创建返回一个使用响应 id 初始化的实体； get 返回一个映射实体； get_all/get_all_ex 返回根据服务响应构造的 TableResponse。

可选的人工修订修复：
> 在 FR-007 中改为：“后端服务客户端应支持 create、get/get_by_id、get_all、get_all_ex 等动作；create 返回包含服务响应 id 的实体，get/get_by_id 返回映射实体，get_all/get_all_ex 返回 TableResponse 形式的表格化结果。”

**人为决定**

- [x] 接受
- [ ] 拒绝
- [ ] 部分接受（`PARTIAL_ACCEPT`：混合声明；有些有效，有些无效）

可选的人工注释：
> client.py 中确实能看到 create 返回带 id 的 entity，get/get_by_id 返回映射实体，get_all/get_all_ex 返回 TableResponse，SRS 的 FR-007 基本成立，但可以更精确。

### R005：架构_详细信息

- 严重性：`minor`
- 建议采取的措施：`accept_as_issue`
- SRS 位置：第二节 产品视角/运行环境
- 证据IDs：E001

**索赔或差距**

SRS 描述了两种集成风格（持久服务 Pod、Kubernetes Glue）和 Docker 套接字同级容器模型。事实架构图 (clearml_architecture.png) 不包含在证据包中，因此架构关系（代理-服务器-队列-pod）仅从 README 散文中断言。

**模型意见**

声明与 E001 散文一致，但没有提供图表证据来证实组件关系。请注意，E001 中的“很快被 podman 取代”详细信息被省略（次要范围/临时注释）。

**推荐人工检查**

根据 docs/clearml_architecture.png 交叉检查两种集成风格和组件交互；决定是否记录计划中的 podman 更换。

**型号建议更改 SRS**

在约束/假设下添加注释：“C-005：用于同级容器管理的 Docker 套接字映射计划由 podman 取代（根据 README）。 [E001]'。验证后可以选择引用架构图。

可选的人工修订修复：
> 在 第 2 节 Product perspective 增加高层背景：
“系统位于 ClearML Agent 与 ClearML Server 协作的运行环境中：用户侧代码和 GPU/worker 机器通过 agent 与 server 交互，server 提供实验管理、可视化、协作、数据跟踪以及 MLOps 监控/编排能力。” 另在 Design constraints 增加：“Kubernetes service-pod 模式当前依赖映射 Docker socket 以管理 sibling containers；README 说明该机制计划后续由 podman 替代。”

**人为决定**

- [x] 接受
- [ ] 拒绝
- [ ] 部分接受（`PARTIAL_ACCEPT`：混合声明；有些有效，有些无效）

可选的人工注释：
> 架构图是高层图，能支持“ClearML Agent/GPU machines 与 ClearML Server、Experiment Manager、MLOps Monitoring/Orchestration 交互”的背景，但不能直接证明 Kubernetes Glue 的细节。

### R006：范围

- 严重性：`minor`
- 建议采取的措施：`accept_as_issue`
- SRS 位置：第 1 部分 产品范围/总体 SRS 覆盖范围
- 证据 IDs：E001、E002、E003

**索赔或差距**

证据包报告了跨多种类型（测试、需求类、部署配置）的 40 个文档和约 142k 令牌，但 SRS 几乎完全由 6 个证据块构建（README、一个 sdk.conf、一个 client.py、两个服务模块）。重要的代理 CLI/运行时行为可能存在但未表示，可能低估了范围。

**模型意见**

SRS 保守地限定为检索到的块，这是有道理的，但它忽略了代理的核心 CLI 以及clearml-agent 存储库将包含的执行行为。范围声明应承认这是一个部分的、证据有限的规范。

**推荐人工检查**

查看其他检索到的文档（测试、部署配置、需求等）以确定 SRS 中是否缺少关键代理行为。

**型号建议更改 SRS**

添加到第 1 节产品范围：“本规范仅涵盖由所引用的证据块证实的行为；存储库中存在的代理 CLI 命令和更广泛的运行时编排超出了本文档的范围，有待进一步证据。

可选的人工修订修复：
> 

**人为决定**

- [ ] 接受
- [x] 拒绝
- [ ] 部分接受（`PARTIAL_ACCEPT`：混合声明；有些有效，有些无效）

可选的人工注释：
> CLI部分缺乏，但是不影响整体需求。

### R007：歧义

- 严重性：`minor`
- 建议采取的措施：`accept_as_issue`
- SRS 位置：数据需求 - 模型对象 (E006)
- 证据IDs：E006

**索赔或差距**

Model 对象将字段 id、name、user、company、created、task 列为“必填/值得注意的字段”，但 E006 是属性的文档字符串列表，没有明确标记为必填；班级是 NonStrictDataModel。 “必填”列标题可能会产生误导。

**模型意见**

字段被证明为属性，但不是必需的。列标题将“必需”和“值得注意”混为一谈。轻微的清晰度修复。

**推荐人工检查**

从 E006/full models.py 确认是否有任何模型字段是架构必需的；相应地调整标签。

**型号建议更改 SRS**

将模型对象行注释重新标记为“值得注意的（非必需）字段”或根据模式拆分必需与可选；澄清 NonStrictDataModel 字段不是严格必需的。

可选的人工修订修复：
> 在 Data Requirements 的 Model object 行 改为：
“Model object | notable nullable fields: id, name, user, company, created, task | 表示模型元数据字段；当前证据未声明这些字段为 required。” 如果表头有 “required fields”，建议改成 “notable fields”。

**人为决定**

- [x] 接受
- [ ] 拒绝
- [ ] 部分接受（`PARTIAL_ACCEPT`：混合声明；有些有效，有些无效）

可选的人工注释：
> Model 类确实包含 id/name/user/company/created/task 等字段，但 schema 没有把它们声明为 required，__init__ 参数也默认 None。当前 DR 表容易让人误读为必填字段。
