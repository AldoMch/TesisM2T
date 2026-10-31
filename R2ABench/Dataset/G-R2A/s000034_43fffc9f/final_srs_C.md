# 软件需求规格说明书 (SRS)

Repository: IBM/torc_py  
Repository URL: https://github.com/IBM/torc_py  
Commit: `cbd7199aad06f7bff7e8e089ebec2cd1b0265c8a`

## 1. 引言

### 1.1 目的
本 SRS 为 `torc_py`（一个用于基于任务并行的 Python 库）定义了基于证据的软件需求。本文档仅依据所提供的代码仓库证据编写，旨在描述可从外部观察到的行为、接口、约束和可验证质量。

### 1.2 产品范围
`torc_py` 被描述为一个平台无关的自适应负载均衡库，用于在共享内存和分布式内存平台上编排多个函数求值的调度。它提供了一个并行计算框架，用于表达和执行基于任务的并行性；其内部使用 MPI，且对用户透明；允许在应用层使用传统 MPI；并支持并行嵌套循环和 map 函数。来源：E004、E001、E003。

### 1.3 目标读者
- 使用 Python 进行基于任务的并行执行的应用开发人员
- 在工作线程、MPI 进程或集群节点上运行工作负载的用户
- 根据示例和测试验证库行为的测试人员和维护人员

### 1.4 参考资料
- 代码仓库 README：证据 ID E001、E003、E004、E005、E006
- 代码仓库测试：证据 ID E002
- 代码仓库元数据：IBM/torc_py，commit `cbd7199aad06f7bff7e8e089ebec2cd1b0265c8a`

## 2. 总体描述

### 2.1 产品视角
`torc_py` 是一个 Python 任务库，供 Python 应用程序提交函数求值以进行并行执行。它可跨工作线程和 MPI 进程运行，包括分布式集群节点，同时提供统一的基于任务的编程模型。来源：E004、E001、E003、E002。

### 2.2 产品功能概述
证据支持以下产品功能：
- 提交函数求值任务以进行并行执行，并等待完成
- 向应用程序返回任务输入和值结果
- 提供并行 map 行为
- 在父任务完成时执行回调任务
- 在可用工作者之间分发工作
- 允许空闲工作者从其他队列窃取任务
- 支持在共享内存和分布式内存平台上使用
- 内部使用 MPI，同时允许在应用层使用传统 MPI

来源：E001、E002、E003、E004、E006。

### 2.3 用户类别
- 对函数求值进行并行化的 Python 开发人员
- 在多个工作线程和 MPI 进程上运行任务的 HPC 用户
- 在集群上对图像数据集进行预处理或运行数值/优化工作负载的用户

来源：E004、E005、E002。

### 2.4 运行环境
支持或有证据表明的执行环境包括：
- 导入 `torc` 的 Python 应用程序
- 进程内的工作线程执行
- 基于 MPI 的多进程执行
- 共享内存和分布式内存平台
- 集群节点执行
- 在测试中使用 `TORC_WORKERS` 环境变量的配置

来源：E004、E003、E005、E002。

### 2.5 假设与依赖
- 库内部使用 MPI。来源：E004。
- 应用程序也可以在应用层使用传统 MPI 代码。来源：E004。
- 某些回调示例假定每个 MPI 进程只有一个工作线程。来源：E003。
- 任务执行依赖于工作者的可用性。来源：E001、E006。

## 3. 外部接口需求

### 3.1 用户接口
没有图形用户界面的证据。交互通过 Python 编程接口和程序输出进行。来源：E002、E004。

### 3.2 软件/API 接口
证据显示以下面向 Python 的接口：

| 接口 | 观察到的行为 | 来源 |
|---|---|---|
| `torc.submit(function, input)` | 提交一个任务以进行异步执行，并返回任务句柄 | E002 |
| `torc.wait()` | 在继续之前等待已提交任务完成 | E002, E001 |
| `torc.gettime()` | 获取用于测量已用执行时间的计时值 | E002 |
| `task.input()` | 返回与任务关联的输入 | E002 |
| `task.result()` | 返回已完成任务的结果 | E002 |

README 还证明了 map 风格操作和基于回调的执行行为，但在所提供的摘录中未公开精确的 API 签名。来源：E001、E003、E006。

### 3.3 通信接口
- 库内部使用基于 MPI 的通信。来源：E004。
- 空闲工作者可以发出窃取请求，从另一个 rank 的队列中获取任务。来源：E003。

### 3.4 数据交换格式
- 任务输入和输出以 Python 函数参数和返回结果的形式交换。来源：E002。
- 一个图像预处理示例将按标签子文件夹组织的图像数据集转换为单个 HDF5 文件。来源：E005。

## 4. 功能需求

