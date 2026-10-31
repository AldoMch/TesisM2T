# 软件需求规格说明书

## 1. 引言

### 目的
本 SRS 规定了在提交 `f0210012a9772dc0cf324cccac6596e3658d573d` 的 `VirtualMotionTracker` 仓库快照中已被证实的外部可观察需求。范围仅限于证据包中存在的面向 OpenVR 的初始化/关闭行为、路径暴露以及输入绑定工件。

### 产品范围
已证实的组件作为场景应用程序与 OpenVR 集成，在启动时验证 `IVRSystem` 接口，并为被跟踪的用户/身体位置暴露标准化的 OpenVR 路径字符串，同时为名为 `mycontroller` 的控制器类型提供旧版控制器绑定。源代码还暴露了该集成使用的 OpenVR 数据结构。

### 目标读者
本文档面向：
- 将该仓库与 OpenVR 集成的开发人员
- 验证 OpenVR 启动、关闭和绑定的测试工程师
- 审查接口和数据兼容性的维护人员

### 参考资料
- 仓库：`gpsnmeajp/VirtualMotionTracker`
- 仓库 URL：<https://github.com/gpsnmeajp/VirtualMotionTracker>
- 快照：<https://github.com/gpsnmeajp/VirtualMotionTracker/tree/f0210012a9772dc0cf324cccac6596e3658d573d>
- 证据来源：`E001` 至 `E006`

## 2. 总体描述

### 产品视角
已证实的产品部分是一个与 OpenVR 集成的组件。它通过 OpenVR 以 `VRApplication_Scene` 进行初始化，检查接口版本兼容性，并通过 OpenVR 运行时进行关闭。它还包含 OpenVR 路径常量和一个 JSON 控制器绑定文件。源证据：`E001`、`E002`、`E003`、`E004`。

### 产品功能概述
- 针对 OpenVR 进行初始化，并在启动成功时返回系统接口。(`E003`)
- 当所需的 OpenVR 接口版本不可用时拒绝初始化。(`E003`)
- 关闭 OpenVR 运行时并使先前获得的接口指针失效。(`E003`)
- 暴露用于用户/身体位置及相关 OpenVR 路径的标准化路径字符串。(`E001`、`E002`)
- 提供一个旧版绑定，将 `mycontroller` 右手输入映射到旧版动作输出。(`E004`)

### 用户类别
- 使用运行时初始化和关闭入口点的 OpenVR 应用程序集成人员。(`E003`)
- 使用控制器绑定 JSON 和 OpenVR 路径标识符的配置/集成用户。(`E001`、`E002`、`E004`)

### 运行环境
- 使用 `vrclient.dll` 和 `IVRSystem` 的 OpenVR 运行时环境。(`E003`)
- OpenVR 应用程序类型 `VRApplication_Scene`。(`E003`)

### 假设与依赖
- 该组件依赖 OpenVR 接口版本的有效性以实现成功启动。(`E003`)
- 绑定行为依赖名为 `mycontroller` 的控制器类型以及位于 `/actions/legacy` 下的 OpenVR 动作路径。(`E004`)

## 3. 外部接口需求

### 用户接口
所提供材料中没有证实任何面向终端用户的图形界面或命令行界面。

### 软件/API 接口
| 接口 | 需求摘要 | 来源 |
|---|---|---|
| OpenVR 初始化 API | 系统使用 OpenVR 初始化，应用程序类型为 `VRApplication_Scene`，验证 `IVRSystem_Version`，并在成功时返回 `OpenVR.System`，失败时返回 `null`。 | `E003` |
| OpenVR 关闭 API | 系统暴露关闭行为以卸载 `vrclient.dll`；关闭后接口指针无效。 | `E003` |
| OpenVR 路径标识符 | 系统暴露 OpenVR 路径字符串，包括 `/user/foot/left`、`/user/foot/right`、`/user/shoulder/left`、`/user/shoulder/right`、`/user/elbow/left`、`/user/elbow/right`、`/user/knee/left`、`/user/knee/right`、`/user/waist`、`/user/chest`、`/user/camera`、`/user/keyboard` 和 `/client_info/app_key`。 | `E001`、`E002` |

### 通信接口
除本地 OpenVR 运行时/库交互外，没有直接证实任何网络或进程间通信协议。

