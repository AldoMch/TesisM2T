# ReTool Software Requirements Specification (Standard SRS Extract)

## 1. Introduction

### Purpose

This document extracts verifiable requirements from `Software Requirements Analysis - Group I - ReTool Requirements Specification V1.3.0.md` and rewrites them according to the compact SRS standard in `architectural_views_rep-pkg/script/templates/SRS.md`. The goal is to provide structured input for architecture generation, test design, and requirements tracing for the ReTool requirements management tool. Source evidence is recorded in `retool_md_evidence_pack.json`. (Source: RT-001)

### Product Scope

ReTool is a requirements management tool for continuously evolving software projects. It supports user management, project management, and requirements management. Requirements management includes requirement itemization, requirement structuring, requirement conflict detection, common requirement identification, requirement association analysis, and forward tracing from requirements to design modules and test cases. The system adopts a front-end/back-end separated mode; the client uses Vue.js and the server uses a microservice architecture. (Source: RT-002, RT-003)

This document follows the terminology definitions in the source requirements document for microservices, Flask, NLP, PyTorch, Vue.js, and MongoDB. The source document does not provide REST paths, database collection structures, or message protocol details. (Source: RT-001, RT-006)

### Intended Audience

This document is intended for ReTool developers, testers, project managers, project leaders, ordinary project members, system administrators, requirements reviewers, and later architecture generation and acceptance testing workflows. (Source: RT-001, RT-004)

### References

| Ref | Source |
| --- | --- |
| REF-001 | GB/T 9385-2008 Computer Software Requirements Specification |
| REF-002 | GB/T 20918-2007 Information Technology, Software Life Cycle Process and Risk Management |
| REF-003 | GB/T 15532-2008 Computer Software Testing Specification |
| REF-004 | GB/T 20917-2007 Software Engineering and Software Measurement Process |

## 2. Overall Description

### Product Perspective

ReTool is a Web tool for requirement change and requirement analysis. The overall system uses front-end/back-end separation and a microservice architecture, including gateway, user management service, project management service, requirements management service, algorithm service, and MongoDB database. The source document states that gateway, user management, project management, and requirements management services run on a local computer, while the algorithm service runs on a server because of machine performance requirements. Activity diagrams split system processing logic into front-end/back-end and algorithm modules, and MongoDB performs data create, read, update, and delete operations. (Source: RT-002, RT-005, RT-006)

### Product Functions Summary

| Capability | Summary | Source |
| --- | --- | --- |
| User management | Supports registration, login, logout, user deletion, password modification, user list, personal information, password reset, role modification, and adding users. | RT-003, RT-007 |
| Project management | Supports project creation, deletion, modification, viewing, project lists, baseline nodes, project information, project members, and project role management. | RT-003, RT-008 |
| Requirement item management | Supports requirement item creation, import, deletion, modification, movement, viewing, and requirement item tree display. | RT-003, RT-009 |
| Requirement analysis | Supports requirement itemization, requirement structuring, common requirement identification, requirement conflict detection, and requirement association analysis. | RT-002, RT-009 |
| Forward tracing | Supports establishing and viewing forward tracing information such as code, test cases, and trace personnel for requirements. | RT-002, RT-009 |

### User Classes

| User Class | Responsibilities / Needs | Source |
| --- | --- | --- |
| Project manager | Overall project owner who uses the tool to create requirements, modify requirements, and manage projects. | RT-004 |
| Project leader | Uses the tool to create and modify requirements and assists project requirements management. | RT-004 |
| Ordinary project member | Completes development and testing according to requirements and views related requirements and tracing information. | RT-004 |
| System administrator | Maintains normal ReTool operation, adds or deletes users, modifies user system roles, resets passwords, and collects suggestions. | RT-004, RT-007 |
| System user | Registers, logs in, and uses project and requirement functions according to project roles. | RT-007, RT-008, RT-009 |

### Operating Environment

| Environment | Requirement | Source |
| --- | --- | --- |
| Client hardware | Intel Core i7-6700HQ CPU, more than 100 MB available storage, complete network support, at least 8 GB memory, and Windows 10 64-bit operating system. | RT-010 |
| Client software | Google Chrome 81.0 or above. | RT-010 |
| Server hardware | Recommended EC2 t2.xlarge, 4 vCPU, 16 GB memory, and up to 5 Gbps network bandwidth. | RT-010 |
| Server operating system | Amazon Linux 2. | RT-010 |
| Service deployment | Gateway, user management service, project management service, and requirements management service run on a local computer, while the algorithm service runs on a server. | RT-005 |
| Network | When users cannot connect to the network, all requirements cannot be realized. | RT-005 |

