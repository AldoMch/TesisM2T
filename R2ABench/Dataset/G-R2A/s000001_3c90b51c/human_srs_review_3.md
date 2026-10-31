# Human SRS Review Sheet

## Metadata

- Sample directory: `s000001_3c90b51c`
- Generated SRS: `final_srs.md`
- Evidence pack: `evidence_pack.json`
- Review model: `claude-opus-4-8`
- Generated at: `2026-06-05T15:23:53.969157Z`
- Raw model response: `model_srs_review_raw.md`
- Parse status: `parsed`

## Overall Model Opinion

- Recommendation: `revise`
- Confidence: `0.78`
- Rationale: The SRS is well-structured and mostly evidence-backed, with strong traceability. However, several issues need attention: FR-001 conflates SeatAllocatorProcessor (E001) with the SeatAllocationMethod interface (E002); the command-line launcher is referenced as evidenced behavior but only the README mentions it without details; the planned web interface is correctly excluded but worth noting; and some traceability entries cite the wrong evidence for specific claims (e.g., immutability).

## Overall Human Decision

- [ ] Accept
- [ ] Reject
- [x] Partial accept

Reason:
> SRS 代码级追溯扎实、措辞保守,整体可接受但需修订。多数 issue 都由证据 chunk 直接支撑、可落地:R001(SeatAllocatorProcessor 与 SeatAllocationMethod 两个 API 面被混为一谈,且 immutable tally 主张张冠李戴)、R002(CLI 仅证存在、无语法不可验证)、R003(planned web interface 应显式标范围外)、R005(abstract nextDivisor 扩展点未捕获)、R006(rounding TODO 未标注)、R007(Majority 子变体枚举不一致)均接受。R004(Candidate 构造参数是否为票数)仍依赖证据包外源码,判 PARTIAL_ACCEPT。R008(架构图)已读取 jseats_architecture.png 核对,Tally→Processor[Filter→Process→Decorate]→Result 流水线及 TallyFilters/TieBreaker/ResultDecorators 配置均被证实,改为接受。

## Positive Observations

- Strong, consistent traceability matrix linking each requirement to specific evidence IDs with explicit/inferred typing and confidence levels.
- Appropriately conservative scoping: the SRS limits supported methods to those documented in evidence (C-003) and marks extensibility NFRs as inferred.
- Accurate extraction of the absolute-majority formula (potentialVotes/2)+1 directly from E005.
- Clear separation of the ResultDecorator interface (E003) as an optional post-processing contract, faithfully reflecting the evidence.
- Exception-handling behavior (SeatAllocationException) is correctly captured as both a functional (FR-009) and fault-handling NFR (NFR-003) requirement, grounded in E001/E002.

## Candidate Issues

### R001: traceability

- Severity: `major`
- Suggested action: `needs_human_check`
- SRS location: FR-001, Section 3 Software/API interfaces, C-002
- Evidence IDs: E001, E002

**Claim or gap**

The SRS describes the 'processing interface' that 'accepts an immutable tally and method properties' citing [E004, E002], but E002 is the SeatAllocationMethod interface (process(InmutableTally, Properties)), while the example usage in E001 uses SeatAllocatorProcessor. The SRS blends two distinct API entry points (SeatAllocatorProcessor vs SeatAllocationMethod) into one 'processing API'.

**Model opinion**

There appear to be two API surfaces: SeatAllocatorProcessor (the high-level caller-facing processor used in E001) and SeatAllocationMethod (the per-method contract in E002). The SRS conflates these. The 'immutable tally' claim derives only from E002's InmutableTally parameter, not from the caller-facing processor in E001, which uses a mutable Tally.

**Recommended human check**

Inspect SeatAllocatorProcessor.java and SeatAllocationMethod.java to confirm whether the public caller API is SeatAllocatorProcessor (taking mutable Tally) versus the internal method contract (taking InmutableTally). Adjust FR-001 and C-002 accordingly.

**Model proposed SRS change**

Revise FR-001 to distinguish the two interfaces: 'FR-001a: The system shall provide a high-level processor (SeatAllocatorProcessor) that callers use to process a Tally into a Result [E001]. FR-001b: The system shall define a per-method contract (SeatAllocationMethod.process(InmutableTally, Properties)) returning a Result or raising SeatAllocationException [E002].' Update C-002 to scope the immutable-tally constraint to the SeatAllocationMethod contract only.

