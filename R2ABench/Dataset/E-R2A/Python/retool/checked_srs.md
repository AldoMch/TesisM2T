# ReTool Software Requirements Specification (Standard SRS Extract)

## 1. Introduction

### Product Scope

ReTool is a requirements management tool for continuously evolving software projects. It supports user management, project management, and requirements management. Requirements management includes requirement itemization, requirement structuring, requirement conflict detection, common requirement identification, requirement association analysis, and forward tracing from requirements to design modules and test cases. The system adopts a front-end/back-end separated mode; the client uses Vue.js and the server uses a microservice architecture.

This document follows the terminology definitions in the requirements specification for microservices, Flask, NLP, PyTorch, Vue.js, and MongoDB. The specification does not provide REST paths, database collection structures, or message protocol details.

### Intended Audience

This document is intended for ReTool developers, testers, project managers, project leaders, ordinary project members, system administrators, requirements reviewers, and later architecture generation and acceptance testing workflows.

## 2. Overall Description

### Product Perspective

ReTool is a Web tool for requirement change and requirement analysis. The overall system uses front-end/back-end separation and a microservice architecture, including gateway, user management service, project management service, requirements management service, algorithm service, and MongoDB database. The specification states that gateway, user management, project management, and requirements management services run on a local computer, while the algorithm service runs on a server because of machine performance requirements. Activity diagrams split system processing logic into front-end/back-end and algorithm modules, and MongoDB performs data create, read, update, and delete operations.

### Product Functions Summary

| Capability | Summary |
| --- | --- |
| User management | Supports registration, login, logout, user deletion, password modification, user list, personal information, password reset, role modification, and adding users. |
| Project management | Supports project creation, deletion, modification, viewing, project lists, baseline nodes, project information, project members, and project role management. |
| Requirement item management | Supports requirement item creation, import, deletion, modification, movement, viewing, and requirement item tree display. |
| Requirement analysis | Supports requirement itemization, requirement structuring, common requirement identification, requirement conflict detection, and requirement association analysis. |
| Forward tracing | Supports establishing and viewing forward tracing information such as code, test cases, and trace personnel for requirements. |

### User Classes

| User Class | Responsibilities / Needs |
| --- | --- |
| Project manager | Overall project owner who uses the tool to create requirements, modify requirements, and manage projects. |
| Project leader | Uses the tool to create and modify requirements and assists project requirements management. |
| Ordinary project member | Completes development and testing according to requirements and views related requirements and tracing information. |
| System administrator | Maintains normal ReTool operation, adds or deletes users, modifies user system roles, resets passwords, and collects suggestions. |
| System user | Registers, logs in, and uses project and requirement functions according to project roles. |

### Operating Environment

| Environment | Requirement |
| --- | --- |
| Client hardware | Intel Core i7-6700HQ CPU, more than 100 MB available storage, complete network support, at least 8 GB memory, and Windows 10 64-bit operating system. |
| Client software | Google Chrome 81.0 or above. |
| Server hardware | Recommended EC2 t2.xlarge, 4 vCPU, 16 GB memory, and up to 5 Gbps network bandwidth. |
| Server operating system | Amazon Linux 2. |
| Service deployment | Gateway, user management service, project management service, and requirements management service run on a local computer, while the algorithm service runs on a server. |
| Network | When users cannot connect to the network, all requirements cannot be realized. |

### Assumptions and Dependencies

| ID | Assumption / Dependency |
| --- | --- |
| AD-001 | System functions depend on user network connection. |
| AD-002 | Requirement changes depend on the established requirement change process and specification review. |
| AD-003 | The algorithm service depends on a higher-performance server environment. |
| AD-004 | The system uses MongoDB as the database for create, read, update, and delete operations. |
| AD-005 | Users can assume different roles and have different permissions in different projects. |

## 3. External Interface Requirements

### User Interfaces

| Interface | Requirement |
| --- | --- |
| User authentication interface | Supports registration, login, logout, password modification, and viewing personal information. |
| User management interface | Supports system administrators viewing user lists, adding users, deleting users, resetting passwords, and modifying user roles. |
| Project list interface | Supports viewing participating projects, creating projects, deleting projects, and viewing/modifying project information. |
| Member management interface | Supports viewing, adding, and deleting project members and modifying project roles. |
| Baseline management interface | Supports creating and viewing project baseline nodes. |
| Requirements management interface | Supports requirement item tree, requirement item creation, import, modification, deletion, movement, content viewing, and trace viewing. |
| Requirement analysis interface | Supports selecting requirement analysis scope and executing structuring, common requirement identification, conflict detection, and association analysis. |

