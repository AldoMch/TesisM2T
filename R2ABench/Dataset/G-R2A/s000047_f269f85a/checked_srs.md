# Software Requirements Specification

## 1. Introduction

### Purpose
This SRS defines the checked software requirements for the `archifiltre-docs` repository snapshot at commit `a93230c0fa557fc0652703bdf2d105788b453aa8`. It covers the subset of behavior addressed in this document: settings sanitization, export generation, hash computation, and language-parameter passing.

### Product Scope
This SRS covers only settings sanitization, export generation, hash computation, and language-parameter passing behavior addressed by the documented repository material. Archifiltre itself is an Electron desktop application for visualizing and improving file trees; broader capabilities such as file-tree loading, visualization, tag/comment user interfaces, search, and navigation are outside this document's scope.

### Intended Audience
This document is intended for:
- Maintainers of the desktop application and export workflows
- Test engineers validating settings, export, and hash-processing behavior
- Integrators and architects working from the documented application subset

### References
- Repository: `SocialGouv/archifiltre-docs`
- Product: `archifiltre-docs`

## 2. Overall Description

### Product Perspective
The documented product behavior is organized as controller-level workflows that invoke background worker or batch-processing mechanisms for export and hash-related operations. It also includes sanitization logic for persisted user settings within an Electron desktop application context.

### Product Functions Summary
The system supports the following functions within the scope of this SRS:
- Sanitize persisted user settings and apply defaults when input is empty, undefined, or invalid
- Generate a tree CSV export asynchronously
- Generate a RESIP export asynchronously
- Generate CSV exports from files, metadata, aliases, comments, tags, and hashes
- Generate Excel exports from CSV-export-compatible data
- Compute hashes in batches for submitted paths
- Write hash debug output files under the application user data directory
- Include the translation module's current language value in export worker inputs

### User Classes
- End users whose preferences are persisted as application settings
- Operators or integrators who trigger export and hash-generation workflows through application interfaces

### Operating Environment
- Electron desktop application runtime
- Runtime environment with access to the application user data directory
- Execution environment supporting background worker, child-process, observable, or stream-like result delivery mechanisms

### Assumptions and Dependencies
- Export generation depends on the current `language` value provided by the translation module
- Hash computation depends on filesystem paths and an application-specific user data directory
- Export and hash workflows depend on worker-based or batch-processing utilities provided by the application

## 3. External Interface Requirements

### User Interfaces
No direct end-user interface behavior is specified in this document.

### Software/API Interfaces
| Interface | Description |
|---|---|
| User settings sanitization | Accept persisted settings input and return normalized settings with defaults when needed |
| Tree CSV export generation | Accept a files-and-folders map and return asynchronous progress and export results |
| RESIP export generation | Accept files, metadata, aliases, comments, and tags and return asynchronous progress and export results |
| Hash computation | Accept file paths and base path options and return a data-processing stream while writing debug outputs |
| CSV export generation | Accept aliases, comments, files, metadata, tags, hashes, and language context for export generation |
| Excel export generation | Accept CSV-export-compatible data and return asynchronous export results |

### Communication Interfaces
| Interface | Requirement |
|---|---|
| Background worker invocation | Export and hash workflows shall use background worker, child-process, or batch-processing mechanisms rather than only direct synchronous computation |
| Observable or stream-like delivery | Tree CSV, RESIP, CSV/Excel export, and hash computation workflows shall expose asynchronous results through Observable or stream-like interfaces |

### Data Exchange Formats
| Format | Usage |
|---|---|
| CSV text | Tree export and CSV export outputs |
| Excel export data | Excel export generated from CSV-export-compatible input data |
| RESIP export data | RESIP export workflow output |
| Hash maps | Batch hash computation result aggregation |

## 4. Functional Requirements

| ID | Description | Trigger/Input | System Behavior | Output | Priority | Verification |
|---|---|---|---|---|---|---|
| FR-001 | Sanitize empty persisted settings | Persisted settings value is `{}`, `""`, or `undefined` | The system shall return a settings object with `isTrackingEnabled: true`, `isMonitoringEnabled: true`, and `language: "en"`. | Normalized settings object | High | Test |
| FR-002 | Sanitize invalid persisted settings values | Persisted settings contain invalid boolean or language values | The system shall replace invalid values with supported defaults while preserving valid values. | Normalized settings object containing valid booleans and language | High | Test |
| FR-003 | Generate tree CSV export asynchronously | A files-and-folders map is submitted for tree export | The system shall start background worker processing and emit computation updates, with the export string emitted last. | Progress emissions followed by final tree CSV export string | High | Demonstration |
| FR-004 | Include language in tree CSV export worker input | Tree CSV export is started | The system shall include the translation module's current language value in the tree CSV export worker input. | Tree CSV export request includes language context | Medium | Inspection |
| FR-005 | Generate RESIP export asynchronously | RESIP export is requested with files/folders, metadata, aliases, comments, and tags | The system shall start the RESIP background worker; during processing, the worker emits progress results containing counts and an empty RESIP CSV, and on completion emits a result containing the final RESIP CSV. The controller shall filter worker result messages and map the output `result` payload. | RESIP progress updates and final export result | High | Demonstration |
| FR-006 | Generate CSV export | CSV export is requested with supported export inputs | The system shall pass the export data and the translation module's current language value to the CSV export worker. | CSV export result delivered asynchronously | High | Inspection |
| FR-007 | Generate Excel export | Excel export is requested with `CsvExporterData` | The system shall pass the export data and the translation module's current language value to the Excel export worker. | Excel export result delivered asynchronously | High | Inspection |
| FR-008 | Compute hashes in batches | A set of paths and a base path are submitted for hash computation | The system shall invoke batch hash computation with the provided paths and base path and aggregate hash results. | Hash processing stream and merged hash map results | High | Inspection |
| FR-009 | Write hash debug outputs | Hash computation is executed | The system shall create buffered file writers for `hash-result-debug` and `hash-error-debug` in the application user data path. | Debug files for hash results and hash errors | Medium | Inspection |

