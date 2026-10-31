# Software Requirements Specification

## 1. Introduction

### 1.1 Purpose
This SRS defines the final checked requirements for Bunny Code, a collaborative coding website with project workspaces, code execution, coding-process replay, real-time battle workflows, authentication, file distribution, and deployment infrastructure. It is prepared as a clean requirements input for downstream architecture diagram generation.

### 1.2 Product Scope
Bunny Code supports:
- User registration, login, JWT authentication, and user detail query.
- Project creation, query, update, version management, and initial file creation.
- Browser-based code editing and workspace authorization.
- Code compilation or execution with returned execution results.
- Recording and playback of coding processes by project, version, and time range.
- Real-time workspace collaboration using socket channels.
- Real-time battle invitation, battle acceptance, readiness, code synchronization, judging, ending, and leave handling.
- Upload and distribution of code files, battle result files, user files, static assets, and archive files.
- Backend coordination through Node.js/Express, REST APIs, Socket.IO channels, MySQL, InfluxDB, Redis, Docker-based code execution, S3-compatible object storage, CloudFront-style distribution, Nginx reverse proxying, and automated deployment flow.

### 1.3 Intended Audience
- Developers implementing frontend, backend, socket, storage, and deployment components.
- Testers validating authentication, project workflows, code execution, replay, battles, and file handling.
- Integrators connecting Bunny Code to databases, cache, object storage, CDN, sandbox, and deployment environments.
- Architecture analysts generating architecture diagrams from the checked requirements.

### 1.4 Terminology
| Term | Definition |
|---|---|
| Workspace | A live project/version editing session accessed by a socket client. |
| Project | A coding workspace entity owned or accessed by users and composed of versions and files. |
| Version | A project revision used for editing, execution, recording, and playback. |
| Battle | A real-time coding competition between users with invitations, readiness, synchronized code, judging, and outcome handling. |
| Battle invitation | A temporary cache-backed invitation created by an inviter and accepted by another user. |
| Coding-process record | Time-series editing data used to replay a user's coding process. |
| Object storage | External storage used for code files, archives, battle files, user files, and distributable URLs. |

## 2. Overall Description

### 2.1 Product Perspective
Bunny Code is a frontend/backend web system. The Vue frontend communicates with the Node.js/Express backend through REST APIs and Socket.IO. The backend manages users, projects, versions, compilation, process recording, battles, and file archives. MySQL stores relational data such as users, projects, versions, problems, and battles. InfluxDB stores time-series coding-process records. Redis supports live workspace coordination and battle state. A Docker sandbox executes user code. Object storage and CDN distribution provide code archives, static assets, and downloadable files. Nginx and automated deployment scripts support runtime delivery.

### 2.2 Product Functions
- Authenticate users through JWT bearer tokens and reject invalid authentication input.
- Manage user accounts and user details.
- Manage projects, project versions, and initial files.
- Authorize workspace access and emit authorization/read-only status to socket clients.
- Coordinate live workspace editing state, editing occupation, workspace leaving, and disconnect cleanup.
- Compile or execute submitted code and return execution results.
- Record coding operations and query replay records for playback.
- Create, accept, synchronize, judge, and end real-time coding battles.
- Upload and distribute code files, battle result files, user files, static assets, and archives.
- Coordinate cache-dependent workflows through Redis.

### 2.3 User Classes
| User Class | Description |
|---|---|
| Visitor | A user who can access public entry points and initiate registration or login. |
| Authenticated user | A user represented by authenticated identity data and allowed to access projects, workspaces, and battles. |
| Project owner or collaborator | A user who creates, edits, queries, or manages projects and versions. |
| Battle participant | A user who sends or accepts battle invitations and participates in real-time battle flows. |
| Maintainer | An operator or developer responsible for backend services, storage, cache, sandbox, and deployment configuration. |

