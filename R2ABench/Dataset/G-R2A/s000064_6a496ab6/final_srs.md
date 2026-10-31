# Software Requirements Specification

## 1. Introduction

### Purpose
This SRS defines evidence-backed software requirements for the gran-book backend and related infrastructure at repository commit `03ab97ccfe81bccbc8e000916a663cd6a2872bf6`.

### Product scope
The repository evidence describes a backend platform for a book-related service composed of multiple internal APIs, mobile and web clients, cloud infrastructure on GCP, and integrations with external services for authentication, book search, and payments. Supported backend domains explicitly identified are:
- Authentication
- User management
- Book management
- EC site
- Support/message management context

### Intended audience
- Product owners
- Backend and infrastructure engineers
- QA engineers
- Integrators of frontend clients and external services
- Reviewers of deployment and interface design

### References
| Ref | Description |
|---|---|
| R1 | `docs/12_backend/01_design/README.md` |
| R2 | `docs/12_backend/12_protobuf/README.md` |
| R3 | `docs/12_backend/32_user_api/README.md` |
| R4 | `docs/14_infrastructure/01_design/README.md` |
| R5 | `docs/14_infrastructure/33_virtual_machine/README.md` |

## 2. Overall Description

### Product perspective
The product is a cloud-hosted backend serving:
- Native mobile applications for Google Play and App Store
- An administrative web application hosted separately

The backend architecture includes:
- Authentication API using Firebase Authentication
- User management API running in containers
- Book management API running in containers
- EC site API running in containers
- Datastores split by domain
- GCP infrastructure including load balancing and object storage

### Product functions summary
Evidence supports the following high-level functions:
- Authenticate users through Firebase Authentication
- Manage user-related data through a dedicated API
- Manage book-related data through a dedicated API
- Support EC-site operations through a dedicated API
- Integrate with Google Books API for book search
- Integrate with Stripe for payment-related processing

### User classes
| User class | Description | Evidence |
|---|---|---|
| End users | Users of the native mobile applications on Google Play / App Store | E006 |
| Administrators | Users of the administrative web application | E006 |
| External service operators/integrators | Systems interacting through Google Books API, Stripe, and Firebase Authentication | E004, E006 |

### Operating environment
| Area | Environment |
|---|---|
| Backend runtime | Container-based services on GCP/GKE-related environment |
| Virtual machine operations | GCE VM setup with Cloud SDK and Let's Encrypt tooling |
| Frontend clients | Native mobile apps and hosted web admin console |
| Datastores | Firebase Authentication, MySQL, NoSQL, Object Storage |

### Assumptions and dependencies
| Item | Type | Basis |
|---|---|---|
| Firebase Authentication is required for authentication capability | Dependency | E006 |
| Google Books API is the adopted external book-search service | Dependency | E004, E006 |
| Stripe is the adopted payment service | Dependency | E004, E006 |
| GCP services, including load balancing and object storage, are part of the target infrastructure | Dependency | E006 |
| Protocol Buffers documentation governs backend API method naming conventions | Assumption supported by design reference | E003 |

## 3. External Interface Requirements

### User interfaces
| Interface | Requirement basis |
|---|---|
| Native mobile applications | Product shall serve native app clients distributed through Google Play and App Store. Evidence identifies these as frontend clients. |
| Administrative web application | Product shall serve a web-based administrative console hosted separately. |

### Software/API interfaces
| Interface | Description | Evidence |
|---|---|---|
| Firebase Authentication | Authentication API dependency | E006 |
| Google Books API | External service for book-search-related functions | E004, E006 |
| Stripe | External service for payment-related functions | E004, E006 |
| Internal backend APIs | Authentication, user management, book management, EC site, and support-oriented API partitioning are documented | E004 |

### Communication interfaces
| Interface | Description | Evidence |
|---|---|---|
| Load-balanced network access | Infrastructure includes an L7 load balancer | E006 |
| GKE credentialed access | Operational environment uses `gcloud container clusters get-credentials` for GKE access | E002 |

