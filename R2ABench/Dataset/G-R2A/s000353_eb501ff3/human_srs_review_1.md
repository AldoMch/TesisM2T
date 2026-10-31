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
- Rationale: The SRS is well-structured and most requirements trace cleanly to evidence. However, several traceability and verification issues exist: E004 evidence supports middleware existence, not configurable "support" as a security control; FR-003 error response 400 is described differently in evidence; and some requirements are stated as testable but the evidence only supports existence/structural inspection. A few claims, such as Jaeger "for requests" and port configurability, are slightly overstated relative to the terse evidence.

## Overall Human Decision

- [ ] Accept
- [ ] Reject
- [x] Partial accept

Reason:
> ACCEPT=5, PARTIAL_ACCEPT=1, REJECT=1.

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

FR-003 lists `400` as a generic failure response, but evidence E006 specifies `400` means "Ensembler is used by other entity", a specific semantic, not a generic bad-request error.

**Model opinion**

The SRS generalizes the documented error codes. E006 gives precise meanings: 400 = used by other entity, 404 = not found, 500 = failed to delete. Collapsing these into "documented error responses including 400, 404, or 500" loses verifiable semantics and slightly mischaracterizes 400.

**Recommended human check**

Confirm in api/api/specs/ensemblers.yaml that 400/404/500 descriptions match the evidence and decide whether the SRS should enumerate the specific meanings.

**Model proposed SRS change**

In FR-003 Output column, replace "documented error responses including 400, 404, or 500" with "documented error responses: `400` (ensembler is used by another entity), `404` (ensembler not found), `500` (failed to delete ensembler)." Mirror this in Section 8 acceptance basis.

Optional human revised fix:
> In Section 4 FR-003 Output, revise to: "On success, return 200 and EnsemblerId JSON; on failure, return documented error responses: 400 means the ensembler is being used by another entity, 404 means the ensembler was not found, and 500 means deletion failed."
> In Section 8 FR-003 acceptance basis, revise similarly: "When the delete ensembler interface is called, success returns 200 + EnsemblerId; when the ensembler is in use, not found, or deletion fails, the system returns 400, 404, or 500 respectively with the corresponding semantics."

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> DELETE /projects/{project_id}/ensemblers/{ensembler_id} has explicit 400/404/500 semantics in the evidence. The current SRS writes them as generalized error responses and loses their verifiable meanings.

### R002: unsupported_claim

- Severity: `major`
- Suggested action: `partial_accept_as_issue`
- SRS location: NFR-001; Section 8 (NFR-001)
- Evidence IDs: E004

**Claim or gap**

NFR-001 states "The API shall support authorization and request validation middleware". E004 only lists a /turing/middleware package described as "HTTP server middlewares e.g. authorization and request validation", meaning examples of middleware, not guaranteed/required behavior.

**Model opinion**

Evidence supports that a middleware package exists with these examples, but phrasing it as a requirement ("shall support") with Security as the quality attribute overstates a directory description. The "e.g." indicates these are illustrative examples. This is verifiable only by code inspection of the package's existence, not by a security behavior test.

**Recommended human check**

Inspect /turing/middleware to confirm authorization and request validation middleware are actually implemented and wired into the HTTP server, not just example listings.

**Model proposed SRS change**

Revise NFR-001 to: "The API server shall include an HTTP middleware layer; the repository documents authorization and request validation as middleware examples." Lower confidence to Medium and keep verification as Inspection of the /turing/middleware package.

Optional human revised fix:
> In Section 5, revise NFR-001 to: "The API service shall provide an HTTP middleware layer for authorization checks and OpenAPI-spec-based request validation; the authorization middleware is mounted when authorization configuration is enabled, and the request validation middleware is mounted when OpenAPI validation configuration is enabled."
> In Section 8 NFR-001 verification, revise to: "Inspection/configuration test: when authorization configuration is enabled, unauthorized requests shall be rejected; when OpenAPI validation is enabled, requests that do not conform to the specification shall return validation errors."

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> The model is too conservative in saying E004 only supports directory existence; after checking the source, authorization middleware and OpenAPI request validation middleware are implemented and mounted in the server by configuration. However, this is not an unconditional security guarantee, because whether authorization is enabled depends on configuration.

