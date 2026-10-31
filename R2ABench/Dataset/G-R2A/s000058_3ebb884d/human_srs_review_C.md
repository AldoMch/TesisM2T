<!-- human_srs_review_A.md 由审阅者 A 生成。保留原始 human_srs_review.md。所有人类的判断都是英语的。 -->

# 人类 SRS 审查表

## 元数据

- 示例目录：`s000058_3ebb884d`
- 生成SRS：`final_srs.md`
- 证据包：`evidence_pack.json`
- 评测型号：`claude-opus-4-8`
- 生成于：`2026-06-05T15:55:57.552818Z`
- 原始模型响应：`model_srs_review_raw.md`
- 解析状态：`parsed`

## 总体模型意见

- 推荐：`revise`
- 置信度：`0.74`
- 理由：SRS 通常可以很好地追踪到六个证据块，并避免了大多数过度范围。然而，一些需求夸大了证据所显示的特殊性（e.g.、FR-002 删除语义、连接器“使用空数组放置然后删除”的细微差别），并且存储库中引用的架构图未得到反映。一些有关用户类别和操作环境的声明得到的支持很弱，应该进行检查。

## 人类整体决策

- [ ] 接受
- [ ] 拒绝
- [x] 部分接受

原因：
> ACCEPT=4，PARTIAL_ACCEPT=2，REJECT=1，PARTIAL_ACCEPT=0。

## 积极的观察

- 强大、一致的可追溯性：每个 FR/NFR/DR 都通过验证方法映射到特定证据 IDs (E001–E006)。
- FR-005 准确捕获了与 E005 匹配的 getSuccessfulDeploys 逻辑（结论！=成功计为失败，通过=总计 - 失败）。
- NFR-004 正确捕获来自 E005/E006 的 per_page: 100 分页和完整聚合行为。
- 手动SNS订阅解耦（FR-004/NFR-002/C-005）忠实地源自E003。
- SRS 适当保守，避免在大多数要求中超出证据范围进行制造。

## 候选人问题

### R001：不支持的声明

- 严重性：`major`
- 建议采取的措施：`accept_as_issue`
- SRS 位置：FR-002 / 第 4 区； DR-002
- 证据IDs：E004

**索赔或差距**

FR-002 指出系统应“为所提供的删除集发出连接器删除”。证据 E004 显示，deleteConnectors 始终使用空数组 (`[]`) 调用，而不是“提供的删除集”。

**模型意见**

该处理程序使用硬编码的空数组调用 `connect.deleteConnectors(process.env.cluster, process.env.service, [])`。将其描述为“提供的删除集”夸大了可配置性并歪曲了实际行为，即不删除任何内容（或对空集进行操作）。

**推荐人工检查**

检查 configureConnectors.js 和 deleteConnectors 签名/实现以确认空数组是否意味着“不删除”或某些其他语义。

**型号建议更改 SRS**

将 FR-002 系统行为修改为：“将连接器定义（放置）应用到目标集群和服务，使用空删除集调用连接器删除，然后重新启动已配置的连接器。”相应更新第 8 节中的验收依据。

可选的人工修订修复：
> 在 FR-002、DR-002、第 8 节验收中，把“按提供的删除集合删除 connector”改为：系统应对目标 cluster/service 应用 connector 定义，调用 connector 删除操作但传入空删除集合，因此当前配置流程不删除任何 connector，随后重启已配置 connector。

**人为决定**

- [x] 接受
- [ ] 拒绝
- [ ] 部分接受（`PARTIAL_ACCEPT`：混合声明；有些有效，有些无效）

可选的人工注释：
> configureConnectors.js 确实调用 deleteConnectors(..., [])；deleteConnectors 会遍历传入数组逐个删除，空数组就是不删除任何 connector。SRS 写“provided deletion set”不准确。

### R002：架构_详细信息

- 严重性：`major`
- 建议采取的措施：`accept_as_issue`
- SRS 位置：第二部分产品视角； FR-003
- 证据IDs：E003

**索赔或差距**

存储库包含架构图 (docs/assets/architecture.png)，E003 引用流程图（“此流程的模式如下所示”），但 SRS 不反映或协调架构图。

**模型意见**

地面实况图像 URL 和 E003 均表示 EventBridge→SNS 模式的记录架构/流程图。 SRS 至少应该注意这一点并验证其功能声明。

**推荐人工检查**

打开 docs/assets/architecture.png 和警报 README 图；确认 EventBridge→SNS 流程以及其他组件（ECS 服务、订阅目标）是否应出现在 SRS 中。

**型号建议更改 SRS**

在第 2 节产品视角中添加对架构图 (docs/assets/architecture.png) 的引用，并确认 FR-003 的 EventBridge→SNS 流程与该图匹配；审核后添加任何缺失的组件。

