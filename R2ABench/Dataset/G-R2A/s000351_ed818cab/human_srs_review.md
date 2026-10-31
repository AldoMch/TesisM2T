# Human SRS Review Sheet

## Metadata

- Sample directory: `s000351_ed818cab`
- Generated SRS: `final_srs.md`
- Evidence pack: `evidence_pack.json`
- Review model: `claude-opus-4-8`
- Generated at: `2026-06-05T16:10:46.665722Z`
- Raw model response: `model_srs_review_raw.md`
- Parse status: `parsed`

## Overall Model Opinion

- Recommendation: `revise`
- Confidence: `0.72`
- Rationale: The SRS is generally well-grounded in the README evidence and traceability is strong. However, several specific CLI option claims (-w, -wi, -ws, -d, -i), the GPU client mode, and the 30-second example are stated as concrete behaviors that are partially or not directly supported by the truncated evidence text. The architecture diagram (DOC/architecture.jpg) is not referenced or checked. A few inferred items are presented with more certainty than evidence supports.

## Overall Human Decision

- [ ] Accept
- [ ] Reject
- [ ] Partial accept

Reason:
> 

## Positive Observations

- Scope is correctly and conservatively limited to README evidence and to SECP256K1 interval ECDLP via Pollard's kangaroo with distinguished points (E004/E005).
- The unauthenticated-server security constraint (NFR-004, C-003) is accurately and faithfully derived from the explicit README warning (E002).
- wsplit backup/reset and offline merge behavior, including the merge-time RAM caveat, are well captured and correctly traced to E001/E006.
- Inferred items (NFR-005, Assumptions) are explicitly labeled as inferred, supporting transparent adjudication.
- Traceability matrix is complete with evidence types, verification methods, and confidence levels per requirement.

## Candidate Issues

### R001: architecture_detail

- Severity: `minor`
- Suggested action: `needs_human_check`
- SRS location: Section 2 Product Perspective / overall SRS
- Evidence IDs: none

**Claim or gap**

The repository includes a ground-truth architecture diagram (DOC/architecture.jpg) that is never referenced or reconciled in the SRS.

**Model opinion**

The SRS bases everything on README text and ignores the available architecture image. The diagram may show the server/client topology, kangaroo herd interactions, or data flow that could confirm or refine FR-010/FR-011 and the Product Perspective. This should be checked rather than assumed irrelevant.

**Recommended human check**

Open DOC/architecture.jpg and compare its depicted components/data flow against Section 2 and FR-010/FR-011. Confirm whether the diagram adds components (e.g., distinct server, multiple clients, GPU workers) not captured.

**Model proposed SRS change**

Add to Section 1 References: 'Architecture diagram: DOC/architecture.jpg'. After human review of the image, add a sentence to Section 2 Product Perspective summarizing the server/client/GPU topology shown, with an architecture-derived evidence note.

Optional human revised fix:
> 

**Human decision**

- [ ] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> 

### R002: unsupported_claim

- Severity: `major`
- Suggested action: `needs_human_check`
- SRS location: FR-011, NFR/Operating Environment, Traceability FR-011
- Evidence IDs: E002

**Claim or gap**

FR-011 asserts a 'documented GPU client mode' and clients 'participate in distributed computation'. Evidence E002 only mentions 'Starting client, using gpu and connect to the server linpons' as a usage line; whether GPU is a first-class mode versus an example invocation is not clearly established.

**Model opinion**

The README snippet shows a single example line referencing gpu and a server name 'linpons'. Calling it a 'documented GPU client mode' overstates the evidence; it may be one example among others. The claim of 'participate in distributed computation' is reasonable inference but not explicitly described in the truncated text.

**Recommended human check**

Review full README usage section for client options to confirm whether GPU is an explicit selectable mode/flag or just an example. Verify how clients contribute work.

**Model proposed SRS change**

Revise FR-011 System Behavior/Output to: 'The system shall connect a client to a named server; usage examples include starting a GPU-enabled client (example server name: linpons).' Downgrade 'GPU client mode' to 'GPU-enabled client invocation (per usage example)' until confirmed.

Optional human revised fix:
> 

**Human decision**

- [ ] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> 

### R003: traceability

- Severity: `minor`
- Suggested action: `accept_as_issue`
- SRS location: FR-004, FR-005, FR-006 (CLI options -w, -wi, -ws, -i, -d)
- Evidence IDs: E001, E003, E006

