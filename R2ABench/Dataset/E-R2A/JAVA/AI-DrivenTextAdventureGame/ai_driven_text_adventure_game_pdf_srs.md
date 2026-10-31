# AI-Driven Text Adventure Game and Community Software Requirements Specification (Standard SRS Extract)

## 1. Introduction

### Purpose

This document extracts verifiable requirements from `AI-DrivenTextAdventureGame_origin.pdf` and rewrites them according to the compact SRS standard in `architectural_views_rep-pkg/script/templates/SRS.md`. Its purpose is to provide structured input for architecture generation, test design, and requirements traceability for an AI-driven text adventure game and community platform. Source evidence is listed in `ai_driven_text_adventure_game_pdf_evidence_pack.json`. (Source: ATG-001)

### Product Scope

The product is a large-language-model-based text adventure game and shared community platform. The game uses model reasoning capabilities to generate dynamic plots, random events, and decision effects, allowing players to obtain a multi-chapter game experience through role-playing, background setup, saves, and choices. The community portion supports players sharing game events, reproduction flows, posts, comments, favorites, and notification interactions. (Source: ATG-002, ATG-003)

This document follows the terminology definitions in the source PDF for Vue.js, Nuxt.js, Iris, Gorm, MySQL, Docker, and Kubernetes. The source document does not specify API routes, database table structures, model-service protocols, or a large-model provider. (Source: ATG-001)

### Intended Audience

This document is intended for developers, testers, administrators, requirements reviewers, and later architecture generation and acceptance testing workflows for the game and community platform. Target users include text adventure game enthusiasts, players who enjoy challenge exploration or role-playing, players who enjoy community interaction, and players who pursue achievement challenges. (Source: ATG-004)

### References

| Ref | Source |
| --- | --- |
| REF-001 | GB/T 9385-2008, Specification for Computer Software Requirements Specification |
| REF-002 | GB/T 15532-2008, Specification for Computer Software Testing |
| REF-003 | Introduction to Database Systems, Higher Education Press, 2015 |
| REF-004 | Official documentation for Vue.js, Nuxt.js, Iris, Gorm, MySQL, Docker, and Kubernetes |

## 2. Overall Description

### Product Perspective

The system consists of a game system, community system, community user system, community administration system, favorites system, and notification system. The game system is responsible for new games, background setup, saves, continuing games, choice-based progression, and save sharing. The community system is responsible for posts, comments, replies, review status, search, and recommendations. The administration system is responsible for user and post governance. The notification system responds to comment, reply, and review events. The source document defines terms related to frontend, backend, database, containers, and container orchestration, but does not provide a complete deployment topology or component interfaces. (Source: ATG-001, ATG-008, ATG-009, ATG-010, ATG-011, ATG-012, ATG-013)

### Product Functions Summary

| Capability | Summary | Source |
| --- | --- | --- |
| Dynamic text adventure game | Generate dynamic plots, random events, and decision effects based on a large language model; support multi-chapter progress and role-playing. | ATG-002, ATG-003, ATG-013 |
| Game save management | Support creating cloud or local saves, viewing saves, deleting saves, continuing existing saves, and sharing existing saves. | ATG-013 |
| Community post interaction | Support publishing, editing, deleting, searching, favoriting, commenting, replying, viewing details, querying review status, and homepage recommendations. | ATG-010 |
| User accounts and profiles | Support registration, login, logout, password recovery, homepage viewing, browsing history, and profile modification. | ATG-008 |
| Administrator governance | Allow administrators to log in and out, view user and post lists, review posts, and handle community governance matters. | ATG-007, ATG-009 |
| Favorites and notifications | Support post favorites, new notifications, viewing read notifications, and deleting notifications. | ATG-011, ATG-012 |

### User Classes

| User Class | Responsibilities / Needs | Source |
| --- | --- | --- |
| Guest | Browse public community posts and comments, search topics or users, and register as a community and game user. | ATG-007 |
| Registered user / player | Play games, manage saves, share saves to the community, create posts, comment, reply, favorite content, receive notifications, and manage profile data. | ATG-007, ATG-013 |
| Community administrator | Manage users, posts, comments, and replies; review posts; handle reports and feedback; ban or restore violating users. | ATG-007, ATG-009 |
| Game content consumer | Obtain a varied game experience through multi-chapter plots, random events, role-playing, and achievement challenges. | ATG-003, ATG-004 |
| Community interaction user | Share game experience and random-event content, participate in post discussions, and obtain inspiration from other players' shared content. | ATG-002, ATG-004 |

### Operating Environment

| Environment | Requirement | Source |
| --- | --- | --- |
| Server deployment environment | Provide stable network connectivity, high-performance hardware facilities, and appropriate security protection to support continuous and stable game service operation. | ATG-006 |
| Server dependency | Depend on a cloud service provider or self-built data center to meet performance, security, and flexible scaling needs. | ATG-006 |
| Client environment | Player client devices should have relatively recent hardware configuration, a smooth operating system, and stable network connectivity. | ATG-006 |
| Client compatibility | The system shall be compatible with different client device types and operating system versions, and shall optimize client performance. | ATG-006, ATG-018 |

### Assumptions and Dependencies

| ID | Assumption / Dependency | Evidence Type | Source |
| --- | --- | --- | --- |
| AD-001 | The game service depends on stable networking, high-performance hardware, and security protection. | explicit | ATG-006 |
| AD-002 | The platform depends on a cloud service provider or self-built data center for performance, security, and scalability. | explicit | ATG-006 |
| AD-003 | Player clients need relatively recent hardware, a smooth operating system, and stable networking. | explicit | ATG-006 |
| AD-004 | Dynamic plots, random events, and game progression depend on large-language-model reasoning capabilities. | explicit | ATG-002, ATG-013 |
| AD-005 | Community sharing, reposting, and commenting are used to strengthen player achievement and community interaction. | explicit | ATG-002, ATG-019 |

## 3. External Interface Requirements

### User Interfaces

