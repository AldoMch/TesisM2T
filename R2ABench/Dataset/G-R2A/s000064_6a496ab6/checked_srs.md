# Software Requirements Specification

## 1. Introduction

### Purpose
This SRS defines the checked software requirements for the gran-book backend platform and related infrastructure.

### Product scope
The product is a backend platform for a book-related service composed of multiple internal APIs, client-facing access layers, and cloud infrastructure on GCP. The documented scope includes:
- Authentication
- User management
- Book management
- EC site management
- Support API / support information domain
- Message management data domain backed by NoSQL
- Integrations with external services for authentication, book search, payments, push notification, and email notification

### Intended audience
This document is intended for:
- Product owners
- Backend and infrastructure engineers
- QA engineers
- Integrators of frontend clients and external services
- Reviewers of deployment and interface design

### References
- Backend design documentation
- Protocol Buffers documentation
- User API documentation
- Infrastructure design documentation
- Virtual machine operation documentation
- Architecture diagram

## 2. Overall Description

### Product perspective
The product is a cloud-hosted backend serving:
- Native mobile applications
- An administrative web application

The documented architecture includes:
- A client-facing gateway or BFF layer for native-app and administrative access
- An authentication API using Firebase Authentication
- Dedicated backend services for user management, book management, EC site management, support/information handling, administration, and notification-related processing
- Domain-specific data stores including MySQL, NoSQL storage, and object storage
- GCP infrastructure including load balancing, container-based deployment, and virtual-machine-based operational components
- External integrations for authentication, payment, book search, push notification, and email notification

Where documentation sources differ on a named external book-search provider, this SRS records only that a book-search API integration is required and avoids fixing a single provider as the sole confirmed dependency.

### Product functions summary
The product shall support the following high-level functions:
- Authenticate users through an external authentication service
- Manage user-related data through a dedicated API
- Manage book-related data through a dedicated API
- Support EC-site operations through a dedicated API
- Process support-related requests through a dedicated support API
- Provide administrative access through documented gateway and service layers
- Integrate with a book-search API for book-related lookup functions
- Integrate with a payment service for payment-related processing
- Support notification-related integrations for push and email delivery

### User classes
| User class | Description |
|---|---|
| End users | Users of the native mobile applications |
| Administrators | Users of the administrative web application |
| Operations engineers | Personnel responsible for cloud deployment, VM setup, certificates, and cluster access |
| External service integrators | Systems and engineers integrating authentication, book-search, payment, push notification, and email services |

### Operating environment
| Area | Environment |
|---|---|
| Backend runtime | Container-based backend services on GCP |
| Cluster operations | Operational documentation includes GKE cluster credential retrieval for cluster access |
| Virtual machine operations | GCE VM setup with Cloud SDK and TLS certificate tooling |
| Frontend clients | Native mobile apps and hosted administrative web application |
| Datastores | Firebase Authentication, MySQL, NoSQL storage, and object storage |

### Assumptions and dependencies
- Firebase Authentication is required for authentication capability.
- The system depends on a book-search API integration, but the exact provider name must be resolved consistently across design sources before implementation is finalized.
- Stripe is a documented payment service dependency.
- Push notification and email notification providers are part of the documented architecture.
- GCP services, including load balancing, container infrastructure, object storage, VM operations, and cluster access procedures, are part of the target environment.
- Protocol Buffers documentation defines backend API naming conventions.

## 3. External Interface Requirements

### User interfaces
| Interface | Requirement summary |
|---|---|
| Native mobile applications | The product shall serve native mobile application clients. |
| Administrative web application | The product shall serve a web-based administrative console through the documented access architecture. |

### Software/API interfaces
| Interface | Requirement summary |
|---|---|
| Firebase Authentication | The system shall use Firebase Authentication for user authentication. |
| Book-search API | The system shall integrate with a documented external book-search API. |
| Stripe | The system shall integrate with Stripe for payment-related processing. |
| Push notification provider | The system shall support a push notification integration. |
| Email notification provider | The system shall support an email notification integration. |
| Internal backend APIs | The documented internal API partitioning includes authentication, user management, book management, EC site, and support APIs. |
| Gateway/BFF layer | The system shall expose client-facing backend access through the documented gateway or BFF layer. |

### Communication interfaces
| Interface | Requirement summary |
|---|---|
| Load-balanced network access | The deployed system shall support load-balanced network access. |
| Cluster access interface | Operations shall support credentialed cluster access using the documented GKE access procedure. |
| VM administration interface | Operations shall support VM-based administrative procedures for setup and certificate management. |

### Data exchange formats
| Format | Requirement summary |
|---|---|
| Protocol Buffers | Backend API definitions shall follow documented Protocol Buffers conventions and method naming rules where specified. |
| Request/response API definitions | Backend interfaces shall follow the documented request/response API design artifacts. |

## 4. Functional Requirements

| ID | Description | Trigger/Input | System behavior | Output | Priority | Verification |
|---|---|---|---|---|---|---|
| FR-001 | Authentication interface | An authentication request from a client application | The system shall provide an authentication interface using Firebase Authentication. | Authentication result returned to the requesting client or gateway. | High | Inspection |
| FR-002 | User management API | A user-management request from a client, gateway, or administrative interface | The system shall process the request through a dedicated user management API. | User-management response. | High | Inspection |
| FR-003 | Book management API | A book-management request from a client, gateway, or administrative interface | The system shall process the request through a dedicated book management API. | Book-management response. | High | Inspection |
| FR-004 | EC site API | An EC-site-related request from a client, gateway, or administrative interface | The system shall process the request through a dedicated EC site API. | EC-site-related response. | High | Inspection |
| FR-005 | Book-search integration | A book-search request requiring external book information | The system shall invoke the configured external book-search API to obtain book-related information. | Retrieved book-search data returned to the requesting component. | High | Inspection |
| FR-006 | Payment integration | A payment-related request from the EC site flow | The system shall use Stripe for payment-related processing. | Payment processing result returned to the requesting component. | High | Inspection |
| FR-007 | Support API | A support-related request from a client or administrative interface | The system shall provide a support/information API separated from other backend APIs to process support-related requests. | Support-related response. | High | Inspection |

