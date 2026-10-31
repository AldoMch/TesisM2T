# Checked Software Requirements Specification: Activiti 7 Guide-Documented Platform Examples

## 1. Introduction

### 1.1 Purpose
This Software Requirements Specification defines normalized requirements for the Activiti 7 developer-guide examples and the platform behaviors they demonstrate, including authentication, process runtime interaction, task runtime authorization, audit observation, cloud deployment access, and scalability configuration.

### 1.2 Scope
This SRS describes Activiti platform behaviors, example processes, and deployment patterns documented or demonstrated by the developer guide. These requirements are not software obligations implemented by the guide content itself.

The SRS covers:
- authentication token acquisition and use for user endpoint access,
- process definition lookup and `SimpleProcess` instance start behavior,
- audit observation for a just-started process instance,
- `TaskRuntime` access control through a logged-in user with the required role,
- a complete example that combines `ProcessRuntime` and `TaskRuntime` APIs with a human participant,
- Kubernetes/GKE ingress-based external access,
- deployment descriptor parameters for scalability experiments,
- architecture background needed for downstream architecture view generation.

The SRS does not define:
- a graphical user interface,
- a quantified performance target for cloud connector transaction handling,
- an ongoing build-artifact version obligation for the developer guide itself,
- guaranteed executability of the full example beyond the documented example/module presence.

### 1.3 Intended Audience
- Developers following Activiti 7 examples.
- Integrators invoking runtime, task, audit, or query APIs.
- Operators deploying example services to Kubernetes or GKE.
- Architecture-generation tools that need normalized requirements without provenance metadata.

### 1.4 Definitions and Abbreviations
| Term | Definition |
|---|---|
| Activiti Cloud | Activiti cloud-oriented runtime and service environment used by the examples. |
| Example Runtime Bundle | Runtime bundle that hosts deployed process definitions and process instances in the examples. |
| Keycloak | Identity provider used to obtain authentication tokens. |
| `ProcessRuntime` | API used for process runtime interaction. |
| `TaskRuntime` | API used for task interaction and requiring a logged-in user with the proper role. |
| `ACTIVITI_USER` | Required user role for interacting with the `TaskRuntime` API. |
| `ROLE_ACTIVITI_USER` | Granted authority form of the `ACTIVITI_USER` role. |
| Ingress Controller | Kubernetes component that routes external traffic to selected internal services. |

## 2. Overall Description

### 2.1 Product Perspective
The described subject is a set of Activiti 7 platform behaviors and examples presented through a developer guide. The runtime behavior is provided by Activiti, Keycloak, Spring Boot, Spring Security, and Kubernetes/GKE infrastructure, while the guide content demonstrates how those parts are used together.

### 2.2 Function Summary
The SRS captures the following capabilities:
- obtaining a Keycloak token for authenticated user endpoint requests,
- using the token to access user endpoints,
- viewing deployed process definitions in the Example Runtime Bundle,
- starting a new instance of `SimpleProcess`,
- checking audit events related to the just-started process instance,
- using `TaskRuntime` only under a logged-in user with `ACTIVITI_USER` / `ROLE_ACTIVITI_USER`,
- documenting a full example that combines `ProcessRuntime`, `TaskRuntime`, and a human participant,
- exposing selected Kubernetes-hosted services through NGINX ingress and a public IP,
- configuring data input rate and cloud component replica counts through deployment descriptors.

### 2.3 User Classes
| User class | Description |
|---|---|
| Authenticated user | Obtains and uses a token to access user endpoints and runtime services. |
| Task API user | Interacts with `TaskRuntime` and must have `ACTIVITI_USER` / `ROLE_ACTIVITI_USER`. |
| Human participant | Participates in a documented process example that requires human interaction. |
| Cluster operator | Configures ingress and public IP access for services deployed in Kubernetes/GKE. |
| Developer or integrator | Follows the examples and invokes Activiti APIs during development or integration. |