| ID | 描述 | 触发器/输入 | 系统行为 | 输出 | 优先级 | 验证 | 源证据 |
|---|---|---|---|---|---|---|---|
| FR-001 | 并行任务提交与完成等待 | 应用程序提交一个或多个函数求值任务并调用等待操作 | 系统应接受已提交任务并在可用工作者上并行执行，且在已提交任务完成之前阻塞等待操作的完成 | `wait` 返回后，可获取结果的已完成任务 | High | Test | E002, E001 |
| FR-002 | 任务结果获取 | 有一个已完成的任务句柄可用 | 系统应通过任务句柄暴露原始任务输入和计算得到的任务结果 | 应用程序可获取任务输入值和任务结果值 | High | Test | E002 |
| FR-003 | 并行 map 执行 | 应用程序调用 map 风格的并行求值 | 系统应支持与逐个提交任务等效的并行 map 行为；示例中记录的默认 chunk size 为 1 | 映射函数结果的集合 | Medium | Demonstration | E001, E006 |
| FR-004 | 完成时执行回调任务 | 一个任务完成，并且有关联的回调任务 | 系统应将已完成任务作为参数传递给回调任务，并在父任务所在节点/进程的工作线程上执行该回调任务 | 回调任务的执行以及任何由回调产生、对应用程序可见的效果 | Medium | Demonstration | E001, E003 |
| FR-005 | 在可用工作者之间进行循环分发 | 一个主任务为可用工作者生成多个子任务 | 系统应在可用工作者之间分发生成的任务，包括示例中记录的循环分发 | 分配给各工作者执行的任务 | Medium | Demonstration | E001, E006 |
| FR-006 | 空闲工作者的任务窃取 | 某工作者发现其本地队列为空，而其他地方的队列中仍有任务 | 系统应允许该空闲工作者发出窃取请求，并从其他工作者或 rank 的队列中获取任务 | 分配给空闲工作者执行的已获取任务 | Medium | Demonstration | E003 |
| FR-007 | 跨共享内存和分布式内存平台的统一执行 | 应用程序使用该库进行基于任务的并行 | 系统应提供一种统一的方法，以在共享内存和分布式内存平台上表达和执行基于任务的并行 | 在受支持的平台类型之间使用相同的基于任务的方法进行并行执行 | High | Inspection | E004 |
| FR-008 | 透明的内部 MPI 使用以及与应用层传统 MPI 的兼容性 | 应用程序在支持 MPI 的环境中于该库下运行，无论其自身是否包含 MPI 代码 | 系统应以对用户透明的方式在内部使用 MPI，并应允许在应用层使用传统 MPI 代码 | 并行运行时无需用户管理内部 MPI 细节，同时保留应用层 MPI 的使用 | High | Inspection | E004 |

## 5. 非功能需求

| ID | 质量属性 | 需求 | 优先级 | 验证 | 证据 | 置信度 |
|---|---|---|---|---|---|---|
| NFR-001 | 可移植性 | 系统应可在共享内存和分布式内存平台上运行。 | High | Inspection | E004 | Explicit |
| NFR-002 | 兼容性 | 系统在内部使用 MPI 的同时，应保持与应用层传统 MPI 代码的兼容性。 | High | Inspection | E004 | Explicit |
| NFR-003 | 性能（已展示能力） | 系统应支持可相对于串行执行减少已用运行时间的并行执行模式；代码仓库证据展示了一个四个工作者各执行一个任务时快 4 倍的示例。 | Medium | Demonstration | E001 | Explicit |
| NFR-004 | 可扩展性（已展示能力） | 系统应支持集群规模执行；代码仓库证据报告了在一个文档化用例中，TMCMC 调度在 1024 个计算节点上的总体并行效率超过 90%。 | Medium | Analysis | E005 | Explicit |
| NFR-005 | 负载均衡 | 当空闲工作者检测到本地队列为空时，系统应通过任务窃取支持自适应负载均衡行为。 | Medium | Demonstration | E003, E004 | Explicit |

## 6. 数据需求

| ID | 数据实体/对象 | 需求 | 源证据 |
|---|---|---|---|
| DR-001 | 任务 | 任务应封装一次已提交的函数求值，并保留对其关联输入和计算结果的访问。 | E002 |
| DR-002 | 任务输入/输出 | 系统应接受 Python 函数输入作为任务输入数据，并生成函数返回值作为任务结果数据。 | E002 |
| DR-003 | 回调参数 | 对于回调执行，已完成任务应作为回调任务参数传递。 | E001, E003 |
| DR-004 | 工作者队列 | 系统应维护足以支持本地执行以及工作者或 rank 之间任务窃取的任务队列。 | E003 |
| DR-005 | 图像预处理数据 | 在文档化的图像预处理用例中，输入数据集由组织在子文件夹中的图像构成，每个子文件夹名称表示标签，输出为单个 HDF5 文件。 | E005 |

## 7. 约束

