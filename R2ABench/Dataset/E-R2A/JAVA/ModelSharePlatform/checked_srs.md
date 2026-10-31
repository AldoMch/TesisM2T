# Deep Learning Model Sharing Platform Software Requirements Specification (Standard SRS Extract)

## 1. Introduction

### Purpose
The goal is to provide structured input for architecture generation, test design, and requirements tracing for the Deep Learning Model Sharing Platform.

### Product Scope

The Deep Learning Model Sharing Platform targets deep learning enthusiasts and professionals, providing a one-stop cloud service for communication, learning, creation, and application of deep learning models. The platform supports a Q&A community, blog sharing, model library management, dataset management, online invocation experiences, paid model sales revenue, follow relationships, and administrator governance.

This document uses the specification terminology for general users, administrators, Q&A community, blogs, models, datasets, online invocation, paid sales, SQL, MySQL, TypeScript, UI, Spring Boot, and Vue.

### Intended Audience

This document is intended for platform general users, administrators, developers, testers, requirements reviewers, and later architecture generation and acceptance testing workflows. General users are the primary platform users, and administrators manage platform-related data.

## 2. Overall Description

### Product Perspective

The platform references existing community product capabilities such as registration, login, personal information management, blog writing, resource sharing, and Q&A communication, and extends them with deep learning domain capabilities including model and dataset upload and sharing, online invocation of pretrained models, and paid transactions for model products. The specification does not provide a complete system architecture, API, database table structure, or deployment topology.

### Product Functions Summary

| Capability | Summary |
| --- | --- |
| Account management | Supports registration, login, password recovery, personal information modification, and account logout. |
| Q&A community | Supports publishing, modifying, and deleting questions, and publishing, modifying, and deleting answers. |
| Blog sharing | Supports publishing, modifying, and deleting blog articles, and publishing, modifying, and deleting blog comments. |
| Model management | Supports model upload, review entry, download, deletion, modification, online invocation, recommendation, and purchase. |
| Dataset management | Supports dataset upload, download, deletion, and modification. |
| Follow management | Supports following users and unfollowing users. |
| Administrator management | Supports account cancellation and deletion of illegal questions, answers, datasets, models, blogs, and blog comments. |

### User Classes

| User Class | Responsibilities / Needs |
| --- | --- |
| General user | Uses platform Q&A, blogs, models, datasets, online invocation, purchase, follow, and personal account features; expects quick use of deep learning models. |
| Administrator | Manages platform data such as user accounts, questions and answers, blogs and comments, datasets, and models. |

### Operating Environment

| Environment | Requirement |
| --- | --- |
| CPU | x86-64 or ARM architecture. |
| Memory | At least 4 GB. |
| Disk | At least 30 GB of available space. |
| Browser | All modern browsers. |
| Unsupported Browser | Internet Explorer is not supported. |

### Assumptions and Dependencies

| ID | Assumption / Dependency |
| --- | --- |
| AD-001 | Core capabilities such as models, datasets, Q&A, blogs, follows, and purchases depend on the general user being logged in. |
| AD-002 | Administrator governance capabilities depend on the user being logged in as an administrator. |
| AD-003 | Model recommendation depends on user browsing history and registration information. |
| AD-004 | Dataset download, deletion, and similar operations depend on corresponding dataset information existing in the database. |
| AD-005 | The specification does not define the model review process, payment channel, API schema, or database table structure; later design must not assume these details are complete. |

## 3. External Interface Requirements

### User Interfaces

| Interface | Requirement |
| --- | --- |
| Account interface | Supports registration, login, password recovery, personal information modification, and account logout. |
| Q&A community interface | Supports publishing, modifying, and deleting questions and answers, with save prompts and failure feedback. |
| Blog interface | Supports publishing, modifying, and deleting blog articles and blog comments, with save prompts and failure feedback. |
| Model interface | Supports model upload, purchased models, uploaded models, online running, recommendation model pool, and purchase/payment interface. |
| Dataset interface | Supports dataset upload, free dataset download, and deletion and modification of personal datasets. |
| Follow interface | Supports abbreviated user profiles, follow status, follow lists, and unfollow confirmation. |
| Administrator interface | Supports user account cancellation and illegal content deletion confirmation. |
| Multilingual interface | Supports switching between Chinese and English. |

