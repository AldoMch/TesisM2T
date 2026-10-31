# Software Requirements Specification

## 1. Introduction

### Purpose
This SRS defines evidence-backed requirements for the repository-specific product represented by `teamgram/teamgram-server` at commit `1d437a5dace319a50c051c025cc953b18d3d3a5e`.

### Product scope
The product is an open source MTProto server written in Go and intended to work with compatible Telegram clients. The repository also documents Docker-based startup, manual build/install, and protocol behaviors related to authorization keys, encrypted sessions, salts, and session lifecycle. Sources: [E001], [E002], [E004].

### Intended audience
- Product owners and maintainers
- Backend and integration engineers
- Test engineers
- Operators deploying the server and its documented dependencies

### References
- Repository README: [E001]
- MTProto mobile protocol description: [E002]
- MTProto service messages documentation: [E004]
- DAL terminology documents: [E005], [E006]
- Goffmpeg dependency README: [E003]

## 2. Overall Description

### Product perspective
The product is a server-side MTProto implementation in Go, intended for use by compatible Telegram clients. It is deployable via Docker or manual build/install and depends on external infrastructure components including MySQL, Redis, etcd, Kafka, and MinIO. Sources: [E001].

### Product functions summary
Supported and documented functions include:
- Serving compatible Telegram clients over MTProto [E001]
- Creating authorization keys and issuing server salts [E002]
- Establishing encrypted sessions for subsequent communication [E002]
- Carrying registration information and phone number validation within sessions [E002]
- Creating new or additional client sessions using session identifiers [E002]
- Handling service messages such as `rpc_drop_answer` and `destroy_session` [E004]
- Supporting requests for future salts [E004]

### User classes
- End users operating compatible Telegram clients through the server [E001]
- Operators/deployers using Docker or manual installation with documented dependencies [E001]
- Developers interacting with documented DAL/DAO/DO abstractions and optional FFmpeg wrapper components [E003], [E005], [E006]

### Operating environment
Documented environment elements:
- Go-based server runtime [E001]
- Docker-based demo/startup path [E001]
- Manual deployment with MySQL, Redis, etcd, Kafka, and MinIO dependencies [E001]
- FFmpeg/FFProbe for the documented transcoding wrapper component; supported platforms for that wrapper are Linux, OS X, and Windows [E003]

### Assumptions and dependencies
- Clients are MTProto/Telegram-compatible [E001]
- Authorization and session handling follow the documented MTProto flow [E002], [E004]
- Server deployment depends on MySQL, Redis, etcd, Kafka, and MinIO [E001]
- Some media-related capability depends on FFmpeg and FFProbe where the wrapper component is used [E003]

## 3. External Interface Requirements

### User interfaces
No end-user graphical or command-line interface requirements are explicitly documented in the evidence pack. Deployment entry points are documented through Docker and manual build/install instructions. Source: [E001].

### Software/API interfaces
- MTProto server interface for compatible Telegram clients [E001]
- Service-message handling including `rpc_drop_answer` and `destroy_session` [E004]
- External infrastructure dependencies: MySQL, Redis, etcd, Kafka, MinIO [E001]
- Optional media-processing dependency interface through FFmpeg/FFProbe wrapper components [E003]

### Communication interfaces
- MTProto client-server communication [E001], [E002]
- Encrypted session communication after authorization-key creation [E002]
- RPC/service-message exchanges including acknowledgments [E004]

### Data exchange formats
Explicit data items exchanged or handled include:
- Authorization keys [E002]
- Server salts and future salts [E002], [E004]
- Session identifiers (`session_id`) [E002]
- Registration information [E002]
- Phone number validation data [E002]
- RPC/service messages such as `rpc_drop_answer` and `destroy_session` [E004]

## 4. Functional Requirements

