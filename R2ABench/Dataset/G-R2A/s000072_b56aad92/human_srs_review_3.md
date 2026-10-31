# Human SRS Review Sheet

## Metadata

- Sample directory: `s000072_b56aad92`
- Generated SRS: `final_srs.md`
- Evidence pack: `evidence_pack.json`
- Review model: `claude-opus-4-8`
- Generated at: `2026-06-05T16:04:10.149762Z`
- Raw model response: `model_srs_review_raw.md`
- Parse status: `parsed`

## Overall Model Opinion

- Recommendation: `revise`
- Confidence: `0.78`
- Rationale: The SRS is generally well-traced to a thin evidence pack (6 chunks from design notes and READMEs). Most requirements are evidence-backed and conservatively phrased. However, several issues warrant human attention: the SRS overstates scope by presenting early-stage/undiscussed design notes (collective.txt, send-sm.txt) as firm system requirements; some claims (e.g., scatter interface as a product function, FR-008 control-field details) rely on speculative or 'undiscussed' notes; the Libfabric verbs evidence describes a bundled third-party module rather than psmpi-native behavior, raising a scope/attribution concern; and the architecture diagram (UCX) is never referenced or reconciled.

## Overall Human Decision

- [ ] Accept
- [ ] Reject
- [x] Partial accept

Reason:
> 八条均成立,且整体问题偏重:证据本质是设计草稿(collective.txt 含"End of undiscussed section"、send-sm.txt 含 TODO)、重复 README(E001≡E002 字节相同)、与第三方 Libfabric README,SRS 却以 High confidence 的"shall"呈现。R001/R002/R006 是把设计笔记/第三方文档当成实现需求的核心问题;R003 的 ground-truth 图来自 vendored 的 ucx 子模块,应注明不代表 psmpi 自身架构。全部接受。

## Positive Observations

- Requirements are conservatively phrased and consistently traced to specific evidence IDs with a clear traceability matrix.
- NFR-001/002/003 accurately reflect the explicit version and build-flag constraints stated in the Libfabric README evidence (E003).
- The SRS correctly captures the manual-test / not-part-of-make-check constraint (C-001) directly supported by E001/E002.
- Verification methods and acceptance bases are present for each requirement, and the document avoids inventing behavior beyond the retrieved chunks in most cases.

## Candidate Issues

### R001: scope

- Severity: `major`
- Suggested action: `needs_human_check`
- SRS location: Section 4 FR-003/FR-004, Section 2 Product functions, Section 3 Software/API interfaces
- Evidence IDs: E004

**Claim or gap**

FR-003/FR-004 and the listed Init/Finalize/Make_progress/Connect/scatter operations are presented as firm system requirements, but the evidence (E004) is a design discussion note that explicitly contains an 'End of undiscussed section' marker and aspirational language ('We should add a gather interface').

**Model opinion**

The source is a collective-communication design notes file, not a specification of implemented/required behavior. Treating these interfaces as binding functional requirements likely overstates the maturity and authority of the evidence. The text itself flags content as undiscussed and proposes future additions, which undermines presenting it as 'shall provide' requirements.

**Recommended human check**

Open mpich2/doc/notes/coll/collective.txt and confirm whether these interfaces describe a proposed/under-discussion design or an actual implemented API. Check the codebase for actual Init/Finalize/Make_progress/Connect symbols to verify they are real requirements.

**Model proposed SRS change**

In FR-003 and FR-004, qualify the source as design-note-derived and lower confidence: change descriptions to note these reflect a proposed/documented communication-design interface, and add a note in Section 2 Product perspective that E004 is a design discussion note (not confirmed implemented). Alternatively downgrade FR-004 priority and mark traceability confidence Low pending code verification.

Optional human revised fix:
> 采用。E004 原文含"-------- End of undiscussed section"及"We should add a gather interface",明显是讨论中的设计笔记;Init/Finalize/Make_progress/Connect/scatter 不应作为 binding"shall provide",标注 design-note-derived 并降 confidence,待代码确认实际符号。

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> FR-004 的 scatter 接口在 E004 里恰处于"undiscussed"段之后的展望文字,尤其不宜列为需求。

### R002: scope

- Severity: `major`
- Suggested action: `needs_human_check`
- SRS location: Section 1 Product scope, Section 2, NFR-001/002/003, C-004/C-005, FR (verbs)
- Evidence IDs: E003

**Claim or gap**

Verbs/Libfabric integration requirements (E003) are derived from mpich2/modules/libfabric/README.md, which is a bundled third-party (OFI/Libfabric) module README describing Libfabric's own verbs provider, not necessarily a psmpi-defined requirement.

**Model opinion**