| Interface | Requirement | Source |
| --- | --- | --- |
| Registration and login interface | Support registration, login, logout, password recovery, password change, and email verification-code interactions. | ATG-008 |
| User homepage and profile interface | Support viewing the user's own homepage, other users' homepages, browsing history, avatar modification, and username modification. | ATG-008 |
| Community homepage and post interface | Support post search, homepage recommendations, post details, posting, editing, deleting, comments, replies, and favorites. | ATG-010 |
| Administrator interface | Support administrators viewing user lists, post lists, pending review posts, and review operations. | ATG-009 |
| Favorites interface | Support adding favorites, viewing favorites, and removing favorites. | ATG-011 |
| Notification interface | Support displaying unread notifications, viewing notifications, updating read status, and deleting notifications. | ATG-012 |
| Game interface | Support starting a new game, viewing saves, deleting saves, continuing a game, sharing saves, setting background information, and choosing options to progress the game. | ATG-013 |

### Software/API Interfaces

| Interface | Requirement | Source |
| --- | --- | --- |
| Frontend framework | The source document defines Vue.js and Nuxt.js for building user interfaces and server-side rendered applications. | ATG-001 |
| Backend framework | The source document defines the Iris framework as a Go web framework that supports MVC, middleware, session management, and API services. | ATG-001 |
| Data access | The source document defines Gorm as a Go ORM library and MySQL as a relational database management system. | ATG-001 |
| Deployment and operations | The source document defines Docker containers and Kubernetes container orchestration for containerization, deployment, scaling, and management. | ATG-001 |
| Large-model reasoning | The game system shall call a large language model or related model reasoning capability to generate plots, events, and state updates; the specific model interface is not given in the source document. | ATG-002, ATG-013, ATG-019 |

### Communication Interfaces

The source document requires the server environment to have stable network connectivity and requires user data to be encrypted during transmission and storage. It does not specify HTTP APIs, WebSocket, RPC, message queues, or large-model invocation protocols. During implementation, these protocol details should be treated as interfaces to be designed rather than facts inferred from the source document. (Source: ATG-006, ATG-016)

### Data Exchange Formats

The system needs to process data such as user accounts, email verification codes, avatars, usernames, posts, comments, replies, favorites, notifications, game saves, game background information, game choices, model-generated plots, random events, decision points, AIGC images, music and sound effects, game currency, and items. The source document does not specify JSON schemas, database table structures, file upload formats, or save serialization formats. (Source: ATG-008, ATG-010, ATG-011, ATG-012, ATG-013, ATG-019)

## 4. Functional Requirements

