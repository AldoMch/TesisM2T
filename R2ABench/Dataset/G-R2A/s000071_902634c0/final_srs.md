# Software Requirements Specification

## 1. Introduction

### Purpose
This SRS defines evidence-backed requirements for the repository component at commit `27cf7dd67f8c6f17aedf02fde961cd4066af524b`, focusing on the ClearML agent runtime, its Kubernetes-oriented execution flow, worker telemetry behavior, and exposed backend service interfaces.

### Product scope
Based on the available evidence, the product supports:
- running ClearML jobs through Kubernetes-related integration modes,
- installing an experiment environment inside a pod and running user code in Docker,
- periodic worker reporting and connectivity checks,
- backend service interactions for entity creation/retrieval and selected events/models data structures.

### Intended audience
- Product and requirements owners
- Maintainers of `allegroai/clearml-agent`
- Integrators deploying the agent in Kubernetes environments
- Test and validation engineers

### References
- Repository: `allegroai/clearml-agent`
- Repository URL: https://github.com/allegroai/clearml-agent
- Commit: `27cf7dd67f8c6f17aedf02fde961cd4066af524b`
- Evidence sources:
  - `README.md` (`E001`)
  - `clearml_agent/backend_api/config/default/sdk.conf` (`E002`)
  - `clearml_agent/backend_api/session/client/client.py` (`E003`)
  - `clearml_agent/backend_api/services/v2_5/events.py` (`E004`)
  - `clearml_agent/backend_api/services/v2_4/models.py` (`E005`, `E006`)

## 2. Overall Description

### Product perspective
The repository provides an agent-oriented component that integrates with ClearML backend services and supports Kubernetes-based job execution flows. The evidence shows two integration flavors in the README: a long-lasting service pod and a Kubernetes Glue mode that converts queued jobs into Kubernetes jobs using a YAML template (`E001`).

### Product functions summary
- Run as a long-lasting service pod using the `clearml-agent` Docker image (`E001`)
- Manage sibling Docker containers through a mapped Docker socket in that mode (`E001`)
- Pull jobs from a ClearML job execution queue and prepare Kubernetes jobs from a provided YAML template (`E001`)
- Inside the pod, install the job/experiment environment and spin and monitor Docker execution for user code (`E001`)
- Periodically report worker status and ping the server (`E002`)
- Optionally log stdout and stderr from execution (`E002`)
- Expose backend client actions for create/get/list-style service access (`E003`)

### User classes
- Kubernetes platform operators deploying the agent or Kubernetes Glue integration (`E001`)
- ClearML users submitting jobs to an execution queue consumed by the integration (`E001`)
- Developers or integrators using backend service client abstractions (`E003`)

### Operating environment
- Kubernetes cluster environment with pods and Kubernetes jobs (`E001`)
- Docker-based execution environment, including sibling container management through a mapped Docker socket (`E001`)
- Connectivity to a ClearML server/backend for status reporting, ping, and service requests (`E002`, `E003`)

### Assumptions and dependencies
- Kubernetes Glue operation depends on a provided YAML template for Kubernetes job preparation (`E001`)
- Long-lasting service pod operation depends on the `clearml-agent` Docker image and mapped Docker socket access (`E001`)
- Worker telemetry depends on connectivity to the server being pinged (`E002`)
- Service actions depend on backend session request/response handling (`E003`)

## 3. External Interface Requirements

### User interfaces
No end-user GUI or CLI requirements are directly supported by the provided evidence.

### Software/API interfaces
| Interface | Description | Evidence |
|---|---|---|
| Backend service client | Supports service actions including `create`, `get`, `get_all`, and `get_all_ex` through session-based request sending and mapped responses | `E003` |
| Events service v2.5 | Supports `multi_task_scalar_metrics_iter_histogram` request/response structures | `E004` |
| Models service v2.4 | Supports model deletion request structure and model data object fields | `E005`, `E006` |

### Communication interfaces
| Interface | Description | Evidence |
|---|---|---|
| Server connectivity ping | Worker pings the server at a configured period; default shown as 30 seconds | `E002` |
| Queue-based job retrieval | Kubernetes Glue pulls jobs from the ClearML job execution queue | `E001` |

