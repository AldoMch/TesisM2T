<!-- human_srs_review_A.md 由审阅者 A 生成。保留原始 human_srs_review.md。所有人类的判断都是英语的。 -->

# 人类 SRS 审查表

## 元数据

- 示例目录：`s000061_2eb4d99c`
- 生成SRS：`final_srs.md`
- 证据包：`evidence_pack.json`
- 评测型号：`claude-opus-4-8`
- 生成于：`2026-06-05T15:57:29.065765Z`
- 原始模型响应：`model_srs_review_raw.md`
- 解析状态：`parsed`

## 总体模型意见

- 推荐：`revise`
- 置信度：`0.72`
- 理由：SRS 结构良好，大多数需求都可以追溯到证据块。然而，证据包很窄（来自一个更大的存储库的 6 个块，包含 38 个文档和记录的架构图），并且 SRS 低估了实际范围（IoT 设备模拟、MQTT/IoT 核心、设备类型、UI）。几个约束和几个 FRs 依赖于部分代码片段；某些声明（e.g.、CORS 状态 200 行为、ROUTE_BUCKET env 约束范围）需要验证。 C-005 许可证约束和 STACK_NAME/SOLUTION_ID env 声明的范围正确，仅适用于已证明的文件，这很好。

## 人类整体决策

- [ ] 接受
- [ ] 拒绝
- [x] 部分接受

原因：
> ACCEPT=5，PARTIAL_ACCEPT=0，REJECT=2，PARTIAL_ACCEPT=0。

## 积极的观察

- 通过专用的可追溯性矩阵和验证/验收部分，要求可以一致地追溯到特定证据 IDs。
- SRS 适当地将范围限制为已证实的行为，并使用谨慎的置信水平（e.g.，自定义资源项的中等）。
- C-005（许可证）的范围正确地限定为“证据中的存储库源文件”，而不是过度声明存储库范围的许可。
- 数据要求 (DR-001/002/003) 密切反映 E001 和 E005 中可见的具体字段，使其易于验证。
- 非功能性需求（日志记录级别、跟踪、REGIONAL 端点、JSON 访问日志）直接映射到 E004 中的显式配置值。

## 候选人问题

### R001：范围

- 严重性：`major`
- 建议采取的措施：`partial_accept_as_issue`
- SRS位置：1.2产品范围； 2.1 产品视角
- 证据 IDs：E003、E005

**索赔或差距**

SRS 将产品范围限定为 API 网关 REST API、CloudFormation 自定义资源以及仅 S3 车辆路线加载。该存储库是一个 IoT 设备模拟器（名称为 README 和 architecture.png），其核心功能是模拟 IoT 设备并发布遥测数据，可能通过 MQTT 发布到 AWS IoT 核心，并具有UI。

**模型意见**

证据包是 38 个文档存储库的一小部分（6 个块），不会显示中央模拟/IoT 发布行为或 UI。 SRS 正确地将自身限制为提供的证据，但生成的范围声明实质上低估了存储库。应检查 architecture.png 真实图以确认省略的组件（IoT 核心、设备生成器、模拟引擎、Web 控制台）。

**推荐人工检查**

打开 architecture.png 和 README 以枚举顶级组件（IoT Core/MQTT、模拟引擎、设备类型、Web UI、DynamoDB）。决定 SRS 范围是否应明确指出这些超出了证据包的范围，而不是扩展 SRS。

**型号建议更改 SRS**

在 1.2 中添加范围限制注释：“此 SRS 仅反映证据包中存在的存储库行为的子集。该存储库是一个 IoT 设备模拟器，还包括设备模拟、遥测发布到 AWS IoT 核心以及管理 UI，这些内容未包含在所提供的证据中，并且超出了本文档的范围。

可选的人工修订修复：
> 在第 1.2 Product scope 和第 2.1 Product perspective 扩展为：本系统是部署在 AWS 上的 IoT 设备模拟器，提供 Web 管理控制台、模拟/设备类型管理 API、设备模拟执行能力、路由数据加载能力，并将模拟设备生成的消息发布到 AWS IoT 主题；系统还包含部署期自定义资源，用于初始化配置和辅助资源。 保留原有 API、自定义资源、S3 路由加载内容，但不要写“这些内容超出本文档范围”。

