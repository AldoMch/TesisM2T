# Model Evolution Version Management Visualization Tool Software Requirements Specification (Standard SRS Extract)

## 1. Introduction

### Purpose

This document extracts verifiable requirements from `Software Requirements Analysis v3.0.docx` and rewrites them according to the compact SRS standard in `architectural_views_rep-pkg/script/templates/SRS.md`. The goal is to provide structured input for architecture generation, test design, and requirements tracing for the Model Evolution Version Management Visualization Tool. Source evidence is recorded in `modelevolution_docx_evidence_pack.json`. (Source: MDE-001, MDE-027)

### Product Scope

The Model Evolution Version Management Visualization Tool targets learners, contributors, and administrators of machine learning models. It visually displays model architecture, performance, and evolution relationships, and supports account management, model search and viewing, model upload and modification, model evolution relationship definition, and user management. The system especially targets models with multiple evolutionary versions, such as YOLO models, helping users understand model structures, source code, and evolution relationships. (Source: MDE-003, MDE-004, MDE-005)

### Intended Audience

This document is intended for developers, testers, system users, and later architecture generation/review workflows. The source document explicitly uses the requirements document as the basis for design, implementation, and testing phases, and provides users with operation and permission baselines. (Source: MDE-001)

### References

The source document cites the following materials. (Source: MDE-002)

| Ref | Source |
| --- | --- |
| REF-001 | Wang Q, Yuan J, Chen S, et al. Visual Genealogy of Deep Neural Networks |
| REF-002 | GB/T 9385-2008 Computer Software Requirements Specification |
| REF-003 | GB/T 8567-2006 Computer Software Documentation Specification |
| REF-004 | React official documentation |
| REF-005 | Django official documentation |
| REF-006 | DNN_Genealogy |

## 2. Overall Description

### Product Perspective

The system adopts a B/S architecture, and users access a specific website through a browser. The system consists of three major modules: front end, back end, and algorithm support. The databases are Neo4j and MySQL. External interfaces include Python libraries, browser Console, and multiple communication protocols. The source document does not expand concrete API paths, database table DDL, service deployment topology, or third-party identity service details. (Source: MDE-008, MDE-009, MDE-017)

### Product Functions Summary

| Capability | Summary | Source |
| --- | --- | --- |
| Account management | Registration, login, logout, password modification, and permission-change application. | MDE-010 |
| Model search and viewing | Search models, view models, view model basic information, view model evolution graphs, and view model evolution details. | MDE-011 |
| Model upload and modification | Contributors upload ONNX, upload and online edit PyTorch code, modify model profiles, and delete models. | MDE-012 |
| Evolution relationship definition | Add, delete, and modify model evolution relationships, and modify computational-layer reuse relationships inside a version. | MDE-013, MDE-014 |
| User management | Manage users, delete users, and review user permission changes. | MDE-015 |

### User Classes

| User Class | Responsibilities / Permissions | Source |
| --- | --- | --- |
| Learner | Browses and searches stored machine learning models in the system and understands model evolution relationships and evolution methods, without modification permission. | MDE-005 |
| Model contributor | Has learner permissions and can add, delete, and modify machine learning models they uploaded, and adjust model evolution relationships and evolution methods. | MDE-005 |
| Administrator | Has contributor permissions and can manage users, delete users, and adjust user permissions. | MDE-005, MDE-015 |

### Operating Environment

| Environment | Requirement | Source |
| --- | --- | --- |
| CPU | x86-64 or ARM architecture. | MDE-007 |
| Memory | At least 4 GB. | MDE-007 |
| Disk | At least 20 GB of available space. | MDE-007 |
| Bandwidth | At least 5 Mbps. | MDE-007 |
| Operating System | Windows 10 or above 64-bit, or Ubuntu 16.04 or above 64-bit; design constraints also require running on Windows, macOS, Linux, and similar systems. | MDE-007, MDE-017 |
| Browser | Mainstream browsers such as Firefox, Chrome, and 360 Browser. | MDE-007, MDE-009 |

### Assumptions and Dependencies

| ID | Assumption / Dependency | Evidence Type | Source |
| --- | --- | --- | --- |
| AD-001 | Requirement changes must follow the specified process and keep the requirements specification consistent. | explicit | MDE-008 |
| AD-002 | The project development process follows the experiment plan. | explicit | MDE-008 |
| AD-003 | The system depends on collaboration among the front-end, back-end, and algorithm-support modules. | explicit | MDE-008 |
| AD-004 | The system depends on Neo4j and MySQL to store model evolution relationships, model data, and user data. | explicit | MDE-017 |
| AD-005 | RUCM details in the source DOCX are mainly given as images, and the body text does not expand complete basic flows, alternative flows, or field constraints. | inferred | MDE-010, MDE-011, MDE-012, MDE-014, MDE-015 |

