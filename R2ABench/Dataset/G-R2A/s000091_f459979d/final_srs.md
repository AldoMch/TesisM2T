# Software Requirements Specification

## 1. Introduction

### Purpose
This SRS specifies repository-evidenced requirements for the components in `ertis-research/lwm2m-blockchain` that:
- expose authenticated user-management HTTP endpoints,
- interact with a blockchain-backed client/bootstrap store, and
- parse LwM2M node JSON structures.

### Product scope
The repository provides backend services that integrate:
- a main application backend with authenticated user operations,
- blockchain access for client/bootstrap information using Ethereum/Web3j, and
- LwM2M data handling using Leshan-related node structures.

### Intended audience
- Product owners and maintainers
- Backend and integration developers
- Test engineers
- Reviewers assessing requirement-to-code traceability

### References
- Repository: `ertis-research/lwm2m-blockchain`
- Repository URL: https://github.com/ertis-research/lwm2m-blockchain
- Commit: `caea581a21ac705c945540d1e54658b0bf82ecab`
- Evidence pack IDs: E001, E002, E003, E004, E005, E006

## 2. Overall Description

### Product perspective
The repository appears to contain multiple Java-based backend components:
- a Spring-based main backend with user endpoints,
- blockchain service integrations using Web3j and smart-contract calls,
- Leshan/LwM2M server-side components for client/bootstrap data and JSON node parsing.

### Product functions summary
- Retrieve users through an authenticated HTTP endpoint.
- Add users through an authenticated HTTP endpoint.
- Retrieve blockchain-stored client/security information.
- Submit client bootstrap data to a blockchain contract.
- Retrieve client bootstrap configuration from a blockchain contract.
- Deserialize LwM2M node JSON into typed node structures and reject invalid node payloads.

### User classes
- Authenticated API clients invoking user-management endpoints.
- Backend services integrating with an Ethereum node.
- LwM2M/Leshan-side components consuming bootstrap and node data.

### Operating environment
Supported by evidence:
- Java-based backend runtime
- Spring web controller/service environment
- Ethereum node reachable through Web3j `HttpService`
- Leshan/LwM2M data model classes

### Assumptions and dependencies
- User-management requests depend on JWT token validation outcomes. [E002]
- Blockchain-backed client operations depend on Ethereum connectivity through Web3j HTTP transport and smart-contract methods. [E001, E003, E004]
- LwM2M node data depends on JSON input matching expected object/array/value structures. [E005, E006]

## 3. External Interface Requirements

### User interfaces
No human-facing GUI is evidenced in the provided material.

### Software/API interfaces

| Interface | Description | Evidence |
|---|---|---|
| User HTTP API | Exposes authenticated user retrieval and user creation operations; creation uses `POST /add` and accepts a `User` request body. | E002 |
| Blockchain client store API | Uses contract calls including `getAllClients()`, `addClient(...)`, and `getClient(...)`. | E001, E004 |
| Ethereum connectivity API | Connects to an Ethereum node using Web3j over `HttpService(url)`. | E001 |
| LwM2M node JSON deserialization | Accepts JSON and converts it to `LwM2mNode` structures. | E005, E006 |

### Communication interfaces

| Interface | Protocol/Mechanism | Evidence |
|---|---|---|
| Main backend API | HTTP request/response via Spring controller mappings | E002 |
| Ethereum node communication | HTTP-based Web3j `HttpService` | E001 |

### Data exchange formats

| Format | Description | Evidence |
|---|---|---|
| JSON `User` payload | Request body for user creation and response payload for created user/list retrieval | E002 |
| Blockchain client/bootstrap fields | Endpoint plus bootstrap/server URL, ID, and key values passed to contract methods | E004 |
| LwM2M node JSON | Object form with fields such as `id` and `instances`; primitive values may map to BOOLEAN, STRING, INTEGER, or floating-point types | E005, E006 |

## 4. Functional Requirements