### R003: ambiguity

- Severity: `minor`
- Suggested action: `accept_as_issue`
- SRS location: NFR-002; Section 8 (NFR-002)
- Evidence IDs: E002

**Claim or gap**

NFR-002 states the router "shall support request tracing through Jaeger client initialization for requests". E002 says "Jaeger client is initialised to trace all requests... However, the tracer's methods determine whether the app adds the trace"; initialization therefore does not guarantee tracing of every request.

**Model opinion**

The evidence explicitly qualifies that the tracer's methods decide whether traces are added. The SRS phrasing "for requests" risks implying all requests are traced. It should reflect the conditional nature.

**Recommended human check**

Verify in engines/router code whether Jaeger tracing is unconditional or conditional/sampled per the README note.

**Model proposed SRS change**

Revise NFR-002 to: "The router component shall initialize a Jaeger client for request tracing; whether a trace is added to a given request is determined by the tracer configuration/methods."

Optional human revised fix:
> In Section 5, revise NFR-002 to: "The Router component shall integrate Jaeger tracing capability; the system initializes a Jaeger client to support request tracing, but whether a specific request receives a trace is determined by the tracer's enabled state or sampling configuration."
> In Section 8 NFR-002 acceptance, revise to: "When tracing is enabled and sampling selects the request, Router requests can generate Jaeger traces; the SRS does not require all requests to unconditionally generate traces."

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> Jaeger client initialization does not mean every request necessarily writes a trace; the README explicitly says whether a trace is added is determined by the tracer enabled state.

### R004: non_verifiable

- Severity: `minor`
- Suggested action: `accept_as_issue`
- SRS location: NFR-003 / C-004; Section 8 (NFR-003)
- Evidence IDs: E002

**Claim or gap**

NFR-003 claims port 8080 is the default and that this port can be configured. E002 is fragmentary ("8080 of the user container by default. This can be configured by setting field. Refer to PR.") and does not capture the configuration field name, making the configurability claim hard to verify as written.

**Model opinion**

The default port 8080 is supported. Configurability is asserted in the evidence, but the specific configuration field is elided ("setting field"). The acceptance basis "can be configured to use another port" is testable in principle but lacks the field reference, weakening precision.

**Recommended human check**

Locate the actual values-file field used to configure the user container port in engines/router and confirm 8080 is the default.

**Model proposed SRS change**

Add a note to NFR-003/C-004 referencing the specific configuration field once identified; if not identifiable from evidence, mark the configurability claim as "documented but field unspecified in evidence pack".

Optional human revised fix:
> Revise Section 5 NFR-003 and Section 7 C-004 to: "The Router user container uses port 8080 by default; this port can be overridden through `ports.containerPort` in deployment configuration."
> Revise Section 8 NFR-003 acceptance to: "Inspect that the default deployment configuration uses 8080; after setting `ports.containerPort`, the Router user container shall use the configured port."

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> The default port 8080 and configurability can both be confirmed from the router README, and the specific configuration field is `ports.containerPort`. The current SRS lacks this verifiable anchor.

### R005: missing_requirement

- Severity: `minor`
- Suggested action: `accept_as_issue`
- SRS location: Section 4 Functional Requirements; FR list
- Evidence IDs: E005

**Claim or gap**

E005 shows a `201` response for a successfully saved ensembler (create) and a `put`/UpdateEnsembler operation, but the SRS omits create and update ensembler operations from the functional requirements.

**Model opinion**

Evidence E005 explicitly references "201: A JSON representation of a successfully saved ensembler" and "put... operationId: UpdateEn...". These create/update operations are evidenced but absent from FRs. The SRS only covers retrieve and delete, understating ensembler API scope.

**Recommended human check**

Confirm in api/api/specs/ensemblers.yaml that create (POST, 201) and update (PUT, UpdateEnsembler) operations exist and decide whether to add corresponding FRs.

