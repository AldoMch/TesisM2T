# Software Requirements Specification

## 1. Introduction

### Purpose
This Software Requirements Specification defines the checked requirements for `kubescape/host-scanner`. It captures the product behavior, interfaces, constraints, and verification criteria supported by the reviewed material for this sample.

### Product scope
`host-scanner` is a host information data collection component in the Kubescape project. It collects Kubernetes node host information to support later security posture assessment. It is typically deployed as a privileged Kubernetes DaemonSet and provides host information to clients through an HTTP API.

This specification includes the subset of behavior confirmed for this sample, including:
- HTTP endpoint behavior validated by end-to-end tests
- CNI configuration directory resolution from runtime and process configuration inputs
- Removal of encryption provider configuration secrets from JSON-like control-plane data
- Provider-specific end-to-end test selection using Go build tags

### Intended audience
- Maintainers of `kubescape/host-scanner`
- Architects and developers integrating with the HTTP API
- Test engineers validating endpoint, runtime-resolution, and sanitization behavior
- Operators deploying and running the component

## 2. Overall Description

### Product perspective
`host-scanner` is a Kubescape component that collects host information from Kubernetes nodes and exposes that information through an HTTP API. It is intended to run in a Kubernetes environment and is typically deployed as a privileged DaemonSet.

Within the scope covered by this specification, the product includes:
- an HTTP-accessible service
- logic that derives a CNI configuration directory from runtime type, configuration data, and process arguments
- logic that sanitizes control-plane JSON data by removing encryption provider configuration secrets
- provider-specific end-to-end test support using Go build tags

### Product functions summary
The system supports the following functions within this specification:
- respond to HTTP GET requests for known and unknown endpoints
- return HTTP 404 for an unknown endpoint request to `/doesnotexist`
- resolve the CNI configuration directory from runtime-specific inputs
- remove encryption provider configuration secrets from processed JSON output
- support provider-specific end-to-end test selection through Go build tags

### User classes
| User class | Description |
|---|---|
| HTTP client | Consumer of the host-scanner HTTP API |
| Operator | User deploying and running host-scanner in Kubernetes |
| Test engineer | User executing end-to-end and unit tests |
| Integrator | User supplying runtime or configuration inputs to host-scanner logic |

### Operating environment
The system operates in the following environment:
- Kubernetes-based deployment environment
- Privileged DaemonSet deployment model
- HTTP service reachable by clients and end-to-end tests
- Go-based implementation and test environment
- Linux-style host and runtime filesystem paths, including paths under `/etc`, `/run`, and `/var/lib`
- Container runtime and node-agent contexts such as kubelet, containerd, and CRI-O scenarios

### Assumptions and dependencies
- The system depends on access to Kubernetes node host information.
- HTTP-based interactions depend on a running host-scanner service instance.
- CNI directory resolution depends on runtime type, default configuration, configuration-file content, and command-line arguments.
- Provider-specific end-to-end tests depend on Go build tags.
- Secret removal operates on JSON-formatted control-plane data.

## 3. External Interface Requirements

### User interfaces
No graphical user interface is required by this specification.

### Software interfaces
| Interface | Requirement |
|---|---|
| HTTP API | The system shall expose HTTP endpoints accessible through standard HTTP requests. |
| Runtime and process configuration input | The system shall accept runtime-specific configuration data, configuration-file content, and command-line arguments used to derive the CNI configuration directory. |
| JSON processing interface | The system shall accept control-plane JSON input and produce sanitized JSON output. |
| Provider-specific test interface | The end-to-end test suite shall support provider-specific expected data selection through Go build tags using `//go:build <provider>` declarations. |

### Communication interfaces
| Interface | Requirement |
|---|---|
| HTTP | The system shall support HTTP request/response communication for endpoint access and status-code-based responses. |

### Data exchange formats
| Format | Usage |
|---|---|
| HTTP request/response | Endpoint invocation and response delivery |
| JSON | Input and output format for control-plane data sanitization |
| Command-line argument strings | Input for runtime-related path resolution |
| Configuration-file content | Input for CNI configuration directory resolution |

## 4. Functional Requirements

