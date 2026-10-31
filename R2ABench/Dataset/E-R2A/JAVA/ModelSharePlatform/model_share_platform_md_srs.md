# Deep Learning Model Sharing Platform Software Requirements Specification (Standard SRS Extract)

## 1. Introduction

### Purpose

This document extracts verifiable requirements from `ModelSharePlatform_origin.md` and rewrites them according to the compact SRS standard in `architectural_views_rep-pkg/script/templates/SRS.md`. The goal is to provide structured input for architecture generation, test design, and requirements tracing for the Deep Learning Model Sharing Platform. Source evidence is recorded in `model_share_platform_md_evidence_pack.json`. (Source: MSP-001)

### Product Scope

The Deep Learning Model Sharing Platform targets deep learning enthusiasts and professionals, providing a one-stop cloud service for communication, learning, creation, and application of deep learning models. The platform supports a Q&A community, blog sharing, model library management, dataset management, online invocation experiences, paid model sales revenue, follow relationships, and administrator governance. (Source: MSP-002)

This document follows the source document terminology for general users, administrators, Q&A community, blogs, models, datasets, online invocation, paid sales, SQL, MySQL, TypeScript, UI, Spring Boot, and Vue. (Source: MSP-001, MSP-002)

### Intended Audience

This document is intended for platform general users, administrators, developers, testers, requirements reviewers, and later architecture generation and acceptance testing workflows. General users are the primary platform users, and administrators manage platform-related data. (Source: MSP-002)

### References

| Ref | Source |
| --- | --- |
| REF-001 | GB/T 9385-2008, Computer Software Requirements Specification |
| REF-002 | GB/T 19003-2008, Software Engineering |
| REF-003 | GB/T 8567-2006, Specification for Computer Software Documentation |
| REF-004 | MySQL, UML, Spring Boot, and Vue reference documentation |
| REF-005 | Practical Software Engineering Tutorial, Introduction to Database Systems, and Requirements Specification Writing Guide |

## 2. Overall Description

### Product Perspective

The platform references existing community product capabilities such as registration, login, personal information management, blog writing, resource sharing, and Q&A communication, and extends them with deep learning domain capabilities including model and dataset upload and sharing, online invocation of pretrained models, and paid transactions for model products. The source document does not provide a complete system architecture, API, database table structure, or deployment topology. (Source: MSP-002)

### Product Functions Summary

| Capability | Summary | Source |
| --- | --- | --- |
| Account management | Supports registration, login, password recovery, personal information modification, and account logout. | MSP-003 |
| Q&A community | Supports publishing, modifying, and deleting questions, and publishing, modifying, and deleting answers. | MSP-004 |
| Blog sharing | Supports publishing, modifying, and deleting blog articles, and publishing, modifying, and deleting blog comments. | MSP-005 |
| Model management | Supports model upload, review entry, download, deletion, modification, online invocation, recommendation, and purchase. | MSP-006 |
| Dataset management | Supports dataset upload, download, deletion, and modification. | MSP-007 |
| Follow management | Supports following users and unfollowing users. | MSP-008 |
| Administrator management | Supports account cancellation and deletion of illegal questions, answers, datasets, models, blogs, and blog comments. | MSP-009 |

### User Classes

| User Class | Responsibilities / Needs | Source |
| --- | --- | --- |
| General user | Uses platform Q&A, blogs, models, datasets, online invocation, purchase, follow, and personal account features; expects quick use of deep learning models. | MSP-002, MSP-003, MSP-004, MSP-005, MSP-006, MSP-007, MSP-008 |
| Administrator | Manages platform data such as user accounts, questions and answers, blogs and comments, datasets, and models. | MSP-002, MSP-009 |

### Operating Environment

| Environment | Requirement | Source |
| --- | --- | --- |
| CPU | x86-64 or ARM architecture. | MSP-011 |
| Memory | At least 4 GB. | MSP-011 |
| Disk | At least 30 GB of available space. | MSP-011 |
| Browser | All modern browsers. | MSP-011 |
| Unsupported Browser | Internet Explorer is not supported. | MSP-011 |

### Assumptions and Dependencies