### 数据交换格式
| 格式 | 用途 | 来源 |
|---|---|---|
| JSON | 包含动作路径、输入路径、控制器类型和绑定元数据的控制器绑定定义。 | `E004` |
| 字符串路径标识符 | 表示用户/身体位置和客户端元数据路径的 OpenVR 路径值。 | `E001`、`E002` |

## 4. 功能需求

| ID | 描述 | 触发器/输入 | 系统行为 | 输出 | 优先级 | 验证方式 | 来源证据 |
|---|---|---|---|---|---|---|---|
| FR-001 | 作为 OpenVR 场景应用程序进行初始化。 | 调用方请求初始化。 | 系统应以应用程序类型 `VRApplication_Scene` 初始化 OpenVR。 | 初始化成功时提供 OpenVR 系统句柄。 | 高 | 测试 | `E003` |
| FR-002 | 当所需 OpenVR 接口版本不可用时拒绝启动。 | OpenVR 初始化完成，但 `IVRSystem_Version` 无效。 | 系统应关闭 OpenVR 运行时，将初始化错误设置为 `Init_InterfaceNotFound`，并返回 `null`。 | 通过 `null` 和接口未找到错误指示失败。 | 高 | 测试 | `E003` |
| FR-003 | 提供运行时关闭。 | 调用方请求关闭。 | 系统应调用 OpenVR 关闭行为并卸载运行时模块。 | 运行时被关闭，先前获得的接口指针变为无效。 | 高 | 演示 | `E003` |
| FR-004 | 暴露标准化的 OpenVR 用户/身体路径标识符。 | 使用组件请求 OpenVR 路径常量。 | 系统应提供左/右脚、左/右肩、左/右肘、左/右膝、腰部、胸部、摄像头、键盘和客户端应用程序键的路径字符串。 | 提供可用于集成的 OpenVR 兼容字符串标识符。 | 中 | 检查 | `E001`、`E002` |
| FR-005 | 为控制器类型 `mycontroller` 提供旧版绑定。 | OpenVR 为 `mycontroller` 加载旧版绑定定义。 | 系统应将 `/user/hand/right/input/a` 映射到 `/actions/legacy/in/right_axis1_press`，将 `/user/hand/right/input/c` 映射到 `/actions/legacy/in/right_a_press`，并将 `/user/hand/right/input/b` 映射到 `/actions/legacy/in/right_grip_press`。 | 可被 OpenVR 使用的 JSON 绑定定义。 | 中 | 测试 | `E004` |

## 5. 非功能需求

| ID | 质量属性 | 需求 | 优先级 | 验证方式 | 证据类型 | 来源证据 |
|---|---|---|---|---|---|---|
| NFR-001 | 兼容性 | 系统应在暴露 OpenVR 系统接口之前验证与 `IVRSystem_Version` 的兼容性。 | 高 | 测试 | explicit | `E003` |
| NFR-002 | 可靠性 | 关闭后，系统不应要求先前获得的 OpenVR 接口指针仍然有效。 | 高 | 演示 | explicit | `E003` |
| NFR-003 | 互操作性 | 控制器绑定应以 JSON 表示，并使用 OpenVR 风格的动作和输入路径字符串。 | 中 | 检查 | explicit | `E004` |

## 6. 数据需求

| ID | 数据项/实体 | 需求 | 来源证据 |
|---|---|---|---|
| DR-001 | OpenVR 路径标识符 | 系统使用用于用户/身体位置和客户端元数据的字符串路径标识符，包括 `/user/foot/left`、`/user/foot/right`、`/user/shoulder/left`、`/user/shoulder/right`、`/user/elbow/left`、`/user/elbow/right`、`/user/knee/left`、`/user/knee/right`、`/user/waist`、`/user/chest`、`/user/camera`、`/user/keyboard` 和 `/client_info/app_key`。 | `E001`、`E002` |
| DR-002 | 控制器绑定文档 | 系统存储一个 JSON 对象，其中包含 `bindings`、位于 `/actions/legacy` 下的动作路径、控制器输入路径、`controller_type`、`description` 和 `name`。 | `E004` |
| DR-003 | OpenVR 运行时姿态/时序数据 | 该集成使用 OpenVR 数据结构，其中包括被跟踪姿态和时序字段，例如 `TrackedDevicePose_t`、合成器基准值以及帧时序字段。 | `E005` |
| DR-004 | 原生/渲染设备数据 | 该集成使用 OpenVR 设备和渲染模型结构，包括原生设备句柄、设备类型、顶点位置/法线/纹理坐标以及纹理尺寸。 | `E006` |