| ID | Requirement | Trigger / Input | System Behavior | Output | Priority | Verification | Source |
| --- | --- | --- | --- | --- | --- | --- | --- |
| FR-001 | The system shall support community user registration. | A guest enters an email address, username, password, password confirmation, and email verification code. | The system sends a verification code and validates the registration information. After validation succeeds, it creates a user account and turns the guest into a user. If fields are missing, the email is already registered, the username is already used, passwords do not match, or the verification code is incorrect, the system reports the reason. | New user account, login state, or error message. | High | Test | ATG-008 |
| FR-002 | The system shall support community user login. | An unauthenticated user enters an account and password. | The system validates the login information. If validation succeeds, it enters the initial page; if validation fails, it displays an error. | User login state or error message. | High | Test | ATG-008 |
| FR-003 | The system shall support community user logout. | A logged-in user initiates logout. | The system validates the request and exits the user's login state, making the user a guest. | Guest state. | High | Test | ATG-008 |
| FR-004 | The system shall support password recovery. | An unauthenticated user enters the registered email address, new password, new password confirmation, and email verification code. | The system sends a verification code, validates the information, and updates the user's password in the database after validation succeeds. For abnormal input, it reports the reason. | Updated password or error message. | High | Test | ATG-008 |
| FR-005 | The system shall support viewing the user's own homepage. | A logged-in user enters the personal homepage. | The system switches to the personal homepage and displays user information. | Personal homepage. | Medium | Demonstration | ATG-008 |
| FR-006 | The system shall support viewing other users' homepages. | A user selects another user's homepage. | The system navigates to the target user's personal homepage. | Other user's homepage. | Medium | Demonstration | ATG-008 |
| FR-007 | The system shall support viewing personal browsing history. | A logged-in user requests browsing history. | The system queries and displays the user's personal browsing history. | Browsing history list. | Medium | Test | ATG-008 |
| FR-008 | The system shall support password changes. | A logged-in user enters the old password, new password, and new password confirmation. | The system validates the information and changes the password after validation succeeds. If the old password is incorrect or the new password confirmation does not match, it displays an error. | Password change result or error message. | High | Test | ATG-008 |
| FR-009 | The system shall support modifying the personal avatar. | A logged-in user submits a new avatar from the personal homepage. | The system modifies the database avatar information and refreshes the frontend display. | New avatar. | Medium | Test | ATG-008 |
| FR-010 | The system shall support modifying the personal username. | A logged-in user submits a new username. | The system modifies the database username information and refreshes the frontend display. | New username. | Medium | Test | ATG-008 |
| FR-011 | The system shall support community administrator login. | An administrator enters administrator account login information. | The system validates whether the account is an administrator account and enters the administrator initial page after validation succeeds. | Administrator login state or error message. | High | Test | ATG-009 |
| FR-012 | The system shall support community administrator logout. | A logged-in administrator initiates logout. | The system validates the request and exits the administrator state. | Administrator logout state. | High | Test | ATG-009 |
| FR-013 | The system shall support administrators viewing the user list. | A logged-in administrator clicks user management on the homepage. | The system displays the user list and supports exiting back to the administrator homepage. | User list. | High | Test | ATG-009 |
| FR-014 | The system shall support administrators viewing the post list. | A logged-in administrator clicks post management on the homepage. | The system displays the list of posts published by users and supports exiting back to the administrator homepage. | Post list. | High | Test | ATG-009 |
| FR-015 | The system shall support administrators reviewing posts. | A logged-in administrator enters the pending review list and views a post. | The administrator decides whether the post passes review. The system notifies the user of the review result. A rejected post can be cancelled or modified and resubmitted for review. | Review status and user notification. | High | Test | ATG-009 |
| FR-016 | The system shall support users publishing posts. | A logged-in user starts creating a post from the homepage and submits a game screenshot, comment content, and additional information. | The system creates a pending review post and causes the administrator review interface to show a pending review item. | Pending review post. | High | Test | ATG-010 |
| FR-017 | The system shall support users editing posts. | The post owner edits the topic or content on the post page. | The system resubmits the edited post and causes the administrator review interface to show the edited post in pending review status. | Pending review post edit record. | High | Test | ATG-010 |
| FR-018 | The system shall support users deleting posts. | A logged-in user clicks delete on the user's own post page. | The system deletes the post so that all users cannot access the post content. | Deleted post inaccessible state. | High | Test | ATG-010 |
| FR-019 | The system shall support post search. | A guest or user enters keywords for post topic or content on the homepage or search page. | The system enters the search page and displays posts related to the keywords. | Search result list. | High | Test | ATG-010 |
| FR-020 | The system shall support favoriting posts. | A logged-in user selects favorite on a post page the user wants to favorite. | The system adds the post to the user's specified favorites folder. | Post link in the favorites folder. | Medium | Test | ATG-010 |
| FR-021 | The system shall support commenting on posts. | A logged-in user submits a comment on an existing post detail page. | The system saves the comment and displays it on the post detail page. If the post does not exist, commenting fails. | New comment or failure message. | High | Test | ATG-010 |
| FR-022 | The system shall support deleting comments. | A logged-in user deletes a comment previously posted by that user on a post detail page. | The system deletes the comment and its related replies. If the post or comment does not exist, deletion fails. | Comment deletion result or failure message. | High | Test | ATG-010 |
| FR-023 | The system shall support replying to comments. | A logged-in user replies to a comment or another reply on a post detail page. | The system saves the reply and displays it on the post detail page. If the related post, comment, or reply does not exist, replying fails. | New reply or failure message. | High | Test | ATG-010 |
| FR-024 | The system shall support deleting replies. | A logged-in user deletes a reply previously posted by that user on a post detail page. | The system deletes the reply. If the related object does not exist, deletion fails. | Reply deletion result or failure message. | High | Test | ATG-010 |
| FR-025 | The system shall support viewing post details. | A guest or user enters a post detail page. | The system displays post detail information. If the post does not exist, it displays a not-queryable or inaccessible state. | Post details or error message. | Medium | Demonstration | ATG-010 |
| FR-026 | The system shall support querying post review status. | A user requests review status after publishing or editing a post. | The system displays the current review status of the post. | Review status information. | Medium | Test | ATG-010 |
| FR-027 | The system shall support homepage recommendations. | A guest or user enters the homepage. | The system recommends popular posts or posts that may interest the user. | Recommended post list. | Medium | Test | ATG-010 |
| FR-028 | The system shall support adding posts to favorites. | A logged-in user chooses to add an existing post to favorites. | The system puts the post into the favorites folder and provides successful favorite feedback on the post detail page. | Successful favorite feedback and favorites record. | Medium | Test | ATG-011 |
| FR-029 | The system shall support viewing favorites. | A logged-in user enters favorites. | The system displays the posts in the user's favorites. | Favorite post list. | Medium | Test | ATG-011 |
| FR-030 | The system shall support removing posts from favorites. | A logged-in user chooses to remove a post from favorites. | The system removes the post from the favorites folder. | Updated favorites folder. | Medium | Test | ATG-011 |
| FR-031 | The system shall support creating notification messages. | A comment, reply, or post review progress update event completes. | The system creates an unread notification and associates it with the corresponding user, increasing the unread notification count by one. | Unread notification and count update. | High | Test | ATG-012 |
| FR-032 | The system shall support viewing messages. | A logged-in user views unread notifications. | The system updates the message status to read and decreases the unread message count by one. | Read message status and count update. | Medium | Test | ATG-012 |
| FR-033 | The system shall support deleting messages. | A logged-in user chooses to delete a message in the notification system. | The system deletes the message from the database and prevents the user notification interface from displaying that notification. | Notification deletion result. | Medium | Test | ATG-012 |
| FR-034 | The system shall support starting a new game. | A logged-in user chooses to start a new game. | The system creates a new cloud game save and starts the game. If cloud saves are temporarily unavailable, it creates a local game save and temporarily saves the game process. | New game save and initial game state. | High | Test | ATG-013 |
| FR-035 | The system shall support viewing existing game saves. | A logged-in user enters the game save list. | The system displays the user's existing game saves. | Game save list. | Medium | Test | ATG-013 |
| FR-036 | The system shall support deleting existing game saves. | A logged-in user selects a target save and confirms deletion. | The system deletes the target save. If the user cancels confirmation, the system performs no operation. | Save list after deletion. | Medium | Test | ATG-013 |
| FR-037 | The system shall support continuing an existing game save. | A logged-in user selects an existing game save. | The system loads the target save and continues the game. | Continued game state. | High | Test | ATG-013 |
| FR-038 | The system shall support sharing an existing game save to the community. | A logged-in user selects a target save, fills in supplementary post text, and clicks share to community. | The system publishes the save-sharing submission and displays submission success. The target game save appears in that user's community post records. | Community post or submission success message. | High | Test | ATG-013 |
| FR-039 | The system shall support setting game background information. | A logged-in user submits a background story when the current game save has empty background information. | The system updates the current game save's background information and starts the game dialogue flow. | Updated background information and game dialogue flow. | High | Test | ATG-013 |
| FR-040 | The system shall support making choices during gameplay to advance the game. | A logged-in user makes a choice in a game save that has background information. | The model updates the game state according to the option, and the system enters the next dialogue round. | Updated game state and next dialogue round. | High | Test | ATG-013 |
| FR-041 | The system shall support user management and custom notification settings. | A logged-in user requests notification setting adjustment. | The system saves the user's notification settings and uses those settings to affect later notification presentation. The source PDF does not expand the specific fields. | Notification setting result. | Medium | Demonstration | ATG-007 |
| FR-042 | The system shall support administrators handling user reports and feedback. | An administrator receives a user report or feedback. | The system provides administrators with the capability to handle reports and feedback. The source PDF does not expand the process details. | Report or feedback handling result. | Medium | Inspection | ATG-007 |
| FR-043 | The system shall support administrators banning and restoring accounts. | An administrator identifies a violating user or an account requiring restoration. | The system supports banning violating users and restoring banned accounts. The source PDF does not expand the status fields or approval process. | Updated account status. | High | Test | ATG-007 |

