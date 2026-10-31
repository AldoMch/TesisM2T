# Human SRS Review Sheet

## Metadata

- Sample directory: `s000093_425295b3`
- Generated SRS: `final_srs.md`
- Evidence pack: `evidence_pack.json`
- Review model: `claude-opus-4-8`
- Generated at: `2026-06-05T16:07:23.704956Z`
- Raw model response: `model_srs_review_raw.md`
- Parse status: `parsed`

## Overall Model Opinion

- Recommendation: `revise`
- Confidence: `0.78`
- Rationale: The SRS is internally consistent and well-traced to the provided evidence chunks, but the evidence pack is almost entirely OpenVR SDK header/binding boilerplate (openvr_api.cs/.json) that is vendored, not authored by this repository. The SRS therefore describes the OpenVR SDK rather than VirtualMotionTracker's actual product (a virtual tracker driver controlled via OSC, per the repo name and architecture). This is a significant scope problem: the core product functionality is missing, and several requirements are attributed to the repo when they belong to the upstream SDK.

## Overall Human Decision

- [ ] Accept
- [ ] Reject
- [ ] Partial accept

Reason:
> 

## Positive Observations

- Requirements that are present (FR-001..FR-005, NFRs, DRs) are each tied to specific evidence IDs with quoted-consistent content, and the traceability matrix is complete and internally coherent.
- The init/shutdown error semantics (Init_InterfaceNotFound, null return, pointer invalidation) in FR-002/FR-003 accurately reflect the E003 code snippet.
- The SRS appropriately uses verifiable acceptance criteria (Test/Inspection/Demonstration) for the requirements it does state.

## Candidate Issues

### R001: scope

- Severity: `critical`
- Suggested action: `needs_human_check`
- SRS location: Section 2 Product perspective; Section 4 FR-001..FR-003
- Evidence IDs: E003

**Claim or gap**

The SRS frames the product as an OpenVR scene application that initializes/validates/shuts down IVRSystem, but all of this behavior (E003) comes from `openvr/headers/openvr_api.cs`, which is the vendored Valve OpenVR SDK, not code authored by VirtualMotionTracker.

**Model opinion**

VirtualMotionTracker is, by repository name and architecture diagram, a virtual tracker driver that receives external input (OSC/network) and presents virtual trackers to SteamVR. The evidence pack retrieved only SDK header boilerplate, so the SRS describes OpenVR's own init/shutdown semantics and attributes them to this repository. FR-001/FR-002/FR-003 are SDK behaviors, not product requirements of this repo.

**Recommended human check**

Open `openvr/headers/openvr_api.cs` and confirm it is the upstream Valve OpenVR C# binding. Inspect the actual product source under `vmt_driver/` and the README to identify VMT's real functions (driver registration, OSC input, virtual device pose injection).

**Model proposed SRS change**

In Section 2 Product perspective and Section 1 Product scope, add a scoping note: 'Evidence E001-E003, E005-E006 originate from the vendored OpenVR SDK (openvr/headers/*) and describe upstream SDK behavior, not requirements authored by this repository.' Demote FR-001..FR-003 to a clearly labeled 'OpenVR SDK dependency behavior' subsection, or mark them as dependency assumptions rather than product functional requirements.

Optional human revised fix:
> 

**Human decision**

- [ ] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> 

### R002: missing_requirement

- Severity: `critical`
- Suggested action: `needs_human_check`
- SRS location: Section 4 Functional Requirements (whole)
- Evidence IDs: none

**Claim or gap**

The SRS omits the core VirtualMotionTracker functionality: creating/driving virtual trackers and receiving external control input (the architecture diagram and repo name strongly imply an OSC/network-driven virtual tracker driver).

**Model opinion**

Given the repository is named VirtualMotionTracker and ships `vmt_driver/`, the central evidenced behavior should be virtual device pose injection driven by external commands. None of this appears in the SRS because retrieval surfaced only SDK headers and one binding file. This is the most important gap.

**Recommended human check**

