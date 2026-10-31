# Software Requirements Specification

## 1. Introduction

### Purpose
This SRS defines repository-specific software requirements for `de1ux/statlord` at commit `2677633e86fa623224308bf35c4a3153c95c0030`, based only on the provided repository evidence.

### Product scope
`statlord` is intended to display realtime data on spare OLEDs, e-paper, LCDs, and browsers. It includes:
- a browser-based editor for creating layouts across displays,
- an API used to post data and register displays,
- a viewer layer described as headless browsers rendering each display’s view.  
Source: [E002]

### Intended audience
- Maintainers and contributors
- Testers and reviewers
- Integrators using the API or browser editor
- Operators deploying the stack

### References
- Repository: https://github.com/de1ux/statlord
- Snapshot: https://github.com/de1ux/statlord/tree/2677633e86fa623224308bf35c4a3153c95c0030
- Evidence sources: [E001], [E002], [E003], [E004], [E005], [E006]

## 2. Overall Description

### Product perspective
The product is a web-based system with:
- a client/editor built with Node.js/npm and deployed as static assets,
- a Python server exposing API-backed data entities,
- a viewer component described as headless browsers rendering display output.  
Sources: [E001], [E002], [E005], [E006]

### Product functions summary
- Accept data posted to an API for use in displays. [E002]
- Allow displays to be registered with a unique name and resolution. [E002]
- Allow layouts to be created for different displays. [E002]
- Support positioning text, gauges, and other data across multiple displays. [E002]
- Render what each display “sees” through viewer instances. [E002]

### User classes
- Browser editor users creating and configuring layouts. [E002]
- API clients posting data and registering displays. [E002]
- Operators/developers running the stack locally or in a containerized environment. [E001], [E002]

### Operating environment
- Development dependencies: PostgreSQL, Python `>3.5`, Node.js, npm. [E002]
- Containerized build/runtime evidence: `python:3.7`, Node.js, curl, Python package installation, static client build, Django development server startup. [E001]
- Browser access is required for the editor workflow. [E002]

### Assumptions and dependencies
- PostgreSQL is a required dependency for development. [E002]
- The client build depends on Node.js and npm. [E001], [E002]
- The server depends on Python and installed Python requirements. [E001], [E002]
- The product depends on display definitions and layout data being supplied through the API/editor workflow. [E002], [E005], [E006]

## 3. External Interface Requirements

### User interfaces
| Interface | Description | Source |
|---|---|---|
| Browser editor | Users open the editor and follow a wizard to create layouts. | [E002] |
| Display-oriented layout editing | The editor is used to create layouts of different displays and position text, gauges, and other data across multiple displays. | [E002] |

### Software/API interfaces
| Interface | Description | Source |
|---|---|---|
| Gauge resource | API-backed data object with fields `key`, `value`. | [E005], [E006] |
| Display resource | API-backed data object with fields `key`, `available`, `resolution_x`, `resolution_y`, `current_layout`, `display_data`, `rotation`. | [E005], [E006] |
| Layout resource | API-backed data object with fields `key`, `data`, `display_positions`. | [E005], [E006] |

### Communication interfaces
| Interface | Description | Evidence Type | Source |
|---|---|---|---|
| Web/API communication | Browser usage, API posting, and Django server execution imply a web-based client/server interface. Specific protocol details are not directly stated. | inferred | [E001], [E002], [E005] |

### Data exchange formats
| Format | Description | Evidence Type | Source |
|---|---|---|---|
| Structured resource payloads | API exchanges data matching the Gauge, Display, and Layout field sets. Concrete wire format is not directly evidenced. | explicit for fields, inferred for payload exchange | [E004], [E005], [E006] |
| Static web assets | Client build output is copied to server static content. | explicit | [E001] |

## 4. Functional Requirements

| ID | Requirement | Trigger/Input | System behavior | Output | Priority | Verification | Source evidence |
|---|---|---|---|---|---|---|---|
| FR-001 | The system shall provide an API-capable gauge data resource containing `key` and `value` fields for posted data used by displays. | API client submits or retrieves gauge data. | The system shall represent gauge data using the fields `key` and `value`. | Gauge resource data with `key` and `value`. | High | Inspection | [E002], [E005], [E006] |
| FR-002 | The system shall allow displays to be registered through the API with a unique key and resolution information. | API client registers a display. | The system shall maintain display records including `key`, `resolution_x`, and `resolution_y`. | A display resource containing identification and resolution fields. | High | Inspection | [E002], [E005], [E006] |
| FR-003 | The system shall maintain display state data for registered displays. | API client creates or updates a display record. | The system shall represent display state using `available`, `current_layout`, `display_data`, and `rotation` in addition to display identity and resolution. | Display resource data reflecting state fields. | Medium | Inspection | [E005], [E006] |
| FR-004 | The system shall provide a browser-based editor workflow for creating display layouts. | User opens the editor in a browser. | The system shall present an editor used to create layouts for different displays. | Editable layout configuration in the browser. | High | Demonstration | [E002] |
| FR-005 | The system shall support layout definitions that position content across multiple displays. | User configures a layout in the editor. | The system shall support layouts that position text, gauges, and other data across multiple displays. | Layout definition spanning one or more displays. | High | Demonstration | [E002] |
| FR-006 | The system shall represent layouts with `key`, `data`, and `display_positions` fields. | Layout is created, stored, or retrieved. | The system shall maintain layout records with those fields. | Layout resource data with `key`, `data`, `display_positions`. | High | Inspection | [E005], [E006] |
| FR-007 | The system shall render the view associated with each display through viewer instances. | A display has data/layout to render. | The viewer subsystem shall render what each display “sees”. | Per-display rendered output. | Medium | Demonstration | [E002] |

