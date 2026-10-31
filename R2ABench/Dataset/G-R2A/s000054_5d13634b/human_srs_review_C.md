<!-- human_srs_review_A.md 由审阅者 A 生成。保留原始 human_srs_review.md。所有人类的判断都是英语的。 -->

# 人类 SRS 审查表

## 元数据

- 示例目录：`s000054_5d13634b`
- 生成SRS：`final_srs.md`
- 证据包：`evidence_pack.json`
- 评测型号：`claude-opus-4-8`
- 生成于：`2026-06-05T15:52:43.482253Z`
- 原始模型响应：`model_srs_review_raw.md`
- 解析状态：`parsed`

## 总体模型意见

- 推荐：`revise`
- 置信度：`0.74`
- 理由：SRS 结构良好，大多数需求都可追溯到六个证据块。然而，有几个要求夸大或插值超出了截断证据实际支持的范围（e.g.、“加载 TokenCard”资格、FR-003 特异性、从截断项目符号列表派生的用户类），并且未检查架构图（基本事实 SVG）。有必要进行重点修订以及对一些插值声明进行人工检查。

## 人类整体决策

- [ ] 接受
- [ ] 拒绝
- [x] 部分接受

原因：
> ACCEPT=3，PARTIAL_ACCEPT=2，REJECT=2，PARTIAL_ACCEPT=0。

## 积极的观察

- 强大、一致的可追溯性：每个 FR/NFR 都引用具体证据 IDs，并提供具有置信度的可追溯性矩阵。
- FR-007/FR-008（adminCount/controllerCount 返回 uint256）精确且正确地基于 E005/E006，包括方法签名。
- SRS 适当地声明没有证据表明最终用户 UI，从而避免伪造。
- 只读呼叫与付费交易/传输交互模式的清晰分离是从 Go 绑定 (E003/E004) 中准确得出的。

## 候选人问题

### R001：不支持的声明

- 严重性：`major`
- 建议采取的措施：`partial_accept_as_issue`
- SRS 位置：第 2 节用户类别；数据实体（所有者、Token Group Ltd 服务地址）
- 证据IDs：E002

**索赔或差距**

SRS 断言特定的用户类别 - “所有者”作为拥有用户智能合约的外部地址，以及“Token Group Ltd 运营的服务地址” - 派生自 E002，但 E002 是一个带有断句的截断项目符号列表（e.g.，“这将拥有用户的所有智能合约”， “- 是一组地址，由 Token Group Ltd 拥有和运营”）。

**模型意见**

E002 支持所有者/外部拥有地址概念的存在，并且 Token Group Ltd 运营一组服务地址，但项目符号是零碎的。推断出角色的精确定义和职责。所有者角色主张得到合理支持；具体的措辞“拥有用户的智能合约”直接在文本中。 Token Group Ltd 的“服务地址”标签是合理但部分插值的重建。

**推荐人工检查**

在提交时打开 README.md 并阅读完整的要求/角色部分以确认角色名称、定义以及是否定义了其他角色（e.g.、控制器、管理员）。

**型号建议更改 SRS**

在第 2 节用户类别中，软化为：“Token Group Ltd 运营的服务地址：由 Token Group Ltd 拥有和运营的一组地址，用于向最终用户提供服务（角色定义已部分证明；请参阅 README 要求部分）。来源：E002。阅读完整的 README 后确认或扩展。

可选的人工修订修复：
> Section 2 User classes，Section 6 Data entities。建议改成：Controller：由 Token Group Ltd 拥有和运营的一组地址，用于向最终用户提供服务，并参与控制/确认类操作。Source: E002 + README 完整 Requirements 部分。Owner 保留，但可写成：Owner：用户的 Owner Address / externally owned address，拥有该用户的智能合约。

**人为决定**

- [ ] 接受
- [ ] 拒绝
- [x] 部分接受（`PARTIAL_ACCEPT`：混合声明；有些有效，有些无效）

