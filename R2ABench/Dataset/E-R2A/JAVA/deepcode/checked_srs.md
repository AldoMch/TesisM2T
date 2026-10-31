# DeepCode Software Requirements Specification (Standard SRS Extract)

## 1. Introduction

### Purpose
The goal is to provide structured input for DeepCode architecture generation, test design, and requirements tracing.

### Product Scope

DeepCode is an AI-assisted online programming platform based on large language models. It provides algorithm learning, code writing, code judging, problem creation, solution publication, forum discussion, and AI-assisted learning capabilities for students, algorithm enthusiasts, and programmers. The system integrates a secure judging mechanism, a communication and learning platform, and large language model interfaces.

This document uses the specification terminology for RUCM, Vue, Spring Boot, AI, LLM, UC, JudgeHost, JudgeCore, problems, solutions, discussions, submission records, and user roles.

### Intended Audience

This document is intended for DeepCode developers, testers, administrators, requirements reviewers, and later architecture generation and acceptance testing workflows. Target end users include students, algorithm enthusiasts, programmers, unregistered visitors, registered users, and administrators.

## 2. Overall Description

### Product Perspective

DeepCode uses a front-end and back-end separated architecture. The front end is based on Vue 3 and interacts with the Spring Boot back end through RESTful APIs. From front end to back end, the system is divided into a front-end layer, presentation layer, proxy layer, business layer, and access layer. Back-end business is divided into modules such as users, problems, solutions, and forum, and is supported by SMTP, LangChain4j, HTTP judging services, MySQL, Redis, MinIO, and Swagger.

### Product Functions Summary

| Capability | Summary |
| --- | --- |
| Users and permissions | Supports registration, login, querying and modifying personal information and activity status, and administrator banning, unbanning, and permission granting. |
| Problem bank and judging | Supports problem browsing, solution access, code submission, judging, submission record viewing, problem upload, and review. |
| Problem and solution management | Authorized users can edit problems and solutions; administrators or authorized users can soft-delete problems and hide related content. |
| Forum interaction | Supports browsing, posting, comments, likes, replies, reporting, draft saving, and content deletion. |
| AI-assisted learning | Supports AI problem recommendation, problem analysis, code explanation, problem review suggestions, and @AI forum replies. |
| Platform operations | Supports security authentication, input validation, sandbox isolation, monitoring and alerting, backup, CI/CD, container deployment, and rollback. |

### User Classes

| User Class | Responsibilities / Needs |
| --- | --- |
| Unregistered user / visitor | Can browse problems and public forum posts; cannot browse solutions, submit code for judging, publish content, or interact. |
| Registered user | Can submit code for judging, view solutions, publish problems and solutions, interact with AI, participate in forum discussions, and view or modify personal information. |
| Administrator | Has all registered-user functions and can perform user management, problem review, forum content management, and problem management. |
| AI service | External or integrated large language model capability used for problem recommendation, problem analysis, code explanation, assisted review, and forum replies. |
| Judging service | Code judging subsystem composed of JudgeHost and JudgeCore, responsible for scheduling judging tasks, executing code, limiting resources, and returning results. |

### Operating Environment

| Environment | Requirement |
| --- | --- |
| General hardware | CPU with at least 8 cores and frequency above 2.4 GHz; at least 32 GB memory; at least 4 TB disk; network bandwidth at gigabit level or above. |
| Operating system | Supports Windows, Linux, and other mainstream operating systems; production, development, and test deployments use Ubuntu 22.04 LTS. |
| Browser | Microsoft Edge, Chrome, Opera, Safari, Firefox, and any browser supporting the HTML5 standard. |
| Production environment | One cloud server integrates Web, application, database, and cache, configured with at least 8 CPU cores, 32 GB memory, and 4 TB disk. |
| Development and test environment | Virtual machine or cloud host with at least 2 CPU cores, 8 GB memory, and 200 GB disk. |
| Supporting software | JDK 21-LTS, MySQL 5.7.44, Redis 7.4.6, Node.js 18.3 or later, Spring Boot 3.1.2, and Apache JMeter 5.6.13. |

### Assumptions and Dependencies

| ID | Assumption / Dependency |
| --- | --- |
| AD-001 | DeepCode browser-side capabilities depend on modern browsers that support HTML5. |
| AD-002 | Solution viewing, code submission, forum posting and interaction, problem upload, editing, and deletion all depend on user login state and permission validation. |
| AD-003 | AI recommendation, analysis, explanation, assisted review, and @AI replies depend on availability of the LLM service. |
| AD-004 | Code judging depends on JudgeHost, JudgeCore, test case files in object storage, and allocatable thread and queue capacity. |
| AD-005 | The specification does not specify concrete API paths, request/response schemas, LLM provider, or the set of judging languages; later design must not assume these details are determined. |

