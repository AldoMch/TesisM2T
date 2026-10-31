# LabHire Software Requirements Specification (Standard SRS Extract)

## 1. Introduction

### Purpose

This document extracts verifiable requirements from `LabHire Requirements Specification V2.2.docx` and rewrites them according to the compact SRS standard in `architectural_views_rep-pkg/script/templates/SRS.md`. The goal is to provide structured input for architecture generation, test design, and requirements tracing for the LabHire university research internship information management platform. Source evidence is recorded in `labhire_docx_evidence_pack.json`. (Source: LAB-001)

### Product Scope

LabHire is a research internship information integration platform for university teachers and students. It supports research internship project publication, recommendation, retrieval, application, management, mutual evaluation, personal information, resumes, mentor search, community communication, internship referrals, and management-side review. The system scope is limited to university research internship information and community referral posts, and does not include social enterprise recruitment information or headhunting advertisements. (Source: LAB-004, LAB-006, LAB-008)

### Intended Audience

This document is intended for developers, testers, project managers, customer representatives, and project-related personnel such as marketing, operations, and maintenance staff. (Source: LAB-002)

### References

| Ref | Source |
| --- | --- |
| REF-001 | GB/T 8566-2007 Information Technology, Software Life Cycle Process |
| REF-002 | GB/T 8567-2006 Computer Software Documentation Specification |
| REF-003 | GB/T 9385-2008 Computer Software Requirements Specification |
| REF-004 | PEP8 Python Coding Standard |

## 2. Overall Description

### Product Perspective

The system connects student users, mentor users, enterprise-certified student users, and administrators, and provides services around the research internship project life cycle and community interaction. Students use the platform to obtain projects, apply, favorite items, view mentors, and participate in the community. Mentors publish and manage projects, screen applicant students, and participate in mutual evaluation. Administrators handle identity certification, enterprise certification, and content review. The source document mentions a back-end database, verification codes, in-site messages, email push, chat, risk-control logs, and audit modules, but does not specify the database product, API protocol, deployment topology, or concrete encryption algorithm. (Source: LAB-004, LAB-005, LAB-026, LAB-029)

### Product Functions Summary

| Capability | Summary | Source |
| --- | --- | --- |
| Research internship projects | Project recommendation, viewing, publication, search, management, favorites, message reminders, mutual evaluation, and application. | LAB-010, LAB-011, LAB-012, LAB-013, LAB-014, LAB-015, LAB-016, LAB-017 |
| Personal information and certification | Campus email registration/login, student resume upload, enterprise certification, personal information completion, mentor search/favorite, and viewing of two-way selection materials. | LAB-018, LAB-019, LAB-020, LAB-021, LAB-022 |
| Community | Post display, post publication, comments, post favorites, and popularity sorting. | LAB-023, LAB-024, LAB-025 |
| Administration | Administrator login, first-round university identity review, second-round enterprise qualification review, post review, and comment review. | LAB-026, LAB-027 |
| Security and quality | Permission control, data confidentiality, response time, robustness, compatibility, portability, and legal compliance. | LAB-029, LAB-033, LAB-034 |

### User Classes

| User Class | Responsibilities / Needs | Source |
| --- | --- | --- |
| Student user | Authenticates through campus email; browses, filters, and favorites research internship projects, applies to projects, maintains personal information and resumes, and participates in the community. | LAB-005, LAB-007, LAB-018, LAB-019 |
| Enterprise-certified student user | Completes secondary certification through enterprise email and gains permission to publish internship referral posts. | LAB-007, LAB-020, LAB-023 |
| Mentor user | Authenticates through campus email; publishes research internship projects, manages applicant students and projects, views applicant student information, and participates in project mutual evaluation. | LAB-005, LAB-012, LAB-014, LAB-016, LAB-022 |
| Administrator | Account is assigned by the back-end database; manages teacher/student certification, enterprise certification, and post/comment content. | LAB-026, LAB-027 |

### Operating Environment

| Environment | Requirement | Source |
| --- | --- | --- |
| Mobile hardware | Quad-core 1.5 GHz CPU, 1 GB RAM + 4 GB ROM. | LAB-031 |
| Mobile software | Android 7.0 and above, iOS 8.0 and above, WeChat 6.5.6 and above. | LAB-031 |
| Desktop hardware/network | At least 2 GB memory and broadband network. | LAB-032 |
| Desktop software | Windows 7 and above, Mac OS X 10.9 and above; Chrome, Firefox, or Microsoft Edge is recommended. | LAB-032 |

### Assumptions and Dependencies

