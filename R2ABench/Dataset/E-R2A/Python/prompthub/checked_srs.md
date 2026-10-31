# PromptHub Software Requirements Specification (Standard SRS Extract)

## 1. Introduction

### Product Scope

PromptHub is a community Web application for sharing AI artworks and Prompts. The system scope includes AI artwork browsing and discussion, artwork categorization and retrieval, user artwork upload and administrator review, user profile and relationship management, favorite management, comments and replies, popular and personalized recommendations, notifications, and the front-end, back-end, algorithm support, and data persistence capabilities that support these functions.

This document follows the terminology definitions in the requirements specification for AIGC, Prompt, Vue.js, Django, SQLite, and Docker. The specification does not define API paths, database table structures, or concrete data exchange formats.

### Intended Audience

This document is intended for PromptHub developers, testers, project managers, requirements reviewers, later architecture generation workflows, and stakeholders who need to understand requirement coverage.

## 2. Overall Description

### Product Perspective

PromptHub is a community Web application composed of three major modules: front end, back end, and algorithm support. The front end handles user interaction and artwork display. The back end handles business services such as users, artworks, favorites, comments, review, and notifications. The algorithm support module handles recommendation capabilities. The specification explicitly constrains the technology stack to Vue/JQuery, Django, SQLite, Docker, PyTorch/TensorFlow, and related technologies, but does not expand concrete deployment topology, API routes, or database ER model.

### Product Functions Summary

| Capability | Summary |
| --- | --- |
| Artwork browsing and discussion | The home page displays AI artworks, and artwork details display Prompt, model, creator, comments, and replies. |
| Categorization, retrieval, and sorting | Users or visitors can query artworks by Prompt keywords, tags, popularity, upload time, model, and other conditions. |
| Upload and review | Users upload AI-generated images, Prompts, models, categories, and additional information, and administrators approve or reject them after review. |
| User and relationship management | Supports registration, login, password maintenance, personal home pages, avatars/usernames, follow relationships, fans, and browsing history. |
| Favorite management | Supports artwork favorites, public and private favorite categories, favorite queries, category deletion, and category modification. |
| Recommendation and notification | Supports popular recommendation, personalized recommendation, disabling personalized recommendation, and notifications for comments, replies, and review progress changes. |
| Administration and content governance | Administrators view users and artworks, review uploaded artworks, and view and delete comments and replies. |

### User Classes

| User Class | Responsibilities / Needs |
| --- | --- |
| Visitor | Browses AI artworks and Prompts, views popular recommendations, queries artworks and artwork details, and can register as a user. |
| Registered user | Manages account profile, artworks, favorites, comments, follows, recommendation preferences, browsing history, and system notifications. |
| Administrator | Maintains community content and environment, views users and artworks, reviews uploaded artworks, and manages comments and replies. |
| AI artwork creator | Uploads their own AI artworks, Prompts, and model information for other users to browse. |
| AI artwork viewer and newcomer | Browses categorized works and asks questions or communicates in comments to learn about AI painting. |

### Operating Environment

| Environment | Requirement |
| --- | --- |
| Minimum client hardware | CPU: 8th Generation Intel Core i7; GPU: NVIDIA GeForce MX250; memory: 4 GB. |
| Recommended client hardware | CPU: Intel Core i5-10600K or above; GPU: NVIDIA GeForce GTX 1060 or above; memory: 16 GB or above. |
| Client software | Chrome 110.0.5481.178 or above, Safari 15.3 or above, Firefox 119.0 or above; the specification also states support for GUI operating systems based on Windows 7 and macOS 8.0 or above kernels. |
| Server hardware | CPU: Intel Core i5-10600K or above; GPU: NVIDIA GeForce GTX 2060 or above; memory: 32 GB or above. |
| Server software | Ubuntu 22.0.4 and Docker 20.10.17. |
| Network | When users cannot connect to the network, all requirements cannot be realized. |

### Assumptions and Dependencies

| ID | Assumption / Dependency |
| --- | --- |
| AD-001 | System functions depend on user network connectivity. |
| AD-002 | Project development depends on the experiment plan and requirement change process. |
| AD-003 | During runtime, the system needs to limit simultaneous access volume to ensure safe and stable operation. |
| AD-004 | SQLite is adopted because of runtime environment constraints, and later high-concurrency scenarios may migrate to databases such as MySQL. |
| AD-005 | The specification contains use case and activity diagrams, but this document extracts only textual requirements; details not expanded in the diagrams are not invented. |