## 3. External Interface Requirements

### User Interfaces

| UI Area | Requirement Summary | Source |
| --- | --- | --- |
| Browser access entry | All users access a specific website through a browser to use the software. | MDE-009 |
| Account management interface | Supports registration, login, logout, password modification, and permission-change application. | MDE-010 |
| Model search and viewing interface | Supports model search, model viewing, textual viewing of model basic attributes, topology-based viewing of evolution relationships, and evolution details. | MDE-011 |
| Model contribution and editing interface | Supports ONNX upload, PyTorch source upload and online editing, model profile modification, and model deletion. | MDE-012 |
| Evolution relationship editing interface | Supports editing model version relationships and computational-layer reuse relationships in internal version structures. | MDE-013, MDE-014 |
| User management interface | Administrators can manage users, delete users, and review permission changes. | MDE-015 |
| Navigation interface | The website shall have no more than 10 navigation interfaces; the main interface is prominent, side and bottom columns are clear, and long pages provide bottom navigation. | MDE-026 |

### Software/API Interfaces

| Interface | Requirement Summary | Source |
| --- | --- | --- |
| Python library interface | The system software interfaces include Python libraries. | MDE-009 |
| Browser Console | The system software interfaces include the browser Console. | MDE-009 |
| Neo4j database | Used as one database storage option and suitable for supporting model evolution relationship graphs. | MDE-017 |
| MySQL database | Used as one database storage option and suitable for supporting users, model attributes, or relational data. | MDE-017 |
| Front-end/back-end/algorithm module interfaces | The source document states that the system includes front-end, back-end, and algorithm-support modules, but does not provide concrete API contracts. | MDE-008 |

### Communication Interfaces

The system communication interfaces include HTTP, HTTPS, TCP, IP, FTP, SMTP, and UDP. The source document does not explain the concrete business use, ports, message formats, or authentication methods corresponding to each protocol. (Source: MDE-009)

### Data Exchange Formats

| Data Group | Fields / Content | Source |
| --- | --- | --- |
| Users and permissions | Learner, contributor, and administrator roles, as well as permission-change applications, permission review, and user management data. | MDE-005, MDE-010, MDE-015 |
| Machine learning model | Can be represented by an ONNX file or PyTorch source code; the model consists of multiple connected operators. | MDE-006, MDE-012 |
| Model basic information | Textual model attribute information; the source document does not expand the field list. | MDE-011 |
| Model performance metrics | Evaluation metrics such as execution time and prediction accuracy. | MDE-013 |
| Dataset | Dataset name and type. | MDE-013 |
| Trained model | Dataset used for training, model code, model label, and source untrained model. | MDE-013 |
| Evolution relationship | Reference or iterative relationship between two models, and the dataset used to generate the new model. | MDE-006, MDE-014 |
| Evolution method/details | Added or deleted operators/layers, adjusted operator parameters, modified connection modes, and computational-layer reuse relationships inside a version structure. | MDE-006, MDE-014 |

## 4. Functional Requirements

