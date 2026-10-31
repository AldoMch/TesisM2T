# POCD Persistent Object Consistency Detection Software Requirements Specification (Standard SRS Extract)

## 1. Introduction

### Purpose

This document extracts verifiable requirements from `POCD_origin.docx` and rewrites them according to the compact SRS standard in `architectural_views_rep-pkg/script/templates/SRS.md`. The goal is to provide structured input for POCD (Persistent Object Consistency) consistency detection, repair, test design, and architecture generation. Source evidence is recorded in `pocd_docx_evidence_pack.json`. (Source: POCD-001)

### Product Scope

POCD is a tool for detecting and resolving inconsistencies between class diagram models and databases. The system parses key information from class diagrams and databases, establishes entity, attribute, and relationship matches, detects inconsistencies in fields, types, attributes/columns, classes/tables, relationship multiplicities, relationship types, and missing/extra relationships, and generates or executes class diagram/database repairs after user selection and authorization. (Source: POCD-002, POCD-003, POCD-007, POCD-008, POCD-009)

The system also provides account, file upload/download, detection rule configuration, detection exception configuration, detection report export, historical detection records, help documents, and detection case capabilities. The source document explicitly states that the system uses a front-end and back-end separated architecture and is generally divided into a user interface layer, business logic layer, and data access layer. (Source: POCD-002, POCD-004, POCD-005)

### Intended Audience

This document is intended for POCD users, R&D personnel, testers, IT operations personnel, software reviewers, developers, and later architecture generation workflows. The primary users are class diagram managers with strong technical backgrounds; the system also provides help documents and sample files for users unfamiliar with POCD. (Source: POCD-002, POCD-004)

### References

The source document references materials related to software requirements specifications, software documentation standards, software engineering, database systems, and RUCM/metrics. (Source: POCD-012)

| Ref | Source |
| --- | --- |
| REF-001 | GB/T 9385-2008, Computer Software Requirements Specification |
| REF-002 | GB/T 8567-2006, Specification for Computer Software Documentation |
| REF-003 | Practical Software Engineering Tutorial and Introduction to Database Systems |
| REF-004 | Research on RUCM-Based Software Security Requirements Modeling and Analysis Technology |
| REF-005 | Horzyk, Adrian. "P-INDEX-a fair alternative to H-INDEX." |

## 2. Overall Description

### Product Perspective

POCD addresses the problem that database schemas and class diagrams gradually diverge during iterative development. By parsing class diagrams and databases, establishing matching relationships, executing rule analysis, generating detection reports, and producing repair suggestions, the system helps users monitor and maintain consistency between database schemas and class diagrams. Phase I already had file transfer, inconsistency display, and modification confirmation capabilities; Phase II extends registration/login, file management, detection item settings, repair suggestion display, repair result display, and beginner tutorial capabilities. (Source: POCD-002, POCD-003, POCD-004)

### Product Functions Summary

| Capability | Summary | Source |
| --- | --- | --- |
| Account and file management | Supports registration, login, class diagram/database file upload, file information modification, deletion, and download. | POCD-005 |
| Detection configuration and records | Supports configuring inconsistency detection rules, detection exceptions, exporting detection reports, and viewing historical detection records. | POCD-005 |
| Help and examples | Supports querying help manuals and downloading detection cases. | POCD-005 |
| File parsing | Supports parsing StarUML `.mdj` class diagram files, MySQL database design files, and database relationships. | POCD-006 |
| Entity matching and detection | Supports entity/relationship/attribute matching and detection of intra-class information and inter-class relationship inconsistencies. | POCD-003, POCD-007, POCD-008 |
| Repair suggestions and automatic repair | Supports class diagram repair suggestions, automatic class diagram repair, database repair suggestions, and automatic database repair. | POCD-009 |

### User Classes

| User Class | Responsibilities / Needs | Source |
| --- | --- | --- |
| Class diagram manager / technical user | Uploads class diagram and database files, configures detection rules, performs consistency detection, views reports and repair suggestions, executes repairs, and queries historical records. | POCD-004, POCD-005 |
| Unauthenticated user | Can register an account and can experience core detection functions and use examples/help materials without logging in. | POCD-002, POCD-005 |
| Logged-in user | Can save database and class diagram files, detection history, modification history, detection configuration, and detection exceptions. | POCD-002, POCD-005 |
| New user | Learns system functions through help documents and detection cases. | POCD-002, POCD-005 |