Review README.md, the architecture diagram (doc/Architecture.png), and source under `vmt_driver/` to enumerate the real functional requirements (e.g., OSC command set, virtual tracker creation, pose updates, room-setup). Confirm whether OSC/UDP is the control interface.

**Model proposed SRS change**

Add functional requirements for the core product after human verification, e.g., FR-006 'The system shall create and drive virtual trackers in SteamVR based on external control input', and FR-007 'The system shall accept control commands over [OSC/UDP — verify] to set tracker pose/state'. Conditional: only add once README/driver source is reviewed.

Optional human revised fix:
> 

**Human decision**

- [ ] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> 

### R003: traceability

- Severity: `major`
- Suggested action: `accept_as_issue`
- SRS location: Section 9 Traceability Matrix; DR-001/DR-004; FR-004
- Evidence IDs: E001, E002, E005, E006

**Claim or gap**

Several requirements are traced to vendored SDK header constants (E001, E002, E005, E006) as if they were product-authored data/interface requirements, giving misleadingly high confidence ('explicit', 'High').

**Model opinion**

Exposing `/user/foot/left` etc. (E001/E002) and using `TrackedDevicePose_t`/render-model structs (E005/E006) is simply the OpenVR SDK API surface. Attributing these as repository requirements inflates traceability quality. The evidence is genuine but mis-attributed to the product's scope.

**Recommended human check**

Confirm these constants/structs live only under `openvr/headers/` and are not redefined by VMT's own driver code. If so, mark them as upstream SDK surface, not product requirements.

**Model proposed SRS change**

In Section 9, add an 'Origin' column distinguishing 'repository-authored' vs 'vendored OpenVR SDK'. Mark FR-004, DR-001, DR-003, DR-004 as vendored-SDK-origin and lower their confidence/relevance accordingly, or move them to an Assumptions/Dependencies appendix.

Optional human revised fix:
> 

**Human decision**

- [ ] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> 

### R004: ambiguity

- Severity: `minor`
- Suggested action: `needs_human_check`
- SRS location: FR-005 / Section 8 acceptance basis
- Evidence IDs: E004

**Claim or gap**

E004 shows the binding mode 'button' and parameter sub_mode 'complex' and a 'Default binding for Sampl...' name, but FR-005 only captures three input->output mappings and omits mode/parameter semantics; the binding file is truncated.

**Model opinion**

The mapping claims are evidence-backed, but the binding file text is truncated ('Default binding for Sampl...'), so additional sources/inputs may exist. FR-005 should not be presented as exhaustive.

**Recommended human check**

Open the full `legacy_binding_mycontroller.json` to confirm whether additional input sources/mappings or left-hand bindings exist beyond the three evidenced.

**Model proposed SRS change**

In FR-005 and its acceptance basis, change wording to 'shall map at least the following right-hand inputs ...' and add a note that mode='button' with sub_mode='complex' applies; verify completeness against the full file.

Optional human revised fix:
> 

**Human decision**

- [ ] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> 

### R005: architecture_detail

- Severity: `major`
- Suggested action: `needs_human_check`
- SRS location: Section 3 Communication interfaces
- Evidence IDs: none

**Claim or gap**

The SRS states 'No network or inter-process communication protocol is directly evidenced', but the repository's architecture (and ground-truth diagram doc/Architecture.png) for a virtual motion tracker driver typically centers on a network/OSC control channel.

**Model opinion**

This is likely an understatement caused by retrieval gaps. A virtual tracker driver receiving external pose data almost always exposes a network/IPC interface. The 'no communication interface evidenced' claim should be re-examined against the diagram and driver source.

**Recommended human check**

Inspect doc/Architecture.png and driver source for a UDP/OSC listener or named-pipe/shared-memory interface. If present, add a communication-interface requirement.

**Model proposed SRS change**

Replace the Section 3 'Communication interfaces' statement with verified content. Conditional: if an OSC/UDP control channel exists, add 'The system shall receive tracker control input over [protocol/port — verify].'

Optional human revised fix:
> 

**Human decision**

- [ ] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
>
