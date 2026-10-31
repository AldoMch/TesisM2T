# Software Requirements Specification

## 1. Introduction

### Purpose
This SRS defines the checked and normalized software requirements for `s000091_f459979d`. It captures the repository-supported behavior of a system for LwM2M-oriented device-management scenarios that combines authenticated management APIs, blockchain-backed storage of client/bootstrap information, and LwM2M node JSON handling.

### Product scope
The product is a backend-oriented system that supports:
- management-side access-controlled user operations,
- storage and retrieval of client/bootstrap information through blockchain integration,
- LwM2M-related data parsing and handling, and
- broader LwM2M device-management and bootstrap scenarios supported by the repository context.

This SRS is limited to behavior that is supported by the provided implementation and review-backed corrections. It does not restate deployment architecture components item by item.

### Intended audience
This document is intended for:
- maintainers of the backend, blockchain-integration, and LwM2M-related components,
- architects deriving component and interface views,
- integration engineers connecting management, blockchain, and LwM2M services, and
- test engineers validating externally observable behavior.

## 2. Overall Description

### Product perspective
The product contains multiple backend components that cooperate in an LwM2M and blockchain-supported management environment, including:
- a Spring-based backend exposing protected user operations,
- blockchain service integrations using Ethereum/Web3j and smart-contract interactions for client/bootstrap information, and
- Leshan/LwM2M-side logic for node parsing and bootstrap-related data handling.

### Product functions summary
The system supports:
- retrieval of users through an access-controlled HTTP operation,
- creation of users through an access-controlled HTTP operation,
- retrieval of blockchain-stored client/security information,
- submission of client bootstrap data to a blockchain contract,
- retrieval of client bootstrap configuration from blockchain-backed data, and
- deserialization of LwM2M node JSON into typed node structures while rejecting invalid payloads.

### User classes
| User class | Description |
|---|---|
| Authenticated API client | Client invoking protected user-management operations through HTTP with an Authorization header. |
| Backend integration service | Service component interacting with Ethereum-compatible blockchain services through Web3j and contract calls. |
| LwM2M service component | Component consuming bootstrap information and parsing LwM2M node JSON structures. |

### Operating environment
| Environment aspect | Supported statement |
|---|---|
| Backend runtime | The system operates in a Java backend environment. |
| Web framework | Protected management operations are exposed through Spring HTTP controller behavior. |
| Blockchain integration | Blockchain connectivity uses Web3j with HTTP transport to an Ethereum-compatible node. |
| LwM2M integration | LwM2M data handling uses Leshan/LwM2M model types and node structures. |

### Assumptions and dependencies
| ID | Statement |
|---|---|
| A-001 | Protected user-management operations depend on Authorization-header token validation results. |
| A-002 | Blockchain-backed client/bootstrap operations depend on Ethereum connectivity through Web3j HTTP transport and smart-contract methods. |
| A-003 | LwM2M node parsing depends on JSON payloads matching the expected node/object/value structure rules. |
| A-004 | Client/bootstrap data exchanged with the blockchain depends on fixed 32-byte ASCII-compatible field encoding and decoding. |

## 3. External Interface Requirements

### User interfaces
No human-facing GUI behavior is specified in this SRS.

### Software/API interfaces
| Interface | Requirement summary |
|---|---|
| User HTTP API | The User API shall support user retrieval and user creation operations, both access-controlled based on the Authorization header. |
| Blockchain client/bootstrap interface | The system shall interact with blockchain-backed client/bootstrap storage through contract operations for retrieving all clients, adding client data, and retrieving a client by endpoint. |
| Ethereum connectivity interface | The system shall connect to an Ethereum-compatible node through Web3j using HTTP transport. |
| LwM2M node deserialization interface | The system shall accept JSON input and convert it into typed LwM2M node structures. |

### Communication interfaces
| Interface | Requirement summary |
|---|---|
| Backend API communication | Management operations shall be exposed through HTTP request/response interactions. |
| Blockchain communication | Blockchain node communication shall use Web3j HTTP transport. |

