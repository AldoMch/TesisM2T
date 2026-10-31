# Human SRS Review Sheet

## Metadata

- Sample directory: `s000067_4d85c913`
- Generated SRS: `final_srs.md`
- Evidence pack: `evidence_pack.json`
- Review model: `claude-opus-4-8`
- Generated at: `2026-06-05T16:01:46.135088Z`
- Raw model response: `model_srs_review_raw.md`
- Parse status: `parsed`

## Overall Model Opinion

- Recommendation: `revise`
- Confidence: `0.74`
- Rationale: The SRS is well-traced and conservative for most claims, but several requirements assert specifics (Kretprobe, NFR-003 'tested on', DR-004 CLI fields, naming-scheme details) where evidence is truncated or thin. A few non-functional and inferred items need human verification, and DR-004 cites evidence that does not fully support its stated constraints.

## Overall Human Decision

- [ ] Accept
- [ ] Reject
- [x] Partial accept

Reason:
> SRS 质量高(score 96)、溯源克制,五条均为成立的小修订:R002(把"tested on"升成"shall operate only on")、R003(命名方案在证据中被打码)、R004(config-driven 是设计意图非可测行为)最值得改。R001/R005 接受。无需驳回项。

## Positive Observations

- Strong, conservative traceability: nearly every FR/NFR cites specific evidence IDs and distinguishes Explicit vs Inferred confidence (e.g., NFR-004 marked Inferred/Low).
- FR-007 ('no handler set -> return 0, do nothing') is precisely grounded in E001 and is testable.
- Data requirements DR-003 accurately reflect the Event_Args fields (position/type/name/suffix/hash_func) from E005.
- Scope is appropriately bounded to the library and reference CLI without inventing unsupported features.

## Candidate Issues

### R001: traceability

- Severity: `minor`
- Suggested action: `needs_human_check`
- SRS location: DR-004
- Evidence IDs: E004

**Claim or gap**

DR-004 lists CLI event structure fields `ProgramID`, `Pids`, `ELFPath` and cites E004; this is supported, but the 'Used by CLI tracing flow' constraint is partly inferential.

**Model opinion**

E004 clearly shows `type Event struct { ProgramID uint64; Pids []int; ELFPath string }`, so field names are well supported. The functional role ('Trace command event selection data') is a reasonable interpretation but not explicitly stated in evidence.

**Recommended human check**

Confirm in cli/cmd/trace.go that this Event struct is used for trace event selection vs. another purpose.

**Model proposed SRS change**

DR-004 Description: replace 'CLI-side event structure includes ...' with 'CLI-side Event struct in cli/cmd/trace.go declares fields ProgramID (uint64), Pids ([]int), ELFPath (string); the functional role is inferred and unverified.'

Optional human revised fix:
> 

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> 

### R002: unsupported_claim

- Severity: `minor`
- Suggested action: `needs_human_check`
- SRS location: NFR-003 / NFR-001
- Evidence IDs: E002, E006

**Claim or gap**

NFR-001 states the system 'shall operate only on Linux' kernels with Kprobe/Kretprobe support, framed as a hard requirement; evidence only says it 'has been tested on' such kernels and the README sentence is truncated ('Though...').

**Model opinion**

E002/E006 phrase this as 'has been tested on kernel versions with eBPF support for Kprobes and Kretprobes' followed by a truncated 'Though...' that may soften the constraint. Promoting 'tested on' to 'shall operate only on' overstates the constraint into a strict requirement.

**Recommended human check**

Read the full README sentence beginning 'Though...' to see whether broader kernel support is claimed or caveated.

**Model proposed SRS change**

NFR-001 Statement: change to 'TraceLeft targets Linux kernels with eBPF support for Kprobes and Kretprobes; the README documents it as tested on such kernels. Strict exclusivity is not explicitly stated in evidence.'

