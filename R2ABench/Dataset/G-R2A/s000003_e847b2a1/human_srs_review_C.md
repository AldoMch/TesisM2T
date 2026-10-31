<!-- human_srs_review_A.md 由审阅者 A 生成。保留原始 human_srs_review.md。所有人类的判断都是英语的。 -->

# 人类 SRS 审查表

## 元数据

- 示例目录：`s000003_e847b2a1`
- 生成SRS：`final_srs.md`
- 证据包：`evidence_pack.json`
- 评测型号：`claude-opus-4-8`
- 生成于：`2026-06-05T15:28:27.708804Z`
- 原始模型响应：`model_srs_review_raw.md`
- 解析状态：`parsed`

## 总体模型意见

- 推荐：`revise`
- 置信度：`0.78`
- 理由：SRS 结构良好且有证据支持，但包含一些可通过真实图表验证的缺失架构细节、模糊的范围边界和不受支持的术语。关键问题包括缺少智能合约细节、不明确的预言机生命周期行为以及缺乏架构图中可见的预测解决工作流程。

## 人类整体决策

- [ ] 接受
- [ ] 拒绝
- [x] 部分接受

原因：
> 来源检查已完成：ACCEPT=9，PARTIAL_ACCEPT=2，REJECT=0，PARTIAL_ACCEPT=0。已将原“部分接受”项转换为来源检查后的接受/部分接受建议；仍需执行的工作是按各 R 项的“来源检查后的修订建议”更新目标 SRS。

## 积极的观察

- SRS严格遵守有证据支持的要求，避免猜测，保持高度的可追溯性信心（所有要求均引用具体证据IDs）。
- 追溯矩阵完整且结构良好，为每项需求提供明确的证据类型和验证方法。
- SRS 正确识别了系统的多组件性质（oracle 服务、前端 API、智能合约集成），并记录技术堆栈（Quarkus、React、Aeternity SDK）并提供证据支持。
- 功能需求是可测试的，包括与验证方法（检查、演示、测试）相关的明确验收标准。
- SRS 正确标记中等置信度项目（e.g.、NFR-005），其中证据是间接的，表明适当的保守性。
- CORS 中的 CORS 配置详细信息通过特定允许的方法和标头进行了精确记录，提供了具体的集成边界规范。

## 候选人问题

### R001：架构_详细信息

- 严重性：`major`
- 建议采取的措施：`accept_as_issue`
- SRS 位置：第 2 部分（产品视角）、第 4 部分 (FR-006)
- 证据IDs：E004

**索赔或差距**

SRS描述了合约交互，但没有指定智能合约语言、部署模型或合约是否在链上。证据 E004 显示通过 AENS 名称解析与合约实例进行交互，但没有证据阐明合约的实现技术或架构层。

**模型意见**

真实架构图可能显示预测卡合约是否是已部署的 Sophia 合约、它与预言机服务的关系以及前端-合约-预言机之间的数据流。如果图表或其他证据支持，SRS 应说明合同技术。

**推荐人工检查**

查看 https://github.com/kryptokrauts/ae-prediction-cards/blob/main/images/architecture.png 上的 architecture.png 图，以确定：(1) 预测卡合约是否是 Sophia 智能合约，(2) 预言机服务如何与合约交互，以及 (3) 架构层边界。

**来源检查结果**

已查看固定提交 `99dae5686d1542aae88bc67a22370ec6c6a567a0` 的 architecture.png、根 README、`contract/PredictionCards.aes` 和 `process-predicition-service`。架构图显示 `PredictionCards Smart Contract` 位于 Aeternity blockchain 内；根 README 明确智能合约由 Sophia 编写，并通过 AENS 名称 `predictioncards.chain` 指向部署合约。预言机交互不是前端直接完成：`process-predicition-service` 对 `CLOSED` 预测调用 `ask_for_winning_option`，`oracle-service` 轮询 oracle query 并响应，随后 `process-predicition-service` 调用 `process_oracle_response`。

**型号建议更改 SRS**

将 SRS 第 2、3、4 节修订为来源支持的架构描述：“系统包括部署在 Aeternity 区块链上的 Sophia `PredictionCards` 智能合约，合约地址通过 AENS 名称 `predictioncards.chain` 解析。前端通过 aepp-sdk-js 和连接的钱包调用该合约；`oracle-service` 注册并维护 Aeternity oracle；`process-predicition-service` 负责触发合约 oracle query 并在 oracle 响应后调用合约处理预测结果。”更新 C-002，明确 Sophia、Aeternity/FATE 合约运行环境、AENS 合约指针和 oracle 交互路径均为技术约束/外部接口证据。