### 2.4 Operating Environment
| Environment aspect | Requirement context |
|---|---|
| Spring Boot application | Provides the application context for security and user setup in the examples. |
| Spring Security | Provides user, group, role, and logged-in user context handling. |
| Keycloak | Issues authentication tokens for subsequent user endpoint requests. |
| Activiti Runtime Bundle | Hosts process definitions and started process instances. |
| Audit Service | Displays audit events for the just-started process instance. |
| Query Service | Provides process execution information as read-oriented process state. |
| Kubernetes / GKE | Hosts cloud-oriented services in the deployment examples. |
| NGINX Ingress Controller | Routes external requests from a public IP to selected internal services. |
| Deployment descriptors | Hold configurable data input rate and cloud component replica counts. |

### 2.5 Architecture Context
The architecture context relevant for downstream view generation includes:
- Gateway or API gateway for routed access into cloud services.
- SSO/identity management, represented by Keycloak in the authentication flow.
- Runtime Bundle for deployed process definitions and process instance execution.
- `ProcessRuntime` and `TaskRuntime` APIs for process and task interactions.
- Audit Service for events associated with the just-started process instance.
- Query Service for process execution information.
- Notification Service and Cloud Connectors as architecture background components.
- Kubernetes registry/config maps and deployment descriptors for cloud deployment configuration.
- NGINX ingress and public IP exposure for external access to selected internal services.

Gateway, Query Service, Notification Service, Cloud Connectors, registry/config maps, and similar components should be treated as architecture background unless a requirement below assigns them explicit behavior.

### 2.6 Assumptions and Dependencies
| ID | Assumption or dependency |
|---|---|
| AD-001 | Authentication tokens are time-limited and may need to be reacquired after expiration or invalidation. |
| AD-002 | User endpoint access depends on obtaining and supplying a valid Keycloak token. |
| AD-003 | `TaskRuntime` interaction depends on the current logged-in user context and the `ACTIVITI_USER` / `ROLE_ACTIVITI_USER` role. |
| AD-004 | External interaction with selected cluster services depends on ingress configuration and public IP availability. |
| AD-005 | Scalability experiments depend on deployment descriptor parameters for input rate and replica count. |
| AD-006 | Version alignment for Activiti project artifacts is a point-in-time compatibility context and not an ongoing build obligation for the developer guide itself. |

## 3. External Interface Requirements

### 3.1 User Interfaces
No graphical user interface is specified. Interaction is performed through developer actions, REST/API requests, example code, and cluster administration commands.

### 3.2 Software and API Interfaces
| ID | Interface | Requirement |
|---|---|---|
| API-001 | Keycloak token acquisition | Users shall be able to obtain an authentication token for subsequent user endpoint requests. |
| API-002 | User endpoints | User endpoints shall require a valid authentication token and reject invalid or expired tokens. |
| API-003 | Process definitions endpoint | Authenticated users shall be able to retrieve deployed process definitions from the Example Runtime Bundle. |
| API-004 | Process start endpoint/API | Authenticated users shall be able to start a new `SimpleProcess` instance. |
| API-005 | Audit Service | Users shall be able to inspect audit events associated with the just-started process instance. |
| API-006 | Query Service | Users shall be able to obtain process execution information where query functionality is available. |
| API-007 | `TaskRuntime` API | Access shall require a logged-in user with `ACTIVITI_USER` / `ROLE_ACTIVITI_USER`. |
| API-008 | `ProcessRuntime` API | The documented full example shall combine `ProcessRuntime` with `TaskRuntime` for a process involving a human participant. |
| API-009 | Ingress-routed service endpoints | Selected internal services shall be reachable externally after ingress and public IP setup. |

### 3.3 Communication Interfaces
| ID | Interface | Requirement |
|---|---|---|
| CI-001 | REST authorization | REST authorization shall establish the currently logged-in user context for protected endpoint interaction. |
| CI-002 | Ingress routing | NGINX ingress shall create routes from external access points to selected internal Kubernetes services. |
| CI-003 | Token-based authentication | User endpoint requests shall include a valid token when protected endpoints are accessed. |

