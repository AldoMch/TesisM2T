# Software Requirements Specification

## 1. Introduction

### Purpose
This SRS defines evidence-backed requirements for the repository component that manages local session establishment and teardown using Firebase authentication tokens, exposes login/logout API interactions, and operates within a frontend/backend setup that includes Firebase functions and OnFleet.

### Product scope
Based on the available evidence, the product includes:
- a frontend that can start independently,
- a backend composed of Firebase serverless functions and OnFleet task handling,
- session handling that sends authenticated login and logout requests to internal API routes,
- environment-driven configuration for Firebase-related values.

This SRS is limited to behaviors and constraints directly supported by the repository evidence.

### Intended audience
- Maintainers and contributors
- Testers
- Deployment/configuration operators
- Integrators working with Firebase-authenticated session flows

### References
- Repository: Neighbor-Army/help-with-covid
- Commit: `b540315578f533e035b704a9d4b8b27b7ae8d3a0`
- Evidence: `E001`–`E006`

## 2. Overall Description

### Product perspective
The repository contains both frontend and backend elements. The backend is described as having two parts:
- Firebase functions used to deploy custom APIs
- OnFleet as the task handling system

A session handler in the frontend communicates with internal API endpoints for login and logout. Firebase-related environment variables are injected into the application configuration.

### Product functions summary
- Obtain a Firebase ID token from an authenticated user and submit it to an internal login API.
- Submit a logout request to an internal logout API when no user is present.
- Accept login API requests containing a token in the request body.
- Verify a Firebase ID token during login processing.
- Expose Firebase configuration values from environment variables.

### User classes
Supported by the evidence:
- Authenticated application user: initiates login through a Firebase-authenticated session flow.
- Logged-out or unauthenticated user: initiates logout or has no active user object.
- Developer/operator: configures environment variables and starts frontend and backend servers.

### Operating environment
Supported by the evidence:
- Frontend server
- Backend server
- Firebase serverless functions
- OnFleet integration
- Next.js-based configuration environment with CSS/Sass and asset loading support

### Assumptions and dependencies
- The login flow depends on Firebase authentication tokens being obtainable from the user object. (`E001`)
- The backend depends on Firebase functions for custom APIs and OnFleet for task handling. (`E002`, `E004`)
- Firebase configuration depends on environment variables being present in the project root configuration setup. (`E002`, `E006`)

## 3. External Interface Requirements

### User interfaces
No direct end-user UI behavior is explicitly described in the evidence. The supported user-facing interaction is limited to authentication-driven session establishment and logout requests triggered by application logic.

### Software/API interfaces
| Interface | Description | Evidence |
|---|---|---|
| `POST /api/login` | Accepts a JSON request containing a `token` value; used by the session handler after obtaining a Firebase ID token. | `E001`, `E003`, `E005` |
| `POST /api/logout` | Accepts a logout request from the session handler using same-origin credentials. | `E001`, `E003` |
| Firebase token verification | Login processing uses Firebase token verification. | `E005` |
| OnFleet backend integration | Backend includes OnFleet as the task handling system. | `E002`, `E004` |

### Communication interfaces
| Interface aspect | Requirement-supported detail | Evidence |
|---|---|---|
| HTTP method | Login and logout requests use `POST`. | `E001`, `E003` |
| Content type | Login requests send `Content-Type: application/json`. | `E001`, `E003` |
| Credential mode | Login and logout requests use `credentials: "same-origin"`. | `E001`, `E003` |

### Data exchange formats
| Exchange | Format | Evidence |
|---|---|---|
| Login request body | JSON object containing `token` | `E001`, `E003`, `E005` |
| Logout request body | No request body shown in evidence | `E001`, `E003` |
| Configuration values | Environment variables mapped into application configuration | `E006` |

## 4. Functional Requirements