可选的人工注释：
> 完整 README 已确认 Owner Address 和 Controller 的定义，所以不是完全 unsupported。但 SRS 把 “Token Group Ltd operated service addresses” 写得太泛，原文更准确的是 Controller，即由 Token Group Ltd 拥有和运营的一组地址。

### R002：不支持的声明

- 严重性：`major`
- 建议采取的措施：`partial_accept_as_issue`
- SRS 位置：FR-003,产品功能汇总,C-003
- 证据IDs：E001

**索赔或差距**

FR-003 和相关声明将白名单“确定哪些令牌可用于加载 TokenCard”作为严格要求，但 E001 在句子中被截断（“...还确定哪些令牌可用于加载 TokenCard 以及哪些...”），从而使完整约束不完整。

**模型意见**

“加载 TokenCard”资格声明直接出现在 E001 中，但该句子被切断，因此白名单管辖的全套条件未知。该要求在精神上得到支持，但不应表述为完整。考虑到截断，将其映射到可验证的“资格决定”输出在某种程度上是推测性的。

**推荐人工检查**

阅读 README.md 中完整的 tokenWhitelist 描述，以捕获白名单管理的所有功能（安全性、加载资格和截断的“and which...”子句）。

**型号建议更改 SRS**

在 FR-003 系统行为中，附加注释：“白名单范围已部分证明；描述 TokenCard 负载资格的 README 句子在证据包中被截断，应根据完整源代码完成。保留要求但标记不完整性。

可选的人工修订修复：
> Product functions summary、FR-003、C-003、Data entities 中 Token whitelist。建议改成：系统应使用 token whitelist 记录 token 的汇率、是否可用于 TokenCard 加载、是否可由 TKN Holder Contract burn，并据此支持钱包安全和加载资格判断。

**人为决定**

- [x] 接受
- [ ] 拒绝
- [ ] 部分接受（`PARTIAL_ACCEPT`：混合声明；有些有效，有些无效）

可选的人工注释：
> 模型担心 E001 截断是对的。完整 README 补全后，白名单不仅决定哪些 token 可用于加载 TokenCard，还决定哪些 token 可被 TKN Holder Contract burn，并且 tokenWhitelist.sol 有 loadable、burnable 字段。

### R003：范围

- 严重性：`major`
- 建议采取的措施：`accept_as_issue`
- SRS位置：整个SRS；第一节 产品范围
- 证据 IDs：E001、E005、E006

**索赔或差距**

该存储库包含 40 个文档，包括 Solidity 合约（README 中引用的 wallet.sol、oracle.sol、controller.sol、tokenWhitelist.sol）和许多 Go 绑定/测试，但 SRS 几乎完全从 6 个证据块中提取功能细节（README + 控制器绑定 + oracle 模拟）。重要的合约行为（白名单添加/删除、控制器管理员管理、预言机更新流程）可能存在，但没有表现出来。

**模型意见**

SRS 诚实地说仅限于提供的证据，但它将自己呈现为存储库的需求声明，但只覆盖了一小部分。 adminCount/controllerCount 表示未捕获的管理员和控制器管理功能。这是对范围风险的轻描淡写，而不是错误的主张。

**推荐人工检查**

检查 controller.sol / controller.go 的状态更改方法（addAdmin、removeController 等）以及 tokenWhitelist.sol 的添加/删除令牌操作，以确定是否缺少实质性功能需求。

**型号建议更改 SRS**

在第 1 节产品范围中添加范围限制注释：“此 SRS 源自有限的证据子集（README 和选定的 Go 绑定）”。合同中存在的状态更改控制器/白名单/预言机操作未完全体现，需要在将此 SRS 视为完整之前进行源审查。

可选的人工修订修复：
> Section 1 Product scope。建议添加：范围限制：本 SRS 主要由 README 和部分 Go bindings 证据生成，尚未完整覆盖 Solidity 合约中的状态变更功能，包括 controller 管理、token whitelist 管理、oracle 汇率更新、钱包白名单与限额配置、Gas Tank top-up 和 TokenCard load 流程。将本 SRS 视为完整需求前，应补充源码级审查。

