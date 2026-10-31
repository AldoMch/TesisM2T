<!-- human_srs_review_A.md 由审阅者 A 生成。保留原始 human_srs_review.md。所有人类的判断都是英语的。 -->

# 人类 SRS 审查表

## 元数据

- 示例目录：`s000010_87e6341f`
- 生成SRS：`final_srs.md`
- 证据包：`evidence_pack.json`
- 评测型号：`claude-opus-4-8`
- 生成于：`2026-06-05T15:36:51.763005Z`
- 原始模型响应：`model_srs_review_raw.md`
- 解析状态：`parsed`

## 总体模型意见

- 推荐：`revise`
- 置信度：`0.74`
- 理由：SRS 在 E001-E003 中具有良好的基础，可追溯性总体较强。然而，证据来自两个不同的子项目（Flutter-Dart 和 Flutter-Android 变体），省略了真实图的标题/Azure-AKS 范围，并且比 README 要点支持更坚定地陈述了一些要求（流验证、一条消息/一项约束、Docker 推送）。这些需要有针对性的修改和人工检查。

## 人类整体决策

- [ ] 接受
- [ ] 拒绝
- [x] 部分接受

原因：
> ACCEPT=4，PARTIAL_ACCEPT=2，REJECT=1，PARTIAL_ACCEPT=0。

## 积极的观察

- 从每个 FR/NFR/DR 到具体证据 IDs (E001-E003) 的强大、明确的可追溯性，具有清晰的可追溯性矩阵。
- 将 NFR-004 和 DR 相关的推断项标记为“推断”时应适当克制，而不是夸大其词。
- 四个中间件端点（addRecipe、ListAllRecipes、ListAllIngredientsAtHome、GetAllIngredientsForRecipe）的功能要求准确反映了 E003 README 枚举。
- 约束部分忠实地捕获了记录的设置依赖项（Dart/protoc PATH、Go/protoc-gen-go、gRPC-Gateway 依赖项、服务器运行先决条件）。

## 候选人问题

### R001：可追溯性

- 严重性：`major`
- 建议采取的措施：`accept_as_issue`
- SRS 位置：第 2 节操作环境；第 4 节 FR-003/FR-004；证据参考 E002
- 证据 IDs：E001、E002、E003

**索赔或差距**

E002（服务器 README）来自 `Flutter-Android-app-and-gRPC-go-server-on-Azure-Kubernetes-Service/server`，而 E001 和 E003 来自 `Flutter-Dart-app-and-gRPC-go-server-on-Azure-Kubernetes-Service`。 SRS 将所有三个视为一个连贯的堆栈，而没有注意到它们来自两个不同的子项目。

**模型意见**

在两个并行样本目录中混合证据可能会将系统误认为是单个集成产品。 Dart客户端（E001）和中间件（E003）属于一个文件夹；引用的服务器 (E002) 来自 Android 变体文件夹。 Dart 文件夹内还可能存在未检索到的服务器 README。

**推荐人工检查**

验证Dart子项目是否有自己的服务器README，并确认Android变体服务器README是否合法适用于Dart客户端/中间件堆栈。决定是否应分割或注释范围。

**型号建议更改 SRS**

在第 1 节“产品范围”和第 2 节“产品视角”中，添加注释：“服务器要求（FR-003、FR-004、NFR-003）由 Flutter-Android 变体服务器 README (E002) 证明；客户端 (E001) 和中间件 (E003) 来自 Flutter-Dart 变体。假设它们共享相同的 gRPC 服务器合约，等待确认。”

可选的人工修订修复：
> 将服务器需求证据改为 Dart 变体 server README；在范围/产品视角中说明目标栈是 Flutter-Dart 客户端 + Dart 变体中间件 + Dart 变体服务器。Android 变体 E002 应降级为历史检索误配或旁证。

**人为决定**

- [x] 接受
- [ ] 拒绝
- [ ] 部分接受（`PARTIAL_ACCEPT`：混合声明；有些有效，有些无效）

可选的人工注释：
> 检查更进一步确认：Dart 变体本身有自己的 server/README.md，当前 SRS 不应继续用 Android 变体 E002 作为服务器主证据。

### R002：范围

- 严重性：`major`
- 建议采取的措施：`partial_accept_as_issue`
- SRS 位置：第 1 部分产品范围；第二节 产品功能总结
- 证据IDs：E002

**索赔或差距**

真实架构图和文件夹名称引用“Azure Kubernetes 服务 (AKS)”，但 SRS 范围仅限于本地 Docker 容器化，并忽略任何 Kubernetes/Azure 部署范围。

