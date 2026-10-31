# Checked Software Requirements Specification: Help With COVID Session and Task Workflow

## 1. Introduction

### 1.1 Purpose

This Software Requirements Specification defines the checked requirements for a frontend and backend system that manages Firebase-authenticated sessions, exposes login and logout API interactions, loads Firebase configuration from environment variables, and routes help-request tasks toward backend task handling.

The document is prepared for architecture view generation and omits review notes, provenance fields, and supporting-material identifiers.

### 1.2 Product Scope

The product includes:

- A Next.js frontend that can run independently.
- A backend run mode that includes Firebase functions for custom APIs and OnFleet task handling.
- A session handler that sends authenticated login and logout requests to internal API routes.
- Login API handling that verifies Firebase ID tokens and writes authentication data into a server-side session object.
- Firebase-related runtime configuration loaded from environment variables.
- A task-request path that can start from end-user channels or a frontend form, pass through middleware checks, and create tasks in OnFleet.

Detailed visual layout, exact task payload schema, and full OnFleet operational behavior are outside this checked SRS unless a requirement below states otherwise.

### 1.3 Intended Audience

The intended audience includes maintainers, contributors, testers, deployment operators, configuration operators, and integrators working with Firebase-authenticated session flows and task-routing behavior.

### 1.4 Definitions and Abbreviations

- API: Application Programming Interface.
- Firebase functions: Serverless backend functions used to deploy custom APIs.
- Firebase ID token: Authentication token obtained from the authenticated user object.
- Middleware: Application layer that performs request processing between frontend entry points and backend task handling.
- OnFleet: Backend task handling system.
- SRS: Software Requirements Specification.

## 2. Overall Description

### 2.1 Product Perspective

The product contains frontend, middleware, and backend elements. The frontend includes a Next.js application and a Firebase session handler. The middleware layer supports task-request processing, including address-to-neighborhood handling and service-area checks. The backend is organized around Firebase functions for custom APIs and OnFleet for task handling.

The backend shall not be described as the entire system boundary. The checked architecture context also includes end-user entry channels, the frontend form, middleware decision logic, Firebase authentication, and OnFleet task creation.

### 2.2 Product Functions

The product shall provide the following high-level functions:

- Obtain a Firebase ID token from an authenticated user.
- Submit login requests to an internal login API.
- Submit logout requests to an internal logout API.
- Validate login request bodies.
- Verify Firebase ID tokens during login processing.
- Store decoded authentication data and token values in a server-side session object.
- Expose Firebase configuration values through environment variables.
- Support documented frontend and backend run modes.
- Route help-task requests from entry channels through middleware to backend task creation.

### 2.3 User Classes

- Authenticated application users initiate login through Firebase-backed session flow.
- Logged-out or unauthenticated users trigger logout behavior or have no active user object.
- End users submit help-task requests through supported entry channels or forms.
- Maintainers and contributors modify and test the frontend, middleware, and backend behavior.
- Deployment and configuration operators provide environment variables and run the server modes.
- Integrators connect Firebase authentication and OnFleet task handling.

### 2.4 Operating Environment

The product shall run in a JavaScript and Next.js environment with frontend and backend server modes. Backend behavior shall use Firebase functions for custom APIs and OnFleet for task handling. Session APIs shall run as Next.js API routes with middleware support. Firebase configuration shall be loaded from environment variables at application configuration time.

### 2.5 Assumptions and Dependencies

- The authenticated user object supports `getIdToken()`.
- Firebase authentication and Firebase admin token verification are available to the login API.
- Session middleware is available and wraps login API handling.
- OnFleet is available for task creation when the task workflow reaches backend handling.
- Required environment variables are present before application startup.

## 3. External Interface Requirements

### 3.1 User Interface Requirements

#### UI-001 Frontend Form Entry

The frontend shall provide a form-based entry path for help-task requests.

#### UI-002 External User Channel Entry

The product shall support an end-user entry path through text or call based interaction where that channel is configured.

#### UI-003 Authentication-Driven Session Interaction

The frontend shall trigger session establishment or logout behavior through application logic rather than through a separately specified end-user screen in this SRS.

### 3.2 Software Interface Requirements

#### SI-001 Login API

The product shall expose `POST /api/login` for authenticated session establishment. The request body shall be a JSON object containing a `token` value.

#### SI-002 Logout API

The product shall expose `POST /api/logout` for session teardown.

#### SI-003 Firebase Token Verification

The login API shall use Firebase ID token verification during login processing.

#### SI-004 Session Middleware

The login API shall execute with middleware support that provides a server-side session object.

#### SI-005 OnFleet Task Interface

The backend task workflow shall call OnFleet task handling to create a task after middleware determines that the request should be served.

### 3.3 Communication Interface Requirements

#### CI-001 Login Request Communication

Login requests shall use HTTP `POST`, `Content-Type: application/json`, same-origin credentials, and a JSON body containing `token`.

