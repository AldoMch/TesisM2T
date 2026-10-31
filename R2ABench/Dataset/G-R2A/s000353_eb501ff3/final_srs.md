# Software Requirements Specification (SRS)

## 1. Introduction

### 1.1 Purpose
This SRS defines evidence-backed requirements for the repository-specific capabilities exposed by the Turing API and related runtime components at commit `22d15b1895af3c813fb7c2490f68158670108d8c`.

### 1.2 Product scope
Based on the repository evidence, Turing provides:
- an HTTP API for Turing resources, including routers and ensemblers,
- cluster-facing components for creating, updating, and deleting Turing router deployments in Kubernetes,
- a PyFuncEnsembler webservice runtime for user-defined ensemblers.

This SRS is limited to behaviors and constraints directly supported by the evidence pack.

### 1.3 Intended audience
- Product owners and maintainers of Turing
- API consumers integrating with Turing endpoints
- QA and verification engineers
- Deployment and platform engineers operating Turing in Kubernetes-based environments

### 1.4 References
- Repository: `caraml-dev/turing`
- Repository URL: https://github.com/caraml-dev/turing
- Commit: `22d15b1895af3c813fb7c2490f68158670108d8c`
- Evidence sources:
  - `api/api/specs/routers.yaml` (`E003`)
  - `api/api/specs/ensemblers.yaml` (`E005`, `E006`)
  - `api/README.md` (`E004`)
  - `engines/router/README.md` (`E002`)
  - `engines/pyfunc-ensembler-service/README.md` (`E001`)

## 2. Overall Description

### 2.1 Product perspective
Turing is an API-driven system with:
- HTTP handlers and routing defined by OpenAPI specifications,
- service and cluster packages for lifecycle management of Turing router deployments in Kubernetes,
- a separate PyFuncEnsembler service used with Turing routers,
- middleware for authorization and request validation.

### 2.2 Product functions summary
Supported by evidence, the product provides:
- listing routers belonging to a project,
- retrieving ensembler details by ID,
- deleting an ensembler by ID,
- persisting and returning ensembler representations,
- exposing user-defined ensemblers as a webservice,
- managing router deployment lifecycle in a Kubernetes cluster.

### 2.3 User classes
- API clients managing Turing resources such as routers and ensemblers
- Platform operators deploying or updating Turing router components in Kubernetes
- Users deploying user-defined ensemblers through the PyFuncEnsembler runtime

### 2.4 Operating environment
- HTTP-based API server (`E004`, `E003`, `E005`, `E006`)
- Kubernetes cluster for router deployment lifecycle management (`E004`)
- Docker-based packaging for the PyFuncEnsembler service (`E001`)
- MLflow model registry as an artifact source for local image building of the PyFuncEnsembler service (`E001`)

### 2.5 Assumptions and dependencies
- Turing API behavior is defined through OpenAPI specifications (`E003`, `E005`, `E006`)
- Router deployment operations depend on Kubernetes cluster access (`E004`)
- PyFuncEnsembler image creation depends on downloading model artifacts from MLflow model registry (`E001`)
- Request tracing may integrate with Jaeger (`E002`)

## 3. External Interface Requirements

### 3.1 User interfaces
| Interface | Description | Source |
|---|---|---|
| HTTP API | API endpoints for routers and ensemblers | `E003`, `E005`, `E006` |
| PyFuncEnsembler webservice | User-defined ensemblers can be run as a webservice | `E001` |

### 3.2 Software/API interfaces
| Interface | Description | Source |
|---|---|---|
| OpenAPI-defined API | API handlers and routing are defined in OpenAPI specs | `E004`, `E003`, `E005`, `E006` |
| Kubernetes cluster interface | Used for creating, updating, and deleting Turing router deployments | `E004` |
| MLflow model registry | Source of model artifacts for local PyFuncEnsembler image builds | `E001` |
| Authorization and request validation middleware | HTTP server middleware layer | `E004` |

### 3.3 Communication interfaces
| Interface | Description | Source |
|---|---|---|
| HTTP | API endpoints are exposed over HTTP | `E004`, `E003`, `E005`, `E006` |
| Application JSON payloads | Responses explicitly use `application/json` | `E005`, `E006` |

### 3.4 Data exchange formats
| Format | Description | Source |
|---|---|---|
| JSON | Ensembler responses are JSON representations | `E005`, `E006` |
| Timeout string | Timeout schema pattern: `^[0-9]+(ms|s|m|h)$` | `E003` |

## 4. Functional Requirements

| ID | Description | Trigger/Input | System Behavior | Output | Priority | Verification | Source Evidence |
|---|---|---|---|---|---|---|---|
| FR-001 | List routers for a project | HTTP `GET /projects/{project_id}/routers` with a project ID path parameter | The system shall provide an endpoint that lists routers belonging to the specified project. | Router list response for the given project | High | Test | `E003` |
| FR-002 | Retrieve ensembler details by ID | HTTP `GET /projects/{project_id}/ensemblers/{ensembler_id}` with project and ensembler IDs | The system shall return the details of the specified ensembler. | `200` response with `application/json` representation of an `Ensembler` | High | Test | `E005` |
| FR-003 | Delete an ensembler by ID | HTTP `DELETE /projects/{project_id}/ensemblers/{ensembler_id}` with project and ensembler IDs | The system shall delete the specified ensembler and report the outcome. | On success, `200` with JSON `EnsemblerId`; on failure, documented error responses including `400`, `404`, or `500` | High | Test | `E006` |
| FR-004 | Expose user-defined ensemblers as a webservice | Deployment/run request for PyFuncEnsemblerRunner | The system shall support running a user-defined ensembler as a webservice for use with Turing routers. | A reachable ensembler webservice | Medium | Demonstration | `E001` |
| FR-005 | Manage Turing router deployments in Kubernetes | Create, update, or delete deployment operations | The system shall provide cluster-facing functionality for creating, updating, and deleting Turing router deployments in a Kubernetes cluster. | Router deployment lifecycle operation result | High | Demonstration | `E004` |