**模型意见**

存储库目录和图表 URL 显式命名 AKS 部署。 SRS 可能低估了部署范围。但是，检索到的 README 文本 (E002) 仅证明本地 Docker 构建/运行/推送，而不是 AKS，因此这可能是合法的证据有限的范围决定。

**推荐人工检查**

检查 AKS/Kubernetes 的架构 diagram.png 和任何部署 README/清单。决定是添加 AKS 部署范围声明，还是由于缺乏文本证据而将其明确标记为超出范围。

**型号建议更改 SRS**

添加到第 1 节产品范围：“注意：存储库目录和架构图引用了 Azure Kubernetes 服务 (AKS) 部署，但没有检索到的 README 证据指定 AKS 部署步骤；因此，AKS 部署被认为超出了已证实的范围，有待架构图和部署清单的审查。

可选的人工修订修复：
> 在产品范围、运行环境、约束/NFR 中补充：服务器支持本地 Kubernetes 部署，并有 AKS 部署清单证据。不要只写“本地 Docker 容器化”。

**人为决定**

- [x] 接受
- [ ] 拒绝
- [ ] 部分接受（`PARTIAL_ACCEPT`：混合声明；有些有效，有些无效）

可选的人工注释：
> 接受，比模型的“部分接受”更强。架构图明确显示 “Hosted in Azure Kubernetes Service”，Dart 变体也有 local k8s README 和 deploy-azure.yaml。

### R003：不可验证

- 严重性：`minor`
- 建议采取的措施：`accept_as_issue`
- SRS 位置：FR-006 / NFR-002 / 第 8 节验证
- 证据IDs：E003

**索赔或差距**

E003 仅声明“请注意，GRPC 网关支持服务器端流”作为附加观察。 SRS 将其提升为可测试的要求，即中间件“应支持其服务器端流行为”并以测试验收为基础“保留服务器端流兼容性”。

**模型意见**

README 注释是对 gRPC 网关功能的描述，而不是具有可观察验收标准的记录的产品要求。 “网关行为保留服务器端流”的接受基础很难从书面证据中得到验证。

**推荐人工检查**

确认 ListAllRecipes 是否实际实现为服务器流式 RPC，以及是否存在或打算进行具体的流式测试。

**型号建议更改 SRS**

将 NFR-002 改写为：“当 ListAllRecipes 作为服务器流式 RPC 实现时，gRPC 网关暴露不应破坏该流式行为（作为 E003 中的功能说明进行证明，而不是经过测试的保证）。”将置信度标记为推断而非显式。

可选的人工修订修复：
> 保留流式需求，但改证据来源：引用 proto、server handler、gateway 生成代码。验收改为“食谱列表查询通过 HTTP 网关返回流式响应结构”，不要只写笼统“preserves streaming”。

**人为决定**

- [ ] 接受
- [ ] 拒绝
- [x] 部分接受（`PARTIAL_ACCEPT`：混合声明；有些有效，有些无效）

可选的人工注释：
> 部分接受。仅凭 E003 README 确实过强；但 proto 明确 ListAllRecipes 是 server-streaming，server handler 逐条发送，gateway 用 stream forward。

### R004：歧义

- 严重性：`minor`
- 建议采取的措施：`accept_as_issue`
- SRS 位置：FR-007 / DR-005（ListAllIngredientsAtHome“一次一条消息”）
- 证据IDs：E003

**索赔或差距**

E003 表示“请注意，这一次仅支持 1 条消息”——过去时且含糊不清。 SRS 将其转换为前瞻性要求（“一次应处理一条消息”），就好像它是一个设计约束一样。

**模型意见**

“支持”这个措辞暗示了当时的限制或怪癖，不一定是必需的行为。将其视为规范性“应当”要求可能会误述意图。

**推荐人工检查**

检查原型/中间件实现以确定一次一条消息是有意的约束还是偶然的限制。

**型号建议更改 SRS**

将 DR-005/FR-007 改写为：“观察到的行为 (E003)：ListAllIngredientsAtHome 一次仅支持一条消息。有待确认这是否是有意的限制或实施限制。将置信度降级为推断。

可选的人工修订修复：
> 把 FR-007/DR-005 改成接口约束：HTTP 网关普通请求体一次映射一个食材消息；原生 gRPC 接口支持客户端流。不要写成系统必须拒绝多消息。置信度降为“推断/接口限制”。

**人为决定**

- [x] 接受
- [ ] 拒绝
- [ ] 部分接受（`PARTIAL_ACCEPT`：混合声明；有些有效，有些无效）

