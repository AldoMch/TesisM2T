# Software Requirements Specification

## 1. Introduction

### Purpose
This SRS defines evidence-backed requirements for the `openshift/configuration-anomaly-detection` repository at commit `01e82afac8f664079b11a2e96569c55a7615ed2e`. It covers the observable behavior and deployment expectations supported by the repository evidence.

### Product scope
Configuration Anomaly Detection (CAD) is described as responsible for reducing manual SRE investigation by detecting cluster anomalies and sending relevant communications to the cluster owner. The repository includes a CLI, `cadctl`, that performs the workflow for "cluster has gone missing" (CHGM) alerts, integration code used by the CLI, and deployment assets including a Tekton `PipelineRun` path that can bypass an event listener. `cadctl` is also described as a CLI tool to detect and mitigate configuration mishaps. Source evidence: `E003`, `E004`, `E005`, `E006`.

### Intended audience
This document is intended for:
- SRE or operations users running CAD workflows through `cadctl` or pipeline assets. Source evidence: `E004`, `E006`.
- Contributors extending CLI endpoints or integrations. Source evidence: `E003`.
- Release and deployment engineers building the containerized CLI artifact. Source evidence: `E005`.

### References
- Repository: `openshift/configuration-anomaly-detection`
- Repository URL: <https://github.com/openshift/configuration-anomaly-detection>
- Snapshot URL: <https://github.com/openshift/configuration-anomaly-detection/tree/01e82afac8f664079b11a2e96569c55a7615ed2e>
- Primary evidence sources: `README.md`, `pkg/README.md`, `Dockerfile`, `deploy/skip-webhook/README.md`, `deploy/skip-webhook/pipeline-run.yaml`, `hack/update-template/README.md`

## 2. Overall Description

### Product perspective
CAD is a CLI-centered operational tool with supporting integration code and deployment assets. The package library holds integrations and code used by the CLI tool. The repository also provides a Tekton-based execution path in which a `PipelineRun` can be created directly instead of using an event listener. Source evidence: `E001`, `E003`, `E006`.

### Product functions summary
- Detect cluster anomalies and send relevant communications to the cluster owner. Source evidence: `E004`.
- Execute the CHGM alert workflow through `cadctl`. Source evidence: `E004`.
- Support integrations identified in the repository as PagerDuty, AWS, and OCM. Source evidence: `E003`, `E004`.
- Allow direct creation of a pipeline run that skips the event listener. Source evidence: `E001`, `E006`.
- Update `configuration-anomaly-detection-template.Template.yaml` through the template update utility. Source evidence: `E002`.

### User classes
| User class | Description | Source evidence |
|---|---|---|
| SRE / operations user | Uses CAD to reduce manual investigation and run CHGM-related workflows. | `E004` |
| Deployment engineer | Runs Tekton-based execution paths, including direct `PipelineRun` creation. | `E001`, `E006` |
| Contributor / developer | Adds CLI endpoints and integration code, and updates templates. | `E002`, `E003` |

### Operating environment
| Aspect | Requirement context | Source evidence |
|---|---|---|
| Runtime form | Containerized CLI runtime containing `/bin/cadctl` | `E005` |
| Build environment | Builder image based on `registry.ci.openshift.org/openshift/release:golang-1.17` | `E005` |
| Runtime base image | `quay.io/app-sre/ubi8-ubi-minimal:8.6-854` | `E005` |
| Pipeline environment | Tekton `v1beta1` `PipelineRun` in namespace `configuration-anomaly-detection` | `E006` |

### Assumptions and dependencies
- CAD depends on external integrations named PagerDuty, AWS, and OCM. Source evidence: `E003`, `E004`.
- Direct pipeline execution depends on a Tekton pipeline named `cad-checks-pipeline`. Source evidence: `E006`.
- The template update workflow depends on a target file named `configuration-anomaly-detection-template.Template.yaml`. Source evidence: `E002`.

## 3. External Interface Requirements

### User interfaces
| Interface | Description | Source evidence |
|---|---|---|
| CLI | `cadctl` is the documented user-facing CLI and performs the CHGM workflow. | `E004` |
| Command-driven maintenance utilities | Repository utilities support running a template update command and direct pipeline execution commands. | `E001`, `E002` |

### Software/API interfaces
| Interface | Description | Source evidence |
|---|---|---|
| Internal integration library | A package library provides integrations/code used by the CLI. | `E003` |
| Named integrations | Supported integration areas explicitly named are PagerDuty, AWS, and OCM. | `E003`, `E004` |
| Tekton pipeline reference | Direct execution targets `pipelineRef.name: cad-checks-pipeline`. | `E006` |

### Communication interfaces
| Interface | Description | Source evidence |
|---|---|---|
| Event-driven pipeline invocation | A payload object is supplied to a Tekton pipeline run; the skip-webhook path bypasses the event listener and creates the pipeline run directly. | `E001`, `E006` |

