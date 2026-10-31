# Software Requirements Specification (SRS)

## 1. Introduction

### Product scope
EasyLaTex is an online system for converting mathematical formulas, tables, images, CSV/Excel/PDF files, and handwritten inputs into LaTex code. The system also provides real-time rendering, project/workspace management, collaboration, version control, comments, and export capabilities.

### Intended audience
- Product managers and requirements reviewers validating the EasyLaTex requirement set.
- Developers implementing user management, file processing, AI recognition, rendering, collaboration, and version control modules.
- Test engineers deriving verification scenarios from functional, interface, performance, compatibility, and security requirements.
- Architecture and evaluation agents that need structured requirements for architecture view generation.

## 2. Overall Description

### Product perspective
The system is a browser-based EasyLaTex application with a front-end/back-end separated architecture. It combines OCR and deep learning models to recognize formulas and tables from user inputs, converts recognized content into LaTex code, renders the output for preview, and manages user projects and collaborative versions.

### Product functions summary
- Accept handwritten formulas/tables, images, CSV, Excel, and PDF inputs.
- Recognize mathematical formulas and tables and convert them into LaTex code.
- Provide user registration, login, password recovery, account modification, authentication, and permission control.
- Manage personal and team projects, groups, shared resources, and collaboration.
- Provide a version tree for historical versions, branches, file edits, restoration, downloads, and version comments.
- Support drag-and-drop upload, manual file selection, post-recognition editing, real-time rendering preview, and export to PDF, LaTex source, or image formats.

### User classes
- General user: uploads files, converts content, edits LaTex results, previews and exports outputs.
- Registered user: accesses a personal workspace, manages projects, historical files, and versions.
- Project collaborator: participates in shared projects and group work according to permissions.
- Project owner/group creator: creates projects or groups and controls collaboration access.
- Developer/tester: uses API, database, environment, and security requirements for implementation and validation.

### Operating environment
The system is intended to run through modern browsers that support WebSocket. Target clients include Windows, macOS, and Linux environments, with Chrome, Firefox, Safari, or Edge. Server-side and development dependencies include relational databases, web servers, Python, Node.js, and a compatible LaTex engine.

### Assumptions and dependencies
- Users operate through modern WebSocket-capable browsers.
- AI model image recognition accuracy is expected to reach at least 90%.
- User network connections are stable enough for uploads and downloads.
- Identity security depends on the existing user authentication mechanism.
- Initial user scale and storage demand are relatively small.

## 3. External Interface Requirements

### User interfaces
The system shall provide browser-based interfaces for registration, login, password recovery, project creation and browsing, group creation/joining/browsing, file upload, LaTex result editing, rendering preview, export, version tree navigation, version operations, and comments.

### Software/API interfaces
The system shall expose HTTP/REST APIs for user registration, login, user information management, project management, file upload, download, collaboration sharing, real-time preview, version management, and comments. It shall also provide internal APIs for user verification, file storage, image recognition, LaTex generation, rendering, collaboration management, and version control.

### Communication interfaces
The specification explicitly identifies HTTP/REST API for external module interactions. It also assumes WebSocket-capable browsers, supporting web interaction scenarios where real-time preview or collaborative updates may require browser communication support.

### Data exchange formats
Supported input formats include JPG, PNG, PDF, CSV, Excel `.xlsx`, and hand-drawn formula/table input. Supported outputs include LaTex code, rendered preview, PDF files, LaTex source files, PNG images, and JPEG images.

## 4. Functional Requirements

