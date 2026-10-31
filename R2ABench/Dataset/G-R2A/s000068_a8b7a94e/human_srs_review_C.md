<!-- human_srs_review_A.md 由审阅者 A 生成。保留原始 human_srs_review.md。所有人类的判断都是英语的。 -->

# 人类 SRS 审查表

## 元数据

- 示例目录：`s000068_a8b7a94e`
- 生成SRS：`final_srs.md`
- 证据包：`evidence_pack.json`
- 评测型号：`claude-opus-4-8`
- 生成于：`2026-06-05T16:02:20.589396Z`
- 原始模型响应：`model_srs_review_raw.md`
- 解析状态：`parsed`

## 总体模型意见

- 推荐：`revise`
- 置信度：`0.78`
- 理由：SRS 结构良好，大部分可追溯至证据，但一些要求夸大了证据支持的内容（特别是 FR-005 命令计数器增量和 cmdUtil 数据包参数语义），将 README 文档与系统行为混为一谈，并将 CI 作业超时呈现为系统 NFRs。该存储库是一个大型飞行软件框架 (cFS)，但 SRS 范围是从少数工作流程/README 块中狭义得出的，这有低估范围的风险。这些需要人类的裁决，而不是按原样接受。

## 人类整体决策

- [ ] 接受
- [ ] 拒绝
- [x] 部分接受

原因：
> ACCEPT=5，PARTIAL_ACCEPT=2，REJECT=1，PARTIAL_ACCEPT=0。

## 积极的观察

- 每个要求都带有明确的证据ID和带有置信度评级的可追溯矩阵，使裁决高效。
- SRS 在某些地方（e.g.、FR-001 构建步骤、FR-006 变更日志类别）适当保守，并准确反映了 E001、E002 和 E005 的字面内容。
- 根据要求提供验证方法和验收基础，支持 CI 派生项目的可测试性。
- 简介诚实地指出，范围仅限于有证据的 README/工作流程材料，而不是夸大整个框架的覆盖范围。

## 候选人问题

### R001：不支持的声明

- 严重性：`major`
- 建议采取的措施：`partial_accept_as_issue`
- SRS 位置：FR-005、DR-002 第 8 部分（FR-005 验收）
- 证据IDs：E004

**索赔或差距**

FR-005 规定系统“应公开用户可观察到的命令计数器增量”作为严格的功能要求，并且 DR-002 将命令计数器视为有保证的输出数据。

**模型意见**

E004 仅表示“应该看到遥测数据，可以发送 noops 并查看命令计数器增量。”这是 README 散文，描述教程流程中的预期行为，而不是规范的系统规范。 “应该”一词是观察性的，而不是具有约束力的要求。将其提升为具有高优先级的“应”功能需求夸大了证据。

**推荐人工检查**

重新阅读 README 中的 E004 完整上下文。确定无操作/计数器行为是教程期望还是可指定的要求；如果仅具有描述性，则降低优先级/可验证性。

**型号建议更改 SRS**

将 FR-005 系统行为改写为：“README 记录启用遥测后，可以发送无操作命令，并且应该可以观察到命令计数器增量。”将验证更改为“演示（基于文档的期望）”并将优先级降低为“中”，或注释为派生/观察而不是“应”。

可选的人工修订修复：
> FR-005、DR-002、第 8 节 FR-005 验收。改为：README documents that after telemetry is enabled, no-op commands can be sent and command counter increments should be observable. 同时把 FR-005 优先级从 High 降为 Medium，验证方式用 Demonstration 或 Inspection/Demonstration，DR-002 改成“documented observable telemetry data”，不要写成保证输出。

**人为决定**

- [ ] 接受
- [ ] 拒绝
- [x] 部分接受（`PARTIAL_ACCEPT`：混合声明；有些有效，有些无效）

可选的人工注释：
> README 确实说启用 telemetry 后可以发送 noops 并看到 command counter 增加，但这是教程式观察，不应升格成强制、高优先级系统功能。

### R002：范围

- 严重性：`major`
- 建议采取的措施：`partial_accept_as_issue`
- SRS 位置：第 1.2、2.1 节，总体
- 证据 IDs：E002、E003、E006

**索赔或差距**

SRS 范围仅限于构建/测试工作流程、遥测交互和源自 6 个证据块的外部集成点。 nasa/cFS 是核心飞行系统框架（带有 cFE、OSAL、PSP 和应用程序的飞行软件产品）。

**模型意见**

