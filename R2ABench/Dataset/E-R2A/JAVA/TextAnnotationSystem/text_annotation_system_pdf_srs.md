# Software Requirements Specification: Intelligent Text Annotation System (ITAS)

Evidence base: `TextAnnotationSystem_origin.pdf`  
Generated to match: `architectural_views_rep-pkg/script/templates/SRS.md`

## 1. Introduction

### Purpose

This SRS normalizes the PDF design document for the Intelligent Text Annotation System (ITAS) into a concise, evidence-backed requirements specification. The document is intended to support downstream architecture view generation, testing, and traceability analysis.

Source evidence: TAS-001, TAS-011

### Product Scope

ITAS is a web-based system for processing and analyzing large volumes of text data. It contains two connected subsystems:

- Text annotation subsystem: supports paragraph/entity annotation for scientific literature and provides annotation results to the mining subsystem.
- Intelligent mining subsystem: uses large language models and natural language processing techniques to identify and extract predefined information from unannotated text.

Source evidence: TAS-001

### Intended Audience

The intended audience includes ITAS developers, testers, system annotation administrators, data annotators, researchers, and the expert group referenced by the source design document.

Source evidence: TAS-001, TAS-002

### References

| Ref | Description | Source |
|---|---|---|
| REF-001 | `TextAnnotationSystem_origin.pdf`, source software design document | TAS-001 |
| REF-002 | GB/T 9385-2008, computer software requirements specification guidance | TAS-011 |
| REF-003 | GB/T 8567-2006, computer software documentation guidance | TAS-011 |

## 2. Overall Description

### Product Perspective

ITAS is described as a front-end/back-end separated web system that combines web application services, structured and object storage, caching, message queues, and machine-learning-based text processing. The annotation subsystem precedes the mining subsystem by producing annotated data that can be used for later extraction and model-related workflows.

Source evidence: TAS-001, TAS-003

### Product Functions Summary

| Area | Summary | Source |
|---|---|---|
| User and role support | Supports system annotation administrators, data annotators, and researchers, including flexible role management and task switching. | TAS-002 |
| Annotation management | Supports annotation projects, annotators, documents, tags, marks, tasks, results, and user information. | TAS-006 |
| Mining workflow | Supports document upload, automatic format conversion, model selection, and information extraction. | TAS-009 |
| Data management | Stores users, projects, documents, tags, tasks, annotation results, object-storage references, and document format references. | TAS-007, TAS-008 |
| User interfaces | Provides screens for login, profile management, mining, upload, results, project creation/management, and task execution. | TAS-010 |

### User Classes

| User class | Description | Major responsibilities | Source |
|---|---|---|---|
| System annotation administrator | Representative of a research institution, university, or enterprise that needs high-quality data support. | Define presets, upload documents, manage annotation projects, export annotation data, and participate in model training and validation. | TAS-002 |
| Data annotator | Professional annotator, domain researcher, or student performing concrete annotation tasks. | Execute assigned document annotation tasks using system guidance and presets. | TAS-002 |
| Researcher | Researcher, scientist, technical worker, or data analyst using the mining subsystem. | Extract and mine key information from literature with minimal manual intervention. | TAS-002 |

### Operating Environment

The source specifies a modern web environment with Vue-based front end, Spring-based back end, Nginx reverse proxy, MySQL, Minio, Redis, BERT/GPT model integration, RabbitMQ, Docker, and Tencent Cloud deployment.

Source evidence: TAS-003, TAS-005

### Assumptions and Dependencies

| ID | Statement | Evidence type | Source |
|---|---|---|---|
| AD-001 | Annotation outputs are expected to support later intelligent mining and extraction workflows. | explicit | TAS-001 |
| AD-002 | Third-party model/API availability, such as GPT API or ChatGPT-like interfaces, is required for the implemented mining model invocation approach. | explicit | TAS-003, TAS-009 |
| AD-003 | Object storage is required for text/unstructured documents, while relational storage keeps structured records and document indexes. | explicit | TAS-003, TAS-007 |
| AD-004 | RabbitMQ-backed asynchronous processing is used for tasks such as file conversion. | explicit | TAS-005 |

