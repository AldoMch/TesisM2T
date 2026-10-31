# Software Requirements Specification (SRS)

Repository: Activiti/activiti-7-developers-guide  
Commit: `a500e1f1b3a6786ef017d510fdba4728e045c712`

## 1. Introduction

### 1.1 Purpose
This SRS defines evidence-backed requirements for the Activiti 7 developer guide repository content that demonstrates authentication, process interaction, task interaction, audit observation, and cloud deployment/access patterns for Activiti-based examples.

### 1.2 Product scope
The repository provides developer-facing examples and deployment guidance for:
- obtaining authentication tokens for user endpoint access,
- interacting with process and task runtime APIs,
- starting process instances and observing audit events,
- exposing services outside a Kubernetes cluster through ingress,
- configuring security roles and aligned platform dependencies.

### 1.3 Intended audience
- Developers using Activiti 7 examples
- Integrators connecting to runtime or task APIs
- Operators deploying example services to Kubernetes/GKE
- Reviewers validating repository behavior and constraints

### 1.4 References
- Repository: https://github.com/Activiti/activiti-7-developers-guide
- Snapshot: https://github.com/Activiti/activiti-7-developers-guide/tree/a500e1f1b3a6786ef017d510fdba4728e045c712
- Evidence sources:
  - `getting-started/getting-started-activiti-cloud/README.md` (E001)
  - `getting-started/getting-started-activiti-core.md` (E002, E003)
  - `getting-started/getting-started-activiti-cloud/google-cloud-gke.md` (E004)
  - `releases/7-ea201712.md` (E005)
  - `releases/7-ea201802.md` (E006)

## 2. Overall Description

### 2.1 Product perspective
The repository is a developer guide and example set for Activiti 7 usage in both core and cloud-oriented scenarios. It relies on external identity, security, runtime, audit, and Kubernetes ingress components rather than being a standalone end-user application.

### 2.2 Product functions summary
Supported functions evidenced in the repository include:
- obtaining a Keycloak token for authenticated requests,
- accessing user endpoints after authentication,
- querying deployed process definitions in an example runtime bundle,
- starting a new process instance from `SimpleProcess`,
- checking audit events related to process activity,
- interacting with `TaskRuntime` as a logged-in user with the required role,
- exposing services externally through NGINX ingress on GKE,
- controlling input rate and replica count in deployment descriptors for scalability experiments.

### 2.3 User classes
| User class | Description | Evidence |
|---|---|---|
| Authenticated user | Uses a token to access user endpoints and runtime services | E001 |
| Task API user | Interacts with `TaskRuntime` and must have role `ACTIVITI_USER` | E003 |
| Human actor | Participates in a process that relies on human interaction | E002 |
| Cluster/operator user | Exposes services outside Kubernetes through ingress and public IP configuration | E004 |

### 2.4 Operating environment
| Environment aspect | Requirement context | Evidence |
|---|---|---|
| Spring Boot application | Security and user setup are described within a Spring Boot application | E003 |
| Spring Security | Roles, groups, and user identity rely on Spring Security modules | E003 |
| Keycloak | Token acquisition is used for authentication to further requests | E001 |
| Kubernetes / GKE | Services are exposed externally from a cluster environment | E004 |
| NGINX Ingress Controller | Used to create routes to internal services for external access | E004 |
| Spring Boot 2.0.0.RELEASE / Spring Cloud Finchley.M9 | Artifact alignment constraint | E006 |

### 2.5 Assumptions and dependencies
| Item | Description | Evidence |
|---|---|---|
| Time-sensitive token | Authentication token is automatically invalidated over time and may need reacquisition | E001 |
| External access dependency | External interaction with cluster services depends on ingress and a public IP | E004 |
| Security context dependency | `TaskRuntime` interaction depends on a currently logged-in user context and required role | E003 |
| Deployment descriptor dependency | Scalability experiments depend on deployment descriptors that control input rate and replica counts | E005 |

## 3. External Interface Requirements

### 3.1 User interfaces
No graphical user interface requirements are directly evidenced. Interaction is described through developer actions, requests, and cluster administration steps.

### 3.2 Software/API interfaces
| Interface | Description | Evidence |
|---|---|---|
| Keycloak token acquisition | User obtains a token for authenticated requests | E001 |
| User endpoints | Accessible after token acquisition | E001 |
| Process Definitions endpoint | Used to view deployed process definitions in the example runtime bundle | E001 |
| Process start endpoint/API | Used to start a new `SimpleProcess` instance | E001 |
| Audit service | Used to inspect events associated with process activity | E001 |
| `TaskRuntime` API | Requires logged-in user with `ACTIVITI_USER` role | E003 |
| `ProcessRuntime` API | Used in examples together with `TaskRuntime` | E002 |

