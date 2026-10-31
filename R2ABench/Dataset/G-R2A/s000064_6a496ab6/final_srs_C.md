# 软件需求规格说明书

## 1. 引言

### 目的
本 SRS 定义了基于证据的软件需求，这些需求适用于 gran-book 后端及其相关基础设施，所依据的仓库提交为 `03ab97ccfe81bccbc8e000916a663cd6a2872bf6`。

### 产品范围
仓库证据描述了一个面向图书相关服务的后端平台，该平台由多个内部 API、移动端和 Web 客户端、GCP 上的云基础设施，以及与外部服务的集成组成，这些外部服务用于认证、图书搜索和支付。明确标识的后端支持域包括：
- 认证
- 用户管理
- 图书管理
- EC 站点
- 支持/消息管理上下文

### 目标读者
- 产品负责人
- 后端与基础设施工程师
- QA 工程师
- 前端客户端和外部服务的集成人员
- 部署与接口设计评审人员

### 参考资料
| Ref | Description |
|---|---|
| R1 | `docs/12_backend/01_design/README.md` |
| R2 | `docs/12_backend/12_protobuf/README.md` |
| R3 | `docs/12_backend/32_user_api/README.md` |
| R4 | `docs/14_infrastructure/01_design/README.md` |
| R5 | `docs/14_infrastructure/33_virtual_machine/README.md` |

## 2. 总体描述

### 产品视角
该产品是一个云托管后端，服务于：
- 面向 Google Play 和 App Store 的原生移动应用
- 单独托管的管理 Web 应用

后端架构包括：
- 使用 Firebase Authentication 的认证 API
- 运行于容器中的用户管理 API
- 运行于容器中的图书管理 API
- 运行于容器中的 EC 站点 API
- 按域拆分的数据存储
- 包括负载均衡和对象存储的 GCP 基础设施

### 产品功能概述
证据支持以下高级功能：
- 通过 Firebase Authentication 对用户进行认证
- 通过专用 API 管理与用户相关的数据
- 通过专用 API 管理与图书相关的数据
- 通过专用 API 支持 EC 站点操作
- 集成 Google Books API 以进行图书搜索
- 集成 Stripe 以进行支付相关处理

### 用户类别
| User class | Description | Evidence |
|---|---|---|
| End users | Google Play / App Store 上原生移动应用的用户 | E006 |
| Administrators | 管理 Web 应用的用户 | E006 |
| External service operators/integrators | 通过 Google Books API、Stripe 和 Firebase Authentication 交互的系统 | E004, E006 |

### 运行环境
| Area | Environment |
|---|---|
| Backend runtime | GCP/GKE 相关环境中的容器化服务 |
| Virtual machine operations | 具有 Cloud SDK 和 Let's Encrypt 工具的 GCE VM 配置 |
| Frontend clients | 原生移动应用和托管的 Web 管理控制台 |
| Datastores | Firebase Authentication、MySQL、NoSQL、对象存储 |

### 假设与依赖关系
| Item | Type | Basis |
|---|---|---|
| Firebase Authentication 是认证能力所必需的 | Dependency | E006 |
| Google Books API 是采用的外部图书搜索服务 | Dependency | E004, E006 |
| Stripe 是采用的支付服务 | Dependency | E004, E006 |
| 包括负载均衡和对象存储在内的 GCP 服务是目标基础设施的一部分 | Dependency | E006 |
| Protocol Buffers 文档规定了后端 API 方法命名约定 | 由设计参考支持的 Assumption | E003 |

## 3. 外部接口需求

### 用户界面
| Interface | Requirement basis |
|---|---|
| 原生移动应用 | 产品应服务于通过 Google Play 和 App Store 分发的原生应用客户端。证据将其标识为前端客户端。 |
| 管理 Web 应用 | 产品应服务于单独托管的基于 Web 的管理控制台。 |

### 软件/API 接口
| Interface | Description | Evidence |
|---|---|---|
| Firebase Authentication | 认证 API 依赖 | E006 |
| Google Books API | 用于图书搜索相关功能的外部服务 | E004, E006 |
| Stripe | 用于支付相关功能的外部服务 | E004, E006 |
| 内部后端 API | 已记录认证、用户管理、图书管理、EC 站点和面向支持的 API 划分 | E004 |