### Assumptions and Dependencies

| ID | Assumption / Dependency | Evidence Type | Source |
| --- | --- | --- | --- |
| AD-001 | System functions depend on user network connection. | explicit | RT-005 |
| AD-002 | Requirement changes depend on the established requirement change process and specification review. | explicit | RT-005 |
| AD-003 | The algorithm service depends on a higher-performance server environment. | explicit | RT-005 |
| AD-004 | The system uses MongoDB as the database for create, read, update, and delete operations. | explicit | RT-001, RT-006 |
| AD-005 | Users can assume different roles and have different permissions in different projects. | explicit | RT-004 |

## 3. External Interface Requirements

### User Interfaces

| Interface | Requirement | Source |
| --- | --- | --- |
| User authentication interface | Supports registration, login, logout, password modification, and viewing personal information. | RT-007 |
| User management interface | Supports system administrators viewing user lists, adding users, deleting users, resetting passwords, and modifying user roles. | RT-007 |
| Project list interface | Supports viewing participating projects, creating projects, deleting projects, and viewing/modifying project information. | RT-008 |
| Member management interface | Supports viewing, adding, and deleting project members and modifying project roles. | RT-008 |
| Baseline management interface | Supports creating and viewing project baseline nodes. | RT-008 |
| Requirements management interface | Supports requirement item tree, requirement item creation, import, modification, deletion, movement, content viewing, and trace viewing. | RT-009 |
| Requirement analysis interface | Supports selecting requirement analysis scope and executing structuring, common requirement identification, conflict detection, and association analysis. | RT-009 |

### Software/API Interfaces

| Interface | Requirement | Source |
| --- | --- | --- |
| Front-end framework | The client uses Vue.js to develop the Web user interface. | RT-002 |
| Server architecture | The server uses a microservice architecture; the terminology states that Flask is suitable for writing server-side code under a microservice architecture. | RT-001, RT-002 |
| Algorithm service | The system uses NLP, PyTorch, Word2vec, and related algorithm capabilities to support requirement analysis. | RT-001, RT-002, RT-009 |
| Database | The MongoDB database accepts processing logic instructions, performs create, read, update, and delete operations, and returns data or execution results. | RT-001, RT-006 |

### Communication Interfaces

The source document only explicitly states that services communicate through the network, the login system depends on Web interfaces, all requirements cannot be realized without network access, and network transmission and open Web interfaces must be secure. The source document does not specify REST, RPC, WebSocket, message queues, or concrete authentication protocols. (Source: RT-001, RT-005, RT-013)

### Data Exchange Formats

The system needs to process data such as username, password, user role, project name, project description, project state, project members, project roles, baseline name and description, Word documents, requirement item name and description, state, priority, expected start/end time, structured results, common requirements, conflict information, association relationships, trace code, trace test cases, and trace personnel. The source document does not specify JSON, form fields, file upload protocols, or MongoDB collection schemas. (Source: RT-007, RT-008, RT-009)

## 4. Functional Requirements

