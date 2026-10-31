# 软件需求规格说明书

## 1. 引言

### 目的
本 SRS 定义了针对 `kubescape/host-scanner` 仓库在提交 `7096303f0cd65f72eeca2ff856ff4a320332639b` 时的快照、基于证据支持的需求。本文档仅限于由所提供仓库证据直接支持的行为和约束。

### 产品范围
现有证据表明：
- 一个通过 HTTP 暴露的服务，其端点行为已通过端到端测试验证，
- 根据运行时/进程配置输入推导 CNI 配置目录的逻辑，
- 从类 JSON 的控制平面数据中移除加密提供程序配置机密的逻辑，
- 使用构建标签的、针对提供商/平台特定的端到端测试方法。

### 目标读者
- `kubescape/host-scanner` 的维护者
- 测试作者和评审者
- 使用 HTTP 接口的集成方
- 需求与质量工程师

### 参考资料
- 仓库：`kubescape/host-scanner`
- 仓库 URL：https://github.com/kubescape/host-scanner
- 快照：https://github.com/kubescape/host-scanner/tree/7096303f0cd65f72eeca2ff856ff4a320332639b
- 提交：`7096303f0cd65f72eeca2ff856ff4a320332639b`
- 证据：E001, E002, E003, E004, E005, E006

## 2. 总体描述

### 产品视角
该仓库包含：
- 一个通过端到端 HTTP 请求和状态码断言验证的 HTTP 服务，
- 解释主机运行时配置的传感器/运行时逻辑，
- 用于 JSON 控制平面内容的数据脱敏逻辑。

该视角仅基于测试和测试文档。

### 产品功能概述
- 响应针对端点的 HTTP GET 请求，包括未知端点。
- 从运行时/进程配置输入解析 CNI 配置目录。
- 从 JSON 数据中移除加密提供程序配置机密。
- 使用构建标签支持针对提供商/平台特定的端到端验证。

### 用户类别
- 调用服务端点的 HTTP 客户端
- 自动化端到端测试作者
- 提供运行时/进程配置数据的集成方或操作人员

### 运行环境
支持性证据表明：
- 基于 HTTP 的端点验证访问
- 使用 Ginkgo/Gomega 风格测试的 Go 测试执行
- 通过构建标签选择的提供商/平台特定测试变体
- Linux 风格的主机/运行时路径，例如 `/var/lib/kubelet`、`/var/run/containerd`、`/run/containerd`、`/etc/cni/` 和 `/var/lib/cni/`  
对 Linux/路径假设的置信度：由测试输入推断。  
来源：E001, E002, E003, E004, E006

### 假设与依赖
- 针对提供商/平台特定的响应验证依赖于通过构建标签选择的数据结构。来源：E003, E006
- 运行时目录解析依赖于进程命令行参数和/或运行时配置默认值。来源：E001, E002
- 机密移除操作作用于反序列化为键/值结构的 JSON 数据。来源：E005

## 3. 外部接口需求

### 用户接口
没有证据表明存在图形或交互式用户界面。

### 软件/API 接口
| Interface | Requirement summary | Source |
|---|---|---|
| HTTP 端点接口 | 系统暴露可通过 `GET` 调用的 HTTP 端点；针对 `/doesnotexist` 的未知端点处理已被验证。 | E004 |
| 运行时/配置输入接口 | 系统接受足以推导 CNI 配置目录的进程/配置输入。 | E001, E002 |
| JSON 数据处理接口 | 系统接受类 JSON 的控制平面数据并输出经过脱敏的 JSON 数据。 | E005 |

### 通信接口
| Interface | Details | Source |
|---|---|---|
| HTTP | 端到端测试发送 HTTP GET 请求并验证 HTTP 状态码。 | E004 |

### 数据交换格式
| Format | Usage | Source |
|---|---|---|
| HTTP 请求/响应 | 端点调用和状态码验证 | E004 |
| JSON | 控制平面数据脱敏的输入和输出格式 | E005 |
| 命令行参数字符串 | 用于推导运行时相关路径的输入 | E001, E002 |

## 4. 功能需求

| ID | Description | Trigger/Input | System behavior | Output | Priority | Verification | Source evidence |
|---|---|---|---|---|---|---|---|
| FR-001 | 未知端点处理 | 对 `/doesnotexist` 的 HTTP `GET` 请求 | 系统应接受该请求并返回 HTTP 状态码 `404`。 | 状态为 `404` 的 HTTP 响应 | 高 | 测试 | E004 |
| FR-002 | CNI 配置目录解析 | 包括命令行参数和/或默认配置数据的运行时/进程配置输入 | 系统应从提供的运行时/进程配置中推导 CNI 配置目录。证据显示，对于已测试输入，预期解析结果包括 `/etc/cni/` 和 `/var/lib/cni/`。 | 解析得到的 CNI 配置目录路径 | 高 | 测试 | E001, E002 |
| FR-003 | 移除加密提供程序配置机密 | 包含加密提供程序配置内容的 JSON 控制平面数据 | 系统应在生成输出之前，从处理后的数据中移除加密提供程序配置机密。 | 已移除机密的脱敏 JSON 数据 | 高 | 测试 | E005 |

