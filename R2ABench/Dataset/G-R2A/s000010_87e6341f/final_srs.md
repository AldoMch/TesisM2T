# Software Requirements Specification

## 1. Introduction

### Purpose
This SRS specifies the evidenced requirements for the repository sample centered on a Home Recipes full-stack application composed of a Flutter/Dart client, a Go gRPC server, and a gRPC-Gateway middleware layer. It is grounded only in the provided repository evidence.

### Product Scope
The product scope supported by evidence is a recipe application stack that:
- provides a client application for multiple platforms,
- connects that client to a gRPC server using generated code from Protocol Buffers,
- exposes selected server capabilities through a gRPC-Gateway HTTP interface, and
- supports local containerization of the server for deployment/testing workflows.

### Intended Audience
This document is intended for:
- developers implementing or modifying the client, server, or middleware,
- testers verifying API and platform behavior,
- operators/developers running the server locally or in Docker,
- reviewers tracing repository evidence to stated requirements.

### References
- Repository: `sm2774us/full_stack_interview_prep_2021`
- Commit: `3dcc2e6fb6c9998a0b458bfc1bb16c7aaa6c61e7`
- Evidence sources:
  - `E001` client README
  - `E002` server README
  - `E003` middleware README

## 2. Overall Description

### Product Perspective
The evidenced product is a multi-component system:
- a Flutter/Dart client application,
- a Go-based gRPC server generated from `.proto` definitions,
- a middleware component using gRPC-Gateway to expose HTTP endpoints over the gRPC service.

### Product Functions Summary
The system supports the following evidenced functions:
- run the Home Recipes client on Android, iOS, Web, and macOS (`E001`);
- generate client and server code from Protocol Buffers definitions (`E001`, `E002`);
- run a gRPC server and package it as a Docker image (`E002`);
- expose recipe-related operations through HTTP endpoints including `addRecipe`, `ListAllRecipes`, `ListAllIngredientsAtHome`, and `GetAllIngredientsForRecipe` (`E003`).

### User Classes
- End users: users interacting with the Home Recipes client application on supported platforms (`E001`).
- API consumers/testers: users invoking middleware endpoints via `curl` (`E003`).
- Developers/operators: users generating code, running the server, running middleware, and building Docker images (`E001`, `E002`, `E003`).

### Operating Environment
Supported and evidenced environments:
- Client platforms: Android, iOS, Web, macOS (`E001`)
- Client toolchain: Dart, protoc plugin, generated Dart code from protos (`E001`)
- Server toolchain: Go, gRPC, `protoc`, `protoc-gen-go` (`E002`)
- Middleware toolchain: gRPC-Gateway generation flow and local dependencies (`E003`)
- Container runtime: Docker for server image build/run/push workflows (`E002`)

### Assumptions and Dependencies
- The client-server contract depends on Protocol Buffers definitions and generated code (`E001`, `E002`, `E003`).
- Middleware execution depends on the server already running as expected (`E003`).
- Server containerization assumes a locally runnable server and Docker availability (`E002`).

## 3. External Interface Requirements

| Interface Area | Requirement |
|---|---|
| User interfaces | The client shall be runnable as applications on Android, iOS, Web, and macOS. Source: `E001` |
| Software/API interfaces | The client shall connect to the server using generated Dart code from Protocol Buffers definitions. Source: `E001` |
| Software/API interfaces | The server shall implement gRPC services generated from `.proto` files using Go tooling. Source: `E002` |
| Software/API interfaces | The middleware shall expose HTTP-accessible endpoints for `addRecipe`, `ListAllRecipes`, `ListAllIngredientsAtHome`, and `GetAllIngredientsForRecipe`. Source: `E003` |
| Communication interfaces | HTTP requests to middleware endpoints shall be invocable with `curl`. Source: `E003` |
| Communication interfaces | The middleware shall support gRPC-Gateway handling for server-side streaming on `ListAllRecipes`. Source: `E003` |
| Data exchange formats | Service contracts shall be based on Protocol Buffers definitions used to generate client, server, and gateway code. Source: `E001`, `E002`, `E003` |

## 4. Functional Requirements

