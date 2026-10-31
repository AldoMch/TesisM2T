# Software Requirements Specification

## 1. Introduction

### Purpose
This SRS defines evidence-backed requirements for the repository component at commit `a93230c0fa557fc0652703bdf2d105788b453aa8`, focusing on persistent user settings, hash computation, and export generation workflows supported by the available evidence.

### Product Scope
The product scope evidenced here covers:
- sanitization of persisted user settings,
- asynchronous generation of tree CSV, CSV, Excel, and RESIP exports,
- batch hash computation with debug output files,
- propagation of language settings into export generation workflows.

### Intended Audience
This document is intended for maintainers, testers, integrators, and reviewers working on the evidenced repository behavior.

### References
- Repository: `SocialGouv/archifiltre-docs`
- Snapshot: `https://github.com/SocialGouv/archifiltre-docs/tree/a93230c0fa557fc0652703bdf2d105788b453aa8`
- Evidence sources: `E001` to `E006`

## 2. Overall Description

### Product Perspective
The evidenced product behavior is organized as controller-level workflows that invoke background worker processes for export and hash-related operations. It also includes persistence-related sanitization for user settings. `E001 E002 E003 E004 E005 E006`

### Product Functions Summary
- Sanitize persisted user settings and apply defaults when input is empty, undefined, or invalid. `E001`
- Generate a tree CSV export asynchronously. `E002`
- Generate a RESIP export asynchronously with progress/result processing. `E003`
- Compute hashes in batches and write debug outputs under the application user data directory. `E004`
- Generate CSV exports from files, metadata, aliases, comments, tags, and hashes. `E005`
- Generate Excel exports from CSV-export-compatible data. `E006`

### User Classes
- End users whose preferences are persisted as settings for tracking, monitoring, and language. `E001`
- Operators or integrators who trigger export and hash generation workflows using repository-provided interfaces. `E002 E003 E004 E005 E006`

### Operating Environment
- Desktop application runtime with access to Electron `remote.app.getPath("userData")`. `E004`
- Execution environment supporting background worker processing and observable-based result delivery. `E002 E003 E005 E006`

### Assumptions and Dependencies
- Export generation depends on a current language value from the translation subsystem. `E002 E003 E005 E006`
- Hash computation depends on filesystem paths and an application-specific user data directory. `E004`

## 3. External Interface Requirements

### User Interfaces
No direct user interface behavior is evidenced in the provided material.

### Software/API Interfaces
| Interface | Description | Evidence |
|---|---|---|
| User settings sanitization | Accepts persisted settings input and returns normalized settings with defaults when needed. | E001 |
| Tree CSV export generation | Accepts a files-and-folders map and returns asynchronous export progress/results. | E002 |
| RESIP export generation | Accepts files, metadata, aliases, comments, and tags and returns asynchronous progress/results. | E003 |
| Hash computation | Accepts file paths and base path options and returns a data processing stream while writing debug outputs. | E004 |
| CSV export generation | Accepts aliases, comments, files, metadata, tags, hashes, and language-dependent context for export generation. | E005 |
| Excel export generation | Accepts CSV-export-compatible data and returns asynchronous export results. | E006 |

### Communication Interfaces
| Interface | Requirement | Evidence |
|---|---|---|
| Background worker invocation | Export and hash workflows shall use background worker or batch-processing mechanisms rather than only direct synchronous computation. | E002 E003 E004 E005 E006 |
| Observable/data stream delivery | Tree CSV, RESIP, and Excel/CSV-related workflows shall expose asynchronous results through observable or stream-like interfaces. | E002 E003 E004 E006 |

### Data Exchange Formats
| Format | Usage | Evidence |
|---|---|---|
| CSV text | Tree export and CSV export outputs. | E002 E005 |
| Excel export data | Excel export generated from CSV-export-compatible input data. | E006 |
| RESIP export data | RESIP export workflow output. | E003 |
| Hash maps | Batch hash computation result aggregation. | E004 |

## 4. Functional Requirements