### Software/API Interfaces

| Interface | Requirement |
| --- | --- |
| Front-end framework | The client uses Vue.js to develop the Web user interface. |
| Server architecture | The server uses a microservice architecture; the terminology states that Flask is suitable for writing server-side code under a microservice architecture. |
| Algorithm service | The system uses NLP, PyTorch, Word2vec, and related algorithm capabilities to support requirement analysis. |
| Database | The MongoDB database accepts processing logic instructions, performs create, read, update, and delete operations, and returns data or execution results. |

### Communication Interfaces

The specification only explicitly states that services communicate through the network, the login system depends on Web interfaces, all requirements cannot be realized without network access, and network transmission and open Web interfaces must be secure. The specification does not specify REST, RPC, WebSocket, message queues, or concrete authentication protocols.

### Data Exchange Formats

The system needs to process data such as username, password, user role, project name, project description, project state, project members, project roles, baseline name and description, Word documents, requirement item name and description, state, priority, expected start/end time, structured results, common requirements, conflict information, association relationships, trace code, trace test cases, and trace personnel. The specification does not specify JSON, form fields, file upload protocols, or MongoDB collection schemas.

## 4. Functional Requirements

| ID | Requirement | Trigger / Input | System Behavior | Output | Priority | Verification |
| --- | --- | --- | --- | --- | --- | --- |
| FR-001 | The system shall support user registration. | A system user accesses the main interface, enters the registration interface, fills in username and password, and clicks register. | The system validates registration information, saves username and password after successful registration, and prompts an error and returns to the registration interface when the username is duplicated or the password does not meet requirements. | New user record, login interface redirect, or error prompt. | High | Test |
| FR-002 | The system shall support user login. | A registered user or administrator enters username and password. | The system confirms that the username exists and password is correct, then prompts successful login; when the username does not exist or password is wrong, it prompts login failure. | Login state or error prompt. | High | Test |
| FR-003 | The system shall support user logout. | A logged-in user clicks the logout button. | The system prompts successful logout and redirects to the main page, and the user loses all permissions in the system. | Unauthenticated state and main page. | High | Test |
| FR-004 | The system shall allow system administrators to delete users. | A system administrator selects user deletion in the user list interface. | The system deletes the selected user record and updates the user list. | User list after deletion. | High | Test |
| FR-005 | The system shall support modifying user passwords. | A logged-in user enters the personal information interface and submits a new password. | The system modifies the user password; if the password does not meet requirements, it prompts an error. | Password modification result or error prompt. | High | Test |
| FR-006 | The system shall allow system administrators to view the user list. | A system administrator enters the user management interface. | The system displays the system user list. | User list. | High | Test |
| FR-007 | The system shall support viewing user personal information. | A logged-in user enters the personal information interface. | The system displays the user's own personal information, such as phone and email. | Personal information page. | Medium | Demonstration |
| FR-008 | The system shall allow system administrators to reset user passwords. | A system administrator selects a user for password reset in the user management interface. | The system resets that user's password to the initial default password. | Password reset result. | High | Test |
| FR-009 | The system shall allow system administrators to modify user roles. | A system administrator selects a user in the user list and changes the user to administrator role. | The system changes the user's role and permissions. | Updated user role. | High | Test |
| FR-010 | The system shall allow system administrators to add users. | A system administrator enters the add-user interface, enters username and password, and selects a system role type. | The system saves the new user's username, password, and role, and returns to the user management interface. | New user record and user management interface. | High | Test |
| FR-011 | The system shall support project creation. | A user clicks create project in the project list interface, fills in project name, project description, project state, adds project members, and sets project roles. | The system creates the project and saves project members and project roles. | New project appears in the project list. | High | Test |
| FR-012 | The system shall allow project managers to delete projects. | A project manager clicks delete project in the project list and confirms. | The system deletes the corresponding project. | Project disappears from the project list. | High | Test |
| FR-013 | The system shall allow project managers to modify projects. | A project manager enters the project information interface from the project list. | The system allows the project manager to select project information or member management and modify corresponding information. | Updated project or member information. | High | Test |
| FR-014 | The system shall support viewing projects. | A user clicks the project information button for a project in the project list. | The system displays concrete project information and the project member management entry. | Project information or member information. | Medium | Test |
| FR-015 | The system shall support viewing the project list. | A user successfully logs in and clicks the project list in project management. | The system displays all projects in which the current user participates. | Project list. | High | Test |
| FR-016 | The system shall support creating project baseline nodes. | A project manager enters baseline management from the project information interface and fills in version name and version description. | The system creates a baseline node and archives current project requirement items; after baseline node creation, requirement items inside the node cannot continue to be changed. | Baseline node and baseline list. | High | Test |
| FR-017 | The system shall support viewing project baseline nodes. | A user enters baseline management from the project information interface and selects a baseline node. | The system displays all baseline nodes under the current project and supports viewing concrete node information. | Baseline node list and node details. | Medium | Test |
| FR-018 | The system shall allow project managers to modify project information. | A project manager enters the project information interface and edits text boxes. | The system saves modifications to project name, description, state, and related project information. | Updated project information. | High | Test |
| FR-019 | The system shall allow project managers to modify project members. | A project manager enters the member management interface. | The system allows the project manager to modify existing project member information. | Updated project member information. | High | Test |
| FR-020 | The system shall support viewing project information. | A user enters the project information interface. | The system displays concrete information about the current project by default. | Project information details. | Medium | Demonstration |
| FR-021 | The system shall support viewing project members. | A user enters the project information interface and clicks member management. | The system switches to the project member interface for that project. | Project member list. | Medium | Test |
| FR-022 | The system shall allow project managers to add project members. | A project manager adds a new member and sets a project role in the member management interface. | The system saves the new project member and corresponding role. | Updated project member list. | High | Test |
| FR-023 | The system shall allow project managers to delete project members. | A project manager deletes an existing member in the member management interface. | The system deletes the project member relationship. | Updated project member list. | High | Test |
| FR-024 | The system shall allow project managers to modify project roles. | A project manager modifies a project member's role in the member management interface. | The system updates that member's role in the project. | Updated project role. | High | Test |
| FR-025 | The system shall support creating requirement items. | A project manager or project leader enters requirements management, selects the operation item and insertion position, and selects the creation method. | The system creates a requirement item or calls subflows such as single-item creation and Word import. | New requirement item displayed in requirements management. | High | Test |
| FR-026 | The system shall support creating a single requirement item. | A project manager or project leader selects a non-text-import method and fills in requirement name, description, state, priority, and expected start/end time. | The system saves the single requirement item and may prompt the user to perform requirement analysis. | New requirement item and its basic information. | High | Test |
| FR-027 | The system shall support importing requirement items from Word. | A project manager or project leader selects import from text and uploads a Word document. | The system uploads the document to the server, performs itemization and requirement analysis, and completes requirement item creation; if no document is uploaded or itemization fails, it prompts failure. | Imported requirement items or failure prompt. | High | Test |
| FR-028 | The system shall support requirement itemization. | A user imports a Word document and clicks start itemization. | The server performs itemization analysis on the document and returns results. | Itemized requirement items. | High | Test |
| FR-029 | The system shall support deleting requirement items. | A project manager or project leader selects a requirement item to delete and confirms. | The system deletes the requirement item; when the user selects the root requirement item, it prompts that this type of requirement item cannot be deleted. | Requirement item disappears from the item tree or error prompt. | High | Test |
| FR-030 | The system shall support modifying requirement items. | A project manager or project leader selects a requirement item to modify and enters the modification interface. | The system allows modifying requirement item content or moving requirement item position and saves the modification. | Modified content displayed in the requirement item tree. | High | Test |
| FR-031 | The system shall support modifying requirement item content. | A project manager or project leader selects the main information or basic information tab of a requirement item and edits it. | The system saves modifications to name, description, state, priority, and similar fields, and may prompt the user whether to perform requirement analysis. | Updated requirement item content. | High | Test |
| FR-032 | The system shall support moving requirement item positions. | A project manager or project leader enters the requirement item position adjustment interface and drags an item. | The system saves the new position of the requirement item in the requirement item tree. | Updated requirement item tree. | High | Test |
| FR-033 | The system shall support establishing requirement forward tracing. | A project manager or project leader selects a requirement item, enters the requirement tracing tab, and fills in trace code, trace test cases, and trace personnel. | The system saves requirement forward tracing information. | Forward tracing content in the requirement item. | High | Test |
| FR-034 | The system shall support entering requirement analysis. | A project manager or project leader clicks requirement analysis on the project main interface. | The system enters the requirement analysis tab and displays selectable concrete analysis functions. | Requirement analysis function selection interface. | High | Demonstration |
| FR-035 | The system shall support requirement structuring. | A user clicks requirement structuring in requirement analysis. | The system uses NLP tools and heuristic rules to analyze requirement items, extract finer-grained syntactic elements, and save structured results. | Requirement structuring result. | High | Test |
| FR-036 | The system shall support common requirement identification. | A user clicks common requirement identification in requirement analysis. | The system uses a trained Word2vec model to detect requirements with basically the same semantics; when common requirements exist, it displays numbers and content, otherwise it gives a prompt. | Common requirement list or no-common prompt. | High | Test |
| FR-037 | The system shall support requirement conflict detection. | A user clicks conflict detection in requirement analysis. | The system uses NLP tools and heuristic rules to detect conflicts in requirement items; when conflicts exist, it displays concrete content, otherwise it prompts that no conflict exists. | Conflict detection result. | High | Test |
| FR-038 | The system shall support requirement association analysis. | A user clicks association analysis in requirement analysis. | The system uses NLP tools and heuristic rules to detect association relationships among requirement items; when associations exist, it displays relationship type and requirement items at both ends, otherwise it prompts that no association exists. | Association analysis result. | High | Test |
| FR-039 | The system shall support viewing the requirement item tree. | A user clicks a project name and enters the project home page. | The system renders all requirement items in the project as a tree structure according to requirement item hierarchy relationships. | Requirement item tree. | High | Test |
| FR-040 | The system shall support viewing requirement item content. | A user clicks a concrete requirement item. | The system displays concrete information such as the requirement item name and description. | Requirement item details. | Medium | Demonstration |
| FR-041 | The system shall support viewing requirement forward tracing. | A user clicks a requirement item and enters the requirement tracing tab. | The system displays forward tracing content such as trace code, trace tests, and trace personnel for the requirement item. | Forward tracing details. | Medium | Test |

