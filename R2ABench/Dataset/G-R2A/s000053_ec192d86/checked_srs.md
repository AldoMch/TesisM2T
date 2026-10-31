# Software Requirements Specification

## 1. Introduction

### Purpose
This SRS defines the checked software requirements for the `openshift/configuration-anomaly-detection` product based on repository-supported behavior and reviewed corrections. It is intended to capture externally observable capabilities and constraints suitable for downstream architecture generation.

### Product scope
Configuration Anomaly Detection (CAD) is an operational tool intended to reduce manual SRE investigation by detecting cluster anomalies, executing investigation and disposition workflows, and sending relevant communications to cluster owners or related operations systems. The repository includes:
- A CLI tool, `cadctl`, for CAD workflows
- Integration code used by the CLI
- Deployment assets for Tekton-based execution
- A skip-webhook execution path that creates a `PipelineRun` directly
- Template update utility assets

### Intended audience
This document is intended for:
- SRE and operations users running CAD workflows
- Deployment engineers operating Tekton-based execution paths
- Developers extending CLI endpoints, integrations, and deployment assets
- Architects deriving component and interface views from repository-supported behavior

## 2. Overall Description

### Product perspective
CAD is a CLI-centered operational system with supporting integration libraries and Tekton-based deployment and execution assets. Its normal event-driven path is triggered by an external alert webhook to a Tekton EventListener; a Trigger creates a `PipelineRun` that executes CAD checks. The repository also provides an alternative skip-webhook path in which a `PipelineRun` can be created directly without using the event listener.

### Product functions summary
The system supports the following functions:
- Provide a CLI named `cadctl` for CAD workflows
- Perform the workflow for "cluster has gone missing" (CHGM) alerts
- Detect cluster anomalies and send relevant communications
- Execute mitigation or disposition actions when investigation results require them, including support-status handling, alert silencing or escalation, and follow-up event handling
- Support integrations for PagerDuty, AWS, and OCM
- Support event-driven Tekton execution through an EventListener and Trigger
- Allow direct creation of a Tekton `PipelineRun` through the skip-webhook path
- Update deployment template artifacts through the template update utility

### User classes
| User class | Description |
|---|---|
| SRE / operations user | Runs CAD workflows to investigate and handle cluster anomalies and CHGM alerts. |
| Deployment engineer | Operates Tekton-based execution paths, including standard event-driven triggering and direct skip-webhook execution. |
| Developer / contributor | Extends CLI commands, integrations, and deployment/template assets. |

### Operating environment
| Aspect | Description |
|---|---|
| Runtime form | Containerized CLI runtime containing `/bin/cadctl` |
| Build environment | Container build using a Go 1.17 builder image |
| Runtime base image | UBI minimal-based runtime image |
| Pipeline environment | Tekton `PipelineRun` resources in the CAD deployment namespace |
| Trigger environment | Tekton EventListener and Trigger for webhook-driven execution |

### Assumptions and dependencies
- CAD depends on external systems and integrations including PagerDuty, AWS, and OCM.
- Tekton-based execution depends on deployment of the referenced pipeline and trigger resources.
- Direct execution depends on submission of a valid `PipelineRun` manifest.
- Template update behavior depends on repository-maintained template assets.

## 3. External Interface Requirements

### User interfaces
| Interface | Requirement summary |
|---|---|
| CLI | The system shall provide `cadctl` as the documented user-facing CLI for CAD workflows. |
| Operations execution path | The system shall support both standard webhook-triggered execution and direct skip-webhook pipeline execution. |
| Maintenance utility | The system shall provide a documented template update utility for deployment artifacts. |

