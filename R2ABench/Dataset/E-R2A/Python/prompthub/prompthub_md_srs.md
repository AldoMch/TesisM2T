# PromptHub Software Requirements Specification (Standard SRS Extract)

## 1. Introduction

### Purpose

This document extracts verifiable requirements from `Software Requirements Specification v1.1.3.md` and rewrites them according to the compact SRS standard in `architectural_views_rep-pkg/script/templates/SRS.md`. The goal is to provide structured input for architecture generation, test design, and requirements tracing for the PromptHub community Web application. Source evidence is recorded in `prompthub_md_evidence_pack.json`. (Source: PH-001)

### Product Scope

PromptHub is a community Web application for sharing AI artworks and Prompts. The system scope includes AI artwork browsing and discussion, artwork categorization and retrieval, user artwork upload and administrator review, user profile and relationship management, favorite management, comments and replies, popular and personalized recommendations, notifications, and the front-end, back-end, algorithm support, and data persistence capabilities that support these functions. (Source: PH-002, PH-004)

This document follows the terminology definitions in the source requirements document for AIGC, Prompt, Vue.js, Django, SQLite, and Docker. The source document does not define API paths, database table structures, or concrete data exchange formats. (Source: PH-001)

### Intended Audience

This document is intended for PromptHub developers, testers, project managers, requirements reviewers, later architecture generation workflows, and stakeholders who need to understand requirement coverage and evidence sources. (Source: PH-001, PH-002)

### References

| Ref | Source |
| --- | --- |
| REF-001 | GB/T 9385-2008 Computer Software Requirements Specification |
| REF-002 | GB/T 20918-2007 Information Technology, Software Life Cycle Process and Risk Management |
| REF-003 | GB/T 15532-2008 Computer Software Testing Specification |
| REF-004 | GB/T 20917-2007 Software Engineering and Software Measurement Process |
| REF-005 | Django, SQLite, Vue.js, and Docker official websites |

## 2. Overall Description

### Product Perspective

PromptHub is a community Web application composed of three major modules: front end, back end, and algorithm support. The front end handles user interaction and artwork display. The back end handles business services such as users, artworks, favorites, comments, review, and notifications. The algorithm support module handles recommendation capabilities. The source document explicitly constrains the technology stack to Vue/JQuery, Django, SQLite, Docker, PyTorch/TensorFlow, and related technologies, but does not expand concrete deployment topology, API routes, or database ER model. (Source: PH-002, PH-004, PH-022)

### Product Functions Summary

| Capability | Summary | Source |
| --- | --- | --- |
| Artwork browsing and discussion | The home page displays AI artworks, and artwork details display Prompt, model, creator, comments, and replies. | PH-002, PH-011, PH-013 |
| Categorization, retrieval, and sorting | Users or visitors can query artworks by Prompt keywords, tags, popularity, upload time, model, and other conditions. | PH-002, PH-011 |
| Upload and review | Users upload AI-generated images, Prompts, models, categories, and additional information, and administrators approve or reject them after review. | PH-002, PH-010, PH-011 |
| User and relationship management | Supports registration, login, password maintenance, personal home pages, avatars/usernames, follow relationships, fans, and browsing history. | PH-007, PH-009 |
| Favorite management | Supports artwork favorites, public and private favorite categories, favorite queries, category deletion, and category modification. | PH-007, PH-012 |
| Recommendation and notification | Supports popular recommendation, personalized recommendation, disabling personalized recommendation, and notifications for comments, replies, and review progress changes. | PH-007, PH-014, PH-015 |
| Administration and content governance | Administrators view users and artworks, review uploaded artworks, and view and delete comments and replies. | PH-008, PH-010 |

### User Classes

| User Class | Responsibilities / Needs | Source |
| --- | --- | --- |
| Visitor | Browses AI artworks and Prompts, views popular recommendations, queries artworks and artwork details, and can register as a user. | PH-006 |
| Registered user | Manages account profile, artworks, favorites, comments, follows, recommendation preferences, browsing history, and system notifications. | PH-007 |
| Administrator | Maintains community content and environment, views users and artworks, reviews uploaded artworks, and manages comments and replies. | PH-008 |
| AI artwork creator | Uploads their own AI artworks, Prompts, and model information for other users to browse. | PH-003 |
| AI artwork viewer and newcomer | Browses categorized works and asks questions or communicates in comments to learn about AI painting. | PH-003 |

### Operating Environment

| Environment | Requirement | Source |
| --- | --- | --- |
| Minimum client hardware | CPU: 8th Generation Intel Core i7; GPU: NVIDIA GeForce MX250; memory: 4 GB. | PH-022 |
| Recommended client hardware | CPU: Intel Core i5-10600K or above; GPU: NVIDIA GeForce GTX 1060 or above; memory: 16 GB or above. | PH-022 |
| Client software | Chrome 110.0.5481.178 or above, Safari 15.3 or above, Firefox 119.0 or above; the source document also states support for GUI operating systems based on Windows 7 and macOS 8.0 or above kernels. | PH-005, PH-022 |
| Server hardware | CPU: Intel Core i5-10600K or above; GPU: NVIDIA GeForce GTX 2060 or above; memory: 32 GB or above. | PH-022 |
| Server software | Ubuntu 22.0.4 and Docker 20.10.17. | PH-022 |
| Network | When users cannot connect to the network, all requirements cannot be realized. | PH-005 |

### Assumptions and Dependencies

| ID | Assumption / Dependency | Evidence Type | Source |
| --- | --- | --- | --- |
| AD-001 | System functions depend on user network connectivity. | explicit | PH-005 |
| AD-002 | Project development depends on the experiment plan and requirement change process. | explicit | PH-004 |
| AD-003 | During runtime, the system needs to limit simultaneous access volume to ensure safe and stable operation. | explicit | PH-004 |
| AD-004 | SQLite is adopted because of runtime environment constraints, and later high-concurrency scenarios may migrate to databases such as MySQL. | explicit | PH-001 |
| AD-005 | The source document contains use case and activity diagrams, but this document extracts only textual evidence; details not expanded in the diagrams are not invented. | inferred | PH-001, PH-009 |