## 5. Non-Functional Requirements

| ID | Quality | Requirement | Fit Criterion | Priority | Verification |
| --- | --- | --- | --- | --- | --- |
| NFR-001 | Performance | The time from user click to first interface display shall be controlled. | Time from click to first interface display does not exceed 1 second. | High | Test |
| NFR-002 | Reliability | The system mean time to failure shall satisfy the threshold. | Mean time to failure > 720 h. | High | Analysis |
| NFR-003 | Reliability | The system mean time to repair shall satisfy the threshold. | Mean time to repair < 30 min. | High | Analysis |
| NFR-004 | Reliability | The data loss rate after system failure shall conform to the specification threshold. | Data loss rate after failure < 99%; this threshold is preserved according to the original source wording and should be confirmed during review. | Medium | Analysis |
| NFR-005 | Reliability | The system shall have automatic release and fault removal capability after errors occur. | After fault injection, the system can automatically recover or enter a recoverable state. | High | Test |
| NFR-006 | Reliability | User-uploaded information shall be persisted quickly. | Time for saving uploaded user information to disk < 1 s. | High | Test |
| NFR-007 | Resource Usage | System memory usage shall be controlled during runtime. | Memory usage < 80%. | High | Test |
| NFR-008 | Resource Usage | System CPU usage shall be controlled during runtime. | CPU usage < 80%. | High | Test |
| NFR-009 | Reliability | The database shall be backed up periodically and support offsite disaster recovery. | The database is backed up periodically, with three-copy offsite disaster recovery backup. | High | Inspection |
| NFR-010 | Security | The login system shall comply with Web security specifications. | Login Web interfaces pass security specification checks. | High | Test |
| NFR-011 | Privacy | The system shall protect user privacy information and personalized information. | Privacy and personalized data are protected by access control and protection measures. | High | Inspection |
| NFR-012 | Security | The system shall identify illegal user inputs and malicious behavior. | Illegal inputs and malicious behavior are identified and recorded. | High | Test |
| NFR-013 | Security | The system shall prevent requirement input from causing database injection attacks. | Requirement input content is restricted and validated, and injection attacks are blocked. | High | Test |
| NFR-014 | Security | Front-end code shall reduce the risk that captured request packets lead to requirement information copying or tampering. | Front-end code uses protection strategies such as minimization and mixing/obfuscation. | Medium | Inspection |
| NFR-015 | Security | The system shall ensure functional module security. | Network transmission, data storage, file storage, and open Web interfaces have security measures. | High | Inspection |
| NFR-016 | Security | The system shall establish permissions for developers and sensitive commands. | Developer and sensitive command permissions can be checked. | High | Inspection |
| NFR-017 | Maintainability | Software structure and documents shall support performance adjustment. | The system has good structure and complete documents, and performance adjustment points can be identified. | Medium | Inspection |
| NFR-018 | Maintainability | Documents shall be clear, readable, and uniformly written. | Documents pass standardization and readability checks. | Medium | Inspection |
| NFR-019 | Maintainability | Server deployment and logs shall support issue tracing. | Deployment process is concise and standardized, and logs are persistently saved, readable, and traceable. | High | Test |
| NFR-020 | Maintainability | The product shall reserve upgrade interfaces and upgrade space. | Design descriptions reflect upgrade interfaces and extension space. | Medium | Inspection |
| NFR-021 | Usability | Interaction design shall reduce user thinking and operation costs. | Users can obtain target information in three clicks or fewer, and important information is presented on the main interface or in obvious locations. | Medium | Demonstration |
| NFR-022 | Usability | The system shall reduce user input and support personalized experience. | Selection lists and search input autocomplete are used, personalized information is recorded, and direct login is supported on revisits. | Medium | Demonstration |
| NFR-023 | UI Design | Interface design shall be unified, adaptive, and compliant with Web design specifications. | Flat style is unified, screen size is adaptive, visual effect is harmonious, icons are concise and intuitive, and colors and text satisfy the specification requirements. | Medium | Inspection |