| ID | Description | Trigger / Input | System Behavior | Output | Priority | Verification | Source Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| FR-001 | The system shall support user registration for new accounts. | An unregistered user enters the account management process and submits registration information. | The system creates a new user account; concrete fields and validation flow are not expanded in the body text. | New user account. | High | Test | MDE-004, MDE-010 |
| FR-002 | The system shall support user login to existing accounts. | A user submits login credentials. | The system completes login verification through two-factor authentication and OAuth 2.0 or a similar security protocol. | Login session or failure prompt. | High | Test | MDE-010, MDE-018 |
| FR-003 | The system shall support user logout from account sessions. | A logged-in user initiates logout. | The system ends the current user session. | Logged-out state. | Medium | Test | MDE-010 |
| FR-004 | The system shall support user password modification. | A logged-in user or a user meeting account recovery conditions initiates password modification. | The system executes the password modification flow; concrete validation fields are not expanded in the body text. | Updated account password state. | Medium | Test | MDE-010 |
| FR-005 | The system shall support user submission of permission-change applications. | A user needs to elevate or adjust permissions. | The system records the permission-change application for administrator review. | Pending permission application. | Medium | Test | MDE-010, MDE-015 |
| FR-006 | The system shall support users searching for specific models. | A user enters model search conditions. | The system retrieves stored machine learning models. | Model search result list. | High | Test | MDE-011, MDE-021 |
| FR-007 | The system shall support users viewing models. | A user selects a model from search results or a model list. | The system displays viewable content of the selected model. | Model viewing page. | High | Demonstration | MDE-011 |
| FR-008 | The system shall display model basic attribute information in text form. | A user chooses to view model information. | The system reads and displays model basic attributes. | Model basic attribute text. | High | Demonstration | MDE-011 |
| FR-009 | The system shall display evolution relationships among multiple models in topology graph form. | A user chooses to view the model evolution graph. | The system generates a topology display according to model evolution relationships. | Model evolution topology graph. | High | Demonstration | MDE-011 |
| FR-010 | The system shall display concrete evolution relationships between two models in topology graph form. | A user chooses to view model evolution details. | The system displays structural changes between two models, such as module deletion and reuse. | Model evolution detail topology graph. | High | Demonstration | MDE-011, MDE-006 |
| FR-011 | The system shall allow model contributors to upload ONNX files. | A contributor initiates ONNX upload. | The system receives and saves the ONNX model file. | Uploaded model record. | High | Test | MDE-012 |
| FR-012 | The system shall allow model contributors to upload PyTorch source code. | A contributor initiates PyTorch source upload. | The system receives and saves the PyTorch source code. | Uploaded source record. | High | Test | MDE-012 |
| FR-013 | The system shall support online editing of PyTorch source code. | A contributor selects editable PyTorch source code. | The system provides online editing capability and saves editing results. | Updated PyTorch source code. | Medium | Test | MDE-012 |
| FR-014 | The system shall allow model contributors to modify model profiles. | A contributor selects a modifiable model and submits profile changes. | The system updates model profile information. | Updated model profile. | Medium | Test | MDE-012 |
| FR-015 | The system shall support model deletion. | An authorized user initiates model deletion. | The system deletes the model according to permission constraints; non-administrator accounts must not delete any approved model. | Deletion result or rejection prompt. | High | Test | MDE-012, MDE-022 |
| FR-016 | The system shall support adding model evolution relationships. | A contributor specifies an old model, dataset, and generated new model. | The system records the evolution relationship between models and associates the dataset used. | New evolution relationship record and visualized relationship. | High | Test | MDE-013, MDE-014 |
| FR-017 | The system shall support deleting model evolution relationships. | A contributor or authorized user selects an existing evolution relationship. | The system deletes the evolution relationship and shall comply with permission and data-protection constraints. | Evolution relationship set after deletion. | Medium | Test | MDE-014, MDE-022 |
| FR-018 | The system shall support modifying model evolution details. | A contributor selects an evolution relationship or an internal version structure reuse relationship. | The system modifies the evolution relationship between whole versions or modifies the reuse relationship of certain computational layers in the internal version structure. | Updated evolution details and topology display. | High | Test | MDE-014 |
| FR-019 | The system shall support recording base datasets and trained model information. | A contributor defines model evolution details or trains a new model. | The system maintains dataset information and trained model information in the back-end database. | Dataset records, trained model records, and corresponding visualization logic. | High | Inspection | MDE-013 |
| FR-020 | The system shall allow administrators to manage users. | An administrator enters user management. | The system allows the administrator to manage user information and permissions. | Updated user state or permissions. | High | Test | MDE-015 |
| FR-021 | The system shall allow administrators to delete users. | An administrator selects a user to delete. | The system deletes the specified user or rejects an illegal deletion request. | User deletion result. | Medium | Test | MDE-015 |
| FR-022 | The system shall allow administrators to review user permission changes. | An administrator receives a permission-change application. | The system allows the administrator to review and adjust user permissions. | Permission review result. | High | Test | MDE-015 |

## 5. Non-Functional Requirements

