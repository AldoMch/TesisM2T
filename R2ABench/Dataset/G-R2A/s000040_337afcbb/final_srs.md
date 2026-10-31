# Software Requirements Specification (SRS)

## 1. Introduction

### 1.1 Purpose
This SRS defines evidence-backed requirements for PlugIt as represented in repository `ebu/PlugIt` at commit `c2c0f6df09e43c1aa942716ebdf0afd99e262f67`.

### 1.2 Product scope
PlugIt is a framework intended to improve the portability and integration of micro-services that require a user interface. It is described as enabling developers to build generic services that can be integrated into multiple environments through a single experience and user interface while maintaining data and process isolation. It also includes support material for service configuration, database-backed services, API access, and example mail-driven processing workflows.  
Source: [E004], [E002], [E001], [E003], [E005], [E006]

### 1.3 Intended audience
- Service developers creating new PlugIt-based services
- Integrators connecting services to the PlugIt Proxy API
- Deployment and operations personnel configuring databases and environment-specific settings
- Maintainers of database-backed or mail-integrated PlugIt services  
Source: [E002], [E001], [E003], [E005], [E006]

### 1.4 References
- Repository: https://github.com/ebu/PlugIt
- Snapshot: https://github.com/ebu/PlugIt/tree/c2c0f6df09e43c1aa942716ebdf0afd99e262f67
- Evidence sources:
  - [E001] `docs/new-plugit-service.md`
  - [E002] `docs/new-plugit-service.md`
  - [E003] `plugit/api.py`
  - [E004] `README.md`
  - [E005] `examples/standalone_proxy/plugIt/management/commands/check_mail.py`
  - [E006] `examples/standalone_proxy/plugIt/management/commands/check_mail.py`

## 2. Overall Description

### 2.1 Product perspective
PlugIt is positioned as a framework for combining multiple micro-services behind a unified user experience while preserving service isolation. It is also described as a basis for creating new services with submodules, database support, and deployment scripts.  
Source: [E004], [E002]

### 2.2 Product functions summary
- Integrate multiple micro-services into a single user experience
- Connect services to a PlugIt Proxy API endpoint
- Support environment-specific service configuration
- Support database-backed services with versioned schema updates
- Provide example processing of inbound mail with validation and routing  
Source: [E004], [E002], [E001], [E003], [E005], [E006]

### 2.3 User classes
| User class | Description | Source |
|---|---|---|
| Service developer | Creates new PlugIt projects, configures settings, defines models, and manages schema changes | [E002], [E001] |
| Integrator | Connects a service to the PlugIt Proxy API and deployment environment | [E002], [E003], [E004] |
| Operator/administrator | Provisions database instances and manages deployment-specific settings | [E001], [E002] |
| Mail workflow maintainer | Operates inbound mail handling and routing behavior | [E005], [E006] |

### 2.4 Operating environment
- A deployment environment with access to a PlugIt Proxy API URL
- A configured database, with examples including MySQL and SQLite
- Configuration files for service-specific and local/private settings
- For mail processing scenarios, access to inbound email messages  
Source: [E002], [E001], [E005], [E006]

### 2.5 Assumptions and dependencies
- A PlugIt Proxy API endpoint is available and configured through `API_URL`  
  Source: [E002]
- A database is selected, created, and configured outside the framework before use  
  Source: [E001]
- Private settings are kept in a local configuration file excluded from source control  
  Source: [E002]

## 3. External Interface Requirements

### 3.1 User interfaces
PlugIt shall support integration of multiple micro-services through a single experience and user interface. Specific UI layouts and interaction patterns are not defined in the evidence pack.  
Source: [E004]

### 3.2 Software/API interfaces
| Interface | Requirement summary | Source |
|---|---|---|
| PlugIt Proxy API | Services shall be configurable with an `API_URL` pointing to the PlugIt Proxy API | [E002] |
| Programmatic API access | The product includes an API access facility instantiated with the main API endpoint URL | [E003] |
| Database interface | Services may use a configured SQLAlchemy database URL and version-managed schema updates | [E002], [E001] |
| Mail callback interface | Mail processing passes decoded routing data and extracted text payload to `newMail(data, payload)` | [E005] |

