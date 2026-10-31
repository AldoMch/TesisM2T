<!-- human_srs_review_A.md 由审阅者 A 生成。保留原始 human_srs_review.md。所有人类的判断都是英语的。 -->

# 人类 SRS 审查表

## 元数据

- 示例目录：`s000028_3e80e738`
- 生成SRS：`final_srs.md`
- 证据包：`evidence_pack.json`
- 评测型号：`claude-opus-4-8`
- 生成于：`2026-06-05T15:41:17.348200Z`
- 原始模型响应：`model_srs_review_raw.md`
- 解析状态：`parsed`

## 总体模型意见

- 推荐：`revise`
- 置信度：`0.72`
- 理由：SRS 具有强大的可追溯性证据，但一些要求夸大了相对于截断证据的置信度（e.g.、令牌有效性单位、回调 URL 值、角色范围），并且 FR-009 将“错误”响应参数错误标记为可用标头。需要进行一些有针对性的修改。

## 人类整体决策

- [ ] 接受
- [ ] 拒绝
- [x] 部分接受

原因：
> ACCEPT=2，PARTIAL_ACCEPT=1，REJECT=3，PARTIAL_ACCEPT=0。

## 积极的观察

- 强大且基本准确的可追溯性：每个 FR/NFR 都引用了与引用的模板工件相匹配的具体证据 IDs。
- 从 E003 正确捕获显式的、可验证的网络事实（PrivateDnsEnabled=true、SQS 服务名称、VPC CIDR 入口）。
- 适当地对声明性 CloudFormation 模板使用“检查”验证，并将 NFR-004 标记为“推断”而不是夸大其词。
- Cognito 细节（AllowUnauthenticatedIdentities、自定义：角色/电子邮件写入属性、ClientId/ProviderName 绑定）忠实地源自 E001。

## 候选人问题

### R001：矛盾

- 严重性：`major`
- 建议采取的措施：`partial_accept_as_issue`
- SRS 位置: FR-009 / 通讯接口 / 数据交换格式
- 证据IDs：E004

**索赔或差距**

SRS 声明 API“应包含”/“应返回”`x-pagopa-pn-cx-role` 标头，但证据显示 `method.response.header.x-pagopa-pn-cx-role: false`，在 API 网关中意味着标头已声明但不是必需/映射的（布尔值指示标头是否是必需的，并且缺少集成映射意味着它实际上不是由默认）。

**模型意见**

证据（E004）仅显示值为 `false` 的方法响应参数声明。这将标头声明为方法响应契约的一部分，但不保证标头在运行时填充/返回。 SRS 语言“API 响应应包括”夸大了这一点。 FR-009 自己的输出措辞（“在方法响应定义中可用”）比通信接口措辞更准确，从而造成内部不一致。

**推荐人工检查**

检查 account-B-api-gateway.yaml 以确认集成响应是否实际映射/设置 `x-pagopa-pn-cx-role` 标头，以及 `false` 布尔值表示什么（必需与可选）。

**型号建议更改 SRS**

将通信接口项目符号修改为：“`WhoAmI` 方法响应定义应声明 `x-pagopa-pn-cx-role` 响应标头（声明为可选，值 `false`）。来源：E004。相应地调整数据交换格式措辞。

可选的人工修订修复：
> 建议改成“角色校验方法的 200 响应配置应声明并映射角色响应头；该响应头在方法响应中为可选声明，值来自认证上下文的角色声明”。

**人为决定**

- [ ] 接受
- [ ] 拒绝
- [x] 部分接受（`PARTIAL_ACCEPT`：混合声明；有些有效，有些无效）

可选的人工注释：
> 完整源码显示集成响应确实映射了角色响应头，但方法响应里 false 表示该头是可选声明，不应写成“API 响应应包含”。

### R002：不支持的声明

- 严重性：`minor`
- 建议采取的措施：`probably_ignore`
- SRS 位置：FR-008 / 数据要求（部署输出）
- 证据IDs：E004