| ID | Quality | Requirement | Fit Criterion | Priority | Verification | Source Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| NFR-001 | Concurrency | The system shall support concurrent online requests. | It can withstand simultaneous online requests from 50 users. | High | Test | MDE-016 |
| NFR-002 | Throughput | The system shall meet throughput requirements for model modification and query requests. | 10 model modification requests per second and 50 query requests per second. | High | Test | MDE-016 |
| NFR-003 | Response Time | Static pages shall respond quickly. | Static page response time does not exceed 1 second. | High | Test | MDE-016 |
| NFR-004 | Processing Time | Adding a model to producing results shall be completed within the specified time. | Time from adding a model to producing results does not exceed 1 minute. | High | Test | MDE-016 |
| NFR-005 | Reliability / Availability | The Web site shall run continuously without interruption. | Runs 7*24 hours, and unplanned downtime per year is no more than 30 hours. | High | Analysis | MDE-020 |
| NFR-006 | Failover | The system shall quickly switch to a standby machine on failure. | Switches to a standby machine within 0.5 hours after failure. | High | Analysis | MDE-020 |
| NFR-007 | Maintainability / Reliability | The system shall satisfy repairability and fault-free operation requirements. | Mean time to repair does not exceed 0.5 hours, and mean time between failures is no less than 4000 hours. | High | Analysis | MDE-020 |
| NFR-008 | Consistency | When multiple administrators modify models simultaneously, the system shall keep final displayed content consistent. | No content conflict, confusion, or loss occurs. | High | Test | MDE-020 |
| NFR-009 | Correctness | The system shall correctly display model structures and evolution relationships and return correct search results. | No exception occurs during user use; model structures and evolution relationships are displayed correctly; search returns correct results. | High | Test | MDE-021 |
| NFR-010 | Authentication Security | User login shall use two-factor authentication. | OAuth 2.0 or a similar security protocol is used. | High | Inspection | MDE-018 |
| NFR-011 | Data Encryption | Sensitive data shall be encrypted during transmission and storage. | TLS encryption is used and PCI DSS is satisfied. | High | Inspection | MDE-018 |
| NFR-012 | Model Encryption | Models in the database shall be stored encrypted. | Symmetric encryption algorithms such as AES and DES are used. | High | Inspection | MDE-018 |
| NFR-013 | Access Control | Before login, the system shall reject all actions that modify website content. | Before successful account login, users cannot upload/modify models or define evolution details. | High | Test | MDE-022 |
| NFR-014 | Privilege Control | Non-administrator accounts shall not delete or modify any approved model. | Deletion/modification requests from non-administrators for approved models return rejection results. | High | Test | MDE-022 |
| NFR-015 | Spoofing Protection | The system shall detect or block forged login data. | When accessed by an impersonated user, the system detects or blocks forged login data. | High | Test | MDE-022 |
| NFR-016 | Tamper Protection | The system shall protect uploaded models and evolution details from arbitrary tampering or deletion. | Unauthorized tampering or deletion operations are rejected and do not affect data integrity. | High | Test | MDE-022 |
| NFR-017 | Privacy Compliance | The system shall follow local privacy regulations to protect personal data. | A privacy policy is provided and user consent is obtained. | High | Inspection | MDE-019 |
| NFR-018 | License Compliance | Third-party libraries, plugins, and tools shall comply with open-source licenses. | They do not infringe others' intellectual property rights. | Medium | Inspection | MDE-019 |
| NFR-019 | Maintainability | When a system fault occurs, it shall be possible to quickly locate and resolve the problem. | Fault location and resolution processes are executable; code is easy to understand, modify, and enhance. | Medium | Inspection | MDE-023 |
| NFR-020 | Code Consistency | Code in the same module shall be written in the same format. | Variable names are semantically related, structure and presentation are separated, HTML is used for structure, and CSS is used for layout and presentation. | Medium | Inspection | MDE-023 |
| NFR-021 | Portability / Responsive UI | The Web interface shall adapt to different operating systems, browsers, and electronic devices. | It adjusts according to operating system, screen size, screen orientation, and similar environments, and Web content is clearly displayed. | High | Test | MDE-024 |
| NFR-022 | Usability | Users shall clearly understand website functions and complete tasks according to prompts. | New users can complete tasks according to prompts; experienced users can complete tasks quickly and efficiently; detailed help documents are provided. | Medium | Demonstration | MDE-025 |
| NFR-023 | UI Aesthetics | System pages shall be coordinated, prominent, and easy to understand. | Navigation interfaces do not exceed 10; the main interface is prominent, side and bottom columns are clear, and long pages have bottom navigation. | Medium | Inspection | MDE-026 |

## 6. Data Requirements