## 3. External Interface Requirements

### User Interfaces

| UI ID | Requirement | Source |
|---|---|---|
| UI-001 | The system shall provide registration and login interfaces. | TAS-010 |
| UI-002 | The system shall provide a personal information management interface. | TAS-010 |
| UI-003 | The system shall provide a mining main interface, mining file upload interface, and mining result display interface. | TAS-010 |
| UI-004 | The system shall provide annotation project creation, annotation project management, and annotation task execution interfaces. | TAS-010 |
| UI-005 | The front-end interface shall be implemented with Vue.js/Vue 3.0 and Ant Design/Ant-Design-Vue components as specified by the source. | TAS-003, TAS-005 |

### Software/API Interfaces

| API ID | Requirement | Source |
|---|---|---|
| API-001 | The annotation subsystem shall expose controller-level functions for annotator, file, label, login, paper, project, result export/return, tag, task, and user management. | TAS-006 |
| API-002 | The mining subsystem shall expose functions for document upload, model selection, and information extraction. | TAS-009 |
| API-003 | The system shall integrate with GPT API or a third-party ChatGPT-like interface for entity annotation or mining model invocation where specified. | TAS-003, TAS-009 |
| API-004 | The system shall interact with MySQL for structured records, Minio for object storage, and Redis for cache access. | TAS-003, TAS-005 |

### Communication Interfaces

| COM ID | Requirement | Source |
|---|---|---|
| COM-001 | The front end shall communicate asynchronously with the back end through Axios HTTP client calls. | TAS-003, TAS-005 |
| COM-002 | Nginx shall provide reverse proxy, request forwarding, and load balancing responsibilities. | TAS-003 |
| COM-003 | Spring Cloud shall support service discovery, configuration management, load balancing, and inter-service communication concerns. | TAS-003, TAS-005 |
| COM-004 | RabbitMQ shall support message-queue-based asynchronous processing for workflows such as file conversion. | TAS-003, TAS-005 |

### Data Exchange Formats

| DATA-IF ID | Requirement | Source |
|---|---|---|
| DIF-001 | The system shall handle uploaded documents and maintain references for PDF, HTML, and TXT representations where document conversion is performed. | TAS-008, TAS-009 |
| DIF-002 | The system shall exchange annotation entities including projects, documents, tags, tasks, labels, and annotation results through back-end data APIs. | TAS-006, TAS-008 |
| DIF-003 | The system shall store object-storage identifiers and bucket references for files whose content is not stored directly in the relational database. | TAS-007, TAS-008 |

## 4. Functional Requirements

