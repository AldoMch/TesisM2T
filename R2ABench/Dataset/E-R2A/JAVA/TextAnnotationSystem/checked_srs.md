# Software Requirements Specification: Intelligent Text Annotation System (ITAS)

## 1. Introduction

### Product Scope

ITAS is a web-based system for processing and analyzing large volumes of text data. It contains two connected subsystems:

- Text annotation subsystem: supports paragraph/entity annotation for scientific literature and provides annotation results to the mining subsystem.
- Intelligent mining subsystem: uses large language models and natural language processing techniques to identify and extract predefined information from unannotated text.

### Intended Audience

The intended audience includes ITAS developers, testers, system annotation administrators, data annotators, researchers, and the expert group referenced by the source design document.

## 2. Overall Description

### Product Perspective

ITAS is described as a front-end/back-end separated web system that combines web application services, structured and object storage, caching, message queues, and machine-learning-based text processing. The annotation subsystem precedes the mining subsystem by producing annotated data that can be used for later extraction and model-related workflows.

### Product Functions Summary

| Area | Summary |
| --- | --- |
| User and role support | Supports system annotation administrators, data annotators, and researchers, including flexible role management and task switching. |
| Annotation management | Supports annotation projects, annotators, documents, tags, marks, tasks, results, and user information. |
| Mining workflow | Supports document upload, automatic format conversion, model selection, and information extraction. |
| Data management | Stores users, projects, documents, tags, tasks, annotation results, object-storage references, and document format references. |
| User interfaces | Provides screens for login, profile management, mining, upload, results, project creation/management, and task execution. |

### User Classes

| User class | Description | Major responsibilities |
| --- | --- | --- |
| System annotation administrator | Representative of a research institution, university, or enterprise that needs high-quality data support. | Define presets, upload documents, manage annotation projects, export annotation data, and participate in model training and validation. |
| Data annotator | Professional annotator, domain researcher, or student performing concrete annotation tasks. | Execute assigned document annotation tasks using system guidance and presets. |
| Researcher | Researcher, scientist, technical worker, or data analyst using the mining subsystem. | Extract and mine key information from literature with minimal manual intervention. |

### Operating Environment

The specification states a modern web environment with Vue-based front end, Spring-based back end, Nginx reverse proxy, MySQL, Minio, Redis, BERT/GPT model integration, RabbitMQ, Docker, and Tencent Cloud deployment.

### Assumptions and Dependencies

| ID | Statement |
| --- | --- |
| AD-001 | Annotation outputs are expected to support later intelligent mining and extraction workflows. |
| AD-002 | Third-party model/API availability, such as GPT API or ChatGPT-like interfaces, is required for the implemented mining model invocation approach. |
| AD-003 | Object storage is required for text/unstructured documents, while relational storage keeps structured records and document indexes. |
| AD-004 | RabbitMQ-backed asynchronous processing is used for tasks such as file conversion. |

## 3. External Interface Requirements

### User Interfaces

| UI ID | Requirement |
| --- | --- |
| UI-001 | The system shall provide registration and login interfaces. |
| UI-002 | The system shall provide a personal information management interface. |
| UI-003 | The system shall provide a mining main interface, mining file upload interface, and mining result display interface. |
| UI-004 | The system shall provide annotation project creation, annotation project management, and annotation task execution interfaces. |
| UI-005 | The front-end interface shall be implemented with Vue.js/Vue 3.0 and Ant Design/Ant-Design-Vue components as specified by the specification. |

### Software/API Interfaces

| API ID | Requirement |
| --- | --- |
| API-001 | The annotation subsystem shall expose controller-level functions for annotator, file, label, login, paper, project, result export/return, tag, task, and user management. |
| API-002 | The mining subsystem shall expose functions for document upload, model selection, and information extraction. |
| API-003 | The system shall integrate with GPT API or a third-party ChatGPT-like interface for entity annotation or mining model invocation where specified. |
| API-004 | The system shall interact with MySQL for structured records, Minio for object storage, and Redis for cache access. |

### Communication Interfaces