### Operating Environment

| Environment | Requirement | Source |
| --- | --- | --- |
| Class diagram input | MetaData Json (MDJ) class diagram files exported by StarUML. | POCD-006 |
| Database input | MySQL database design files, MySQL database scripts, or database access information composed of address, port, username, password, and database name. | POCD-006 |
| Database access | Database parsing depends on a JDBC-based database connector. | POCD-006 |
| Data exchange | Class diagram and database parsing results are converted into JSON format that is easy for the core business algorithms to accept. | POCD-006 |
| Deployment environment | The source document does not specify operating system, browser compatibility list, server configuration, or deployment method. | POCD-001 |

### Assumptions and Dependencies

| ID | Assumption / Dependency | Evidence Type | Source |
| --- | --- | --- | --- |
| AD-001 | Detection and repair depend on successful parsing of class diagram files and database design files/connections. | explicit | POCD-006, POCD-007, POCD-008 |
| AD-002 | Most file management, configuration, report, and historical record functions depend on user login. | explicit | POCD-005 |
| AD-003 | Relationship-level detection depends on correspondence having been established between classes in the class diagram and tables in the database. | explicit | POCD-008 |
| AD-004 | Automatic repair depends on the user selecting repair items and the system arranging the correct repair order. | explicit | POCD-009 |
| AD-005 | The source document does not specify API schemas, database version, MDJ schema, repair rollback strategy, or complete permission matrix. | explicit | POCD-006, POCD-009, POCD-010 |

## 3. External Interface Requirements

### User Interfaces

| Interface | Requirement | Source |
| --- | --- | --- |
| Registration and login interface | Supports user registration, login, input validation, and error prompts. | POCD-005 |
| File management interface | Supports class diagram/database file upload, file name modification, deletion, download, and file list refresh. | POCD-005 |
| Detection configuration interface | Supports selecting preset inconsistency detection rules, customizing detection rules, configuring detection exceptions, and saving them. | POCD-005 |
| Detection record interface | Supports historical detection record lists and viewing detection record details. | POCD-005 |
| Report export interface | Supports selecting an export location and exporting detection reports, and displays the reason when export fails. | POCD-005 |
| Detection result interface | Supports displaying class diagram/database inconsistencies, matching results, repair suggestions, and repair results. | POCD-003, POCD-007, POCD-008, POCD-009 |
| Help and case interface | Supports help manual browsing/search and detection case browsing, search, and download. | POCD-005 |

### Software/API Interfaces

| Interface | Requirement | Source |
| --- | --- | --- |
| JDBC database connector | The system shall extract table names, field names, primary keys, foreign keys, triggers, and other information from MySQL databases through JDBC. | POCD-006 |
| MDJ parser | The system shall parse classes, interfaces, enumerations, and relationships from StarUML MDJ files through a class diagram parser. | POCD-006 |
| Jackson / JSON conversion | The system shall convert class diagram and database parsing results into JSON format acceptable to the core business algorithms. | POCD-006 |
| Open API | The system shall provide open API interfaces to facilitate third-party application integration and extension. | POCD-010 |

### Communication Interfaces

All sensitive data transmission must use SSL encryption. The source document does not specify HTTP paths, REST/RPC style, message queues, or third-party interface protocols. (Source: POCD-010)

### Data Exchange Formats

The system needs to process user accounts, passwords, contact information, class diagram `.mdj` files, MySQL database design files, database connection information, MySQL scripts, classes/interfaces/enumerations, attributes, relationships, entity tables, relationship tables, table names, field names, primary keys, foreign keys, triggers, detection rules, detection exceptions, matching results, inconsistency reports, repair suggestions, repair operation topology diagrams, repair results, detection reports, historical detection records, modification records, help manuals, and sample files. The source document does not specify complete JSON schemas, field lengths, error codes, or data retention periods. (Source: POCD-005, POCD-006, POCD-003, POCD-009)

## 4. Functional Requirements

