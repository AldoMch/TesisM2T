# AwesomeMusic Software Requirements Specification (Standard SRS Extract)

## 1. Introduction

### Purpose

This document extracts verifiable requirements from `AwesomeMusic_origin.md` and rewrites them according to the compact SRS standard in `architectural_views_rep-pkg/script/templates/SRS.md`. Its purpose is to provide structured input for architecture generation, test design, and requirements traceability for an AI music creation and sharing platform. Source evidence is listed in `awesome_music_md_evidence_pack.json`. (Source: AM-001)

### Product Scope

The AI music creation and sharing platform is a Web system for music enthusiasts. After registration, users can use the platform for AI music creation, score generation, score upload and sharing, favorites, follows, recommendations, search, hot charts, and downloads. The system contains three modules: Web frontend, Web backend, and algorithm service. The algorithm service generates music from user-provided source files and includes online music generation and offline model iterative upgrade services. (Source: AM-001, AM-002, AM-003)

This document follows the source document definitions of MQ, score, track seed, and midi music. A score is an abc-format plain-text file that can generate midi music. A track seed is the beginning part of an abc score and is less than 10 seconds long. Midi music is a music file playable by midi-capable players. (Source: AM-001, AM-002)

### Intended Audience

This document is intended for customers, product managers, developers, testers, and downstream architecture generation and requirements review workflows. Target end users are music enthusiasts, especially users interested in AI music creation, music sharing, and novel approaches to music creation. (Source: AM-001, AM-004)

### References

| Ref | Source |
| --- | --- |
| REF-001 | GB/T 9385-2008, Computer Software Requirements Specification, Standardization Administration of China |

## 2. Overall Description

### Product Perspective

AwesomeMusic is a Web system supported by a Web frontend, Web backend, algorithm service, and scheduling capability. The frontend provides interactions such as login, source file upload, music generation, and music sharing. The backend provides data interfaces, data storage, and service coordination and scheduling. The algorithm service generates music from input source files. The scheduling module triggers daily training, classification, recommendation, and user-submitted generation tasks through task queues. (Source: AM-002, AM-010)

### Product Functions Summary

| Capability | Summary | Source |
| --- | --- | --- |
| Account and user relationships | Support registration, login, and following users. | AM-003, AM-008 |
| Score content management | Support favoriting scores, uploading scores, downloading scores, searching scores, and viewing hot charts. | AM-003, AM-008 |
| AI score generation | Users select a model and original music to generate a score; the algorithm converts midi to abc, extracts 5 track seeds, generates a score, and converts it back to midi. | AM-003, AM-008, AM-009 |
| Model management | Support favoriting models; the algorithm trains and updates a dedicated GPT-2 score generation model for each user every day. | AM-008, AM-009 |
| Recommendations and hot charts | The system recommends scores based on favorites, follows, and score similarity, and updates score and user hot charts. | AM-003, AM-008, AM-009 |
| Scheduled tasks | Trigger training, classification, and recommendation tasks early every morning; trigger generation tasks when users submit them. | AM-010 |

### User Classes

| User Class | Responsibilities / Needs | Source |
| --- | --- | --- |
| General user / music enthusiast | After registration and login, use the platform for music creation, score upload, download, search, favorites, follows, recommendations, and hot-chart browsing. | AM-003, AM-004 |
| Music production beginner | Needs simple and understandable interactions, descriptions, prompts, and guidance to get started quickly. | AM-012 |
| Composer | Uses the trained generation model and score generation capability to create midi music. | AM-009 |
| Music appreciator | Browses, classifies, recommends, and downloads scores, and cares about music quality and diversity of music styles. | AM-004, AM-009 |

### Operating Environment

| Environment | Requirement | Source |
| --- | --- | --- |
| Hardware | 4 virtual machines, each with CPU 4 * 2400MHz, 8GB memory, and 200GB storage. | AM-007 |
| Operating system | Ubuntu 18.04 LTS. | AM-007 |
| Software interfaces | Apache Hadoop 3.2.2, RabbitMQ 3.8.14, etcd 3.4.15, and Nginx 1.19.8. | AM-007 |
| Communication protocols | HTTPS and TCP/IP. | AM-007 |
| Frontend technology | HTML, CSS, JavaScript, and Bootstrap framework. | AM-005 |
| Backend technology | Golang and Gin framework. | AM-005 |