| ID | Requirement | Trigger / Input | System Behavior | Output | Priority | Verification | Source |
| --- | --- | --- | --- | --- | --- | --- | --- |
| FR-001 | The system shall support user registration. | A system user accesses the main interface, enters the registration interface, fills in username and password, and clicks register. | The system validates registration information, saves username and password after successful registration, and prompts an error and returns to the registration interface when the username is duplicated or the password does not meet requirements. | New user record, login interface redirect, or error prompt. | High | Test | RT-007 |
| FR-002 | The system shall support user login. | A registered user or administrator enters username and password. | The system confirms that the username exists and password is correct, then prompts successful login; when the username does not exist or password is wrong, it prompts login failure. | Login state or error prompt. | High | Test | RT-007 |
| FR-003 | The system shall support user logout. | A logged-in user clicks the logout button. | The system prompts successful logout and redirects to the main page, and the user loses all permissions in the system. | Unauthenticated state and main page. | High | Test | RT-007 |
| FR-004 | The system shall allow system administrators to delete users. | A system administrator selects user deletion in the user list interface. | The system deletes the selected user record and updates the user list. | User list after deletion. | High | Test | RT-007 |
| FR-005 | The system shall support modifying user passwords. | A logged-in user enters the personal information interface and submits a new password. | The system modifies the user password; if the password does not meet requirements, it prompts an error. | Password modification result or error prompt. | High | Test | RT-007 |
| FR-006 | The system shall allow system administrators to view the user list. | A system administrator enters the user management interface. | The system displays the system user list. | User list. | High | Test | RT-007 |
| FR-007 | The system shall support viewing user personal information. | A logged-in user enters the personal information interface. | The system displays the user's own personal information, such as phone and email. | Personal information page. | Medium | Demonstration | RT-007 |
| FR-008 | The system shall allow system administrators to reset user passwords. | A system administrator selects a user for password reset in the user management interface. | The system resets that user's password to the initial default password. | Password reset result. | High | Test | RT-007 |
| FR-009 | The system shall allow system administrators to modify user roles. | A system administrator selects a user in the user list and changes the user to administrator role. | The system changes the user's role and permissions. | Updated user role. | High | Test | RT-007 |
| FR-010 | The system shall allow system administrators to add users. | A system administrator enters the add-user interface, enters username and password, and selects a system role type. | The system saves the new user's username, password, and role, and returns to the user management interface. | New user record and user management interface. | High | Test | RT-007 |
| FR-011 | The system shall support project creation. | A user clicks create project in the project list interface, fills in project name, project description, project state, adds project members, and sets project roles. | The system creates the project and saves project members and project roles. | New project appears in the project list. | High | Test | RT-008 |
| FR-012 | The system shall allow project managers to delete projects. | A project manager clicks delete project in the project list and confirms. | The system deletes the corresponding project. | Project disappears from the project list. | High | Test | RT-008 |
| FR-013 | The system shall allow project managers to modify projects. | A project manager enters the project information interface from the project list. | The system allows the project manager to select project information or member management and modify corresponding information. | Updated project or member information. | High | Test | RT-008 |
| FR-014 | The system shall support viewing projects. | A user clicks the project information button for a project in the project list. | The system displays concrete project information and the project member management entry. | Project information or member information. | Medium | Test | RT-008 |
| FR-015 | The system shall support viewing the project list. | A user successfully logs in and clicks the project list in project management. | The system displays all projects in which the current user participates. | Project list. | High | Test | RT-008 |
| FR-016 | The system shall support creating project baseline nodes. | A project manager enters baseline management from the project information interface and fills in version name and version description. | The system creates a baseline node and archives current project requirement items; after baseline node creation, requirement items inside the node cannot continue to be changed. | Baseline node and baseline list. | High | Test | RT-008 |
| FR-017 | The system shall support viewing project baseline nodes. | A user enters baseline management from the project information interface and selects a baseline node. | The system displays all baseline nodes under the current project and supports viewing concrete node information. | Baseline node list and node details. | Medium | Test | RT-008 |
| FR-018 | The system shall allow project managers to modify project information. | A project manager enters the project information interface and edits text boxes. | The system saves modifications to project name, description, state, and related project information. | Updated project information. | High | Test | RT-008 |
| FR-019 | The system shall allow project managers to modify project members. | A project manager enters the member management interface. | The system allows the project manager to modify existing project member information. | Updated project member information. | High | Test | RT-008 |
| FR-020 | The system shall support viewing project information. | A user enters the project information interface. | The system displays concrete information about the current project by default. | Project information details. | Medium | Demonstration | RT-008 |
| FR-021 | The system shall support viewing project members. | A user enters the project information interface and clicks member management. | The system switches to the project member interface for that project. | Project member list. | Medium | Test | RT-008 |
| FR-022 | The system shall allow project managers to add project members. | A project manager adds a new member and sets a project role in the member management interface. | The system saves the new project member and corresponding role. | Updated project member list. | High | Test | RT-008 |
| FR-023 | The system shall allow project managers to delete project members. | A project manager deletes an existing member in the member management interface. | The system deletes the project member relationship. | Updated project member list. | High | Test | RT-008 |
| FR-024 | The system shall allow project managers to modify project roles. | A project manager modifies a project member's role in the member management interface. | The system updates that member's role in the project. | Updated project role. | High | Test | RT-008 |
| FR-025 | The system shall support creating requirement items. | A project manager or project leader enters requirements management, selects the operation item and insertion position, and selects the creation method. | The system creates a requirement item or calls subflows such as single-item creation and Word import. | New requirement item displayed in requirements management. | High | Test | RT-009 |
| FR-026 | The system shall support creating a single requirement item. | A project manager or project leader selects a non-text-import method and fills in requirement name, description, state, priority, and expected start/end time. | The system saves the single requirement item and may prompt the user to perform requirement analysis. | New requirement item and its basic information. | High | Test | RT-009 |
| FR-027 | The system shall support importing requirement items from Word. | A project manager or project leader selects import from text and uploads a Word document. | The system uploads the document to the server, performs itemization and requirement analysis, and completes requirement item creation; if no document is uploaded or itemization fails, it prompts failure. | Imported requirement items or failure prompt. | High | Test | RT-009 |
| FR-028 | The system shall support requirement itemization. | A user imports a Word document and clicks start itemization. | The server performs itemization analysis on the document and returns results. | Itemized requirement items. | High | Test | RT-009 |
| FR-029 | The system shall support deleting requirement items. | A project manager or project leader selects a requirement item to delete and confirms. | The system deletes the requirement item; when the user selects the root requirement item, it prompts that this type of requirement item cannot be deleted. | Requirement item disappears from the item tree or error prompt. | High | Test | RT-009 |
| FR-030 | The system shall support modifying requirement items. | A project manager or project leader selects a requirement item to modify and enters the modification interface. | The system allows modifying requirement item content or moving requirement item position and saves the modification. | Modified content displayed in the requirement item tree. | High | Test | RT-009 |
| FR-031 | The system shall support modifying requirement item content. | A project manager or project leader selects the main information or basic information tab of a requirement item and edits it. | The system saves modifications to name, description, state, priority, and similar fields, and may prompt the user whether to perform requirement analysis. | Updated requirement item content. | High | Test | RT-009 |
| FR-032 | The system shall support moving requirement item positions. | A project manager or project leader enters the requirement item position adjustment interface and drags an item. | The system saves the new position of the requirement item in the requirement item tree. | Updated requirement item tree. | High | Test | RT-009 |
| FR-033 | The system shall support establishing requirement forward tracing. | A project manager or project leader selects a requirement item, enters the requirement tracing tab, and fills in trace code, trace test cases, and trace personnel. | The system saves requirement forward tracing information. | Forward tracing content in the requirement item. | High | Test | RT-009 |
| FR-034 | The system shall support entering requirement analysis. | A project manager or project leader clicks requirement analysis on the project main interface. | The system enters the requirement analysis tab and displays selectable concrete analysis functions. | Requirement analysis function selection interface. | High | Demonstration | RT-009 |
| FR-035 | The system shall support requirement structuring. | A user clicks requirement structuring in requirement analysis. | The system uses NLP tools and heuristic rules to analyze requirement items, extract finer-grained syntactic elements, and save structured results. | Requirement structuring result. | High | Test | RT-009 |
| FR-036 | The system shall support common requirement identification. | A user clicks common requirement identification in requirement analysis. | The system uses a trained Word2vec model to detect requirements with basically the same semantics; when common requirements exist, it displays numbers and content, otherwise it gives a prompt. | Common requirement list or no-common prompt. | High | Test | RT-009 |
| FR-037 | The system shall support requirement conflict detection. | A user clicks conflict detection in requirement analysis. | The system uses NLP tools and heuristic rules to detect conflicts in requirement items; when conflicts exist, it displays concrete content, otherwise it prompts that no conflict exists. | Conflict detection result. | High | Test | RT-009 |
| FR-038 | The system shall support requirement association analysis. | A user clicks association analysis in requirement analysis. | The system uses NLP tools and heuristic rules to detect association relationships among requirement items; when associations exist, it displays relationship type and requirement items at both ends, otherwise it prompts that no association exists. | Association analysis result. | High | Test | RT-009 |
| FR-039 | The system shall support viewing the requirement item tree. | A user clicks a project name and enters the project home page. | The system renders all requirement items in the project as a tree structure according to requirement item hierarchy relationships. | Requirement item tree. | High | Test | RT-009 |
| FR-040 | The system shall support viewing requirement item content. | A user clicks a concrete requirement item. | The system displays concrete information such as the requirement item name and description. | Requirement item details. | Medium | Demonstration | RT-009 |
| FR-041 | The system shall support viewing requirement forward tracing. | A user clicks a requirement item and enters the requirement tracing tab. | The system displays forward tracing content such as trace code, trace tests, and trace personnel for the requirement item. | Forward tracing details. | Medium | Test | RT-009 |