可选的人工修订修复：
> 在第 2 节 Product perspective 增加：本系统支持将 Appian 侧数据变更传递到 CMS BigMAC，并包含用于 connector 配置、topic 管理、服务事件告警和运行状态观测的 AWS 相关能力。架构图可作为后续架构建模参考，但本 SRS 仅记录需求级职责和外部系统交互，不直接规定具体部署拓扑。在 FR-003 中改为：当项目服务产生符合告警规则的运行事件时，系统应通过 AWS 事件路由能力将该事件发送到通知主题，并支持由该通知主题分发给人工维护的订阅目标。

**人为决定**

- [x] 接受
- [ ] 拒绝
- [ ] 部分接受（`PARTIAL_ACCEPT`：混合声明；有些有效，有些无效）

可选的人工注释：
> 架构图 docs/assets/architecture.png 明确包含 Appian Oracle DB、VPC peering、AWS Fargate Kafka Connect Cluster、topics Lambda、CMS BigMAC、EventBridge、SNS Topic 和订阅目标。当前 SRS 只写 EventBridge→SNS，架构视角偏窄。

### R003：不支持的声明

- 严重性：`minor`
- 建议采取的措施：`partial_accept_as_issue`
- SRS 位置：第 2 节用户类别； FR-004
- 证据IDs：E003

**索赔或差距**

SRS 定义了“通知管理员”用户类，用于“手动添加或删除 SNS 订阅”。 E003 表示订阅服务是“手动管理”的，但没有定义不同的用户角色。

**模型意见**

支持手动管理语句，但发明一个命名用户类（“通知管理员”）是一个推论。作为正式角色，这是合理的，但没有证据支持。

**推荐人工检查**

确认是否有任何文档定义了订阅管理的角色/角色；否则软化为“执行手动订阅管理的操作员/维护人员”。

**型号建议更改 SRS**

在第 2 节用户类中，将“通知管理员”合并到操作员/维护者中，或将其注释为推断的角色。将 FR-004 触发器措辞调整为“具有订阅管理访问权限的用户”。

可选的人工修订修复：
> 在第 2 节 User classes 删除独立的：Notification administrators改为在 Operators/DevOps users 中写：Operators/DevOps users: provide AWS credentials, run AWS-account-scoped operations, observe alerts, and manually manage SNS topic subscriptions when they have subscription management access.FR-004 触发条件改为：A user/operator with SNS subscription management access adds or removes subscribers.

**人为决定**

- [ ] 接受
- [ ] 拒绝
- [x] 部分接受（`PARTIAL_ACCEPT`：混合声明；有些有效，有些无效）

可选的人工注释：
> 手工管理 SNS subscription 是明确支持的；但“Notification administrators”这个正式用户类没有文档定义。更稳妥是并入 operators/maintainers。

### R004：歧义

- 严重性：`minor`
- 建议采取的措施：`accept_as_issue`
- SRS 位置：FR-001 / DR-001
- 证据IDs：E001

**索赔或差距**

FR-001 描述了用于列出阶段的“运行脚本”，但 E001 仅声明“使用运行脚本：”，而没有命名或描述脚本或其输出格式。

**模型意见**

证据中确实没有明确说明过程细节（文档片段被截断并且没有给出脚本名称或输出模式）。 SRS 忠实地反映了这一差距，但应将其标记为无法验证且无法验证。

**推荐人工检查**

找到 list-running-stages.md 中引用的实际运行脚本以捕获脚本名称和输出格式，以获得更强的验收标准。

**型号建议更改 SRS**

在FR-001和DR-001中，注意证据中没有指定具体的脚本和输出格式；找到脚本后，将其名称和输出模式添加到验收基础中。

可选的人工修订修复：
> 在 FR-001、DR-001、第 8 节验收中，把泛泛的“stage-listing script”改为：用户完成 onboarding 并设置 AWS CLI credentials 后，运行 nvm use 和 run listRunningStages。系统应查询当前 AWS account/region 中的 running stages，并以 runningStages=<comma-separated stages> 形式输出结果。

**人为决定**

- [x] 接受
- [ ] 拒绝
- [ ] 部分接受（`PARTIAL_ACCEPT`：混合声明；有些有效，有些无效）

可选的人工注释：
> 完整文档不是缺失脚本名。list-running-stages.md 写明先 nvm use，再运行 run listRunningStages；src/run.ts 中该命令还会输出 runningStages=<逗号分隔列表>。

### R005：可追溯性

- 严重性：`minor`
- 建议采取的措施：`probably_ignore`
- SRS 位置：运行环境（第 2 部分）； NFR-003 / C-004
- 证据 IDs：E001、E002

**索赔或差距**

