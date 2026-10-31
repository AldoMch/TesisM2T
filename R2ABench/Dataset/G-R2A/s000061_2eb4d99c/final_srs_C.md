# 软件需求规格说明书

## 1. 引言

### 1.1 目的
本 SRS 规定了仓库 `aws-solutions/iot-device-simulator` 在提交 `6ee7b0261b9ba2a045f533e54be603d3af939e9b` 时仓库快照的、具有证据支持的需求。其范围仅限于由仓库证据包直接支持的行为和接口。

### 1.2 产品范围
有证据支持的系统范围包括：
- 一个用于 IoT Device Simulator 的 AWS API Gateway REST API 构造，
- 一条 CloudFormation 自定义资源交互路径，
- 用于从 Amazon S3 加载仿真车辆路线数据的功能。

### 1.3 目标读者
- 将该解决方案集成到 AWS 环境中的部署人员和运维人员
- 使用 REST API 的 API 集成人员
- 验证部署和路线加载行为的测试人员
- 评估可追踪功能和接口需求的维护人员

### 1.4 参考资料
- 仓库：`aws-solutions/iot-device-simulator`
- 仓库 URL：https://github.com/aws-solutions/iot-device-simulator
- 快照 URL：https://github.com/aws-solutions/iot-device-simulator/tree/6ee7b0261b9ba2a045f533e54be603d3af939e9b
- 证据来源：
  - `source/infrastructure/lib/api.ts` (E003, E004)
  - `source/custom-resource/test/index.test.ts` (E002)
  - `source/simulator/lib/device/generators/vehicle/dynamics/dynamics-model.js` (E005, E006)
  - `source/resources/routes/route-b.json` (E001)

## 2. 总体描述

### 2.1 产品视角
该产品是一组托管于 AWS 的解决方案组件。证据表明其包括：
- 一个 API Gateway REST API 前端，
- 基于 Lambda 的微服务集成，
- CloudFormation 自定义资源处理，
- 由 S3 支持的车辆模拟器路线数据检索。

### 2.2 产品功能概述
- 暴露已部署的 REST API 端点和 API 标识符
- 接受包括 `GET`、`POST`、`PUT`、`DELETE` 和 `OPTIONS` 在内的 REST 方法
- 验证请求参数和请求体
- 支持包括 `X-Api-Key` 在内的 CORS 标头
- 构建并返回 CloudFormation 自定义资源响应体
- 从 S3 加载路线数据并组装用于仿真的路线状态

### 2.3 用户类别
- 调用模拟器 REST API 的 API 客户端
- 调用自定义资源的 AWS 部署工作流
- 从 S3 加载车辆路线状态的模拟器组件

### 2.4 运行环境
- AWS API Gateway REST API（`REGIONAL` 端点类型）
- AWS Lambda
- Amazon S3
- AWS CloudFormation 自定义资源执行上下文
- 环境变量，包括 `AWS_REGION`、`SOLUTION_ID`、`SOLUTION_VERSION`、`STACK_NAME` 和 `ROUTE_BUCKET`

### 2.5 假设和依赖
- 路线检索依赖于由 `ROUTE_BUCKET` 标识的 S3 存储桶，以及从 `routeName` 派生的对象键。(E005)
- API 部署依赖于 API Gateway 请求验证和阶段部署配置。(E004)
- 自定义资源行为依赖于 AWS 提供的调用上下文和解决方案环境变量。(E002)

## 3. 外部接口需求

### 3.1 用户界面
在所提供材料中，没有关于终端用户图形界面的证据。

### 3.2 软件/API 接口

| 接口 | 需求概述 | 来源 |
|---|---|---|
| REST API | 系统暴露一个具有已部署端点和 API ID 的 API Gateway REST API。 | E003, E004 |
| 请求验证 | API 验证请求参数和请求体。 | E004 |
| CloudFormation 自定义资源 | 系统在自定义资源处理期间构建 CloudFormation 响应体。 | E002 |
| S3 路线检索 | 模拟器使用存储桶 `ROUTE_BUCKET` 和对象键 `routeName` 从 S3 检索路线 JSON。 | E005 |

### 3.3 通信接口

| 接口 | 需求概述 | 来源 |
|---|---|---|
| API 方法 | 支持的方法包括 `GET`、`POST`、`PUT`、`DELETE` 和 `OPTIONS`。 | E004 |
| CORS 标头 | 允许的标头包括 `Content-Type`、`X-Amz-Date`、`Authorization` 和 `X-Api-Key`。 | E004 |

### 3.4 数据交换格式

| 格式 | 描述 | 来源 |
|---|---|---|
| JSON 路线文件 | 路线数据从 S3 进行 JSON 解析，并包含分阶段的路线段。 | E001, E005 |
| JSON 访问日志 | API 访问日志使用带有标准字段的 JSON。 | E004 |
| CloudFormation 响应体 | 自定义资源处理为 CloudFormation 构建响应体。 | E002 |