| ID | Description | Trigger/Input | System Behavior | Output | Priority | Verification | Source Evidence |
|---|---|---|---|---|---|---|---|
| FR-001 | The system shall sanitize persisted user settings and apply defaults when the input is empty, an empty string, or undefined. | Persisted settings value is `{}`, `""`, or `undefined`. | Return a settings object with `isTrackingEnabled: true`, `isMonitoringEnabled: true`, and `language: "en"`. | Normalized settings object. | High | Test | E001 |
| FR-002 | The system shall sanitize invalid persisted setting values before use. | Persisted settings contain invalid booleans or invalid language values. | Replace invalid values with supported defaults while preserving valid values. | Normalized settings object containing valid booleans and language. | High | Test | E001 |
| FR-003 | The system shall generate a tree CSV export asynchronously from a files-and-folders map. | A files-and-folders map is submitted for tree export. | Start background worker processing and emit updates as files are computed, with the export string emitted last. | Progress emissions followed by final tree CSV export string. | High | Demonstration | E002 |
| FR-004 | The system shall propagate the current language into tree CSV export generation. | Tree CSV export is started. | Include the current translation language in the worker input. | Tree CSV export generated using the current language context. | Medium | Inspection | E002 |
| FR-005 | The system shall generate a RESIP export asynchronously from file structure and metadata inputs. | RESIP export is requested with files/folders, metadata, aliases, comments, and tags. | Start background worker processing and map/filter worker results into RESIP export progress and output. | RESIP progress updates and final export result. | High | Demonstration | E003 |
| FR-006 | The system shall generate a CSV export from files, metadata, aliases, comments, tags, and hashes. | CSV export is requested with the supported export option set. | Pass the export data and current language into background worker processing. | CSV export result delivered asynchronously. | High | Inspection | E005 |
| FR-007 | The system shall generate an Excel export from CSV-export-compatible input data. | Excel export is requested with `CsvExporterData`. | Pass the data and current language into background worker processing. | Excel export result delivered asynchronously. | High | Inspection | E006 |
| FR-008 | The system shall compute hashes in batches for the requested paths. | A set of paths and a base path are submitted for hash computation. | Invoke batch hash computation with the provided paths and base path and aggregate hash results. | Hash processing stream and merged hash map results. | High | Inspection | E004 |
| FR-009 | The system shall write hash debug outputs under the application user data directory. | Hash computation is executed. | Create buffered file writers for `hash-result-debug` and `hash-error-debug` in the Electron user data path. | Debug files for hash results and hash errors. | Medium | Inspection | E004 |

## 5. Non-Functional Requirements

| ID | Requirement | Quality Attribute | Priority | Verification | Evidence | Confidence |
|---|---|---|---|---|---|---|
| NFR-001 | Export generation workflows shall execute asynchronously through background worker processing and provide non-blocking progress or result delivery mechanisms. | Performance/Responsiveness | High | Inspection | E002 E003 E005 E006 | Explicit |
| NFR-002 | Hash computation shall process inputs in batches rather than as a single unpartitioned operation. | Performance/Scalability | Medium | Inspection | E004 | Explicit |
| NFR-003 | User settings handling shall be resilient to empty, undefined, and invalid persisted values by returning a valid settings object with defaults. | Reliability | High | Test | E001 | Explicit |
| NFR-004 | Hash debug artifacts shall be stored under the runtime-provided application user data directory to preserve environment portability across installations. | Portability | Medium | Inspection | E004 | Inferred |

## 6. Data Requirements

| Category | Requirement | Evidence |
|---|---|---|
| Data entities | User settings shall include `isTrackingEnabled`, `isMonitoringEnabled`, and `language`. | E001 |
| Data entities | CSV export input shall include aliases, comments, files and folders, files and folders metadata, tags, and hashes. | E005 |
| Data entities | RESIP export input shall include files and folders metadata, aliases, comments, files and folders, and tags. | E003 |
| Data entities | Excel export input shall conform to `CsvExporterData`. | E006 |
| Data entities | Hash computation input shall include `paths` and `basePath`; output aggregation shall produce hash maps. | E004 |
| Input/output data | Tree export output shall be an export string emitted after intermediate computation updates. | E002 |
| Input/output data | Hash computation shall produce debug result and error files named `hash-result-debug` and `hash-error-debug`. | E004 |
| Storage | Debug files for hash computation shall be written to the application user data directory. | E004 |

