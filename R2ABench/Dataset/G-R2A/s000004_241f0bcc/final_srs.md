# Software Requirements Specification

## 1. Introduction

### Purpose
This SRS defines evidence-backed requirements for the supported components of the `bcgov/embc-ess` repository at commit `19d9e1c803e5ba2a7fed5ca53f8a44c16d717d25`, based only on the provided repository evidence pack.

### Product scope
The evidence supports a web front-end application that:
- runs in a web browser,
- consumes a backend API,
- applies role-based routing and login/session handling,
- performs HTTP operations against several business endpoints,
- uses a client-side store for selected shared data,
- and includes SQL scripts for managing data in an MS SQL database.

### Intended audience
- Product owners and business analysts
- Developers and testers
- System integrators and operators
- Database administrators maintaining repository-provided SQL scripts

### References
- Repository: `bcgov/embc-ess`
- Commit: `19d9e1c803e5ba2a7fed5ca53f8a44c16d717d25`
- Evidence sources:
  - `E001` `embc-app/ClientApp/README.md`
  - `E003` `embc-app/ClientApp/src/app/core/README.md`
  - `E004` `embc-app/ClientApp/src/app/core/README.md`
  - `E005` `embc-app/ClientApp/src/app/store/README.md`
  - `E006` `sql-scripts/readme.md`

## 2. Overall Description

### Product perspective
The product is a browser-based front-end that depends on an API for operation and integrates with role-based access and session handling. It also includes database-maintenance SQL scripts for an MS SQL database. The front-end uses an NgRx store for selected client-side state. Sources: `E001`, `E004`, `E005`, `E006`.

### Product functions summary
Supported functions evidenced in the repository include:
- directing users to routes appropriate for their role,
- redirecting unauthenticated users to login,
- checking route access against user role,
- logging out users and showing a session-expired page after unauthorized API responses,
- resetting a watchdog timer on HTTP requests,
- loading infrequently changing controlled-list data at initialization,
- performing endpoint operations for evacuee, incident-task, organization, referral, and registration services,
- queuing and displaying user notifications,
- managing selected MS SQL data through repository SQL scripts.  
Sources: `E003`, `E004`, `E005`, `E006`.

### User classes
| User class | Description | Source |
|---|---|---|
| Role-based front-end users | Users whose landing route and route access depend on assigned role | `E001`, `E004` |
| Logged-in users | Users with active application session subject to unauthorized/session-expiry handling | `E004` |
| Developers | Users running the front-end locally with proxy and role-paired tokens in a designated development environment | `E001` |
| Database operators/administrators | Users executing repository SQL scripts against the MS SQL database | `E006` |

### Operating environment
| Aspect | Requirement-supported environment | Source |
|---|---|---|
| Client runtime | Web browser | `E001` |
| Backend dependency | API required by the front-end | `E001` |
| Local development | Designated development environment using proxy and tokens | `E001` |
| Database | MS SQL Database for repository SQL scripts | `E006` |

### Assumptions and dependencies
- The front-end requires an API to consume. `E001`
- Development access depends on proxy and three role-paired tokens. `E001`
- The application respects SiteMinder, with a backend-only development back door enabled only in a specifically designated development environment. `E001`
- SQL maintenance scripts depend on access to the target MS SQL database. `E006`

## 3. External Interface Requirements

### User interfaces
| Interface | Requirement-supported behavior | Source |
|---|---|---|
| Landing page routing | Users are directed to the correct route for their role | `E004` |
| Login/session handling | Unauthenticated users are redirected to login; expired sessions lead to a session expired page | `E004` |
| Notifications | A notifier component can observe queued notifications and display them to users | `E003` |

### Software/API interfaces
| Interface | Supported operation | Source |
|---|---|---|
| `evacuee` endpoint | HTTP service performs read operations with parameters | `E003` |
| `incident-task` endpoint | HTTP service performs create, read, and update operations with parameters | `E003` |
| `organization` endpoint | HTTP service performs create, read, and update operations with parameters | `E003` |
| `referral` endpoint | HTTP service performs create, read, update, and delete operations with parameters | `E003` |
| `registration` endpoint | HTTP service performs create, read, and update operations with parameters | `E003` |
| `controlled-list` endpoint/data source | Loads infrequently changing data at initialization into the client store | `E003` |