## 5. 非功能需求

| ID | Quality attribute | Requirement | Priority | Verification | Evidence type | Source evidence |
|---|---|---|---|---|---|---|
| NFR-001 | 安全性 | 系统不得在处理后的 JSON 输出中暴露加密提供程序配置机密。 | 高 | 测试 | explicit | E005 |
| NFR-002 | 可移植性/可维护性 | 端到端验证应通过基于构建标签的测试选择，支持针对提供商/平台特定的预期数据结构。 | 中 | 检查 | explicit | E003, E006 |
| NFR-003 | 兼容性 | HTTP 接口应使用标准 HTTP 请求/响应语义，包括对未知路径基于状态码的错误报告。 | 中 | 测试 | explicit | E004 |

## 6. 数据需求

### 数据实体或对象
| Data entity | Description | Source |
|---|---|---|
| HTTP 请求 | 发送到服务端点（例如 `/doesnotexist`）的 `GET` 请求 | E004 |
| HTTP 响应 | 包含状态码的响应对象 | E004 |
| 运行时/进程详情 | 用于确定 CNI 配置目录的命令行参数和运行时属性 | E001, E002 |
| CNI 配置目录路径 | 解析得到的文件系统路径，例如 `/etc/cni/` 或 `/var/lib/cni/` | E001, E002 |
| 控制平面 JSON 数据 | 为移除机密而反序列化到键/值映射中的 JSON | E005 |
| 提供商/平台特定的预期结构 | 通过构建标签选择的测试侧预期响应结构 | E003, E006 |

### 输入/输出数据
| Flow | Input | Output | Source |
|---|---|---|---|
| 端点验证 | HTTP `GET /doesnotexist` | HTTP 状态 `404` | E004 |
| 运行时检查 | 进程/配置数据 | 解析得到的 CNI 目录路径 | E001, E002 |
| 数据脱敏 | 包含加密提供程序配置的 JSON 数据 | 已移除机密的脱敏 JSON | E005 |

### 存储、隐私、完整性、保留、迁移
| Topic | Requirement | Source |
|---|---|---|
| 隐私/保密性 | 加密提供程序配置机密应从处理后的 JSON 输出中移除。 | E005 |
| 存储/保留/迁移 | 现有证据未予以确定。 | — |

## 7. 约束

| ID | Constraint | Source | Evidence type |
|---|---|---|---|
| C-001 | 针对提供商/平台特定的端到端测试依赖 Go 构建标签来选择面向平台设计的数据结构。 | E003, E006 | explicit |
| C-002 | 运行时目录解析受运行时/进程输入约束，这些输入可能包括 Linux 风格文件系统路径和容器运行时端点。 | E001, E002 | inferred |
| C-003 | HTTP 行为验证受限于可通过标准 HTTP 调用观察到的请求/响应交互。 | E004 | explicit |

## 8. 验证与验收

| Requirement ID | Verification method | Acceptance criteria |
|---|---|---|
| FR-001 | 测试 | 对 `/doesnotexist` 的 `GET` 请求返回 HTTP `404`。 |
| FR-002 | 测试 | 对于提供的运行时/进程测试输入，解析得到的 CNI 目录与预期路径一致。 |
| FR-003 | 测试 | 给定包含加密提供程序配置机密的输入 JSON，生成的 JSON 与预期的脱敏输出一致。 |
| NFR-001 | 测试 | 脱敏后的 JSON 输出不包含加密提供程序配置机密。 |
| NFR-002 | 检查 | 测试资源显示通过构建标签选择的提供商/平台特定预期结构。 |
| NFR-003 | 测试 | HTTP 交互使用请求/响应语义，并对未知路径采用基于状态码的报告。 |

## 9. 可追溯性矩阵

| ID | Requirement | Type | Source | Evidence Type | Verification | Confidence |
|---|---|---|---|---|---|---|
| FR-001 | 未知端点 `GET /doesnotexist` 返回 `404` | 功能 | E004 | explicit | 测试 | 高 |
| FR-002 | 从运行时/进程配置推导 CNI 配置目录 | 功能 | E001, E002 | explicit | 测试 | 中 |
| FR-003 | 从 JSON 数据中移除加密提供程序配置机密 | 功能 | E005 | explicit | 测试 | 高 |
| NFR-001 | 不在处理后的 JSON 输出中暴露加密提供程序配置机密 | 非功能 | E005 | explicit | 测试 | 高 |
| NFR-002 | 通过构建标签支持针对提供商/平台特定的 e2e 验证 | 非功能 | E003, E006 | explicit | 检查 | 中 |
| NFR-003 | 使用标准 HTTP 语义并基于状态码进行错误报告 | 非功能 | E004 | explicit | 测试 | 中 |