### Data exchange formats
| Format/item | Requirement summary |
|---|---|
| User payload | User creation shall accept a `User` request body, and successful user operations shall return user data. |
| Client/bootstrap contract fields | Client/bootstrap interactions shall handle endpoint, bootstrap server URL, bootstrap identity, bootstrap key, server URL, server identity, and server key fields. |
| Blockchain string encoding | String fields exchanged with the smart contract shall be encoded as fixed 32-byte ASCII values on submission and decoded back to ASCII strings on retrieval. |
| LwM2M node JSON | LwM2M node JSON shall support object structures with node identifiers, instances, and primitive values mapped to typed resource representations. |

## 4. Functional Requirements

| ID | Description | Trigger/Input | System behavior | Output | Priority | Verification |
|---|---|---|---|---|---|---|
| FR-001 | Authenticated user retrieval | HTTP GET request with Authorization header to the user retrieval endpoint | The system shall validate the token before retrieving users. If validation result is `0`, it shall return the user list. If result is `1`, it shall reject the request as unauthorized. If result is `2`, it shall reject the request as forbidden. Otherwise, it shall return bad request. | HTTP `200 OK` with user list, or `401 Unauthorized`, `403 Forbidden`, or `400 Bad Request` | High | Test |
| FR-002 | Authenticated user creation | `POST /add` request with Authorization header and `User` request body | The system shall validate the token before creating a user. If validation result is `0`, it shall add the user through the user service. If result is `1`, it shall reject the request as unauthorized. If result is `2`, it shall reject the request as forbidden. Otherwise, it shall return bad request. | HTTP `201 Created` with created user payload, or `401 Unauthorized`, `403 Forbidden`, or `400 Bad Request` | High | Test |
| FR-003 | Retrieval of blockchain-backed client/security information | Request to retrieve stored client/security information | The system shall retrieve client security information from the blockchain-backed contract and convert the result into a returned security-information collection. When contract access fails, the system shall record the exception according to the current implementation and return an empty collection without propagating the exception to the caller. | Returned collection of security-information records, or an empty collection on contract-access failure | High | Test |
| FR-004 | Submission of client bootstrap data to the blockchain contract | Client bootstrap data containing endpoint, bootstrap server URL/identity/key, and server URL/identity/key | Before submitting client bootstrap data, the system shall convert the relevant string fields into fixed 32-byte ASCII representation and invoke the blockchain contract add-client operation with those values. | Blockchain transaction receipt for the add operation | High | Demonstration |
| FR-005 | Retrieval of client bootstrap configuration by endpoint | Client endpoint identifier | The system shall convert the endpoint into fixed 32-byte form, invoke the blockchain retrieval operation for that endpoint, decode returned fixed 32-byte fields to ASCII strings, and construct the bootstrap configuration from the decoded values. | Bootstrap configuration associated with the endpoint | High | Test |
| FR-006 | LwM2M node JSON deserialization | JSON payload representing a LwM2M node | The system shall deserialize valid JSON payloads into typed LwM2M node structures. It shall reject invalid node payloads. | Typed LwM2M node structure, or parsing failure for invalid payload | High | Test |

## 5. Non-Functional Requirements

| ID | Quality attribute | Requirement | Priority | Verification |
|---|---|---|---|---|
| NFR-001 | Security | User-management endpoints shall enforce token-based access control before performing retrieval or creation operations. Requests that fail validation shall not perform the protected operation and shall return the corresponding error status. | High | Test |
| NFR-002 | Compatibility | Blockchain integration shall be compatible with an Ethereum-compatible node reachable via HTTP through Web3j. | Medium | Inspection |
| NFR-003 | Data integrity | LwM2M node JSON processing shall reject structurally invalid payloads rather than silently accepting them. Invalid node elements, and `instances` objects missing required `id`, shall cause parsing failure. | Medium | Test |
| NFR-004 | Interoperability | Smart-contract string-field exchange shall use fixed 32-byte ASCII-compatible encoding on submission and ASCII decoding on retrieval to match contract interaction requirements. | High | Inspection |