| ID | Requirement | Trigger/Input | System behavior | Output | Priority | Verification | Source evidence |
|---|---|---|---|---|---|---|---|
| FR-001 | The system shall provide an authenticated user-retrieval operation. | HTTP request with `Authorization` header to the user retrieval endpoint. | The system shall validate the token using `JwtUtility.isValidToken(auth, 1)`. If validation result is `0`, it shall return all users. If result is `1`, it shall reject the request as unauthorized. If result is `2`, it shall reject the request as forbidden. Otherwise, it shall return bad request. | HTTP `200 OK` with user list, or `401 Unauthorized`, `403 Forbidden`, or `400 Bad Request`. | High | Test | E002 |
| FR-002 | The system shall provide an authenticated user-creation operation. | `POST /add` request with `Authorization` header and `User` request body. | The system shall validate the token using `JwtUtility.isValidToken(auth, 1)`. If validation result is `0`, it shall add the user through the user service. If result is `1`, it shall reject the request as unauthorized. If result is `2`, it shall reject the request as forbidden. Otherwise, it shall return bad request. | HTTP `201 Created` with the created user payload, or `401 Unauthorized`, `403 Forbidden`, or `400 Bad Request`. | High | Test | E002 |
| FR-003 | The system shall retrieve blockchain-backed client/security information. | Request to retrieve all stored client/security entries. | The system shall invoke the blockchain contract method `getAllClients().send()`, convert the returned tuple collection to security information objects, and return the collection. | Collection of security information records. | High | Test | E001 |
| FR-004 | The system shall submit client bootstrap data to the blockchain contract. | Client bootstrap data containing endpoint, bootstrap server URL/ID/key, and server URL/ID/key. | The system shall convert the supplied string fields to byte-array representations and invoke the contract method `addClient(...)` with those values. | Blockchain transaction receipt for the add operation. | High | Demonstration | E004 |
| FR-005 | The system shall retrieve a client's bootstrap configuration from the blockchain contract by endpoint. | Client endpoint identifier. | The system shall invoke the contract method `getClient(...)` using the endpoint converted to the contract input format and shall construct a `BootstrapConfig` from the response. | Bootstrap configuration associated with the endpoint. | High | Test | E004 |

## 5. Non-Functional Requirements

| ID | Requirement | Quality attribute | Measure / condition | Priority | Verification | Evidence type | Source evidence |
|---|---|---|---|---|---|---|---|
| NFR-001 | User-management endpoints shall enforce token-based access control before performing user retrieval or creation. | Security | Requests without a valid token shall not perform the protected operation and shall return `401`, `403`, or `400` according to validation outcome. | High | Test | explicit | E002 |
| NFR-002 | Blockchain integration shall be compatible with an Ethereum node reachable via HTTP through Web3j. | Compatibility | Blockchain connectivity shall use Web3j built with `HttpService(url)`. | Medium | Inspection | explicit | E001 |
| NFR-003 | LwM2M node JSON processing shall reject structurally invalid node payloads rather than silently accepting them. | Data integrity | Invalid node elements, and `instances` objects missing `id`, shall cause a `JsonParseException`. | Medium | Test | explicit | E005, E006 |

## 6. Data Requirements

| ID | Data item | Requirement | Source evidence |
|---|---|---|---|
| DR-001 | User payload | The system shall accept a `User` object as the request body for user creation and return user data in successful responses. | E002 |
| DR-002 | Client/bootstrap contract payload | The system shall represent client bootstrap data using endpoint, bootstrap server URL, bootstrap ID, bootstrap key, server URL, server ID, and server key fields. | E004 |
| DR-003 | Blockchain client/security collection | The system shall handle blockchain retrieval results returned as tuple collections and convert them to security information objects. | E001 |
| DR-004 | LwM2M node JSON | The system shall accept node JSON objects with optional `id`; when `instances` is present, `id` is required. | E006 |
| DR-005 | LwM2M primitive typing | The system shall map JSON primitive values to Leshan resource types BOOLEAN, STRING, INTEGER, or floating-point type according to the JSON value kind. | E005 |