## 3. External Interface Requirements

### User Interfaces

| Interface | Requirement |
| --- | --- |
| Registration/login interface | Supports visitor account registration, user login, and error prompts. |
| User home/profile center | Supports personal information, activity status, submission record queries, and profile editing. |
| Problem list and problem detail interface | Supports problem browsing, problem information display, solution entry, submission record display, and code submission entry. |
| Problem management/review interface | Supports problem upload, pending problem viewing, approval/rejection, and problem/solution editing and deletion. |
| Forum home/post detail interface | Supports post lists, post body, comments, posting, comments, likes, replies, reports, and deletion. |
| AI assistance interface | Supports AI problem recommendation, AI problem analysis, AI code explanation, AI-assisted review, and @AI reply triggering. |
| Administration console | Supports user banning, unbanning, permission granting, problem review, forum content management, and problem management. |

### Software/API Interfaces

| Interface | Requirement |
| --- | --- |
| RESTful API | The front end shall interact with the back end through RESTful APIs. |
| Authentication interface | The back end shall perform permission authentication through filters and use JWT or OAuth 2.0/JWT for identity authentication. |
| Judging service interface | The back end shall call the judging service through HTTP requests, send code to the judging server, and receive judging results. |
| LLM service interface | The back end shall call the LLM service through LangChain4j to support recommendation, analysis, explanation, review suggestions, and forum replies. |
| SMTP mail service | The back end shall provide email service through SMTP. |
| Data storage interfaces | The back end shall use MySQL to store business data, Redis to cache temporary and high-frequency data, and MinIO to store images, test cases, and other files. |
| API documentation | During development, Swagger shall be used to manage API documentation and support front-end/back-end debugging. |

### Communication Interfaces

External communication must use HTTPS. Internal services communicate through intranet IP addresses and are restricted by firewalls; static resources are distributed through CDN; DNS is used for domain name resolution. The specification does not specify complete API routes, load balancing strategy, or messaging protocol.

### Data Exchange Formats

The system needs to exchange username, email, password, nickname, avatar URL, personal profile, user state/permissions, problem ID, problem title, description, difficulty, tags, test samples, solution content, code content, user ID, submission language, submission time, run result, elapsed time, memory, forum posts, comments, likes, reports, AI prompt context, AI analysis results, and review suggestions. The specification does not specify JSON schemas, error code tables, API versioning strategy, or authentication token field format.

## 4. Functional Requirements

