<!-- human_srs_review_A.md aligned with reviewer C content. Original human_srs_review.md is preserved. All human judgments are in English. -->

# Human SRS Review Sheet

## Metadata

- Sample directory: `s000063_a02034f6`
- Generated SRS: `final_srs.md`
- Evidence pack: `evidence_pack.json`
- Review model: `claude-opus-4-8`
- Generated at: `2026-06-05T15:59:07.330084Z`
- Raw model response: `model_srs_review_raw.md`
- Parse status: `parsed`

## Overall Model Opinion

- Recommendation: `revise`
- Confidence: `0.74`
- Rationale: The SRS is generally well-traced to the evidence pack, but it over-attributes some protocol behaviors to the server (the MTProto docs describe client-side behavior, not necessarily implemented server requirements), and several FRs assert server-side guarantees that the evidence only documents as protocol description. A few items (FR-002/003/004 framing, FR-009 verification semantics) need human verification against actual code. The architecture diagram referenced in repository docs is not represented in the SRS.

## Overall Human Decision

- [ ] Accept
- [ ] Reject
- [x] Partial accept

Reason:
> ACCEPT=3, PARTIAL_ACCEPT=3, REJECT=0.

## Positive Observations

- Every requirement carries explicit evidence IDs and a traceability matrix, making adjudication straightforward.
- Conservative scoping language ('where the wrapper component is used', 'Optional media-processing dependency') appropriately qualifies the FFmpeg-related claims.
- Functional requirements for MTProto service messages (rpc_drop_answer, destroy_session, future salts) are accurately drawn from E004 with reasonable trigger/output decomposition.
- NFR-001 (Go implementation) and C-002 (MySQL/Redis/etcd/Kafka/MinIO dependencies) are directly and correctly supported by the README evidence.

## Candidate Issues

### R001: unsupported_claim

- Severity: `major`
- Suggested action: `partial_accept_as_issue`
- SRS location: FR-002, FR-003, FR-004, FR-005, NFR-002, DR-001/003/004
- Evidence IDs: E002

**Claim or gap**

These requirements state server-side behaviors (system shall provide salt, establish encrypted session, process registration info within the session). The cited evidence E002 is the MTProto protocol description and is written from the client's perspective ('the client obtains its server salt', 'the client then creates an encrypted session'). It describes protocol semantics, not verified server implementation behavior in this repository.

**Model opinion**

The SRS converts protocol-description prose into firm server functional requirements. This is reasonable for an MTProto server, but the evidence pack does not contain server code confirming these are implemented. The claims should be hedged or backed by code evidence rather than the protocol doc alone.

**Recommended human check**

Locate server-side code (e.g., auth/salt/session handlers) in the repository confirming salt issuance, encrypted session establishment, and registration handling, then attach those evidence paths to FR-002 through FR-005.

**Model proposed SRS change**

Add a note to FR-002-FR-005 and NFR-002: 'Behavior derived from the MTProto protocol description [E002]; confirm against server implementation code.' Conditionally, after locating handler code, replace the source evidence with code-level evidence IDs.

Optional human revised fix:
> Add a scope statement before Product Scope or the functional requirements: The system implements MTProto server capabilities; for protocol behaviors involving authorization keys, server salt, encrypted sessions, and related items, the SRS shall rely on both protocol documentation and server-side implementation evidence. Also narrow FR-002/FR-003/FR-004 wording from "the system fully executes the protocol flow" to "the server shall support/process the data and interactions required by the protocol."

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> The SRS content about MTProto authorization keys, server salt, and encrypted sessions mainly comes from the protocol documentation. The source code does show authsession implementation related to auth keys, future salts, and sessions, but the current SRS turns protocol descriptions directly into implemented system capabilities, so the evidence chain is too strong.

### R002: ambiguity

- Severity: `major`
- Suggested action: `partial_accept_as_issue`
- SRS location: FR-009, C-004, NFR/Acceptance for FR-009
- Evidence IDs: E001

