# Software Requirements Specification

## 1. Introduction

### Purpose
This SRS defines checked software requirements for the `teamgram/teamgram-server` product. It consolidates repository-backed requirements into a normalized specification suitable for downstream architecture and design activities.

### Product scope
The product is an open-source server system for Telegram-compatible clients using MTProto-related protocols and services. The repository also documents deployment and operation using Docker or manual build/install, integration with infrastructure services, protocol handling for authorization keys, salts, sessions, and selected MTProto service messages.

For protocol behaviors involving authorization keys, server salt, encrypted sessions, future salts, and related session interactions, this SRS relies conservatively on protocol documentation together with repository implementation cues. Requirements are therefore framed as server support for protocol-required interactions rather than as stronger claims about full protocol-flow guarantees unless directly supported.

### Intended audience
This document is intended for:
- Product maintainers and backend engineers
- Architects and integration engineers
- Test engineers
- Operators deploying the server and its required infrastructure

## 2. Overall Description

### Product perspective
The product is a Go-based server system organized as a layered, multi-service architecture rather than a single monolithic server process. The repository structure and documented architecture indicate collaborating layers and services including:
- A client access layer for Telegram-compatible client communication
- A BFF or access-facing service layer
- Business/service-layer components such as messaging-related services
- Storage-facing components and supporting infrastructure integrations
- Asynchronous and supporting components such as Kafka-, push-, and sync-related flows

The deployed system depends on external infrastructure including MySQL, Redis, etcd, Kafka, and MinIO.

### Product functions summary
The product supports or documents the following functions:
- Serving Telegram-compatible clients through MTProto-related server behavior
- Supporting authorization-key and session-related protocol interactions
- Supporting server-salt and future-salt related interactions required by the protocol
- Supporting encrypted-session communication after authorization
- Handling selected MTProto service messages such as `rpc_drop_answer` and `destroy_session`
- Supporting Docker-based startup and manual deployment/install workflows
- Optionally using FFmpeg/FFProbe through an embedded wrapper component where media-processing functionality is enabled

### User classes
- End users operating Telegram-compatible clients against the server
- Operators and deployers configuring and running the server and its infrastructure dependencies
- Developers and integrators working with the service components and deployment environment

### Operating environment
The system operates in an environment that includes:
- A Go runtime/build environment
- Docker-based deployment or startup support
- External infrastructure services: MySQL, Redis, etcd, Kafka, and MinIO
- Optional FFmpeg and FFProbe tools where the media wrapper component is used

### Assumptions and dependencies
- Clients are compatible with Telegram/MTProto expectations used by the server
- Deployment includes the required infrastructure services
- Protocol-facing session, salt, and service-message behavior follows documented MTProto semantics
- If the optional media wrapper capability is used, FFmpeg and FFProbe are available in the runtime environment

## 3. External Interface Requirements

### User interfaces
No end-user graphical user interface requirements are explicitly defined in the available repository material.

Operational user interaction is provided through documented deployment and startup paths, including Docker-based startup and manual build/install procedures.

### Software/API interfaces
The system shall provide or use the following software interfaces:
- An MTProto-compatible server interface for Telegram-compatible clients
- Service-message handling interfaces for messages including `rpc_drop_answer` and `destroy_session`
- Integration interfaces to MySQL, Redis, etcd, Kafka, and MinIO
- An optional FFmpeg/FFProbe wrapper interface where media-processing functionality is used

### Communication interfaces
The system shall support:
- MTProto client-server communication
- Encrypted session communication after authorization-related setup
- RPC and service-message exchanges needed for supported MTProto interactions

### Data exchange formats
The system handles or exchanges data including:
- Authorization keys
- Server salts and future salts
- Session identifiers such as `session_id`
- Registration information
- Phone number verification-related data
- MTProto service messages including `rpc_drop_answer` and `destroy_session`

## 4. Functional Requirements

