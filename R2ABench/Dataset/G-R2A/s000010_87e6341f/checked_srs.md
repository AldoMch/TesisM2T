# Software Requirements Specification

## 1. Introduction

### 1.1 Purpose
This SRS defines the final checked requirements for the Home Recipes full-stack application. It is prepared as a clean requirements input for downstream architecture diagram generation.

### 1.2 Product Scope
Home Recipes is a recipe application stack composed of:
- A Flutter/Dart client application.
- A Go gRPC server generated from Protocol Buffers service definitions.
- A gRPC-Gateway middleware layer exposing selected gRPC operations through HTTP endpoints.
- Container and Kubernetes deployment assets for local and Azure Kubernetes Service deployment workflows.

The target architecture shall use one coherent Protocol Buffers service contract shared by the client, server, and gateway middleware.

### 1.3 Intended Audience
- Developers implementing or modifying the client, server, or middleware.
- Testers validating platform support and API behavior.
- Operators deploying the server locally, in Docker, in local Kubernetes, or on Azure Kubernetes Service.
- Architecture reviewers generating or validating architecture diagrams.

### 1.4 Terminology
| Term | Definition |
|---|---|
| Client | The Flutter/Dart Home Recipes application used by end users. |
| gRPC server | The Go backend service generated from Protocol Buffers definitions. |
| gRPC-Gateway | Middleware that maps HTTP requests to gRPC service operations. |
| Protocol Buffers contract | The `.proto` service and message definitions shared across client, server, and gateway code generation. |
| Recipe | A domain object representing a recipe handled by recipe-related operations. |
| Ingredient | A domain object representing an ingredient in a recipe or available at home. |
| AKS | Azure Kubernetes Service, used for Kubernetes-based deployment of the server stack. |

## 2. Overall Description

### 2.1 Product Perspective
Home Recipes is a multi-component full-stack system. The Flutter/Dart client runs on supported user platforms and communicates with the backend through generated Protocol Buffers client code. The Go gRPC server implements recipe and ingredient services generated from the same service contract. The gRPC-Gateway middleware exposes selected gRPC operations through HTTP endpoints for API clients and testers.

The server shall support local execution, Docker container execution, local Kubernetes deployment, and Azure Kubernetes Service deployment through the corresponding deployment configuration.

### 2.2 Product Functions
- Run the Home Recipes client on Android, iOS, Web, and macOS.
- Generate Dart client code from Protocol Buffers definitions.
- Generate Go gRPC server code from Protocol Buffers definitions.
- Run the Go gRPC server.
- Package and run the server as a Docker container.
- Deploy the server stack through Kubernetes configuration, including Azure Kubernetes Service deployment.
- Expose recipe and ingredient operations through a gRPC-Gateway HTTP interface.
- Invoke middleware HTTP endpoints with standard HTTP clients such as `curl`.

### 2.3 User Classes
| User Class | Description |
|---|---|
| End user | Uses the Home Recipes client application on a supported platform. |
| API consumer or tester | Calls HTTP gateway endpoints to validate recipe and ingredient operations. |
| Developer | Generates protocol code and implements client, server, and gateway logic. |
| Operator | Builds, runs, and deploys the server through Docker or Kubernetes workflows. |

### 2.4 Operating Environment
- Flutter/Dart client runtime for Android, iOS, Web, and macOS.
- Dart toolchain with Protocol Buffers generation support.
- Go runtime and gRPC server tooling.
- Protocol Buffers compiler and Go/Dart generation plugins.
- gRPC-Gateway generation and runtime dependencies.
- Docker runtime for server image build and local container execution.
- Kubernetes environment for local cluster deployment.
- Azure Kubernetes Service for managed Kubernetes deployment.

### 2.5 Assumptions and Dependencies
- Client, server, and gateway code generation depend on shared `.proto` definitions.
- The middleware depends on the gRPC server being available at runtime.
- Docker-based execution depends on a locally buildable server image.
- Kubernetes and AKS deployment depend on valid deployment manifests and an available target cluster.
- HTTP gateway behavior shall be validated against the generated gateway contract rather than inferred from README steps alone.

## 3. External Interface Requirements

### 3.1 User Interfaces
| ID | Interface | Requirement |
|---|---|---|
| UI-001 | Flutter/Dart client | The client shall run as a Home Recipes application on Android, iOS, Web, and macOS. |

