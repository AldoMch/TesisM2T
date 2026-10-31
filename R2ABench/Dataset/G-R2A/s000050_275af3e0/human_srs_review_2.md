# Human SRS Review Sheet

## Metadata

- Sample directory: `s000050_275af3e0`
- Generated SRS: `final_srs.md`
- Evidence pack: `evidence_pack.json`
- Review model: `claude-opus-4-8`
- Generated at: `2026-06-05T15:51:08.828418Z`
- Raw model response: `model_srs_review_raw.md`
- Parse status: `parsed`

## Overall Model Opinion

- Recommendation: `revise`
- Confidence: `0.72`
- Rationale: The SRS is generally well-traced to the evidence pack and conservative in scope, but it misses the project's core identity (hAFL2 as a Hyper-V hypervisor/distributed cloud fuzzer, per the architecture diagram and repo name) and includes a few claims with weaker support than asserted. Several constraints traced to E003 actually belong to E004 and vice versa, and the C-005 'restart VM' detail is partially inferred. The architecture diagram referenced in scope is not represented in the SRS at all.

## Overall Human Decision

- [ ] Accept
- [ ] Reject
- [ ] Partial accept

Reason:
> 

## Positive Observations

- Requirements are conservatively scoped to retrieved evidence chunks and most claims carry explicit evidence IDs.
- Strong traceability matrix linking FR/NFR/DR/C items to evidence with confidence ratings.
- Deterministic mutation invariants (NFR-002 payload restoration, NFR-003 Hamming-distance) are accurately derived from the test code in E005/E006 and are genuinely verifiable.
- Verification and Acceptance section provides concrete, mostly testable criteria for each requirement.
- Windows helper binary roles (packet_sender.exe / loader.exe) are accurately captured from E003.

## Candidate Issues

### R001: scope

- Severity: `major`
- Suggested action: `needs_human_check`
- SRS location: Section 1 Product Scope / Section 2 Product Perspective
- Evidence IDs: E003, E004

**Claim or gap**

The SRS frames hAFL2 narrowly as a 'fuzzing support toolset' (test runner, Linux launch scripts, Windows binaries) and omits the project's core identity as a Hyper-V hypervisor / distributed cloud fuzzing system, which is implied by the repo name (hAFL2), the root/child partition VM terminology, and the referenced Architecture.png.

**Model opinion**

The evidence pack chunks (E003, E004) repeatedly reference root partition VM, child partition VM, netvsc packet sending to the root partition, and Hyper-V-style virtualization. The ground-truth image URL is an Architecture diagram. The SRS understates the system scope by treating it as a support toolset rather than a hypervisor fuzzing platform. This is a meaningful scope understatement, though the available text chunks are sparse on the overall architecture.

**Recommended human check**

Open the repository README and Architecture.png to confirm hAFL2 is a Hyper-V / distributed cloud hypervisor fuzzer. If confirmed, widen the Product Scope/Perspective to describe the hypervisor fuzzing architecture (root vs child partition, netvsc target).

**Model proposed SRS change**

In Section 2 Product Perspective, add: 'hAFL2 is a fuzzing system targeting the Hyper-V virtualization stack, operating across root and child partition VMs and fuzzing the netvsc network path to the root partition. The evidenced artifacts (test runner, Linux launch scripts, Windows helper binaries/drivers) are components of this larger fuzzing platform.' Conditional on diagram/README confirmation.

Optional human revised fix:
> 

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> 没有引用架构图。issue不成立。

### R002: architecture_detail

- Severity: `major`
- Suggested action: `needs_human_check`
- SRS location: Section 1 References / Section 3 External Interfaces
- Evidence IDs: E004

**Claim or gap**

The architecture diagram (Architecture.png) named as the ground-truth image is not referenced or reflected anywhere in the SRS, and the netvsc-to-root-partition packet path (E004) is not captured as an interface/data-flow requirement.

**Model opinion**

