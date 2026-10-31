# Software Requirements Specification

## 1. Introduction

### Purpose
This SRS defines the checked software requirements for the `FAC10/week4-jajascript` web application. The specification is limited to behavior and interfaces supported by the reviewed repository artifacts.

### Product scope
The product is a Nobel Prize laureates autocomplete web application. A user enters text into an input field and receives Nobel Prize laureate suggestions to support easier search. The application serves a home page, handles search requests separately from other requests, and serves static web assets.

### Intended audience
This document is intended for developers, testers, maintainers, and reviewers of the application.

### References
- Repository: `FAC10/week4-jajascript`
- Reviewed artifacts include project documentation, routing and handler modules, autocomplete/search algorithm code, frontend and backend tests, and the architecture diagram.

## 2. Overall Description

### Product perspective
The product is a server-backed web application with distinct responsibilities for:
- frontend user input and request initiation
- HTTP routing
- request handling for the home page, static resources, and not-found responses
- search-hint/autocomplete algorithm processing
- local data access for laureate data

The router delegates requests containing `search` to the search-hint/autocomplete algorithm module. The handler module is responsible for the home page, static resources, and not-found responses.

### Product functions summary
The application supports the following functions:
- accept user text input for laureate search
- return an array of laureate names from local laureate data
- serve the application home page
- serve public static assets
- route search requests to the autocomplete/search-hint algorithm
- provide backend autocomplete behavior over stored laureate data

### User classes
| User class | Description |
|---|---|
| End user | Person entering text into an input field to search for Nobel Prize laureates |
| Developer/tester | Person validating frontend helper behavior, routing, and backend autocomplete/data behavior through tests |
| Deployer/operator | Person running or deploying the Node.js web application |

### Operating environment
| Aspect | Description |
|---|---|
| Server runtime | JavaScript server environment using CommonJS modules |
| Client environment | Web browser consuming HTML, CSS, JavaScript, and image assets |
| Data environment | Local JSON-based laureate data used by autocomplete logic |
| Deployment environment | The application is expected to run using the Node.js start script and is intended for deployment to Heroku |

### Assumptions and dependencies
| ID | Statement |
|---|---|
| A-001 | The application depends on files under the public asset directory, including the home page and static assets. |
| A-002 | Backend autocomplete depends on local laureate data. |
| A-003 | Search routing depends on URL substring matching for `search`. |
| A-004 | The application is expected to be deployed to Heroku as described in project documentation, using the Node.js start script. |

## 3. External Interface Requirements

### User interfaces
| Interface | Requirement summary |
|---|---|
| Search input field | The system shall provide an input field in which the user can enter text for laureate search. |
| Suggestions/list output | The system shall present laureate search suggestions in response to user input. |

### Software/API interfaces
| Interface | Requirement summary |
|---|---|
| `GET /` | The system shall serve the application home page. |
| URL containing `search` | The router shall delegate requests containing the substring `search` to the autocomplete/search-hint algorithm module. |
| Static file requests | The router shall delegate non-home, non-search requests to public file serving. |
| Local data source | The autocomplete/search-hint algorithm shall use local laureate data. |

### Communication interfaces
| Interface | Requirement summary |
|---|---|
| HTTP request/response | The server shall accept HTTP requests and return HTTP responses for home page, search, and static asset access. |

### Data exchange formats
| Format/item | Requirement summary |
|---|---|
| HTML | The system shall serve HTML for the home page and not-found page. |
| CSS | The system shall serve CSS static assets. |
| JavaScript | The system shall serve JavaScript static assets. |
| JPG | The system shall serve JPG image assets. |
| ICO | The system shall serve ICO icon assets. |
| Search input | Search input shall be a user-entered string. |
| Search output | Search output shall be an array of laureate names. |

## 4. Functional Requirements

