# Software Requirements Specification

## 1. Introduction

### Purpose
This SRS defines evidence-backed requirements for the `lowes/auditor` component at commit `9e995377e5dd8669c96a13d79a196737a41cef2b`. The documented scope is the client-side auditing capability that compares object states and publishes audit events. Sources are limited to the repository evidence pack. `E001`, `E002`, `E003`

### Product Scope
The product provides an application-facing auditing API that accepts an old object state, a new object state, and optional event configuration, then produces an `AuditEvent` describing detected changes. Supported evidence shows configuration of application name, event source, event subtype, metadata, and element filters, plus publication of a serialized audit event consumable as an `AuditEvent` object. `E001`, `E002`, `E003`

### Intended Audience
This document is intended for:
- Application developers integrating the auditor client API into their services. `E003`
- Test and QA engineers verifying emitted audit events. `E001`, `E002`
- Maintainers of event publishing and filtering integrations. `E003`

### References
- Repository: `https://github.com/lowes/auditor`
- Snapshot: `https://github.com/lowes/auditor/tree/9e995377e5dd8669c96a13d79a196737a41cef2b`
- Primary evidence: `E001` to `E006`

## 2. Overall Description

### Product Perspective
`lowes/auditor` is a client library component within a larger application architecture. It depends on pluggable infrastructure interfaces including an `EventPublisher`, a `LogProvider`, and an `AuditEventElementFilter`. `E003`

### Product Functions Summary
The supported product functions are:
- Accept old and new object states for audit comparison. `E001`, `E002`
- Generate an `AuditEvent` that identifies updated elements, including previous and updated values and element metadata. `E002`
- Apply caller-provided event configuration such as application name, event source, event subtype, metadata, and element filters. `E001`, `E002`
- Publish the resulting audit event through an event-publishing interface. `E003`

### User Classes
- Integrating application developers calling the auditing API. `E001`, `E002`, `E003`
- Infrastructure integrators providing event publishing and logging implementations. `E003`

### Operating Environment
The component is implemented as a Kotlin library and is evidenced in Kotlin-based client and example modules. This implies a JVM-based integration environment. `E003`, `E005`, `E006`  
Evidence type: inferred for JVM environment.

### Assumptions and Dependencies
- The component requires an event publishing implementation to deliver audit events. `E003`
- The component uses filtering support to limit which elements are audited. `E001`, `E003`
- Consuming systems are expected to deserialize emitted payloads into `AuditEvent` objects. `E001`, `E002`

## 3. External Interface Requirements

### User Interfaces
No end-user graphical or command-line interface is evidenced in the provided materials.

### Software/API Interfaces
| Interface | Requirement |
|---|---|
| Auditing API | The system shall expose an API through which a caller provides `oldObject`, `newObject`, and optional `AuditorEventConfig` to initiate auditing. `E001`, `E002`, `E003` |
| Configuration input | The API shall accept configuration values for `applicationName`, `eventSource`, `eventSubType`, `metadata`, and element filters. `E001`, `E002` |
| Publisher integration | The system shall integrate with an `EventPublisher` abstraction for event delivery. `E003` |

### Communication Interfaces
| Interface | Requirement |
|---|---|
| Event publication | The system shall publish audit results as serialized event messages that can be consumed and deserialized as `AuditEvent`. `E001`, `E002`, `E003` |

### Data Exchange Formats
| Format | Evidence |
|---|---|
| `AuditEvent` serialized payload | Functional tests deserialize consumed message values into `AuditEvent`. `E001`, `E002` |
| Event element payload | Event elements include `name`, `updatedValue`, `previousValue`, and `metadata.fqdn`. `E002` |
| Domain object inputs | Example domain objects include scalar, map, list, nested object, and UUID fields. `E005`, `E006` |

## 4. Functional Requirements

| ID | Description | Trigger/Input | System Behavior | Output | Priority | Verification | Source Evidence |
|---|---|---|---|---|---|---|---|
| FR-001 | Audit updated object fields | Caller invokes the auditing API with `oldObject` and `newObject` containing at least one changed field. | The system shall detect updated fields and create an `AuditEvent` with event type `UPDATED`. For each detected updated field, the event shall include an element containing the field name, previous value, updated value, and element metadata FQDN. | A published `AuditEvent` describing the updated field set. | High | Test | `E002` |
| FR-002 | Apply caller-specified event configuration | Caller invokes the auditing API with an `AuditorEventConfig` containing `applicationName`, `eventSource`, `eventSubType`, and `metadata`. | The system shall populate the emitted `AuditEvent` using the provided configuration values. | A published `AuditEvent` whose metadata reflects the caller-supplied configuration. | High | Test | `E001`, `E002` |
| FR-003 | Support element inclusion filtering | Caller invokes the auditing API with filters that enable element filtering and provide an includes list. | The system shall restrict the audit event content to elements matching the configured includes list. | A published `AuditEvent` containing only included elements. | High | Test | `E001` |
| FR-004 | Publish generated audit events through the configured publisher interface | An audit operation produces an `AuditEvent`. | The system shall send the generated event through its event publishing integration. | A serialized event available to downstream consumers. | High | Inspection | `E003`, `E001`, `E002` |

