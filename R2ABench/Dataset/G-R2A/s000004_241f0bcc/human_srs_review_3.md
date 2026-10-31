# Human SRS Review Sheet

## Metadata

- Sample directory: `s000004_241f0bcc`
- Generated SRS: `final_srs.md`
- Evidence pack: `evidence_pack.json`
- Review model: `claude-opus-4-8`
- Generated at: `2026-06-05T15:32:04.952075Z`
- Raw model response: `model_srs_review_raw.md`
- Parse status: `parsed`

## Overall Model Opinion

- Recommendation: `revise`
- Confidence: `0.72`
- Rationale: The SRS is generally well-traced to the limited evidence pack and conservatively scoped to front-end, store, and SQL-script behavior. However, a few requirements overstate or sharpen evidence (e.g., FR-003 'logged in' state precision, controlled-list characterized as an API endpoint, three 'tokens' inferred from truncated text), and there is an unexamined architecture-diagram dimension (a broader system with backend services) that the SRS does not flag as out-of-scope/unverified. Targeted revisions are warranted before acceptance.

## Overall Human Decision

- [ ] Accept
- [ ] Reject
- [x] Partial accept

Reason:
> SRS 追溯性强、对前端/store/SQL 范围保守,整体可接受但需修订。R001(声明 backend 超范围)、R002(controlled-list 误列为 API 端点)为成立的 major,需修;R003(three tokens 源文截断)、R004(NFR-004 为历史设计说明而非可测需求)、R007(DR-005 拆分、CON-005 验证方式)为成立的 minor,接受;R005(遗漏 Module Import/Redirect guard、registration PDF)以证据级保守补充,接受;R006(架构图)已读取架构图核对,图确证前端↔HTTP↔.NET Core/EF 后端拓扑(坐实 R001),但图中未显式出现 MS SQL、SiteMinder,故改为部分接受:据图补后端组件关系,MS SQL/SiteMinder 仍保持 inferred。

## Positive Observations

- Strong, disciplined traceability: nearly every FR/NFR/DR/CON cites specific evidence IDs (E001-E006) and the traceability matrix is consistent with the body.
- Conservative scoping: the SRS explicitly notes where the evidence does not define payload schemas/message formats rather than inventing them (Section 3 Data exchange formats).
- FR-003, FR-004, and the guard/interceptor functional requirements are accurately and faithfully derived from E004's core README description.
- SQL-script requirements (DR-004, DR-005, CON-004, CON-005) are precise and well-anchored to E006, including the Volunteer.Active=0 by Id behavior and transaction/backup precautions.
- Verification methods are assigned per requirement and aggregated in Section 8, supporting testability for most items.

## Candidate Issues

### R001: scope

- Severity: `major`
- Suggested action: `needs_human_check`
- SRS location: Section 1 Product scope; Section 2 Product perspective; overall SRS
- Evidence IDs: E001

**Claim or gap**

The SRS scopes the product almost entirely to the front-end ClientApp, NgRx store, and SQL scripts, but the repository name (embc-ess) and the ground-truth architecture diagram imply a larger system including a backend API/server that is repeatedly referenced ('mandatory that the front-end have an API to consume').

**Model opinion**

The evidence pack provided is heavily front-end-weighted (5 of 6 chunks from ClientApp/store, 1 from sql-scripts), so the SRS scoping is defensible given the pack. But the architecture diagram and the repeated API dependency suggest backend components exist and are not represented. The SRS should explicitly state this is a front-end-focused subset and that backend/server components are out of scope for this evidence pack, to avoid understating repository scope.

**Recommended human check**

Open the architecture-diagram.png and repository tree to confirm whether backend/server projects exist (e.g., an ASP.NET/embc-app server). Confirm whether the SRS should declare them out of scope.

**Model proposed SRS change**

In Section 1 Product scope, add: 'This SRS is limited to the front-end ClientApp, its NgRx store, and the repository SQL scripts as represented in the evidence pack. Backend/API server components referenced as dependencies are out of scope for this document and were not provided as evidence.'