## 3. External Interface Requirements

### User Interfaces

| Interface | Requirement | Source |
| --- | --- | --- |
| Home page and artwork list interface | Displays AI artworks and supports popular recommendation, personalized recommendation entry, search, sorting, and filtering. | PH-002, PH-011, PH-014 |
| Registration, login, and account interface | Supports registration, login, logout, password change, password recovery, avatar change, and username change. | PH-009 |
| Artwork detail interface | Displays artwork image, Prompt, AI model, tag/category, uploader, additional information, comments, and replies. | PH-011, PH-013 |
| Upload and edit interface | Supports users uploading or editing AI images, Prompts, models, categories, and additional information, and entering the review flow. | PH-011 |
| Favorite management interface | Supports favorite, public/private favorite categories, viewing, querying, cancellation, deletion, and favorite category modification. | PH-012 |
| Administrator interface | Supports administrators viewing user and artwork lists, reviewing uploaded artworks, and viewing and deleting comments and replies. | PH-010 |
| Notification interface | Supports displaying unread notifications, marking them as read, and deleting notifications. | PH-015 |

### Software/API Interfaces

| Interface | Requirement | Source |
| --- | --- | --- |
| Front-end module | The front end shall be developed with HTML, CSS, JavaScript, and frameworks such as Vue and JQuery. | PH-004 |
| Back-end module | The back end shall be developed with Python, Java, and the Django framework. | PH-004 |
| Algorithm support module | The algorithm support module shall use Python and frameworks such as PyTorch and TensorFlow. | PH-004 |
| SQLite database | The system uses lightweight SQLite as the back-end database; later high-concurrency scenarios may migrate to databases such as MySQL. | PH-001 |
| Docker runtime environment | The server runtime environment specifies Docker 20.10.17, and reliability requirements also assume Docker deployment. | PH-017, PH-022 |

### Communication Interfaces

The source document requires Web pages to use secure HTTP requests, authenticate user operations, enable firewalls and cross-origin access control on the server, and prevent illegal links, XSS, and SQL injection. The source document does not provide REST, RPC, WebSocket, or message queue protocol details. (Source: PH-018)

### Data Exchange Formats

The source document explicitly identifies data objects and interaction content, including account information, AI-generated images, Prompt, model, category, tags, artwork additional information, comments, replies, favorites, follows, browsing history, review progress, and notifications. It does not specify JSON, forms, multimedia upload, or database field formats. Implementation and review should mark unspecified formats as design details to be determined rather than known facts. (Source: PH-009, PH-011, PH-012, PH-013, PH-015)

## 4. Functional Requirements