**人为决定**

- [x] 接受
- [ ] 拒绝
- [ ] 部分接受（`PARTIAL_ACCEPT`：混合声明；有些有效，有些无效）

可选的人工注释：
> 完整源码显示 SRS 覆盖面明显偏窄。遗漏了 controller 的管理员/控制器增删、tokenWhitelist 的 token 增删和汇率更新、oracle 的汇率更新流程、wallet 的地址白名单、每日限额、Gas Tank top-up、TokenCard load 等大量核心行为。

### R004：可追溯性

- 严重性：`minor`
- 建议采取的措施：`probably_ignore`
- SRS 位置：FR-006，通信接口，第 3 节控制器合同
- 证据 IDs：E003、E004

**索赔或差距**

FR-006 仅引用了控制器 Transact/Transfer 的 E003，但 Transfer/Transact 语义在 E003（控制器）和 E004（oracle 模拟）中的证明是相同的。通用绑定模式 (FR-009) 是 E004 的更好归宿； FR-006 关于控制器具体应注意 E003 是控制器特定源。

**模型意见**

较小的可追溯性清洁度。 E003 确实涵盖控制器交易和传输，因此 FR-006 的来源正确。没有矛盾；只需确保 E004（oracle 模拟）不用于证明其他地方特定于控制器的声明的合理性。

**推荐人工检查**

确认 E003 单独证实控制器交易/传输，并且没有控制器声明仅依赖于预言机模拟 (E004)。

**型号建议更改 SRS**

E003确认后无需更改；可以选择注释 FR-009 以澄清 E004 是 oracle-mock 绑定示例，而不是控制器源。

可选的人工修订修复：
> 

**人为决定**

- [ ] 接受
- [x] 拒绝
- [ ] 部分接受（`PARTIAL_ACCEPT`：混合声明；有些有效，有些无效）

可选的人工注释：
> FR-006 引用 E003 是正确的，E003 本身就能证明 controller 的 Transact / Transfer。E004 是 oracle mock 的绑定样例，用于证明通用绑定模式更合适，不构成必须修改的 SRS 缺陷。

### R005：架构_详细信息

- 严重性：`major`
- 建议采取的措施：`accept_as_issue`
- SRS 位置：第二部分产品视角；建筑学
- 证据 IDs：E001、E002

**索赔或差距**

真实的高级架构图 (docs/high_level_architecture.svg) 存在，但未使用。 SRS 架构叙述（钱包 -> ENS -> oracle/控制器/白名单）应对照图表进行交叉检查，这可能会显示其他组件或关系（e.g.、气罐、所有者、控制器-管理员关系、oraclize 连接器）。

**模型意见**

该图是权威的架构来源，可以揭示缺失的组件或纠正错误的描述。对于架构部分来说，不咨询它是一个显着的差距。

**推荐人工检查**

打开 docs/high_level_architecture.svg 并将其组件和边缘与第 2 部分和数据实体表进行比较；添加任何缺少的组件/关系。

**型号建议更改 SRS**

添加到参考文献和第 2 部分：引用 docs/high_level_architecture.svg 作为架构源，并在审核后协调组件列表/关系。

可选的人工修订修复：
> References、Section 2 Product perspective、Section 6 Data entities。建议添加：架构来源包括 docs/high_level_architecture.svg。系统以 Consumer Contract Wallet 为中心，Owner Address 控制钱包；钱包通过 ENS 解析 controller、token whitelist、licence 等支持合约；token whitelist 和 oracle 提供 token 支持状态与汇率；controller 地址参与 2FA/控制类操作；Gas Tank 表示 Owner Address 上、位于钱包合约外部的 gas ETH。

**人为决定**

- [x] 接受
- [ ] 拒绝
- [ ] 部分接受（`PARTIAL_ACCEPT`：混合声明；有些有效，有些无效）

