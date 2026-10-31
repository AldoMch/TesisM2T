# Smart Recipe System Software Requirements Specification (Standard SRS Extract)

## 1. Introduction

### Purpose

This document extracts verifiable requirements from `SmartRecipe_origin.docx` and rewrites them according to the compact SRS standard in `architectural_views_rep-pkg/script/templates/SRS.md`. Its purpose is to provide structured input for architecture generation, test design, and requirements traceability for a deep-learning-based smart recipe system. Source evidence is listed in `smart_recipe_docx_evidence_pack.json`. (Source: SR-001)

### Product Scope

The Smart Recipe System is a deep-learning-based photo recipe generation app. It allows users to recognize food by taking photos, generate ingredient lists and cooking steps, and obtain calorie judgment, food-combination taboo checks, nutrition analysis, diet plans, daily check-ins, community sharing, and personalized recommendations. The source document states that the system is an Android application, while the non-functional requirements require the foreground interface to be usable on common mobile terminals such as Android and iOS devices. (Source: SR-001, SR-002, SR-003, SR-009)

### Intended Audience

This document is intended for general users, health-conscious users, food-making users, food critics, catering companies, system administrators, developers, testers, and downstream architecture generation workflows. Administrators are responsible for daily operations and maintenance, upgrades, fault handling, user management, recipe database management, user feedback handling, and review of user-published data. (Source: SR-002, SR-003)

### References

The source document does not list an independent reference section. Its version history shows initial writing, module-description and flowchart changes, review issue fixes, and re-review issue fixes. (Source: SR-010)

## 2. Overall Description

### Product Perspective

The system includes a mobile app interface and backend services. The app communicates with the backend service layer through Ajax interaction and direct interaction. The backend service layer includes the business layer, control layer, service layer, and data access layer, and is built with Spring Boot and Flask. Spring Boot handles the main business logic, while Flask provides the model inference service. The backend uses MySQL to store structured data and Redis to cache data for improved performance. (Source: SR-004)

### Product Functions Summary

| Capability | Summary | Source |
| --- | --- | --- |
| Personal information | Manage user information, implement account registration and login, and allow administrators to manage accounts in batches. | SR-004 |
| Photo-based recipe recognition | Preprocess food photos, perform validity checks and model inference, and return recipe information or error messages. | SR-005, SR-007, SR-008 |
| Text-based recipe search | Compare user search text with recipe data in the database and return results sorted by relevance. | SR-005, SR-007, SR-008 |
| Health analysis | Combine recipes, nutrition data, and user health data to provide nutrition analysis, diet advice, diet plans, and daily check-ins. | SR-003, SR-005, SR-008 |
| Community sharing | Support users uploading recipe text and images, administrator review before publication, push to other users, likes, comments, and merchant location display. | SR-003, SR-004, SR-007, SR-008 |
| Intelligent recommendation | Recommend recipes based on query history, browsing data, follows, recipe analysis history, and sharing records. | SR-003, SR-004, SR-005, SR-007, SR-008 |
| Administrator management | Allow administrators to add recipes, review user recipes, and maintain users and the recipe database. | SR-002, SR-007, SR-008 |

### User Classes

| User Class | Responsibilities / Needs | Source |
| --- | --- | --- |
| General user | Use photo recognition, recipe generation, calorie judgment, food-combination taboo prompts, health advice, community sharing, and intelligent recommendation. | SR-002, SR-003 |
| Health-conscious user | Focus on dish nutrition, calories, and personalized diet plans. | SR-002, SR-003 |
| Food-making user | Obtain dish names, preparation processes, ingredients, and cooking steps from food images. | SR-003 |
| Food critic | Browse, share, like, and comment on recipe image-and-text content. | SR-003, SR-004 |
| Catering company | Use user-related data to support dish design, marketing strategies, and new dish research and development. | SR-003 |
| System administrator | Perform operations and maintenance, upgrades, fault handling, review of user-published data, and user and recipe database management. | SR-002, SR-003, SR-007 |

### Operating Environment

