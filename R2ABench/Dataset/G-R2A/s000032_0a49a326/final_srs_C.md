# 软件需求规格说明书（SRS）

Repository: Activiti/activiti-7-developers-guide  
Commit: `a500e1f1b3a6786ef017d510fdba4728e045c712`

## 1. 引言

### 1.1 目的
本 SRS 为 Activiti 7 开发者指南仓库内容定义了基于证据的需求，这些内容展示了基于 Activiti 的示例中的认证、流程交互、任务交互、审计观察以及云部署/访问模式。

### 1.2 产品范围
该仓库为以下内容提供面向开发者的示例和部署指导：
- 获取用于访问用户端点的认证令牌，
- 与流程和任务运行时 API 交互，
- 启动流程实例并观察审计事件，
- 通过 ingress 将服务暴露到 Kubernetes 集群外部，
- 配置安全角色以及对齐的平台依赖项。

### 1.3 预期受众
- 使用 Activiti 7 示例的开发者
- 连接到运行时或任务 API 的集成人员
- 将示例服务部署到 Kubernetes/GKE 的运维人员
- 验证仓库行为和约束的审查人员

### 1.4 参考资料
- Repository: https://github.com/Activiti/activiti-7-developers-guide
- Snapshot: https://github.com/Activiti/activiti-7-developers-guide/tree/a500e1f1b3a6786ef017d510fdba4728e045c712
- 证据来源：
  - `getting-started/getting-started-activiti-cloud/README.md` (E001)
  - `getting-started/getting-started-activiti-core.md` (E002, E003)
  - `getting-started/getting-started-activiti-cloud/google-cloud-gke.md` (E004)
  - `releases/7-ea201712.md` (E005)
  - `releases/7-ea201802.md` (E006)

## 2. 总体描述

### 2.1 产品视角
该仓库是 Activiti 7 在核心和面向云场景中使用的开发者指南与示例集合。它依赖外部身份、认证安全、运行时、审计和 Kubernetes ingress 组件，而不是一个独立的终端用户应用程序。

### 2.2 产品功能概述
仓库中有证据支持的功能包括：
- 获取用于认证请求的 Keycloak 令牌，
- 在认证后访问用户端点，
- 查询示例运行时包中已部署的流程定义，
- 从 `SimpleProcess` 启动新的流程实例，
- 检查与流程活动相关的审计事件，
- 以具有所需角色的已登录用户身份与 `TaskRuntime` 交互，
- 在 GKE 上通过 NGINX ingress 对外暴露服务，
- 在部署描述符中控制输入速率和副本数量，以进行可扩展性实验。

### 2.3 用户类别
| 用户类别 | 描述 | 证据 |
|---|---|---|
| 已认证用户 | 使用令牌访问用户端点和运行时服务 | E001 |
| 任务 API 用户 | 与 `TaskRuntime` 交互，且必须具有 `ACTIVITI_USER` 角色 | E003 |
| 人工参与者 | 参与依赖人工交互的流程 | E002 |
| 集群/运维用户 | 通过 ingress 和公共 IP 配置将服务暴露到 Kubernetes 外部 | E004 |

### 2.4 运行环境
| 环境方面 | 需求上下文 | 证据 |
|---|---|---|
| Spring Boot 应用程序 | 安全和用户设置是在 Spring Boot 应用程序中描述的 | E003 |
| Spring Security | 角色、组和用户身份依赖于 Spring Security 模块 | E003 |
| Keycloak | 令牌获取用于认证后续请求 | E001 |
| Kubernetes / GKE | 服务从集群环境中对外暴露 | E004 |
| NGINX Ingress Controller | 用于创建从外部访问到内部服务的路由 | E004 |
| Spring Boot 2.0.0.RELEASE / Spring Cloud Finchley.M9 | 制品对齐约束 | E006 |

### 2.5 假设与依赖项
| 项目 | 描述 | 证据 |
|---|---|---|
| 时效性令牌 | 认证令牌会随时间自动失效，可能需要重新获取 | E001 |
| 外部访问依赖 | 与集群服务的外部交互依赖于 ingress 和公共 IP | E004 |
| 安全上下文依赖 | `TaskRuntime` 交互依赖于当前已登录用户上下文和所需角色 | E003 |
| 部署描述符依赖 | 可扩展性实验依赖于控制输入速率和副本数量的部署描述符 | E005 |

## 3. 外部接口需求

### 3.1 用户界面
没有直接证据表明存在图形用户界面需求。交互是通过开发者操作、请求以及集群管理步骤来描述的。

### 3.2 软件/API 接口
| 接口 | 描述 | 证据 |
|---|---|---|
| Keycloak 令牌获取 | 用户获取令牌以发起认证请求 | E001 |
| 用户端点 | 在获取令牌后可访问 | E001 |
| 流程定义端点 | 用于查看示例运行时包中已部署的流程定义 | E001 |
| 流程启动端点/API | 用于启动新的 `SimpleProcess` 实例 | E001 |
| 审计服务 | 用于检查与流程活动相关的事件 | E001 |
| `TaskRuntime` API | 要求已登录用户具有 `ACTIVITI_USER` 角色 | E003 |
| `ProcessRuntime` API | 在示例中与 `TaskRuntime` 一起使用 | E002 |