| ID | Description | Trigger/Input | System Behavior | Output | Priority | Verification | Source Evidence |
|---|---|---|---|---|---|---|---|
| FR-001 | Multi-platform client availability | User launches the Home Recipes client on a supported platform | The system shall provide a client runnable on Android, iOS, Web, and macOS | Running client application on the selected platform | High | Demonstration | `E001` |
| FR-002 | Client-server integration through generated contracts | Client build/integration using `.proto` definitions | The system shall generate Dart client code from Protocol Buffers definitions and use it to implement client logic that connects to the server | Client integration layer based on generated Dart code | High | Inspection | `E001` |
| FR-003 | gRPC server implementation | Developer creates and runs the server from `.proto` definitions | The system shall generate Go gRPC code from `.proto` definitions and provide a runnable server implementation | Running gRPC server | High | Demonstration | `E002` |
| FR-004 | Server containerization | Operator builds and runs the server image | The system shall support packaging the server as a Docker image that can be run locally | Docker image and locally runnable containerized server | Medium | Demonstration | `E002` |
| FR-005 | HTTP gateway for adding recipes | HTTP request to `addRecipe` | The middleware shall translate the HTTP request into the corresponding backend gRPC operation | HTTP response from `addRecipe` endpoint | High | Test | `E003` |
| FR-006 | HTTP gateway for listing all recipes | HTTP request to `ListAllRecipes` | The middleware shall expose `ListAllRecipes` and support its server-side streaming behavior through gRPC-Gateway | Streamed or gateway-delivered recipe listing response | High | Test | `E003` |
| FR-007 | HTTP gateway for listing ingredients at home | HTTP request to `ListAllIngredientsAtHome` | The middleware shall expose `ListAllIngredientsAtHome` and process one message at a time for this operation | Response containing ingredients-at-home data for one message | Medium | Test | `E003` |
| FR-008 | HTTP gateway for retrieving recipe ingredients | HTTP request to `GetAllIngredientsForRecipe` | The middleware shall expose `GetAllIngredientsForRecipe` and accept a request containing only one item | Response containing ingredients for the requested recipe item | Medium | Test | `E003` |

## 5. Non-Functional Requirements

| ID | Requirement | Quality Attribute | Priority | Verification | Evidence | Confidence |
|---|---|---|---|---|---|---|
| NFR-001 | The client shall be portable across Android, iOS, Web, and macOS without requiring a different product definition per platform. | Portability | High | Demonstration | `E001` | Explicit |
| NFR-002 | The middleware shall preserve server-side streaming compatibility for `ListAllRecipes` when exposed through gRPC-Gateway. | Compatibility | High | Test | `E003` | Explicit |
| NFR-003 | The server shall be deployable as a Docker container image that can be run locally. | Deployability | Medium | Demonstration | `E002` | Explicit |
| NFR-004 | The system interfaces shall remain contract-driven through generated code from Protocol Buffers for client, server, and gateway components. | Maintainability/Compatibility | Medium | Inspection | `E001`, `E002`, `E003` | Inferred |

## 6. Data Requirements

| ID | Data Requirement | Type | Source Evidence | Confidence |
|---|---|---|---|---|
| DR-001 | The system shall exchange service definitions through Protocol Buffers (`.proto`) files used to generate client, server, and gateway code. | Data contract | `E001`, `E002`, `E003` | Explicit |
| DR-002 | The system shall support recipe-related data exchanged via operations named `addRecipe`, `ListAllRecipes`, and `GetAllIngredientsForRecipe`. | Domain data | `E003` | Explicit |
| DR-003 | The system shall support ingredient-related data exchanged via operations named `ListAllIngredientsAtHome` and `GetAllIngredientsForRecipe`. | Domain data | `E003` | Explicit |
| DR-004 | `GetAllIngredientsForRecipe` requests shall contain only one item. | Input constraint | `E003` | Explicit |
| DR-005 | `ListAllIngredientsAtHome` shall process one message at a time. | Message constraint | `E003` | Explicit |

## 7. Constraints