### 3.3 Communication interfaces
| Interface | Description | Evidence |
|---|---|---|
| REST with authorization | REST authorization sets the currently logged-in user | E003 |
| Ingress-routed external access | NGINX ingress creates routes from public IP to internal services | E004 |

### 3.4 Data exchange formats
| Format/object | Description | Evidence |
|---|---|---|
| Authentication token | Token used to authenticate further requests | E001 |
| Deployment descriptor values | Input rate and replica counts are controlled through deployment descriptors | E005 |

## 4. Functional Requirements

| ID | Description | Trigger/Input | System behavior | Output | Priority | Verification | Source evidence |
|---|---|---|---|---|---|---|---|
| FR-001 | The system shall require a Keycloak token before allowing interaction with user endpoints. | User requests access to user endpoints. | The system shall accept authenticated requests using a previously obtained token and reject requests when the token is invalid or expired. | Authorized endpoint access or unauthorized error. | High | Demonstration | E001 |
| FR-002 | The system shall allow an authenticated user to view which process definitions are deployed in the Example Runtime Bundle. | Authenticated request to inspect process definitions. | The system shall return the deployed process definitions for the example runtime bundle. | Process definition listing. | High | Demonstration | E001 |
| FR-003 | The system shall allow an authenticated user to start a new process instance from `SimpleProcess`. | Authenticated request to start `SimpleProcess`. | The system shall create a new process instance for `SimpleProcess`. | Confirmation of started process instance. | High | Demonstration | E001 |
| FR-004 | The system shall provide audit visibility for events associated with process activity. | User checks the audit service after process activity. | The system shall expose audit events associated with the relevant process instance/activity. | Audit event records. | Medium | Inspection | E001 |
| FR-005 | The system shall permit interaction with the `TaskRuntime` API only for a currently logged-in user having role `ACTIVITI_USER` (`ROLE_ACTIVITI_USER`). | User invokes `TaskRuntime` API operations. | The system shall evaluate the current user context and required role before allowing task API interaction. | Task API access granted or denied. | High | Test | E003 |
| FR-006 | The system shall support process examples that combine `ProcessRuntime` and `TaskRuntime` APIs for processes involving a human actor. | Execution of the full example process. | The system shall allow use of both runtime APIs within the example process flow. | Executable process flow involving runtime and task interactions. | Medium | Demonstration | E002 |
| FR-007 | The deployed example environment shall support external access to selected internal services through an ingress controller. | Operator exposes services from outside the cluster. | The system shall route external requests to internal services through configured ingress routes and public IP exposure. | Externally reachable service endpoints. | High | Demonstration | E004 |

## 5. Non-Functional Requirements

| ID | Requirement | Quality attribute | Priority | Verification | Source evidence |
|---|---|---|---|---|---|
| NFR-001 | Authentication tokens used for endpoint access shall be time-limited and become invalid automatically after their validity period. | Security | High | Test | E001 |
| NFR-002 | Cloud connector transaction handling shall support improved performance relative to prior behavior. This requirement is release-stated and not quantitatively bounded in the evidence. | Performance | Medium | Analysis | E005 |
| NFR-003 | The example deployment shall allow scalability experiments by configuring data input rate and the number of cloud component replicas in deployment descriptors. | Scalability | Medium | Inspection | E005 |
| NFR-004 | Repository artifacts shall remain aligned with Spring Boot `2.0.0.RELEASE` and Spring Cloud `Finchley.M9`. | Compatibility | Medium | Inspection | E006 |

## 6. Data Requirements

| ID | Data entity/object | Requirement | Source evidence |
|---|---|---|---|
| DR-001 | Authentication token | The system shall use a token obtained from Keycloak to authenticate further requests to user endpoints. | E001 |
| DR-002 | Process definition data | The system shall expose information about deployed process definitions in the Example Runtime Bundle. | E001 |
| DR-003 | Process instance data | The system shall create and expose a started instance for `SimpleProcess` when requested by an authenticated user. | E001 |
| DR-004 | Audit event data | The system shall make events associated with process activity available through the audit service. | E001 |
| DR-005 | User role data | The system shall use user/group/role information managed via Spring Security, including `ACTIVITI_USER` / `ROLE_ACTIVITI_USER` for task API access. | E003 |
| DR-006 | Deployment descriptor parameters | The system shall accept deployment descriptor parameters controlling data input rate and replica counts for cloud components. | E005 |