Optional human revised fix:
> 采用模型建议:把 FR-001 拆成 FR-001a(面向调用者的高层 SeatAllocatorProcessor,处理 Tally→Result,E001)与 FR-001b(每方法契约 SeatAllocationMethod.process(InmutableTally, Properties)→Result/抛 SeatAllocationException,E002);并把 C-002、Section 3 的"immutable tally"约束限定到 SeatAllocationMethod 契约,不要套到调用者 API 上。注意:E001 可见 `processor` 操作的是 `new Tally()`(可变),"InmutableTally" 仅出现在 E002/E005/E006 的方法签名里,故现表述把两者揉成一个"processing API"确属误植。

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> Issue 成立(major)。E001 的调用方用 `SeatAllocatorProcessor` 配 `new Tally()`(可变 Tally),E002 才是 `SeatAllocationMethod.process(InmutableTally, Properties)`。SRS 在 Section 3/FR-001 把两个不同入口合称"processing interface accepts an immutable tally",并把 immutable 主张挂到调用者 API,属真实的追溯错误。拆分两接口、把不可变约束限定到方法契约,均由证据 chunk 直接支撑,接受。

### R002: non_verifiable

- Severity: `major`
- Suggested action: `needs_human_check`
- SRS location: FR-003, Section 3 Command line, NFR-004, FR (implicit)
- Evidence IDs: E004

**Claim or gap**

The command-line launcher requirement (Section 3, NFR-004) is asserted as a verifiable behavior, but E004 only states 'JSeats provides both a clean java API and a command line launcher' and shows the prompt 'The command line looks like this:' with no actual command syntax, flags, or behavior captured in evidence.

**Model opinion**

There is insufficient evidence to specify or test the command-line launcher's behavior. The README references it but the evidence chunk truncates before showing the actual CLI usage. The requirement is currently non-verifiable as no acceptance criterion (command syntax, expected output) is derivable from evidence.

**Recommended human check**

Retrieve the full README CLI section and locate the launcher main class (e.g., a Launcher.java or Main.java) to capture actual command syntax and arguments. Without this, mark the CLI requirement as low-confidence/inferred.

**Model proposed SRS change**

Add a note to NFR-004 and the Section 3 command-line row: 'Evidence confirms existence of a command-line launcher [E004] but does not specify its invocation syntax or output; CLI acceptance criteria require verification against the launcher source.' Downgrade verification from Demonstration to 'needs evidence' pending confirmation.

Optional human revised fix:
> 采用模型建议:在 NFR-004 与 Section 3 命令行行加注——E004 仅确认存在命令行 launcher,未给出调用语法/输出,CLI 验收标准需对照 launcher 源码确认。把该项验证标注为"待证据"而非可演示。E004 原文在 "The command line looks like this:" 处截断,确无任何命令语法,现 SRS 的 CLI 验收无可导出的接受标准。

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> Issue 成立(major)。E004 只说 "JSeats provides both a clean java API and a command line launcher",并在 "The command line looks like this:" 后截断,无任何命令语法/参数/输出。NFR-004、Section 3 命令行行把 CLI 当可演示行为,但证据无法导出验收标准。应加注并降级为待证据,接受。CLI"存在"本身有据,故不删,仅标注不可验证。

### R003: scope

- Severity: `minor`
- Suggested action: `accept_as_issue`
- SRS location: Section 2 Product perspective, Section 1 Product scope
- Evidence IDs: E004

**Claim or gap**

E004 explicitly states 'A web interface is planned.' The SRS correctly excludes it but does not note this planned-but-unimplemented scope boundary, which is relevant for scope clarity.

**Model opinion**

Noting the planned (unimplemented) web interface as out-of-scope would strengthen scope accuracy and prevent reviewers from assuming the omission was an oversight. This is a positive exclusion that should be made explicit.

**Recommended human check**

Confirm via README that the web interface is planned and not present at this commit.

**Model proposed SRS change**

Add to Section 1 Product scope: 'A web interface is mentioned as planned in repository documentation but is out of scope for this specification as it is not evidenced as implemented at this commit. [E004]'

Optional human revised fix:
> 采用模型建议:在 Section 1 Product scope 加一句,说明仓库文档提到 web interface 属计划中、本提交未实现,故列为范围外(E004)。该声明完全基于 E004 的 "A web interface is planned",显式标注正向排除可避免审阅者误以为是遗漏。

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> Issue 成立(minor)。E004 明确 "A web interface is planned"。SRS 正确地未把它当已实现功能,但也未点明这一"计划未实现"的范围边界。补一句显式排除有据、提升范围清晰度,接受。

### R004: unsupported_claim