### Software and API interfaces
| Interface | Requirement summary |
|---|---|
| Integration library | The system shall provide package-level integration code used by the CLI. |
| Named integrations | The system shall support integrations for PagerDuty, AWS, and OCM. |
| Tekton pipeline interface | The system shall integrate with Tekton `EventListener`, `Trigger`, and `PipelineRun` resources for execution orchestration. |
| Pipeline reference | In the repository's documented default/example direct-execution path, the `PipelineRun` references a pipeline named `cad-checks-pipeline` and uses the `configuration-anomaly-detection` namespace. |

### Communication interfaces
| Interface | Requirement summary |
|---|---|
| Alert webhook input | The system shall support receiving external alert webhooks through a Tekton EventListener. |
| Triggered pipeline execution | The system shall trigger Tekton pipeline execution from the event-listener path. |
| Direct pipeline invocation | The system shall support a skip-webhook path that bypasses the event listener and creates a `PipelineRun` directly. |

### Data exchange formats
| Format/item | Requirement summary |
|---|---|
| JSON payload | The direct `PipelineRun` execution path shall accept a `payload` parameter encoded as JSON. |
| Alert identifier | The JSON payload shall support an `event.data.id` field. |
| YAML manifests | Deployment and direct-execution assets shall be represented as YAML manifests. |

## 4. Functional Requirements

| ID | Description | Trigger/Input | System behavior | Output | Priority | Verification |
|---|---|---|---|---|---|---|
| FR-001 | CLI availability | User invokes CAD tooling | The system shall provide a CLI named `cadctl` as the CAD executable entry point. | Executable CLI available to the user | High | Inspection |
| FR-002 | CHGM workflow execution | A CHGM workflow is initiated | The system shall perform the workflow for "cluster has gone missing" alerts through `cadctl`. | CHGM workflow processing is executed | High | Demonstration |
| FR-003 | Anomaly detection and communication | A cluster anomaly is processed | The system shall detect cluster anomalies and send relevant communications to the cluster owner or related operations systems. | Investigation outcome and relevant communication are produced | High | Demonstration |
| FR-004 | Mitigation and disposition handling | Investigation results require follow-up action | The system shall execute mitigation or disposition actions when investigation results require them, including updating support status, silencing or escalating alerts, and recording follow-up handling information in related operations systems. | Required mitigation or disposition actions are executed | High | Inspection |
| FR-005 | Standard event-driven execution | An external alert webhook is received | The system shall support receiving alert webhooks through an event listener and triggering a Tekton `PipelineRun` to execute CAD checks. | Pipeline execution is initiated from the normal trigger path | High | Inspection |
| FR-006 | Direct skip-webhook execution | User follows the skip-webhook path | The system shall support a direct execution path that bypasses the event listener and creates a Tekton `PipelineRun` directly. | A `PipelineRun` resource is created directly | Medium | Demonstration |
| FR-007 | Default/example Tekton target values | A direct-execution manifest is submitted using the documented repository path | In the repository's documented default/example Tekton direct-execution path, the system shall reference a pipeline named `cad-checks-pipeline` and use the `configuration-anomaly-detection` namespace. | Tekton execution request targets the documented pipeline and namespace | Medium | Inspection |
| FR-008 | Direct execution payload | A direct `PipelineRun` is created | The system shall accept a `payload` parameter encoded as JSON and carrying `event.data.id`. | JSON payload is available to pipeline execution | Medium | Inspection |
| FR-009 | Integration support | CLI workflows require external-system interaction | The system shall provide integration code used by the CLI for PagerDuty, AWS, and OCM. | Integration-capable CLI behavior is available for the named systems | Medium | Inspection |
| FR-010 | Template update workflow | User runs the template update utility | The system shall provide a workflow that updates repository deployment template artifacts. | Updated template artifact is produced | Low | Demonstration |

## 5. Non-Functional Requirements

