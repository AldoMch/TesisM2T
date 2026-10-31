# Software Requirements Specification

## 1. Introduction

### Purpose
This SRS defines the observable requirements for the HypnoLog Server repository at commit `11dc566c7f0136215b032fec7d49ca9ef1bc74b9`, based only on the provided repository evidence.

### Product scope
HypnoLog Server is a server component for logging data by receiving HTTP requests and enabling visualization of logged data through a browser-based web UI. The documented intent is to support logging from any platform, language, or environment capable of sending HTTP requests. Evidence also indicates browser clients receive data from the same server and connect using WebSocket.

### Intended audience
- Maintainers of HypnoLog Server
- Integrators building logging clients
- Users accessing the visualization web UI
- Testers verifying server behavior

### References
- Repository: `SimonLdj/hypnolog-server`
- Commit: `11dc566c7f0136215b032fec7d49ca9ef1bc74b9`
- Evidence:
  - `E002` — `doc/HypnoLog-documentation.md`
  - `E003` — `doc/api-doc.md`
  - `E005` — `doc/hypnolog-data-obejct-schema.json`
  - `E006` — `public/javascripts/client.js`
  - `E004` — `README.md`

## 2. Overall Description

### Product perspective
HypnoLog Server sits between logging producers and browser-based consumers:
1. Logging code sends HTTP requests to the server.
2. The server receives logged data.
3. A browser accesses the web UI and receives data from the same server for visualization.

In the simplest documented scenario, the logging code, server, and browser can run on the same machine. Sources: `E002`.

### Product functions summary
- Receive logged data via HTTP POST. (`E003`)
- Accept JSON log objects described by the documented schema. (`E003`, `E005`)
- Provide a browser-accessed web UI for viewing logged data. (`E002`)
- Provide server-to-browser data delivery used by the client through WebSocket. (`E006`, inferred from client code)

### User classes
- Logging client developers sending data to the server over HTTP from arbitrary languages or technologies. (`E002`, `E003`)
- End users viewing logged data in a browser. (`E002`)

### Operating environment
- Server environment capable of handling HTTP requests. (`E002`, `E003`)
- Browser environment for the web UI. (`E002`)
- Browser client capable of opening a WebSocket connection to the server. (`E006`)

### Assumptions and dependencies
- Logging clients can send HTTP requests and JSON payloads. (`E002`, `E003`)
- Browser clients connect to the same server instance that receives logs. (`E002`)
- Browser-side processing uses a JSON schema validator to validate server-provided data objects. (`E006`)

## 3. External Interface Requirements

### User interfaces
| Interface | Requirement |
|---|---|
| Browser web UI | The system shall provide access to logged data through a web UI used from a browser. Source: `E002` |

### Software/API interfaces
| Interface | Requirement |
|---|---|
| HTTP logging API | The system shall accept logging input via HTTP POST. Sources: `E002`, `E003` |
| WebSocket interface | The system shall support browser client connection to the server using WebSocket for receiving server data. Source: `E006` (inferred) |

### Communication interfaces
| Interface | Details |
|---|---|
| HTTP | Used by logging producers to send data to the server. Sources: `E002`, `E003` |
| WebSocket | Used by browser clients to connect to the server and receive data. Source: `E006` (inferred) |

### Data exchange formats
| Format | Usage |
|---|---|
| JSON | Logging messages are sent as JSON; the documented data object requires `data` and `type` properties. Sources: `E003`, `E005` |

## 4. Functional Requirements

| ID | Description | Trigger/Input | System behavior | Output | Priority | Verification | Source evidence |
|---|---|---|---|---|---|---|---|
| FR-001 | Receive log submissions over HTTP | Client sends an HTTP POST request to the server | The system shall accept log data submitted through an HTTP POST interface. | HTTP-level acceptance of the submission for server processing | High | Test | `E002`, `E003` |
| FR-002 | Accept structured JSON log objects | Client submits a JSON logging message | The system shall accept logging messages in JSON object form matching the documented HypnoLog Data Object structure. | Logged message object available to the server in structured form | High | Test | `E003`, `E005` |
| FR-003 | Require core log object fields | Client submits a HypnoLog data object | The system shall require the log object to contain `data` and `type` fields. | Object is processable only when required fields are present | High | Test | `E005` |
| FR-004 | Provide browser-based access to logged data | User accesses the system from a browser | The system shall make logged data viewable through a browser-accessed web UI. | Browser can view logged data | High | Demonstration | `E002` |
| FR-005 | Deliver server data to browser clients through a persistent connection | Browser client loads the web application and connects to the server | The system shall provide data to browser clients through a WebSocket connection to the server. | Browser client receives server data over WebSocket | Medium | Test | `E006` |
| FR-006 | Support language-agnostic log producers | A producer implemented in any language or technology sends an HTTP request | The system shall expose its logging interface through HTTP so that producers are not restricted to a specific implementation language. | Producers from different languages can submit logs using HTTP | Medium | Analysis | `E002`, `E003` |

