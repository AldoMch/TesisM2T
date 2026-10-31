# Software Requirements Specification

## 1. Introduction

### 1.1 Purpose
This SRS defines checked requirements for PlugIt, a framework for portable integration of user-interface-oriented micro-services. The document is prepared as a clean requirements input for downstream architecture diagram generation, implementation review, and verification planning.

### 1.2 Product Scope
PlugIt provides a framework for integrating multiple micro-services through a common proxy-mediated experience while keeping service data and processes separated. The covered scope includes:
- PlugIt Proxy and PlugIt Service topology.
- Service creation and environment-specific configuration.
- PlugIt Proxy API endpoint configuration.
- Programmatic PlugIt API client access.
- Database-backed services with versioned schema upgrades.
- Example mail-driven processing in the standalone proxy workflow.

Mail-driven processing is example/standalone proxy scope and is not a required capability of every core PlugIt service. Specific end-user screen layouts and detailed interaction patterns are not specified.

### 1.3 Intended Audience
- Service developers creating PlugIt-based services.
- Integrators connecting services to a PlugIt Proxy API.
- Operators and administrators configuring databases, private settings, and deployment environments.
- Maintainers of database-backed or mail-integrated PlugIt services.
- Architects generating or reviewing architecture artifacts from requirements.

## 2. Overall Description

### 2.1 Product Perspective
PlugIt is a framework for organizing multiple micro-services behind a shared proxy and user experience. Its product objective is to let developers design generic services that can be integrated into multiple environments while preserving each service's data and process boundaries. The current requirements identify this as an architectural goal; the concrete isolation mechanism and acceptance scenario must be specified during detailed design.

Architecture overview: PlugIt consists of a PlugIt Proxy as the host platform, a proxy-side data store, and one or more mutually isolated PlugIt Services. External users or systems access services through the proxy. The proxy communicates with each service through the PlugIt protocol. Each PlugIt Service may maintain its own service-specific data store.

### 2.2 Product Functions Summary
| Capability | Summary |
|---|---|
| Proxy-mediated service integration | Organize multiple PlugIt Services behind a PlugIt Proxy and shared user experience. |
| Service configuration | Configure service-specific and deployment-specific values through project and local configuration files. |
| Proxy API endpoint configuration | Configure services with the main PlugIt Proxy API endpoint URL. |
| Programmatic API client | Provide a PlugIt API client initialized with the main endpoint URL for API requests. |
| API capability categories | Support programmatic client capabilities related to user information, subscription tags, organization information, project members, email sending, forum topics, and related PlugIt API interactions. |
| Database-backed services | Support service database setup and schema evolution using version-managed upgrade files. |
| Private settings management | Keep private deployment settings in local configuration that is excluded from source control. |
| Example inbound mail processing | In standalone proxy example scope, validate inbound mail routing data, suppress auto-response messages, extract text payloads, and invoke a mail handler. |

### 2.3 User Classes
| User Class | Responsibilities / Needs |
|---|---|
| Service developer | Creates PlugIt projects, defines models, configures settings, and manages schema changes. |
| Integrator | Connects services to the PlugIt Proxy API and deployment environment. |
| Operator / administrator | Provisions databases, manages local/private configuration, and deploys PlugIt services. |
| API client maintainer | Maintains code that calls PlugIt API client capabilities. |
| Mail workflow maintainer | Operates the standalone proxy inbound mail workflow and validates routing behavior. |

### 2.4 Operating Environment
| Environment | Requirement |
|---|---|
| Proxy environment | The deployment shall provide a reachable PlugIt Proxy API endpoint. |
| Service environment | PlugIt Services shall be configured with service-specific settings and deployment-specific local settings. |
| Database environment | A database technology shall be selected, provisioned, and configured before database-backed service use. Examples include MySQL and SQLite. |
| Internal network topology | PlugIt Proxy and PlugIt Services may be deployed inside an internal network while external access reaches services through the proxy. |
| Standalone proxy mail environment | Example mail processing requires access to inbound email messages and mail routing settings. |

### 2.5 Assumptions and Dependencies
| ID | Assumption / Dependency |
|---|---|
| AD-001 | A PlugIt Proxy API endpoint is available before a service can integrate through the proxy. |
| AD-002 | Database creation, user creation, and connection configuration are handled before database-backed service operation. |
| AD-003 | Private settings are maintained in local configuration and are not published through source control. |
| AD-004 | The protocol and implementation are draft-level and may contain issues or instability. |
| AD-005 | Mail processing behavior applies to the standalone proxy example workflow unless a product design explicitly promotes it to core framework behavior. |

## 3. External Interface Requirements

### 3.1 User Interfaces
| Interface | Requirement |
|---|---|
| Unified service experience | PlugIt shall support the product objective of presenting multiple micro-services through a single user experience. Specific screen layouts and interaction patterns are not specified. |