| ID | 约束 | 源证据 |
|---|---|---|
| C-001 | 该产品是一个通过 Python 模块接口（`import torc`）使用的 Python 库。 | E002 |
| C-002 | 该产品的内部运行依赖 MPI。 | E004 |
| C-003 | 某些文档化的回调行为假定每个 MPI 进程只有一个工作线程。 | E003 |
| C-004 | 测试中通过 `TORC_WORKERS` 环境变量体现了工作者数量配置。 | E002 |
| C-005 | 代码仓库材料在测试源文件中包含 Eclipse Public License v1.0 声明。 | E002 |

## 8. 验证与验收

| Requirement ID | Verification method | Acceptance basis |
|---|---|---|
| FR-001 | Test | 已提交任务完成，且 `wait` 仅在完成后返回 |
| FR-002 | Test | 对于每个已完成任务，`input()` 和 `result()` 返回预期值 |
| FR-003 | Demonstration | map 风格执行产生预期的并行求值行为 |
| FR-004 | Demonstration | 已完成任务被提供给回调任务，且回调在父任务的节点/进程上执行 |
| FR-005 | Demonstration | 多个任务按文档说明分发到可用工作者之间 |
| FR-006 | Demonstration | 本地队列为空的空闲工作者发出窃取请求并执行窃取到的任务 |
| FR-007 | Inspection | 文档和示例展示了一种跨共享/分布式内存平台的基于任务的方法 |
| FR-008 | Inspection | 文档说明了透明的内部 MPI 使用以及应用层允许使用传统 MPI |
| NFR-001 | Inspection | 文档说明了在共享内存和分布式内存平台上的运行 |
| NFR-002 | Inspection | 文档说明了与传统 MPI 代码的兼容性 |
| NFR-003 | Demonstration | 示例显示了并行执行下已用运行时间的降低 |
| NFR-004 | Analysis | 文档化用例报告了在 1024 个节点上的效率 >90% |
| NFR-005 | Demonstration | 任务窃取示例显示空闲工作者从另一个队列中获取任务 |

## 9. 可追溯性矩阵

| ID | 需求 | 类型 | 来源 | 证据类型 | 验证 | 置信度 |
|---|---|---|---|---|---|---|
| FR-001 | 接受已提交任务进行并行执行并等待完成 | Functional | E002, E001 | explicit | Test | High |
| FR-002 | 通过任务句柄暴露任务输入和结果 | Functional | E002 | explicit | Test | High |
| FR-003 | 支持并行 map 行为 | Functional | E001, E006 | explicit | Demonstration | Medium |
| FR-004 | 在父节点/进程上以已完成任务参数执行回调任务 | Functional | E001, E003 | explicit | Demonstration | Medium |
| FR-005 | 在可用工作者之间分发任务 | Functional | E001, E006 | explicit | Demonstration | Medium |
| FR-006 | 支持从非空队列中进行任务窃取 | Functional | E003 | explicit | Demonstration | High |
| FR-007 | 在共享/分布式内存平台上提供统一的基于任务的执行 | Functional | E004 | explicit | Inspection | High |
| FR-008 | 透明地在内部使用 MPI，并允许在应用层使用传统 MPI | Functional | E004 | explicit | Inspection | High |
| NFR-001 | 在共享内存和分布式内存平台上运行 | Non-functional | E004 | explicit | Inspection | High |
| NFR-002 | 保持与传统 MPI 代码兼容 | Non-functional | E004 | explicit | Inspection | High |
| NFR-003 | 支持在并行执行下降低运行时间；已展示快 4 倍的示例 | Non-functional | E001 | explicit | Demonstration | Medium |
| NFR-004 | 支持集群规模执行；用例中展示了在 1024 个节点上 >90% 的效率 | Non-functional | E005 | explicit | Analysis | Medium |
| NFR-005 | 通过任务窃取支持自适应负载均衡 | Non-functional | E003, E004 | explicit | Demonstration | High |
| DR-001 | 任务存储输入和结果 | Data | E002 | explicit | Inspection | High |
| DR-002 | 任务 I/O 由 Python 函数参数和返回值组成 | Data | E002 | explicit | Inspection | High |
| DR-003 | 已完成任务是回调输入 | Data | E001, E003 | explicit | Inspection | Medium |
| DR-004 | 队列支持本地执行和窃取 | Data | E003 | inferred | Inspection | Medium |
| DR-005 | 带标签的图像数据集文件夹被转换为 HDF5 输出 | Data | E005 | explicit | Inspection | Medium |
| C-001 | Python 模块接口约束 | Constraint | E002 | explicit | Inspection | High |
| C-002 | 内部 MPI 依赖 | Constraint | E004 | explicit | Inspection | High |
| C-003 | 某些回调示例中每进程单工作者的假设 | Constraint | E003 | explicit | Inspection | Medium |
| C-004 | 在测试中通过 `TORC_WORKERS` 配置工作者数量 | Constraint | E002 | explicit | Inspection | Medium |
| C-005 | 代码仓库测试源中存在 EPL v1.0 许可证声明 | Constraint | E002 | explicit | Inspection | Medium |