| ID | Description | Trigger / Input | System behavior | Output | Priority | Verification |
| --- | --- | --- | --- | --- | --- | --- |
| FR-001 | Support handwritten formula and table input | User provides handwritten formula or table through touch screen, digital pen, paper-to-image, or equivalent input | The system shall recognize handwritten formulas and tables and convert them into normalized LaTex code, including single formulas, tables, multi-line formulas, and large table structures | LaTex code representing the handwritten content | High | Test |
| FR-002 | Support image-based formula and table input | User uploads an image containing formulas or tables | The system shall parse PNG, JPEG, BMP, JPG, or similar image formats using recognition models and convert formulas or tables into LaTex code | LaTex code extracted from image content | High | Test |
| FR-003 | Support CSV and Excel input | User uploads CSV or Excel files containing formulas or tabular data | The system shall parse one or more worksheets and convert structured content into LaTex code | LaTex code generated from CSV/Excel content | High | Test |
| FR-004 | Support PDF input | User uploads a PDF file containing formulas, tables, or related content | The system shall extract relevant content from the PDF and convert formulas and tables into LaTex code | LaTex code generated from PDF content | High | Test |
| FR-005 | Register users | New user submits email, username, and password | The system shall validate input format, username uniqueness, and email uniqueness, then create the account if validation succeeds | Registration result and created user account | High | Test |
| FR-006 | Authenticate users | Registered user submits username and password | The system shall validate credentials through encrypted verification and allow access to the workspace after successful login; it shall provide abnormal login prompts for invalid attempts | Authenticated session or login failure message | High | Test |
| FR-007 | Recover password | User forgets account password and provides registered email and username | The system shall verify identity information and support password recovery or access restoration according to the configured recovery process | Password recovery result | Medium | Demonstration |
| FR-008 | Manage projects | Logged-in user creates or views projects | The system shall support creating and viewing projects containing recognition tasks, input/output content, owner information, and last modified time | Project records and project list/detail views | High | Test |
| FR-009 | Manage groups for collaboration | User creates, joins, or browses groups | The system shall support group creation, joining existing groups, browsing group information, managing members, and sharing resources for collaborative work | Group records, membership state, and group views | Medium | Test |
| FR-010 | Manage version tree and historical files | User views or operates on project versions | The system shall show version relationships, locate historical versions, create child versions, view version files, add files to selected versions, edit version files, restore or modify versions, download final versions, and attach version comments | Version tree, version files, branches, comments, and downloadable versions | High | Test |
| FR-011 | Upload files by drag and drop or file selection | User drags a file into the upload area or selects a file manually | The system shall accept supported file types and start parsing/conversion automatically when applicable | Uploaded file record and processing task | High | Demonstration |
| FR-012 | Edit generated LaTex results | User reviews generated LaTex code after recognition | The system shall allow the user to edit generated formula, table, text, format, content, or structure before final output | Updated LaTex code | High | Demonstration |
| FR-013 | Render LaTex preview in real time | User edits or submits LaTex code | The system shall render LaTex code and update the displayed preview so the user can inspect formulas, tables, and text layout | Rendered preview result | High | Test |
| FR-014 | Export generated outputs | User requests export after conversion or editing | The system shall export complete LaTex documents as PDF, export LaTex source files, and export rendered formulas/tables as PNG or JPEG images | PDF, LaTex source file, PNG image, or JPEG image | Medium | Demonstration |
| FR-015 | Store and retrieve project data | User, group, or project operations create or update persistent data | The system shall persist users, groups, projects, versions, file paths, parsed content, workspace content, edit times, and comments according to database schema constraints | Stored database records and retrievable project data | High | Inspection |

## 5. Non-Functional Requirements

| ID | Requirement | Quality attribute | Priority | Verification |
| --- | --- | --- | --- | --- |
| NFR-001 | For common handwritten formulas, standard formula images, and regular CSV/Excel/PDF files, LaTex conversion accuracy shall be at least 88%. | Accuracy | High | Test |
| NFR-002 | The LaTex rendering module shall keep rendering latency below 2 seconds. | Performance | High | Test |
| NFR-003 | Each user operation such as page navigation or loading shall respond within 2 seconds. | Performance | High | Test |
| NFR-004 | The system shall concurrently process at least 100 user requests. | Scalability | High | Test |
| NFR-005 | The system shall support normal access through Chrome, Firefox, Edge, and Safari on PC and mobile browsers. | Compatibility / portability | High | Demonstration |
| NFR-006 | File input compatibility shall include at least JPG, PNG, PDF, CSV, and Excel `.xlsx`. | Compatibility | High | Test |
| NFR-007 | Generated LaTex results shall be compatible with mainstream LaTex editors and compilation environments such as Overleaf and TeXstudio. | Compatibility | Medium | Demonstration |
| NFR-008 | User information including email, username, and password shall be encrypted during storage and transmission. | Security / privacy | High | Inspection |
| NFR-009 | Project collaboration shall enforce permission control with at least project owner and collaborator roles. | Security / access control | High | Test |
| NFR-010 | The system shall provide defenses against common Web vulnerabilities including SQL injection, XSS, and CSRF. | Security | High | Security test |
| NFR-011 | The user interface shall be concise and consistent with user operation habits so users can quickly get started. | Usability | Medium | Demonstration |
| NFR-012 | The system shall use modular design, standardized API design, complete interface documentation, unit tests, integration tests, and deployment documentation to support maintainability and iteration. | Maintainability | Medium | Inspection |

## 6. Data Requirements

