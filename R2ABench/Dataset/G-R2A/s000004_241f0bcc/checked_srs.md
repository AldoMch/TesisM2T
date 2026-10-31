# Software Requirements Specification

## 1. Introduction

### 1.1 Purpose
This SRS defines the final checked requirements for the EMBC ESS application scope covered here. It is prepared as a clean input for downstream architecture diagram generation.

### 1.2 Product Scope
The system scope covered by this SRS focuses on:
- An Angular front-end ClientApp that runs in a web browser.
- HTTP communication from the front-end to a backend API.
- Role-based routing, login/session handling, and HTTP request interception in the front-end.
- Selected client-side shared state managed through NgRx.
- Front-end service wrappers for evacuee, incident-task, organization, referral, registration, notification, and controlled-list behavior.
- Repository SQL scripts for managing selected data in an MS SQL database.

The broader architecture context includes an Angular client, HTTP API communication, a .NET Core WebAPI server, controllers, C# domain classes, domain services, Entity Framework/DbContext, and persistent database entities. Detailed backend business behavior beyond the named API interactions is outside the behavioral scope of this checked SRS unless explicitly listed below.

### 1.3 Intended Audience
- Product owners and business analysts.
- Front-end, API, and database developers.
- Test engineers and system integrators.
- Operators and database administrators.
- Architecture reviewers generating or validating architecture diagrams.

### 1.4 Terminology
| Term | Definition |
|---|---|
| ClientApp | Browser-based Angular front-end application. |
| Backend API | Server-side HTTP API consumed by the ClientApp. |
| SiteMinder | Authentication/access-control mechanism respected by the front-end/API integration. |
| Development back door | Backend-only mechanism enabled only in designated development environments to support developer access. |
| Role-paired token | Development token associated with a front-end role such as `volunteer`, `local authority`, or `provincial admin`. |
| Controlled-list loader | Initialization behavior that loads infrequently changing controlled-list data into the client store; it is not modeled here as a parameterized HTTP endpoint. |
| NgRx store | Client-side state container and data cache/sharing mechanism. |

## 2. Overall Description

### 2.1 Product Perspective
The system is a browser-based front-end application that depends on a backend API for runtime operation. The broader architecture has a front-end layer, an HTTP API/server layer, a domain-service layer, Entity Framework/DbContext data access, and persistent database entities. The front-end also uses client-side state management for selected shared data and includes repository scripts for MS SQL data maintenance.

### 2.2 Architecture Context
The architecture context for diagram generation includes:
- Angular front-end ClientApp.
- HTTP API communication between the front-end and server-side services.
- .NET Core WebAPI server and controllers.
- C# domain classes and domain services.
- Entity Framework/DbContext for data access.
- Persistent database entities.
- MS SQL database maintenance scripts.
- SiteMinder-aware authentication context.

No queue component is required by this SRS.

### 2.3 Product Functions
- Direct users to landing routes appropriate for their roles.
- Enforce login and role checks on routed pages.
- Redirect unauthenticated users to login.
- Log out users and show a session-expired page after unauthorized API responses while the application is in a logged-in state.
- Reset a watchdog timer on client HTTP activity.
- Load controlled-list data at application initialization into the NgRx store.
- Perform supported operations against evacuee, incident-task, organization, referral, and registration API service wrappers.
- Queue user notifications for notifier display.
- Route to external URLs through a redirect guard.
- Alert developers when a module is double-loaded.
- Include registration-service PDF collection capability at a high level.
- Support MS SQL data-maintenance scripts for selected operational tasks.

### 2.4 User Classes
| User Class | Description |
|---|---|
| Role-based front-end user | User whose landing route and route access depend on assigned role. |
| Logged-in user | User with an active application session subject to unauthorized-response and session-expiry handling. |
| Developer | User running the front-end locally with proxy configuration and role-paired development tokens. |
| System integrator/operator | User responsible for front-end/API integration, authentication configuration, and runtime environment setup. |
| Database operator/administrator | User executing repository SQL scripts against the MS SQL database. |

