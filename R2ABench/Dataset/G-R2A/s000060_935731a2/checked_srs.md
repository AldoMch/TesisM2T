# Software Requirements Specification

## 1. Introduction

### Purpose
This SRS defines the checked software requirements for the `lowes/auditor` component. The documented scope is the client-side auditing capability that compares object states and publishes audit events. The specification is limited to behavior and interfaces supported by the reviewed repository materials.

### Product Scope
The product provides an application-facing auditing API that accepts an old object state, a new object state, and optional event configuration, then produces an `AuditEvent` describing detected changes. Supported behavior includes configuration of application name, event source, event subtype, metadata, and element filters, plus publication of an audit event consumable as an `AuditEvent` object.

### Intended Audience
This document is intended for:
- Application developers integrating the auditor client API into their services
- Test and QA engineers verifying emitted audit events
- Maintainers of event publishing and filtering integrations
- Architects generating downstream component and interface views

### References
- Repository: `lowes/auditor`

## 2. Overall Description

### Product Perspective
`lowes/auditor` is a client library component used within JVM applications. It depends on pluggable infrastructure interfaces including an `EventPublisher`, a `LogProvider`, and an `AuditEventElementFilter`.

The system acts as an audit client library inside applications, generates audit and log events, and sends audit events to an event stream through a configurable event publishing interface. The default publishing implementation is Kafka-based. Downstream services may consume the published events and persist them, but those downstream services are outside the scope of this SRS.

### Product Functions Summary
The supported product functions are:
- Accept old and new object states for audit comparison
- Generate `AuditEvent` instances that identify detected changes, including created, updated, and deleted elements
- Apply caller-provided event configuration such as application name, event source, event subtype, metadata, and element filters
- Publish the resulting audit event through an event-publishing interface
- Support element inclusion filtering for emitted audit elements

### User Classes
- Integrating application developers calling the auditing API
- Infrastructure integrators providing event publishing, logging, and filter implementations
- Test and QA engineers validating event content and publication behavior

### Operating Environment
The component is implemented as a Kotlin library for JVM applications. The reviewed materials support a JVM-targeted environment and indicate Java 11 / JVM 11 as the compilation target.

### Assumptions and Dependencies
- The component requires an event publishing implementation to deliver audit events.
- The default event publishing implementation uses Kafka.
- The component uses filtering support to limit which elements are audited.
- Consuming systems are expected to deserialize emitted payloads into `AuditEvent` objects.

## 3. External Interface Requirements

### User Interfaces
No end-user graphical or command-line interface is within the evidenced scope.

### Software/API Interfaces
| Interface | Requirement |
|---|---|
| Auditing API | The system shall expose an API through which a caller provides `oldObject`, `newObject`, and optional `AuditorEventConfig` to initiate auditing. |
| Configuration input | The API shall accept configuration values for `applicationName`, `eventSource`, `eventSubType`, `metadata`, and element filters. |
| Publisher integration | The system shall integrate with an `EventPublisher` abstraction for audit-event delivery. |
| Logging integration | The system shall integrate with a `LogProvider` abstraction for logging support. |
| Element filter integration | The system shall integrate with an `AuditEventElementFilter` abstraction for element filtering behavior. |

### Communication Interfaces
| Interface | Requirement |
|---|---|
| Event publication | The system shall publish generated audit events through `EventPublisher`. |
| Default event stream | The default publishing implementation shall send serialized audit events to a Kafka topic. |

### Data Exchange Formats
| Format | Requirement |
|---|---|
| `AuditEvent` payload | The published event payload shall be a JSON string deserializable by consumers into `AuditEvent`. |
| Event element payload | Event elements shall support `name`, `updatedValue`, `previousValue`, and `metadata.fqdn`. |
| Domain object inputs | Input domain objects may contain scalar, nullable, map, list, nested-object, and UUID fields. |

## 4. Functional Requirements

| ID | Description | Trigger/Input | System Behavior | Output | Priority | Verification |
|---|---|---|---|---|---|---|
| FR-001 | Audit changed object fields | Caller invokes the auditing API with `oldObject` and `newObject` that differ. | The system shall generate an `AuditEvent` of the corresponding type based on the differences between `oldObject` and `newObject`: `UPDATED` when field values change, `CREATED` when a new object or element is added relative to the old object, and `DELETED` when an old object or element is removed relative to the new object. For each detected changed element, the event shall include the field name, `previousValue`, `updatedValue`, and `metadata.fqdn`. | A published `AuditEvent` describing the detected changes. | High | Test |
| FR-002 | Apply caller-specified event configuration | Caller invokes the auditing API with an `AuditorEventConfig` containing `applicationName`, `eventSource`, `eventSubType`, and `metadata`. | The system shall populate the emitted `AuditEvent` using the provided configuration values. | A published `AuditEvent` whose metadata reflects the caller-supplied configuration. | High | Test |
| FR-003 | Support element inclusion filtering | Caller invokes the auditing API with element filtering enabled and filter type `InclusionFilter`, with an `includes` list. | The system shall include only elements matching the configured `includes` list in the `AuditEvent`; unmatched elements shall not appear in that event. | A published `AuditEvent` containing only the included elements. | High | Test |
| FR-004 | Publish generated audit events | An audit operation produces an `AuditEvent`. | The system shall publish generated audit events through `EventPublisher`; the default implementation shall use Kafka producer configuration to send serialized events to the configured topic. | A serialized audit event is made available to downstream consumers. | High | Inspection |