### 3.3 Communication interfaces
| Interface | Description | Source |
|---|---|---|
| Proxy API endpoint | URL-based communication with the PlugIt Proxy API | [E002], [E003] |
| Email intake | Incoming email messages are parsed and conditionally processed or discarded | [E005], [E006] |

### 3.4 Data exchange formats
| Data item | Format indicated by evidence | Source |
|---|---|---|
| `API_URL` | String URL | [E002] |
| `SQLALCHEMY_URL` | String connection URL | [E002] |
| `PI_BASE_URL` | String path, example `'/'` | [E002] |
| `PI_ALLOWED_NETWORKS` | List of CIDR-formatted network strings, example `['127.0.0.1/32']` | [E002] |
| Mail token | `hash:data`, then decoded into `projectid, data` | [E006] |
| Mail payload | First text part of the email message | [E005] |

## 4. Functional Requirements

| ID | Description | Trigger/Input | System behavior | Output | Priority | Verification | Source evidence |
|---|---|---|---|---|---|---|---|
| FR-001 | The system shall support deployment-specific configuration through project and local configuration files. | Creation or deployment of a PlugIt service; configuration values for `API_URL`, `SQLALCHEMY_URL`, `DEBUG`, `PI_BASE_URL`, `PI_ALLOWED_NETWORKS` | The system shall accept these settings from configuration files and use them to define API endpoint, database connection, debug mode, base URL, and allowed networks. | A configured service instance suitable for its target environment | High | Inspection | [E002] |
| FR-002 | The system shall support database-backed services with version-managed schema upgrades. | A change to service models and a need to update the database schema | The system shall use Alembic-managed upgrade files to represent schema version changes and enable database upgrades for collaborators and production deployments. | Upgrade files and an upgradable database schema | Medium | Demonstration | [E001] |
| FR-003 | The system shall support combining multiple micro-services into a single experience and user interface while maintaining data and process isolation. | Integration of one or more micro-services into an environment | The system shall allow services to be combined behind a unified experience without merging their data and process boundaries. | An integrated micro-service environment | High | Demonstration | [E004] |
| FR-004 | The system shall provide programmatic access to the PlugIt API using a configured main endpoint URL. | A client provides the main API endpoint URL | The system shall create an API access instance bound to that endpoint for subsequent API use. | An initialized API access facility | Medium | Demonstration | [E003] |
| FR-005 | The system shall extract the first text part from an inbound email message and submit it with decoded routing data to the mail handler. | Receipt of an inbound email message containing text content and decodable routing data | The system shall decode the message payload, obtain the first text part, and call `newMail(data, payload)`. If the handler reports success, the processed message shall be acknowledged and deleted. | Handler invocation result; successful messages removed from the mailbox | Medium | Test | [E005] |
| FR-006 | The system shall validate inbound mail routing tokens and suppress auto-response messages before mail handling. | Receipt of an inbound email message | The system shall compare the expected hash against the received hash, reject messages with unexpected hashes, identify auto-response indicators, and discard auto-response messages instead of processing them. | Invalid or auto-response messages are not processed | High | Test | [E006] |

## 5. Non-Functional Requirements

| ID | Quality attribute | Requirement | Priority | Verification | Evidence type | Source evidence |
|---|---|---|---|---|---|---|
| NFR-001 | Portability | The product shall support deployment of services in multiple environments by externalizing environment-specific settings into configuration files rather than hardcoding them. | High | Inspection | explicit | [E004], [E002] |
| NFR-002 | Maintainability | Database schema evolution shall be managed through Alembic version files so that schema updates can be applied consistently across developer and production environments. | Medium | Inspection | explicit | [E001] |
| NFR-003 | Confidentiality | Private deployment settings shall be kept in a local configuration file that is excluded from source control to reduce unintended publication of private settings. | High | Inspection | explicit | [E002] |
| NFR-004 | Reliability | Mail processing shall avoid acting on auto-generated replies and messages with invalid routing hashes. | High | Test | explicit | [E006] |

## 6. Data Requirements

