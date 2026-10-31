# Software Requirements Specification

## 1. Introduction

### Purpose
This SRS defines the software requirements for `de1ux/statlord` at commit `2677633e86fa623224308bf35c4a3153c95c0030`.

### Product scope
`statlord` is intended to display realtime data on spare OLEDs, e-paper, LCDs, and browsers. It includes:
- a browser-based editor for creating layouts across displays,
- an API used to post data and register displays,
- a viewer layer for rendering each display’s view.

The current containerized deployment is development-grade and shall not be interpreted as production-ready.

### Intended audience
This document is intended for:
- Maintainers and contributors
- Testers and reviewers
- Integrators using the API or browser editor
- Operators deploying or evaluating the stack

### References
- Repository: `de1ux/statlord`

## 2. Overall Description

### Product perspective
The product is a web-based system comprising:
- a client/editor built with Node.js and npm and deployed as static assets,
- a Python server exposing API-backed data entities,
- a viewer component for rendering display output.

The client/editor is a TypeScript/React single-page application that uses a Redux store to manage controls, elements, layouts, gauges, and display device state, and supports layout editing, render requests, and delete requests through canvas-related operations.

### Product functions summary
The system supports:
- accepting posted data for use in displays,
- registering displays with a unique identifier and resolution,
- creating layouts for different displays,
- positioning text, gauges, and other data across multiple displays,
- rendering display-oriented views through the viewer path.

### User classes
- Browser editor users creating and configuring layouts
- API clients posting data and registering displays
- Operators and developers running the stack locally or in a containerized environment

### Operating environment
- Development dependencies include PostgreSQL, Python greater than 3.5, Node.js, and npm.
- The supplied containerized environment uses Python 3.7, Node.js, npm, Python package installation, static client build steps, and Django server startup.
- Browser access is required for the editor workflow.

### Assumptions and dependencies
- PostgreSQL is required for development.
- The client build depends on Node.js and npm.
- The server depends on Python and installed Python package requirements.
- The product depends on display definitions and layout data being supplied through the API and editor workflow.

## 3. External Interface Requirements

### User interfaces
| Interface | Requirement summary |
|---|---|
| Browser editor | The system shall provide a browser-based editor for creating and editing display layouts. |
| Layout editing interface | The editor shall allow users to position text, gauges, and other data across multiple displays. |
| Viewer interface | The system shall provide a viewer path for display-oriented rendering. |

### Software/API interfaces
| Interface | Requirement summary |
|---|---|
| Gauge resource | The system shall expose or process a gauge data resource containing `key` and `value` fields. |
| Display resource (server-side) | The server-side display resource shall include `key`, `available`, `resolution_x`, `resolution_y`, `current_layout`, `display_data`, and `rotation`. |
| Display state (client-side) | The client-side display state shall include `key`, `available`, `resolution_x`, `resolution_y`, `display_data`, and `rotation`. |
| Layout resource | The system shall expose or process a layout resource containing `key`, `data`, and `display_positions`. |
| Editor state management | The client/editor shall use Redux-managed state for controls, elements, layouts, gauges, and displays. |

### Communication interfaces
| Interface | Requirement summary |
|---|---|
| Web/API communication | The system shall provide browser-based client/server communication for editor access, API usage, and viewer access. |

### Data exchange formats
| Format/item | Requirement summary |
|---|---|
| Structured resource payloads | The system shall exchange structured data matching the documented Gauge, Display, and Layout field sets. |
| Static web assets | The client build output shall be deployed as server-served static assets. |

## 4. Functional Requirements

| ID | Description | Trigger/Input | System behavior | Output | Priority | Verification |
|---|---|---|---|---|---|---|
| FR-001 | Gauge data resource | API client submits or retrieves gauge data | The system shall represent gauge data using the fields `key` and `value`. | Gauge resource data with `key` and `value` | High | Inspection |
| FR-002 | Display registration | API client registers a display | The system shall maintain display records including `key`, `resolution_x`, and `resolution_y`. | A display resource containing identifier and resolution fields | High | Inspection |
| FR-003 | Display state management | API client creates, updates, or retrieves a display record | The system shall represent server-side display state using `available`, `current_layout`, `display_data`, and `rotation` in addition to identifier and resolution fields. The client-side display state may omit `current_layout`. | Display resource and client state reflecting supported fields | Medium | Inspection |
| FR-004 | Browser-based editor workflow | User opens the editor in a browser | The system shall provide a TypeScript/React single-page editor that supports layout creation and editing through Redux-managed state for controls, elements, layouts, gauges, and displays. | Editable layout configuration in the browser | High | Demonstration |
| FR-005 | Multi-display layout composition | User configures a layout in the editor | The system shall support layouts that position text, gauges, and other data across multiple displays and shall support canvas-related render and delete operations during editing. | Layout definition spanning one or more displays | High | Demonstration |
| FR-006 | Layout data representation | Layout is created, stored, or retrieved | The system shall maintain layout records with `key`, `data`, and `display_positions` fields. | Layout resource data with `key`, `data`, and `display_positions` | High | Inspection |
| FR-007 | Viewer rendering path | A display has data or layout to render | The system shall provide a viewer behavior that reads display data and generates a black-and-white pixel view rendered at the display resolution. Full headless-browser automated rendering requires separate verification. | Per-display rendered output through the viewer path | Medium | Demonstration |