| COM ID | Requirement |
| --- | --- |
| COM-001 | The front end shall communicate asynchronously with the back end through Axios HTTP client calls. |
| COM-002 | Nginx shall provide reverse proxy, request forwarding, and load balancing responsibilities. |
| COM-003 | Spring Cloud shall support service discovery, configuration management, load balancing, and inter-service communication concerns. |
| COM-004 | RabbitMQ shall support message-queue-based asynchronous processing for workflows such as file conversion. |

### Data Exchange Formats

| DATA-IF ID | Requirement |
| --- | --- |
| DIF-001 | The system shall handle uploaded documents and maintain references for PDF, HTML, and TXT representations where document conversion is performed. |
| DIF-002 | The system shall exchange annotation entities including projects, documents, tags, tasks, labels, and annotation results through back-end data APIs. |
| DIF-003 | The system shall store object-storage identifiers and bucket references for files whose content is not stored directly in the relational database. |

## 4. Functional Requirements

| ID | Description | Trigger/Input | System Behavior | Output | Priority | Verification |
| --- | --- | --- | --- | --- | --- | --- |
| FR-001 | The system shall support three user classes: system annotation administrator, data annotator, and researcher. | A user account is created or used. | The system associates users with role-specific responsibilities and functions. | Role-specific access and task context. | Must | Demonstration |
| FR-002 | The system shall support flexible role management and task switching for users who perform multiple research-stage responsibilities. | A user needs to operate under a different role or task context. | The system enables switching between role/task contexts without losing the relevant workflow context. | Active role/task context. | Should | Demonstration |
| FR-003 | The system shall allow first-time users to register accounts. | A user submits registration information. | The system creates a user account record. | Registered user account. | Must | Test |
| FR-004 | The system shall authenticate users and support login, logout, and personal information viewing. | A user submits credentials or requests account information. | The system validates access and returns the requested session/profile operation. | Authenticated session, logout result, or personal information view. | Must | Test |
| FR-005 | The system shall allow administrators to define and create annotation presets for paragraph/entity annotation and extraction. | An administrator identifies that existing presets do not satisfy a research need. | The system records configurable rules/templates used to guide annotation and extraction. | New or updated preset. | Should | Demonstration |
| FR-006 | The system shall support annotation project management. | An administrator creates, updates, lists, or queries annotation projects. | The system creates projects, updates projects, lists all projects, lists the user's projects, updates project introductions, and queries projects by ID. | Project record or project list. | Must | Test |
| FR-007 | The system shall support annotation personnel management per project. | An administrator adds, deletes, or queries project annotators. | The system updates or returns the annotator set for the project. | Annotator membership result or annotator list. | Must | Test |
| FR-008 | The system shall support annotation literature/document management. | A user uploads, deletes, views, or queries project literature. | The system stores document metadata and supports retrieval by project ID. | Uploaded document record, deleted status, document view, or query result. | Must | Test |
| FR-009 | The system shall support file download. | A user requests a downloadable file. | The system retrieves the referenced file content or object-storage record. | Downloaded file. | Should | Test |
| FR-010 | The system shall support tag management for annotation tasks and documents. | A user creates, edits, deletes, or queries labels/tags. | The system maintains tag records and supports queries by task ID and document ID. | Created/updated/deleted tag or tag query result. | Must | Test |
| FR-011 | The system shall support annotation task assignment and task lookup. | An administrator assigns tasks or a user requests task lists/details. | The system assigns annotation tasks, returns all tasks, returns the current user's tasks, and queries tasks by ID. | Assigned task or task query result. | Must | Test |
| FR-012 | The system shall allow users to mark annotation tasks as completed. | An annotator finishes an assigned task. | The system updates the task completion state. | Completed-task status. | Must | Test |
| FR-013 | The system shall provide task-level data statistics for annotation management. | A user requests task statistics. | The system computes and returns task-related statistical information. | Task statistics result. | Should | Test |
| FR-014 | The system shall support annotation mark management. | An annotator adds, views, modifies, or deletes an annotation mark. | The system creates, reads, updates, or deletes the mark record. | Annotation mark result. | Must | Test |
| FR-015 | The system shall persist annotation results with content, remark, tag, location, offset, creator, and timestamp information. | An annotation mark/result is submitted. | The system stores the annotation result fields defined in the label/annotation-result table. | Persisted annotation result. | Must | Inspection |
| FR-016 | The system shall support returning or exporting annotation results for downstream use. | An administrator or workflow requests annotation results. | The system returns the collected annotation result data. | Annotation result output. | Must | Demonstration |
| FR-017 | The mining subsystem shall support document upload. | A researcher uploads a document for mining. | The system accepts the user-selected document for later processing. | Uploaded mining document record. | Must | Test |
| FR-018 | The mining subsystem shall support automatic document format conversion. | A document is uploaded for mining or annotation processing. | The system converts the document into supported representations where required. | Converted document representation and related identifiers. | Must | Test |
| FR-019 | The mining subsystem shall support model selection. | A researcher prepares to run data mining. | The system allows selection from built-in preset models, community-shared models, or third-party interfaces, with third-party API invocation specified as implemented. | Selected model or model invocation configuration. | Must | Demonstration |
| FR-020 | The mining subsystem shall extract paragraph annotation information and key data according to user needs. | A document and model selection are ready. | The system runs the selected model workflow to extract paragraph-level information and key data. | Extraction result. | Must | Test |
| FR-021 | The system shall support automated paragraph localization and entity recognition for text processing. | A text document is processed by the annotation/mining workflow. | The system uses paragraph-location and entity-recognition model capabilities to identify relevant paragraphs and entities. | Located paragraph and recognized entity information. | Must | Test |
| FR-022 | The system shall support few-shot-learning-oriented extraction for data-scarce research scenarios. | The available annotated examples are scarce. | The mining model workflow uses few-shot learning support to improve information extraction from unannotated text. | Extraction results under scarce-data conditions. | Should | Analysis |
| FR-023 | The system shall provide user interface pages for registration/login, profile management, mining, upload, result display, project creation, project management, and task execution. | A user navigates to a supported workflow. | The front end displays the corresponding workflow interface. | Rendered workflow page. | Must | Demonstration |