## 4. 功能需求

| ID | 描述 | 触发器/输入 | 系统行为 | 输出 | 优先级 | 验证方式 | 来源证据 |
|---|---|---|---|---|---|---|---|
| FR-001 | 为 IoT Device Simulator 暴露一个已部署的 REST API。 | API 构造的部署或初始化 | 系统应创建一个 API Gateway REST API，部署它，并提供 API 端点和 API ID。 | 可访问的 API 部署元数据，包括端点和 API ID | 高 | 检查 | E003, E004 |
| FR-002 | 为 API 访问支持核心 REST 方法和 CORS 标头。 | 客户端请求或 CORS 预检请求 | 系统应允许方法 `GET`、`POST`、`PUT`、`DELETE` 和 `OPTIONS`，并应允许标头 `Content-Type`、`X-Amz-Date`、`Authorization` 和 `X-Api-Key`。 | 与允许的方法和标头兼容的 API 响应；CORS 状态码 `200` | 高 | 测试 | E004 |
| FR-003 | 验证传入的 API 请求。 | 包含参数和/或请求体的客户端请求 | 系统应通过已配置的 API 请求验证器验证请求参数和请求体。 | 已接受的请求继续处理；无效请求被 API Gateway 验证拒绝 | 高 | 检查 | E004 |
| FR-004 | 构建 CloudFormation 自定义资源响应体。 | CloudFormation 自定义资源调用 | 系统应使用调用上下文和已配置环境为自定义资源响应构建响应体。 | CloudFormation 响应体 | 中 | 测试 | E002 |
| FR-005 | 为车辆仿真从 S3 加载路线数据。 | 包含 `routeInfo.routeName` 的快照 | 系统应使用 `routeName` 键从由 `ROUTE_BUCKET` 命名的 S3 存储桶读取路线对象，解析 JSON 负载，并组装包括路线元数据和源自快照字段在内的路线状态。 | 包含路线数据和路线相关状态的路线状态对象 | 高 | 测试 | E005 |
| FR-006 | 传播路线加载失败。 | S3 路线检索期间发生失败 | 当从 S3 检索路线失败时，系统应抛出遇到的错误。 | 返回给调用方的错误 | 中 | 测试 | E005 |

## 5. 非功能需求

| ID | 质量属性 | 需求 | 优先级 | 验证方式 | 来源证据 | 证据类型 |
|---|---|---|---|---|---|---|
| NFR-001 | 可维护性 / 可观测性 | API 部署应将访问日志输出到日志目标，使用带有标准字段的 JSON。 | 中 | 检查 | E004 | 明确 |
| NFR-002 | 可运维性 | API 部署应使用 `INFO` 方法日志级别。 | 中 | 检查 | E004 | 明确 |
| NFR-003 | 可追踪性 / 可观测性 | API 部署应启用追踪。 | 中 | 检查 | E004 | 明确 |
| NFR-004 | 兼容性 | API 端点类型应为 `REGIONAL`。 | 中 | 检查 | E004 | 明确 |

## 6. 数据需求

### 6.1 数据实体和对象

| ID | 数据实体 | 需求 | 来源证据 |
|---|---|---|---|
| DR-001 | 路线段 | 路线数据应支持包含 `stage`、`start`、`end` 和 `km` 字段的分阶段段；`start` 和 `end` 为坐标数组。 | E001 |
| DR-002 | 路线状态 | 路线加载输出应包括 `routeName`、`odometer`、`routeStage`、`burndown`、`burndownCalc`、`routeEnded`、`route` 和 `randomTriggers`。 | E005 |
| DR-003 | 路线源对象 | 路线负载应作为 JSON 对象存储在 S3 中，并从 UTF-8 文本解析。 | E005 |

### 6.2 输入/输出数据

| 数据流 | 输入 | 输出 | 来源证据 |
|---|---|---|---|
| API 请求验证 | 请求参数和请求体 | API Gateway 中的验证通过/失败 | E004 |
| 自定义资源 | 调用上下文和环境变量 | CloudFormation 响应体 | E002 |
| 路线加载 | `routeInfo.routeName`、`ROUTE_BUCKET`、快照字段 | 已解析的路线状态对象或抛出的错误 | E005 |

## 7. 约束

| ID | 约束 | 来源证据 |
|---|---|---|
| C-001 | REST API 被约束为使用阶段名称 `prod` 的 API Gateway 部署。 | E004 |
| C-002 | API 配置被约束为允许的方法 `GET`、`POST`、`PUT`、`DELETE` 和 `OPTIONS`。 | E004 |
| C-003 | 路线加载被约束为使用存储桶环境变量 `ROUTE_BUCKET` 和键 `routeName` 进行 S3 对象检索。 | E005 |
| C-004 | 自定义资源执行受环境变量 `AWS_REGION`、`SOLUTION_ID`、`SOLUTION_VERSION` 和 `STACK_NAME` 约束。 | E002 |
| C-005 | 证据中的仓库源文件声明 SPDX 许可证标识符 `Apache-2.0`。 | E006 |

