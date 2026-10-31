# Human SRS Review Sheet

## Metadata

- Sample directory: `s000075_7722edce`
- Generated SRS: `final_srs.md`
- Evidence pack: `evidence_pack.json`
- Review model: `claude-opus-4-8`
- Generated at: `2026-06-05T16:05:46.752387Z`
- Raw model response: `model_srs_review_raw.md`
- Parse status: `parsed`

## Overall Model Opinion

- Recommendation: `revise`
- Confidence: `0.72`
- Rationale: The SRS is well-structured and mostly evidence-traceable, but it contains a field-level contradiction (Display fields and Gauge field types vs. evidence), a few inferred claims dressed as explicit, and a missing architecture detail (Redux client state / TypeScript editor implementation from E003/E004 is underused). Targeted fixes are needed before acceptance.

## Overall Human Decision

- [ ] Accept
- [ ] Reject
- [x] Partial accept

Reason:
> 六条均成立。R001 是真实矛盾:E004(client Models.ts)的 Display 无 current_layout,E005(server serializer)有,SRS 把统一字段表同时归给 E005/E006 掩盖了 client/server 分歧,应分开归属并标注。R003(E003 Redux store/canvas actions、E004 编辑器架构被低用)、R004/R005(README 自述"not 100% standalone/ready"、Dockerfile 用 runserver 等 dev-grade 信号未surfacing)也实质。R002/R006 为引用/措辞小修。全部接受。

## Positive Observations

- Functional and data requirements are closely tied to concrete schema/model evidence (E004, E005, E006), with accurate field listings for Gauge, Display, and Layout.
- The SRS appropriately marks several items as 'inferred' (communication interfaces, wire format) rather than overstating, and explicitly notes absence of privacy/retention/migration evidence.
- Constraints C-001 through C-005 are well-grounded in the Dockerfile (E001) and README (E002), including the client-build-before-server-packaging dependency.
- Traceability matrix with per-requirement evidence IDs, evidence type, and confidence is provided and mostly consistent with the evidence pack.

## Candidate Issues

### R001: contradiction

- Severity: `major`
- Suggested action: `needs_human_check`
- SRS location: Section 3 Software/API interfaces - Display resource; FR-002/FR-003; Section 6 Data entities - Display
- Evidence IDs: E004, E005, E006

**Claim or gap**

The SRS lists the Display resource with field `key`, but the client Models.ts (E004) defines Display fields as `key, available, resolution_x, resolution_y, display_data, rotation` (no `current_layout`), while the server serializer (E005) includes `current_layout` and omits nothing. The SRS Display field list mixes server-only fields without flagging the client/server divergence.

**Model opinion**

E004 (client) and E005 (server) define divergent Display field sets: client has no `current_layout`; server serializer has `current_layout` but client Models.ts lacks it. The SRS presents a single unified field list attributed to both [E005] and [E006], which obscures a real discrepancy. This is a traceability/contradiction concern worth surfacing.

**Recommended human check**

Compare client/src/Models.ts (E004), server serializer (E005), and models.py (E006) field-by-field for the Display entity and confirm whether `current_layout` is intentionally client-absent.

**Model proposed SRS change**

In Section 3 Display resource and Section 6 Display entity, add a note: 'The server-side Display model/serializer (E005, E006) includes `current_layout` (FK to Layout, nullable, SET_NULL on delete); the client-side Display interface (E004) omits `current_layout`. This client/server field divergence should be reconciled.' Attribute client-derived fields to [E004] and server-derived to [E005]/[E006] separately.

Optional human revised fix:
> 采用。E004 client Display = {key, available, resolution_x, resolution_y, display_data, rotation},确无 current_layout;E005/E006 server 含 current_layout(FK→Layout, SET_NULL, null=True)。SRS 在 3 节/6 节把含 current_layout 的统一字段表同时标 [E005][E006],掩盖了 client 端缺失,应分开归属并加分歧说明。

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> 已逐字核对证据,client/server 分歧属实。