| ID | Data entity/object | Requirement | Source evidence |
|---|---|---|---|
| DR-001 | Service configuration | The system shall use configuration data for `API_URL`, `SQLALCHEMY_URL`, `DEBUG`, `PI_BASE_URL`, and `PI_ALLOWED_NETWORKS`. | [E002] |
| DR-002 | Database schema version data | The system shall maintain versioned database upgrade information through Alembic-generated upgrade files when models change. | [E001] |
| DR-003 | Mail routing token | The system shall process a mail routing token formatted as `hash:data`, and further decode `data` into `projectid` and remaining data. | [E006] |
| DR-004 | Mail payload | The system shall extract the first text part of an inbound email for downstream handling. | [E005] |
| DR-005 | Mail integrity check data | The system shall derive an expected hash using `sha512(data + secret)` and compare a substring of that digest against the received hash before processing. | [E006] |

## 7. Constraints

| ID | Constraint | Source evidence |
|---|---|---|
| C-001 | A database technology must be selected and provisioned externally before configuration; examples given are MySQL and SQLite. | [E001] |
| C-002 | The service depends on a configured PlugIt Proxy API URL. | [E002] |
| C-003 | Private settings are expected to reside in a separate local configuration file and not be published in source control. | [E002] |
| C-004 | The README describes the protocol and implementation as a draft, so adopters should treat maturity as limited. | [E004] |

## 8. Verification and Acceptance

| Requirement ID | Verification method | Acceptance criterion |
|---|---|---|
| FR-001 | Inspection | Configuration files contain the documented settings and the service can be shown to use them for environment setup. |
| FR-002 | Demonstration | A model change produces an Alembic upgrade file and the database can be upgraded using it. |
| FR-003 | Demonstration | An integration scenario shows multiple services presented through one experience while preserving service isolation. |
| FR-004 | Demonstration | Providing an endpoint URL results in an initialized API access instance. |
| FR-005 | Test | A valid inbound email with text content causes `newMail(data, payload)` to be invoked and successful processing deletes the message. |
| FR-006 | Test | Messages with invalid hashes or auto-response indicators are not passed to the mail handler. |
| NFR-001 | Inspection | Environment-specific values are defined in configuration files rather than hardcoded service logic. |
| NFR-002 | Inspection | Schema version changes are represented by Alembic upgrade files. |
| NFR-003 | Inspection | Private settings are placed in a local configuration file excluded from source control. |
| NFR-004 | Test | Auto-generated replies and invalid-hash messages are rejected during mail processing. |

## 9. Traceability Matrix

| ID | Requirement | Type | Source | Evidence Type | Verification | Confidence |
|---|---|---|---|---|---|---|
| FR-001 | Support deployment-specific configuration through config files | Functional | [E002] | explicit | Inspection | High |
| FR-002 | Support database-backed services with version-managed schema upgrades | Functional | [E001] | explicit | Demonstration | High |
| FR-003 | Combine multiple micro-services in one experience while maintaining isolation | Functional | [E004] | explicit | Demonstration | Medium |
| FR-004 | Provide programmatic access to PlugIt API using endpoint URL | Functional | [E003] | explicit | Demonstration | High |
| FR-005 | Extract first text part from inbound mail and submit it to handler | Functional | [E005] | explicit | Test | High |
| FR-006 | Validate mail routing token and suppress auto-responses | Functional | [E006] | explicit | Test | High |
| NFR-001 | Externalize environment-specific settings for multi-environment deployment | Non-functional | [E004], [E002] | explicit | Inspection | Medium |
| NFR-002 | Manage schema evolution through Alembic version files | Non-functional | [E001] | explicit | Inspection | High |
| NFR-003 | Keep private settings out of source control | Non-functional | [E002] | explicit | Inspection | High |
| NFR-004 | Prevent processing of invalid or auto-generated mail | Non-functional | [E006] | explicit | Test | High |
| DR-001 | Use documented service configuration data | Data | [E002] | explicit | Inspection | High |
| DR-002 | Maintain versioned database upgrade data | Data | [E001] | explicit | Inspection | High |
| DR-003 | Process `hash:data` mail routing tokens | Data | [E006] | explicit | Test | High |
| DR-004 | Extract first text-part mail payload | Data | [E005] | explicit | Test | High |
| DR-005 | Compare derived hash before mail processing | Data | [E006] | explicit | Test | High |