## 5. Non-Functional Requirements

| ID | Quality | Requirement | Priority | Verification |
| --- | --- | --- | --- | --- |
| NFR-001 | Accuracy/Consistency | The system shall use preset annotation rules/templates to improve the accuracy and consistency of paragraph/entity annotation and extraction. | Must | Analysis |
| NFR-002 | Efficiency | The system shall support efficient processing and analysis of large text datasets; the specification does not provide a numeric throughput target. | Must | Analysis |
| NFR-003 | Responsiveness | The system shall use asynchronous front-end/back-end interaction and cache support to improve perceived response speed; the specification does not provide a latency threshold. | Should | Test |
| NFR-004 | Scalability/Extensibility | The system shall use service discovery, configuration management, load balancing, and microservice support to enable service extension and deployment scaling. | Should | Inspection |
| NFR-005 | Security | The system shall support user authentication and authorization through the specified gateway/security stack. | Must | Test |
| NFR-006 | Portability | The system shall use Docker containerization to preserve environment consistency and deployment portability. | Should | Inspection |
| NFR-007 | Usability | The system shall provide rich, intuitive web user interfaces using the specified Vue and Ant Design technology choices. | Should | Demonstration |
| NFR-008 | Maintainability | The system shall use the specified layered web architecture, ORM/data access tooling, and development workflow to support manageable development and testing. | Should | Inspection |
| NFR-009 | Asynchronous Processing | The system shall process asynchronous tasks such as file conversion through RabbitMQ to reduce synchronous workflow delay. | Should | Test |
| NFR-010 | Reliability/Deployment Stability | The system shall deploy on the specified cloud/runtime infrastructure to provide a stable operating environment; the specification does not define availability targets. | Should | Inspection |

## 6. Data Requirements

### Data Entities or Objects

