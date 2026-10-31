# 软件需求规格说明书

## 1. 引言

### 目的
本 SRS 定义了针对提交 `baa3a04d1e5d2e0f4b85a97611c8dfe53fb7167f` 时 `chaitin/veinmind-tools` 仓库快照的、基于证据支撑的需求。其涵盖了仓库证据所支持的可观察行为、接口、数据结构和约束。

### 产品范围
`veinmind-tools` 被描述为一套基于 `veinmind-sdk` 的自研容器安全工具集。该仓库包括：
- 用于扫描本地镜像的工具集，
- 用于镜像和容器扫描的 CLI 命令，
- 一个将 Docker 插件请求映射为操作的 runner/authz 组件，
- 示例插件打包，
- 面向报告的恶意文件和 IaC 扫描结果数据模型。  
来源：[E002], [E003], [E004], [E005], [E006], [E001]

### 目标读者
- 使用该工具集扫描镜像或容器的安全运维人员
- 使用仓库示例构建 `veinmind-tool` 插件的插件开发者
- 使用 Docker 和 `veinmind-runner` 部署该工具集的集成人员  
来源：[E002], [E003], [E001]

### 参考资料
- 仓库：https://github.com/chaitin/veinmind-tools
- 快照：https://github.com/chaitin/veinmind-tools/tree/baa3a04d1e5d2e0f4b85a97611c8dfe53fb7167f
- 证据来源：
  - `README.en.md` [E002]
  - `example/go/cmd/cli.go` [E003]
  - `veinmind-runner/pkg/authz/route/docker_plugin_action.go` [E004]
  - `plugins/go/veinmind-malicious/database/model/model.go` [E005]
  - `plugins/go/veinmind-iac/cmd/cli.go` [E006]
  - `example/python/Dockerfile` [E001]

## 2. 总体描述

### 产品视角
该仓库提供了一个构建于 `veinmind-sdk` 之上的容器安全工具集，并提供了一个要求使用 Docker 和 `veinmind-runner` 的文档化快速开始流程。它还提供了用于创建插件的示例代码，并包含用于扫描及请求授权/路由的组件。  
来源：[E002], [E003], [E004], [E001]

### 产品功能概述
- 通过 CLI 命令扫描镜像
- 通过 CLI 命令扫描容器
- 在并行容器中运行工具
- 通过 HTTP 方法和 URI 匹配 Docker 插件授权请求到操作
- 生成/报告恶意文件和 IaC 发现项的结构化扫描结果数据
- 为基于 Python 的工具/插件提供示例打包  
来源：[E002], [E003], [E004], [E005], [E006], [E001]

### 用户类别
| 用户类别 | 描述 | 证据 |
|---|---|---|
| 安全运维人员 | 执行本地镜像快速扫描并使用工具命令 | [E002], [E003] |
| 插件开发者 | 使用示例快速创建 `veinmind-tool` 插件 | [E002], [E001], [E003] |
| 部署/集成运维人员 | 安装 Docker 和 `veinmind-runner`，使用启动脚本和容器化执行 | [E002] |

### 运行环境
| 方面 | 支持环境 | 证据 |
|---|---|---|
| 容器运行时 | 必须正确安装 Docker | [E002] |
| Runner 依赖 | `veinmind-runner` 镜像作为快速开始的一部分被安装 | [E002] |
| 执行模型 | 工具支持在并行容器中运行 | [E002] |
| 示例 Python 运行时 | `veinmind/python3.6:1.3.1-stretch` 基础镜像 | [E001] |

### 假设与依赖
- 该工具集依赖于目标环境中可用的 Docker。[E002]
- 快速开始的使用依赖于安装 `veinmind-runner` 镜像并获取并行容器启动脚本。[E002]
- 该项目基于 `veinmind-sdk`。[E002]
- 示例 Python 打包依赖于 `pip install -r requirements.txt`。[E001]

## 3. 外部接口需求

### 用户接口
| 接口 | 描述 | 证据 |
|---|---|---|
| CLI `scan-image` | 用于镜像扫描的命令行入口点 | [E003] |
| CLI `scan-container` | 用于容器扫描的命令行入口点 | [E003] |

### 软件/API 接口
| 接口 | 描述 | 证据 |
|---|---|---|
| `veinmind-sdk` / `libveinmind` | 该工具集及 Go CLI 示例所使用的基础 SDK/库 | [E002], [E003] |
| `veinmind-runner` | 快速开始工作流中所需的 runner 镜像 | [E002] |
| Docker 授权请求接口 | authz 逻辑消费请求方法和请求 URI 以确定 Docker 插件操作 | [E004] |