## 6. Data Requirements

| ID | Data item/entity | Requirement |
|---|---|---|
| DR-001 | User payload | The system shall accept a `User` object as the request body for user creation and shall return user data in successful user-operation responses. |
| DR-002 | Client/bootstrap contract payload | The system shall represent client bootstrap data using endpoint, bootstrap server URL, bootstrap identity, bootstrap key, server URL, server identity, and server key fields. String fields exchanged with the smart contract shall be encoded as fixed 32-byte ASCII values on submission and decoded back from fixed 32-byte values to ASCII strings on retrieval. |
| DR-003 | Blockchain client/security collection | The system shall convert blockchain retrieval results into security-information objects and return them as a collection. |
| DR-004 | LwM2M node JSON structure | The system shall accept node JSON objects with optional `id`; when `instances` is present, `id` shall be required. |
| DR-005 | LwM2M primitive type mapping | JSON primitive values shall be mapped as follows: boolean to `BOOLEAN`; string to `STRING`; number to `INTEGER` if its double value can be losslessly represented as a long value; other numbers to `FLOAT`; primitive value types not otherwise covered shall be handled as `STRING` by default. |

## 7. System Constraints

| ID | Constraint |
|---|---|
| C-001 | Protected user operations are constrained by token validation using `JwtUtility.isValidToken(auth, 1)`. |
| C-002 | Blockchain connectivity is constrained to Web3j using HTTP transport to an Ethereum-compatible node. |
| C-003 | Blockchain client/bootstrap operations are constrained by smart-contract interaction patterns for retrieving all clients, adding client data, and retrieving a client by endpoint. |
| C-004 | LwM2M JSON handling is constrained by Leshan/LwM2M node and resource model types. |
| C-005 | Contract-exchanged string fields are constrained to fixed 32-byte ASCII-compatible encoding and decoding behavior. |

## 8. Verification and Acceptance Criteria

| Requirement ID | Verification method | Acceptance criterion |
|---|---|---|
| FR-001 | Test | A valid authenticated GET request returns `200 OK` with the user list. Validation result `1` returns `401 Unauthorized`, result `2` returns `403 Forbidden`, and other invalid validation outcomes return `400 Bad Request`. |
| FR-002 | Test | A valid `POST /add` request with Authorization header and `User` body returns `201 Created` with the created user. Validation result `1` returns `401 Unauthorized`, result `2` returns `403 Forbidden`, and other invalid validation outcomes return `400 Bad Request`. |
| FR-003 | Test | On successful blockchain access, the system returns a converted security-information collection. When contract access fails, the system returns an empty collection and does not interrupt the caller flow. |
| FR-004 | Demonstration | Supplying valid client bootstrap fields results in fixed 32-byte ASCII conversion of the relevant string inputs and submission of the add-client blockchain operation, producing a transaction receipt. |
| FR-005 | Test | Supplying an endpoint results in fixed 32-byte encoding of the endpoint, retrieval of the corresponding blockchain-backed client data, ASCII decoding of returned fields, and construction of the expected bootstrap configuration. |
| FR-006 | Test | Valid LwM2M node JSON is deserialized into typed node structures. Invalid node JSON, including `instances` payloads without required `id`, results in parsing failure. |
| NFR-001 | Test | Protected user operations do not execute when token validation fails and return the corresponding HTTP error status. |
| NFR-002 | Inspection | Blockchain connection logic uses Web3j with HTTP transport to connect to the Ethereum-compatible node. |
| NFR-003 | Test | Structurally invalid node payloads are rejected rather than silently accepted. |
| NFR-004 | Inspection | Contract string fields are encoded to fixed 32-byte ASCII-compatible form on submission and decoded back to ASCII on retrieval. |
