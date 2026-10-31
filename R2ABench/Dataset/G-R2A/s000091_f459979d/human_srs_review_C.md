<!-- human_srs_review_A.md 由审阅者 A 生成。保留原始 human_srs_review.md。所有人类的判断都是英语的。 -->

# 人类 SRS 审查表

## 元数据

- 示例目录：`s000091_f459979d`
- 生成SRS：`final_srs.md`
- 证据包：`evidence_pack.json`
- 评测型号：`claude-opus-4-8`
- 生成于：`2026-06-05T16:06:34.695322Z`
- 原始模型响应：`model_srs_review_raw.md`
- 解析状态：`parsed`

## 总体模型意见

- 推荐：`revise`
- 置信度：`0.72`
- 理由：SRS 具有良好的证据块基础，并将需求忠实地映射到代码。然而，一些要求夸大了截断证据中不可见的特异性（检索端点的 HTTP 状态代码、POST /add 201 路径），并且更广泛的系统上下文（根据架构图的区块链 LwM2M 引导架构）被低估。一些可追溯性和可验证性问题需要人工裁决。

## 人类整体决策

- [ ] 接受
- [ ] 拒绝
- [x] 部分接受

原因：
> ACCEPT=2，PARTIAL_ACCEPT=4，REJECT=0，PARTIAL_ACCEPT=0。

## 积极的观察

- FR-001/FR-002 中的 JWT 验证结果映射（0->200、1->401、2->403，否则 400）准确且精确地追溯到 E002。
- NFR-003 和 DR-004 直接从 E005/E006 正确捕获 LwM2M 反序列化器的不变量（无效节点元素上的 JsonParseException，以及当实例不存在 id 时“缺少 id”）。
- Web3j HttpService 连接（NFR-002、C-002）忠实地基于 E001。
- 可追溯性矩阵一致地分配合理反映证据强度的置信水平（对于区块链/测试派生项目为中，对于直接显示的代码行为为高）。

## 候选人问题

### R001：不支持的声明

- 严重性：`minor`
- 建议采取的措施：`partial_accept_as_issue`
- SRS 位置：FR-001 / 第 3 节软件/API 接口（用户 HTTP API 行）
- 证据IDs：E002

**索赔或差距**

FR-001 描述了具有特定 HTTP 路由的经过身份验证的用户检索操作，但 E002 仅显示处理程序的尾部部分（`Service.getAll()` 返回 `HttpStatus.OK`），而没有用于检索的方法映射、路由路径或 `@GetMapping` 注释。

**模型意见**

两个处理程序都很好地支持验证结果到状态映射（0->OK、1->401、2->403，否则 400）。但是，E002 中未显示检索操作的route/HTTP 方法（仅添加端点的`/add` 映射可见）。 SRS 没有断言特定的检索路线，因此风险较低，但应确认它是独特的“检索端点”。

**推荐人工检查**

打开 UserController.java 并确认检索处理程序的 HTTP 方法和路径（e.g.、@GetMapping）。验证它是 `getAll()` 驱动并返回用户列表。

**型号建议更改 SRS**

FR-001 触发器/输入：将“带有 `Authorization` 标头的 HTTP 请求发送到用户检索端点”替换为“带有 `Authorization` 标头的 HTTP GET 请求发送到用户检索端点”（具体路由需要根据 UserController 进行确认）映射）'。

可选的人工修订修复：
> 在 FR-001 的触发器/输入处，将：带有 Authorization 头的 HTTP 请求发送到用户检索端点 改为：带有 Authorization 头的 HTTP GET 请求发送到用户检索端点；系统根据令牌验证结果返回用户列表或对应错误状态。第 3 节用户 HTTP API 行也可补一句：用户 API 应支持用户检索和用户创建操作，两者均基于 Authorization 头进行访问控制。

**人为决定**

- [ ] 接受
- [ ] 拒绝
- [x] 部分接受（`PARTIAL_ACCEPT`：混合声明；有些有效，有些无效）

可选的人工注释：
> 部分接受。原因是模型说 E002 没显示用户检索端点的 HTTP 方法，但源码中已确认用户检索是 GET，因此问题不在于“无法支持”，而在于 SRS 可以把触发条件写得更明确。

### R002：不可验证

- 严重性：`minor`
- 建议采取的措施：`partial_accept_as_issue`
- SRS 位置：FR-003 / 第 8 节验证（FR-003 行）
- 证据IDs：E001

**索赔或差距**

FR-003 接受标准“检索请求导致合约 getAllClients().send() 使用”测试内部实现调用而不是可观察的行为，并且 E001 显示 catch 块吞噬异常 (e.printStackTrace) 返回可能为空的列表。

**模型意见**

断言调用特定的内部合约方法是白盒且脆弱的作为验收标准。更重要的是，E001 揭示了在异常时返回空/部分集合的错误处理，这在 SRS 中未指定。错误行为的缺失要求可能是合理的。

**推荐人工检查**

检查 ClientStoreService.getAll()：确认合约失败时它返回一个空集合而不是传播错误，并决定是否应要求此错误处理行为。