### Data exchange formats
| Format | Description | Source evidence |
|---|---|---|
| JSON | The Tekton parameter `payload` is a JSON string containing `event.data.id`. | `E006` |
| YAML | Deployment assets include a Tekton `PipelineRun` manifest and a template YAML target. | `E002`, `E006` |

## 4. Functional Requirements

| ID | Description | Trigger / Input | System behavior | Output | Priority | Verification | Source evidence |
|---|---|---|---|---|---|---|---|
| FR-001 | The system shall provide a CLI named `cadctl` for CAD workflows. | User invokes `cadctl`. | The system exposes `cadctl` as the repository's CLI artifact and runtime entrypoint. | Executable CLI available to the user. | High | Inspection | `E004`, `E005` |
| FR-002 | The `cadctl` CLI shall perform the workflow for "cluster has gone missing" (CHGM) alerts. | A CHGM workflow is initiated through `cadctl`. | The system executes the CHGM workflow through the CLI. | CHGM workflow processing through `cadctl`. | High | Demonstration | `E004` |
| FR-003 | The system shall support CAD operation for detecting cluster anomalies and sending relevant communications to the cluster owner. | A cluster anomaly is processed by CAD. | The system performs anomaly-detection-related processing and issues relevant owner communications as part of CAD scope. | Relevant communication to the cluster owner. | High | Analysis | `E004` |
| FR-004 | The system shall provide a direct execution path that skips the event listener and creates a Tekton `PipelineRun` directly. | User follows the skip-webhook usage path. | The system accepts direct `PipelineRun` creation instead of requiring the event listener path. | A Tekton `PipelineRun` resource is created. | Medium | Demonstration | `E001`, `E006` |
| FR-005 | When the direct Tekton execution path is used, the system shall invoke the pipeline named `cad-checks-pipeline` in namespace `configuration-anomaly-detection`. | A direct `PipelineRun` manifest is submitted. | The system references `pipelineRef.name: cad-checks-pipeline` and runs in namespace `configuration-anomaly-detection`. | Tekton pipeline execution request targeting the named pipeline and namespace. | Medium | Inspection | `E006` |
| FR-006 | The direct Tekton execution path shall accept a `payload` parameter encoded as JSON and carrying `event.data.id`. | A `PipelineRun` is created with the `payload` parameter. | The system passes the `payload` parameter value to the pipeline run. | JSON payload available to pipeline execution. | Medium | Inspection | `E006` |
| FR-007 | The system shall provide integration code used by the CLI for PagerDuty, AWS, and OCM integration areas. | CLI workflows require supported integrations. | The system includes integration/library support for the named external systems. | Integration-capable CLI/library behavior for the named systems. | Medium | Inspection | `E003`, `E004` |
| FR-008 | The system shall provide a template update workflow that updates `configuration-anomaly-detection-template.Template.yaml`. | User runs the documented update-template utility. | The system updates the target template file. | Updated `configuration-anomaly-detection-template.Template.yaml`. | Low | Demonstration | `E002` |

## 5. Non-Functional Requirements

| ID | Quality attribute | Requirement | Priority | Verification | Source evidence |
|---|---|---|---|---|---|
| NFR-001 | Portability | The CLI runtime artifact shall be packaged as a container image based on `quay.io/app-sre/ubi8-ubi-minimal:8.6-854` and shall include `/bin/cadctl`. | Medium | Inspection | `E005` |
| NFR-002 | Build compatibility | The documented container build for the CLI shall use the builder image `registry.ci.openshift.org/openshift/release:golang-1.17`. | Medium | Inspection | `E005` |
| NFR-003 | Build metadata traceability | The container image shall expose image labels for vendor, name, description, display-name, version, build-date, VCS reference, and Dockerfile path. | Low | Inspection | `E005` |
| NFR-004 | Maintainability | Integration logic intended for CLI use shall be organized in a package library so new CLI endpoints can call required integration code. This requirement is inferred from the documented extension workflow. | Low | Analysis | `E003` |

## 6. Data Requirements

### Data entities / objects
| ID | Data entity | Description | Source evidence |
|---|---|---|---|
| DR-001 | `payload` | JSON string parameter passed to a Tekton `PipelineRun`. | `E006` |
| DR-002 | `event.data.id` | Identifier nested inside the `payload` JSON object. Example value shown as `incidentid`. | `E006` |
| DR-003 | `PipelineRun` | Tekton resource used for direct execution of CAD checks. | `E006` |
| DR-004 | `configuration-anomaly-detection-template.Template.yaml` | Template file updated by the template update workflow. | `E002` |

### Input / output data
| Requirement ID | Requirement | Verification | Source evidence |
|---|---|---|---|
| DR-REQ-001 | The direct execution path shall accept input as a Tekton `PipelineRun` manifest in YAML format. | Inspection | `E006` |
| DR-REQ-002 | The direct execution path shall accept a `payload` parameter whose value is JSON text. | Inspection | `E006` |
| DR-REQ-003 | The template update workflow shall output an updated `configuration-anomaly-detection-template.Template.yaml` file. | Demonstration | `E002` |

