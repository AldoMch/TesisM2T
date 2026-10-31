# 软件需求规格说明书

## 1. 引言

### 目的
本 SRS 规定了以 Home Recipes 全栈应用为中心的仓库样本的、具有证据支持的需求。该应用由 Flutter/Dart 客户端、Go gRPC 服务器以及 gRPC-Gateway 中间件层组成。本文档仅基于所提供的仓库证据。

### 产品范围
证据所支持的产品范围是一个食谱应用技术栈，其：
- 为多个平台提供客户端应用，
- 使用从 Protocol Buffers 生成的代码将该客户端连接到 gRPC 服务器，
- 通过 gRPC-Gateway HTTP 接口公开选定的服务器能力，以及
- 支持服务器的本地容器化以用于部署/测试工作流。

### 目标读者
本文档面向：
- 实现或修改客户端、服务器或中间件的开发人员，
- 验证 API 和平台行为的测试人员，
- 在本地或 Docker 中运行服务器的运维人员/开发人员，
- 将仓库证据追溯到已声明需求的审查人员。

### 参考资料
- 仓库：`sm2774us/full_stack_interview_prep_2021`
- 提交：`3dcc2e6fb6c9998a0b458bfc1bb16c7aaa6c61e7`
- 证据来源：
  - `E001` 客户端 README
  - `E002` 服务器 README
  - `E003` 中间件 README

## 2. 总体描述

### 产品视角
有证据支持的产品是一个多组件系统：
- 一个 Flutter/Dart 客户端应用，
- 一个基于 Go 的、由 `.proto` 定义生成的 gRPC 服务器，
- 一个使用 gRPC-Gateway 通过 gRPC 服务公开 HTTP 端点的中间件组件。

### 产品功能概述
系统支持以下有证据支持的功能：
- 在 Android、iOS、Web 和 macOS 上运行 Home Recipes 客户端（`E001`）；
- 从 Protocol Buffers 定义生成客户端和服务器代码（`E001`, `E002`）；
- 运行 gRPC 服务器并将其打包为 Docker 镜像（`E002`）；
- 通过 HTTP 端点公开与食谱相关的操作，包括 `addRecipe`、`ListAllRecipes`、`ListAllIngredientsAtHome` 和 `GetAllIngredientsForRecipe`（`E003`）。

### 用户类别
- 终端用户：在受支持平台上与 Home Recipes 客户端应用交互的用户（`E001`）。
- API 使用者/测试人员：通过 `curl` 调用中间件端点的用户（`E003`）。
- 开发人员/运维人员：生成代码、运行服务器、运行中间件以及构建 Docker 镜像的用户（`E001`, `E002`, `E003`）。

### 运行环境
受支持且有证据支持的环境：
- 客户端平台：Android、iOS、Web、macOS（`E001`）
- 客户端工具链：Dart、protoc 插件、从 protos 生成的 Dart 代码（`E001`）
- 服务器工具链：Go、gRPC、`protoc`、`protoc-gen-go`（`E002`）
- 中间件工具链：gRPC-Gateway 生成流程和本地依赖项（`E003`）
- 容器运行时：用于服务器镜像构建/运行/推送工作流的 Docker（`E002`）

### 假设与依赖
- 客户端-服务器契约依赖于 Protocol Buffers 定义和生成的代码（`E001`, `E002`, `E003`）。
- 中间件执行依赖于服务器已按预期运行（`E003`）。
- 服务器容器化假定服务器可在本地运行且 Docker 可用（`E002`）。

## 3. 外部接口需求

| 接口领域 | 需求 |
|---|---|
| 用户界面 | 客户端应可作为应用在 Android、iOS、Web 和 macOS 上运行。来源：`E001` |
| 软件/API 接口 | 客户端应使用从 Protocol Buffers 定义生成的 Dart 代码连接到服务器。来源：`E001` |
| 软件/API 接口 | 服务器应使用 Go 工具链实现从 `.proto` 文件生成的 gRPC 服务。来源：`E002` |
| 软件/API 接口 | 中间件应为 `addRecipe`、`ListAllRecipes`、`ListAllIngredientsAtHome` 和 `GetAllIngredientsForRecipe` 公开可通过 HTTP 访问的端点。来源：`E003` |
| 通信接口 | 对中间件端点的 HTTP 请求应可通过 `curl` 调用。来源：`E003` |
| 通信接口 | 中间件应支持 gRPC-Gateway 对 `ListAllRecipes` 上服务器端流式传输的处理。来源：`E003` |
| 数据交换格式 | 服务契约应基于用于生成客户端、服务器和网关代码的 Protocol Buffers 定义。来源：`E001`, `E002`, `E003` |

## 4. 功能需求