## 3. External Interface Requirements

### User Interfaces

| Interface | Requirement |
| --- | --- |
| Home page and artwork list interface | Displays AI artworks and supports popular recommendation, personalized recommendation entry, search, sorting, and filtering. |
| Registration, login, and account interface | Supports registration, login, logout, password change, password recovery, avatar change, and username change. |
| Artwork detail interface | Displays artwork image, Prompt, AI model, tag/category, uploader, additional information, comments, and replies. |
| Upload and edit interface | Supports users uploading or editing AI images, Prompts, models, categories, and additional information, and entering the review flow. |
| Favorite management interface | Supports favorite, public/private favorite categories, viewing, querying, cancellation, deletion, and favorite category modification. |
| Administrator interface | Supports administrators viewing user and artwork lists, reviewing uploaded artworks, and viewing and deleting comments and replies. |
| Notification interface | Supports displaying unread notifications, marking them as read, and deleting notifications. |

### Software/API Interfaces

| Interface | Requirement |
| --- | --- |
| Front-end module | The front end shall be developed with HTML, CSS, JavaScript, and frameworks such as Vue and JQuery. |
| Back-end module | The back end shall be developed with Python, Java, and the Django framework. |
| Algorithm support module | The algorithm support module shall use Python and frameworks such as PyTorch and TensorFlow. |
| SQLite database | The system uses lightweight SQLite as the back-end database; later high-concurrency scenarios may migrate to databases such as MySQL. |
| Docker runtime environment | The server runtime environment specifies Docker 20.10.17, and reliability requirements also assume Docker deployment. |

### Communication Interfaces

The specification requires Web pages to use secure HTTP requests, authenticate user operations, enable firewalls and cross-origin access control on the server, and prevent illegal links, XSS, and SQL injection. The specification does not provide REST, RPC, WebSocket, or message queue protocol details.

### Data Exchange Formats

The specification explicitly identifies data objects and interaction content, including account information, AI-generated images, Prompt, model, category, tags, artwork additional information, comments, replies, favorites, follows, browsing history, review progress, and notifications. It does not specify JSON, forms, multimedia upload, or database field formats. Implementation and review should mark unspecified formats as design details to be determined rather than known facts.

## 4. Functional Requirements