| ID | Requirement | Trigger / Input | System Behavior | Output | Priority | Verification | Source |
| --- | --- | --- | --- | --- | --- | --- | --- |
| FR-001 | The system shall allow visitors to register user accounts. | A visitor enters email, account name, password, confirmed password, and email verification code. | The system sends a verification code and validates registration information; after validation succeeds it creates a user record and converts the visitor into a user; when required fields are missing, email is registered, username is used, passwords mismatch, or verification code is wrong, it prompts the reason. | New user account, login state, or error prompt. | High | Test | PH-009 |
| FR-002 | The system shall allow users to log in. | A visitor enters account name and password and submits login. | The system validates account name and password; after validation succeeds it enters the initial page; when username does not exist or password is wrong, it prompts the reason. | Logged-in user state or error prompt. | High | Test | PH-009 |
| FR-003 | The system shall allow users to log out. | A logged-in user clicks logout. | The system exits the user's login state and changes the identity to visitor. | Visitor state. | High | Test | PH-009 |
| FR-004 | The system shall allow users to change login passwords. | A logged-in user enters original password, new password, and confirmed new password. | The system validates the original password and new-password consistency; after validation succeeds it modifies the user password in the database; when original password is wrong, old and new passwords are the same, or confirmation mismatches, it prompts the reason. | Updated password or error prompt. | High | Test | PH-009 |
| FR-005 | The system shall allow users to recover passwords. | An unauthenticated user enters registered email, new password, confirmed new password, and email verification code. | The system sends a verification code to the email and validates information; after validation succeeds it modifies the user password in the database and enters the home page; when required fields are missing, email does not exist, verification code is wrong, or passwords mismatch, it prompts the reason. | Reset password, home page entry, or error prompt. | High | Test | PH-009 |
| FR-006 | The system shall support viewing a personal home page. | A logged-in user clicks the personal home page entry. | The system loads and displays the user's personal home page. | Personal home page. | Medium | Demonstration | PH-009 |
| FR-007 | The system shall support viewing another user's home page. | A user selects another user's home page entry. | The system enters the selected user's home page. | Other user's home page. | Medium | Demonstration | PH-009 |
| FR-008 | The system shall support viewing user-uploaded artworks. | A user requests to view uploaded artworks from a user home page or artwork entry. | The system queries and displays artworks uploaded by that user. | User-uploaded artwork list. | Medium | Test | PH-009 |
| FR-009 | The system shall support viewing personal favorites. | A logged-in user enters personal favorites. | The system queries and displays the user's favorites. | Personal favorites list. | Medium | Test | PH-009 |
| FR-010 | The system shall support viewing another user's favorites. | A user enters another user's favorites entry. | The system queries and displays the target user's visible favorites. | Other user's favorites list. | Medium | Test | PH-009 |
| FR-011 | The system shall support viewing personal browsing history. | A logged-in user enters browsing history. | The system queries and displays personal browsing history. | Browsing history list. | Medium | Test | PH-009 |
| FR-012 | The system shall support viewing a user's follow list. | A user requests to view a user's follow list. | The system queries and displays the list of users followed by that user. | Follow list. | Medium | Test | PH-009 |
| FR-013 | The system shall support viewing a user's fan list. | A user requests to view a user's fan list. | The system queries and displays that user's fan list. | Fan list. | Medium | Test | PH-009 |
| FR-014 | The system shall support following users. | A logged-in user clicks follow and no such follow record exists in the database. | The system adds a user follow record and refreshes the front-end follow state. | Followed state. | High | Test | PH-009 |
| FR-015 | The system shall support unfollowing users. | A logged-in user clicks unfollow and the follow record exists in the database. | The system deletes the user follow record and refreshes the front-end follow state. | Unfollowed state. | High | Test | PH-009 |
| FR-016 | The system shall support modifying personal avatars. | A logged-in user submits a new avatar. | The system modifies the user avatar in the database and refreshes the user profile. | Updated avatar. | Medium | Test | PH-009 |
| FR-017 | The system shall support modifying personal usernames. | A logged-in user submits a new username. | The system validates and modifies the username in the database. | Updated username or error prompt. | Medium | Test | PH-009 |
| FR-018 | The system shall support administrator login. | A visitor enters administrator login information. | The system validates administrator identity; after validation succeeds, it enters administrator state. | Administrator login state or error prompt. | High | Test | PH-010 |
| FR-019 | The system shall support administrator logout. | A logged-in administrator clicks logout. | The system exits administrator login state. | Non-administrator login state. | High | Test | PH-010 |
| FR-020 | The system shall allow administrators to view the user list. | A logged-in administrator requests the user list. | The system queries and displays the user list. | User list. | High | Test | PH-010 |
| FR-021 | The system shall allow administrators to view the artwork list. | A logged-in administrator requests the artwork list. | The system queries and displays the artwork list. | Artwork list. | High | Test | PH-010 |
| FR-022 | The system shall allow administrators to review uploaded artworks. | A logged-in administrator selects a pending artwork and decides approve or reject. | The system marks the artwork as approved or rejected. | Review result and artwork state. | High | Test | PH-010 |
| FR-023 | The system shall allow administrators to view comments. | A logged-in administrator enters comment management. | The system queries and displays artwork comments. | Comment list. | High | Test | PH-010 |
| FR-024 | The system shall allow administrators to view replies. | A logged-in administrator enters reply management. | The system queries and displays reply content. | Reply list. | High | Test | PH-010 |
| FR-025 | The system shall allow administrators to delete comments. | A logged-in administrator selects comment deletion. | The system deletes the comment record from the database and refreshes the front end. | Page after comment removal. | High | Test | PH-010 |
| FR-026 | The system shall allow administrators to delete replies. | A logged-in administrator selects reply deletion. | The system deletes the reply record from the database and refreshes the front end. | Page after reply removal. | High | Test | PH-010 |
| FR-027 | The system shall allow users to upload artworks. | A logged-in user uploads an AI-generated image, Prompt, model, category, and additional information. | The system inserts uploaded artwork information into the artwork review queue visible to administrators and marks the review record as in progress. | Pending artwork record and review progress. | High | Test | PH-011 |
| FR-028 | The system shall allow users to edit uploaded artworks. | A logged-in user edits artwork content they uploaded. | The system allows the user to edit information such as AI-generated image and Prompt, inserts the edited artwork into the review queue, and marks the review record as in progress; users can only edit artworks they successfully uploaded. | Updated pending artwork record. | High | Test | PH-011 |
| FR-029 | The system shall allow users to delete uploaded artworks. | A logged-in user deletes an artwork they uploaded. | The system deletes content related to the user's own artwork. | Artwork deletion result. | High | Test | PH-011 |
| FR-030 | The system shall support artwork query. | A visitor or user enters Prompt keywords or tags and may choose sorting and filtering rules. | The system obtains corresponding artworks from the database according to input information and sorting/filtering rules such as popularity, upload time, and model. | Query result list. | High | Test | PH-011 |
| FR-031 | The system shall support viewing artwork details. | A visitor or user enters the artwork detail interface. | The system obtains artwork image, Prompt, AI model used, tag/category, uploader, additional information, comments, and replies from the database; when the artwork has been deleted, it enters a 404 page and prompts that details were not found. | Artwork details or 404 prompt. | High | Test | PH-011 |
| FR-032 | The system shall support querying review progress for uploaded artworks. | A logged-in user requests to view review progress for uploaded artworks. | The system queries and displays review progress for artworks uploaded by the user. | Review progress information. | High | Test | PH-011 |
| FR-033 | The system shall support adding favorites. | A logged-in user selects a liked image and adds it to favorites. | The system stores the image favorite relationship in the database. | Favorite success state. | High | Test | PH-012 |
| FR-034 | The system shall support creating public favorite categories. | A logged-in user creates a public favorite category on the favorite management page. | The system records favorite category information; when there are too many categories or a duplicate name, it prompts the user to delete extra favorites or rename. | New public favorite category or error prompt. | Medium | Test | PH-012 |
| FR-035 | The system shall support creating private favorite categories. | A logged-in user creates a private favorite category on the favorite management page. | The system records favorite category information; when there are too many categories or a duplicate name, it prompts the user to delete extra favorites or rename. | New private favorite category or error prompt. | Medium | Test | PH-012 |
| FR-036 | The system shall support viewing favorites. | A logged-in user enters the favorite viewing page. | The system queries and displays the user's favorite content. | Favorite list. | Medium | Test | PH-012 |
| FR-037 | The system shall support canceling favorites. | A logged-in user cancels favorite for an already favorited artwork. | The system deletes the corresponding favorite information from the database. | Favorite removal result. | Medium | Test | PH-012 |
| FR-038 | The system shall support querying favorites. | A logged-in user enters favorite query conditions. | The system queries and displays matching favorite content. | Favorite query result. | Medium | Test | PH-012 |
| FR-039 | The system shall support creating new favorite categories. | A logged-in user creates a new favorite category. | The system records the new favorite category in the database. | New favorite category. | Medium | Test | PH-012 |
| FR-040 | The system shall support deleting favorite categories. | A logged-in user deletes an existing favorite category. | The system deletes the favorite category from the database. | Category deletion result. | Medium | Test | PH-012 |
| FR-041 | The system shall support renaming favorite categories. | A logged-in user submits a new favorite category name. | The system modifies the favorite category name in the database; when the name is invalid, it prompts the user to choose another name. | Updated category name or error prompt. | Medium | Test | PH-012 |
| FR-042 | The system shall support modifying favorite category visibility. | A logged-in user chooses to modify favorite category visibility. | The system modifies the visibility of the favorite category in the database. | Updated visibility. | Medium | Test | PH-012 |
| FR-043 | The system shall allow users to comment on artworks. | A logged-in user submits a comment on an existing artwork detail page. | The system associates the comment content with the artwork and stores it in the database; if the artwork has been deleted, commenting fails. | New comment or failure prompt. | High | Test | PH-013 |
| FR-044 | The system shall allow users to delete their own artwork comments. | A logged-in user chooses to delete their own comment. | The system deletes the comment from the database; deletion fails when the artwork or comment does not exist. | Comment deletion result or failure prompt. | High | Test | PH-013 |
| FR-045 | The system shall allow users to reply to comments or replies. | A logged-in user submits a reply to an existing comment or reply. | The system associates the reply with the artwork, comment, or parent reply and stores it in the database; reply fails when related objects do not exist. | New reply or failure prompt. | High | Test | PH-013 |
| FR-046 | The system shall allow users to delete their own replies. | A logged-in user chooses to delete their own reply. | The system deletes the reply from the database; deletion fails when the artwork, comment, or reply does not exist. | Reply deletion result or failure prompt. | High | Test | PH-013 |
| FR-047 | The system shall support popular recommendation. | A user or visitor clicks popular recommendation on the main interface. | The system sorts recent artworks by descending popularity and displays them. | Popular artwork list. | High | Test | PH-014 |
| FR-048 | The system shall support personalized recommendation. | A registered and logged-in user clicks personalized recommendation. | The system executes the recommendation algorithm and displays personalized recommended artworks; when the user is not logged in or personalized recommendation is not enabled, it prompts and handles the condition. | Personalized artwork list or prompt. | High | Test | PH-014 |
| FR-049 | The system shall support disabling personalized recommendation. | A logged-in user with personalized recommendation enabled clicks disable. | The system disables personalized recommendation; when the user is not logged in or it is already disabled, it prompts. | Recommendation preference disabled state or prompt. | Medium | Test | PH-014 |
| FR-050 | The system shall support adding notification messages. | A user comment, reply, or artwork review progress update event completes. | The system listens to the event, adds an unread notification associated with the corresponding user, and increments the unread notification count by 1. | Unread notification record and count update. | High | Test | PH-015 |
| FR-051 | The system shall support marking notification messages as read. | A logged-in user views an unread notification. | The system updates the message state in the database to read and decrements unread notification count by 1. | Read notification state and count update. | Medium | Test | PH-015 |
| FR-052 | The system shall support deleting notification messages. | A logged-in user selects a notification to delete in the notification interface. | The system deletes the message from the database and removes it from the notification interface. | Notification deletion result. | Medium | Test | PH-015 |