## 5. Non-Functional Requirements

| ID | Quality attribute | Requirement | Priority | Verification |
|---|---|---|---|---|
| NFR-001 | Environment compatibility | The system shall be compatible with a runtime and build environment that provides Python 3.7, Node.js, and npm for the supplied containerized setup. | Medium | Inspection |
| NFR-002 | Development environment compatibility | The development environment shall be compatible with PostgreSQL, Python greater than 3.5, Node.js, and npm. | Medium | Inspection |
| NFR-003 | Client architecture consistency | The editor client shall use a Redux-based state management approach for controls, elements, layouts, gauges, and displays. | Medium | Inspection |
| NFR-004 | Deployment maturity | The supplied containerized deployment shall be treated as development-grade rather than production-ready. | High | Inspection |

## 6. Data Requirements

### 6.1 Data entities
| ID | Data item/entity | Requirement |
|---|---|---|
| DR-001 | Gauge | The Gauge entity shall contain `key` and `value`. |
| DR-002 | Display server resource | The server-side Display entity shall contain `key`, `available`, `resolution_x`, `resolution_y`, `current_layout`, `display_data`, and `rotation`. |
| DR-003 | Display client state | The client-side Display state shall contain `key`, `available`, `resolution_x`, `resolution_y`, `display_data`, and `rotation`. |
| DR-004 | Layout | The Layout entity shall contain `key`, `data`, and `display_positions`. |

### 6.2 Data characteristics
| ID | Data item | Requirement |
|---|---|---|
| DR-005 | Gauge value | The Gauge `value` field shall support up to 600 characters. |
| DR-006 | Layout data | The Layout `data` field shall support binary content. |
| DR-007 | Layout display positions | The Layout `display_positions` field shall support text content. |

### 6.3 Data relationships and persistence
| ID | Data relationship | Requirement |
|---|---|---|
| DR-008 | Display to Layout relationship | A Display may reference a Layout through `current_layout`. |
| DR-009 | Display to Layout deletion behavior | If a referenced Layout is deleted, the Display `current_layout` reference shall be set to null. |
| DR-010 | Persistent storage | The system shall persist Gauge, Display, and Layout entities on the server side. |

## 7. System Constraints

| ID | Constraint |
|---|---|
| C-001 | Development requires PostgreSQL, Python greater than 3.5, Node.js, and npm. |
| C-002 | The supplied container definition uses Python 3.7 as the base image. |
| C-003 | The client must be built before server packaging using `npm install` and `npm run build`. |
| C-004 | Built client assets are served from server static content. |
| C-005 | The supplied runtime command starts the server with `./manage.py runserver`. |
| C-006 | The provided containerized deployment is development-grade and not fully production-ready; the Dockerfile starts Django using the development server. |

## 8. Verification and Acceptance Criteria

| Requirement ID | Verification method | Acceptance criterion |
|---|---|---|
| FR-001 | Inspection | The implemented API and data model represent gauge data with `key` and `value`. |
| FR-002 | Inspection | The implemented API and data model support display registration with identifier and resolution fields. |
| FR-003 | Inspection | Server-side display handling includes `available`, `current_layout`, `display_data`, and `rotation`, and client-side display state supports the documented client field set. |
| FR-004 | Demonstration | A reviewer can open the browser editor and observe layout editing supported by Redux-managed state for controls, elements, layouts, gauges, and displays. |
| FR-005 | Demonstration | A reviewer can show layout configuration across multiple displays and observe canvas-related render or delete operations used during editing. |
| FR-006 | Inspection | The implemented API and data model represent layouts with `key`, `data`, and `display_positions`. |
| FR-007 | Demonstration | A reviewer can inspect that the viewer route and browser rendering path can read display data and generate a black-and-white pixel view rendered at the display resolution. Complete headless-browser automated rendering requires separate verification. |
| NFR-001 | Inspection | The supplied build and runtime setup includes Python 3.7, Node.js, and npm. |
| NFR-002 | Inspection | The documented development setup includes PostgreSQL, Python greater than 3.5, Node.js, and npm. |
| NFR-003 | Inspection | The client implementation uses Redux-managed state for controls, elements, layouts, gauges, and displays. |
| NFR-004 | Inspection | The deployment setup uses development-oriented server startup and is documented or constrained as non-production-ready. |