### 3.2 Software and API Interfaces
| ID | Interface | Requirement |
|---|---|---|
| API-001 | Protocol Buffers contract | The system shall define service and message contracts in `.proto` files used to generate client, server, and gateway code. |
| API-002 | Dart generated client | The client shall connect to the backend using Dart code generated from the shared `.proto` contract. |
| API-003 | Go gRPC server | The backend shall implement gRPC services generated from the shared `.proto` contract using Go tooling. |
| API-004 | gRPC-Gateway middleware | The middleware shall expose selected gRPC operations as HTTP endpoints. |
| API-005 | `addRecipe` endpoint | The middleware shall expose an HTTP endpoint for adding a recipe. |
| API-006 | `ListAllRecipes` endpoint | The middleware shall expose an HTTP endpoint for listing recipes. |
| API-007 | `ListAllIngredientsAtHome` endpoint | The middleware shall expose an HTTP endpoint for listing ingredients available at home. |
| API-008 | `GetAllIngredientsForRecipe` endpoint | The middleware shall expose an HTTP endpoint for retrieving ingredients for a recipe. |

### 3.3 Communication Interfaces
| ID | Interface | Requirement |
|---|---|---|
| COM-001 | Client-to-server communication | Client/server communication shall be based on generated Protocol Buffers and gRPC-compatible contracts. |
| COM-002 | HTTP gateway communication | API consumers shall be able to invoke gateway endpoints through HTTP requests. |
| COM-003 | gRPC-Gateway to gRPC server | The gateway shall translate HTTP requests into corresponding gRPC service calls. |
| COM-004 | Server streaming through gateway | Where `ListAllRecipes` is implemented as a server-streaming RPC, gateway exposure shall preserve a streaming response structure. |

### 3.4 Data Exchange Formats
| ID | Format | Required Content |
|---|---|---|
| DEF-001 | Protocol Buffers service definition | Service operations and message structures for recipe and ingredient exchange. |
| DEF-002 | Recipe data | Recipe fields required by add and list operations. |
| DEF-003 | Ingredient data | Ingredient fields required by home-ingredient and recipe-ingredient operations. |
| DEF-004 | Add-recipe response | Response body conforming to the add-recipe response contract and containing a success indicator. |
| DEF-005 | Recipe-ingredient request | A request message containing a single recipe object. |
| DEF-006 | Home-ingredient gateway request | A normal HTTP gateway request body representing one ingredient message per request. |

## 4. Functional Requirements

| ID | Requirement | Trigger/Input | System Behavior | Output | Priority | Verification |
|---|---|---|---|---|---|---|
| FR-001 | The system shall provide a multi-platform Home Recipes client. | User launches the client on a supported platform. | The client runs on Android, iOS, Web, and macOS. | Running client application on the selected platform. | High | Demonstration |
| FR-002 | The system shall generate and use Dart client code from Protocol Buffers definitions. | Developer builds or integrates the client. | The build process generates Dart code from `.proto` definitions, and the client uses that generated code to connect to the backend. | Client integration layer based on generated Dart code. | High | Inspection |
| FR-003 | The system shall generate and run a Go gRPC server from Protocol Buffers definitions. | Developer creates or runs the server. | The server code is generated from `.proto` definitions and implemented as a runnable Go gRPC service. | Running gRPC server. | High | Demonstration |
| FR-004 | The system shall support Docker containerization of the server. | Operator builds and runs the server image. | The server is packaged as a Docker image and can run locally as a container. | Docker image and local containerized server. | Medium | Demonstration |
| FR-005 | The system shall support Kubernetes deployment of the server stack. | Operator applies deployment configuration to a Kubernetes target. | The server stack is deployable through Kubernetes manifests or equivalent configuration. | Running Kubernetes deployment. | Medium | Demonstration |
| FR-006 | The system shall support Azure Kubernetes Service deployment. | Operator applies AKS deployment configuration. | The server stack is deployable to an AKS cluster using the provided deployment configuration. | Running AKS deployment. | Medium | Demonstration |
| FR-007 | The middleware shall expose an HTTP gateway endpoint for adding recipes. | HTTP request targets the add-recipe endpoint. | The gateway translates the HTTP request into the corresponding backend gRPC operation. | HTTP response conforming to the add-recipe response contract with a success indicator. | High | Test |
| FR-008 | The middleware shall expose an HTTP gateway endpoint for listing all recipes. | HTTP request targets the recipe-list endpoint. | The gateway translates the HTTP request into the corresponding backend gRPC operation and returns recipe-list data. | Recipe-list response, preserving streaming response structure where applicable. | High | Test |
| FR-009 | The middleware shall expose an HTTP gateway endpoint for listing ingredients available at home. | HTTP request targets the home-ingredients endpoint. | The gateway accepts a normal HTTP request body that maps to one ingredient message and invokes the corresponding backend gRPC operation. | Ingredient-at-home response for the submitted message. | Medium | Test |
| FR-010 | The middleware shall expose an HTTP gateway endpoint for retrieving ingredients for a recipe. | HTTP request targets the recipe-ingredients endpoint. | The gateway accepts a request message containing a single recipe object and invokes the corresponding backend gRPC operation. | Ingredient response for the requested recipe. | Medium | Test |