| ID | Assumption / Dependency | Evidence Type | Source |
| --- | --- | --- | --- |
| AD-001 | Core capabilities such as models, datasets, Q&A, blogs, follows, and purchases depend on the general user being logged in. | explicit | MSP-003, MSP-004, MSP-005, MSP-006, MSP-007, MSP-008 |
| AD-002 | Administrator governance capabilities depend on the user being logged in as an administrator. | explicit | MSP-009 |
| AD-003 | Model recommendation depends on user browsing history and registration information. | explicit | MSP-006 |
| AD-004 | Dataset download, deletion, and similar operations depend on corresponding dataset information existing in the database. | explicit | MSP-007 |
| AD-005 | The source document does not define the model review process, payment channel, API schema, or database table structure; later design must not assume these details are complete. | explicit | MSP-006, MSP-007, MSP-009 |

## 3. External Interface Requirements

### User Interfaces

| Interface | Requirement | Source |
| --- | --- | --- |
| Account interface | Supports registration, login, password recovery, personal information modification, and account logout. | MSP-003 |
| Q&A community interface | Supports publishing, modifying, and deleting questions and answers, with save prompts and failure feedback. | MSP-004 |
| Blog interface | Supports publishing, modifying, and deleting blog articles and blog comments, with save prompts and failure feedback. | MSP-005 |
| Model interface | Supports model upload, purchased models, uploaded models, online running, recommendation model pool, and purchase/payment interface. | MSP-006 |
| Dataset interface | Supports dataset upload, free dataset download, and deletion and modification of personal datasets. | MSP-007 |
| Follow interface | Supports abbreviated user profiles, follow status, follow lists, and unfollow confirmation. | MSP-008 |
| Administrator interface | Supports user account cancellation and illegal content deletion confirmation. | MSP-009 |
| Multilingual interface | Supports switching between Chinese and English. | MSP-010 |

### Software/API Interfaces

The source document lists MySQL, Spring Boot, Vue, TypeScript, SQL, UI-related terms, and reference materials, but does not explicitly define API paths, interface protocols, database schemas, upload/download protocols, model online invocation protocols, or payment interfaces. (Source: MSP-001)

### Communication Interfaces

The source document does not explicitly define HTTP, HTTPS, WebSocket, RPC, message queues, or third-party payment communication interfaces. It can only be determined that the system runs in modern browsers and does not support Internet Explorer. (Source: MSP-011)

### Data Exchange Formats

The system needs to handle account information, login credentials, verification codes, registration email addresses, passwords, personal information, questions, question answers, blog articles, blog comments, model basic information, model usage methods, required model files, sale prices, model purchase status, model running input datasets, model running results, user browsing history, user registration information, dataset names, dataset files, follow relationships, administrator deletion objects, and illegal content data. The source document does not specify JSON schemas, file formats, field lengths, error codes, or data retention periods. (Source: MSP-003, MSP-004, MSP-005, MSP-006, MSP-007, MSP-008, MSP-009)

## 4. Functional Requirements

