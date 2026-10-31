<!-- human_srs_review_A.md 由审阅者 A 生成。保留原始 human_srs_review.md。所有人类的判断都是英语的。 -->

# 人类 SRS 审查表

## 元数据

- 示例目录：`s000064_6a496ab6`
- 生成SRS：`final_srs.md`
- 证据包：`evidence_pack.json`
- 评测型号：`claude-opus-4-8`
- 生成于：`2026-06-05T15:59:53.874653Z`
- 原始模型响应：`model_srs_review_raw.md`
- 解析状态：`parsed`

## 总体模型意见

- 推荐：`revise`
- 置信度：`0.78`
- 理由：SRS 在证据包中有着充分的依据，大多数声明都可以清晰地追溯到 E001-E006。然而，它省略了记录的内部 API（支持 API），通过不一致地将架构/设计参考标记为“面向支持的 API 分区”夸大了证据，并在没有确认的情况下处理一些推论（e.g.、Node.js、替代外部服务）。一些验证条目仅供检查，不可测试。应根据真实图检查架构细节。

## 人类整体决策

- [ ] 接受
- [ ] 拒绝
- [x] 部分接受

原因：
> ACCEPT=4，PARTIAL_ACCEPT=1，REJECT=2，PARTIAL_ACCEPT=0。

## 积极的观察

- FR-001 到 FR-006 和 DR-001 到 DR-006 清晰明确地追踪到 E006 和 E004；域到数据存储的映射忠实于证据。
- 可追溯性矩阵分配合理反映证据强度的差异化置信水平（e.g.、NFR-002/NFR-003、DR-005 的中值）。
- NFR-002 准确地捕获了来自 E002 的 Let's Encrypt DNS-01 挑战流程详细信息，而没有夸大其词。
- SRS 适当地将文档构建为特定提交的设计基线要求，并避免捏造证据中不存在的性能/容量数据。

## 候选人问题

### R001：缺少需求

- 严重性：`major`
- 建议采取的措施：`accept_as_issue`
- SRS 位置：第 4 节功能要求；第一节 产品范围
- 证据IDs：E004

**索赔或差距**

E004 明确列出了五个内部 APIs：身份验证 API、用户管理 API、图书管理 API、EC 站点 API 和支持 API（支持API）。 SRS 定义了身份验证、用户、书籍和 EC 站点 APIs（FR-001 到 FR-004）的功能要求，但没有提供支持 API 的功能要求，尽管在范围内命名了“支持/消息管理上下文”。

**模型意见**

支持 API 是有证据支持的内部 API，在功能要求中被省略。 SRS 在范围文本中部分承认它，但没有为其提供并行的 FR，从而在范围和功能覆盖范围之间造成不一致。

**推荐人工检查**

在 docs/12_backend/01_design/README.md 中确认支持 API 与其他四个一起列为内部 API，并决定是否添加专用 FR。

**型号建议更改 SRS**

添加 FR-007：“系统应提供与其他后端 APIs 分离的支持 API。”触发器：来自客户端或管理界面的与支持相关的请求。系统行为：通过专用支持API处理请求。输出：与支持相关的响应。优先级：高。验证：检查。证据来源：E004。添加相应的追溯行。

可选的人工修订修复：
> 在 FR-004 后或 FR-006 后新增。FR-007：系统应提供与其他后端 API 分离的支持/信息 API，用于处理来自客户端或管理界面的支持相关请求，并返回支持相关响应。优先级：High；验证方式：Inspection；证据：E004。同时在第 8 节和第 9 节补充对应验收与追踪行。

**人为决定**

- [x] 接受
- [ ] 拒绝
- [ ] 部分接受（`PARTIAL_ACCEPT`：混合声明；有些有效，有些无效）

可选的人工注释：
> E004 明确列出 5 个内部 API：认证、用户、书籍、EC 站点、支持 API。SRS 只给前 4 个写了 FR，漏掉了支持 API；架构图里也有 Support Service。