| ID | Description | Trigger/Input | System Behavior | Output | Priority | Verification | Source Evidence |
|---|---|---|---|---|---|---|---|
| FR-001 | The system shall support three user classes: system annotation administrator, data annotator, and researcher. | A user account is created or used. | The system associates users with role-specific responsibilities and functions. | Role-specific access and task context. | Must | Demonstration | TAS-002 |
| FR-002 | The system shall support flexible role management and task switching for users who perform multiple research-stage responsibilities. | A user needs to operate under a different role or task context. | The system enables switching between role/task contexts without losing the relevant workflow context. | Active role/task context. | Should | Demonstration | TAS-002 |
| FR-003 | The system shall allow first-time users to register accounts. | A user submits registration information. | The system creates a user account record. | Registered user account. | Must | Test | TAS-006, TAS-010 |
| FR-004 | The system shall authenticate users and support login, logout, and personal information viewing. | A user submits credentials or requests account information. | The system validates access and returns the requested session/profile operation. | Authenticated session, logout result, or personal information view. | Must | Test | TAS-006, TAS-010 |
| FR-005 | The system shall allow administrators to define and create annotation presets for paragraph/entity annotation and extraction. | An administrator identifies that existing presets do not satisfy a research need. | The system records configurable rules/templates used to guide annotation and extraction. | New or updated preset. | Should | Demonstration | TAS-002, TAS-004 |
| FR-006 | The system shall support annotation project management. | An administrator creates, updates, lists, or queries annotation projects. | The system creates projects, updates projects, lists all projects, lists the user's projects, updates project introductions, and queries projects by ID. | Project record or project list. | Must | Test | TAS-006 |
| FR-007 | The system shall support annotation personnel management per project. | An administrator adds, deletes, or queries project annotators. | The system updates or returns the annotator set for the project. | Annotator membership result or annotator list. | Must | Test | TAS-006 |
| FR-008 | The system shall support annotation literature/document management. | A user uploads, deletes, views, or queries project literature. | The system stores document metadata and supports retrieval by project ID. | Uploaded document record, deleted status, document view, or query result. | Must | Test | TAS-006, TAS-008 |
| FR-009 | The system shall support file download. | A user requests a downloadable file. | The system retrieves the referenced file content or object-storage record. | Downloaded file. | Should | Test | TAS-006, TAS-008 |
| FR-010 | The system shall support tag management for annotation tasks and documents. | A user creates, edits, deletes, or queries labels/tags. | The system maintains tag records and supports queries by task ID and document ID. | Created/updated/deleted tag or tag query result. | Must | Test | TAS-006, TAS-008 |
| FR-011 | The system shall support annotation task assignment and task lookup. | An administrator assigns tasks or a user requests task lists/details. | The system assigns annotation tasks, returns all tasks, returns the current user's tasks, and queries tasks by ID. | Assigned task or task query result. | Must | Test | TAS-006 |
| FR-012 | The system shall allow users to mark annotation tasks as completed. | An annotator finishes an assigned task. | The system updates the task completion state. | Completed-task status. | Must | Test | TAS-006, TAS-008 |
| FR-013 | The system shall provide task-level data statistics for annotation management. | A user requests task statistics. | The system computes and returns task-related statistical information. | Task statistics result. | Should | Test | TAS-006 |
| FR-014 | The system shall support annotation mark management. | An annotator adds, views, modifies, or deletes an annotation mark. | The system creates, reads, updates, or deletes the mark record. | Annotation mark result. | Must | Test | TAS-006, TAS-008 |
| FR-015 | The system shall persist annotation results with content, remark, tag, location, offset, creator, and timestamp information. | An annotation mark/result is submitted. | The system stores the annotation result fields defined in the label/annotation-result table. | Persisted annotation result. | Must | Inspection | TAS-008 |
| FR-016 | The system shall support returning or exporting annotation results for downstream use. | An administrator or workflow requests annotation results. | The system returns the collected annotation result data. | Annotation result output. | Must | Demonstration | TAS-002, TAS-006 |
| FR-017 | The mining subsystem shall support document upload. | A researcher uploads a document for mining. | The system accepts the user-selected document for later processing. | Uploaded mining document record. | Must | Test | TAS-009 |
| FR-018 | The mining subsystem shall support automatic document format conversion. | A document is uploaded for mining or annotation processing. | The system converts the document into supported representations where required. | Converted document representation and related identifiers. | Must | Test | TAS-008, TAS-009 |
| FR-019 | The mining subsystem shall support model selection. | A researcher prepares to run data mining. | The system allows selection from built-in preset models, community-shared models, or third-party interfaces, with third-party API invocation specified as implemented. | Selected model or model invocation configuration. | Must | Demonstration | TAS-009 |
| FR-020 | The mining subsystem shall extract paragraph annotation information and key data according to user needs. | A document and model selection are ready. | The system runs the selected model workflow to extract paragraph-level information and key data. | Extraction result. | Must | Test | TAS-009 |
| FR-021 | The system shall support automated paragraph localization and entity recognition for text processing. | A text document is processed by the annotation/mining workflow. | The system uses paragraph-location and entity-recognition model capabilities to identify relevant paragraphs and entities. | Located paragraph and recognized entity information. | Must | Test | TAS-003, TAS-005 |
| FR-022 | The system shall support few-shot-learning-oriented extraction for data-scarce research scenarios. | The available annotated examples are scarce. | The mining model workflow uses few-shot learning support to improve information extraction from unannotated text. | Extraction results under scarce-data conditions. | Should | Analysis | TAS-001 |
| FR-023 | The system shall provide user interface pages for registration/login, profile management, mining, upload, result display, project creation, project management, and task execution. | A user navigates to a supported workflow. | The front end displays the corresponding workflow interface. | Rendered workflow page. | Must | Demonstration | TAS-010 |