| ID | Requirement | Trigger / Input | System Behavior | Output | Priority | Verification |
| --- | --- | --- | --- | --- | --- | --- |
| FR-001 | The system shall allow visitors to register user accounts. | A visitor enters email, account name, password, confirmed password, and email verification code. | The system sends a verification code and validates registration information; after validation succeeds it creates a user record and converts the visitor into a user; when required fields are missing, email is registered, username is used, passwords mismatch, or verification code is wrong, it prompts the reason. | New user account, login state, or error prompt. | High | Test |
| FR-002 | The system shall allow users to log in. | A visitor enters account name and password and submits login. | The system validates account name and password; after validation succeeds it enters the initial page; when username does not exist or password is wrong, it prompts the reason. | Logged-in user state or error prompt. | High | Test |
| FR-003 | The system shall allow users to log out. | A logged-in user clicks logout. | The system exits the user's login state and changes the identity to visitor. | Visitor state. | High | Test |
| FR-004 | The system shall allow users to change login passwords. | A logged-in user enters original password, new password, and confirmed new password. | The system validates the original password and new-password consistency; after validation succeeds it modifies the user password in the database; when original password is wrong, old and new passwords are the same, or confirmation mismatches, it prompts the reason. | Updated password or error prompt. | High | Test |
| FR-005 | The system shall allow users to recover passwords. | An unauthenticated user enters registered email, new password, confirmed new password, and email verification code. | The system sends a verification code to the email and validates information; after validation succeeds it modifies the user password in the database and enters the home page; when required fields are missing, email does not exist, verification code is wrong, or passwords mismatch, it prompts the reason. | Reset password, home page entry, or error prompt. | High | Test |
| FR-006 | The system shall support viewing a personal home page. | A logged-in user clicks the personal home page entry. | The system loads and displays the user's personal home page. | Personal home page. | Medium | Demonstration |
| FR-007 | The system shall support viewing another user's home page. | A user selects another user's home page entry. | The system enters the selected user's home page. | Other user's home page. | Medium | Demonstration |
| FR-008 | The system shall support viewing user-uploaded artworks. | A user requests to view uploaded artworks from a user home page or artwork entry. | The system queries and displays artworks uploaded by that user. | User-uploaded artwork list. | Medium | Test |
| FR-009 | The system shall support viewing personal favorites. | A logged-in user enters personal favorites. | The system queries and displays the user's favorites. | Personal favorites list. | Medium | Test |
| FR-010 | The system shall support viewing another user's favorites. | A user enters another user's favorites entry. | The system queries and displays the target user's visible favorites. | Other user's favorites list. | Medium | Test |
| FR-011 | The system shall support viewing personal browsing history. | A logged-in user enters browsing history. | The system queries and displays personal browsing history. | Browsing history list. | Medium | Test |
| FR-012 | The system shall support viewing a user's follow list. | A user requests to view a user's follow list. | The system queries and displays the list of users followed by that user. | Follow list. | Medium | Test |
| FR-013 | The system shall support viewing a user's fan list. | A user requests to view a user's fan list. | The system queries and displays that user's fan list. | Fan list. | Medium | Test |
| FR-014 | The system shall support following users. | A logged-in user clicks follow and no such follow record exists in the database. | The system adds a user follow record and refreshes the front-end follow state. | Followed state. | High | Test |
| FR-015 | The system shall support unfollowing users. | A logged-in user clicks unfollow and the follow record exists in the database. | The system deletes the user follow record and refreshes the front-end follow state. | Unfollowed state. | High | Test |
| FR-016 | The system shall support modifying personal avatars. | A logged-in user submits a new avatar. | The system modifies the user avatar in the database and refreshes the user profile. | Updated avatar. | Medium | Test |
| FR-017 | The system shall support modifying personal usernames. | A logged-in user submits a new username. | The system validates and modifies the username in the database. | Updated username or error prompt. | Medium | Test |
| FR-018 | The system shall support administrator login. | A visitor enters administrator login information. | The system validates administrator identity; after validation succeeds, it enters administrator state. | Administrator login state or error prompt. | High | Test |
| FR-019 | The system shall support administrator logout. | A logged-in administrator clicks logout. | The system exits administrator login state. | Non-administrator login state. | High | Test |
| FR-020 | The system shall allow administrators to view the user list. | A logged-in administrator requests the user list. | The system queries and displays the user list. | User list. | High | Test |
| FR-021 | The system shall allow administrators to view the artwork list. | A logged-in administrator requests the artwork list. | The system queries and displays the artwork list. | Artwork list. | High | Test |
| FR-022 | The system shall allow administrators to review uploaded artworks. | A logged-in administrator selects a pending artwork and decides approve or reject. | The system marks the artwork as approved or rejected. | Review result and artwork state. | High | Test |
| FR-023 | The system shall allow administrators to view comments. | A logged-in administrator enters comment management. | The system queries and displays artwork comments. | Comment list. | High | Test |
| FR-024 | The system shall allow administrators to view replies. | A logged-in administrator enters reply management. | The system queries and displays reply content. | Reply list. | High | Test |
| FR-025 | The system shall allow administrators to delete comments. | A logged-in administrator selects comment deletion. | The system deletes the comment record from the database and refreshes the front end. | Page after comment removal. | High | Test |
| FR-026 | The system shall allow administrators to delete replies. | A logged-in administrator selects reply deletion. | The system deletes the reply record from the database and refreshes the front end. | Page after reply removal. | High | Test |
| FR-027 | The system shall allow users to upload artworks. | A logged-in user uploads an AI-generated image, Prompt, model, category, and additional information. | The system inserts uploaded artwork information into the artwork review queue visible to administrators and marks the review record as in progress. | Pending artwork record and review progress. | High | Test |
| FR-028 | The system shall allow users to edit uploaded artworks. | A logged-in user edits artwork content they uploaded. | The system allows the user to edit information such as AI-generated image and Prompt, inserts the edited artwork into the review queue, and marks the review record as in progress; users can only edit artworks they successfully uploaded. | Updated pending artwork record. | High | Test |
| FR-029 | The system shall allow users to delete uploaded artworks. | A logged-in user deletes an artwork they uploaded. | The system deletes content related to the user's own artwork. | Artwork deletion result. | High | Test |
| FR-030 | The system shall support artwork query. | A visitor or user enters Prompt keywords or tags and may choose sorting and filtering rules. | The system obtains corresponding artworks from the database according to input information and sorting/filtering rules such as popularity, upload time, and model. | Query result list. | High | Test |
| FR-031 | The system shall support viewing artwork details. | A visitor or user enters the artwork detail interface. | The system obtains artwork image, Prompt, AI model used, tag/category, uploader, additional information, comments, and replies from the database; when the artwork has been deleted, it enters a 404 page and prompts that details were not found. | Artwork details or 404 prompt. | High | Test |
| FR-032 | The system shall support querying review progress for uploaded artworks. | A logged-in user requests to view review progress for uploaded artworks. | The system queries and displays review progress for artworks uploaded by the user. | Review progress information. | High | Test |
| FR-033 | The system shall support adding favorites. | A logged-in user selects a liked image and adds it to favorites. | The system stores the image favorite relationship in the database. | Favorite success state. | High | Test |
| FR-034 | The system shall support creating public favorite categories. | A logged-in user creates a public favorite category on the favorite management page. | The system records favorite category information; when there are too many categories or a duplicate name, it prompts the user to delete extra favorites or rename. | New public favorite category or error prompt. | Medium | Test |
| FR-035 | The system shall support creating private favorite categories. | A logged-in user creates a private favorite category on the favorite management page. | The system records favorite category information; when there are too many categories or a duplicate name, it prompts the user to delete extra favorites or rename. | New private favorite category or error prompt. | Medium | Test |
| FR-036 | The system shall support viewing favorites. | A logged-in user enters the favorite viewing page. | The system queries and displays the user's favorite content. | Favorite list. | Medium | Test |
| FR-037 | The system shall support canceling favorites. | A logged-in user cancels favorite for an already favorited artwork. | The system deletes the corresponding favorite information from the database. | Favorite removal result. | Medium | Test |
| FR-038 | The system shall support querying favorites. | A logged-in user enters favorite query conditions. | The system queries and displays matching favorite content. | Favorite query result. | Medium | Test |
| FR-039 | The system shall support creating new favorite categories. | A logged-in user creates a new favorite category. | The system records the new favorite category in the database. | New favorite category. | Medium | Test |
| FR-040 | The system shall support deleting favorite categories. | A logged-in user deletes an existing favorite category. | The system deletes the favorite category from the database. | Category deletion result. | Medium | Test |
| FR-041 | The system shall support renaming favorite categories. | A logged-in user submits a new favorite category name. | The system modifies the favorite category name in the database; when the name is invalid, it prompts the user to choose another name. | Updated category name or error prompt. | Medium | Test |
| FR-042 | The system shall support modifying favorite category visibility. | A logged-in user chooses to modify favorite category visibility. | The system modifies the visibility of the favorite category in the database. | Updated visibility. | Medium | Test |
| FR-043 | The system shall allow users to comment on artworks. | A logged-in user submits a comment on an existing artwork detail page. | The system associates the comment content with the artwork and stores it in the database; if the artwork has been deleted, commenting fails. | New comment or failure prompt. | High | Test |
| FR-044 | The system shall allow users to delete their own artwork comments. | A logged-in user chooses to delete their own comment. | The system deletes the comment from the database; deletion fails when the artwork or comment does not exist. | Comment deletion result or failure prompt. | High | Test |
| FR-045 | The system shall allow users to reply to comments or replies. | A logged-in user submits a reply to an existing comment or reply. | The system associates the reply with the artwork, comment, or parent reply and stores it in the database; reply fails when related objects do not exist. | New reply or failure prompt. | High | Test |
| FR-046 | The system shall allow users to delete their own replies. | A logged-in user chooses to delete their own reply. | The system deletes the reply from the database; deletion fails when the artwork, comment, or reply does not exist. | Reply deletion result or failure prompt. | High | Test |
| FR-047 | The system shall support popular recommendation. | A user or visitor clicks popular recommendation on the main interface. | The system sorts recent artworks by descending popularity and displays them. | Popular artwork list. | High | Test |
| FR-048 | The system shall support personalized recommendation. | A registered and logged-in user clicks personalized recommendation. | The system executes the recommendation algorithm and displays personalized recommended artworks; when the user is not logged in or personalized recommendation is not enabled, it prompts and handles the condition. | Personalized artwork list or prompt. | High | Test |
| FR-049 | The system shall support disabling personalized recommendation. | A logged-in user with personalized recommendation enabled clicks disable. | The system disables personalized recommendation; when the user is not logged in or it is already disabled, it prompts. | Recommendation preference disabled state or prompt. | Medium | Test |
| FR-050 | The system shall support adding notification messages. | A user comment, reply, or artwork review progress update event completes. | The system listens to the event, adds an unread notification associated with the corresponding user, and increments the unread notification count by 1. | Unread notification record and count update. | High | Test |
| FR-051 | The system shall support marking notification messages as read. | A logged-in user views an unread notification. | The system updates the message state in the database to read and decrements unread notification count by 1. | Read notification state and count update. | Medium | Test |
| FR-052 | The system shall support deleting notification messages. | A logged-in user selects a notification to delete in the notification interface. | The system deletes the message from the database and removes it from the notification interface. | Notification deletion result. | Medium | Test |

