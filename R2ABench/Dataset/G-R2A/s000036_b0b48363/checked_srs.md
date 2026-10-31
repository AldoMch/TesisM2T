# Checked Software Requirements Specification: HypnoLog Server

## 1. Introduction

### 1.1 Purpose
This Software Requirements Specification defines normalized requirements for HypnoLog Server, a Node.js/Express logging and visualization server. The system receives JSON log messages over HTTP, forwards them to browser clients through Socket.IO, validates incoming browser messages against the HypnoLog Data Object schema, and renders log objects in a browser UI through windows and visualizers.

### 1.2 Scope
The system scope includes:
- HTTP-based log submission from clients implemented in any language or environment capable of sending HTTP requests.
- A JSON logging payload model called the HypnoLog Data Object.
- A Node.js/Express server started through npm or CLI entry points.
- A logging route for JSON POST submissions.
- Browser-based viewing through the server-hosted web UI.
- Socket.IO delivery from the server to connected browser clients.
- Browser-side schema validation and invalid-message wrapping.
- Window dispatch and visualizer dispatch for displaying received log objects.
- Type-based visualizer selection through `canDisplay` and `display` functions.

The system scope does not include explicit requirements for persistence, retention, deletion, privacy controls, authentication, authorization, or migration.

### 1.3 Intended Audience
- Maintainers of HypnoLog Server.
- Integrators building logging clients.
- Users viewing log data through the browser UI.
- Testers verifying HTTP submission, Socket.IO delivery, schema validation, and visualizer rendering.
- Architecture-generation tools consuming a clean SRS without review metadata.

### 1.4 Definitions and Abbreviations
| Term | Definition |
|---|---|
| HypnoLog Data Object | JSON object representing one logged item. |
| Visualizer | Browser-side component that can display selected HypnoLog Data Objects. |
| Window | Browser-side display area that receives data and delegates rendering to visualizers. |
| Socket.IO | Real-time client/server communication library used by the browser and server. |
| Ajv | JSON Schema validator used by the browser client. |
| Logging producer | External client that sends log messages to the server over HTTP. |

## 2. Overall Description

### 2.1 Product Perspective
HypnoLog Server sits between logging producers and browser-based consumers. Logging code sends JSON messages to the server through HTTP. The server forwards received log objects to connected browser clients. Browser clients validate the received objects, keep a received-data list, update the UI state, and pass the objects to windows. Windows delegate rendering to configured visualizers that select whether they can display each object.

In the simplest usage scenario, the logging code, server, and browser can run on the same machine.

### 2.2 Function Summary
The system shall provide:
- HTTP JSON log ingestion.
- JSON parsing for submitted log messages.
- A `/logger/in` endpoint for log submission.
- A `/logger/status` endpoint for status checking.
- Browser web UI access through `/client.html`.
- Socket.IO connection management for display clients.
- Broadcast of submitted log data to connected display clients.
- Browser-side validation of received log objects.
- Conversion of invalid received messages into displayable `HypnoLog-error` objects.
- Window dispatch to all registered windows.
- Visualizer loading from configuration.
- Visualizer selection by the first matching `canDisplay` result.
- Visualizer rendering through `display`.
- Tag and variable-name display handling where supplied by the logged object.

### 2.3 User Classes
| User class | Description |
|---|---|
| Logging client developer | Builds clients that send JSON log objects through HTTP. |
| Visualization user | Uses a browser to view logged data. |
| Visualizer developer | Adds or modifies browser-side visualizers. |
| Server operator | Starts the Node.js server and selects the runtime port. |
| Tester | Verifies ingestion, delivery, validation, and rendering behavior. |

### 2.4 Operating Environment
| Environment aspect | Requirement context |
|---|---|
| Node.js runtime | The server is started with `node ./bin/www`, npm start, or CLI aliases. |
| Express application | HTTP routing, static file hosting, body parsing, and web UI delivery run through Express. |
| HTTP server | The Express app is hosted by a Node HTTP server. |
| Default port | The server listens on port `7000` when no command-line port is provided. |
| Configurable port | The server accepts a command-line port argument. |
| Browser client | The UI runs in a standard browser and loads JavaScript bundles. |
| Socket.IO | The server attaches Socket.IO to the HTTP server; browser clients connect with Socket.IO to the same origin. |
| JSON body parser | The server parses JSON bodies with a configured size limit of `50mb`. |
| Static web files | Browser assets are served from the public web directory. |