## 5. Non-Functional Requirements

| ID | Quality attribute | Requirement | Priority | Verification |
|---|---|---|---|---|
| NFR-001 | Deployability | User management, book management, EC site, and related backend services shall be deployable as container-based components in the target GCP environment. | High | Inspection |
| NFR-002 | Security | The deployed environment shall support TLS certificate provisioning using Let's Encrypt with a DNS-01 challenge flow in the VM operational environment. | Medium | Inspection |
| NFR-003 | Interface consistency | Backend API definitions shall follow documented Protocol Buffers standard method naming rules to maintain interface consistency. | Medium | Inspection |
| NFR-004 | Architectural interoperability | The system architecture shall support integration with external authentication, payment, book-search, push notification, and email notification services. | High | Inspection |
| NFR-005 | Access architecture | The deployed architecture shall support a gateway or BFF layer for native-client and administrative access. | Medium | Inspection |

## 6. Data Requirements

| ID | Data item | Requirement | Verification |
|---|---|---|---|
| DR-001 | Authentication data | Authentication data shall be managed through Firebase Authentication. | Inspection |
| DR-002 | User management data | User management data shall be stored in MySQL. | Inspection |
| DR-003 | Book management data | Book management data shall be stored in MySQL. | Inspection |
| DR-004 | EC site data | EC site data shall be stored in MySQL. | Inspection |
| DR-005 | Message management data | Message management data shall be stored in NoSQL storage. | Inspection |
| DR-006 | Thumbnail and object data | Thumbnail or related object data shall be stored in object storage. | Inspection |
| DR-007 | API definition data | Backend interfaces shall use documented request/response design artifacts and Protocol Buffers-related API conventions where defined. | Inspection |

## 7. System Constraints

| ID | Constraint |
|---|---|
| C-001 | User API documentation identifies Golang as an implementation language for that backend area. |
| C-002 | The target cloud environment is GCP; available operational procedures include GCE VM setup and GKE credential retrieval. |
| C-003 | Authentication depends on Firebase Authentication rather than a standalone repository-defined authentication store. |
| C-004 | Payment processing is constrained to the documented Stripe integration in the current baseline. |
| C-005 | Documented frontend consumers are native mobile applications and an administrative web application. |
| C-006 | Backend service API documentation identifies Golang for several internal APIs; backend design documentation also references a Node.js-style directory structure for gateway or BFF design. This indicates mixed design references and shall not be interpreted as proof that every backend service uses Node.js. |
| C-007 | The exact external book-search provider name shall remain unresolved in the requirements baseline until the textual design documents and architecture diagram are consistent. |

## 8. Verification and Acceptance Criteria

| Requirement ID | Verification method | Acceptance criterion |
|---|---|---|
| FR-001 | Inspection | Design documentation defines an authentication interface using Firebase Authentication. |
| FR-002 | Inspection | Design documentation defines a dedicated user management API. |
| FR-003 | Inspection | Design documentation defines a dedicated book management API. |
| FR-004 | Inspection | Design documentation defines a dedicated EC site API. |
| FR-005 | Inspection | Design documentation defines an external book-search API integration for book-related lookup. |
| FR-006 | Inspection | Design documentation defines Stripe as the payment-related integration. |
| FR-007 | Inspection | Design documentation defines a dedicated support or support-information API. |
| NFR-001 | Inspection | Infrastructure and architecture documentation show container-based deployment on GCP for the relevant backend services. |
| NFR-002 | Inspection | VM operational documentation shows TLS certificate provisioning steps using Let's Encrypt DNS-01 flow. |
| NFR-003 | Inspection | Protocol Buffers documentation defines standard method naming rules for APIs. |
| NFR-004 | Inspection | Architecture documentation identifies the required external service integration categories. |
| NFR-005 | Inspection | Architecture documentation shows a gateway or BFF layer supporting client and administrative access. |
| DR-001 | Inspection | Architecture and interface documentation map authentication data handling to Firebase Authentication. |
| DR-002 | Inspection | Architecture documentation maps user management data to MySQL. |
| DR-003 | Inspection | Architecture documentation maps book management data to MySQL. |
| DR-004 | Inspection | Architecture documentation maps EC site data to MySQL. |
| DR-005 | Inspection | Architecture documentation maps message management data to NoSQL storage. |
| DR-006 | Inspection | Architecture documentation maps thumbnail or related object data to object storage. |
| DR-007 | Inspection | Backend design documentation references request/response API definitions and Protocol Buffers conventions. |
| C-001 | Inspection | User API documentation identifies Golang for the documented backend area. |
| C-002 | Inspection | Infrastructure documentation identifies GCP as the target environment and includes VM and GKE operational procedures. |
| C-003 | Inspection | Authentication design identifies Firebase Authentication as the authentication dependency. |
| C-004 | Inspection | Payment design identifies Stripe as the documented payment integration. |
| C-005 | Inspection | Client architecture documentation identifies native mobile applications and an administrative web application as consumers. |
| C-006 | Inspection | Design documentation shows Golang-based service references and a separate Node.js-style gateway or BFF directory reference. |
| C-007 | Inspection | Source documents are checked to confirm that the book-search provider remains unresolved until naming is made consistent across design artifacts. |