| ID | Data Object | Requirement | Privacy / Integrity Notes | Verification | Source Evidence |
| --- | --- | --- | --- | --- | --- |
| DR-001 | Users and roles | The system shall maintain three user types and their permissions: learners, contributors, and administrators. | Permissions determine model modification, deletion, and user management capabilities. | Inspection | MDE-005, MDE-010, MDE-015 |
| DR-002 | Permission-change application | The system shall record user permission-change applications and administrator review results. | Permission changes must follow the specified process. | Test | MDE-008, MDE-010, MDE-015 |
| DR-003 | Machine learning model | The system shall save machine learning models composed of multiple connected operators. | Models in the database must be encrypted and must not be arbitrarily tampered with or deleted. | Inspection | MDE-006, MDE-012, MDE-018, MDE-022 |
| DR-004 | ONNX file | The system shall support contributors uploading and saving ONNX model files. | Uploaded files must be constrained by permissions and model protection. | Test | MDE-012, MDE-022 |
| DR-005 | PyTorch source code | The system shall support contributors uploading, online editing, and saving PyTorch source code. | Source changes must follow user permissions. | Test | MDE-012 |
| DR-006 | Model basic attributes | The system shall save and display model basic attribute information in text form. | The source DOCX body does not expand the field list. | Inspection | MDE-011 |
| DR-007 | Model performance metrics | The system shall record model evaluation metrics such as execution time and prediction accuracy. | Metrics are used for quantitative evaluation of trained models. | Analysis | MDE-013 |
| DR-008 | Dataset | The system shall save base dataset names and types. | Datasets are associated with model training and evolution relationships. | Inspection | MDE-013 |
| DR-009 | Trained model | The system shall save the dataset used for training, model code, model label, and source untrained model. | Trained models are used to visualize the internal logic of model evolution. | Inspection | MDE-013 |
| DR-010 | Evolution relationship | The system shall save reference or iterative relationships between two models and the dataset used to generate the new model. | Evolution relationships shall be addable, deletable, and editable. | Test | MDE-006, MDE-014 |
| DR-011 | Evolution method/details | The system shall record structural changes such as adding/deleting operators or layers, adjusting parameters, modifying connection modes, module deletion, module reuse, and computational-layer reuse. | Evolution details shall be visualized through topology graphs. | Test | MDE-006, MDE-011, MDE-014 |
| DR-012 | Database storage | The system shall use Neo4j and MySQL to store data and comply with the company's data security policy. | Database products are explicit technical constraints. | Inspection | MDE-017 |

## 7. Constraints

| ID | Constraint | Evidence Type | Source |
| --- | --- | --- | --- |
| C-001 | The system adopts a B/S architecture, and users access a specific website through a browser. | explicit | MDE-009 |
| C-002 | The hardware environment shall satisfy x86-64 or ARM CPU, at least 4 GB memory, at least 20 GB available disk, and at least 5 Mbps bandwidth. | explicit | MDE-007 |
| C-003 | The operating system environment shall support Windows 10 or above 64-bit or Ubuntu 16.04 or above 64-bit, and satisfy cross-platform constraints such as Windows, macOS, and Linux. | explicit | MDE-007, MDE-017 |
| C-004 | The runtime environment includes mainstream browsers such as Firefox, Chrome, and 360 Browser. | explicit | MDE-007 |
| C-005 | There are no hardware interfaces. | explicit | MDE-009 |
| C-006 | Software interfaces include Python libraries and browser Console. | explicit | MDE-009 |
| C-007 | Communication interfaces include HTTP, HTTPS, TCP, IP, FTP, SMTP, and UDP. | explicit | MDE-009 |
| C-008 | The databases are Neo4j and MySQL and must comply with the company's data security policy. | explicit | MDE-017 |
| C-009 | User login uses two-factor authentication with OAuth 2.0 or a similar security protocol. | explicit | MDE-018 |
| C-010 | Sensitive data transmission and storage use TLS encryption and comply with PCI DSS. | explicit | MDE-018 |
| C-011 | Models in the database are encrypted using symmetric encryption algorithms such as AES and DES. | explicit | MDE-018 |
| C-012 | The software must follow local privacy regulations, provide a privacy policy, and obtain user consent. | explicit | MDE-019 |
| C-013 | Third-party libraries, plugins, and tools must comply with related open-source licenses and must not infringe intellectual property rights. | explicit | MDE-019 |
| C-014 | Requirement changes shall follow the specified process and maintain specification consistency. | explicit | MDE-008 |

## 8. Verification and Acceptance