该存储库是一个重要的飞行软件框架。将产品范围限制为 CI 工作流程和遥测教程低估了存储库范围。 SRS 明确否认这一点（“范围仅限于记录的构建/测试工作流程...”），这是诚实的，但读者可能会误认为这是完整的产品。真实图是可重用工作流程架构图，表明 CI 架构比捕获的更复杂。

**推荐人工检查**

确认证据包是否确实缺少 cFE/OSAL/PSP 架构内容，或者检索是否对 README 进行了欠采样。决定是否应更加突出范围限制注释。

**型号建议更改 SRS**

在第 1.2 节中添加粗体限制声明：“NOTE：此 SRS 仅捕获由检索到的 README 和 CI 工作流块证明的 cFS 行为子集。更广泛的 cFS 框架（cFE、OSAL、PSP、捆绑应用程序）超出了当前证据的范围，此处未指定。

可选的人工修订修复：
> 第 1.2 节 Product scope、第 2.1 节。增加：cFS is a Core Flight System bundle composed of submodules that make up the cFS framework, including cFE, OSAL, PSP, framework applications and tools.

**人为决定**

- [ ] 接受
- [ ] 拒绝
- [x] 部分接受（`PARTIAL_ACCEPT`：混合声明；有些有效，有些无效）

可选的人工注释：
> cFS 是更大的 Core Flight System bundle，README 明确说它包含 cFE、OSAL、PSP、framework apps/tools 等；当前 SRS 只覆盖 CI/README 证据子集，范围提示需要更醒目。但不能凭空补全未检索证据里的完整架构需求。

### R003：不可验证

- 严重性：`major`
- 建议采取的措施：`accept_as_issue`
- SRS 位置：NFR-003，第 8 部分 (NFR-003)
- 证据IDs：E006

**索赔或差距**

NFR-003“测试边界”要求功能测试工作流程“在 15 分钟 CI 超时内完成”。这是 CI 作业配置（超时分钟：15），而不是系统性能要求，超时是终止上限，而不是完成时间保证。

**模型意见**

E006 显示“超时分钟：15”，这是作业被终止之前允许的最大时间，而不是实际完成时的断言界限。声明测试“应在 15 分钟内完成”是不可验证的，因为超时并不能保证完成；作业可能会在 15 分钟内失败或被终止。这将 CI 安全限制与性能要求混为一谈。

**推荐人工检查**

验证 15 分钟是完成 SLA 还是仅仅是 CI 终止开关。重新构建 NFR-003 以反映配置约束而不是性能保证。

**型号建议更改 SRS**

将 NFR-003 改写为：“已弃用的功能测试 CI 作业应配置 15 分钟的超时上限（超时分钟数：15）；超过此数量的工作将被终止。验收依据：“工作流定义显示超时分钟数：15。”验证：检查（不是测试）。

可选的人工修订修复：
> NFR-003、第 8 节 NFR-003 验收、Traceability Matrix。改为：The functional-test CI job shall be configured with a 15-minute timeout ceiling; jobs exceeding this ceiling are terminated by CI. 验证方式改为 Inspection，验收依据改为：Workflow definition shows timeout-minutes: 15.

**人为决定**

- [x] 接受
- [ ] 拒绝
- [ ] 部分接受（`PARTIAL_ACCEPT`：混合声明；有些有效，有些无效）

可选的人工注释：
> timeout-minutes: 15 是 GitHub Actions 的终止上限，不是“测试必须在 15 分钟内完成”的性能保证。

### R004：歧义

- 严重性：`minor`
- 建议采取的措施：`accept_as_issue`
- SRS 位置：DR-003、FR-003，第 3.4 节
- 证据IDs：E006

**索赔或差距**

命令包参数被描述为字段“pktid、cmdcode、endian、uint32”。证据显示这些是一个特定命令的 cmdUtil CLI 标志 (--pktid=0x1806 --cmdcode=17 --endian=LE --uint32=3 --uint32=0x40000000)，而不是命令包结构的一般规范。

**模型意见**

SRS 将单个具体 cmdUtil 调用概括为数据格式要求。 'endian' 和 'uint32' 是 CLI 参数类型，而不是数据包字段本身，并且该示例发送两个 --uint32 值。将这些称为“面向数据包的参数”是一个合理的抽象，但有点不精确；证据仅支持 cmdUtil 接受这些标志，而不是完整的数据包字段模式。

**推荐人工检查**

从存储库工具中确认 cmdUtil 的实际参数集；决定 DR-003 的范围是否应为“cmdUtil 接受这些 CLI 标志”而不是数据包架构。