| ID | Quality attribute | Requirement | Priority | Verification |
|---|---|---|---|---|
| NFR-001 | Portability | The CLI runtime artifact shall be packaged as a container image based on a UBI minimal runtime image and shall include `/bin/cadctl`. | Medium | Inspection |
| NFR-002 | Build compatibility | The documented container build for the CLI shall use a Go 1.17 builder image. | Medium | Inspection |
| NFR-003 | Build metadata | The container image shall expose standard image labels for vendor, name, description, display name, version, build date, VCS reference, and Dockerfile path. | Low | Inspection |
| NFR-004 | Maintainability | Integration logic intended for CLI use shall be organized in a package library so CLI endpoints can call required integration code. | Low | Inspection |

## 6. Data Requirements

| ID | Data item/entity | Requirement |
|---|---|---|
| DR-001 | `payload` | The direct execution path shall accept a `payload` parameter as JSON text. |
| DR-002 | `event.data.id` | The JSON payload shall support an identifier field at `event.data.id`. |
| DR-003 | `PipelineRun` | Direct execution shall use a Tekton `PipelineRun` resource as the invocation object. |
| DR-004 | Deployment template artifact | The template update workflow shall update the repository deployment template artifact. |
| DR-005 | Alert webhook payload | The normal event-driven path shall accept alert input suitable for EventListener-triggered pipeline execution. |

## 7. System Constraints

| ID | Constraint |
|---|---|
| C-001 | The runtime delivery form is constrained to a container image containing `/bin/cadctl`. |
| C-002 | The documented build process is constrained to a Go 1.17 builder image. |
| C-003 | The documented runtime base image is constrained to a UBI minimal runtime image. |
| C-004 | Direct Tekton execution is constrained to Tekton `v1beta1` `PipelineRun` manifests as documented in repository deployment assets. |
| C-005 | In the repository's documented default/example direct-execution path, the `PipelineRun` references `cad-checks-pipeline` in the `configuration-anomaly-detection` namespace. |
| C-006 | The skip-webhook execution path is constrained to bypass the event listener rather than use the normal trigger flow. |

## 8. Verification and Acceptance Criteria

| Requirement ID | Verification method | Acceptance criterion |
|---|---|---|
| FR-001 | Inspection | Repository build and runtime artifacts show `cadctl` as the CLI binary and entry point. |
| FR-002 | Demonstration | The repository-supported CLI workflow executes CHGM handling behavior. |
| FR-003 | Demonstration | The repository-supported workflow produces anomaly-handling behavior and relevant communications. |
| FR-004 | Inspection | Repository artifacts show mitigation or disposition behavior such as support-status handling, alert silencing or escalation, or follow-up event recording. |
| FR-005 | Inspection | Deployment artifacts show a normal webhook-to-EventListener-to-Trigger-to-`PipelineRun` execution path for CAD checks. |
| FR-006 | Demonstration | Direct pipeline execution can be performed without using the event-listener path. |
| FR-007 | Inspection | The documented direct-execution manifest targets `cad-checks-pipeline` in `configuration-anomaly-detection`. |
| FR-008 | Inspection | The direct-execution manifest contains a JSON `payload` parameter with `event.data.id`. |
| FR-009 | Inspection | The repository exposes integration code for PagerDuty, AWS, and OCM for CLI use. |
| FR-010 | Demonstration | Running the template update workflow updates the repository deployment template artifact. |
| NFR-001 | Inspection | Container definition uses the documented runtime base image and includes `/bin/cadctl`. |
| NFR-002 | Inspection | Container definition uses the documented Go 1.17 builder image. |
| NFR-003 | Inspection | Container definition includes the documented image labels. |
| NFR-004 | Inspection | Repository structure shows CLI-used integrations organized in a package library. |
| DR-001 | Inspection | Direct execution input includes `payload` as JSON text. |
| DR-002 | Inspection | The JSON payload structure includes `event.data.id`. |
| DR-003 | Inspection | Direct execution input is represented as a Tekton `PipelineRun` manifest. |
| DR-004 | Demonstration | Template update execution produces an updated deployment template artifact. |
| DR-005 | Inspection | Deployment assets show alert input feeding the EventListener-based execution path. |