| ID | 描述 | 触发器/输入 | 系统行为 | 输出 | 优先级 | 验证 | 来源证据 |
|---|---|---|---|---|---|---|---|
| FR-001 | 多平台客户端可用性 | 用户在受支持平台上启动 Home Recipes 客户端 | 系统应提供可在 Android、iOS、Web 和 macOS 上运行的客户端 | 在所选平台上运行的客户端应用 | 高 | 演示 | `E001` |
| FR-002 | 通过生成契约实现客户端-服务器集成 | 使用 `.proto` 定义进行客户端构建/集成 | 系统应从 Protocol Buffers 定义生成 Dart 客户端代码，并使用其实现连接到服务器的客户端逻辑 | 基于生成的 Dart 代码的客户端集成层 | 高 | 检查 | `E001` |
| FR-003 | gRPC 服务器实现 | 开发人员根据 `.proto` 定义创建并运行服务器 | 系统应从 `.proto` 定义生成 Go gRPC 代码并提供可运行的服务器实现 | 正在运行的 gRPC 服务器 | 高 | 演示 | `E002` |
| FR-004 | 服务器容器化 | 运维人员构建并运行服务器镜像 | 系统应支持将服务器打包为可在本地运行的 Docker 镜像 | Docker 镜像和可在本地运行的容器化服务器 | 中 | 演示 | `E002` |
| FR-005 | 用于添加食谱的 HTTP 网关 | 对 `addRecipe` 的 HTTP 请求 | 中间件应将该 HTTP 请求转换为相应的后端 gRPC 操作 | 来自 `addRecipe` 端点的 HTTP 响应 | 高 | 测试 | `E003` |
| FR-006 | 用于列出所有食谱的 HTTP 网关 | 对 `ListAllRecipes` 的 HTTP 请求 | 中间件应公开 `ListAllRecipes`，并通过 gRPC-Gateway 支持其服务器端流式传输行为 | 流式或经网关传递的食谱列表响应 | 高 | 测试 | `E003` |
| FR-007 | 用于列出家中所有食材的 HTTP 网关 | 对 `ListAllIngredientsAtHome` 的 HTTP 请求 | 中间件应公开 `ListAllIngredientsAtHome`，并对该操作一次处理一条消息 | 包含单条消息对应家中食材数据的响应 | 中 | 测试 | `E003` |
| FR-008 | 用于获取食谱食材的 HTTP 网关 | 对 `GetAllIngredientsForRecipe` 的 HTTP 请求 | 中间件应公开 `GetAllIngredientsForRecipe`，并接受仅包含一个条目的请求 | 包含所请求食谱条目食材的响应 | 中 | 测试 | `E003` |

## 5. 非功能需求

| ID | 需求 | 质量属性 | 优先级 | 验证 | 证据 | 置信度 |
|---|---|---|---|---|---|---|
| NFR-001 | 客户端应可在 Android、iOS、Web 和 macOS 之间移植，而无需为每个平台定义不同的产品。 | 可移植性 | 高 | 演示 | `E001` | 明确 |
| NFR-002 | 当通过 gRPC-Gateway 公开时，中间件应为 `ListAllRecipes` 保持服务器端流式传输兼容性。 | 兼容性 | 高 | 测试 | `E003` | 明确 |
| NFR-003 | 服务器应可部署为可在本地运行的 Docker 容器镜像。 | 可部署性 | 中 | 演示 | `E002` | 明确 |
| NFR-004 | 系统接口应通过由 Protocol Buffers 为客户端、服务器和网关组件生成的代码保持契约驱动。 | 可维护性/兼容性 | 中 | 检查 | `E001`, `E002`, `E003` | 推断 |

## 6. 数据需求

| ID | 数据需求 | 类型 | 来源证据 | 置信度 |
|---|---|---|---|---|
| DR-001 | 系统应通过用于生成客户端、服务器和网关代码的 Protocol Buffers（`.proto`）文件交换服务定义。 | 数据契约 | `E001`, `E002`, `E003` | 明确 |
| DR-002 | 系统应支持通过名为 `addRecipe`、`ListAllRecipes` 和 `GetAllIngredientsForRecipe` 的操作交换与食谱相关的数据。 | 领域数据 | `E003` | 明确 |
| DR-003 | 系统应支持通过名为 `ListAllIngredientsAtHome` 和 `GetAllIngredientsForRecipe` 的操作交换与食材相关的数据。 | 领域数据 | `E003` | 明确 |
| DR-004 | `GetAllIngredientsForRecipe` 请求应仅包含一个条目。 | 输入约束 | `E003` | 明确 |
| DR-005 | `ListAllIngredientsAtHome` 应一次处理一条消息。 | 消息约束 | `E003` | 明确 |

## 7. 约束