## 7. Constraints

| ID | Constraint | Type | Source evidence |
|---|---|---|---|
| C-001 | Security, roles, and groups rely on Spring Security modules within a Spring Boot application context. | Technology | E003 |
| C-002 | `TaskRuntime` access requires the `ACTIVITI_USER` role (`ROLE_ACTIVITI_USER`). | Access control | E003 |
| C-003 | External cluster access depends on configuring NGINX Ingress Controller and obtaining a public IP. | Deployment/Network | E004 |
| C-004 | Artifact alignment follows Spring Boot `2.0.0.RELEASE` and Spring Cloud `Finchley.M9`. | Compatibility | E006 |

## 8. Verification and Acceptance

| Requirement ID | Verification method | Acceptance criterion |
|---|---|---|
| FR-001 | Demonstration | A valid token enables endpoint access; an expired/invalid token results in unauthorized access. |
| FR-002 | Demonstration | An authenticated request returns deployed process definitions from the example runtime bundle. |
| FR-003 | Demonstration | An authenticated request successfully starts a `SimpleProcess` instance. |
| FR-004 | Inspection | Audit service output shows events associated with the executed process activity. |
| FR-005 | Test | `TaskRuntime` access succeeds for a logged-in user with `ROLE_ACTIVITI_USER` and is denied otherwise. |
| FR-006 | Demonstration | The documented full example executes using both `ProcessRuntime` and `TaskRuntime` APIs. |
| FR-007 | Demonstration | After ingress setup, selected internal services are reachable through externally exposed routes/public IP. |
| NFR-001 | Test | Previously issued tokens become unusable after expiration/invalidation. |
| NFR-002 | Analysis | Release evidence confirms connector transaction handling was changed to improve performance. |
| NFR-003 | Inspection | Deployment descriptors expose configurable input-rate and replica-count parameters. |
| NFR-004 | Inspection | Repository artifact/dependency references remain aligned with the stated Spring versions. |

## 9. Traceability Matrix

| ID | Requirement | Type | Source | Evidence Type | Verification | Confidence |
|---|---|---|---|---|---|---|
| FR-001 | Require Keycloak token for user endpoint access | Functional | E001 | explicit | Demonstration | High |
| FR-002 | View deployed process definitions | Functional | E001 | explicit | Demonstration | High |
| FR-003 | Start `SimpleProcess` instance | Functional | E001 | explicit | Demonstration | High |
| FR-004 | Provide audit visibility for process events | Functional | E001 | explicit | Inspection | Medium |
| FR-005 | Restrict `TaskRuntime` to logged-in user with `ACTIVITI_USER` role | Functional | E003 | explicit | Test | High |
| FR-006 | Support example combining `ProcessRuntime` and `TaskRuntime` with human actor | Functional | E002 | explicit | Demonstration | Medium |
| FR-007 | Expose services externally through ingress | Functional | E004 | explicit | Demonstration | High |
| NFR-001 | Time-limited token invalidation | Non-functional | E001 | explicit | Test | High |
| NFR-002 | Improved connector transaction performance | Non-functional | E005 | explicit | Analysis | Medium |
| NFR-003 | Configurable input rate and replica count for scalability experiments | Non-functional | E005 | explicit | Inspection | High |
| NFR-004 | Align artifacts with Spring Boot 2.0.0.RELEASE and Spring Cloud Finchley.M9 | Non-functional | E006 | explicit | Inspection | High |
| DR-001 | Use Keycloak token for authenticated requests | Data | E001 | explicit | Inspection | High |
| DR-002 | Expose process definition data | Data | E001 | explicit | Inspection | High |
| DR-003 | Create/process process instance data for `SimpleProcess` | Data | E001 | explicit | Inspection | High |
| DR-004 | Expose audit event data | Data | E001 | explicit | Inspection | Medium |
| DR-005 | Use Spring Security role/group/user data | Data | E003 | explicit | Inspection | High |
| DR-006 | Accept deployment descriptor scalability parameters | Data | E005 | explicit | Inspection | High |
| C-001 | Depend on Spring Security in Spring Boot context | Constraint | E003 | explicit | Inspection | High |
| C-002 | Require `ROLE_ACTIVITI_USER` for `TaskRuntime` | Constraint | E003 | explicit | Inspection | High |
| C-003 | Depend on NGINX ingress and public IP for external access | Constraint | E004 | explicit | Inspection | High |
| C-004 | Constrain platform alignment to Spring Boot / Spring Cloud versions | Constraint | E006 | explicit | Inspection | High |
