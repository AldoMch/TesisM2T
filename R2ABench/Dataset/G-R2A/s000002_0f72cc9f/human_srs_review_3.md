# Human SRS Review Sheet

## Metadata

- Sample directory: `s000002_0f72cc9f`
- Generated SRS: `final_srs.md`
- Evidence pack: `evidence_pack.json`
- Review model: `claude-opus-4-8`
- Generated at: `2026-06-05T15:27:37.075021Z`
- Raw model response: `model_srs_review_raw.md`
- Parse status: `parsed`

## Overall Model Opinion

- Recommendation: `revise`
- Confidence: `0.72`
- Rationale: The SRS is generally well-traced to evidence and conservative in most claims. However, several requirements overstate or misattribute behavior (e.g., credential submission flow, NFR-002 deterministic phrasing), the VR/scene-based content domain (Lobby, Louvre, Berlin, etc.) is understated, and the architecture diagram is not referenced despite being available. A few traceability tags are weak. Targeted revisions are warranted before acceptance.

## Overall Human Decision

- [ ] Accept
- [ ] Reject
- [x] Partial accept

Reason:
> 服务端用户控制器需求(FR-003/004/005)与 bcrypt 安全需求扎实,整体可接受但需修订。R003(signup/signin 仅为展示组件、捕获与提交逻辑共享于 App.js,SRS 夸大了两表单各自捕获)、R004(NFR-002 "deterministic" 措辞超出 E005 可证)、R005(FR-001 把 E005 当 signup 专属证据,实为共享处理器)、R006(submitFn 提交步骤缺失,以能力级补、不指定端点)、R007(bcrypt 命名统一为 bcrypt-nodejs)均成立、接受。R001(VR 多场景被低估)部分接受:按 E006 import 枚举场景成立,但断言其为"核心产品"依赖仓库名/架构图、不接受。R002(架构图)已读取 architecture1.png 核对,Web Client(A-Frame/React/React-Router)↔ Web Server(Node/Express/DigitalOcean)↔ Redis/MariaDB(Users/Likes/Photos/Comments)+ AWS S3 图片存储均被证实,改为接受、据图补充组件与通信关系。

## Positive Observations

- Server-side user controller requirements (FR-003 create, FR-004 findAll/findOne, FR-005 comparePassword) are accurately and directly traced to E001/E002.
- NFR-001 (bcrypt comparison instead of plaintext equality) is a strong, evidence-backed security requirement.
- The SRS appropriately records explicit absence of privacy/retention/migration evidence rather than inventing requirements.
- Verification methods and acceptance bases are largely observable and tied to concrete UI/code behaviors (e.g., .error element display, recursion termination).
- Traceability matrix with confidence levels is present and mostly well-aligned to evidence chunks.

## Candidate Issues

### R001: scope

- Severity: `major`
- Suggested action: `needs_human_check`
- SRS location: Section 1 Product scope; Section 2 Product functions summary
- Evidence IDs: E006

**Claim or gap**

The SRS describes the product narrowly as 'authentication and client interaction capabilities' and 'paragraph-oriented content,' but E006 shows the client imports many scene components (Lobby, SF, Louvre, Berlin, Milan, Rome, Hack, Camera, Sky, Plane, TextPlane) indicating a VR/immersive multi-scene experience that is the apparent core product.

**Model opinion**

The repository name (escape-reality), the architecture diagram, and the extensive A-Frame scene imports strongly suggest the product's primary purpose is a VR/immersive multi-location experience, not merely authentication. The SRS understates the core domain and frames it as incidental.

**Recommended human check**

Inspect react-client/src/components/App.js and the referenced scene components (Lobby, Louvre, Berlin, etc.) to confirm the product is a multi-scene VR experience. Review architecture1.png.

**Model proposed SRS change**

In Section 1 Product scope, add a bullet: 'A multi-scene A-Frame/VR client composed of distinct location scenes (e.g., Lobby, Louvre, Berlin, Milan, Rome, SF, Hack) rendered via aframe-react (E006).' Adjust the Purpose sentence to acknowledge the immersive scene-based experience as a primary capability rather than secondary.