| ID | Requirement | Trigger / Input | System Behavior | Output | Priority | Verification |
| --- | --- | --- | --- | --- | --- | --- |
| FR-001 | The system shall allow visitors to register accounts. | A visitor clicks registration on the login page and fills in username, email, password longer than 8 characters, and other information. | The front end validates the password format, the back end checks username uniqueness, generates a unique user identifier, and stores it in the user database; on exception it displays the corresponding warning. | Registration success prompt and return to login page, or format/username error prompt. | High | Test |
| FR-002 | The system shall allow users to log in. | A user enters username and password on the login page and clicks login. | The back end verifies that the username exists and the password is correct, then returns login success state; on error it prompts the user to re-enter information. | Login state and user home page redirect, or login error prompt. | High | Test |
| FR-003 | The system shall allow registered users to query personal information and activity status. | A logged-in user enters the personal home page or clicks refresh. | The back end validates login state, queries the user database for personal information and activity status such as comment count, solution count, and accepted problem count; if login state is invalid, it clears the state and returns to the home page. | Personal information, activity status, or login invalidation prompt. | Medium | Test |
| FR-004 | The system shall allow registered users to edit personal information. | A user clicks edit on the personal home page, modifies nickname, avatar URL, and personal profile, and submits. | The back end validates login state, updates the user database, and refreshes the display with the latest data. | Modification success prompt and latest personal information. | Medium | Test |
| FR-005 | The system shall allow administrators to manage user permissions and status. | An administrator selects a target user and a ban, unban, or permission-granting operation in the user management module. | The back end validates administrator permissions and operation legality, and updates status/permission fields such as `is_admin` or `disabled` in the user database. | Operation success prompt or illegal operation error prompt. | High | Test |
| FR-006 | The system shall allow users to view problem details, solutions, and submission records. | A user clicks a problem in the problem list. | The front end sends the problem ID and login state; the back end queries problem title, description, difficulty, tags, and solution list; for logged-in users it also attaches submission records for the problem; when an unauthenticated user clicks a solution, it prompts login. | Problem details, solution list, submission records, or error prompt. | High | Test |
| FR-007 | The system shall allow logged-in users to submit code for judging. | A logged-in user uploads code content on the problem page and submits problem ID, code, and user ID. | The back end validates problem existence and login state, sends the code to the judging server, and records submission time, language, and code snippet. | Submission record and later judging result entry. | High | Test |
| FR-008 | The judging service shall execute code judging and return results. | JudgeHost receives a judging request. | JudgeHost allocates a thread or queues the task, returns service busy when the queue is full, obtains test case files, calls JudgeCore to compile and execute code, compares actual output with expected output, and packages the result. | Judging result, service busy prompt, or runtime error state. | High | Test |
| FR-009 | JudgeCore shall execute user code in a restricted environment. | JudgeCore receives parameters such as code file path, input file path, runtime limit, memory limit, and output limit. | JudgeCore validates parameters, creates a child process to execute code, sets runtime, memory, and output limits, redirects standard input/output/error, and uses seccomp to restrict prohibited system calls. | Run result, resource usage data, or restriction/validation error. | High | Test |
| FR-010 | The system shall allow registered users to upload problems and enter the review process. | A registered user clicks problem upload, fills in title, description, test samples, and other information, and submits. | The system submits problem information to the back end and stores it in the pending problem bank; unauthenticated users must log in first. | Pending problem record or login prompt. | High | Test |
| FR-011 | The system shall allow administrators to review problems. | An administrator enters the review interface, views pending problems, and chooses approve or reject. | On approval, the problem state is updated to reviewed and opened to users; on rejection, the reason is recorded and the submitter is notified; if the problem is withdrawn, the process terminates. | Review state, rejection reason notification, or process termination prompt. | High | Test |
| FR-012 | The system shall allow authorized users to edit problems and solutions. | A problem author, administrator, or user with editing permission enters the management interface and submits modified content. | The back end validates editing permission and content format and updates the database; if locked or unauthorized, it displays an error prompt. | Updated problem/solution or error prompt. | Medium | Test |
| FR-013 | The system shall allow administrators or authorized users to delete problems. | An administrator or authorized user selects a target problem and clicks delete. | The back end validates permissions and associated activities; when allowed, it soft-deletes the problem and hides related solutions and submission records; when associated activities exist or permission is absent, it prohibits the operation. | Soft deletion result or deletion-denied prompt. | Medium | Test |
| FR-014 | The system shall allow users to browse forum posts. | A user enters the forum home page or a board, or clicks a specific post. | The front end requests the post list and loads the post body and comments. | Post list, post body, and comments. | Medium | Test |
| FR-015 | The system shall allow logged-in users to publish forum posts. | A logged-in user clicks publish post and fills in title and content. | The back end validates format and content length, stores the post in the database after validation, and redirects to the post detail page; when format is wrong or content is too long, it prompts modification. | New post detail page or modification prompt. | Medium | Test |
| FR-016 | The system shall allow users to publish comments and perform comment interactions. | A user enters content in the comment area or selects like, reply, or report. | The back end checks comment sensitive words and length; after validation it stores the comment in the comment table and associates it with the post ID; likes are logged and counted, replies generate child comments, reports trigger the review process, and drafts are saved on network interruption. | Comment, like count, child comment, report process, or draft recovery. | Medium | Test |
| FR-017 | The system shall allow authors or administrators to delete forum content. | A post author, comment author, post author, or administrator selects a post/comment and confirms deletion. | The back end validates deletion permission and soft-deletes the post and associated comments/interactions, or soft-deletes the comment and child replies. | Refreshed page, updated comment area, or unauthorized prompt. | Medium | Test |
| FR-018 | The system shall support AI problem recommendation. | A user clicks intelligent problem recommendation. | The system checks the number of completed problems; if at least 5 problems have been completed, it analyzes historical behavior and knowledge points, otherwise it returns beginner recommendations; it calls the AI interface to generate recommended difficulty and tags and retrieves matching problems. | Recommended problem list or AI service exception prompt. | Medium | Test |
| FR-019 | The system shall support AI problem analysis and code explanation. | A user clicks AI analysis on the problem detail page or AI explanation on the submission record page. | The system extracts problem content or code snippets, concatenates a prompt, and calls AI; after returning analysis it stores and displays the result, and directly retrieves existing historical analysis when available. | Solution ideas, code logic explanation, or AI service exception prompt. | Medium | Test |
| FR-020 | The system shall support AI-assisted review and forum @AI replies. | An administrator clicks AI-assisted review, or a user enters @AI in a comment. | The system sends problem content to AI to generate review suggestions; @AI replies must check that the cooldown time is at least 10 minutes, extract post context, call AI, and publish a comment with the @AI account. | Review suggestion, AI reply, or retry-later prompt. | Medium | Test |