**型号建议更改 SRS**

添加 FR-003a：“如果区块链合约调用失败，系统应返回一个空的安全信息集合（当前行为记录异常并且不会传播它）。 [E001]' 并将 FR-003 改写为可观察输出（返回的集合内容）而不是内部方法使用。

可选的人工修订修复：
> 在 FR-003 的行为或验收标准中，将内部调用式描述改为结果式描述：系统应从区块链合约检索客户端安全信息，并将结果转换为安全信息集合返回；当合约调用失败时，系统按当前实现记录异常并返回空集合，不向调用方传播异常。第 8 节 FR-003 验收标准改为：成功时返回转换后的安全信息集合；合约访问失败时返回空集合，并保持调用方流程不中断。

**人为决定**

- [ ] 接受
- [ ] 拒绝
- [x] 部分接受（`PARTIAL_ACCEPT`：混合声明；有些有效，有些无效）

可选的人工注释：
> 原因是 FR-003 当前验收标准偏白盒，强调内部合约调用，而不是外部可观察行为；源码还显示合约调用异常时会记录异常并返回空集合。

### R003：缺少需求

- 严重性：`minor`
- 建议采取的措施：`accept_as_issue`
- SRS 位置：第 3 节 / FR-004 / FR-005 — 转换器 byte32 转换
- 证据IDs：E004

**索赔或差距**

E004 显示字符串字段通过 `Converter.asciiToByte32(...)` 转换并通过 `Converter.byteToAscii(...)` 进行响应。 SRS 在 FR-004 中一般提到“字节数组表示”，但省略了用于 addClient 和 getClient 的显式 ASCII<->byte32 转换约束。

**模型意见**

asciiToByte32/byteToAscii 转换是 E004 中可见的具体且可测试的数据格式约束，并且与智能合约的互操作性相关。它被部分捕获用于 FR-004，但不用于 FR-005 检索解码。

**推荐人工检查**

确认 addClient 和 getClient 路径中的 Converter.asciiToByte32 / byteToAscii 使用情况以及 32 字节固定编码是否是硬合约约束。

**型号建议更改 SRS**

增强 DR-002 和 FR-005：添加“与合约交换的字符串字段应在提交时编码为固定 32 字节 (byte32) ASCII 值，并在检索时从 byte32 解码为 ASCII。 [E004]'。

可选的人工修订修复：
> 在 DR-002 增加：与智能合约交换的 endpoint、bootstrap/server URL、identity、key 等字符串字段，在提交时应编码为固定 32 字节 ASCII 值；在检索时应从固定 32 字节值解码回 ASCII 字符串。在 FR-004 补充：提交客户端引导数据前，系统应将相关字符串字段转换为固定 32 字节 ASCII 表示。在 FR-005 补充：检索客户端引导配置时，系统应使用固定 32 字节形式提交 endpoint，并将返回字段解码为 ASCII 后构造引导配置。

**人为决定**

- [x] 接受
- [ ] 拒绝
- [ ] 部分接受（`PARTIAL_ACCEPT`：混合声明；有些有效，有些无效）

可选的人工注释：
> 接受。原因是证据显示区块链交互中的字符串字段存在明确的 ASCII <-> byte32 固定长度转换约束，当前 SRS 只泛泛写了字节数组表示，不够精确。

### R004：范围

- 严重性：`major`
- 建议采取的措施：`partial_accept_as_issue`
- SRS 位置：第 1 节产品范围/第 2 节总体描述
- 证据 IDs：E001、E003

**索赔或差距**

SRS 范围将项目简化为“用户管理端点、区块链客户端/引导存储和 LwM2M JSON 解析”，但存储库（名称、architecture.png、README、部署/配置文档、多个模块：mainApp、leshan Server、评估/测试）描述了更广泛的内容LwM2M-具有部署架构的区块链引导系统。

**模型意见**

证据包涵盖部署和 user_scenario 类别（category_hits 显示部署：58、user_scenario：78），文档类型包括 readme/config/cli，表明系统级架构未反映在 SRS 范围中。 SRS 仅关注五个检索到的代码块，从而低估了范围。应添加架构级范围声明或明确指出限制。

**推荐人工检查**

查看 README 和 architecture.png 以及配置/部署文档，以确定总体系统用途（通过区块链 BootstrapStore 合约保护的 LwM2M 设备引导程序）以及 SRS 是否应声明此端到端范围。

**型号建议更改 SRS**

第 1 节产品范围：添加“整个系统提供由以太坊智能合约 (BootstrapStore) 支持的 LwM2M 设备引导/安全配置，将基于 Leshan 的 LwM2M 服务器与 Spring 后端和 Web3j 区块链访问集成。此 SRS 重点关注已证实的后端组件；完整的部署架构（参见 architecture.png）应该进行交叉检查。 （待 README/图表确认）。