| ID | Assumption / Dependency | Evidence Type | Source |
| --- | --- | --- | --- |
| AD-001 | Registration and enterprise certification depend on campus email, enterprise email, and verification-code mechanisms. | explicit | LAB-018, LAB-020, LAB-029 |
| AD-002 | Administrator account passwords are directly assigned by the back-end database; the system needs administrator login but has no administrator registration entry. | explicit | LAB-026 |
| AD-003 | Message reminders depend on in-site notifications, email push, or equivalent notification mechanisms. | explicit | LAB-015, LAB-026 |
| AD-004 | Project recommendation depends on user interest tags, skill tags, historical behavior, and project tags. | explicit | LAB-010 |
| AD-005 | The source document does not specify the database product, interface protocol, email service provider, SMS service provider, or encryption algorithm. | inferred | LAB-018, LAB-020, LAB-026, LAB-029 |

## 3. External Interface Requirements

### User Interfaces

| UI Area | Requirement Summary | Source |
| --- | --- | --- |
| Project home/recommendation page | Displays personalized research internship project recommendations to students. | LAB-010 |
| Project detail page | Displays project title, internship content, start time, recruitment count, mentor profile, university, internship duration, online/offline mode, and required skills. | LAB-011 |
| Project publication and management page | Mentors fill in project information and manage recruitment count, status, and chat with applicant students. | LAB-012, LAB-014 |
| Search page | Students search for projects or mentors according to rules such as university, mentor, and major direction. | LAB-013, LAB-022 |
| Personal information page | Students and mentors supplement personal information; students upload resumes; users view materials within the allowed scope during two-way selection. | LAB-019, LAB-021, LAB-022 |
| Community page | Displays post details and supports post publication, comments, favorites, and popularity sorting. | LAB-023, LAB-024, LAB-025 |
| Administration side | After login, administrators handle identity certification, enterprise certification, post review, and comment review. | LAB-026, LAB-027 |
| GUI style | The student side should be more attractive, the mentor side should be more task-oriented, and pages should be concise, clear, and aesthetically pleasing; interface elements should support efficiency and friendliness. | LAB-030 |

### Software/API Interfaces

| Interface | Requirement Summary | Evidence Type | Source |
| --- | --- | --- | --- |
| Email verification-code interface | Registration must send a verification code to a university email address; enterprise certification must send a verification code to an enterprise-domain email address. | explicit | LAB-018, LAB-020 |
| Notification interface | Favorite updates, mentor messages, comment replies, project applications, and review states need to trigger notifications; review feedback can be sent through in-site messages and email push. | explicit | LAB-015, LAB-026 |
| Chat interface | Mentors chat with applicant students in project management, and chat content must be encrypted. | explicit | LAB-014, LAB-029 |
| Recommendation algorithm interface | Project recommendation uses collaborative filtering, tag matching, and cold-start rule-driven strategies. | explicit | LAB-010 |
| Review/risk-control interface | Automatic field validation, manual review, abnormal behavior detection, risk-control logs, and audit alerts support certification and content governance. | explicit | LAB-026, LAB-029 |
| Database interface | Administrator accounts are assigned by the back-end database; administrators can manage entity information; the concrete database product is not specified. | explicit | LAB-026, LAB-028 |

### Communication Interfaces

The system needs to support email verification codes, in-site messages, email push, inter-user chat, and message reminders. The source document does not specify communication protocols, ports, message formats, SMS platforms, or email service providers. (Source: LAB-015, LAB-018, LAB-020, LAB-026, LAB-029)

### Data Exchange Formats

| Data Group | Fields / Content | Source |
| --- | --- | --- |
| Project information | Title, internship content, start time, recruitment count, mentor profile, affiliated university, internship duration, online/offline mode, required skills, field, and project status. | LAB-010, LAB-011, LAB-012, LAB-014 |
| Registration information | Name, university, email, user type, student/employee number, password, and verification code. | LAB-018 |
| Student information | Name, university, email, major direction, research projects, competition awards, academic performance, and strong skills. | LAB-021 |
| Mentor information | Name, university, email, major direction, personal homepage URL, professional title, education experience, published papers, and research projects. | LAB-021 |
| Resume file | Local resume file, supporting formats such as PDF, with a maximum size of 10 MB. | LAB-019 |
| Community post | Ordinary post or internship referral post, within 400 words, supporting text formats such as HTML and Markdown. | LAB-023 |
| Comments and popularity | Comment content, like count, comment count, view count, publication time, and time-decay item. | LAB-024, LAB-025 |
| Mutual evaluation data | Mentor evaluation and score of student performance, and student evaluation and score of mentor assistance. | LAB-016 |
| Review data | Required field validation result, review state, feedback notification, failure reason, and resubmission record. | LAB-026 |

## 4. Functional Requirements