## 5. Non-Functional Requirements

| ID | Quality | Requirement | Metric / Acceptance | Priority | Verification |
| --- | --- | --- | --- | --- | --- |
| NFR-001 | Security | The system shall enforce HTTPS for all external communication. | All external entrances are accessed through HTTPS. | High | Inspection |
| NFR-002 | Security | The system shall use OAuth 2.0 or JWT for user identity authentication. | Protected interfaces require valid authentication credentials. | High | Test |
| NFR-003 | Security | The system shall perform permission authentication in back-end filters. | Login state and permission validation are completed before requests enter the business layer. | High | Test |
| NFR-004 | Security | The system shall strictly validate user-submitted data. | Front end and back end jointly validate password length, image size, sensitive words, and other inputs; SQL injection and XSS attacks are prevented. | High | Test |
| NFR-005 | Security | The system shall execute code judging in independent Docker containers and limit resources. | Judging processes are limited by CPU time, memory size, and other resources. | High | Test |
| NFR-006 | Security | JudgeCore shall restrict prohibited system calls from user code. | seccomp is used to restrict prohibited system calls. | High | Test |
| NFR-007 | Security | The system shall expose only necessary ports. | Firewall rules restrict access to unnecessary ports. | High | Inspection |
| NFR-008 | Privacy / Integrity | The system shall store sensitive information such as passwords in encrypted form. | Passwords and other sensitive information are not stored in plaintext in the database. | High | Inspection |
| NFR-009 | Reliability | The system shall execute transaction rollback when database operations fail. | Database operation failures in common processes trigger transaction rollback. | High | Test |
| NFR-010 | Reliability | The system shall handle exceptions when calling external AI services. | On network timeout or service unavailability, the system prompts users to retry and records logs. | Medium | Test |
| NFR-011 | Reliability | The system shall back up the database daily and store backups offsite. | Database backups are executed daily and backup copies are stored offsite. | High | Inspection |
| NFR-012 | Performance | The system shall distribute client requests through an Nginx reverse proxy. | Client requests are reverse-proxied by Nginx to back-end servers. | Medium | Inspection |
| NFR-013 | Performance | The system shall distribute static resources through CDN. | Images, CSS, and JS files are distributed through CDN. | Medium | Inspection |
| NFR-014 | Performance | Judging tasks shall enter a waiting queue when threads are insufficient, and return service busy when the queue is full. | When no available thread exists and the queue is not full, tasks are queued; when the queue is full, new tasks are not accepted and a busy prompt is returned. | High | Test |
| NFR-015 | Observability | The system shall collect infrastructure, application, and database monitoring metrics. | CPU, memory, disk I/O, interface response time, error rate, QPS, database query latency, and connection count are collected. | High | Inspection |
| NFR-016 | Observability | The system shall trigger alerts according to explicit thresholds. | Alerts are triggered when CPU or memory usage exceeds 80%, interface error rate exceeds 1%, or database query latency exceeds 15 seconds. | High | Test |
| NFR-017 | Observability | The system shall use specified monitoring and alerting tools. | Prometheus is used for collection, Grafana for display, and PagerDuty or DingTalk robot for alert delivery. | Medium | Inspection |
| NFR-018 | Maintainability | Database tables and fields shall use standardized names and keep meanings explicit. | Table names and field names are readable and semantically clear. | Medium | Inspection |
| NFR-019 | Data Integrity | Explicit relationships and foreign key constraints shall be set between database tables. | Related tables have foreign key constraints to ensure data consistency. | High | Inspection |
| NFR-020 | Performance / Data | The system shall reasonably design indexes according to business needs to improve query performance. | Appropriate indexes are created on key query fields. | Medium | Analysis |
| NFR-021 | Maintainability | Database design shall follow third normal form and make explainable redundancy tradeoffs when query efficiency requires it. | The data model reduces unnecessary redundancy, and redundant fields have query-performance justification. | Medium | Analysis |
| NFR-022 | Deployability | The system shall support automated build, containerized deployment, automatic scaling, and fast rollback. | GitLab CI/CD builds Docker images, pushes them to a private registry, and deploys, scales, and rolls back through Kubernetes. | Medium | Demonstration |