## 5. Non-Functional Requirements

| ID | Quality | Requirement | Fit Criterion | Priority | Verification |
| --- | --- | --- | --- | --- | --- |
| NFR-001 | Performance | Services such as account management, likes, and favorite management shall respond quickly. | Login, registration, likes, account management, and favorite management service response time does not exceed 0.5 seconds. | High | Test |
| NFR-002 | Performance | Image display shall respond quickly. | Each image display remains within 0.5 seconds. | High | Test |
| NFR-003 | Performance | For images that can be loaded as streams and do not need to be displayed all at once, the system may use a longer loading process. | The test report shall distinguish ordinary image display from streaming loading scenarios. | Medium | Analysis |
| NFR-004 | Reliability | The system single point of failure mean occurrence time shall satisfy the reliability threshold. | Under Docker deployment, mean time to single point failure is greater than 720 hours. | High | Analysis |
| NFR-005 | Reliability | The system shall limit data loss after failure. | Data lost after failure does not exceed 1%. | High | Test |
| NFR-006 | Reliability | The system shall automatically recover and notify developers after an error. | Docker automatically restarts and sends an email alert to developers. | High | Test |
| NFR-007 | Reliability | Persistent user data shall have offsite disaster recovery backups. | After user data is persistently stored, offsite disaster recovery backups exist. | High | Inspection |
| NFR-008 | Reliability | Server disk usage shall be controlled. | Server disk usage is below 80%; when the threshold is reached, operations staff are reminded to expand capacity. | High | Test |
| NFR-009 | Security | Web requests and user operations shall be protected. | Secure HTTP requests are used, and user operations are authenticated. | High | Test |
| NFR-010 | Security | The server shall prevent common Web attacks. | Firewall and cross-origin access control are enabled, and illegal links, XSS, and SQL injection are prohibited. | High | Test |
| NFR-011 | Security | Source dependencies shall undergo vulnerability checks. | Well-known vulnerability scanning tools are used to inspect source code, and packages with security vulnerabilities are prohibited. | High | Inspection |
| NFR-012 | Security | User sensitive data shall be encrypted and protected. | End-to-end encryption is used, and both server and client encrypt stored user sensitive data. | High | Test |
| NFR-013 | Security | Front-end publishing and back-end validation shall reduce malicious tampering risk. | The front end is published after obfuscation and source compression, and all data is revalidated on the back end. | High | Inspection |
| NFR-014 | Security | Internal personnel shall not disseminate source code or user data. | Developers must not disseminate source code or user data. | High | Inspection |
| NFR-015 | Maintainability | Project documents shall be clear, readable, and uniformly standardized. | Requirements, design, testing, and related documents pass standardization checks. | Medium | Inspection |
| NFR-016 | Maintainability | System logs shall support fault localization. | All logs are backed up and stored, and error occurrence time can be located from logs. | High | Test |
| NFR-017 | Maintainability | Product development shall be organized by modules. | Modules have high cohesion and low coupling and support later extension. | High | Inspection |
| NFR-018 | Usability | Interaction design shall reduce user operation cost. | Users can obtain target information in three clicks or fewer, most operations can be completed using only the mouse, and user habits can be recorded through cookies. | Medium | Demonstration |
| NFR-019 | UI Design | Interface design shall be unified, responsive, and information-hierarchical. | Style is unified, layout is responsive, information hierarchy is clear, icons are concise and intuitive, colors are consistent and harmonious, and text uses mature open-source fonts. | Medium | Inspection |

