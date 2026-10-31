# 软件需求规格说明书

## 1. 引言

### 目的
本 SRS 规定了 `ertis-research/lwm2m-blockchain` 中各组件的、由仓库证据支持的需求，这些组件：
- 暴露经过身份验证的用户管理 HTTP 端点，
- 与基于区块链的客户端/引导存储进行交互，以及
- 解析 LwM2M 节点 JSON 结构。

### 产品范围
该仓库提供了集成以下功能的后端服务：
- 具有已认证用户操作的主应用后端，
- 使用 Ethereum/Web3j 访问客户端/引导信息的区块链能力，以及
- 使用与 Leshan 相关的节点结构处理 LwM2M 数据。

### 目标读者
- 产品负责人和维护者
- 后端和集成开发人员
- 测试工程师
- 评估需求到代码可追溯性的审查人员

### 参考资料
- 仓库：`ertis-research/lwm2m-blockchain`
- 仓库 URL：https://github.com/ertis-research/lwm2m-blockchain
- 提交：`caea581a21ac705c945540d1e54658b0bf82ecab`
- 证据包 ID：E001, E002, E003, E004, E005, E006

## 2. 总体描述

### 产品视角
该仓库似乎包含多个基于 Java 的后端组件：
- 基于 Spring 的主后端，带有用户端点，
- 使用 Web3j 和智能合约调用的区块链服务集成，
- 用于客户端/引导数据和 JSON 节点解析的 Leshan/LwM2M 服务端组件。

### 产品功能概述
- 通过经过身份验证的 HTTP 端点检索用户。
- 通过经过身份验证的 HTTP 端点添加用户。
- 检索存储在区块链中的客户端/安全信息。
- 向区块链合约提交客户端引导数据。
- 从区块链合约检索客户端引导配置。
- 将 LwM2M 节点 JSON 反序列化为类型化的节点结构，并拒绝无效的节点负载。

### 用户类别
- 调用用户管理端点的已认证 API 客户端。
- 与 Ethereum 节点集成的后端服务。
- 使用引导和节点数据的 LwM2M/Leshan 侧组件。

### 运行环境
证据支持如下：
- 基于 Java 的后端运行时
- Spring Web 控制器/服务环境
- 可通过 Web3j `HttpService` 访问的 Ethereum 节点
- Leshan/LwM2M 数据模型类

### 假设和依赖
- 用户管理请求依赖于 JWT 令牌验证结果。[E002]
- 基于区块链的客户端操作依赖于通过 Web3j HTTP 传输的 Ethereum 连接以及智能合约方法。[E001, E003, E004]
- LwM2M 节点数据依赖于 JSON 输入符合预期的对象/数组/值结构。[E005, E006]

## 3. 外部接口需求

### 用户界面
提供的材料中没有体现面向人工用户的 GUI。

### 软件/API 接口

| 接口 | 描述 | 证据 |
|---|---|---|
| 用户 HTTP API | 暴露经过身份验证的用户检索和用户创建操作；创建使用 `POST /add` 并接受 `User` 请求体。 | E002 |
| 区块链客户端存储 API | 使用包括 `getAllClients()`, `addClient(...)`, 和 `getClient(...)` 在内的合约调用。 | E001, E004 |
| Ethereum 连接 API | 使用基于 `HttpService(url)` 的 Web3j 连接到 Ethereum 节点。 | E001 |
| LwM2M 节点 JSON 反序列化 | 接受 JSON 并将其转换为 `LwM2mNode` 结构。 | E005, E006 |

### 通信接口

| 接口 | 协议/机制 | 证据 |
|---|---|---|
| 主后端 API | 通过 Spring 控制器映射进行 HTTP 请求/响应 | E002 |
| Ethereum 节点通信 | 基于 HTTP 的 Web3j `HttpService` | E001 |

### 数据交换格式

| 格式 | 描述 | 证据 |
|---|---|---|
| JSON `User` 负载 | 用于用户创建的请求体，以及用于已创建用户/列表检索的响应负载 | E002 |
| 区块链客户端/引导字段 | 传递给合约方法的 endpoint 以及引导/服务器 URL、ID 和密钥值 | E004 |
| LwM2M 节点 JSON | 具有诸如 `id` 和 `instances` 等字段的对象形式；原始值可映射到 BOOLEAN、STRING、INTEGER 或浮点类型 | E005, E006 |

## 4. 功能需求