**Claim or gap**

Several requirements reference specific options (-w, -wi, -ws, -i, -d) implicitly through behavior, but the SRS narrative does not name the actual option flags even though E003 explicitly lists them; conversely the '30-second example' (FR-004) comes from E001/E006 which only say 'save work file every 30 seconds' as an example workflow, not a guaranteed feature.

**Model opinion**

The evidence supports save/resume/dp-size options and a 30-second example. The SRS could strengthen traceability by naming the flags from E003 (-w, -wi, -ws, -d, -i) and should frame '30 seconds' as an example value rather than a documented system capability. FR-004 currently embeds 'including the documented 30-second example workflow' which is fine as example but should not imply 30s is a fixed requirement.

**Recommended human check**

Confirm in full README/Usage the exact flags and their semantics; verify save interval is user-configurable (not fixed at 30s).

**Model proposed SRS change**

In FR-004 change '...at the configured interval, including the documented 30-second example workflow' to '...at a user-configured save interval (README example uses 30 seconds).' In FR-005/FR-006 reference the README option flags (-i for resume, -ws for kangaroo state, -d for DP size) per E003.

Optional human revised fix:
> 

**Human decision**

- [ ] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> 

### R004: missing_requirement

- Severity: `minor`
- Suggested action: `needs_human_check`
- SRS location: Constraints / Section 7
- Evidence IDs: E002

**Claim or gap**

E002 contains a warning about clients reconnecting and sending 'wrong points' ('...otherwise they will reconnect and send wrong points'). This operational constraint about client behavior on reconnection is not captured.

**Model opinion**

The truncated text indicates a constraint that clients must be handled carefully or they reconnect and send wrong points. This is an evidence-supported operational constraint that the SRS omits. The preceding context is cut off, so the exact precondition is unclear.

**Recommended human check**

Read the full sentence preceding 'otherwise they will reconnect and send wrong points' in README to identify the precondition (likely about not changing config/DP bits mid-run).

**Model proposed SRS change**

After verifying the full sentence, add a constraint C-005: 'Distributed clients must be managed per documented guidance to avoid reconnections that submit invalid points.' Cite E002. Make conditional on confirming the precondition.

Optional human revised fix:
> 

**Human decision**

- [ ] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> 

### R005: non_verifiable

- Severity: `minor`
- Suggested action: `accept_as_issue`
- SRS location: NFR-005
- Evidence IDs: E003

**Claim or gap**

NFR-005 ('support continuation across different hardware or changed DP settings, but performance may degrade') is marked inferred and verified by Demonstration, but 'performance may degrade' has no measurable acceptance criterion.

**Model opinion**

E003 supports that continuation across changed hardware/DP settings is possible but 'performance may not be optimal'. The requirement is acceptable as a portability note but is not independently verifiable as written ('may degrade'). It is reasonably evidence-backed, so I would keep it but flag verifiability.

**Recommended human check**

Confirm README wording supports continuation across changed hardware/DP bits; decide whether to keep as informational note or define a measurable criterion.

**Model proposed SRS change**

Reframe NFR-005 acceptance basis to: 'A saved work file resumes successfully on changed hardware or DP settings (functional success); performance is informational, not a pass/fail criterion.'

Optional human revised fix:
> 

**Human decision**

- [ ] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> 

### R006: ambiguity

- Severity: `minor`
- Suggested action: `accept_as_issue`
- SRS location: FR-002, DR-001/DR-002
- Evidence IDs: E004, E005

**Claim or gap**

FR-002 states the system will produce 'input rejection on invalid format', but the evidence (E004/E005) only describes accepted formats (hex values; compressed/uncompressed keys) and does not document rejection/error handling behavior.

**Model opinion**

The acceptance of hex and both key encodings is well supported. The added 'input rejection on invalid format' is a plausible but unsupported assertion about error handling not present in the evidence.

**Recommended human check**

Check README/Usage for any documented input validation or error behavior. If none, remove the rejection claim.

**Model proposed SRS change**

In FR-002 Output, change 'Parsed problem instance or input rejection on invalid format' to 'Parsed problem instance.' unless error handling is confirmed in evidence.

Optional human revised fix:
> 

**Human decision**

- [ ] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
>