- Severity: `minor`
- Suggested action: `needs_human_check`
- SRS location: FR-002, DR-002
- Evidence IDs: E001

**Claim or gap**

FR-002 states the system supports 'construction of tally data from candidate vote totals' citing [E001]. E001 shows tally.addCandidate(new Candidate("Green Party",100)) which supports this, but the chunk is truncated. The vote-count association (DR-002) is reasonable but rests on a single truncated example.

**Model opinion**

The claim is plausibly supported by the visible E001 snippet (Candidate name + integer). It is low-risk but rests on truncated evidence. The Candidate class signature should be confirmed to validate that the second argument is indeed a vote count.

**Recommended human check**

Inspect Candidate.java constructor to confirm the integer parameter represents vote count and that addCandidate is the construction path.

**Model proposed SRS change**

No change if Candidate(name, int votes) is confirmed. If the integer is not a vote count, revise FR-002/DR-002 to reflect the actual semantic of the Candidate constructor parameter.

Optional human revised fix:
> 定论前查看 Candidate.java 构造函数。E001 仅可见 `tally.addCandidate(new Candidate("Green Party",100))` 且片段在此截断,整数 100 是否确为票数无法从证据确认。模型的"确认则不改、否则改 FR-002/DR-002"是条件式处理,方向正确,但必须先核 Candidate 构造签名。当前 FR-002/DR-002 把该整数当作 vote count 属合理但单点截断证据上的推断,暂不改、待核。

**Human decision**

- [ ] Accept
- [ ] Reject
- [x] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> 证据不足,需讨论(minor)。`new Candidate("Green Party",100)` 中第二个参数是否为票数,需核 Candidate.java 构造函数;E001 在此截断,无法仅凭证据确认。推断合理但属低风险单点证据,确认前不宜直接接受或否定。

### R005: missing_requirement

- Severity: `minor`
- Suggested action: `accept_as_issue`
- SRS location: FR-006, DR (data)
- Evidence IDs: E006

**Claim or gap**

FR-006 / E006 reference HighestAveragesMethod which defines an abstract nextDivisor(int round) method, implying a per-round divisor progression and that each concrete method (D'Hondt, Sainte-Lague, etc.) supplies its own divisor sequence. The SRS describes 'method-specific divisor progression' but does not capture the extensibility point (abstract nextDivisor) as a contract.

**Model opinion**

The abstract nextDivisor(int round) is a meaningful extension contract for highest-averages variants and supports NFR-001 (extensibility). It is partially captured but could be made explicit as the mechanism by which divisor variants are implemented.

**Recommended human check**

Confirm in HighestAveragesMethod.java that nextDivisor(int round) is the abstract hook implemented by each variant; verify the truncated process() loop logic.

**Model proposed SRS change**

Augment FR-006 system behavior: 'Each highest-averages variant shall define its divisor sequence via an abstract nextDivisor(round) operation, enabling D'Hondt, Sainte-Lague, Imperiali, and Danish variants. [E006]'

Optional human revised fix:
> 采用模型建议:在 FR-006 系统行为补充——各 highest-averages 变体通过抽象操作 `nextDivisor(int round)` 定义自身除数序列,从而支撑 D'Hondt、Sainte-Lague、Imperiali、Danish 等变体(E006)。E006 明确可见 `public abstract double nextDivisor(int round);`,这是 NFR-001 可扩展性的具体机制,补为显式契约有据。

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> Issue 成立(minor)。E006 显式给出 `HighestAveragesMethod` 的抽象方法 `nextDivisor(int round)`,这是各除数变体的扩展挂钩。SRS 仅泛称 "method-specific divisor progression",未捕获该抽象契约。补为显式机制提升完整性并坐实 NFR-001,接受。

### R006: ambiguity

- Severity: `minor`
- Suggested action: `accept_as_issue`
- SRS location: FR-005, DR-005
- Evidence IDs: E005

**Claim or gap**

E005 includes a code comment 'TODO this requires more testing for rounding errors.' The SRS presents the (potentialVotes/2)+1 formula as a firm requirement with High traceability confidence but does not flag the documented rounding-correctness uncertainty.

**Model opinion**

The formula is accurately extracted, but the source explicitly flags it as needing more testing for rounding errors. Presenting it as a settled, High-confidence requirement slightly overstates certainty. A note preserves fidelity to the evidence.

**Recommended human check**

Confirm the TODO comment is present and decide whether to annotate the requirement's maturity/known-limitation status.

**Model proposed SRS change**

Add a note to FR-005/DR-005: 'Source code notes this computation requires further testing for rounding errors (developer TODO), indicating the rounding behavior is not finalized. [E005]'

Optional human revised fix:
> 采用模型建议:在 FR-005/DR-005 加注——源码注明该计算需进一步测试舍入误差(开发者 TODO),说明舍入行为尚未定型(E005)。E005 明确含注释 `// TODO this requires more testing for rounding errors.`,而 SRS 以 High 置信把 `(potentialVotes/2)+1` 当成定稿需求,加注以保真证据中的已知不确定性。

**Human decision**

- [ ] Accept
- [ ] Reject
- [x] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> Issue 成立(minor)。E005 源码内明确标 `TODO this requires more testing for rounding errors`,而 FR-005/DR-005 以 High 置信呈现该公式为既定需求,略微夸大确定性。加一条已知限制注记即可,公式本身提取准确无需改动,接受。

### R007: traceability

- Severity: `minor`
- Suggested action: `accept_as_issue`
- SRS location: Section 1 Product scope, FR-003
- Evidence IDs: E004

**Claim or gap**

The Majority family in E004 lists Simple, Qualified, Absolute sub-variants; FR-003 lists 'Majority' but does not enumerate Simple/Qualified/Absolute, while the scope section enumerates Highest Averages variants. Enumeration is inconsistent across the method families.

**Model opinion**

Minor consistency issue: E004 provides a full hierarchy (Majority: Simple/Qualified/Absolute; Ranked: by votes). The SRS partially enumerates. For traceability completeness, the supported-methods table should mirror the README hierarchy.

**Recommended human check**

Compare the SRS supported-methods listing against the README's full method hierarchy and align enumeration.

**Model proposed SRS change**

Expand FR-003 to enumerate per E004: 'Majority (Simple, Qualified, Absolute), Ranked (by votes), Equal Proportions (Huntington-Hill), Largest Remainder (Hare, Droop, Imperiali), Highest Averages (D'Hondt, Sainte-Lague/Webster with user-provided first divisor, Imperiali, Danish). [E004]'

