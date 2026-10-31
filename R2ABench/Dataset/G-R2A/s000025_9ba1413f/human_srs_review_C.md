<!-- human_srs_review_A.md 由审阅者 A 生成。保留原始 human_srs_review.md。所有人类的判断都是英语的。 -->

# 人类 SRS 审查表

## 元数据

- 示例目录：`s000025_9ba1413f`
- 生成SRS：`final_srs.md`
- 证据包：`evidence_pack.json`
- 评测型号：`claude-opus-4-8`
- 生成于：`2026-06-05T15:39:59.738084Z`
- 原始模型响应：`model_srs_review_raw.md`
- 解析状态：`parsed`

## 总体模型意见

- 推荐：`revise`
- 置信度：`0.78`
- 理由：SRS 对于大多数声明来说都是有迹可循且保守的，但有几个要求夸大了证据：FR-005 断言当 E005 仅导入 verifyIdToken 而不显示调用时调用令牌验证； cookie 存储声明来自代码注释，而不是行为； FR-007/return-400 的细节稍微超出了截断证据显示的内容。

## 人类整体决策

- [ ] 接受
- [ ] 拒绝
- [x] 部分接受

原因：
> ACCEPT=1，PARTIAL_ACCEPT=1，REJECT=4，PARTIAL_ACCEPT=0。

## 积极的观察

- FR-001/FR-002 到 E001/E003 中的准确提取调用具有强大、准确的可追溯性，包括方法、内容类型和同源凭证。
- SRS 在注意到注销没有请求正文并且没有证据描述直接最终用户 UI 方面是适当保守的。
- Firebase 环境变量外部化 (FR-006/NFR-003/DR-004) 精确地基于 next.config.js (E006)。
- 验证方法和接受标准对于请求/响应行为是具体的。

## 候选人问题

### R001：不支持的声明

- 严重性：`major`
- 建议采取的措施：`partial_accept_as_issue`
- SRS 位置：FR-005；第 8 条；可追溯性 FR-005
- 证据IDs：E005

**索赔或差距**

FR-005 声明登录 API“应在处理登录请求时调用 Firebase 令牌验证”。 E005 导入 `verifyIdToken` 并包含有关解码令牌的注释，但显示的处理程序文本被截断，并且实际上不显示对 `verifyIdToken(token)` 的调用。

**模型意见**

导入和解释性注释的存在是比观察到的调用更弱的证据。显示的处理程序主体仅提取 `token` 并在缺少主体时返回 400；验证调用在块中不可见。这种说法可能部分是有抱负的（评论描述了预期的方法）。

**推荐人工检查**

在提交时打开pages/api/login.js，并确认`verifyIdToken(token)`（或等效的）是否在处理程序中实际调用，而不仅仅是导入。

**型号建议更改 SRS**

如果代码中不存在该调用，请将 FR-005 改写为：“登录 API 导入 Firebase ID 令牌验证 (`verifyIdToken`) 以在登录处理期间使用。”并将可追溯性置信度降低至“低”。如果存在呼叫，请添加特定线路作为证据。

可选的人工修订修复：
> 不需要削弱 FR-005。可选：把置信度从 Medium 提到 High，因为源码直接支持。

**人为决定**

- [ ] 接受
- [x] 拒绝
- [ ] 部分接受（`PARTIAL_ACCEPT`：混合声明；有些有效，有些无效）

可选的人工注释：
> 完整源码里 pages/api/login.js 确实调用了 verifyIdToken(token)，并在 session 中写入结果，所以“只导入未调用”不成立。

### R002：不支持的声明

- 严重性：`major`
- 建议采取的措施：`accept_as_issue`
- SRS 位置：第 6 节数据要求 – 存储行（“会话存储”）
- 证据IDs：E005

**索赔或差距**

SRS 引用 E005 指出“用户的 Firebase 令牌已解码并存储在 cookie 中”。 E005 仅将其显示为代码注释（“// 这里，我们解码用户的 Firebase 令牌并将其存储在 cookie 中”），而不是实现的行为。

**模型意见**

将描述性/愿望性评论视为系统行为是一种错误归因。该评论甚至建议使用快速会话“或类似”作为指导，这意味着它尚未实施。

**推荐人工检查**

验证 cookie/会话存储是否实际在 login.js 或 commonMiddleware 中实现，或者是否仅作为规划注释存在。

**型号建议更改 SRS**

将 Session 存储语句替换为：“代码注释表明了解码 Firebase 令牌并将其存储在 cookie 中的预期设计；现有证据并未证明实际的 cookie/会话存储。将信心标记为低。

可选的人工修订修复：
> 

**人为决定**

- [ ] 接受
- [x] 拒绝
- [ ] 部分接受（`PARTIAL_ACCEPT`：混合声明；有些有效，有些无效）

可选的人工注释：
> 完整源码显示 commonMiddleware 注入 cookie session，login 成功后写入 req.session.decodedToken 和 req.session.token；不是只有注释。

### R003：歧义

- 严重性：`minor`
- 建议采取的措施：`probably_ignore`
- SRS 位置：FR-003；第 8 条
- 证据IDs：E005

**索赔或差距**

FR-003 表示 API 在失踪尸体上返回“HTTP 状态 400”。 E005 显示设置状态但可能无法发送完整响应的 `return res.status(400);`（无 `.end()`/`.send()`/`.json()`）。

**模型意见**

