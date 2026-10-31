# 软件需求规格说明书

## 1. 引言

### 目的
本 SRS 定义了针对 `mendhak/gpslogger` 仓库在提交 `ab894229de5ef1fec726b8a9588e98089b9564c6` 时基于证据的软件需求。其涵盖了证据包中可见的受支持运行时行为、集成、数据处理和运行约束。

### 产品范围
GPSLogger 是一个基于 Android 的 GPS 日志应用程序/服务，用于获取位置更新、在应用程序内部分发这些更新，并支持可选的外部集成，包括 OpenStreetMap、Dropbox 和 OpenGTS。证据还表明存在面向 Android 开发的构建/导入工作流，以及至少一项功能依赖 Google Play Services。来源：`E001`、`E003`、`E004`、`E005`、`E006`。

### 目标读者
本文档面向：
- 维护与实现仓库一致行为的维护者和贡献者
- 验证受支持集成和平台兼容性的测试人员
- 配置项目所引用外部服务的集成人员

### 参考资料
- 仓库：`mendhak/gpslogger`
- 提交：`ab894229de5ef1fec726b8a9588e98089b9564c6`
- 证据来源：`E001`、`E002`、`E003`、`E004`、`E005`、`E006`

## 2. 总体描述

### 产品视角
该产品是一个围绕 GPS 日志服务和事件总线组织的 Android 应用程序。当获取到位置时，它会被发布到事件总线，并由多个 fragment 消费。可选外部服务需要单独配置凭据。来源：`E003`、`E004`。

### 产品功能概述
- 获取位置更新并发布以供应用内消费（`E003`）
- 支持可选的基于凭据的 OpenStreetMap 设置（`E001`、`E004`）
- 支持可选的基于凭据的 Dropbox 设置（`E001`、`E004`）
- 使用 UDP 将位置数据发送到 OpenGTS 端点（`E005`）
- 将位置数据编码为 GPRMC/NMEA 风格字符串以实现 OpenGTS 互操作性（`E005`）

### 用户类别
- 运行 Android 应用程序并配置可选服务集成的终端用户（`E001`、`E004`）
- 构建、导入和调试 Android 项目的开发人员（`E002`、`E006`）

### 运行环境
- 文档指出，Android 2.2 及以上版本的手机已安装所引用功能所需的 Google Play Services 框架（`E003`）
- Android 模拟器应为 Android 4.2.2（API 级别 17）或更高版本才能使用同一功能（`E003`）
- 开发环境需要 README 中列出的 Android SDK 组件（`E002`、`E006`）

### 假设与依赖
- 可选的 OpenStreetMap 集成依赖用户提供的 consumer key 和 consumer secret（`E001`、`E004`）
- 可选的 Dropbox 集成依赖用户提供的 app key 和 app secret（`E001`、`E004`）
- 某些功能依赖 Google Play Services 框架（`E003`）
- 如果未自动检测到，Android 项目导入依赖于包含 `sdk.dir` 的有效 `local.properties` 文件（`E002`、`E006`）

## 3. 外部接口需求

### 用户界面
证据未描述完整的应用内 UI。仓库证据确实支持：
- 消费位置事件的应用程序 fragment（`E003`）
- 在 OpenStreetMap 和 Dropbox 开发者控制台中获取凭据的外部设置步骤（`E001`、`E004`）

### 软件/API 接口
- 通过 `GPSLOGGER_OSM_CONSUMERKEY` 和 `GPSLOGGER_OSM_CONSUMERSECRET` 配置值进行 OpenStreetMap 集成（`E001`、`E004`）
- 通过 `GPSLOGGER_DROPBOX_APPKEY` 和 `GPSLOGGER_DROPBOX_APPSECRET` 配置值进行 Dropbox 集成（`E001`、`E004`）
- 用于开发/运行时支持的 Android SDK 和 Google Play Services 依赖（`E002`、`E003`、`E006`）
- 使用服务器、可选端口和可选路径的 OpenGTS 服务器接口（`E005`）

### 通信接口
- 使用 UDP 传输发送 OpenGTS 消息（`E005`）

### 数据交换格式
- OpenGTS 位置载荷可以编码为 GPRMC 字符串数据，并引用 NMEA0183 解析预期（`E005`）
- 配置数据通过用于外部集成和 Android SDK 路径的命名键/值条目提供（`E001`、`E002`、`E004`、`E006`）

## 4. 功能需求