可选的人工注释：
> 存在 docs/high_level_architecture.svg，且 README 架构段和合约关系说明支持对架构部分补充。当前 SRS 对钱包、ENS、oracle、controller、tokenWhitelist 的关系写得太少，也缺少 Gas Tank、Owner、Controller、Licence/TKN Holder/CryptoFloat 等与加载流程相关的关系。

### R006：不可验证

- 严重性：`minor`
- 建议采取的措施：`partial_accept_as_issue`
- SRS位置：FR-001、FR-002、FR-003验证行；第 8 条
- 证据IDs：E001

**索赔或差距**

FR-001/002/003 被分配验证方法“测试”并接受“证明钱包安全相关操作检索预言机汇率数据”，但底层证据（README 散文）没有指定这些钱包流的可观察接口或测试工具；所证明的绑定适用于控制器/预言机，而不是钱包的预言机获取流程。

**模型意见**

这些验收标准被设计为可测试的，但没有证据表明钱包的预言机检索可作为可测量的输出。将它们标记为“测试”可能会夸大仅给出 README 散文的可验证性。在检查 wallet.sol 之前，检查或源自源的测试目标会更加诚实。

**推荐人工检查**

检查 wallet.sol / 钱包绑定是否有可观察的预言机率检索或 ENS 分辨率接口，可以作为具体的接受目标；否则降级验证方法。

**型号建议更改 SRS**

对于 FR-001/FR-002/FR-003，将验证从“测试”更改为“检查”（或添加前提条件：“等待识别 wallet.sol 中的可观察钱包接口”），直到确认具体的测试目标。

可选的人工修订修复：
> FR-001 验收：通过钱包换算接口验证 token/稳定币/ETH 汇率数据被用于金额换算，并验证 rate 为 0 或 token 不可用时失败。FR-002 验收：通过 ENS 测试环境验证 controller、token whitelist、oracle/licence 等节点可注册并解析为目标合约地址。FR-003 验收：通过 TokenCard load 测试验证 token loadable 状态控制加载成功/失败，并产生相应加载事件或失败结果。

**人为决定**

- [ ] 接受
- [ ] 拒绝
- [x] 部分接受（`PARTIAL_ACCEPT`：混合声明；有些有效，有些无效）

可选的人工注释：
> 模型指出“仅凭 README 不能设为 Test”是合理的；但完整源码和测试已经提供可观察接口，例如 ConvertToEther、ConvertToStablecoin、LoadTokenCard、ENS 注册/解析 setup。因此不建议直接降级为 Inspection，而应补充测试依据和验收目标。

### R007：歧义

- 严重性：`minor`
- 建议采取的措施：`probably_ignore`
- SRS 位置：FR-005 / NFR-002（气罐）
- 证据IDs：E002

**索赔或差距**

E002 文本是零散的：“储气罐是用户的 ETH 的表示。” （句子被截断）。 FR-005 指出天然气 ETH“表示为智能合约钱包外部的储气罐”，这是受支持的，但精确的位置/表示（“在用户的……上”）尚未解决。

**模型意见**

核心主张（gas ETH 不受保护，在钱包之外）得到了很好的支持。由于截断，气罐 ETH 所在位置的确切表示是不明确的。风险低，但值得澄清。

**推荐人工检查**

阅读 README 中完整的 Gas Tank 语句，以确定气体 ETH 所在的位置（e.g.，在用户的外部拥有的地址上）。

**型号建议更改 SRS**

在 FR-005 中，可选地在验证后完成描述：“天然气支付 ETH 表示为位于钱包合约外部的储气罐（e.g.，在用户的外部拥有地址上 - 确认 README 中的确切措辞）。”

可选的人工修订修复：
> 

**人为决定**

- [ ] 接受
- [x] 拒绝
- [ ] 部分接受（`PARTIAL_ACCEPT`：混合声明；有些有效，有些无效）

可选的人工注释：
> 完整 README 明确说明 Gas Tank 是用户 Owner Address 上的 ETH，并且在智能合约钱包外部，不受钱包安全特性保护。SRS 当前核心说法正确，只是可以更精确。
