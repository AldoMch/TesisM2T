# Software Requirements Specification

## 1. Introduction

### Purpose
This SRS defines the evidenced requirements for the `FAC10/week4-jajascript` repository at commit `ef2fe84e25cdb9621e47e8bd36cb4a1e225a00ba`. The scope is limited to behavior supported by the provided repository evidence.

### Product scope
The product is a Nobel Prize laureates autocomplete web application. A user enters text into an input field and receives suggestions or a list of Nobel Prize laureates to support easier search. `search` requests are handled separately from the home page and static assets. Sources: `E001`, `E003`, `E005`.

### Intended audience
This document is intended for developers, testers, maintainers, and reviewers of the repository. Source: `E001`, `E002`, `E006`.

### References
- Repository: `FAC10/week4-jajascript`
- Commit: `ef2fe84e25cdb9621e47e8bd36cb4a1e225a00ba`
- Evidence sources: `README.md`, `src/router.js`, `src/handler.js`, `test/frontendTests.js`, `test/backendTests.js`

## 2. Overall Description

### Product perspective
The product is a server-backed web application with:
- an HTTP router that serves the home page at `/`
- a dedicated `search` route for autocomplete hints
- static file serving for public assets
- backend autocomplete logic tested against local data

Sources: `E003`, `E004`, `E006`.

### Product functions summary
- Accept user text input for laureate search suggestions.
- Return Nobel Prize laureate suggestions as the user types.
- Serve the application home page.
- Serve public static assets.
- Provide backend autocomplete behavior over stored laureate data.

Sources: `E001`, `E003`, `E004`, `E005`, `E006`.

### User classes
| User class | Description | Source |
|---|---|---|
| End user | Person entering text into an input box to search for Nobel Prize laureates | `E001`, `E005` |
| Developer/tester | Person validating frontend helper behavior and backend autocomplete/data behavior through tests | `E002`, `E006` |

### Operating environment
| Aspect | Requirement-relevant description | Evidence |
|---|---|---|
| Server runtime | JavaScript server environment using CommonJS modules and filesystem-based static file serving | `E003`, `E004`, `E006` |
| Client environment | Web browser consuming HTML, CSS, and JavaScript assets | `E004` |

### Assumptions and dependencies
| Item | Description | Evidence type | Source |
|---|---|---|---|
| Local public assets | The application depends on files under `public`, including `index.html` and static assets | explicit | `E004` |
| Local laureate dataset | Backend autocomplete depends on a local JSON dataset imported by tests | explicit | `E006` |
| Search endpoint handling | Requests containing `search` are delegated to autocomplete logic | explicit | `E003` |

## 3. External Interface Requirements

### User interfaces
| Interface | Requirement-relevant description | Source |
|---|---|---|
| Text input field | The user shall be able to enter text into an input box/input field for search | `E001`, `E005` |
| Suggestions/list output | The system shall present suggestions or a list of Nobel Prize laureates in response to user input | `E001`, `E005` |

### Software/API interfaces
| Interface | Description | Source |
|---|---|---|
| `GET /` | Serves the application home page | `E003`, `E004` |
| `GET` request containing `search` in URL | Routed to autocomplete hint handling | `E003` |
| Static file requests | Routed to public file serving | `E003`, `E004` |

### Communication interfaces
| Interface | Description | Source |
|---|---|---|
| HTTP request/response | The server handles incoming HTTP requests and returns HTTP responses | `E003`, `E004` |

### Data exchange formats
| Format | Description | Support status | Source |
|---|---|---|---|
| HTML | Home page/static page content | explicit | `E004` |
| CSS | Static stylesheet content | explicit | `E004` |
| JavaScript | Static client-side script content | explicit | `E004` |
| JPG | Static image content | explicit | `E004` |
| ICO | Static icon content | explicit | `E004` |
| Search response payload | Response structure for autocomplete results is not specified in the evidence pack | unsupported | `E001`, `E003`, `E006` |

## 4. Functional Requirements

| ID | Description | Trigger/Input | System behavior | Output | Priority | Verification | Source evidence |
|---|---|---|---|---|---|---|---|
| FR-001 | The system shall allow a user to enter text into an input field to search Nobel Prize laureates. | User types into the input box | The system accepts the entered string as search input. | Captured user input for search processing | High | Demonstration, Test | `E001`, `E002`, `E005` |
| FR-002 | The system shall provide Nobel Prize laureate suggestions/list results in response to entered text. | User enters text while searching | The system returns sensible suggestions or a list of Nobel Prize laureates matching the entered string. | Search suggestions/list results | High | Test, Demonstration | `E001`, `E005`, `E006` |
| FR-003 | The system shall serve the application home page when the request URL is `/`. | HTTP request to `/` | The router delegates the request to home-page handling, which reads and returns `index.html`. | HTTP 200 response with HTML content when file read succeeds | High | Test, Inspection | `E003`, `E004` |
| FR-004 | The system shall route requests containing `search` to autocomplete hint handling. | HTTP request whose URL contains `search` | The router delegates the request to the autocomplete handler. | Search request processed by hint-serving logic | High | Test, Inspection | `E003` |
| FR-005 | The system shall serve requested public static assets when the request is not `/` and does not match `search`. | HTTP request for a public asset | The router delegates the request to public file handling, which reads the requested file from `public`. | HTTP response containing requested file content when file read succeeds | Medium | Test, Inspection | `E003`, `E004` |
| FR-006 | The system shall return the appropriate content type for supported static file extensions. | Successful static file read for supported extension | The server sets `Content-Type` based on extension mapping for `html`, `css`, `js`, `jpg`, and `ico`. | HTTP response with matching MIME type header | Medium | Test, Inspection | `E004` |
| FR-007 | The system shall invoke not-found handling when a requested file cannot be read. | File read error during home or public asset serving | The server logs the error and delegates to not-found handling. | Not-found response behavior | Medium | Test, Inspection | `E004` |
| FR-008 | The backend autocomplete capability shall operate on array-based values derived from stored laureate data. | Backend autocomplete call using stored data and a search string | The backend exposes value extraction and autocomplete operations that return arrays. | Array result from data extraction and autocomplete | Medium | Test | `E006` |

