# Software Requirements Specification

## 1. Introduction

### Purpose
This SRS defines software requirements for the `allegroai/clearml-agent` component, focusing on the ClearML agent runtime, its Kubernetes-oriented execution flow, worker telemetry behavior, and exposed backend service interfaces.

### Product scope
The product supports:
- running ClearML jobs through Kubernetes-related integration modes,
- installing an experiment environment inside a pod and starting and monitoring the experiment process,
- periodic worker reporting and connectivity checks,
- backend service interactions for entity creation and retrieval, and
- selected events and models service data structures.

### Intended audience
This document is intended for:
- product and requirements owners,
- maintainers of `allegroai/clearml-agent`,
- integrators deploying the agent in Kubernetes environments, and
- test and validation engineers.

### References
- Repository: `allegroai/clearml-agent`

## 2. Overall Description

### Product perspective
The repository provides an agent-oriented component that integrates with ClearML backend services and supports Kubernetes-based job execution flows. The product operates in an environment where ClearML Agent and ClearML Server collaborate; user-side code and GPU or worker machines interact with the server through the agent, while the server provides experiment management, visualization, collaboration, data tracking, and MLOps monitoring and orchestration capabilities.

Two Kubernetes-related integration flavors are described:
- a long-lasting service pod mode, and
- a Kubernetes Glue mode that converts queued jobs into Kubernetes jobs using a YAML template.

### Product functions summary
The product provides:
- execution as a long-lasting service pod using the `clearml-agent` Docker image,
- sibling Docker container management through a mapped Docker socket in service-pod mode,
- retrieval of jobs from a ClearML execution queue and preparation of Kubernetes jobs from a provided YAML template,
- installation of the experiment environment inside the pod and starting and monitoring the experiment process,
- periodic worker status reporting,
- periodic server connectivity pinging,
- default enablement of stdout and stderr logging, and
- backend client actions for create, get, get_by_id, get_all, and get_all_ex service access.

### User classes
- Kubernetes platform operators deploying the agent or Kubernetes Glue integration
- ClearML users submitting jobs to an execution queue consumed by the integration
- Developers or integrators using backend service client abstractions

### Operating environment
- Kubernetes cluster environment with pods and Kubernetes jobs
- Docker-based execution environment, including sibling container management through a mapped Docker socket in service-pod mode
- Connectivity to a ClearML server or backend for status reporting, ping, and service requests

### Assumptions and dependencies
- Kubernetes Glue operation depends on a provided YAML template for Kubernetes job preparation.
- Long-lasting service-pod operation depends on the `clearml-agent` Docker image and mapped Docker socket access.
- Worker telemetry depends on connectivity to the ClearML server.
- Backend service actions depend on backend session request and response handling.

## 3. External Interface Requirements

### User interfaces
No end-user GUI requirements are specified.

### Software/API interfaces
| Interface | Requirement summary |
|---|---|
| Backend service client | The system shall support backend service actions including `create`, `get`, `get_by_id`, `get_all`, and `get_all_ex` through session-based request handling. |
| Events service interface | The system shall support request and response structures for multi-task scalar metrics iteration histograms. |
| Models service interface | The system shall support model deletion request structures and model data object fields. |

### Communication interfaces
| Interface | Requirement summary |
|---|---|
| Server connectivity ping | The worker shall ping the server at a configurable period. |
| Queue-based job retrieval | Kubernetes Glue shall pull jobs from the ClearML execution queue. |

### Data exchange formats
| Format/item | Requirement summary |
|---|---|
| Structured service objects | Backend services shall use structured request and response objects. |
| Histogram key values | Event histogram queries shall support `iter`, `iso_time`, and `timestamp` axis selectors. |
| Kubernetes job template input | Kubernetes Glue shall prepare jobs based on a provided YAML template. |

## 4. Functional Requirements

| ID | Description | Trigger/Input | System behavior | Output | Priority | Verification |
|---|---|---|---|---|---|---|
| FR-001 | Kubernetes Glue job preparation | Availability of jobs in the ClearML execution queue and a provided YAML template | The system shall support a Kubernetes Glue execution flow that pulls jobs from the ClearML execution queue and prepares a Kubernetes job from the provided YAML template. | Prepared Kubernetes job | High | Demonstration |
| FR-002 | In-pod experiment startup and monitoring | A job is prepared for execution in a pod | The system shall install the experiment environment inside the pod, and start and monitor the experiment process. | Running and monitored experiment process in the pod | High | Demonstration |
| FR-003 | Long-lasting service-pod mode | Deployment of the long-lasting service-pod integration | The system shall support running as a long-lasting service pod using the `clearml-agent` Docker image and managing sibling Docker containers through a mapped Docker socket. | Running service pod with sibling-container management capability | Medium | Inspection |
| FR-004 | Worker status reporting | Worker runtime is active | The worker shall send status reports at a configurable reporting period. The default reporting period shall be 2 seconds. | Periodic worker status reports | Medium | Test |
| FR-005 | Server connectivity ping | Worker runtime is active | The worker shall ping the server at a configurable connectivity-check period. The default ping period shall be 30 seconds. | Periodic connectivity pings | Medium | Test |
| FR-006 | Default stdout and stderr logging | Worker runtime using default configuration | The default worker configuration shall enable stdout and stderr logging (`log_stdout=true`). The current requirement covers default enablement and does not require separate runtime disable semantics. | Execution logs include stdout and stderr under default configuration | Medium | Inspection |
| FR-007 | Backend service client actions | Consumer invokes a supported backend action | Backend service clients shall support actions such as `create`, `get`, `get_by_id`, `get_all`, and `get_all_ex`; `create` shall return an entity containing the service response ID, `get` and `get_by_id` shall return a mapped entity, and `get_all` and `get_all_ex` shall return tabular results in `TableResponse` form. | Created entity, mapped entity, or tabular result as applicable | Medium | Inspection |