| ID | Description | Trigger / Input | System Behavior | Output | Priority | Verification | Source Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| FR-001 | The system shall recommend research internship projects to students personally. | A student enters the platform home page or recommendation page, and the system can read the student's interest fields, strong skills, historical behavior, and tags. | The system generates project recommendations based on collaborative filtering, tag matching, and cold-start rules. | Recommendation list containing project name, time, recruitment count, affiliated university, and field. | High | Test | LAB-010 |
| FR-002 | The system shall allow users to view research internship project details. | A user clicks a project from recommendations or search results. | The system displays detailed project information. | Project title, internship content, start time, recruitment count, mentor profile, university, internship duration, online/offline mode, and required skills. | High | Demonstration | LAB-011 |
| FR-003 | The system shall allow mentors to publish research internship projects. | A mentor logs in or registers, fills in project information, and submits it. | The system creates the research internship project for students to browse, favorite, and apply to. | Newly published project record. | High | Test | LAB-012, LAB-009 |
| FR-004 | The system shall allow students to retrieve research internship projects according to rules. | A student logs in and enters search criteria such as university and mentor on the search page. | The system searches for related projects according to the search rules. | Project search result list. | High | Test | LAB-013 |
| FR-005 | The system shall allow mentors to manage published projects. | A mentor enters the project management page. | The system allows the mentor to chat with applicant students, increase or decrease recruitment count, and modify project status. | Updated project status, recruitment count, or chat record. | High | Test | LAB-014 |
| FR-006 | The system shall allow students to favorite and unfavorite projects. | A student sees an interesting project or operates in the favorites folder. | The system saves or cancels the student's favorite relationship with the project. | Project list in the favorites folder. | Medium | Test | LAB-015, LAB-009 |
| FR-007 | The system shall send project- and interaction-related message reminders to users. | A mentor sends a message, favorite content is updated, a comment is replied to, or a mentor project is applied to. | The system generates notifications and reminds related users. | Message reminder or notification record. | High | Test | LAB-015 |
| FR-008 | The system shall enable teacher-student mutual evaluation after project completion. | A mentor sets a project to ended state. | The system allows the mentor to evaluate and score student performance and allows the student to evaluate and score mentor assistance. | Mutual evaluation result for reference by other students and mentors. | Medium | Test | LAB-016 |
| FR-009 | The system shall allow students to submit project application requests. | A student clicks apply on the project detail page and submits an application. | The system records the application and makes it available for mentor screening in project management. | Project application record. | High | Test | LAB-017 |
| FR-010 | The system shall require first-time users to register or log in before full functionality is displayed. | A user first enters the platform or accesses complete functions. | The system requires registration or login. During registration it collects name, university, email, user type, student/employee number, and password, and authenticates through a university email verification code. | Certified user account or login session. | High | Test | LAB-018 |
| FR-011 | The system shall allow students to upload local resume files. | A student selects a resume file on the personal information completion page. | The system receives and saves a resume file in a supported format, with maximum size 10 MB; other allowed users can download and view it when viewing personal information. | Uploaded resume file. | High | Test | LAB-019 |
| FR-012 | The system shall support student enterprise certification and unlock internship referral post permission. | An ordinary student submits enterprise email certification. | The system sends a verification code to an enterprise-domain email and completes certification; after certification passes, it grants referral-post publication permission. | Enterprise certification state and referral post publication permission. | High | Test | LAB-020 |
| FR-013 | The system shall allow students and mentors to complete personal information and integrate it into resume form. | A user logs in and enters the personal information completion page. | The system saves student or mentor personal information and automatically imports completed platform projects into the research project field. | User profile or resume view. | High | Test | LAB-021 |
| FR-014 | The system shall allow students to search for and favorite mentors. | A student logs in and searches for mentors by rules such as university and major direction. | The system performs fuzzy search and allows the student to favorite preferred mentors. | Mentor search results and mentor favorites list. | Medium | Test | LAB-022, LAB-009 |
| FR-015 | The system shall support personal information viewing during two-way selection. | A student views a project or a mentor views applicant students. | The system displays mentor or applicant student personal information according to permissions. | Authorized personal information. | High | Test | LAB-022, LAB-029 |
| FR-016 | The system shall display community posts and support viewing post details. | A student user logs in and enters the community. | The system displays the community post list, and displays post details after the user clicks a post. | Post list and detail page. | Medium | Demonstration | LAB-023 |
| FR-017 | The system shall allow students to publish, modify, and delete community posts. | A student user submits a post; an enterprise-certified student submits an internship referral post. | The system distinguishes permissions for ordinary posts and internship referral posts, limits posts to within 400 words, supports text formats such as HTML and Markdown, and supports modification and deletion by default for publication functions. | Added, modified, or deleted post. | High | Test | LAB-023, LAB-009 |
| FR-018 | The system shall allow students to publish comments. | A logged-in student submits a comment under any post. | The system saves the comment and displays it synchronously in the post comment area; sensitive words, advertisements, and malicious attacks are used as review criteria. | Comment content visible to all students. | Medium | Test | LAB-024 |
| FR-019 | The system shall allow students to favorite and unfavorite posts. | A student sees an interesting post and performs favorite or unfavorite operation. | The system saves or cancels the student's favorite relationship with the post. | Post list in the favorites folder. | Medium | Test | LAB-025, LAB-009 |
| FR-020 | The system shall support popularity sorting of posts and comments. | A user browses community posts or comment lists. | The system calculates popularity based on factors such as like count, comment count, view count, publication time, and time-decay item, and sorts accordingly. | Posts or comments sorted by popularity. | Medium | Test | LAB-025 |
| FR-021 | The system shall support administrator login. | An administrator logs in using the account and password assigned by the back-end database. | The system verifies the administrator account and provides teacher/student user management and community post management capabilities; the system provides no administrator registration entry. | Administrator login session. | High | Test | LAB-026 |
| FR-022 | The system shall support first-round university identity review for teachers and students. | A user submits a resume or materials. | The system automatically validates required fields; after passing validation, it enters manual review. Administrators complete review within 72 hours and can add or cancel certification qualifications; the system supports state tracking, in-site messages and email feedback, failure reason display, and resubmission. | Review state, certification qualification, and feedback notification. | High | Test | LAB-026 |
| FR-023 | The system shall support second-round enterprise qualification review for students. | A student submits an enterprise certification application. | Administrators view application information and manually approve or reject the student certification application. | Enterprise qualification review result. | High | Test | LAB-027 |
| FR-024 | The system shall allow administrators to review and delete violating posts. | An administrator discovers a violating community post. | The system allows the administrator to view all posts and delete violating posts. | Updated post list and review record. | High | Test | LAB-027 |
| FR-025 | The system shall allow administrators to review and delete violating comments. | An administrator discovers a violating comment. | The system allows the administrator to view comments under all community posts and delete violating comments. | Updated comment list and review record. | High | Test | LAB-027 |

