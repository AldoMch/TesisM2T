# Software Requirements Specification

## 1. Introduction

### Purpose
This SRS defines evidence-backed requirements for the `chaitin/veinmind-tools` repository snapshot at commit `baa3a04d1e5d2e0f4b85a97611c8dfe53fb7167f`. It covers the observable behavior, interfaces, data structures, and constraints supported by the repository evidence.

### Product scope
`veinmind-tools` is described as a self-developed container security toolset based on `veinmind-sdk`. The repository includes:
- a toolset for scanning local images,
- CLI commands for image and container scanning,
- a runner/authz component that maps Docker plugin requests to actions,
- example plugin packaging,
- report-oriented data models for malicious file and IaC scan results.  
Sources: [E002], [E003], [E004], [E005], [E006], [E001]

### Intended audience
- Security operators using the toolset to scan images or containers
- Plugin developers using repository examples to build `veinmind-tool` plugins
- Integrators deploying the toolset with Docker and `veinmind-runner`  
Sources: [E002], [E003], [E001]

### References
- Repository: https://github.com/chaitin/veinmind-tools
- Snapshot: https://github.com/chaitin/veinmind-tools/tree/baa3a04d1e5d2e0f4b85a97611c8dfe53fb7167f
- Evidence sources:
  - `README.en.md` [E002]
  - `example/go/cmd/cli.go` [E003]
  - `veinmind-runner/pkg/authz/route/docker_plugin_action.go` [E004]
  - `plugins/go/veinmind-malicious/database/model/model.go` [E005]
  - `plugins/go/veinmind-iac/cmd/cli.go` [E006]
  - `example/python/Dockerfile` [E001]

## 2. Overall Description

### Product perspective
The repository provides a container security toolset built on `veinmind-sdk`, with a documented quick-start flow requiring Docker and `veinmind-runner`. It also provides example code for creating plugins and includes components for scanning and request authorization/routing.  
Sources: [E002], [E003], [E004], [E001]

### Product functions summary
- Scan images through a CLI command
- Scan containers through a CLI command
- Run tools in parallel containers
- Match Docker plugin authorization requests to actions by HTTP method and URI
- Produce/report structured scan result data for malicious files and IaC findings
- Provide example packaging for Python-based tools/plugins  
Sources: [E002], [E003], [E004], [E005], [E006], [E001]

### User classes
| User class | Description | Evidence |
|---|---|---|
| Security operator | Runs quick scans of local images and uses tool commands | [E002], [E003] |
| Plugin developer | Uses examples to create a `veinmind-tool` plugin quickly | [E002], [E001], [E003] |
| Deployment/integration operator | Installs Docker and `veinmind-runner`, uses startup script and containerized execution | [E002] |

### Operating environment
| Aspect | Supported environment | Evidence |
|---|---|---|
| Container runtime | Docker must be installed correctly | [E002] |
| Runner dependency | `veinmind-runner` image is installed as part of quick start | [E002] |
| Execution model | Tools support running in parallel containers | [E002] |
| Example Python runtime | `veinmind/python3.6:1.3.1-stretch` base image | [E001] |

### Assumptions and dependencies
- The toolset depends on Docker being available in the target environment. [E002]
- Quick-start use depends on installing the `veinmind-runner` image and obtaining the parallel container startup script. [E002]
- The project is based on `veinmind-sdk`. [E002]
- Example Python packaging depends on `pip install -r requirements.txt`. [E001]

## 3. External Interface Requirements

### User interfaces
| Interface | Description | Evidence |
|---|---|---|
| CLI `scan-image` | Command-line entry point for image scanning | [E003] |
| CLI `scan-container` | Command-line entry point for container scanning | [E003] |

### Software/API interfaces
| Interface | Description | Evidence |
|---|---|---|
| `veinmind-sdk` / `libveinmind` | Base SDK/library used by the toolset and Go CLI example | [E002], [E003] |
| `veinmind-runner` | Required runner image in quick-start workflow | [E002] |
| Docker authorization request interface | Authz logic consumes request method and request URI to determine Docker plugin action | [E004] |