### R002: unsupported_claim

- Severity: `minor`
- Suggested action: `probably_ignore`
- SRS location: Section 6 Data entities - Gauge ('value max length 600'); Layout ('data is binary'; 'display_positions is text')
- Evidence IDs: E006

**Claim or gap**

Field-level details such as `value` max length 600, `data` stored as binary, `display_positions` as text are stated as fact. These are supported by E006 (models.py) but E006's text is truncated and the Gauge max_length=600 is visible; binary/text are visible. This is largely supported but the SRS should cite E006 specifically per claim rather than co-citing E005.

**Model opinion**

The detailed type claims are actually supported by E006 (models.py shows max_length=600, BinaryField, TextField). The issue is minor traceability: these model-specific details should cite E006 alone, not the serializer E005. Content itself is accurate.

**Recommended human check**

Confirm models.py (E006) shows value max_length=600, data=BinaryField, display_positions=TextField; ensure citations point to E006 for these type details.

**Model proposed SRS change**

In Section 6, change the Notes-column citations for type-specific details (max length 600, binary data, text display_positions, primary keys, SET_NULL) to cite [E006] only.

Optional human revised fix:
> 采用。E006(models.py)确显 value max_length=600、data=BinaryField、display_positions=TextField、各 key primary_key、current_layout SET_NULL;这些类型细节应单引 E006 而非连带 serializer E005。内容本身准确。

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> 纯溯源精确化,内容无误。

### R003: architecture_detail

- Severity: `major`
- Suggested action: `accept_as_issue`
- SRS location: Section 2 Product perspective; Section 3 User interfaces; FR-004/FR-005
- Evidence IDs: E003, E004

**Claim or gap**

Evidence E003 (client/src/Store.tsx) and E004 (Models.ts) show the editor is a TypeScript/React + Redux single-page client with defined actions (CONTROL_ADDED, ELEMENT_ADDED, SET_LAYOUTS, SET_GAUGES, SET_DISPLAYS, REQUEST_CANVAS_RENDER, etc.) and a canvas rendering model. The SRS describes the editor only abstractly ('wizard', 'create layouts') and never cites E003 or uses E004 for the editor architecture.

**Model opinion**

There is concrete evidence of the editor's client-side architecture (Redux store, canvas render/delete actions, gauge/layout/display state) that the SRS underuses. This is relevant for the architecture diagram check and would strengthen FR-004/FR-005. The 'wizard' description from E002 is fine but thin given richer code evidence.

**Recommended human check**

Review Store.tsx (E003) and Models.ts (E004) to confirm Redux-based client with canvas rendering and the listed action types; compare with docs/architecture.png ground-truth diagram for editor/viewer/server topology.

**Model proposed SRS change**

In Section 2 Product perspective, refine: 'The client/editor is a TypeScript/React single-page application using a Redux store (E003) with actions for adding/updating controls and elements, setting layouts/gauges/displays, and requesting canvas render/delete operations (E003, E004).' Add [E003] citation to FR-004/FR-005 traceability.

Optional human revised fix:
> 采用。E003(Store.tsx)有 redux createStore 及 CONTROL_ADDED/ELEMENT_ADDED/SET_LAYOUTS/SET_GAUGES/SET_DISPLAYS/REQUEST_CANVAS_RENDER/REQUEST_CANVAS_DELETE_OBJECT 等 action,编辑器架构有具体代码证据却被 SRS 仅以"wizard"抽象描述、从未引 E003;补充可强化 FR-004/FR-005。

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> docs/architecture.png 已缓存,editor/viewer/server 拓扑待开图对照。

### R004: non_verifiable

- Severity: `minor`
- Suggested action: `needs_human_check`
- SRS location: FR-007; Section 8 acceptance for FR-007
- Evidence IDs: E002