## 5. Non-Functional Requirements

| ID | Quality | Requirement | Fit Criterion | Priority | Verification | Source Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| NFR-001 | Performance | The system shall provide timely feedback for any user input. | For any user input, the system gives feedback within 1 second. | High | Test | LAB-033 |
| NFR-002 | Robustness | The system shall remain normally operational under all possible user inputs. | It does not crash because of abnormal input and provides timely feedback for erroneous operations. | High | Test | LAB-029, LAB-033 |
| NFR-003 | Access Control | The system shall ensure that each type of user can only obtain and modify information within their permissions. | Mentors can only view resumes of students selected for their projects; students cannot view each other's resumes; group members can view basic information but cannot view resumes. | High | Test | LAB-029, LAB-033 |
| NFR-004 | Data Confidentiality | The system shall protect login, registration, and chat data. | User login/registration and chat content must be encrypted; the source document does not specify an encryption algorithm. | High | Inspection | LAB-029 |
| NFR-005 | Abuse Prevention | The system shall restrict abnormal login and operation behavior. | Supports login and operation frequency limits based on IP and user behavior, graphical verification codes, SMS verification codes, and abnormal behavior detection. | High | Test | LAB-029 |
| NFR-006 | Auditability | The system shall support back-end risk-control logs and behavior audit. | Risk-control logs and behavior audit modules support manual analysis and alerting. | Medium | Inspection | LAB-029 |
| NFR-007 | Usability | The system shall allow most new users to naturally find functional modules and learn how to use them. | Usage instructions are provided to guide the remaining users. | Medium | Demonstration | LAB-033 |
| NFR-008 | User Interface Quality | The system interface shall improve efficiency and friendliness around user roles. | The student side may be more attractive; the mentor side should be concise, clear, and aesthetically pleasing; input/output methods, interaction methods, and functional distribution should support work efficiency. | Medium | Inspection | LAB-030 |
| NFR-009 | Correctness | System operation and presentation logic shall conform to functional requirement goals. | Key functional flows are consistent with the functional requirements in this SRS. | High | Test | LAB-033 |
| NFR-010 | Clarity | System descriptions shall be clear and functional boundaries shall be clearly divided. | Requirements, pages, and module responsibilities are not confused. | Medium | Inspection | LAB-033 |
| NFR-011 | Extensibility | The system shall reduce coupling between components and support extension. | Component coupling is reduced, and new functions do not require broad changes to existing modules. | Medium | Inspection | LAB-033 |
| NFR-012 | Browser Compatibility | The system shall be normally accessible through mainstream browsers. | Chrome, Firefox, or Microsoft Edge can access core functions normally. | High | Test | LAB-032, LAB-033 |
| NFR-013 | Portability | The system shall support browsing on multiple device types while maintaining consistent page logic and functions. | Core page logic and functions are consistent between mobile and desktop. | High | Test | LAB-031, LAB-032, LAB-033 |
| NFR-014 | Legal Compliance | User-published content displayed by the system shall comply with relevant laws. | Violating posts or comments can be reviewed and deleted, and displayed content complies with relevant laws. | High | Inspection | LAB-027, LAB-034 |