### 2.5 Assumptions and Dependencies
| ID | Assumption or dependency |
|---|---|
| AD-001 | Logging producers can send HTTP POST requests. |
| AD-002 | JSON log submissions use `Content-Type: application/json`. |
| AD-003 | Browser users can access the server-hosted UI. |
| AD-004 | Socket.IO client and server libraries are available. |
| AD-005 | The browser can load configured visualizer modules. |
| AD-006 | Visualizers implement `canDisplay(obj)` and `display(obj, callback)`. |
| AD-007 | No server-side schema rejection is required unless later route-level validation is added. |

## 3. External Interface Requirements

### 3.1 User Interfaces
| ID | Interface | Requirement |
|---|---|---|
| UI-001 | Browser web UI | The system shall provide a browser-accessible UI for viewing logged data. |
| UI-002 | Default client page | The server shall expose the browser UI at `/client.html`. |
| UI-003 | Display windows | The browser UI shall display log objects through registered windows. |
| UI-004 | Visualizer output | Visualizers shall create browser-visible HTML elements for matching log objects. |

### 3.2 Software and API Interfaces
| ID | Interface | Requirement |
|---|---|---|
| API-001 | HTTP logging endpoint | Clients shall submit JSON log messages with HTTP POST to `/logger/in`. |
| API-002 | Default local API URL | In the default local configuration, logging clients shall be able to use `http://127.0.0.1:7000/logger/in`. |
| API-003 | HTTP status endpoint | Clients shall be able to request `/logger/status` and receive HTTP status success behavior. |
| API-004 | Socket.IO browser connection | Browser clients shall establish a Socket.IO connection to the same server origin. |
| API-005 | Socket.IO notification event | The server shall send received log objects to browser clients through a Socket.IO `notification` event. |
| API-006 | Visualizer configuration | The browser shall load visualizers from configuration, using default configuration when user configuration is unavailable. |
| API-007 | Visualizer plugin contract | Visualizer modules shall expose `canDisplay` and `display` functions. |
| API-008 | CLI startup aliases | The package shall provide CLI aliases for starting the server. |

### 3.3 Communication Interfaces
| ID | Interface | Requirement |
|---|---|---|
| CI-001 | HTTP POST | Logging producers shall send JSON payloads to the logging endpoint using HTTP POST. |
| CI-002 | JSON request body | The server shall parse JSON request bodies before forwarding them to display clients. |
| CI-003 | Socket.IO delivery | The server shall deliver received data to connected browser clients through Socket.IO; the requirement shall not assume raw WebSocket-only transport. |
| CI-004 | Same-origin browser connection | Browser clients shall connect to the origin from which the UI page was loaded. |

### 3.4 Data Exchange Items
| ID | Data item | Description |
|---|---|---|
| DE-001 | HypnoLog Data Object | JSON object containing at least `data` and `type`. |
| DE-002 | `data` field | Logged value or structure to visualize. |
| DE-003 | `type` field | String used to identify how the log object should be displayed. |
| DE-004 | `tags` field | Optional array used for UI filtering and tag display. |
| DE-005 | `name` field | Optional variable name displayed with a log line. |
| DE-006 | `HypnoLog-error` object | Browser-generated object used when an incoming message fails schema validation. |
| DE-007 | Visualizer DOM element | Browser element generated by a visualizer for display in a window. |

## 4. Functional Requirements