## 5. Non-Functional Requirements

| ID | Requirement | Priority | Verification |
|---|---|---|---|
| NFR-001 | The component shall remain integration-oriented by using abstract infrastructure interfaces for event publishing, logging, and element filtering rather than requiring a fixed concrete implementation. | Medium | Inspection |
| NFR-002 | The product shall operate as a JVM library component suitable for integration into Java 11 / JVM 11 application environments. | Medium | Inspection |
| NFR-003 | In verified single-event scenarios, the system shall publish the expected matching audit event and shall not publish additional events within the observed 2-second verification window. This requirement is limited to the tested scenarios and does not imply that every audit call produces only one event. | Medium | Test |

## 6. Data Requirements

| ID | Data Entity / Object | Requirement |
|---|---|---|
| DR-001 | `AuditEvent` | The audit output shall be representable as an `AuditEvent` object, and the published payload shall be a JSON string deserializable by consumers into `AuditEvent`. |
| DR-002 | Event element | Each changed element in an `AuditEvent` shall support `name`, `updatedValue`, `previousValue`, and `metadata.fqdn`. |
| DR-003 | `AuditorEventConfig` | The audit request configuration shall support `applicationName`, `eventSource`, `eventSubType`, `metadata`, and `filters.element` options including `enabled`, `types`, and `includes`. |
| DR-004 | Domain object inputs | System input domain objects may contain UUIDs, nullable and non-null scalar fields, maps, lists, and nested objects. |

## 7. System Constraints

| ID | Constraint |
|---|---|
| C-001 | The product is constrained to a Kotlin client-library implementation for JVM application integration rather than a standalone end-user application. |
| C-002 | Event delivery depends on externally provided infrastructure implementations for publishing and logging. |
| C-003 | The default event-stream transport is Kafka, although publication is abstracted through `EventPublisher`. |
| C-004 | Supported filtering behavior is constrained to the element-filter configuration evidenced in the reviewed materials, including enablement, type selection, and includes lists. |

## 8. Verification and Acceptance Criteria

| Requirement ID | Verification Method | Acceptance Criteria |
|---|---|---|
| FR-001 | Test | Tests demonstrate that detected differences produce `AuditEvent` records with corresponding `UPDATED`, `CREATED`, and `DELETED` event types as applicable, and that each reported changed element includes correct field name, prior value, updated value, and `metadata.fqdn`. |
| FR-002 | Test | Tests demonstrate that supplied configuration values appear in the emitted `AuditEvent`. |
| FR-003 | Test | Tests demonstrate that when `InclusionFilter` is configured with an `includes` list, only matching elements are present in the emitted `AuditEvent` and non-matching changed elements are absent. |
| FR-004 | Inspection | Source and integration materials show use of `EventPublisher`, and the default implementation shows Kafka-based publication of serialized audit events to a configured topic. |
| NFR-001 | Inspection | Source inspection confirms abstraction-based integration points for publisher, logger, and filter dependencies. |
| NFR-002 | Inspection | Build and source materials confirm JVM-targeted library integration with Java 11 / JVM 11 support. |
| NFR-003 | Test | In the verified single-event scenarios, tests observe one expected matching event and no additional event within a 2-second observation window. |
| DR-001 | Test | A published payload can be parsed as JSON and deserialized without error into `AuditEvent`. |
| DR-002 | Test | Tests confirm that emitted event elements expose `name`, `updatedValue`, `previousValue`, and `metadata.fqdn`. |
| DR-003 | Inspection | Source and tests confirm support for the documented `AuditorEventConfig` fields and filter structure. |
| DR-004 | Inspection | Example models and tests demonstrate acceptance of UUID, scalar, nullable, map, list, and nested-object fields. |
| C-001 | Inspection | Source structure and usage patterns show a code-level library rather than a standalone user application. |
| C-002 | Inspection | Source inspection confirms dependency on externally supplied publisher and logger implementations. |
| C-003 | Inspection | Source and configuration materials confirm Kafka as the default event-stream transport behind `EventPublisher`. |
| C-004 | Inspection | Source and tests confirm supported element-filter configuration options and inclusion-list behavior. |