| ID | 描述 | 触发器/输入 | 系统行为 | 输出 | 优先级 | 验证方式 | 来源证据 |
|---|---|---|---|---|---|---|---|
| FR-001 | 发布已获取的位置更新以供应用内消费。 | 获取到一个位置。 | 系统应将获取到的位置放入事件总线，以便消费它的 fragment 能够接收。 | 可供监听 fragment/组件使用的位置事件。 | 高 | 演示 | `E003` |
| FR-002 | 接受 OpenStreetMap 集成凭据。 | 启用 OpenStreetMap 设置且提供了凭据。 | 系统应接受 `GPSLOGGER_OSM_CONSUMERKEY` 和 `GPSLOGGER_OSM_CONSUMERSECRET` 作为可选 OpenStreetMap 集成的配置输入。 | OpenStreetMap 凭据值可用于应用程序配置。 | 中 | 检查 | `E001`、`E004` |
| FR-003 | 接受 Dropbox 集成凭据。 | 启用 Dropbox 设置且提供了凭据。 | 系统应接受 `GPSLOGGER_DROPBOX_APPKEY` 和 `GPSLOGGER_DROPBOX_APPSECRET` 作为可选 Dropbox 集成的配置输入。 | Dropbox 凭据值可用于应用程序配置。 | 中 | 检查 | `E001`、`E004` |
| FR-004 | 根据已配置的端点组成部分构建 OpenGTS 目标 URL。 | 需要一个 OpenGTS 传输目标。 | 系统应使用 server 值构建目标，并在存在这些值时追加 port 和 path。 | 形如 `server[:port][path]` 的目标字符串。 | 中 | 测试 | `E005` |
| FR-005 | 通过 UDP 发送 OpenGTS 消息。 | 可用于传输的 OpenGTS 消息、服务器和端口已就绪。 | 系统应创建一个发送到已配置服务器和端口的数据报包，并使用 UDP 发送该消息。 | 包含该消息的 UDP 数据包被传输到目标端点。 | 高 | 测试 | `E005` |
| FR-006 | 将位置数据编码为 GPRMC 以实现 OpenGTS 互操作性。 | 必须准备一个可序列化位置以供 OpenGTS 传输。 | 系统应将该位置编码为与所引用 NMEA0183 解析预期一致的 GPRMC 字符串数据。 | 位置的 GPRMC 格式字符串表示。 | 高 | 测试 | `E005` |

## 5. 非功能需求

| ID | 需求 | 质量属性 | 优先级 | 验证方式 | 来源证据 | 证据类型 |
|---|---|---|---|---|---|---|
| NFR-001 | 对于需要 Google Play Services 的功能，系统应可在运行 Android 4.2.2（API 级别 17）或更高版本的 Android 模拟器上运行。 | 兼容性 | 高 | 演示 | `E003` | 显式 |
| NFR-002 | 对于同一功能，系统应可在 README 所述已安装 Google Play Services 框架的 Android 2.2 及以上手机上运行。 | 兼容性 | 高 | 演示 | `E003` | 显式 |
| NFR-003 | 外部服务凭据应通过命名配置值提供，而不是直接嵌入运行时消息或端点字符串中。 | 可维护性/安全性 | 中 | 检查 | `E001`、`E004`、`E005` | 推断 |

## 6. 数据需求

| ID | 数据需求 | 类型 | 描述 | 验证方式 | 来源证据 | 证据类型 |
|---|---|---|---|---|---|---|
| DR-001 | 位置事件数据 | 运行时数据 | 获取到的位置数据应能够表示为可放入事件总线并由 fragment 消费的事件。 | 演示 | `E003` | 显式 |
| DR-002 | 可序列化位置数据 | 运行时数据 | OpenGTS 编码应接受 `SerializableLocation` 输入对象以转换为 GPRMC 字符串数据。 | 测试 | `E005` | 显式 |
| DR-003 | GPRMC 消息数据 | 输出数据 | 与 OpenGTS 兼容的位置输出应表示为 GPRMC 字符串数据。 | 测试 | `E005` | 显式 |
| DR-004 | 端点配置数据 | 配置数据 | OpenGTS 端点配置应由 server 组成，并且还可额外包括 port 和 path 值。 | 检查 | `E005` | 显式 |
| DR-005 | 外部集成凭据 | 配置数据 | 可选的 OpenStreetMap 和 Dropbox 集成应使用文档规定的命名 key/secret 配置值。 | 检查 | `E001`、`E004` | 显式 |
| DR-006 | Android SDK 路径配置 | 开发配置数据 | 当未发生环境检测时，项目应支持名为 `sdk.dir` 的 `local.properties` 条目来指定 Android SDK 位置。 | 检查 | `E002`、`E006` | 显式 |

## 7. 约束

