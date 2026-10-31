# 软件需求规格说明书（SRS）

## 1. 引言

### 1.1 目的
本 SRS 定义了在提交 `22d15b1895af3c813fb7c2490f68158670108d8c` 时，由 Turing API 及相关运行时组件所公开的、基于证据支持的仓库特定能力需求。

### 1.2 产品范围
基于仓库证据，Turing 提供：
- 面向 Turing 资源的 HTTP API，包括 router 和 ensembler，
- 面向集群的组件，用于在 Kubernetes 中创建、更新和删除 Turing router 部署，
- 用于用户自定义 ensembler 的 PyFuncEnsembler webservice 运行时。

本 SRS 仅限于证据包直接支持的行为和约束。

### 1.3 目标读者
- Turing 的产品负责人和维护者
- 与 Turing 端点集成的 API 使用者
- QA 和验证工程师
- 在基于 Kubernetes 的环境中运行 Turing 的部署与平台工程师

### 1.4 参考资料
- 仓库：`caraml-dev/turing`
- 仓库 URL：https://github.com/caraml-dev/turing
- 提交：`22d15b1895af3c813fb7c2490f68158670108d8c`
- 证据来源：
  - `api/api/specs/routers.yaml` (`E003`)
  - `api/api/specs/ensemblers.yaml` (`E005`, `E006`)
  - `api/README.md` (`E004`)
  - `engines/router/README.md` (`E002`)
  - `engines/pyfunc-ensembler-service/README.md` (`E001`)

## 2. 总体描述

### 2.1 产品视角
Turing 是一个 API 驱动的系统，具有：
- 由 OpenAPI 规范定义的 HTTP 处理程序和路由，
- 用于在 Kubernetes 中管理 Turing router 部署生命周期的服务和集群包，
- 与 Turing router 配合使用的独立 PyFuncEnsembler 服务，
- 用于授权和请求验证的中间件。

### 2.2 产品功能概述
根据证据支持，该产品提供：
- 列出属于某个项目的 router，
- 按 ID 获取 ensembler 详情，
- 按 ID 删除 ensembler，
- 持久化并返回 ensembler 表示，
- 将用户定义的 ensembler 作为 webservice 暴露，
- 在 Kubernetes 集群中管理 router 部署生命周期。

### 2.3 用户类别
- 管理 Turing 资源（如 router 和 ensembler）的 API 客户端
- 在 Kubernetes 中部署或更新 Turing router 组件的平台运维人员
- 通过 PyFuncEnsembler 运行时部署用户自定义 ensembler 的用户

### 2.4 运行环境
- 基于 HTTP 的 API 服务器（`E004`, `E003`, `E005`, `E006`）
- 用于 router 部署生命周期管理的 Kubernetes 集群（`E004`）
- 用于 PyFuncEnsembler 服务的基于 Docker 的打包（`E001`）
- 作为 PyFuncEnsembler 服务本地镜像构建制品来源的 MLflow model registry（`E001`）

### 2.5 假设和依赖
- Turing API 行为通过 OpenAPI 规范定义（`E003`, `E005`, `E006`）
- Router 部署操作依赖于 Kubernetes 集群访问（`E004`）
- PyFuncEnsembler 镜像创建依赖于从 MLflow model registry 下载模型制品（`E001`）
- 请求追踪可与 Jaeger 集成（`E002`）

## 3. 外部接口需求

### 3.1 用户接口
| 接口 | 描述 | 来源 |
|---|---|---|
| HTTP API | 用于 router 和 ensembler 的 API 端点 | `E003`, `E005`, `E006` |
| PyFuncEnsembler webservice | 用户定义的 ensembler 可作为 webservice 运行 | `E001` |

### 3.2 软件/API 接口
| 接口 | 描述 | 来源 |
|---|---|---|
| OpenAPI 定义的 API | API 处理程序和路由在 OpenAPI 规范中定义 | `E004`, `E003`, `E005`, `E006` |
| Kubernetes 集群接口 | 用于创建、更新和删除 Turing router 部署 | `E004` |
| MLflow model registry | 本地 PyFuncEnsembler 镜像构建的模型制品来源 | `E001` |
| 授权和请求验证中间件 | HTTP 服务器中间件层 | `E004` |