## 5. Non-Functional Requirements

| ID | Quality | Requirement | Fit Criterion | Priority | Verification | Source |
| --- | --- | --- | --- | --- | --- | --- |
| NFR-001 | Performance | The time from user click to first interface display shall be controlled. | Time from click to first interface display does not exceed 1 second. | High | Test | RT-011 |
| NFR-002 | Reliability | The system mean time to failure shall satisfy the threshold. | Mean time to failure > 720 h. | High | Analysis | RT-012 |
| NFR-003 | Reliability | The system mean time to repair shall satisfy the threshold. | Mean time to repair < 30 min. | High | Analysis | RT-012 |
| NFR-004 | Reliability | The data loss rate after system failure shall conform to the source document threshold. | Data loss rate after failure < 99%; this threshold is preserved according to the original source wording and should be confirmed during review. | Medium | Analysis | RT-012 |
| NFR-005 | Reliability | The system shall have automatic release and fault removal capability after errors occur. | After fault injection, the system can automatically recover or enter a recoverable state. | High | Test | RT-012 |
| NFR-006 | Reliability | User-uploaded information shall be persisted quickly. | Time for saving uploaded user information to disk < 1 s. | High | Test | RT-012 |
| NFR-007 | Resource Usage | System memory usage shall be controlled during runtime. | Memory usage < 80%. | High | Test | RT-012 |
| NFR-008 | Resource Usage | System CPU usage shall be controlled during runtime. | CPU usage < 80%. | High | Test | RT-012 |
| NFR-009 | Reliability | The database shall be backed up periodically and support offsite disaster recovery. | The database is backed up periodically, with three-copy offsite disaster recovery backup. | High | Inspection | RT-012 |
| NFR-010 | Security | The login system shall comply with Web security specifications. | Login Web interfaces pass security specification checks. | High | Test | RT-013 |
| NFR-011 | Privacy | The system shall protect user privacy information and personalized information. | Privacy and personalized data are protected by access control and protection measures. | High | Inspection | RT-013 |
| NFR-012 | Security | The system shall identify illegal user inputs and malicious behavior. | Illegal inputs and malicious behavior are identified and recorded. | High | Test | RT-013 |
| NFR-013 | Security | The system shall prevent requirement input from causing database injection attacks. | Requirement input content is restricted and validated, and injection attacks are blocked. | High | Test | RT-013 |
| NFR-014 | Security | Front-end code shall reduce the risk that captured request packets lead to requirement information copying or tampering. | Front-end code uses protection strategies such as minimization and mixing/obfuscation. | Medium | Inspection | RT-013 |
| NFR-015 | Security | The system shall ensure functional module security. | Network transmission, data storage, file storage, and open Web interfaces have security measures. | High | Inspection | RT-013 |
| NFR-016 | Security | The system shall establish permissions for developers and sensitive commands. | Developer and sensitive command permissions can be checked. | High | Inspection | RT-013 |
| NFR-017 | Maintainability | Software structure and documents shall support performance adjustment. | The system has good structure and complete documents, and performance adjustment points can be identified. | Medium | Inspection | RT-014 |
| NFR-018 | Maintainability | Documents shall be clear, readable, and uniformly written. | Documents pass standardization and readability checks. | Medium | Inspection | RT-014 |
| NFR-019 | Maintainability | Server deployment and logs shall support issue tracing. | Deployment process is concise and standardized, and logs are persistently saved, readable, and traceable. | High | Test | RT-014 |
| NFR-020 | Maintainability | The product shall reserve upgrade interfaces and upgrade space. | Design descriptions reflect upgrade interfaces and extension space. | Medium | Inspection | RT-014 |
| NFR-021 | Usability | Interaction design shall reduce user thinking and operation costs. | Users can obtain target information in three clicks or fewer, and important information is presented on the main interface or in obvious locations. | Medium | Demonstration | RT-015 |
| NFR-022 | Usability | The system shall reduce user input and support personalized experience. | Selection lists and search input autocomplete are used, personalized information is recorded, and direct login is supported on revisits. | Medium | Demonstration | RT-015 |
| NFR-023 | UI Design | Interface design shall be unified, adaptive, and compliant with Web design specifications. | Flat style is unified, screen size is adaptive, visual effect is harmonious, icons are concise and intuitive, and colors and text satisfy the source document requirements. | Medium | Inspection | RT-016 |

