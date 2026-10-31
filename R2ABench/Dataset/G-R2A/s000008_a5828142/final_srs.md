# Software Requirements Specification

## 1. Introduction

### Purpose
This SRS defines evidence-backed requirements for the repository component set represented in commit `931e3b780b390e26f32259cbfda3a7b5b565a59e` of `domingo1021/Bunny-code`. The scope is limited to behaviors directly supported by the provided evidence pack, primarily JWT authentication, socket-based project authorization/status reporting, battle acceptance handling, and Redis-backed runtime dependencies.

### Product scope
The evidenced product scope is a Node.js-based backend/service layer that:
- validates JWT bearer tokens and returns authenticated user information,
- authorizes socket clients for project workspace access and reports access state,
- accepts battle invitations through socket workflows with cache-backed race-condition handling,
- depends on Redis cache/configuration for runtime coordination and persistence-related settings.

### Intended audience
This document is intended for maintainers, testers, integrators, and reviewers who need a concise, traceable statement of repository-supported requirements.

### References
- Repository: `domingo1021/Bunny-code`
- Commit: `931e3b780b390e26f32259cbfda3a7b5b565a59e`
- Evidence sources: `E001` to `E006`

## 2. Overall Description

### Product perspective
The repository evidence indicates a backend service with socket controllers and utility-backed authentication/cache integration. Redis is used as a cache/runtime coordination dependency, and socket events are used to communicate authorization and battle workflow outcomes. Source evidence: `E002`, `E004`, `E003`, `E005`, `E006`.

### Product functions summary
- Validate JWT tokens and return user identity data on success. `E001`
- Reject missing or malformed JWT token input with an API exception. `E001`
- Check project authorization based on `projectID` and `versionID`, then emit access status to the socket client. `E004`
- Mark unauthorized or incomplete project requests as read-only and unauthorized in the status response. `E004`
- Accept battle invitations using isolated cache access to reduce race conditions and handle invitation timeout/failure. `E002`

### User classes
- Authenticated application users whose identity is represented by JWT claims containing at least `id`, `name`, and `email`. `E001`
- Socket clients connecting to workspace/project features. `E004`
- Socket clients participating in battle invitation acceptance flows. `E002`

### Operating environment
- Node.js server-side runtime is inferred from CommonJS `require(...)` usage and JavaScript test/controller files. `E001`, `E002`, `E004`
- Redis cache/service is a required runtime dependency for cache-backed operations and configuration. `E002`, `E004`, `E003`, `E005`, `E006`

### Assumptions and dependencies
- Cache-backed battle acceptance requires the cache service to be ready before operation. `E002`
- Non-read-only project access may write a socket-to-version mapping into cache when cache is ready. `E004`
- Redis deployments may use ACL-based authentication and RDB checksum/sanitization settings as configured in the provided Redis example configuration. `E005`, `E006`

## 3. External Interface Requirements

### User interfaces
No direct end-user graphical interface is evidenced.

### Software/API interfaces
| Interface | Requirement | Source |
|---|---|---|
| JWT authentication function | The system shall accept a JWT bearer token input and either return user identity information or raise an API exception for invalid input. | `E001` |
| Socket event `statusChecked` | The system shall emit a `statusChecked` event containing project authorization and read-only status after project access evaluation. | `E004` |
| Battle acceptance socket flow | The system shall process battle acceptance requests using `socketID` and `firstUserID` inputs. | `E002` |
| Redis cache interface | The system shall use Redis hash/cache operations and isolated execution for battle acceptance and project workspace coordination. | `E002`, `E004` |

### Communication interfaces
| Interface | Description | Source |
|---|---|---|
| Socket-based server push | Server responses include socket emits such as `statusChecked`. | `E004` |
| Redis client/server communication | Cache access uses Redis commands including isolated execution, `WATCH`, `HGETALL`, and `HDEL`. | `E002` |

### Data exchange formats
| Format | Description | Source |
|---|---|---|
| JWT token string | Authentication input token, including bearer-token scenarios. | `E001` |
| User info object | Authentication success payload containing `id`, `name`, and `email`. | `E001` |
| Project status object | Socket response object containing `readOnly` and `authorization` fields. | `E004` |
| Battle acceptance input object | Socket input containing `socketID` and `firstUserID`. | `E002` |

## 4. Functional Requirements

| ID | Description | Trigger/Input | System Behavior | Output | Priority | Verification | Source Evidence |
|---|---|---|---|---|---|---|---|
| FR-001 | The system shall validate a provided JWT token and, when valid, return the authenticated user's information object. | JWT token input representing a user with `id`, `name`, `email` and expiration. | Validate the token and resolve authentication to the encoded user information. | User info object. | High | Test | `E001` |
| FR-002 | The system shall reject empty or malformed JWT token input by raising an API exception. | Empty token or token input consisting only of bearer prefix. | Detect invalid authentication input and fail authentication. | `APIException`. | High | Test | `E001` |
| FR-003 | The system shall evaluate project access requests and emit a `statusChecked` socket event with authorization status. | Socket request containing a project object. | Set default response to `readOnly: true` and `authorization: false`; if `projectID` or `versionID` is missing, emit the default status immediately; otherwise evaluate project authorization and emit the resulting status. | `statusChecked` event with response object. | High | Demonstration | `E004` |
| FR-004 | The system shall persist workspace-related socket/version mapping in cache for non-read-only project access when cache is ready. | Successful project access check resulting in non-read-only access and cache readiness. | Store the mapping in cache before emitting status. | Cache entry plus `statusChecked` event. | Medium | Inspection | `E004` |
| FR-005 | The system shall accept battle invitations using isolated cache access to reduce race-condition conflicts. | Battle acceptance request containing `socketID` and `firstUserID`. | Verify cache readiness, execute isolated cache transaction, watch the cache state, retrieve the battle object, and remove the corresponding cache entry. | Battle object when acceptance succeeds. | High | Inspection | `E002` |
| FR-006 | The system shall fail battle acceptance with a socket exception when isolated acceptance times out or battle creation fails. | Battle acceptance processing error/timeout. | Catch the failure and raise a `SocketException` identified as `battleFailed` with a failure message for battle acceptance timeout/creation failure. | Socket exception/error outcome. | High | Test | `E002` |