### Storage, privacy, integrity, retention, migration
No supported requirements were found in the evidence pack.

## 7. Constraints

| ID | Constraint | Source evidence |
|---|---|---|
| C-001 | The runtime delivery form is constrained to a container image containing `/bin/cadctl`. | `E005` |
| C-002 | The documented build process is constrained to the Go 1.17 builder image `registry.ci.openshift.org/openshift/release:golang-1.17`. | `E005` |
| C-003 | The documented runtime base image is constrained to `quay.io/app-sre/ubi8-ubi-minimal:8.6-854`. | `E005` |
| C-004 | Direct execution is constrained to Tekton `apiVersion: tekton.dev/v1beta1`. | `E006` |
| C-005 | The direct `PipelineRun` example is constrained to namespace `configuration-anomaly-detection` and pipeline name `cad-checks-pipeline`. | `E006` |
| C-006 | The skip-webhook execution path is explicitly defined as bypassing the event listener. | `E001` |

## 8. Verification and Acceptance

| Requirement ID | Verification method | Acceptance basis |
|---|---|---|
| FR-001 | Inspection | Container/runtime artifact and repository documentation show `cadctl` as the CLI and runtime binary. |
| FR-002 | Demonstration | A CHGM workflow can be initiated through `cadctl` per documented purpose. |
| FR-003 | Analysis | Repository documentation states CAD scope includes anomaly detection and communication to the cluster owner. |
| FR-004 | Demonstration | Direct pipeline execution can be performed without the event listener path. |
| FR-005 | Inspection | The submitted `PipelineRun` manifest targets `cad-checks-pipeline` in `configuration-anomaly-detection`. |
| FR-006 | Inspection | The `PipelineRun` manifest contains the JSON `payload` parameter with `event.data.id`. |
| FR-007 | Inspection | The repository exposes CLI-used integration areas for PagerDuty, AWS, and OCM. |
| FR-008 | Demonstration | Running the update-template workflow updates `configuration-anomaly-detection-template.Template.yaml`. |
| NFR-001 | Inspection | Container definition uses the specified runtime base image and copies `/bin/cadctl`. |
| NFR-002 | Inspection | Container definition uses the specified Go 1.17 builder image. |
| NFR-003 | Inspection | Container definition includes the documented labels. |
| NFR-004 | Analysis | Documented extension workflow shows CLI endpoint additions calling package-library integration code. |
| DR-REQ-001 | Inspection | Direct execution input is represented as YAML `PipelineRun`. |
| DR-REQ-002 | Inspection | Input includes `payload` as JSON text. |
| DR-REQ-003 | Demonstration | Update-template workflow produces the updated template file. |

## 9. Traceability Matrix

| ID | Requirement | Type | Source | Evidence Type | Verification | Confidence |
|---|---|---|---|---|---|---|
| FR-001 | Provide a CLI named `cadctl` for CAD workflows. | Functional | `E004`, `E005` | explicit | Inspection | High |
| FR-002 | `cadctl` performs the CHGM workflow. | Functional | `E004` | explicit | Demonstration | High |
| FR-003 | CAD detects cluster anomalies and sends relevant communications to the cluster owner. | Functional | `E004` | explicit | Analysis | Medium |
| FR-004 | Support a skip-webhook path that creates a Tekton `PipelineRun` directly. | Functional | `E001`, `E006` | explicit | Demonstration | High |
| FR-005 | Direct execution invokes `cad-checks-pipeline` in namespace `configuration-anomaly-detection`. | Functional | `E006` | explicit | Inspection | High |
| FR-006 | Direct execution accepts JSON `payload` containing `event.data.id`. | Functional | `E006` | explicit | Inspection | High |
| FR-007 | Provide CLI-used integrations for PagerDuty, AWS, and OCM. | Functional | `E003`, `E004` | explicit | Inspection | Medium |
| FR-008 | Provide a workflow to update `configuration-anomaly-detection-template.Template.yaml`. | Functional | `E002` | explicit | Demonstration | Medium |
| NFR-001 | Package the runtime as a UBI minimal container containing `/bin/cadctl`. | Non-functional | `E005` | explicit | Inspection | High |
| NFR-002 | Use the Go 1.17 builder image for documented container builds. | Non-functional | `E005` | explicit | Inspection | High |
| NFR-003 | Expose build metadata labels in the container image. | Non-functional | `E005` | explicit | Inspection | High |
| NFR-004 | Organize CLI-used integrations in a package library to support endpoint extension. | Non-functional | `E003` | inferred | Analysis | Medium |
| DR-REQ-001 | Accept direct execution input as YAML `PipelineRun`. | Data | `E006` | explicit | Inspection | High |
| DR-REQ-002 | Accept direct execution `payload` as JSON text. | Data | `E006` | explicit | Inspection | High |
| DR-REQ-003 | Output an updated template YAML file from the update workflow. | Data | `E002` | explicit | Demonstration | Medium |