| ID | Description | Trigger/Input | System behavior | Output | Priority | Verification | Source evidence |
|---|---|---|---|---|---|---|---|
| FR-001 | The system shall submit a login request when a user object is provided. | A non-null user object is passed to the session handler. | The system shall call `user.getIdToken()`, then send `POST /api/login` with a JSON body containing the token and same-origin credentials. | An HTTP request to `/api/login` is issued. | High | Test | `E001`, `E003` |
| FR-002 | The system shall submit a logout request when no user object is provided. | No user object is passed to the session handler. | The system shall send `POST /api/logout` using same-origin credentials. | An HTTP request to `/api/logout` is issued. | High | Test | `E001`, `E003` |
| FR-003 | The login API shall require a request body. | A request is received by the login API. | If no request body is present, the system shall return HTTP status 400. | HTTP 400 response for missing body. | High | Test | `E005` |
| FR-004 | The login API shall extract the authentication token from the request body. | A login request contains a body. | The system shall read `token` from `req.body`. | Token value becomes available for login processing. | High | Inspection | `E005` |
| FR-005 | The login API shall verify the Firebase ID token during login processing. | A login request provides a token. | The system shall invoke Firebase token verification as part of processing the login request. | Verification is performed before session establishment proceeds. | High | Inspection | `E005` |
| FR-006 | The system shall expose Firebase configuration values from environment variables. | Application startup/configuration load. | The system shall map Firebase auth domain, database URL, project ID, and public API key from environment variables into runtime configuration. | Firebase configuration values are available to the application. | Medium | Inspection | `E006` |
| FR-007 | The product shall support running frontend and backend server components. | Developer starts the application. | The system shall support starting both frontend and backend servers, frontend only, or backend only as described in repository documentation. | Frontend and/or backend server processes can be started per mode. | Medium | Demonstration | `E002` |

## 5. Non-Functional Requirements

| ID | Requirement | Quality attribute | Priority | Verification | Source evidence | Evidence type |
|---|---|---|---|---|---|---|
| NFR-001 | Login requests shall be sent using `Content-Type: application/json`. | Compatibility | High | Test | `E001`, `E003` | explicit |
| NFR-002 | Login and logout requests shall use same-origin credentials. | Security/compatibility | High | Test | `E001`, `E003` | explicit |
| NFR-003 | The system shall externalize Firebase configuration through environment variables rather than hard-coded values. | Maintainability/portability | Medium | Inspection | `E002`, `E006` | explicit |
| NFR-004 | The backend architecture shall remain compatible with Firebase serverless functions and OnFleet task handling integration. | Compatibility | Medium | Inspection | `E002`, `E004` | explicit |

## 6. Data Requirements

| ID | Data entity/object | Description | Source evidence |
|---|---|---|---|
| DR-001 | User object | Input to the session handler; when present, it must support retrieval of an ID token. | `E001` |
| DR-002 | Firebase ID token | Authentication token retrieved from the user object and transmitted in login requests. | `E001`, `E005` |
| DR-003 | Login request body | JSON payload containing `token`. | `E001`, `E003`, `E005` |
| DR-004 | Firebase configuration values | `FIREBASE_AUTH_DOMAIN`, `FIREBASE_DATABASE_URL`, `FIREBASE_PROJECT_ID`, `FIREBASE_PUBLIC_API_KEY` loaded from environment variables. | `E006` |

### Input/output data
| Flow | Input | Output | Evidence |
|---|---|---|---|
| Session login | User object | `POST /api/login` request with JSON token payload | `E001`, `E003` |
| Session logout | Null/absent user object | `POST /api/logout` request | `E001`, `E003` |
| Login API processing | Request body with `token` | HTTP 400 if body is absent; otherwise token available for verification | `E005` |

### Storage, privacy, integrity, retention
| Aspect | Requirement-supported statement | Evidence |
|---|---|---|
| Session storage | The login flow documentation/comments state the user's Firebase token is decoded and stored in a cookie. | `E005` |
| Integrity | Token verification is part of login processing. | `E005` |

## 7. Constraints