| ID | Description | Trigger/Input | System behavior | Output | Priority | Verification | Source evidence |
|---|---|---|---|---|---|---|---|
| FR-001 | The system shall operate as an MTProto server compatible with Telegram clients. | A compatible Telegram client connects and sends protocol requests. | The system shall accept and process client communication as an MTProto server. | Protocol-compatible server responses. | High | Demonstration | [E001] |
| FR-002 | During authorization-key creation, the system shall provide a server salt to the client. | Client initiates authorization-key creation. | The system shall issue the server salt associated with the new authorization key. | Server salt delivered to the client. | High | Test | [E002] |
| FR-003 | After authorization-key creation, the system shall establish an encrypted session using the newly generated key for subsequent communication. | Successful creation of a new authorization key. | The system shall use the new key for an encrypted session and continue communication within that session. | Encrypted session established for further exchanges. | High | Test | [E002] |
| FR-004 | The system shall support transmission of user registration information and phone number validation within the encrypted session created from a new authorization key. | Client submits registration information or phone validation data after session establishment. | The system shall receive and process that information within the encrypted session. | Registration and phone-validation exchanges occur within the session. | High | Test | [E002] |
| FR-005 | The system shall allow the client to create new or additional sessions by providing a new random `session_id`. | Client chooses a new random `session_id`. | The system shall establish a new session corresponding to the provided identifier. | New or additional session becomes available. | Medium | Test | [E002] |
| FR-006 | The system shall acknowledge receipt of `rpc_drop_answer` requests. | Client sends `rpc_drop_answer`. | The system shall return an acknowledgment for the request and treat it as receipt of the original query whose response is to be forgotten. | Acknowledgment response for `rpc_drop_answer`. | Medium | Test | [E004] |
| FR-007 | The system shall allow a client to create a new session after connection reset and removal of the old session through `destroy_session`. | Connection reset followed by old-session removal through `destroy_session`. | The system shall permit creation of a replacement session after the old session is removed. | New session established after old-session removal. | Medium | Test | [E004] |
| FR-008 | The system shall support client requests for several future salts. | Client requests future salts. | The system shall process the request and provide future salts. | Future salts returned to the client. | Medium | Test | [E004] |
| FR-009 | Unless reconfigured, the system shall use `12345` as the default verification code for sign-in and sign-out. | Sign-in or sign-out verification under default configuration. | The system shall validate using the documented default verification code. | Verification succeeds when code `12345` is supplied under default settings. | Medium | Test | [E001] |

## 5. Non-Functional Requirements

| ID | Description | Priority | Verification | Evidence type | Source evidence |
|---|---|---|---|---|---|
| NFR-001 | The system shall be implemented in Go. | High | Inspection | explicit | [E001] |
| NFR-002 | Communication after authorization-key creation shall occur within an encrypted session using the newly generated key. | High | Test | explicit | [E002] |
| NFR-003 | The system shall maintain interoperability with compatible Telegram clients through its MTProto server behavior. | High | Demonstration | explicit | [E001] |
| NFR-004 | Where the repository’s documented transcoding wrapper capability is used, the runtime environment shall provide FFmpeg and FFProbe. | Low | Inspection | explicit | [E003] |
| NFR-005 | The transcoding wrapper component shall be portable across Linux, OS X, and Windows environments. | Low | Demonstration | explicit | [E003] |

## 6. Data Requirements

| ID | Data entity/object | Requirement | Source evidence |
|---|---|---|---|
| DR-001 | Authorization key | The system shall create and use an authorization key as the basis for subsequent encrypted communication. | [E002] |
| DR-002 | Server salt / future salts | The system shall provide server salt during authorization-key creation and shall support providing future salts on request. | [E002], [E004] |
| DR-003 | Session / `session_id` | The system shall associate communication with sessions and shall support creation of new or additional sessions using new random `session_id` values. | [E002] |
| DR-004 | Registration information and phone number validation data | The system shall handle registration information and phone number validation data within the encrypted session. | [E002] |
| DR-005 | Service-message data | The system shall process service-message data including `rpc_drop_answer` and `destroy_session`. | [E004] |
| DR-006 | Data access abstractions | Repository data access terminology shall distinguish DAL, DO, and DAO abstractions. | [E005], [E006] |

## 7. Constraints

| ID | Constraint | Source evidence |
|---|---|---|
| C-001 | The product is constrained to a Go implementation. | [E001] |
| C-002 | Documented deployment depends on MySQL, Redis, etcd, Kafka, and MinIO. | [E001] |
| C-003 | The repository documents Docker-based startup and manual build/install as deployment paths. | [E001] |
| C-004 | Default sign-in/sign-out verification code is `12345` unless changed from the documented default. | [E001] |
| C-005 | Media transcoding wrapper usage depends on FFmpeg and FFProbe. | [E003] |