## 6. Data Requirements

| ID | Data Object | Requirement | Rationale / Constraint | Verification |
| --- | --- | --- | --- | --- |
| DR-001 | User account | The system shall save user information such as username, password, phone, and email. | Supports registration, login, personal information viewing, and password modification. | Test |
| DR-002 | User roles and permissions | The system shall save system roles and permissions such as system user and system administrator. | Supports user role modification, administrator operations, and permission control. | Test |
| DR-003 | Project | The system shall save project name, project description, and project state. | Supports project creation, modification, viewing, and deletion. | Test |
| DR-004 | Project member relationship | The system shall save member relationships for users participating in projects. | Supports viewing, adding, and deleting project members. | Test |
| DR-005 | Project role | The system shall save project roles held by users in different projects. | Supports different role permissions in different projects and project role modification. | Test |
| DR-006 | Project baseline node | The system shall save baseline node name, description, and archived requirement items. | Supports creating and viewing project baseline nodes; after baseline creation, requirements inside the node cannot continue to be changed. | Test |
| DR-007 | Requirement item | The system shall save requirement item name, description, state, priority, and expected start/end time. | Supports creating, viewing, modifying, deleting, and moving requirement items. | Test |
| DR-008 | Word document | The system shall receive and upload Word documents to the server. | Supports importing requirement items from Word and requirement itemization. | Test |
| DR-009 | Requirement item tree | The system shall save hierarchy relationships and positions among requirement items. | Supports tree display and moving requirement item positions. | Test |
| DR-010 | Requirement structuring result | The system shall save syntactic elements extracted by NLP tools and heuristic rules. | Supports other requirement analysis algorithm services. | Test |
| DR-011 | Common requirement identification result | The system shall save or display numbers and content of requirements with basically the same semantics. | Supports common requirement identification. | Test |
| DR-012 | Conflict detection result | The system shall save or display concrete requirement conflict content. | Supports requirement conflict detection and later handling. | Test |
| DR-013 | Association analysis result | The system shall save or display association relationship type and requirement items at both ends. | Supports requirement association analysis. | Test |
| DR-014 | Forward tracing information | The system shall save trace code, trace test case, and trace personnel information. | Supports establishing and viewing requirement forward tracing. | Test |
| DR-015 | Log | The system shall persistently save readable logs. | Supports issue tracing and maintenance. | Inspection |
| DR-016 | Privacy and personalized information | The system shall protect user privacy information and personalized information. | Supports security and confidentiality requirements. | Inspection |

