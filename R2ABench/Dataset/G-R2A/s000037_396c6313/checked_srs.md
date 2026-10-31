# Software Requirements Specification

## 1. Introduction

### 1.1 Purpose

This Software Requirements Specification defines the checked requirements for `veinmind-tools`, a container security tool suite based on `veinmind-sdk` / `libveinmind`. The document is intended as a clean SRS input for subsequent architecture view generation.

### 1.2 Product Scope

The product shall provide container security scanning capabilities for local images, running containers, and IaC files. It shall also provide plugin packaging examples, a runner-oriented execution workflow, Docker authorization action classification, and structured scan report data.

This SRS focuses on the requirements listed below. Other tools in the broader suite are outside this SRS unless explicitly listed.

### 1.3 Intended Audience

| User class | Responsibilities and expectations |
|---|---|
| Security operator | Runs local image, container, and IaC scans and reads scan results. |
| Plugin developer | Builds or packages scanning plugins using the SDK and example projects. |
| Deployment operator | Prepares Docker, runner image, startup scripts, and containerized execution environments. |
| Integrator | Integrates Docker authorization routing and scan result handling into a larger security workflow. |

### 1.4 Definitions

| Term | Definition |
|---|---|
| `veinmind-tools` | Container security tool suite covered by this SRS. |
| `veinmind-sdk` / `libveinmind` | SDK/library family used by the tools and plugin examples. |
| `veinmind-runner` | Runner image and execution support used by the quick-start workflow and parallel-container execution mode. |
| IaC | Infrastructure as Code files scanned for policy or configuration risks. |
| Docker plugin action | Classified action returned by Docker authorization routing based on request method and URI. |
| `NoneDockerPlugin` | Fallback Docker plugin action returned when no route matches an authorization request. |

## 2. Overall Description

### 2.1 Product Perspective

`veinmind-tools` is a command-line and plugin-oriented tool suite for container security scanning. It depends on Docker for the quick-start workflow, uses `veinmind-runner` for runner-based execution, and supports scanning logic implemented through SDK-backed tool commands.

The SRS states required behavior and quality constraints only. It does not prescribe a complete architecture topology; later architecture generation should derive structure from the requirements in this document.

### 2.2 Product Functions

The product shall support the following primary functions:

| Function area | Summary |
|---|---|
| Image scanning | Provide image-oriented scanning through CLI and quick-start workflows. |
| Container scanning | Provide container-oriented scanning through CLI workflows. |
| IaC scanning | Load policy libraries, scan IaC input, and produce structured alert details. |
| Runner execution | Support documented tools running through parallel-container startup scripts. |
| Authorization routing | Classify Docker authorization requests into plugin actions by method and URI. |
| Plugin packaging | Provide container packaging behavior for a Python tool example. |
| Reporting data | Represent malicious-file and IaC findings through structured report objects. |

### 2.3 Operating Environment

| Environment aspect | Requirement |
|---|---|
| Container runtime | Docker shall be available for quick-start execution. |
| Runner image | The runner image shall be available before quick-start scanning commands are executed. |
| Startup script | The parallel-container startup script shall be available before the quick-start local image scan is executed. |
| Example Python runtime | The Python example shall run in a container image based on `veinmind/python3.6:1.3.1-stretch`. |

### 2.4 Assumptions and Dependencies

| ID | Assumption or dependency |
|---|---|
| DEP-001 | Security operators have permission to invoke Docker commands and access local images or containers targeted for scanning. |
| DEP-002 | The runner image and startup script are prepared before quick-start scanning workflows are used. |
| DEP-003 | Plugin examples are executed in an environment where SDK/library dependencies are available. |
| DEP-004 | IaC scanning input is supplied in a format accepted by the IaC scanning command. |

## 3. External Interface Requirements

### 3.1 Command-Line Interfaces

| ID | Interface | Requirement |
|---|---|---|
| CLI-001 | `scan-image` | The product shall expose a command named `scan-image` for image-oriented scanning. |
| CLI-002 | `scan-container` | The product shall expose a command named `scan-container` for container-oriented scanning. |
| CLI-003 | `scan-iac` | The product shall expose or map an IaC scan command for scanning IaC input. |
| CLI-004 | `./run.sh scan-host image` | The quick-start workflow shall support starting local image scanning through the documented parallel-container startup command. |