可选的人工修订修复：
> 应在目标 SRS 中按以下位置修改：第 2 节“产品视角”应补充：“系统应由前端应用、部署在 Aeternity blockchain 上的 Sophia 智能合约、预言机服务和预测处理服务组成；链上合约应通过 AENS 名称进行定位，并承担预测相关链上状态管理职责。”第 3 节“软件/API 接口”应补充：“前端应用应通过已连接的钱包与链上合约交互；预测处理服务应负责发起预测结果判定所需的预言机查询，并在预言机响应可用后推动链上合约完成结果处理；预言机服务应负责维护 Aeternity 预言机并提交结果响应。”第 7 节“约束”中 C-002 描述应修改为：“系统的链上预测逻辑应受 Aeternity blockchain、Sophia 智能合约运行环境、AENS 合约定位机制以及预言机服务与预测处理服务职责分工的约束。”上述修改应保留来源追溯，不应写入具体函数名或源码级接口名。

**人为决定**

- [x] 接受
- [ ] 拒绝
- [ ] 部分接受（`PARTIAL_ACCEPT`：混合声明；有些有效，有些无效）

可选的人工注释：
> 来源检查已完成，接受该问题。architecture.png、根 README、合约源码和服务源码共同支持：SRS 当前对合约技术、AENS 解析和 oracle 服务边界描述不足，且可以安全地按来源证据修订。

### R002：缺少需求

- 严重性：`major`
- 建议采取的措施：`accept_as_issue`
- SRS 位置：第 4 节（功能要求）
- 证据IDs：E001

**索赔或差距**

SRS 记录预测创建 (FR-006)，但不描述预测分辨率、结算或结果确定。该存储库被命名为“预测卡”，证据显示预言机请求/响应处理（FR-001、FR-002），表明预言机可能会回答预测查询或解决结果。没有功能需求捕获此工作流程。

**模型意见**

预言机服务可能在解决预测中发挥作用（回答“发生了哪个结果”），但 SRS 没有记录此行为。真实图可以显示预测生命周期，包括解决/结算流程。

**推荐人工检查**

查看架构图和预言机服务 README (E001) 以确定预言机服务是否解析预测、如何确定预测结果以及是否存在结算或支付步骤。

**来源检查结果**

根 README、architecture.png、`process-predicition-service/README.md` 与服务源码确认预测解决流程存在且未被当前 SRS 充分捕获：`process-predicition-service` 定期查找 `CLOSED` 状态预测并调用 `ask_for_winning_option` 发起 OracleQueryTx；`oracle-service` 查询 CoinGecko 价格后响应 `higher` 或 `lower_or_equal`；若 oracle 及时响应，`process-predicition-service` 调用 `process_oracle_response`，智能合约确定 winning NFT，并允许 winning NFT renters 根据 HODL 时间和累计租金领取奖励。

**型号建议更改 SRS**

添加 FR-010：“预测结果解决：当预测进入 `CLOSED` 状态后，`process-predicition-service` 应定期检测该预测并调用 `PredictionCards.ask_for_winning_option` 发起 oracle query；`oracle-service` 应根据查询内容从 CoinGecko 取得资产价格并提交 `higher` 或 `lower_or_equal` 响应；oracle 响应后，`process-predicition-service` 应调用 `process_oracle_response`，由智能合约确定 winning NFT 并启用奖励领取。”添加 DR-007：“预测解决数据：oracle query 使用 `asset;target_price;end_timestamp` 字符串格式；oracle response 使用 `higher` 或 `lower_or_equal`。”引用根 README、`process-predicition-service/README.md`、`PredictionOracle.java`、`PredictionCards.aes` 和 E001。

可选的人工修订修复：
> 应在目标 SRS 中按以下位置修改：第 4 节“功能需求”应新增预测结果判定需求：“当预测达到关闭状态后，系统应启动预测结果判定流程；预测处理服务应发起结果判定所需的预言机查询，预言机服务应基于外部价格数据源提交结果响应，链上合约应根据响应确定获胜结果并开放奖励领取。”第 6 节“数据需求”应新增 DR-007：“预测结果判定数据应包括资产标识、目标价格、结束时间和结果取值。”该修订不应将预测结果判定流程归因于预言机服务单独完成。

**人为决定**

- [x] 接受
- [ ] 拒绝
- [ ] 部分接受（`PARTIAL_ACCEPT`：混合声明；有些有效，有些无效）

可选的人工注释：
> 来源检查已完成，接受该问题。根 README、架构图、process-predicition-service 和合约源码均确认预测结果解决、winning NFT 确定和奖励领取是核心工作流，应补入功能需求和数据需求。

### R003：缺少需求

- 严重性：`minor`
- 建议采取的措施：`accept_as_issue`
- SRS 位置：第 4 部分 (FR-003)
- 证据IDs：E001

**索赔或差距**