### 3.3 通信接口
| 接口 | 描述 | 来源 |
|---|---|---|
| HTTP | API 端点通过 HTTP 暴露 | `E004`, `E003`, `E005`, `E006` |
| Application JSON 载荷 | 响应明确使用 `application/json` | `E005`, `E006` |

### 3.4 数据交换格式
| 格式 | 描述 | 来源 |
|---|---|---|
| JSON | Ensembler 响应为 JSON 表示 | `E005`, `E006` |
| 超时字符串 | 超时 schema 模式：`^[0-9]+(ms|s|m|h)$` | `E003` |

## 4. 功能需求

| ID | 描述 | 触发器/输入 | 系统行为 | 输出 | 优先级 | 验证 | 来源证据 |
|---|---|---|---|---|---|---|---|
| FR-001 | 列出某个项目的 router | 带有项目 ID 路径参数的 HTTP `GET /projects/{project_id}/routers` | 系统应提供一个端点，列出属于指定项目的 router。 | 给定项目的 router 列表响应 | 高 | 测试 | `E003` |
| FR-002 | 按 ID 获取 ensembler 详情 | 带有项目 ID 和 ensembler ID 的 HTTP `GET /projects/{project_id}/ensemblers/{ensembler_id}` | 系统应返回指定 ensembler 的详情。 | 带有 `Ensembler` 的 `application/json` 表示的 `200` 响应 | 高 | 测试 | `E005` |
| FR-003 | 按 ID 删除 ensembler | 带有项目 ID 和 ensembler ID 的 HTTP `DELETE /projects/{project_id}/ensemblers/{ensembler_id}` | 系统应删除指定 ensembler 并报告结果。 | 成功时，返回带有 JSON `EnsemblerId` 的 `200`；失败时，返回已文档化的错误响应，包括 `400`、`404` 或 `500` | 高 | 测试 | `E006` |
| FR-004 | 将用户定义的 ensembler 作为 webservice 暴露 | 针对 PyFuncEnsemblerRunner 的部署/运行请求 | 系统应支持将用户定义的 ensembler 作为 webservice 运行，以供 Turing router 使用。 | 可访问的 ensembler webservice | 中 | 演示 | `E001` |
| FR-005 | 在 Kubernetes 中管理 Turing router 部署 | 创建、更新或删除部署操作 | 系统应提供面向集群的功能，用于在 Kubernetes 集群中创建、更新和删除 Turing router 部署。 | Router 部署生命周期操作结果 | 高 | 演示 | `E004` |

## 5. 非功能需求

| ID | 质量属性 | 需求 | 优先级 | 验证 | 来源证据 | 证据类型 |
|---|---|---|---|---|---|---|
| NFR-001 | 安全性 | API 应支持用于 HTTP 请求的授权和请求验证中间件。 | 高 | 检查 | `E004` | explicit |
| NFR-002 | 可观测性 | Router 组件应支持通过 Jaeger 客户端初始化对请求进行追踪。 | 中 | 演示 | `E002` | explicit |
| NFR-003 | 可配置性 | Router 用户容器应默认使用端口 `8080`，并允许对此端口进行配置。 | 中 | 测试 | `E002` | explicit |
| NFR-004 | 互操作性 | API 规范应符合 OpenAPI `3.0.3`，适用于已文档化的端点和 schema。 | 中 | 检查 | `E003` | explicit |

## 6. 数据需求

### 6.1 数据实体或对象
| 实体/对象 | 描述 | 来源 |
|---|---|---|
| Router | 在项目下列出的资源 | `E003` |
| Ensembler | 在 ensembler API 中以 JSON 返回的资源 | `E005`, `E006` |
| EnsemblerId | 表示已删除 ensembler ID 的 JSON 对象 | `E006` |
| Project ID | 用于限定 router 和 ensembler 范围的路径参数 | `E003`, `E005`, `E006` |
| Ensembler ID | 用于标识特定 ensembler 的路径参数 | `E005`, `E006` |
| Timeout | 受 `^[0-9]+(ms|s|m|h)$` 约束的字符串值 | `E003` |