| ID | 约束 | 类型 | 验证方式 | 来源证据 |
|---|---|---|---|---|
| C-001 | 开发环境应包含 Android SDK Build Tools `19.0.3`。 | 技术/构建 | 检查 | `E002`、`E006` |
| C-002 | 开发环境应包含 Android Support Repository、Android Support Library、Google Play services 和 Google Repository。 | 技术/构建 | 检查 | `E002`、`E006` |
| C-003 | 使用依赖 Google Play Services 的功能需要运行 Android 4.2.2（API 级别 17）或更高版本的模拟器，或满足所述框架可用性的手机环境。 | 平台/运行时 | 演示 | `E003` |
| C-004 | OpenGTS UDP 传输需要可解析的服务器地址和端口。 | 运行/网络 | 测试 | `E005` |

## 8. 验证与验收

| Requirement IDs | Verification Method | Acceptance Basis |
|---|---|---|
| `FR-001`, `DR-001`, `C-003`, `NFR-001`, `NFR-002` | 演示 | 兼容的 Android 运行时显示获取到的位置已被发布并可供消费它的 fragment 使用。 |
| `FR-002`, `FR-003`, `DR-004`, `DR-005`, `DR-006`, `C-001`, `C-002`, `NFR-003` | 检查 | 配置名称、受支持的端点字段以及文档化的平台/构建依赖与仓库证据一致。 |
| `FR-004`, `FR-005`, `FR-006`, `DR-002`, `DR-003`, `C-004` | 测试 | 单元测试或集成测试使用代表性输入确认 URL 构造、UDP 传输行为以及 GPRMC 编码行为。 |

## 9. 可追溯性矩阵

| ID | 需求 | 类型 | 来源 | 证据类型 | 验证方式 | 置信度 |
|---|---|---|---|---|---|---|
| FR-001 | 在事件总线上发布已获取的位置更新以供 fragment 消费。 | 功能 | `E003` | 显式 | 演示 | 高 |
| FR-002 | 接受 OpenStreetMap consumer key 和 consumer secret 配置。 | 功能 | `E001`、`E004` | 显式 | 检查 | 高 |
| FR-003 | 接受 Dropbox app key 和 app secret 配置。 | 功能 | `E001`、`E004` | 显式 | 检查 | 高 |
| FR-004 | 由 server、可选 port 和可选 path 构造 OpenGTS 目标字符串。 | 功能 | `E005` | 显式 | 测试 | 高 |
| FR-005 | 使用 UDP 数据报发送 OpenGTS 消息。 | 功能 | `E005` | 显式 | 测试 | 高 |
| FR-006 | 为 OpenGTS 将位置数据编码为 GPRMC 字符串数据。 | 功能 | `E005` | 显式 | 测试 | 高 |
| NFR-001 | 在模拟器 Android 4.2.2/API 17+ 上运行依赖 Google Play Services 的功能。 | 非功能 | `E003` | 显式 | 演示 | 中 |
| NFR-002 | 在已按说明安装框架的 Android 2.2+ 手机上运行依赖 Google Play Services 的功能。 | 非功能 | `E003` | 显式 | 演示 | 中 |
| NFR-003 | 通过命名配置值提供外部服务凭据。 | 非功能 | `E001`、`E004`、`E005` | 推断 | 检查 | 中 |
| DR-001 | 将获取到的位置数据表示为 fragment 可消费的事件总线数据。 | 数据 | `E003` | 显式 | 演示 | 中 |
| DR-002 | 接受 `SerializableLocation` 作为 OpenGTS 编码输入。 | 数据 | `E005` | 显式 | 测试 | 高 |
| DR-003 | 将 OpenGTS 输出表示为 GPRMC 字符串数据。 | 数据 | `E005` | 显式 | 测试 | 高 |
| DR-004 | 支持 OpenGTS 端点数据字段：server、可选 port、可选 path。 | 数据 | `E005` | 显式 | 检查 | 高 |
| DR-005 | 支持 OpenStreetMap 和 Dropbox 凭据的命名配置数据。 | 数据 | `E001`、`E004` | 显式 | 检查 | 高 |
| DR-006 | 支持带有 `sdk.dir` 的 `local.properties` 以指定 Android SDK 位置。 | 数据 | `E002`、`E006` | 显式 | 检查 | 高 |
| C-001 | 在开发环境中要求 Android SDK Build Tools `19.0.3`。 | 约束 | `E002`、`E006` | 显式 | 检查 | 高 |
| C-002 | 在开发环境中要求列出的 Android 支持与 Google 仓库/库。 | 约束 | `E002`、`E006` | 显式 | 检查 | 高 |
| C-003 | 将依赖 Google Play Services 的功能约束于所述 Android 运行环境。 | 约束 | `E003` | 显式 | 演示 | 中 |
| C-004 | 要求 OpenGTS UDP 传输具备可解析的服务器地址和端口。 | 约束 | `E005` | 显式 | 测试 | 高 |