FR-003 声明“系统应定期检查预言机扩展是否必要”，但没有定义“扩展”的含义（TTL 扩展？查询生命周期扩展？）或需要扩展时采取什么操作。

**模型意见**

Aeternity 预言机有一个生存时间 (TTL) 参数。 oracle 服务可能会监视 TTL 并在到期前延长 oracle 注册以保持其活动状态。 SRS 应澄清此行为和相应的操作。

**推荐人工检查**

检查 oracle-service README 或源代码，确认“扩展”是否指扩展 oracle TTL，以及服务采取什么操作（e.g.，提交 OracleExtendTransaction）。

**来源检查结果**

`oracle-service/README.md`、`PredictionOracle.java` 与 `ChainInteraction.java` 确认“扩展”指 oracle 注册 TTL/区块高度余量维护。服务在启动和 `scheduler.oracle_expired_interval` 调度中调用 `extendOrRegisterOracle()`；如果 oracle 未注册则注册，如果剩余 TTL 小于等于 `oracle.min_blocks_extension_trigger`，则提交 `OracleExtendTransactionModel`，使用 `oracle.extension_ttl` 延长 oracle。

**型号建议更改 SRS**

将 FR-003 描述替换为：“`oracle-service` 应在启动时和按 `scheduler.oracle_expired_interval` 周期检查 Aeternity oracle 注册状态；若 oracle 未注册，应注册 oracle；若 oracle 剩余 TTL 小于或等于 `oracle.min_blocks_extension_trigger`，应提交 oracle extension transaction，并使用 `oracle.extension_ttl` 维持 oracle 可用性。”添加 NFR-006 或配置约束：“Oracle 可用性：oracle 服务应在注册到期前通过 TTL 扩展保持 oracle 持续可用。”引用 E001、`PredictionOracle.java` 和 `ChainInteraction.java`。

可选的人工修订修复：
> 应在目标 SRS 中按以下位置修改：第 4 节 FR-003 描述应修改为：“系统应在预言机服务启动和周期运行时检查预言机注册状态；当预言机未注册时，系统应注册预言机；当预言机剩余有效期低于配置阈值时，系统应延长预言机有效期。”第 5 节“非功能需求”可补充预言机可用性要求：“系统应在预言机注册到期前维护其持续可用性。”第 7 节“约束”应说明预言机注册、有效期阈值和有效期延长策略受运行时配置约束。

**人为决定**

- [x] 接受
- [ ] 拒绝
- [ ] 部分接受（`PARTIAL_ACCEPT`：混合声明；有些有效，有些无效）

可选的人工注释：
> 来源检查已完成，接受该问题。E001 的 README 线索由源码确认：oracle-service 会注册 oracle，并在 TTL 即将耗尽时提交 `OracleExtendTransactionModel`。

### R004：歧义

- 严重性：`minor`
- 建议采取的措施：`accept_as_issue`
- SRS 位置：第 4 部分（FR-001、FR-002）
- 证据IDs：E001

**索赔或差距**

FR-001和FR-002描述了检查和应答oracle请求，但没有指定oracle查询格式、查询源或响应格式。目前尚不清楚预言机提供哪些数据或谁/什么提交了预言机查询。

**模型意见**

预言机可能会接收来自智能合约的查询（e.g.，“事件 X 的结果是什么？”）并以结果数据进行响应。 SRS 应阐明查询-响应数据模型和交互流程。

**推荐人工检查**

查看预言机服务源代码和架构图以确定：（1）哪个实体提交预言机查询（合约？用户？），（2）查询和响应数据结构，以及（3）预言机咨询的外部数据源（API？区块链状态？）。

**来源检查结果**

来源检查确认：`process-predicition-service` 通过合约调用 `ask_for_winning_option` 触发 oracle query；合约 `PredictionCards.aes` 将 query 构造成 `asset;target_price;end_timestamp`；`oracle-service` 轮询该 oracle 的 queries，按分号解析为 ticker、目标价格和结束时间戳，调用 CoinGecko API 获取日期价格，比较目标价格与实际价格，并用字符串 `higher` 或 `lower_or_equal` 提交 oracle response。

**型号建议更改 SRS**

更新 FR-001 描述：“`oracle-service` 应按 `scheduler.oracle_query_interval` 轮询 Aeternity oracle queries，处理由 `PredictionCards` 合约经 `ask_for_winning_option` 创建的查询。”更新 FR-002 描述：“`oracle-service` 应解析每个查询的 `asset;target_price;end_timestamp` 字符串，从 CoinGecko 获取对应资产在预测结束日期的 USD 价格，比较目标价格与实际价格，并提交 `higher` 或 `lower_or_equal` oracle response transaction。”添加 DR-008：“Oracle 查询/响应格式：query 为 `asset;target_price;end_timestamp`；response 为 `higher` 或 `lower_or_equal` 字符串。”引用 `PredictionCards.aes`、`PredictionOracle.java`、`ChainInteraction.java` 和 E001。