### Assumptions and Dependencies

| ID | Assumption / Dependency | Evidence Type | Source |
| --- | --- | --- | --- |
| AD-001 | Changes to programming languages or development frameworks may affect project phases and the overall schedule. | explicit | AM-006 |
| AD-002 | Temporary hardware devices such as servers may not meet requirements and affect product deployment planning. | explicit | AM-006 |
| AD-003 | Late changes to requirements analysis can cause rework in documentation and code and may delay the schedule. | explicit | AM-006 |
| AD-004 | R&D team member changes or communication deviations may affect development cycle and product quality. | explicit | AM-006 |
| AD-005 | If the algorithm model cannot satisfy user needs, final product quality will decrease. | explicit | AM-006 |
| AD-006 | The product testing phase depends on stable collaboration among modules. | explicit | AM-006 |
| AD-007 | All use-case diagram requirements listed in the source document are planned for implementation in the current version. | explicit | AM-006 |

## 3. External Interface Requirements

### User Interfaces

| Interface | Requirement | Source |
| --- | --- | --- |
| Registration and login interface | Support account registration and login interactions. | AM-007, AM-008 |
| Homepage interface | Support display of recommendations, hot charts, and main entries. | AM-007, AM-008 |
| Search and list interface | Support searching scores by song name and displaying search results. | AM-007, AM-008 |
| Song detail interface | Support viewing score details, favoriting, downloading, and related operations. | AM-007, AM-008 |
| Song generation interface | Support selecting a model and original music to generate a score. | AM-007, AM-008 |
| Personal center interface | Support personal resource management such as favorites, follows, and model lists. | AM-007, AM-008 |

### Software/API Interfaces

| Interface | Requirement | Source |
| --- | --- | --- |
| Web frontend interface | The frontend uses HTML, CSS, JavaScript, and Bootstrap. | AM-005 |
| Web backend interface | The backend uses Golang and Gin and provides data interfaces, data storage, and service coordination and scheduling for the frontend. | AM-002, AM-005 |
| Algorithm service interface | The algorithm service generates music from user-provided source files and includes online generation and offline model iterative upgrade. | AM-002, AM-009 |
| Scheduling and message interface | The scheduling module serializes task metadata and pushes it to a task queue, then polls task status; the source document defines MQ for reliable message transmission. | AM-001, AM-010 |
| Basic software interface | The system uses software interfaces such as Hadoop, RabbitMQ, etcd, and Nginx. | AM-007 |

### Communication Interfaces

System communication interfaces are HTTPS and TCP/IP. The source document does not specify concrete REST APIs, RPC, message formats, or authentication protocols. (Source: AM-007)

### Data Exchange Formats

The system needs to process user identity information, email, score data, score ID, followed user fields, favorited model ID, original music data, model ID, user-favorited score information, followed user information, song name, user ID, playlist, midi files, abc scores, track seeds, task metadata, task status, and logs. The source document does not specify JSON schemas, database table structures, or file upload protocols. (Source: AM-008, AM-009, AM-010)

## 4. Functional Requirements