## 7. Constraints

| ID | Constraint | Type | Source evidence |
|---|---|---|---|
| C-001 | Protected user operations depend on JWT token validation using `JwtUtility.isValidToken(auth, 1)`. | Security/operational | E002 |
| C-002 | Blockchain connectivity uses Web3j with HTTP transport to an Ethereum node. | Technology/platform | E001 |
| C-003 | Blockchain operations depend on smart-contract methods including `getAllClients`, `addClient`, and `getClient`; one referenced contract name is `BootstrapStore`. | Integration | E001, E003, E004 |
| C-004 | LwM2M JSON data handling depends on Leshan node/resource model types. | Technology/data model | E005, E006 |

## 8. Verification and Acceptance

| Requirement ID | Verification method | Acceptance criterion |
|---|---|---|
| FR-001 | Test | Authenticated valid request returns `200` with user list; invalid token states return `401`, `403`, or `400` as defined. |
| FR-002 | Test | `POST /add` with valid token and `User` body returns `201` and the created user; invalid token states return `401`, `403`, or `400`. |
| FR-003 | Test | A retrieval request results in contract `getAllClients().send()` usage and returns converted security information records. |
| FR-004 | Demonstration | Supplying endpoint and bootstrap/server fields results in contract `addClient(...)` invocation and a transaction receipt. |
| FR-005 | Test | Supplying an endpoint results in contract `getClient(...)` invocation and a returned `BootstrapConfig`. |
| NFR-001 | Test | Protected operations do not execute when token validation fails and return the corresponding HTTP status. |
| NFR-002 | Inspection | Blockchain connection logic uses Web3j `HttpService(url)` to build the client. |
| NFR-003 | Test | Invalid node JSON and `instances` payloads without `id` raise `JsonParseException`. |

## 9. Traceability Matrix

| ID | Requirement | Type | Source | Evidence Type | Verification | Confidence |
|---|---|---|---|---|---|---|
| FR-001 | Authenticated user retrieval with defined HTTP status outcomes | Functional | E002 | explicit | Test | High |
| FR-002 | Authenticated user creation at `POST /add` with defined HTTP status outcomes | Functional | E002 | explicit | Test | High |
| FR-003 | Retrieve all blockchain-backed client/security entries | Functional | E001 | explicit | Test | Medium |
| FR-004 | Submit client bootstrap data to blockchain contract | Functional | E004 | explicit | Demonstration | Medium |
| FR-005 | Retrieve bootstrap configuration by endpoint from blockchain | Functional | E004 | explicit | Test | Medium |
| NFR-001 | Token-based access control on protected user endpoints | Non-functional | E002 | explicit | Test | High |
| NFR-002 | Ethereum HTTP/Web3j compatibility | Non-functional | E001 | explicit | Inspection | High |
| NFR-003 | Reject invalid LwM2M node JSON | Non-functional | E005, E006 | explicit | Test | High |
| DR-001 | User request/response payload handling | Data | E002 | explicit | Inspection | High |
| DR-002 | Client/bootstrap contract field set | Data | E004 | explicit | Inspection | Medium |
| DR-003 | Tuple-to-security-information conversion | Data | E001 | explicit | Inspection | Medium |
| DR-004 | LwM2M node JSON structure rules | Data | E006 | explicit | Inspection | High |
| DR-005 | Primitive type mapping for LwM2M node values | Data | E005 | explicit | Inspection | High |
| C-001 | JWT validation dependency | Constraint | E002 | explicit | Inspection | High |
| C-002 | Web3j HTTP Ethereum dependency | Constraint | E001 | explicit | Inspection | High |
| C-003 | Smart-contract method dependency including `BootstrapStore` | Constraint | E001, E003, E004 | explicit | Inspection | Medium |
| C-004 | Leshan node/resource model dependency | Constraint | E005, E006 | explicit | Inspection | High |