| ID | Requirement | Trigger / Input | System Behavior | Output | Priority | Verification | Source |
| --- | --- | --- | --- | --- | --- | --- | --- |
| FR-001 | The system shall allow unregistered users to register as general users. | An unauthenticated user selects registration and enters personal information and a password. | The system returns the registration page, validates the registration information, prompts registration success after successful submission, and returns to the home page; if the username is already registered, information is inconsistent, or a system exception occurs, it displays a prompt. | General user account or registration failure prompt. | High | Test | MSP-003 |
| FR-002 | The system shall allow general users to log in. | An unauthenticated user enters username, password, and verification code and submits them. | The system validates the login information, records the user as logged in after successful validation, and returns to the main page; if information is incorrect or a system exception occurs, it displays a prompt. | Login state or error prompt. | High | Test | MSP-003 |
| FR-003 | The system shall allow registered but unauthenticated users to recover passwords. | A user selects password recovery, enters the registered email address, and submits a new password. | The system returns the password recovery page, sends an email, prompts successful modification after successful verification, and redirects to the login page; if verification fails or an exception occurs, it displays a prompt. | Password reset result and login page redirect. | High | Test | MSP-003 |
| FR-004 | The system shall allow logged-in users to modify personal information. | A general user or administrator selects personal information modification and submits new information. | The system validates the input, prompts modification success after successful validation, and returns to the modification page with a prompt if the input is incorrect or an exception occurs. | Updated personal information or error prompt. | Medium | Test | MSP-003 |
| FR-005 | The system shall allow logged-in users to log out. | A general user or administrator selects account logout. | The system exits the login state, prompts success, and returns to the website home page; if the system is busy or an exception occurs, it displays a prompt. | Logged-out state and website home page. | Medium | Test | MSP-003 |
| FR-006 | The system shall allow logged-in users to publish questions. | A user enters the question publishing interface, enters a question, and submits it. | The system saves the question, prompts publishing success, and returns to the Q&A community; if the user exits before submission, it prompts whether to save, and if an exception occurs, it provides feedback. | New question or publishing failure prompt. | High | Test | MSP-004 |
| FR-007 | The system shall allow users to delete questions they published. | A logged-in user selects a question they published and chooses deletion. | The system deletes the selected question, prompts success, and returns to the Q&A community; it does not respond when no content is selected and displays a prompt on exception. | Deletion result or error prompt. | Medium | Test | MSP-004 |
| FR-008 | The system shall allow users to modify questions they published. | A logged-in user selects a question they published, modifies it, and submits it. | The system saves the modification, prompts success, and returns to the Q&A community; if the user exits before submission, it prompts whether to save, and if an exception occurs, it provides feedback. | Updated question or error prompt. | Medium | Test | MSP-004 |
| FR-009 | The system shall allow logged-in users to publish answers to questions. | A user selects publishing an answer, enters the answer, and submits it. | The system saves the answer, prompts publishing success, and returns to the Q&A community; if the user exits before submission, it prompts whether to save, and if an exception occurs, it provides feedback. | New answer or error prompt. | High | Test | MSP-004 |
| FR-010 | The system shall allow users to delete answers they published. | A logged-in user selects an answer they published and chooses deletion. | The system deletes the selected answer, prompts success, and returns to the Q&A community; it does not respond when no content is selected and displays a prompt on exception. | Deletion result or error prompt. | Medium | Test | MSP-004 |
| FR-011 | The system shall allow users to modify answers they published. | A logged-in user selects an answer they published, modifies it, and submits it. | The system saves the modification, prompts success, and returns to the Q&A community; if the user exits before submission, it prompts whether to save, and if an exception occurs, it provides feedback. | Updated answer or error prompt. | Medium | Test | MSP-004 |
| FR-012 | The system shall allow logged-in users to publish blog articles. | A user selects new article creation, enters article content, and submits it. | The system saves the article, prompts publishing success, and returns to the blog home page; if no title is entered or a system exception occurs, it displays a prompt. | New blog article or error prompt. | High | Test | MSP-005 |
| FR-013 | The system shall allow users to delete blog articles they published. | A logged-in user selects an article to delete and submits a deletion request. | The system deletes the article, prompts success, and returns to the blog home page; if no article is selected or an exception occurs, it displays a prompt. | Deletion result or error prompt. | Medium | Test | MSP-005 |
| FR-014 | The system shall allow users to modify blog articles they published. | A logged-in user selects an article to modify, modifies the content, and submits it. | The system saves the modification, prompts success, and returns to the article page; if an exception occurs, it displays a prompt and remains on the modification page. | Updated article or error prompt. | Medium | Test | MSP-005 |
| FR-015 | The system shall allow logged-in users to publish blog comments. | A user views a blog article and comment area, writes a comment, and submits it. | The system validates that the comment is non-empty and within the maximum word count, saves the comment, and refreshes the database state and comment area page. | New comment and updated comment area, or validation prompt. | Medium | Test | MSP-005 |
| FR-016 | The system shall allow users to delete published blog comments. | A user views their blog comments and clicks delete. | The system deletes the comment, prompts success, and refreshes the database state and comment area page; if an exception occurs, it displays a prompt. | Deletion result or error prompt. | Medium | Test | MSP-005 |
| FR-017 | The system shall allow users to modify published blog comments. | A user views their blog comments, clicks modify, and submits the modification. | The system saves the modification, prompts success, and refreshes the database state and comment area page; if an exception occurs, it displays a prompt. | Updated comment or error prompt. | Medium | Test | MSP-005 |
| FR-018 | The system shall allow logged-in users to upload models and choose whether to sell them. | A user edits model basic information, usage method, required files, sale settings, and price, then clicks upload. | The system validates the completed information, prompts upload success after validation, and enters the model review stage; if information is incomplete, it prompts modification. | Model pending review or validation prompt. | High | Test | MSP-006 |
| FR-019 | The system shall allow users to download purchased models. | A user enters the purchased models page, selects a model and local save path, and clicks download. | The system selects the model from the database and transfers it; after transfer completion it prompts download success; if the network is interrupted or local space is insufficient, it displays a prompt. | Local model file or download error prompt. | High | Test | MSP-006 |
| FR-020 | The system shall allow users to delete their uploaded models. | A logged-in user enters the uploaded models page, selects a model, and clicks delete. | The system selects the model from the database for deletion and prompts success after completion; if the network is interrupted, it prompts the user to check the network. | Deletion result or error prompt. | Medium | Test | MSP-006 |
| FR-021 | The system shall allow users to modify their uploaded models. | A user selects an uploaded model, modifies its basic information and required files, and submits it. | The system selects the model from the database for modification and prompts success after completion; if the network is interrupted or information is incomplete, it displays a prompt. | Updated model information or error prompt. | Medium | Test | MSP-006 |
| FR-022 | The system shall allow users to invoke models online. | A user selects a model from the personal model list or purchased model list, chooses a platform dataset or uploads a dataset, and clicks run. | The system runs the model and displays the run result; if the system is busy, the dataset format is wrong, or processing fails, it displays a prompt. | Model run result or error prompt. | High | Test | MSP-006 |
| FR-023 | The system shall recommend models to users. | A logged-in user enters the model module. | The system displays a recommendation model pool based on user browsing history and registration information; if a network exception occurs, it displays a prompt. | Recommended model list or error prompt. | Medium | Test | MSP-006 |
| FR-024 | The system shall allow users to purchase models. | A user selects a model from the full model list and clicks purchase, then clicks pay in the payment interface. | The system processes the purchase, prompts purchase success after completion, and adds the model to the purchased model list; if the balance is insufficient, the system is busy, or an exception occurs, it displays a prompt. | Purchased model record or purchase failure prompt. | High | Test | MSP-006 |
| FR-025 | The system shall allow logged-in users to upload datasets. | A user selects an upload path, names the dataset, and submits it. | The system checks naming legality and returns to the dataset page after successful upload; if the name is duplicated or illegal, it displays a warning. | New dataset or naming warning. | High | Test | MSP-007 |
| FR-026 | The system shall allow general users to download free datasets. | A general user enters the free datasets page and clicks download. | The system confirms that corresponding dataset information exists in the database and downloads the free dataset from the server to the user's local environment. | Local dataset file. | Medium | Test | MSP-007 |
| FR-027 | The system shall allow users to delete their datasets. | A logged-in authorized user enters their dataset page and selects deletion. | The system processes the deletion request and prompts the result; the prerequisite is that corresponding dataset information exists in the database. | Deletion result. | Medium | Test | MSP-007 |
| FR-028 | The system shall allow users to modify their datasets. | A user selects a dataset from their uploaded dataset list and clicks modify. | The system displays the modification interface, saves the user-submitted modification, and prompts success; if the system is busy or an exception occurs, it displays a prompt. | Updated dataset or error prompt. | Medium | Test | MSP-007 |
| FR-029 | The system shall allow users to follow other users. | A user clicks an author or avatar while browsing blogs or Q&A and clicks follow. | The system displays the user's abbreviated profile and follow status, prompts success after following, and adds the target user to the follow list; if the confirmation dialog is canceled, it makes no change. | Updated follow list or no change. | Medium | Test | MSP-008 |
| FR-030 | The system shall allow users to unfollow. | A user selects a target user from the personal follow list, clicks unfollow, and confirms. | The system removes the target user from the follow list; if confirmation is canceled, it makes no change. | Updated follow list or no change. | Medium | Test | MSP-008 |
| FR-031 | The system shall allow administrators to cancel user accounts. | A logged-in administrator selects a user account and confirms cancellation. | The system displays a confirmation prompt and removes the account from the user account list after administrator confirmation. | Cancellation result and updated account list. | High | Test | MSP-009 |
| FR-032 | The system shall allow administrators to delete illegal content. | A logged-in administrator selects an illegal question, answer, dataset, model, blog, or blog comment and confirms deletion. | The system displays a confirmation prompt and deletes the corresponding data after administrator confirmation, then returns a success prompt. | Deletion result. | High | Test | MSP-009 |