| ID | Requirement | Trigger / Input | System Behavior | Output | Priority | Verification | Source |
| --- | --- | --- | --- | --- | --- | --- | --- |
| FR-001 | The system shall support ordinary users registering accounts. | An unauthenticated user opens the registration page, fills in identity information such as username, password, and email, and clicks register. | The system validates information format and whether the username is duplicated. If the information is invalid or the username is duplicated, it prompts the user and requests re-entry. | New account or registration error prompt. | High | Test | AM-008 |
| FR-002 | The system shall support ordinary users logging in. | A registered user enters account name and password and clicks login. | The system checks whether the account exists and whether login information is correct. After success, it redirects to the homepage or previously browsed page; after failure, it prompts the reason. | Login state or error prompt. | High | Test | AM-008 |
| FR-003 | The system shall support favoriting scores. | A logged-in user clicks the favorite button for a score resource. | The system places the resource into favorites and prompts success. When the system is busy or a network issue occurs, it prompts the user to try later. The user can cancel the favorite. | Favorite record and feedback prompt. | High | Test | AM-008 |
| FR-004 | The system shall support following users. | A logged-in user clicks the follow button for a target user. | The system places the target user into the follow list, prompts success, and changes the button style. When the system is busy or a network issue occurs, it prompts the user to try later. The user can unfollow. | Follow record and feedback prompt. | High | Test | AM-008 |
| FR-005 | The system shall support Web-side score generation. | A logged-in user selects a training model and original music, then clicks generate score. | The system submits user fields, original music data, and model, generates a score, and displays the result. When the system is busy or a network issue occurs, it prompts the user to try later. | Generated score or failure prompt. | High | Test | AM-008 |
| FR-006 | The system shall support score upload. | A logged-in user who has generated a score clicks upload. | The system saves user fields and score data, modifies the database, and prompts upload success. When the system is busy or a network issue occurs, it prompts the user to try later. | Uploaded score record or failure prompt. | High | Test | AM-008 |
| FR-007 | The system shall support favoriting models. | A logged-in user enters another user's homepage, views a model, and clicks favorite. | The system adds the model to the user's model list and prompts success. The user can manage the user's own model list. | Model favorite record and feedback prompt. | Medium | Test | AM-008 |
| FR-008 | The system shall support obtaining a recommended music list. | A logged-in user enters the homepage and views the recommended playlist. | The system generates or displays a recommended playlist based on user fields, favorite score information, and followed user information. When the system is busy or a network issue occurs, it prompts the user to try later. | Recommended music list or failure prompt. | High | Test | AM-008 |
| FR-009 | The system shall support score search. | A logged-in user enters the search page and inputs a song name. | The system searches piano pieces and scores by song name and displays search results, which may be empty. When the system is busy or a network issue occurs, it prompts the user to try later. | Search results or failure prompt. | High | Test | AM-008 |
| FR-010 | The system shall support hot-chart viewing. | A logged-in user enters the homepage to view hot charts. | The system displays hot songs and creator lists. When the system is busy or a network issue occurs, it prompts the user to try later. | Hot song and creator lists. | Medium | Test | AM-008 |
| FR-011 | The system shall support score download. | A logged-in user clicks the score download button and selects a download path. | The system returns download success or failure. When the system is busy or a network issue occurs, it prompts the user to try later. | Local score file or failure prompt. | Medium | Test | AM-008 |
| FR-012 | The algorithm module shall train user-specific generation models. | A user ID and playlist are given, or a daily training task is triggered. | The system reads user model parameters, converts midi playlists to abc, preprocesses and selects the main track, fine-tunes and saves model parameters. If midi cannot be converted, it notifies the scheduler of an exception. | Updated user generation model parameters. | High | Test | AM-009 |
| FR-013 | The algorithm module shall generate scores. | A user ID and seed score are given. | The system reads user model parameters, converts the seed score to abc, preprocesses and selects 5 track seeds, generates a score of a certain length, concatenates it into an abc file, and converts it to midi. If conversion fails, it retries; after two failures, it notifies the backend to restore model parameters. | Reasonable midi song or exception notification. | High | Test | AM-009 |
| FR-014 | The algorithm module shall classify all scores. | A score list to be classified is obtained. | The system converts scores to abc, loads an existing model to generate score representations, and classifies scores based on representations. If midi cannot be converted, it notifies the backend of an exception. | Score labels. | High | Test | AM-009 |
| FR-015 | The algorithm module shall recommend songs for users. | User IDs and their song lists are given. | The system converts scores to abc, uses an existing model to generate representations, calculates song cosine similarity and user similarity, and recommends some songs from similar users to the current user. If a user has no playlist, it recommends randomly. | Song recommendation list for each user. | High | Test | AM-009 |
| FR-016 | The scheduling module shall trigger training tasks. | The task runs automatically at 02:00 every day. | The system serializes training model IDs, score IDs to be classified, and user IDs for recommendation, pushes them to the task queue, and polls task status. When queue write or status retrieval fails, it records logs and retries. | Training, classification, and recommendation task status. | High | Test | AM-010 |
| FR-017 | The scheduling module shall trigger generation tasks. | A user submits a score generation task. | The system encodes generation source material ID and model ID, pushes them to the task queue, triggers the generation task when the algorithm module is idle, and polls task status. When queue write or status retrieval fails, it records logs and retries. | Generation task status. | High | Test | AM-010 |
| FR-018 | The system shall update score hot charts and user hot charts. | A user accesses the product. | The system updates score hot charts based on score attention level and updates user hot charts by calculating user popularity according to rules. | Updated score hot charts and user hot charts. | Medium | Test | AM-003 |