### Communication interfaces
| Interface | Description | Evidence |
|---|---|---|
| Docker plugin authz routing | Requests are classified by `RequestMethod` and `RequestURI` against configured route regexes | [E004] |

### Data exchange formats
| Format/object | Description | Evidence |
|---|---|---|
| Malicious scan report objects | `ReportData`, `ReportImage`, `ReportLayer`, `MaliciousFileInfo` structured data | [E005] |
| IaC alert/report detail objects | Rule metadata and file-location details including line numbers, file path, and original content | [E006] |

## 4. Functional Requirements

| ID | Description | Trigger / Input | System behavior | Output | Priority | Verification method | Source evidence |
|---|---|---|---|---|---|---|---|
| FR-001 | The system shall provide a CLI command named `scan-image` for image scanning. | User invokes `scan-image`. | The CLI shall expose the `scan-image` command and run image-oriented scan logic against an image handle. | Command success or error status. | High | Demonstration | [E003] |
| FR-002 | The system shall provide a CLI command named `scan-container` for container scanning. | User invokes `scan-container`. | The CLI shall expose the `scan-container` command and run container-oriented scan flow. | Command success or error status. | High | Demonstration | [E003] |
| FR-003 | The system shall support scanning of local images in the quick-start workflow. | User follows quick-start steps and requests a local image scan. | The system shall allow a local image scan within the documented toolset workflow. | Local image scan execution. | High | Demonstration | [E002] |
| FR-004 | The Docker authorization/routing component shall determine the Docker plugin action by matching the incoming request method and request URI against configured route regexes. | An authorization request with `RequestMethod` and `RequestURI` is received. | The component shall return the action associated with the first matching route whose method matches the request. | Selected Docker plugin action. | Medium | Test | [E004] |
| FR-005 | The Docker authorization/routing component shall return `NoneDockerPlugin` when no configured route matches the request method and URI. | An authorization request does not match any configured route regex for the request method. | The component shall return `NoneDockerPlugin`. | `NoneDockerPlugin` action result. | Medium | Test | [E004] |
| FR-006 | The example Python tool package shall execute `python scan.py` with forwarded CLI arguments through its container entrypoint. | Container starts with user-supplied arguments. | The entrypoint shall invoke `python scan.py $*`. | Python scan process starts with forwarded arguments. | Medium | Demonstration | [E001] |

## 5. Non-Functional Requirements

| ID | Quality attribute | Requirement | Priority | Verification method | Source evidence | Evidence type |
|---|---|---|---|---|---|---|
| NFR-001 | Scalability / execution model | All tools shall support running in parallel containers. | High | Demonstration | [E002] | explicit |
| NFR-002 | Compatibility | The product shall target compatibility with cloud-native infrastructure. | Medium | Inspection | [E002] | explicit |
| NFR-003 | Portability | The example Python tool shall be runnable in a container environment based on `veinmind/python3.6:1.3.1-stretch`. | Medium | Inspection | [E001] | explicit |

## 6. Data Requirements

### Data entities or objects
| Data entity | Key fields evidenced | Purpose supported by evidence | Source |
|---|---|---|---|
| `MaliciousFileInfo` | `Engine`, `ImageID`, `LayerID`, `RelativePath`, `FileName`, `FileSize`, `FileMd5`, `FileSha256`, `FileCreated`, `Description` | Captures malicious-file findings associated with an image/layer/file | [E005] |
| `ReportData` | `ScanImageCount`, `MaliciousFileCount`, `ScanSpendTime`, `ScanStartTime`, `ScanFileCount`, `ScanImageResult` | Aggregates scan summary and per-image results | [E005] |
| `ReportImage` | `ImageName`, `ImageID`, `MaliciousFileCount`, `ScanFileCount`, `ImageCreatedAt`, `MaliciousFileInfos`, `Layers` | Holds per-image report data | [E005] |
| `ReportLayer` | `ImageID`, `LayerID` and associated malicious file info collection | Holds per-layer report data | [E005] |
| IaC rule detail | `Id`, `Name`, `Description`, `Reference`, `Severity`, `Solution`, `Type` | Represents IaC rule metadata in alerts | [E006] |
| IaC file detail | `StartLine`, `EndLine`, `FilePath`, `Original` | Represents file-location details for IaC findings | [E006] |