| ID | 需求 | 触发器/输入 | 系统行为 | 输出 | 优先级 | 验证 | 来源证据 |
|---|---|---|---|---|---|---|---|
| FR-001 | 系统应提供经过身份验证的用户检索操作。 | 带有 `Authorization` 头的、发往用户检索端点的 HTTP 请求。 | 系统应使用 `JwtUtility.isValidToken(auth, 1)` 验证令牌。如果验证结果为 `0`，则应返回所有用户。如果结果为 `1`，则应以未授权拒绝该请求。如果结果为 `2`，则应以禁止访问拒绝该请求。否则，应返回错误请求。 | HTTP `200 OK` 和用户列表，或 `401 Unauthorized`、`403 Forbidden`、或 `400 Bad Request`。 | 高 | 测试 | E002 |
| FR-002 | 系统应提供经过身份验证的用户创建操作。 | 带有 `Authorization` 头和 `User` 请求体的 `POST /add` 请求。 | 系统应使用 `JwtUtility.isValidToken(auth, 1)` 验证令牌。如果验证结果为 `0`，则应通过用户服务添加用户。如果结果为 `1`，则应以未授权拒绝该请求。如果结果为 `2`，则应以禁止访问拒绝该请求。否则，应返回错误请求。 | HTTP `201 Created` 和已创建用户负载，或 `401 Unauthorized`、`403 Forbidden`、或 `400 Bad Request`。 | 高 | 测试 | E002 |
| FR-003 | 系统应检索基于区块链的客户端/安全信息。 | 检索所有已存储客户端/安全条目的请求。 | 系统应调用区块链合约方法 `getAllClients().send()`，将返回的元组集合转换为安全信息对象，并返回该集合。 | 安全信息记录集合。 | 高 | 测试 | E001 |
| FR-004 | 系统应将客户端引导数据提交到区块链合约。 | 包含 endpoint、引导服务器 URL/ID/密钥 和 服务器 URL/ID/密钥 的客户端引导数据。 | 系统应将提供的字符串字段转换为字节数组表示，并使用这些值调用合约方法 `addClient(...)`。 | 添加操作的区块链交易回执。 | 高 | 演示 | E004 |
| FR-005 | 系统应按 endpoint 从区块链合约中检索客户端的引导配置。 | 客户端 endpoint 标识符。 | 系统应使用转换为合约输入格式的 endpoint 调用合约方法 `getClient(...)`，并根据响应构造 `BootstrapConfig`。 | 与该 endpoint 关联的引导配置。 | 高 | 测试 | E004 |

## 5. 非功能需求

| ID | 需求 | 质量属性 | 度量 / 条件 | 优先级 | 验证 | 证据类型 | 来源证据 |
|---|---|---|---|---|---|---|---|
| NFR-001 | 用户管理端点在执行用户检索或创建之前应强制实施基于令牌的访问控制。 | 安全性 | 没有有效令牌的请求不得执行受保护操作，并应根据验证结果返回 `401`、`403` 或 `400`。 | 高 | 测试 | explicit | E002 |
| NFR-002 | 区块链集成应兼容可通过 HTTP 经由 Web3j 访问的 Ethereum 节点。 | 兼容性 | 区块链连接应使用通过 `HttpService(url)` 构建的 Web3j。 | 中 | 检查 | explicit | E001 |
| NFR-003 | LwM2M 节点 JSON 处理应拒绝结构无效的节点负载，而不是静默接受它们。 | 数据完整性 | 无效的节点元素，以及缺少 `id` 的 `instances` 对象，应导致 `JsonParseException`。 | 中 | 测试 | explicit | E005, E006 |

## 6. 数据需求

| ID | 数据项 | 需求 | 来源证据 |
|---|---|---|---|
| DR-001 | 用户负载 | 系统应接受 `User` 对象作为用户创建的请求体，并在成功响应中返回用户数据。 | E002 |
| DR-002 | 客户端/引导合约负载 | 系统应使用 endpoint、引导服务器 URL、引导 ID、引导密钥、服务器 URL、服务器 ID 和服务器密钥字段来表示客户端引导数据。 | E004 |
| DR-003 | 区块链客户端/安全集合 | 系统应处理以元组集合形式返回的区块链检索结果，并将其转换为安全信息对象。 | E001 |
| DR-004 | LwM2M 节点 JSON | 系统应接受可选带有 `id` 的节点 JSON 对象；当存在 `instances` 时，`id` 为必需。 | E006 |
| DR-005 | LwM2M 原始类型映射 | 系统应根据 JSON 值的种类，将 JSON 原始值映射到 Leshan 资源类型 BOOLEAN、STRING、INTEGER 或浮点类型。 | E005 |