## 6. Data Requirements

| ID | Data Object | Requirement | Rationale / Constraint | Verification | Source |
| --- | --- | --- | --- | --- | --- |
| DR-001 | User account | The system shall save user information such as username, password, phone, and email. | Supports registration, login, personal information viewing, and password modification. | Test | RT-007 |
| DR-002 | User roles and permissions | The system shall save system roles and permissions such as system user and system administrator. | Supports user role modification, administrator operations, and permission control. | Test | RT-004, RT-007 |
| DR-003 | Project | The system shall save project name, project description, and project state. | Supports project creation, modification, viewing, and deletion. | Test | RT-008 |
| DR-004 | Project member relationship | The system shall save member relationships for users participating in projects. | Supports viewing, adding, and deleting project members. | Test | RT-008 |
| DR-005 | Project role | The system shall save project roles held by users in different projects. | Supports different role permissions in different projects and project role modification. | Test | RT-004, RT-008 |
| DR-006 | Project baseline node | The system shall save baseline node name, description, and archived requirement items. | Supports creating and viewing project baseline nodes; after baseline creation, requirements inside the node cannot continue to be changed. | Test | RT-008 |
| DR-007 | Requirement item | The system shall save requirement item name, description, state, priority, and expected start/end time. | Supports creating, viewing, modifying, deleting, and moving requirement items. | Test | RT-009 |
| DR-008 | Word document | The system shall receive and upload Word documents to the server. | Supports importing requirement items from Word and requirement itemization. | Test | RT-009 |
| DR-009 | Requirement item tree | The system shall save hierarchy relationships and positions among requirement items. | Supports tree display and moving requirement item positions. | Test | RT-009 |
| DR-010 | Requirement structuring result | The system shall save syntactic elements extracted by NLP tools and heuristic rules. | Supports other requirement analysis algorithm services. | Test | RT-009 |
| DR-011 | Common requirement identification result | The system shall save or display numbers and content of requirements with basically the same semantics. | Supports common requirement identification. | Test | RT-009 |
| DR-012 | Conflict detection result | The system shall save or display concrete requirement conflict content. | Supports requirement conflict detection and later handling. | Test | RT-009 |
| DR-013 | Association analysis result | The system shall save or display association relationship type and requirement items at both ends. | Supports requirement association analysis. | Test | RT-009 |
| DR-014 | Forward tracing information | The system shall save trace code, trace test case, and trace personnel information. | Supports establishing and viewing requirement forward tracing. | Test | RT-009 |
| DR-015 | Log | The system shall persistently save readable logs. | Supports issue tracing and maintenance. | Inspection | RT-014 |
| DR-016 | Privacy and personalized information | The system shall protect user privacy information and personalized information. | Supports security and confidentiality requirements. | Inspection | RT-013 |