## 5. Non-Functional Requirements

| ID | Quality | Requirement | Fit Criterion | Priority | Verification | Source |
| --- | --- | --- | --- | --- | --- | --- |
| NFR-001 | Performance | The game system server shall respond to player input promptly. | Text generation and reasoning response time <= 20s. | High | Test | ATG-014 |
| NFR-002 | Performance | Login, logout, entering the game, and exiting the game shall respond promptly. | Response time <= 3s. | High | Test | ATG-014 |
| NFR-003 | Scalability | The game system server shall support concurrent players. | At least 100 users simultaneously receive game service satisfying response-time requirements. | High | Test | ATG-014 |
| NFR-004 | Resource Usage | The game system server process resource utilization shall be controlled. | Service process resource utilization <= 90%. | High | Test | ATG-014 |
| NFR-005 | Performance | Game save access shall complete promptly. | Access time for 5 save points in a normal game scenario <= 3s. | High | Test | ATG-014 |
| NFR-006 | Reliability | The frequency of unexpected system exceptions shall be controlled. | Unexpected exception frequency is less than once per month. | High | Analysis | ATG-015 |
| NFR-007 | Reliability | The system shall verify game save data integrity. | Integrity verification is executed when the client accesses game saves. | High | Test | ATG-015 |
| NFR-008 | Reliability | The system shall support fault detection and recovery. | The system can detect faults, perform basic data repair, and provide error messages and solutions. | High | Test | ATG-015 |
| NFR-009 | Reliability | The system shall maintain service continuity. | Game continuity and stability are maintained under external factors such as network fluctuation or server failure. | High | Analysis | ATG-015 |
| NFR-010 | Security | Sensitive user data shall be encrypted. | Sensitive data such as user passwords and personal information is encrypted during transmission and storage. | High | Test | ATG-016 |
| NFR-011 | Security | The system shall implement access control. | Only authorized administrator users can access sensitive data and sensitive functions. | High | Test | ATG-016 |
| NFR-012 | Security | The server shall perform vulnerability management regularly. | Security vulnerability scanning and assessment are performed regularly, and vulnerabilities are repaired in a timely manner. | High | Inspection | ATG-016 |
| NFR-013 | Observability | The system shall record and monitor sensitive operations and system events. | The server and database record sensitive operations and system events, and real-time monitoring is implemented. | High | Inspection | ATG-016 |
| NFR-014 | Maintainability | The system shall adopt a modular design. | Modules are independent, loosely coupled, easy to maintain, and easy to extend. | Medium | Inspection | ATG-017 |
| NFR-015 | Maintainability | System code shall be version controlled and backed up. | Modern version control tools are used, with regular version management and code backup. | Medium | Inspection | ATG-017 |
| NFR-016 | Maintainability | The system shall provide a fault-tolerance mechanism. | When errors occur, the system can handle them and respond in a timely manner. | High | Test | ATG-017 |
| NFR-017 | Testability | The system shall provide an automated testing system. | Unit tests, integration tests, and other automated tests are established so that functions can be verified quickly after changes. | Medium | Inspection | ATG-017 |
| NFR-018 | Usability | Game interaction shall be easy to understand and learn. | The interface is intuitive and easy to understand, reducing user learning cost. | Medium | Demonstration | ATG-018 |
| NFR-019 | Usability | Client interaction feedback shall be timely. | The interval from user operation to client feedback <= 500ms. | High | Test | ATG-018 |
| NFR-020 | Usability | Internal game interactions shall remain consistent. | Interface style and operation logic are consistent across modules. | Medium | Inspection | ATG-018 |
| NFR-021 | Accessibility | Game interfaces and operations shall accommodate different user groups. | Different user groups can use game functions smoothly. | Medium | Demonstration | ATG-018 |
| NFR-022 | Usability | The system shall provide clear operation feedback. | Operations such as button clicks and task completion provide clear feedback. | Medium | Demonstration | ATG-018 |
| NFR-023 | UI Design | The game interface shall have modern visual appeal. | Color matching and visual effects attract users and reflect the game theme and atmosphere. | Medium | Inspection | ATG-018 |
| NFR-024 | UI Design | The interface layout shall be reasonable. | Information overload and confusion are avoided, and users can clearly understand game information and operate the system. | Medium | Inspection | ATG-018 |
| NFR-025 | UI Design | The interface shall provide some customizability. | Users can adjust interface style or layout according to personal preferences. | Low | Demonstration | ATG-018 |
| NFR-026 | Portability | The game interface shall adapt across platforms. | The interface displays and operates normally on different devices, resolutions, and screen sizes. | High | Test | ATG-018 |
| NFR-027 | UI Design | Interface design shall be intuitive. | Users can quickly find needed functions and information. | Medium | Demonstration | ATG-018 |
| NFR-028 | Game Design | The game shall provide a tutorial. | The tutorial explains the UI, all interaction elements, and the game itself. | Medium | Demonstration | ATG-019 |
| NFR-029 | Game Design | The game shall provide multi-chapter plots and large-model-extended plots. | The script consists of human design and large-model external expansion/generalization. | High | Inspection | ATG-019 |
| NFR-030 | Game Design | Large-model-generated plots shall be consistent with the player's background. | Generated scripts remain consistent with player-defined background information and avoid out-of-character content. | High | Test | ATG-019 |
| NFR-031 | Game Design | The game shall provide music and sound effects. | Music and sound effects matching the scene setting are provided during gameplay. | Medium | Demonstration | ATG-019 |
| NFR-032 | Game Design | The game shall provide audiovisual feedback. | AIGC is combined with game text to generate images, and sound effects are combined to provide feedback. | Medium | Demonstration | ATG-019 |
| NFR-033 | Game Design | The game shall maintain freshness during play. | AIGC tools reduce repeated gameplay content and improve user stickiness. | Medium | Analysis | ATG-019 |
| NFR-034 | Game Design | The game shall provide achievement feedback. | Community reposting and comments allow players to gain recognition and achievement from other users. | Medium | Demonstration | ATG-019 |
| NFR-035 | Game Design | The game shall provide positive feedback through item rewards. | Playing and posting can earn game currency, and currency can buy items such as health packs and resurrection coins. | Medium | Test | ATG-019 |