Optional human revised fix:
> 部分采用。① 采用:在 Section 1 Product scope 增加一条,按 E006 实际 import 枚举场景组件——"由多个地点场景(Lobby、Louvre、Berlin、Milan、Rome、SF、Hack 等)经 aframe-react 渲染的多场景 A-Frame 客户端(E006)"。这些 import 在 E006 明确可见。② 不采用:不要据此把场景体验改写为"primary capability/核心产品"。E006 只证明这些组件被 import 存在,未提供任何场景行为/导航/交互证据;"核心是 VR 沉浸体验"依赖仓库名 escape-reality 与架构图的推断,证据不足。建议把场景渲染列为已证能力之一,与认证并列,而非武断判定主次。

**Human decision**

- [ ] Accept
- [ ] Reject
- [x] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> 部分接受(major)。成立:E006 明确 import 了 Lobby/SF/Louvre/Berlin/Milan/Rome/Hack/Camera/Sky/Plane/TextPlane,SRS 仅泛称"scene-based rendering"、未枚举,可按证据补全场景组件清单。不成立:把这些升格为"apparent core product / primary purpose is VR"依赖仓库名与架构图(均不在可分析证据中),且 import 存在 ≠ 行为有据。故接受枚举、不接受重定主次。注:SRS Product scope 已含 A-Frame 场景渲染一条,并非完全忽略。

### R002: architecture_detail

- Severity: `major`
- Suggested action: `needs_human_check`
- SRS location: Section 2 Product perspective; References
- Evidence IDs: none

**Claim or gap**

A ground-truth architecture diagram exists (diagrams/architecture1.png) but is neither referenced nor reconciled against the SRS's client-server description.

**Model opinion**

The SRS infers a client-server architecture from controller code, but does not cite or validate against the provided architecture diagram. Architectural claims (e.g., what server endpoints exist, how the React client communicates) should be checked against the diagram.

**Recommended human check**

Open diagrams/architecture1.png and confirm the described client-server structure, the communication mechanism between React client and the user controller, and whether any components (DB, API routes, VR scene server) are missing from the SRS.

**Model proposed SRS change**

Add to Section 1 References: 'Architecture diagram: diagrams/architecture1.png.' Add a note in Section 2 Product perspective stating the client-server topology should be validated against architecture1.png, and list any additional components shown there.

Optional human revised fix:
> 定论前查看 diagrams/architecture1.png。该图不在证据包(本条 Evidence IDs=none),客户端-服务端拓扑、React 客户端与 user controller 的通信机制、是否有 DB/API 路由/VR 场景服务器等都需核图确认。可先在 References 列出该图、在 Section 2 加"拓扑待对照 architecture1.png 验证"的注记,但任何具体组件关系须核图后再写。SRS 现以 "appears to be a client-server web application" 的保守措辞表述,本身未越界。

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> 

### R003: unsupported_claim

- Severity: `major`
- Suggested action: `needs_human_check`
- SRS location: FR-001 / FR-002 (System behavior, Output)
- Evidence IDs: E003, E004, E005

**Claim or gap**

FR-001 and FR-002 claim distinct credential capture for separate sign-up vs sign-in forms with state capture, but the evidence (E003, E004) shows signup.jsx and signin.jsx are presentational components calling props.onEmailChange/onPasswordChange; the actual state capture and submitFn live in App.js (E005) shared across both. The mapping of capture to two separate forms with independent behavior is partially inferred.

**Model opinion**

E005 shows a single onEmailChange/onPasswordChange/submitFn in App.js feeding both views. The SRS's split into FR-001 and FR-002 with separate 'captured email/password state' per form may overstate separation. The credential submission behavior (submitFn) is also visible in E005 but is truncated and not captured as a requirement.

**Recommended human check**

Confirm in App.js whether email/password state and submission are shared handlers used by both signup and signin views, and whether the submission flow (submitFn) posts credentials to the server.

**Model proposed SRS change**

Revise FR-001/FR-002 system behavior to note that credential capture handlers (onEmailChange/onPasswordChange) and submission are implemented in the shared App component (E005), with signup.jsx/signin.jsx providing presentational input fields and cross-navigation (E003/E004). Consider adding FR-008 for credential submission once the submitFn target is verified.

