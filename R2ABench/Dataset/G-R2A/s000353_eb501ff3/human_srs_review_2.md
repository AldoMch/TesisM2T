# Human SRS Review Sheet

## Metadata

- Sample directory: `s000353_eb501ff3`
- Generated SRS: `final_srs.md`
- Evidence pack: `evidence_pack.json`
- Review model: `claude-opus-4-8`
- Generated at: `2026-06-05T16:11:41.547226Z`
- Raw model response: `model_srs_review_raw.md`
- Parse status: `parsed`

## Overall Model Opinion

- Recommendation: `revise`
- Confidence: `0.78`
- Rationale: The SRS is well-structured and most requirements trace cleanly to evidence. However, several traceability and verification issues exist: E004 evidence supports middleware existence (not configurable 'support' as a security control), FR-003 error response 400 is described differently in evidence, and some requirements are stated as testable but the evidence only supports existence/structural inspection. A few claims (Jaeger 'for requests', port configurability) are slightly overstated relative to the terse evidence.

## Overall Human Decision

- [ ] Accept
- [ ] Reject
- [ ] Partial accept

Reason:
> 

## Positive Observations

- Functional requirements FR-001 through FR-003 are precisely traced to OpenAPI evidence (E003, E005, E006) with correct paths, methods, and response content types.
- The SRS appropriately scopes out unsupported areas (Section 6.3 explicitly notes absence of retention/privacy/migration evidence) rather than inventing requirements.
- Evidence IDs are consistently attached to each requirement and the traceability matrix includes confidence levels, supporting auditability.
- OpenAPI 3.0.3 conformance (NFR-004) and the timeout pattern constraint are accurately captured directly from E003.

## Candidate Issues

### R001: contradiction

- Severity: `minor`
- Suggested action: `accept_as_issue`
- SRS location: FR-003; Section 8 (FR-003 acceptance); Data Requirements 6.1 (EnsemblerId)
- Evidence IDs: E006

**Claim or gap**

FR-003 lists `400` as a generic failure response, but evidence E006 specifies `400` means 'Ensembler is used by other entity' (a specific semantic), not a generic bad-request error.

**Model opinion**

The SRS generalizes the documented error codes. E006 gives precise meanings: 400 = used by other entity, 404 = not found, 500 = failed to delete. Collapsing these into 'documented error responses including 400, 404, or 500' loses verifiable semantics and slightly mischaracterizes 400.

**Recommended human check**

Confirm in api/api/specs/ensemblers.yaml that 400/404/500 descriptions match the evidence and decide whether SRS should enumerate the specific meanings.

**Model proposed SRS change**

In FR-003 Output column, replace 'documented error responses including 400, 404, or 500' with 'documented error responses: `400` (ensembler is used by another entity), `404` (ensembler not found), `500` (failed to delete ensembler)'. Mirror this in Section 8 acceptance basis.

Optional human revised fix:
> 

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> issue成立，E006 对错误码语义有明确描述，应该写明，建议采纳。

### R002: unsupported_claim

- Severity: `major`
- Suggested action: `needs_human_check`
- SRS location: NFR-001; Section 8 (NFR-001)
- Evidence IDs: E004

**Claim or gap**

NFR-001 states 'The API shall support authorization and request validation middleware'. E004 only lists a /turing/middleware package described as 'HTTP server middlewares e.g. authorization and request validation' — i.e., examples of middleware, not a guaranteed/required behavior.

**Model opinion**

Evidence supports that a middleware package exists with these examples, but phrasing it as a requirement ('shall support') with Security as the quality attribute overstates a directory description. The 'e.g.' indicates these are illustrative examples. This is verifiable only by code inspection of the package's existence, not by a security behavior test.

**Recommended human check**

Inspect /turing/middleware to confirm authorization and request validation middleware are actually implemented and wired into the HTTP server, not just example listings.

**Model proposed SRS change**

Revise NFR-001 to: 'The API server shall include an HTTP middleware layer; the repository documents authorization and request validation as middleware examples.' Lower confidence to Medium and keep verification as Inspection of the /turing/middleware package.

Optional human revised fix:
> 

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> Issue 成立。E004 是目录职责说明，不能直接证明运行时授权/校验行为。建议采纳。

### R003: ambiguity

- Severity: `minor`
- Suggested action: `accept_as_issue`
- SRS location: NFR-002; Section 8 (NFR-002)
- Evidence IDs: E002

**Claim or gap**

NFR-002 states the router 'shall support request tracing through Jaeger client initialization for requests'. E002 says 'Jaeger client is initialised to trace all requests... However, the tracer's methods determine whether the app adds the trace' — i.e., initialization does not guarantee tracing of every request.

**Model opinion**

The evidence explicitly qualifies that the tracer's methods decide whether traces are added. The SRS phrasing 'for requests' risks implying all requests are traced. Should reflect the conditional nature.

**Recommended human check**

Verify in engines/router code whether Jaeger tracing is unconditional or conditional/sampled per the README note.

**Model proposed SRS change**