## 5. Non-Functional Requirements

| ID | Quality Attribute | Requirement | Priority | Verification | Source Evidence | Evidence Type |
|---|---|---|---|---|---|---|
| NFR-001 | Security | The API shall support authorization and request validation middleware for HTTP requests. | High | Inspection | `E004` | explicit |
| NFR-002 | Observability | The router component shall support request tracing through Jaeger client initialization for requests. | Medium | Demonstration | `E002` | explicit |
| NFR-003 | Configurability | The router user container shall use port `8080` by default and allow this port to be configured. | Medium | Test | `E002` | explicit |
| NFR-004 | Interoperability | API specifications shall conform to OpenAPI `3.0.3` for documented endpoints and schemas. | Medium | Inspection | `E003` | explicit |

## 6. Data Requirements

### 6.1 Data entities or objects
| Entity/Object | Description | Source |
|---|---|---|
| Router | Resource listed under a project | `E003` |
| Ensembler | Resource returned as JSON in ensembler APIs | `E005`, `E006` |
| EnsemblerId | JSON object representing the ID of a deleted ensembler | `E006` |
| Project ID | Path parameter used to scope routers and ensemblers | `E003`, `E005`, `E006` |
| Ensembler ID | Path parameter used to identify a specific ensembler | `E005`, `E006` |
| Timeout | String value constrained by `^[0-9]+(ms|s|m|h)$` | `E003` |

### 6.2 Input/output data
| Data | Direction | Requirement | Source |
|---|---|---|---|
| `project_id` | Input | The system shall accept project ID as a required path parameter for project-scoped router and ensembler operations. | `E003`, `E005`, `E006` |
| `ensembler_id` | Input | The system shall accept ensembler ID as a required path parameter for ensembler retrieval and deletion operations. | `E005`, `E006` |
| `Ensembler` JSON | Output | The system shall return an `Ensembler` object in `application/json` for ensembler detail operations. | `E005` |
| `EnsemblerId` JSON | Output | The system shall return an `EnsemblerId` object in `application/json` after successful deletion. | `E006` |

### 6.3 Storage, integrity, privacy, retention, migration
No repository evidence in the provided pack explicitly defines retention, privacy handling, persistence guarantees, or migration requirements.

## 7. Constraints

| ID | Constraint | Source |
|---|---|---|
| C-001 | The API is constrained to OpenAPI-defined endpoints and schemas, including OpenAPI version `3.0.3`. | `E003`, `E004` |
| C-002 | Router deployment lifecycle management is constrained to a Kubernetes cluster environment. | `E004` |
| C-003 | Local Docker image building for the PyFuncEnsembler service requires prior download of model artifacts from the MLflow model registry. | `E001` |
| C-004 | Router user containers default to port `8080` unless configured otherwise. | `E002` |

## 8. Verification and Acceptance

| Requirement ID | Verification Method | Acceptance Basis |
|---|---|---|
| FR-001 | Test | Calling `GET /projects/{project_id}/routers` returns routers for the specified project. |
| FR-002 | Test | Calling `GET /projects/{project_id}/ensemblers/{ensembler_id}` returns `200` and an `Ensembler` JSON body. |
| FR-003 | Test | Calling `DELETE /projects/{project_id}/ensemblers/{ensembler_id}` returns documented success or error responses. |
| FR-004 | Demonstration | A user-defined ensembler can be run as a webservice for use with Turing routers. |
| FR-005 | Demonstration | The system can perform create, update, and delete operations for router deployments in Kubernetes. |
| NFR-001 | Inspection | Middleware support for authorization and request validation is present in the API server. |
| NFR-002 | Demonstration | Request tracing can be produced through Jaeger integration in the router component. |
| NFR-003 | Test | The router container listens on port `8080` by default and can be configured to use another port. |
| NFR-004 | Inspection | The API specification declares OpenAPI `3.0.3`. |

## 9. Traceability Matrix

| ID | Requirement | Type | Source | Evidence Type | Verification | Confidence |
|---|---|---|---|---|---|---|
| FR-001 | List routers for a project | Functional | `E003` | explicit | Test | High |
| FR-002 | Retrieve ensembler details by ID | Functional | `E005` | explicit | Test | High |
| FR-003 | Delete an ensembler by ID | Functional | `E006` | explicit | Test | High |
| FR-004 | Expose user-defined ensemblers as a webservice | Functional | `E001` | explicit | Demonstration | Medium |
| FR-005 | Manage Turing router deployments in Kubernetes | Functional | `E004` | explicit | Demonstration | Medium |
| NFR-001 | Support authorization and request validation middleware | Non-functional | `E004` | explicit | Inspection | Medium |
| NFR-002 | Support Jaeger-based request tracing | Non-functional | `E002` | explicit | Demonstration | Medium |
| NFR-003 | Default to port 8080 with configurability | Non-functional | `E002` | explicit | Test | High |
| NFR-004 | Conform API documentation to OpenAPI 3.0.3 | Non-functional | `E003` | explicit | Inspection | High |