### 3.2 Software and API Interfaces
| Interface | Requirement |
|---|---|
| PlugIt Proxy API endpoint | Services shall be configurable with a main API endpoint URL for communication with the PlugIt Proxy. |
| PlugIt API client | The system shall provide a programmatic client initialized with the main endpoint URL for making PlugIt API requests and accessing supported capability categories. |
| Service configuration files | The system shall read service configuration values from project and local configuration files. |
| Database interface | Database-backed services shall use configured database connection information and version-managed schema updates. |
| Alembic migration interface | Schema changes shall be represented through generated upgrade files that can be applied to update database schemas. |
| Standalone proxy mail handler | In example/standalone proxy scope, decoded routing data and extracted text payload shall be passed to the mail handler. |

### 3.3 Communication Interfaces
| Interface | Requirement |
|---|---|
| External-to-proxy access | External users or systems shall access PlugIt services through the PlugIt Proxy. |
| Proxy-to-service communication | PlugIt Proxy shall communicate with PlugIt Services through the PlugIt protocol. |
| Service-to-database communication | Each database-backed PlugIt Service shall use its own configured database connection. |
| Email intake | In example/standalone proxy scope, inbound email messages shall be parsed, validated, conditionally processed, and conditionally removed from the mailbox. |

### 3.4 Data Exchange Formats
| Data Item | Format / Requirement |
|---|---|
| API endpoint URL | `API_URL` shall be represented as a string URL. |
| Database URL | `SQLALCHEMY_URL` shall be represented as a string database connection URL. |
| Debug setting | `DEBUG` shall be represented as a boolean setting. |
| Base path | `PI_BASE_URL` shall be represented as a string path. |
| Allowed networks | `PI_ALLOWED_NETWORKS` shall be represented as a list of CIDR-formatted network strings. |
| Mail routing token | The standalone proxy mail workflow shall process routing tokens in `hash:data` form. |
| Mail payload | The standalone proxy mail workflow shall extract the first text part of an inbound email message as payload. |

## 4. Functional Requirements

| ID | Requirement | Trigger / Input | System Behavior | Output | Priority | Verification |
|---|---|---|---|---|---|---|
| FR-001 | Support deployment-specific service configuration. | A PlugIt service is created or deployed with environment-specific values. | The system shall accept settings such as `API_URL`, `SQLALCHEMY_URL`, `DEBUG`, `PI_BASE_URL`, and `PI_ALLOWED_NETWORKS` from configuration files. | A configured service instance suitable for the target environment. | High | Inspection |
| FR-002 | Support local/private configuration separation. | A deployment contains private settings. | The system shall support placing private settings in a local configuration file that is excluded from source control. | Private settings are separated from publishable project configuration. | High | Inspection |
| FR-003 | Support database-backed service schema management. | Service models change and the database schema must be updated. | The system shall use version-managed upgrade files to represent schema changes and enable database upgrades across developer and production environments. | Upgrade files and an upgradable database schema. | Medium | Demonstration |
| FR-004 | Configure services for PlugIt Proxy API integration. | A service is connected to a PlugIt Proxy deployment. | The system shall allow the service to be configured with the main PlugIt Proxy API endpoint URL. | Service configuration points to the intended proxy API endpoint. | High | Inspection |
| FR-005 | Provide a PlugIt API client. | A caller provides the main PlugIt API endpoint URL. | The system shall provide a programmatic client initialized with the main endpoint URL for making PlugIt API requests and accessing capabilities related to user information, subscription tags, organization information, project members, email sending, forum topics, and related PlugIt API interactions. | An initialized API client that can invoke supported capability categories. | Medium | Test / Inspection |
| FR-006 | Support example inbound mail text extraction. | The standalone proxy mail workflow receives an inbound email with text content and valid routing data. | The workflow shall extract the first text part of the email message and pass the decoded routing data and payload to the mail handler. If handling succeeds, the message shall be acknowledged and removed from the mailbox. | Handler invocation result and removal of successfully processed messages. | Medium | Test |
| FR-007 | Validate example mail routing tokens. | The standalone proxy mail workflow receives an inbound email with a routing token. | The workflow shall parse the routing token in `hash:data` form, compute the expected hash from the routing data and configured mail secret, and reject messages whose received hash does not match the expected value. | Invalidly routed messages are not passed to the mail handler. | High | Test |
| FR-008 | Suppress example mail auto-responses. | The standalone proxy mail workflow receives an inbound email with auto-response indicators. | The workflow shall discard the message and not pass it to the mail handler when it contains `x-auto-response-suppress`, `Auto-Autorespond`, or `auto-submitted`; when `Auto-Submitted` is not equal to `no`; or when `precedence` or `x-precedence` has a value in `auto_reply`, `bluk`, or `junk`. | Auto-response messages are dropped and not processed by the mail handler. | High | Test |