### 3.2 Software Interfaces

| ID | Interface | Requirement |
|---|---|---|
| API-001 | `veinmind-sdk` / `libveinmind` | Tool and plugin implementations shall use the SDK/library family for scan command integration. |
| API-002 | Docker authorization request | The authorization routing component shall consume request method and request URI values. |
| API-003 | Report event client | The IaC scanning tool shall publish structured alert details through the report event mechanism. |

### 3.3 Data Exchange Formats

| ID | Data exchange object | Requirement |
|---|---|---|
| DAT-IF-001 | Malicious-file report data | The product shall represent malicious-file scan summaries, per-image results, per-layer results, and file findings. |
| DAT-IF-002 | IaC alert details | The product shall represent IaC rule metadata and file-location details for detected risks. |
| DAT-IF-003 | Docker plugin action result | The authorization routing component shall return a Docker plugin action value, including a fallback action when no route matches. |

## 4. Functional Requirements

| ID | Requirement | Trigger / input | Required behavior | Output | Priority | Verification |
|---|---|---|---|---|---|---|
| FR-001 | The product shall provide a CLI command named `scan-image` for image scanning. | A user invokes `scan-image` with valid image scan context. | The command shall run image-oriented scan logic against the provided image handle or image scan context. | Command completion status and any generated scan results. | High | Demonstration |
| FR-002 | The product shall provide a CLI command named `scan-container` for container scanning. | A user invokes `scan-container` with valid container scan context. | The command shall run container-oriented scan logic against the provided container handle or container scan context. | Command completion status and any generated scan results. | High | Demonstration |
| FR-003 | The product shall support initiating local image scanning in the quick-start workflow through the parallel-container startup script. | After Docker, the runner image, and the startup script are prepared, a user executes `./run.sh scan-host image`. | The product shall enter the local image scanning flow through the startup script. | Local image scanning workflow starts and reports completion or failure. | High | Demonstration |
| FR-004 | The Docker authorization routing component shall determine the Docker plugin action by matching request method and request URI against configured route patterns. | An authorization request containing method and URI is received. | The component shall evaluate configured route patterns and select the first route whose method and URI pattern match the request. | Matching Docker plugin action. | High | Test |
| FR-005 | The Docker authorization routing component shall return `NoneDockerPlugin` when no configured route matches the request method and URI. | An authorization request does not match any configured route pattern for the request method and URI. | The component shall return the fallback action. | `NoneDockerPlugin`. | High | Test |
| FR-006 | The Python example package shall forward container entrypoint arguments to `python scan.py`. | The example container starts with user-supplied arguments. | The entrypoint shall invoke `python scan.py $*`. | Python scan process starts with forwarded arguments. | Medium | Demonstration |
| FR-007 | The IaC scanning tool shall load policy libraries, scan IaC input, and produce structured alert details for detected risks. | A user invokes the IaC scan command with valid IaC input. | The tool shall load policy libraries, run the scanner, merge duplicated result groups, build alert details with rule metadata and file-location fields, and publish a report event. | IaC alert details and command completion status. | High | Test |

## 5. Non-Functional Requirements

| ID | Quality attribute | Requirement | Fit criterion | Priority | Verification |
|---|---|---|---|---|---|
| NFR-001 | Scalability / execution model | Documented tools shall support running in container mode through the corresponding parallel-container startup scripts. | At least two documented tools can be started through their respective parallel-container startup scripts and enter corresponding scanning flows in independent container environments. | High | Demonstration |
| NFR-002 | Compatibility | The product shall explicitly support compatibility with the listed cloud-native infrastructure objects. | Compatibility coverage includes image-registry objects DockerHub, Docker Registry, and Harbor, and container-runtime objects Docker and Containerd. | Medium | Inspection |
| NFR-003 | Portability | The Python example package shall be runnable in a container environment based on `veinmind/python3.6:1.3.1-stretch`. | The example container build uses that base image, installs Python dependencies, and starts the scan entrypoint. | Medium | Inspection |
| NFR-004 | Modifiability | Plugin examples shall support SDK-backed scanner implementation and command mapping. | A developer can add scan logic behind mapped scan commands without changing the runner workflow contract. | Medium | Inspection |
| NFR-005 | Verifiability | Each requirement in this SRS shall have a verification method and observable acceptance condition. | Requirements can be checked through demonstration, test, inspection, or analysis without relying on hidden review notes. | Medium | Inspection |

