# Software Requirements Specification

## 1. Introduction

### 1.1 Purpose
This SRS defines requirements for the Escape application, covering authentication, client-side content retrieval, scene-based client rendering, data handling, external interfaces, constraints, and acceptance criteria. The document is prepared as a clean requirements input for downstream architecture diagram generation.

### 1.2 Product Scope
The product is a browser-based React application with a Node.js server-side component. It includes:
- Sign-up and sign-in user interfaces with email and password entry and cross-view navigation.
- Shared client-side credential input handling and credential submission from authentication views.
- Server-side user account creation, user lookup, and password authentication.
- Client-side retrieval of paragraph-oriented content with visible error handling.
- A scene-based client built with A-Frame and aframe-react components, including scene/support components such as Lobby, SF, Louvre, Berlin, Milan, Rome, Hack, Camera, Sky, Plane, and TextPlane.
- A client-server architecture that includes a web client, web server, image storage service, cache, and database.

### 1.3 Intended Audience
- Product owners and maintainers.
- Front-end and back-end developers.
- Test engineers.
- Architecture and design reviewers.

## 2. Overall Description

### 2.1 Product Perspective
The system is a client-server web application. The web client uses React, React-Router, jQuery, A-Frame, and aframe-react for authentication views, client interactions, and scene-based rendering. The server side uses Node.js, Express-style routing, a user controller layer, and a user model for persistence-backed user operations.

The architecture includes:
- Web Client: React, React-Router, A-Frame, and aframe-react.
- Web Server: Node.js and Express-style HTTP routing.
- Image Storage Service: AWS S3-style image storage.
- Cache: Redis-style cache.
- Database: MariaDB-style relational database containing user and application data such as users, likes, photos, and comments.

### 2.2 Product Functions
- Present sign-up and sign-in interfaces.
- Capture credential input through shared client handlers.
- Submit credentials for registration or authentication.
- Create user records.
- Retrieve one or more user records.
- Verify attempted passwords against stored password values.
- Fetch paragraph/content data sequentially.
- Display an error indication when content retrieval fails.
- Render scene-based client components.

### 2.3 User Classes
- Anonymous visitor: can access sign-up and sign-in views.
- Registered user: can submit credentials for authentication and access authenticated application areas after successful authentication.
- System operator/developer: maintains client, server, persistence, cache, and storage behavior.

### 2.4 Operating Environment
- Browser client supporting React, React-Router, jQuery, A-Frame, and aframe-react.
- Node.js server environment.
- Persistence layer exposed through a User model/controller interface.
- Password verification library: `bcrypt-nodejs`.
- Deployment environment containing a web server, database, cache, and image storage service.

### 2.5 Assumptions and Dependencies
- User persistence is provided through a User model interface.
- Password comparison depends on `bcrypt-nodejs`.
- Client navigation depends on React-Router.
- Client rendering depends on A-Frame, aframe-react, and related scene components.
- Authentication views share credential input and submission logic in the top-level client application component.

## 3. External Interface Requirements

### 3.1 User Interfaces
| Interface | Requirement |
|---|---|
| Sign-up view | The system shall present a sign-up interface labeled "Escape Signup" with email and password input fields that invoke shared client input handlers, and a navigation link to the sign-in view. |
| Sign-in view | The system shall present a sign-in interface labeled "Escape Signin" with email and password input fields that invoke shared client input handlers, and a navigation link to the sign-up view. |
| Error display | When paragraph/content retrieval fails, the client shall show a visible error indicator. |
| Scene rendering UI | The client shall support scene-based rendering through A-Frame and aframe-react scene/support components. |

### 3.2 Software and API Interfaces
| Interface | Requirement |
|---|---|
| User persistence interface | The system shall use a User model interface that supports creating, saving, retrieving all users, and retrieving one queried user. |
| Password verification interface | The system shall compare attempted password values with stored password values using `bcrypt-nodejs`. |
| Authentication route interface | The client shall submit credential data to the current authentication route for registration or authentication processing. |
| Content retrieval interface | The client shall request title-based paragraph/content data asynchronously. |