Optional human revised fix:
> 采用模型建议:改写 FR-001/FR-002 系统行为,说明凭据捕获处理器(onEmailChange/onPasswordChange)与提交逻辑实现在共享的 App 组件(E005),而 signup.jsx/signin.jsx 只提供展示性输入字段与跨页导航(E003/E004)。E003/E004 可见两组件均为 `props => (...)` 纯展示、回调 `props.onEmailChange/onPasswordChange`;E005 的 App.js 持有 state 与 submitFn,两视图共用。故现 SRS 把"每个表单各自捕获独立 state"夸大了分离度。新增 FR-008(提交)见 R006,待 submitFn 目标确认后再加。

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> Issue 成立(major)。E003/E004 显示 signup.jsx、signin.jsx 是纯展示组件(`props => (...)`,仅回调 onEmailChange/onPasswordChange);E005(App.js)持有 email/password state 与 submitFn,被两视图共享。SRS 的 FR-001/FR-002 把捕获描述为两个表单各自独立捕获 state,夸大了分离。应改述为"共享处理器 + 展示组件",有据,接受。

### R004: ambiguity

- Severity: `minor`
- Suggested action: `needs_human_check`
- SRS location: NFR-002 / FR-006
- Evidence IDs: E005

**Claim or gap**

NFR-002 phrases sequential content retrieval as 'deterministic' reliability with 'set the final paragraph state exactly once.' The evidence (E005) shows a recursion terminating at titleIndex === allTitles.length calling setStateParagraph(result), but does not establish determinism guarantees (e.g., ordering under async fetch races).

**Model opinion**

The recursion is sequential by construction (each fetch callback triggers the next), so ordering is plausible, but 'deterministic' and 'reliability' framing may overstate a verifiable quality attribute. The 'exactly once' claim is reasonable from the termination branch but the truncated code should be confirmed.

**Recommended human check**

Review the full recurse/fetch implementation in App.js to confirm setStateParagraph is invoked once at termination and that fetches truly run in sequence (not in parallel).

**Model proposed SRS change**

Reword NFR-002 to: 'The client shall process titles sequentially via recursive fetch callbacks, invoking the final state-setting operation once when the title index equals the title list length (E005).' Remove the unsupported 'deterministic' qualifier unless verified.

Optional human revised fix:
> 采用模型建议:把 NFR-002 改为"客户端通过递归 fetch 回调按序处理各 title,在 titleIndex 等于 title 列表长度时调用最终状态设置操作一次(E005)",去掉无据的 "deterministic/reliability" 限定。E005 可见递归在 `titleIndex === allTitles.length` 终止并调用 `setStateParagraph(result)`,支持"按序 + 终止时设一次",但不支持"确定性"这类需排除异步竞态的质量保证。Traceability 矩阵中 NFR-002 的同类 "deterministically" 措辞一并改。

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> Issue 成立(minor)。E005 显示递归 fetch 在 `titleIndex === allTitles.length` 终止时 `setStateParagraph(result)`,可证"顺序处理 + 终止设一次";但 "deterministic/reliability" 暗含对异步竞态下顺序的保证,证据未确立(且代码截断)。应去掉该限定、改为可观察的顺序+单次设置表述,接受。

### R005: traceability

- Severity: `minor`
- Suggested action: `accept_as_issue`
- SRS location: FR-001 evidence (E003, E005); Data exchange / E005 attribution
- Evidence IDs: E003, E004, E005

**Claim or gap**

FR-001 cites E005 for sign-up capture, but E005 (App.js) contains shared handlers and content fetch logic, not sign-up-specific behavior. The evidence linkage between presentational components (E003/E004) and the App.js handlers (E005) is conflated.

**Model opinion**

The traceability is broadly correct but imprecise: E005 supports the existence of capture/submit handlers generally, not sign-up-specific capture. Tightening evidence attribution improves verifiability.

**Recommended human check**

Verify which component owns the email/password state and confirm whether sign-up and sign-in share the same handlers.

**Model proposed SRS change**