## 6. Data Requirements

| ID | Data Object | Requirement | Privacy / Integrity Notes | Verification | Source Evidence |
| --- | --- | --- | --- | --- | --- |
| DR-001 | Research internship project | The system shall record title, internship content, start time, recruitment count, mentor profile, affiliated university, field, internship duration, online/offline mode, required skills, and project status. | Project status affects application, management, and mutual evaluation activation. | Inspection | LAB-010, LAB-011, LAB-012, LAB-014 |
| DR-002 | User account | The system shall record name, university, email, user type, student/employee number, password, and verification-code authentication state. | Passwords and the authentication process shall be protected by encryption and access control. | Inspection | LAB-018, LAB-029 |
| DR-003 | Student personal information | The system shall record student name, university, email, major direction, research projects, competition awards, academic performance, and strong skills. | Student resumes cannot be viewed by other students. | Inspection | LAB-021, LAB-029 |
| DR-004 | Mentor personal information | The system shall record mentor name, university, email, major direction, personal homepage URL, professional title, education experience, published papers, and research projects. | Students can view corresponding mentor information when viewing projects. | Inspection | LAB-021, LAB-022 |
| DR-005 | Resume file | The system shall support students uploading local resume files, with formats such as PDF and maximum size 10 MB. | Resume access is permission-controlled, and mentors can only view resumes of students selected for their projects. | Test | LAB-019, LAB-029 |
| DR-006 | Enterprise certification application | The system shall record enterprise email verification information, enterprise certification application information, and review result. | After certification passes, it affects internship referral post publication permission. | Test | LAB-020, LAB-027 |
| DR-007 | Favorite relationship | The system shall record student favorite relationships for projects, mentors, and posts, and support cancellation. | Favorite content updates need to trigger notifications. | Test | LAB-015, LAB-022, LAB-025, LAB-009 |
| DR-008 | Application request | The system shall record project application requests submitted by students for mentor screening. | Application relationships determine which student resumes a mentor can view. | Test | LAB-017, LAB-029 |
| DR-009 | Chat and notification | The system shall record mentor-applicant chat, message reminders, in-site messages, email push, and comment reply notifications. | Chat content must be encrypted. | Test | LAB-014, LAB-015, LAB-026, LAB-029 |
| DR-010 | Post | The system shall record ordinary posts and internship referral posts, with posts within 400 words and support for text formats such as HTML and Markdown. | Referral posts can only be published by enterprise-certified students; content must comply with laws. | Test | LAB-023, LAB-034 |
| DR-011 | Comment | The system shall record student comments on posts and support review criteria such as sensitive words, advertisements, and malicious attacks. | Violating comments can be deleted by administrators. | Test | LAB-024, LAB-027 |
| DR-012 | Popularity indicators | The system shall record or calculate popularity sorting data such as like count, comment count, view count, publication time, and time-decay item. | Weights can be dynamically adjusted, and CTR and conversion rate can be introduced later. | Analysis | LAB-025 |
| DR-013 | Mutual evaluation record | The system shall record mentor evaluation and score of student performance, and student evaluation and score of mentor assistance. | Mutual evaluation results are available for reference by other students and mentors. | Test | LAB-016 |
| DR-014 | Review record | The system shall record required field validation results, manual review state, 72-hour review time limit, failure reason, resubmission, and feedback notification. | Review state affects user certification qualifications and functional permissions. | Test | LAB-026, LAB-027 |
| DR-015 | Relationship model | The system shall support project-mentor, project-student, student-post, student-comment, post-comment, student-mentor, mentor-lab, and administrator-related entity relationships. | Administrators can manage all entity information. | Inspection | LAB-028 |

## 7. Constraints