## 5. Non-Functional Requirements

| ID | Requirement | Priority | Verification | Evidence Type | Source evidence |
|---|---|---|---|---|---|
| NFR-001 | The system shall be compatible with a runtime/deployment environment that provides Python 3.7, Node.js, and npm when built from the supplied container definition. | Medium | Inspection | explicit | [E001] |
| NFR-002 | The development environment shall be compatible with PostgreSQL, Python greater than 3.5, Node.js, and npm. | Medium | Inspection | explicit | [E002] |

## 6. Data Requirements

### Data entities / objects
| Entity | Fields evidenced | Notes | Source |
|---|---|---|---|
| Gauge | `key`, `value` | `key` is the primary key; `value` max length 600 in model. | [E005], [E006] |
| Display | `key`, `available`, `resolution_x`, `resolution_y`, `current_layout`, `display_data`, `rotation` | `key` is the primary key; `current_layout` references `Layout` and may be null. | [E005], [E006] |
| Layout | `key`, `data`, `display_positions` | `key` is the primary key; `data` is stored as binary; `display_positions` is text. | [E005], [E006] |

### Input/output data
| Data | Direction | Description | Source |
|---|---|---|---|
| Gauge data | Input/Output | Posted and retrieved data item identified by `key` and `value`. | [E002], [E005], [E006] |
| Display registration data | Input/Output | Unique display key and display resolution values, plus state fields. | [E002], [E005], [E006] |
| Layout data | Input/Output | Layout identifier, binary `data`, and `display_positions`. | [E005], [E006] |

### Storage, integrity, retention, privacy, migration
| Topic | Requirement / observation | Source |
|---|---|---|
| Storage | The system stores Gauge, Display, and Layout entities in persistent server-side models. | [E006] |
| Referential integrity | A Display may reference a Layout through `current_layout`; if the Layout is deleted, the reference is set to null. | [E006] |
| Privacy / retention / migration | No repository evidence supports specific privacy, retention, or migration requirements. | — |

## 7. Constraints

| ID | Constraint | Source |
|---|---|---|
| C-001 | Development requires PostgreSQL, Python `>3.5`, Node.js, and npm. | [E002] |
| C-002 | The supplied container definition uses `python:3.7` as the base image. | [E001] |
| C-003 | The client must be built before server packaging, using `npm install` and `npm run build`. | [E001] |
| C-004 | Built client assets are served from server static content. | [E001] |
| C-005 | The supplied runtime command starts the server with `./manage.py runserver`. | [E001] |

## 8. Verification and Acceptance

| Requirement ID | Verification method | Acceptance basis |
|---|---|---|
| FR-001 | Inspection | API/data model evidence shows gauge resource fields `key` and `value`. |
| FR-002 | Inspection | API/data model evidence shows display registration fields including unique key and resolution. |
| FR-003 | Inspection | API/data model evidence shows display state fields. |
| FR-004 | Demonstration | A reviewer can open the editor workflow in a browser-based system context. |
| FR-005 | Demonstration | A reviewer can show layout configuration across multiple displays with positioned content. |
| FR-006 | Inspection | API/data model evidence shows layout fields `key`, `data`, `display_positions`. |
| FR-007 | Demonstration | A reviewer can show per-display rendered output by viewer instances. |
| NFR-001 | Inspection | Container definition shows required runtime/build environment components. |
| NFR-002 | Inspection | README lists required development dependencies. |

## 9. Traceability Matrix

| ID | Requirement | Type | Source | Evidence Type | Verification | Confidence |
|---|---|---|---|---|---|---|
| FR-001 | API-capable gauge resource with `key` and `value` | Functional | [E002], [E005], [E006] | explicit | Inspection | High |
| FR-002 | Display registration with unique key and resolution | Functional | [E002], [E005], [E006] | explicit | Inspection | High |
| FR-003 | Display state data fields maintained | Functional | [E005], [E006] | explicit | Inspection | High |
| FR-004 | Browser-based editor workflow | Functional | [E002] | explicit | Demonstration | Medium |
| FR-005 | Multi-display layout configuration with positioned content | Functional | [E002] | explicit | Demonstration | Medium |
| FR-006 | Layout resource with `key`, `data`, `display_positions` | Functional | [E005], [E006] | explicit | Inspection | High |
| FR-007 | Viewer renders each display’s view | Functional | [E002] | explicit | Demonstration | Medium |
| NFR-001 | Compatibility with Python 3.7, Node.js, npm in container build/runtime | Non-functional | [E001] | explicit | Inspection | High |
| NFR-002 | Development compatibility with PostgreSQL, Python >3.5, Node.js, npm | Non-functional | [E002] | explicit | Inspection | High |