### R002：可追溯性

- 严重性：`minor`
- 建议采取的措施：`accept_as_issue`
- SRS 位置：第 3 部分软件/API 接口 - '内部后端 APIs' 行； DR-005 / 第 1 节范围“支持/消息管理上下文”
- 证据 IDs：E004、E006

**索赔或差距**

SRS 将“面向支持的 API 分区”（E004 的支持 API）与“消息管理”（E006 的消息管理 DB / NoSQL）合并在一起。这些是不同的证据项：E004 列出了支持 API，而 E006 列出了消息管理 DB。 SRS 短语“支持/消息管理上下文”合并了两个独立的概念。

**模型意见**

支持 API (E004) 和消息管理 DB (E006) 可能是也可能不是同一个域。证据并未证明支持 API 使用消息管理 NoSQL DB。将它们合并是一个不受支持的推论。

**推荐人工检查**

检查存储库是否将支持 API 链接到消息管理 NoSQL 存储，或者它们是否是独立的域。如果未链接，请将范围和 DR-005 中的两个概念分开。

**型号建议更改 SRS**

在第 1 节产品范围中，将“支持/消息管理上下文”替换为两个不同的项目：“支持 API（内部，根据 E004）”和“消息管理数据域（NoSQL，根据 E006）”。除非有证据支持，否则不要断言它们之间存在关系。

可选的人工修订修复：
> 第 1 节 Product scope。把：Support/message management context 改为两项：Support API / support information domain ；Message management data domain backed by NoSQL 位置：第 3 节 Software/API interfaces。把内部 API 描述改为：Authentication, user management, book management, EC site, and support API partitioning are documented. DR-005 仍保留消息管理 NoSQL，但不要和 Support API 绑定。

**人为决定**

- [x] 接受
- [ ] 拒绝
- [ ] 部分接受（`PARTIAL_ACCEPT`：混合声明；有些有效，有些无效）

可选的人工注释：
> SRS 把 Support API 和 Message management DB / NoSQL 合成了“Support/message management context”。源码证据没有证明支持 API 一定使用消息管理 NoSQL；这两个概念应分开。

### R003：不支持的声明

- 严重性：`minor`
- 建议采取的措施：`partial_accept_as_issue`
- SRS位置：第2节操作环境-“后端运行时：GCP/GKE相关环境上基于容器的服务”； C-002
- 证据 IDs：E002、E006

**索赔或差距**

SRS 为后端运行时断言“GCP/GKE 相关环境”。 E006 确认 GCP 和容器部署； E002 确认 GKE 集群凭证检索 (gcloud 容器集群 get-credentials)。 GKE 得到合理支持，但“GKE 相关”是对冲/模糊的，并且容器后端 APIs 和 GKE 之间的链接在 E006 中具体是推断性的，而不是显式的。

**模型意见**

GKE 推断是合理的（E002 引用 GKE 集群），但 E006 仅表示“容器”。 “GKE 相关”这一措辞含糊不清。这是低风险的，但应该精确。

**推荐人工检查**

验证后端 APIs 是否显式部署到 GKE 与通用容器。 E002 在操作上引用 GKE 集群；确认这是后端运行时。

**型号建议更改 SRS**

在操作环境中，将“GCP/GKE 相关环境上基于容器的服务”替换为“GCP 上基于容器的服务（根据 E006 进行容器部署；根据 E002 操作使用的 GKE 集群凭证）”。

可选的人工修订修复：
> 第 2 节 Operating environment。把：Container-based services on GCP/GKE-related environment 改为：Container-based backend services on GCP; operational documentation includes GKE cluster credential retrieval for cluster access. 第 7 节 C-002。改为：The target cloud environment is GCP; available operational procedures include GCE VM setup and GKE credential retrieval.

**人为决定**

- [ ] 接受
- [ ] 拒绝
- [x] 部分接受（`PARTIAL_ACCEPT`：混合声明；有些有效，有些无效）