### 2.5 Operating Environment
- Web browser for the Angular front-end.
- Backend HTTP API required by the front-end.
- .NET Core WebAPI and domain service runtime for the broader server-side architecture.
- Entity Framework/DbContext data-access layer.
- MS SQL database for data scripts and persistent entities.
- NgRx for selected client-side state.
- Local development setup with proxy configuration and role-paired tokens.

### 2.6 Assumptions and Dependencies
- The front-end requires a backend API and is not standalone.
- Local development requires proxy configuration and role-paired `SM_TOKEN` values for `volunteer`, `local authority`, and `provincial admin`.
- The application must respect SiteMinder.
- The development back door is backend-only and enabled only in designated development environments.
- SQL maintenance scripts require access to the target MS SQL database.
- Backend API payload schemas and detailed server-side workflows must be specified separately when needed.

## 3. External Interface Requirements

### 3.1 User Interfaces
| Interface | Requirement |
|---|---|
| Landing routing | The system shall direct users to the route appropriate for their assigned role. |
| Login handling | The system shall redirect unauthenticated users to the login page. |
| Session-expired page | The system shall show a session-expired page after applicable unauthorized API responses. |
| Notifications | The system shall allow queued notifications to be observed by a notifier component and displayed to users. |
| External redirect | The system shall support routing to an external URL through a redirect guard. |
| Developer diagnostic alert | The system shall alert a developer when a module is double-loaded. |

### 3.2 Software/API Interfaces
| Interface | Requirement |
|---|---|
| Backend API | The ClientApp shall consume a backend API for runtime operation. |
| Evacuee service | The front-end shall support read operations with parameters for evacuee data. |
| Incident-task service | The front-end shall support create, read, and update operations with parameters for incident-task data. |
| Organization service | The front-end shall support create, read, and update operations with parameters for organization data. |
| Referral service | The front-end shall support create, read, update, and delete operations with parameters for referral data. |
| Registration service | The front-end shall support create, read, and update operations with parameters for registration data. |
| Registration PDF collection | The registration service shall include PDF collection capability; detailed PDF payload schema is not specified here. |
| Notification queue service | The front-end shall add user notifications to a queue that can be observed by a notifier component. |
| Controlled-list loader | The front-end shall load infrequently changing controlled-list data during initialization and place it into the NgRx store. |
| Cookie service | The front-end shall support get and set operations for cookies. |

### 3.3 Communication Interfaces
| Interface | Requirement |
|---|---|
| Client HTTP requests | Client HTTP requests shall be subject to unauthorized-response handling and watchdog timer reset behavior. |
| Local development API access | Local development API access shall use proxy configuration and role-paired tokens. |
| Frontend-to-API communication | The browser front-end shall communicate with the backend API through HTTP interactions. |
| API-to-data-layer communication | Server-side components shall interact with persistent data through domain services and Entity Framework/DbContext in the broader architecture. |

### 3.4 Data Exchange Formats
Parameterized endpoint operations are required for the named front-end service wrappers. Detailed payload schemas, registration PDF schemas, and message formats are not specified in this SRS and should be defined in API-level contracts when needed.

## 4. Functional Requirements