## 5. Non-Functional Requirements

| ID | Quality attribute | Requirement | Priority | Verification |
|---|---|---|---|---|
| NFR-001 | Operability | The default worker telemetry configuration shall provide status reporting every 2 seconds and connectivity ping every 30 seconds unless overridden by configuration. | Medium | Inspection |
| NFR-002 | Operability | The worker shall support two memory reporting scopes: process or subprocess scope by default, and entire-machine scope when `report_global_mem_used` is enabled. | Low | Test |
| NFR-003 | Compatibility | The system shall maintain compatibility with versioned backend service interfaces including at least models service v2.4 and events service v2.5 as represented by the available request and response structures. | Medium | Inspection |

## 6. Data Requirements

### Data entities and objects
| ID | Data item/entity | Requirement |
|---|---|---|
| DR-001 | Worker configuration | The system shall support worker configuration fields including `report_period_sec`, `ping_period_sec`, `log_stdout`, and `report_global_mem_used`. |
| DR-002 | Histogram request | The system shall support histogram request fields including `task`, `samples`, and `key`, where `key` supports `iter`, `iso_time`, and `timestamp`. |
| DR-003 | Model delete request | The system shall support a model delete request containing `model` and `force` fields. |
| DR-004 | Model object | The system shall support model metadata fields including notable nullable fields such as `id`, `name`, `user`, `company`, `created`, and `task`. These fields are not specified as required by the current schema. |
| DR-005 | Queue job input | The system shall accept ClearML execution-queue jobs as input for Kubernetes Glue processing. |
| DR-006 | Kubernetes job template input | The system shall accept a Kubernetes YAML template as input for job preparation. |

## 7. System Constraints

| ID | Constraint |
|---|---|
| C-001 | The long-lasting service-pod integration is constrained to use the `clearml-agent` Docker image. |
| C-002 | Sibling Docker container management in service-pod mode requires mapping the Docker socket into the pod. |
| C-003 | Kubernetes Glue job preparation requires a provided YAML template. |
| C-004 | Supported backend interfaces are constrained by versioned service definitions, including events v2.5 and models v2.4. |
| C-005 | Kubernetes service-pod mode currently depends on Docker-socket mapping for sibling-container management; this mechanism is planned to be replaced by podman. |

## 8. Verification and Acceptance Criteria

| Requirement ID | Verification method | Acceptance criterion |
|---|---|---|
| FR-001 | Demonstration | A queued job is shown being converted into a Kubernetes job using a provided YAML template. |
| FR-002 | Demonstration | In-pod execution shows environment installation and the experiment process being started and monitored. |
| FR-003 | Inspection | Deployment configuration or runtime setup shows use of the `clearml-agent` image and mapped Docker socket. |
| FR-004 | Test | The worker emits status reports according to `report_period_sec`, with a default value of 2 seconds when not overridden. |
| FR-005 | Test | The worker pings the server according to `ping_period_sec`, with a default value of 30 seconds when not overridden. |
| FR-006 | Inspection | Default configuration sets `log_stdout=true` and indicates stdout and stderr logging is enabled by default. |
| FR-007 | Inspection | Client implementation shows `create` returning an entity with the response ID, `get` or `get_by_id` returning a mapped entity, and `get_all` or `get_all_ex` returning `TableResponse`. |
| NFR-001 | Inspection | Default configuration contains reporting and ping intervals of 2 seconds and 30 seconds. |
| NFR-002 | Test | Memory reporting behavior changes between process or subprocess scope and machine-wide scope based on configuration. |
| NFR-003 | Inspection | Version markers for the cited service interfaces match v2.4 and v2.5. |
| DR-001 | Inspection | Worker configuration definitions include `report_period_sec`, `ping_period_sec`, `log_stdout`, and `report_global_mem_used`. |
| DR-002 | Inspection | Histogram request definitions include `task`, `samples`, and `key`, and `key` supports `iter`, `iso_time`, and `timestamp`. |
| DR-003 | Inspection | Model delete request definitions include `model` and `force`. |
| DR-004 | Inspection | Model schema includes the listed nullable metadata fields and does not mark them as required. |
| DR-005 | Demonstration | Kubernetes Glue accepts a queued ClearML job as input. |
| DR-006 | Demonstration | Kubernetes Glue accepts a YAML template and uses it to prepare a Kubernetes job. |