接受标准“返回 HTTP 400”是可观察到的，但底层代码可能无法正确终止响应。这是值得注意的一个微小的可验证性细微差别，但外部可观察的 400 状态可能是可以接受的。

**推荐人工检查**

确认 res.status(400) 实际上在运行时框架中向客户端发出响应（Next.js API 路由）。

**型号建议更改 SRS**

可以选择附加到 FR-003 验证注释：“通过观察到的 HTTP 400 状态验证验收；确认响应已完全终止。”

可选的人工修订修复：
> 

**人为决定**

- [ ] 接受
- [x] 拒绝
- [ ] 部分接受（`PARTIAL_ACCEPT`：混合声明；有些有效，有些无效）

可选的人工注释：
> 这属于实现细节风险，不足以构成 SRS 缺陷。	无需修改 final_srs.md (line 96) 和验收项 line 148 (line 148)。

### R004：不可验证

- 严重性：`minor`
- 建议采取的措施：`accept_as_issue`
- SRS 位置：FR-007 / NFR-004
- 证据 IDs：E002、E004

**索赔或差距**

FR-007 枚举运行模式（前端+后端、仅前端、仅后端），但 E002/E004 README 文本的实际命令被截断/空白（“将同时启动两个...”）。 NFR-004（“与...OnFleet保持兼容”）无法客观地测试。

**模型意见**

运行模式看似真实，但具体命令不明显，因此对演示验收的支持较弱。 NFR-004 是一个模糊的兼容性声明，没有可衡量的标准。

**推荐人工检查**

检查 README/package.json 脚本以了解每种模式的实际启动命令；评估是否可以为 NFR-004 提供可验证的标准或降级为约束。

**型号建议更改 SRS**

对于FR-007，添加“未捕获证据的特定启动命令；根据 package.json 脚本进行验证。'对于 NFR-004，删除或重新声明为约束 C-002（已存在）以避免出现不可验证的 NFR。

可选的人工修订修复：
> 保留 FR-007，并把证据从 E002 扩展到 E002/E004 + README/package.json。删除或改写 NFR-004，避免不可验证 NFR。

**人为决定**

- [ ] 接受
- [ ] 拒绝
- [x] 部分接受（`PARTIAL_ACCEPT`：混合声明；有些有效，有些无效）

可选的人工注释：
> README/package.json 支持三种启动模式，所以 FR-007 不应弱化；但 NFR-004 “保持兼容”不可测，确实像约束而非 NFR。

### R005：架构_详细信息

- 严重性：`minor`
- 建议采取的措施：`accept_as_issue`
- SRS 位置：第二部分产品视角； C-002
- 证据 IDs：E002、E004

**索赔或差距**

SRS 将后端描述为严格的“两部分架构（Firebase 功能 + OnFleet）”。参考了真实架构图（architecture-2.png），但未合并；可能还有其他组件（数据库、Next.js 前端、身份验证）未反映。

**模型意见**

将后端“限制为”两个部分可能会低估图中所示的实际架构。 README 措辞“分成两部分”是指后端的运行方式，不一定是完整的架构约束。

**推荐人工检查**

查看 docs/images/architecture-2.png 以确认组件以及“两部分”是否是准确、完整的表征。

**型号建议更改 SRS**

将 C-002 软化为：“根据 README，后端被组织为 Firebase 功能（自定义 APIs）和 OnFleet（任务处理）；每个架构图可能存在其他组件。

可选的人工修订修复：
> 把 C-002 从 “constrained to a two-part architecture” 改成 “backend is described/organized as Firebase functions for custom APIs and OnFleet for task handling; architecture evidence also shows frontend and middleware interactions”。

**人为决定**

- [x] 接受
- [ ] 拒绝
- [ ] 部分接受（`PARTIAL_ACCEPT`：混合声明；有些有效，有些无效）

可选的人工注释：
> 架构图显示 End user、Frontend、Middleware、Backend 多层交互；README 的“两部分”只适合描述 backend 组织方式，不适合写成严格架构约束。

### R006：可追溯性

- 严重性：`minor`
- 建议采取的措施：`probably_ignore`
- SRS 位置：FR-006 / DR-004 / C-004
- 证据IDs：E006

**索赔或差距**

FR-006 和 C-004 源自 E006 (next.config.js)。资产加载器列表 (C-004) 和环境映射对于 E006 是准确的，但请注意 `API_URI` 已被注释掉 — SRS 正确地省略了它。遗漏没有问题，但置信度标签只能注明有限的 4 个环境变量。

**模型意见**

这里的可追溯性很强而且准确。次要：SRS 可以明确指出，仅公开了四个未注释的 FIREBASE_* 变量（API_URI 已注释掉）。

**推荐人工检查**

确认 env.js 中的其他位置没有暴露其他环境变量（这是 next.config.js 所要求的，但没有证据表明）。

**型号建议更改 SRS**

在 DR-004 中添加注释：“只有四个 FIREBASE_* 变量通过 next.config.js 公开； API_URI 存在但被注释掉。

可选的人工修订修复：
> 

**人为决定**

- [ ] 接受
- [x] 拒绝
- [ ] 部分接受（`PARTIAL_ACCEPT`：混合声明；有些有效，有些无效）

可选的人工注释：
> next.config.js 只公开四个 Firebase 变量，API_URI 被注释；env.js 只负责加载 dotenv，不额外公开变量。