可选的人工注释：
> 接受并细化。proto 是 client-streaming，server 可循环接收多条；README 的“只支持 1 message”更像 HTTP gateway 普通请求示例/限制，而不是服务层硬约束。

### R005：歧义

- 严重性：`minor`
- 建议采取的措施：`accept_as_issue`
- SRS 位置：FR-008 / DR-004（GetAllIngredientsForRecipe“仅一项”）
- 证据IDs：E003

**索赔或差距**

与 R004 相同：E003 括号“请注意，请求只能有一个项目”被重述为具有高置信度和测试接受度的硬输入约束。

**模型意见**

README 括号中不清楚“一项”是强制验证规则还是使用说明。接受基础“仅接受一项请求”意味着未证明拒绝行为。

**推荐人工检查**

在原型/中间件中验证多项目请求是否被拒绝或根本不支持。

**型号建议更改 SRS**

将 DR-004 改写为：“记录 GetAllIngredientsForRecipe 请求 (E003) 以包含单个项目；执行/拒绝多项目请求尚未得到证实。”相应软化FR-008验收依据。

可选的人工修订修复：
> 把 DR-004 改成数据结构说明：每个食谱食材查询请求消息包含单个食谱对象；不声明拒绝多项数组。FR-008 验收改为“单食谱请求返回对应食材流”。另建议统一命名，源码实际是 GetIngredientsForAllRecipes。

**人为决定**

- [x] 接受
- [ ] 拒绝
- [ ] 部分接受（`PARTIAL_ACCEPT`：混合声明；有些有效，有些无效）

可选的人工注释：
> 接受并细化。proto 每个请求消息只有一个 recipe 字段，但 RPC 本身是双向流，server 可处理多个请求消息；没有证据证明“多项请求会被拒绝”。

### R006：不支持的声明

- 严重性：`minor`
- 建议采取的措施：`accept_as_issue`
- SRS 位置：FR-005 / 第 8 节（addRecipe 返回“有效端点响应”）
- 证据IDs：E003

**索赔或差距**

未定义接受基础“addRecipe 的curl 调用返回有效的端点响应”； E003 仅将“Curl the addRecipe 端点”列为步骤，而不指定请求/响应协定。

**模型意见**

没有证明响应模式、状态代码或成功标准。验收标准无法按照书面形式进行明显验证。

**推荐人工检查**

找到 addRecipe 的原型定义和任何示例 curl 请求/响应，以定义具体的接受标准。

**型号建议更改 SRS**

FR-005 接受：将“返回有效端点响应”替换为“返回与 addRecipe 原型合约一致的 HTTP 2xx 响应（一旦定位，将从原型中指定响应模式）”。

可选的人工修订修复：
> 将“valid endpoint response”改为明确验收：新增食谱 HTTP 调用返回 2xx，响应体符合新增食谱响应契约，并包含成功标志。

**人为决定**

- [ ] 接受
- [ ] 拒绝
- [x] 部分接受（`PARTIAL_ACCEPT`：混合声明；有些有效，有些无效）

可选的人工注释：
> 部分接受。README 没定义响应，但 proto、swagger、handler 都定义了：响应含 success 布尔值，handler 返回成功。

### R007：缺少需求

- 严重性：`minor`
- 建议采取的措施：`probably_ignore`
- SRS 位置：第 4 节 / 第 7 节（Docker 推送和 Android APK 生成）
- 证据 IDs：E001、E002

**索赔或差距**

E002 记录了 Docker 推送到注册表工作流程（登录 + 推送最新标签），E001 提到为 Android 手机创建 APK；两者都没有被捕获为功能需求（只有 C-005 部分涵盖推送）。

**模型意见**

这些是经过验证的开发人员/操作人员工作流程。尽管它们可能被认为超出了产品范围，但将它们作为功能需求的省略只是对范围的轻描淡写。

**推荐人工检查**

决定图像发布和 APK 打包是否应成为功能要求或保留限制/超出范围的构建步骤。

**型号建议更改 SRS**

添加FR-009（可选）：“系统应支持通过docker登录+推送（E002）将服务器Docker镜像发布到注册表。” FR-010：“客户端应支持生成 Android APK 以安装在 Android 设备上 (E001)。”

可选的人工修订修复：
> 

**人为决定**

- [ ] 接受
- [x] 拒绝
- [ ] 部分接受（`PARTIAL_ACCEPT`：混合声明；有些有效，有些无效）

可选的人工注释：
> 拒绝作为必修缺陷。Docker push 和 APK 生成是开发/发布工作流，不一定是产品功能需求；当前 C-005 已覆盖 Docker 登录依赖。