## 8. Verification and Acceptance

| Requirement ID | Verification method | Acceptance criterion |
|---|---|---|
| FR-001 | Demonstration | A compatible Telegram client can connect and exchange MTProto messages with the server. |
| FR-002 | Test | Authorization-key creation returns a server salt to the client. |
| FR-003 | Test | After key creation, subsequent communication occurs within an encrypted session using the new key. |
| FR-004 | Test | Registration and phone-validation exchanges are accepted within the encrypted session. |
| FR-005 | Test | Supplying a new random `session_id` results in a new or additional session. |
| FR-006 | Test | Sending `rpc_drop_answer` produces an acknowledgment response. |
| FR-007 | Test | After `destroy_session` removes the old session, a new session can be created following reset. |
| FR-008 | Test | A future-salts request returns multiple salts. |
| FR-009 | Test | Under default configuration, code `12345` is accepted for sign-in and sign-out verification. |
| NFR-001 | Inspection | The implementation language is Go. |
| NFR-002 | Test | Post-auth communication is encrypted and bound to the newly generated key. |
| NFR-003 | Demonstration | The server interoperates with a compatible Telegram client. |
| NFR-004 | Inspection | Environments using the wrapper capability include FFmpeg and FFProbe. |
| NFR-005 | Demonstration | The wrapper component operates on Linux, OS X, and Windows. |

## 9. Traceability Matrix

| ID | Requirement | Type | Source | Evidence Type | Verification | Confidence |
|---|---|---|---|---|---|---|
| FR-001 | Operate as an MTProto server compatible with Telegram clients | Functional | E001 | explicit | Demonstration | High |
| FR-002 | Provide server salt during authorization-key creation | Functional | E002 | explicit | Test | High |
| FR-003 | Establish encrypted session using newly generated key | Functional | E002 | explicit | Test | High |
| FR-004 | Handle registration information and phone validation within encrypted session | Functional | E002 | explicit | Test | High |
| FR-005 | Support creation of new/additional sessions using random `session_id` | Functional | E002 | explicit | Test | High |
| FR-006 | Acknowledge `rpc_drop_answer` | Functional | E004 | explicit | Test | Medium |
| FR-007 | Allow new session creation after reset and `destroy_session` removal of old session | Functional | E004 | explicit | Test | Medium |
| FR-008 | Support request for several future salts | Functional | E004 | explicit | Test | Medium |
| FR-009 | Use default verification code `12345` for sign-in/sign-out unless reconfigured | Functional | E001 | explicit | Test | High |
| NFR-001 | Implement in Go | Non-functional | E001 | explicit | Inspection | High |
| NFR-002 | Use encrypted session after authorization-key creation | Non-functional | E002 | explicit | Test | High |
| NFR-003 | Maintain Telegram-client interoperability | Non-functional | E001 | explicit | Demonstration | High |
| NFR-004 | Require FFmpeg and FFProbe where transcoding wrapper is used | Non-functional | E003 | explicit | Inspection | Medium |
| NFR-005 | Wrapper component portability across Linux, OS X, Windows | Non-functional | E003 | explicit | Demonstration | Medium |
| DR-001 | Authorization key as communication basis | Data | E002 | explicit | Inspection | High |
| DR-002 | Server salt and future salts handling | Data | E002, E004 | explicit | Inspection | High |
| DR-003 | Session and `session_id` data handling | Data | E002 | explicit | Inspection | High |
| DR-004 | Registration and phone-validation data handling | Data | E002 | explicit | Inspection | High |
| DR-005 | Service-message data handling | Data | E004 | explicit | Inspection | Medium |
| DR-006 | DAL/DO/DAO terminology separation | Data | E005, E006 | explicit | Inspection | Medium |
| C-001 | Go implementation constraint | Constraint | E001 | explicit | Inspection | High |
| C-002 | Dependency on MySQL, Redis, etcd, Kafka, MinIO | Constraint | E001 | explicit | Inspection | High |
| C-003 | Docker and manual build/install deployment paths | Constraint | E001 | explicit | Inspection | High |
| C-004 | Default verification code `12345` | Constraint | E001 | explicit | Inspection | High |
| C-005 | FFmpeg/FFProbe dependency for wrapper usage | Constraint | E003 | explicit | Inspection | Medium |