可选的人工注释：
> E006 支持 GCP 和容器化部署；E002 支持 GKE 凭证获取。但“GCP/GKE-related environment”太模糊，不能强推所有后端服务都明确部署在 GKE 上。

### R004：范围

- 严重性：`minor`
- 建议采取的措施：`probably_ignore`
- SRS 位置：第 2 节假设和依赖关系；第 7 节 C-004
- 证据IDs：E004

**索赔或差距**

E004 将 Google 图书 API 和 Stripe 列为已采用（已采用）的外部服务，但也列出了正在考虑的替代方案（正在考虑的替代方案）：亚马逊广告 API、乐天图书 API、PayPal。 SRS 正确说明了所采用的服务，但没有注意到设计文档正在考虑的替代方案，这是范围/依赖性稳定性的相关上下文。

**模型意见**

SRS 的采用服务声明是准确的。对于需求基线来说，省略“正在考虑”的替代方案是可以接受的，但作为依赖性稳定性警告值得注意，因为设计明确地将这些替代方案标记为尚未最终。

**推荐人工检查**

在 E004 中确认亚马逊广告 API、乐天图书 API 和 PayPal 被列为考虑中的候选者，并决定是否将此记录为依赖项注释。

**型号建议更改 SRS**

向 C-004 添加注释：“设计文档还列出了正在考虑的替代候选服务（亚马逊广告 API、乐天图书 API、PayPal）；当前基线 (E004) 中未采用这些。

可选的人工修订修复：
> 

**人为决定**

- [ ] 接受
- [x] 拒绝
- [ ] 部分接受（`PARTIAL_ACCEPT`：混合声明；有些有效，有些无效）

可选的人工注释：
> E004 的确列出了 Amazon Advertising API、楽天Book API、PayPal 作为“考虑中”的替代方案，但 SRS 只记录当前采用的 Google Books API 和 Stripe 是合理的。候选方案不属于当前需求基线的必需内容。

### R005：不可验证

- 严重性：`minor`
- 建议采取的措施：`accept_as_issue`
- SRS 位置：第 4 部分（FR-001 至 FR-006）；第 8 节 验证
- 证据 IDs：E004、E006

**索赔或差距**

所有功能需求都使用针对架构/设计文档的“检查”作为验证方法。由于证据是设计文档 README 内容（而不是运行行为），因此需求描述了记录的意图而不是可测试的运行时行为。像“架构文档显示专用 X API”这样的验收基础验证文档的存在，而不是功能行为。

**模型意见**

鉴于证据完全是 READMEs 的设计，基于检查的验证是站得住脚的。然而，FR 措辞（“应通过...处理请求”）意味着运行时行为无法直接从证据中验证。验证方法应明确声明它确认设计一致性，而不是运行时功能。

**推荐人工检查**

决定 FRs 是否应构建为设计一致性要求（可通过检查验证）或运行时行为要求（需要测试）。相应地调整验收基础语言。

**型号建议更改 SRS**

在第 8 节中，澄清验收基础措辞 e.g.、FR-002：“设计文档（E004、E006）定义了专用的、容器部署的用户管理 API；验证确认设计一致性，而不是运行时行为。”

可选的人工修订修复：
> 

**人为决定**

- [ ] 接受
- [x] 拒绝
- [ ] 部分接受（`PARTIAL_ACCEPT`：混合声明；有些有效，有些无效）

可选的人工注释：
> 不重要。

### R006：架构_详细信息

- 严重性：`minor`
- 建议采取的措施：`accept_as_issue`
- SRS 位置：第 2 部分 产品视角/运行环境；整体架构映射
- 证据IDs：E006

**索赔或差距**

架构映射（Firebase Auth、三个容器 APIs、每个域 MySQL、用于消息的 NoSQL、用于缩略图的对象存储、L7 LB）源自 E006 文本，应根据真实架构图进行交叉检查(architecture.jpeg) 以确认没有遗漏或歪曲任何组件或关系。