## 5. Non-Functional Requirements

| ID | Quality | Requirement | Evidence Type | Priority | Verification | Source Evidence |
|---|---|---|---|---|---|---|
| NFR-001 | Accuracy/Consistency | The system shall use preset annotation rules/templates to improve the accuracy and consistency of paragraph/entity annotation and extraction. | explicit | Must | Analysis | TAS-001, TAS-004 |
| NFR-002 | Efficiency | The system shall support efficient processing and analysis of large text datasets; the source does not provide a numeric throughput target. | explicit | Must | Analysis | TAS-001, TAS-003 |
| NFR-003 | Responsiveness | The system shall use asynchronous front-end/back-end interaction and cache support to improve perceived response speed; the source does not provide a latency threshold. | explicit | Should | Test | TAS-003, TAS-005 |
| NFR-004 | Scalability/Extensibility | The system shall use service discovery, configuration management, load balancing, and microservice support to enable service extension and deployment scaling. | explicit | Should | Inspection | TAS-003, TAS-005 |
| NFR-005 | Security | The system shall support user authentication and authorization through the specified gateway/security stack. | explicit | Must | Test | TAS-005 |
| NFR-006 | Portability | The system shall use Docker containerization to preserve environment consistency and deployment portability. | explicit | Should | Inspection | TAS-003, TAS-005 |
| NFR-007 | Usability | The system shall provide rich, intuitive web user interfaces using the specified Vue and Ant Design technology choices. | explicit | Should | Demonstration | TAS-003, TAS-005, TAS-010 |
| NFR-008 | Maintainability | The system shall use the specified layered web architecture, ORM/data access tooling, and development workflow to support manageable development and testing. | explicit | Should | Inspection | TAS-003, TAS-005 |
| NFR-009 | Asynchronous Processing | The system shall process asynchronous tasks such as file conversion through RabbitMQ to reduce synchronous workflow delay. | explicit | Should | Test | TAS-005 |
| NFR-010 | Reliability/Deployment Stability | The system shall deploy on the specified cloud/runtime infrastructure to provide a stable operating environment; the source does not define availability targets. | explicit | Should | Inspection | TAS-005 |

## 6. Data Requirements

### Data Entities or Objects

| ID | Entity/Object | Required Data | Source |
|---|---|---|---|
| DR-001 | User | User ID, username, real name, password, roles, creation date, update date. | TAS-008 |
| DR-002 | Role identity | Administrator and annotator identities can vary according to project context. | TAS-007 |
| DR-003 | Annotation project | Project ID, name, introduction, status/assignment fields, attachment ID/name, creation/update/assignment/completion timing where defined. | TAS-007, TAS-008 |
| DR-004 | Document/object file | File ID, filename, object name, object-storage bucket, creation date, update date. | TAS-007, TAS-008 |
| DR-005 | Paper/document relation | Project ID, identifier, filename, PDF ID, HTML ID, TXT ID, status, creation date, update date. | TAS-008 |
| DR-006 | Annotator relation | Project ID and user ID relation between annotation projects and annotators. | TAS-007, TAS-008 |
| DR-007 | Tag | Tag ID, project ID, tag key, tag name, creation date, update date. | TAS-008 |
| DR-008 | Task | Task ID, project ID, user ID, paper ID, document identifiers, PDF/HTML/TXT IDs, completion flag, timestamps. | TAS-008 |
| DR-009 | Annotation result/label | Task ID, content, remark, tag ID, location, start offset, end offset, creator ID, creator name, timestamps. | TAS-008 |
| DR-010 | Model/preset concepts | Paragraph model, entity model, preset, paragraph preset, and entity preset definitions used by annotation/extraction workflows. | TAS-004 |