**人为决定**

- [x] 接受
- [ ] 拒绝
- [ ] 部分接受（`PARTIAL_ACCEPT`：混合声明；有些有效，有些无效）

可选的人工注释：
> README 和源码确认该仓库是 GUI based IoT Device Simulator，不只是 API Gateway、自定义资源和 S3 路由加载。源码还显示 Web 控制台、Cognito、DynamoDB、Step Functions、模拟引擎、AWS IoT 发布等能力。

### R002：不可验证

- 严重性：`major`
- 建议采取的措施：`partial_accept_as_issue`
- SRS 位置：FR-002；第8节（FR-002受理）
- 证据IDs：E004

**索赔或差距**

FR-002 声明“CORS 状态代码 200”作为输出和接受标准。 E004 在 CORS 预检配置 (defaultCorsPreflightOptions) 中显示 `statusCode: 200`，这是一个配置值，而不是书面表述的可观察的运行时 CORS 状态保证。

**模型意见**

“200 CORS 状态行为”可以通过检查配置来验证，但将其表述为响应状态的“测试”接受可能会夸大所证明的内容。验证方法（测试）和验收文本将配置检查与运行时行为混合在一起。建议将验证与 CORS 预检配置的检查对齐，除非存在运行时测试。

**推荐人工检查**

确认 `statusCode: 200` 是否是 api.ts 中的 CORS 预检选项，以及是否有任何测试执行实时 OPTIONS 请求。相应调整验证方法。

**型号建议更改 SRS**

在 FR-002 中，将验证更改为“检查”并接受为：“API 构造 CORS 预检选项指定allowMethods [GET、POST、PUT、DELETE、 OPTIONS]、allowHeaders [内容类型、X-Amz-日期、授权、X-Api-Key] 和 statusCode 200。

可选的人工修订修复：
> 在 FR-002 中把 Verification 从 Test 改为 Inspection。系统行为改为：系统应配置 CORS 预检选项，允许 GET、POST、PUT、DELETE、OPTIONS 方法，允许 Authorization、Content-Type、X-Amz-Date、X-Amz-Security-Token、X-Api-Key 请求头，并将预检配置的 statusCode 设置为 200。 第 8 节 FR-002 验收也改成“检查 API 构造中的 CORS 配置”。

**人为决定**

- [x] 接受
- [ ] 拒绝
- [ ] 部分接受（`PARTIAL_ACCEPT`：混合声明；有些有效，有些无效）

可选的人工注释：
> statusCode: 200 是 API Gateway CORS 预检配置值，不是已验证的运行时 OPTIONS 响应测试。当前 FR-002 和第 8 节把它写成 Test/运行时行为，过强。

### R003：可追溯性

- 严重性：`minor`
- 建议采取的措施：`partial_accept_as_issue`
- SRS 位置：FR-001； 3.2 REST API；第 8 节 FR-001
- 证据 IDs：E003、E004

**索赔或差距**

FR-001 断言系统“提供 API 端点和 API ID”。 E004 显示 `this.apiEndpoint = ;`（块中被截断/为空）和 `this.apiId = api.restApiId;`。 apiEndpoint 分配值在证据中不可见。

**模型意见**

apiId 有据可查； apiEndpoint 分配被截断，因此端点声明依赖于部分可见的片段。这是一个弱可追溯性问题，而不是一个矛盾。严重程度较低，但值得一看。

**推荐人工检查**

检查 api.ts 以确认 apiEndpoint 已分配给真实的 URL 表达式（非空），支持“API 端点”声明。

**型号建议更改 SRS**

如果端点分配已确认，请保持 FR-001 不变。如果未确认，请将 FR-001 输出缩小为“an API ID (restApiId)”，并将端点声明标记为需求验证。

可选的人工修订修复：
> 

**人为决定**

- [ ] 接受
- [x] 拒绝
- [ ] 部分接受（`PARTIAL_ACCEPT`：混合声明；有些有效，有些无效）