## 5. Non-Functional Requirements

| ID | Quality | Requirement | Metric / Acceptance | Priority | Verification | Source |
| --- | --- | --- | --- | --- | --- | --- |
| NFR-001 | Security | The system shall use multiple security mechanisms to prevent malicious operations from affecting the platform. | Malicious operations cannot damage core functions or data. | High | Test | MSP-010 |
| NFR-002 | Security | The system shall prevent common injection attacks. | Common injection attacks are blocked. | High | Test | MSP-010 |
| NFR-003 | Security | The system shall securely authenticate users and allow administrators to restrict functions for violating users. | After authentication, administrators can delete illegal information or cancel violating user accounts. | High | Test | MSP-010 |
| NFR-004 | Consistency | The system shall keep server data and front-end data consistent. | Server data and front-end data are consistent within a 3-second time interval. | High | Test | MSP-010 |
| NFR-005 | Usability | The system interface shall follow modern aesthetics, maintain a consistent style, and use a minimalist theme. | Main interfaces are stylistically consistent and match the minimalist theme. | Medium | Inspection | MSP-010 |
| NFR-006 | Usability | System operation entries shall be obvious, and access cost shall match usage frequency. | High-frequency operation entries are easier to access; when there are too many interfaces, classification aggregation or quick search is supported. | Medium | Demonstration | MSP-010 |
| NFR-007 | Reliability | The system shall meet a long-running target when the hardware and software runtime environments remain unchanged. | Expected time to failure is greater than 1 year. | High | Analysis | MSP-010 |
| NFR-008 | Availability | System maintenance windows shall be scheduled during low-impact periods. | 1:00 to 4:00 may be used as the system maintenance time. | Medium | Inspection | MSP-010 |
| NFR-009 | Capacity | The system shall support the required scale of user data storage. | Stores data for more than 10,000 users. | High | Analysis | MSP-010 |
| NFR-010 | Performance | The system shall support application request throughput. | Supports 1,000 application requests per second. | High | Test | MSP-010 |
| NFR-011 | Recoverability | The system shall be repaired promptly when it crashes because the data load exceeds the processing limit. | Repair is completed within 1 hour. | High | Demonstration | MSP-010 |
| NFR-012 | Internationalization | The system interface shall support switching between Chinese and English. | Users can switch between Chinese and English interfaces. | Medium | Test | MSP-010 |
| NFR-013 | Maintainability | The system shall have stability and partial self-troubleshooting ability without manual intervention. | Faults can be automatically identified or partially handled by the system. | Medium | Inspection | MSP-010 |
| NFR-014 | Extensibility | The system shall provide extensible interfaces through object orientation, abstraction, and modular code. | Later development can extend business requirements through interfaces. | Medium | Analysis | MSP-010 |
| NFR-015 | Recommendation Quality | The system shall add intelligent recommendation algorithms on top of traditional recommendation algorithms. | Recommended model content better matches users' personalized needs. | Medium | Test | MSP-010 |