### Input/Output Data

| ID | Data flow | Requirement | Source |
|---|---|---|---|
| DIO-001 | Uploaded documents | The system shall accept documents for annotation and mining workflows and maintain metadata/index records. | TAS-006, TAS-009 |
| DIO-002 | Converted documents | The system shall maintain PDF, HTML, and TXT references when document format conversion is used. | TAS-008, TAS-009 |
| DIO-003 | Annotation outputs | The system shall produce annotation result data that can be returned and used by downstream mining/model workflows. | TAS-001, TAS-006, TAS-008 |
| DIO-004 | Mining outputs | The system shall produce extracted paragraph annotation information and key data. | TAS-009 |

### Storage, Privacy, Integrity, Retention, or Migration

| ID | Requirement | Evidence Type | Source |
|---|---|---|---|
| DSR-001 | Structured records shall be stored in MySQL. | explicit | TAS-003, TAS-005 |
| DSR-002 | Text and unstructured document content shall be stored through Minio/object storage, with relational records storing indexes. | explicit | TAS-003, TAS-007, TAS-008 |
| DSR-003 | Redis shall be used as a cache to improve access speed and system response. | explicit | TAS-003, TAS-005 |
| DSR-004 | The PDF source does not specify retention duration, deletion policy, encryption method, or migration requirements. | explicit missing information | TAS-001 |

## 7. Constraints

| ID | Constraint | Type | Source |
|---|---|---|---|
| C-001 | The front end shall use Vue.js/Vue 3.0 with vue-router, Pinia, Ant Design/Ant-Design-Vue, and Axios as specified. | Technology | TAS-003, TAS-005 |
| C-002 | The back end shall use Spring Boot/Spring Cloud microservice architecture where specified. | Technology | TAS-003, TAS-005 |
| C-003 | The gateway/security stack shall use Spring Gateway and Spring Security for authentication and authorization. | Technology/Security | TAS-005 |
| C-004 | Nginx shall act as reverse proxy for load balancing and request forwarding. | Deployment | TAS-003 |
| C-005 | Mybatis/Mybatis Plus shall be used for database access/ORM operations. | Technology | TAS-003, TAS-005 |
| C-006 | MySQL, Minio, and Redis shall be used for structured storage, object storage, and caching respectively. | Data platform | TAS-003, TAS-005 |
| C-007 | BERT shall be used for paragraph model capability and GPT/GPT API shall be used for entity model/interface capability as specified. | ML/model | TAS-003, TAS-005 |
| C-008 | RabbitMQ shall be used for asynchronous message queue processing such as file conversion. | Infrastructure | TAS-003, TAS-005 |
| C-009 | Docker shall be used for containerized deployment and environment consistency. | Deployment | TAS-003, TAS-005 |
| C-010 | Tencent Cloud is specified as the deployment/runtime environment and public access hosting platform. | Deployment | TAS-005 |
| C-011 | The source document references GB/T 9385-2008 and GB/T 8567-2006 as documentation standards. | Standard | TAS-011 |

## 8. Verification and Acceptance

Verification methods:

- Test: execute the function or quality check through system/API/UI tests.
- Demonstration: show the workflow in the running system or prototype.
- Inspection: review design, configuration, database schema, or code artifacts.
- Analysis: reason from evidence, logs, data samples, or model behavior where direct execution is not sufficient.

Acceptance criteria:

- Each functional requirement in Section 4 has a demonstrable or testable workflow.
- Each non-functional requirement in Section 5 is either backed by a specified mechanism or explicitly marked as lacking a numeric threshold.
- Each data requirement in Section 6 maps to an entity, table, storage mechanism, or data-flow statement from the PDF.
- Each constraint in Section 7 maps to an explicitly named technology, platform, model, or standard from the PDF.
- The full per-requirement verification mapping is provided in the traceability matrix below.

