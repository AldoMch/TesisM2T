# 软件需求规格说明书

## 1. 引言

### 目的
本 SRS 定义了针对提交 `01e82afac8f664079b11a2e96569c55a7615ed2e` 的 `openshift/configuration-anomaly-detection` 仓库的、基于证据支持的需求。其涵盖由仓库证据支持的可观察行为和部署预期。

### 产品范围
Configuration Anomaly Detection (CAD) 被描述为负责通过检测集群异常并向集群所有者发送相关通信来减少人工 SRE 调查。该仓库包含一个 CLI，`cadctl`，用于执行“cluster has gone missing”（CHGM）告警的工作流、CLI 使用的集成代码，以及部署资产，包括一条可绕过事件监听器的 Tekton `PipelineRun` 路径。`cadctl` 还被描述为用于检测和缓解配置失误的 CLI 工具。来源证据：`E003`、`E004`、`E005`、`E006`。

### 目标读者
本文档面向：
- 通过 `cadctl` 或流水线资产运行 CAD 工作流的 SRE 或运维用户。来源证据：`E004`、`E006`。
- 扩展 CLI 端点或集成的贡献者。来源证据：`E003`。
- 构建容器化 CLI 工件的发布与部署工程师。来源证据：`E005`。

### 参考资料
- 仓库：`openshift/configuration-anomaly-detection`
- 仓库 URL：<https://github.com/openshift/configuration-anomaly-detection>
- 快照 URL：<https://github.com/openshift/configuration-anomaly-detection/tree/01e82afac8f664079b11a2e96569c55a7615ed2e>
- 主要证据来源：`README.md`、`pkg/README.md`、`Dockerfile`、`deploy/skip-webhook/README.md`、`deploy/skip-webhook/pipeline-run.yaml`、`hack/update-template/README.md`

## 2. 总体描述

### 产品视角
CAD 是一个以 CLI 为中心的运维工具，带有配套的集成代码和部署资产。包库保存了 CLI 工具使用的集成和代码。该仓库还提供了一条基于 Tekton 的执行路径，其中可以直接创建 `PipelineRun`，而不是使用事件监听器。来源证据：`E001`、`E003`、`E006`。

### 产品功能概述
- 检测集群异常并向集群所有者发送相关通信。来源证据：`E004`。
- 通过 `cadctl` 执行 CHGM 告警工作流。来源证据：`E004`。
- 支持仓库中标识的 PagerDuty、AWS 和 OCM 集成。来源证据：`E003`、`E004`。
- 允许直接创建跳过事件监听器的流水线运行。来源证据：`E001`、`E006`。
- 通过模板更新工具更新 `configuration-anomaly-detection-template.Template.yaml`。来源证据：`E002`。

### 用户类别
| 用户类别 | 描述 | 来源证据 |
|---|---|---|
| SRE / 运维用户 | 使用 CAD 减少人工调查并运行与 CHGM 相关的工作流。 | `E004` |
| 部署工程师 | 运行基于 Tekton 的执行路径，包括直接创建 `PipelineRun`。 | `E001`, `E006` |
| 贡献者 / 开发者 | 添加 CLI 端点和集成代码，并更新模板。 | `E002`, `E003` |

### 运行环境
| 方面 | 需求上下文 | 来源证据 |
|---|---|---|
| 运行时形式 | 包含 `/bin/cadctl` 的容器化 CLI 运行时 | `E005` |
| 构建环境 | 基于 `registry.ci.openshift.org/openshift/release:golang-1.17` 的构建器镜像 | `E005` |
| 运行时基础镜像 | `quay.io/app-sre/ubi8-ubi-minimal:8.6-854` | `E005` |
| 流水线环境 | 命名空间 `configuration-anomaly-detection` 中的 Tekton `v1beta1` `PipelineRun` | `E006` |

### 假设与依赖
- CAD 依赖名为 PagerDuty、AWS 和 OCM 的外部集成。来源证据：`E003`、`E004`。
- 直接流水线执行依赖名为 `cad-checks-pipeline` 的 Tekton 流水线。来源证据：`E006`。
- 模板更新工作流依赖名为 `configuration-anomaly-detection-template.Template.yaml` 的目标文件。来源证据：`E002`。