### 通信接口
| 接口 | 描述 | 证据 |
|---|---|---|
| Docker 插件 authz 路由 | 请求依据 `RequestMethod` 和 `RequestURI` 针对已配置路由正则进行分类 | [E004] |

### 数据交换格式
| 格式/对象 | 描述 | 证据 |
|---|---|---|
| 恶意扫描报告对象 | `ReportData`, `ReportImage`, `ReportLayer`, `MaliciousFileInfo` 结构化数据 | [E005] |
| IaC 告警/报告详情对象 | 包括行号、文件路径和原始内容在内的规则元数据及文件位置详情 | [E006] |

## 4. 功能需求

| ID | 描述 | 触发 / 输入 | 系统行为 | 输出 | 优先级 | 验证方法 | 来源证据 |
|---|---|---|---|---|---|---|---|
| FR-001 | 系统应提供名为 `scan-image` 的 CLI 命令用于镜像扫描。 | 用户调用 `scan-image`。 | CLI 应暴露 `scan-image` 命令，并针对镜像句柄运行面向镜像的扫描逻辑。 | 命令成功或错误状态。 | 高 | 演示 | [E003] |
| FR-002 | 系统应提供名为 `scan-container` 的 CLI 命令用于容器扫描。 | 用户调用 `scan-container`。 | CLI 应暴露 `scan-container` 命令，并运行面向容器的扫描流程。 | 命令成功或错误状态。 | 高 | 演示 | [E003] |
| FR-003 | 系统应在快速开始工作流中支持扫描本地镜像。 | 用户遵循快速开始步骤并请求本地镜像扫描。 | 系统应允许在文档化的工具集工作流内执行本地镜像扫描。 | 本地镜像扫描执行。 | 高 | 演示 | [E002] |
| FR-004 | Docker 授权/路由组件应通过将传入请求方法和请求 URI 与已配置路由正则进行匹配来确定 Docker 插件操作。 | 收到带有 `RequestMethod` 和 `RequestURI` 的授权请求。 | 该组件应返回与首个匹配路由关联的操作，且该路由的方法必须与请求匹配。 | 选定的 Docker 插件操作。 | 中 | 测试 | [E004] |
| FR-005 | 当没有任何已配置路由与请求方法和 URI 匹配时，Docker 授权/路由组件应返回 `NoneDockerPlugin`。 | 授权请求未匹配该请求方法下的任何已配置路由正则。 | 该组件应返回 `NoneDockerPlugin`。 | `NoneDockerPlugin` 操作结果。 | 中 | 测试 | [E004] |
| FR-006 | 示例 Python 工具包应通过其容器入口点使用透传的 CLI 参数执行 `python scan.py`。 | 容器使用用户提供的参数启动。 | 入口点应调用 `python scan.py $*`。 | Python 扫描进程使用透传参数启动。 | 中 | 演示 | [E001] |

## 5. 非功能需求

| ID | 质量属性 | 需求 | 优先级 | 验证方法 | 来源证据 | 证据类型 |
|---|---|---|---|---|---|---|
| NFR-001 | 可扩展性 / 执行模型 | 所有工具都应支持在并行容器中运行。 | 高 | 演示 | [E002] | 明确 |
| NFR-002 | 兼容性 | 产品应以与云原生基础设施兼容为目标。 | 中 | 检查 | [E002] | 明确 |
| NFR-003 | 可移植性 | 示例 Python 工具应可在基于 `veinmind/python3.6:1.3.1-stretch` 的容器环境中运行。 | 中 | 检查 | [E001] | 明确 |

## 6. 数据需求

### 数据实体或对象
| 数据实体 | 已证实的关键字段 | 证据支持的用途 | 来源 |
|---|---|---|---|
| `MaliciousFileInfo` | `Engine`, `ImageID`, `LayerID`, `RelativePath`, `FileName`, `FileSize`, `FileMd5`, `FileSha256`, `FileCreated`, `Description` | 捕获与镜像/层/文件相关联的恶意文件发现项 | [E005] |
| `ReportData` | `ScanImageCount`, `MaliciousFileCount`, `ScanSpendTime`, `ScanStartTime`, `ScanFileCount`, `ScanImageResult` | 汇总扫描摘要及每个镜像的结果 | [E005] |
| `ReportImage` | `ImageName`, `ImageID`, `MaliciousFileCount`, `ScanFileCount`, `ImageCreatedAt`, `MaliciousFileInfos`, `Layers` | 保存每个镜像的报告数据 | [E005] |
| `ReportLayer` | `ImageID`, `LayerID` 及其关联的恶意文件信息集合 | 保存每层的报告数据 | [E005] |
| IaC 规则详情 | `Id`, `Name`, `Description`, `Reference`, `Severity`, `Solution`, `Type` | 表示告警中的 IaC 规则元数据 | [E006] |
| IaC 文件详情 | `StartLine`, `EndLine`, `FilePath`, `Original` | 表示 IaC 发现项的文件位置详情 | [E006] |