Optional human revised fix:
> 采用模型建议:在 Section 1 Product scope 增加一句,声明本 SRS 仅限证据包中的前端 ClientApp、NgRx store 与 SQL 脚本,被反复引用为依赖的 backend/API 服务超出本文档范围且未作为证据提供。这一声明完全基于 E001 自身("mandatory that the front-end have an API to consume"),不依赖架构图。

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> Issue 成立(major)。E001 明确前端依赖一个必须存在的 API,仓库名 embc-ess 也暗示更大系统,但证据包 6 个 chunk 中 5 个来自 ClientApp/store、1 个来自 sql-scripts。SRS 据此收窄范围是合理的,但应显式声明 backend 超范围,避免低估仓库整体范围。该声明有 E001 直接支撑,可直接写入。

### R002: unsupported_claim

- Severity: `major`
- Suggested action: `accept_as_issue`
- SRS location: Section 3 Software/API interfaces — `controlled-list` row; FR-005; DR-002
- Evidence IDs: E003

**Claim or gap**

The SRS lists `controlled-list` as an 'endpoint/data source' in the Software/API interfaces table. Evidence E003 describes controlled-list only as 'Load infrequently changing data at init time. Puts things into the ngrx store' — it does not characterize it as an HTTP endpoint with parameters like the evacuee/incident-task/etc. services.

**Model opinion**

The other services in E003 are explicitly described as 'Http service to perform [CRUD] with params on the endpoint', but controlled-list is described differently (a loader into the store). Listing it under Software/API interfaces alongside HTTP endpoints overstates evidence. The functional behavior (load at init into store, FR-005/DR-002) is supported; the API-endpoint classification is not.

**Recommended human check**

Inspect the controlled-list service source to confirm whether it makes HTTP calls to a 'controlled-list' endpoint or aggregates other data. Decide whether it belongs in the API interface table.

**Model proposed SRS change**

In Section 3 Software/API interfaces, change the `controlled-list` row description to: 'Controlled-list loader (not characterized as a parameterized HTTP endpoint in evidence) — loads infrequently changing data at initialization into the client store.' Alternatively move this row out of the API interfaces table into the data-loading description.

Optional human revised fix:
> 采用模型建议:把 Software/API interfaces 表中的 `controlled-list` 行改为"controlled-list 加载器(证据未将其描述为带参 HTTP 端点)——在初始化时把不常变动的数据加载进客户端 store",或直接移出 API 接口表归入数据加载描述。FR-005/DR-002 的加载行为有据,保留;仅去除其"HTTP 端点"定性。

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> Issue 成立(major)。E003 中其他服务都明写 "Http service to perform CRUD with params on the endpoint",而 controlled-list 仅描述为 "Load infrequently changing data at init time. Puts things into the ngrx store"。SRS 把它与 HTTP 端点并列放进 Software/API interfaces 表属过度断言,应改述或移位。加载行为本身(FR-005/DR-002)有据,保留。

### R003: ambiguity

- Severity: `minor`
- Suggested action: `needs_human_check`
- SRS location: FR-003; CON-002; Section 2 Assumptions; NFR-001
- Evidence IDs: E001

**Claim or gap**

Evidence E001 text is truncated ('There are three different s that are needed', 'set the proxy and token in the file in a way similar to seen in') and the word for the 'three different' items is missing. The SRS infers 'three role-paired tokens', but the actual noun is not visible in the evidence.

**Model opinion**

FR-003 'while application state is logged in' is well-supported by E004 ('a 401 when the application state is logged in'). However the 'three role-paired tokens' claim in CON-002 and Assumptions rests on a truncated sentence where the noun ('s') was cut off. The pairing-to-roles is plausibly supported ('The tokens are paired to front-end roles'), but the count 'three' attaches to an unclear noun. This is a low-risk inference that should be flagged.

**Recommended human check**

Read the full ClientApp/README.md to confirm that exactly three tokens (not users/views/roles) are required and that they are role-paired.

**Model proposed SRS change**

In CON-002 and Section 2 Assumptions, soften to: 'Local development requires proxy configuration and a set of role-paired tokens (evidence indicates three items are needed; exact noun obscured by evidence truncation — verify).' Or confirm and keep 'three tokens'.

Optional human revised fix:
> 采用模型的软化方案:把 CON-002 与 Section 2 Assumptions 改为"本地开发需要 proxy 配置和一组与前端角色配对的 token(证据显示需要三个,但具体名词因证据截断不可见,待核实)"。E001 明确说 "three different s ... are needed" 且 "tokens are paired to front-end roles",token 配对到角色有据,只是"三个"所修饰的名词被截断,故软化而非删除。

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> Issue 成立(minor)。E001 在 "three different s that are needed" 处名词被截断,SRS 直接写成 "three role-paired tokens"。"token 配对角色"有据,但"三个"修饰的对象不确定,应按模型软化措辞并标注待核实,而非保留确定性表述。