### Software/API Interfaces

The specification lists MySQL, Spring Boot, Vue, TypeScript, SQL, UI-related terms, and reference materials, but does not explicitly define API paths, interface protocols, database schemas, upload/download protocols, model online invocation protocols, or payment interfaces.

### Communication Interfaces

The specification does not explicitly define HTTP, HTTPS, WebSocket, RPC, message queues, or third-party payment communication interfaces. It can only be determined that the system runs in modern browsers and does not support Internet Explorer.

### Data Exchange Formats

The system needs to handle account information, login credentials, verification codes, registration email addresses, passwords, personal information, questions, question answers, blog articles, blog comments, model basic information, model usage methods, required model files, sale prices, model purchase status, model running input datasets, model running results, user browsing history, user registration information, dataset names, dataset files, follow relationships, administrator deletion objects, and illegal content data. The specification does not specify JSON schemas, file formats, field lengths, error codes, or data retention periods.

## 4. Functional Requirements

| ID | Requirement | Trigger / Input | System Behavior | Output | Priority | Verification |
| --- | --- | --- | --- | --- | --- | --- |
| FR-001 | The system shall allow unregistered users to register as general users. | An unauthenticated user selects registration and enters personal information and a password. | The system returns the registration page, validates the registration information, prompts registration success after successful submission, and returns to the home page; if the username is already registered, information is inconsistent, or a system exception occurs, it displays a prompt. | General user account or registration failure prompt. | High | Test |
| FR-002 | The system shall allow general users to log in. | An unauthenticated user enters username, password, and verification code and submits them. | The system validates the login information, records the user as logged in after successful validation, and returns to the main page; if information is incorrect or a system exception occurs, it displays a prompt. | Login state or error prompt. | High | Test |
| FR-003 | The system shall allow registered but unauthenticated users to recover passwords. | A user selects password recovery, enters the registered email address, and submits a new password. | The system returns the password recovery page, sends an email, prompts successful modification after successful verification, and redirects to the login page; if verification fails or an exception occurs, it displays a prompt. | Password reset result and login page redirect. | High | Test |
| FR-004 | The system shall allow logged-in users to modify personal information. | A general user or administrator selects personal information modification and submits new information. | The system validates the input, prompts modification success after successful validation, and returns to the modification page with a prompt if the input is incorrect or an exception occurs. | Updated personal information or error prompt. | Medium | Test |
| FR-005 | The system shall allow logged-in users to log out. | A general user or administrator selects account logout. | The system exits the login state, prompts success, and returns to the website home page; if the system is busy or an exception occurs, it displays a prompt. | Logged-out state and website home page. | Medium | Test |
| FR-006 | The system shall allow logged-in users to publish questions. | A user enters the question publishing interface, enters a question, and submits it. | The system saves the question, prompts publishing success, and returns to the Q&A community; if the user exits before submission, it prompts whether to save, and if an exception occurs, it provides feedback. | New question or publishing failure prompt. | High | Test |
| FR-007 | The system shall allow users to delete questions they published. | A logged-in user selects a question they published and chooses deletion. | The system deletes the selected question, prompts success, and returns to the Q&A community; it does not respond when no content is selected and displays a prompt on exception. | Deletion result or error prompt. | Medium | Test |
| FR-008 | The system shall allow users to modify questions they published. | A logged-in user selects a question they published, modifies it, and submits it. | The system saves the modification, prompts success, and returns to the Q&A community; if the user exits before submission, it prompts whether to save, and if an exception occurs, it provides feedback. | Updated question or error prompt. | Medium | Test |
| FR-009 | The system shall allow logged-in users to publish answers to questions. | A user selects publishing an answer, enters the answer, and submits it. | The system saves the answer, prompts publishing success, and returns to the Q&A community; if the user exits before submission, it prompts whether to save, and if an exception occurs, it provides feedback. | New answer or error prompt. | High | Test |
| FR-010 | The system shall allow users to delete answers they published. | A logged-in user selects an answer they published and chooses deletion. | The system deletes the selected answer, prompts success, and returns to the Q&A community; it does not respond when no content is selected and displays a prompt on exception. | Deletion result or error prompt. | Medium | Test |
| FR-011 | The system shall allow users to modify answers they published. | A logged-in user selects an answer they published, modifies it, and submits it. | The system saves the modification, prompts success, and returns to the Q&A community; if the user exits before submission, it prompts whether to save, and if an exception occurs, it provides feedback. | Updated answer or error prompt. | Medium | Test |
| FR-012 | The system shall allow logged-in users to publish blog articles. | A user selects new article creation, enters article content, and submits it. | The system saves the article, prompts publishing success, and returns to the blog home page; if no title is entered or a system exception occurs, it displays a prompt. | New blog article or error prompt. | High | Test |
| FR-013 | The system shall allow users to delete blog articles they published. | A logged-in user selects an article to delete and submits a deletion request. | The system deletes the article, prompts success, and returns to the blog home page; if no article is selected or an exception occurs, it displays a prompt. | Deletion result or error prompt. | Medium | Test |
| FR-014 | The system shall allow users to modify blog articles they published. | A logged-in user selects an article to modify, modifies the content, and submits it. | The system saves the modification, prompts success, and returns to the article page; if an exception occurs, it displays a prompt and remains on the modification page. | Updated article or error prompt. | Medium | Test |
| FR-015 | The system shall allow logged-in users to publish blog comments. | A user views a blog article and comment area, writes a comment, and submits it. | The system validates that the comment is non-empty and within the maximum word count, saves the comment, and refreshes the database state and comment area page. | New comment and updated comment area, or validation prompt. | Medium | Test |
| FR-016 | The system shall allow users to delete published blog comments. | A user views their blog comments and clicks delete. | The system deletes the comment, prompts success, and refreshes the database state and comment area page; if an exception occurs, it displays a prompt. | Deletion result or error prompt. | Medium | Test |
| FR-017 | The system shall allow users to modify published blog comments. | A user views their blog comments, clicks modify, and submits the modification. | The system saves the modification, prompts success, and refreshes the database state and comment area page; if an exception occurs, it displays a prompt. | Updated comment or error prompt. | Medium | Test |
| FR-018 | The system shall allow logged-in users to upload models and choose whether to sell them. | A user edits model basic information, usage method, required files, sale settings, and price, then clicks upload. | The system validates the completed information, prompts upload success after validation, and enters the model review stage; if information is incomplete, it prompts modification. | Model pending review or validation prompt. | High | Test |
| FR-019 | The system shall allow users to download purchased models. | A user enters the purchased models page, selects a model and local save path, and clicks download. | The system selects the model from the database and transfers it; after transfer completion it prompts download success; if the network is interrupted or local space is insufficient, it displays a prompt. | Local model file or download error prompt. | High | Test |
| FR-020 | The system shall allow users to delete their uploaded models. | A logged-in user enters the uploaded models page, selects a model, and clicks delete. | The system selects the model from the database for deletion and prompts success after completion; if the network is interrupted, it prompts the user to check the network. | Deletion result or error prompt. | Medium | Test |
| FR-021 | The system shall allow users to modify their uploaded models. | A user selects an uploaded model, modifies its basic information and required files, and submits it. | The system selects the model from the database for modification and prompts success after completion; if the network is interrupted or information is incomplete, it displays a prompt. | Updated model information or error prompt. | Medium | Test |
| FR-022 | The system shall allow users to invoke models online. | A user selects a model from the personal model list or purchased model list, chooses a platform dataset or uploads a dataset, and clicks run. | The system runs the model and displays the run result; if the system is busy, the dataset format is wrong, or processing fails, it displays a prompt. | Model run result or error prompt. | High | Test |
| FR-023 | The system shall recommend models to users. | A logged-in user enters the model module. | The system displays a recommendation model pool based on user browsing history and registration information; if a network exception occurs, it displays a prompt. | Recommended model list or error prompt. | Medium | Test |
| FR-024 | The system shall allow users to purchase models. | A user selects a model from the full model list and clicks purchase, then clicks pay in the payment interface. | The system processes the purchase, prompts purchase success after completion, and adds the model to the purchased model list; if the balance is insufficient, the system is busy, or an exception occurs, it displays a prompt. | Purchased model record or purchase failure prompt. | High | Test |
| FR-025 | The system shall allow logged-in users to upload datasets. | A user selects an upload path, names the dataset, and submits it. | The system checks naming legality and returns to the dataset page after successful upload; if the name is duplicated or illegal, it displays a warning. | New dataset or naming warning. | High | Test |
| FR-026 | The system shall allow general users to download free datasets. | A general user enters the free datasets page and clicks download. | The system confirms that corresponding dataset information exists in the database and downloads the free dataset from the server to the user's local environment. | Local dataset file. | Medium | Test |
| FR-027 | The system shall allow users to delete their datasets. | A logged-in authorized user enters their dataset page and selects deletion. | The system processes the deletion request and prompts the result; the prerequisite is that corresponding dataset information exists in the database. | Deletion result. | Medium | Test |
| FR-028 | The system shall allow users to modify their datasets. | A user selects a dataset from their uploaded dataset list and clicks modify. | The system displays the modification interface, saves the user-submitted modification, and prompts success; if the system is busy or an exception occurs, it displays a prompt. | Updated dataset or error prompt. | Medium | Test |
| FR-029 | The system shall allow users to follow other users. | A user clicks an author or avatar while browsing blogs or Q&A and clicks follow. | The system displays the user's abbreviated profile and follow status, prompts success after following, and adds the target user to the follow list; if the confirmation dialog is canceled, it makes no change. | Updated follow list or no change. | Medium | Test |
| FR-030 | The system shall allow users to unfollow. | A user selects a target user from the personal follow list, clicks unfollow, and confirms. | The system removes the target user from the follow list; if confirmation is canceled, it makes no change. | Updated follow list or no change. | Medium | Test |
| FR-031 | The system shall allow administrators to cancel user accounts. | A logged-in administrator selects a user account and confirms cancellation. | The system displays a confirmation prompt and removes the account from the user account list after administrator confirmation. | Cancellation result and updated account list. | High | Test |
| FR-032 | The system shall allow administrators to delete illegal content. | A logged-in administrator selects an illegal question, answer, dataset, model, blog, or blog comment and confirms deletion. | The system displays a confirmation prompt and deletes the corresponding data after administrator confirmation, then returns a success prompt. | Deletion result. | High | Test |