## 7. Constraints

| ID | Constraint | Evidence |
|---|---|---|
| C-001 | The product behavior evidenced here depends on Electron application runtime services, specifically `remote.app.getPath("userData")`. | E004 |
| C-002 | Export generation is coupled to a translation subsystem that provides a current `language` value. | E002 E003 E005 E006 |
| C-003 | Export and hash workflows are implemented through background worker or batch-processing utilities. | E002 E003 E004 E005 E006 |
| C-004 | Verification of settings sanitization relies on automated tests covering empty and invalid persisted values. | E001 |

## 8. Verification and Acceptance

| Requirement ID | Verification Method | Acceptance Basis |
|---|---|---|
| FR-001 | Test | Automated tests confirm defaults for `{}`, `""`, and `undefined`. |
| FR-002 | Test | Automated tests confirm invalid values are replaced by valid defaults. |
| FR-003 | Demonstration | A run emits intermediate updates and a final tree CSV string. |
| FR-004 | Inspection | Source inspection confirms current language is included in tree export worker input. |
| FR-005 | Demonstration | A run shows asynchronous RESIP processing and final result emission. |
| FR-006 | Inspection | Source inspection confirms CSV export accepts the documented input set and uses background worker processing. |
| FR-007 | Inspection | Source inspection confirms Excel export accepts `CsvExporterData` and uses background worker processing. |
| FR-008 | Inspection | Source inspection confirms batch-based hash computation with base path input and result aggregation. |
| FR-009 | Inspection | Source inspection confirms debug writers target `hash-result-debug` and `hash-error-debug` under user data. |
| NFR-001 | Inspection | Source inspection confirms background worker usage and asynchronous result interfaces. |
| NFR-002 | Inspection | Source inspection confirms batch size configuration for hash computation. |
| NFR-003 | Test | Automated tests confirm valid settings object output from invalid or empty persisted inputs. |
| NFR-004 | Inspection | Source inspection confirms use of runtime user data directory for debug artifacts. |

## 9. Traceability Matrix

| ID | Requirement | Type | Source | Evidence Type | Verification | Confidence |
|---|---|---|---|---|---|---|
| FR-001 | Sanitize empty persisted settings to defaults | Functional | E001 | Explicit | Test | High |
| FR-002 | Sanitize invalid persisted setting values | Functional | E001 | Explicit | Test | Medium |
| FR-003 | Asynchronous tree CSV export with progress and final string | Functional | E002 | Explicit | Demonstration | High |
| FR-004 | Propagate language into tree CSV export generation | Functional | E002 | Explicit | Inspection | High |
| FR-005 | Asynchronous RESIP export from supported input sets | Functional | E003 | Explicit | Demonstration | Medium |
| FR-006 | CSV export from files, metadata, aliases, comments, tags, and hashes | Functional | E005 | Explicit | Inspection | High |
| FR-007 | Excel export from `CsvExporterData` | Functional | E006 | Explicit | Inspection | High |
| FR-008 | Batch hash computation for submitted paths | Functional | E004 | Explicit | Inspection | High |
| FR-009 | Write hash debug outputs to application user data directory | Functional | E004 | Explicit | Inspection | High |
| NFR-001 | Asynchronous background-worker-based export processing | Non-functional | E002 E003 E005 E006 | Explicit | Inspection | High |
| NFR-002 | Batch-oriented hash processing | Non-functional | E004 | Explicit | Inspection | High |
| NFR-003 | Resilient settings handling for invalid persisted values | Non-functional | E001 | Explicit | Test | High |
| NFR-004 | Portable placement of hash debug artifacts in user data directory | Non-functional | E004 | Inferred | Inspection | Medium |