## 7. Constraints

| ID | Constraint | Evidence Type | Source |
| --- | --- | --- | --- |
| C-001 | Requirement changes must strictly follow the requirement change process, and the requirements specification must be reasonably modified and reviewed. | explicit | RT-005 |
| C-002 | The overall tool adopts a front-end/back-end separated mode. | explicit | RT-002, RT-005 |
| C-003 | The front end shall use a lightweight, community-supported, and maintainable framework; the product description explicitly states that the client uses Vue.js. | explicit | RT-002, RT-005 |
| C-004 | The server uses a microservice architecture. | explicit | RT-002 |
| C-005 | During runtime, the system needs to limit simultaneous access volume; when the peak is exceeded, some user processes are blocked until the current carrying capacity can handle new processes. | explicit | RT-005 |
| C-006 | Gateway, user management service, project management service, and requirements management service run on a local computer. | explicit | RT-005 |
| C-007 | The algorithm service runs on a server because of machine performance requirements. | explicit | RT-005 |
| C-008 | When users cannot connect to the network, all requirements cannot be realized. | explicit | RT-005 |
| C-009 | Client hardware shall satisfy Intel Core i7-6700HQ CPU, more than 100 MB available storage, complete network support, and at least 8 GB memory. | explicit | RT-010 |
| C-010 | The client operating system is Windows 10 64-bit. | explicit | RT-010 |
| C-011 | The client browser is Google Chrome 81.0 or above. | explicit | RT-010 |
| C-012 | Recommended server configuration is EC2 t2.xlarge, 4 vCPU, 16 GB memory, and up to 5 Gbps network bandwidth. | explicit | RT-010 |
| C-013 | The server operating system is Amazon Linux 2. | explicit | RT-010 |
| C-014 | The database is MongoDB, responsible for accepting processing logic instructions and performing create, read, update, and delete operations. | explicit | RT-001, RT-006 |

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