## 7. Constraints

| ID | Constraint |
| --- | --- |
| C-001 | Requirement changes must strictly follow the requirement change process, and the requirements specification must be reasonably modified and reviewed. |
| C-002 | The overall tool adopts a front-end/back-end separated mode. |
| C-003 | The front end shall use a lightweight, community-supported, and maintainable framework; the product description explicitly states that the client uses Vue.js. |
| C-004 | The server uses a microservice architecture. |
| C-005 | During runtime, the system needs to limit simultaneous access volume; when the peak is exceeded, some user processes are blocked until the current carrying capacity can handle new processes. |
| C-006 | Gateway, user management service, project management service, and requirements management service run on a local computer. |
| C-007 | The algorithm service runs on a server because of machine performance requirements. |
| C-008 | When users cannot connect to the network, all requirements cannot be realized. |
| C-009 | Client hardware shall satisfy Intel Core i7-6700HQ CPU, more than 100 MB available storage, complete network support, and at least 8 GB memory. |
| C-010 | The client operating system is Windows 10 64-bit. |
| C-011 | The client browser is Google Chrome 81.0 or above. |
| C-012 | Recommended server configuration is EC2 t2.xlarge, 4 vCPU, 16 GB memory, and up to 5 Gbps network bandwidth. |
| C-013 | The server operating system is Amazon Linux 2. |
| C-014 | The database is MongoDB, responsible for accepting processing logic instructions and performing create, read, update, and delete operations. |