| ID | Entity/Object | Required Data |
| --- | --- | --- |
| DR-001 | User | User ID, username, real name, password, roles, creation date, update date. |
| DR-002 | Role identity | Administrator and annotator identities can vary according to project context. |
| DR-003 | Annotation project | Project ID, name, introduction, status/assignment fields, attachment ID/name, creation/update/assignment/completion timing where defined. |
| DR-004 | Document/object file | File ID, filename, object name, object-storage bucket, creation date, update date. |
| DR-005 | Paper/document relation | Project ID, identifier, filename, PDF ID, HTML ID, TXT ID, status, creation date, update date. |
| DR-006 | Annotator relation | Project ID and user ID relation between annotation projects and annotators. |
| DR-007 | Tag | Tag ID, project ID, tag key, tag name, creation date, update date. |
| DR-008 | Task | Task ID, project ID, user ID, paper ID, document identifiers, PDF/HTML/TXT IDs, completion flag, timestamps. |
| DR-009 | Annotation result/label | Task ID, content, remark, tag ID, location, start offset, end offset, creator ID, creator name, timestamps. |
| DR-010 | Model/preset concepts | Paragraph model, entity model, preset, paragraph preset, and entity preset definitions used by annotation/extraction workflows. |

### Input/Output Data

| ID | Data flow | Requirement |
| --- | --- | --- |
| DIO-001 | Uploaded documents | The system shall accept documents for annotation and mining workflows and maintain metadata/index records. |
| DIO-002 | Converted documents | The system shall maintain PDF, HTML, and TXT references when document format conversion is used. |
| DIO-003 | Annotation outputs | The system shall produce annotation result data that can be returned and used by downstream mining/model workflows. |
| DIO-004 | Mining outputs | The system shall produce extracted paragraph annotation information and key data. |

### Storage, Privacy, Integrity, Retention, or Migration

| ID | Requirement |
| --- | --- |
| DSR-001 | Structured records shall be stored in MySQL. |
| DSR-002 | Text and unstructured document content shall be stored through Minio/object storage, with relational records storing indexes. |
| DSR-003 | Redis shall be used as a cache to improve access speed and system response. |
| DSR-004 | The PDF document does not specify retention duration, deletion policy, encryption method, or migration requirements. |

## 7. Constraints

| ID | Constraint | Type |
| --- | --- | --- |
| C-001 | The front end shall use Vue.js/Vue 3.0 with vue-router, Pinia, Ant Design/Ant-Design-Vue, and Axios as specified. | Technology |
| C-002 | The back end shall use Spring Boot/Spring Cloud microservice architecture where specified. | Technology |
| C-003 | The gateway/security stack shall use Spring Gateway and Spring Security for authentication and authorization. | Technology/Security |
| C-004 | Nginx shall act as reverse proxy for load balancing and request forwarding. | Deployment |
| C-005 | Mybatis/Mybatis Plus shall be used for database access/ORM operations. | Technology |
| C-006 | MySQL, Minio, and Redis shall be used for structured storage, object storage, and caching respectively. | Data platform |
| C-007 | BERT shall be used for paragraph model capability and GPT/GPT API shall be used for entity model/interface capability as specified. | ML/model |
| C-008 | RabbitMQ shall be used for asynchronous message queue processing such as file conversion. | Infrastructure |
| C-009 | Docker shall be used for containerized deployment and environment consistency. | Deployment |
| C-010 | Tencent Cloud is specified as the deployment/runtime environment and public access hosting platform. | Deployment |
| C-011 | The specification references GB/T 9385-2008 and GB/T 8567-2006 as documentation standards. | Standard |

## 8. Verification and Acceptance

Verification methods:

- Test: execute the function or quality check through system/API/UI tests.
- Demonstration: show the workflow in the running system or prototype.
- Inspection: review design, configuration, database schema, or code artifacts.
- Analysis: reason from logs, data samples, or model behavior where direct execution is not sufficient.

Acceptance criteria:

- Each functional requirement in Section 4 has a demonstrable or testable workflow.
- Each non-functional requirement in Section 5 is either backed by a specified mechanism or explicitly marked as lacking a numeric threshold.
- Each data requirement in Section 6 maps to an entity, table, storage mechanism, or data-flow statement defined in the SRS.
- Each constraint in Section 7 maps to an explicitly named technology, platform, model, or standard defined in the SRS.
- Requirement verification methods are listed in the applicable requirement tables and acceptance criteria.