| ID | Requirement | Trigger / Input | System Behavior | Output | Priority | Verification | Source |
| --- | --- | --- | --- | --- | --- | --- | --- |
| FR-001 | The system shall allow unauthenticated users to register accounts. | An unauthenticated user enters username, password, contact information, and other personal information and submits it. | The system checks input legality and username uniqueness, saves registration information and prompts registration success when legal, and prompts when input is illegal or duplicated. | Registered account or error prompt. | High | Test | POCD-005 |
| FR-002 | The system shall allow registered users to log in. | A user enters account and password and clicks login. | The system verifies account and password, enters the logged-in state on success, and prompts completion or modification when information is missing or incorrect. | Login state or error prompt. | High | Test | POCD-005 |
| FR-003 | The system shall allow logged-in users to upload class diagram or database files. | A user selects a class diagram or database file and confirms upload. | The system receives the file and completes upload. | Uploaded file record. | High | Test | POCD-005 |
| FR-004 | The system shall allow logged-in users to modify file information. | A user selects a file from the file list, enters new file information, and saves it. | The system validates file information legality, updates the database and refreshes the file list when legal, and prompts when no file is selected or information is illegal. | Updated file list or error prompt. | Medium | Test | POCD-005 |
| FR-005 | The system shall allow logged-in users to delete class diagram and database files. | A user selects a file from the file list and clicks delete. | The system deletes the file record, updates the database, and refreshes the file list. | Updated file list. | Medium | Test | POCD-005 |
| FR-006 | The system shall allow logged-in users to download class diagram and database files. | A user selects a file from the file list and clicks download. | The system starts file transfer and monitors download status; on failure it prompts download failure. | Local file or download failure prompt. | Medium | Test | POCD-005 |
| FR-007 | The system shall allow logged-in users to configure inconsistency detection rules. | A user checks preset detection rules or customizes rules and saves them. | The system saves the detection rule configuration; on save failure it returns the failure reason. | Saved detection rules or failure reason. | High | Test | POCD-005 |
| FR-008 | The system shall allow logged-in users to configure database and class diagram detection exceptions. | A user enters the detection exception configuration interface, checks or customizes exception rules, and saves them. | The system saves the exception configuration to the database; on save failure it returns the failure reason. | Saved detection exceptions or failure reason. | Medium | Test | POCD-005 |
| FR-009 | The system shall allow logged-in users to export detection reports. | A user selects an export location in the detection record detail interface. | The system exports the detection report to the specified location; if export is impossible, it returns the reason and displays the detection report on the front end. | Exported report file or export failure prompt. | Medium | Test | POCD-005 |
| FR-010 | The system shall allow logged-in users to view historical detection records. | A user enters the historical detection record interface and selects a record. | The system displays the specified historical detection record and enters the detail view; when query fails, it returns the reason and goes back to the file management interface. | Historical detection record details or query failure prompt. | Medium | Test | POCD-005 |
| FR-011 | The system shall allow users to query help manuals. | A user selects help or accesses the online help center. | The system provides catalog browsing or search and displays the selected help document. | Operation guidance or problem solution. | Medium | Test | POCD-005 |
| FR-012 | The system shall allow users to download detection cases. | A user browses/searches in the detection case interface and selects a case. | The system provides sample class diagram and database file downloads. | Case files. | Medium | Test | POCD-005 |
| FR-013 | The system shall parse StarUML `.mdj` class diagram files. | A user uploads a `.mdj` class diagram file. | The system validates file format, parses classes, interfaces, enumerations, attributes, and relationships, stores parsing results, and records and prompts errors when format or content is incorrect. | Class diagram parsing data or error prompt. | High | Test | POCD-006 |
| FR-014 | The system shall parse MySQL database design files or database connection information. | A user uploads a MySQL database design file/script or provides database address, port, username, password, and database name. | The system validates the format, extracts table structures, fields, data types, primary keys, foreign keys, triggers, relationships, and other information, stores parsing results, and records and prompts errors on failure. | Database parsing data or error prompt. | High | Test | POCD-006 |
| FR-015 | The system shall extract database relationship types. | The database design file has been uploaded and validated. | The system scans foreign keys and triggers, identifies one-to-one, one-to-many, many-to-many, and implicit complex relationships, and stores relationship details in internal data structures; when a relationship cannot be identified, it records the location and continues processing. | Database relationship summary or error prompt. | High | Test | POCD-006 |
| FR-016 | The system shall establish matching relationships between class diagram and database entities. | Class diagram and database parsing are complete. | The system builds attribute-attribute, entity-entity, and relationship-relationship bipartite graphs based on string, data type, attribute, structure, and relationship similarity, and executes matching algorithms. | Clear matching results. | High | Test | POCD-003 |
| FR-017 | The system shall detect inconsistencies between class diagram fields and database fields. | A user selects field inconsistency detection, and the class diagram file and database connection are loaded. | The system compares class names with table names and attribute names with column names, and records missing or naming-inconsistent cases. | Field inconsistency report. | High | Test | POCD-007 |
| FR-018 | The system shall detect inconsistencies between class diagram attribute types and database column types. | A user selects attribute type and column type detection, and corresponding classes and tables have been matched. | The system compares data type compatibility between corresponding attributes and columns and records incompatibilities. | Type inconsistency report. | High | Test | POCD-007 |
| FR-019 | The system shall detect mismatches between class diagram attributes and database columns. | A user selects attribute-column mismatch detection, and corresponding classes and tables have been matched. | The system compares whether attributes and columns correspond one-to-one and records extra or missing attributes and columns. | Attribute/column mismatch report. | High | Test | POCD-007 |
| FR-020 | The system shall detect mismatches between class diagram classes and database tables. | A user selects class-table mismatch detection, and both the class diagram and database contain at least one class/table. | The system compares the class list and table list and records classes or tables missing from or extra in the class diagram or database. | Class/table mismatch report. | High | Test | POCD-007 |
| FR-021 | The system shall detect relationship multiplicity inconsistencies. | A user selects multiplicity inconsistency detection, corresponding relationships have been established, and relationship multiplicities exist. | The system analyzes the entity relationship model, checks whether upper and lower bounds of many-to-one, one-to-one, and one-to-many relationships are consistent, and prompts on exceptions or insufficient permissions. | Multiplicity inconsistency report or error prompt. | High | Test | POCD-008 |
| FR-022 | The system shall detect relationship type inconsistencies. | A user selects aggregation, composition, and inheritance relationship detection, and corresponding relationships have been established. | The system matches class diagram relationships with database foreign-key representations and checks whether relationship types are consistent; on exception or insufficient permissions, it displays a prompt. | Relationship type inconsistency report or error prompt. | High | Test | POCD-008 |
| FR-023 | The system shall detect mismatches between class diagram relationships and database relationships. | A user selects relationship matching detection and has sufficient permission and complete class diagram/database implementation. | The system compares class diagram relationships and database relationships, extracting relationships that exist in the class diagram but are missing from the database and relationships that exist in the database but are not defined in the class diagram. | Missing/extra relationship report or consistency confirmation. | High | Test | POCD-008 |
| FR-024 | The system shall generate class diagram repair suggestions. | The system has generated an inconsistency detection report, and the user checks class diagram inconsistency items that need repair. | The system generates and displays class diagram repair suggestions based on the user's selections. | Class diagram repair suggestions. | High | Test | POCD-009 |
| FR-025 | The system shall execute automatic class diagram repair. | A user checks class diagram repair items to execute. | The system arranges the correct repair order and modifies the class diagram item by item; on exception it returns exception information. | Repaired class diagram or exception information. | High | Test | POCD-009 |
| FR-026 | The system shall generate database repair suggestions. | A user is logged in, has successfully uploaded a class diagram and database, and selects database repair. | The system runs the database detection program, displays database inconsistency information, and provides repair suggestions; if the file is damaged or cannot be parsed, it prompts re-upload. | Database repair suggestions or exception prompt. | High | Test | POCD-009 |
| FR-027 | The system shall execute automatic database repair. | The database detection program runs successfully, and the user clicks automatic database repair. | The system runs the database repair program and prompts repair completion; when the program has an exception, it displays exception information. | Database repair result or exception information. | High | Test | POCD-009 |

