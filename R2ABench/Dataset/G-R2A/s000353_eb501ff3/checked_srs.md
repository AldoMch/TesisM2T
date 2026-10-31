# Software Requirements Specification

## 1. Introduction

### Purpose
This SRS defines the checked software requirements for Turing and its related runtime components. It is limited to repository-supported behavior and interfaces reflected in the reviewed source materials.

### Product scope
Turing provides:
- an HTTP API for Turing resources, including routers and ensemblers,
- cluster-facing components for creating, updating, and deleting Turing router deployments in Kubernetes,
- a PyFuncEnsembler webservice runtime for user-defined ensemblers.

### Intended audience
This document is intended for:
- product owners and maintainers of Turing,
- API consumers integrating with Turing endpoints,
- QA and verification engineers,
- deployment and platform engineers operating Turing in Kubernetes-based environments.

## 2. Overall Description

### Product perspective
Turing is an API-driven system comprising:
- HTTP handlers and routing defined by OpenAPI specifications,
- service and cluster components for lifecycle management of Turing router deployments in Kubernetes,
- a separate PyFuncEnsembler service used with Turing routers,
- middleware for authorization and request validation.

### Product functions summary
The product supports:
- listing routers belonging to a project,
- creating, retrieving, updating, and deleting ensemblers,
- exposing user-defined ensemblers as a webservice,
- managing router deployment lifecycle in a Kubernetes cluster.

### User classes
- API clients managing Turing resources such as routers and ensemblers
- Platform operators deploying or updating Turing router components in Kubernetes
- Users deploying user-defined ensemblers through the PyFuncEnsembler runtime

### Operating environment
- HTTP-based API server
- Kubernetes cluster for router deployment lifecycle management
- Docker-based packaging for the PyFuncEnsembler service
- MLflow model registry as an artifact source for local image building of the PyFuncEnsembler service

### Assumptions and dependencies
- API behavior is defined through OpenAPI specifications.
- Router deployment operations depend on Kubernetes cluster access.
- PyFuncEnsembler image creation depends on downloading model artifacts from an MLflow model registry.
- Request tracing may integrate with Jaeger.
- Middleware behavior for authorization and OpenAPI request validation depends on service configuration.

## 3. External Interface Requirements

### User interfaces
| Interface | Requirement summary |
|---|---|
| HTTP API | The system shall expose HTTP API endpoints for routers and ensemblers. |
| PyFuncEnsembler webservice | The system shall allow user-defined ensemblers to run as a webservice for use with Turing routers. |

### Software/API interfaces
| Interface | Requirement summary |
|---|---|
| OpenAPI-defined API | API handlers and routing shall be defined by OpenAPI specifications. |
| Kubernetes cluster interface | The system shall use Kubernetes interfaces for creating, updating, and deleting Turing router deployments. |
| MLflow model registry | The PyFuncEnsembler local image build flow shall use model artifacts downloaded from an MLflow model registry. |
| Middleware layer | The API service shall provide an HTTP middleware layer for authorization checks and OpenAPI-spec-based request validation, subject to configuration. |

### Communication interfaces
| Interface | Requirement summary |
|---|---|
| HTTP | API endpoints shall be exposed over HTTP. |
| JSON payloads | Ensembler API responses shall use `application/json` where documented. |

### Data exchange formats
| Format/item | Requirement summary |
|---|---|
| JSON | Ensembler create, retrieve, update, and delete responses shall use JSON representations where documented. |
| Timeout string | Router timeout values shall conform to the pattern `^[0-9]+(ms|s|m|h)$`. |
| Router protocol | Router configuration shall support protocol values `HTTP_JSON` and `UPI_V1`. The selected protocol shall constrain valid traffic-rule field sources. |

## 4. Functional Requirements

| ID | Description | Trigger/Input | System behavior | Output | Priority | Verification |
|---|---|---|---|---|---|---|
| FR-001 | List routers for a project | HTTP `GET /projects/{project_id}/routers` with a project ID path parameter | The system shall provide an endpoint that lists routers belonging to the specified project. | Router list response for the given project | High | Test |
| FR-002 | Retrieve ensembler details by ID | HTTP `GET /projects/{project_id}/ensemblers/{ensembler_id}` with project and ensembler IDs | The system shall return the details of the specified ensembler. | `200` response with `application/json` representation of an `Ensembler` | High | Test |
| FR-003 | Create ensembler | HTTP create request with `project_id` and ensembler payload | The system shall save a user-defined ensembler for the specified project. | `201` response with `application/json` representation of the saved `Ensembler` | High | Test |
| FR-004 | Update ensembler | HTTP update request with `project_id`, `ensembler_id`, and ensembler payload | The system shall update the specified ensembler. | `200` response with `application/json` representation of the updated `Ensembler` | High | Test |
| FR-005 | Delete an ensembler by ID | HTTP `DELETE /projects/{project_id}/ensemblers/{ensembler_id}` with project and ensembler IDs | The system shall delete the specified ensembler and report the outcome. | On success, return `200` and `EnsemblerId` JSON; on failure, return documented error responses: `400` means the ensembler is being used by another entity, `404` means the ensembler was not found, and `500` means deletion failed. | High | Test |
| FR-006 | Expose user-defined ensemblers as a webservice | Deployment or run request for PyFuncEnsemblerRunner | The system shall support running a user-defined ensembler as a webservice for use with Turing routers. | A reachable ensembler webservice | Medium | Demonstration |
| FR-007 | Manage Turing router deployments in Kubernetes | Create, update, or delete deployment operations | The system shall provide cluster-facing functionality for creating, updating, and deleting Turing router deployments in a Kubernetes cluster. | Router deployment lifecycle operation result | High | Demonstration |

