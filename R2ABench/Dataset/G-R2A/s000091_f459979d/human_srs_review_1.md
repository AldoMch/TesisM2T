# Human SRS Review Sheet

## Metadata

- Sample directory: `s000091_f459979d`
- Generated SRS: `final_srs.md`
- Evidence pack: `evidence_pack.json`
- Review model: `claude-opus-4-8`
- Generated at: `2026-06-05T16:06:34.695322Z`
- Raw model response: `model_srs_review_raw.md`
- Parse status: `parsed`

## Overall Model Opinion

- Recommendation: `revise`
- Confidence: `0.72`
- Rationale: The SRS is well-grounded in the evidence chunks and maps requirements to code faithfully. However, several requirements overstate specificity not visible in the truncated evidence, including HTTP status codes for the retrieval endpoint and the POST /add 201 path, and the broader system context, namely the blockchain LwM2M bootstrap architecture shown by the architecture diagram, is understated. A few traceability and verifiability concerns require human adjudication.

## Overall Human Decision

- [ ] Accept
- [ ] Reject
- [x] Partial accept

Reason:
> ACCEPT=2, PARTIAL_ACCEPT=4, REJECT=0.

## Positive Observations

- The JWT validation-result mapping (0->200, 1->401, 2->403, else 400) in FR-001/FR-002 is accurately and precisely traced to E002.
- NFR-003 and DR-004 correctly capture the LwM2M deserializer's invariants directly from E005/E006, including JsonParseException for an invalid node element and "Missing id" when instances exist without id.
- Web3j HttpService connectivity (NFR-002, C-002) is faithfully grounded in E001.
- The traceability matrix consistently assigns confidence levels that reasonably reflect evidence strength: Medium for blockchain/test-derived items and High for directly shown code behaviors.

## Candidate Issues

### R001: unsupported_claim

- Severity: `minor`
- Suggested action: `partial_accept_as_issue`
- SRS location: FR-001 / Section 3 Software/API interfaces (User HTTP API row)
- Evidence IDs: E002

**Claim or gap**

FR-001 describes an authenticated user-retrieval operation with specific HTTP routing, but E002 only shows the trailing portion of a handler (`Service.getAll()` returning `HttpStatus.OK`) without the method mapping, route path, or `@GetMapping` annotation for retrieval.

**Model opinion**

The validation-result-to-status mapping (0->OK, 1->401, 2->403, else 400) is well supported for both handlers. However, the route/HTTP method of the retrieval operation is not shown in E002; only the add endpoint's `/add` mapping is visible. The SRS does not assert a specific retrieval route, so this is low risk, but the claim that it is a distinct retrieval endpoint should be confirmed.

**Recommended human check**

Open UserController.java and confirm the retrieval handler's HTTP method and path, for example `@GetMapping`. Verify that it is driven by `getAll()` and returns the user list.

**Model proposed SRS change**

FR-001 Trigger/Input: replace "HTTP request with `Authorization` header to the user retrieval endpoint" with "HTTP GET request with `Authorization` header to the user-retrieval endpoint (exact route to be confirmed against UserController mapping)".

Optional human revised fix:
> In the FR-001 Trigger/Input, change "HTTP request with Authorization header to the user retrieval endpoint" to "HTTP GET request with Authorization header to the user retrieval endpoint; the system returns the user list or the corresponding error status according to the token validation result." In the Section 3 User HTTP API row, also add: "The User API shall support user retrieval and user creation operations, both access-controlled based on the Authorization header."

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> Partial accept. The reason is that the model says E002 does not show the HTTP method for the user retrieval endpoint, but the source code has confirmed that user retrieval is GET. Therefore, the issue is not that the claim is unsupported; rather, the SRS can make the trigger condition more explicit.

### R002: non_verifiable

- Severity: `minor`
- Suggested action: `partial_accept_as_issue`
- SRS location: FR-003 / Section 8 Verification (FR-003 row)
- Evidence IDs: E001

**Claim or gap**

FR-003 acceptance criterion "A retrieval request results in contract getAllClients().send() usage" tests an internal implementation call rather than observable behavior, and E001 shows that the catch block swallows exceptions (`e.printStackTrace`) and may return an empty list.

**Model opinion**

Asserting that a specific internal contract method is invoked is white-box and brittle as an acceptance criterion. More importantly, E001 reveals error handling that returns an empty or partial collection on exception, which is unspecified in the SRS. A missing requirement on error behavior may be warranted.

**Recommended human check**