| ID | Description | Trigger/Input | System behavior | Output | Priority | Verification |
|---|---|---|---|---|---|---|
| FR-001 | Search input capture | User types into the input field | The system shall accept text entered into the search input field for laureate search processing. | Captured search string | High | Demonstration, Test |
| FR-002 | Laureate autocomplete results | User enters a search string | The system shall return an array of laureate names from local laureate data. Returned items shall prefix-match the input string, and the result count shall be at most 10. | Array of laureate names | High | Test, Demonstration |
| FR-003 | Home page serving | HTTP request to `/` | The system shall serve the application home page. | HTTP response containing the home page | High | Test, Inspection |
| FR-004 | Search request routing | HTTP request whose URL contains the substring `search` | The router shall delegate the request to the autocomplete/search-hint algorithm module. Search routing is implemented by plain URL substring matching; any URL containing the substring `search` is routed to autocomplete logic. | Search request handled by the autocomplete/search-hint algorithm | High | Test, Inspection |
| FR-005 | Static asset serving | HTTP request that is not `/` and whose URL does not contain `search` | The system shall serve the requested public static asset. | HTTP response containing the requested asset when available | Medium | Test, Inspection |
| FR-006 | Static content type mapping | Successful static file read for a supported extension | The system shall set the response `Content-Type` according to the file extension mapping for `html`, `css`, `js`, `jpg`, and `ico`. | HTTP response with matching media type header | Medium | Test, Inspection |
| FR-007 | Not-found handling | File read failure during home page or static asset serving | The system shall invoke not-found handling and return a 404 HTML response indicating page not found. | HTTP 404 response with HTML not-found content | Medium | Test, Inspection |
| FR-008 | Backend value extraction | Request for field values from laureate data | The backend shall extract values for a specified field from object-based laureate data and return them as an array. | Array of field values | Medium | Test |
| FR-009 | Backend autocomplete operation | Backend autocomplete call with a search string and laureate-name array | The backend shall filter laureate-name values by prefix match and limit results to at most 10. | Array of matching laureate names | Medium | Test, Inspection |

## 5. Non-Functional Requirements

| ID | Quality attribute | Requirement | Priority | Verification |
|---|---|---|---|---|
| NFR-001 | Maintainability | The project shall include automated tests covering frontend helper behavior and backend autocomplete/data behavior. | Medium | Inspection |
| NFR-002 | Compatibility | For supported static file types, the server shall identify response media type explicitly as `text/html`, `text/css`, `application/javascript`, `image/jpg`, or `image/x-icon`. | Medium | Test, Inspection |
| NFR-003 | Modularity | The application shall separate frontend input/request handling, backend routing, request handling, search algorithm, and local data access into distinct responsibility modules. | Medium | Inspection |
| NFR-004 | Deployability | The application shall support runtime startup through the Node.js start script and shall be suitable for Heroku deployment as stated in project documentation. | Low | Inspection, Demonstration |

## 6. Data Requirements

| ID | Data item/entity | Requirement |
|---|---|---|
| DR-001 | Laureate names | The application shall use Nobel Prize laureate names as the search domain data. |
| DR-002 | Local data source | Backend autocomplete shall use a local JSON data source. |
| DR-003 | Object field extraction | Backend value extraction shall operate on object data and field names such as `firstname`, returning an array of values. |
| DR-004 | Search input string | Search input shall be captured from a user input event value. |
| DR-005 | Static assets | Static content shall include HTML, CSS, JavaScript, JPG, and ICO files under the public asset path. |

## 7. System Constraints

| ID | Constraint |
|---|---|
| C-001 | Server-side implementation is constrained to a JavaScript/CommonJS environment using module import/export patterns compatible with Node.js. |
| C-002 | Static content serving is constrained to filesystem reads from the public asset directory. |
| C-003 | Explicitly mapped static file extensions are limited to `html`, `css`, `js`, `jpg`, and `ico`. |
| C-004 | Search routing is implemented by URL substring matching; any URL containing the substring `search` is routed to autocomplete logic. |
| C-005 | The application is expected to be deployed to Heroku and started using the Node.js start script. |

## 8. Verification and Acceptance Criteria

| Requirement ID | Verification method | Acceptance criterion |
|---|---|---|
| FR-001 | Demonstration, Test | A user can type text into the search input field, and the entered value is captured for processing. |
| FR-002 | Test, Demonstration | For a given input string, the system returns an array of laureate names that prefix-match the input, with no more than 10 results. |
| FR-003 | Test, Inspection | A request to `/` returns the application home page. |
| FR-004 | Test, Inspection | Requests whose URL contains `search` are routed to the autocomplete/search-hint algorithm module. |
| FR-005 | Test, Inspection | Requests for non-home, non-search resources return the requested static asset when the asset exists. |
| FR-006 | Test, Inspection | Responses for supported static file extensions contain the expected `Content-Type` header. |
| FR-007 | Test, Inspection | When a requested home page or static asset cannot be read, the system returns an HTTP 404 HTML not-found response. |
| FR-008 | Test | Given object-based laureate data and a field name, the backend returns an array of values for that field. |
| FR-009 | Test, Inspection | Given a search string and a laureate-name array, the backend returns only prefix-matching names and limits the result set to 10 or fewer items. |
| NFR-001 | Inspection | Automated tests are present for frontend helper behavior and backend autocomplete/data behavior. |
| NFR-002 | Test, Inspection | Supported static file responses use the documented explicit media types. |
| NFR-003 | Inspection | The implementation separates frontend request initiation, routing, request handling, algorithm logic, and data access into distinct modules or responsibilities. |
| NFR-004 | Inspection, Demonstration | The application can be started through the Node.js start script, and project documentation identifies Heroku as the intended deployment environment. |