## 5. Non-Functional Requirements

| ID | Quality | Requirement | Metric / Acceptance | Priority | Verification |
| --- | --- | --- | --- | --- | --- |
| NFR-001 | Security | The system shall use multiple security mechanisms to prevent malicious operations from affecting the platform. | Malicious operations cannot damage core functions or data. | High | Test |
| NFR-002 | Security | The system shall prevent common injection attacks. | Common injection attacks are blocked. | High | Test |
| NFR-003 | Security | The system shall securely authenticate users and allow administrators to restrict functions for violating users. | After authentication, administrators can delete illegal information or cancel violating user accounts. | High | Test |
| NFR-004 | Consistency | The system shall keep server data and front-end data consistent. | Server data and front-end data are consistent within a 3-second time interval. | High | Test |
| NFR-005 | Usability | The system interface shall follow modern aesthetics, maintain a consistent style, and use a minimalist theme. | Main interfaces are stylistically consistent and match the minimalist theme. | Medium | Inspection |
| NFR-006 | Usability | System operation entries shall be obvious, and access cost shall match usage frequency. | High-frequency operation entries are easier to access; when there are too many interfaces, classification aggregation or quick search is supported. | Medium | Demonstration |
| NFR-007 | Reliability | The system shall meet a long-running target when the hardware and software runtime environments remain unchanged. | Expected time to failure is greater than 1 year. | High | Analysis |
| NFR-008 | Availability | System maintenance windows shall be scheduled during low-impact periods. | 1:00 to 4:00 may be used as the system maintenance time. | Medium | Inspection |
| NFR-009 | Capacity | The system shall support the required scale of user data storage. | Stores data for more than 10,000 users. | High | Analysis |
| NFR-010 | Performance | The system shall support application request throughput. | Supports 1,000 application requests per second. | High | Test |
| NFR-011 | Recoverability | The system shall be repaired promptly when it crashes because the data load exceeds the processing limit. | Repair is completed within 1 hour. | High | Demonstration |
| NFR-012 | Internationalization | The system interface shall support switching between Chinese and English. | Users can switch between Chinese and English interfaces. | Medium | Test |
| NFR-013 | Maintainability | The system shall have stability and partial self-troubleshooting ability without manual intervention. | Faults can be automatically identified or partially handled by the system. | Medium | Inspection |
| NFR-014 | Extensibility | The system shall provide extensible interfaces through object orientation, abstraction, and modular code. | Later development can extend business requirements through interfaces. | Medium | Analysis |
| NFR-015 | Recommendation Quality | The system shall add intelligent recommendation algorithms on top of traditional recommendation algorithms. | Recommended model content better matches users' personalized needs. | Medium | Test |