可选的人工修订修复：
> 应在目标 SRS 中按以下位置修改：第 4 节 FR-001 描述应修改为：“系统应周期性检查由链上预测流程产生的待处理预言机查询。”第 4 节 FR-002 描述应修改为：“系统应根据预言机查询中的资产、目标价格和结束时间获取相应价格数据，比较目标价格与实际价格，并提交符合 SRS 定义的结果响应。”第 6 节“数据需求”应补充：“预言机查询数据应包括资产标识、目标价格和结束时间；预言机响应数据应使用明确的结果枚举表示价格比较结果。”修订后应删除 `[数据源，如果已知]`、`[查询结构]` 等占位符。

**人为决定**

- [x] 接受
- [ ] 拒绝
- [ ] 部分接受（`PARTIAL_ACCEPT`：混合声明；有些有效，有些无效）

可选的人工注释：
> 来源检查已完成，接受该问题。FR-001/FR-002 可用源码证据具体化：process-predicition-service 触发合约查询，oracle-service 解析 `asset;target_price;end_timestamp`，咨询 CoinGecko，并提交 `higher`/`lower_or_equal`。

### R005：不支持的声明

- 严重性：`minor`
- 建议采取的措施：`partial_accept_as_issue`
- SRS 位置：第 1 节（产品范围）、第 2 节（产品功能概述）
- 证据 IDs：无

**索赔或差距**

SRS 使用短语“预测卡智能合约接口”和“预测卡 API”，但没有证据表明“卡”是有意义的架构或领域概念。证据显示“预测”创建，但没有明确的“卡”实体或多预测卡容器。

**模型意见**

存储库名称包含“预测卡”，但证据 E003 和 E004 显示“PredictionCardsApi”和“PredictionEvent”，但未定义“卡”。 SRS 应避免使用不受支持的术语，除非证据或图表阐明了域模型。

**推荐人工检查**

查看架构图、智能合约源（如果在存储库中可用）和前端域模型，以确定“卡”是否是已定义的实体（e.g.，包含多个预测的卡或 UI 隐喻）或只是没有架构意义的品牌/命名选择。

**来源检查结果**

来源检查显示该问题部分成立。根 README 将产品命名为 `Prediction Cards`，说明它是 NFT art 与 prediction markets 的混合；每个预测结果是一个 unique NFT，当前每个预测有两个 outcome NFTs（`lower_or_equal` / `higher`）。源码也有 `PredictionCards` 合约、`PredictionCardsApi` 和前端 `PredictionCard` UI 组件。因此，“Prediction Cards”作为产品/代码命名和 UI/NFT 隐喻是有证据的。但没有发现独立的“Card”领域实体或“包含多个预测的卡”数据结构；核心领域实体应是 prediction、outcome NFT、rent、renter、oracle query/response。

**型号建议更改 SRS**

部分修订 SRS：保留 `Prediction Cards`、`PredictionCards` 智能合约、`PredictionCardsApi` 等来源中出现的产品名和代码名；不要把“卡”建模为独立领域实体或多预测容器。第 2 节和数据需求应将核心领域对象表述为“预测”和“两种结果 NFT（higher 与 lower_or_equal）”；若使用“卡”，应在术语表说明它是产品/UI/NFT 隐喻，不是单独的数据实体。FR-005 可保留 `PredictionCardsApi` 名称，FR-006 应描述 `create_prediction` 创建一个 prediction 并为两个 outcome NFTs 写入 IPFS 元数据。

可选的人工修订修复：
> 应在目标 SRS 中按以下位置修改：第 1 节“产品范围”可保留来源支持的产品名称，但不应将“卡”定义为独立领域实体或多预测容器。第 2 节“产品功能概述”应将核心领域对象表述为“预测”和“预测结果 NFT”。第 6 节“数据需求”应围绕预测、结果 NFT、租用/资金记录、预言机查询和预言机响应组织数据项。若 SRS 使用“卡”一词，应在术语说明中限定其为产品命名或界面隐喻，而不是单独的数据实体。

**人为决定**

- [ ] 接受
- [ ] 拒绝
- [x] 部分接受（`PARTIAL_ACCEPT`：混合声明；有些有效，有些无效）

可选的人工注释：
> 来源检查已完成，部分接受该问题。原审查对“卡”术语缺少领域定义的担忧有效；但建议中“将 PredictionCardsApi 改为预测 API”等替换过度，因为 `Prediction Cards` 和 `PredictionCardsApi` 是来源支持的产品/代码名。修订重点应是澄清“卡”不是单独的数据实体。

### R006：可追溯性