### 3.4 Data Exchange Items
| ID | Data item | Description |
|---|---|---|
| DE-001 | Authentication token | Token obtained from Keycloak and supplied to protected user endpoints. |
| DE-002 | Process definition listing | Data returned when viewing deployed process definitions. |
| DE-003 | Process instance start request | Request to start a new `SimpleProcess` instance. |
| DE-004 | Audit event records | Event records associated with the just-started process instance. |
| DE-005 | Process execution information | Read-oriented process execution data exposed through query functionality. |
| DE-006 | User role information | User, group, and role data used by Spring Security authorization. |
| DE-007 | Deployment descriptor parameters | Input rate and replica count parameters used for scalability experiments. |

## 4. Functional Requirements

| ID | Requirement | Trigger/Input | Required behavior | Output | Priority | Verification |
|---|---|---|---|---|---|---|
| FR-001 | The guide-documented platform shall require a valid Keycloak token before allowing access to protected user endpoints. | A user requests a protected user endpoint. | Accept requests with a valid token and reject requests with an invalid or expired token. | Authorized endpoint response or unauthorized error. | High | Test |
| FR-002 | The guide-documented platform shall allow an authenticated user to view deployed process definitions in the Example Runtime Bundle. | Authenticated request to inspect process definitions. | Return the process definitions deployed in the Example Runtime Bundle. | Process definition listing. | High | Demonstration |
| FR-003 | The guide-documented platform shall allow an authenticated user to start a new process instance from `SimpleProcess`. | Authenticated request to start `SimpleProcess`. | Create a new `SimpleProcess` process instance. | Started process instance confirmation. | High | Demonstration |
| FR-004 | The Audit Service shall display audit events associated with the just-started process instance. | User checks the Audit Service after starting a process instance. | Expose audit events for the just-started process instance without claiming unspecified event types. | Audit event records. | Medium | Inspection |
| FR-005 | The guide-documented platform shall permit `TaskRuntime` interaction only for a currently logged-in user with `ACTIVITI_USER` / `ROLE_ACTIVITI_USER`. | User invokes `TaskRuntime` operations. | Evaluate the logged-in user context and required role before allowing task API interaction. | Task API access granted or denied. | High | Test |
| FR-006 | The developer guide shall document a complete example that combines `ProcessRuntime` and `TaskRuntime` APIs and involves a human participant. | Developer follows the full example section. | Provide the documented example and its related module reference; do not imply guaranteed execution beyond documented presence. | Example description and module reference. | Medium | Inspection |
| FR-007 | The deployed example environment shall support external access to selected internal services through NGINX ingress and public IP exposure. | Operator configures ingress for Kubernetes/GKE services. | Route external requests through ingress to selected internal services. | Externally reachable service endpoints. | High | Demonstration |

## 5. Non-Functional Requirements

| ID | Requirement | Quality attribute | Priority | Verification |
|---|---|---|---|---|
| NFR-001 | Authentication tokens used for protected endpoint access shall be time-limited and shall become invalid after their validity period or invalidation event. | Security | High | Test |
| NFR-002 | The example deployment shall support scalability experimentation by allowing data input rate and cloud component replica counts to be configured through deployment descriptors. | Scalability | Medium | Inspection |
| NFR-003 | Protected endpoint and task API access shall preserve role-based authorization boundaries through token authentication and logged-in user context. | Security | High | Test |

No measurable latency, throughput, or performance-improvement threshold is specified for cloud connector transaction handling in this SRS.

## 6. Data Requirements