| Environment | Requirement | Source |
| --- | --- | --- |
| Mobile app | The source document states that the system is developed as an Android application. | SR-002 |
| Mobile terminals | The foreground interface program shall be usable on common user mobile terminals, such as Android and iOS systems. | SR-009 |
| Backend OS | The backend program can run on various mainstream operating systems. | SR-009 |
| Backend frameworks | Spring Boot is used for the main business logic, and Flask is used for the model inference service. | SR-004 |
| Data storage | MySQL stores structured data, and Redis is used as a cache. | SR-004 |

### Assumptions and Dependencies

| ID | Assumption / Dependency | Evidence Type | Source |
| --- | --- | --- | --- |
| AD-001 | Login is a precondition for most business use cases, including photo recognition, text search, sharing, recommendation, administrator adding, and administrator review. | explicit | SR-007 |
| AD-002 | Photo recognition depends on the backend model inference service and existing recipe data. | explicit | SR-005, SR-008 |
| AD-003 | Health analysis depends on recipe data, nutrition data, and user health data. | explicit | SR-005, SR-008 |
| AD-004 | Intelligent recommendation depends on user history records, query data, follows, and recipe sharing records. | explicit | SR-007, SR-008 |
| AD-005 | Publication of community sharing content depends on administrator review. | explicit | SR-004, SR-007, SR-008 |
| AD-006 | The source document does not specify model metrics, API schema, image size limits, privacy compliance, or backup strategy. | explicit | SR-005, SR-009 |

## 3. External Interface Requirements

### User Interfaces

| Interface | Requirement | Source |
| --- | --- | --- |
| Login interface | Support users or administrators selecting an identity and entering account, password, and verification code. | SR-007 |
| User main interface | Support a search box, personal health center, community entry, and camera entry. | SR-008 |
| Photo recognition interface | Support taking or uploading food images, cropping and modifying images, canceling recognition, and submitting analysis. | SR-005, SR-007, SR-008 |
| Recipe display interface | Display recipe data returned by image recognition or text search. | SR-005, SR-008 |
| Health center / nutrition analysis interface | Support editing personal health data, viewing nutrition data, obtaining personalized nutrition advice, diet plans, and daily check-ins. | SR-003, SR-008 |
| Community sharing interface | Support viewing other users' recipe images and text, publishing image-and-text content, liking, and commenting. | SR-003, SR-004, SR-008 |
| Recommendation interface | Display intelligently recommended recipes or recommendation sections. | SR-003, SR-007, SR-008 |
| Administrator interface | Support reviewing user recipes, adding recipes, and uploading datasets. | SR-007, SR-008 |

### Software/API Interfaces

| Interface | Requirement | Source |
| --- | --- | --- |
| Ajax / direct backend interaction | The mobile app interface communicates with the backend service layer through Ajax interaction and direct interaction. | SR-004 |
| Spring Boot service | The backend Spring Boot service is responsible for main business logic processing. | SR-004 |
| Flask inference service | Flask is used to build the model inference service. | SR-004 |
| MySQL | MySQL stores structured data such as user data, recipe information, and nutrition data. | SR-004, SR-006 |
| Redis | Redis caches data to improve performance. | SR-004 |
| Image recognition model | The backend model receives preprocessed image matrix vectors and calculates recipes. | SR-005 |

### Communication Interfaces

The source document states that the mobile app and backend services communicate through Ajax interaction and direct interaction, but does not provide HTTP methods, URL paths, authentication headers, WebSocket, RPC, or third-party interface protocols. (Source: SR-004)

### Data Exchange Formats

The system needs to process account, password, verification code, token, basic user information, user health data, food images, image URLs, image matrix vectors, text search keywords, recipe titles, recipe content, recipe images, taste, category, ingredients, nutrition components, calories, heat, chronic diseases, food-combination taboos, user query history, search history, recommendation features, food sharing images and text, comments, merchant locations, and administrator review results. The source document does not specify JSON schemas, image formats, image size limits, or error code formats. (Source: SR-005, SR-006, SR-008)

## 4. Functional Requirements