### Data exchange formats
| Format | Requirement basis |
|---|---|
| Protocol Buffers | Backend documentation includes Protocol Buffers and standard method naming rules | E003 |
| Request/response API design artifacts | Backend design includes request/response design documentation | E004 |

## 4. Functional Requirements

| ID | Description | Trigger/Input | System behavior | Output | Priority | Verification | Source evidence |
|---|---|---|---|---|---|---|---|
| FR-001 | The system shall provide an authentication interface using Firebase Authentication. | An authentication request from a client application. | The system shall use Firebase Authentication as the authentication API component for user authentication. | Authentication result returned through the authentication interface. | High | Inspection | E006 |
| FR-002 | The system shall provide a user management API separated from other backend APIs. | A user-management request from a client or administrative interface. | The system shall process the request through a dedicated user management API deployed as a containerized backend component. | User-management response. | High | Inspection | E004, E006 |
| FR-003 | The system shall provide a book management API separated from other backend APIs. | A book-management request from a client or administrative interface. | The system shall process the request through a dedicated book management API deployed as a containerized backend component. | Book-management response. | High | Inspection | E004, E006 |
| FR-004 | The system shall provide an EC site API separated from other backend APIs. | An EC-site-related request from a client or administrative interface. | The system shall process the request through a dedicated EC site API deployed as a containerized backend component. | EC-site-related response. | High | Inspection | E004, E006 |
| FR-005 | The system shall integrate with Google Books API for book-search-related functionality. | A book-search request requiring external book information. | The system shall use Google Books API as the adopted external book-search service. | Retrieved book-search data returned to the requesting component. | High | Inspection | E004, E006 |
| FR-006 | The system shall integrate with Stripe for payment-related functionality. | A payment-related request from the EC site flow. | The system shall use Stripe as the adopted payment-related external API. | Payment processing result returned to the requesting component. | High | Inspection | E004, E006 |

## 5. Non-Functional Requirements

| ID | Quality | Requirement | Priority | Verification | Source evidence | Evidence type |
|---|---|---|---|---|---|---|
| NFR-001 | Portability/Deployability | User management, book management, and EC site backend services shall be deployable as container-based components in the target infrastructure. | High | Inspection | E006 | explicit |
| NFR-002 | Security | The deployed environment shall support TLS certificate provisioning using Let's Encrypt with DNS-01 challenge flow on the VM environment. | Medium | Inspection | E002 | explicit |
| NFR-003 | Compatibility | Backend API definitions shall follow documented Protocol Buffers standard method naming rules to maintain interface consistency. | Medium | Inspection | E003 | explicit |

## 6. Data Requirements

| ID | Data requirement | Type | Source evidence | Verification |
|---|---|---|---|---|
| DR-001 | Authentication data shall be managed through Firebase Authentication. | Data storage/integration | E006 | Inspection |
| DR-002 | User management data shall be stored in MySQL. | Data storage | E006 | Inspection |
| DR-003 | Book management data shall be stored in MySQL. | Data storage | E006 | Inspection |
| DR-004 | EC site data shall be stored in MySQL. | Data storage | E006 | Inspection |
| DR-005 | Message management data shall be stored in NoSQL. | Data storage | E006 | Inspection |
| DR-006 | Thumbnail data shall be stored in object storage. | Data storage | E006 | Inspection |
| DR-007 | Backend interfaces shall use documented request/response design artifacts and Protocol Buffers-related API conventions where defined. | Input/output format | E003, E004 | Inspection |

## 7. Constraints

| ID | Constraint | Source evidence |
|---|---|---|
| C-001 | The User API documentation identifies Golang as the implementation language for that backend area. | E001 |
| C-002 | The target cloud environment is GCP and includes GKE/GCE operational procedures. | E002, E006 |
| C-003 | Authentication depends on Firebase Authentication rather than a repository-defined standalone auth store. | E006 |
| C-004 | External integrations adopted in the documented design are Google Books API and Stripe. | E004, E006 |
| C-005 | Frontend consumers are limited in evidence to native mobile applications and an administrative web application. | E006 |