**模型意见**

基于文本的映射与 E006 非常吻合。由于存在真实图，视觉交叉检查将增强对组件数量、连接性（e.g.、LB 放置、哪些服务位于 LB 后面）以及 README 文本中未捕获的任何数据存储关系的信心。

**推荐人工检查**

将 SRS 架构映射与 docs/12_backend/01_design/images/architecture.jpeg 进行比较以确保完整性（e.g.、LB 到服务连接、任何 CDN/缓存、支持 API 数据存储）。

**型号建议更改 SRS**

审查图表后，将第 2 节产品视角与 architecture.jpeg 进行协调；添加图中存在但 README 派生文本中不存在的任何组件/关系（以图表结果为条件）。

可选的人工修订修复：
> 第 2 节 Product perspective。把后端架构列表扩展为：The backend architecture includes a BFF/API gateway layer for native-app and admin-console access, a microservice layer including user, book, store/EC, authentication, support/information, admin, and notification services, and storage/external dependencies including MySQL, Firestore/NoSQL, Cloud Storage, payment API, book-search API, push notification, and email notification providers. 位置：第 2 节 Assumptions and dependencies 或第 7 节 Constraints 增加一条一致性说明：The textual design identifies Google Books API as the adopted book-search service, while the backend architecture diagram labels Rakuten Books API; this discrepancy should be resolved before treating either as the sole confirmed book-search dependency.

**人为决定**

- [x] 接受
- [ ] 拒绝
- [ ] 部分接受（`PARTIAL_ACCEPT`：混合声明；有些有效，有些无效）

可选的人工注释：
> 架构图比当前 SRS 更丰富。当前 SRS 漏了 BFF/API Gateway、Native/Admin Gateway、Support Service、Admin Service、Notification Service、FCM、SendGrid 等关键架构角色。另一个重要点是：文本证据写 Google Books API，但架构图标的是楽天ブックスAPI，存在源间不一致，不能直接二选一。

### R007：不支持的声明

- 严重性：`minor`
- 建议采取的措施：`accept_as_issue`
- SRS 位置：第 2 节 运行环境；缺少对 Node.js 的引用
- 证据 IDs：E001、E004

**索赔或差距**

E004 提到了“Golang - 目录结构”和“Node.js - 目录结构”，这意味着后端可能同时使用 Golang 和 Node.js。 C-001 仅说明 Golang（对于用户 API，根据 E001）。 SRS 没有提及 Node.js，这可能低估了实现语言的范围。

**模型意见**

C-001 的范围正确为用户 API (E001)。但是，E004 对 Node.js 目录结构的引用表明至少部分后端使用 Node.js。这是 SRS 中省略的有证据支持的细节。

**推荐人工检查**

在E004中验证Node.js是否是任何后端服务的实现语言；如果是这样，请将其与 Golang 一起记为约束。

**型号建议更改 SRS**

添加C-006：'后端设计同时参考Golang和Node.js目录结构，表示跨服务的多种实现语言（E004）；用户 API 特别使用 Golang (E001)。

可选的人工修订修复：
> 第 7 节 Constraints，新增 C-006。建议写成：Backend service API documentation identifies Golang for several internal APIs; backend design documentation also references a Node.js-style directory structure for gateway/BFF design. This indicates mixed design references, but does not prove that every backend service uses Node.js.同时第 9 节补 C-006 追踪行，证据用 E001、E004。

**人为决定**

- [x] 接受
- [ ] 拒绝
- [ ] 部分接受（`PARTIAL_ACCEPT`：混合声明；有些有效，有些无效）

可选的人工注释：
> E004 确实引用了 Golang 和 Node.js 目录结构；但 User/Book/Store/Support API 的 README 都写的是 Golang。Node.js 更像 BFF/API Gateway 设计参考，不能写成“后端服务整体同时使用 Node.js”。