**型号建议更改 SRS**

将 DR-003 改写为：“cmdUtil 主机实用程序接受命令行标志，包括 --pktid、--cmdcode、--endian 和一个或多个 --uint32 参数，如单个功能测试调用所证明的那样。这并不构成完整的命令包模式。

可选的人工修订修复：
> 第 3.4 节 Data exchange formats、FR-003、DR-003。
DR-003 改为：The cmdUtil host utility accepts command-line flags including --pktid, --cmdcode, --endian, and typed payload arguments such as --uint32, as evidenced by CI functional-test invocations. This does not define a complete command packet schema.

**人为决定**

- [x] 接受
- [ ] 拒绝
- [ ] 部分接受（`PARTIAL_ACCEPT`：混合声明；有些有效，有些无效）

可选的人工注释：
> pktid/cmdcode/endian/uint32 是 cmdUtil 的命令行参数示例，不是完整命令包字段 schema；而且 workflow 中出现多个 --uint32、--half、--string、--uint8、--uint16 参数。

### R005：歧义

- 严重性：`minor`
- 建议采取的措施：`accept_as_issue`
- SRS 位置：第 3.1 节，FR-004
- 证据IDs：E004

**索赔或差距**

“遥测支持 UI”要求表示“系统文档应支持用户流程......”混合文档和系统行为。目前尚不清楚这是否是系统或 README 的要求。

**模型意见**

E004 是 README 演练（“选择启用 Tlm”、“输入 IP 地址...”）。 SRS 的措辞“系统文档应支持用户流程”很混乱——文档描述了流程；它不“支持”它。这是指定 UI 行为与指定文档存在之间的歧义。

**推荐人工检查**

决定是指定启用遥测的 UI 行为，还是指定 README 记录该过程，并一致地重新表述。

**型号建议更改 SRS**

将第 3.1 节要求改写为：“README 应记录遥测启用程序，其中操作员启用遥测并输入执行 cFS 的系统的 IP 地址（本地执行为 127.0.0.1）。”

可选的人工修订修复：
> 第 3.1 节、FR-004。建议改为系统行为：The system shall support telemetry enablement by allowing an operator to enter the IP address of the system executing cFS, including 127.0.0.1 for local execution.
第 8 节验收：After telemetry is enabled with the entered IP address, telemetry is visible as documented in the README walkthrough.

**人为决定**

- [x] 接受
- [ ] 拒绝
- [ ] 部分接受（`PARTIAL_ACCEPT`：混合声明；有些有效，有些无效）

可选的人工注释：
> E004 是 README 操作步骤，当前 “system documentation shall support a user flow” 混合了“文档要求”和“系统 UI 行为”。应写成 README 记录了遥测启用流程，或直接写系统支持遥测连接。

### R006：架构_详细信息

- 严重性：`minor`
- 建议采取的措施：`accept_as_issue`
- SRS 位置：第 2 节，NFR-001/NFR-004，参考文献
- 证据IDs：E005

**索赔或差距**

真实图像是“Reusable-Workflows-Architecture.svg”，表示可重用/可调用的工作流架构（workflow_call出现在E005中）。 SRS 不描述可重用工作流架构或构建、测试、格式检查和变更日志工作流之间的关系。

**模型意见**

E005 显示“workflow_call:”，指示这些工作流程是为重用/组合而设计的。真实图名称证实了经过深思熟虑的可重用工作流架构。 SRS 将每个工作流程视为一个独立的功能，并省略了编排/重用架构，这似乎是一个值得注意的设计功能。

**推荐人工检查**

检查可重用工作流-Architecture.svg 和完整工作流集，以确定是否应将可重用工作流架构描述添加到第 2 部分。

**型号建议更改 SRS**

添加到第 2.1 节：“CI 工作流程专为重用/组合 (workflow_call) 而设计，与存储库的可重用工作流程架构一致。 [等待针对 Reusable-Workflows-Architecture.svg 和完整工作流程集的验证。]'

可选的人工修订修复：
> 第 2.1 节 Product perspective，也可补到 NFR-004。增加：The repository CI includes a reusable-workflow architecture: cFS bundle workflows relate to reusable CodeQL, static-analysis, and format-check workflows, with reuse paths for cFS and submodules. Workflows using workflow_call are intended for reuse/composition across repositories.

**人为决定**

- [x] 接受
- [ ] 拒绝
- [ ] 部分接受（`PARTIAL_ACCEPT`：混合声明；有些有效，有些无效）