| ID | Requirement | Trigger/Input | System Behavior | Output | Priority | Verification |
|---|---|---|---|---|---|---|
| FR-001 | Role-based landing routing | User reaches the landing page. | The system shall direct the user to the route appropriate for the user's role. | User is routed to a role-appropriate page. | High | Demonstration |
| FR-002 | Login and route-role enforcement | User attempts to access the application or a routed page. | The system shall allow access only when the user is logged in, redirect unauthenticated users to login, and check the user's role against the role specified in routing. | Authorized users proceed; unauthorized users are redirected or blocked from mismatched routes. | High | Test |
| FR-003 | Unauthorized-response session handling | A client HTTP request returns `401` while application state is logged in. | The system shall log out the user and cause the session-expired page to be shown. | User session ends and the session-expired page is displayed. | High | Test |
| FR-004 | Watchdog reset on HTTP activity | Any client HTTP request is made. | The system shall reset the watchdog timer on each HTTP request. | Watchdog timer is refreshed. | Medium | Test |
| FR-005 | Controlled-list initialization loading | Application initialization. | The system shall load infrequently changing controlled-list data at initialization and place it into the NgRx store. | Controlled-list data is available in client state. | Medium | Test |
| FR-006 | Business endpoint operation support | Client requests operations against supported business service wrappers. | The system shall support read for evacuee; create/read/update for incident-task, organization, and registration; and create/read/update/delete for referral, using endpoint parameters. | Requested API operation is issued to the corresponding service wrapper. | High | Test |
| FR-007 | User notification display flow | A notification is added for a user. | The system shall place the notification in the notification queue so that a notifier component can observe and display it. | Notification becomes available for user display. | Medium | Demonstration |
| FR-008 | Redirect guard | A route requires navigation to an external URL. | The system shall support a redirect guard that routes to an external URL using the router. | User is routed to the configured external URL. | Medium | Demonstration |
| FR-009 | Module import diagnostic | A module is double-loaded during development or application composition. | The system shall alert a developer that the module has been double-loaded. | Developer receives a diagnostic alert. | Low | Inspection |
| FR-010 | Registration PDF collection capability | Registration service handles registration-related operations. | The system shall include PDF collection capability in the registration service. | PDF collection behavior is available for registration-related workflows. | Low | Inspection |
| FR-011 | SQL volunteer deactivation | Database operator executes the volunteer deactivation script with a target volunteer identifier. | The system's SQL script shall set `Volunteer.Active` to `0` for the matching volunteer `Id`. | Matching volunteer is deactivated in the target database after permanent execution. | Medium | Test |

## 5. Non-Functional Requirements

| ID | Quality Attribute | Requirement | Priority | Verification |
|---|---|---|---|---|
| NFR-001 | Security | The development API bypass mechanism shall be backend-only and shall be enabled only in a specifically designated development environment. | High | Inspection |
| NFR-002 | Compatibility | The front-end shall operate in a web browser and depend on a backend API for runtime operation. | High | Demonstration |
| NFR-003 | Data consistency | For models placed in the NgRx store, client state shall be represented as a single immutable data structure, with state changes described by actions and computed through reducers. | Medium | Inspection |
| NFR-004 | Session integrity | Unauthorized API responses while the application is logged in shall terminate the session and display the session-expired user flow. | High | Test |

## 6. Data Requirements

### 6.1 Data Entities and Structures
| ID | Data Item | Requirement |
|---|---|---|
| DR-001 | Client-side shared state | The system shall maintain selected shared client-side data in an NgRx store used as a client-side data cache and sharing mechanism. |
| DR-002 | Controlled-list data | Infrequently changing controlled-list data shall be loaded at initialization and stored for client use. |
| DR-003 | Endpoint request parameters | Supported endpoint service wrappers shall accept parameters when performing documented operations. |
| DR-004 | Notification queue data | User notifications shall be represented in a queue that can be observed by notifier components. |
| DR-005 | Registration PDF collection data | Registration PDF collection data exists as a registration-service concern; detailed schema is not specified here. |
| DR-006 | Volunteer activation status | SQL scripts shall support setting `Volunteer.Active` to `0` for a matching `Id` when deactivating a volunteer. |
| DR-007 | SQL script execution safety | SQL scripts shall target filtered data through a variable at the top of the script and run within a transaction. |
| DR-008 | Role-paired development tokens | Local development shall use role-paired `SM_TOKEN` values for `volunteer`, `local authority`, and `provincial admin`. |

### 6.2 Input and Output Data
| Data Flow | Requirement |
|---|---|
| Role input | User role information shall determine landing route and route access. |
| HTTP request input | Client HTTP requests shall trigger watchdog reset behavior and unauthorized-response handling. |
| Controlled-list output | Controlled-list loading shall produce client-store data available after initialization. |
| Endpoint operation output | Supported service wrappers shall issue the requested create, read, update, or delete operation to the backend API. |
| Notification output | Added notifications shall become observable by notifier components. |
| SQL script output | Data-management scripts shall update filtered target data only after intentional permanent execution. |