### 3.3 通信接口
| 接口 | 描述 | 证据 |
|---|---|---|
| 带授权的 REST | REST 授权设置当前已登录用户 | E003 |
| 通过 ingress 路由的外部访问 | NGINX ingress 创建从公共 IP 到内部服务的路由 | E004 |

### 3.4 数据交换格式
| 格式/对象 | 描述 | 证据 |
|---|---|---|
| 认证令牌 | 用于认证后续请求的令牌 | E001 |
| 部署描述符值 | 输入速率和副本数量通过部署描述符进行控制 | E005 |

## 4. 功能需求

| ID | 描述 | 触发器/输入 | 系统行为 | 输出 | 优先级 | 验证 | 来源证据 |
|---|---|---|---|---|---|---|---|
| FR-001 | 系统应在允许与用户端点交互之前要求提供 Keycloak 令牌。 | 用户请求访问用户端点。 | 系统应接受使用先前获取的令牌发起的已认证请求，并在令牌无效或过期时拒绝请求。 | 已授权的端点访问或未授权错误。 | 高 | 演示 | E001 |
| FR-002 | 系统应允许已认证用户查看 Example Runtime Bundle 中部署了哪些流程定义。 | 用于检查流程定义的已认证请求。 | 系统应返回该示例运行时包中已部署的流程定义。 | 流程定义列表。 | 高 | 演示 | E001 |
| FR-003 | 系统应允许已认证用户从 `SimpleProcess` 启动新的流程实例。 | 用于启动 `SimpleProcess` 的已认证请求。 | 系统应为 `SimpleProcess` 创建一个新的流程实例。 | 已启动流程实例的确认信息。 | 高 | 演示 | E001 |
| FR-004 | 系统应为与流程活动相关的事件提供审计可见性。 | 用户在流程活动后检查审计服务。 | 系统应暴露与相关流程实例/活动相关联的审计事件。 | 审计事件记录。 | 中 | 检查 | E001 |
| FR-005 | 系统应仅允许当前已登录且具有 `ACTIVITI_USER` (`ROLE_ACTIVITI_USER`) 角色的用户与 `TaskRuntime` API 交互。 | 用户调用 `TaskRuntime` API 操作。 | 系统应在允许任务 API 交互之前评估当前用户上下文和所需角色。 | 任务 API 访问被授予或被拒绝。 | 高 | 测试 | E003 |
| FR-006 | 系统应支持将 `ProcessRuntime` 和 `TaskRuntime` API 结合用于涉及人工参与者的流程示例。 | 执行完整示例流程。 | 系统应允许在示例流程中使用这两个运行时 API。 | 涉及运行时和任务交互的可执行流程。 | 中 | 演示 | E002 |
| FR-007 | 已部署的示例环境应支持通过 ingress controller 从外部访问选定的内部服务。 | 运维人员从集群外部暴露服务。 | 系统应通过已配置的 ingress 路由和公共 IP 暴露，将外部请求路由到内部服务。 | 可从外部访问的服务端点。 | 高 | 演示 | E004 |

## 5. 非功能需求

| ID | 需求 | 质量属性 | 优先级 | 验证 | 来源证据 |
|---|---|---|---|---|---|
| NFR-001 | 用于端点访问的认证令牌应具有时效性，并在其有效期结束后自动失效。 | 安全性 | 高 | 测试 | E001 |
| NFR-002 | 云连接器事务处理应支持相对于先前行为的性能提升。该需求在发布说明中提出，证据中未给出定量边界。 | 性能 | 中 | 分析 | E005 |
| NFR-003 | 示例部署应允许通过在部署描述符中配置数据输入速率和云组件副本数量来进行可扩展性实验。 | 可扩展性 | 中 | 检查 | E005 |
| NFR-004 | 仓库制品应保持与 Spring Boot `2.0.0.RELEASE` 和 Spring Cloud `Finchley.M9` 对齐。 | 兼容性 | 中 | 检查 | E006 |

## 6. 数据需求

| ID | 数据实体/对象 | 需求 | 来源证据 |
|---|---|---|---|
| DR-001 | 认证令牌 | 系统应使用从 Keycloak 获取的令牌来认证对用户端点的后续请求。 | E001 |
| DR-002 | 流程定义数据 | 系统应暴露 Example Runtime Bundle 中已部署流程定义的信息。 | E001 |
| DR-003 | 流程实例数据 | 当已认证用户提出请求时，系统应为 `SimpleProcess` 创建并暴露已启动的实例。 | E001 |
| DR-004 | 审计事件数据 | 系统应通过审计服务提供与流程活动相关的事件。 | E001 |
| DR-005 | 用户角色数据 | 系统应使用通过 Spring Security 管理的用户/组/角色信息，包括用于任务 API 访问的 `ACTIVITI_USER` / `ROLE_ACTIVITI_USER`。 | E003 |
| DR-006 | 部署描述符参数 | 系统应接受用于控制云组件数据输入速率和副本数量的部署描述符参数。 | E005 |