### 6.2 输入/输出数据
| 数据 | 方向 | 需求 | 来源 |
|---|---|---|---|
| `project_id` | 输入 | 系统应接受项目 ID 作为项目范围 router 和 ensembler 操作的必需路径参数。 | `E003`, `E005`, `E006` |
| `ensembler_id` | 输入 | 系统应接受 ensembler ID 作为 ensembler 检索和删除操作的必需路径参数。 | `E005`, `E006` |
| `Ensembler` JSON | 输出 | 系统应在 ensembler 详情操作中以 `application/json` 返回一个 `Ensembler` 对象。 | `E005` |
| `EnsemblerId` JSON | 输出 | 系统应在成功删除后以 `application/json` 返回一个 `EnsemblerId` 对象。 | `E006` |

### 6.3 存储、完整性、隐私、保留、迁移
在提供的证据包中，没有仓库证据明确规定保留策略、隐私处理、持久性保证或迁移需求。

## 7. 约束

| ID | 约束 | 来源 |
|---|---|---|
| C-001 | API 受限于 OpenAPI 定义的端点和 schema，包括 OpenAPI 版本 `3.0.3`。 | `E003`, `E004` |
| C-002 | Router 部署生命周期管理受限于 Kubernetes 集群环境。 | `E004` |
| C-003 | PyFuncEnsembler 服务的本地 Docker 镜像构建要求预先从 MLflow model registry 下载模型制品。 | `E001` |
| C-004 | Router 用户容器默认使用端口 `8080`，除非另有配置。 | `E002` |

## 8. 验证与验收

| Requirement ID | Verification Method | Acceptance Basis |
|---|---|---|
| FR-001 | 测试 | 调用 `GET /projects/{project_id}/routers` 会返回指定项目的 router。 |
| FR-002 | 测试 | 调用 `GET /projects/{project_id}/ensemblers/{ensembler_id}` 会返回 `200` 和一个 `Ensembler` JSON 响应体。 |
| FR-003 | 测试 | 调用 `DELETE /projects/{project_id}/ensemblers/{ensembler_id}` 会返回已文档化的成功或错误响应。 |
| FR-004 | 演示 | 用户定义的 ensembler 可以作为 webservice 运行，以供 Turing router 使用。 |
| FR-005 | 演示 | 系统可以在 Kubernetes 中对 router 部署执行创建、更新和删除操作。 |
| NFR-001 | 检查 | API 服务器中存在对授权和请求验证中间件的支持。 |
| NFR-002 | 演示 | 在 router 组件中可以通过 Jaeger 集成生成请求追踪。 |
| NFR-003 | 测试 | Router 容器默认监听端口 `8080`，并且可以配置为使用其他端口。 |
| NFR-004 | 检查 | API 规范声明了 OpenAPI `3.0.3`。 |

## 9. 可追溯性矩阵

| ID | 需求 | 类型 | 来源 | 证据类型 | 验证 | 置信度 |
|---|---|---|---|---|---|---|
| FR-001 | 列出某个项目的 router | 功能 | `E003` | explicit | 测试 | 高 |
| FR-002 | 按 ID 获取 ensembler 详情 | 功能 | `E005` | explicit | 测试 | 高 |
| FR-003 | 按 ID 删除 ensembler | 功能 | `E006` | explicit | 测试 | 高 |
| FR-004 | 将用户定义的 ensembler 作为 webservice 暴露 | 功能 | `E001` | explicit | 演示 | 中 |
| FR-005 | 在 Kubernetes 中管理 Turing router 部署 | 功能 | `E004` | explicit | 演示 | 中 |
| NFR-001 | 支持授权和请求验证中间件 | 非功能 | `E004` | explicit | 检查 | 中 |
| NFR-002 | 支持基于 Jaeger 的请求追踪 | 非功能 | `E002` | explicit | 演示 | 中 |
| NFR-003 | 默认使用端口 8080 且可配置 | 非功能 | `E002` | explicit | 测试 | 高 |
| NFR-004 | API 文档符合 OpenAPI 3.0.3 | 非功能 | `E003` | explicit | 检查 | 高 |