## 6. Data Requirements

| ID | Data Object | Requirement | Rationale / Constraint | Verification | Source |
| --- | --- | --- | --- | --- | --- |
| DR-001 | User account | The system shall save account data such as email address, username, password, and login state. | Support registration, login, logout, password recovery, and password change. | Test | ATG-008 |
| DR-002 | User profile | The system shall save profile data such as avatar, username, personal homepage, and browsing history. | Support profile display and modification. | Test | ATG-008 |
| DR-003 | Administrator account and permissions | The system shall save administrator identity and permission data. | Support administrator login, review, and governance capabilities. | Test | ATG-009, ATG-016 |
| DR-004 | Post | The system shall save post topic, content, game screenshot, additional information, author, review status, and shared save reference. | Support posting, editing, deleting, search, details, review, and save sharing. | Test | ATG-010, ATG-013 |
| DR-005 | Post review record | The system shall save post review result, re-upload status, and user notification relationship. | Support post review, review status query, and notification. | Test | ATG-009, ATG-010, ATG-012 |
| DR-006 | Comment | The system shall save comment content, commenting user, and associated post. | Support commenting on posts and deleting comments. | Test | ATG-010 |
| DR-007 | Reply | The system shall save reply content, replying user, and associated comment or parent reply. | Support replying to comments and deleting replies. | Test | ATG-010 |
| DR-008 | Favorites | The system shall save user favorites and favorite post links. | Support favoriting, viewing favorites, and removing favorites. | Test | ATG-011 |
| DR-009 | Notification message | The system shall save notification content, associated user, and unread or read status. | Support creating messages, viewing messages, and deleting messages. | Test | ATG-012 |
| DR-010 | Game save | The system shall save cloud game saves, local temporary saves, save lists, and save status. | Support starting, viewing, deleting, continuing, and sharing saves. | Test | ATG-013 |
| DR-011 | Game background information | The system shall save the background story set by the player for a save. | Support model-generated plot consistency with the player's background. | Test | ATG-013, ATG-019 |
| DR-012 | Game state and choices | The system shall save game state, player choices, random events, and decision points. | Support choice-based game progression and the decision-effect system. | Test | ATG-003, ATG-013 |
| DR-013 | Generated plot and AIGC feedback | The system shall process model-generated plot text, images, and sound-effect feedback. | Support dynamic plots, audiovisual feedback, and freshness. | Demonstration | ATG-002, ATG-019 |
| DR-014 | Achievements, currency, and items | The system shall save achievement, game currency, health pack, resurrection coin, and other item data. | Support the achievement system and positive item-reward feedback. | Test | ATG-003, ATG-019 |
| DR-015 | Search data | The system shall process search inputs such as community topics, users, post topics, and post content. | Support guest and user search. | Test | ATG-007, ATG-010 |
| DR-016 | Sensitive data and logs | The system shall encrypt sensitive data and record sensitive operations and system events. | Support security confidentiality and monitoring requirements. | Inspection | ATG-016 |
| DR-017 | Report feedback and account status | The system shall save report feedback, ban status, and restoration status. | Support administrators handling reports, banning accounts, and restoring accounts. | Inspection | ATG-007 |

## 7. Constraints

| ID | Constraint | Evidence Type | Source |
| --- | --- | --- | --- |
| C-001 | During development, technical capabilities and resource limitations need to be considered, and the development cycle and technical implementation plan need to be planned reasonably. | explicit | ATG-005 |
| C-002 | Game content requires strict content review and compliance with relevant laws, regulations, and social moral standards. | explicit | ATG-005 |
| C-003 | Collection and processing of user data must comply with data security and privacy protection legal requirements. | explicit | ATG-005 |
| C-004 | The random event and decision-effect system needs to balance game difficulty and challenge, avoiding excessive dependence on luck or excessive difficulty. | explicit | ATG-005 |
| C-005 | The game community and user interaction platform need strengthened community management and interaction monitoring to prevent harmful speech and behavior. | explicit | ATG-005 |
| C-006 | Game content creation and operation need to protect copyright and intellectual property and avoid infringement. | explicit | ATG-005 |
| C-007 | The system needs to value user experience and feedback handling, and continuously optimize product functions and services. | explicit | ATG-005 |
| C-008 | The server deployment environment shall have stable network connectivity, high-performance hardware, and appropriate security protection. | explicit | ATG-006 |
| C-009 | The server depends on a cloud service provider or self-built data center to meet performance, security, and scalability needs. | explicit | ATG-006 |
| C-010 | Client devices need relatively recent hardware configuration, a smooth operating system, and stable network connectivity. | explicit | ATG-006 |
| C-011 | The system needs to be compatible with different client device types and operating system versions. | explicit | ATG-006 |
| C-012 | The source document defines Vue.js, Nuxt.js, Iris, Gorm, MySQL, Docker, and Kubernetes as project-related technical terms. | explicit | ATG-001 |
| C-013 | Model-generated script content must remain consistent with player-defined background information and avoid out-of-character content. | explicit | ATG-019 |

## 8. Verification and Acceptance