- 严重性：`minor`
- 建议采取的措施：`accept_as_issue`
- SRS 位置：第 4 部分 (FR-004)
- 证据IDs：E001

**索赔或差距**

FR-004 指出 oracle 服务需要一个“包含正确运行所需属性的 .env 文件”，但没有列出或引用特定的所需属性。 E001 声明“以下属性”，但证据片段被截断并且不显示属性列表。

**模型意见**

证据不完整。 SRS 应列出所需的属性（如果在完整的 E001 文档中可用）或声明属性列表记录在 oracle-service README 中并遵循该来源。

**推荐人工检查**

查看完整的 oracle-service README.md 以提取所需的 .env 属性列表。验证这些是否包括 Aeternity 节点 URLs、密钥对、oracle 配置等。

**来源检查结果**

完整 `oracle-service/README.md` 和 `OracleConfigration.java` 均确认所需运行时配置。README 列出：`oracle_private_key`、`beneficiary_private_key`、`base_url`、`compiler_url`、`network`、`target_vm`、`vm_version`、`abi_version`、`scheduler.oracle_query_interval`、`scheduler.oracle_expired_interval`、`local_node`、`oracle.min_blocks_extension_trigger`、`oracle.query_fee`、`oracle.initial_ttl`、`oracle.extension_ttl`。源码还包含默认的 `num_trials_default` 配置项。

**型号建议更改 SRS**

将 FR-004 或配置约束更新为：“`oracle-service` 应通过 `.env` 提供运行时配置，至少包括 `oracle_private_key`、`beneficiary_private_key`、`base_url`、`compiler_url`、`network`、`target_vm`、`vm_version`、`abi_version`、`scheduler.oracle_query_interval`、`scheduler.oracle_expired_interval`、`local_node`、`oracle.min_blocks_extension_trigger`、`oracle.query_fee`、`oracle.initial_ttl` 和 `oracle.extension_ttl`。这些配置用于 Aeternity 节点/编译器连接、oracle 密钥、调度周期、oracle 费用和 TTL 管理。”将该项归类为配置/技术约束或数据需求，而不是普通用户功能；引用 E001、`oracle-service/README.md` 和 `OracleConfigration.java`。

可选的人工修订修复：
> 应在目标 SRS 中按以下位置修改：第 4 节 FR-004 描述应修改为：“系统应在预言机服务启动前要求提供完整的运行时配置。”第 6 节“数据需求”或第 7 节“约束”应补充配置类别：“预言机服务配置应覆盖密钥、区块链节点连接、编译服务连接、网络环境、调度周期、预言机费用和预言机有效期管理参数。”修订后不应继续使用“包含正确运行所需属性”这类不可验证表述，也不应把该配置要求写成普通用户功能。

**人为决定**

- [x] 接受
- [ ] 拒绝
- [ ] 部分接受（`PARTIAL_ACCEPT`：混合声明；有些有效，有些无效）

可选的人工注释：
> 来源检查已完成，接受该问题。E001 截断导致原 SRS 缺少可追溯配置细节；完整 README 和配置源码可支持精确列出 `.env` 属性。

### R007：不可验证

- 严重性：`minor`
- 建议采取的措施：`accept_as_issue`
- SRS 位置：第 4 部分 (FR-005)
- 证据IDs：E003

**索赔或差距**

FR-005 验证标准是“演示：呈现提供程序使得 API 可通过子组件从上下文中获取”。这是未指定的——没有定义具体的测试步骤、输入或预期的可观察输出。

**模型意见**

验收标准应指定如何验证行为（e.g.，渲染测试子组件，调用 usePredictionCardsApi()，验证返回的对象具有预期的方法）。

**推荐人工检查**

定义一个具体的测试场景：(1) 使用模拟钱包渲染 PredictionCardsProvider，(2) 渲染调用 usePredictionCardsApi() 的子组件，(3) 验证返回的 API 实例是否已定义并且具有 createPrediction 方法。

**型号建议更改 SRS**

更新 FR-005 接受标准的第 8 节验证表：“使用测试钱包渲染 PredictionCardsProvider”。渲染调用 usePredictionCardsApi() 的子组件。验证返回的 API 对象是否已定义并公开 createPrediction 方法。

可选的人工修订修复：
> 应在目标 SRS 中按以下位置修改：第 8 节“验证”中 FR-005 的验证说明应修改为：“在测试钱包上下文中渲染前端 API 提供机制，并验证子组件能够获取可用的预测操作能力。”第 4 节 FR-005 的验收标准应补充可观察结果：“子组件能够从前端上下文获得预测操作入口，且该入口可用于执行预测创建相关操作。”修订后不应写入具体组件名、钩子名或方法名。

**人为决定**

- [x] 接受
- [ ] 拒绝
- [ ] 部分接受（`PARTIAL_ACCEPT`：混合声明；有些有效，有些无效）