## 6. Data Requirements

### 6.1 Malicious-File Report Data

| ID | Data object | Required fields |
|---|---|---|
| DR-001 | `MaliciousFileInfo` | `Engine`, `ImageID`, `LayerID`, `RelativePath`, `FileName`, `FileSize`, `FileMd5`, `FileSha256`, `FileCreated`, `Description`. |
| DR-002 | `ReportData` | `ScanImageCount`, `MaliciousFileCount`, `ScanSpendTime`, `ScanStartTime`, `ScanFileCount`, `ScanImageResult`. |
| DR-003 | `ReportImage` | `ImageName`, `ImageID`, `MaliciousFileCount`, `ScanFileCount`, `ImageCreatedAt`, `MaliciousFileInfos`, `Layers`. |
| DR-004 | `ReportLayer` | `ImageID`, `LayerID`, `MaliciousFileInfos`. |

### 6.2 IaC Report Data

| ID | Data object | Required fields |
|---|---|---|
| DR-005 | IaC rule metadata | `Id`, `Name`, `Description`, `Reference`, `Severity`, `Solution`, `Type`. |
| DR-006 | IaC file-location detail | `StartLine`, `EndLine`, `FilePath`, `Original`. |
| DR-007 | IaC alert detail | Rule metadata and file-location detail associated with each detected IaC risk. |

### 6.3 Data Handling Constraints

| ID | Requirement |
|---|---|
| DR-008 | Scan report data shall preserve the relationship between images, layers, and malicious-file findings. |
| DR-009 | IaC alert data shall preserve the relationship between a detected risk, its rule metadata, and its file-location details. |
| DR-010 | This SRS does not define retention, privacy, backup, or migration behavior for scan report data. |

## 7. Technical and Operational Constraints

| ID | Constraint |
|---|---|
| CON-001 | Docker shall be installed and operational before quick-start scanning workflows are used. |
| CON-002 | The runner image shall be installed before runner-based scanning workflows are used. |
| CON-003 | The parallel-container startup script shall be available before quick-start local image scanning is initiated. |
| CON-004 | Tool and plugin implementations shall use the `veinmind-sdk` / `libveinmind` integration model. |
| CON-005 | The Python example shall install dependencies from `requirements.txt` during container build. |
| CON-006 | The Python example shall use `/tool/entrypoint.sh` as the container entrypoint. |

## 8. Verification and Acceptance

| Requirement ID | Verification | Acceptance criterion |
|---|---|---|
| FR-001 | Demonstration | Invoking `scan-image` reaches image-oriented scan logic and returns a completion or error status. |
| FR-002 | Demonstration | Invoking `scan-container` reaches container-oriented scan logic and returns a completion or error status. |
| FR-003 | Demonstration | Executing `./run.sh scan-host image` after setup starts the local image scanning flow. |
| FR-004 | Test | A request with method and URI matching a configured route returns the expected Docker plugin action. |
| FR-005 | Test | A request with no matching route returns `NoneDockerPlugin`. |
| FR-006 | Demonstration | Starting the Python example container invokes `python scan.py` with supplied arguments. |
| FR-007 | Test | A valid IaC input causes policy libraries to load, scanner execution to run, alert details to be built, and a report event to be published. |
| NFR-001 | Demonstration | At least two documented tools can be started through their respective parallel-container startup scripts and enter corresponding scanning flows in independent container environments. |
| NFR-002 | Inspection | Compatibility coverage lists DockerHub, Docker Registry, Harbor, Docker, and Containerd. |
| NFR-003 | Inspection | The Python example container uses `veinmind/python3.6:1.3.1-stretch`, installs dependencies, and starts the configured entrypoint. |
| NFR-004 | Inspection | Plugin examples expose SDK-backed scan command mapping and leave scan logic replaceable by plugin developers. |
| NFR-005 | Inspection | Each requirement row contains a verification method and acceptance condition. |