| ID | Constraint | Source Evidence |
|---|---|---|
| C-001 | Client integration depends on Dart installation, protoc plugin activation, PATH configuration, and generated Dart code from protos. | `E001` |
| C-002 | Server implementation depends on Go, gRPC, `protoc`, and `protoc-gen-go` being installed and available in PATH. | `E002` |
| C-003 | Middleware generation depends on local installation of three dependencies, copying third-party libraries under `def`, and adding annotations to the proto file. | `E003` |
| C-004 | Middleware runtime depends on the server already running as expected. | `E003` |
| C-005 | Server Docker push workflow depends on Docker login for the session. | `E002` |

## 8. Verification and Acceptance

| Requirement ID | Verification Method | Acceptance Basis |
|---|---|---|
| FR-001 | Demonstration | Client launches on Android, iOS, Web, and macOS |
| FR-002 | Inspection | Generated Dart code from proto definitions is present and used for client-server connection |
| FR-003 | Demonstration | Generated Go service code and runnable server are available |
| FR-004 | Demonstration | Docker image builds and runs locally |
| FR-005 | Test | `curl` invocation of `addRecipe` returns a valid endpoint response |
| FR-006 | Test | `curl` invocation of `ListAllRecipes` succeeds through gateway with streaming support |
| FR-007 | Test | `curl` invocation of `ListAllIngredientsAtHome` succeeds with one-message-at-a-time behavior |
| FR-008 | Test | `GetAllIngredientsForRecipe` accepts only a one-item request and returns a response |
| NFR-001 | Demonstration | Same client product runs on all four listed platforms |
| NFR-002 | Test | Gateway behavior preserves server-side streaming for `ListAllRecipes` |
| NFR-003 | Demonstration | Containerized server runs locally from Docker image |
| NFR-004 | Inspection | Interfaces are generated from shared proto contracts across components |

## 9. Traceability Matrix

| ID | Requirement | Type | Source | Evidence Type | Verification | Confidence |
|---|---|---|---|---|---|---|
| FR-001 | Client runs on Android, iOS, Web, and macOS | Functional | `E001` | Explicit | Demonstration | High |
| FR-002 | Client connects to server using generated Dart proto code | Functional | `E001` | Explicit | Inspection | High |
| FR-003 | Go gRPC server is generated from proto and runnable | Functional | `E002` | Explicit | Demonstration | High |
| FR-004 | Server can be packaged and run as a Docker image | Functional | `E002` | Explicit | Demonstration | High |
| FR-005 | Middleware exposes `addRecipe` over HTTP | Functional | `E003` | Explicit | Test | High |
| FR-006 | Middleware exposes `ListAllRecipes` with streaming support | Functional | `E003` | Explicit | Test | High |
| FR-007 | Middleware exposes `ListAllIngredientsAtHome` with one-message processing | Functional | `E003` | Explicit | Test | Medium |
| FR-008 | Middleware exposes `GetAllIngredientsForRecipe` with one-item request limit | Functional | `E003` | Explicit | Test | Medium |
| NFR-001 | Client is portable across four platforms | Non-functional | `E001` | Explicit | Demonstration | High |
| NFR-002 | Gateway preserves streaming compatibility for `ListAllRecipes` | Non-functional | `E003` | Explicit | Test | High |
| NFR-003 | Server is locally deployable via Docker | Non-functional | `E002` | Explicit | Demonstration | High |
| NFR-004 | Interfaces remain contract-driven via proto generation | Non-functional | `E001`, `E002`, `E003` | Inferred | Inspection | Medium |
| DR-001 | Proto files define exchange contracts across components | Data | `E001`, `E002`, `E003` | Explicit | Inspection | High |
| DR-002 | Recipe data is exchanged through recipe endpoints | Data | `E003` | Explicit | Inspection | Medium |
| DR-003 | Ingredient data is exchanged through ingredient endpoints | Data | `E003` | Explicit | Inspection | Medium |
| DR-004 | `GetAllIngredientsForRecipe` request contains one item | Data | `E003` | Explicit | Test | High |
| DR-005 | `ListAllIngredientsAtHome` processes one message at a time | Data | `E003` | Explicit | Test | High |