**Claim or gap**

FR-009 states the system 'shall use 12345 as the default verification code for sign-in and sign-out' and that 'verification succeeds when code 12345 is supplied.' The README only states 'default signIn and signOut verify code is 12345.' It is ambiguous whether 12345 is the code the system sends/accepts in a demo/default config, and whether it applies to both sign-in and sign-out or is a development default only.

**Model opinion**

The README note is brief and likely describes a development/demo default. Treating it as a firm verification-success requirement may overstate it. The acceptance criterion 'code 12345 is accepted' needs confirmation of exact semantics (is it the code sent to the user, or a bypass code?).

**Recommended human check**

Inspect the verification-code configuration/code path to confirm whether 12345 is a fixed default accepted by the server and applies to both sign-in and sign-out, and whether it is intended only for non-production use.

**Model proposed SRS change**

Revise FR-009 to: 'Under the documented default configuration, the system shall use 12345 as the sign-in/sign-out verification code [E001]. (Confirm whether this is a development/demo default and the exact acceptance semantics.)' Add the development-default qualification once verified.

Optional human revised fix:
> Revise FR-009: Under the default/none verifier or test configuration, the system shall accept 12345 as the sign-in/sign-out verification code. When an external verification-code service is enabled, the verification code returned and checked by that external service shall be authoritative. Revise the acceptance criterion so it only verifies the default or none-verifier path.

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> The README states that the default sign-in/sign-out verification code is 12345, and the source code's none/default verifier also checks 12345, so the test/default path is valid. However, the SRS must not state that every production deployment always uses the fixed code 12345.

### R003: architecture_detail

- Severity: `minor`
- Suggested action: `accept_as_issue`
- SRS location: Section 2 Product perspective / Section 3
- Evidence IDs: E003, E005, E006

**Claim or gap**

The repository documents an architecture diagram (architecture-001.png, referenced as the ground-truth image) and the README has an 'Architecture' section, but the SRS does not describe the system's multi-service/microservice decomposition (the evidence paths reveal app/service/dfs, app/bff/authorization, app/messenger/msg, etc.).

**Model opinion**

Evidence paths strongly imply a microservice architecture (bff, messenger, dfs services). The SRS treats the product as a monolithic 'MTProto server.' This understates architectural scope. The diagram should be checked to capture key components.

**Recommended human check**

Review architecture-001.png and the README Architecture section to determine whether to add an architecture overview describing the major services (BFF/authorization, messenger/msg, dfs/media) and their dependencies.

**Model proposed SRS change**

Add to Section 2 Product perspective: 'The repository is organized as multiple services (e.g., BFF/authorization, messenger, distributed file service) as indicated by the source tree [E003][E005][E006] and the documented architecture diagram.' Verify against the diagram before finalizing.

Optional human revised fix:
> Add a high-level architecture description to Section 2 Product Perspective: The system uses a layered service architecture that includes a client access layer, BFF layer, business service layer, and storage layer. Services cooperate through RPC and message queues. Storage depends on Redis, MySQL, and MinIO, and asynchronous flows involve Kafka, Sync, Push, and related components. Describe only the derivable architecture and do not translate the architecture diagram box-by-box.

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> The architecture diagram and source structure show that the system is not a monolithic MTProto server. It includes a client access layer, BFF, service layer, storage layer, Kafka/Push/Sync, and other collaborating components. The current Product Perspective is too generic.

### R004: traceability

- Severity: `minor`
- Suggested action: `accept_as_issue`
- SRS location: DR-006, Section 2 user classes
- Evidence IDs: E005, E006

**Claim or gap**

DR-006 elevates 'DAL/DO/DAO terminology separation' to a data requirement based on two README glossary stubs (E005, E006) that only define terms in Chinese. This is terminology documentation, not a verifiable system data requirement.

**Model opinion**

The evidence supports that the codebase uses DAL/DO/DAO patterns, but framing 'terminology shall distinguish' as a requirement is weak and non-verifiable as a product behavior. Better as an architectural/development note than a data requirement.