可选的人工注释：
> 接受这个问题。该问题位于第 4 节 (FR-005)，引用的证据 (E003) 支持报告的不可验证问题。FR-005 验证标准是“演示：渲染提供程序使得 API 可通过子组件从上下文中获取”。这是未指定的——没有定义具体的测试步骤、输入或预期的可观察输出。有针对性的 SRS 修订是必要的，前提是更改保持在引用的证据范围内并且不引入新的假设。

### R008：范围

- 严重性：`minor`
- 建议采取的措施：`accept_as_issue`
- SRS 位置：第 2 部分（用户类别）
- 证据 IDs：E003、E004

**索赔或差距**

SRS 定义了三个用户类别，但不描述直接的最终用户行为（e.g.，通过前端 UI 创建预测、查看预测或索赔支出的参与者）。 “带钱包的前端用户”类仅被描述为“通过连接的钱包支持的 API 上下文操作前端”，它以实现为中心，而不是以用户目标为中心。

**模型意见**

该存储库似乎支持最终用户预测创建和交互，但 SRS 不记录面向用户的目标或场景（e.g.，“用户通过下注创建对事件 X 的预测”）。用户类表应该描述用户角色和目标，而不仅仅是技术接口。

**推荐人工检查**

查看前端 UI（如果在存储库中可用）和架构图以了解最终用户工作流程。确定用户是否可以：创建预测、查看预测、参与预测、领取奖励等。

**来源检查结果**

根 README 和前端源码确认最终用户工作流存在。用户通过 Superhero Wallet 连接前端，可以创建新的 prediction、查看 prediction 列表和详情、为 higher/lower outcome NFT deposit/rent、withdraw，并在 prediction 处理完成后对 winning NFT 执行 claim。前端 `NewEventForm` 收集 asset、target price、start/end timestamp 与 higher/lower IPFS image；`EventDashboard` 显示并刷新 prediction；`PredictionDetails` 支持 rent、deposit、withdraw、claim。

**型号建议更改 SRS**

将“带钱包的前端用户”替换为更目标导向的用户类别：“预测参与者：使用连接的 Aeternity/Superhero 钱包通过前端 UI 创建预测、查看预测、为 higher/lower outcome NFT 存入资金和租用 outcome NFT，并在预测处理完成后 withdraw 或 claim 奖励的用户。”在第 2 节或新的用户场景小节中添加：“用户选择资产、目标价格、开始/结束时间和 two outcome NFT images 来创建预测；用户查看 active/processed predictions；用户为某个 outcome NFT 设置 rent price 和 deposit；winning NFT 的 renter 在 `ORACLE_PROCESSED` 后可 claim 奖励。”引用根 README、E003、E004、`NewEventForm.tsx`、`EventDashboard.tsx` 和 `PredictionDetails.tsx`。

可选的人工修订修复：
> 应在目标 SRS 中按以下位置修改：第 2 节“用户类别”中“带钱包的前端用户”应修改为：“预测参与者：使用已连接的钱包通过前端应用创建预测、查看预测、为预测结果 NFT 提供或租用资金、撤回资金，并在预测结果确定后领取奖励的用户。”第 2 节可新增用户场景：“预测参与者应能够选择资产、目标价格、预测时间范围和结果 NFT 素材来创建预测；应能够查看进行中和已处理的预测；应能够在结果确定后执行资金撤回或奖励领取。”修订时不应使用“下注”等来源未支持的术语。

**人为决定**

- [x] 接受
- [ ] 拒绝
- [ ] 部分接受（`PARTIAL_ACCEPT`：混合声明；有些有效，有些无效）

可选的人工注释：
> 来源检查已完成，接受该问题。前端和 README 支持更清晰的最终用户类别和场景，当前 SRS 的“带钱包的前端用户”过于实现中心。

### R009：架构_详细信息

- 严重性：`critical`
- 建议采取的措施：`accept_as_issue`
- SRS 位置：第 2 部分（产品视角）、第 3 部分（软件/API 接口）
- 证据 IDs：无

**索赔或差距**

SRS 没有描述三个主要组件（前端、智能合约、预言机服务）之间的数据流或交互顺序。目前尚不清楚预言机服务是否监控合约、合约是否发出事件或预测生命周期状态转换如何发生。

**模型意见**

https://github.com/kryptokrauts/ae-prediction-cards/blob/main/images/architecture.png 上的架构图被明确引用，并且可能显示组件交互、数据流和预测生命周期。 SRS 应根据该图记录此架构。

**推荐人工检查**

查看 architecture.png 图以提取：(1) 组件交互流（前端 → 合约 → 预言机 → 合约？），(2) 事件触发器（合约事件？计划轮询？），(3) 用于预测创建、预言机查询和结果解析的数据流，以及 (4) 预言机咨询的任何外部数据源。