| ID | Requirement | Trigger / Input | System Behavior | Output | Priority | Verification | Source |
| --- | --- | --- | --- | --- | --- | --- | --- |
| FR-001 | The system shall support user or administrator login. | A user or administrator selects an identity, enters account, password, and verification code, and clicks login. | The system verifies user permissions. If verification succeeds, it enters the main interface; if verification fails, it remains on the login interface. | Login state or login failure stay. | High | Test | SR-007 |
| FR-002 | The system shall support user account registration/login and administrator batch account management. | A user or administrator enters the personal information module. | The system manages user information and implements user account registration and login; administrators can manage accounts in batches. | User account information or administrator management result. | High | Test | SR-004 |
| FR-003 | The system shall support photo-based recipe recognition. | A logged-in user clicks the camera button, takes a food image, crops it as needed, and uploads it. | The app locally preprocesses the image and performs a simple food check; the food image is uploaded to the server for model inference and combined with recipe data to generate results; non-food images return error information. | Recipe information or invalid image error prompt. | High | Test | SR-005, SR-007, SR-008 |
| FR-004 | The system shall support text-based recipe search. | A logged-in user clicks the text search box, enters recipe search keywords, and searches. | The backend searches the database by text matching and sorts results by relevance. | Recipe result list or not-found failure information. | High | Test | SR-005, SR-007, SR-008 |
| FR-005 | The system shall support nutrition data analysis. | A user clicks nutrition analysis after photo-based recipe recognition. | The system analyzes the recognized recipe data together with server-side nutrition data. | Recipe nutrition data. | High | Test | SR-005, SR-007, SR-008 |
| FR-006 | The system shall support personalized nutrition advice. | A user clicks to obtain personalized nutrition advice after nutrition analysis. | The system combines recipe data, nutrition data, and user health data to generate individual nutrition analysis. | Personalized diet advice. | High | Test | SR-005, SR-007, SR-008 |
| FR-007 | The system shall support personalized diet plans. | A user provides needs and physical conditions, including height, weight, and body measurements. | The system creates a personalized diet plan with calories specified for each meal. | Diet plan. | Medium | Test | SR-003 |
| FR-008 | The system shall support daily check-ins and diet evaluation. | A user performs daily check-in activities and completes the plan cycle. | The system gives an overall diet evaluation, calorie analysis, and subsequent diet advice based on the user's check-in records. | Check-in records, diet evaluation, calorie analysis, and advice. | Medium | Test | SR-003 |
| FR-009 | The system shall support users sharing recipe images and text. | A logged-in user enters the community, clicks the share icon, edits recipe images and text on the edit interface, and uploads them. | The system submits the shared content for administrator review. After approval, it publishes the content to the community and pushes it to other users; if rejected, it returns failure information. | Community image-and-text content or rejection reason. | High | Test | SR-004, SR-007, SR-008 |
| FR-010 | The system shall support community interaction. | A user views recipe image-and-text content published by other users. | The system allows the user to like and comment on the image-and-text content. | Like records and comments. | Medium | Test | SR-003, SR-004 |
| FR-011 | The system shall support intelligent recipe recommendation. | A logged-in user enters the community or initiates a recommendation request. | The system uses recommendation algorithms to generate recommendations based on user follows, past query data, recipe analysis history, and recipe sharing records. | Recommended users, recommended recipes, or recommendation sections. | High | Test | SR-003, SR-004, SR-005, SR-007, SR-008 |
| FR-012 | The system shall support administrators adding recipes. | A logged-in administrator clicks the add recipe button and edits image-and-text content on the add page. | The system adds the new recipe submitted by the administrator to the database; cancellation causes no submission. | New recipe record or no change. | High | Test | SR-007, SR-008 |
| FR-013 | The system shall support administrators reviewing user recipes. | A logged-in administrator clicks the review button and selects a user recipe to view details. | The system allows the administrator to approve or reject the recipe. If approved, the user recipe is uploaded to the community and approval information is returned; if not approved, it is rejected and a rejection message is returned. | Approval or rejection result. | High | Test | SR-007, SR-008 |
| FR-014 | The system shall support administrators handling user feedback. | An administrator receives user feedback. | The administrator handles user feedback to ensure normal application operation and user experience. | Feedback handling result. | Medium | Inspection | SR-002 |
| FR-015 | The system shall support merchant location display. | A user accesses community sharing or merchant-related content. | The system displays merchant locations on a map to help users find dining locations. | Merchant location on a map. | Medium | Demonstration | SR-004 |
| FR-016 | The system shall support data support for catering companies. | A catering company needs references for dish design or marketing strategy. | The system provides some dining student data and characteristic data to support dish design, marketing strategy, and new dish research and development. | Catering data support or characteristic data. | Low | Inspection | SR-003 |