## 5. Non-Functional Requirements

| ID | Quality | Requirement | Fit Criterion | Priority | Verification | Source |
| --- | --- | --- | --- | --- | --- | --- |
| NFR-001 | Performance | Services such as account management, likes, and favorite management shall respond quickly. | Login, registration, likes, account management, and favorite management service response time does not exceed 0.5 seconds. | High | Test | PH-016 |
| NFR-002 | Performance | Image display shall respond quickly. | Each image display remains within 0.5 seconds. | High | Test | PH-016 |
| NFR-003 | Performance | For images that can be loaded as streams and do not need to be displayed all at once, the system may use a longer loading process. | The test report shall distinguish ordinary image display from streaming loading scenarios. | Medium | Analysis | PH-016 |
| NFR-004 | Reliability | The system single point of failure mean occurrence time shall satisfy the reliability threshold. | Under Docker deployment, mean time to single point failure is greater than 720 hours. | High | Analysis | PH-017 |
| NFR-005 | Reliability | The system shall limit data loss after failure. | Data lost after failure does not exceed 1%. | High | Test | PH-017 |
| NFR-006 | Reliability | The system shall automatically recover and notify developers after an error. | Docker automatically restarts and sends an email alert to developers. | High | Test | PH-017 |
| NFR-007 | Reliability | Persistent user data shall have offsite disaster recovery backups. | After user data is persistently stored, offsite disaster recovery backups exist. | High | Inspection | PH-017 |
| NFR-008 | Reliability | Server disk usage shall be controlled. | Server disk usage is below 80%; when the threshold is reached, operations staff are reminded to expand capacity. | High | Test | PH-017 |
| NFR-009 | Security | Web requests and user operations shall be protected. | Secure HTTP requests are used, and user operations are authenticated. | High | Test | PH-018 |
| NFR-010 | Security | The server shall prevent common Web attacks. | Firewall and cross-origin access control are enabled, and illegal links, XSS, and SQL injection are prohibited. | High | Test | PH-018 |
| NFR-011 | Security | Source dependencies shall undergo vulnerability checks. | Well-known vulnerability scanning tools are used to inspect source code, and packages with security vulnerabilities are prohibited. | High | Inspection | PH-018 |
| NFR-012 | Security | User sensitive data shall be encrypted and protected. | End-to-end encryption is used, and both server and client encrypt stored user sensitive data. | High | Test | PH-018 |
| NFR-013 | Security | Front-end publishing and back-end validation shall reduce malicious tampering risk. | The front end is published after obfuscation and source compression, and all data is revalidated on the back end. | High | Inspection | PH-018 |
| NFR-014 | Security | Internal personnel shall not disseminate source code or user data. | Developers must not disseminate source code or user data. | High | Inspection | PH-018 |
| NFR-015 | Maintainability | Project documents shall be clear, readable, and uniformly standardized. | Requirements, design, testing, and related documents pass standardization checks. | Medium | Inspection | PH-019 |
| NFR-016 | Maintainability | System logs shall support fault localization. | All logs are backed up and stored, and error occurrence time can be located from logs. | High | Test | PH-019 |
| NFR-017 | Maintainability | Product development shall be organized by modules. | Modules have high cohesion and low coupling and support later extension. | High | Inspection | PH-019 |
| NFR-018 | Usability | Interaction design shall reduce user operation cost. | Users can obtain target information in three clicks or fewer, most operations can be completed using only the mouse, and user habits can be recorded through cookies. | Medium | Demonstration | PH-020 |
| NFR-019 | UI Design | Interface design shall be unified, responsive, and information-hierarchical. | Style is unified, layout is responsive, information hierarchy is clear, icons are concise and intuitive, colors are consistent and harmonious, and text uses mature open-source fonts. | Medium | Inspection | PH-021 |