**索赔或差距**

SRS 断言 `CallbackURL` 输出已发布为“API 网关端点”，但证据截断了实际的 `Value:` 表达式，因此 URL 的精确内容/格式未知。

**模型意见**

E004 显示 `Outputs: CallbackURL: Description: "API Gateway endpoint" Value: !Sub "`，但该值被截断。支持输出的存在；确切的 URL 结构不是。 FR-008 仅通过声称存在输出来保持安全，这很好，但审阅者应确认没有过度规范的出现。

**推荐人工检查**

确认 CallbackURL 的完整 `!Sub` 表达式，以验证它确实是网关调用 URL。

**型号建议更改 SRS**

如果 FR-008 仍限于“发布描述为 API 网关端点的 CallbackURL 输出”，则无需进行更改。除非经过验证，否则请避免指定 URL 格式。

可选的人工修订修复：
> 

**人为决定**

- [ ] 接受
- [x] 拒绝
- [ ] 部分接受（`PARTIAL_ACCEPT`：混合声明；有些有效，有些无效）

可选的人工注释：
> 人工检查确认 CallbackURL 是完整的 API Gateway execution URL；当前 SRS 只说“输出一个被标识为 API Gateway 端点的回调 URL”，没有过度规定格式。

### R003：不可验证

- 严重性：`minor`
- 建议采取的措施：`accept_as_issue`
- SRS 位置：NFR-004 / FR-005
- 证据IDs：E001

**索赔或差距**

NFR-004（“未经授权的访问...应限制在模板描述的范围内”）无法独立验证，因为实际的 IAM 策略语句在 E001 中被截断。

**模型意见**

E001 显示该角色是使用 AssumeRolePolicyDocument 创建的，但实际权限语句（“访问非常有限”）被截断。 “有限范围”是由模板注释断言的，而不是由明显的可观察策略断言的。 NFR-004 被正确标记为“推断”，这很好，但其接受基础（“匹配已证明的配置意图”）不是可验证的测试。

**推荐人工检查**

查看 account-A-cognito.yaml 中的完整 IAM 角色策略，以确定构成“受限访问”的具体允许操作/资源。

**型号建议更改 SRS**

将 NFR-004 修改为：“未经授权的访问 IAM 角色只能由已创建的身份池（Web 身份联合）中的身份承担。”策略验证后将枚举具体允许的操作。更新验收依据以引用 AssumeRolePolicyDocument 条件。

可选的人工修订修复：
> 将 NFR-004 的把“按模板描述限制其范围”改成可检查条件：未认证角色只能由指定身份池中的 unauthenticated Web 身份联合身份承担，策略范围限于模板列出的未认证访问动作。

**人为决定**

- [x] 接受
- [ ] 拒绝
- [ ] 部分接受（`PARTIAL_ACCEPT`：混合声明；有些有效，有些无效）

可选的人工注释：
> 来源检查已完成，接受该问题。原句太泛，验收时无法独立判断。

### R004：范围

- 严重性：`minor`
- 建议采取的措施：`accept_as_issue`
- SRS 位置：C-005 / FR 列表 / 第 1 部分范围
- 证据IDs：E005

**索赔或差距**

安装 README (E005) 引用了许多仅抽象提及的附加服务和步骤（数据保管库堆栈、SPID 集线器、DNS 委派、服务相关角色、多个配置文件）； SRS 范围可能低估了此存储库执行的安装编排的广度。

**模型意见**

E005 揭示了大量的部署编排（多个 AWS 配置文件、ECS 的服务相关角色创建、公共 DNS/证书设置、数据保管库 CFN 堆栈）。 SRS 将其减少为 C-005 和一个数据行。保守地说这是可以接受的，但可能低估了存储库范围。值得人类决定是否添加要求或明确限制范围。

**推荐人工检查**

充分查看 Installation/README.md 以确定其他安装要求（DNS、证书、服务相关角色、多配置文件编排）是否属于范围。