Attributing Libfabric's dependency requirements (libibverbs >= 1.1.8, librdmacm >= 1.0.16) to psmpi as system requirements may misattribute third-party module documentation as repository-native requirements. The dependency is real but belongs to the embedded Libfabric submodule; whether psmpi requires/enables this build path is unverified.

**Recommended human check**

Confirm whether psmpi build configuration actually enables the Libfabric verbs provider and whether these version constraints propagate to psmpi builds, or whether this is purely vendored third-party documentation.

**Model proposed SRS change**

Add a qualifier to NFR-001/NFR-002/NFR-003 and C-004/C-005 noting the source is the embedded Libfabric module README and the constraint applies only when the Libfabric verbs provider is built/enabled within psmpi. Scope statement in Section 1 should clarify this is conditional on building the bundled Libfabric verbs provider.

Optional human revised fix:
> 采用。E003 是 mpich2/modules/libfabric/README.md(OFI/Libfabric 自身的 verbs provider 文档),libibverbs>=1.1.8 / librdmacm>=1.0.16 是该第三方模块的依赖,将其作为 psmpi 原生系统需求属误归属;应限定为"构建/启用 bundled Libfabric verbs provider 时适用"。

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> 依赖真实存在,但归属层级错位,加条件限定即可。

### R003: architecture_detail

- Severity: `major`
- Suggested action: `needs_human_check`
- SRS location: Whole document / Section 2 Product perspective
- Evidence IDs: none

**Claim or gap**

The ground-truth architecture image is mpich2/modules/ucx/docs/doxygen/Architecture.png (a UCX architecture diagram), but the SRS contains no UCX content and never reconciles its architectural picture (VC progress, verbs, packet send) against this diagram.

**Model opinion**

Either the architecture diagram points to a major transport subsystem (UCX) entirely absent from the SRS, indicating a scope/coverage gap, or the diagram is from a vendored third-party module and is not representative of psmpi's architecture. The mismatch should be examined: the SRS's architectural framing (VC-oriented, verbs, send-sm) may not align with the referenced ground-truth diagram.

**Recommended human check**

Inspect the UCX Architecture.png and determine whether UCX is a primary psmpi transport that should be represented in the SRS, or a vendored module. If primary, add coverage; if vendored, note that the ground-truth image is not representative.

**Model proposed SRS change**

Add a Section 2 note acknowledging the UCX module/architecture and either (a) add requirements covering UCX transport if it is in scope, or (b) explicitly state UCX is a vendored module outside the evidence-backed scope. Conditional on human verification of UCX's role.

Optional human revised fix:
> 采用 (b)。image_url 路径为 mpich2/modules/ucx/docs/doxygen/Architecture.png,位于 vendored 的 ucx 子模块,是第三方传输库自带的架构图,并不代表 psmpi 自身架构;应注明 ground-truth 图来自 vendored 模块、不具代表性,而非据其补 UCX 需求。具体可待开图确认,但路径已强烈指向 vendored。

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> 与 s000067/068 等"图缺口"情形不同:此图属第三方 vendored,补的是"不代表性"说明而非组件需求。

### R004: non_verifiable

- Severity: `minor`
- Suggested action: `needs_human_check`
- SRS location: Section 4 FR-001, Section 8 acceptance
- Evidence IDs: E001, E002

**Claim or gap**

FR-001 states the system 'shall execute a battery of tests' but the acceptance basis is circular ('Running the script executes a battery of tests') and 'battery of tests' is not enumerated or observable as a pass/fail criterion.

**Model opinion**

The verification basis restates the trigger rather than defining an observable success condition. 'Battery of tests' is vague; an acceptance criterion should specify expected exit status or that all embedded tests pass.

**Recommended human check**

Inspect run-embedded-tests.sh to determine its observable pass/fail signal (exit code, output) and what tests constitute the battery.

**Model proposed SRS change**

Revise FR-001 acceptance basis in Section 8 to: 'run-embedded-tests.sh <tarball> completes with success exit status and reports all embedded verification tests as passing.' Adjust once script behavior is confirmed.

Optional human revised fix:
> 采用。原验收"Running the script executes a battery of tests"循环复述触发条件,"battery of tests"未枚举、无 pass/fail,改为以退出状态/全部通过为可观察准则。

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> 

### R005: traceability

- Severity: `minor`
- Suggested action: `probably_ignore`
- SRS location: Section 1 References / FR-001, FR-002, NFR-004, C-001..C-003
- Evidence IDs: E001, E002

**Claim or gap**

E001 and E002 are byte-identical duplicate README files at two different paths, yet they are cited as if they were two independent corroborating evidence sources throughout the document.

**Model opinion**

Citing two copies of the same file as 'E001, E002' inflates apparent corroboration. It is not a factual error but slightly overstates evidentiary strength; the human should know these are duplicates (likely one is a vendored copy of the other).

**Recommended human check**