### R004: non_verifiable

- Severity: `minor`
- Suggested action: `needs_human_check`
- SRS location: NFR-004; DR-001
- Evidence IDs: E005

**Claim or gap**

NFR-004 ('client store usage shall be limited to models where significant benefit is found') and the framing of DR-001 derive from E005 ('Due to time constraints the Ngrx store is established for a limited number of models and only used when significant benefit is found'), which describes a past design decision/rationale rather than an enforceable, testable requirement.

**Model opinion**

This is a descriptive observation of historical scoping ('due to time constraints'), not a prescriptive requirement with an observable acceptance criterion. 'Significant benefit' is subjective and not verifiable by inspection in a repeatable way. Consider re-labeling as a design note/constraint rather than a maintainability NFR, or rewrite with a measurable criterion.

**Recommended human check**

Confirm whether this should be a requirement at all, or recorded as a design rationale/assumption. Determine an observable acceptance criterion if it remains an NFR.

**Model proposed SRS change**

Reclassify NFR-004 as a design note/assumption: 'Design note (E005): NgRx store usage is intentionally limited to a subset of models where significant benefit is identified; universal store adoption was not pursued due to time constraints.' Remove from the verifiable NFR table or add a concrete inspection criterion.

Optional human revised fix:
> 采用模型建议:把 NFR-004 从可验证 NFR 表移出,改记为设计说明/假设——"(E005)NgRx store 仅限用于能获得显著收益的部分模型;因时间限制未全面采用"。"significant benefit" 主观、不可重复验证,作为 NFR 不合适。

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> Issue 成立(minor)。E005 原文 "Due to time constraints the Ngrx store is established for a limited number of models and only used when significant benefit is found" 是对历史设计取舍的描述性说明,而非可观察、可重复验证的需求;"significant benefit" 主观。应重分类为设计说明/假设,或给出具体可检查标准。

### R005: missing_requirement

- Severity: `minor`
- Suggested action: `needs_human_check`
- SRS location: Section 3 Software/API interfaces; Section 4 Functional Requirements
- Evidence IDs: E003, E004

**Claim or gap**

E004 lists additional core guards/interceptors not captured as requirements: 'Module Import' guard (alerts a developer to a double-loaded module) and 'Redirect' guard (route to an external URL using a router). E003 also notes the registration service 'contains PDF collect...' which the SRS mentions only in passing under data exchange formats.

**Model opinion**

The SRS captured Landing, Logged In, and Role guards plus Unauthorized and Watchdog interceptors, but omitted the Module Import and Redirect guards described in the same E004 chunk. These are arguably developer-tooling/minor, but for completeness and traceability they should at least be acknowledged. The registration PDF-collection behavior is also under-specified relative to evidence.

**Recommended human check**

Confirm whether Module Import guard, Redirect guard, and registration PDF collection warrant their own requirements or an explicit note that they are intentionally excluded as developer/diagnostic features.

**Model proposed SRS change**

Add to Section 4 (or a note): 'FR-008 (optional): The system shall support a redirect guard to route to an external URL via the router (E004).' and 'Developer diagnostic: a module-import guard alerts developers to double-loaded modules (E004).' Also note registration service includes PDF collection behavior (E003) pending schema verification.

Optional human revised fix:
> 采用模型建议,保守落地:在 Section 4 补 Redirect guard(经 router 跳转外部 URL,E004),并以开发者诊断说明记录 Module Import guard(提示模块被重复加载,E004)。registration 服务的 PDF collection(E003)以注记形式记录、标注 schema 待验证。三项均直接出自 E003/E004 文本,不引入证据外细节;PDF 行为因证据本身在 "PDF collect..." 处截断,只作能力注记,不展开。

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> Issue 成立(minor)。E004 与 Landing/Logged In/Role guard、Unauthorized/Watchdog interceptor 在同一段落明确列出 Module Import guard 与 Redirect guard,E003 也提到 registration 服务含 PDF collection,SRS 均遗漏。三项都有显式证据,应补充(可作低优先级 FR 或注记)。PDF 证据截断,仅作能力注记、不展开 schema。