可选的人工修订修复：
> 在第 1 节 Product scope 或第 2 节 Product perspective 增加高层范围说明：本系统面向 LwM2M 设备管理场景，将 LwM2M 服务、设备引导/安全信息管理、管理端访问控制与区块链可信存储结合起来，用于提升客户端引导信息和关键访问控制信息的可靠性与可审计性。SRS 覆盖用户访问控制、客户端/引导信息的区块链读写、LwM2M 数据解析及相关后端服务行为。

**人为决定**

- [ ] 接受
- [ ] 拒绝
- [x] 部分接受（`PARTIAL_ACCEPT`：混合声明；有些有效，有些无效）

可选的人工注释：
> 部分接受。原因是 README 和架构图显示系统范围不只是用户管理、区块链存储和 JSON 解析，还包括 LwM2M server、bootstrap server、secure API、management web UI、blockchain network 等整体关系。但不建议把架构图逐项翻译进 SRS，否则会变成“答案泄露”。

### R005：可追溯性

- 严重性：`minor`
- 建议采取的措施：`partial_accept_as_issue`
- SRS 位置：C-003 / FR-005 / FR-003 证据分配
- 证据 IDs：E001、E003、E004

**索赔或差距**

FR-005 (getClient -> BootstrapConfig) 引用 E004（测试文件，ClientTest.java）作为“显式”源，而生产实现出现在 ClientService (E003) 和 ClientStoreService 下（E001）。合约名称 `BootstrapStore` 来自 E003，但显示的 getClient/addClient 代码来自测试 (E004)。

**模型意见**

主要从测试文件导出功能需求作为支持证据是可以接受的，但作为权威来源却很弱。生产 getClient/addClient 逻辑可能与测试工具不同。可追溯性信心标记为“中”是合理的，但证据最好应该指向生产服务代码。

**推荐人工检查**

确认 FR-004/FR-005 中指定的 addClient/getClient 是否反映生产 ClientService/ClientStoreService 代码，而不仅仅是 ClientTest.java，并添加生产代码证据引用。

**型号建议更改 SRS**

FR-004/FR-005 源证据：在 E004 旁边添加生产代码证据参考 (ClientService/ClientStoreService)，或注释 E004 是测试衍生源，待生产代码确认。

可选的人工修订修复：
> 在第 9 节可追溯性矩阵中调整证据分配：FR-004 的证据改为引用生产服务证据和测试证据，例如 E003, E004。
FR-005 的证据保留 E004，并补充 Leshan/bootstrap 侧生产实现证据，例如 E001。如果矩阵有说明列，可写：E004 为测试派生证据，用于确认合约字段转换和调用形态；生产路径由后端服务和 Leshan/bootstrap 存储实现共同支持。

**人为决定**

- [ ] 接受
- [ ] 拒绝
- [x] 部分接受（`PARTIAL_ACCEPT`：混合声明；有些有效，有些无效）

可选的人工注释：
> 部分接受。原因是 FR-004 的新增客户端数据路径有生产代码支持，但 FR-005 的 getClient/bootstrap 配置检索证据较多来自测试和 Leshan 侧实现。SRS 需要更清楚地区分生产证据和测试证据。

### R006：歧义

- 严重性：`minor`
- 建议采取的措施：`accept_as_issue`
- SRS 位置：DR-005 / NFR-003 / E005 浮点类型
- 证据IDs：E005

**索赔或差距**

DR-005 一般列出“浮点类型”。 E005 显示逻辑：当 getAsDouble()==getAsLong() 时，数字映射到 INTEGER，否则映射到（截断的、未显示的）FLOAT/DOUBLE 类型。 SRS 中未指定确切的非整数类型名称和整数与浮点区分规则。

**模型意见**

区分规则（如果 double 等于 long，则为整数，否则为浮点）在 E005 中是具体且可测试的，并且应声明为使 DR-005 可验证，而不是松散的“浮点类型”。

**推荐人工检查**

阅读 LwM2mNodeDeserializer.java 中完整的 getTypeFor 方法，以确认确切的非整数返回类型和相等规则。

**型号建议更改 SRS**

DR-005：对于布尔值，将映射描述替换为 'BOOLEAN；对于字符串值，将映射描述替换为 STRING；当数值满足 getAsDouble()==getAsLong() 时，将映射描述替换为 INTEGER；以及浮点资源类型（FLOAT/DOUBLE — 确认确切类型）否则。 [E005]'。

可选的人工修订修复：
> 在 DR-005 中将类型映射规则改为：JSON 原始值映射规则如下：boolean 映射为 BOOLEAN；string 映射为 STRING；number 若其 double 值可无损表示为 long 值，则映射为 INTEGER；其他 number 映射为 FLOAT；未覆盖的原始值类型默认按 STRING 处理。

**人为决定**

- [x] 接受
- [ ] 拒绝
- [ ] 部分接受（`PARTIAL_ACCEPT`：混合声明；有些有效，有些无效）

可选的人工注释：
> 接受。原因是 LwM2M JSON 数值类型映射规则在源码中很明确：布尔值、字符串、整数型数字、非整数数字分别映射，不应笼统写“浮点类型”。