Revise NFR-002 to: 'The router component shall initialize a Jaeger client for request tracing; whether a trace is added to a given request is determined by the tracer configuration/methods.'

Optional human revised fix:
> 

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> issue成立，建议采纳。

### R004: non_verifiable

- Severity: `minor`
- Suggested action: `needs_human_check`
- SRS location: NFR-003 / C-004; Section 8 (NFR-003)
- Evidence IDs: E002

**Claim or gap**

NFR-003 claims port 8080 default 'and allow this port to be configured'. E002 is fragmentary ('8080 of the user container by default. This can be configured by setting field. Refer to PR.') — the configuration field name is not captured, making the configurability claim hard to verify as written.

**Model opinion**

The default port 8080 is supported. Configurability is asserted in the evidence but the specific configuration field is elided ('setting field'). The acceptance basis 'can be configured to use another port' is testable in principle but lacks the field reference, weakening precision.

**Recommended human check**

Locate the actual values-file field used to configure the user container port in engines/router and confirm 8080 is the default.

**Model proposed SRS change**

Add a note to NFR-003/C-004 referencing the specific configuration field once identified; if not identifiable from evidence, mark configurability claim as 'documented but field unspecified in evidence pack'.

Optional human revised fix:
> 

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> issue成立，建议采纳模型修改建议。

### R005: missing_requirement

- Severity: `minor`
- Suggested action: `accept_as_issue`
- SRS location: Section 4 Functional Requirements; FR list
- Evidence IDs: E005

**Claim or gap**

E005 shows a `201` response for a successfully saved ensembler (create) and a `put`/UpdateEnsembler operation, but the SRS omits create and update ensembler operations from the functional requirements.

**Model opinion**

Evidence E005 explicitly references '201: A JSON representation of a successfully saved ensembler' and 'put... operationId: UpdateEn...'. These create/update operations are evidenced but absent from FRs. The SRS only covers retrieve and delete, understating ensembler API scope.

**Recommended human check**

Confirm in api/api/specs/ensemblers.yaml that create (POST, 201) and update (PUT, UpdateEnsembler) operations exist and decide whether to add corresponding FRs.

**Model proposed SRS change**

Add FR-006 'Create ensembler' (POST returning 201 with Ensembler JSON, source E005) and FR-007 'Update ensembler' (PUT, operationId UpdateEnsembler, source E005), with corresponding traceability and acceptance rows.

Optional human revised fix:
> 

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> Issue 成立。E005 直接显示了 create/update 相关内容。

### R006: scope

- Severity: `minor`
- Suggested action: `needs_human_check`
- SRS location: Section 3.4 / 6.1 (Timeout)
- Evidence IDs: E003

**Claim or gap**

The Timeout schema and the HTTP_JSON/UPI_V1 protocol details appear in E003 but the SRS only captures the timeout pattern and omits the protocol distinction (HTTP_JSON vs UPI_V1) that is part of router configuration semantics.

**Model opinion**

E003 text mentions 'For HTTP_JSON protocol, the valid are... Whereas, for UPI_V1 protocol...'. This indicates router protocol options that are part of the evidenced API but not represented. Minor since the excerpt is fragmentary, but worth a human check on completeness.

**Recommended human check**

Review routers.yaml to determine whether HTTP_JSON/UPI_V1 protocol selection is a documented router data field worth a data requirement entry.

**Model proposed SRS change**

Optionally add a Data Requirements row for router 'protocol' field (HTTP_JSON | UPI_V1) sourced to E003 once confirmed; otherwise leave as out-of-scope with a noted rationale.

Optional human revised fix:
> 建议采纳，先增加待确认说明：“protocol-specific router configuration semantics are visible in E003 (`HTTP_JSON` vs `UPI_V1`) but the excerpt is fragmentary; confirm the exact `protocol` field in `routers.yaml` before adding a precise data requirement.” 

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> Issue 成立。E003 片段足以说明 protocol distinction 存在，但精确定义需完整 spec。

### R007: traceability

- Severity: `minor`
- Suggested action: `probably_ignore`
- SRS location: FR-005; Traceability matrix (FR-005)
- Evidence IDs: E004

**Claim or gap**

FR-005 is verified by 'Demonstration' and traced to E004, which is a directory/package description ('Packages for creating, updating and deleting Turing router deployment in Kubernetes cluster'). The evidence supports existence of such packages but not a demonstrable runtime behavior without further code.

**Model opinion**

The traceability is reasonable but the verification method 'Demonstration' implies running deployments, whereas E004 only documents package responsibilities. Inspection may be the more honest near-term verification given the evidence pack.

**Recommended human check**

Decide whether FR-005 verification should be 'Inspection' (of cluster packages) given current evidence, or whether deployment demonstration is feasible/in-scope.

**Model proposed SRS change**

Consider changing FR-005 verification from 'Demonstration' to 'Inspection/Demonstration' and note that E004 evidences package responsibilities rather than observed runtime behavior.

Optional human revised fix:
> 

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
>Issue 成立。当前证据不足以单独支撑 Demonstration。建议直接采纳