## 5. Non-Functional Requirements

| ID | Quality | Requirement | Fit Criterion | Priority | Verification | Source |
| --- | --- | --- | --- | --- | --- | --- |
| NFR-001 | Performance | Average account registration latency shall satisfy the performance table. | Average latency <= 200ms. | High | Test | AM-011 |
| NFR-002 | Performance | Average login latency shall satisfy the performance table. | Average latency <= 200ms. | High | Test | AM-011 |
| NFR-003 | Performance | Average score favorite latency shall satisfy the performance table. | Average latency <= 200ms. | High | Test | AM-011 |
| NFR-004 | Performance | Average follow-user latency shall satisfy the performance table. | Average latency <= 200ms. | High | Test | AM-011 |
| NFR-005 | Performance | Average score upload latency shall satisfy the performance table. | Average latency <= 3000ms. | High | Test | AM-011 |
| NFR-006 | Performance | Average model favorite latency shall satisfy the performance table. | Average latency <= 200ms. | Medium | Test | AM-011 |
| NFR-007 | Performance | Average Web-side score generation latency shall satisfy the performance table. | Average latency <= 200ms. | High | Test | AM-011 |
| NFR-008 | Performance | Average score download latency shall satisfy the performance table. | Average latency <= 3000ms. | Medium | Test | AM-011 |
| NFR-009 | Performance | Average recommendation retrieval latency shall satisfy the performance table. | Average latency <= 500ms. | High | Test | AM-011 |
| NFR-010 | Performance | Average score search latency shall satisfy the performance table. | Average latency <= 1000ms. | High | Test | AM-011 |
| NFR-011 | Performance | Average hot-chart viewing latency shall satisfy the performance table. | Average latency <= 200ms. | Medium | Test | AM-011 |
| NFR-012 | Performance | Algorithm training for generation models shall complete daily. | Throughput 1/day, average latency <= 1.5h. | High | Test | AM-011 |
| NFR-013 | Performance | Algorithm score generation shall satisfy throughput and latency requirements. | Throughput 5ops, average latency <= 1min. | High | Test | AM-011 |
| NFR-014 | Performance | Classifying all scores shall complete daily. | Throughput 1/day, average latency <= 1.5h. | High | Test | AM-011 |
| NFR-015 | Performance | Song recommendation shall complete daily. | Throughput 1/day, average latency <= 1.5h. | High | Test | AM-011 |
| NFR-016 | Scalability | The Web system shall support the preset concurrent access throughput. | Concurrent access throughput is no less than 2000QPS. | High | Test | AM-011 |
| NFR-017 | Scalability | The Web system shall support transaction change throughput. | Transaction changes are no less than 100TPS. | High | Test | AM-011 |
| NFR-018 | Usability | System interactions shall be suitable for music production beginners. | Interactions are simple and understandable and do not require professional function design. | Medium | Demonstration | AM-012 |
| NFR-019 | Usability | The system shall provide user instructions, prompts, and guidance. | Comprehensive instructions, prompts, and guidance exist to help users get started quickly. | Medium | Inspection | AM-012 |
| NFR-020 | Security | The gateway shall isolate internal and external network boundaries. | Internal systems are not exposed externally due to loose security configuration. | High | Inspection | AM-013 |
| NFR-021 | Reliability | Important data shall be stored in multiple replicas. | Important data is stored in 3 replicas. | High | Inspection | AM-013 |
| NFR-022 | Availability | The system shall remain available under partial failures. | The system remains usable when some internal nodes are upgraded, crash, or experience a certain level of network partition. | High | Test | AM-014 |
| NFR-023 | Maintainability | Code shall be readable. | Code follows naming conventions, and names correspond to actual meaning. | Medium | Inspection | AM-005 |
| NFR-024 | Maintainability | Code shall avoid excessive coupling. | Code supports later iterative optimization, extension of existing functions, and addition of new functions. | Medium | Inspection | AM-005 |
| NFR-025 | Load Balancing | The system shall maintain stable response and reasonable resource utilization under high access volume. | Load balancing technology is provided when user access volume is high. | High | Test | AM-005 |