## 7. 约束

| ID | 约束 | 类型 | 来源证据 |
|---|---|---|---|
| C-001 | 安全、角色和组依赖于 Spring Boot 应用程序上下文中的 Spring Security 模块。 | 技术 | E003 |
| C-002 | `TaskRuntime` 访问要求 `ACTIVITI_USER` 角色 (`ROLE_ACTIVITI_USER`)。 | 访问控制 | E003 |
| C-003 | 外部集群访问依赖于配置 NGINX Ingress Controller 并获取公共 IP。 | 部署/网络 | E004 |
| C-004 | 制品对齐遵循 Spring Boot `2.0.0.RELEASE` 和 Spring Cloud `Finchley.M9`。 | 兼容性 | E006 |

## 8. 验证与验收

| Requirement ID | Verification method | Acceptance criterion |
|---|---|---|
| FR-001 | 演示 | 有效令牌可启用端点访问；过期/无效令牌将导致未授权访问。 |
| FR-002 | 演示 | 已认证请求返回示例运行时包中已部署的流程定义。 |
| FR-003 | 演示 | 已认证请求成功启动一个 `SimpleProcess` 实例。 |
| FR-004 | 检查 | 审计服务输出显示与已执行流程活动相关的事件。 |
| FR-005 | 测试 | 对于具有 `ROLE_ACTIVITI_USER` 的已登录用户，`TaskRuntime` 访问成功；否则被拒绝。 |
| FR-006 | 演示 | 文档化的完整示例使用 `ProcessRuntime` 和 `TaskRuntime` API 成功执行。 |
| FR-007 | 演示 | 在完成 ingress 设置后，选定的内部服务可通过对外暴露的路由/公共 IP 访问。 |
| NFR-001 | 测试 | 先前发出的令牌在过期/失效后变得不可用。 |
| NFR-002 | 分析 | 发布证据确认连接器事务处理已更改以提高性能。 |
| NFR-003 | 检查 | 部署描述符暴露可配置的输入速率和副本数量参数。 |
| NFR-004 | 检查 | 仓库制品/依赖引用保持与所述 Spring 版本对齐。 |

## 9. 可追溯性矩阵

| ID | 需求 | 类型 | 来源 | 证据类型 | 验证 | 置信度 |
|---|---|---|---|---|---|---|
| FR-001 | 要求用户端点访问提供 Keycloak 令牌 | Functional | E001 | explicit | 演示 | 高 |
| FR-002 | 查看已部署的流程定义 | Functional | E001 | explicit | 演示 | 高 |
| FR-003 | 启动 `SimpleProcess` 实例 | Functional | E001 | explicit | 演示 | 高 |
| FR-004 | 为流程事件提供审计可见性 | Functional | E001 | explicit | 检查 | 中 |
| FR-005 | 将 `TaskRuntime` 限制为具有 `ACTIVITI_USER` 角色的已登录用户 | Functional | E003 | explicit | 测试 | 高 |
| FR-006 | 支持将 `ProcessRuntime` 和 `TaskRuntime` 与人工参与者结合的示例 | Functional | E002 | explicit | 演示 | 中 |
| FR-007 | 通过 ingress 对外暴露服务 | Functional | E004 | explicit | 演示 | 高 |
| NFR-001 | 时效性令牌失效 | Non-functional | E001 | explicit | 测试 | 高 |
| NFR-002 | 改进的连接器事务性能 | Non-functional | E005 | explicit | 分析 | 中 |
| NFR-003 | 用于可扩展性实验的可配置输入速率和副本数量 | Non-functional | E005 | explicit | 检查 | 高 |
| NFR-004 | 使制品与 Spring Boot 2.0.0.RELEASE 和 Spring Cloud Finchley.M9 对齐 | Non-functional | E006 | explicit | 检查 | 高 |
| DR-001 | 对已认证请求使用 Keycloak 令牌 | Data | E001 | explicit | 检查 | 高 |
| DR-002 | 暴露流程定义数据 | Data | E001 | explicit | 检查 | 高 |
| DR-003 | 为 `SimpleProcess` 创建/处理流程实例数据 | Data | E001 | explicit | 检查 | 高 |
| DR-004 | 暴露审计事件数据 | Data | E001 | explicit | 检查 | 中 |
| DR-005 | 使用 Spring Security 角色/组/用户数据 | Data | E003 | explicit | 检查 | 高 |
| DR-006 | 接受部署描述符可扩展性参数 | Data | E005 | explicit | 检查 | 高 |
| C-001 | 在 Spring Boot 上下文中依赖 Spring Security | Constraint | E003 | explicit | 检查 | 高 |
| C-002 | `TaskRuntime` 要求 `ROLE_ACTIVITI_USER` | Constraint | E003 | explicit | 检查 | 高 |
| C-003 | 外部访问依赖 NGINX ingress 和公共 IP | Constraint | E004 | explicit | 检查 | 高 |
| C-004 | 将平台对齐约束为 Spring Boot / Spring Cloud 版本 | Constraint | E006 | explicit | 检查 | 高 |