In the traceability matrix, annotate that E003/E004 support the presentational input fields and E005 supports the shared state/submission handlers, rather than implying E005 is sign-up specific.

Optional human revised fix:
> 采用模型建议:在 Traceability 矩阵中注明 E003/E004 支撑的是展示性输入字段、E005 支撑的是共享的 state/提交处理器,而非暗示 E005 为 signup 专属。与 R003 一致:E005 的 App.js 是 signup/signin 共用,FR-001 引 E005 作 signup 捕获证据属归因不精确,收紧归因即可,无需删除引用。

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> Issue 成立(minor)。E005(App.js)含共享处理器与内容 fetch 逻辑,并非 signup 专属;FR-001 引 E005 支撑"signup 捕获"属归因不精确。按"E003/E004=展示字段、E005=共享 state/提交"收紧追溯归因,提升可验证性,接受。与 R003 同源,属追溯层面的精修。

### R006: missing_requirement

- Severity: `minor`
- Suggested action: `needs_human_check`
- SRS location: Section 4 Functional Requirements (credential submission)
- Evidence IDs: E005

**Claim or gap**

E005 shows a submitFn that grabs email/password and is annotated 'Submit email and password for verification,' but no functional requirement captures the client-side credential submission to the server.

**Model opinion**

Submission of captured credentials for verification is a core authentication step visible in evidence but absent from the functional requirements, which only cover capture (FR-001/002) and server-side compare (FR-005). The connecting submission step is missing.

**Recommended human check**

Inspect submitFn in App.js to determine the submission target (endpoint/route) and add a requirement for client credential submission.

**Model proposed SRS change**

Add FR-008: 'The client shall submit captured email and password values for verification upon form submission (E005).' Specify the server endpoint after verifying submitFn's request target.

Optional human revised fix:
> 采用模型建议,保守落地:补 FR-008 "客户端在表单提交时,将捕获的 email、password 提交以供验证(E005)"。E005 可见 `submitFn()` 抓取 email/password 并带注释 "Submit email and password for verification",支持"存在提交步骤"。但片段在此截断,提交目标端点不可见——故 FR-008 只到"提交以供验证"为止,不写具体 endpoint/路由,待核 submitFn 请求目标后再补。

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> Issue 成立(minor)。E005 的 submitFn 抓取 email/password 且注释 "Submit email and password for verification",但 SRS 只覆盖捕获(FR-001/002)与服务端比对(FR-005),缺少中间的客户端提交步骤。补 FR-008 有据,接受;但因证据截断、提交端点不可见,FR-008 只作能力级表述、不指定 endpoint。

### R007: unsupported_claim

- Severity: `minor`
- Suggested action: `probably_ignore`
- SRS location: Operating environment / NFR-001 — bcrypt naming
- Evidence IDs: E001

**Claim or gap**

The SRS sometimes refers to 'bcrypt' generically and the constraint C-003 to 'bcrypt-nodejs.' E001 explicitly uses require('bcrypt-nodejs'). Consistency is fine, but NFR-001 verification 'Inspection' relies on the comparePassword path which uses callback(isMatch) — acceptable. No contradiction, but generic 'bcrypt' wording could be tightened.

**Model opinion**

Minor wording consistency; evidence clearly supports bcrypt-nodejs. Low priority.

**Recommended human check**

Confirm bcrypt-nodejs is the only password hashing library; ensure SRS consistently names it.

**Model proposed SRS change**

Standardize references to 'bcrypt-nodejs' across Operating environment, NFR-001, and FR-005 where the specific library is meant.

Optional human revised fix:
> 采用模型建议:在 Operating environment、NFR-001、FR-005 等指代具体库之处统一为 `bcrypt-nodejs`。E001 明确 `require('bcrypt-nodejs')`,而 SRS 多处泛写 "bcrypt"。属低优先级措辞一致性修整,统一命名即可,无证据冲突。

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> Issue 成立(minor,低影响)。E001 显式使用 `bcrypt-nodejs`,C-003 也用该名,但 Operating environment/NFR-001/FR-005 泛称 "bcrypt"。统一为 bcrypt-nodejs 提升一致性,无矛盾、低风险,接受。