**Recommended human check**

Decide whether DAL/DO/DAO is a meaningful product data requirement or merely an internal coding convention; consider demoting DR-006 to a development note.

**Model proposed SRS change**

Demote DR-006 to a development/architecture note: 'The codebase employs a Data Access Layer pattern distinguishing DAL, DO, and DAO components [E005][E006].' Remove the 'shall' requirement framing.

Optional human revised fix:
> Delete DR-006, or move it to an Architecture/development note: Some services in the codebase use a data access layer organization, where DAL means Data Access Layer, DO means Data Object, and DAO means Data Access Object. It is not recommended to keep this as a formal data requirement.

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> DAL/DO/DAO is only internal data-access-layer terminology in the codebase, not a user-facing or system-behavior data requirement. Keeping it in Data Requirements makes it look like a product requirement.

### R005: unsupported_claim

- Severity: `minor`
- Suggested action: `partial_accept_as_issue`
- SRS location: FR-008 / DR-002, Verification for FR-008
- Evidence IDs: E004

**Claim or gap**

FR-008 and its acceptance criterion state the system returns 'multiple' future salts. E004 is truncated ('between 1 and...') and does not confirm the count semantics or that the server implements this.

**Model opinion**

The 'several (between 1 and N)' range is cut off in the evidence, so 'multiple' is an inference. Acceptance criterion 'returns multiple salts' may not match the actual bound (could be 1).

**Recommended human check**

Confirm the future-salts range/count from the full Service_Messages doc and server implementation; adjust the acceptance criterion accordingly.

**Model proposed SRS change**

Revise FR-008 acceptance criterion to: 'A future-salts request returns the documented number of future salts (range to be confirmed from [E004] and implementation).'

Optional human revised fix:
> Revise FR-008: The system shall process future-salts requests. The requested count follows the protocol range 1-64; when num is 0, the implementation defaults to requesting 32 salts. The response may return at most the requested number of salts and may return fewer than requested. Revise the acceptance criterion to check that the FutureSalts response contains req_msg_id, now, and salts, and that the number of salts does not exceed the requested value or the default value of 32.

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> The protocol documentation states that the get_future_salts request count range is 1-64, that the server may return at most num salts, and that it may return fewer. In the source code, num=0 defaults to 32. The current FR-008 wording only says "multiple salts," which is too coarse.

### R006: non_verifiable

- Severity: `minor`
- Suggested action: `accept_as_issue`
- SRS location: NFR-005 / FR-007 wording
- Evidence IDs: E003

**Claim or gap**

NFR-005 states the transcoding wrapper 'shall be portable across Linux, OS X, and Windows' verified by Demonstration. This is the goffmpeg dependency's documented supported platforms (E003), not necessarily a requirement on the teamgram product, and demonstrating tri-platform portability is heavy/unverifiable in scope.

**Model opinion**

This is a property of a third-party wrapper dependency, mis-elevated to a product NFR. Scope-wise it overstates what the repository guarantees.

**Recommended human check**

Confirm whether teamgram-server itself claims tri-platform support or only the embedded goffmpeg dependency does; rescope NFR-005 accordingly.

**Model proposed SRS change**

Revise NFR-005 to: 'The embedded goffmpeg wrapper dependency documents support for Linux, OS X, and Windows [E003].' Change verification to Inspection and lower or remove as a product NFR.

Optional human revised fix:
> Delete NFR-005, or revise it as a dependency/component note: The embedded goffmpeg wrapper documentation states support for Linux, OS X, and Windows. This statement applies only to the media transcoding wrapper component and does not represent a cross-platform runtime guarantee for the entire system. Change verification to Inspection.

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> The goffmpeg README only states that the embedded FFmpeg wrapper supports Linux, OS X, and Windows. It does not imply that the whole teamgram-server product is cross-platform. The current NFR-005 overgeneralizes this dependency property.