## 5. Non-Functional Requirements

| ID | Quality Attribute | Requirement | Priority | Verification |
|---|---|---|---|---|
| NFR-001 | Performance/Responsiveness | Export generation workflows shall execute asynchronously through a background worker or child process and deliver progress or results through an Observable; this is expected to reduce the risk of main-thread blocking. | High | Inspection |
| NFR-002 | Performance/Scalability | Hash computation shall process inputs in batches rather than as a single unpartitioned operation. | Medium | Inspection |
| NFR-003 | Reliability | User settings handling shall return a valid settings object with defaults when persisted values are empty, undefined, or invalid. | High | Test |
| NFR-004 | Portability | Hash debug artifacts shall be stored under the runtime-provided application user data directory. | Medium | Inspection |

## 6. Data Requirements

| ID | Data Item | Requirement |
|---|---|---|
| DR-001 | User settings | The settings data model shall include `isTrackingEnabled`, `isMonitoringEnabled`, and `language`. |
| DR-002 | CSV export input | CSV export input shall include aliases, comments, files and folders, files-and-folders metadata, tags, and hashes. |
| DR-003 | RESIP export input | RESIP export input shall include files and folders, metadata, aliases, comments, and tags. |
| DR-004 | Excel export input | Excel export input shall conform to `CsvExporterData`. |
| DR-005 | Hash computation input | Hash computation input shall include `paths` and `basePath`. |
| DR-006 | Hash computation output | Hash computation shall aggregate results into hash maps. |
| DR-007 | Tree export output | Tree export output shall be an export string emitted after intermediate computation updates. |
| DR-008 | Hash debug files | Hash computation shall produce debug files named `hash-result-debug` and `hash-error-debug`. |
| DR-009 | Debug file storage location | Hash debug files shall be written to the application user data directory. |

## 7. System Constraints

| ID | Constraint |
|---|---|
| C-001 | The documented behavior depends on Electron application runtime services, including access to `app.getPath("userData")`. |
| C-002 | Export generation depends on the current `language` value provided by the translation module, rather than an independent language-switching or propagation mechanism. |
| C-003 | Export and hash workflows are implemented through background worker, child-process, or batch-processing utilities. |

## 8. Verification and Acceptance Criteria

| Requirement ID | Verification Method | Acceptance Criterion |
|---|---|---|
| FR-001 | Test | Automated tests confirm defaults for `{}`, `""`, and `undefined` are `isTrackingEnabled: true`, `isMonitoringEnabled: true`, and `language: "en"`. |
| FR-002 | Test | Automated tests confirm invalid values are replaced by valid defaults while valid values are preserved. |
| FR-003 | Demonstration | A tree export run emits intermediate updates and a final CSV string. |
| FR-004 | Inspection | Source inspection confirms the tree CSV export worker input includes the translation module's current language value. |
| FR-005 | Demonstration | A RESIP export run shows in-progress results with counts and an empty RESIP CSV, then a final result containing the completed RESIP CSV; source inspection confirms filtering and mapping of worker result messages. |
| FR-006 | Inspection | Source inspection confirms CSV export accepts the documented input set and passes both export data and the translation module's current language value to the worker. |
| FR-007 | Inspection | Source inspection confirms Excel export accepts `CsvExporterData` and passes both export data and the translation module's current language value to the worker. |
| FR-008 | Inspection | Source inspection confirms batch-based hash computation using submitted `paths` and `basePath`, with aggregated hash-map output. |
| FR-009 | Inspection | Source inspection confirms debug writers target `hash-result-debug` and `hash-error-debug` under the application user data directory. |
| NFR-001 | Inspection | Source inspection confirms export workflows use a background worker or child process and return progress or results through an Observable interface. |
| NFR-002 | Inspection | Source inspection confirms hash computation uses batch-oriented processing. |
| NFR-003 | Test | Automated tests confirm the system returns a valid settings object from empty, undefined, and invalid persisted inputs. |
| NFR-004 | Inspection | Source inspection confirms hash debug artifacts are written under the runtime-provided application user data directory. |