## 6. Data Requirements

| ID | Data Entity / Object | Requirement | Source |
| --- | --- | --- | --- |
| DR-001 | User account data | The system shall store registration information, login state, email address, password, verification-code-related information, personal information, and user role. | MSP-003 |
| DR-002 | Question data | The system shall store questions published by general users and support author modification, author deletion, and administrator deletion of illegal questions. | MSP-004, MSP-009 |
| DR-003 | Answer data | The system shall store question answers and support author modification, author deletion, and administrator deletion of illegal answers. | MSP-004, MSP-009 |
| DR-004 | Blog article data | The system shall store blog articles and support author modification, author deletion, and administrator deletion of illegal blogs. | MSP-005, MSP-009 |
| DR-005 | Blog comment data | The system shall store blog comments, update database state and the comment area page, and support deletion of related comments by the author, blog author, or administrator. | MSP-005, MSP-009 |
| DR-006 | Model data | The system shall store model basic information, usage methods, required files, review state, sale flag, price, purchase relationships, and data required for download and online invocation. | MSP-006 |
| DR-007 | Dataset data | The system shall store dataset name, upload path, file content, owner, and database existence information. | MSP-007 |
| DR-008 | Follow relationship data | The system shall store user follow lists and followed-user relationships. | MSP-008 |
| DR-009 | Recommendation data | The system shall use user browsing history and registration information to support model recommendation. | MSP-006 |
| DR-010 | Administrator governance data | The system shall allow administrators to delete or cancel user accounts and illegal content data. | MSP-009 |