## 5. Non-Functional Requirements

| ID | Quality Attribute | Requirement | Priority | Verification | Source Evidence | Confidence |
|---|---|---|---|---|---|---|
| NFR-001 | Reliability | Cache-backed battle acceptance shall use isolated execution and watched cache state to mitigate race conditions during acceptance processing. | High | Inspection | `E002` | explicit |
| NFR-002 | Data integrity | Redis persistence shall keep RDB checksum validation enabled. | Medium | Inspection | `E005` | explicit |
| NFR-003 | Robustness | Redis loading/restoration shall support full sanitization checks for persisted or restored payloads as a configurable protection against corruption-related failures. | Medium | Inspection | `E005` | explicit |
| NFR-004 | Security | Redis deployments used by the system shall support authenticated access through ACL/user authentication rather than assuming unauthenticated access. | Medium | Inspection | `E006` | explicit |
| NFR-005 | Availability dependency | Cache-dependent operations shall verify cache readiness before execution. | High | Inspection | `E002`, `E004` | explicit |

## 6. Data Requirements

| ID | Data Item / Entity | Requirement | Source |
|---|---|---|---|
| DR-001 | User info object | Authentication success data shall include at least `id`, `name`, and `email`. | `E001` |
| DR-002 | JWT token | Authentication input shall be supplied as a token string; empty token input is invalid. | `E001` |
| DR-003 | Project status object | Project authorization responses shall contain `readOnly` and `authorization` fields. | `E004` |
| DR-004 | Project access request | Project authorization checks depend on `projectID` and `versionID`; missing either field results in unauthorized read-only status. | `E004` |
| DR-005 | Battle acceptance input | Battle acceptance requests shall include `socketID` and `firstUserID`. | `E002` |
| DR-006 | Battle cache object | Battle acceptance reads a battle object from Redis hash storage and deletes the related cache entry after retrieval. | `E002` |
| DR-007 | Redis persisted data | Redis persisted data shall use checksum-enabled RDB files; sanitization checks are supported during load/restore. | `E005` |

## 7. Constraints

| ID | Constraint | Source |
|---|---|---|
| C-001 | The evidenced implementation is constrained to a JavaScript/CommonJS server environment. | `E001`, `E002`, `E004` |
| C-002 | Cache-backed project and battle workflows depend on Redis availability/readiness. | `E002`, `E004` |
| C-003 | Redis configuration may require ACL-based authentication for connections. | `E006` |
| C-004 | Battle acceptance behavior is constrained to isolated Redis operations using watch/read/delete semantics. | `E002` |

## 8. Verification and Acceptance

| Requirement ID | Verification Method | Acceptance Basis |
|---|---|---|
| FR-001 | Test | Valid JWT input returns the expected user info object. |
| FR-002 | Test | Empty or malformed token input raises `APIException`. |
| FR-003 | Demonstration | A project access request causes a `statusChecked` emit with the expected authorization/read-only fields. |
| FR-004 | Inspection | Source inspection confirms cache write on non-read-only access when cache is ready. |
| FR-005 | Inspection | Source inspection confirms isolated cache execution with watched state, retrieval, and deletion. |
| FR-006 | Test | Battle acceptance failure path raises the documented socket exception/error outcome. |
| NFR-001 | Inspection | Source inspection confirms isolated cache execution and watched state for race-condition mitigation. |
| NFR-002 | Inspection | Redis configuration shows `rdbchecksum yes`. |
| NFR-003 | Inspection | Redis configuration documents sanitization-check support during load/restore. |
| NFR-004 | Inspection | Redis configuration documents ACL/authenticated access behavior. |
| NFR-005 | Inspection | Source inspection confirms readiness checks before cache-dependent operations. |

## 9. Traceability Matrix

| ID | Requirement | Type | Source | Evidence Type | Verification | Confidence |
|---|---|---|---|---|---|---|
| FR-001 | Validate JWT and return user info on success | Functional | `E001` | explicit | Test | High |
| FR-002 | Reject empty/malformed JWT input with API exception | Functional | `E001` | explicit | Test | High |
| FR-003 | Evaluate project access and emit `statusChecked` | Functional | `E004` | explicit | Demonstration | High |
| FR-004 | Cache socket/version mapping for non-read-only access | Functional | `E004` | explicit | Inspection | Medium |
| FR-005 | Accept battle invitations via isolated cache access | Functional | `E002` | explicit | Inspection | High |
| FR-006 | Raise socket exception on battle acceptance timeout/failure | Functional | `E002` | explicit | Test | High |
| NFR-001 | Use isolated cache execution to mitigate race conditions | Non-functional | `E002` | explicit | Inspection | High |
| NFR-002 | Keep Redis RDB checksum enabled | Non-functional | `E005` | explicit | Inspection | High |
| NFR-003 | Support sanitization checks for Redis load/restore | Non-functional | `E005` | explicit | Inspection | Medium |
| NFR-004 | Support authenticated Redis access via ACL/user auth | Non-functional | `E006` | explicit | Inspection | Medium |
| NFR-005 | Check cache readiness before cache-dependent operations | Non-functional | `E002`, `E004` | explicit | Inspection | High |