## 5. Non-Functional Requirements

| ID | Requirement | Quality attribute | Priority | Verification | Source evidence | Evidence type |
|---|---|---|---|---|---|---|
| NFR-001 | The logging interface shall be protocol-compatible with clients from any language, technology, or environment that can send HTTP requests. | Compatibility/Portability | High | Analysis | `E002`, `E003` | explicit |
| NFR-002 | The browser-facing portion of the system shall operate through a standard web browser. | Compatibility/Usability | High | Demonstration | `E002` | explicit |
| NFR-003 | Browser clients shall validate server-provided HypnoLog data objects against the documented JSON schema before use. | Data integrity | Medium | Inspection | `E005`, `E006` | inferred |

## 6. Data Requirements

### Data entities or objects

| Entity | Description | Required fields | Source evidence |
|---|---|---|---|
| HypnoLog Data Object | Data logged using HypnoLog and received by the server via HTTP API | `data`, `type` | `E005` |

### Input/output data

| Direction | Data | Description | Source evidence |
|---|---|---|---|
| Input to server | JSON log message | Logging payload sent via HTTP POST | `E003`, `E005` |
| Output to browser client | HypnoLog data object(s) | Data received by browser client from the server and validated against schema | `E006` |

### Data integrity, storage, retention, privacy, migration
No explicit repository evidence was provided for persistence, retention period, deletion, privacy controls, or migration behavior.

## 7. Constraints

| ID | Constraint | Source evidence |
|---|---|---|
| C-001 | Logging integration is constrained to HTTP-based submission. | `E002`, `E003` |
| C-002 | Log message structure is constrained by the documented JSON object model requiring `data` and `type`. | `E005` |
| C-003 | Browser consumption is constrained to clients capable of using the web UI and establishing a WebSocket connection. | `E002`, `E006` |

## 8. Verification and Acceptance

| Requirement ID | Verification method | Acceptance basis |
|---|---|---|
| FR-001 | Test | An HTTP POST carrying a logging payload is accepted by the server interface. |
| FR-002 | Test | A JSON log object conforming to the documented structure is accepted. |
| FR-003 | Test | Objects missing `data` or `type` fail requirement validation; objects containing both satisfy it. |
| FR-004 | Demonstration | A user can access logged data from a browser web UI. |
| FR-005 | Test | A browser client connects via WebSocket and receives data from the server. |
| FR-006 | Analysis | Interface definition shows no language-specific client dependency beyond HTTP capability. |
| NFR-001 | Analysis | The interface specification uses HTTP, enabling broad client compatibility. |
| NFR-002 | Demonstration | The visualization path is exercised through a browser. |
| NFR-003 | Inspection | Client behavior shows schema-based validation of server-provided data objects. |

## 9. Traceability Matrix

| ID | Requirement | Type | Source | Evidence Type | Verification | Confidence |
|---|---|---|---|---|---|---|
| FR-001 | Receive log submissions over HTTP | Functional | `E002`, `E003` | explicit | Test | High |
| FR-002 | Accept structured JSON log objects | Functional | `E003`, `E005` | explicit | Test | High |
| FR-003 | Require core log object fields | Functional | `E005` | explicit | Test | High |
| FR-004 | Provide browser-based access to logged data | Functional | `E002` | explicit | Demonstration | High |
| FR-005 | Deliver server data to browser clients through a persistent connection | Functional | `E006` | inferred | Test | Medium |
| FR-006 | Support language-agnostic log producers | Functional | `E002`, `E003` | explicit | Analysis | Medium |
| NFR-001 | HTTP-based cross-language compatibility | Non-functional | `E002`, `E003` | explicit | Analysis | High |
| NFR-002 | Browser-based operation | Non-functional | `E002` | explicit | Demonstration | High |
| NFR-003 | Schema validation of server-provided data in browser client | Non-functional | `E005`, `E006` | inferred | Inspection | Medium |