## 5. Non-Functional Requirements

| ID | Quality | Requirement | Metric / Acceptance | Priority | Verification | Source |
| --- | --- | --- | --- | --- | --- | --- |
| NFR-001 | Performance | The system shall support fast and accurate analysis of large databases and complex class diagrams. | For a large database containing thousands of entities, inconsistency detection shall be completed within 30 minutes. | High | Test | POCD-010 |
| NFR-002 | Performance | The system shall limit CPU usage while executing detection tasks. | CPU usage does not exceed 30%. | High | Test | POCD-010 |
| NFR-003 | Performance | The system shall limit memory usage while executing detection tasks. | Memory usage is controlled within 2 GB. | High | Test | POCD-010 |
| NFR-004 | Usability / Performance | The system shall support an asynchronous processing mechanism. | Users can continue other work during detection. | High | Demonstration | POCD-010 |
| NFR-005 | Usability | The user interface shall be concise and intuitive and reduce learning cost. | Provides a quick-start operation experience. | Medium | Inspection | POCD-010 |
| NFR-006 | Usability | The system shall provide clear navigation, intuitive icons, and explicit operation feedback. | Success, error, and waiting states all have prompts. | Medium | Demonstration | POCD-010 |
| NFR-007 | Security | Sensitive data transmission shall use SSL encryption. | All sensitive data transmission uses SSL. | High | Inspection | POCD-010 |
| NFR-008 | Security | The system shall implement role-based access control. | Users can access only authorized resources. | High | Test | POCD-010 |
| NFR-009 | Security | The system shall perform regular security audits. | Potential security vulnerabilities can be discovered and fixed. | Medium | Inspection | POCD-010 |
| NFR-010 | Auditability | The system shall record operation logs. | Operation logs support after-the-fact review and monitoring. | Medium | Inspection | POCD-010 |
| NFR-011 | Extensibility | The system shall use modular design. | Functional modules can be independently developed and deployed. | Medium | Analysis | POCD-010 |
| NFR-012 | Interoperability | The system shall provide open API interfaces. | Third-party applications can integrate and extend the system. | Medium | Inspection | POCD-010 |
| NFR-013 | Data Extensibility | Database design shall be forward-looking. | It can accommodate data types and structures that may be added in the future. | Medium | Analysis | POCD-010 |
| NFR-014 | Maintainability | Code shall follow industry-standard coding conventions. | Code is readable and maintainable. | Medium | Inspection | POCD-010 |
| NFR-015 | Maintainability | System documentation shall be comprehensive. | Includes design documents, user manuals, and operation guides. | Medium | Inspection | POCD-010 |
| NFR-016 | Testability | The system shall implement an automated test framework. | System stability and reliability can be verified after each update. | Medium | Demonstration | POCD-010 |
| NFR-017 | Usability | Page layout shall be based on functional access frequency and conform to ergonomics. | High-frequency functions are easier to access. | Medium | Inspection | POCD-011 |
| NFR-018 | Usability | Important functions shall be placed in obvious or easy-to-associate locations. | Users can quickly find important functions. | Medium | Demonstration | POCD-011 |
| NFR-019 | Usability | Users shall be able to obtain needed information through few hierarchy levels. | Desired information can be obtained in three clicks or fewer. | Medium | Test | POCD-011 |
| NFR-020 | Usability | The system shall reduce keyboard and mouse switching. | Most operations can be completed with the mouse only. | Low | Demonstration | POCD-011 |

