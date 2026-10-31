# 软件需求规格说明书

## 1. 引言

### 目的
本 SRS 定义了由所提供证据包中表示的 `pn-infra` 仓库组件的、基于证据支撑的需求：用于 Cognito 认证资源、API Gateway 暴露、VPC 端点以及安装/部署支持的基础设施模板和脚本。

### 产品范围
有证据支持的范围包括：
- 基于 AWS CloudFormation 创建 Cognito 用户池和身份池资源
- 用于角色校验的 API Gateway 部署和响应头暴露
- 面向 Amazon SQS 的 VPC 接口端点配置
- 安装时的预配输入和特定环境参数

### 目标读者
本文档面向：
- 部署或审查所提供模板的基础设施工程师
- 使用已暴露 API Gateway 端点的集成人员
- 验证网络和身份配置的安全与运维审查人员

### 参考资料
- 仓库：`pagopa/pn-infra`
- 仓库 URL：https://github.com/pagopa/pn-infra
- 提交：`3898c35e634efe1527655e90a586ee6247de24f4`
- 证据来源：`E001` 至 `E006`

## 2. 总体描述

### 产品视角
有证据支持的产品是一个由 CloudFormation 模板和安装脚本组成的 AWS 基础设施层。它预配 Cognito 认证资源、API Gateway 部署工件以及到 AWS 服务的 VPC 接口连接。来源：`E001`, `E002`, `E003`, `E004`, `E005`。

### 产品功能概述
- 通过 CloudFormation 创建 Cognito 用户池和身份池（`E002`）
- 将 Cognito 身份池与 Cognito 用户池客户端/提供者关联（`E001`）
- 在身份池中允许未认证身份（`E001`）
- 创建与身份池绑定的、用于未授权访问路径的受限 IAM 角色（`E001`）
- 部署 API Gateway 阶段并发布回调端点 URL（`E004`）
- 从 `WhoAmI` API 方法返回与角色相关的响应头（`E004`）
- 在指定子网和 VPC 中预配启用私有 DNS 的 SQS VPC 接口端点（`E003`）

### 用户类别
- 调用安装/设置命令并部署模板的基础设施操作人员（`E005`）
- 使用 API Gateway 回调端点和响应头的 API 客户端（`E004`）
- 由 Cognito 支持的身份，包括身份池支持的未认证身份（`E001`）

### 运行环境
- AWS CloudFormation（`E002`）
- AWS Cognito 用户池和身份池（`E001`, `E002`）
- AWS IAM 角色（`E001`）
- AWS API Gateway（`E004`）
- AWS VPC、子网、安全组和 VPC 接口端点（`E003`）
- 通过区域服务端点命名访问 Amazon SQS（`E003`）

### 假设与依赖
- 部署依赖于提供给 CloudFormation 和安装脚本的 AWS 账户及区域上下文（`E002`, `E003`, `E005`）
- API Gateway 部署依赖于在部署前已定义 `WhoAmI` 和 `ECS` 方法（`E004`）
- VPC 端点依赖于已提供现有 VPC、VPC CIDR 和目标子网（`E003`）

## 3. 外部接口需求

### 用户接口
没有图形用户界面的证据。该仓库通过命令执行和 CloudFormation 参数暴露基于脚本和模板驱动的操作接口。来源：`E002`, `E005`。

### 软件/API 接口

| 接口 | 需求 |
|---|---|
| Cognito | 系统使用 AWS Cognito 用户池和身份池资源，并使用 `ClientId` 和 `ProviderName` 将身份池绑定到 Cognito 提供者。来源：`E001`, `E002` |
| API Gateway | 系统暴露一个带有阶段名称参数和回调 URL 输出的 API Gateway 部署。来源：`E004` |
| 通过 VPC 端点访问 SQS | 系统通过 AWS VPC 接口端点与 Amazon SQS 集成，使用区域服务名称 `com.amazonaws.${AWS::Region}.sqs`。来源：`E003` |
| IAM | 系统为与身份池关联的未授权访问创建 IAM 角色资源。来源：`E001` |

### 通信接口
- 到 SQS 的 AWS 私有网络通信应通过启用了私有 DNS 的接口 VPC 端点进行。来源：`E003`
- API 响应应在有证据支持的 `WhoAmI` 方法响应中包含 `x-pagopa-pn-cx-role` 头。来源：`E004`