## 3. 外部接口需求

### 用户接口
| 接口 | 描述 | 来源证据 |
|---|---|---|
| CLI | `cadctl` 是文档化的面向用户 CLI，并执行 CHGM 工作流。 | `E004` |
| 命令驱动的维护工具 | 仓库工具支持运行模板更新命令和直接流水线执行命令。 | `E001`, `E002` |

### 软件/API 接口
| 接口 | 描述 | 来源证据 |
|---|---|---|
| 内部集成库 | 包库提供 CLI 使用的集成/代码。 | `E003` |
| 已命名集成 | 明确命名的受支持集成领域为 PagerDuty、AWS 和 OCM。 | `E003`, `E004` |
| Tekton 流水线引用 | 直接执行目标为 `pipelineRef.name: cad-checks-pipeline`。 | `E006` |

### 通信接口
| 接口 | 描述 | 来源证据 |
|---|---|---|
| 事件驱动的流水线调用 | 向 Tekton 流水线运行提供一个 payload 对象；skip-webhook 路径绕过事件监听器并直接创建流水线运行。 | `E001`, `E006` |

### 数据交换格式
| 格式 | 描述 | 来源证据 |
|---|---|---|
| JSON | Tekton 参数 `payload` 是一个包含 `event.data.id` 的 JSON 字符串。 | `E006` |
| YAML | 部署资产包括一个 Tekton `PipelineRun` 清单和一个模板 YAML 目标。 | `E002`, `E006` |

## 4. 功能需求

| ID | 描述 | 触发器 / 输入 | 系统行为 | 输出 | 优先级 | 验证 | 来源证据 |
|---|---|---|---|---|---|---|---|
| FR-001 | 系统应提供一个名为 `cadctl` 的 CLI 用于 CAD 工作流。 | 用户调用 `cadctl`。 | 系统将 `cadctl` 公开为仓库的 CLI 工件和运行时入口点。 | 用户可用的可执行 CLI。 | 高 | 检查 | `E004`, `E005` |
| FR-002 | `cadctl` CLI 应执行“cluster has gone missing”（CHGM）告警的工作流。 | 通过 `cadctl` 启动 CHGM 工作流。 | 系统通过 CLI 执行 CHGM 工作流。 | 通过 `cadctl` 进行 CHGM 工作流处理。 | 高 | 演示 | `E004` |
| FR-003 | 系统应支持 CAD 运行，用于检测集群异常并向集群所有者发送相关通信。 | CAD 处理一个集群异常。 | 系统执行与异常检测相关的处理，并作为 CAD 范围的一部分发出相关所有者通信。 | 向集群所有者发送相关通信。 | 高 | 分析 | `E004` |
| FR-004 | 系统应提供一条直接执行路径，跳过事件监听器并直接创建 Tekton `PipelineRun`。 | 用户遵循 skip-webhook 使用路径。 | 系统接受直接创建 `PipelineRun`，而不是要求使用事件监听器路径。 | 创建一个 Tekton `PipelineRun` 资源。 | 中 | 演示 | `E001`, `E006` |
| FR-005 | 当使用直接 Tekton 执行路径时，系统应在命名空间 `configuration-anomaly-detection` 中调用名为 `cad-checks-pipeline` 的流水线。 | 提交一个直接 `PipelineRun` 清单。 | 系统引用 `pipelineRef.name: cad-checks-pipeline` 并在命名空间 `configuration-anomaly-detection` 中运行。 | 面向指定流水线和命名空间的 Tekton 流水线执行请求。 | 中 | 检查 | `E006` |
| FR-006 | 直接 Tekton 执行路径应接受一个以 JSON 编码且携带 `event.data.id` 的 `payload` 参数。 | 使用 `payload` 参数创建一个 `PipelineRun`。 | 系统将 `payload` 参数值传递给流水线运行。 | 可供流水线执行使用的 JSON payload。 | 中 | 检查 | `E006` |
| FR-007 | 系统应提供 CLI 使用的集成代码，用于 PagerDuty、AWS 和 OCM 集成领域。 | CLI 工作流需要受支持的集成。 | 系统包含对已命名外部系统的集成/库支持。 | 针对已命名系统的具备集成能力的 CLI/库行为。 | 中 | 检查 | `E003`, `E004` |
| FR-008 | 系统应提供一个模板更新工作流，用于更新 `configuration-anomaly-detection-template.Template.yaml`。 | 用户运行文档化的 update-template 工具。 | 系统更新目标模板文件。 | 更新后的 `configuration-anomaly-detection-template.Template.yaml`。 | 低 | 演示 | `E002` |