## 6. Data Requirements

| ID | Data Entity / Object | Requirement | Source |
| --- | --- | --- | --- |
| DR-001 | User account data | The system shall store registered users' usernames, passwords, contact information, and login states. | POCD-005 |
| DR-002 | Class diagram files | The system shall store uploaded StarUML `.mdj` class diagram files and their file names, parsing states, and parsing results. | POCD-005, POCD-006 |
| DR-003 | Database design files / connection information | The system shall process MySQL database design files, MySQL scripts, or database connection information. | POCD-006 |
| DR-004 | Class diagram parsing model | The system shall store class diagram information such as classes, interfaces, enumerations, attributes, and relationships. | POCD-006 |
| DR-005 | Database parsing model | The system shall store database information such as table names, field names, primary keys, foreign keys, triggers, table structures, data types, and relationships. | POCD-006 |
| DR-006 | Detection rule configuration | The system shall store inconsistency detection rules selected or customized by users. | POCD-005 |
| DR-007 | Detection exception configuration | The system shall store classes, database tables, and exception rules configured by users that do not need to be detected. | POCD-005 |
| DR-008 | Matching results | The system shall store or output matching results for entities, attributes, and relationships for later detection. | POCD-003 |
| DR-009 | Inconsistency detection reports | The system shall store detection results for fields, types, attributes/columns, classes/tables, relationship multiplicities, relationship types, and relationship matching. | POCD-007, POCD-008 |
| DR-010 | Repair suggestions and repair results | The system shall store class diagram/database repair suggestions, repair order, repair operations, and repaired class diagram or database results. | POCD-009 |
| DR-011 | Historical detection and modification records | The system shall store historical inconsistency detection information and modification records for user viewing. | POCD-005 |
| DR-012 | Help manuals and detection cases | The system shall provide help manuals, FAQs, sample class diagrams, and database files. | POCD-005 |
| DR-013 | Operation logs | The system shall record operation logs to support review and monitoring. | POCD-010 |