## 5. Non-Functional Requirements

| ID | Requirement | Priority | Verification | Source Evidence | Confidence |
|---|---|---|---|---|---|
| NFR-001 | For a single audited update operation verified in the functional tests, the system shall emit exactly one matching audit event and no additional event during the observed no-event verification interval. | Medium | Test | `E001`, `E002` | Explicit |
| NFR-002 | The published event payload shall be compatible with deserialization into the `AuditEvent` data structure used by consumers. | High | Test | `E001`, `E002` | Explicit |
| NFR-003 | The component shall remain integration-oriented by using abstract infrastructure interfaces for event publishing, logging, and element filtering rather than requiring a fixed concrete implementation. | Medium | Inspection | `E003` | Inferred |

## 6. Data Requirements

| ID | Data Entity / Object | Requirement | Source Evidence |
|---|---|---|---|
| DR-001 | `AuditEvent` | The audit output shall be representable as an `AuditEvent` object consumable by downstream deserializers. | `E001`, `E002` |
| DR-002 | Event element | Each updated element in an `AuditEvent` shall support `name`, `updatedValue`, `previousValue`, and `metadata.fqdn`. | `E002` |
| DR-003 | `AuditorEventConfig` | The audit request configuration shall support `applicationName`, `eventSource`, `eventSubType`, `metadata`, and `filters.element` options including `enabled`, `types`, and `includes`. | `E001`, `E002` |
| DR-004 | Domain object inputs | The system input domain objects may contain UUIDs, nullable and non-null scalar fields, maps, lists, and nested objects, as shown in example `Item` models. | `E005`, `E006` |

## 7. Constraints

| ID | Constraint | Source Evidence |
|---|---|---|
| C-001 | The product scope evidenced here is a Kotlin client library integrated through code-level APIs rather than a standalone user application. | `E003`, `E005`, `E006` |
| C-002 | Event delivery depends on externally provided infrastructure implementations for publishing and logging. | `E003` |
| C-003 | Supported filtering behavior is limited to the element-filter configuration evidenced in tests, including enablement, type selection, and includes lists. | `E001` |

## 8. Verification and Acceptance

| Requirement ID | Verification Method | Acceptance Basis |
|---|---|---|
| FR-001 | Test | A test demonstrates that a changed field produces an `AuditEvent` with type `UPDATED` and correct element values. |
| FR-002 | Test | A test demonstrates that supplied configuration values appear in the emitted `AuditEvent`. |
| FR-003 | Test | A test demonstrates that configured inclusion filters constrain emitted event elements. |
| FR-004 | Inspection | Code and integration evidence show use of an event publishing interface and emitted serialized events consumed by tests. |
| NFR-001 | Test | A test verifies one matching event and no additional event during the observed interval. |
| NFR-002 | Test | A test successfully deserializes consumed message payloads into `AuditEvent`. |
| NFR-003 | Inspection | Source inspection confirms abstraction-based integration points. |

## 9. Traceability Matrix

| ID | Requirement | Type | Source | Evidence Type | Verification | Confidence |
|---|---|---|---|---|---|---|
| FR-001 | Detect and report updated fields in an `AuditEvent` | Functional | `E002` | Explicit | Test | High |
| FR-002 | Apply caller-provided event configuration to emitted events | Functional | `E001`, `E002` | Explicit | Test | High |
| FR-003 | Restrict emitted elements using inclusion filters | Functional | `E001` | Explicit | Test | High |
| FR-004 | Publish generated events through publisher integration | Functional | `E003`, `E001`, `E002` | Explicit | Inspection | Medium |
| NFR-001 | Emit one matching event and no extra event in the observed interval per tested audit call | Non-functional | `E001`, `E002` | Explicit | Test | Medium |
| NFR-002 | Maintain payload compatibility with `AuditEvent` deserialization | Non-functional | `E001`, `E002` | Explicit | Test | High |
| NFR-003 | Use abstract integration interfaces for publisher, logger, and filter dependencies | Non-functional | `E003` | Inferred | Inspection | Medium |
| DR-001 | Represent audit output as `AuditEvent` | Data | `E001`, `E002` | Explicit | Inspection | High |
| DR-002 | Include element name, previous value, updated value, and FQDN metadata | Data | `E002` | Explicit | Inspection | High |
| DR-003 | Support structured audit request configuration fields and filters | Data | `E001`, `E002` | Explicit | Inspection | High |
| DR-004 | Accept domain objects containing UUIDs, maps, lists, and nested objects | Data | `E005`, `E006` | Explicit | Inspection | Medium |
| C-001 | Kotlin client-library integration scope | Constraint | `E003`, `E005`, `E006` | Inferred | Inspection | Medium |
| C-002 | Depend on external publisher and logger implementations | Constraint | `E003` | Explicit | Inspection | High |
| C-003 | Filtering constrained to evidenced element-filter options | Constraint | `E001` | Explicit | Inspection | High |