## 6. Data Requirements

| ID | Data Object | Requirement | Rationale / Constraint | Verification |
| --- | --- | --- | --- | --- |
| DR-001 | User account | The system shall save account data such as email, account name, password, avatar, username, and account login state. | Supports registration, login, password change, password recovery, avatar modification, and username modification. | Test |
| DR-002 | Administrator account | The system shall save administrator authentication state and identity data required for administrator operations. | Supports administrator login, logout, review, and content management. | Test |
| DR-003 | AI artwork | The system shall save AI-generated image, Prompt, model used, category, tags, uploader, and additional information. | Supports artwork upload, editing, detail display, search, and review. | Test |
| DR-004 | Review record | The system shall save the artwork review queue, review progress, and approval or rejection result. | Users need to query review progress, and administrators need to review uploaded artworks. | Test |
| DR-005 | Query and sorting conditions | The system shall process query, sorting, and filtering data such as Prompt keywords, tags, popularity, upload time, and model. | Supports artwork categorization and retrieval. | Test |
| DR-006 | Comment | The system shall save comment content, commenting user, associated artwork, and deletion state. | Supports commenting on artworks, viewing comments, deleting comments, and triggering notifications. | Test |
| DR-007 | Reply | The system shall save reply content, replying user, associated artwork, associated comment, or parent reply. | Supports user replies, administrator reply viewing, reply deletion, and notification triggering. | Test |
| DR-008 | Favorite | The system shall save favorite relationships between users and artworks. | Supports adding, viewing, querying, and canceling favorites. | Test |
| DR-009 | Favorite category | The system shall save favorite category name, public or private visibility, and owning user. | Supports public favorites, private favorites, category creation, deletion, renaming, and visibility modification. | Test |
| DR-010 | Follow relationship | The system shall save follow records between users. | Supports follow, unfollow, follow lists, and fan lists. | Test |
| DR-011 | Browsing history | The system shall save user browsing history. | Supports users viewing personal browsing history and personalized services. | Test |
| DR-012 | Recommendation signals and preferences | The system shall process visited images, liked images, favorited Prompts, follow relationships, browsing history, and personalized recommendation switches. | Supports popular recommendation, personalized recommendation, and disabling recommendation. | Analysis |
| DR-013 | Notification message | The system shall save notification content, associated user, unread/read state, and deletion state. | Supports adding notifications, marking messages as read, and deleting notifications. | Test |
| DR-014 | Log | The system shall back up and store logs and retain error occurrence time. | Supports fault localization and maintainability. | Inspection |
| DR-015 | Sensitive data | The system shall store user sensitive data encrypted and revalidate data received by the back end. | Supports security and confidentiality requirements. | Test |