**Claim or gap**

FR-007 ('viewer subsystem shall render what each display sees') and its acceptance ('a reviewer can show per-display rendered output') rely solely on the README prose (E002), which itself is incomplete ('Th...' truncated) and the README notes the docker image is 'not 100% standalone/ready'. The viewer is described aspirationally; no code evidence for headless-browser rendering is provided.

**Model opinion**

The viewer requirement is supported only by truncated README prose and there is no code/deployment evidence of an implemented headless-browser viewer. Given README's own 'not 100% ready' caveat, FR-007 may overstate implemented scope. The acceptance criterion is demonstration-based but may not be demonstrable in current state.

**Recommended human check**

Search the repository for any viewer/headless-browser implementation code; verify whether the viewer is implemented or only conceptual at this commit.

**Model proposed SRS change**

Mark FR-007 priority/status as planned-or-conceptual: append to FR-007 Requirement text 'This describes intended viewer behavior per the README architecture section (E002); implementation evidence at this commit is limited.' Lower confidence to Low in Section 9.

Optional human revised fix:
> 采用。FR-007 仅靠 E002 截断散文("...rendering what each display \"sees\"... Th"被截),且 README 自述 docker"not 100% standalone/ready",无 headless-browser viewer 代码证据;标为 intended/conceptual 并降 Low。

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> 建议搜库确认 viewer 是否已实现;当前仅概念描述。

### R005: scope

- Severity: `minor`
- Suggested action: `accept_as_issue`
- SRS location: Section 1 Product scope; NFR-001/Constraints C-005
- Evidence IDs: E001, E002

**Claim or gap**

The SRS does not surface the README's explicit caveat that the docker image is 'building, but not 100% standalone/ready' (E002) and the Dockerfile's TODOs (fixed npm version, real WSGI server, runserver used as CMD) (E001). These indicate the deployment is dev-grade/incomplete, which affects operational scope claims.

**Model opinion**

Both E001 and E002 contain explicit incompleteness signals (TODOs, 'not 100% ready', `runserver` not a production WSGI server). The SRS presents deployment constraints neutrally without noting these are development-stage. Including this prevents overstating production readiness.

**Recommended human check**

Confirm Dockerfile uses `manage.py runserver` (dev server) and README's standalone caveat; decide whether to add a maturity/limitations note.

**Model proposed SRS change**

Add to Section 7 a constraint C-006: 'The supplied deployment is development-grade: the Dockerfile uses Django `runserver` (not a production WSGI server) and the README states the docker image is not yet fully standalone (E001, E002).'

Optional human revised fix:
> 采用。E001 含"# TODO - use real wsgi server"且 CMD 为 ./manage.py runserver,E002 含"docker image is building, but not 100% standalone/ready",均为开发阶段信号;加 C-006 防止高估生产就绪度。

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> 

### R006: ambiguity

- Severity: `minor`
- Suggested action: `probably_ignore`
- SRS location: FR-002; Section 3 'unique name and resolution'
- Evidence IDs: E002, E006

**Claim or gap**

FR-002 states displays are registered with a 'unique key'. README (E002) says 'unique name'; the model (E006) uses `key` as primary key (CharField max_length=100). The SRS conflates 'name' and 'key'. Whether the display's human-facing 'name' equals the primary-key `key` is unstated.

**Model opinion**

Minor ambiguity: README's 'unique name' vs model's primary-key `key`. They are likely the same field, but the SRS should state this mapping explicitly to be verifiable.

**Recommended human check**

Confirm that the README 'unique name' maps to the model `key` primary key field.

**Model proposed SRS change**

In FR-002 add: 'The unique display identifier (README "name") corresponds to the model `key` primary key field (E006).'

Optional human revised fix:
> 采用。E002 说"unique name",E006 用 key(CharField max_length=100, primary_key)。二者大概率同一字段,明示映射使 FR-002 可验证。

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> 