## 7. 约束

| ID | 约束 | 类型 | 来源证据 |
|---|---|---|---|
| C-001 | 受保护的用户操作依赖于使用 `JwtUtility.isValidToken(auth, 1)` 进行 JWT 令牌验证。 | 安全/运行 | E002 |
| C-002 | 区块链连接使用 Web3j 通过 HTTP 传输连接到 Ethereum 节点。 | 技术/平台 | E001 |
| C-003 | 区块链操作依赖于包括 `getAllClients`、`addClient` 和 `getClient` 在内的智能合约方法；其中一个被引用的合约名称是 `BootstrapStore`。 | 集成 | E001, E003, E004 |
| C-004 | LwM2M JSON 数据处理依赖于 Leshan 节点/资源模型类型。 | 技术/数据模型 | E005, E006 |

## 8. 验证与验收

| Requirement ID | Verification method | Acceptance criterion |
|---|---|---|
| FR-001 | 测试 | 经过身份验证的有效请求返回带有用户列表的 `200`；无效令牌状态按定义返回 `401`、`403` 或 `400`。 |
| FR-002 | 测试 | 带有有效令牌和 `User` 请求体的 `POST /add` 返回 `201` 和已创建用户；无效令牌状态返回 `401`、`403` 或 `400`。 |
| FR-003 | 测试 | 检索请求会使用合约 `getAllClients().send()`，并返回转换后的安全信息记录。 |
| FR-004 | 演示 | 提供 endpoint 和引导/服务器字段会导致调用合约 `addClient(...)` 并返回交易回执。 |
| FR-005 | 测试 | 提供 endpoint 会导致调用合约 `getClient(...)` 并返回 `BootstrapConfig`。 |
| NFR-001 | 测试 | 当令牌验证失败时，受保护操作不会执行，并返回相应的 HTTP 状态。 |
| NFR-002 | 检查 | 区块链连接逻辑使用 Web3j `HttpService(url)` 构建客户端。 |
| NFR-003 | 测试 | 无效的节点 JSON 和不带 `id` 的 `instances` 负载会引发 `JsonParseException`。 |

## 9. 可追溯性矩阵

| ID | Requirement | Type | Source | Evidence Type | Verification | Confidence |
|---|---|---|---|---|---|---|
| FR-001 | 具有已定义 HTTP 状态结果的已认证用户检索 | Functional | E002 | explicit | Test | High |
| FR-002 | 在 `POST /add` 上具有已定义 HTTP 状态结果的已认证用户创建 | Functional | E002 | explicit | Test | High |
| FR-003 | 检索所有基于区块链的客户端/安全条目 | Functional | E001 | explicit | Test | Medium |
| FR-004 | 向区块链合约提交客户端引导数据 | Functional | E004 | explicit | Demonstration | Medium |
| FR-005 | 按 endpoint 从区块链中检索引导配置 | Functional | E004 | explicit | Test | Medium |
| NFR-001 | 受保护用户端点上的基于令牌的访问控制 | Non-functional | E002 | explicit | Test | High |
| NFR-002 | Ethereum HTTP/Web3j 兼容性 | Non-functional | E001 | explicit | Inspection | High |
| NFR-003 | 拒绝无效的 LwM2M 节点 JSON | Non-functional | E005, E006 | explicit | Test | High |
| DR-001 | 用户请求/响应负载处理 | Data | E002 | explicit | Inspection | High |
| DR-002 | 客户端/引导合约字段集 | Data | E004 | explicit | Inspection | Medium |
| DR-003 | 元组到安全信息的转换 | Data | E001 | explicit | Inspection | Medium |
| DR-004 | LwM2M 节点 JSON 结构规则 | Data | E006 | explicit | Inspection | High |
| DR-005 | LwM2M 节点值的原始类型映射 | Data | E005 | explicit | Inspection | High |
| C-001 | JWT 验证依赖 | Constraint | E002 | explicit | Inspection | High |
| C-002 | Web3j HTTP Ethereum 依赖 | Constraint | E001 | explicit | Inspection | High |
| C-003 | 包括 `BootstrapStore` 在内的智能合约方法依赖 | Constraint | E001, E003, E004 | explicit | Inspection | Medium |
| C-004 | Leshan 节点/资源模型依赖 | Constraint | E005, E006 | explicit | Inspection | High |