可选的人工注释：
> 实际存在 .github/workflows/Reusable-Workflows-Architecture.PNG 和 workflows README；图中体现 cFS Bundle、CodeQL、Static Analysis、Format Check、cFS Reuse、Submodules Reuse 的复用关系。当前 SRS 把 workflow 当成孤立能力，漏了 reusable workflow 架构。

### R007：可追溯性

- 严重性：`minor`
- 建议采取的措施：`probably_ignore`
- SRS 位置：第 1.4 节参考资料 / FR-006 / E001
- 证据IDs：E001

**索赔或差距**

FR-006 和 DR-004 使用特定的变更日志生成器 (heinrichreimer/github-changelog-generator-action)，其中 pullRequests: false 和author: false，并且仅在工作流程_dispatch 上运行。 SRS 捕获类别和手动触发，但忽略禁用 PRs/authors 以及所使用的特定操作。

**模型意见**

可追溯性差距较小。证据 E001 指定 pullRequests: false 和author: false，这会影响变更日志内容。 DR-004/FR-006 中未捕获此情况。影响不大，但值得注意的是完整性。

**推荐人工检查**

决定变更日志生成详细信息（排除 PRs、排除作者、具体操作）是否值得包含。

**型号建议更改 SRS**

增强 DR-004 详细信息：“变更日志内容不包括拉取请求和作者（pullRequests：false，作者：false），并且是通过手动（workflow_dispatch）触发器上的 github-changelog-generator 操作生成的。”

可选的人工修订修复：
> 

**人为决定**

- [ ] 接受
- [x] 拒绝
- [ ] 部分接受（`PARTIAL_ACCEPT`：混合声明；有些有效，有些无效）

可选的人工注释：
> changelog 的 pullRequests: false、author: false 和具体 action 确实存在，但 SRS 已捕获“手动触发、生成分类 changelog、上传 artifact”这些核心需求；缺少 PR/author 排除细节不明显损害正确性。

### R008：可追溯性

- 严重性：`minor`
- 建议采取的措施：`accept_as_issue`
- SRS 位置：第 1.4 节参考文献，NFR-001
- 证据 IDs：E001、E005、E006

**索赔或差距**

第 1.4 节引用了工作流程“build-cfs-deprecated.yml”，并提供证据 E002/E006，并且 NFR-001 引用了 E006 的“ubuntu-latest”，但 E006（功能测试）在“ubuntu-18.04”上运行。 ubuntu-latest (E001/E005) 和 ubuntu-18.04 (E002/E006) 的组合应该被精确归因。

**模型意见**

NFR-001 引用 E001、E005、E006 来表示“ubuntu-latest 和 ubuntu-18.04”。 E006 仅显示 ubuntu-18.04（不是 ubuntu-latest）； ubuntu-最新版本来自 E001/E005。分组引用大多是准确的，但混淆了哪个运行程序映射到哪个工作流程。另请注意，这些工作流程明确是“[DEPRECATED]”，NFRs 是在其基础上构建的 - 应标记已弃用状态，因为它会影响需求货币。

**推荐人工检查**

验证运行程序到工作流的映射并确认 NFRs 是基于标记为“[DEPRECATED]”的工作流；考虑标记已弃用的派生需求。

**型号建议更改 SRS**

向 NFR-001/NFR-002/NFR-003 添加注释：“这些要求源自标记为 [DEPRECATED] 的工作流程 (build-cfs-deprecated.yml)；他们的货币应该根据活动的构建/测试工作流程重新验证。正确的运行器归属：ubuntu-latest（E001、E005）； ubuntu-18.04（E002、E006）。

可选的人工修订修复：
> NFR-001、NFR-002、NFR-003、第 1.4 节 References、Traceability Matrix。增加注释：Some build/test requirements are derived from workflows labeled [Deprecated] or [DEPRECATED]; their currency should be revalidated against active workflows.
NFR-001 改为：Workflow runner usage shall be attributed per workflow/job: changelog and duplicate-check jobs use ubuntu-latest, while the evidenced build, run, functional-test, and format-checker jobs use ubuntu-18.04.

**人为决定**

- [x] 接受
- [ ] 拒绝
- [ ] 部分接受（`PARTIAL_ACCEPT`：混合声明；有些有效，有些无效）

可选的人工注释：
> runner 归属确实混淆了：changelog 和 duplicate-check 类 job 用 ubuntu-latest，build/test/functional-test 和 format-checker 主要是 ubuntu-18.04；且部分需求来自 [Deprecated] workflow，需要标明来源时效性。