## 6. Data Requirements

| ID | Data Object | Requirement | Rationale / Constraint | Verification | Source |
| --- | --- | --- | --- | --- | --- |
| DR-001 | User account | The system shall save account data such as email, account name, password, avatar, username, and account login state. | Supports registration, login, password change, password recovery, avatar modification, and username modification. | Test | PH-009 |
| DR-002 | Administrator account | The system shall save administrator authentication state and identity data required for administrator operations. | Supports administrator login, logout, review, and content management. | Test | PH-010 |
| DR-003 | AI artwork | The system shall save AI-generated image, Prompt, model used, category, tags, uploader, and additional information. | Supports artwork upload, editing, detail display, search, and review. | Test | PH-011 |
| DR-004 | Review record | The system shall save the artwork review queue, review progress, and approval or rejection result. | Users need to query review progress, and administrators need to review uploaded artworks. | Test | PH-010, PH-011 |
| DR-005 | Query and sorting conditions | The system shall process query, sorting, and filtering data such as Prompt keywords, tags, popularity, upload time, and model. | Supports artwork categorization and retrieval. | Test | PH-011 |
| DR-006 | Comment | The system shall save comment content, commenting user, associated artwork, and deletion state. | Supports commenting on artworks, viewing comments, deleting comments, and triggering notifications. | Test | PH-013, PH-015 |
| DR-007 | Reply | The system shall save reply content, replying user, associated artwork, associated comment, or parent reply. | Supports user replies, administrator reply viewing, reply deletion, and notification triggering. | Test | PH-013, PH-015 |
| DR-008 | Favorite | The system shall save favorite relationships between users and artworks. | Supports adding, viewing, querying, and canceling favorites. | Test | PH-012 |
| DR-009 | Favorite category | The system shall save favorite category name, public or private visibility, and owning user. | Supports public favorites, private favorites, category creation, deletion, renaming, and visibility modification. | Test | PH-012 |
| DR-010 | Follow relationship | The system shall save follow records between users. | Supports follow, unfollow, follow lists, and fan lists. | Test | PH-009 |
| DR-011 | Browsing history | The system shall save user browsing history. | Supports users viewing personal browsing history and personalized services. | Test | PH-007, PH-009 |
| DR-012 | Recommendation signals and preferences | The system shall process visited images, liked images, favorited Prompts, follow relationships, browsing history, and personalized recommendation switches. | Supports popular recommendation, personalized recommendation, and disabling recommendation. | Analysis | PH-014, PH-020 |
| DR-013 | Notification message | The system shall save notification content, associated user, unread/read state, and deletion state. | Supports adding notifications, marking messages as read, and deleting notifications. | Test | PH-015 |
| DR-014 | Log | The system shall back up and store logs and retain error occurrence time. | Supports fault localization and maintainability. | Inspection | PH-019 |
| DR-015 | Sensitive data | The system shall store user sensitive data encrypted and revalidate data received by the back end. | Supports security and confidentiality requirements. | Test | PH-018 |

## 7. Constraints

| ID | Constraint | Evidence Type | Source |
| --- | --- | --- | --- |
| C-001 | Requirement changes must strictly follow the requirement change process, and the requirements specification must be reasonably modified and reviewed. | explicit | PH-004 |
| C-002 | The project development process must strictly follow the experiment plan. | explicit | PH-004 |
| C-003 | During runtime, the system needs to limit simultaneous access volume to ensure safe and stable operation. | explicit | PH-004 |
| C-004 | The front end is developed with HTML, CSS, JavaScript, and frameworks such as Vue and JQuery. | explicit | PH-004 |
| C-005 | The back end is developed with Python, Java, and the Django framework. | explicit | PH-004 |
| C-006 | The algorithm support module is developed with Python and frameworks such as PyTorch and TensorFlow. | explicit | PH-004 |
| C-007 | Because of runtime environment constraints, the back-end database uses SQLite; later high-concurrency scenarios may migrate to databases such as MySQL. | explicit | PH-001 |
| C-008 | Client operating systems support GUI operating systems based on Windows 7 and macOS 8.0 or above kernels. | explicit | PH-005 |
| C-009 | Client browsers must satisfy requirements such as Firefox 119.0 or above or Chromium 110.0 or above. | explicit | PH-005, PH-022 |
| C-010 | When users cannot connect to the network, all requirements cannot be realized. | explicit | PH-005 |
| C-011 | Minimum client hardware is 8th Generation Intel Core i7, NVIDIA GeForce MX250, and 4 GB memory. | explicit | PH-022 |
| C-012 | Recommended server configuration is Intel Core i5-10600K or above, NVIDIA GeForce GTX 2060 or above, and 32 GB memory or above. | explicit | PH-022 |
| C-013 | Server software environment is Ubuntu 22.0.4 and Docker 20.10.17. | explicit | PH-022 |