#### CI-002 Logout Request Communication

Logout requests shall use HTTP `POST` and same-origin credentials.

#### CI-003 Frontend-to-Middleware Task Communication

Task requests from supported frontend or channel entry points shall be passed to middleware for address and service-area processing.

#### CI-004 Middleware-to-Backend Task Communication

Middleware shall pass eligible task requests to backend task handling for OnFleet task creation.

### 3.4 Data Exchange Formats

#### DI-001 Login Request Body

The login request body shall be JSON and shall contain a `token` field.

#### DI-002 Logout Request Body

The logout request shall not require a request body.

#### DI-003 Runtime Configuration Values

Firebase configuration values shall be mapped from environment variables into runtime configuration.

#### DI-004 Task Request Data

Task-request data shall include the user-provided information needed for address-to-neighborhood handling, service-area determination, and backend task creation.

## 4. Functional Requirements

### FR-001 Submit Login Request for Authenticated User

When a non-null user object is passed to the session handler, the system shall call `user.getIdToken()` and send `POST /api/login` with same-origin credentials and a JSON body containing the token.

**Priority:** High

**Verification:** Test.

**Acceptance Criteria:**

- A valid user object causes the session handler to request a Firebase ID token.
- The session handler sends `POST /api/login`.
- The login request body contains `{ "token": <token value> }`.
- The login request includes `Content-Type: application/json`.
- The login request uses same-origin credentials.

### FR-002 Submit Logout Request When User Is Absent

When no user object is passed to the session handler, the system shall send `POST /api/logout` with same-origin credentials.

**Priority:** High

**Verification:** Test.

**Acceptance Criteria:**

- An absent user object causes the session handler to send `POST /api/logout`.
- The logout request uses same-origin credentials.
- The logout request does not require a request body.

### FR-003 Validate Login Request Body

The login API shall reject a login request that does not provide a request body by setting HTTP status `400`.

**Priority:** High

**Verification:** Test.

**Acceptance Criteria:**

- A login request without a request body receives HTTP status `400`.
- A login request with a request body proceeds to token extraction.

### FR-004 Extract Login Token

The login API shall extract `token` from `req.body` when a login request body is present.

**Priority:** High

**Verification:** Inspection and test.

**Acceptance Criteria:**

- The `token` value is read from the request body.
- The extracted token is used for subsequent login processing.

### FR-005 Verify Firebase ID Token

The login API shall verify the Firebase ID token by invoking Firebase token verification with the extracted token.

**Priority:** High

**Verification:** Inspection and test.

**Acceptance Criteria:**

- Login processing invokes Firebase ID token verification.
- Successful verification produces decoded token data.
- Failed verification returns an error response.

### FR-006 Store Authentication Data in Server-Side Session

After successful Firebase ID token verification, the login API shall store the decoded token and original token in a server-side session object backed by session middleware.

**Priority:** High

**Verification:** Inspection and integration test.

**Acceptance Criteria:**

- The decoded token is assigned to the session object.
- The original token is assigned to the session object.
- Session handling is provided by middleware around the API handler.

### FR-007 Return Successful Login Response

After successful token verification and session update, the login API shall return a successful JSON response containing login status and decoded token data.

**Priority:** Medium

**Verification:** Test.

**Acceptance Criteria:**

- Successful login returns HTTP status `200`.
- The JSON response indicates successful status.
- The JSON response includes decoded token data.

### FR-008 Expose Firebase Runtime Configuration

The system shall map Firebase auth domain, database URL, project ID, and public API key from environment variables into runtime configuration.

**Priority:** Medium

**Verification:** Inspection.

**Acceptance Criteria:**

- `FIREBASE_AUTH_DOMAIN` is available in runtime configuration.
- `FIREBASE_DATABASE_URL` is available in runtime configuration.
- `FIREBASE_PROJECT_ID` is available in runtime configuration.
- `FIREBASE_PUBLIC_API_KEY` is available in runtime configuration.

### FR-009 Support Documented Server Run Modes

The product shall support run modes for starting both frontend and backend servers, starting only the frontend server, and starting only the backend server.

**Priority:** Medium

**Verification:** Demonstration.

**Acceptance Criteria:**

- One command can start both frontend and backend server behavior for development.
- One command can start only the frontend server.
- One command can start only the backend server.

### FR-010 Accept Help-Task Requests

The product shall accept help-task requests from supported end-user channels or the frontend form.

**Priority:** Medium

**Verification:** Demonstration and inspection.

**Acceptance Criteria:**

- A task request can be initiated from a configured user channel.
- A task request can be initiated from the frontend form.
- The task request is handed to middleware for processing.

### FR-011 Process Address and Service-Area Decision

The middleware shall process task-request address information to determine the relevant neighborhood and whether the product operates for that request.

**Priority:** Medium

**Verification:** Test.