Optional human revised fix:
> 采用。eBPF/Kprobe 本就是 Linux 专属,平台前提没错;问题在 E002/E006 原文是"has been tested on ... Kprobes ans Kretprobes. Though..."(截断),把"tested on"升级为"shall operate only on"是把观察叙述硬化成排他性需求,改为目标平台表述更贴证据。

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> 末尾"Though..."被截断,可能本就在软化该约束,需读全句。

### R003: ambiguity

- Severity: `minor`
- Suggested action: `needs_human_check`
- SRS location: FR-009 / C-004
- Evidence IDs: E001

**Claim or gap**

The handler-probe naming scheme is referenced as 'documented naming conventions' but the evidence text is redacted (scheme names removed: 'follow the scheme where is the name...').

**Model opinion**

E001 confirms a naming scheme exists and that k{,ret}probe names define which handler map to update, but the actual scheme tokens are missing from the chunk. FR-009/C-004 should not imply a fully specified, verifiable convention when the concrete pattern is not in evidence.

**Recommended human check**

Inspect documentation/README.md and probe loader source to capture the exact handler/map naming pattern.

**Model proposed SRS change**

FR-009 Verification note: add 'Exact naming pattern not captured in evidence chunk; verify concrete scheme from README/probe source before treating as a testable convention.'

Optional human revised fix:
> 采用。E001 里方案名被打码("follow the scheme where is the name...""expects handler probes to follow the scheme and"),FR-009/C-004 不应暗示已完整可验证的约定。

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> 命名方案存在可确认,但具体 token 缺失,标注待核。

### R004: non_verifiable

- Severity: `minor`
- Suggested action: `needs_human_check`
- SRS location: FR-005, NFR-004
- Evidence IDs: E002, E006

**Claim or gap**

'Configuration-driven tracing/auditing' requirements lack an observable acceptance criterion; they restate marketing-style framing from the README.

**Model opinion**

E002/E006 describe TraceLeft as 'designed as a framework to build configuration driven system auditing tools'. This is a design intent, not a testable behavior. FR-005/NFR-004 as written cannot be objectively verified.

**Recommended human check**

Determine whether a concrete config-loading code path exists (e.g., generator/config.pb.go usage) to anchor a testable criterion.

**Model proposed SRS change**

FR-005 Acceptance Basis: tie to a concrete artifact, e.g. 'Generated config structures (Event_Args with position/type/name/suffix/hash_func) can be supplied to drive event handling [E005].' If no runtime path is confirmed, demote to a design-goal note rather than a requirement.

Optional human revised fix:
> 采用。E002/E006 的"designed as a framework to build configuration driven ... tools"是设计意图,FR-005/NFR-004 照搬成需求无可观察验收准则;可锚定 E005 的 Event_Args 结构,或降为设计目标说明。

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> NFR-004 已自标 Inferred/Low,与本条一并处理。

### R005: architecture_detail

- Severity: `minor`
- Suggested action: `needs_human_check`
- SRS location: Section 2 / FR-006, FR-008
- Evidence IDs: E001

**Claim or gap**

The tail-call probe/handler architecture and single shared event map are described from README text but not cross-checked against the ground-truth architecture diagram.

**Model opinion**

E001 supports trace probes tail-calling handler probes and a single shared event map. The architecture diagram (traceleft-architecture.png) is referenced in the evidence pack but not provided as text; key dataflow (kernel->userspace tracer dispatch) should be confirmed against it.

**Recommended human check**

Compare Section 2 product perspective against documentation/traceleft-architecture.png for components and event flow.

**Model proposed SRS change**

Section 2 Product perspective: add note 'Architecture per README; not yet reconciled with traceleft-architecture.png — verify component/dataflow names against the diagram.'

Optional human revised fix:
> 采用。traceleft-architecture.png 已缓存确实存在,补图引用并标待对照;kernel→userspace 分派等数据流需开图确认(本环境读不到图片内容)。

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> 图存在但不在证据文本里,补引用合理,组件级核对待开图。