| ID | Verification | Acceptance Criterion |
| --- | --- | --- |
| FR-001 | Test | A guest can register successfully, and abnormal registration input returns the corresponding error message. |
| FR-002 | Test | Correct credentials log in successfully, and incorrect credentials fail to log in. |
| FR-003 | Test | A logged-in user becomes a guest after logout. |
| FR-004 | Test | The password is changed after email verification succeeds, and abnormal input is rejected. |
| FR-005 | Demonstration | The user can open the personal homepage. |
| FR-006 | Demonstration | The user can open another user's homepage. |
| FR-007 | Test | The user can view personal browsing history. |
| FR-008 | Test | The user can change the password and receives a prompt when password validation is abnormal. |
| FR-009 | Test | The frontend displays the new avatar after the user's avatar is updated. |
| FR-010 | Test | The frontend displays the new username after the username is updated. |
| FR-011 | Test | The administrator enters the administrator page after account validation succeeds. |
| FR-012 | Test | The administrator can log out of the administrator page. |
| FR-013 | Test | The administrator can view the user list. |
| FR-014 | Test | The administrator can view the post list. |
| FR-015 | Test | The administrator can review posts and notify users of results. |
| FR-016 | Test | A pending review post appears in the administrator review interface after a user posts. |
| FR-017 | Test | Edited post content enters pending review status after the user edits a post. |
| FR-018 | Test | All users cannot access the post content after the user deletes the post. |
| FR-019 | Test | Related posts can be found by topic or content keywords. |
| FR-020 | Test | The user can favorite a post into a specified favorites folder. |
| FR-021 | Test | A comment is saved and displayed, and commenting fails when the post does not exist. |
| FR-022 | Test | A comment and related replies are deleted, and deletion fails when abnormal objects do not exist. |
| FR-023 | Test | A reply is saved and displayed, and replying fails when abnormal objects do not exist. |
| FR-024 | Test | A reply is deleted, and deletion fails when abnormal objects do not exist. |
| FR-025 | Demonstration | A guest or user can view post details. |
| FR-026 | Test | The user can view review status after posting or editing. |
| FR-027 | Test | The homepage displays popular or potentially interesting posts. |
| FR-028 | Test | A post can be added to favorites and displays successful feedback. |
| FR-029 | Test | The user can view posts in favorites. |
| FR-030 | Test | The user can remove a post from favorites. |
| FR-031 | Test | A new unread notification is created after a comment, reply, or review progress update. |
| FR-032 | Test | After the user views an unread message, the message becomes read and the unread count decreases. |
| FR-033 | Test | After the user deletes a notification, the notification cannot be viewed in the notification interface. |
| FR-034 | Test | The user can create a new game save and start the game. |
| FR-035 | Test | The user can view the existing game save list. |
| FR-036 | Test | The target save no longer appears after the user confirms deletion. |
| FR-037 | Test | The user can continue the game from an existing save. |
| FR-038 | Test | The user can share the target save to the community and generate a post record. |
| FR-039 | Test | The user can set background information for a game save and enter the dialogue flow. |
| FR-040 | Test | After the user makes a choice, the model updates the game state and progresses to the next dialogue round. |
| FR-041 | Demonstration | The user can save notification settings; specific fields are confirmed during design. |
| FR-042 | Inspection | An entry point and records for administrator report and feedback handling exist. |
| FR-043 | Test | The administrator can ban violating accounts and restore accounts. |
| NFR-001 | Test | Text generation and reasoning response time <= 20s. |
| NFR-002 | Test | Login, logout, entering the game, and exiting the game response time <= 3s. |
| NFR-003 | Test | At least 100 concurrent users meet the response-time requirement. |
| NFR-004 | Test | Service process resource utilization <= 90%. |
| NFR-005 | Test | Access time for 5 save points <= 3s. |
| NFR-006 | Analysis | Unexpected exception frequency is less than once per month. |
| NFR-007 | Test | Data integrity verification is executed when accessing game saves. |
| NFR-008 | Test | During faults, the system provides repair, error prompts, or solutions. |
| NFR-009 | Analysis | Continuity and stability are maintained under network fluctuation or server failure. |
| NFR-010 | Test | Sensitive data is encrypted during both transmission and storage. |
| NFR-011 | Test | Unauthorized users cannot access sensitive data or sensitive functions. |
| NFR-012 | Inspection | Security scanning assessment and vulnerability repair records exist. |
| NFR-013 | Inspection | Sensitive operation and system event logs and monitoring exist. |
| NFR-014 | Inspection | Modular and loosely coupled design documentation exists. |
| NFR-015 | Inspection | Version control and regular backup mechanisms exist. |
| NFR-016 | Test | The fault-tolerance mechanism can handle and respond when errors occur. |
| NFR-017 | Inspection | Automated tests such as unit tests and integration tests exist. |
| NFR-018 | Demonstration | New users can understand and master basic operations. |
| NFR-019 | Test | User operation to client feedback <= 500ms. |
| NFR-020 | Inspection | Interface style and operation logic remain consistent. |
| NFR-021 | Demonstration | Different user groups can smoothly use core functions. |
| NFR-022 | Demonstration | Operations produce clear feedback. |
| NFR-023 | Inspection | The interface conforms to modern aesthetics and the game theme. |
| NFR-024 | Inspection | The interface layout avoids information overload and confusion. |
| NFR-025 | Demonstration | Users can adjust interface style or layout. |
| NFR-026 | Test | The interface displays and operates normally on different devices and resolutions. |
| NFR-027 | Demonstration | Users can quickly find functions and information. |
| NFR-028 | Demonstration | The game tutorial covers UI, interaction elements, and game instructions. |
| NFR-029 | Inspection | Game plots include human-designed and large-model-expanded parts. |
| NFR-030 | Test | Generated plots are consistent with player background. |
| NFR-031 | Demonstration | The game plays music and sound effects matching the scene. |
| NFR-032 | Demonstration | AIGC image and sound-effect feedback is visible and audible. |
| NFR-033 | Analysis | Repeated gameplay content has variability. |
| NFR-034 | Demonstration | Community reposting and comments can form achievement feedback. |
| NFR-035 | Test | Playing or posting can obtain currency and buy items. |
| DR-001 | Test | User account data can be created, read, and modified. |
| DR-002 | Test | User profile and browsing history can be saved and displayed. |
| DR-003 | Test | Administrator permission data can control access to management functions. |
| DR-004 | Test | Post data can be created, reviewed, searched, viewed, and deleted. |
| DR-005 | Test | Post review records can be queried and can trigger notifications. |
| DR-006 | Test | Comment data can be saved and deleted. |
| DR-007 | Test | Reply data can be saved and deleted. |
| DR-008 | Test | Favorites data can be added, viewed, and removed. |
| DR-009 | Test | Notification messages can be created, marked read, and deleted. |
| DR-010 | Test | Game saves can be created, viewed, deleted, continued, and shared. |
| DR-011 | Test | Game background information can be saved and used for the game flow. |
| DR-012 | Test | Game state and choices can be saved and advanced. |
| DR-013 | Demonstration | Generated plot, image, and sound-effect feedback can be displayed. |
| DR-014 | Test | Achievement, currency, and item data can be saved and used. |
| DR-015 | Test | Search input can be used to query topics, users, or posts. |
| DR-016 | Inspection | Sensitive data encryption and logging mechanisms exist. |
| DR-017 | Inspection | Report feedback and account status records exist. |
| C-001 | Inspection | The development plan reflects technical and resource limitations. |
| C-002 | Inspection | Content review and legal compliance mechanisms exist. |
| C-003 | Inspection | User data processing meets privacy protection requirements. |
| C-004 | Analysis | Game difficulty and randomness are balanced through analysis. |
| C-005 | Inspection | Community management and interaction monitoring mechanisms exist. |
| C-006 | Inspection | Copyright and intellectual property protection mechanisms exist. |
| C-007 | Inspection | A user feedback handling process exists. |
| C-008 | Inspection | The server deployment environment meets network, hardware, and security requirements. |
| C-009 | Inspection | Cloud service or data center dependency is recorded. |
| C-010 | Inspection | Client devices meet hardware, system, and network assumptions. |
| C-011 | Test | Different client devices and operating system versions are compatible. |
| C-012 | Inspection | Project technical terms and technology selection records are traceable. |
| C-013 | Test | Model-generated content does not deviate from the player's background setting. |