| ID | Requirement | Priority | Verification |
|---|---|---|---|
| FR-001 | The system shall operate as an MTProto-compatible server for Telegram-compatible clients. | High | Demonstration |
| FR-002 | The system shall support protocol-required server-salt handling during authorization-key creation and related authorization flows. | High | Inspection and test |
| FR-003 | The system shall support establishment and use of encrypted sessions associated with authorization-key creation for subsequent client-server communication. | High | Inspection and test |
| FR-004 | The system shall support processing of registration information and phone-number verification interactions within the applicable session/protocol flow. | High | Inspection and test |
| FR-005 | The system shall support creation of new or additional client sessions using `session_id` values as required by the protocol. | Medium | Inspection and test |
| FR-006 | The system shall acknowledge receipt of `rpc_drop_answer` requests. | Medium | Test |
| FR-007 | The system shall support session replacement behavior associated with connection reset and old-session removal through `destroy_session`. | Medium | Test |
| FR-008 | The system shall process future-salts requests. When the request specifies a count, the response shall return no more than the requested number of salts; the response may return fewer than requested. When the request count is `0`, the implementation shall use the default behavior of requesting 32 salts. | Medium | Inspection and test |
| FR-009 | Under the default or none-verifier/test configuration, the system shall accept `12345` as the sign-in/sign-out verification code. When an external verification-code service is enabled, the verification code returned and checked by that external service shall be authoritative. | Medium | Test |

## 5. Non-Functional Requirements

| ID | Requirement | Priority | Verification |
|---|---|---|---|
| NFR-001 | The system shall be implemented in Go. | High | Inspection |
| NFR-002 | The system shall maintain interoperability with Telegram-compatible clients through its MTProto server behavior. | High | Demonstration |
| NFR-003 | The system shall support deployment through documented Docker-based and manual build/install paths. | Medium | Demonstration |
| NFR-004 | Where the repository’s media wrapper capability is used, the runtime environment shall provide FFmpeg and FFProbe. | Low | Inspection |

## 6. Data Requirements

| ID | Data item | Requirement |
|---|---|---|
| DR-001 | Authorization key | The system shall create, use, or process authorization-key data as part of supported authorization and encrypted-session flows. |
| DR-002 | Server salt and future salts | The system shall handle server-salt data during authorization-related flows and shall process future-salts request/response data. |
| DR-003 | Session and `session_id` | The system shall associate communication with session data and shall support session creation or replacement using `session_id` values in applicable protocol flows. |
| DR-004 | Registration and verification data | The system shall process registration information and phone-number verification-related data within the applicable session/protocol flow. |
| DR-005 | Service-message data | The system shall process service-message data including `rpc_drop_answer` and `destroy_session`. |

## 7. System Constraints

| ID | Constraint |
|---|---|
| C-001 | The product is constrained to a Go implementation. |
| C-002 | Deployment is constrained by dependencies on MySQL, Redis, etcd, Kafka, and MinIO. |
| C-003 | The documented deployment paths are Docker-based startup and manual build/install. |
| C-004 | The fixed verification code `12345` applies only to the default or none-verifier/test configuration; deployments using an external verification service are constrained by that service’s returned and validated code. |
| C-005 | Use of the media wrapper capability is constrained by the availability of FFmpeg and FFProbe. |

## 8. Verification and Acceptance Criteria

| Requirement ID | Verification method | Acceptance criteria |
|---|---|---|
| FR-001 | Demonstration | A Telegram-compatible client can connect to the system and exchange MTProto-compatible messages. |
| FR-002 | Inspection and test | Repository implementation and protocol-facing behavior show support for server-salt handling during authorization-related flows. |
| FR-003 | Inspection and test | Repository implementation and runtime behavior show that post-authorization communication can occur within an encrypted session associated with the authorization key. |
| FR-004 | Inspection and test | Repository implementation and runtime behavior show support for registration and phone-number verification interactions within the applicable session/protocol flow. |
| FR-005 | Inspection and test | Supplying a new or replacement `session_id` through the applicable protocol flow results in support for a new or additional session. |
| FR-006 | Test | Sending `rpc_drop_answer` produces the required acknowledgment response. |
| FR-007 | Test | After old-session removal through `destroy_session`, the system supports creation of a replacement session in the applicable flow. |
| FR-008 | Inspection and test | A future-salts request produces a response containing `req_msg_id`, `now`, and `salts`. The number of returned salts does not exceed the requested count; when the request count is `0`, the implementation uses the default count of 32 as the request basis and may still return fewer salts than requested. |
| FR-009 | Test | In the default or none-verifier/test configuration, sign-in/sign-out verification succeeds when code `12345` is supplied. When an external verification service is enabled, verification follows the code returned and validated by that service rather than the fixed default code. |
| NFR-001 | Inspection | The implementation language used by the product is Go. |
| NFR-002 | Demonstration | The system interoperates with a Telegram-compatible client through its MTProto server behavior. |
| NFR-003 | Demonstration | The product can be deployed or started using the documented Docker-based path and the documented manual build/install path. |
| NFR-004 | Inspection | Environments using the media wrapper capability include FFmpeg and FFProbe. |