| ID | Constraint | Evidence Type | Source |
| --- | --- | --- | --- |
| C-001 | The system scope is limited to university research internship information and community internship referrals, excluding social enterprise recruitment and headhunting advertisements. | explicit | LAB-006 |
| C-002 | Registered users shall complete student or mentor identity certification through university email domains and verification codes. | explicit | LAB-018 |
| C-003 | Enterprise-certified students must pass enterprise email verification before publishing internship referral posts. | explicit | LAB-020, LAB-023 |
| C-004 | Administrator account passwords are directly assigned by the back-end database, and the system has no administrator registration entry. | explicit | LAB-026 |
| C-005 | Manual identity review shall be completed by administrators within 72 hours. | explicit | LAB-026 |
| C-006 | Student resume upload supports formats such as PDF, with maximum file size 10 MB. | explicit | LAB-019 |
| C-007 | Community posts are limited to within 400 words and support text formats such as HTML and Markdown. | explicit | LAB-023 |
| C-008 | Mobile devices shall satisfy quad-core 1.5 GHz CPU, 1 GB RAM + 4 GB ROM, Android 7.0 or iOS 8.0 and above, and WeChat 6.5.6 and above. | explicit | LAB-031 |
| C-009 | Desktop devices shall satisfy at least 2 GB memory, broadband network, Windows 7 or Mac OS X 10.9 and above; Chrome, Firefox, or Microsoft Edge is recommended. | explicit | LAB-032 |
| C-010 | The system and requirements documents shall follow GB/T 8566-2007, GB/T 8567-2006, and GB/T 9385-2008, and Python code shall follow PEP8. | explicit | LAB-003 |
| C-011 | Display of user-published content must comply with relevant laws. | explicit | LAB-034 |

## 8. Verification and Acceptance

| ID | Verification Method | Acceptance Focus |
| --- | --- | --- |
| FR-001 | Test | The student home page shows project recommendations based on interests, skills, historical behavior, and tags. |
| FR-002 | Demonstration | After entering the detail page from recommendations or search results, complete project fields are displayed. |
| FR-003 | Test | After a mentor submits project information, the project can be browsed, favorited, and applied to on the student side. |
| FR-004 | Test | After a student searches by conditions such as university and mentor, matching projects are returned. |
| FR-005 | Test | The mentor can chat, adjust recruitment count, and modify project status. |
| FR-006 | Test | The student can favorite and unfavorite projects and view results in the favorites folder. |
| FR-007 | Test | When mentor messages, favorite updates, comment replies, or project applications are triggered, related users receive reminders. |
| FR-008 | Test | After a project ends, teachers and students can evaluate and score each other. |
| FR-009 | Test | After a student submits an application, the mentor management side can view and screen the application. |
| FR-010 | Test | An unauthenticated user accessing complete functions is required to register or log in; after university email verification-code authentication passes, the user can log in. |
| FR-011 | Test | After a student uploads a resume in PDF or another supported format not exceeding 10 MB, authorized users can download and view it. |
| FR-012 | Test | After enterprise email certification passes, the student obtains referral-post publication permission. |
| FR-013 | Test | Student and mentor personal information can be saved and displayed in resume form. |
| FR-014 | Test | A student can search for and favorite mentors by conditions such as university and major direction. |
| FR-015 | Test | Students and mentors can only view personal materials authorized in the two-way selection scenario. |
| FR-016 | Demonstration | After logging into the community, students can browse posts and enter detail pages. |
| FR-017 | Test | Ordinary students can publish ordinary posts, enterprise-certified students can publish referral posts, and posts can be modified, deleted, and limited to no more than 400 words. |
| FR-018 | Test | After a student publishes a comment, the comment is visible to all students in the post comment area and can enter review criteria. |
| FR-019 | Test | Students can favorite and unfavorite posts. |
| FR-020 | Test | Posts and comments can be sorted and displayed according to popularity-formula-related indicators. |
| FR-021 | Test | Administrators log in using back-end-assigned accounts, and the system has no administrator registration entry. |
| FR-022 | Test | User materials enter manual review after automatic field validation, and state and feedback are given within 72 hours. |
| FR-023 | Test | Administrators can approve or reject student enterprise qualification applications. |
| FR-024 | Test | Administrators can view and delete violating posts. |
| FR-025 | Test | Administrators can view and delete violating comments. |
| NFR-001 | Test | Any user input receives system feedback within 1 second. |
| NFR-002 | Test | Abnormal input does not cause system crash and produces error feedback. |
| NFR-003 | Test | Data access permissions for mentors, students, group members, and administrators conform to constraints. |
| NFR-004 | Inspection | Login/registration and chat encryption mechanisms exist; algorithms or protocols are defined separately. |
| NFR-005 | Test | Abnormal behaviors such as high-frequency operations, frequent registration, and massive comments are limited or blocked. |
| NFR-006 | Inspection | Risk-control logs, behavior audit, manual analysis, and alerting capabilities exist. |
| NFR-007 | Demonstration | New users can find main functional modules, and the system provides usage instructions. |
| NFR-008 | Inspection | Student-side and mentor-side interface styles match the goals of corresponding roles. |
| NFR-009 | Test | Actual operation results of core flows are consistent with functional requirements. |
| NFR-010 | Inspection | Functional boundaries and page responsibilities are clear in design documents or implementation. |
| NFR-011 | Inspection | Module coupling and extension points support later functional extension. |
| NFR-012 | Test | Chrome, Firefox, and Microsoft Edge can access core functions. |
| NFR-013 | Test | Core page logic and functions are consistent between mobile and desktop. |
| NFR-014 | Inspection | Violating content can be reviewed and deleted, and displayed content satisfies legal requirements. |
| DR-001 | Inspection | Project information fields are completely defined and used for details, publication, recommendation, and management. |
| DR-002 | Inspection | Registration information fields and certification state are completely defined. |
| DR-003 | Inspection | Student personal information fields are completely defined and permission-controlled. |
| DR-004 | Inspection | Mentor personal information fields are completely defined and can be displayed in two-way selection scenarios. |
| DR-005 | Test | Resume file format, size, and download permission satisfy requirements. |
| DR-006 | Test | Enterprise certification application data affects referral-post permission. |
| DR-007 | Test | Favorite relationships for projects, mentors, and posts can be added and canceled. |
| DR-008 | Test | Application requests are associated with mentor screening flows. |
| DR-009 | Test | Chat, notification, in-site message, and email push records can be generated. |
| DR-010 | Test | Post type, length, and format constraints are enforced. |
| DR-011 | Test | Comments can be saved, displayed, reviewed, and deleted. |
| DR-012 | Analysis | Popularity indicators can be calculated and produce sorting results. |
| DR-013 | Test | Mutual evaluation records can be saved and used as references for other users. |
| DR-014 | Test | Review state, failure reason, and resubmission records can be traced. |
| DR-015 | Inspection | The relationship model covers the entity relationships listed in the source document. |
| C-001 | Inspection | The product scope statement excludes social enterprise recruitment and headhunting advertisements. |
| C-002 | Test | University email and verification-code authentication is effective. |
| C-003 | Test | Students without enterprise certification cannot publish referral posts. |
| C-004 | Inspection | Administrator account source is the back-end database and there is no registration entry. |
| C-005 | Test | The review process records manual review results within 72 hours. |
| C-006 | Test | Resume uploads exceeding 10 MB or unsupported formats are rejected. |
| C-007 | Test | Posts exceeding 400 words are restricted or rejected. |
| C-008 | Inspection | Mobile runtime environment satisfies requirements. |
| C-009 | Inspection | Desktop runtime environment satisfies requirements. |
| C-010 | Inspection | Documents, tests, and Python code follow corresponding standards. |
| C-011 | Inspection | User-published content display complies with relevant laws. |