### Data exchange formats
| Format aspect | Supported details | Evidence |
|---|---|---|
| Structured request/response objects | Backend services use object-structured request and response schemas | `E004`, `E005` |
| Primitive field types | Strings, integers, booleans, datetime-like values are defined in service/model structures | `E004`, `E005`, `E006` |
| Histogram key values | Event histogram query supports `iter`, `iso_time`, and `timestamp` axis selectors | `E004` |
| Kubernetes job template input | Kubernetes Glue prepares jobs based on a provided YAML template | `E001` |

## 4. Functional Requirements

| ID | Requirement | Trigger / Input | System behavior | Output | Priority | Verification | Source evidence |
|---|---|---|---|---|---|---|---|
| FR-001 | The system shall support a Kubernetes Glue execution flow that pulls jobs from the ClearML job execution queue and prepares a Kubernetes job from a provided YAML template. | Availability of jobs in the ClearML execution queue and a provided YAML template | Pull the queued job and construct a Kubernetes job based on the template | Prepared Kubernetes job | High | Demonstration | `E001` |
| FR-002 | Within the pod used for job execution, the system shall install the job/experiment environment and spin and monitor a Docker execution for the user code. | A job is prepared for execution in the pod | Install the experiment environment, start Docker-based execution, and monitor it | Running and monitored user-code execution in Docker | High | Demonstration | `E001` |
| FR-003 | In the long-lasting service pod integration flavor, the system shall run using the `clearml-agent` Docker image and manage sibling Docker containers through a mapped Docker socket. | Deployment of the long-lasting service pod integration | Use the `clearml-agent` image and use mapped Docker socket access to manage sibling containers | Running service pod with sibling-container management capability | Medium | Inspection | `E001` |
| FR-004 | The worker shall send status reports at a configurable reporting period. The default reporting period shall be 2 seconds. | Worker runtime is active | Emit status reports according to configured `report_period_sec` | Periodic worker status reports | Medium | Test | `E002` |
| FR-005 | The worker shall ping the server at a configurable connectivity-check period. The default ping period shall be 30 seconds. | Worker runtime is active | Ping the server according to configured `ping_period_sec` | Periodic connectivity pings | Medium | Test | `E002` |
| FR-006 | When stdout/stderr logging is enabled, the worker shall log both stdout and stderr from execution. | `log_stdout` is enabled | Capture and log stdout and stderr | Execution logs containing stdout/stderr | Medium | Test | `E002` |
| FR-007 | The backend service client shall support service actions for `create`, `get`, `get_all`, and `get_all_ex` by sending the corresponding request through the session and returning the mapped result form. | Consumer invokes one of the supported service actions | Send the request via session and return either an entity or a table-style response, as applicable | Created entity reference, retrieved entity, or collection response | Medium | Test | `E003` |

## 5. Non-Functional Requirements

| ID | Requirement | Quality attribute | Measure / condition | Priority | Verification | Source evidence |
|---|---|---|---|---|---|---|
| NFR-001 | The default worker telemetry configuration shall provide status reporting every 2 seconds and connectivity ping every 30 seconds unless overridden by configuration. | Operability | Defaults of `report_period_sec: 2` and `ping_period_sec: 30` | Medium | Inspection | `E002` |
| NFR-002 | The worker shall support two memory reporting scopes: process/sub-process scope by default, and entire-machine scope when `report_global_mem_used` is enabled. | Compatibility / operability | `report_global_mem_used: false` reports process/sub-process usage; enabled mode reports entire machine usage | Low | Test | `E002` |
| NFR-003 | The system shall maintain compatibility with versioned backend service interfaces including at least models service v2.4 and events service v2.5 as represented by the available request/response structures. | Compatibility | Service definitions expose `_version = "2.4"` and `_version = "2.5"` for the cited interfaces | Medium | Inspection | `E004`, `E005` |

## 6. Data Requirements

### Data entities or objects
| Entity / object | Required / notable fields | Notes | Source evidence |
|---|---|---|---|
| Worker configuration | `report_period_sec`, `ping_period_sec`, `log_stdout`, `report_global_mem_used` | Controls telemetry, connectivity checks, logging, and memory reporting scope | `E002` |
| Histogram request | `task` (string), `samples` (int, default 10000), `key` (`iter` / `iso_time` / `timestamp`) | Used for scalar metrics iteration histogram retrieval | `E004` |
| Model delete request | `model` (required string), `force` (boolean) | `force` is required when tasks use the model as an execution model, or when the creating task is published | `E005` |
| Model object | `id`, `name`, `user`, `company`, `created`, `task` | Represents model metadata fields shown in the data model | `E006` |