| ID | 约束 | 来源证据 |
|---|---|---|
| C-001 | 客户端集成依赖于 Dart 安装、protoc 插件激活、PATH 配置，以及从 protos 生成的 Dart 代码。 | `E001` |
| C-002 | 服务器实现依赖于已安装 Go、gRPC、`protoc` 和 `protoc-gen-go`，并且它们在 PATH 中可用。 | `E002` |
| C-003 | 中间件生成依赖于在本地安装三个依赖项、在 `def` 下复制第三方库，以及向 proto 文件添加注解。 | `E003` |
| C-004 | 中间件运行时依赖于服务器已按预期运行。 | `E003` |
| C-005 | 服务器 Docker 推送工作流依赖于会话已执行 Docker 登录。 | `E002` |

## 8. 验证与验收

| Requirement ID | Verification Method | Acceptance Basis |
|---|---|---|
| FR-001 | 演示 | 客户端可在 Android、iOS、Web 和 macOS 上启动 |
| FR-002 | 检查 | 来自 proto 定义的生成 Dart 代码存在，并用于客户端-服务器连接 |
| FR-003 | 演示 | 生成的 Go 服务代码和可运行服务器可用 |
| FR-004 | 演示 | Docker 镜像可在本地构建并运行 |
| FR-005 | 测试 | 对 `addRecipe` 的 `curl` 调用返回有效的端点响应 |
| FR-006 | 测试 | 对 `ListAllRecipes` 的 `curl` 调用可通过网关成功执行并支持流式传输 |
| FR-007 | 测试 | 对 `ListAllIngredientsAtHome` 的 `curl` 调用成功，且具有一次一条消息的行为 |
| FR-008 | 测试 | `GetAllIngredientsForRecipe` 仅接受单条目请求并返回响应 |
| NFR-001 | 演示 | 相同客户端产品可在列出的全部四个平台上运行 |
| NFR-002 | 测试 | 网关行为为 `ListAllRecipes` 保持服务器端流式传输 |
| NFR-003 | 演示 | 容器化服务器可从 Docker 镜像在本地运行 |
| NFR-004 | 检查 | 各组件间的接口由共享 proto 契约生成 |

## 9. 追溯矩阵

| ID | 需求 | 类型 | 来源 | 证据类型 | 验证 | 置信度 |
|---|---|---|---|---|---|---|
| FR-001 | 客户端可在 Android、iOS、Web 和 macOS 上运行 | 功能 | `E001` | 明确 | 演示 | 高 |
| FR-002 | 客户端使用生成的 Dart proto 代码连接到服务器 | 功能 | `E001` | 明确 | 检查 | 高 |
| FR-003 | Go gRPC 服务器由 proto 生成且可运行 | 功能 | `E002` | 明确 | 演示 | 高 |
| FR-004 | 服务器可被打包并作为 Docker 镜像运行 | 功能 | `E002` | 明确 | 演示 | 高 |
| FR-005 | 中间件通过 HTTP 公开 `addRecipe` | 功能 | `E003` | 明确 | 测试 | 高 |
| FR-006 | 中间件公开支持流式传输的 `ListAllRecipes` | 功能 | `E003` | 明确 | 测试 | 高 |
| FR-007 | 中间件公开具有单消息处理的 `ListAllIngredientsAtHome` | 功能 | `E003` | 明确 | 测试 | 中 |
| FR-008 | 中间件公开具有单条目请求限制的 `GetAllIngredientsForRecipe` | 功能 | `E003` | 明确 | 测试 | 中 |
| NFR-001 | 客户端可在四个平台间移植 | 非功能 | `E001` | 明确 | 演示 | 高 |
| NFR-002 | 网关为 `ListAllRecipes` 保持流式传输兼容性 | 非功能 | `E003` | 明确 | 测试 | 高 |
| NFR-003 | 服务器可通过 Docker 在本地部署 | 非功能 | `E002` | 明确 | 演示 | 高 |
| NFR-004 | 接口通过 proto 生成保持契约驱动 | 非功能 | `E001`, `E002`, `E003` | 推断 | 检查 | 中 |
| DR-001 | Proto 文件定义跨组件的交换契约 | 数据 | `E001`, `E002`, `E003` | 明确 | 检查 | 高 |
| DR-002 | 食谱数据通过食谱端点交换 | 数据 | `E003` | 明确 | 检查 | 中 |
| DR-003 | 食材数据通过食材端点交换 | 数据 | `E003` | 明确 | 检查 | 中 |
| DR-004 | `GetAllIngredientsForRecipe` 请求包含一个条目 | 数据 | `E003` | 明确 | 测试 | 高 |
| DR-005 | `ListAllIngredientsAtHome` 一次处理一条消息 | 数据 | `E003` | 明确 | 测试 | 高 |