操作环境引用 E002 来表示“入职期间基于终端的本地执行”。 E002 涵盖工作区设置（setup.sh，终端），但 GitHub 操作 CI/CD 声明（NFR-003、C-004）可追溯到 E001，其代码片段仅部分显示它（'This项目使用 GitHub Actions 作为其 CI/CD 工具...'）。

**模型意见**

GitHub 操作 CI/CD 声明受 E001 支持，但代码片段被截断；痕迹是可以接受的，但处于临界点。支持 E002 终端声明。值得快速检查一下 NFR-003 置信度（“中”）是否合适并且源代码行是否真实。

**推荐人工检查**

验证完整的 E001 文本，确认 GitHub 操作为 CI/CD 工具；确认该行是否位于 list-running-stages 文档或其他文件中。

**型号建议更改 SRS**

如果 E001 确认 GitHub 行动声明，则不会发生任何变化；否则，将 NFR-003/C-004 重新来源到工作流程 YAML 或 CI 文档。

可选的人工修订修复：
> 

**人为决定**

- [ ] 接受
- [x] 拒绝
- [ ] 部分接受（`PARTIAL_ACCEPT`：混合声明；有些有效，有些无效）

可选的人工注释：
> 完整 E001 文档明确写着“this project uses GitHub Actions as its CI/CD tool”，仓库也有 .github/workflows 下的多个 workflow；E002 也支持 terminal/setup.sh onboarding。模型担心只是截断证据造成的边界问题，不构成必须修改的 SRS 缺陷。

### R006：不可验证

- 严重性：`minor`
- 建议采取的措施：`accept_as_issue`
- SRS 位置：FR-006 / 第 8 区
- 证据IDs：E006

**索赔或差距**

FR-006 使用 `differenceInHours` 和 `... || 0` 后备计算平均值。接受基础（“预期的averageTimeToMerge，或当没有符合条件时为0”）是可验证的，但未说明differenceInHours（整数小时）的舍入/截断行为。

**模型意见**

E006 使用 date-fns DifferenceInHours 截断为整个小时； SRS 描述了“小时差异”，但没有注意到整数截断，这可能会影响测试预期。

**推荐人工检查**

确认 DifferenceInHours 截断行为以及是否根据整数小时值计算平均值。

**型号建议更改 SRS**

添加到 FR-006 / DR-005：“合并持续时间按整小时差异计算（date-fns DifferenceInHours，截断），当不存在符合条件的 PRs 时，平均值默认为 0。”

可选的人工修订修复：
> 接受模型意见。

**人为决定**

- [x] 接受
- [ ] 拒绝
- [ ] 部分接受（`PARTIAL_ACCEPT`：混合声明；有些有效，有些无效）

可选的人工注释：
> getPrsToBranch.ts 使用 date-fns@2.29.3 的 differenceInHours；该函数默认 roundingMethod='trunc'，也就是整小时截断。SRS 只写“hour differences”，容易让验收预期不清楚。

### R007：范围

- 严重性：`minor`
- 建议采取的措施：`partial_accept_as_issue`
- SRS 位置：第 1 节 产品范围 / 第 2 节
- 证据 IDs：无

**索赔或差距**

证据包包括多种类型（配置、部署配置、测试、教程）的 40 个文档，但 SRS 仅由 6 个证据块构建。范围可能低估了更广泛的存储库功能（e.g.、完整部署/无服务器配置、测试）。

**模型意见**

SRS 在坚持检索到的证据方面相当保守，但“macpro-appian-connector”名称和广泛的文档集表明连接器部署/无服务器基础设施可能是比所表示的更大的功能。这是范围覆盖警告，而不是缺陷。

**推荐人工检查**

查看其他存储库文档/无服务器配置，以确定范围中是否缺少主要功能（部署管道、Appian 集成细节）。

**型号建议更改 SRS**

在第 1 节中添加范围注释，即 SRS 涵盖检索到的证据子集支持的行为，并且可能不会枚举所有存储库部署/基础设施功能。

可选的人工修订修复：
> 在第 1 节 Product scope 开头增加：
本仓库用于支持 Appian 数据变更向 CMS BigMAC 的传输与运维管理。系统应支持 connector 配置与运行维护、数据 topic 管理、服务运行事件告警、运行阶段查询、部署与 PR 指标统计，以及基于 GitHub Actions 的部署/运维工作流。

**人为决定**

- [ ] 接受
- [ ] 拒绝
- [x] 部分接受（`PARTIAL_ACCEPT`：混合声明；有些有效，有些无效）

可选的人工注释：
> SRS 确实只覆盖证据包 6 个 chunk 中的行为，但仓库完整文档显示它的核心定位更大：Kafka Connector 将 Appian 数据流向 BigMAC，并包含 Serverless services、GitHub Actions CI/CD、安全扫描、部署工作流、GitHub Pages 文档等。没必要把 40 个文档都展开，但应加范围说明和核心身份。