## 7. Constraints

| ID | Constraint | Source |
| --- | --- | --- |
| C-001 | The system architecture is divided into a user interface layer, business logic layer, and data access layer. | POCD-002 |
| C-002 | The system uses a front-end and back-end separated architecture. | POCD-002 |
| C-003 | Class diagram parsing input shall support the MDJ format exported by StarUML. | POCD-006 |
| C-004 | Database parsing input shall support MySQL database design files or MySQL database scripts. | POCD-006 |
| C-005 | Database connection parsing depends on a JDBC database connector. | POCD-006 |
| C-006 | Class diagram and database parsing results shall be converted into JSON format acceptable to the core business algorithms. | POCD-006 |
| C-007 | Class diagram parsing results are stored internally as Java objects and converted through Jackson. | POCD-006 |
| C-008 | Sensitive data transmission must use SSL encryption. | POCD-010 |
| C-009 | The source document does not specify concrete deployment OS, browser scope, database version, or server configuration. | POCD-001 |

## 8. Verification and Acceptance

| Verification Method | Applicable Requirement IDs | Acceptance Basis |
| --- | --- | --- |
| Test | FR-001 to FR-027; NFR-001, NFR-002, NFR-003, NFR-008, NFR-019 | Execute account, file, configuration, parsing, matching, detection, repair, report, history, help, performance, resource limit, access control, and three-click tests; results satisfy corresponding requirements. |
| Inspection | NFR-005, NFR-007, NFR-009, NFR-010, NFR-012, NFR-014, NFR-015, NFR-017; DR-001 to DR-013; C-001 to C-009 | Inspect interfaces, documents, logs, permissions, secure transmission, APIs, data model, architecture constraints, and coding conventions. |
| Analysis | NFR-011, NFR-013 | Review modular design, database forward compatibility, and future data type/structure extensibility. |
| Demonstration | NFR-004, NFR-006, NFR-016, NFR-018, NFR-020 | Demonstrate asynchronous detection, operation feedback, automated test framework, discoverability of important functions, and mouse-dominant operation paths. |

## 9. Traceability Matrix