可选的人工注释：
> 源码确认 apiEndpoint 被赋值为 API Gateway URL，apiId 也来自 restApiId，所以 FR-001 “提供 API endpoint 和 API ID”成立。

### R004：不支持的声明

- 严重性：`minor`
- 建议采取的措施：`accept_as_issue`
- SRS位置：2.1产品视角； 2.2（“Lambda 支持的微服务集成”）
- 证据IDs：E003

**索赔或差距**

SRS 指出“Lambda 支持的微服务集成”。 E003 将 `microservicesLambda: LambdaFunction` 和 `microservicesLambdaFunction` 引用为属性，但证据未显示集成接线（i.e.，路由到 Lambda 的方法）。

**模型意见**

微服务 Lambda 属性的存在已得到证实；推断实际的 API 到 Lambda 集成行为。这种说法是有道理的，但集成机制并不完整。保留但严格遵守属性声明，或标记为推断。

**推荐人工检查**

在 api.ts 中验证 REST 方法是否与微服务Lambda (LambdaIntegration) 集成。如果是的话，证据就足够了。

**型号建议更改 SRS**

在 2.1 中，除非在 api.ts 中确认集成接线，否则将改写为“与 API（LambdaFunction 属性）关联的微服务 Lambda 构造”。

可选的人工修订修复：
> 

**人为决定**

- [x] 接受
- [ ] 拒绝
- [ ] 部分接受（`PARTIAL_ACCEPT`：混合声明；有些有效，有些无效）

可选的人工注释：
> 源码确认 API Gateway 使用 AWS_PROXY integration，URI 指向 microservices Lambda，并将 /simulation、/devicetypes 等资源方法接到该 integration，所以不是 unsupported claim。

### R005：歧义

- 严重性：`minor`
- 建议采取的措施：`accept_as_issue`
- SRS 位置：FR-005； DR-002； C-003
- 证据IDs：E005

**索赔或差距**

E005 显示 `routeName = snapshot.routeInfo?.routeName || `（默认回退被截断）。 SRS 指出 S3 密钥是 `routeName`，但如果未定义routeName，则密钥可能为空/默认。未指定对丢失的routeName 的处理。

**模型意见**

路由加载逻辑使用可选链接和后备默认值，该默认值在证据中被截断。 SRS 不解决空/默认路由名称的情况，从而使丢失路由信息的行为不明确。次要但影响 FR-005/FR-006 完整性。

**推荐人工检查**

检查dynamics-model.js以查看snapshot.routeInfo.routeName不存在时routeName的默认值以及空键是否触发FR-006错误路径。

**型号建议更改 SRS**

在 FR-005 中添加一个子句：“如果 routeInfo.routeName 不存在，系统应使用已实现的默认密钥值（在动态中验证 -model.js）。”检查后解析准确的默认文本。

可选的人工修订修复：
> 在 FR-005 改为：当 snapshot 提供 routeInfo.routeName 时，系统应使用该值作为 S3 object key；当 routeInfo.routeName 不存在时，系统应生成默认 route key，格式为 route-{随机路由标识}.json；随后从 ROUTE_BUCKET 指定的 S3 bucket 读取并解析 JSON 路由数据，组装 route state。 同步修改 DR-002/C-003，说明 routeName 是“输入 routeName 或生成的默认 route key”。

**人为决定**

- [x] 接受
- [ ] 拒绝
- [ ] 部分接受（`PARTIAL_ACCEPT`：混合声明；有些有效，有些无效）

可选的人工注释：
> 源码确认当 snapshot.routeInfo.routeName 不存在时，会生成默认 key：route-{随机路由标识}.json。当前 SRS 只写使用 routeName，漏了缺省行为。

### R006：可追溯性

- 严重性：`minor`
- 建议采取的措施：`accept_as_issue`
- SRS 位置：C-004； 2.4 运行环境
- 证据 IDs：E002、E005

**索赔或差距**