## 8. 验证与验收

| 需求 ID | 验证方法 | 验收标准 |
|---|---|---|
| FR-001 | 检查 | API 构造定义显示已部署的 REST API，并暴露端点和 API ID。 |
| FR-002 | 测试 | 请求和预检交互展示允许的方法、标头以及 `200` CORS 状态行为。 |
| FR-003 | 检查 | API 配置包括一个已启用请求参数和请求体验证的请求验证器。 |
| FR-004 | 测试 | 自定义资源测试确认在提供的调用上下文下构建了 CloudFormation 响应体。 |
| FR-005 | 测试 | 给定有效的 `routeName` 和 `ROUTE_BUCKET`，路线加载返回具有所需字段的已解析路线状态。 |
| FR-006 | 测试 | S3 检索失败会导致路线加载操作抛出遇到的错误。 |
| NFR-001 | 检查 | API 部署配置显示已启用带有标准字段的 JSON 访问日志。 |
| NFR-002 | 检查 | API 部署配置显示 `INFO` 方法日志级别。 |
| NFR-003 | 检查 | API 部署配置显示已启用追踪。 |
| NFR-004 | 检查 | API 配置指定端点类型为 `REGIONAL`。 |
| DR-001 | 检查 | 示例路线数据包含 `stage`、`start`、`end` 和 `km` 字段。 |
| DR-002 | 检查 | 路线加载逻辑返回列出的路线状态字段。 |
| DR-003 | 检查 | 路线加载逻辑将 S3 对象体解析为 UTF-8 JSON 文本。 |
| C-001 | 检查 | API 部署配置指定阶段 `prod`。 |
| C-002 | 检查 | API 配置限制为列出的 HTTP 方法。 |
| C-003 | 检查 | 路线加载逻辑使用 `ROUTE_BUCKET` 和 `routeName` 进行 S3 检索。 |
| C-004 | 检查 | 自定义资源测试上下文包含列出的环境变量。 |
| C-005 | 检查 | 证据文件头包含 SPDX 标识符 `Apache-2.0`。 |

## 9. 可追踪性矩阵

| ID | 需求 | 类型 | 来源 | 证据类型 | 验证方式 | 置信度 |
|---|---|---|---|---|---|---|
| FR-001 | 暴露具有端点和 API ID 的已部署 REST API | 功能 | E003, E004 | 明确 | 检查 | 高 |
| FR-002 | 支持列出的 REST 方法和 CORS 标头 | 功能 | E004 | 明确 | 测试 | 高 |
| FR-003 | 验证请求参数和请求体 | 功能 | E004 | 明确 | 检查 | 高 |
| FR-004 | 构建 CloudFormation 自定义资源响应体 | 功能 | E002 | 明确 | 测试 | 中 |
| FR-005 | 从 S3 加载路线数据并组装路线状态 | 功能 | E005 | 明确 | 测试 | 高 |
| FR-006 | 传播路线加载失败 | 功能 | E005 | 明确 | 测试 | 高 |
| NFR-001 | 输出带有标准字段的 JSON 访问日志 | 非功能 | E004 | 明确 | 检查 | 高 |
| NFR-002 | 使用 `INFO` 方法日志级别 | 非功能 | E004 | 明确 | 检查 | 高 |
| NFR-003 | 启用追踪 | 非功能 | E004 | 明确 | 检查 | 高 |
| NFR-004 | 使用 `REGIONAL` 端点类型 | 非功能 | E004 | 明确 | 检查 | 高 |
| DR-001 | 路线段包含 `stage`、`start`、`end`、`km` | 数据 | E001 | 明确 | 检查 | 高 |
| DR-002 | 路线状态包括命名路线和快照字段 | 数据 | E005 | 明确 | 检查 | 高 |
| DR-003 | 路线负载从 S3 中的 UTF-8 JSON 解析 | 数据 | E005 | 明确 | 检查 | 高 |
| C-001 | API 阶段为 `prod` | 约束 | E004 | 明确 | 检查 | 高 |
| C-002 | API 方法限制为列出的动词 | 约束 | E004 | 明确 | 检查 | 高 |
| C-003 | 路线加载依赖于 `ROUTE_BUCKET` 和 `routeName` | 约束 | E005 | 明确 | 检查 | 高 |
| C-004 | 自定义资源依赖于 AWS 解决方案环境变量 | 约束 | E002 | 明确 | 检查 | 中 |
| C-005 | 源证据声明 Apache-2.0 许可证标识符 | 约束 | E006 | 明确 | 检查 | 高 |