### 输入/输出数据
| 方向 | 数据 | 证据 |
|---|---|---|
| 输入 | `scan-image` 和 `scan-container` 的 CLI 命令调用 | [E003] |
| 输入 | Docker 授权请求字段 `RequestMethod` 和 `RequestURI` | [E004] |
| 输出 | Docker 插件操作选择，包括 `NoneDockerPlugin` 回退 | [E004] |
| 输出 | 结构化恶意扫描报告对象 | [E005] |
| 输出 | 带有规则和文件信息的结构化 IaC 告警详情 | [E006] |

### 存储、完整性、保留、隐私、迁移
仅通过 GORM 模型定义证实了面向持久化的模型结构。除结构化报告实体的存在之外，仓库中没有明确证据支持保留、隐私、迁移、备份或完整性控制。  
来源：[E005]

## 7. 约束

| 约束 | 描述 | 证据 |
|---|---|---|
| 部署依赖 | 为使用快速开始功能，机器上必须正确安装 Docker。 | [E002] |
| Runner 依赖 | 快速开始的使用要求安装 `veinmind-runner` 镜像。 | [E002] |
| 启动依赖 | 快速开始的使用要求下载 `veinmind-runner` 并行容器启动脚本。 | [E002] |
| 技术约束 | 该工具集基于 `veinmind-sdk`。 | [E002] |
| 示例运行时约束 | 示例 Python 打包使用 `veinmind/python3.6:1.3.1-stretch` 并从 `requirements.txt` 安装依赖。 | [E001] |

## 8. 验证与验收

| 需求 ID | 验证方法 | 验收标准 |
|---|---|---|
| FR-001 | 演示 | 调用 CLI 时显示并执行 `scan-image` 命令路径。 |
| FR-002 | 演示 | 调用 CLI 时显示并执行 `scan-container` 命令路径。 |
| FR-003 | 演示 | 文档化的快速开始流程可用于发起本地镜像扫描。 |
| FR-004 | 测试 | 对于方法和 URI 与已配置路由正则匹配的请求，返回相应的 Docker 插件操作。 |
| FR-005 | 测试 | 对于没有匹配路由的请求，结果为 `NoneDockerPlugin`。 |
| FR-006 | 演示 | 启动示例 Python 容器时使用透传参数运行 `python scan.py`。 |
| NFR-001 | 演示 | 工具可按文档说明在并行容器中运行。 |
| NFR-002 | 检查 | 仓库文档明确说明其以与云原生基础设施兼容为目标。 |
| NFR-003 | 检查 | 示例 Python 运行时基础镜像为 `veinmind/python3.6:1.3.1-stretch`。 |

## 9. 可追溯性矩阵

| ID | 需求 | 类型 | 来源 | 证据类型 | 验证 | 置信度 |
|---|---|---|---|---|---|---|
| FR-001 | 提供 `scan-image` CLI 命令 | 功能 | [E003] | 明确 | 演示 | 高 |
| FR-002 | 提供 `scan-container` CLI 命令 | 功能 | [E003] | 明确 | 演示 | 高 |
| FR-003 | 在快速开始工作流中支持本地镜像扫描 | 功能 | [E002] | 明确 | 演示 | 中 |
| FR-004 | 将 authz 请求方法/URI 匹配到已配置的 Docker 插件操作 | 功能 | [E004] | 明确 | 测试 | 高 |
| FR-005 | 当没有 authz 路由匹配时返回 `NoneDockerPlugin` | 功能 | [E004] | 明确 | 测试 | 高 |
| FR-006 | 示例 Python 入口点使用透传参数执行 `python scan.py` | 功能 | [E001] | 明确 | 演示 | 高 |
| NFR-001 | 支持在并行容器中运行所有工具 | 非功能 | [E002] | 明确 | 演示 | 高 |
| NFR-002 | 以与云原生基础设施兼容为目标 | 非功能 | [E002] | 明确 | 检查 | 中 |
| NFR-003 | 示例 Python 工具可在 `veinmind/python3.6:1.3.1-stretch` 上运行 | 非功能 | [E001] | 明确 | 检查 | 高 |
