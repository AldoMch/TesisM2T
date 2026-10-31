# 软件需求规格说明书

## 1. 引言

### 目的
本 SRS 定义了针对仓库组件在提交 `27cf7dd67f8c6f17aedf02fde961cd4066af524b` 时基于证据的需求，重点关注 ClearML agent 运行时、其面向 Kubernetes 的执行流程、worker 遥测行为以及暴露的后端服务接口。

### 产品范围
根据现有证据，产品支持：
- 通过与 Kubernetes 相关的集成模式运行 ClearML 作业，
- 在 pod 内安装实验环境并在 Docker 中运行用户代码，
- 定期进行 worker 上报和连通性检查，
- 用于实体创建/获取以及选定 events/models 数据结构的后端服务交互。

### 目标读者
- 产品和需求负责人
- `allegroai/clearml-agent` 的维护者
- 在 Kubernetes 环境中部署 agent 的集成方
- 测试与验证工程师

### 参考资料
- 仓库：`allegroai/clearml-agent`
- 仓库 URL：https://github.com/allegroai/clearml-agent
- 提交：`27cf7dd67f8c6f17aedf02fde961cd4066af524b`
- 证据来源：
  - `README.md` (`E001`)
  - `clearml_agent/backend_api/config/default/sdk.conf` (`E002`)
  - `clearml_agent/backend_api/session/client/client.py` (`E003`)
  - `clearml_agent/backend_api/services/v2_5/events.py` (`E004`)
  - `clearml_agent/backend_api/services/v2_4/models.py` (`E005`, `E006`)

## 2. 总体描述

### 产品视角
该仓库提供了一个面向 agent 的组件，用于与 ClearML 后端服务集成，并支持基于 Kubernetes 的作业执行流程。证据显示，README 中有两种集成形式：长期运行的服务 pod，以及一种 Kubernetes Glue 模式，该模式使用 YAML 模板将排队作业转换为 Kubernetes 作业（`E001`）。

### 产品功能概述
- 使用 `clearml-agent` Docker 镜像作为长期运行的服务 pod（`E001`）
- 在该模式下通过映射的 Docker socket 管理同级 Docker 容器（`E001`）
- 从 ClearML 作业执行队列中拉取作业，并根据提供的 YAML 模板准备 Kubernetes 作业（`E001`）
- 在 pod 内安装作业/实验环境，并为用户代码启动和监控 Docker 执行（`E001`）
- 定期上报 worker 状态并 ping 服务器（`E002`）
- 可选地记录执行中的 stdout 和 stderr（`E002`）
- 暴露用于 `create`、`get`、`get_all`、`get_all_ex` 风格服务访问的后端客户端操作（`E003`）

### 用户类别
- 部署 agent 或 Kubernetes Glue 集成的 Kubernetes 平台运维人员（`E001`）
- 向该集成所消费的执行队列提交作业的 ClearML 用户（`E001`）
- 使用后端服务客户端抽象的开发者或集成方（`E003`）

### 运行环境
- 具有 pods 和 Kubernetes 作业的 Kubernetes 集群环境（`E001`）
- 基于 Docker 的执行环境，包括通过映射的 Docker socket 管理同级容器（`E001`）
- 与 ClearML 服务器/后端的连通性，用于状态上报、ping 和服务请求（`E002`, `E003`）

### 假设与依赖
- Kubernetes Glue 的运行依赖于用于准备 Kubernetes 作业的已提供 YAML 模板（`E001`）
- 长期运行的服务 pod 模式依赖于 `clearml-agent` Docker 镜像以及映射的 Docker socket 访问（`E001`）
- Worker 遥测依赖于与被 ping 服务器的连通性（`E002`）
- 服务操作依赖于后端 session 请求/响应处理（`E003`）

## 3. 外部接口需求

### 用户接口
提供的证据未直接支持任何最终用户 GUI 或 CLI 需求。

### 软件/API 接口
| 接口 | 描述 | 证据 |
|---|---|---|
| 后端服务客户端 | 通过基于 session 的请求发送和映射响应，支持包括 `create`、`get`、`get_all` 和 `get_all_ex` 在内的服务操作 | `E003` |
| Events 服务 v2.5 | 支持 `multi_task_scalar_metrics_iter_histogram` 请求/响应结构 | `E004` |
| Models 服务 v2.4 | 支持模型删除请求结构和模型数据对象字段 | `E005`, `E006` |

### 通信接口
| 接口 | 描述 | 证据 |
|---|---|---|
| 服务器连通性 ping | Worker 按配置周期 ping 服务器；默认值显示为 30 秒 | `E002` |
| 基于队列的作业获取 | Kubernetes Glue 从 ClearML 作业执行队列中拉取作业 | `E001` |