## 5. Non-Functional Requirements

| ID | Quality Attribute | Requirement | Priority | Verification |
|---|---|---|---|---|
| NFR-001 | Portability | The system shall support deployment of services in multiple environments by externalizing environment-specific settings into configuration files. | High | Inspection |
| NFR-002 | Maintainability | Database schema evolution shall be managed through versioned upgrade files so schema updates can be applied consistently across developer and production environments. | Medium | Inspection |
| NFR-003 | Confidentiality | Private deployment settings shall be kept in local configuration excluded from source control to reduce unintended publication of private settings. | High | Inspection |
| NFR-004 | Reliability | In example/standalone proxy scope, mail processing shall avoid acting on messages with invalid routing hashes or auto-response indicators. | High | Test |

## 6. Data Requirements

| ID | Data Entity / Object | Requirement |
|---|---|---|
| DR-001 | Service configuration | The system shall manage configuration values including `API_URL`, `SQLALCHEMY_URL`, `DEBUG`, `PI_BASE_URL`, and `PI_ALLOWED_NETWORKS`. |
| DR-002 | Local/private settings | The system shall support a local configuration file for private settings that should not be published through source control. |
| DR-003 | Database schema version data | The system shall maintain versioned database upgrade information when service models change. |
| DR-004 | API client endpoint | The programmatic API client shall store or use the main endpoint URL supplied during initialization. |
| DR-005 | API capability request/response data | The programmatic API client shall process request and response data for supported capability categories such as users, subscription tags, organizations, project members, email, and forum topics. |
| DR-006 | Mail routing token | In standalone proxy mail scope, the workflow shall process a routing token formatted as `hash:data`, then decode `data` into `projectid` and remaining routing data where applicable. |
| DR-007 | Mail integrity check data | In standalone proxy mail scope, the workflow shall compute the SHA-512 hexadecimal digest using the mail routing data and configured mail secret, take characters 30 through 41 using slice `[30:42]`, and compare that value with the received hash before processing. |
| DR-008 | Mail auto-response header data | In standalone proxy mail scope, the workflow shall inspect auto-response header conditions including `x-auto-response-suppress`, `Auto-Submitted`, `Auto-Autorespond`, `auto-submitted`, `precedence`, and `x-precedence`. |
| DR-009 | Mail payload | In standalone proxy mail scope, the workflow shall extract the first text part of the inbound email message as the payload for the mail handler. |

## 7. Constraints

| ID | Constraint |
|---|---|
| C-001 | A database technology must be selected and provisioned externally before database-backed service operation; supported examples include MySQL and SQLite. |
| C-002 | A service that integrates through PlugIt depends on a configured PlugIt Proxy API endpoint URL. |
| C-003 | Network access control configuration is constrained by the `PI_ALLOWED_NETWORKS` CIDR list where that setting is used. |
| C-004 | Mail-driven processing requirements are constrained to the example/standalone proxy workflow unless explicitly promoted to core framework scope. |
| C-005 | Detailed end-user interface layouts and interaction patterns are outside this SRS scope. |

## 8. Verification and Acceptance

| Requirement Set | Verification Method | Acceptance Criteria |
|---|---|---|
| FR-001, FR-002, NFR-001, NFR-003, DR-001, DR-002 | Inspection | Configuration files contain the documented service settings, and private settings are separated into local configuration excluded from source control. |
| FR-003, NFR-002, DR-003 | Demonstration / Inspection | A model change produces a versioned upgrade file, and the database can be upgraded using the generated migration path. |
| FR-004, C-002 | Inspection | A service configuration contains the main PlugIt Proxy API endpoint URL used for proxy integration. |
| FR-005, DR-004, DR-005 | Test / Inspection | After an endpoint URL is provided, the API client can be created and at least one supported capability category can be invoked or inspected as available. |
| FR-006, DR-009 | Test | A valid inbound email with text content causes the standalone proxy workflow to pass decoded routing data and the first text payload to the mail handler; successful processing removes the message. |
| FR-007, DR-006, DR-007 | Test | Messages with malformed routing tokens or mismatched `[30:42]` SHA-512 hash slices are not passed to the mail handler. |
| FR-008, NFR-004, DR-008 | Test | Messages with `x-auto-response-suppress`, `Auto-Autorespond`, or `auto-submitted`; messages where `Auto-Submitted` is not `no`; or messages where `precedence` or `x-precedence` is `auto_reply`, `bluk`, or `junk` are discarded and not passed to the mail handler. |
| C-001, C-003, C-004, C-005 | Inspection | Database provisioning, allowed-network configuration, example mail scope, and unspecified UI details are recorded in design or deployment documentation. |