C-004 列出环境变量 AWS_REGION、SOLUTION_ID、SOLUTION_VERSION、STACK_NAME 作为自定义资源约束，这些约束源自设置 process.env 进行模拟的测试文件 (E002)。 2.4 另外将 ROUTE_BUCKET 列为自定义资源环境上下文的一部分。

**模型意见**

E002 中的环境变量来自单元测试模拟 (process.env = {...})，这是代码读取它们的合理证据，但应根据实际处理程序确认将它们构建为生产“约束”。另外ROUTE_BUCKET（E005）属于模拟器动力学模型，而不是自定义资源；在 2.4 中将它们混合在一个环境列表下有点不精确。

**推荐人工检查**

确认自定义资源处理程序在运行时实际读取 SOLUTION_ID/SOLUTION_VERSION/STACK_NAME（不仅在测试中），并将 ROUTE_BUCKET 归因于模拟器组件。

**型号建议更改 SRS**

在 2.4 中，按组件拆分环境列表：自定义资源（AWS_REGION、SOLUTION_ID、SOLUTION_VERSION、STACK_NAME）和模拟器（ROUTE_BUCKET）。将 C-004 源标记为“测试模拟派生”；在处理程序中进行验证。

可选的人工修订修复：
> 在 2.4 Operating environment 按组件拆分：自定义资源运行环境：AWS Lambda / CloudFormation invocation context，并可使用 solution ID/version 环境配置设置 AWS SDK user agent。模拟器运行环境：ROUTE_BUCKET 用于定位路由数据 S3 bucket。 将 C-004 改为：自定义资源处理依赖 CloudFormation 事件、Lambda context，以及 solution ID/version 环境配置；StackName 应作为自定义资源输入属性处理。

**人为决定**

- [x] 接受
- [ ] 拒绝
- [ ] 部分接受（`PARTIAL_ACCEPT`：混合声明；有些有效，有些无效）

可选的人工注释：
> ROUTE_BUCKET 属于 simulator route loading，不属于 custom resource。自定义资源 handler 直接读取的是 SOLUTION_ID/SOLUTION_VERSION；STACK_NAME 是 custom resource input property，不是 handler 中的环境变量。当前 2.4/C-004 把它们混在一起。

### R007：架构_详细信息

- 严重性：`minor`
- 建议采取的措施：`accept_as_issue`
- SRS位置：2.4运行环境；整体
- 证据 IDs：无

**索赔或差距**

没有提及 AWS IoT Core / MQTT、DynamoDB、Cognito 或 IoT 设备模拟器架构通常包含且 architecture.png 可能描述的其他组件。

**模型意见**

由于证据包忽略了这些，因此 SRS 无法断言它们；但真实的架构图是明确可用的，应该查阅以确保在检索过程中不会遗漏任何关键的证据组件。这是架构细节完整性检查，而不是断言错误。

**推荐人工检查**

检查 architecture.png，确认 IoT Core/MQTT、DynamoDB、Cognito、模拟引擎和 UI 是否属于系统的一部分；决定证据包/SRS是否需要扩展。

**型号建议更改 SRS**

图表审查后，可以选择添加操作环境注释，枚举图表确认的 AWS 服务，这些服务超出了证据包范围，在此 SRS 中明确标记为不满足要求。

可选的人工修订修复：
> 和 R001 合并改：在 2.4 Operating environment 增加抽象描述：系统运行在 AWS 托管服务环境中，包括 Web 控制台静态托管与分发、身份认证、API Gateway、Lambda、DynamoDB、Step Functions、Amazon S3、AWS IoT 以及 CloudFormation 自定义资源。 若新增 FR，建议加一条：系统应运行设备模拟并将生成的设备消息发布到 AWS IoT 主题。

**人为决定**

- [x] 接受
- [ ] 拒绝
- [ ] 部分接受（`PARTIAL_ACCEPT`：混合声明；有些有效，有些无效）

可选的人工注释：
> 架构图和源码确认有 Web 控制台、CloudFront/S3、Cognito、API Gateway、Lambda、DynamoDB、Step Functions、AWS IoT、S3 等运行环境。当前 SRS 的 operating environment 太窄。