### 2.4 Operating Environment
- Browser frontend runtime for the Vue application.
- Node.js server runtime for Express and Socket.IO services.
- REST API and Socket.IO communication between frontend and backend.
- MySQL for relational application data.
- InfluxDB for time-series coding-process records.
- Redis for live workspace and battle coordination.
- Docker-based sandbox for code compilation or execution.
- S3-compatible object storage and CDN distribution for files and archives.
- Nginx reverse proxy and automated deployment environment.

### 2.5 Assumptions and Dependencies
- JWT authentication depends on a configured token signing and validation mechanism.
- Workspace and battle operations that use cache depend on Redis readiness.
- Code execution depends on an available sandbox environment.
- Process replay depends on persisted time-series coding records.
- File distribution depends on available object storage and URL distribution configuration.
- Final Redis persistence, checksum, append-only, protected mode, and authentication details are deployment configuration decisions rather than mandatory product behavior unless selected for the target deployment.

## 3. External Interface Requirements

### 3.1 User Interfaces
| ID | Interface | Requirement |
|---|---|---|
| UI-001 | Web frontend | The system shall provide a browser-based frontend for login, project workspaces, code editing, playback, and battle participation. |
| UI-002 | Workspace editor | The frontend shall allow users to edit code within an authorized project/version workspace. |
| UI-003 | Battle view | The frontend shall allow users to send, accept, play, and leave real-time battles. |
| UI-004 | Playback view | The frontend shall allow users to inspect coding-process playback records by project, version, and time range. |

### 3.2 Software and API Interfaces
| ID | Interface | Requirement |
|---|---|---|
| API-001 | Authentication API | The backend shall support user registration, login, JWT authentication, and user detail query. |
| API-002 | JWT authentication function | The backend shall accept a JWT bearer token and, when valid, resolve it to an authenticated user information object. |
| API-003 | Invalid JWT handling | The backend shall reject empty or malformed JWT bearer-token input by raising an API error. |
| API-004 | Project API | The backend shall support creating, querying, and updating projects. |
| API-005 | Version API | The backend shall support creating project versions and initial files for versions. |
| API-006 | Code execution API | The backend shall accept submitted code for compilation or execution and return execution results. |
| API-007 | Playback API | The backend shall support querying coding-process records by project, version, and time range. |
| API-008 | File upload API | The backend shall upload code files, battle result files, and user-related files to object storage and return distributable URLs. |
| API-009 | Socket workspace API | The backend shall use socket channels for workspace authorization, edit state, editing occupation, leave handling, and disconnect cleanup. |
| API-010 | Socket battle API | The backend shall use socket channels for battle invitation, acceptance, readiness, code synchronization, judging, outcome, and leave handling. |

### 3.3 Communication Interfaces
| ID | Interface | Requirement |
|---|---|---|
| COM-001 | REST communication | The frontend and backend shall exchange request/response data over REST-style HTTP APIs. |
| COM-002 | Socket.IO communication | The frontend and backend shall use real-time socket events for workspaces and battles. |
| COM-003 | Redis communication | The backend shall use Redis cache operations for live workspace coordination and battle state. |
| COM-004 | Database communication | The backend shall communicate with MySQL for relational data and InfluxDB for time-series records. |
| COM-005 | Sandbox communication | The backend shall invoke a Docker-based execution environment to compile or execute submitted code. |
| COM-006 | Object storage and CDN communication | The backend shall upload files to object storage and provide URLs suitable for distribution. |

### 3.4 Data Exchange Formats
| ID | Format | Required Content |
|---|---|---|
| DEF-001 | JWT bearer token | Token string used for authenticated requests. |
| DEF-002 | User information object | At least `id`, `name`, and `email`. |
| DEF-003 | Project access request | Project identifier and version identifier. |
| DEF-004 | Project status object | `readOnly` and `authorization` fields. |
| DEF-005 | Workspace socket mapping | Socket identifier mapped to an active project version or workspace session. |
| DEF-006 | Battle invitation object | Invitation socket identifier, battle name, battle difficulty, inviter user ID, and inviter username. |
| DEF-007 | Battle acceptance input | Acceptor socket context plus `socketID` and `firstUserID` fields identifying the temporary invitation and inviter. |
| DEF-008 | Battle state object | Participant readiness, code content, remaining chances per participant, and problem answer data. |
| DEF-009 | Execution result | Compilation or execution status, output, and error details where applicable. |
| DEF-010 | Playback query | Project, version, and time-range filters. |
| DEF-011 | File upload result | Distributable URL and file metadata. |