Optional human revised fix:
> 采用模型建议:把 FR-003 的方法清单按 E004 README 层级补全——Majority(Simple/Qualified/Absolute)、Ranked(by votes)、Equal Proportions(Huntington-Hill)、Largest Remainder(Hare/Droop/Imperiali)、Highest Averages(D'Hondt、Sainte-Lague/Webster 含用户自定首除数、Imperiali、Danish)。E004 给出完整层级,SRS 现仅部分枚举(Highest Averages 变体列了、Majority 子变体没列),对齐即可,无新增证据外内容。

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> Issue 成立(minor)。E004 列出完整方法层级(含 Majority 的 Simple/Qualified/Absolute、Ranked by votes),SRS 的 FR-003 枚举不一致——有的家族列了变体、Majority 没列。按 README 层级对齐枚举提升追溯完整性,有据,接受。

### R008: architecture_detail

- Severity: `minor`
- Suggested action: `needs_human_check`
- SRS location: Section 2 Product perspective
- Evidence IDs: none

**Claim or gap**

A ground-truth architecture diagram exists (jseats_architecture.png) but the SRS does not reference or reconcile any architectural structure against it (e.g., processor -> method -> decorator pipeline).

**Model opinion**

The architecture image is available as ground truth. The SRS's implied architecture (processor, method contract, decorator) should be checked against the diagram to confirm component relationships and any data-flow not captured by the code chunks.

**Recommended human check**

Review jseats_architecture.png and confirm that the SRS component model (SeatAllocatorProcessor, SeatAllocationMethod, ResultDecorator, Tally) matches the diagram's depicted architecture and pipeline.

**Model proposed SRS change**

Add an architecture overview paragraph to Section 2 reconciled with the diagram once reviewed: 'The architecture comprises a processor orchestrating a selected SeatAllocationMethod over a Tally, producing a Result optionally transformed by a ResultDecorator (verify against jseats_architecture.png).'

Optional human revised fix:
> 定论前查看 jseats_architecture.png。该图不在证据包(本条 Evidence IDs=none),不能据以补充架构段落。模型拟写的概览("processor orchestrating a selected SeatAllocationMethod over a Tally ... optionally transformed by a ResultDecorator")与现有代码 chunk 推断一致、读来合理,但其定位是"reconcile against 图",必须先核图确认组件关系与数据流再写入。

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> 可按模型建议在 Section 2 补一段与图对账的架构概览,并据图补充 filter/tie-breaker 阶段。