## 6. Data Requirements

| ID | Data Object | Requirement | Rationale / Constraint | Verification | Source |
| --- | --- | --- | --- | --- | --- |
| DR-001 | User account | The system shall save username, password, email, and login account name. | Support registration and login; username must be non-duplicated and non-empty, and password and email must be non-empty. | Test | AM-008 |
| DR-002 | Score favorite record | The system shall save user fields and favorited score ID fields. | Support favoriting and canceling score favorites. | Test | AM-008 |
| DR-003 | Follow relationship | The system shall save user fields and followed user fields. | Support following and unfollowing users. | Test | AM-008 |
| DR-004 | Score data | The system shall save scores uploaded and generated by users. | Support upload, favorites, download, search, and hot charts. | Test | AM-008 |
| DR-005 | Model favorite record | The system shall save user fields and favorited model ID fields. | Support favoriting and managing model lists. | Test | AM-008 |
| DR-006 | Recommendation input data | The system shall save or read user favorite score information and followed user information. | Support recommendation retrieval and song recommendation algorithm. | Test | AM-008, AM-009 |
| DR-007 | Search input | The system shall process song names entered by users. | Support score search by name. | Test | AM-008 |
| DR-008 | Midi music | The system shall process midi songs no longer than 4 minutes. | Support training, generation, classification, and recommendation algorithms. | Test | AM-009 |
| DR-009 | Abc score | The system shall convert midi to abc format and process abc scores. | Support track seed extraction, score concatenation, and midi output. | Test | AM-002, AM-009 |
| DR-010 | Track seed | The system shall select 5 track seeds from an abc score. | Support algorithmic score generation. | Test | AM-003, AM-009 |
| DR-011 | User generation model parameters | The system shall save each user's own GPT-2 score generation model parameters. | Support daily update and personalized generation. | Test | AM-009 |
| DR-012 | LSTM score representation | The system shall generate and use score representations. | Support classification of all scores and song recommendation. | Test | AM-009 |
| DR-013 | Score label | The system shall save score classification labels. | Support score classification and recommendation. | Test | AM-009 |
| DR-014 | Task metadata | The scheduling system shall save metadata such as training model IDs, score IDs to be classified, recommendation user IDs, generation source material IDs, and model IDs. | Support task queue scheduling. | Test | AM-010 |
| DR-015 | Task status and logs | The system shall record task status, queue write errors, status retrieval errors, and retry logs. | Support reliable execution of scheduled tasks and issue tracking. | Inspection | AM-010 |
| DR-016 | Hot-chart data | The system shall save score attention level and user popularity data. | Support updating score and user hot charts. | Test | AM-003 |

## 7. Constraints

| ID | Constraint | Evidence Type | Source |
| --- | --- | --- | --- |
| C-001 | Frontend languages are HTML, CSS, and JavaScript; the frontend framework is Bootstrap. | explicit | AM-005 |
| C-002 | Backend language is Golang; backend framework is Gin. | explicit | AM-005 |
| C-003 | Webpage response time shall be within 1 second. | explicit | AM-005 |
| C-004 | Music generation model training time shall be within 2 hours. | explicit | AM-005 |
| C-005 | The algorithm model shall be able to generate enough varieties of music styles. | explicit | AM-005 |
| C-006 | Generated music quality shall be above the baseline. | explicit | AM-005 |
| C-007 | Algorithm model response time shall be controlled within 1 minute. | explicit | AM-005 |
| C-008 | Product interfaces shall reflect user friendliness and have a certain degree of aesthetics. | explicit | AM-005 |
| C-009 | Project R&D shall strictly follow the project management process to avoid phase delays affecting later development. | explicit | AM-005 |
| C-010 | System hardware environment consists of 4 virtual machines, each with CPU 4 * 2400MHz, 8GB memory, and 200GB storage. | explicit | AM-007 |
| C-011 | System software environment includes Ubuntu 18.04 LTS, Hadoop 3.2.2, RabbitMQ 3.8.14, etcd 3.4.15, and Nginx 1.19.8. | explicit | AM-007 |
| C-012 | Communication protocols are HTTPS and TCP/IP. | explicit | AM-007 |
| C-013 | Task metadata must conform to database constraints and limit task size. | explicit | AM-010 |
| C-014 | When task submission fails, erroneous data needs to be automatically skipped and retried. | explicit | AM-010 |
| C-015 | All requirements listed in use-case diagrams are planned for the current version and do not need to be assigned to future versions. | explicit | AM-006 |