## 7. 约束

| ID | 约束 | 来源证据 |
|---|---|---|
| C-001 | 该集成受限于 OpenVR 运行时及其接口版本控制模型。 | `E003` |
| C-002 | 初始化受限于 OpenVR 应用程序类型 `VRApplication_Scene`。 | `E003` |
| C-003 | 控制器输入映射受限于以 JSON 表达的 OpenVR 动作路径和输入路径约定。 | `E004` |
| C-004 | 身体位置标识符受限于由 `/user/...` 及相关路径常量表示的 OpenVR 路径命名空间。 | `E001`、`E002` |

## 8. 验证与验收

| 需求 ID | 验证方法 | 验收依据 |
|---|---|---|
| FR-001 | 测试 | 当 OpenVR 和接口版本有效时，以 `VRApplication_Scene` 初始化会返回非 `null` 的系统接口。 |
| FR-002 | 测试 | 无效的 `IVRSystem_Version` 会导致关闭、`Init_InterfaceNotFound` 以及返回 `null`。 |
| FR-003 | 演示 | 关闭后，运行时被卸载，先前的接口指针不再可供使用。 |
| FR-004 | 检查 | 暴露的常量与已证实的 OpenVR 路径字符串一致。 |
| FR-005 | 测试 | 加载绑定文件会暴露控制器类型 `mycontroller` 的已证实右手输入映射。 |
| NFR-001 | 测试 | 在暴露系统接口之前，启动会拒绝无效的 `IVRSystem_Version`。 |
| NFR-002 | 演示 | 关闭会使先前的接口指针无效。 |
| NFR-003 | 检查 | 绑定数据被编码为 JSON，并带有 OpenVR 风格的路径字段。 |

## 9. 可追溯性矩阵

| ID | 需求 | 类型 | 来源 | 证据类型 | 验证方式 | 置信度 |
|---|---|---|---|---|---|---|
| FR-001 | 作为 OpenVR 场景应用程序进行初始化 | 功能 | `E003` | explicit | 测试 | 高 |
| FR-002 | 在 `IVRSystem_Version` 无效时拒绝启动 | 功能 | `E003` | explicit | 测试 | 高 |
| FR-003 | 提供运行时关闭并使指针失效 | 功能 | `E003` | explicit | 演示 | 高 |
| FR-004 | 暴露标准化的 OpenVR 用户/身体路径标识符 | 功能 | `E001`、`E002` | explicit | 检查 | 高 |
| FR-005 | 为 `mycontroller` 提供旧版绑定 | 功能 | `E004` | explicit | 测试 | 高 |
| NFR-001 | 在使用前验证 OpenVR 接口兼容性 | 非功能 | `E003` | explicit | 测试 | 高 |
| NFR-002 | 关闭后不依赖接口指针有效性 | 非功能 | `E003` | explicit | 演示 | 高 |
| NFR-003 | 以 JSON 和 OpenVR 路径字符串表示绑定 | 非功能 | `E004` | explicit | 检查 | 高 |
| DR-001 | 使用 OpenVR 路径字符串数据项 | 数据 | `E001`、`E002` | explicit | 检查 | 高 |
| DR-002 | 存储控制器绑定 JSON 数据 | 数据 | `E004` | explicit | 检查 | 高 |
| DR-003 | 使用 OpenVR 姿态和时序结构 | 数据 | `E005` | explicit | 检查 | 中 |
| DR-004 | 使用原生/渲染设备结构 | 数据 | `E006` | explicit | 检查 | 中 |
| C-001 | OpenVR 运行时/接口版本依赖 | 约束 | `E003` | explicit | 检查 | 高 |
| C-002 | `VRApplication_Scene` 应用程序类型约束 | 约束 | `E003` | explicit | 检查 | 高 |
| C-003 | OpenVR JSON 动作/输入路径约束 | 约束 | `E004` | explicit | 检查 | 高 |
| C-004 | OpenVR `/user/...` 路径命名空间约束 | 约束 | `E001`、`E002` | explicit | 检查 | 高 |