| ID | Requirement | Type | Source | Evidence Type | Verification | Confidence |
| --- | --- | --- | --- | --- | --- | --- |
| FR-001 | Account registration | Functional | POCD-005 | explicit | Test | High |
| FR-002 | User login | Functional | POCD-005 | explicit | Test | High |
| FR-003 | File upload | Functional | POCD-005 | explicit | Test | High |
| FR-004 | File information modification | Functional | POCD-005 | explicit | Test | High |
| FR-005 | File deletion | Functional | POCD-005 | explicit | Test | High |
| FR-006 | File download | Functional | POCD-005 | explicit | Test | High |
| FR-007 | Configure detection rules | Functional | POCD-005 | explicit | Test | High |
| FR-008 | Configure detection exceptions | Functional | POCD-005 | explicit | Test | High |
| FR-009 | Export detection report | Functional | POCD-005 | explicit | Test | High |
| FR-010 | View historical detection records | Functional | POCD-005 | explicit | Test | High |
| FR-011 | Query help manual | Functional | POCD-005 | explicit | Test | High |
| FR-012 | Download detection cases | Functional | POCD-005 | explicit | Test | High |
| FR-013 | Parse class diagram files | Functional | POCD-006 | explicit | Test | High |
| FR-014 | Parse database design | Functional | POCD-006 | explicit | Test | High |
| FR-015 | Extract database relationships | Functional | POCD-006 | explicit | Test | High |
| FR-016 | Establish entity matching relationships | Functional | POCD-003 | explicit | Test | High |
| FR-017 | Field inconsistency detection | Functional | POCD-007 | explicit | Test | High |
| FR-018 | Type inconsistency detection | Functional | POCD-007 | explicit | Test | High |
| FR-019 | Attribute/column mismatch detection | Functional | POCD-007 | explicit | Test | High |
| FR-020 | Class/table mismatch detection | Functional | POCD-007 | explicit | Test | High |
| FR-021 | Relationship multiplicity detection | Functional | POCD-008 | explicit | Test | High |
| FR-022 | Relationship type detection | Functional | POCD-008 | explicit | Test | High |
| FR-023 | Relationship matching detection | Functional | POCD-008 | explicit | Test | High |
| FR-024 | Class diagram repair suggestions | Functional | POCD-009 | explicit | Test | High |
| FR-025 | Automatic class diagram repair | Functional | POCD-009 | explicit | Test | High |
| FR-026 | Database repair suggestions | Functional | POCD-009 | explicit | Test | High |
| FR-027 | Automatic database repair | Functional | POCD-009 | explicit | Test | High |
| NFR-001 | Large-scale detection time limit | Non-functional | POCD-010 | explicit | Test | High |
| NFR-002 | CPU limit | Non-functional | POCD-010 | explicit | Test | High |
| NFR-003 | Memory limit | Non-functional | POCD-010 | explicit | Test | High |
| NFR-004 | Asynchronous processing | Non-functional | POCD-010 | explicit | Demonstration | High |
| NFR-005 | Concise and intuitive interface | Non-functional | POCD-010 | explicit | Inspection | High |
| NFR-006 | Navigation, icons, and feedback | Non-functional | POCD-010 | explicit | Demonstration | High |
| NFR-007 | SSL encryption | Non-functional | POCD-010 | explicit | Inspection | High |
| NFR-008 | Role-based access control | Non-functional | POCD-010 | explicit | Test | High |
| NFR-009 | Security audit | Non-functional | POCD-010 | explicit | Inspection | High |
| NFR-010 | Operation logs | Non-functional | POCD-010 | explicit | Inspection | High |
| NFR-011 | Modular design | Non-functional | POCD-010 | explicit | Analysis | High |
| NFR-012 | Open API | Non-functional | POCD-010 | explicit | Inspection | High |
| NFR-013 | Database extensibility | Non-functional | POCD-010 | explicit | Analysis | High |
| NFR-014 | Coding conventions | Non-functional | POCD-010 | explicit | Inspection | High |
| NFR-015 | System documentation | Non-functional | POCD-010 | explicit | Inspection | High |
| NFR-016 | Automated testing | Non-functional | POCD-010 | explicit | Demonstration | High |
| NFR-017 | Access-frequency-based layout | Non-functional | POCD-011 | explicit | Inspection | High |
| NFR-018 | Important function placement | Non-functional | POCD-011 | explicit | Demonstration | High |
| NFR-019 | Three-click access | Non-functional | POCD-011 | explicit | Test | High |
| NFR-020 | Reduce keyboard/mouse switching | Non-functional | POCD-011 | explicit | Demonstration | High |
| DR-001 | User account data | Data | POCD-005 | explicit | Inspection | High |
| DR-002 | Class diagram files | Data | POCD-005, POCD-006 | explicit | Inspection | High |
| DR-003 | Database files / connection information | Data | POCD-006 | explicit | Inspection | High |
| DR-004 | Class diagram parsing model | Data | POCD-006 | explicit | Inspection | High |
| DR-005 | Database parsing model | Data | POCD-006 | explicit | Inspection | High |
| DR-006 | Detection rule configuration | Data | POCD-005 | explicit | Inspection | High |
| DR-007 | Detection exception configuration | Data | POCD-005 | explicit | Inspection | High |
| DR-008 | Matching results | Data | POCD-003 | explicit | Inspection | High |
| DR-009 | Inconsistency detection report | Data | POCD-007, POCD-008 | explicit | Inspection | High |
| DR-010 | Repair suggestions and results | Data | POCD-009 | explicit | Inspection | High |
| DR-011 | Historical detection and modification records | Data | POCD-005 | explicit | Inspection | High |
| DR-012 | Help manuals and cases | Data | POCD-005 | explicit | Inspection | High |
| DR-013 | Operation logs | Data | POCD-010 | explicit | Inspection | High |
| C-001 | Three-layer architecture | Constraint | POCD-002 | explicit | Inspection | High |
| C-002 | Front-end/back-end separation | Constraint | POCD-002 | explicit | Inspection | High |
| C-003 | MDJ class diagram format | Constraint | POCD-006 | explicit | Inspection | High |
| C-004 | MySQL design input | Constraint | POCD-006 | explicit | Inspection | High |
| C-005 | JDBC connector | Constraint | POCD-006 | explicit | Inspection | High |
| C-006 | JSON parsing results | Constraint | POCD-006 | explicit | Inspection | High |
| C-007 | Java objects and Jackson | Constraint | POCD-006 | explicit | Inspection | High |
| C-008 | SSL encryption | Constraint | POCD-010 | explicit | Inspection | High |
| C-009 | Unspecified deployment environment | Constraint | POCD-001 | explicit | Inspection | High |