## 9. Traceability Matrix

| ID | Requirement | Type | Source | Evidence Type | Verification | Confidence |
| --- | --- | --- | --- | --- | --- | --- |
| FR-001 | Personalized project recommendation | Functional | LAB-010 | explicit | Test | High |
| FR-002 | View project details | Functional | LAB-011 | explicit | Demonstration | High |
| FR-003 | Mentor publishes project | Functional | LAB-012, LAB-009 | explicit | Test | High |
| FR-004 | Student project search | Functional | LAB-013 | explicit | Test | High |
| FR-005 | Mentor project management | Functional | LAB-014 | explicit | Test | High |
| FR-006 | Favorite and unfavorite projects | Functional | LAB-015, LAB-009 | explicit | Test | High |
| FR-007 | Project and interaction message reminders | Functional | LAB-015 | explicit | Test | High |
| FR-008 | Teacher-student mutual evaluation after project completion | Functional | LAB-016 | explicit | Test | High |
| FR-009 | Student applies to project | Functional | LAB-017 | explicit | Test | High |
| FR-010 | Campus email registration/login | Functional | LAB-018 | explicit | Test | High |
| FR-011 | Student resume upload | Functional | LAB-019 | explicit | Test | High |
| FR-012 | Enterprise certification and referral permission | Functional | LAB-020 | explicit | Test | High |
| FR-013 | Complete personal information | Functional | LAB-021 | explicit | Test | High |
| FR-014 | Mentor search and favorite | Functional | LAB-022, LAB-009 | explicit | Test | High |
| FR-015 | Two-way selection material viewing | Functional | LAB-022, LAB-029 | explicit | Test | High |
| FR-016 | Community post display | Functional | LAB-023 | explicit | Demonstration | High |
| FR-017 | Publish, modify, and delete posts | Functional | LAB-023, LAB-009 | explicit | Test | High |
| FR-018 | Publish comments | Functional | LAB-024 | explicit | Test | High |
| FR-019 | Favorite and unfavorite posts | Functional | LAB-025, LAB-009 | explicit | Test | High |
| FR-020 | Popularity sorting for posts and comments | Functional | LAB-025 | explicit | Test | High |
| FR-021 | Administrator login | Functional | LAB-026 | explicit | Test | High |
| FR-022 | First-round university identity review for teachers and students | Functional | LAB-026 | explicit | Test | High |
| FR-023 | Second-round student enterprise qualification review | Functional | LAB-027 | explicit | Test | High |
| FR-024 | Post content review and deletion | Functional | LAB-027 | explicit | Test | High |
| FR-025 | Comment content review and deletion | Functional | LAB-027 | explicit | Test | High |
| NFR-001 | Feedback within 1 second | Non-functional | LAB-033 | explicit | Test | High |
| NFR-002 | Robustness and error feedback | Non-functional | LAB-029, LAB-033 | explicit | Test | High |
| NFR-003 | Access and modification within permissions | Non-functional | LAB-029, LAB-033 | explicit | Test | High |
| NFR-004 | Login/registration and chat encryption | Non-functional | LAB-029 | explicit | Inspection | High |
| NFR-005 | Frequency limits, verification codes, and abnormal detection | Non-functional | LAB-029 | explicit | Test | High |
| NFR-006 | Risk-control logs and behavior audit | Non-functional | LAB-029 | explicit | Inspection | High |
| NFR-007 | Usability and usage instructions | Non-functional | LAB-033 | explicit | Demonstration | Medium |
| NFR-008 | User-role-related interface quality | Non-functional | LAB-030 | explicit | Inspection | Medium |
| NFR-009 | Functional logic correctness | Non-functional | LAB-033 | explicit | Test | High |
| NFR-010 | Clarity | Non-functional | LAB-033 | explicit | Inspection | Medium |
| NFR-011 | Extensibility | Non-functional | LAB-033 | explicit | Inspection | Medium |
| NFR-012 | Browser compatibility | Non-functional | LAB-032, LAB-033 | explicit | Test | High |
| NFR-013 | Multi-device portability | Non-functional | LAB-031, LAB-032, LAB-033 | explicit | Test | High |
| NFR-014 | Content legal compliance | Non-functional | LAB-027, LAB-034 | explicit | Inspection | High |
| DR-001 | Research internship project data | Data | LAB-010, LAB-011, LAB-012, LAB-014 | explicit | Inspection | High |
| DR-002 | User account data | Data | LAB-018, LAB-029 | explicit | Inspection | High |
| DR-003 | Student personal information | Data | LAB-021, LAB-029 | explicit | Inspection | High |
| DR-004 | Mentor personal information | Data | LAB-021, LAB-022 | explicit | Inspection | High |
| DR-005 | Resume file | Data | LAB-019, LAB-029 | explicit | Test | High |
| DR-006 | Enterprise certification application | Data | LAB-020, LAB-027 | explicit | Test | High |
| DR-007 | Favorite relationship | Data | LAB-015, LAB-022, LAB-025, LAB-009 | explicit | Test | High |
| DR-008 | Application request | Data | LAB-017, LAB-029 | explicit | Test | High |
| DR-009 | Chat and notification | Data | LAB-014, LAB-015, LAB-026, LAB-029 | explicit | Test | High |
| DR-010 | Post | Data | LAB-023, LAB-034 | explicit | Test | High |
| DR-011 | Comment | Data | LAB-024, LAB-027 | explicit | Test | High |
| DR-012 | Popularity indicators | Data | LAB-025 | explicit | Analysis | High |
| DR-013 | Mutual evaluation record | Data | LAB-016 | explicit | Test | High |
| DR-014 | Review record | Data | LAB-026, LAB-027 | explicit | Test | High |
| DR-015 | Entity relationship model | Data | LAB-028 | explicit | Inspection | High |
| C-001 | Exclude social recruitment and headhunting advertisements | Constraint | LAB-006 | explicit | Inspection | High |
| C-002 | University email authentication | Constraint | LAB-018 | explicit | Test | High |
| C-003 | Enterprise email certification unlocks referral posts | Constraint | LAB-020, LAB-023 | explicit | Test | High |
| C-004 | No administrator registration entry | Constraint | LAB-026 | explicit | Inspection | High |
| C-005 | 72-hour manual review | Constraint | LAB-026 | explicit | Test | High |
| C-006 | Resume maximum 10 MB | Constraint | LAB-019 | explicit | Test | High |
| C-007 | Posts within 400 words and support HTML/Markdown | Constraint | LAB-023 | explicit | Test | High |
| C-008 | Mobile environment constraints | Constraint | LAB-031 | explicit | Inspection | High |
| C-009 | Desktop environment constraints | Constraint | LAB-032 | explicit | Inspection | High |
| C-010 | Standards and PEP8 constraints | Constraint | LAB-003 | explicit | Inspection | High |
| C-011 | User-published content legal compliance | Constraint | LAB-034 | explicit | Inspection | High |
