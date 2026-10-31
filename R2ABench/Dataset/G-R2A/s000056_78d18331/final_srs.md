# Software Requirements Specification

## 1. Introduction

### Purpose
This SRS defines evidence-backed requirements for the `kubescape/host-scanner` repository snapshot at commit `7096303f0cd65f72eeca2ff856ff4a320332639b`. The document is limited to behaviors and constraints directly supported by the provided repository evidence.

### Product scope
Available evidence shows:
- an HTTP-exposed service with endpoint behavior validated by end-to-end tests,
- logic that derives a CNI configuration directory from runtime/process configuration inputs,
- logic that removes encryption provider configuration secrets from JSON-like control-plane data,
- a provider/platform-specific end-to-end test approach using build tags.

### Intended audience
- Maintainers of `kubescape/host-scanner`
- Test authors and reviewers
- Integrators consuming the HTTP interface
- Requirements and quality engineers

### References
- Repository: `kubescape/host-scanner`
- Repository URL: https://github.com/kubescape/host-scanner
- Snapshot: https://github.com/kubescape/host-scanner/tree/7096303f0cd65f72eeca2ff856ff4a320332639b
- Commit: `7096303f0cd65f72eeca2ff856ff4a320332639b`
- Evidence: E001, E002, E003, E004, E005, E006

## 2. Overall Description

### Product perspective
The repository contains:
- an HTTP service verified through end-to-end HTTP requests and status-code assertions,
- sensor/runtime logic that interprets host runtime configuration,
- data-sanitization logic for JSON control-plane content.

This perspective is based on tests and test documentation only.

### Product functions summary
- Respond to HTTP GET requests for endpoints, including unknown endpoints.
- Resolve a CNI configuration directory from runtime/process configuration inputs.
- Remove encryption provider configuration secrets from JSON data.
- Support provider/platform-specific end-to-end validation using build tags.

### User classes
- HTTP clients invoking service endpoints
- Automated end-to-end test authors
- Integrators or operators supplying runtime/process configuration data

### Operating environment
Supported evidence indicates:
- HTTP-based access for endpoint validation
- Go-based test execution with Ginkgo/Gomega-style tests
- provider/platform-specific test variants selected via build tags
- Linux-style host/runtime paths such as `/var/lib/kubelet`, `/var/run/containerd`, `/run/containerd`, `/etc/cni/`, and `/var/lib/cni/`  
Confidence for Linux/path assumptions: inferred from test inputs.  
Sources: E001, E002, E003, E004, E006

### Assumptions and dependencies
- Provider/platform-specific response validation depends on build-tag-selected data structures. Source: E003, E006
- Runtime directory resolution depends on process command-line arguments and/or runtime config defaults. Source: E001, E002
- Secret removal operates on JSON data unmarshaled into a key/value structure. Source: E005

## 3. External Interface Requirements

### User interfaces
No graphical or interactive user interface is evidenced.

### Software/API interfaces
| Interface | Requirement summary | Source |
|---|---|---|
| HTTP endpoint interface | The system exposes HTTP endpoints that can be invoked with `GET`; unknown endpoint handling is verified for `/doesnotexist`. | E004 |
| Runtime/config input interface | The system accepts process/configuration inputs sufficient to derive a CNI config directory. | E001, E002 |
| JSON data processing interface | The system accepts JSON-like control-plane data and outputs sanitized JSON data. | E005 |

### Communication interfaces
| Interface | Details | Source |
|---|---|---|
| HTTP | End-to-end tests send HTTP GET requests and validate HTTP status codes. | E004 |

### Data exchange formats
| Format | Usage | Source |
|---|---|---|
| HTTP request/response | Endpoint invocation and status-code validation | E004 |
| JSON | Input and output format for control-plane data sanitization | E005 |
| Command-line argument strings | Input used to derive runtime-related paths | E001, E002 |

## 4. Functional Requirements

| ID | Description | Trigger/Input | System behavior | Output | Priority | Verification | Source evidence |
|---|---|---|---|---|---|---|---|
| FR-001 | Unknown endpoint handling | HTTP `GET` request to `/doesnotexist` | The system shall accept the request and respond with HTTP status code `404`. | HTTP response with status `404` | High | Test | E004 |
| FR-002 | CNI configuration directory resolution | Runtime/process configuration input including command-line arguments and/or default config data | The system shall derive a CNI configuration directory from the provided runtime/process configuration. Evidence shows expected resolutions such as `/etc/cni/` and `/var/lib/cni/` for tested inputs. | Resolved CNI configuration directory path | High | Test | E001, E002 |
| FR-003 | Removal of encryption provider configuration secrets | JSON control-plane data containing encryption provider configuration content | The system shall remove encryption provider configuration secrets from the processed data before producing output. | Sanitized JSON data with secrets removed | High | Test | E005 |