## 5. 非功能需求

| ID | 质量属性 | 需求 | 优先级 | 验证 | 来源证据 |
|---|---|---|---|---|---|
| NFR-001 | 可移植性 | CLI 运行时工件应打包为基于 `quay.io/app-sre/ubi8-ubi-minimal:8.6-854` 的容器镜像，并应包含 `/bin/cadctl`。 | 中 | 检查 | `E005` |
| NFR-002 | 构建兼容性 | 文档化的 CLI 容器构建应使用构建器镜像 `registry.ci.openshift.org/openshift/release:golang-1.17`。 | 中 | 检查 | `E005` |
| NFR-003 | 构建元数据可追踪性 | 容器镜像应公开 vendor、name、description、display-name、version、build-date、VCS reference 和 Dockerfile path 的镜像标签。 | 低 | 检查 | `E005` |
| NFR-004 | 可维护性 | 供 CLI 使用的集成逻辑应组织在包库中，以便新的 CLI 端点可以调用所需的集成代码。此需求是根据文档化的扩展工作流推断得出。 | 低 | 分析 | `E003` |

## 6. 数据需求

### 数据实体 / 对象
| ID | 数据实体 | 描述 | 来源证据 |
|---|---|---|---|
| DR-001 | `payload` | 传递给 Tekton `PipelineRun` 的 JSON 字符串参数。 | `E006` |
| DR-002 | `event.data.id` | 嵌套在 `payload` JSON 对象中的标识符。示例值显示为 `incidentid`。 | `E006` |
| DR-003 | `PipelineRun` | 用于直接执行 CAD 检查的 Tekton 资源。 | `E006` |
| DR-004 | `configuration-anomaly-detection-template.Template.yaml` | 由模板更新工作流更新的模板文件。 | `E002` |

### 输入 / 输出数据
| Requirement ID | Requirement | Verification | Source evidence |
|---|---|---|---|
| DR-REQ-001 | 直接执行路径应接受 YAML 格式的 Tekton `PipelineRun` 清单作为输入。 | 检查 | `E006` |
| DR-REQ-002 | 直接执行路径应接受一个值为 JSON 文本的 `payload` 参数。 | 检查 | `E006` |
| DR-REQ-003 | 模板更新工作流应输出更新后的 `configuration-anomaly-detection-template.Template.yaml` 文件。 | 演示 | `E002` |

### 存储、隐私、完整性、保留、迁移
在证据包中未找到受支持的需求。

## 7. 约束

| ID | 约束 | 来源证据 |
|---|---|---|
| C-001 | 运行时交付形式被约束为包含 `/bin/cadctl` 的容器镜像。 | `E005` |
| C-002 | 文档化的构建过程被约束为 Go 1.17 构建器镜像 `registry.ci.openshift.org/openshift/release:golang-1.17`。 | `E005` |
| C-003 | 文档化的运行时基础镜像被约束为 `quay.io/app-sre/ubi8-ubi-minimal:8.6-854`。 | `E005` |
| C-004 | 直接执行被约束为 Tekton `apiVersion: tekton.dev/v1beta1`。 | `E006` |
| C-005 | 直接 `PipelineRun` 示例被约束为命名空间 `configuration-anomaly-detection` 和流水线名称 `cad-checks-pipeline`。 | `E006` |
| C-006 | skip-webhook 执行路径被明确定义为绕过事件监听器。 | `E001` |

## 8. 验证与验收