| ID | Data requirement |
|---|---|
| DR-001 | The platform shall use a Keycloak-issued authentication token for protected user endpoint requests. |
| DR-002 | The platform shall expose deployed process definition information for the Example Runtime Bundle. |
| DR-003 | The platform shall create and expose a started `SimpleProcess` process instance when an authenticated start request succeeds. |
| DR-004 | The Audit Service shall expose audit event records associated with the just-started process instance. |
| DR-005 | The Query Service shall expose process execution information where query functionality is available. |
| DR-006 | Spring Security shall manage user, group, and role information needed for `TaskRuntime` authorization. |
| DR-007 | Deployment descriptors shall contain configurable data input rate and cloud component replica count parameters for scalability experiments. |

## 7. Constraints

| ID | Constraint | Type |
|---|---|---|
| C-001 | Security, user identity, groups, and roles shall rely on Spring Security modules within a Spring Boot application context. | Technology |
| C-002 | `TaskRuntime` access shall require the `ACTIVITI_USER` role and its `ROLE_ACTIVITI_USER` granted-authority form. | Access control |
| C-003 | External access to selected Kubernetes/GKE services shall depend on NGINX Ingress Controller configuration and public IP availability. | Deployment/network |
| C-004 | For Activiti 7.0.0-EA-201802 compatibility context, Activiti project artifacts are aligned with Spring Boot `2.0.0.RELEASE` and Spring Cloud `Finchley.M8`; this shall not be treated as an ongoing build constraint on the developer guide itself. | Compatibility |
| C-005 | The developer guide content shall not be treated as the runtime implementation of Activiti, Keycloak, Spring Security, or Kubernetes behavior. | Scope |
| C-006 | Architecture background components shall not be expanded into mandatory functional behavior unless a functional requirement assigns behavior to them. | Architecture scope |

## 8. Verification and Acceptance Matrix

| Requirement ID | Verification method | Acceptance criterion |
|---|---|---|
| FR-001 | Test | A valid token enables protected endpoint access; an invalid or expired token is rejected. |
| FR-002 | Demonstration | An authenticated request returns deployed process definitions from the Example Runtime Bundle. |
| FR-003 | Demonstration | An authenticated request starts a new `SimpleProcess` process instance. |
| FR-004 | Inspection | Audit Service output shows events associated with the just-started process instance. |
| FR-005 | Test | `TaskRuntime` access succeeds for a logged-in user with `ROLE_ACTIVITI_USER` and is denied otherwise. |
| FR-006 | Inspection | The guide contains the full example and related module reference combining `ProcessRuntime`, `TaskRuntime`, and a human participant. |
| FR-007 | Demonstration | After ingress setup, selected internal services are reachable externally through ingress/public IP routing. |
| NFR-001 | Test | Previously issued tokens become unusable after expiration or invalidation. |
| NFR-002 | Inspection | Deployment descriptors expose configurable input-rate and replica-count parameters. |
| NFR-003 | Test | Protected endpoint and task API access enforce token authentication and role-based checks. |
| DR-001 | Inspection | Token data is used for protected user endpoint requests. |
| DR-002 | Inspection | Process definition data is returned for the Example Runtime Bundle. |
| DR-003 | Inspection | Started process instance data exists after a successful start request. |
| DR-004 | Inspection | Audit event records are available for the just-started process instance. |
| DR-005 | Inspection | Query functionality exposes process execution information where available. |
| DR-006 | Inspection | User, group, and role data support `TaskRuntime` authorization. |
| DR-007 | Inspection | Deployment descriptor parameters include input rate and replica count controls. |
| C-001 | Inspection | Security setup uses Spring Security within a Spring Boot context. |
| C-002 | Test | `ROLE_ACTIVITI_USER` is required for allowed `TaskRuntime` interaction. |
| C-003 | Demonstration | Public IP and NGINX ingress route traffic to selected internal services. |
| C-004 | Inspection | Compatibility context uses Spring Boot `2.0.0.RELEASE` and Spring Cloud `Finchley.M8` only as point-in-time Activiti project alignment. |
| C-005 | Inspection | Requirements distinguish developer-guide content from runtime platform implementation. |
| C-006 | Inspection | Architecture diagrams keep background components separate from explicitly required behaviors. |