### Input/output data
| Direction | Data | Source evidence |
|---|---|---|
| Input | ClearML execution queue jobs | `E001` |
| Input | Kubernetes YAML template for job preparation | `E001` |
| Input | Backend service request objects for events and models | `E004`, `E005` |
| Output | Kubernetes job definitions prepared from the template | `E001` |
| Output | Status reports, connectivity pings, stdout/stderr logs | `E002` |
| Output | Backend service response objects, including entity and collection-style responses | `E003`, `E004` |

### Storage, integrity, privacy, retention, migration
No storage, privacy, retention, or migration requirements are directly supported by the provided evidence.

## 7. Constraints

| ID | Constraint | Type | Source evidence |
|---|---|---|---|
| C-001 | The long-lasting service pod integration uses the `clearml-agent` Docker image. | Deployment | `E001` |
| C-002 | Sibling Docker container management requires mapping the Docker socket into the pod. | Operational / deployment | `E001` |
| C-003 | Kubernetes Glue job preparation depends on a provided YAML template. | Integration | `E001` |
| C-004 | Supported backend interfaces in the evidence are versioned, including events v2.5 and models v2.4. | Compatibility | `E004`, `E005` |

## 8. Verification and Acceptance

| Requirement ID | Verification method | Acceptance criterion |
|---|---|---|
| FR-001 | Demonstration | A queued job is shown being converted into a Kubernetes job using a provided YAML template. |
| FR-002 | Demonstration | In-pod execution shows environment installation and Docker-based user-code execution being monitored. |
| FR-003 | Inspection | Deployment configuration or runtime setup shows use of the `clearml-agent` image and mapped Docker socket. |
| FR-004 | Test | Worker emits status reports according to `report_period_sec`, with default value 2 seconds when not overridden. |
| FR-005 | Test | Worker pings the server according to `ping_period_sec`, with default value 30 seconds when not overridden. |
| FR-006 | Test | With `log_stdout` enabled, stdout and stderr are both present in produced logs. |
| FR-007 | Test | Invoking `create`, `get`, `get_all`, and `get_all_ex` returns the expected mapped entity or collection response forms. |
| NFR-001 | Inspection | Default configuration contains reporting and ping intervals of 2 and 30 seconds. |
| NFR-002 | Test | Memory reporting behavior changes between process/sub-process scope and machine-wide scope based on configuration. |
| NFR-003 | Inspection | Version markers for the cited service interfaces match v2.4 and v2.5. |

## 9. Traceability Matrix

| ID | Requirement | Type | Source | Evidence Type | Verification | Confidence |
|---|---|---|---|---|---|---|
| FR-001 | Pull queued jobs and prepare Kubernetes jobs from a YAML template | Functional | `E001` | explicit | Demonstration | High |
| FR-002 | Install experiment environment and run/monitor Docker-based user code in pod | Functional | `E001` | explicit | Demonstration | High |
| FR-003 | Run long-lasting service pod with `clearml-agent` image and mapped Docker socket | Functional | `E001` | explicit | Inspection | Medium |
| FR-004 | Send periodic status reports with configurable/default interval | Functional | `E002` | explicit | Test | High |
| FR-005 | Ping server with configurable/default interval | Functional | `E002` | explicit | Test | High |
| FR-006 | Log stdout and stderr when enabled | Functional | `E002` | explicit | Test | High |
| FR-007 | Support `create`, `get`, `get_all`, `get_all_ex` service actions | Functional | `E003` | explicit | Test | Medium |
| NFR-001 | Default telemetry intervals are 2s and 30s | Non-functional | `E002` | explicit | Inspection | High |
| NFR-002 | Support selectable memory reporting scope | Non-functional | `E002` | explicit | Test | Medium |
| NFR-003 | Maintain compatibility with versioned backend interfaces v2.4 and v2.5 | Non-functional | `E004`, `E005` | explicit | Inspection | Medium |