## 6. Data Requirements

| ID | Data Entity / Object | Requirement |
| --- | --- | --- |
| DR-001 | User account data | The system shall store registration information, login state, email address, password, verification-code-related information, personal information, and user role. |
| DR-002 | Question data | The system shall store questions published by general users and support author modification, author deletion, and administrator deletion of illegal questions. |
| DR-003 | Answer data | The system shall store question answers and support author modification, author deletion, and administrator deletion of illegal answers. |
| DR-004 | Blog article data | The system shall store blog articles and support author modification, author deletion, and administrator deletion of illegal blogs. |
| DR-005 | Blog comment data | The system shall store blog comments, update database state and the comment area page, and support deletion of related comments by the author, blog author, or administrator. |
| DR-006 | Model data | The system shall store model basic information, usage methods, required files, review state, sale flag, price, purchase relationships, and data required for download and online invocation. |
| DR-007 | Dataset data | The system shall store dataset name, upload path, file content, owner, and database existence information. |
| DR-008 | Follow relationship data | The system shall store user follow lists and followed-user relationships. |
| DR-009 | Recommendation data | The system shall use user browsing history and registration information to support model recommendation. |
| DR-010 | Administrator governance data | The system shall allow administrators to delete or cancel user accounts and illegal content data. |

## 7. Constraints