### 3.3 Communication Interfaces
| Interface | Requirement |
|---|---|
| Client credential submission | The client shall submit captured email and password values from shared application state as JSON POST data. |
| Client content retrieval | The client shall perform asynchronous content retrieval and invoke success or error handling according to the request outcome. |
| Client-server communication | The web client shall communicate with the web server through HTTP-style request/response interactions. |

### 3.4 Data Exchange Formats
| Data Format | Requirement |
|---|---|
| Credential payload | The client shall exchange credentials as email and password values. |
| Authentication response | The server shall return a registration or authentication response that the client can use to determine the next navigation step. |
| Title query | The client shall request content using title-based query values. |
| Paragraph/content result | The client shall accumulate paragraph/content results from successful content retrieval. |

## 4. Functional Requirements

| ID | Requirement | Trigger/Input | System Behavior | Output | Priority | Verification |
|---|---|---|---|---|---|---|
| FR-001 | Sign-up credential input interface | User enters values in the sign-up view. | The sign-up view shall provide email and password input fields that invoke the shared client handlers for email and password changes, and shall provide navigation to the sign-in view. | Updated shared email/password state and sign-in navigation option. | High | Demonstration |
| FR-002 | Sign-in credential input interface | User enters values in the sign-in view. | The sign-in view shall provide email and password input fields that invoke the shared client handlers for email and password changes, and shall provide navigation to the sign-up view. | Updated shared email/password state and sign-up navigation option. | High | Demonstration |
| FR-003 | User account creation | User properties are submitted to the server-side create operation. | The system shall build and save a user record and return the created user through a callback or response path. | Created user object. | High | Test |
| FR-004 | User retrieval | A request is made to retrieve users. | The system shall support retrieval of all users and retrieval of one user matching a query. | User collection or single matching user. | Medium | Test |
| FR-005 | Password authentication | Attempted login password and retrieved user record are available. | The system shall compare the attempted password with the stored password value using `bcrypt-nodejs` and return match status through a callback or response path. | Boolean authentication result. | High | Test |
| FR-006 | Sequential content retrieval | The client receives a title list and starts title-based content retrieval. | The system shall request content one title at a time in title order; after each request succeeds, it shall continue to the next title, and after all titles have been successfully processed, it shall set the final paragraph result state once. | Accumulated paragraph/content result state; failed requests follow FR-007. | Medium | Test |
| FR-007 | Content retrieval error handling | A client content retrieval request fails. | The system shall log the retrieval error and display a visible error indicator in the UI. | Logged error and visible error indication. | Medium | Demonstration |
| FR-008 | Client credential submission | User submits the sign-up or sign-in view. | The system shall use the shared credential submission function to read email and password from client state and submit them as JSON POST data to the current authentication route. | Server registration or authentication response; successful authentication navigates the client to the authenticated application area. | High | Test |
| FR-009 | Scene component availability | The client application initializes scene-based rendering. | The system shall import and make available scene/support components for A-Frame-based rendering, including Lobby, SF, Louvre, Berlin, Milan, Rome, Hack, Camera, Sky, Plane, and TextPlane. | Scene-capable client rendering structure. | Medium | Inspection |

## 5. Non-Functional Requirements

| ID | Quality Attribute | Requirement | Priority | Verification |
|---|---|---|---|---|
| NFR-001 | Security | The system shall verify passwords using `bcrypt-nodejs` comparison against the stored password value rather than direct plaintext equality. | High | Inspection |
| NFR-002 | Reliability | On the successful title-retrieval path, the client shall process titles sequentially through recursive/asynchronous callbacks and invoke the final state-setting operation once after all titles have been processed. | Medium | Test |
| NFR-003 | Usability | The authentication UI shall provide direct cross-navigation between sign-up and sign-in views. | Medium | Demonstration |
| NFR-004 | Compatibility | The client shall operate in an environment supporting React, React-Router, jQuery, A-Frame, and aframe-react dependencies. | Medium | Inspection |
| NFR-005 | Maintainability | Authentication input handling shall be centralized through shared client handlers rather than duplicated independently in each authentication view. | Medium | Inspection |