**型号建议更改 SRS**

在第 1 节产品范围中添加边界注释：“在此 SRS 中引用了超出已证实的 Cognito/API/VPC 工件（e.g.、DNS/证书设置、数据保管库堆栈、服务相关角色）的安装编排，但未完全指定。”如果范围内得到确认，则可以选择添加 FR 以创建服务相关角色。

可选的人工修订修复：
> 

**人为决定**

- [ ] 接受
- [x] 拒绝
- [ ] 部分接受（`PARTIAL_ACCEPT`：混合声明；有些有效，有些无效）

可选的人工注释：
> 本 SRS 只详细规定已证实的 Cognito/API/VPC 工件。没有问题

### R005：架构_详细信息

- 严重性：`minor`
- 建议采取的措施：`accept_as_issue`
- SRS 位置：第二节/整体架构
- 证据 IDs：E001、E004

**索赔或差距**

未引用描述 Cognito REST-API 身份验证流程的真实架构图 (architecture-cognito.png)，并且 SRS 中未捕获跨账户拆分（account-A-cognito 与 account-B-api-gateway）。

**模型意见**

证据文件名表明有两个帐户架构（Cognito 的帐户 A，API 网关的帐户 B），这是 SRS 中缺少的重要架构细节。该图可以确认身份验证/角色验证流程。这应该根据地面实况图像进行检查。

**推荐人工检查**

打开架构-cognito.png并确认跨账户拓扑（账户A Cognito提供商，账户B API网关）和角色标头验证流程；添加到产品视角。

**型号建议更改 SRS**

添加到第 2 节产品视角：“该解决方案涵盖两个 AWS 帐户：根据rest-api-cognito 架构，帐户 A 托管 Cognito 用户/身份池 (account-A-cognito.yaml)，帐户 B 托管 API 网关 (account-B-api-gateway.yaml)。来源：E001、E004。

可选的人工修订修复：
> 建议在“产品视角”补充跨账户拓扑：认证资源位于 Cognito 账户，API Gateway 位于 API Gateway 账户，并通过用户池 ARN/授权器形成跨账户认证关系。

**人为决定**

- [x] 接受
- [ ] 拒绝
- [ ] 部分接受（`PARTIAL_ACCEPT`：混合声明；有些有效，有些无效）

可选的人工注释：
> 来源检查已完成，接受该问题。

### R006：可追溯性

- 严重性：`minor`
- 建议采取的措施：`probably_ignore`
- SRS 位置：可追溯性矩阵 FR-002 / NFR-003 置信度评级
- 证据IDs：E002

**索赔或差距**

FR-002/NFR-003 被评为“高”/“显式”置信度，但 AllowedValues 枚举仅针对 AccessTokenValidityUnits 完全显示； IdToken/RefreshToken 单位参数被截断（E002）。

**模型意见**

E002 显式显示 AccessTokenValidityUnits 的 AllowedValues [天、小时、分钟、秒]，并以类似方式描述 IdTokenValidityUnits，但 Id/Refresh 单元的 AllowedValues 块被截断。该要求将枚举概括为所有三个参数。可能是正确的，但三个参数中的两个的证据是部分的。

**推荐人工检查**

确认 AllowedValues 在 account-A-cognito.yaml 中对 IdTokenValidityUnits 和 RefreshTokenValidityUnits 的定义相同。

**型号建议更改 SRS**

如果未确认，请将 FR-002 缩小为“至少 AccessTokenValidityUnits”，或添加注释，假定 Id/Refresh 枚举与待验证相同。

可选的人工修订修复：
> 

**人为决定**

- [ ] 接受
- [x] 拒绝
- [ ] 部分接受（`PARTIAL_ACCEPT`：混合声明；有些有效，有些无效）

可选的人工注释：
> 不建议改。完整源码确认 Access/Id/Refresh 三类 token validity unit 都有相同枚举值；问题只是证据片段截断导致的疑虑。