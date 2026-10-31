# Human SRS Review Sheet

## Metadata

- Sample directory: `s000008_a5828142`
- Generated SRS: `final_srs.md`
- Evidence pack: `evidence_pack.json`
- Review model: `claude-opus-4-8`
- Generated at: `2026-06-05T15:34:37.360732Z`
- Raw model response: `model_srs_review_raw.md`
- Parse status: `parsed`

## Overall Model Opinion

- Recommendation: `revise`
- Confidence: `0.78`
- Rationale: The SRS is generally well-traced to the evidence pack and conservative in scope. However, several claims overstate what the evidence shows, notably FR-001's user info return given the test's buggy call, and the Redis config NFRs which are example/default config and not necessarily system-imposed requirements. The repo is named "Bunny-code" with a system architecture diagram suggesting a broader product, namely a collaborative coding editor with battles, so scope may be understated, but evidence is limited. Targeted fixes to the unsupported/overstated claims and traceability are recommended.

## Overall Human Decision

- [ ] Accept
- [ ] Reject
- [x] Partial accept

Reason:
> ACCEPT=2, PARTIAL_ACCEPT=1, REJECT=3.

## Positive Observations

- Strong, consistent traceability: every FR/NFR/DR carries explicit evidence IDs and a traceability matrix.
- Conservative scoping explicitly limits requirements to evidence-supported behaviors, with verification methods assigned per requirement.
- The JWT empty/Bearer-only rejection path (FR-002) and the statusChecked default-then-evaluate logic (FR-003) are accurately captured and well supported by E001 and E004.
- Functional, non-functional, data, and constraint requirements are clearly separated with priority and confidence annotations.

## Candidate Issues

### R001: unsupported_claim

- Severity: `major`
- Suggested action: `partial_accept_as_issue`
- SRS location: FR-001 / DR-001 / Software-API interfaces (JWT authentication)
- Evidence IDs: E001

**Claim or gap**

FR-001 states that the system validates a provided JWT token and returns the user info object. The E001 test snippet for the success case appears to call `jwtAuthenticate()` with no argument, then asserts that `authResult` deepEquals `userInfo`. The token is created but does not appear to be passed, so the evidence for "validate the provided token and return user info" is weak or possibly a buggy test.

**Model opinion**

The success-path assertion in E001 appears to call the auth function without passing the created token, which undercuts the strength of the claim that token validation returns user info. The behavior may still hold, but the cited evidence does not cleanly demonstrate token-in to userInfo-out.

**Recommended human check**

Open test/project_test.js and the jwtAuthenticate implementation to confirm whether the success test actually passes the token and whether userInfo is returned on valid input.

**Model proposed SRS change**

FR-001: Soften to "The system shall provide a JWT authentication function that, on valid token input, resolves to an authenticated user information object containing id, name, and email. (Note: success-path test E001 invokes the function without passing the token; confirm implementation behavior.)" Mark verification confidence as Medium until implementation is confirmed.

Optional human revised fix:
>

**Human decision**

- [ ] Accept
- [ ] Reject
- [x] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> The model's judgment comes from truncated evidence. In the complete test/project_test.js, the success case actually calls jwtAuthenticate with a Bearer token argument, not with no argument; server/services/auth.js also parses the JWT from the Bearer token and returns decoded.payload.

### R002: unsupported_claim

- Severity: `major`
- Suggested action: `accept_as_issue`
- SRS location: NFR-002, NFR-003, NFR-004, DR-007, C-003 (Redis configuration requirements)
- Evidence IDs: E005, E006, E003

**Claim or gap**

NFR-002/003/004 and related items treat Redis example config defaults (`rdbchecksum yes`, sanitization checks, ACL auth) as system requirements. The evidence (E003/E005/E006) is from `redis_example.conf`, which is a stock/example Redis configuration file with commented-out documentation, not necessarily a deliberate requirement imposed by this system.

**Model opinion**

These are Redis stock-config documentation comments and defaults. Elevating them to "shall" non-functional requirements of the product overstates intent. `rdbchecksum yes` is a Redis default; ACL/sanitization text in the evidence is mostly commented documentation. They should be framed as deployment-config observations, not as binding system requirements, unless the actual config file enforces them.

**Recommended human check**

Inspect Docker/Cache/redis_example.conf to determine which directives are actually set (uncommented) versus default documentation, and whether the file is an example template or the deployed config.

**Model proposed SRS change**

Reword NFR-002/003/004 from "shall" requirements to "The provided Redis example configuration enables/documents X" observations, or move them to a Deployment Configuration note. Lower confidence to "derived/example" and update DR-007 and C-003 to state these are example-config-derived rather than mandated.