### 通信接口
| Interface | Description | Evidence |
|---|---|---|
| 负载均衡网络访问 | 基础设施包含一个 L7 负载均衡器 | E006 |
| GKE 凭证访问 | 运行环境使用 `gcloud container clusters get-credentials` 访问 GKE | E002 |

### 数据交换格式
| Format | Requirement basis |
|---|---|
| Protocol Buffers | 后端文档包含 Protocol Buffers 以及标准方法命名规则 |
| 请求/响应 API 设计工件 | 后端设计包含请求/响应设计文档 |

## 4. 功能需求

| ID | Description | Trigger/Input | System behavior | Output | Priority | Verification | Source evidence |
|---|---|---|---|---|---|---|---|
| FR-001 | 系统应提供使用 Firebase Authentication 的认证接口。 | 来自客户端应用的认证请求。 | 系统应使用 Firebase Authentication 作为用户认证的认证 API 组件。 | 通过认证接口返回认证结果。 | High | Inspection | E006 |
| FR-002 | 系统应提供与其他后端 API 分离的用户管理 API。 | 来自客户端或管理界面的用户管理请求。 | 系统应通过部署为容器化后端组件的专用用户管理 API 处理该请求。 | 用户管理响应。 | High | Inspection | E004, E006 |
| FR-003 | 系统应提供与其他后端 API 分离的图书管理 API。 | 来自客户端或管理界面的图书管理请求。 | 系统应通过部署为容器化后端组件的专用图书管理 API 处理该请求。 | 图书管理响应。 | High | Inspection | E004, E006 |
| FR-004 | 系统应提供与其他后端 API 分离的 EC 站点 API。 | 来自客户端或管理界面的 EC 站点相关请求。 | 系统应通过部署为容器化后端组件的专用 EC 站点 API 处理该请求。 | EC 站点相关响应。 | High | Inspection | E004, E006 |
| FR-005 | 系统应集成 Google Books API 以支持图书搜索相关功能。 | 需要外部图书信息的图书搜索请求。 | 系统应使用 Google Books API 作为采用的外部图书搜索服务。 | 将获取到的图书搜索数据返回给请求组件。 | High | Inspection | E004, E006 |
| FR-006 | 系统应集成 Stripe 以支持支付相关功能。 | 来自 EC 站点流程的支付相关请求。 | 系统应使用 Stripe 作为采用的支付相关外部 API。 | 将支付处理结果返回给请求组件。 | High | Inspection | E004, E006 |

## 5. 非功能需求

| ID | Quality | Requirement | Priority | Verification | Source evidence | Evidence type |
|---|---|---|---|---|---|---|
| NFR-001 | 可移植性/可部署性 | 用户管理、图书管理和 EC 站点后端服务应可作为基于容器的组件部署到目标基础设施中。 | High | Inspection | E006 | explicit |
| NFR-002 | 安全性 | 部署环境应支持在 VM 环境中使用 Let's Encrypt 和 DNS-01 挑战流程进行 TLS 证书配置。 | Medium | Inspection | E002 | explicit |
| NFR-003 | 兼容性 | 后端 API 定义应遵循已记录的 Protocol Buffers 标准方法命名规则，以保持接口一致性。 | Medium | Inspection | E003 | explicit |

## 6. 数据需求

| ID | Data requirement | Type | Source evidence | Verification |
|---|---|---|---|---|
| DR-001 | 认证数据应通过 Firebase Authentication 进行管理。 | Data storage/integration | E006 | Inspection |
| DR-002 | 用户管理数据应存储在 MySQL 中。 | Data storage | E006 | Inspection |
| DR-003 | 图书管理数据应存储在 MySQL 中。 | Data storage | E006 | Inspection |
| DR-004 | EC 站点数据应存储在 MySQL 中。 | Data storage | E006 | Inspection |
| DR-005 | 消息管理数据应存储在 NoSQL 中。 | Data storage | E006 | Inspection |
| DR-006 | 缩略图数据应存储在对象存储中。 | Data storage | E006 | Inspection |
| DR-007 | 后端接口应在已定义之处使用已记录的请求/响应设计工件和与 Protocol Buffers 相关的 API 约定。 | Input/output format | E003, E004 | Inspection |

## 7. 约束