## 4. Functional Requirements

| ID | Requirement | Trigger/Input | System Behavior | Output | Priority | Verification |
|---|---|---|---|---|---|---|
| FR-001 | The system shall support user registration, login, JWT authentication, and user detail query. | User submits account or authentication request. | The backend creates or validates user identity and returns the requested account details when authorized. | User session or user detail response. | High | Test |
| FR-002 | The system shall validate a provided JWT bearer token and return the authenticated user's information when the token is valid. | Valid JWT bearer-token input. | The backend parses and validates the token and resolves the authenticated identity. | User information object containing at least `id`, `name`, and `email`. | High | Test |
| FR-003 | The system shall reject empty or malformed JWT bearer-token input. | Empty token, malformed token, or bearer prefix without a token. | The backend detects invalid authentication input and fails authentication. | API error. | High | Test |
| FR-004 | The system shall support creating, querying, and updating projects. | Authenticated user submits project operations. | The backend validates authorization and persists or retrieves project data. | Project operation result. | High | Test |
| FR-005 | The system shall support creating project versions and initial files. | Authenticated user creates a version or initializes project files. | The backend creates version metadata and associated initial file records or file assets. | Version and initial-file result. | High | Test |
| FR-006 | The system shall accept submitted code for compilation or execution and return execution results. | User submits code for execution. | The backend routes the submission to the sandbox and collects the execution outcome. | Execution result with status, output, and errors where applicable. | High | Test |
| FR-007 | The system shall record user coding processes and support playback queries. | User edits code or requests playback records. | The backend records coding events and retrieves playback data by project, version, and time range. | Coding-process record or playback data. | High | Test |
| FR-008 | The system shall evaluate workspace project access and emit authorization status through a socket event. | Socket request contains a project object. | The backend sets default `readOnly: true` and `authorization: false`; if project identifier or version identifier is missing, it emits the default status; otherwise it evaluates project authorization and emits the resulting status. | `statusChecked` event with a project status object. | High | Demonstration |
| FR-009 | The system shall persist workspace socket/version mapping in Redis for non-read-only project access when Redis is ready. | Project access is authorized as non-read-only and Redis is ready. | The backend stores the socket-to-version or workspace mapping before emitting status. | Redis mapping and `statusChecked` event. | Medium | Inspection |
| FR-010 | The system shall support workspace editing state, editing occupation, leaving workspace, and disconnect cleanup through sockets. | Workspace socket events occur. | The backend updates workspace state, coordinates editing occupation, removes leaving users, and cleans up disconnected socket state. | Updated workspace state events and cleared stale mappings. | High | Test |
| FR-011 | The system shall allow authenticated users to create battle invitations. | User initiates a battle invitation. | The backend creates a temporary invitation containing invitation socket identifier, battle name, battle difficulty, inviter user ID, and inviter username. | Temporary battle invitation. | High | Test |
| FR-012 | The system shall limit repeated battle invitations within a short period and delete temporary invitations after timeout. | User repeatedly creates invitations or invitation timeout expires. | The backend checks temporary invitation state and removes expired invitation data. | Rejected duplicate invitation or removed expired invitation. | Medium | Test |
| FR-013 | The system shall accept battle invitations using Redis isolated execution and watched cache state. | Battle acceptance request includes `socketID` and `firstUserID`. | The backend checks Redis readiness, reads the temporary invitation, and deletes the corresponding cache entry so the same invitation cannot be consumed repeatedly. | Accepted temporary invitation data. | High | Inspection |
| FR-014 | The system shall create a battle when a valid invitation is accepted by a user who is not the inviter. | Valid battle invitation is accepted. | The backend creates a battle record, initializes both users' battle state, and emits battle-created-success events to both users. | Battle record, initialized battle state, and success events. | High | Test |
| FR-015 | The system shall fail battle acceptance when the invitation is expired, the inviter and acceptor are the same user, cache read fails, or battle creation fails. | Invalid or failed battle acceptance path. | The backend returns a battle-failed socket event or socket error. | Battle-failed outcome. | High | Test |
| FR-016 | The system shall support battle readiness, code synchronization, compile-and-judge, win/loss ending, and leave handling. | Battle participant sends a battle socket event. | The backend updates battle state, synchronizes code, invokes judging or execution flow, determines outcomes, and handles participant leave events. | Battle state updates and participant outcome events. | High | Test |
| FR-017 | The system shall upload code files, battle result files, and user-related files to object storage. | User or battle workflow uploads a file. | The backend stores the file in object storage and records related metadata. | Stored file metadata and distributable URL. | Medium | Test |
| FR-018 | The system shall distribute static assets and archive files through configured URL distribution. | User or frontend requests distributed assets. | The system provides URLs that allow retrieval of stored assets or archives. | Distributable asset or archive URL. | Medium | Demonstration |