| ID | Verification Method | Acceptance Focus |
| --- | --- | --- |
| FR-001 | Test | An unregistered user can create a new account. |
| FR-002 | Test | A user obtains a login session after passing two-factor authentication. |
| FR-003 | Test | After logout, a logged-in user cannot continue operations using the original session. |
| FR-004 | Test | A user can complete the password modification flow. |
| FR-005 | Test | A permission-change application is recorded and can enter review. |
| FR-006 | Test | Search conditions return matching model results. |
| FR-007 | Demonstration | After selecting a model, the user can enter the model viewing page. |
| FR-008 | Demonstration | Model basic attributes are displayed in text form. |
| FR-009 | Demonstration | Multi-model evolution relationships are displayed as a topology graph. |
| FR-010 | Demonstration | Evolution details between two models are displayed as a topology graph and can reflect structural changes. |
| FR-011 | Test | A contributor can upload an ONNX file and form a model record. |
| FR-012 | Test | A contributor can upload PyTorch source code. |
| FR-013 | Test | A contributor can edit and save PyTorch source code online. |
| FR-014 | Test | A contributor can modify a model profile. |
| FR-015 | Test | Unauthorized users cannot delete approved models, and data state is correct after authorized users delete models. |
| FR-016 | Test | After a contributor specifies dataset and old/new models, the system adds an evolution relationship. |
| FR-017 | Test | A selected evolution relationship can be deleted by an authorized user. |
| FR-018 | Test | After version relationships or computational-layer reuse relationships are modified, the evolution detail display is updated. |
| FR-019 | Inspection | The back-end data model contains dataset and trained model records. |
| FR-020 | Test | Administrators can manage user states and permissions. |
| FR-021 | Test | Administrators can delete specified users. |
| FR-022 | Test | Administrators can review permission-change applications and produce review results. |
| NFR-001 | Test | The system can carry 50 users making online requests simultaneously. |
| NFR-002 | Test | The system satisfies 10 model modification requests per second and 50 query requests per second. |
| NFR-003 | Test | Static page response time does not exceed 1 second. |
| NFR-004 | Test | Adding a model to producing results does not exceed 1 minute. |
| NFR-005 | Analysis | Operation records prove 7*24 operation and annual unplanned downtime no greater than 30 hours. |
| NFR-006 | Analysis | The failover plan proves switching to a standby machine within 0.5 hours. |
| NFR-007 | Analysis | Maintenance records prove MTTR <= 0.5 hours and MTBF >= 4000 hours. |
| NFR-008 | Test | Concurrent modification by multiple administrators does not cause content conflict, confusion, or loss. |
| NFR-009 | Test | Model structures, evolution relationships, and search results are correct. |
| NFR-010 | Inspection | Login design or implementation includes two-factor authentication and OAuth 2.0 or a similar protocol. |
| NFR-011 | Inspection | Sensitive data transmission and storage use TLS and satisfy PCI DSS requirements. |
| NFR-012 | Inspection | Database model encryption uses AES, DES, or equivalent symmetric encryption. |
| NFR-013 | Test | Unauthenticated users cannot upload or modify models or define evolution details. |
| NFR-014 | Test | Non-administrators cannot delete or modify approved models. |
| NFR-015 | Test | Forged login data is detected or blocked. |
| NFR-016 | Test | Unauthorized tampering or deletion of models and evolution details is rejected. |
| NFR-017 | Inspection | A privacy policy exists and supports user consent records. |
| NFR-018 | Inspection | Third-party dependency licenses are checked and show no obvious infringement. |
| NFR-019 | Inspection | Fault location, comments, and maintainable code conventions exist. |
| NFR-020 | Inspection | Code format is consistent within the same module, and HTML/CSS responsibilities are separated. |
| NFR-021 | Test | Web content is clearly displayed under different operating systems, browsers, and devices. |
| NFR-022 | Demonstration | New users can complete tasks according to prompts, and help documents are accessible. |
| NFR-023 | Inspection | Navigation count, main interface, side/bottom columns, and long-page navigation satisfy requirements. |
| DR-001 | Inspection | User role and permission data structures cover learners, contributors, and administrators. |
| DR-002 | Test | Permission-change applications and review results can be saved and queried. |
| DR-003 | Inspection | Model data can be saved and is constrained by encryption and protection. |
| DR-004 | Test | After ONNX file upload, a model record can be formed. |
| DR-005 | Test | PyTorch source code can be uploaded, edited, and saved. |
| DR-006 | Inspection | Model basic attributes can be displayed; field list is supplemented later. |
| DR-007 | Analysis | Metrics such as execution time and prediction accuracy can be recorded or calculated. |
| DR-008 | Inspection | Dataset names and types can be saved. |
| DR-009 | Inspection | Trained model fields can be saved and associated with source models. |
| DR-010 | Test | Evolution relationships can be added, deleted, and queried. |
| DR-011 | Test | Evolution details can be recorded and displayed by topology graphs. |
| DR-012 | Inspection | Neo4j and MySQL storage configurations exist and satisfy security policy. |
| C-001 | Inspection | System design documents and access method reflect B/S architecture. |
| C-002 | Inspection | Deployment hardware satisfies CPU, memory, disk, and bandwidth requirements. |
| C-003 | Inspection | Target operating systems satisfy version and platform constraints. |
| C-004 | Test | Mainstream browsers can access the system. |
| C-005 | Inspection | The system does not depend on hardware interfaces. |
| C-006 | Inspection | Python library and browser Console interfaces are available. |
| C-007 | Inspection | Communication protocol support list is consistent with design. |
| C-008 | Inspection | Neo4j and MySQL are used and data security policy is satisfied. |
| C-009 | Inspection | Login uses two-factor authentication and OAuth 2.0 or a similar protocol. |
| C-010 | Inspection | TLS and PCI DSS related design or implementation evidence exists. |
| C-011 | Inspection | Model database encryption uses AES, DES, or equivalent algorithm. |
| C-012 | Inspection | Privacy policy and user consent mechanism exist. |
| C-013 | Inspection | Third-party dependency licenses are compliant. |
| C-014 | Inspection | Requirement change process and specification consistency maintenance mechanism exist. |