### R006: architecture_detail

- Severity: `minor`
- Suggested action: `needs_human_check`
- SRS location: Section 2 Product perspective; whole SRS
- Evidence IDs: E001, E006

**Claim or gap**

The repository provides an architecture-diagram.png (ground-truth image URL) that is not referenced or reconciled in the SRS. Key architectural relationships (front-end ↔ API ↔ MS SQL, SiteMinder integration) may be depicted there and could confirm/extend the front-end-only view.

**Model opinion**

The SRS infers the architecture from README fragments (browser front-end, required API, MS SQL DB, SiteMinder). The ground-truth diagram should be checked to validate these relationships and to determine whether additional components (auth, backend services, queues) belong in the product perspective. Currently the diagram is unused evidence.

**Recommended human check**

View architecture-diagram.png and confirm whether the front-end/API/SiteMinder/MS SQL relationships in Section 2 match, and whether additional components should be added or noted as out of scope.

**Model proposed SRS change**

In Section 1 References, add the architecture diagram and in Section 2 Product perspective add: 'The repository architecture diagram (architecture-diagram.png) depicts the broader system context; components beyond the front-end, store, and SQL scripts are noted as dependencies and are out of scope for this evidence-based SRS pending diagram review.'

Optional human revised fix:
> 定论前需查看 architecture-diagram.png。该图不在证据包中,front-end↔API↔MS SQL、SiteMinder 等关系目前是从 README 片段推断的。可先按模型建议在 References 列出该图、在 Section 2 加"图描绘更广系统上下文、超出部分为依赖且暂列范围外"的注记;但任何基于图的组件关系细化必须等核图后进行。注:本条的"backend 超范围"声明已由 R001 覆盖落地。

**Human decision**

- [ ] Accept
- [ ] Reject
- [x] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> 图中后端是 .NET Core + Entity Framework(经 DbContext 操作 DB Entities),并未显式标出独立的 "MS SQL" 数据库,也未出现 "SiteMinder";故 Section 2 中 MS SQL、SiteMinder 关系仍属 E001/E006 文本推断,不能据此图坐实,应保持 inferred 标注。范围声明部分与 R001 重叠,已在 R001 落地。

### R007: traceability

- Severity: `minor`
- Suggested action: `probably_ignore`
- SRS location: Section 8 Verification; DR-005 / CON-005
- Evidence IDs: E006

**Claim or gap**

DR-005 combines two distinct E006 behaviors (target-filter variable at top of script AND running within a transaction) into one requirement, and CON-005 (backup precaution) is verification-by-inspection though it is a procedural pre-condition, not an inspectable code property.

**Model opinion**

Both DR-005 and CON-005 are well-evidenced by E006. The minor concern is that DR-005 bundles two verifiable properties (could be split for clean testing) and CON-005 ('backup target database before execution') is an operational procedure whose 'Inspection' verification is weak — it cannot be inspected from the artifact alone. These are low-severity traceability/verifiability refinements.

**Recommended human check**

Decide whether to split DR-005 into two checkable items and whether CON-005 should be re-cast as an operational/procedural pre-condition rather than an inspectable requirement.

**Model proposed SRS change**

Optionally split DR-005 into DR-005a (script includes a top-of-script filter variable) and DR-005b (script executes within a transaction). For CON-005, reword verification as 'Operational procedure check (documentation review)' rather than code Inspection.

Optional human revised fix:
> 采用模型建议:把 DR-005 拆为 DR-005a(脚本顶部含目标过滤变量)与 DR-005b(脚本在事务内执行),便于各自验证;CON-005(执行前备份目标库)的验证方式从 "Inspection" 改为"操作流程检查(文档审查)",因为备份是操作前置条件,无法从脚本工件本身检查。两项均有 E006 支撑。

**Human decision**

- [ ] Accept
- [x] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> Issue 成立(minor,低影响)。E006 充分支持 DR-005 与 CON-005。DR-005 把"顶部过滤变量"与"事务内执行"两个可分别验证的属性绑在一条,拆开更利于测试;CON-005 的备份属操作前置条件,标 "Inspection" 偏弱,改为流程/文档审查更准确。属可选精修,采纳。