### 6.3 Storage, Integrity, Privacy, Retention, and Migration
| Topic | Requirement |
|---|---|
| NgRx state integrity | Stored client models shall follow the NgRx single immutable state pattern. |
| SQL script safety | SQL scripts shall use target-filter variables and transaction structure to reduce unintended data changes. |
| Database backup prerequisite | Target database backup is required as a precaution before SQL script execution. |
| Persistent data layer | Persistent database entities are managed through the broader server-side data layer. |
| Privacy, retention, and migration | Privacy, retention, deletion, and migration behavior are not specified in this SRS. |

## 7. System Constraints

| ID | Constraint |
|---|---|
| CON-001 | The front-end requires a backend API and is not standalone. |
| CON-002 | Local development requires proxy configuration and role-paired tokens for `volunteer`, `local authority`, and `provincial admin`. |
| CON-003 | The application must respect SiteMinder; the development bypass is backend-only and limited to designated development environments. |
| CON-004 | Repository data-management scripts target an MS SQL database. |
| CON-005 | The target database must be backed up before executing repository SQL scripts. |
| CON-006 | Controlled-list behavior shall be treated as initialization data loading into the client store, not as a parameterized HTTP endpoint in this SRS. |
| CON-007 | Backend API payload schemas and detailed server-side business logic are not defined in this SRS. |

## 8. Verification and Acceptance Criteria

| Requirement ID | Verification Method | Acceptance Criteria |
|---|---|---|
| FR-001 | Demonstration | A user reaching the landing page is routed to the page appropriate for the user's role. |
| FR-002 | Test | Logged-in users can access matching role routes; unauthenticated users are redirected to login; users with mismatched roles are redirected or blocked. |
| FR-003 | Test | A `401` response during logged-in application state logs out the user and displays the session-expired page. |
| FR-004 | Test | Each client HTTP request resets the watchdog timer. |
| FR-005 | Test | Controlled-list data is loaded during initialization and becomes available in the NgRx store. |
| FR-006 | Test | The front-end service wrappers issue the supported operations for evacuee, incident-task, organization, referral, and registration. |
| FR-007 | Demonstration | Added notifications are observable by the notifier component and can be displayed to users. |
| FR-008 | Demonstration | A configured redirect guard routes to the intended external URL. |
| FR-009 | Inspection | The module import diagnostic behavior alerts developers when a module is double-loaded. |
| FR-010 | Inspection | The registration service includes PDF collection capability. |
| FR-011 | Test | The volunteer deactivation script sets `Volunteer.Active` to `0` for the matching `Id` when permanently executed. |
| NFR-001 | Inspection | The development API bypass is backend-only and enabled only in the designated development environment. |
| NFR-002 | Demonstration | The front-end runs in a browser and communicates with the backend API. |
| NFR-003 | Inspection | Stored client models follow the NgRx single immutable state, action, and reducer pattern. |
| NFR-004 | Test | Unauthorized API responses during logged-in state terminate the session and show the session-expired flow. |
| DR-001 | Inspection | Selected shared client-side data is stored in NgRx. |
| DR-002 | Test | Controlled-list data is loaded and cached for client use. |
| DR-003 | Test | Supported service wrapper operations accept and use request parameters. |
| DR-004 | Demonstration | Notifications added to the queue are observable by notifier components. |
| DR-005 | Inspection | Registration PDF collection data handling exists as a registration-service concern. |
| DR-006 | Test | Volunteer deactivation changes the matching volunteer active status. |
| DR-007 | Inspection | SQL scripts include a target-filter variable and transaction structure. |
| DR-008 | Inspection | Local development token configuration includes role-paired values for `volunteer`, `local authority`, and `provincial admin`. |
| CON-001 | Inspection | Front-end runtime configuration requires backend API availability. |
| CON-002 | Inspection | Local development setup includes proxy configuration and role-paired tokens. |
| CON-003 | Inspection | SiteMinder and development-bypass constraints are documented in runtime setup. |
| CON-004 | Inspection | Repository data-management scripts target MS SQL. |
| CON-005 | Inspection | Operational instructions require target database backup before SQL script execution. |