### 数据交换格式
| 格式方面 | 支持的细节 | 证据 |
|---|---|---|
| 结构化请求/响应对象 | 后端服务使用对象结构化的请求和响应模式 | `E004`, `E005` |
| 基本字段类型 | 服务/模型结构中定义了字符串、整数、布尔值、类 datetime 值 | `E004`, `E005`, `E006` |
| 直方图键值 | 事件直方图查询支持 `iter`、`iso_time` 和 `timestamp` 轴选择器 | `E004` |
| Kubernetes 作业模板输入 | Kubernetes Glue 基于提供的 YAML 模板准备作业 | `E001` |

## 4. 功能需求

| ID | 需求 | 触发 / 输入 | 系统行为 | 输出 | 优先级 | 验证方式 | 来源证据 |
|---|---|---|---|---|---|---|---|
| FR-001 | 系统应支持一种 Kubernetes Glue 执行流程，该流程从 ClearML 作业执行队列中拉取作业，并根据提供的 YAML 模板准备一个 Kubernetes 作业。 | ClearML 执行队列中有可用作业且已提供 YAML 模板 | 拉取排队作业并基于模板构建 Kubernetes 作业 | 已准备好的 Kubernetes 作业 | 高 | 演示 | `E001` |
| FR-002 | 在用于作业执行的 pod 内，系统应安装作业/实验环境，并为用户代码启动和监控一次 Docker 执行。 | 已为在 pod 中执行准备好一个作业 | 安装实验环境，启动基于 Docker 的执行并监控它 | 在 Docker 中运行并被监控的用户代码执行 | 高 | 演示 | `E001` |
| FR-003 | 在长期运行的服务 pod 集成形式中，系统应使用 `clearml-agent` Docker 镜像运行，并通过映射的 Docker socket 管理同级 Docker 容器。 | 部署长期运行的服务 pod 集成 | 使用 `clearml-agent` 镜像，并使用映射的 Docker socket 访问来管理同级容器 | 具备同级容器管理能力的运行中服务 pod | 中 | 检查 | `E001` |
| FR-004 | Worker 应按可配置的上报周期发送状态报告。默认上报周期应为 2 秒。 | Worker 运行时处于活动状态 | 根据配置的 `report_period_sec` 发出状态报告 | 周期性的 worker 状态报告 | 中 | 测试 | `E002` |
| FR-005 | Worker 应按可配置的连通性检查周期 ping 服务器。默认 ping 周期应为 30 秒。 | Worker 运行时处于活动状态 | 根据配置的 `ping_period_sec` ping 服务器 | 周期性的连通性 ping | 中 | 测试 | `E002` |
| FR-006 | 当启用 stdout/stderr 日志记录时，worker 应记录执行中的 stdout 和 stderr。 | 已启用 `log_stdout` | 捕获并记录 stdout 和 stderr | 包含 stdout/stderr 的执行日志 | 中 | 测试 | `E002` |
| FR-007 | 后端服务客户端应通过 session 发送相应请求并返回映射后的结果形式，以支持 `create`、`get`、`get_all` 和 `get_all_ex` 的服务操作。 | 调用方调用某个受支持的服务操作 | 通过 session 发送请求，并视情况返回实体或表格风格响应 | 已创建实体引用、已获取实体或集合响应 | 中 | 测试 | `E003` |

## 5. 非功能需求

| ID | 需求 | 质量属性 | 度量 / 条件 | 优先级 | 验证方式 | 来源证据 |
|---|---|---|---|---|---|---|
| NFR-001 | 默认 worker 遥测配置应提供每 2 秒一次的状态上报和每 30 秒一次的连通性 ping，除非被配置覆盖。 | 可运维性 | `report_period_sec: 2` 和 `ping_period_sec: 30` 的默认值 | 中 | 检查 | `E002` |
| NFR-002 | Worker 应支持两种内存上报范围：默认的进程/子进程范围，以及在启用 `report_global_mem_used` 时的整机范围。 | 兼容性 / 可运维性 | `report_global_mem_used: false` 上报进程/子进程使用量；启用后上报整机使用量 | 低 | 测试 | `E002` |
| NFR-003 | 系统应保持与带版本的后端服务接口兼容，至少包括 models 服务 v2.4 和 events 服务 v2.5，如可用请求/响应结构所示。 | 兼容性 | 服务定义对所引用接口暴露 `_version = "2.4"` 和 `_version = "2.5"` | 中 | 检查 | `E004`, `E005` |

## 6. 数据需求