### 数据交换格式
- 使用 CloudFormation YAML 模板进行基础设施声明。来源：`E002`, `E003`, `E004`
- API Gateway 响应元数据包含 HTTP 头 `x-pagopa-pn-cx-role`。来源：`E004`

## 4. 功能需求

| ID | 描述 | 触发器/输入 | 系统行为 | 输出 | 优先级 | 验证 | 来源证据 |
|---|---|---|---|---|---|---|---|
| FR-001 | 预配 Cognito 认证资源 | 使用所需参数部署 Cognito CloudFormation 栈 | 系统应创建 Cognito 用户池和身份池资源作为栈的一部分。 | 已创建的 Cognito 认证资源 | 高 | 检查 | `E002` |
| FR-002 | 支持可配置的令牌有效期单位 | 栈参数 `AccessTokenValidityUnits`、`IdTokenValidityUnits`、`RefreshTokenValidityUnits` | 对于有证据支持的令牌单位参数，系统应仅接受 `days`、`hours`、`minutes` 或 `seconds` 的令牌有效期单位值。 | 参数化的令牌有效期配置 | 中 | 检查 | `E002` |
| FR-003 | 将身份池绑定到 Cognito 提供者 | 创建身份池并引用用户池客户端和提供者 | 系统应使用指定的 `ClientId` 和 `ProviderName` 为身份池配置 Cognito 身份提供者。 | 与 Cognito 提供者关联的身份池 | 高 | 检查 | `E001` |
| FR-004 | 允许未认证身份 | 身份池部署 | 系统应允许在已创建的身份池中存在未认证身份。 | 身份池接受未认证身份 | 高 | 检查 | `E001` |
| FR-005 | 创建受限的未授权访问角色 | 身份池部署 | 系统应创建一个与已创建身份池关联的、用于未授权访问的 IAM 角色。 | 未授权访问 IAM 角色 | 高 | 检查 | `E001` |
| FR-006 | 暴露可写用户属性 | 用户池客户端配置 | 系统应为属性 `custom:Role` 和 `email` 配置写访问权限。 | 可写用户属性包括角色和电子邮件 | 中 | 检查 | `E001` |
| FR-007 | 部署 API Gateway 阶段 | 使用 `ApiGatewayStageName` 部署 API Gateway | 系统应使用提供的阶段名称创建 API Gateway 部署。 | 已部署的 API Gateway 阶段 | 高 | 检查 | `E004` |
| FR-008 | 发布 API 回调端点 | API Gateway 成功部署 | 系统应输出一个被标识为 API Gateway 端点的回调 URL。 | `CallbackURL` 输出 | 中 | 检查 | `E004` |
| FR-009 | 在 `WhoAmI` 响应中返回角色头 | 调用有证据支持的 `WhoAmI` 方法并进入 HTTP 200 响应路径 | 系统应在方法响应中定义响应头 `x-pagopa-pn-cx-role` 以进行角色头校验。 | 在方法响应定义中可用的 HTTP 响应头 `x-pagopa-pn-cx-role` | 高 | 检查 | `E004` |
| FR-010 | 在 VPC 内提供私有 SQS 连接 | 使用 VPC、子网和安全组参数部署 VPC 端点模板 | 系统应在指定的 VPC 和子网中为 Amazon SQS 创建一个接口 VPC 端点。 | SQS 接口端点 | 高 | 检查 | `E003` |

## 5. 非功能需求

| ID | 需求 | 质量属性 | 优先级 | 验证 | 来源证据 | 置信度 |
|---|---|---|---|---|---|---|
| NFR-001 | SQS VPC 端点应将 `PrivateDnsEnabled` 设置为 `true`。 | 兼容性 / 网络集成 | 高 | 检查 | `E003` | 明确 |
| NFR-002 | 对接口端点的访问应由安全组限制，其入站来源为已配置的 VPC CIDR。 | 安全性 | 高 | 检查 | `E003` | 明确 |
| NFR-003 | 应将令牌有效期单位参数限制为枚举值 `days`、`hours`、`minutes` 或 `seconds`，以确保配置一致性。 | 可维护性 / 配置完整性 | 中 | 检查 | `E002` | 明确 |
| NFR-004 | 通过身份池角色进行的未授权访问应按模板描述限制其范围。 | 安全性 | 中 | 检查 | `E001` | 推断 |

## 6. 数据需求

