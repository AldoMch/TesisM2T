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
- Rationale: The SRS is generally well-grounded in the README evidence and traceability is strong. However, several specific CLI option claims (-w, -wi, -ws, -d, -i), the GPU client mode, and the 30-second example are stated as concrete behaviors that are partially or not directly supported by the truncated evidence text. The architecture diagram (DOC/architecture.jpg) is not referenced or checked. A few inferred items are presented with more certainty than the evidence supports.

## Overall Human Decision

- [ ] Accept
- [ ] Reject
- [x] Partial accept

Reason:
> ACCEPT=5, PARTIAL_ACCEPT=1, REJECT=0.

## Positive Observations

- Scope is correctly and conservatively limited to README evidence and to SECP256K1 interval ECDLP via Pollard's kangaroo with distinguished points (E004/E005).
- The unauthenticated-server security constraint (NFR-004, C-003) is accurately and faithfully derived from the explicit README warning (E002).
- wsplit backup/reset and offline merge behavior, including the merge-time RAM caveat, are well captured and correctly traced to E001/E006.
- Inferred items (NFR-005, Assumptions) are explicitly labeled as inferred, supporting transparent adjudication.
- The traceability matrix is complete with evidence types, verification methods, and confidence levels per requirement.

## Candidate Issues

### R001: architecture_detail

- Severity: `minor`
- Suggested action: `accept_as_issue`
- SRS location: Section 2 Product Perspective / overall SRS
- Evidence IDs: none

**Claim or gap**

The repository includes a ground-truth architecture diagram (DOC/architecture.jpg) that is never referenced or reconciled in the SRS.

**Model opinion**

The SRS bases everything on README text and ignores the available architecture image. The diagram may show the server/client topology, kangaroo herd interactions, or data flow that could confirm or refine FR-010/FR-011 and the Product Perspective. This should be checked rather than assumed irrelevant.

**Recommended human check**

Open DOC/architecture.jpg and compare its depicted components/data flow against Section 2 and FR-010/FR-011. Confirm whether the diagram adds components such as distinct servers, multiple clients, or GPU workers that are not captured.

**Model proposed SRS change**

Add to Section 1 References: "Architecture diagram: DOC/architecture.jpg". After human review of the image, add a sentence to Section 2 Product Perspective summarizing the server/client/GPU topology shown, with an architecture-derived evidence note.

Optional human revised fix:
> In Section 2 Product perspective, add: "The architecture diagram shows that Kangaroo distributed execution can be coordinated by one or more wsplit-enabled servers and multiple clients; clients perform kangaroo computation and produce local kangaroo/work data, while servers periodically output work files/hash tables and result files. Later, an offline merger can combine multiple work files into a master work file/hash table and discover or aggregate solving results during the merge process."

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> The architecture diagram shows Server -wsplit, multiple Clients, each client's kangaroo file, server-produced work files/hash table and result.txt, and a Merger combining multiple work files into a master workfile/hash table. The current SRS only describes generalized client/server and work file behavior, and misses the important wsplit + multi-server/multi-client + offline-merge topology shown in the diagram.

### R002: unsupported_claim

- Severity: `major`
- Suggested action: `partial_accept_as_issue`
- SRS location: FR-011, NFR/Operating Environment, Traceability FR-011
- Evidence IDs: E002

**Claim or gap**

FR-011 asserts a documented GPU client mode and says clients participate in distributed computation. Evidence E002 only mentions "Starting client, using gpu and connect to the server linpons" as a usage line; whether GPU is a first-class mode versus an example invocation is not clearly established.

**Model opinion**

The README snippet shows a single example line referencing GPU and a server name "linpons". Calling it a documented GPU client mode overstates the evidence; it may be one example among others. The claim of participating in distributed computation is a reasonable inference but not explicitly described in the truncated text.

**Recommended human check**

Review the full README usage section for client options to confirm whether GPU is an explicit selectable mode/flag or just an example. Verify how clients contribute work.

**Model proposed SRS change**

Revise FR-011 System Behavior/Output to: "The system shall connect a client to a named server; usage examples include starting a GPU-enabled client (example server name: linpons)." Downgrade "GPU client mode" to "GPU-enabled client invocation (per usage example)" until confirmed.

Optional human revised fix:
> Revise FR-011 to: "The system shall support clients connecting to a specified server to participate in distributed execution; clients may run with general GPU-computation options, for example using GPU computation while connecting to a specified server."
> Revise Section 2 Operating environment to: "Clients may run in CPU or GPU-enabled command-line execution environments; GPU-related capability is enabled through command-line options."

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> The model is concerned that "GPU client mode" may come only from a truncated example, but the full README Usage explicitly lists -gpu, -gpuId, and -g, and the distributed section example is Kangaroo.exe -t 0 -gpu -c linpons. Therefore GPU support is not invented. However, "GPU client mode" can be written more accurately and should not be presented as a separate architecture mode.

### R003: traceability

- Severity: `minor`
- Suggested action: `accept_as_issue`
- SRS location: FR-004, FR-005, FR-006 (CLI options -w, -wi, -ws, -i, -d)
- Evidence IDs: E001, E003, E006

**Claim or gap**

Several requirements reference specific options (-w, -wi, -ws, -i, -d) implicitly through behavior, but the SRS narrative does not name the actual option flags even though E003 explicitly lists them; conversely, the 30-second example (FR-004) comes from E001/E006, which only say "save work file every 30 seconds" as an example workflow, not a guaranteed feature.

**Model opinion**

The evidence supports save/resume/dp-size options and a 30-second example. The SRS could strengthen traceability by naming the flags from E003 (-w, -wi, -ws, -d, -i) and should frame "30 seconds" as an example value rather than a documented system capability. FR-004 currently embeds "including the documented 30-second example workflow"; this is fine as an example but should not imply 30 seconds is a fixed requirement.