## 7. Constraints

| ID | Constraint | Source |
| --- | --- | --- |
| C-001 | Reference technologies include MySQL, Spring Boot, Vue, TypeScript, SQL, and UI-related technologies. | MSP-001 |
| C-002 | Runtime hardware CPU shall use x86-64 or ARM architecture. | MSP-011 |
| C-003 | The runtime environment shall have at least 4 GB of memory. | MSP-011 |
| C-004 | The runtime environment shall have at least 30 GB of available disk space. | MSP-011 |
| C-005 | The runtime environment shall be all modern browsers. | MSP-011 |
| C-006 | The system shall not support Internet Explorer. | MSP-011 |
| C-007 | The development deadline is limited to completion in early May. | MSP-011 |

## 8. Verification and Acceptance

| Verification Method | Applicable Requirement IDs | Acceptance Basis |
| --- | --- | --- |
| Test | FR-001 to FR-032; NFR-001, NFR-002, NFR-003, NFR-004, NFR-010, NFR-012, NFR-015 | Execute account, Q&A, blog, model, dataset, follow, administrator governance, security, synchronization, throughput, multilingual, and recommendation tests; results satisfy the corresponding outputs and thresholds. |
| Inspection | NFR-005, NFR-008, NFR-013; DR-001 to DR-010; C-001 to C-007 | Inspect whether the interface, maintenance window, data model, permission design, runtime environment, and development constraints are covered. |
| Analysis | NFR-007, NFR-009, NFR-014 | Confirm satisfaction through review of availability targets, capacity estimates, and extensible interface design. |
| Demonstration | NFR-006, NFR-011 | Demonstrate high-frequency entry accessibility, classification/search capability, and recovery within one hour after overload crash. |

## 9. Traceability Matrix