E004 explicitly mentions 'use it in order to send packets to the root partition' via a netvsc global list pointer. This is a core data-flow detail for the Windows/Hyper-V fuzzing path that the SRS only captures obliquely as 'packet-sending IOCTL.' The architecture diagram should be checked to confirm the communication topology.

**Recommended human check**

Inspect Architecture.png and tutorial.md to confirm the netvsc->root-partition packet flow and whether it should be an explicit communication interface requirement.

**Model proposed SRS change**

In Section 3 Communication Interfaces, add: 'The Windows fuzzing workflow locates the netvsc global list pointer to send packets from the child partition to the root partition. Source: E004.' Add the Architecture diagram URL to Section 1 References and a note that the architecture topology is documented in Architecture.png.

Optional human revised fix:
> 建议采纳 E004 支持的 netvsc/root-partition data flow；但对于架构图部分不做任何修改。

**Human decision**

- [ ] Accept
- [ ] Reject
- [x] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> issue部分成立，E004 直接支持从 child partition/netvsc 向 root partition 发送 packets 的通信路径，当前表述过于笼统。但是没有涉及到架构图部分，这一表述属于模型偏好。

### R003: traceability

- Severity: `major`
- Suggested action: `needs_human_check`
- SRS location: C-005, C-006 (Section 7) and traceability matrix
- Evidence IDs: E003, E004

**Claim or gap**

Constraint C-005 (DSE disablement + VM restart) is traced to E003, but the 'restart the child partition VM after you're done' text appears in E003 while the configuration-off-state details belong to E004. C-006 is traced to E004 correctly, but the evidence assignment between C-005 and C-006 should be re-checked for accuracy.

**Model opinion**

E003 does contain 'Disable Child Partition DSE ... (restart the child partition VM after you're done)', so C-005's E003 trace is supportable. However, the SRS Verification table for C-005 asserts 'DSE disablement is executed from an elevated command prompt and the child partition VM is restarted' — the elevated command prompt detail is in E003 and is fine. This is borderline; main concern is ensuring no cross-attribution error. Low-to-medium risk.

**Recommended human check**

Re-read E003 and E004 to confirm C-005 maps to E003 (DSE + elevated prompt + restart) and C-006 maps to E004 (VM off before configuration). Confirm no detail is fabricated.

**Model proposed SRS change**

No change if traces verify. If misattributed, correct the Source Evidence column for C-005/C-006 accordingly.

Optional human revised fix:
> 

**Human decision**

- [ ] Accept
- [x] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> issue不成立，C-005/C-006 证据映射基本成立，属于模型偏好。

### R004: ambiguity

- Severity: `minor`
- Suggested action: `probably_ignore`
- SRS location: FR-002 / E002
- Evidence IDs: E002

**Claim or gap**

FR-002 and E002 state the binary is 'launched via [blank]' — the evidence text shows a truncated/missing launch mechanism ('launched via .'). The SRS does not flag that the specific launch mechanism is unknown from evidence.

**Model opinion**

The evidence chunk E002 has a gap: 'packaged into an initrd and launched via .' The launch transport (likely QEMU/kAFL) is elided. The SRS reasonably abstracts to 'launched in kAFL,' but should not imply a verified launch mechanism beyond what E002 provides.

**Recommended human check**

Inspect the full tests/user_bench/README.md to recover the elided launch mechanism (e.g., QEMU/kAFL invocation).

**Model proposed SRS change**

In FR-002 System Behavior, soften to: 'The system shall build an initrd containing the selected binary and launch it in kAFL (specific launch transport per the user_bench launch scripts).' Optionally add an assumption that the exact launch command is defined in the launch scripts.

Optional human revised fix:
> 

**Human decision**

- [ ] Accept
- [x] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> issue不成立，当前证据能够支持binary “launched via [blank]”。证据没有写出具体的launch mechanism，SRS也没有列出实际的具体 launch mechanism，无需标注。属于模型偏好。