| ID | Data entity / object | Requirement |
| --- | --- | --- |
| DR-001 | User account | The system shall store user ID, username, email, encrypted password, team ID, and personal project ID; user ID, username, and email shall be unique. |
| DR-002 | Group | The system shall store group ID, group name, member IDs, and group project IDs; each group shall have at least one member and support many-user/many-group relationships. |
| DR-003 | Project and version content | The system shall store project ID, project name, creator name, version name, project type, previous version project ID, current project file path, file parsed content, workspace content, edit time, comment content, and comment time. |
| DR-004 | Uploaded file | The system shall manage uploaded images, PDFs, CSV files, and Excel files as input files associated with users and projects. |
| DR-005 | Recognition and generation result | The system shall manage recognized content, generated LaTex code, rendered preview results, and exported PDF/source/image artifacts. |
| DR-006 | Authentication and privacy data | The system shall protect passwords, email addresses, uploaded files, images, and formulas through encryption, input validation, and anonymity/de-identification mechanisms where applicable. |

## 7. Constraints

| ID | Constraint |
| --- | --- |
| C-001 | Users are assumed to use modern browsers that support WebSocket technology. |
| C-002 | The AI model is assumed to reach at least 90% image recognition accuracy during design and development. |
| C-003 | Upload and download workflows depend on stable user network connections. |
| C-004 | Identity security depends on the existing user authentication mechanism. |
| C-005 | Minimum client hardware includes Intel Core i3 or equivalent CPU, 4 GB RAM, 20 GB free disk space, integrated graphics, and a 1024x768 display. |
| C-006 | Recommended client hardware includes Intel Core i5 or higher CPU, 8 GB RAM or more, 50 GB free disk space with SSD recommended, graphics acceleration, and 1920x1080 or higher display. |
| C-007 | Supported operating systems include Windows 10 or higher, macOS 10.14 or higher, and Ubuntu 18.04 or higher. |
| C-008 | Supported database management systems include MySQL 8.0 or higher, PostgreSQL 12 or higher, or another compatible relational database. |
| C-009 | Supported web servers include Apache HTTP Server 2.4 or higher and Nginx 1.18 or higher. |
| C-010 | Development/runtime dependencies include Python 3.8 or higher, Node.js 14.x or higher, and TeX Live, MiKTeX, or another compatible LaTex engine. |
| C-011 | External application interfaces use HTTP/REST API. |
| C-012 | The system shall follow privacy-protection regulations such as GDPR and other data-protection regulations. |

## 8. Verification and Acceptance

| Requirement ID | Verification method | Acceptance basis |
|---|---|---|
| FR-001 | Test | Handwritten formula/table inputs are converted into editable LaTex code. |
| FR-002 | Test | Uploaded images in supported formats are parsed and converted into LaTex code. |
| FR-003 | Test | CSV and Excel files, including multiple worksheets when present, are converted into LaTex code. |
| FR-004 | Test | PDF files containing formulas or tables are parsed and converted into LaTex code. |
| FR-005 | Test | New users can register after valid and unique email/username/password checks. |
| FR-006 | Test | Registered users can log in with valid credentials and receive failure prompts for invalid credentials. |
| FR-007 | Demonstration | Users can initiate password recovery using registered identity information. |
| FR-008 | Test | Logged-in users can create and view projects with expected metadata. |
| FR-009 | Test | Users can create, join, and view groups for collaboration. |
| FR-010 | Test | Users can navigate versions, create child versions, edit version files, and add version comments. |
| FR-011 | Demonstration | Users can upload supported files through drag-and-drop or file selection. |
| FR-012 | Demonstration | Users can modify generated LaTex code before final output. |
| FR-013 | Test | Editing or submitting LaTex code updates the rendered preview. |
| FR-014 | Demonstration | Users can export PDF, LaTex source, PNG, or JPEG output artifacts. |
| FR-015 | Inspection | Database schema and persistence logic store users, groups, projects, versions, files, and comments. |
| NFR-001 | Test | Conversion accuracy on supported common inputs is at least 88%. |
| NFR-002 | Test | LaTex render latency remains below 2 seconds. |
| NFR-003 | Test | User operations such as page navigation/loading respond within 2 seconds. |
| NFR-004 | Load test | System handles at least 100 concurrent user requests. |
| NFR-005 | Demonstration | System works through Chrome, Firefox, Edge, and Safari on PC and mobile browsers. |
| NFR-006 | Test | JPG, PNG, PDF, CSV, and `.xlsx` files are accepted or handled as specified. |
| NFR-007 | Demonstration | Generated LaTex can be used in Overleaf or TeXstudio-compatible workflows. |
| NFR-008 | Inspection | User information is encrypted for storage and transmission. |
| NFR-009 | Test | Project owner and collaborator permissions restrict collaborative access. |
| NFR-010 | Security test | SQL injection, XSS, and CSRF defenses are present and effective for relevant inputs. |
| NFR-011 | Demonstration | Users can complete core tasks through a clear interface without extended training. |
| NFR-012 | Inspection | Code style, modular structure, API documentation, tests, and deployment documents are present. |