| ID | Requirement | Trigger/Input | Required behavior | Output | Priority | Verification |
|---|---|---|---|---|---|---|
| FR-001 | The system shall accept JSON log submissions over HTTP. | Client sends `POST /logger/in` with `Content-Type: application/json`. | Parse the JSON request body and accept it for forwarding to display clients. | HTTP 200 response and forwarded log object. | High | Test |
| FR-002 | The system shall support language-agnostic log producers. | Producer implemented in any language sends an HTTP JSON request. | Avoid requiring a language-specific client library for basic log submission. | Log submission accepted through HTTP. | High | Analysis |
| FR-003 | The HypnoLog Data Object model shall define `data` and `type` as required fields. | A log object is created or checked against the schema. | Treat `data` and `type` as schema-required fields without asserting server-side rejection. | Object satisfies or violates the data model. | High | Inspection |
| FR-004 | The server shall forward received log bodies to connected browser display clients. | `/logger/in` receives a parsed request body. | Emit the received object to each connected display client using Socket.IO. | Socket.IO `notification` event delivered to clients. | High | Test |
| FR-005 | The browser client shall receive server notifications through Socket.IO. | Browser UI loads and connects to the same server origin. | Create a Socket.IO connection and handle `notification` messages. | Browser-side message handler invocation. | High | Test |
| FR-006 | The browser client shall validate received messages against the HypnoLog Data Object schema. | Socket.IO notification message is received. | Invoke the Ajv-compiled validator on the received message. | Validation result. | High | Test |
| FR-007 | The browser client shall convert invalid received messages into `HypnoLog-error` objects. | Received message fails schema validation. | Wrap validation error details and the received message into a new object with type `HypnoLog-error`. | Displayable error object. | Medium | Test |
| FR-008 | The browser client shall store and display received messages after validation or error wrapping. | A valid object or generated error object is ready. | Append the object to the received-data list, update last-update time, and send it to the window dispatcher. | Updated UI state and display pipeline invocation. | High | Demonstration |
| FR-009 | The system shall render logged objects through registered display windows. | Window dispatcher receives a log object. | Pass the object to each registered window for display. | Window display action. | High | Demonstration |
| FR-010 | The default window shall render log lines through configured visualizers. | Default window receives a log object. | Use a visualizer dispatcher to create a DOM element and append it to the window. | Browser-visible log line. | High | Demonstration |
| FR-011 | The visualizer dispatcher shall select the first visualizer capable of displaying a log object. | A log object is submitted for visualization. | Evaluate visualizers in configured order using `canDisplay(obj)` and call `display` on the first match. | DOM element created by the selected visualizer. | High | Test |
| FR-012 | The visualizer dispatcher shall tolerate visualizer loading failures. | One or more configured visualizers fail to load. | Continue loading other visualizers and ignore failed entries. | Successfully loaded visualizers remain available. | Medium | Inspection |
| FR-013 | The UI shall support tag-based display metadata. | A received log object contains `tags`. | Add tags to the window filter and apply tag-related CSS classes/display text. | Tag-filterable log line. | Medium | Demonstration |
| FR-014 | The UI shall support variable-name display metadata. | A received log object contains `name`. | Prepend a variable-name element to the displayed log line. | Log line with variable-name prefix. | Low | Demonstration |
| FR-015 | The server shall provide a status endpoint. | Client sends request to `/logger/status`. | Respond with HTTP success status. | HTTP 200 response. | Low | Test |
| FR-016 | The server startup script shall open or announce the browser client URL. | Server starts on a selected port. | Build `http://localhost:<port>/client.html`, print the URL, and attempt to open the default browser. | Browser UI URL made available. | Medium | Demonstration |

## 5. Non-Functional Requirements

| ID | Requirement | Quality attribute | Priority | Verification |
|---|---|---|---|---|
| NFR-001 | The logging interface shall be compatible with clients from any language or environment capable of sending HTTP requests with JSON bodies. | Interoperability | High | Analysis |
| NFR-002 | The visualization UI shall operate in a standard browser. | Usability | High | Demonstration |
| NFR-003 | The browser communication requirement shall be expressed as Socket.IO real-time delivery and shall not depend on raw WebSocket-only transport. | Interoperability | High | Inspection |
| NFR-004 | The browser client shall validate received server messages and expose invalid messages to users as displayable error objects rather than silently discarding them. | Data integrity | Medium | Test |
| NFR-005 | The server shall parse JSON bodies up to the configured request size limit. | Robustness | Medium | Test |
| NFR-006 | The visualizer mechanism shall support extensibility by loading visualizers from configuration and by requiring a small `canDisplay`/`display` contract. | Modifiability | High | Inspection |
| NFR-007 | The system shall not claim persistence, retention, authentication, authorization, or privacy behavior unless those capabilities are separately implemented. | Scope control | High | Inspection |

## 6. Data Requirements

| ID | Data requirement |
|---|---|
| DR-001 | A HypnoLog Data Object shall be a JSON object. |
| DR-002 | A HypnoLog Data Object shall define a `data` property. |
| DR-003 | A HypnoLog Data Object shall define a string `type` property. |
| DR-004 | A HypnoLog Data Object may include `tags` for UI filtering. |
| DR-005 | A HypnoLog Data Object may include `name` for variable-name display. |
| DR-006 | The server shall forward the parsed request body to browser display clients without asserting server-side schema validation. |
| DR-007 | The browser shall keep received valid or wrapped log objects in a client-side received-data list. |
| DR-008 | Invalid received messages shall be represented as `HypnoLog-error` objects containing error message, validator error details, and the original received message. |
| DR-009 | Visualizers shall receive a HypnoLog Data Object and produce a DOM element through callback-based rendering. |