## 5. Non-Functional Requirements

| ID | Quality attribute | Requirement | Priority | Verification | Evidence type | Source evidence |
|---|---|---|---|---|---|---|
| NFR-001 | Security | The system shall not expose encryption provider configuration secrets in processed JSON output. | High | Test | explicit | E005 |
| NFR-002 | Portability/Maintainability | End-to-end verification shall support provider/platform-specific expected data structures through build-tag-based test selection. | Medium | Inspection | explicit | E003, E006 |
| NFR-003 | Compatibility | The HTTP interface shall use standard HTTP request/response semantics, including status-code-based error reporting for unknown paths. | Medium | Test | explicit | E004 |

## 6. Data Requirements

### Data entities or objects
| Data entity | Description | Source |
|---|---|---|
| HTTP request | A `GET` request sent to a service endpoint such as `/doesnotexist` | E004 |
| HTTP response | Response object containing status code | E004 |
| Runtime/process details | Command-line arguments and runtime properties used to determine CNI config directory | E001, E002 |
| CNI configuration directory path | Derived filesystem path such as `/etc/cni/` or `/var/lib/cni/` | E001, E002 |
| Control-plane JSON data | JSON unmarshaled into a key/value map for secret removal | E005 |
| Provider/platform-specific expected structures | Test-side expected response structures selected via build tags | E003, E006 |

### Input/output data
| Flow | Input | Output | Source |
|---|---|---|---|
| Endpoint validation | HTTP `GET /doesnotexist` | HTTP status `404` | E004 |
| Runtime inspection | Process/configuration data | Resolved CNI directory path | E001, E002 |
| Data sanitization | JSON data containing encryption provider config | Sanitized JSON with secrets removed | E005 |

### Storage, privacy, integrity, retention, migration
| Topic | Requirement | Source |
|---|---|---|
| Privacy/confidentiality | Encryption provider configuration secrets shall be removed from processed JSON output. | E005 |
| Storage/retention/migration | Not established by available evidence. | — |

## 7. Constraints

| ID | Constraint | Source | Evidence type |
|---|---|---|---|
| C-001 | Provider/platform-specific end-to-end tests depend on Go build tags to select platform-designed data structures. | E003, E006 | explicit |
| C-002 | Runtime directory resolution is constrained by runtime/process inputs that may include Linux-style filesystem paths and container runtime endpoints. | E001, E002 | inferred |
| C-003 | HTTP behavior verification is constrained to request/response interactions observable through standard HTTP calls. | E004 | explicit |

## 8. Verification and Acceptance

| Requirement ID | Verification method | Acceptance criteria |
|---|---|---|
| FR-001 | Test | A `GET` request to `/doesnotexist` returns HTTP `404`. |
| FR-002 | Test | For supplied runtime/process test inputs, the resolved CNI directory matches the expected path. |
| FR-003 | Test | Given input JSON containing encryption provider configuration secrets, produced JSON matches the expected sanitized output. |
| NFR-001 | Test | Sanitized JSON output excludes encryption provider configuration secrets. |
| NFR-002 | Inspection | Test assets show provider/platform-specific expected structures selected via build tags. |
| NFR-003 | Test | HTTP interactions use request/response semantics with status-code-based reporting for unknown paths. |

## 9. Traceability Matrix

| ID | Requirement | Type | Source | Evidence Type | Verification | Confidence |
|---|---|---|---|---|---|---|
| FR-001 | Unknown endpoint `GET /doesnotexist` returns `404` | Functional | E004 | explicit | Test | High |
| FR-002 | Derive CNI config directory from runtime/process configuration | Functional | E001, E002 | explicit | Test | Medium |
| FR-003 | Remove encryption provider configuration secrets from JSON data | Functional | E005 | explicit | Test | High |
| NFR-001 | Do not expose encryption provider configuration secrets in processed JSON output | Non-functional | E005 | explicit | Test | High |
| NFR-002 | Support provider/platform-specific e2e verification via build tags | Non-functional | E003, E006 | explicit | Inspection | Medium |
| NFR-003 | Use standard HTTP semantics with status-code-based error reporting | Non-functional | E004 | explicit | Test | Medium |