| ID | Constraint | Source evidence |
|---|---|---|
| C-001 | User API 文档将 Golang 标识为该后端领域的实现语言。 | E001 |
| C-002 | 目标云环境是 GCP，并包括 GKE/GCE 运行流程。 | E002, E006 |
| C-003 | 认证依赖 Firebase Authentication，而不是仓库中定义的独立认证存储。 | E006 |
| C-004 | 已记录设计中采用的外部集成是 Google Books API 和 Stripe。 | E004, E006 |
| C-005 | 证据表明，前端消费者仅限于原生移动应用和管理 Web 应用。 | E006 |

## 8. 验证与验收

| Requirement ID | Verification method | Acceptance basis |
|---|---|---|
| FR-001 | Inspection | 架构和接口定义显示 Firebase Authentication 作为认证接口。 |
| FR-002 | Inspection | 架构/设计文档显示专用的用户管理 API 被部署为容器。 |
| FR-003 | Inspection | 架构/设计文档显示专用的图书管理 API 被部署为容器。 |
| FR-004 | Inspection | 架构/设计文档显示专用的 EC 站点 API 被部署为容器。 |
| FR-005 | Inspection | 设计文档将 Google Books API 标识为采用的图书搜索集成。 |
| FR-006 | Inspection | 设计文档将 Stripe 标识为采用的支付集成。 |
| NFR-001 | Inspection | 基础设施设计显示相关后端 API 采用基于容器的部署。 |
| NFR-002 | Inspection | VM 运维文档显示了使用 DNS-01 hooks 的 Let's Encrypt 证书配置步骤。 |
| NFR-003 | Inspection | Protocol Buffers 文档定义了 API 的标准方法命名规则。 |
| DR-001 to DR-006 | Inspection | 架构文档将每个域映射到其声明的数据存储或存储服务。 |
| DR-007 | Inspection | 后端设计引用了请求/响应设计和 Protocol Buffers 约定。 |
| C-001 to C-005 | Inspection | 约束声明均由仓库文档直接支持。 |

## 9. 可追溯性矩阵

| ID | Requirement | Type | Source | Evidence Type | Verification | Confidence |
|---|---|---|---|---|---|---|
| FR-001 | 使用 Firebase Authentication 提供认证接口 | Functional | E006 | explicit | Inspection | High |
| FR-002 | 提供专用用户管理 API | Functional | E004, E006 | explicit | Inspection | High |
| FR-003 | 提供专用图书管理 API | Functional | E004, E006 | explicit | Inspection | High |
| FR-004 | 提供专用 EC 站点 API | Functional | E004, E006 | explicit | Inspection | High |
| FR-005 | 集成 Google Books API 以进行图书搜索 | Functional | E004, E006 | explicit | Inspection | High |
| FR-006 | 集成 Stripe 以支持支付相关功能 | Functional | E004, E006 | explicit | Inspection | High |
| NFR-001 | 核心后端服务的基于容器的可部署性 | Non-functional | E006 | explicit | Inspection | High |
| NFR-002 | 通过 Let's Encrypt DNS-01 流程支持 TLS 证书配置 | Non-functional | E002 | explicit | Inspection | Medium |
| NFR-003 | Protocol Buffers 标准方法命名一致性 | Non-functional | E003 | explicit | Inspection | Medium |
| DR-001 | 认证数据由 Firebase Authentication 管理 | Data | E006 | explicit | Inspection | High |
| DR-002 | 用户管理数据存储于 MySQL | Data | E006 | explicit | Inspection | High |
| DR-003 | 图书管理数据存储于 MySQL | Data | E006 | explicit | Inspection | High |
| DR-004 | EC 站点数据存储于 MySQL | Data | E006 | explicit | Inspection | High |
| DR-005 | 消息管理数据存储于 NoSQL | Data | E006 | explicit | Inspection | Medium |
| DR-006 | 缩略图数据存储于对象存储 | Data | E006 | explicit | Inspection | High |
| DR-007 | 请求/响应遵循已记录的 API 和 Protocol Buffers 约定 | Data | E003, E004 | explicit | Inspection | Medium |
| C-001 | User API 使用 Golang | Constraint | E001 | explicit | Inspection | High |
| C-002 | GCP/GKE/GCE 目标环境 | Constraint | E002, E006 | explicit | Inspection | High |
| C-003 | 认证依赖 Firebase Authentication | Constraint | E006 | explicit | Inspection | High |
| C-004 | 外部集成是 Google Books API 和 Stripe | Constraint | E004, E006 | explicit | Inspection | High |
| C-005 | 支持的前端消费者是原生移动应用和管理 Web 应用 | Constraint | E006 | explicit | Inspection | High |