## 8. Verification and Acceptance

| ID | Verification | Acceptance Criterion |
| --- | --- | --- |
| FR-001 | Test | A user can register successfully, and prompts are shown when the username is duplicated or the password is noncompliant. |
| FR-002 | Test | Correct username and password log in successfully, and wrong credentials fail login. |
| FR-003 | Test | After logout, the user loses system permissions and returns to the main page. |
| FR-004 | Test | After an administrator deletes a user, the user list is updated. |
| FR-005 | Test | User password can be changed, and invalid passwords are rejected. |
| FR-006 | Test | An administrator can view the system user list. |
| FR-007 | Demonstration | A user can view personal information. |
| FR-008 | Test | An administrator can reset a user's password to the default password. |
| FR-009 | Test | An administrator can modify a user's system role and permissions. |
| FR-010 | Test | An administrator can add a new user and save username, password, and role. |
| FR-011 | Test | A user can create a project and see the new project in the project list. |
| FR-012 | Test | A project manager can delete a project, and the deleted project no longer appears in the list. |
| FR-013 | Test | A project manager can modify project or member information. |
| FR-014 | Test | A user can view concrete project information and the project member entry. |
| FR-015 | Test | A logged-in user can view all projects they participate in. |
| FR-016 | Test | A project manager can create a baseline node and archive current requirement items. |
| FR-017 | Test | A user can view the project baseline node list and details. |
| FR-018 | Test | A project manager can save project information modifications. |
| FR-019 | Test | A project manager can modify project member information. |
| FR-020 | Demonstration | A user can view concrete information of the current project. |
| FR-021 | Test | A user can view the project member list. |
| FR-022 | Test | A project manager can add project members and set roles. |
| FR-023 | Test | A project manager can delete project members. |
| FR-024 | Test | A project manager can modify project member roles. |
| FR-025 | Test | A user can create requirement items through the add flow. |
| FR-026 | Test | A user can create a single requirement item and save main and basic information. |
| FR-027 | Test | A user can import requirement items from Word, and abnormal import receives a prompt. |
| FR-028 | Test | The system can execute requirement itemization on an uploaded Word document and return results. |
| FR-029 | Test | A user can delete non-root requirement items, and root requirement item deletion is rejected. |
| FR-030 | Test | A user can modify a requirement item and see the update in the item tree. |
| FR-031 | Test | A user can modify main and basic information of a requirement item. |
| FR-032 | Test | A user can move a requirement item and save the new position. |
| FR-033 | Test | A user can save requirement forward tracing information. |
| FR-034 | Demonstration | A user can enter the requirement analysis tab and see concrete functions. |
| FR-035 | Test | The system can generate and save requirement structuring results. |
| FR-036 | Test | The system can display common requirement numbers and content or no-common prompt. |
| FR-037 | Test | The system can display conflict details or no-conflict prompt. |
| FR-038 | Test | The system can display association relationship type and requirement items at both ends or no-association prompt. |
| FR-039 | Test | The system can render requirement items as a tree structure. |
| FR-040 | Demonstration | A user can view requirement item name and description. |
| FR-041 | Test | A user can view requirement forward tracing content. |
| NFR-001 | Test | Time from click to first interface display does not exceed 1 second. |
| NFR-002 | Analysis | Mean time to failure is greater than 720 hours. |
| NFR-003 | Analysis | Mean time to repair is less than 30 minutes. |
| NFR-004 | Analysis | Data loss rate threshold is checked according to the original source wording and marked for confirmation. |
| NFR-005 | Test | After failure, the system automatically recovers or enters a recoverable state. |
| NFR-006 | Test | Uploaded information is saved to disk in less than 1 second. |
| NFR-007 | Test | Memory usage is below 80%. |
| NFR-008 | Test | CPU usage is below 80%. |
| NFR-009 | Inspection | The database is backed up periodically and has three-copy offsite disaster recovery. |
| NFR-010 | Test | The login interface passes Web security specification testing. |
| NFR-011 | Inspection | Privacy and personalized information protection mechanisms exist. |
| NFR-012 | Test | Illegal input and malicious behavior are identified and recorded. |
| NFR-013 | Test | Database injection attacks through requirement input are blocked. |
| NFR-014 | Inspection | Front-end code protection strategy is applied. |
| NFR-015 | Inspection | Security measures exist for network transmission, data storage, file storage, and open interfaces. |
| NFR-016 | Inspection | Developer and sensitive command permissions can be audited. |
| NFR-017 | Inspection | System structure and documentation support performance adjustment. |
| NFR-018 | Inspection | Documents are clear, readable, and uniformly standardized. |
| NFR-019 | Test | Logs are persistently saved and can be used for issue tracing. |
| NFR-020 | Inspection | Upgrade interfaces and extension space are reserved in the design. |
| NFR-021 | Demonstration | Target information can be obtained in three clicks or fewer. |
| NFR-022 | Demonstration | Selection lists, autocomplete, and personalized information recording are available. |
| NFR-023 | Inspection | The interface satisfies unified, adaptive, icon, color, and text requirements. |
| DR-001 | Test | User account data can be created, read, and modified. |
| DR-002 | Test | User roles and permissions can be saved and modified. |
| DR-003 | Test | Project data can be created, read, modified, and deleted. |
| DR-004 | Test | Project member relationships can be added, deleted, and queried. |
| DR-005 | Test | Project roles can be saved and modified. |
| DR-006 | Test | Baseline nodes can be saved and associated with archived requirement items. |
| DR-007 | Test | Main and basic requirement item information can be saved and modified. |
| DR-008 | Test | Word documents can be uploaded and used for itemization. |
| DR-009 | Test | Requirement item hierarchy relationships and positions can be saved. |
| DR-010 | Test | Requirement structuring results can be saved. |
| DR-011 | Test | Common requirement identification results can be displayed or saved. |
| DR-012 | Test | Conflict detection results can be displayed or saved. |
| DR-013 | Test | Association analysis results can be displayed or saved. |
| DR-014 | Test | Forward tracing information can be saved and viewed. |
| DR-015 | Inspection | Logs can be persisted and used for tracing. |
| DR-016 | Inspection | Privacy and personalized information protection measures exist. |
| C-001 | Inspection | Requirement change records follow the process and update the requirements specification. |
| C-002 | Inspection | System design reflects front-end/back-end separation. |
| C-003 | Inspection | The front-end framework satisfies lightweight, community-supported, and maintainable constraints and uses Vue.js. |
| C-004 | Inspection | The server adopts a microservice architecture. |
| C-005 | Test | Simultaneous access limit and blocking/waiting strategy are effective. |
| C-006 | Inspection | Gateway and core management service deployment locations conform to constraints. |
| C-007 | Inspection | The algorithm service is deployed on the server. |
| C-008 | Test | Without network connection, system functions are unavailable or have explicit failure behavior. |
| C-009 | Inspection | Client hardware configuration satisfies constraints. |
| C-010 | Inspection | Client operating system is Windows 10 64-bit. |
| C-011 | Inspection | Chrome version is no lower than 81.0. |
| C-012 | Inspection | Server hardware satisfies the recommended configuration. |
| C-013 | Inspection | Server operating system is Amazon Linux 2. |
| C-014 | Inspection | Database is MongoDB and performs create, read, update, and delete operations. |