## 8. Verification and Acceptance

| ID | Verification | Acceptance Criterion |
| --- | --- | --- |
| FR-001 | Test | A visitor can complete registration, and abnormal input returns the corresponding error prompt. |
| FR-002 | Test | Correct account and password login succeeds, and wrong account or password prompts the failure reason. |
| FR-003 | Test | A logged-in user becomes a visitor after logout. |
| FR-004 | Test | Password is changed after original password and new password validation pass, and wrong input is rejected. |
| FR-005 | Test | Password is reset after email verification-code validation passes, and wrong input is rejected. |
| FR-006 | Demonstration | A logged-in user can open the personal home page. |
| FR-007 | Demonstration | A user can open another user's home page. |
| FR-008 | Test | The system displays the specified user's uploaded artwork list. |
| FR-009 | Test | The system displays personal favorites. |
| FR-010 | Test | The system displays another user's visible favorites. |
| FR-011 | Test | The system displays personal browsing history. |
| FR-012 | Test | The system displays a user's follow list. |
| FR-013 | Test | The system displays a user's fan list. |
| FR-014 | Test | Follow operation adds a follow record and updates front-end state. |
| FR-015 | Test | Unfollow operation deletes the follow record and updates front-end state. |
| FR-016 | Test | User avatar can be changed and the new avatar is displayed. |
| FR-017 | Test | Username can be changed or validation error is returned. |
| FR-018 | Test | Administrator logs in successfully with correct identity information. |
| FR-019 | Test | Administrator exits administrator state after logout. |
| FR-020 | Test | Administrator can view the user list. |
| FR-021 | Test | Administrator can view the artwork list. |
| FR-022 | Test | Administrator can mark artwork review result as approved or not approved. |
| FR-023 | Test | Administrator can view the comment list. |
| FR-024 | Test | Administrator can view the reply list. |
| FR-025 | Test | After administrator deletes a comment, the front end no longer displays that comment. |
| FR-026 | Test | After administrator deletes a reply, the front end no longer displays that reply. |
| FR-027 | Test | After artwork upload, the artwork enters the review queue and progress is in progress. |
| FR-028 | Test | Users can only edit artworks they successfully uploaded, and edited artworks enter the review queue. |
| FR-029 | Test | Users can delete artworks they uploaded. |
| FR-030 | Test | Search, sorting, and filtering conditions return matching artwork lists. |
| FR-031 | Test | Artwork details display complete information, and deleted artworks enter a 404 prompt. |
| FR-032 | Test | Users can view review progress for artworks they uploaded. |
| FR-033 | Test | Users can add artworks to favorites. |
| FR-034 | Test | Users can create public favorite categories and receive prompts for duplicate or excessive categories. |
| FR-035 | Test | Users can create private favorite categories and receive prompts for duplicate or excessive categories. |
| FR-036 | Test | Users can view favorite content. |
| FR-037 | Test | Users can cancel favorites and delete favorite relationships. |
| FR-038 | Test | Users can query favorite content. |
| FR-039 | Test | Users can create new favorite categories. |
| FR-040 | Test | Users can delete favorite categories. |
| FR-041 | Test | Users can modify favorite category names, and invalid names are rejected. |
| FR-042 | Test | Users can modify favorite category visibility. |
| FR-043 | Test | Comments are saved and displayed; commenting fails when the artwork does not exist. |
| FR-044 | Test | Users can delete their own comments; deletion fails when related objects do not exist. |
| FR-045 | Test | Replies are saved and displayed; reply fails when related objects do not exist. |
| FR-046 | Test | Users can delete their own replies; deletion fails when related objects do not exist. |
| FR-047 | Test | Popular recommendation displays recent artworks in descending popularity order. |
| FR-048 | Test | Logged-in users with recommendation enabled can view personalized recommendation, and abnormal states receive prompts. |
| FR-049 | Test | Users can disable personalized recommendation. |
| FR-050 | Test | Unread notifications are added after comments, replies, or review progress updates. |
| FR-051 | Test | After a user views an unread notification, the message becomes read and unread count decreases. |
| FR-052 | Test | After a user deletes a notification, it is removed from the database and interface. |
| NFR-001 | Test | Account management, like, and favorite management service response time does not exceed 0.5 seconds. |
| NFR-002 | Test | Each image displays within 0.5 seconds. |
| NFR-003 | Analysis | Streaming image loading scenarios are separately explained in the performance report. |
| NFR-004 | Analysis | Mean time to single point failure is greater than 720 hours. |
| NFR-005 | Test | Data loss after failure does not exceed 1%. |
| NFR-006 | Test | Docker automatically restarts and sends an email alert after an error. |
| NFR-007 | Inspection | Persistent user data has offsite disaster recovery backup. |
| NFR-008 | Test | Capacity expansion reminder is triggered when disk usage reaches threshold, and normal operation remains below 80%. |
| NFR-009 | Test | Secure HTTP requests and user operation authentication are effective. |
| NFR-010 | Test | Firewall, cross-origin control, XSS protection, and SQL injection protection pass security tests. |
| NFR-011 | Inspection | Source dependency vulnerability detection report contains no forbidden vulnerable packages. |
| NFR-012 | Test | User sensitive data is encrypted during both transmission and storage. |
| NFR-013 | Inspection | Front-end release artifacts are obfuscated and compressed, and back-end data revalidation is performed. |
| NFR-014 | Inspection | Internal security requirements prohibiting developers from disseminating source code and user data are recorded and enforced. |
| NFR-015 | Inspection | Project documents are clear, readable, and uniformly standardized. |
| NFR-016 | Test | Log backups can be used to locate error occurrence time. |
| NFR-017 | Inspection | Module boundaries are clear, with high-cohesion and low-coupling design descriptions. |
| NFR-018 | Demonstration | Target information can be reached in three clicks or fewer, and most operations can be completed with mouse only. |
| NFR-019 | Inspection | The interface satisfies unified style, responsive layout, hierarchy, icon, color, and font requirements. |
| DR-001 | Test | User account data can be created, updated, and read. |
| DR-002 | Test | Administrator identity data can support administrator login and management operations. |
| DR-003 | Test | AI artwork data can be uploaded, edited, displayed, and queried. |
| DR-004 | Test | Review records can save progress and result. |
| DR-005 | Test | Query and sorting/filtering data can drive artwork search. |
| DR-006 | Test | Comment data can be saved, displayed, and deleted. |
| DR-007 | Test | Reply data can be saved, displayed, and deleted. |
| DR-008 | Test | Favorite relationships can be saved and deleted. |
| DR-009 | Test | Favorite category names and visibility can be saved and modified. |
| DR-010 | Test | Follow relationships can be added, deleted, and queried. |
| DR-011 | Test | Browsing history can be saved and viewed. |
| DR-012 | Analysis | Recommendation signals and preferences can explain recommendation input sources. |
| DR-013 | Test | Notification messages can be added, marked read, and deleted. |
| DR-014 | Inspection | Log backups can be checked and used for error localization. |
| DR-015 | Test | Sensitive data encryption and back-end revalidation can be verified. |
| C-001 | Inspection | Requirement change records comply with the change process. |
| C-002 | Inspection | Project plan is consistent with the experiment plan. |
| C-003 | Test | Concurrent access limit strategy is effective. |
| C-004 | Inspection | Front-end technology stack conforms to constraints. |
| C-005 | Inspection | Back-end technology stack conforms to constraints. |
| C-006 | Inspection | Algorithm support module technology stack conforms to constraints. |
| C-007 | Inspection | Database selection and migration assumptions are recorded. |
| C-008 | Inspection | Client operating system scope conforms to constraints. |
| C-009 | Inspection | Browser version satisfies constraints. |
| C-010 | Test | Behavior when system requirements are unavailable without network connection is tested or documented. |
| C-011 | Inspection | Minimum client hardware configuration is recorded. |
| C-012 | Inspection | Recommended server hardware configuration is recorded. |
| C-013 | Inspection | Server software environment conforms to Ubuntu 22.0.4 and Docker 20.10.17. |