**Model proposed SRS change**

Add FR-006 "Create ensembler" (POST returning 201 with Ensembler JSON, source E005) and FR-007 "Update ensembler" (PUT, operationId UpdateEnsembler, source E005), with corresponding traceability and acceptance rows.

Optional human revised fix:
> In Section 4 Functional Requirements, add two rows, preferably after FR-002 and before the delete requirement: FR-003 Create ensembler: input `project_id` and Ensembler JSON; the system shall save a user-defined ensembler; on success, it returns 201 and Ensembler JSON.
> FR-004 Update ensembler: input `project_id`, `ensembler_id`, and Ensembler JSON; the system shall update an existing ensembler; on success, it returns 200 and the updated Ensembler JSON.
> Also shift the existing delete requirement numbering, or append these as FR-006/FR-007 if avoiding renumbering. Synchronize Section 2.2, 6.2, 8, and 9 with the create/update ensembler overview, inputs/outputs, acceptance, and traceability.

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> ensemblers.yaml clearly contains create and update ensembler operations, but the current SRS only documents get and delete, so the functional scope is incomplete.

### R006: scope

- Severity: `minor`
- Suggested action: `accept_as_issue`
- SRS location: Section 3.4 / 6.1 (Timeout)
- Evidence IDs: E003

**Claim or gap**

The Timeout schema and the HTTP_JSON/UPI_V1 protocol details appear in E003, but the SRS only captures the timeout pattern and omits the protocol distinction (HTTP_JSON vs UPI_V1) that is part of router configuration semantics.

**Model opinion**

E003 text mentions "For HTTP_JSON protocol, the valid are... Whereas, for UPI_V1 protocol...". This indicates router protocol options that are part of the evidenced API but not represented. Minor since the excerpt is fragmentary, but worth a human check on completeness.

**Recommended human check**

Review routers.yaml to determine whether HTTP_JSON/UPI_V1 protocol selection is a documented router data field worth a data requirement entry.

**Model proposed SRS change**

Optionally add a Data Requirements row for router `protocol` field (`HTTP_JSON | UPI_V1`) sourced to E003 once confirmed; otherwise leave as out-of-scope with a noted rationale.

Optional human revised fix:
> In Section 3.4 or Section 6.1, add: "Router configuration shall include a protocol field with values HTTP_JSON or UPI_V1. The protocol constrains field sources in traffic-rule conditions: HTTP_JSON supports header and payload; UPI_V1 supports header and prediction_context. Field meanings shall be interpreted according to the selected field source."
> In Section 9 Traceability matrix, add this data requirement with source E003.

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> routers.yaml defines not only timeout, but also router protocol: HTTP_JSON and UPI_V1. The protocol affects legal field_source values in traffic-rule conditions. The current SRS misses this data semantic.

### R007: traceability

- Severity: `minor`
- Suggested action: `probably_ignore`
- SRS location: FR-005; Traceability matrix (FR-005)
- Evidence IDs: E004

**Claim or gap**

FR-005 is verified by Demonstration and traced to E004, which is a directory/package description ("Packages for creating, updating and deleting Turing router deployment in Kubernetes cluster"). The evidence supports existence of such packages but not a demonstrable runtime behavior without further code.

**Model opinion**

The traceability is reasonable, but the verification method Demonstration implies running deployments, whereas E004 only documents package responsibilities. Inspection may be the more honest near-term verification given the evidence pack.

**Recommended human check**

Decide whether FR-005 verification should be Inspection (of cluster packages) given current evidence, or whether deployment demonstration is feasible/in-scope.

**Model proposed SRS change**

Consider changing FR-005 verification from Demonstration to Inspection/Demonstration and note that E004 evidences package responsibilities rather than observed runtime behavior.

Optional human revised fix:
>

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> FR-005 traceability to E004 is reasonable: E004 explicitly says /turing/cluster is responsible for creating, updating, and deleting router deployments in Kubernetes. Changing the verification method from Demonstration to Inspection is mainly a rigor preference, not an SRS defect.