Review ClientStoreService.getAll(): confirm that on contract failure it returns an empty collection rather than propagating an error, and decide whether this error-handling behavior should be a requirement.

**Model proposed SRS change**

Add FR-003a: "If the blockchain contract call fails, the system shall return an empty security-information collection (current behavior logs the exception and does not propagate it). [E001]" and reword FR-003 acceptance to observable output, namely returned collection content, rather than internal method usage.

Optional human revised fix:
> In the FR-003 behavior or acceptance criterion, change the internal-call description to a result-oriented description: "The system shall retrieve client security information from the blockchain contract and convert the result into a returned security-information collection; when the contract call fails, the system records the exception according to the current implementation and returns an empty collection without propagating the exception to the caller." In Section 8, revise the FR-003 acceptance criterion to: "On success, the converted security-information collection is returned; when contract access fails, an empty collection is returned and the caller flow is not interrupted."

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> The reason is that the current FR-003 acceptance criterion is too white-box: it emphasizes an internal contract call instead of externally observable behavior. The source code also shows that when the contract call throws an exception, the system records the exception and returns an empty collection.

### R003: missing_requirement

- Severity: `minor`
- Suggested action: `accept_as_issue`
- SRS location: Section 3 / FR-004 / FR-005 - Converter byte32 transformation
- Evidence IDs: E004

**Claim or gap**

E004 shows string fields are converted via `Converter.asciiToByte32(...)` and responses via `Converter.byteToAscii(...)`. The SRS mentions byte-array representations generically in FR-004 but omits the explicit ASCII <-> byte32 conversion constraint used for both addClient and getClient.

**Model opinion**

The asciiToByte32/byteToAscii conversion is a concrete and testable data-format constraint visible in E004 and relevant to interoperability with the smart contract. It is partially captured for FR-004 but not for FR-005 retrieval decoding.

**Recommended human check**

Confirm Converter.asciiToByte32 / byteToAscii usage in both addClient and getClient paths, and confirm whether fixed 32-byte encoding is a hard contract constraint.

**Model proposed SRS change**

Augment DR-002 and FR-005: add "String fields exchanged with the contract shall be encoded as fixed 32-byte (byte32) ASCII values on submission and decoded from byte32 to ASCII on retrieval. [E004]".

Optional human revised fix:
> In DR-002, add: "String fields exchanged with the smart contract, such as endpoint, bootstrap/server URL, identity, and key, shall be encoded as fixed 32-byte ASCII values on submission and decoded back from fixed 32-byte values to ASCII strings on retrieval." In FR-004, add: "Before submitting client bootstrap data, the system shall convert the relevant string fields into fixed 32-byte ASCII representation." In FR-005, add: "When retrieving client bootstrap configuration, the system shall submit the endpoint in fixed 32-byte form and decode returned fields as ASCII before constructing the bootstrap configuration."

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> Accept. The reason is that the evidence shows a clear ASCII <-> byte32 fixed-length conversion constraint for string fields in blockchain interaction. The current SRS only states byte-array representation in general terms, which is not precise enough.

### R004: scope

- Severity: `major`
- Suggested action: `partial_accept_as_issue`
- SRS location: Section 1 Product scope / Section 2 Overall Description
- Evidence IDs: E001, E003

**Claim or gap**

The SRS scope reduces the project to user-management endpoints, blockchain client/bootstrap store, and LwM2M JSON parsing, but the repository name, architecture.png, README, deployment/config docs, and multiple modules such as mainApp, Leshan Server, and evaluation/tests describe a broader LwM2M-over-blockchain bootstrap system with a deployment architecture.

**Model opinion**

The evidence pack covered deployment and user_scenario categories, with category_hits showing deployment:58 and user_scenario:78, and document types include readme/config/cli, indicating a system-level architecture not reflected in the SRS scope. The SRS understates scope by focusing only on the five retrieved code chunks. An architecture-level scope statement should be added or the limitation explicitly noted.

**Recommended human check**

Review the README and architecture.png plus configuration/deployment documentation to determine the overall system purpose, namely LwM2M device bootstrap secured via a blockchain BootstrapStore contract, and whether the SRS should state this end-to-end scope.

**Model proposed SRS change**

Section 1 Product scope: add "The overall system provides LwM2M device bootstrap/security provisioning backed by an Ethereum smart contract (BootstrapStore), integrating a Leshan-based LwM2M server with a Spring backend and Web3j blockchain access. This SRS focuses on the evidenced backend components; the full deployment architecture (see architecture.png) should be cross-checked." (pending README/diagram confirmation).