## 9. Traceability Matrix

| ID | Requirement | Type | Source | Evidence Type | Verification | Confidence |
| --- | --- | --- | --- | --- | --- | --- |
| FR-001 | Community user registration | Functional | ATG-008 | explicit | Test | High |
| FR-002 | Community user login | Functional | ATG-008 | explicit | Test | High |
| FR-003 | Community user logout | Functional | ATG-008 | explicit | Test | High |
| FR-004 | Password recovery | Functional | ATG-008 | explicit | Test | High |
| FR-005 | View personal homepage | Functional | ATG-008 | explicit | Demonstration | High |
| FR-006 | View other user homepage | Functional | ATG-008 | explicit | Demonstration | High |
| FR-007 | View personal browsing history | Functional | ATG-008 | explicit | Test | High |
| FR-008 | Change password | Functional | ATG-008 | explicit | Test | High |
| FR-009 | Modify avatar | Functional | ATG-008 | explicit | Test | High |
| FR-010 | Modify username | Functional | ATG-008 | explicit | Test | High |
| FR-011 | Administrator login | Functional | ATG-009 | explicit | Test | High |
| FR-012 | Administrator logout | Functional | ATG-009 | explicit | Test | High |
| FR-013 | View user list | Functional | ATG-009 | explicit | Test | High |
| FR-014 | View post list | Functional | ATG-009 | explicit | Test | High |
| FR-015 | Review posts | Functional | ATG-009 | explicit | Test | High |
| FR-016 | Publish posts | Functional | ATG-010 | explicit | Test | High |
| FR-017 | Edit posts | Functional | ATG-010 | explicit | Test | High |
| FR-018 | Delete posts | Functional | ATG-010 | explicit | Test | High |
| FR-019 | Search posts | Functional | ATG-010 | explicit | Test | High |
| FR-020 | Favorite posts | Functional | ATG-010 | explicit | Test | High |
| FR-021 | Comment on posts | Functional | ATG-010 | explicit | Test | High |
| FR-022 | Delete comments | Functional | ATG-010 | explicit | Test | High |
| FR-023 | Reply to comments | Functional | ATG-010 | explicit | Test | High |
| FR-024 | Delete replies | Functional | ATG-010 | explicit | Test | High |
| FR-025 | View post details | Functional | ATG-010 | explicit | Demonstration | High |
| FR-026 | Query review status | Functional | ATG-010 | explicit | Test | High |
| FR-027 | Homepage recommendations | Functional | ATG-010 | explicit | Test | High |
| FR-028 | Add to favorites | Functional | ATG-011 | explicit | Test | High |
| FR-029 | View favorites | Functional | ATG-011 | explicit | Test | High |
| FR-030 | Remove from favorites | Functional | ATG-011 | explicit | Test | High |
| FR-031 | Create notifications | Functional | ATG-012 | explicit | Test | High |
| FR-032 | View messages | Functional | ATG-012 | explicit | Test | High |
| FR-033 | Delete messages | Functional | ATG-012 | explicit | Test | High |
| FR-034 | Start a new game | Functional | ATG-013 | explicit | Test | High |
| FR-035 | View game saves | Functional | ATG-013 | explicit | Test | High |
| FR-036 | Delete game saves | Functional | ATG-013 | explicit | Test | High |
| FR-037 | Continue game save | Functional | ATG-013 | explicit | Test | High |
| FR-038 | Share game save | Functional | ATG-013 | explicit | Test | High |
| FR-039 | Set background information | Functional | ATG-013 | explicit | Test | High |
| FR-040 | Choose to progress game | Functional | ATG-013 | explicit | Test | High |
| FR-041 | Notification settings | Functional | ATG-007 | explicit | Demonstration | Medium |
| FR-042 | Report and feedback handling | Functional | ATG-007 | explicit | Inspection | Medium |
| FR-043 | Account ban and restoration | Functional | ATG-007 | explicit | Test | Medium |
| NFR-001 | Text generation response | Non-functional | ATG-014 | explicit | Test | High |
| NFR-002 | Login and game entry/exit response | Non-functional | ATG-014 | explicit | Test | High |
| NFR-003 | Concurrent user count | Non-functional | ATG-014 | explicit | Test | High |
| NFR-004 | Service process resource utilization | Non-functional | ATG-014 | explicit | Test | High |
| NFR-005 | Save access speed | Non-functional | ATG-014 | explicit | Test | High |
| NFR-006 | Exception frequency | Non-functional | ATG-015 | explicit | Analysis | High |
| NFR-007 | Save integrity verification | Non-functional | ATG-015 | explicit | Test | High |
| NFR-008 | Fault detection and recovery | Non-functional | ATG-015 | explicit | Test | High |
| NFR-009 | Service continuity | Non-functional | ATG-015 | explicit | Analysis | High |
| NFR-010 | Sensitive data encryption | Non-functional | ATG-016 | explicit | Test | High |
| NFR-011 | Access control | Non-functional | ATG-016 | explicit | Test | High |
| NFR-012 | Vulnerability management | Non-functional | ATG-016 | explicit | Inspection | High |
| NFR-013 | Logging and monitoring | Non-functional | ATG-016 | explicit | Inspection | High |
| NFR-014 | Modular design | Non-functional | ATG-017 | explicit | Inspection | High |
| NFR-015 | Version control and backup | Non-functional | ATG-017 | explicit | Inspection | High |
| NFR-016 | Fault tolerance mechanism | Non-functional | ATG-017 | explicit | Test | High |
| NFR-017 | Automated testing | Non-functional | ATG-017 | explicit | Inspection | High |
| NFR-018 | User friendliness | Non-functional | ATG-018 | explicit | Demonstration | High |
| NFR-019 | Client feedback time | Non-functional | ATG-018 | explicit | Test | High |
| NFR-020 | Interaction consistency | Non-functional | ATG-018 | explicit | Inspection | High |
| NFR-021 | Accessibility | Non-functional | ATG-018 | explicit | Demonstration | High |
| NFR-022 | Operation feedback mechanism | Non-functional | ATG-018 | explicit | Demonstration | High |
| NFR-023 | Interface aesthetics | Non-functional | ATG-018 | explicit | Inspection | High |
| NFR-024 | Reasonable layout | Non-functional | ATG-018 | explicit | Inspection | High |
| NFR-025 | Interface customizability | Non-functional | ATG-018 | explicit | Demonstration | High |
| NFR-026 | Cross-platform adaptation | Non-functional | ATG-018 | explicit | Test | High |
| NFR-027 | Interface intuitiveness | Non-functional | ATG-018 | explicit | Demonstration | High |
| NFR-028 | Game tutorial | Non-functional | ATG-019 | explicit | Demonstration | High |
| NFR-029 | Multi-chapter and model-extended plot | Non-functional | ATG-019 | explicit | Inspection | High |
| NFR-030 | Background consistency | Non-functional | ATG-019 | explicit | Test | High |
| NFR-031 | Music and sound effects | Non-functional | ATG-019 | explicit | Demonstration | High |
| NFR-032 | Audiovisual feedback | Non-functional | ATG-019 | explicit | Demonstration | High |
| NFR-033 | Gameplay freshness | Non-functional | ATG-019 | explicit | Analysis | Medium |
| NFR-034 | Achievement feedback | Non-functional | ATG-019 | explicit | Demonstration | High |
| NFR-035 | Item rewards | Non-functional | ATG-019 | explicit | Test | High |
| DR-001 | User account data | Data | ATG-008 | explicit | Test | High |
| DR-002 | User profile data | Data | ATG-008 | explicit | Test | High |
| DR-003 | Administrator permission data | Data | ATG-009, ATG-016 | explicit | Test | High |
| DR-004 | Post data | Data | ATG-010, ATG-013 | explicit | Test | High |
| DR-005 | Review record | Data | ATG-009, ATG-010, ATG-012 | explicit | Test | High |
| DR-006 | Comment data | Data | ATG-010 | explicit | Test | High |
| DR-007 | Reply data | Data | ATG-010 | explicit | Test | High |
| DR-008 | Favorites data | Data | ATG-011 | explicit | Test | High |
| DR-009 | Notification message data | Data | ATG-012 | explicit | Test | High |
| DR-010 | Game save data | Data | ATG-013 | explicit | Test | High |
| DR-011 | Game background information | Data | ATG-013, ATG-019 | explicit | Test | High |
| DR-012 | Game state and choices | Data | ATG-003, ATG-013 | explicit | Test | High |
| DR-013 | Generated plot and feedback data | Data | ATG-002, ATG-019 | explicit | Demonstration | High |
| DR-014 | Achievement currency item data | Data | ATG-003, ATG-019 | explicit | Test | High |
| DR-015 | Search data | Data | ATG-007, ATG-010 | explicit | Test | High |
| DR-016 | Sensitive data and logs | Data | ATG-016 | explicit | Inspection | High |
| DR-017 | Report feedback and account status | Data | ATG-007 | explicit | Inspection | Medium |
| C-001 | Technical and resource limitations | Constraint | ATG-005 | explicit | Inspection | High |
| C-002 | Content review and legal compliance | Constraint | ATG-005 | explicit | Inspection | High |
| C-003 | Data security and privacy protection | Constraint | ATG-005 | explicit | Inspection | High |
| C-004 | Game difficulty balance | Constraint | ATG-005 | explicit | Analysis | High |
| C-005 | Community management and monitoring | Constraint | ATG-005 | explicit | Inspection | High |
| C-006 | Copyright and intellectual property | Constraint | ATG-005 | explicit | Inspection | High |
| C-007 | User feedback handling | Constraint | ATG-005 | explicit | Inspection | High |
| C-008 | Server networking, hardware, and security | Constraint | ATG-006 | explicit | Inspection | High |
| C-009 | Cloud service or data center dependency | Constraint | ATG-006 | explicit | Inspection | High |
| C-010 | Client hardware, system, and network | Constraint | ATG-006 | explicit | Inspection | High |
| C-011 | Client compatibility | Constraint | ATG-006 | explicit | Test | High |
| C-012 | Project technical terminology | Constraint | ATG-001 | explicit | Inspection | Medium |
| C-013 | Model-generated background consistency | Constraint | ATG-019 | explicit | Test | High |
