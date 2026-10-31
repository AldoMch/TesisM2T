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
- [ ] Partial accept

Reason:
> 

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
> Issue 成立。E004 不直接证明字段在 CLI trace flow 中的具体选择语义。建议采纳模型修改建议。

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
> 

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> Issue 成立。当前 evidence 支持目标/测试环境，但不支持严格唯一的运行环境。建议采纳模型修改意见。

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
> 建议采纳。也可选择：FR-009 和 C-004 可保留 “naming scheme exists” 的事实，但 Acceptance 改为：“evidence confirms naming-scheme dependency; exact pattern must be verified from full README/probe source before testing.”

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> issue成立，当前证据被截断，无法判断是否存在既定的命名规则。

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
> 建议采纳。将 FR-005/NFR-004 改为 “documented design goal” 或补充具体配置结构与运行路径；在未确认 runtime config-loading 前，不要写成可测试功能需求。

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> Issue 成立。当前 SRS 只能通过文档检查确认定位，没有标准验收 configuration actually drives tracing behavior。


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
> 

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> issue不成立，证据不涉及ground-truth architecture diagram
