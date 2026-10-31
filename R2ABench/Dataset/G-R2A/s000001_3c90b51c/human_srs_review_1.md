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
> As reviewer A, I completed the issue-by-issue human review for s000001_3c90b51c. The overall judgment is Partially Accepted because the candidate review contains a combination of accepted issues, 1 partially accepted issue, and 1 rejected issue (ACCEPT=5, PARTIAL_ACCEPT=1, REJECT=2). 

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
> Revise FR-001 to distinguish two interfaces: FR-001a: The system shall provide a caller-facing seat allocation entry point that allows callers to submit tally data, select an allocation method, and provide configuration parameters; the system returns an allocation result or reports an allocation error. FR-001b: The system shall define a processing contract that each allocation method must satisfy: an allocation method receives a protected view of the tally data and configuration parameters, and returns an allocation result or reports an allocation error. C-002: The immutable tally constraint applies only to the allocation-method contract and must not be extended into a global constraint on the caller-facing entry-point API.

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> I accept this issue. E001 demonstrates the higher-level caller-facing `SeatAllocatorProcessor` interface, while E002 defines the lower-level `SeatAllocationMethod` contract involving `InmutableTally` and `Properties`. The current SRS merges these two API surfaces into a single processing API, making the requirement level and constraint scope unclear. This confusion should be corrected, but the model's proposed revision is too close to implementation detail; it should be reframed as an interface-behavior requirement at the SRS level.

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
> The system shall provide a command-line interface that supports users querying available allocation methods and related extensions, submitting candidate vote totals or reading tally/configuration files, selecting an allocation method and setting processing parameters, and generating tally, allocation-result, or configuration output when output options are specified. Verification shall be based on the CLI capabilities declared in the README and the launcher implementation, confirmed through demonstration or testing.

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> The complete README and `SeatAllocatorLauncher.java` provide concrete CLI options. The SRS only needs to enrich the CLI requirement.

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
> After review, the current evidence does not show an implemented web interface. Therefore, web-interface-related requirements should be removed from the SRS to avoid presenting planned or unverified functionality as current system capability.

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> I accept this issue. E004 explicitly indicates that a web interface is planned, while the SRS focuses on the Java API and command-line launcher. Because planned but unimplemented functionality can easily be mistaken for current scope, the SRS should delete the web-interface content directly.

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
> 

**Human decision**

- [ ] Accept
- [ ] Reject
- [x] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> I reject this issue. The model's concern is mainly based on the truncation of E001, but source-code inspection resolves the ambiguity: `Candidate.java` contains the `votes` field, the `Candidate(String, int)` constructor, `setVotes`, and `getVotes`. Therefore, the SRS claim that candidate entries include vote totals is supported and should not be treated as an unsupported claim.

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
> The highest-averages allocation function shall support divisor sequences defined by the specific variant and shall calculate each candidate's priority in each seat-allocation round according to that variant's divisor rule. Different highest-averages variants shall be able to produce their corresponding seat-allocation results through their respective divisor sequences. Source: [E006].

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> I accept this question. E006 directly displays the `HighestAveragesMethod` declaration abstract `nextDivisor(int round)` operation. The current SRS mentions a method-specific divisor series, but it does not capture the explicit extension point to achieve the highest average variant. Adding this detail is evidence-based, smaller in scope, and helps enforce the contract retrospectively.

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
> 

**Human decision**

- [ ] Accept
- [ ] Reject
- [x] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> I reject this issue. This is an implementation-side test risk or verification note, not a requirement that the system must satisfy.

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
> Expand the method enumeration and scope text in FR-003 to mirror E004. Suggested SRS text: Supported methods include majority (simple, qualified, absolute), ranking (by voting), equal proportions (Huntington-Hill), maximum remainder (Hare, Droop, Imperali), and maximum average (D'Hondt, Sainte-Lague/Webster and user-supplied first divisor, Imperali, Danish). Source: [E004].

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> I accept this question. E004 provides a more complete method hierarchy than SRS currently enumerates. SRS mentions method families and some variants, but omits details of most subvariants and ranking by vote when listing other variants. This is a minor traceability and consistency flaw that can be fixed by enumerating the evidence directly.

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

Review jseats_architecture.png and confirm that the SRS component model (SeatAlloczatorProcessor, SeatAllocationMethod, ResultDecorator, Tally) matches the diagram's depicted architecture and pipeline.

**Model proposed SRS change**

Add an architecture overview paragraph to Section 2 reconciled with the diagram once reviewed: 'The architecture comprises a processor orchestrating a selected SeatAllocationMethod over a Tally, producing a Result optionally transformed by a ResultDecorator (verify against jseats_architecture.png).'

Optional human revised fix:
> The system shall support a configurable seat-allocation workflow: a user or caller can provide tally data and configure allocation parameters, the allocation method, tally filtering rules, tie-breaking rules, and result output decoration rules; the system shall process the tally data according to that configuration, execute the selected seat-allocation method, and generate the final allocation result that conforms to the configuration. Source: `jseats_architecture.png` and `SeatAllocatorProcessor.java`.

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> I accept this question. The architecture diagram and `SeatAllocatorProcessor.java` show the specific processing pipeline: candidates and votes form `Tally`, the configuration provides parameters, methods, filters, tiebreakers and result decorators, and the processor executes Filter, Process and Decorate before generating the results. SRS The related API elements are mentioned, but they are not coordinated into this architectural process.