## 9. Traceability Matrix

| ID | Requirement | Type | Source | Evidence Type | Verification | Confidence |
| --- | --- | --- | --- | --- | --- | --- |
| FR-001 | User registration | Functional | RT-007 | explicit | Test | High |
| FR-002 | User login | Functional | RT-007 | explicit | Test | High |
| FR-003 | User logout | Functional | RT-007 | explicit | Test | High |
| FR-004 | Delete user | Functional | RT-007 | explicit | Test | High |
| FR-005 | Modify user password | Functional | RT-007 | explicit | Test | High |
| FR-006 | View user list | Functional | RT-007 | explicit | Test | High |
| FR-007 | View user personal information | Functional | RT-007 | explicit | Demonstration | High |
| FR-008 | Reset user password | Functional | RT-007 | explicit | Test | High |
| FR-009 | Modify user role | Functional | RT-007 | explicit | Test | High |
| FR-010 | Add user | Functional | RT-007 | explicit | Test | High |
| FR-011 | Create project | Functional | RT-008 | explicit | Test | High |
| FR-012 | Delete project | Functional | RT-008 | explicit | Test | High |
| FR-013 | Modify project | Functional | RT-008 | explicit | Test | High |
| FR-014 | View project | Functional | RT-008 | explicit | Test | High |
| FR-015 | View project list | Functional | RT-008 | explicit | Test | High |
| FR-016 | Create project baseline node | Functional | RT-008 | explicit | Test | High |
| FR-017 | View project baseline node | Functional | RT-008 | explicit | Test | High |
| FR-018 | Modify project information | Functional | RT-008 | explicit | Test | High |
| FR-019 | Modify project members | Functional | RT-008 | explicit | Test | High |
| FR-020 | View project information | Functional | RT-008 | explicit | Demonstration | High |
| FR-021 | View project members | Functional | RT-008 | explicit | Test | High |
| FR-022 | Add project members | Functional | RT-008 | explicit | Test | High |
| FR-023 | Delete project members | Functional | RT-008 | explicit | Test | High |
| FR-024 | Modify project role | Functional | RT-008 | explicit | Test | High |
| FR-025 | Create requirement item | Functional | RT-009 | explicit | Test | High |
| FR-026 | Create single requirement item | Functional | RT-009 | explicit | Test | High |
| FR-027 | Import requirement items from Word | Functional | RT-009 | explicit | Test | High |
| FR-028 | Requirement itemization | Functional | RT-009 | explicit | Test | High |
| FR-029 | Delete requirement item | Functional | RT-009 | explicit | Test | High |
| FR-030 | Modify requirement item | Functional | RT-009 | explicit | Test | High |
| FR-031 | Modify requirement item content | Functional | RT-009 | explicit | Test | High |
| FR-032 | Move requirement item position | Functional | RT-009 | explicit | Test | High |
| FR-033 | Establish requirement forward tracing | Functional | RT-009 | explicit | Test | High |
| FR-034 | Requirement analysis | Functional | RT-009 | explicit | Demonstration | High |
| FR-035 | Requirement structuring | Functional | RT-009 | explicit | Test | High |
| FR-036 | Common requirement identification | Functional | RT-009 | explicit | Test | High |
| FR-037 | Requirement conflict detection | Functional | RT-009 | explicit | Test | High |
| FR-038 | Requirement association analysis | Functional | RT-009 | explicit | Test | High |
| FR-039 | View requirement item tree | Functional | RT-009 | explicit | Test | High |
| FR-040 | View requirement item content | Functional | RT-009 | explicit | Demonstration | High |
| FR-041 | View requirement forward tracing | Functional | RT-009 | explicit | Test | High |
| NFR-001 | First-interface response time | Non-functional | RT-011 | explicit | Test | High |
| NFR-002 | Mean time to failure | Non-functional | RT-012 | explicit | Analysis | High |
| NFR-003 | Mean time to repair | Non-functional | RT-012 | explicit | Analysis | High |
| NFR-004 | Data loss rate after failure | Non-functional | RT-012 | explicit | Analysis | Medium |
| NFR-005 | Automatic fault recovery | Non-functional | RT-012 | explicit | Test | High |
| NFR-006 | Uploaded information persistence time | Non-functional | RT-012 | explicit | Test | High |
| NFR-007 | Memory usage | Non-functional | RT-012 | explicit | Test | High |
| NFR-008 | CPU usage | Non-functional | RT-012 | explicit | Test | High |
| NFR-009 | Database backup and disaster recovery | Non-functional | RT-012 | explicit | Inspection | High |
| NFR-010 | Login Web security | Non-functional | RT-013 | explicit | Test | High |
| NFR-011 | Privacy and personalized information protection | Non-functional | RT-013 | explicit | Inspection | High |
| NFR-012 | Illegal input and malicious behavior record | Non-functional | RT-013 | explicit | Test | High |
| NFR-013 | Database injection prevention | Non-functional | RT-013 | explicit | Test | High |
| NFR-014 | Front-end code protection | Non-functional | RT-013 | explicit | Inspection | High |
| NFR-015 | Functional module security | Non-functional | RT-013 | explicit | Inspection | High |
| NFR-016 | Internal permission security | Non-functional | RT-013 | explicit | Inspection | High |
| NFR-017 | Structure and document maintainability | Non-functional | RT-014 | explicit | Inspection | High |
| NFR-018 | Document standardization | Non-functional | RT-014 | explicit | Inspection | High |
| NFR-019 | Deployment and log traceability | Non-functional | RT-014 | explicit | Test | High |
| NFR-020 | Upgrade space | Non-functional | RT-014 | explicit | Inspection | High |
| NFR-021 | Interaction click cost | Non-functional | RT-015 | explicit | Demonstration | High |
| NFR-022 | Input reduction and personalization | Non-functional | RT-015 | explicit | Demonstration | High |
| NFR-023 | Interface design | Non-functional | RT-016 | explicit | Inspection | High |
| DR-001 | User account data | Data | RT-007 | explicit | Test | High |
| DR-002 | User roles and permissions | Data | RT-004, RT-007 | explicit | Test | High |
| DR-003 | Project data | Data | RT-008 | explicit | Test | High |
| DR-004 | Project member relationship | Data | RT-008 | explicit | Test | High |
| DR-005 | Project role | Data | RT-004, RT-008 | explicit | Test | High |
| DR-006 | Project baseline node | Data | RT-008 | explicit | Test | High |
| DR-007 | Requirement item | Data | RT-009 | explicit | Test | High |
| DR-008 | Word document | Data | RT-009 | explicit | Test | High |
| DR-009 | Requirement item tree | Data | RT-009 | explicit | Test | High |
| DR-010 | Requirement structuring result | Data | RT-009 | explicit | Test | High |
| DR-011 | Common requirement identification result | Data | RT-009 | explicit | Test | High |
| DR-012 | Conflict detection result | Data | RT-009 | explicit | Test | High |
| DR-013 | Association analysis result | Data | RT-009 | explicit | Test | High |
| DR-014 | Forward tracing information | Data | RT-009 | explicit | Test | High |
| DR-015 | Log | Data | RT-014 | explicit | Inspection | High |
| DR-016 | Privacy and personalized information | Data | RT-013 | explicit | Inspection | High |
| C-001 | Requirement change process | Constraint | RT-005 | explicit | Inspection | High |
| C-002 | Front-end/back-end separation | Constraint | RT-002, RT-005 | explicit | Inspection | High |
| C-003 | Vue.js front-end framework | Constraint | RT-002, RT-005 | explicit | Inspection | High |
| C-004 | Microservice architecture | Constraint | RT-002 | explicit | Inspection | High |
| C-005 | Simultaneous access limit | Constraint | RT-005 | explicit | Test | High |
| C-006 | Local core service deployment | Constraint | RT-005 | explicit | Inspection | High |
| C-007 | Algorithm service server deployment | Constraint | RT-005 | explicit | Inspection | High |
| C-008 | Network dependency | Constraint | RT-005 | explicit | Test | High |
| C-009 | Client hardware | Constraint | RT-010 | explicit | Inspection | High |
| C-010 | Client operating system | Constraint | RT-010 | explicit | Inspection | High |
| C-011 | Chrome browser version | Constraint | RT-010 | explicit | Inspection | High |
| C-012 | Server hardware | Constraint | RT-010 | explicit | Inspection | High |
| C-013 | Amazon Linux 2 | Constraint | RT-010 | explicit | Inspection | High |
| C-014 | MongoDB database | Constraint | RT-001, RT-006 | explicit | Inspection | High |