| ID | Description | Trigger/Input | System behavior | Output | Priority | Verification |
|---|---|---|---|---|---|---|
| FR-001 | Unknown endpoint handling | HTTP `GET` request to `/doesnotexist` | The system shall respond with HTTP status code `404`. | HTTP response with status `404` | High | Test |
| FR-002 | CNI configuration directory resolution | Runtime type, default configuration, configuration-file content, and command-line arguments | The system shall resolve the CNI configuration directory based on runtime type, default configuration, configuration-file content, and command-line CNI directory arguments. Verified scenarios include: kubelet/containerd default input resolves to `/etc/cni/`; explicit CNI directory argument scenarios resolve to `/var/lib/cni/`; configuration-file parsing scenarios may also return more specific CNI subpaths. | Resolved CNI configuration directory path | High | Test |
| FR-003 | Removal of encryption provider configuration secrets | Control-plane JSON data containing encryption provider configuration content | The system shall remove encryption provider configuration secrets before producing output. | Sanitized JSON data with secrets removed | High | Test |

## 5. Non-Functional Requirements

| ID | Quality attribute | Requirement | Priority | Verification |
|---|---|---|---|---|
| NFR-001 | Security | The system shall not expose encryption provider configuration secrets in processed JSON output. | High | Test |
| NFR-002 | Maintainability and portability | End-to-end tests shall select provider-specific expected data structures through Go build tags. Platform-specific test files shall use the `//go:build <provider>` form to declare tags. | Medium | Inspection |
| NFR-003 | Compatibility | The HTTP API shall use standard HTTP request/response semantics, including status-code-based reporting for unknown paths. | Medium | Test |

## 6. Data Requirements

| ID | Data item | Requirement |
|---|---|---|
| DR-001 | HTTP request | The system shall accept HTTP GET requests to service endpoints, including unknown paths such as `/doesnotexist`. |
| DR-002 | HTTP response | The system shall return HTTP responses containing status codes that reflect endpoint outcomes. |
| DR-003 | Runtime and process configuration data | The system shall consume runtime-specific configuration data, configuration-file content, and command-line arguments to determine the CNI configuration directory. |
| DR-004 | CNI configuration directory path | The system shall produce a resolved CNI configuration directory path based on the supplied runtime inputs. Verified results include `/etc/cni/`, `/var/lib/cni/`, and configuration-derived CNI subpaths for corresponding scenarios. |
| DR-005 | Control-plane JSON data | The system shall accept JSON-formatted control-plane data for sanitization. |
| DR-006 | Sanitized JSON output | The system shall output JSON data with encryption provider configuration secrets removed. |
| DR-007 | Provider-specific test declarations | Provider-specific end-to-end test files shall declare Go build tags using the `//go:build <provider>` form. |

## 7. System Constraints

| ID | Constraint |
|---|---|
| C-001 | Provider-specific end-to-end test selection is constrained to Go build-tag mechanisms using `//go:build <provider>` declarations. |
| C-002 | CNI configuration directory resolution is constrained by the available runtime type, configuration-file content, defaults, and command-line arguments. |
| C-003 | HTTP behavior verification is constrained to externally observable HTTP request/response interactions. |
| C-004 | The product is intended for Kubernetes node-host data collection and privileged DaemonSet deployment scenarios. |

## 8. Verification and Acceptance Criteria

| Requirement ID | Verification method | Acceptance criterion |
|---|---|---|
| FR-001 | Test | A `GET` request to `/doesnotexist` returns HTTP `404`. |
| FR-002 | Test | For each supplied runtime scenario, the resolved CNI configuration directory matches the expected result for that scenario, including `/etc/cni/` for kubelet/containerd default input, `/var/lib/cni/` for explicit CNI directory argument scenarios, and configuration-derived subpaths where applicable. |
| FR-003 | Test | Given input JSON containing encryption provider configuration secrets, the produced JSON excludes those secrets and matches the expected sanitized structure. |
| NFR-001 | Test | Sanitized JSON output does not contain encryption provider configuration secrets. |
| NFR-002 | Inspection | Provider-specific end-to-end test files declare Go build tags using the `//go:build <provider>` form, and provider-specific expected data structures are separated accordingly. |
| NFR-003 | Test | HTTP interactions use standard request/response semantics and unknown paths are reported through appropriate HTTP status codes, including `404` for `/doesnotexist`. |
| DR-003 | Test | Runtime-specific configuration data, configuration-file content, and command-line arguments are accepted and used in CNI directory resolution. |
| DR-004 | Test | The resolved CNI configuration directory path matches the expected path for each tested runtime scenario. |
| DR-006 | Test | Output JSON retains the expected structure while excluding encryption provider configuration secrets. |