## 9. Traceability Matrix

| ID | Requirement | Type | Source | Evidence Type | Verification | Confidence |
| --- | --- | --- | --- | --- | --- | --- |
| FR-001 | Register new account | Functional | MDE-004, MDE-010 | explicit | Test | Medium |
| FR-002 | Login to existing account | Functional | MDE-010, MDE-018 | explicit | Test | High |
| FR-003 | Logout session | Functional | MDE-010 | explicit | Test | Medium |
| FR-004 | Modify password | Functional | MDE-010 | explicit | Test | Medium |
| FR-005 | Permission-change application | Functional | MDE-010, MDE-015 | explicit | Test | Medium |
| FR-006 | Search models | Functional | MDE-011, MDE-021 | explicit | Test | High |
| FR-007 | View model | Functional | MDE-011 | explicit | Demonstration | High |
| FR-008 | View model basic information | Functional | MDE-011 | explicit | Demonstration | High |
| FR-009 | View model evolution graph | Functional | MDE-011 | explicit | Demonstration | High |
| FR-010 | View model evolution details | Functional | MDE-011, MDE-006 | explicit | Demonstration | High |
| FR-011 | Upload ONNX file | Functional | MDE-012 | explicit | Test | High |
| FR-012 | Upload PyTorch source code | Functional | MDE-012 | explicit | Test | High |
| FR-013 | Online edit PyTorch source code | Functional | MDE-012 | explicit | Test | High |
| FR-014 | Modify model profile | Functional | MDE-012 | explicit | Test | High |
| FR-015 | Delete model | Functional | MDE-012, MDE-022 | explicit | Test | High |
| FR-016 | Add model evolution relationship | Functional | MDE-013, MDE-014 | explicit | Test | High |
| FR-017 | Delete model evolution relationship | Functional | MDE-014, MDE-022 | explicit | Test | High |
| FR-018 | Modify model evolution details | Functional | MDE-014 | explicit | Test | High |
| FR-019 | Record datasets and trained models | Functional | MDE-013 | explicit | Inspection | High |
| FR-020 | Manage users | Functional | MDE-015 | explicit | Test | Medium |
| FR-021 | Delete users | Functional | MDE-015 | explicit | Test | Medium |
| FR-022 | Review permission changes | Functional | MDE-015 | explicit | Test | Medium |
| NFR-001 | 50-user concurrency | Non-functional | MDE-016 | explicit | Test | High |
| NFR-002 | Modification/query throughput | Non-functional | MDE-016 | explicit | Test | High |
| NFR-003 | Static page <= 1 second | Non-functional | MDE-016 | explicit | Test | High |
| NFR-004 | Add model to result <= 1 minute | Non-functional | MDE-016 | explicit | Test | High |
| NFR-005 | 7*24 operation and annual downtime <= 30 hours | Non-functional | MDE-020 | explicit | Analysis | High |
| NFR-006 | Failover within 0.5 hours | Non-functional | MDE-020 | explicit | Analysis | High |
| NFR-007 | MTTR/MTBF | Non-functional | MDE-020 | explicit | Analysis | High |
| NFR-008 | Multi-administrator concurrency consistency | Non-functional | MDE-020 | explicit | Test | High |
| NFR-009 | Display and search correctness | Non-functional | MDE-021 | explicit | Test | High |
| NFR-010 | Two-factor authentication | Non-functional | MDE-018 | explicit | Inspection | High |
| NFR-011 | TLS and PCI DSS | Non-functional | MDE-018 | explicit | Inspection | High |
| NFR-012 | AES/DES model encryption | Non-functional | MDE-018 | explicit | Inspection | High |
| NFR-013 | Modification prohibited before login | Non-functional | MDE-022 | explicit | Test | High |
| NFR-014 | Non-administrators cannot modify/delete approved models | Non-functional | MDE-022 | explicit | Test | High |
| NFR-015 | Detect/block forged login | Non-functional | MDE-022 | explicit | Test | High |
| NFR-016 | Model and evolution detail tamper protection | Non-functional | MDE-022 | explicit | Test | High |
| NFR-017 | Privacy compliance | Non-functional | MDE-019 | explicit | Inspection | High |
| NFR-018 | Open-source license compliance | Non-functional | MDE-019 | explicit | Inspection | High |
| NFR-019 | Maintainability | Non-functional | MDE-023 | explicit | Inspection | High |
| NFR-020 | Code consistency and structure/presentation separation | Non-functional | MDE-023 | explicit | Inspection | High |
| NFR-021 | Portable and responsive interface | Non-functional | MDE-024 | explicit | Test | High |
| NFR-022 | Operability and help documents | Non-functional | MDE-025 | explicit | Demonstration | High |
| NFR-023 | UI aesthetics and navigation | Non-functional | MDE-026 | explicit | Inspection | High |
| DR-001 | Users and roles | Data | MDE-005, MDE-010, MDE-015 | explicit | Inspection | High |
| DR-002 | Permission-change application | Data | MDE-008, MDE-010, MDE-015 | explicit | Test | High |
| DR-003 | Machine learning model | Data | MDE-006, MDE-012, MDE-018, MDE-022 | explicit | Inspection | High |
| DR-004 | ONNX file | Data | MDE-012, MDE-022 | explicit | Test | High |
| DR-005 | PyTorch source code | Data | MDE-012 | explicit | Test | High |
| DR-006 | Model basic attributes | Data | MDE-011 | explicit | Inspection | Medium |
| DR-007 | Model performance metrics | Data | MDE-013 | explicit | Analysis | High |
| DR-008 | Dataset | Data | MDE-013 | explicit | Inspection | High |
| DR-009 | Trained model | Data | MDE-013 | explicit | Inspection | High |
| DR-010 | Evolution relationship | Data | MDE-006, MDE-014 | explicit | Test | High |
| DR-011 | Evolution method and details | Data | MDE-006, MDE-011, MDE-014 | explicit | Test | High |
| DR-012 | Neo4j/MySQL storage | Data | MDE-017 | explicit | Inspection | High |
| C-001 | B/S architecture | Constraint | MDE-009 | explicit | Inspection | High |
| C-002 | Hardware environment | Constraint | MDE-007 | explicit | Inspection | High |
| C-003 | Operating system environment | Constraint | MDE-007, MDE-017 | explicit | Inspection | High |
| C-004 | Mainstream browsers | Constraint | MDE-007 | explicit | Test | High |
| C-005 | No hardware interface | Constraint | MDE-009 | explicit | Inspection | High |
| C-006 | Python library and Console interfaces | Constraint | MDE-009 | explicit | Inspection | High |
| C-007 | Communication protocol list | Constraint | MDE-009 | explicit | Inspection | High |
| C-008 | Neo4j/MySQL and data security policy | Constraint | MDE-017 | explicit | Inspection | High |
| C-009 | OAuth 2.0 or similar security protocol | Constraint | MDE-018 | explicit | Inspection | High |
| C-010 | TLS and PCI DSS | Constraint | MDE-018 | explicit | Inspection | High |
| C-011 | AES/DES model encryption | Constraint | MDE-018 | explicit | Inspection | High |
| C-012 | Privacy regulations and user consent | Constraint | MDE-019 | explicit | Inspection | High |
| C-013 | Open-source licenses and intellectual property | Constraint | MDE-019 | explicit | Inspection | High |
| C-014 | Requirement change process | Constraint | MDE-008 | explicit | Inspection | High |