### 数据实体或对象
| 实体 / 对象 | 必需 / 重要字段 | 说明 | 来源证据 |
|---|---|---|---|
| Worker 配置 | `report_period_sec`, `ping_period_sec`, `log_stdout`, `report_global_mem_used` | 控制遥测、连通性检查、日志记录和内存上报范围 | `E002` |
| 直方图请求 | `task`（string）、`samples`（int，默认 10000）、`key`（`iter` / `iso_time` / `timestamp`） | 用于获取标量指标迭代直方图 | `E004` |
| 模型删除请求 | `model`（必需 string）、`force`（boolean） | 当任务将该模型用作执行模型，或创建任务已发布时，`force` 为必需 | `E005` |
| 模型对象 | `id`, `name`, `user`, `company`, `created`, `task` | 表示数据模型中显示的模型元数据字段 | `E006` |

### 输入/输出数据
| 方向 | 数据 | 来源证据 |
|---|---|---|
| 输入 | ClearML 执行队列作业 | `E001` |
| 输入 | 用于作业准备的 Kubernetes YAML 模板 | `E001` |
| 输入 | 用于 events 和 models 的后端服务请求对象 | `E004`, `E005` |
| 输出 | 根据模板准备的 Kubernetes 作业定义 | `E001` |
| 输出 | 状态报告、连通性 ping、stdout/stderr 日志 | `E002` |
| 输出 | 后端服务响应对象，包括实体和集合风格响应 | `E003`, `E004` |

### 存储、完整性、隐私、保留、迁移
提供的证据未直接支持任何存储、隐私、保留或迁移需求。

## 7. 约束

| ID | 约束 | 类型 | 来源证据 |
|---|---|---|---|
| C-001 | 长期运行的服务 pod 集成使用 `clearml-agent` Docker 镜像。 | 部署 | `E001` |
| C-002 | 同级 Docker 容器管理要求将 Docker socket 映射到 pod 中。 | 运行 / 部署 | `E001` |
| C-003 | Kubernetes Glue 作业准备依赖于已提供的 YAML 模板。 | 集成 | `E001` |
| C-004 | 证据中受支持的后端接口带有版本，包括 events v2.5 和 models v2.4。 | 兼容性 | `E004`, `E005` |

## 8. 验证与验收

| Requirement ID | Verification method | Acceptance criterion |
|---|---|---|
| FR-001 | 演示 | 展示一个排队作业被使用已提供的 YAML 模板转换为 Kubernetes 作业。 |
| FR-002 | 演示 | pod 内执行显示环境安装以及对基于 Docker 的用户代码执行进行监控。 |
| FR-003 | 检查 | 部署配置或运行时设置显示使用了 `clearml-agent` 镜像和映射的 Docker socket。 |
| FR-004 | 测试 | Worker 按照 `report_period_sec` 发出状态报告，在未覆盖时默认值为 2 秒。 |
| FR-005 | 测试 | Worker 按照 `ping_period_sec` ping 服务器，在未覆盖时默认值为 30 秒。 |
| FR-006 | 测试 | 启用 `log_stdout` 时，生成的日志中同时包含 stdout 和 stderr。 |
| FR-007 | 测试 | 调用 `create`、`get`、`get_all` 和 `get_all_ex` 返回预期的映射实体或集合响应形式。 |
| NFR-001 | 检查 | 默认配置包含 2 秒和 30 秒的上报与 ping 间隔。 |
| NFR-002 | 测试 | 内存上报行为会根据配置在进程/子进程范围和整机范围之间变化。 |
| NFR-003 | 检查 | 所引用服务接口的版本标记与 v2.4 和 v2.5 匹配。 |

## 9. 可追溯性矩阵

| ID | 需求 | 类型 | 来源 | 证据类型 | 验证方式 | 置信度 |
|---|---|---|---|---|---|---|
| FR-001 | 拉取排队作业并根据 YAML 模板准备 Kubernetes 作业 | Functional | `E001` | explicit | Demonstration | High |
| FR-002 | 在 pod 中安装实验环境并运行/监控基于 Docker 的用户代码 | Functional | `E001` | explicit | Demonstration | High |
| FR-003 | 使用 `clearml-agent` 镜像和映射的 Docker socket 运行长期服务 pod | Functional | `E001` | explicit | Inspection | Medium |
| FR-004 | 以可配置/默认间隔发送周期性状态报告 | Functional | `E002` | explicit | Test | High |
| FR-005 | 以可配置/默认间隔 ping 服务器 | Functional | `E002` | explicit | Test | High |
| FR-006 | 启用时记录 stdout 和 stderr | Functional | `E002` | explicit | Test | High |
| FR-007 | 支持 `create`、`get`、`get_all`、`get_all_ex` 服务操作 | Functional | `E003` | explicit | Test | Medium |
| NFR-001 | 默认遥测间隔为 2s 和 30s | Non-functional | `E002` | explicit | Inspection | High |
| NFR-002 | 支持可选择的内存上报范围 | Non-functional | `E002` | explicit | Test | Medium |
| NFR-003 | 保持与版本化后端接口 v2.4 和 v2.5 的兼容性 | Non-functional | `E004`, `E005` | explicit | Inspection | Medium |