### R005: unsupported_claim

- Severity: `minor`
- Suggested action: `needs_human_check`
- SRS location: C-001 (License) traced to E001, E006
- Evidence IDs: E001, E006

**Claim or gap**

C-001 states repository artifacts are licensed AGPL-3.0-or-later based on E001/E006, both of which carry an Intel Corporation copyright header. The SRS does not note these are inherited kAFL/Intel files, which could mislead on the repository's own licensing.

**Model opinion**

E001 and E006 both bear 'Copyright (C) 2019-2020 Intel Corporation SPDX-License-Identifier: AGPL-3.0-or-later'. These are inherited kAFL files. Asserting the whole repository is AGPL-3.0-or-later from two Intel-headed test files is a mild over-generalization. The constraint is likely correct but the trace evidence is narrow.

**Recommended human check**

Check the repository root LICENSE file to confirm the project-wide license rather than relying on per-file headers in inherited kAFL files.

**Model proposed SRS change**

Reword C-001 to: 'Evidenced source files (kAFL-Fuzzer test utilities) carry AGPL-3.0-or-later SPDX headers (Intel Corporation). Confirm the repository-wide license against the root LICENSE file.' Source: E001, E006.

Optional human revised fix:
> 

**Human decision**

- [ ] Accept
- [ ] Reject
- [x] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> issue不成立，C-001 已经写明in evidence，不会产生误导。模型属于过度推断。

### R006: missing_requirement

- Severity: `minor`
- Suggested action: `probably_ignore`
- SRS location: Section 4 Functional Requirements / FR-001
- Evidence IDs: E001, E005

**Claim or gap**

E001 imports and runs random, deterministic, AND havoc test modules (rand_main, deter_main, havoc_main), but only deterministic mutation behavior (NFR-002/003) is captured as detailed non-functional requirements. The havoc and random test suites are mentioned in FR-001 but have no corresponding correctness requirements.

**Model opinion**

This is a minor completeness gap. FR-001 covers running all three suites, which is adequate at the functional level. Deterministic detail exists because E005/E006 provide it; random/havoc internals are not in the evidence pack, so no further requirements can be derived. Acceptable to leave as-is, but worth noting the asymmetry.

**Recommended human check**

Confirm there is no available test_random.py / test_havoc_handler.py evidence to support additional NFRs; if present, consider symmetric NFRs.

**Model proposed SRS change**

No change required unless random/havoc test evidence is retrieved. If retrieved, add NFRs mirroring NFR-002/003 for those suites.

Optional human revised fix:
> 

**Human decision**

- [ ] Accept
- [x] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> issue不成立，这种不成立是证据粒度不同导致的，没有造成影响，属于模型偏好，不必修改。

### R007: non_verifiable

- Severity: `minor`
- Suggested action: `needs_human_check`
- SRS location: FR-003 / Verification 'Demonstration'
- Evidence IDs: E002

**Claim or gap**

FR-003 acceptance criterion ('exhibits AFL-style I/O inside the guest via the embedded forkserver') is difficult to observe as a concrete, testable acceptance check; 'AFL-style I/O' is not operationally defined.

**Model opinion**

The evidence (E002) states the forkserver maps kAFL hypercalls to AFL-style I/O, so the requirement is supported, but the acceptance criterion is hard to verify objectively. Consider tying it to an observable outcome (successful fuzzing run / coverage feedback) rather than the abstract 'AFL-style I/O.'

**Recommended human check**

Determine an observable signal (e.g., successful target launch under kAFL with coverage feedback) that demonstrates forkserver operation.

**Model proposed SRS change**

Revise FR-003 acceptance to: 'A userspace target launches and runs under kAFL with the forkserver active, demonstrated by successful fuzzing iterations/coverage feedback.' Keep Source E002.

Optional human revised fix:
> 

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> issue成立，当前验收语句验收标准不清晰，建议采纳。