**来源检查结果**

architecture.png 和 README 确认系统不只是三个组件，而是至少包含 User/Frontend、Aeternity blockchain 上的 `PredictionCards` Smart Contract、`oracle-service`、`process-prediction-service` 和 IPFS。前端向合约执行 create prediction、deposit、rent NFT、withdraw/claim rewards，并用 dry-run 读合约数据；前端从 IPFS 加载 NFT GIFs。`process-prediction-service` 轮询 `CLOSED` predictions，调用 `ask_for_winning_option`，并在 oracle 已响应时调用 `process_oracle_response`。`oracle-service` 轮询 oracle queries，从 CoinGecko API 获取价格，确定 outcome，并向 oracle query 响应 `higher`/`lower_or_equal`。

**型号建议更改 SRS**

添加第 2.6 节“系统架构和数据流”：“系统包括 User/Frontend、Aeternity blockchain 上的 Sophia `PredictionCards` smart contract、`oracle-service`、`process-predicition-service` 和 IPFS。预测生命周期：（1）用户通过前端和钱包调用合约 `create_prediction` 创建 prediction，并为 two outcome NFTs 提供 IPFS metadata；（2）用户通过前端对 outcome NFT deposit、rent、withdraw 或 claim；（3）前端通过 dry-run 读取 prediction、NFT owner/renter、pot size、deposit 和 metadata；（4）`process-predicition-service` 按计划轮询 `CLOSED` predictions 并调用 `ask_for_winning_option` 生成 oracle query；（5）`oracle-service` 轮询 oracle queries，从 CoinGecko API 获取价格并响应 `higher` 或 `lower_or_equal`；（6）`process-predicition-service` 检测 oracle 已响应后调用 `process_oracle_response`，合约确定 winning NFT 和奖励领取逻辑。”更新第 3 节的软件/API 接口，分别列出前端-合约、process-service-合约、oracle-service-Aeternity oracle、oracle-service-CoinGecko、前端-IPFS 的接口。

可选的人工修订修复：
> 应在目标 SRS 中按以下位置修改：第 2 节应新增“系统架构和数据流”小节：“系统应包括用户前端、链上智能合约、预言机服务、预测处理服务和预测素材存储；用户前端负责预测创建、预测查看和资金/奖励操作；链上合约负责维护预测和结果状态；预测处理服务负责推动关闭预测进入结果判定流程；预言机服务负责提供结果判定所需的外部数据响应。”第 3 节“软件/API 接口”应补充前端与链上合约、后台服务与链上合约、预言机服务与外部价格数据源、前端与预测素材存储之间的数据交换职责。修订后应删除 `[根据图表进行描述]`、`[源]`、`[结算逻辑]` 等占位符。

**人为决定**

- [x] 接受
- [ ] 拒绝
- [ ] 部分接受（`PARTIAL_ACCEPT`：混合声明；有些有效，有些无效）

可选的人工注释：
> 来源检查已完成，接受该问题。架构图和 README 明确给出组件和数据流；SRS 应补充动态流程和软件/API 接口边界，尤其是 process-predicition-service 与 oracle-service 的分工。

### R010：缺少需求

- 严重性：`minor`
- 建议采取的措施：`accept_as_issue`
- SRS 位置：第 4 节（功能要求）
- 证据IDs：E004

**索赔或差距**

E004 显示前端 API 在提交合约之前转换事件开始时间戳（行：“this.convertDate(event.start_timestamp...)”），但 SRS 未指定转换逻辑、目标格式或转换原因（时区？ Aeternity 时间戳格式？）。

**模型意见**

时间戳转换是一种数据转换要求，具有潜在的正确性影响（错误的时区或格式可能会破坏预测计时）。 SRS 应记录转换规则。

**推荐人工检查**

查看 PredictionCards.api.ts 中的 ConvertDate 方法实现以确定转换逻辑（e.g、JavaScript 日期到 Unix 时间戳、UTC 规范化等）。

**来源检查结果**

`frontend/src/common/api/PredictionCards.api.ts` 中的 `convertDate(dateString)` 使用 `new Date(dateString)` 创建 JavaScript Date，并返回 `asDate.getTime()`。`NewEventForm.tsx` 使用 `datetime-local` 输入生成类似 `YYYY-MM-DDTHH:mm` 的字符串。因此，提交给合约的 start/end timestamp 是 JavaScript epoch milliseconds。源码没有显式 UTC 规范化；`datetime-local` 字符串会按浏览器/JavaScript Date 解析语义处理，本点应在 SRS 中说明或作为时区歧义风险记录。

**型号建议更改 SRS**