Optional human revised fix:
> In Section 5, delete or downgrade NFR-002, NFR-003, and NFR-004. Replace them with a deployment configuration note: "The Redis example configuration provided by the repository includes settings for persistence, RDB checksum, AOF, protected mode, and default user password. These settings show that Redis deployment can use authentication and persistence protection, but unless the final deployment uses this configuration, they should not be treated as mandatory product-level non-functional requirements."
> In DR-007, revise to: "Redis configuration data: the repository example configuration records cache persistence and access-authentication related settings; the SRS only requires the cache layer to support project collaboration and battle flows, and does not mandate specific Redis default items."
> In C-003, revise to: "Redis connectivity depends on environment variables for host, port, username, and password; the repository example configuration provides an ACL/password configuration reference, and final constraints depend on the actual deployment configuration."

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> Docker/Cache/redis_example.conf is an example configuration, and the Dockerfile copies redis.conf, which is not present in the current commit. rdbchecksum yes, appendonly yes, and user default on >TestPassword can be treated as example configuration facts; sanitize-dump-payload is only commented documentation and cannot be written as a system requirement.

### R003: scope

- Severity: `major`
- Suggested action: `partial_accept_as_issue`
- SRS location: Section 1 Product scope / Section 2 Overall Description
- Evidence IDs: E002, E004

**Claim or gap**

The repository name "Bunny-code" and the ground-truth System_architecture.png, plus models like editor_model and battle_controller, suggest a collaborative coding/editor product with a battle/competition feature and a real-time editor. The SRS narrows scope to JWT auth, socket authorization, battle acceptance, and Redis, potentially understating the overall product.

**Model opinion**

The evidence pack is intentionally narrow (six chunks), so the SRS conservatism is defensible. But the architecture diagram and component names imply a larger system: a real-time collaborative code editor plus battle game. The SRS should at least acknowledge that the evidenced requirements are a subset of a larger product to avoid understating scope.

**Recommended human check**

Review System_architecture.png and the repo README to determine the full product scope (collaborative editor, battles, user system) and whether the SRS scope statement should be expanded or explicitly marked as partial.

**Model proposed SRS change**

Add to Section 1 Product scope: "This SRS covers only the subset of behaviors supported by the provided evidence pack; the repository (Bunny-code) appears to implement a broader real-time collaborative coding editor with a battle feature per the system architecture diagram, which is out of scope for this evidence-bound document."

Optional human revised fix:
> In Section 1 Product scope, replace with: "Bunny Code is a collaborative coding website for learning and practice. The system supports user registration/login, project creation and version management, code editing and execution, coding-process recording and playback, real-time battles, battle problem and result management, and upload/distribution of code files and archives. The system is supported by a Vue frontend, Node.js/Express backend, REST APIs, Socket.IO real-time channels, MySQL, InfluxDB, Redis, Docker code sandbox, S3/CloudFront static and archive storage, Nginx reverse proxy, and automated deployment flow."
> In Section 2 Product perspective, add: "The frontend interacts with the backend through API request/response and Socket connection; the backend is responsible for users, projects, versions, compilation, recording, battles, and file archives; MySQL stores relational data such as users, projects, versions, problems, and battles; InfluxDB stores time-series records of coding processes; Redis supports real-time collaboration and battle state; the Docker sandbox executes user code; S3/CloudFront provide code archives and static-resource distribution."
> In Section 4, add functional requirements:
> The system shall support user registration, login, JWT authentication, and user detail query.
> The system shall support users creating, querying, and updating projects, and creating versions and initial files for projects.
> The system shall support submitting code for compilation/execution and returning execution results.
> The system shall record user coding processes and support querying playback records by project, version, and time range.
> The system shall support workspace editing state, editing occupation, leaving workspace, and disconnect cleanup through socket.
> The system shall support real-time battle invitation, acceptance, readiness, code synchronization, compile-and-judge, win/loss ending, and leave handling.
> The system shall support uploading code files, battle result files, and user-related files to object storage and returning distributable URLs.

**Human decision**

- [ ] Accept
- [ ] Reject
- [x] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> The README and architecture diagram clearly show that Bunny Code is not merely a JWT/socket/Redis backend, but a collaborative coding website: code editing, execution, version control, coding-process recording and playback, real-time battles, static archives, sandbox execution, frontend/backend separation, and deployment flow all have evidence.

### R004: ambiguity

- Severity: `minor`
- Suggested action: `accept_as_issue`
- SRS location: FR-005 / FR-006 / E002
- Evidence IDs: E002

**Claim or gap**

FR-005 describes isolated cache access and FR-006 a battleFailed SocketException, but the E002 snippet shows function calls with empty argument lists, for example `isolatedClient.watch()`, `HGETALL()`, and `HDEL( , )`, so the exact keys/arguments and the battle object structure are not observable from evidence.