## 5. Non-Functional Requirements

| ID | Requirement | Quality attribute | Priority | Verification | Evidence type | Source evidence |
|---|---|---|---|---|---|---|
| NFR-001 | The project shall include automated tests covering frontend helper behavior and backend autocomplete/data behavior. | Maintainability | Medium | Inspection | explicit | `E001`, `E002`, `E006` |
| NFR-002 | For supported static file types, the server shall identify response media type explicitly as `text/html`, `text/css`, `application/javascript`, `image/jpg`, or `image/x-icon`. | Compatibility | Medium | Test, Inspection | explicit | `E004` |
| NFR-003 | The application structure shall separate routing, request handling, and autocomplete logic into distinct modules. | Maintainability | Low | Inspection | inferred | `E001`, `E003`, `E004` |

## 6. Data Requirements

| ID | Data requirement | Type | Source evidence |
|---|---|---|---|
| DR-001 | The application data domain includes Nobel Prize laureate names used for autocomplete/search suggestions. | explicit | `E001`, `E005` |
| DR-002 | Backend autocomplete uses a local JSON data source imported as `data.json`. | explicit | `E006` |
| DR-003 | Backend value extraction operates on object data and field names such as `firstname`, and returns an array of values. | explicit | `E006` |
| DR-004 | Search input data is a user-entered string captured from the input event target value. | explicit | `E002` |
| DR-005 | Static content served by the system includes HTML, CSS, JavaScript, JPG, and ICO files under the public asset path. | explicit | `E004` |

## 7. Constraints

| Constraint | Description | Source evidence |
|---|---|---|
| C-001 | Server-side implementation is constrained to a JavaScript/CommonJS environment using `require` and `module.exports`. | `E003`, `E004`, `E006` |
| C-002 | Static content serving is constrained to filesystem reads from the repository `public` directory. | `E004` |
| C-003 | Supported explicitly mapped static file extensions are limited to `html`, `css`, `js`, `jpg`, and `ico`. | `E004` |
| C-004 | Search request routing depends on URL matching that checks whether the URL contains the substring `search`. | `E003` |

## 8. Verification and Acceptance

| Requirement ID | Verification method |
|---|---|
| FR-001 | Demonstration, Test |
| FR-002 | Test, Demonstration |
| FR-003 | Test, Inspection |
| FR-004 | Test, Inspection |
| FR-005 | Test, Inspection |
| FR-006 | Test, Inspection |
| FR-007 | Test, Inspection |
| FR-008 | Test |
| NFR-001 | Inspection |
| NFR-002 | Test, Inspection |
| NFR-003 | Inspection |

Acceptance is achieved when each listed requirement is satisfied by its mapped verification method using the repository artifacts and tests evidenced in the pack.

## 9. Traceability Matrix

| ID | Requirement | Type | Source | Evidence Type | Verification | Confidence |
|---|---|---|---|---|---|---|
| FR-001 | Accept text input for laureate search | Functional | `E001`, `E002`, `E005` | explicit | Demonstration, Test | High |
| FR-002 | Return laureate suggestions/list results | Functional | `E001`, `E005`, `E006` | explicit | Test, Demonstration | Medium |
| FR-003 | Serve home page at `/` | Functional | `E003`, `E004` | explicit | Test, Inspection | High |
| FR-004 | Route `search` requests to autocomplete handler | Functional | `E003` | explicit | Test, Inspection | High |
| FR-005 | Serve public static assets | Functional | `E003`, `E004` | explicit | Test, Inspection | High |
| FR-006 | Set MIME type for supported static files | Functional | `E004` | explicit | Test, Inspection | High |
| FR-007 | Invoke not-found handling on file read failure | Functional | `E004` | explicit | Test, Inspection | Medium |
| FR-008 | Provide array-based backend autocomplete operations over stored data | Functional | `E006` | explicit | Test | Medium |
| NFR-001 | Include automated frontend and backend tests | Non-functional | `E001`, `E002`, `E006` | explicit | Inspection | High |
| NFR-002 | Use explicit media types for supported static files | Non-functional | `E004` | explicit | Test, Inspection | High |
| NFR-003 | Separate routing, handling, and autocomplete logic into modules | Non-functional | `E001`, `E003`, `E004` | inferred | Inspection | Medium |
| DR-001 | Nobel laureate names are the search domain data | Data | `E001`, `E005` | explicit | Inspection | High |
| DR-002 | Local JSON dataset is used by backend logic | Data | `E006` | explicit | Inspection | High |
| DR-003 | Value extraction uses field-based object access and returns arrays | Data | `E006` | explicit | Test | Medium |
| DR-004 | Search input is a user-entered string from event target value | Data | `E002` | explicit | Test | High |
| DR-005 | Static data includes HTML/CSS/JS/JPG/ICO assets | Data | `E004` | explicit | Inspection | High |