## 9. Traceability Matrix

| ID | Requirement | Type | Source | Evidence Type | Verification | Confidence |
| --- | --- | --- | --- | --- | --- | --- |
| FR-001 | User registration | Functional | PH-009 | explicit | Test | High |
| FR-002 | User login | Functional | PH-009 | explicit | Test | High |
| FR-003 | User logout | Functional | PH-009 | explicit | Test | High |
| FR-004 | Change password | Functional | PH-009 | explicit | Test | High |
| FR-005 | Recover password | Functional | PH-009 | explicit | Test | High |
| FR-006 | View personal home page | Functional | PH-009 | explicit | Demonstration | High |
| FR-007 | View other user home page | Functional | PH-009 | explicit | Demonstration | High |
| FR-008 | View user-uploaded artworks | Functional | PH-009 | explicit | Test | High |
| FR-009 | View personal favorites | Functional | PH-009 | explicit | Test | High |
| FR-010 | View other user favorites | Functional | PH-009 | explicit | Test | High |
| FR-011 | View personal browsing history | Functional | PH-009 | explicit | Test | High |
| FR-012 | View user follow list | Functional | PH-009 | explicit | Test | High |
| FR-013 | View user fan list | Functional | PH-009 | explicit | Test | High |
| FR-014 | Follow user | Functional | PH-009 | explicit | Test | High |
| FR-015 | Unfollow user | Functional | PH-009 | explicit | Test | High |
| FR-016 | Modify personal avatar | Functional | PH-009 | explicit | Test | High |
| FR-017 | Modify personal username | Functional | PH-009 | explicit | Test | High |
| FR-018 | Administrator login | Functional | PH-010 | explicit | Test | High |
| FR-019 | Administrator logout | Functional | PH-010 | explicit | Test | High |
| FR-020 | View user list | Functional | PH-010 | explicit | Test | High |
| FR-021 | View artwork list | Functional | PH-010 | explicit | Test | High |
| FR-022 | Review uploaded artwork | Functional | PH-010 | explicit | Test | High |
| FR-023 | Administrator views comments | Functional | PH-010 | explicit | Test | High |
| FR-024 | Administrator views replies | Functional | PH-010 | explicit | Test | High |
| FR-025 | Administrator deletes comments | Functional | PH-010 | explicit | Test | High |
| FR-026 | Administrator deletes replies | Functional | PH-010 | explicit | Test | High |
| FR-027 | Upload artwork | Functional | PH-011 | explicit | Test | High |
| FR-028 | Edit artwork | Functional | PH-011 | explicit | Test | High |
| FR-029 | Delete artwork | Functional | PH-011 | explicit | Test | High |
| FR-030 | Query artwork | Functional | PH-011 | explicit | Test | High |
| FR-031 | View artwork details | Functional | PH-011 | explicit | Test | High |
| FR-032 | Query review progress | Functional | PH-011 | explicit | Test | High |
| FR-033 | Add favorite | Functional | PH-012 | explicit | Test | High |
| FR-034 | Create public favorite category | Functional | PH-012 | explicit | Test | High |
| FR-035 | Create private favorite category | Functional | PH-012 | explicit | Test | High |
| FR-036 | View favorites | Functional | PH-012 | explicit | Test | High |
| FR-037 | Cancel favorite | Functional | PH-012 | explicit | Test | High |
| FR-038 | Query favorites | Functional | PH-012 | explicit | Test | High |
| FR-039 | Create favorite category | Functional | PH-012 | explicit | Test | High |
| FR-040 | Delete favorite category | Functional | PH-012 | explicit | Test | High |
| FR-041 | Rename favorite category | Functional | PH-012 | explicit | Test | High |
| FR-042 | Modify favorite category visibility | Functional | PH-012 | explicit | Test | High |
| FR-043 | Comment on artwork | Functional | PH-013 | explicit | Test | High |
| FR-044 | Delete comment | Functional | PH-013 | explicit | Test | High |
| FR-045 | Reply to comment | Functional | PH-013 | explicit | Test | High |
| FR-046 | Delete reply | Functional | PH-013 | explicit | Test | High |
| FR-047 | Popular recommendation | Functional | PH-014 | explicit | Test | High |
| FR-048 | Personalized recommendation | Functional | PH-014 | explicit | Test | High |
| FR-049 | Disable personalized recommendation | Functional | PH-014 | explicit | Test | High |
| FR-050 | Add notification | Functional | PH-015 | explicit | Test | High |
| FR-051 | Mark message read | Functional | PH-015 | explicit | Test | High |
| FR-052 | Delete message | Functional | PH-015 | explicit | Test | High |
| NFR-001 | Account and favorite service response time | Non-functional | PH-016 | explicit | Test | High |
| NFR-002 | Image display response time | Non-functional | PH-016 | explicit | Test | High |
| NFR-003 | Streaming image loading note | Non-functional | PH-016 | explicit | Analysis | Medium |
| NFR-004 | Mean time to single point failure | Non-functional | PH-017 | explicit | Analysis | High |
| NFR-005 | Data loss limit after failure | Non-functional | PH-017 | explicit | Test | High |
| NFR-006 | Docker automatic restart and email alert | Non-functional | PH-017 | explicit | Test | High |
| NFR-007 | Offsite disaster recovery backup | Non-functional | PH-017 | explicit | Inspection | High |
| NFR-008 | Disk usage threshold reminder | Non-functional | PH-017 | explicit | Test | High |
| NFR-009 | Secure HTTP and authentication | Non-functional | PH-018 | explicit | Test | High |
| NFR-010 | Web attack protection | Non-functional | PH-018 | explicit | Test | High |
| NFR-011 | Vulnerability scanning | Non-functional | PH-018 | explicit | Inspection | High |
| NFR-012 | Sensitive data encryption | Non-functional | PH-018 | explicit | Test | High |
| NFR-013 | Front-end obfuscation and back-end revalidation | Non-functional | PH-018 | explicit | Inspection | High |
| NFR-014 | Internal security constraint | Non-functional | PH-018 | explicit | Inspection | High |
| NFR-015 | Document standardization | Non-functional | PH-019 | explicit | Inspection | High |
| NFR-016 | Log backup and fault localization | Non-functional | PH-019 | explicit | Test | High |
| NFR-017 | High cohesion and low coupling modules | Non-functional | PH-019 | explicit | Inspection | High |
| NFR-018 | Interaction operation cost | Non-functional | PH-020 | explicit | Demonstration | High |
| NFR-019 | Interface design consistency | Non-functional | PH-021 | explicit | Inspection | High |
| DR-001 | User account data | Data | PH-009 | explicit | Test | High |
| DR-002 | Administrator account data | Data | PH-010 | explicit | Test | High |
| DR-003 | AI artwork data | Data | PH-011 | explicit | Test | High |
| DR-004 | Review record | Data | PH-010, PH-011 | explicit | Test | High |
| DR-005 | Query and sorting conditions | Data | PH-011 | explicit | Test | High |
| DR-006 | Comment data | Data | PH-013, PH-015 | explicit | Test | High |
| DR-007 | Reply data | Data | PH-013, PH-015 | explicit | Test | High |
| DR-008 | Favorite data | Data | PH-012 | explicit | Test | High |
| DR-009 | Favorite category data | Data | PH-012 | explicit | Test | High |
| DR-010 | Follow relationship data | Data | PH-009 | explicit | Test | High |
| DR-011 | Browsing history data | Data | PH-007, PH-009 | explicit | Test | High |
| DR-012 | Recommendation signals and preferences | Data | PH-014, PH-020 | explicit | Analysis | Medium |
| DR-013 | Notification message data | Data | PH-015 | explicit | Test | High |
| DR-014 | Log data | Data | PH-019 | explicit | Inspection | High |
| DR-015 | Sensitive data | Data | PH-018 | explicit | Test | High |
| C-001 | Requirement change process | Constraint | PH-004 | explicit | Inspection | High |
| C-002 | Experiment plan constraint | Constraint | PH-004 | explicit | Inspection | High |
| C-003 | Simultaneous access limit | Constraint | PH-004 | explicit | Test | High |
| C-004 | Front-end technology stack | Constraint | PH-004 | explicit | Inspection | High |
| C-005 | Back-end technology stack | Constraint | PH-004 | explicit | Inspection | High |
| C-006 | Algorithm technology stack | Constraint | PH-004 | explicit | Inspection | High |
| C-007 | SQLite database and migration assumption | Constraint | PH-001 | explicit | Inspection | High |
| C-008 | Client operating system | Constraint | PH-005 | explicit | Inspection | High |
| C-009 | Client browser version | Constraint | PH-005, PH-022 | explicit | Inspection | High |
| C-010 | Network dependency | Constraint | PH-005 | explicit | Test | High |
| C-011 | Minimum client hardware | Constraint | PH-022 | explicit | Inspection | High |
| C-012 | Recommended server hardware | Constraint | PH-022 | explicit | Inspection | High |
| C-013 | Server software environment | Constraint | PH-022 | explicit | Inspection | High |