## 8. Verification and Acceptance

| ID | Verification | Acceptance Criterion |
| --- | --- | --- |
| FR-001 | Test | A user can register successfully; duplicated username, empty fields, or invalid information produces a prompt. |
| FR-002 | Test | A registered user can log in; non-existent account, wrong login information, or busy system produces a prompt. |
| FR-003 | Test | A user can favorite and unfavorite scores, and favorites records update. |
| FR-004 | Test | A user can follow and unfollow users, and the follow list and button state update. |
| FR-005 | Test | A user can select a model and original music to generate a score and see the result. |
| FR-006 | Test | A user can upload a generated score and update the database. |
| FR-007 | Test | A user can favorite another user's model and manage the user's own model list. |
| FR-008 | Test | A user can view the system-recommended music list. |
| FR-009 | Test | A user can obtain search results by entering a song name; results may be empty. |
| FR-010 | Test | A user can view hot song and creator lists. |
| FR-011 | Test | A user can download a score locally. |
| FR-012 | Test | The algorithm can update user generation model parameters according to the user's playlist. |
| FR-013 | Test | The algorithm can generate reasonable midi songs and handle conversion exceptions through the fallback flow. |
| FR-014 | Test | The algorithm can return score labels. |
| FR-015 | Test | The algorithm can generate recommendation lists for each user and recommend randomly when no playlist exists. |
| FR-016 | Test | The daily 02:00 training task is queued and task status can be polled; exceptions are logged and retried. |
| FR-017 | Test | After a user submits a generation task, the task is queued and status can be polled; exceptions are logged and retried. |
| FR-018 | Test | Score hot charts and user hot charts update when users access the product. |
| NFR-001 | Test | Average account registration latency <= 200ms. |
| NFR-002 | Test | Average account login latency <= 200ms. |
| NFR-003 | Test | Average score favorite latency <= 200ms. |
| NFR-004 | Test | Average follow-user latency <= 200ms. |
| NFR-005 | Test | Average score upload latency <= 3000ms. |
| NFR-006 | Test | Average model favorite latency <= 200ms. |
| NFR-007 | Test | Average Web-side score generation latency <= 200ms. |
| NFR-008 | Test | Average score download latency <= 3000ms. |
| NFR-009 | Test | Average recommendation retrieval latency <= 500ms. |
| NFR-010 | Test | Average score search latency <= 1000ms. |
| NFR-011 | Test | Average hot-chart viewing latency <= 200ms. |
| NFR-012 | Test | Generation model training runs once per day and average latency <= 1.5h. |
| NFR-013 | Test | Algorithm score generation throughput is 5ops and average latency <= 1min. |
| NFR-014 | Test | Classifying all scores runs once per day and average latency <= 1.5h. |
| NFR-015 | Test | Song recommendation runs once per day and average latency <= 1.5h. |
| NFR-016 | Test | Concurrent access throughput is no less than 2000QPS. |
| NFR-017 | Test | Transaction changes are no less than 100TPS. |
| NFR-018 | Demonstration | Beginners can understand core flows and complete basic operations. |
| NFR-019 | Inspection | Instructions, prompts, and guidance exist. |
| NFR-020 | Inspection | Gateway isolates internal and external network boundaries. |
| NFR-021 | Inspection | Important data uses 3-replica storage. |
| NFR-022 | Test | Core system functions remain available during node upgrades, crashes, or network partitions. |
| NFR-023 | Inspection | Code naming is standardized and readable. |
| NFR-024 | Inspection | Code structure avoids excessive coupling. |
| NFR-025 | Test | Load balancing keeps response stable under high access volume. |
| DR-001 | Test | User account fields can be saved and validated. |
| DR-002 | Test | Score favorite records can be created and deleted. |
| DR-003 | Test | Follow relationships can be created and deleted. |
| DR-004 | Test | Score data can be saved, searched, downloaded, and displayed. |
| DR-005 | Test | Model favorite records can be saved and managed. |
| DR-006 | Test | Recommendation input data can be used to generate recommendations. |
| DR-007 | Test | Song name input can be used for search. |
| DR-008 | Test | Midi music no longer than 4 minutes can be processed. |
| DR-009 | Test | The midi and abc score conversion flow is available. |
| DR-010 | Test | Five track seeds can be selected. |
| DR-011 | Test | User GPT-2 model parameters can be saved and updated. |
| DR-012 | Test | LSTM score representations can be generated and used for similarity calculation. |
| DR-013 | Test | Score labels can be generated and saved. |
| DR-014 | Test | Task metadata conforms to database constraints and can be queued. |
| DR-015 | Inspection | Task status and exception logs can be queried. |
| DR-016 | Test | Hot-chart data can be saved and updated. |
| C-001 | Inspection | Frontend technology stack conforms to constraints. |
| C-002 | Inspection | Backend technology stack conforms to constraints. |
| C-003 | Test | Webpage response time <= 1s. |
| C-004 | Test | Model training time <= 2h. |
| C-005 | Analysis | The model covers enough music styles. |
| C-006 | Inspection | Generated music quality reaches the baseline. |
| C-007 | Test | Algorithm model response time <= 1min. |
| C-008 | Inspection | The interface is user-friendly and visually pleasing. |
| C-009 | Inspection | The project plan follows the management process. |
| C-010 | Inspection | Virtual machine hardware configuration conforms to constraints. |
| C-011 | Inspection | Software environment versions conform to constraints. |
| C-012 | Inspection | Communication protocols conform to constraints. |
| C-013 | Test | Task metadata conforms to database constraints and task size is limited. |
| C-014 | Test | When task submission fails, erroneous data is skipped and retried. |
| C-015 | Inspection | Current version implementation scope covers use-case diagram requirements. |