## 9. Traceability Matrix

| ID | Requirement | Type | Source | Evidence Type | Verification | Confidence |
|---|---|---|---|---|---|---|
| FR-001 | Support administrator, annotator, and researcher user classes. | Functional | TAS-002 | explicit | Demonstration | High |
| FR-002 | Support flexible role management and task switching. | Functional | TAS-002 | explicit | Demonstration | Medium |
| FR-003 | Allow first-time user registration. | Functional | TAS-006, TAS-010 | explicit | Test | High |
| FR-004 | Authenticate users and support login/logout/profile viewing. | Functional | TAS-006, TAS-010 | explicit | Test | High |
| FR-005 | Define and create annotation presets. | Functional | TAS-002, TAS-004 | explicit | Demonstration | Medium |
| FR-006 | Manage annotation projects. | Functional | TAS-006 | explicit | Test | High |
| FR-007 | Manage project annotators. | Functional | TAS-006 | explicit | Test | High |
| FR-008 | Manage annotation literature/documents. | Functional | TAS-006, TAS-008 | explicit | Test | High |
| FR-009 | Download files. | Functional | TAS-006, TAS-008 | explicit | Test | Medium |
| FR-010 | Manage tags for tasks/documents. | Functional | TAS-006, TAS-008 | explicit | Test | High |
| FR-011 | Assign and query annotation tasks. | Functional | TAS-006 | explicit | Test | High |
| FR-012 | Mark annotation tasks as completed. | Functional | TAS-006, TAS-008 | explicit | Test | High |
| FR-013 | Provide task-level data statistics. | Functional | TAS-006 | explicit | Test | Medium |
| FR-014 | Manage annotation marks. | Functional | TAS-006, TAS-008 | explicit | Test | High |
| FR-015 | Persist annotation result details. | Functional/Data | TAS-008 | explicit | Inspection | High |
| FR-016 | Return or export annotation results. | Functional | TAS-002, TAS-006 | explicit | Demonstration | Medium |
| FR-017 | Upload mining documents. | Functional | TAS-009 | explicit | Test | High |
| FR-018 | Convert uploaded documents into supported formats. | Functional | TAS-008, TAS-009 | explicit | Test | High |
| FR-019 | Select mining model from supported sources/interfaces. | Functional | TAS-009 | explicit | Demonstration | High |
| FR-020 | Extract paragraph annotation information and key data. | Functional | TAS-009 | explicit | Test | High |
| FR-021 | Locate paragraphs and recognize entities using model capabilities. | Functional | TAS-003, TAS-005 | explicit | Test | High |
| FR-022 | Support few-shot-learning-oriented extraction. | Functional | TAS-001 | explicit | Analysis | Medium |
| FR-023 | Provide the listed UI workflow pages. | Functional/UI | TAS-010 | explicit | Demonstration | High |
| NFR-001 | Improve annotation/extraction accuracy and consistency through presets. | Non-functional | TAS-001, TAS-004 | explicit | Analysis | Medium |
| NFR-002 | Efficiently process and analyze large text datasets. | Non-functional | TAS-001, TAS-003 | explicit | Analysis | Medium |
| NFR-003 | Improve response speed through async interaction and cache support. | Non-functional | TAS-003, TAS-005 | explicit | Test | Medium |
| NFR-004 | Support scalability/extensibility through microservice mechanisms. | Non-functional | TAS-003, TAS-005 | explicit | Inspection | Medium |
| NFR-005 | Support authentication and authorization. | Non-functional | TAS-005 | explicit | Test | High |
| NFR-006 | Preserve deployment portability through Docker. | Non-functional | TAS-003, TAS-005 | explicit | Inspection | High |
| NFR-007 | Provide intuitive web UI using the selected UI stack. | Non-functional | TAS-003, TAS-005, TAS-010 | explicit | Demonstration | Medium |
| NFR-008 | Support maintainability through architecture/tooling choices. | Non-functional | TAS-003, TAS-005 | explicit | Inspection | Medium |
| NFR-009 | Use asynchronous queue processing for conversion-like tasks. | Non-functional | TAS-005 | explicit | Test | High |
| NFR-010 | Deploy on specified stable cloud/runtime infrastructure. | Non-functional | TAS-005 | explicit | Inspection | Medium |
| DR-001 | Store user data. | Data | TAS-008 | explicit | Inspection | High |
| DR-002 | Represent role identity by project context. | Data | TAS-007 | explicit | Inspection | Medium |
| DR-003 | Store annotation project data. | Data | TAS-007, TAS-008 | explicit | Inspection | High |
| DR-004 | Store document/object file references. | Data | TAS-007, TAS-008 | explicit | Inspection | High |
| DR-005 | Store paper/document relation and format references. | Data | TAS-008 | explicit | Inspection | High |
| DR-006 | Store annotator relations. | Data | TAS-007, TAS-008 | explicit | Inspection | High |
| DR-007 | Store tags. | Data | TAS-008 | explicit | Inspection | High |
| DR-008 | Store tasks. | Data | TAS-008 | explicit | Inspection | High |
| DR-009 | Store annotation result/label data. | Data | TAS-008 | explicit | Inspection | High |
| DR-010 | Represent model and preset concepts. | Data | TAS-004 | explicit | Inspection | Medium |
| DIO-001 | Accept uploaded documents and maintain metadata/index records. | Data flow | TAS-006, TAS-009 | explicit | Test | High |
| DIO-002 | Maintain PDF/HTML/TXT references after conversion. | Data flow | TAS-008, TAS-009 | explicit | Inspection | High |
| DIO-003 | Produce annotation outputs for downstream workflows. | Data flow | TAS-001, TAS-006, TAS-008 | explicit | Demonstration | Medium |
| DIO-004 | Produce extracted paragraph/key data outputs. | Data flow | TAS-009 | explicit | Test | High |
| DSR-001 | Store structured records in MySQL. | Data storage | TAS-003, TAS-005 | explicit | Inspection | High |
| DSR-002 | Store documents in object storage and indexes in relational storage. | Data storage | TAS-003, TAS-007, TAS-008 | explicit | Inspection | High |
| DSR-003 | Use Redis cache for access speed and response improvement. | Data storage | TAS-003, TAS-005 | explicit | Inspection | High |
| DSR-004 | Retention, deletion, encryption, and migration details are not specified in the PDF. | Missing data requirement | TAS-001 | explicit missing information | Inspection | High |
| C-001 | Use Vue/Vue 3.0, vue-router, Pinia, Ant Design, and Axios. | Constraint | TAS-003, TAS-005 | explicit | Inspection | High |
| C-002 | Use Spring Boot/Spring Cloud. | Constraint | TAS-003, TAS-005 | explicit | Inspection | High |
| C-003 | Use Spring Gateway and Spring Security. | Constraint | TAS-005 | explicit | Inspection | High |
| C-004 | Use Nginx as reverse proxy/load balancer. | Constraint | TAS-003 | explicit | Inspection | High |
| C-005 | Use Mybatis/Mybatis Plus. | Constraint | TAS-003, TAS-005 | explicit | Inspection | High |
| C-006 | Use MySQL, Minio, and Redis. | Constraint | TAS-003, TAS-005 | explicit | Inspection | High |
| C-007 | Use BERT and GPT/GPT API model capabilities. | Constraint | TAS-003, TAS-005 | explicit | Inspection | High |
| C-008 | Use RabbitMQ for async queues. | Constraint | TAS-003, TAS-005 | explicit | Inspection | High |
| C-009 | Use Docker for containerized deployment. | Constraint | TAS-003, TAS-005 | explicit | Inspection | High |
| C-010 | Use Tencent Cloud for runtime/deployment. | Constraint | TAS-005 | explicit | Inspection | High |
| C-011 | Reference GB/T 9385-2008 and GB/T 8567-2006 standards. | Constraint | TAS-011 | explicit | Inspection | High |