## 6. Data Requirements

### 6.1 Data Entities
| Entity/Object | Requirement |
|---|---|
| User | The system shall manage user objects through a persistent user model with create and query operations. |
| Credential data | The system shall capture, store in shared client state, submit, and verify email/password values as authentication inputs. |
| Paragraph/content result | The client shall maintain accumulated paragraph/content results derived from title-based fetch operations. |
| Scene component data | The client shall maintain scene/support component definitions required for A-Frame rendering. |
| Photo/image data | The system architecture shall support image storage through an external image storage service. |
| Application interaction data | The system architecture shall support relational application data such as users, likes, photos, and comments. |

### 6.2 Input and Output Data
| Data Flow | Requirement |
|---|---|
| Credential input | Email and password shall be accepted from sign-up/sign-in UI events and stored in shared client state before submission. |
| Credential submission output | Client credential submission shall produce a server registration or authentication response. |
| Authentication output | Password authentication shall output a boolean match result or equivalent authentication status. |
| User operation output | User creation and query operations shall output user object data. |
| Content retrieval output | Content retrieval shall output final paragraph/result state or an error indication. |

### 6.3 Storage, Integrity, Privacy, Retention, and Migration
| Topic | Requirement |
|---|---|
| Credential integrity | Stored password values used for authentication shall be processed through `bcrypt-nodejs` comparison logic. |
| User persistence | User records shall be stored and retrieved through the system persistence layer. |
| Application persistence | Application data such as users, likes, photos, and comments shall be represented in the database layer. |
| Image storage | Image/photo data shall be handled by the external image storage service. |
| Privacy, retention, and migration | Privacy notices, retention periods, deletion behavior, and migration behavior are not specified and should be defined before production use. |

## 7. System Constraints

| ID | Constraint |
|---|---|
| C-001 | The client implementation is constrained to React and React-Router for UI composition and navigation. |
| C-002 | The client rendering stack is constrained by A-Frame, aframe-react, and related A-Frame components. |
| C-003 | Password verification is constrained to `bcrypt-nodejs`. |
| C-004 | User persistence is constrained to the repository's User model/controller interface. |
| C-005 | The server environment is constrained to a Node.js/Express-style web server. |
| C-006 | The deployment architecture includes a web client, web server, database, cache, and image storage service. |

## 8. Verification and Acceptance Criteria

| Requirement ID | Verification Method | Acceptance Criteria |
|---|---|---|
| FR-001 | Demonstration | The sign-up view provides email/password fields wired to shared client input handlers and offers navigation to sign-in. |
| FR-002 | Demonstration | The sign-in view provides email/password fields wired to shared client input handlers and offers navigation to sign-up. |
| FR-003 | Test | Creating a user with valid properties returns a created user object or equivalent success result. |
| FR-004 | Test | Querying all users returns a collection, and querying one user returns a single matching user when present. |
| FR-005 | Test | Given stored password data and an attempted password, `bcrypt-nodejs` comparison returns the correct match status. |
| FR-006 | Test | Given a title list and successful content requests, the client fetches titles in order and sets final paragraph state once after completion. |
| FR-007 | Demonstration | On content retrieval failure, the system logs the error and displays the visible error indication. |
| FR-008 | Test | Submitting either authentication view sends shared client email/password state as JSON POST data and handles the server response, including authenticated navigation on success. |
| FR-009 | Inspection | The scene/support components required for A-Frame rendering are present in the client rendering structure. |
| NFR-001 | Inspection | Password verification uses `bcrypt-nodejs` comparison rather than plaintext equality. |
| NFR-002 | Test | Success-path sequential completion behavior matches the callback order, termination condition, and single final state-setting operation. |
| NFR-003 | Demonstration | Each authentication screen visibly links to the alternative authentication screen. |
| NFR-004 | Inspection | Required client dependencies are present and compatible with the target browser environment. |
| NFR-005 | Inspection | Sign-up and sign-in views delegate email/password changes to shared client handlers. |