**Recommended human check**

Confirm in full README/Usage the exact flags and their semantics; verify save interval is user-configurable and not fixed at 30 seconds.

**Model proposed SRS change**

In FR-004 change "...at the configured interval, including the documented 30-second example workflow" to "...at a user-configured save interval (README example uses 30 seconds)." In FR-005/FR-006 reference the README option flags (-i for resume, -ws for kangaroo state, -d for DP size) per E003.

Optional human revised fix:
> Revise FR-004 to: "The system shall support using -w to specify a work file and -wi to specify the periodic save interval; the README example uses 30 seconds, but the save interval is user-configured."
> Revise FR-005 to: "The system shall support resuming a search from a saved work file using -i, without requiring the original input ASCII file."
> Revise FR-006 to: "The system shall support using -ws to save kangaroo state into a work file; -d is used to manually specify the distinguished-point bit count."

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> The README explicitly lists options such as -w, -wi, -ws, -i, and -d. The 30-second value is only the example -wi 30, not a fixed system requirement. The current SRS does not name the option flags and can make 30 seconds sound like fixed behavior.

### R004: missing_requirement

- Severity: `minor`
- Suggested action: `accept_as_issue`
- SRS location: Constraints / Section 7
- Evidence IDs: E002

**Claim or gap**

E002 contains a warning about clients reconnecting and sending wrong points ("...otherwise they will reconnect and send wrong points"). This operational constraint about client behavior on reconnection is not captured.

**Model opinion**

The truncated text indicates a constraint that clients must be handled carefully or they reconnect and send wrong points. This is an evidence-supported operational constraint that the SRS omits. The preceding context is cut off, so the exact precondition is unclear.

**Recommended human check**

Read the full sentence preceding "otherwise they will reconnect and send wrong points" in README to identify the precondition, likely about not changing config/DP bits mid-run.

**Model proposed SRS change**

After verifying the full sentence, add a constraint C-005: "Distributed clients must be managed per documented guidance to avoid reconnections that submit invalid points." Cite E002. Make conditional on confirming the precondition.

Optional human revised fix:
> Add C-005 in Section 7: "When a distributed server is restarted with a different configuration, especially when the solving range or target key changes, the operator must stop existing clients; otherwise clients may automatically reconnect and submit wrong points that do not match the new configuration."
> Add to Section 8 acceptance: "Inspect the distributed-running documentation and confirm that the operational constraint requiring clients to be stopped when server configuration changes is recorded."

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> The full README explains that if the server is restarted with a different configuration, such as changed range or key, all clients need to be stopped; otherwise clients will reconnect and send wrong points. The current SRS does not capture this distributed-operation constraint.

### R005: non_verifiable

- Severity: `minor`
- Suggested action: `accept_as_issue`
- SRS location: NFR-005
- Evidence IDs: E003

**Claim or gap**

NFR-005 ("support continuation across different hardware or changed DP settings, but performance may degrade") is marked inferred and verified by Demonstration, but "performance may degrade" has no measurable acceptance criterion.

**Model opinion**

E003 supports that continuation across changed hardware/DP settings is possible but "performance may not be optimal". The requirement is acceptable as a portability note but is not independently verifiable as written ("may degrade"). It is reasonably evidence-backed, so it should be kept but its verifiability should be fixed.

**Recommended human check**

Confirm README wording supports continuation across changed hardware/DP bits; decide whether to keep it as an informational note or define a measurable criterion.

**Model proposed SRS change**

Reframe NFR-005 acceptance basis to: "A saved work file resumes successfully on changed hardware or DP settings (functional success); performance is informational, not a pass/fail criterion."

Optional human revised fix:
> Revise NFR-005 to: "The system shall allow a work file to be continued or merged under the same key and range across different hardware, different distinguished-point bit counts, or different kangaroo-count configurations. These configuration changes may introduce additional overhead, but the overhead is an operational note rather than an acceptance criterion."
> Revise Section 8 NFR-005 acceptance to: "A saved work file can be successfully resumed or merged after hardware or DP-setting changes; performance variation is only an explanatory observation."

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> The README supports that a work file can continue across different hardware, different DP bit counts, and different kangaroo counts, but with overhead. However, "performance may degrade" cannot serve as a pass/fail acceptance criterion.

### R006: ambiguity

- Severity: `minor`
- Suggested action: `accept_as_issue`
- SRS location: FR-002, DR-001/DR-002
- Evidence IDs: E004, E005

**Claim or gap**

FR-002 states the system will produce input rejection on invalid format, but the evidence (E004/E005) only describes accepted formats (hex values; compressed/uncompressed keys) and does not document rejection/error handling behavior.

**Model opinion**

The acceptance of hex and both key encodings is well supported. The added "input rejection on invalid format" is a plausible but unsupported assertion about error handling not present in the evidence.

**Recommended human check**

Check README/Usage for any documented input validation or error behavior. If none, remove the rejection claim.

**Model proposed SRS change**

In FR-002 Output, change "Parsed problem instance or input rejection on invalid format" to "Parsed problem instance" unless error handling is confirmed in evidence.

Optional human revised fix:
> Revise FR-002 Output to: "Parsed problem instance."
> Revise FR-002 System behavior to: "The system shall parse hexadecimal input values and accept public keys in compressed or uncompressed form."
> Keep DR-001/DR-002 as positive format requirements and do not add error handling: "The input ASCII file shall contain problem values in hexadecimal format. Public key input shall allow compressed or uncompressed form."

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> The README only explains the input file format: all values are hex, and the public key can be compressed or uncompressed. It does not document invalid-format rejection behavior or an error message. The current FR-002 statement that invalid-format input is rejected goes beyond the evidence.