**Acceptance Criteria:**

- Address information can be passed into middleware.
- Middleware determines a neighborhood value or equivalent routing result.
- Middleware determines whether the request is in an operated area.

### FR-012 Create OnFleet Task for Eligible Request

For an eligible task request, the backend shall create a task through OnFleet task handling.

**Priority:** Medium

**Verification:** Integration test or mocked API test.

**Acceptance Criteria:**

- An eligible request reaches backend task handling.
- Backend task handling calls OnFleet task creation.
- The task creation result can be observed by the workflow.

## 5. Non-Functional Requirements

### NFR-001 JSON Login Compatibility

Login requests shall use `Content-Type: application/json`.

**Metric:** All login requests generated by the session handler include the JSON content type header.

### NFR-002 Same-Origin Session Request Handling

Login and logout requests shall use same-origin credentials.

**Metric:** The session handler sends both login and logout requests with same-origin credential mode.

### NFR-003 Configuration Externalization

Firebase runtime configuration shall be externalized through environment variables rather than hard-coded directly into the application configuration.

**Metric:** The Firebase runtime configuration fields are populated from environment variables at application configuration time.

### NFR-004 Modular Task Handling

The task request workflow shall separate frontend entry, middleware decision logic, and backend OnFleet task creation responsibilities.

**Metric:** Architecture and tests can identify distinct frontend entry, middleware processing, and backend task creation responsibilities.

## 6. Data Requirements

### DR-001 User Object

The session handler shall accept a user object that can provide a Firebase ID token.

### DR-002 Firebase ID Token

The system shall exchange a Firebase ID token from the authenticated user object to the login API.

### DR-003 Login Request Payload

The login request payload shall be a JSON object containing `token`.

### DR-004 Session Authentication Data

The server-side session object shall store decoded token data and the original token after successful login verification.

### DR-005 Firebase Configuration Values

The application shall use environment-backed values for `FIREBASE_AUTH_DOMAIN`, `FIREBASE_DATABASE_URL`, `FIREBASE_PROJECT_ID`, and `FIREBASE_PUBLIC_API_KEY`.

### DR-006 Task Request Data

The task workflow shall carry user-provided task-request information from entry points into middleware.

### DR-007 Address and Neighborhood Data

The task workflow shall carry address information and derived neighborhood or routing data for service-area processing.

### DR-008 Service-Area Decision Data

The middleware shall produce a decision indicating whether the product operates for the given request.

### DR-009 OnFleet Task Data

The backend shall provide OnFleet with the task information required to create a task for an eligible request.

## 7. System Constraints

### CON-001 Firebase Configuration Constraint

Firebase runtime values shall be provided through environment variables in the project setup.

### CON-002 Backend Organization Constraint

The backend is organized into Firebase functions for custom APIs and OnFleet for task handling. This organization shall not be treated as excluding frontend, middleware, authentication, or task-request entry components from the overall architecture.

### CON-003 Session Endpoint Constraint

Internal authentication session operations shall use `/api/login` and `/api/logout`.

### CON-004 Middleware Session Constraint

Login API handling shall execute through middleware that provides session support.

### CON-005 Asset and Style Configuration Constraint

Application build configuration shall support CSS, Sass, and bundled static asset types including `png`, `jpg`, `gif`, `svg`, `eot`, `ttf`, `woff`, and `woff2`.

### CON-006 Development Run Mode Constraint

The development setup shall provide commands for both-server, frontend-only, and backend-only run modes.

## 8. Verification and Acceptance Criteria

| Requirement | Verification Method | Expected Result |
| --- | --- | --- |
| FR-001 | Test | Authenticated user produces a same-origin JSON `POST /api/login` request containing `token` |
| FR-002 | Test | Missing user produces a same-origin `POST /api/logout` request |
| FR-003 | Test | Login request without a body sets HTTP status `400` |
| FR-004 | Inspection and test | Login API extracts `token` from the request body |
| FR-005 | Inspection and test | Login API verifies the extracted Firebase ID token |
| FR-006 | Inspection and integration test | Decoded token data and token are written to the session object |
| FR-007 | Test | Successful login returns HTTP `200` and JSON success data |
| FR-008 | Inspection | Firebase runtime fields are mapped from environment variables |
| FR-009 | Demonstration | Both-server, frontend-only, and backend-only run modes can be started |
| FR-010 | Demonstration and inspection | Task requests from supported entry points reach middleware |
| FR-011 | Test | Middleware derives neighborhood or routing data and an operated-area decision |
| FR-012 | Integration test or mocked API test | Eligible requests create OnFleet tasks |
| NFR-001 | Test | Login requests include JSON content type |
| NFR-002 | Test | Login and logout requests use same-origin credentials |
| NFR-003 | Inspection | Firebase configuration is environment-driven |
| NFR-004 | Analysis and inspection | Frontend, middleware, and backend task responsibilities are separable |