## 7. System Constraints

| ID | Constraint | Type |
|---|---|---|
| C-001 | Basic log submission is constrained to HTTP POST with JSON content. | Interface |
| C-002 | The primary logging endpoint is `/logger/in`. | Interface |
| C-003 | JSON submissions should set `Content-Type: application/json`. | Interface |
| C-004 | Browser delivery uses Socket.IO and must not be specified as raw WebSocket-only. | Communication |
| C-005 | The browser-side data model requires `data` and `type`; server-side route rejection is not asserted. | Data model |
| C-006 | Visualizers must implement `canDisplay` and `display`. | Extension contract |
| C-007 | Visualizer order matters because the first matching visualizer is used. | Rendering |
| C-008 | A user configuration file may override or supplement default visualizer configuration when loadable. | Configuration |
| C-009 | The default local server port is `7000`. | Runtime |
| C-010 | No explicit persistence, retention, deletion, authentication, authorization, or privacy-control behavior is specified. | Scope |

## 8. Verification and Acceptance Criteria

| Requirement ID | Verification method | Acceptance criterion |
|---|---|---|
| FR-001 | Test | `POST /logger/in` with `Content-Type: application/json` returns HTTP 200 and forwards the parsed body. |
| FR-002 | Analysis | A client can submit logs using only HTTP and JSON, without a language-specific SDK. |
| FR-003 | Inspection | The data model defines `data` and `type` as required fields. |
| FR-004 | Test | A connected display client receives the posted object through Socket.IO notification. |
| FR-005 | Test | The browser creates a Socket.IO connection to the same server origin and handles notifications. |
| FR-006 | Test | The browser invokes the Ajv validator for each received notification message. |
| FR-007 | Test | An invalid received message is converted into a `HypnoLog-error` object with validation details. |
| FR-008 | Demonstration | Valid or wrapped objects are stored, update the last-update UI state, and are sent to windows. |
| FR-009 | Demonstration | Each registered window receives display calls for incoming objects. |
| FR-010 | Demonstration | The default window appends visualizer-created DOM output for received objects. |
| FR-011 | Test | The first visualizer whose `canDisplay` returns true is selected and its `display` function is called. |
| FR-012 | Inspection | Visualizer-loading failures do not prevent successfully loaded visualizers from being added. |
| FR-013 | Demonstration | Objects with tags create tag display/filtering information in the UI. |
| FR-014 | Demonstration | Objects with `name` display the variable name before the rendered value. |
| FR-015 | Test | `/logger/status` returns HTTP 200 behavior. |
| FR-016 | Demonstration | Startup prints the client URL and attempts to open `/client.html` on the selected port. |
| NFR-001 | Analysis | HTTP/JSON submission is usable from multiple client languages. |
| NFR-002 | Demonstration | A standard browser can load and display the UI. |
| NFR-003 | Inspection | Communication uses Socket.IO terminology and does not assert raw WebSocket-only transport. |
| NFR-004 | Test | Invalid received objects are surfaced as `HypnoLog-error` objects. |
| NFR-005 | Test | JSON bodies within the configured limit are parsed. |
| NFR-006 | Inspection | Visualizers are loaded from configuration and implement `canDisplay`/`display`. |
| NFR-007 | Inspection | The SRS does not specify persistence, retention, authentication, authorization, or privacy controls. |
| DR-001 | Inspection | Log payloads are JSON objects. |
| DR-002 | Inspection | `data` is part of the required data model. |
| DR-003 | Inspection | `type` is a required string in the data model. |
| DR-004 | Demonstration | `tags` can be used for UI tag handling. |
| DR-005 | Demonstration | `name` can be rendered as variable-name metadata. |
| DR-006 | Inspection | The server forwards parsed request body data without route-level schema rejection. |
| DR-007 | Inspection | Browser code stores received display objects in a client-side list. |
| DR-008 | Test | Invalid notifications generate `HypnoLog-error` objects. |
| DR-009 | Inspection | Visualizers return DOM elements through callback rendering. |