Confirm E001 and E002 are duplicate copies of the same embedded hwloc test README and decide whether to cite both or note the duplication.

**Model proposed SRS change**

Add a note in Section 1 References that E001 and E002 are duplicate copies of the same README at different vendored paths, so dual citation does not imply independent corroboration.

Optional human revised fix:
> 采用。E001(mpich2/modules/hwloc/.../README.txt)与 E002(mpich2/src/pm/hydra/.../hwloc/.../README.txt)文本逐字相同,系同一 vendored hwloc README 的两份拷贝,双引会夸大佐证强度。

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> 非事实错误,但属诚实标注,采纳。

### R006: non_verifiable

- Severity: `major`
- Suggested action: `needs_human_check`
- SRS location: Section 4 FR-005, FR-006, FR-007, FR-008; Section 8
- Evidence IDs: E005, E006

**Claim or gap**

FR-005 through FR-008 are assigned Verification = 'Test', but the underlying evidence (E005/E006) is a state-machine/pseudocode design note (send-sm.txt) containing TODO markers (e.g., '// TODO: Add buffer packing into flow', '// pack data from DD'), suggesting these describe a design sketch rather than testable implemented behavior.

**Model opinion**

Requirements derived from pseudocode with open TODOs may not correspond to verifiable shipped behavior. Designating 'Test' as the verification method implies an executable acceptance test exists; for design-note-derived behavior, 'Inspection' (of code/design) may be more appropriate until implementation is confirmed.

**Recommended human check**

Verify in the codebase that the flow-control/direct-access/packet-packing send path is implemented and observable, justifying 'Test' verification. If only documented as a design note with TODOs, reclassify verification method.

**Model proposed SRS change**

Conditional: if behavior is implemented, retain 'Test' but add concrete acceptance assertions. If only design notes exist, change FR-005..FR-008 verification to 'Inspection' and annotate that source send-sm.txt is a design state-machine note with open TODOs.

Optional human revised fix:
> 采用。E005/E006 是 send-sm.txt 状态机伪代码,含"// TODO: Add buffer packing into flow""// pack data from DD"等开放标记;在确认实现前用 Test 暗示已有可执行验收过头,宜改 Inspection 并标 design-note 来源。

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> FR-005~008 全部 Test 验证,但证据为含 TODO 的伪代码,与 FR-001~004 的设计笔记问题同源。

### R007: ambiguity

- Severity: `minor`
- Suggested action: `accept_as_issue`
- SRS location: Section 3 Data exchange formats; FR-008; DR-004
- Evidence IDs: E006

**Claim or gap**

Terms 'LIBA', 'LIBA(OD)', 'OD', 'DD', and 'envelope' are used without definition, making FR-008 and DR-004 difficult to interpret or verify.

**Model opinion**

These are domain abbreviations lifted verbatim from the design note. Without a glossary, the requirements are underspecified for a reader who must verify them. Verifiability suffers because the data fields are opaque.

**Recommended human check**

Locate definitions of LIBA, OD, DD in send-sm.txt or related notes and confirm meanings.

**Model proposed SRS change**

Add a glossary entry or inline definitions in Section 3 / Section 6 for LIBA, OD (object descriptor), DD (data descriptor), and 'envelope', derived from the source note, to make FR-008/DR-004 interpretable.

Optional human revised fix:
> 采用。LIBA/LIBA(OD)/OD/DD/envelope 直接照搬自设计笔记,无定义,FR-008/DR-004 对读者不可解读、不可验证,应补术语表。

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> 定义需从 send-sm.txt 全文提取。

### R008: unsupported_claim

- Severity: `minor`
- Suggested action: `needs_human_check`
- SRS location: Section 2 Product functions / Product perspective ('packetized data transfer', 'flow control')
- Evidence IDs: E005, E006

**Claim or gap**

The SRS frames flow control and packetized send as established 'product functions' of psmpi broadly, but E005/E006 only document a single send state-machine note ('send-sm.txt') without confirming this is the system-wide communication model.

**Model opinion**

Generalizing a single agent send-path note to a product-level function may overstate scope. The evidence supports a specific send path's behavior, not necessarily a general product claim.

**Recommended human check**

Determine whether send-sm.txt describes the general/primary send path of psmpi or a specific agent/component, and scope the product-function claims accordingly.

**Model proposed SRS change**

Qualify Section 2 product-function bullets to state that flow-control/packet-send behavior is documented for the specific send-state-machine ('send-sm') path described in evidence, not asserted as a system-wide function.

Optional human revised fix:
> 采用。E005/E006 仅记一个 send 状态机笔记,将 flow control / packetized send 提升为 psmpi 全局产品功能过宽,应限定到 send-sm 路径。

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> 与 R007(术语未定义:LIBA/OD/DD/envelope)可一并补 glossary,使 FR-008/DR-004 可解读。