## 6. Data Requirements

| ID | Data Entity / Object | Requirement |
| --- | --- | --- |
| DR-001 | User | The system shall store user and administrator information, including id, email, password, nickname, avatar, is_admin, and description. |
| DR-002 | Follow | The system shall store user follow relationships, including follower, followed user, and follow date. |
| DR-003 | Question | The system shall store problem information, including title, content, difficulty, and deletion state. |
| DR-004 | TestCase | The system shall store problem test cases, including problem ID, input file URL, and expected output file URL. |
| DR-005 | QuestionTag / QuestionTagMap | The system shall store problem tags and mapping relationships between problems and tags. |
| DR-006 | Record | The system shall store code submission records, including user, problem, language, code, result, runtime, memory, submission time, additional information, total number of test cases, and number passed. |
| DR-007 | Language | The system shall store names of supported programming languages. |
| DR-008 | Solution | The system shall store solutions, including associated problem, author, title, content, likes, views, creation time, and deletion state. |
| DR-009 | SolutionTag / SolutionTagMap | The system shall store solution tags and mapping relationships between solutions and tags. |
| DR-010 | SolutionLike / SolutionComment | The system shall store solution likes and comments. |
| DR-011 | Discussion | The system shall store discussion posts, including user, title, content, views, creation time, and deletion state. |
| DR-012 | DiscussionLike / DiscussionComment | The system shall store discussion likes and comments. |
| DR-013 | Object Storage Files | The system shall store images, test cases, and other files, and object storage shall be provided by MinIO. |
| DR-014 | AI Results | The system shall store AI problem analysis and code explanation results so existing historical analyses can be retrieved directly. |
| DR-015 | Monitoring Data | The system shall store or collect monitoring data, including infrastructure, application, and database metrics. |

## 7. Constraints

| ID | Constraint |
| --- | --- |
| C-001 | The front end shall use technologies such as Vue 3, TypeScript, Vuex, vue-router, Ant Design Vue, CodeMirror, wangEditor, ECharts, Axios, Webpack, Vue CLI, and ESLint. |
| C-002 | The back end shall use technologies such as Spring Boot 3.1.2, JDK 21-LTS, Lombok, MyBatis-Plus, Swagger, JWT, SMTP, Interceptor, WebFlux, and thread pools. |
| C-003 | Data storage shall use MySQL 5.7.44, Redis 7.4.6, and MinIO. |
| C-004 | Front-end and back-end interaction shall use RESTful APIs. |
| C-005 | The judging service shall consist of JudgeHost and JudgeCore and be called by the back end through HTTP requests. |
| C-006 | Browser clients shall support HTML5 and be compatible with Microsoft Edge, Chrome, Opera, Safari, and Firefox. |
| C-007 | The production server shall use Ubuntu 22.04 LTS, at least 8 CPU cores, at least 32 GB memory, and at least 4 TB disk. |
| C-008 | The development and test environment shall use Ubuntu 22.04 LTS, at least 2 CPU cores, at least 8 GB memory, and at least 200 GB disk. |
| C-009 | Internal services shall communicate through intranet IP addresses and be restricted by firewalls. |
| C-010 | Static resources shall be distributed through CDN, and domain name resolution shall use DNS services. |
| C-011 | The deployment process shall use GitLab CI/CD, Docker, a private image registry, and Kubernetes. |
| C-012 | Performance testing or stress testing tools include Apache JMeter 5.6.13. |

## 8. Verification and Acceptance

| Verification Method | Applicable Requirement IDs | Acceptance Basis |
| --- | --- | --- |
| Test | FR-001 to FR-020; NFR-002, NFR-003, NFR-004, NFR-005, NFR-006, NFR-009, NFR-010, NFR-014, NFR-016 | Execute functional flows, authentication and authorization, input validation, judging, AI exception handling, transaction rollback, queue busy handling, and alert threshold tests; results satisfy corresponding outputs and metrics. |
| Inspection | NFR-001, NFR-007, NFR-008, NFR-011, NFR-012, NFR-013, NFR-015, NFR-017, NFR-018, NFR-019; DR-001 to DR-015; C-001 to C-012 | Inspect whether design documents, configuration, database schema, API documentation, deployment configuration, monitoring configuration, backup strategy, and technical constraints cover requirements. |
| Analysis | NFR-020, NFR-021 | Confirm data quality and performance goals through analysis of database index design, query paths, normal forms, and redundancy tradeoffs. |
| Demonstration | NFR-022 | Demonstrate CI/CD build, image push, Kubernetes deployment, scaling, and rollback processes. |