## 7. Constraints

| ID | Constraint |
| --- | --- |
| C-001 | Requirement changes must strictly follow the requirement change process, and the requirements specification must be reasonably modified and reviewed. |
| C-002 | The project development process must strictly follow the experiment plan. |
| C-003 | During runtime, the system needs to limit simultaneous access volume to ensure safe and stable operation. |
| C-004 | The front end is developed with HTML, CSS, JavaScript, and frameworks such as Vue and JQuery. |
| C-005 | The back end is developed with Python, Java, and the Django framework. |
| C-006 | The algorithm support module is developed with Python and frameworks such as PyTorch and TensorFlow. |
| C-007 | Because of runtime environment constraints, the back-end database uses SQLite; later high-concurrency scenarios may migrate to databases such as MySQL. |
| C-008 | Client operating systems support GUI operating systems based on Windows 7 and macOS 8.0 or above kernels. |
| C-009 | Client browsers must satisfy requirements such as Firefox 119.0 or above or Chromium 110.0 or above. |
| C-010 | When users cannot connect to the network, all requirements cannot be realized. |
| C-011 | Minimum client hardware is 8th Generation Intel Core i7, NVIDIA GeForce MX250, and 4 GB memory. |
| C-012 | Recommended server configuration is Intel Core i5-10600K or above, NVIDIA GeForce GTX 2060 or above, and 32 GB memory or above. |
| C-013 | Server software environment is Ubuntu 22.0.4 and Docker 20.10.17. |

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