## 8. Verification and Acceptance

| Requirement ID | Verification method | Acceptance basis |
|---|---|---|
| FR-001 | Inspection | Architecture and interface definitions show Firebase Authentication as the authentication interface. |
| FR-002 | Inspection | Architecture/design documents show a dedicated user management API deployed as a container. |
| FR-003 | Inspection | Architecture/design documents show a dedicated book management API deployed as a container. |
| FR-004 | Inspection | Architecture/design documents show a dedicated EC site API deployed as a container. |
| FR-005 | Inspection | Design documents identify Google Books API as the adopted book-search integration. |
| FR-006 | Inspection | Design documents identify Stripe as the adopted payment integration. |
| NFR-001 | Inspection | Infrastructure design shows container-based deployment for the relevant backend APIs. |
| NFR-002 | Inspection | VM operation documentation shows Let's Encrypt certificate provisioning steps using DNS-01 hooks. |
| NFR-003 | Inspection | Protocol Buffers documentation defines standard method naming rules for APIs. |
| DR-001 to DR-006 | Inspection | Architecture documentation maps each domain to its stated data store or storage service. |
| DR-007 | Inspection | Backend design references request/response design and Protocol Buffers conventions. |
| C-001 to C-005 | Inspection | Constraint statements are directly supported by repository documentation. |

## 9. Traceability Matrix

| ID | Requirement | Type | Source | Evidence Type | Verification | Confidence |
|---|---|---|---|---|---|---|
| FR-001 | Provide authentication interface using Firebase Authentication | Functional | E006 | explicit | Inspection | High |
| FR-002 | Provide dedicated user management API | Functional | E004, E006 | explicit | Inspection | High |
| FR-003 | Provide dedicated book management API | Functional | E004, E006 | explicit | Inspection | High |
| FR-004 | Provide dedicated EC site API | Functional | E004, E006 | explicit | Inspection | High |
| FR-005 | Integrate with Google Books API for book search | Functional | E004, E006 | explicit | Inspection | High |
| FR-006 | Integrate with Stripe for payment-related functions | Functional | E004, E006 | explicit | Inspection | High |
| NFR-001 | Container-based deployability for core backend services | Non-functional | E006 | explicit | Inspection | High |
| NFR-002 | TLS certificate provisioning support via Let's Encrypt DNS-01 flow | Non-functional | E002 | explicit | Inspection | Medium |
| NFR-003 | Protocol Buffers standard method naming consistency | Non-functional | E003 | explicit | Inspection | Medium |
| DR-001 | Authentication data managed by Firebase Authentication | Data | E006 | explicit | Inspection | High |
| DR-002 | User management data stored in MySQL | Data | E006 | explicit | Inspection | High |
| DR-003 | Book management data stored in MySQL | Data | E006 | explicit | Inspection | High |
| DR-004 | EC site data stored in MySQL | Data | E006 | explicit | Inspection | High |
| DR-005 | Message management data stored in NoSQL | Data | E006 | explicit | Inspection | Medium |
| DR-006 | Thumbnail data stored in object storage | Data | E006 | explicit | Inspection | High |
| DR-007 | Requests/responses follow documented API and Protocol Buffers conventions | Data | E003, E004 | explicit | Inspection | Medium |
| C-001 | User API uses Golang | Constraint | E001 | explicit | Inspection | High |
| C-002 | GCP/GKE/GCE target environment | Constraint | E002, E006 | explicit | Inspection | High |
| C-003 | Authentication depends on Firebase Authentication | Constraint | E006 | explicit | Inspection | High |
| C-004 | External integrations are Google Books API and Stripe | Constraint | E004, E006 | explicit | Inspection | High |
| C-005 | Supported frontend consumers are native mobile apps and admin web app | Constraint | E006 | explicit | Inspection | High |