Optional human revised fix:
> In Section 1 Product scope or Section 2 Product perspective, add a high-level scope statement: "This system targets LwM2M device-management scenarios and combines LwM2M services, device bootstrap/security-information management, management-side access control, and blockchain trusted storage to improve the reliability and auditability of client bootstrap information and key access-control information. The SRS covers user access control, blockchain read/write of client/bootstrap information, LwM2M data parsing, and related backend service behavior."

**Human decision**

- [ ] Accept
- [ ] Reject
- [x] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> Partial accept. The reason is that the README and architecture diagram show the system scope is not limited to user management, blockchain storage, and JSON parsing; it also includes the LwM2M server, bootstrap server, secure API, management web UI, blockchain network, and their overall relationships. However, the architecture diagram should not be translated item by item into the SRS, because that would turn into answer leakage.

### R005: traceability

- Severity: `minor`
- Suggested action: `partial_accept_as_issue`
- SRS location: C-003 / FR-005 / FR-003 evidence assignments
- Evidence IDs: E001, E003, E004

**Claim or gap**

FR-005 (getClient -> BootstrapConfig) cites E004, a test file named ClientTest.java, as an explicit source, while the production implementation appears under ClientService (E003) and ClientStoreService (E001). The contract name `BootstrapStore` is from E003, but the shown getClient/addClient code is from the test (E004).

**Model opinion**

Deriving functional requirements primarily from a test file is acceptable as supporting evidence but weak as the authoritative source. The production getClient/addClient logic may differ from the test harness. Traceability confidence labeled Medium is reasonable, but evidence should ideally point to production service code.

**Recommended human check**

Confirm whether addClient/getClient as specified in FR-004/FR-005 reflect production ClientService/ClientStoreService code, not only ClientTest.java, and add the production-code evidence reference.

**Model proposed SRS change**

FR-004/FR-005 Source evidence: add production-code evidence reference (ClientService/ClientStoreService) alongside E004, or annotate that E004 is a test-derived source pending production-code confirmation.

Optional human revised fix:
> In the Section 9 traceability matrix, adjust evidence assignments: for FR-004, cite production service evidence and test evidence, such as E003 and E004. For FR-005, keep E004 and add Leshan/bootstrap-side production implementation evidence, such as E001. If the matrix has a note column, state: "E004 is test-derived evidence used to confirm contract field conversion and call shape; the production path is jointly supported by backend service and Leshan/bootstrap store implementation evidence."

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> Partial accept. The reason is that the new-client data path in FR-004 has production-code support, but the evidence for FR-005 getClient/bootstrap configuration retrieval comes more from tests and Leshan-side implementation. The SRS needs to distinguish production evidence and test evidence more clearly.

### R006: ambiguity

- Severity: `minor`
- Suggested action: `accept_as_issue`
- SRS location: DR-005 / NFR-003 / E005 floating-point typing
- Evidence IDs: E005

**Claim or gap**

DR-005 lists floating-point type generically. E005 shows the logic: a number maps to INTEGER when `getAsDouble()==getAsLong()`, otherwise to a truncated, unshown FLOAT/DOUBLE type. The exact non-integer type name and the integer-vs-float discrimination rule are underspecified in the SRS.

**Model opinion**

The discrimination rule, integer if double equals long and floating otherwise, is concrete and testable in E005 and should be stated to make DR-005 verifiable rather than using loose "floating-point type" wording.

**Recommended human check**

Read the full getTypeFor method in LwM2mNodeDeserializer.java to confirm the exact non-integer return type and the equality rule.

**Model proposed SRS change**

DR-005: replace mapping description with "BOOLEAN for boolean values, STRING for string values, INTEGER when the numeric value satisfies getAsDouble()==getAsLong(), and a floating-point resource type (FLOAT/DOUBLE - confirm exact type) otherwise. [E005]".

Optional human revised fix:
> In DR-005, revise the type mapping rule to: "JSON primitive values are mapped as follows: boolean maps to BOOLEAN; string maps to STRING; number maps to INTEGER if its double value can be losslessly represented as a long value; other numbers map to FLOAT; primitive value types not otherwise covered are handled as STRING by default."

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> Accept. The reason is that the LwM2M JSON numeric type mapping rule is clear in the source code: boolean, string, integer-like number, and non-integer number are mapped separately. The SRS should not simply write "floating-point type" in a generic way.