| ID | Constraint |
| --- | --- |
| C-001 | Reference technologies include MySQL, Spring Boot, Vue, TypeScript, SQL, and UI-related technologies. |
| C-002 | Runtime hardware CPU shall use x86-64 or ARM architecture. |
| C-003 | The runtime environment shall have at least 4 GB of memory. |
| C-004 | The runtime environment shall have at least 30 GB of available disk space. |
| C-005 | The runtime environment shall be all modern browsers. |
| C-006 | The system shall not support Internet Explorer. |
| C-007 | The development deadline is limited to completion in early May. |

## 8. Verification and Acceptance

| Verification Method | Applicable Requirement IDs | Acceptance Basis |
| --- | --- | --- |
| Test | FR-001 to FR-032; NFR-001, NFR-002, NFR-003, NFR-004, NFR-010, NFR-012, NFR-015 | Execute account, Q&A, blog, model, dataset, follow, administrator governance, security, synchronization, throughput, multilingual, and recommendation tests; results satisfy the corresponding outputs and thresholds. |
| Inspection | NFR-005, NFR-008, NFR-013; DR-001 to DR-010; C-001 to C-007 | Inspect whether the interface, maintenance window, data model, permission design, runtime environment, and development constraints are covered. |
| Analysis | NFR-007, NFR-009, NFR-014 | Confirm satisfaction through review of availability targets, capacity estimates, and extensible interface design. |
| Demonstration | NFR-006, NFR-011 | Demonstrate high-frequency entry accessibility, classification/search capability, and recovery within one hour after overload crash. |