## 5. Non-Functional Requirements

| ID | Quality attribute | Requirement | Priority | Verification |
|---|---|---|---|---|
| NFR-001 | Security and validation | The API service shall provide an HTTP middleware layer for authorization checks and OpenAPI-spec-based request validation; authorization middleware shall be mounted when authorization configuration is enabled, and request validation middleware shall be mounted when OpenAPI validation configuration is enabled. | High | Inspection and configuration test |
| NFR-002 | Observability | The Router component shall integrate Jaeger tracing capability; the system shall initialize a Jaeger client to support request tracing, but whether a specific request receives a trace shall be determined by the tracer enabled state or sampling configuration. | Medium | Demonstration |
| NFR-003 | Configurability | The Router user container shall use port `8080` by default and shall allow this port to be overridden through `ports.containerPort` in deployment configuration. | Medium | Test |
| NFR-004 | Interoperability | API specifications shall conform to OpenAPI `3.0.3` for documented endpoints and schemas. | Medium | Inspection |

## 6. Data Requirements

| ID | Data item/entity | Requirement |
|---|---|---|
| DR-001 | Router | The system shall represent Router as a project-scoped resource that can be listed through the routers API. |
| DR-002 | Ensembler | The system shall represent Ensembler as a JSON resource used in ensembler create, retrieve, and update operations. |
| DR-003 | EnsemblerId | The system shall represent the result of successful ensembler deletion as an `EnsemblerId` JSON object. |
| DR-004 | Project ID | The system shall accept `project_id` as a required path parameter for project-scoped router and ensembler operations. |
| DR-005 | Ensembler ID | The system shall accept `ensembler_id` as a required path parameter for ensembler retrieval, update, and deletion operations. |
| DR-006 | Timeout | The system shall accept timeout values matching the pattern `^[0-9]+(ms|s|m|h)$`. |
| DR-007 | Router protocol | Router configuration shall include a protocol field with values `HTTP_JSON` or `UPI_V1`. The selected protocol shall constrain legal traffic-rule field-source values. |
| DR-008 | Ensembler JSON | The system shall return an `Ensembler` object in `application/json` for successful ensembler retrieval, creation, and update operations. |
| DR-009 | EnsemblerId JSON | The system shall return an `EnsemblerId` object in `application/json` after successful ensembler deletion. |

No repository-supported requirements were found for data retention, privacy handling, persistence guarantees, or migration behavior.

## 7. System Constraints

| ID | Constraint |
|---|---|
| C-001 | The API is constrained to OpenAPI-defined endpoints and schemas, including OpenAPI version `3.0.3`. |
| C-002 | Router deployment lifecycle management is constrained to a Kubernetes cluster environment. |
| C-003 | Local Docker image building for the PyFuncEnsembler service requires prior download of model artifacts from an MLflow model registry. |
| C-004 | Router user containers use port `8080` by default unless overridden through `ports.containerPort`. |

## 8. Verification and Acceptance Criteria

| Requirement ID | Verification method | Acceptance criterion |
|---|---|---|
| FR-001 | Test | Calling `GET /projects/{project_id}/routers` returns routers for the specified project. |
| FR-002 | Test | Calling `GET /projects/{project_id}/ensemblers/{ensembler_id}` returns `200` and an `Ensembler` JSON body. |
| FR-003 | Test | Calling the ensembler create interface returns `201` and an `Ensembler` JSON body for a successfully saved ensembler. |
| FR-004 | Test | Calling the ensembler update interface returns `200` and the updated `Ensembler` JSON body. |
| FR-005 | Test | When the delete ensembler interface is called, success returns `200` with `EnsemblerId`; when the ensembler is in use, not found, or deletion fails, the system returns `400`, `404`, or `500` respectively with the corresponding semantics. |
| FR-006 | Demonstration | A user-defined ensembler can be run as a webservice for use with Turing routers. |
| FR-007 | Demonstration | The system can perform create, update, and delete operations for router deployments in Kubernetes. |
| NFR-001 | Inspection and configuration test | When authorization configuration is enabled, unauthorized requests are rejected by authorization middleware; when OpenAPI validation is enabled, requests that do not conform to the specification return validation errors. |
| NFR-002 | Demonstration | When tracing is enabled and sampling selects the request, Router requests can generate Jaeger traces; the system is not required to generate traces for every request unconditionally. |
| NFR-003 | Test | The default deployment configuration uses port `8080`; after setting `ports.containerPort`, the Router user container uses the configured port. |
| NFR-004 | Inspection | The API specification declares OpenAPI `3.0.3`. |