## 9. Traceability Matrix

| ID | Requirement | Type | Source | Evidence Type | Verification | Confidence |
| --- | --- | --- | --- | --- | --- | --- |
| FR-001 | Register account | Functional | AM-008 | explicit | Test | High |
| FR-002 | Login account | Functional | AM-008 | explicit | Test | High |
| FR-003 | Favorite score | Functional | AM-008 | explicit | Test | High |
| FR-004 | Follow user | Functional | AM-008 | explicit | Test | High |
| FR-005 | Web-side score generation | Functional | AM-008 | explicit | Test | High |
| FR-006 | Upload score | Functional | AM-008 | explicit | Test | High |
| FR-007 | Favorite model | Functional | AM-008 | explicit | Test | High |
| FR-008 | Obtain recommendation | Functional | AM-008 | explicit | Test | High |
| FR-009 | Search score | Functional | AM-008 | explicit | Test | High |
| FR-010 | View hot chart | Functional | AM-008 | explicit | Test | High |
| FR-011 | Download score | Functional | AM-008 | explicit | Test | High |
| FR-012 | Train generation model | Functional | AM-009 | explicit | Test | High |
| FR-013 | Algorithm score generation | Functional | AM-009 | explicit | Test | High |
| FR-014 | Classify all scores | Functional | AM-009 | explicit | Test | High |
| FR-015 | Recommend songs | Functional | AM-009 | explicit | Test | High |
| FR-016 | Trigger training task | Functional | AM-010 | explicit | Test | High |
| FR-017 | Trigger generation task | Functional | AM-010 | explicit | Test | High |
| FR-018 | Update hot charts | Functional | AM-003 | explicit | Test | Medium |
| NFR-001 | Registration latency | Non-functional | AM-011 | explicit | Test | High |
| NFR-002 | Login latency | Non-functional | AM-011 | explicit | Test | High |
| NFR-003 | Score favorite latency | Non-functional | AM-011 | explicit | Test | High |
| NFR-004 | Follow-user latency | Non-functional | AM-011 | explicit | Test | High |
| NFR-005 | Score upload latency | Non-functional | AM-011 | explicit | Test | High |
| NFR-006 | Model favorite latency | Non-functional | AM-011 | explicit | Test | High |
| NFR-007 | Web-side score generation latency | Non-functional | AM-011 | explicit | Test | High |
| NFR-008 | Score download latency | Non-functional | AM-011 | explicit | Test | High |
| NFR-009 | Recommendation retrieval latency | Non-functional | AM-011 | explicit | Test | High |
| NFR-010 | Score search latency | Non-functional | AM-011 | explicit | Test | High |
| NFR-011 | Hot-chart viewing latency | Non-functional | AM-011 | explicit | Test | High |
| NFR-012 | Generation model training performance | Non-functional | AM-011 | explicit | Test | High |
| NFR-013 | Algorithm score generation performance | Non-functional | AM-011 | explicit | Test | High |
| NFR-014 | Classifying all scores performance | Non-functional | AM-011 | explicit | Test | High |
| NFR-015 | Song recommendation performance | Non-functional | AM-011 | explicit | Test | High |
| NFR-016 | Concurrent access throughput | Non-functional | AM-011 | explicit | Test | High |
| NFR-017 | Transaction change throughput | Non-functional | AM-011 | explicit | Test | High |
| NFR-018 | Interaction usability | Non-functional | AM-012 | explicit | Demonstration | High |
| NFR-019 | User guidance | Non-functional | AM-012 | explicit | Inspection | High |
| NFR-020 | Gateway isolation | Non-functional | AM-013 | explicit | Inspection | High |
| NFR-021 | Three-replica storage | Non-functional | AM-013 | explicit | Inspection | High |
| NFR-022 | Partial-failure availability | Non-functional | AM-014 | explicit | Test | High |
| NFR-023 | Code readability | Non-functional | AM-005 | explicit | Inspection | High |
| NFR-024 | Code robustness | Non-functional | AM-005 | explicit | Inspection | High |
| NFR-025 | Load balancing | Non-functional | AM-005 | explicit | Test | High |
| DR-001 | User account data | Data | AM-008 | explicit | Test | High |
| DR-002 | Score favorite record | Data | AM-008 | explicit | Test | High |
| DR-003 | Follow relationship | Data | AM-008 | explicit | Test | High |
| DR-004 | Score data | Data | AM-008 | explicit | Test | High |
| DR-005 | Model favorite record | Data | AM-008 | explicit | Test | High |
| DR-006 | Recommendation input data | Data | AM-008, AM-009 | explicit | Test | High |
| DR-007 | Search input | Data | AM-008 | explicit | Test | High |
| DR-008 | Midi music | Data | AM-009 | explicit | Test | High |
| DR-009 | Abc score | Data | AM-002, AM-009 | explicit | Test | High |
| DR-010 | Track seed | Data | AM-003, AM-009 | explicit | Test | High |
| DR-011 | User generation model parameters | Data | AM-009 | explicit | Test | High |
| DR-012 | LSTM score representation | Data | AM-009 | explicit | Test | High |
| DR-013 | Score label | Data | AM-009 | explicit | Test | High |
| DR-014 | Task metadata | Data | AM-010 | explicit | Test | High |
| DR-015 | Task status and logs | Data | AM-010 | explicit | Inspection | High |
| DR-016 | Hot-chart data | Data | AM-003 | explicit | Test | Medium |
| C-001 | Frontend technology stack | Constraint | AM-005 | explicit | Inspection | High |
| C-002 | Backend technology stack | Constraint | AM-005 | explicit | Inspection | High |
| C-003 | Webpage response time | Constraint | AM-005 | explicit | Test | High |
| C-004 | Model training time | Constraint | AM-005 | explicit | Test | High |
| C-005 | Music style coverage | Constraint | AM-005 | explicit | Analysis | High |
| C-006 | Generated music quality | Constraint | AM-005 | explicit | Inspection | High |
| C-007 | Algorithm model response time | Constraint | AM-005 | explicit | Test | High |
| C-008 | Interface friendliness | Constraint | AM-005 | explicit | Inspection | High |
| C-009 | Project management process | Constraint | AM-005 | explicit | Inspection | High |
| C-010 | Hardware environment | Constraint | AM-007 | explicit | Inspection | High |
| C-011 | Software environment | Constraint | AM-007 | explicit | Inspection | High |
| C-012 | Communication protocol | Constraint | AM-007 | explicit | Inspection | High |
| C-013 | Task metadata constraints | Constraint | AM-010 | explicit | Test | High |
| C-014 | Task failure retry | Constraint | AM-010 | explicit | Test | High |
| C-015 | Current version scope | Constraint | AM-006 | explicit | Inspection | High |