| 区域 | 需求 | 来源证据 |
|---|---|---|
| 配置参数 | 系统使用部署参数，包括 `AuthName`、`CognitoUserPoolName` 和令牌有效期单位参数。 | `E002`, `E006` |
| 身份数据 | Cognito 配置包括可写属性 `custom:Role` 和 `email`。 | `E001` |
| 身份引用 | 身份池配置使用 `UserPoolId`、`ClientId` 和 `ProviderName` 引用。 | `E001` |
| API 响应数据 | API Gateway 方法响应定义头 `x-pagopa-pn-cx-role`。 | `E004` |
| 部署输出 | API 部署将 `CallbackURL` 作为输出发布。 | `E004` |
| 网络配置数据 | VPC 端点需要 `VpcId`、`Subnets`、`VpcCidr` 以及区域 SQS 服务名称。 | `E003` |
| 特定环境输入 | 安装工件引用环境/profile 值和服务特定键，例如 `UserRegistryApiKeyForPF` 以及 DNS/域输入。 | `E005` |

## 7. 约束

| ID | 约束 | 来源证据 |
|---|---|---|
| C-001 | 基础设施被定义为 AWS CloudFormation 模板，使用模板格式版本 `2010-09-09`。 | `E002` |
| C-002 | 认证解决方案被限制为 AWS Cognito 用户池和身份池服务。 | `E001`, `E002` |
| C-003 | 私有 SQS 连接被限制为 AWS VPC 接口端点和区域 AWS 服务命名。 | `E003` |
| C-004 | API 部署受限于在部署前依赖 `WhoAmI` 和 `ECS` 方法资源。 | `E004` |
| C-005 | 安装需要特定环境/profile 的操作输入以及 AWS CLI/服务设置步骤。 | `E005` |

## 8. 验证与验收

| Requirement IDs | Verification method | Acceptance basis |
|---|---|---|
| `FR-001`, `FR-003`, `FR-004`, `FR-005`, `FR-006`, `FR-007`, `FR-008`, `FR-010` | 检查 | CloudFormation 模板定义了所需的资源、属性和输出。 |
| `FR-002`, `NFR-003` | 检查 | 参数定义将令牌单位值限制为有证据支持的枚举。 |
| `FR-009` | 检查 | API Gateway 方法响应定义包含头 `x-pagopa-pn-cx-role`。 |
| `NFR-001`, `NFR-002`, `NFR-004` | 检查 | 端点和 IAM/安全组属性符合有证据支持的配置意图。 |

## 9. 可追溯性矩阵

| ID | 需求 | 类型 | 来源 | 证据类型 | 验证 | 置信度 |
|---|---|---|---|---|---|---|
| FR-001 | 预配 Cognito 认证资源 | 功能 | `E002` | 明确 | 检查 | 高 |
| FR-002 | 支持可配置的令牌有效期单位 | 功能 | `E002` | 明确 | 检查 | 高 |
| FR-003 | 将身份池绑定到 Cognito 提供者 | 功能 | `E001` | 明确 | 检查 | 高 |
| FR-004 | 允许未认证身份 | 功能 | `E001` | 明确 | 检查 | 高 |
| FR-005 | 创建受限的未授权访问角色 | 功能 | `E001` | 明确 | 检查 | 中 |
| FR-006 | 暴露可写用户属性 | 功能 | `E001` | 明确 | 检查 | 高 |
| FR-007 | 部署 API Gateway 阶段 | 功能 | `E004` | 明确 | 检查 | 高 |
| FR-008 | 发布 API 回调端点 | 功能 | `E004` | 明确 | 检查 | 高 |
| FR-009 | 在 `WhoAmI` 响应中返回角色头 | 功能 | `E004` | 明确 | 检查 | 中 |
| FR-010 | 在 VPC 内提供私有 SQS 连接 | 功能 | `E003` | 明确 | 检查 | 高 |
| NFR-001 | 在 SQS VPC 端点上启用私有 DNS | 非功能 | `E003` | 明确 | 检查 | 高 |
| NFR-002 | 将端点入站限制为 VPC CIDR | 非功能 | `E003` | 明确 | 检查 | 高 |
| NFR-003 | 将令牌有效期单位限制为枚举值 | 非功能 | `E002` | 明确 | 检查 | 高 |
| NFR-004 | 限制未授权访问角色范围 | 非功能 | `E001` | 推断 | 检查 | 中 |