## 5. Non-Functional Requirements

| ID | Requirement | Quality Attribute | Priority | Verification |
|---|---|---|---|---|
| NFR-001 | The battle invitation acceptance flow shall use Redis isolated execution and watched cache state to control concurrent access, so that the same temporary invitation can be consumed by at most one acceptance flow under concurrent acceptance. | Reliability / concurrency control | High | Inspection and concurrent acceptance test |
| NFR-002 | Cache-dependent workspace and battle operations shall verify Redis readiness before executing cache operations. | Availability dependency | High | Inspection |
| NFR-003 | Authentication-protected APIs and socket workflows shall require a valid authenticated user context before performing user-specific operations. | Security | High | Test |
| NFR-004 | Project workspace authorization shall preserve read-only behavior for unauthorized, incomplete, or missing project/version requests. | Access control | High | Test |
| NFR-005 | Code execution shall run through an isolated sandbox environment rather than directly inside the main backend process. | Safety / isolation | High | Inspection |
| NFR-006 | Coding-process playback data shall be retrievable by project, version, and time range. | Usability / data retrievability | Medium | Test |
| NFR-007 | Uploaded files and archive outputs shall be retrievable through distributable URLs after successful storage. | Interoperability | Medium | Demonstration |
| NFR-008 | Automated deployment shall support the configured frontend, backend, reverse proxy, cache, databases, sandbox, object storage, and distribution services. | Deployability | Medium | Inspection |

## 6. Data Requirements

| ID | Data Item | Requirement |
|---|---|---|
| DR-001 | User account data | The system shall store user identity data needed for registration, login, authentication, and user detail query. |
| DR-002 | User information object | Authentication success data shall include at least `id`, `name`, and `email`. |
| DR-003 | JWT token | Authentication input shall be supplied as a bearer token string; empty or malformed token input is invalid. |
| DR-004 | Project data | The system shall store project metadata needed for creation, query, update, authorization, and workspace access. |
| DR-005 | Version and file data | The system shall store project version metadata and initial file data. |
| DR-006 | Project access request | Workspace authorization checks shall use project identifier and version identifier. |
| DR-007 | Project status object | Project authorization responses shall contain `readOnly` and `authorization` fields. |
| DR-008 | Workspace socket mapping | Redis shall store live workspace socket/version mappings when authorized workspace access is non-read-only and cache is ready. |
| DR-009 | Coding-process record | The system shall store time-series editing data sufficient to support playback by project, version, and time range. |
| DR-010 | Battle invitation data | A temporary battle invitation shall include invitation socket identifier, battle name, battle difficulty, inviter user ID, and inviter username. |
| DR-011 | Battle cache data | Battle cache data shall include temporary invitation data and formal battle state data. |
| DR-012 | Battle state data | Formal battle state shall include participant readiness state, code content, remaining chances by participant, and problem answer data. |
| DR-013 | Battle record data | The system shall store battle records and battle outcomes needed for result management. |
| DR-014 | Execution result data | Code execution results shall include execution status, output, and error details where applicable. |
| DR-015 | File metadata | Uploaded files and generated archives shall have metadata sufficient to return distributable URLs. |
| DR-016 | Redis configuration data | Redis connection shall support deployment-provided host, port, username, and password settings; product requirements do not mandate specific Redis default persistence, checksum, append-only, or ACL options unless selected by deployment configuration. |