| Requirement ID | Verification method | Acceptance basis |
|---|---|---|
| FR-001 | 检查 | 容器/运行时工件和仓库文档显示 `cadctl` 是 CLI 和运行时二进制文件。 |
| FR-002 | 演示 | 可根据文档化目的通过 `cadctl` 启动 CHGM 工作流。 |
| FR-003 | 分析 | 仓库文档说明 CAD 范围包括异常检测和向集群所有者通信。 |
| FR-004 | 演示 | 无需事件监听器路径即可执行直接流水线执行。 |
| FR-005 | 检查 | 提交的 `PipelineRun` 清单以 `configuration-anomaly-detection` 中的 `cad-checks-pipeline` 为目标。 |
| FR-006 | 检查 | `PipelineRun` 清单包含带有 `event.data.id` 的 JSON `payload` 参数。 |
| FR-007 | 检查 | 仓库公开了供 CLI 使用的 PagerDuty、AWS 和 OCM 集成领域。 |
| FR-008 | 演示 | 运行 update-template 工作流会更新 `configuration-anomaly-detection-template.Template.yaml`。 |
| NFR-001 | 检查 | 容器定义使用指定的运行时基础镜像并复制 `/bin/cadctl`。 |
| NFR-002 | 检查 | 容器定义使用指定的 Go 1.17 构建器镜像。 |
| NFR-003 | 检查 | 容器定义包含文档化的标签。 |
| NFR-004 | 分析 | 文档化的扩展工作流显示 CLI 端点新增会调用包库集成代码。 |
| DR-REQ-001 | 检查 | 直接执行输入表示为 YAML `PipelineRun`。 |
| DR-REQ-002 | 检查 | 输入包含作为 JSON 文本的 `payload`。 |
| DR-REQ-003 | 演示 | update-template 工作流生成更新后的模板文件。 |

## 9. 可追溯性矩阵

| ID | Requirement | Type | Source | Evidence Type | Verification | Confidence |
|---|---|---|---|---|---|---|
| FR-001 | 为 CAD 工作流提供一个名为 `cadctl` 的 CLI。 | Functional | `E004`, `E005` | explicit | Inspection | High |
| FR-002 | `cadctl` 执行 CHGM 工作流。 | Functional | `E004` | explicit | Demonstration | High |
| FR-003 | CAD 检测集群异常并向集群所有者发送相关通信。 | Functional | `E004` | explicit | Analysis | Medium |
| FR-004 | 支持一条直接创建 Tekton `PipelineRun` 的 skip-webhook 路径。 | Functional | `E001`, `E006` | explicit | Demonstration | High |
| FR-005 | 直接执行在命名空间 `configuration-anomaly-detection` 中调用 `cad-checks-pipeline`。 | Functional | `E006` | explicit | Inspection | High |
| FR-006 | 直接执行接受包含 `event.data.id` 的 JSON `payload`。 | Functional | `E006` | explicit | Inspection | High |
| FR-007 | 为 PagerDuty、AWS 和 OCM 提供供 CLI 使用的集成。 | Functional | `E003`, `E004` | explicit | Inspection | Medium |
| FR-008 | 提供一个工作流来更新 `configuration-anomaly-detection-template.Template.yaml`。 | Functional | `E002` | explicit | Demonstration | Medium |
| NFR-001 | 将运行时打包为包含 `/bin/cadctl` 的 UBI minimal 容器。 | Non-functional | `E005` | explicit | Inspection | High |
| NFR-002 | 在文档化的容器构建中使用 Go 1.17 构建器镜像。 | Non-functional | `E005` | explicit | Inspection | High |
| NFR-003 | 在容器镜像中公开构建元数据标签。 | Non-functional | `E005` | explicit | Inspection | High |
| NFR-004 | 将供 CLI 使用的集成组织在包库中，以支持端点扩展。 | Non-functional | `E003` | inferred | Analysis | Medium |
| DR-REQ-001 | 接受 YAML `PipelineRun` 作为直接执行输入。 | Data | `E006` | explicit | Inspection | High |
| DR-REQ-002 | 接受 JSON 文本形式的直接执行 `payload`。 | Data | `E006` | explicit | Inspection | High |
| DR-REQ-003 | 从更新工作流输出更新后的模板 YAML 文件。 | Data | `E002` | explicit | Demonstration | Medium |