### Input/output data
| Direction | Data | Evidence |
|---|---|---|
| Input | CLI command invocation for `scan-image` and `scan-container` | [E003] |
| Input | Docker authorization request fields `RequestMethod` and `RequestURI` | [E004] |
| Output | Docker plugin action selection, including `NoneDockerPlugin` fallback | [E004] |
| Output | Structured malicious scan report objects | [E005] |
| Output | Structured IaC alert details with rule and file information | [E006] |

### Storage, integrity, retention, privacy, migration
Only persistence-oriented model structures are evidenced through GORM model definitions. No explicit repository evidence supports retention, privacy, migration, backup, or integrity controls beyond the presence of structured report entities.  
Sources: [E005]

## 7. Constraints

| Constraint | Description | Evidence |
|---|---|---|
| Deployment dependency | Docker must be installed correctly on the machine for quick-start use. | [E002] |
| Runner dependency | Quick-start use requires installation of the `veinmind-runner` image. | [E002] |
| Startup dependency | Quick-start use requires downloading the `veinmind-runner` parallel container startup script. | [E002] |
| Technology constraint | The toolset is based on `veinmind-sdk`. | [E002] |
| Example runtime constraint | The example Python packaging uses `veinmind/python3.6:1.3.1-stretch` and installs dependencies from `requirements.txt`. | [E001] |

## 8. Verification and Acceptance

| Requirement ID | Verification method | Acceptance criterion |
|---|---|---|
| FR-001 | Demonstration | Invoking the CLI shows and executes the `scan-image` command path. |
| FR-002 | Demonstration | Invoking the CLI shows and executes the `scan-container` command path. |
| FR-003 | Demonstration | The documented quick-start flow can be used to initiate a local image scan. |
| FR-004 | Test | For a request whose method and URI match a configured route regex, the corresponding Docker plugin action is returned. |
| FR-005 | Test | For a request with no matching route, the result is `NoneDockerPlugin`. |
| FR-006 | Demonstration | Starting the example Python container runs `python scan.py` with forwarded arguments. |
| NFR-001 | Demonstration | Tools can be run in parallel containers as documented. |
| NFR-002 | Inspection | Repository documentation explicitly states cloud-native infrastructure compatibility target. |
| NFR-003 | Inspection | The example Python runtime base image is `veinmind/python3.6:1.3.1-stretch`. |

## 9. Traceability Matrix

| ID | Requirement | Type | Source | Evidence Type | Verification | Confidence |
|---|---|---|---|---|---|---|
| FR-001 | Provide `scan-image` CLI command | Functional | [E003] | explicit | Demonstration | High |
| FR-002 | Provide `scan-container` CLI command | Functional | [E003] | explicit | Demonstration | High |
| FR-003 | Support local image scanning in quick-start workflow | Functional | [E002] | explicit | Demonstration | Medium |
| FR-004 | Match authz request method/URI to configured Docker plugin action | Functional | [E004] | explicit | Test | High |
| FR-005 | Return `NoneDockerPlugin` when no authz route matches | Functional | [E004] | explicit | Test | High |
| FR-006 | Example Python entrypoint executes `python scan.py` with forwarded args | Functional | [E001] | explicit | Demonstration | High |
| NFR-001 | Support running all tools in parallel containers | Non-functional | [E002] | explicit | Demonstration | High |
| NFR-002 | Target compatibility with cloud-native infrastructure | Non-functional | [E002] | explicit | Inspection | Medium |
| NFR-003 | Example Python tool runnable on `veinmind/python3.6:1.3.1-stretch` | Non-functional | [E001] | explicit | Inspection | High |