| ID | Requirement | Type | Source | Evidence Type | Verification | Confidence |
| --- | --- | --- | --- | --- | --- | --- |
| FR-001 | Registration | Functional | MSP-003 | explicit | Test | High |
| FR-002 | Login | Functional | MSP-003 | explicit | Test | High |
| FR-003 | Password recovery | Functional | MSP-003 | explicit | Test | High |
| FR-004 | Modify personal information | Functional | MSP-003 | explicit | Test | High |
| FR-005 | Account logout | Functional | MSP-003 | explicit | Test | High |
| FR-006 | Publish question | Functional | MSP-004 | explicit | Test | High |
| FR-007 | Delete question | Functional | MSP-004 | explicit | Test | High |
| FR-008 | Modify question | Functional | MSP-004 | explicit | Test | High |
| FR-009 | Publish answer | Functional | MSP-004 | explicit | Test | High |
| FR-010 | Delete answer | Functional | MSP-004 | explicit | Test | High |
| FR-011 | Modify answer | Functional | MSP-004 | explicit | Test | High |
| FR-012 | Publish blog article | Functional | MSP-005 | explicit | Test | High |
| FR-013 | Delete blog article | Functional | MSP-005 | explicit | Test | High |
| FR-014 | Modify blog article | Functional | MSP-005 | explicit | Test | High |
| FR-015 | Publish blog comment | Functional | MSP-005 | explicit | Test | High |
| FR-016 | Delete blog comment | Functional | MSP-005 | explicit | Test | High |
| FR-017 | Modify blog comment | Functional | MSP-005 | explicit | Test | High |
| FR-018 | Upload model | Functional | MSP-006 | explicit | Test | High |
| FR-019 | Download model | Functional | MSP-006 | explicit | Test | High |
| FR-020 | Delete model | Functional | MSP-006 | explicit | Test | High |
| FR-021 | Modify model | Functional | MSP-006 | explicit | Test | High |
| FR-022 | Online model invocation | Functional | MSP-006 | explicit | Test | High |
| FR-023 | Recommend model | Functional | MSP-006 | explicit | Test | High |
| FR-024 | Purchase model | Functional | MSP-006 | explicit | Test | High |
| FR-025 | Upload dataset | Functional | MSP-007 | explicit | Test | High |
| FR-026 | Download dataset | Functional | MSP-007 | explicit | Test | High |
| FR-027 | Delete dataset | Functional | MSP-007 | explicit | Test | High |
| FR-028 | Modify dataset | Functional | MSP-007 | explicit | Test | High |
| FR-029 | Follow | Functional | MSP-008 | explicit | Test | High |
| FR-030 | Unfollow | Functional | MSP-008 | explicit | Test | High |
| FR-031 | Administrator cancels user account | Functional | MSP-009 | explicit | Test | High |
| FR-032 | Administrator deletes illegal content | Functional | MSP-009 | explicit | Test | High |
| NFR-001 | Prevent malicious operations | Non-functional | MSP-010 | explicit | Test | High |
| NFR-002 | Prevent injection attacks | Non-functional | MSP-010 | explicit | Test | High |
| NFR-003 | Secure authentication and violation restriction | Non-functional | MSP-010 | explicit | Test | High |
| NFR-004 | Front-end and back-end data consistency | Non-functional | MSP-010 | explicit | Test | High |
| NFR-005 | Interface style | Non-functional | MSP-010 | explicit | Inspection | High |
| NFR-006 | Operation entries and access cost | Non-functional | MSP-010 | explicit | Demonstration | High |
| NFR-007 | Expected time to failure | Non-functional | MSP-010 | explicit | Analysis | High |
| NFR-008 | Maintenance window | Non-functional | MSP-010 | explicit | Inspection | High |
| NFR-009 | User data capacity | Non-functional | MSP-010 | explicit | Analysis | High |
| NFR-010 | Application request throughput | Non-functional | MSP-010 | explicit | Test | High |
| NFR-011 | Overload crash recovery | Non-functional | MSP-010 | explicit | Demonstration | High |
| NFR-012 | Chinese-English switching | Non-functional | MSP-010 | explicit | Test | High |
| NFR-013 | Stability and self-troubleshooting | Non-functional | MSP-010 | explicit | Inspection | High |
| NFR-014 | Extensible interfaces | Non-functional | MSP-010 | explicit | Analysis | High |
| NFR-015 | Personalized recommendation | Non-functional | MSP-010 | explicit | Test | High |
| DR-001 | User account data | Data | MSP-003 | explicit | Inspection | High |
| DR-002 | Question data | Data | MSP-004, MSP-009 | explicit | Inspection | High |
| DR-003 | Answer data | Data | MSP-004, MSP-009 | explicit | Inspection | High |
| DR-004 | Blog article data | Data | MSP-005, MSP-009 | explicit | Inspection | High |
| DR-005 | Blog comment data | Data | MSP-005, MSP-009 | explicit | Inspection | High |
| DR-006 | Model data | Data | MSP-006 | explicit | Inspection | High |
| DR-007 | Dataset data | Data | MSP-007 | explicit | Inspection | High |
| DR-008 | Follow relationship data | Data | MSP-008 | explicit | Inspection | High |
| DR-009 | Recommendation data | Data | MSP-006 | explicit | Inspection | High |
| DR-010 | Administrator governance data | Data | MSP-009 | explicit | Inspection | High |
| C-001 | Reference technologies | Constraint | MSP-001 | explicit | Inspection | High |
| C-002 | CPU architecture | Constraint | MSP-011 | explicit | Inspection | High |
| C-003 | Memory | Constraint | MSP-011 | explicit | Inspection | High |
| C-004 | Disk | Constraint | MSP-011 | explicit | Inspection | High |
| C-005 | Modern browsers | Constraint | MSP-011 | explicit | Inspection | High |
| C-006 | No IE support | Constraint | MSP-011 | explicit | Inspection | High |
| C-007 | Development deadline | Constraint | MSP-011 | explicit | Inspection | High |