添加 DR-009（需要时重新编号）：“事件时间戳转换：前端在调用 `create_prediction` 之前，应将 `datetime-local`/JavaScript Date 可解析的 start/end timestamp 转换为 Unix epoch milliseconds（`Date.getTime()` 返回值），并将该毫秒值提交给合约。”更新 FR-006，引用该数据转换规则。不要声称源码已执行显式 UTC 规范化；如 SRS 需要消除时区风险，应新增约束：“系统应定义并验证 `datetime-local` 输入的时区解释，避免浏览器本地时区导致预测时间偏移。”

可选的人工修订修复：
> 应在目标 SRS 中按以下位置修改：第 6 节“数据需求”应新增事件时间数据要求：“系统提交给链上合约的预测开始时间和结束时间应使用统一的毫秒级时间戳格式。”第 4 节 FR-006 应引用该时间格式要求，说明预测创建提交前必须完成时间格式转换。第 7 节“约束”或“风险/开放问题”应补充：“SRS 应定义前端本地时间输入的时区解释规则，避免不同运行环境导致预测时间偏移。”修订时不应声称系统已经实现显式 UTC 规范化。

**人为决定**

- [x] 接受
- [ ] 拒绝
- [ ] 部分接受（`PARTIAL_ACCEPT`：混合声明；有些有效，有些无效）

可选的人工注释：
> 接受这个问题。该问题位于第 4 节（功能需求），引用的证据 (E004) 支持报告的 Missing_requirement 问题。E004 显示前端 API 在提交合同之前转换事件开始时间戳（行：“this.convertDate(event.start_timestamp...)”），但 SRS 未指定转换逻辑、目标格式或原因转换（时区？有针对性的 SRS 修订是有必要的，前提是更改保持在引用的证据范围内并且不引入新的假设。

### R011：缺少需求

- 严重性：`minor`
- 建议采取的措施：`partial_accept_as_issue`
- SRS 位置：第 5 节（非功能要求）
- 证据IDs：E002

**索赔或差距**

E002 在测试/部署工件 (nginx-cors.conf) 中显示 CORS 配置，表明系统包含 HTTP 服务器或反向代理。 SRS 没有指定部署架构、是否需要 nginx，或者由什么组件服务 HTTP 请求。

**模型意见**

CORS 配置意味着 Web 服务器边界，但 SRS 未记录 HTTP 服务层。架构图可以显示 nginx 是必需的组件还是只是一个测试装置。

**推荐人工检查**

查看架构图和部署文档（docker-compose、部署脚本等）以确定：(1) nginx 是生产组件还是仅在测试中使用，(2) service(s) nginx 代理什么，以及 (3) HTTP API 表面（REST 端点、静态文件服务、WebSocket、等）。

**来源检查结果**

来源检查显示该问题仅部分成立。`nginx-cors.conf` 和 nginx proxy 出现在 `contract-test/docker-compose.yml` 与 `contract-test/docker` 下，代理本地 Aeternity node、debug endpoint、Sophia compiler 和 index 服务；`nginx-default.conf` 中 `include cors.conf` 还是注释状态。根 README 与架构图没有把 nginx 描述为生产部署组件。因此不能基于 E002 添加生产 nginx/HTTP 边界需求；更合适的修订是把 E002 限定为 contract-test/local integration test 的 CORS/proxy fixture，或从生产 NFR/部署约束中移除。

**型号建议更改 SRS**

不要添加生产 nginx 或反向代理约束。将原建议改为：“E002 应作为测试/本地集成环境证据处理：`contract-test/docker-compose.yml` 使用 nginx proxy 暴露 Aeternity node、debug、compiler 和 index 服务；`nginx-cors.conf` 描述可用于测试代理的 CORS 头配置。若 SRS 当前把 E002 当成生产部署或系统 HTTP 边界证据，应改为第 8 节验证/测试环境说明，或删除相关生产 NFR/约束。”如需增加部署说明，应限于 contract-test local stack，而不是产品运行时架构。

可选的人工修订修复：
> 应在目标 SRS 中按以下位置修改：如果第 5 节“非功能需求”或第 7 节“约束”已将 E002 描述为生产环境 HTTP/CORS 或反向代理要求，应删除该生产运行时约束。第 8 节“验证”或“测试环境说明”可补充：“本地合约集成测试环境包含用于跨源访问验证的测试代理/CORS 配置。”修订后应明确 E002 仅支持测试环境说明，不支持新增生产部署组件或生产级 HTTP 边界要求。

**人为决定**

- [ ] 接受
- [ ] 拒绝
- [x] 部分接受（`PARTIAL_ACCEPT`：混合声明；有些有效，有些无效）

可选的人工注释：
> 来源检查已完成，部分接受该问题。E002 不支持生产 nginx/HTTP 边界需求；它只支持 contract-test/local integration proxy 与 CORS fixture。