## 5. Non-Functional Requirements

| ID | Quality | Requirement | Metric / Acceptance | Priority | Verification | Source |
| --- | --- | --- | --- | --- | --- | --- |
| NFR-001 | Usability | The system shall be simple and easy to use. | Users can conveniently upload photos and obtain information. | High | Demonstration | SR-002, SR-009 |
| NFR-002 | Usability | The system interface shall be concise, clear, and smooth to operate. | Key process interfaces are clear, and operations have no obvious blocking. | High | Inspection | SR-002 |
| NFR-003 | Performance | The system shall quickly recognize food and generate recipes. | Photo recognition and recipe generation support a smooth user experience. | High | Test | SR-002 |
| NFR-004 | Performance | The system shall have high processing efficiency. | The backend uses Redis caching to improve performance. | Medium | Inspection | SR-004, SR-009 |
| NFR-005 | Reliability | Data storage shall be reliable. | Persistent data is not lost after restart following non-hardware faults. | High | Test | SR-009 |
| NFR-006 | Security | User personal information and uploaded photos shall be strictly protected. | Personal information and photos must not be leaked to third parties. | High | Inspection | SR-002 |
| NFR-007 | Security | Management system access shall only allow account-password authentication. | Any illegal access shall be rejected. | High | Test | SR-009 |
| NFR-008 | Security / Integrity | The system shall reject improper operations and erroneous data writes. | Improper operations are not executed, and erroneous data is not written. | High | Test | SR-009 |
| NFR-009 | Availability | The system shall be immediately restartable after non-hardware faults. | The system can restart immediately after non-hardware faults. | Medium | Demonstration | SR-009 |
| NFR-010 | Atomicity | Uploading images and uploading recipes shall be atomic operations. | Incomplete recipe entry does not occur. | High | Test | SR-009 |
| NFR-011 | Portability | The backend program shall run on various mainstream operating systems. | The backend can be deployed on mainstream operating systems. | Medium | Inspection | SR-009 |
| NFR-012 | Portability | The foreground interface program shall be usable on common mobile terminals. | Common mobile terminals such as Android and iOS systems are supported. | Medium | Inspection | SR-009 |
| NFR-013 | Extensibility | The system shall be modifiable and extensible. | Underlying data representation, backend interfaces, and frontend layout support future business growth and change. | Medium | Analysis | SR-009 |
| NFR-014 | Functional Completeness | The system shall be technically advanced, functionally complete, and highly extensible. | Architecture and module design cover existing functions and preserve room for extension. | Medium | Analysis | SR-009 |

## 6. Data Requirements