### Communication interfaces
| Interface | Supported behavior | Source |
|---|---|---|
| Client HTTP requests | Requests are subject to unauthorized-response handling and watchdog timer reset | `E004` |
| Local development API access | Uses proxy and tokens; development bypass is backend-only and environment-limited | `E001` |

### Data exchange formats
Supported evidence identifies parameterized HTTP endpoint usage and PDF collection in the registration service, but does not define payload schemas or message formats in the evidence pack. Sources: `E003`.

## 4. Functional Requirements

| ID | Description | Trigger/Input | System behavior | Output | Priority | Verification | Source evidence |
|---|---|---|---|---|---|---|---|
| FR-001 | Role-based landing routing | User reaches the landing page | The system shall direct the user to the route appropriate for the user's role | User is routed to a role-appropriate page | High | Demonstration | `E004` |
| FR-002 | Login and route-role enforcement | User attempts to access the application or a routed page | The system shall allow access only when the user is logged in, redirect unauthenticated users to the login page, and check the user's role against the role specified in routing | Authorized users proceed; unauthorized users are redirected or blocked from mismatched routes | High | Test | `E004` |
| FR-003 | Unauthorized-response session handling | An HTTP request returns `401` while application state is logged in | The system shall log out the user and cause the session expired page to be shown | User session ends and session expired page is displayed | High | Test | `E004` |
| FR-004 | Watchdog reset on HTTP activity | Any client HTTP request is made | The system shall reset the watchdog timer on each HTTP request | Watchdog timer is refreshed | Medium | Test | `E004` |
| FR-005 | Controlled-list initialization loading | Application initialization | The system shall load infrequently changing controlled-list data at initialization and place it into the NgRx store | Controlled-list data is available in client state | Medium | Test | `E003`, `E005` |
| FR-006 | Endpoint operations support | Client requests operations against supported business endpoints | The system shall support: read for `evacuee`; create/read/update for `incident-task`, `organization`, and `registration`; and create/read/update/delete for `referral`, using endpoint parameters | Requested endpoint operation is issued to the corresponding API | High | Test | `E003` |
| FR-007 | User notification display flow | A notification is added for a user | The system shall place the notification in the notification queue so that a notifier component can observe and display it | Notification becomes available for user display | Medium | Demonstration | `E003` |

## 5. Non-Functional Requirements

| ID | Quality attribute | Requirement | Priority | Verification | Evidence type | Source evidence |
|---|---|---|---|---|---|---|
| NFR-001 | Security | The development API bypass mechanism shall be backend-only and shall be enabled only in a specifically designated development environment | High | Inspection | explicit | `E001` |
| NFR-002 | Compatibility | The front-end shall operate in a web browser and depend on an API for runtime operation | High | Demonstration | explicit | `E001` |
| NFR-003 | Data consistency | For models placed in the NgRx store, client state shall be represented as a single immutable data structure | Medium | Inspection | explicit | `E005` |
| NFR-004 | Maintainability | The client store usage shall be limited to models where significant benefit is found, rather than universally applied | Low | Inspection | explicit | `E005` |

## 6. Data Requirements

| ID | Data requirement | Type | Details | Verification | Evidence type | Source evidence |
|---|---|---|---|---|---|---|
| DR-001 | Client-side shared state | Data structure | The system shall maintain selected client-side shared data in an NgRx store used as a client-side data cache/sharing mechanism | Inspection | explicit | `E005` |
| DR-002 | Controlled-list data | Input/cache data | Infrequently changing controlled-list data shall be loaded at initialization and stored for client use | Test | explicit | `E003`, `E005` |
| DR-003 | Endpoint request parameters | Input data | Supported endpoint services shall accept parameters when performing their documented operations | Test | explicit | `E003` |
| DR-004 | Volunteer activation status | Stored data | Repository SQL scripts shall support setting `Volunteer.Active` to `0` for a matching `Id` when deactivating a volunteer | Test | explicit | `E006` |
| DR-005 | SQL script execution safety | Data integrity | Repository SQL scripts shall target filtered data via a variable at the top of the script and run within a transaction | Inspection | explicit | `E006` |