## 5. Non-Functional Requirements

| ID | Requirement | Quality Attribute | Priority | Verification |
|---|---|---|---|---|
| NFR-001 | The same client product shall be portable across Android, iOS, Web, and macOS. | Portability | High | Demonstration |
| NFR-002 | System interfaces shall remain contract-driven through generated code from Protocol Buffers for the client, server, and gateway components. | Maintainability / compatibility | High | Inspection |
| NFR-003 | The server shall be locally deployable as a Docker container image. | Deployability | Medium | Demonstration |
| NFR-004 | The server shall be deployable through Kubernetes configuration, including AKS deployment configuration. | Deployability | Medium | Demonstration |
| NFR-005 | Where recipe listing is implemented as a server-streaming RPC, gRPC-Gateway exposure shall not break the streaming response structure. | Compatibility | Medium | Test |

## 6. Data Requirements

| ID | Data Item | Requirement |
|---|---|---|
| DR-001 | Protocol Buffers definitions | The system shall maintain `.proto` files as the shared service and message contract for client, server, and gateway generation. |
| DR-002 | Recipe data | The system shall exchange recipe-related data through add-recipe and list-recipes operations. |
| DR-003 | Ingredient data | The system shall exchange ingredient-related data through home-ingredient and recipe-ingredient operations. |
| DR-004 | Add-recipe response | Add-recipe responses shall include a success indicator defined by the service contract. |
| DR-005 | Recipe-ingredient request | Each recipe-ingredient query request message shall contain a single recipe object; rejection behavior for multi-message or array-style requests is outside this SRS unless specified by the service contract. |
| DR-006 | Home-ingredient gateway message | A normal HTTP gateway request for home ingredients shall map to one ingredient message; native gRPC streaming behavior shall be governed by the `.proto` service definition. |

## 7. System Constraints

| ID | Constraint |
|---|---|
| C-001 | Client integration depends on Dart installation, Protocol Buffers plugin activation, PATH configuration, and generated Dart code from `.proto` definitions. |
| C-002 | Server implementation depends on Go, gRPC, `protoc`, and `protoc-gen-go` being installed and available in the development environment. |
| C-003 | Middleware generation depends on gRPC-Gateway dependencies, copied third-party libraries under the gateway definition folder, and annotations in the `.proto` file. |
| C-004 | Middleware runtime depends on the gRPC server running and reachable. |
| C-005 | Server Docker execution depends on a successfully built server image and Docker runtime availability. |
| C-006 | Kubernetes deployment depends on valid deployment manifests and an available local Kubernetes cluster. |
| C-007 | AKS deployment depends on valid Azure Kubernetes Service manifests and access to a configured AKS cluster. |
| C-008 | Docker registry publishing, Docker login, and APK generation are release/build workflow activities and are not product functional requirements in this SRS. |

## 8. Verification and Acceptance Criteria

| Requirement IDs | Verification Method | Acceptance Criteria |
|---|---|---|
| FR-001, NFR-001 | Demonstration | The Home Recipes client launches on Android, iOS, Web, and macOS. |
| FR-002, DR-001, C-001 | Inspection | Dart code is generated from `.proto` definitions and used by the client integration layer. |
| FR-003, DR-001, C-002 | Demonstration and inspection | Go gRPC server code is generated from `.proto` definitions, implemented, and runnable. |
| FR-004, NFR-003, C-005 | Demonstration | The server Docker image builds and runs locally. |
| FR-005, NFR-004, C-006 | Demonstration | The server stack can be deployed to a local Kubernetes target using valid deployment configuration. |
| FR-006, NFR-004, C-007 | Demonstration | The server stack can be deployed to Azure Kubernetes Service using valid AKS deployment configuration. |
| FR-007, DR-002, DR-004 | Test | The add-recipe HTTP call returns a response conforming to the add-recipe contract and containing the expected success indicator. |
| FR-008, NFR-005 | Test | The recipe-list HTTP gateway call returns recipe-list data, and streaming response structure is preserved when the backend RPC is server-streaming. |
| FR-009, DR-003, DR-006 | Test | A normal HTTP gateway call for home ingredients succeeds with a request body mapped to one ingredient message. |
| FR-010, DR-003, DR-005 | Test | A recipe-ingredient HTTP gateway call succeeds with a request message containing a single recipe object and returns the corresponding ingredient data. |
| NFR-002 | Inspection | Client, server, and gateway interfaces are generated from shared Protocol Buffers contracts. |
| C-003, C-004 | Inspection | Gateway dependencies, proto annotations, generated gateway code, and server runtime prerequisites are present. |
| C-008 | Inspection | Docker registry publishing and APK packaging remain documented build/release workflows rather than mandatory product functions. |