**Model opinion**

The general flow (executeIsolated -> watch -> HGETALL -> HDEL, catch -> SocketException "battleFailed") is supported. But specifics like which cache keys are watched/read/deleted and the battle object shape are not evidenced; DR-006 implies a structured battle object that is not shown.

**Recommended human check**

Read socket/controllers/battle_controller.js fully to confirm the watched key, HGETALL key, HDEL fields, and the battle object structure.

**Model proposed SRS change**

FR-005/DR-006: Add a note that exact cache keys and battle object fields are not specified in the evidence and should be confirmed against battle_controller.js; avoid implying a known battle object schema.

Optional human revised fix:
> Near the existing FR-005/FR-006, revise to:
> "The system shall support authenticated users creating battle invitations. An invitation shall include the inviter socket identifier, battle name, battle difficulty, inviter user ID, and inviter username; the system shall limit repeated invitations within a short period and delete the temporary invitation after timeout.
> When a user accepts a battle invitation, the system shall read the temporary invitation from cache and delete the corresponding entry to prevent the same invitation from being accepted repeatedly; if the invitation exists and the acceptor is not the inviter, the system shall create a battle record, initialize both users' battle state, and send battle-created-success events to both users.
> If the invitation has expired, the inviter and acceptor are the same user, cache read fails, or battle creation fails, the system shall return a battle-failed event."
> In DR-006, revise to:
> "Battle cache data includes temporary invitation objects and formal battle state objects. A temporary invitation object contains at least invitation socket, battle name, difficulty, inviter user ID, and inviter username; formal battle state stores readiness state, code content, remaining chances by participating user, and problem answer data."

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> The complete battle_controller.js confirms the details: the invitation object contains socketID, battleName, battleLevel, firstUserID, and firstUserName; the temporary invitation uses the inviter socket as the cache key and the inviter user ID as the hash field; accepting reads and then deletes it; after success, the system creates the battle and writes ready/codes/chance state for both users.

### R005: traceability

- Severity: `minor`
- Suggested action: `probably_ignore`
- SRS location: Operating environment / C-001 (Node.js / CommonJS inference)
- Evidence IDs: E001, E002, E004

**Claim or gap**

Node.js runtime is inferred from `require(...)` usage. This is an inference, not explicit evidence, yet C-001 and the operating environment present it with high certainty.

**Model opinion**

The inference is reasonable (CommonJS require, .js test/controller files) but should be marked as inferred rather than explicit to keep traceability honest.

**Recommended human check**

Confirm package.json / engines field or server entry point to verify Node.js runtime explicitly.

**Model proposed SRS change**

Annotate C-001 and Operating environment as inferred confidence rather than implying explicit evidence; reference package.json if available for explicit confirmation.

Optional human revised fix:
>

**Human decision**

- [ ] Accept
- [x] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> This is not a weak inference. package.json clearly shows a Node project and declares Express, Socket.IO, Redis, MySQL, InfluxDB, AWS SDK, and other dependencies; app.js and socket.js also clearly indicate an Express + Socket.IO server.

### R006: non_verifiable

- Severity: `minor`
- Suggested action: `probably_ignore`
- SRS location: NFR-001 / NFR-005 (race condition mitigation, readiness)
- Evidence IDs: E002, E004

**Claim or gap**

NFR-001 ("mitigate race conditions") and NFR-005 ("verify cache readiness before execution") are verified only by Inspection. "Mitigate race conditions" is not stated as a measurable/observable acceptance criterion beyond the presence of isolated execution code.

**Model opinion**

These are acceptable as inspection-based requirements, but "mitigate race conditions" is inherently hard to verify as a quality outcome. Tying the acceptance basis strictly to the presence of executeIsolated/watch and checkCacheReady calls, as the SRS mostly does, keeps it verifiable.

**Recommended human check**

Confirm the acceptance basis for NFR-001 is the presence of isolated/watch semantics rather than an unmeasurable "no race conditions" guarantee.

**Model proposed SRS change**

NFR-001: Restate as "The system shall implement battle acceptance using Redis isolated execution with WATCH semantics" (observable code structure) rather than asserting the abstract outcome of race-condition mitigation.

Optional human revised fix:
> In NFR-001, revise to: "The battle invitation acceptance flow shall use isolated execution and watched cache state to control concurrent access, so that the same temporary invitation can be consumed by at most one acceptance flow under concurrent acceptance." In the acceptance criteria, revise to: "Confirm through source inspection or a concurrent acceptance test that the system deletes the corresponding cache entry after reading the temporary invitation and prevents the same invitation from being successfully accepted repeatedly."

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> The current NFR-001/NFR-005 already use source inspection as the acceptance method and are basically acceptable. However, "mitigate race conditions" could be made more verifiable.