| ID | Data Entity / Object | Requirement | Source |
| --- | --- | --- | --- |
| DR-001 | Administrator/user information | The system shall save user ID, name, gender, phone number, avatar URL, address, cancellation status, creation time, update time, and administrator status. | SR-006 |
| DR-002 | User login | The system shall save user ID, user account, user password, token, creation time, and update time. | SR-006 |
| DR-003 | Image | The system shall save image URLs. | SR-006 |
| DR-004 | Recipe | The system shall save recipe title, content, image, taste, category, ingredients, publisher, comments, review status, deletion status, and creation time. | SR-006 |
| DR-005 | Personal health information | The system shall save user ID, height, weight, age, blood pressure, chronic disease description, creation time, and update time. | SR-006 |
| DR-006 | Chronic disease | The system shall save chronic disease information. | SR-006 |
| DR-007 | Health analysis | The system shall save health table ID, feature, publish time, and update time for health analysis. | SR-006 |
| DR-008 | User recommendation | The system shall save user, feature, creation time, and update time for personalized recommendation. | SR-006 |
| DR-009 | Food recommendation | The system shall save food title, content, image, taste, category, merchant, rating, comments, creation time, and update time. | SR-006 |
| DR-010 | Merchant information | The system shall save merchant name, introduction, rating, comment ID, longitude, latitude, creation time, and update time. | SR-006 |
| DR-011 | Comment | The system shall save publisher ID, comment content, creation time, and update time. | SR-006 |
| DR-012 | Ingredient | The system shall save ingredient name and ingredient calories. | SR-006 |
| DR-013 | Ingredient food-combination taboo | The system shall save food-combination taboo relationships between two ingredient IDs. | SR-006 |
| DR-014 | User history data | The system shall save user query history, search history, recipe analysis history, and recipe sharing records for health analysis and recommendation. | SR-008 |

## 7. Constraints

| ID | Constraint | Source |
| --- | --- | --- |
| C-001 | The system is developed as an Android application. | SR-002 |
| C-002 | The foreground interface program shall be usable on common mobile terminals such as Android and iOS. | SR-009 |
| C-003 | The system includes a mobile app interface and backend services. | SR-004 |
| C-004 | The mobile app and backend services communicate through Ajax interaction and direct interaction. | SR-004 |
| C-005 | The backend service layer includes the business layer, control layer, service layer, and data access layer. | SR-004 |
| C-006 | The backend uses Spring Boot for main business logic. | SR-004 |
| C-007 | The backend uses Flask to build the model inference service. | SR-004 |
| C-008 | The backend uses MySQL to store structured data. | SR-004 |
| C-009 | The backend uses Redis to cache data for improved performance. | SR-004 |

## 8. Verification and Acceptance

| Verification Method | Applicable Requirement IDs | Acceptance Basis |
| --- | --- | --- |
| Test | FR-001 to FR-013; NFR-003, NFR-005, NFR-007, NFR-008, NFR-010 | Execute login, photo recognition, text search, nutrition analysis, recommendation, sharing, administrator add/review, security rejection, erroneous write rejection, and atomic upload tests. |
| Inspection | FR-014, FR-016; NFR-002, NFR-004, NFR-006, NFR-011, NFR-012; DR-001 to DR-014; C-001 to C-009 | Inspect management processes, data models, privacy protection, cache design, runtime environment, architecture constraints, and database field coverage. |
| Analysis | NFR-013, NFR-014 | Review underlying data representation, backend interfaces, frontend layout, and module extensibility. |
| Demonstration | FR-015; NFR-001, NFR-009 | Demonstrate merchant map location, usability of core operations, and system restart after non-hardware faults. |

## 9. Traceability Matrix