## 7. Constraints

| ID | Constraint | Source evidence |
|---|---|---|
| CON-001 | The front-end requires an API to consume and is not evidenced as standalone | `E001` |
| CON-002 | Local development requires proxy configuration and three tokens paired to front-end roles | `E001` |
| CON-003 | The application must respect SiteMinder; development bypass is limited to designated development environments | `E001` |
| CON-004 | Repository data-management scripts target an MS SQL Database | `E006` |
| CON-005 | Target database backup is required as a precaution before executing repository SQL scripts | `E006` |

## 8. Verification and Acceptance

| Requirement IDs | Verification method |
|---|---|
| FR-001, FR-007, NFR-002 | Demonstration |
| FR-002, FR-003, FR-004, FR-005, FR-006, DR-002, DR-003, DR-004 | Test |
| NFR-001, NFR-003, NFR-004, DR-001, DR-005, CON-001, CON-002, CON-003, CON-004, CON-005 | Inspection |

Acceptance is achieved when each listed requirement is verified by its assigned method using the repository-supported behavior and constraints above.

## 9. Traceability Matrix

| ID | Requirement | Type | Source | Evidence Type | Verification | Confidence |
|---|---|---|---|---|---|---|
| FR-001 | Direct user to correct route for role from landing page | Functional | `E004` | explicit | Demonstration | High |
| FR-002 | Enforce login and route-role checks | Functional | `E004` | explicit | Test | High |
| FR-003 | Log out and show session expired page on `401` while logged in | Functional | `E004` | explicit | Test | High |
| FR-004 | Reset watchdog timer on each HTTP request | Functional | `E004` | explicit | Test | High |
| FR-005 | Load controlled-list data at initialization into store | Functional | `E003`, `E005` | explicit | Test | High |
| FR-006 | Support documented operations on named endpoints | Functional | `E003` | explicit | Test | High |
| FR-007 | Queue notifications for observation and display | Functional | `E003` | explicit | Demonstration | Medium |
| NFR-001 | Development API bypass limited to backend-only designated development environment | Non-functional | `E001` | explicit | Inspection | High |
| NFR-002 | Browser-based front-end with required API dependency | Non-functional | `E001` | explicit | Demonstration | High |
| NFR-003 | Single immutable client state structure for stored models | Non-functional | `E005` | explicit | Inspection | Medium |
| NFR-004 | Store usage limited to models with significant benefit | Non-functional | `E005` | explicit | Inspection | Medium |
| DR-001 | Use NgRx store as client-side data cache/sharing | Data | `E005` | explicit | Inspection | High |
| DR-002 | Store controlled-list data loaded at initialization | Data | `E003`, `E005` | explicit | Test | High |
| DR-003 | Accept parameters for supported endpoint operations | Data | `E003` | explicit | Test | High |
| DR-004 | Support setting `Volunteer.Active = 0` by matching `Id` | Data | `E006` | explicit | Test | High |
| DR-005 | Execute SQL scripts with target-filter variable and transaction | Data | `E006` | explicit | Inspection | High |
| CON-001 | Front-end requires API | Constraint | `E001` | explicit | Inspection | High |
| CON-002 | Local development requires proxy and three role-paired tokens | Constraint | `E001` | explicit | Inspection | High |
| CON-003 | SiteMinder-respecting development bypass constraint | Constraint | `E001` | explicit | Inspection | High |
| CON-004 | SQL scripts target MS SQL Database | Constraint | `E006` | explicit | Inspection | High |
| CON-005 | Backup target database before SQL script execution | Constraint | `E006` | explicit | Inspection | High |