| ID | Constraint | Source evidence |
|---|---|---|
| C-001 | Firebase-related runtime values must be provided through environment variables in the project setup. | `E002`, `E006` |
| C-002 | The backend is constrained to a two-part architecture consisting of Firebase functions for custom APIs and OnFleet for task handling. | `E002`, `E004` |
| C-003 | Internal authentication session operations are constrained to the `/api/login` and `/api/logout` HTTP endpoints shown in the repository evidence. | `E001`, `E003` |
| C-004 | Application asset handling is configured to support CSS, Sass, and bundled static asset types including png, jpg, gif, svg, eot, ttf, woff, and woff2. | `E006` |

## 8. Verification and Acceptance

| Requirement ID | Verification method | Acceptance criterion |
|---|---|---|
| FR-001 | Test | With a valid user object, the system issues `POST /api/login` with JSON `{ "token": ... }` and same-origin credentials. |
| FR-002 | Test | Without a user object, the system issues `POST /api/logout` with same-origin credentials. |
| FR-003 | Test | A login request without a body returns HTTP 400. |
| FR-004 | Inspection | The login API reads `token` from the request body. |
| FR-005 | Inspection | Login processing includes Firebase ID token verification. |
| FR-006 | Inspection | Firebase configuration fields are populated from environment variables. |
| FR-007 | Demonstration | The documented run modes support starting frontend and backend together, frontend only, or backend only. |
| NFR-001 | Test | Login requests include `Content-Type: application/json`. |
| NFR-002 | Test | Login and logout requests use same-origin credentials. |
| NFR-003 | Inspection | Firebase configuration is environment-driven. |
| NFR-004 | Inspection | Repository documentation and configuration remain aligned with Firebase functions and OnFleet backend use. |

## 9. Traceability Matrix

| ID | Requirement | Type | Source | Evidence Type | Verification | Confidence |
|---|---|---|---|---|---|---|
| FR-001 | Submit login request with token when user object is provided | Functional | `E001`, `E003` | explicit | Test | High |
| FR-002 | Submit logout request when no user object is provided | Functional | `E001`, `E003` | explicit | Test | High |
| FR-003 | Return HTTP 400 when login request body is missing | Functional | `E005` | explicit | Test | High |
| FR-004 | Extract `token` from login request body | Functional | `E005` | explicit | Inspection | High |
| FR-005 | Verify Firebase ID token during login processing | Functional | `E005` | explicit | Inspection | Medium |
| FR-006 | Expose Firebase configuration from environment variables | Functional | `E006` | explicit | Inspection | High |
| FR-007 | Support documented frontend/backend run modes | Functional | `E002` | explicit | Demonstration | Medium |
| NFR-001 | Use JSON content type for login requests | Non-functional | `E001`, `E003` | explicit | Test | High |
| NFR-002 | Use same-origin credentials for login/logout requests | Non-functional | `E001`, `E003` | explicit | Test | High |
| NFR-003 | Externalize Firebase configuration via environment variables | Non-functional | `E002`, `E006` | explicit | Inspection | High |
| NFR-004 | Maintain compatibility with Firebase functions and OnFleet backend integration | Non-functional | `E002`, `E004` | explicit | Inspection | Medium |
| DR-001 | User object used as login flow input | Data | `E001` | explicit | Inspection | High |
| DR-002 | Firebase ID token exchanged for login | Data | `E001`, `E005` | explicit | Inspection | High |
| DR-003 | Login request body contains `token` | Data | `E001`, `E003`, `E005` | explicit | Inspection | High |
| DR-004 | Firebase config values loaded from environment | Data | `E006` | explicit | Inspection | High |
| C-001 | Environment variables required for Firebase configuration | Constraint | `E002`, `E006` | explicit | Inspection | High |
| C-002 | Backend constrained to Firebase functions plus OnFleet | Constraint | `E002`, `E004` | explicit | Inspection | Medium |
| C-003 | Session operations use internal login/logout endpoints | Constraint | `E001`, `E003` | explicit | Inspection | High |
| C-004 | Asset and style support constrained by configured loaders/plugins | Constraint | `E006` | explicit | Inspection | Medium |