## 7. System Constraints

| ID | Constraint |
|---|---|
| C-001 | The backend shall run in a Node.js/Express server environment with Socket.IO support. |
| C-002 | The frontend shall run as a Vue browser application. |
| C-003 | Relational data shall be stored in MySQL. |
| C-004 | Coding-process replay data shall be stored in InfluxDB or an equivalent time-series store configured for the deployment. |
| C-005 | Live workspace and battle coordination shall depend on Redis readiness. |
| C-006 | Battle acceptance shall use Redis isolated execution with watched read/delete semantics for temporary invitation consumption. |
| C-007 | Redis connectivity shall be configured through deployment environment values for host, port, username, and password. |
| C-008 | Redis persistence, checksum, append-only, protected mode, and default user password settings are deployment configuration choices and shall not be treated as mandatory product-level behavior unless adopted by the target deployment. |
| C-009 | Code compilation or execution shall be performed through a Docker-based sandbox. |
| C-010 | Code files, battle result files, user files, static assets, and archive files shall be stored through object storage and distributed through configured URLs. |
| C-011 | Nginx reverse proxying and automated deployment scripts shall align with the configured frontend, backend, cache, databases, sandbox, object storage, and CDN endpoints. |

## 8. Verification and Acceptance Criteria

| Requirement IDs | Verification Method | Acceptance Criteria |
|---|---|---|
| FR-001, FR-002, FR-003, DR-001, DR-002, DR-003, NFR-003 | Test | Valid login or JWT input authenticates the user and returns user identity data; empty or malformed token input fails with an API error; protected operations require authenticated user context. |
| FR-004, FR-005, DR-004, DR-005 | Test | Authenticated users can create, query, and update projects, create versions, and initialize files; unauthorized operations are rejected. |
| FR-006, DR-014, NFR-005, C-009 | Test and inspection | Submitted code is executed through the sandbox and returns execution status, output, and errors without direct execution in the main backend process. |
| FR-007, DR-009, NFR-006, C-004 | Test | Coding-process records are stored and can be queried for playback by project, version, and time range. |
| FR-008, FR-009, FR-010, DR-006, DR-007, DR-008, NFR-002, NFR-004 | Demonstration and inspection | Workspace socket requests emit authorization/read-only status; missing project or version data produces read-only unauthorized status; non-read-only workspace access writes cache mapping only when Redis is ready; leave and disconnect cleanup remove stale state. |
| FR-011, FR-012, DR-010 | Test | Battle invitations contain the required invitation fields, repeated invitations within the configured short period are limited, and expired temporary invitations are deleted. |
| FR-013, NFR-001, C-006 | Inspection and concurrent acceptance test | Battle acceptance uses Redis isolated execution and watched cache state; after a temporary invitation is read, the corresponding entry is deleted and cannot be successfully accepted repeatedly. |
| FR-014, FR-015, FR-016, DR-011, DR-012, DR-013 | Test | Valid battle acceptance creates a battle, initializes participant state, and emits success events; invalid or failed acceptance emits a battle-failed outcome; readiness, code synchronization, judging, outcome, and leave handling update battle state correctly. |
| FR-017, FR-018, DR-015, NFR-007, C-010 | Test and demonstration | Uploaded files and archives are stored with metadata and return distributable URLs that can be used to retrieve the assets. |
| NFR-008, C-001, C-002, C-003, C-005, C-007, C-008, C-011 | Inspection | Deployment configuration defines the frontend, backend, reverse proxy, Redis, MySQL, InfluxDB, sandbox, object storage, and distribution endpoints; Redis default persistence/authentication options are treated as deployment choices unless explicitly adopted. |