| ID | Requirement | Type | Source | Evidence Type | Verification | Confidence |
| --- | --- | --- | --- | --- | --- | --- |
| FR-001 | Login | Functional | SR-007 | explicit | Test | High |
| FR-002 | Account registration/login and batch management | Functional | SR-004 | explicit | Test | High |
| FR-003 | Photo-based recipe recognition | Functional | SR-005, SR-007, SR-008 | explicit | Test | High |
| FR-004 | Text-based recipe search | Functional | SR-005, SR-007, SR-008 | explicit | Test | High |
| FR-005 | Nutrition data analysis | Functional | SR-005, SR-007, SR-008 | explicit | Test | High |
| FR-006 | Personalized nutrition advice | Functional | SR-005, SR-007, SR-008 | explicit | Test | High |
| FR-007 | Personalized diet plan | Functional | SR-003 | explicit | Test | High |
| FR-008 | Daily check-in and diet evaluation | Functional | SR-003 | explicit | Test | High |
| FR-009 | Recipe image-and-text sharing | Functional | SR-004, SR-007, SR-008 | explicit | Test | High |
| FR-010 | Community interaction | Functional | SR-003, SR-004 | explicit | Test | High |
| FR-011 | Intelligent recommendation | Functional | SR-003, SR-004, SR-005, SR-007, SR-008 | explicit | Test | High |
| FR-012 | Administrator adds recipe | Functional | SR-007, SR-008 | explicit | Test | High |
| FR-013 | Administrator reviews recipe | Functional | SR-007, SR-008 | explicit | Test | High |
| FR-014 | Handle user feedback | Functional | SR-002 | explicit | Inspection | Medium |
| FR-015 | Merchant location display | Functional | SR-004 | explicit | Demonstration | High |
| FR-016 | Catering company data support | Functional | SR-003 | explicit | Inspection | Medium |
| NFR-001 | Simple and easy operation | Non-functional | SR-002, SR-009 | explicit | Demonstration | High |
| NFR-002 | Concise and smooth interface | Non-functional | SR-002 | explicit | Inspection | High |
| NFR-003 | Fast recognition and generation | Non-functional | SR-002 | explicit | Test | Medium |
| NFR-004 | Processing efficiency and cache | Non-functional | SR-004, SR-009 | explicit | Inspection | High |
| NFR-005 | Reliable data storage | Non-functional | SR-009 | explicit | Test | High |
| NFR-006 | Privacy and photo protection | Non-functional | SR-002 | explicit | Inspection | High |
| NFR-007 | Authentication and illegal access rejection | Non-functional | SR-009 | explicit | Test | High |
| NFR-008 | Reject improper operations and erroneous data | Non-functional | SR-009 | explicit | Test | High |
| NFR-009 | Restart after non-hardware fault | Non-functional | SR-009 | explicit | Demonstration | High |
| NFR-010 | Upload atomicity | Non-functional | SR-009 | explicit | Test | High |
| NFR-011 | Backend portability | Non-functional | SR-009 | explicit | Inspection | High |
| NFR-012 | Foreground mobile terminal compatibility | Non-functional | SR-009 | explicit | Inspection | High |
| NFR-013 | Modifiability and extensibility | Non-functional | SR-009 | explicit | Analysis | High |
| NFR-014 | Functional completeness and extension space | Non-functional | SR-009 | explicit | Analysis | Medium |
| DR-001 | User information | Data | SR-006 | explicit | Inspection | High |
| DR-002 | Login data | Data | SR-006 | explicit | Inspection | High |
| DR-003 | Image data | Data | SR-006 | explicit | Inspection | High |
| DR-004 | Recipe data | Data | SR-006 | explicit | Inspection | High |
| DR-005 | Personal health information | Data | SR-006 | explicit | Inspection | High |
| DR-006 | Chronic disease | Data | SR-006 | explicit | Inspection | High |
| DR-007 | Health analysis | Data | SR-006 | explicit | Inspection | High |
| DR-008 | User recommendation | Data | SR-006 | explicit | Inspection | High |
| DR-009 | Food recommendation | Data | SR-006 | explicit | Inspection | High |
| DR-010 | Merchant information | Data | SR-006 | explicit | Inspection | High |
| DR-011 | Comment | Data | SR-006 | explicit | Inspection | High |
| DR-012 | Ingredient | Data | SR-006 | explicit | Inspection | High |
| DR-013 | Ingredient food-combination taboo | Data | SR-006 | explicit | Inspection | High |
| DR-014 | User history data | Data | SR-008 | explicit | Inspection | High |
| C-001 | Android application | Constraint | SR-002 | explicit | Inspection | High |
| C-002 | Android/iOS terminal | Constraint | SR-009 | explicit | Inspection | High |
| C-003 | Mobile app and backend services | Constraint | SR-004 | explicit | Inspection | High |
| C-004 | Ajax and direct interaction | Constraint | SR-004 | explicit | Inspection | High |
| C-005 | Backend layering | Constraint | SR-004 | explicit | Inspection | High |
| C-006 | Spring Boot | Constraint | SR-004 | explicit | Inspection | High |
| C-007 | Flask inference service | Constraint | SR-004 | explicit | Inspection | High |
| C-008 | MySQL | Constraint | SR-004 | explicit | Inspection | High |
| C-009 | Redis | Constraint | SR-004 | explicit | Inspection | High |
