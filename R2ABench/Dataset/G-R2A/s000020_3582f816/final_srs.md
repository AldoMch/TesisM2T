# Software Requirements Specification

## 1. Introduction

### Purpose
This SRS defines evidence-backed requirements for the MyEMS repository sample `s000020_3582f816` at commit `ac856ead88566ccd9e5812c301462c43c7bbd2d8`, focusing on the supported web administration and API service behavior visible in the repository evidence.

### Product scope
MyEMS includes:
- A RESTful API service for MyEMS components and third-party applications.
- A web administration interface with routed pages including user settings and settings pages.

Scope is limited to behaviors and interfaces directly supported by the evidence pack.  
Sources: [E001], [E003], [E004], [E005]

### Intended audience
- Product owners and maintainers of MyEMS
- Test and QA engineers
- Integrators of MyEMS components and third-party applications
- Administrators using the web administration interface

Sources: [E001], [E004], [E005]

### References
- Repository: `https://github.com/MyEMS/myems`
- Snapshot: `https://github.com/MyEMS/myems/tree/ac856ead88566ccd9e5812c301462c43c7bbd2d8`
- Evidence files:
  - `myems-api/README.md` [E004]
  - `myems-admin/app/api.js` [E003]
  - `myems-admin/app/config.router.js` [E001], [E002], [E005]
  - `myems-admin/app/controllers.js` [E006]

## 2. Overall Description

### Product perspective
The repository contains at least two relevant product parts:
1. A web administration application (`myems-admin`) that defines routed views and client-side service loading.
2. An API service (`myems-api`) described as a RESTful API for MyEMS components and third-party applications.

The admin application accesses the API through an `/api/` path built from the browser protocol, hostname, and port, indicating same-origin reverse-proxy deployment behavior.  
Sources: [E003], [E004]

### Product functions summary
Supported functions evidenced in the repository include:
- Exposing a RESTful API service for MyEMS components and third-party applications.
- Providing a user settings page at route `/user`.
- Providing a settings contact page at route `/contact`.
- Loading user, login, tariff, category, and contact-related client modules for corresponding admin pages.

Sources: [E001], [E004], [E005]

### User classes
| User class | Description | Evidence |
|---|---|---|
| Administrator / web admin user | Uses routed administration pages such as user settings and contact settings. | [E001], [E005] |
| MyEMS component integrator | Uses the RESTful API service from MyEMS components. | [E004] |
| Third-party application integrator | Uses the RESTful API service from external applications. | [E004] |

### Operating environment
| Aspect | Supported environment |
|---|---|
| Admin client | Browser-based web application using current page protocol, host, and port to reach `/api/`. |
| API service runtime | Python-based service with dependencies including `falcon`, `falcon_cors`, `gunicorn`, `mysql-connector-python`, `openpyxl`, `pillow`, and others. |
| Development OS | Linux and Windows quick-run instructions are explicitly mentioned. |
| Deployment option | Docker installation is explicitly supported. |

Sources: [E003], [E004]

### Assumptions and dependencies
| Item | Statement | Evidence type | Evidence |
|---|---|---|---|
| Reverse proxy dependency | The deployment is expected to expose the API at `/api/` on the same protocol, host, and port as the web app, with Nginx mentioned to avoid CORS issues. | explicit | [E003] |
| Python package dependency | The API service depends on listed Python packages including `falcon`, `falcon_cors`, `mysql-connector-python`, and `gunicorn`. | explicit | [E004] |
| Modular admin UI dependency | The admin UI depends on lazy-loaded client modules and libraries such as `ui.select`, `ui.checkbox`, `daterangepicker`, `toaster`, and SweetAlert for certain pages. | explicit | [E001], [E005] |

## 3. External Interface Requirements

### User interfaces
| Interface | Requirement | Source |
|---|---|---|
| User settings page | The system shall provide a web administration route at `/user` with page title `MENU.USERSETTING.USER`. | [E001] |
| Contact settings page | The system shall provide a web administration route at `/contact` with page title `MENU.SETTINGS.CONTACT`. | [E005] |

### Software/API interfaces
| Interface | Requirement | Source |
|---|---|---|
| REST API | The system shall expose a RESTful API service for MyEMS components and third-party applications. | [E004] |
| Admin-to-API endpoint | The admin client shall address the API using `{window.location.protocol}//{window.location.hostname}:{window.location.port}/api/`. | [E003] |

### Communication interfaces
| Interface | Requirement | Source |
|---|---|---|
| Browser-to-API communication | The deployed system shall support browser access to the API through the `/api/` path on the same host and port as the web application. | [E003] |

### Data exchange formats
The evidence pack explicitly states that the API is RESTful but does not provide reliable payload-format details. No additional data exchange format requirement is specified beyond RESTful API interaction.  
Source: [E004]

## 4. Functional Requirements

| ID | Description | Trigger/Input | System behavior | Output | Priority | Verification | Source evidence |
|---|---|---|---|---|---|---|---|
| FR-001 | Provide RESTful API service | A MyEMS component or third-party application sends an API request | The system shall expose a RESTful API service for MyEMS components and third-party applications | API response from the RESTful service | High | Inspection | [E004] |
| FR-002 | Provide user settings route | A web admin user navigates to `/user` | The system shall display the user settings page identified by page title `MENU.USERSETTING.USER` | User settings page rendered in the admin UI | High | Demonstration | [E001] |
| FR-003 | Load user-management client modules for user settings route | The `/user` route is activated | The system shall load the route’s declared client modules, including user service, user controller, login service, login controller, and related UI libraries | Route dependencies available and page able to initialize | Medium | Inspection | [E001], [E002] |
| FR-004 | Provide contact settings route | A web admin user navigates to `/contact` | The system shall display the contact settings page identified by page title `MENU.SETTINGS.CONTACT` | Contact settings page rendered in the admin UI | Medium | Demonstration | [E005] |
| FR-005 | Load tariff/category/contact-related client modules for contact settings route | The `/contact` route is activated | The system shall load the route’s declared client modules, including tariff service, tariff constants, category service, and contact controller dependencies | Route dependencies available and page able to initialize | Medium | Inspection | [E005] |
| FR-006 | Resolve API base path from current browser location | The admin client needs the API base URL | The system shall construct the API base URL from the current page protocol, hostname, and port, ending with `/api/` | API base URL string for client requests | High | Test | [E003] |

## 5. Non-Functional Requirements

| ID | Quality attribute | Requirement | Priority | Verification | Evidence type | Source evidence |
|---|---|---|---|---|---|---|
| NFR-001 | Compatibility | The admin client shall be deployable so that API requests are sent to the same protocol, hostname, and port as the web application under the `/api/` path. | High | Test | explicit | [E003] |
| NFR-002 | Portability | The API service shall support development quick-run on Linux and Windows environments. | Medium | Inspection | explicit | [E004] |
| NFR-003 | Deployability | The API service shall support Docker-based installation as one installation option. | Medium | Inspection | explicit | [E004] |
| NFR-004 | Modularity | The admin UI shall support lazy loading of route-specific modules and libraries before route activation. | Medium | Inspection | explicit | [E001], [E005] |

## 6. Data Requirements

| ID | Data item / entity | Requirement | Evidence type | Source |
|---|---|---|---|---|
| DR-001 | User data | The system shall support a user-related administration page and associated client service/controller modules for user data operations. | inferred from route/service naming | [E001], [E002] |
| DR-002 | Contact settings data | The system shall support a contact-related settings page and associated client controller/module loading. | inferred from route/service naming | [E005] |
| DR-003 | Tariff data | The system shall support tariff-related client service and constant loading within settings workflows. | inferred from service naming | [E005] |
| DR-004 | Category data | The system shall support category-related client service loading within settings workflows. | inferred from service naming | [E005] |
| DR-005 | API base URL value | The admin client shall derive and use an API base URL composed of browser protocol, hostname, port, and the `/api/` suffix. | explicit | [E003] |

## 7. Constraints

| ID | Constraint | Source |
|---|---|---|
| C-001 | The API service is constrained to Python package dependencies including `anytree`, `simplejson`, `mysql-connector-python`, `falcon`, `falcon_cors`, `falcon-multipart`, `gunicorn`, `et_xmlfile`, `jdcal`, `openpyxl`, `pillow`, and `python-decouple`. | [E004] |
| C-002 | To avoid CORS issues, deployment is constrained to exposing `myems-api` through an `/api/` path on the same IP/port as the web application, with Nginx identified as the proxy mechanism. | [E003] |
| C-003 | The admin UI is constrained to route/module loading mechanisms that use the declared lazy-loaded libraries and page assets. | [E001], [E005] |

## 8. Verification and Acceptance

| Requirement ID | Verification method | Acceptance basis |
|---|---|---|
| FR-001 | Inspection | API service documentation and exposed interface indicate RESTful API service for MyEMS components and third-party applications. |
| FR-002 | Demonstration | Navigating to `/user` renders the configured user settings page. |
| FR-003 | Inspection | Route definition shows required modules and libraries are loaded for `/user`. |
| FR-004 | Demonstration | Navigating to `/contact` renders the configured contact settings page. |
| FR-005 | Inspection | Route definition shows required modules and libraries are loaded for `/contact`. |
| FR-006 | Test | Client computes API base URL as current protocol + hostname + port + `/api/`. |
| NFR-001 | Test | Deployed admin successfully accesses API through same-origin `/api/`. |
| NFR-002 | Inspection | API documentation includes Linux and Windows quick-run guidance. |
| NFR-003 | Inspection | API documentation includes Docker installation option. |
| NFR-004 | Inspection | Route configuration uses lazy loading before page activation. |
| DR-001 | Inspection | Evidence shows user-related page and modules are present. |
| DR-002 | Inspection | Evidence shows contact-related page and modules are present. |
| DR-003 | Inspection | Evidence shows tariff-related client modules are present. |
| DR-004 | Inspection | Evidence shows category-related client modules are present. |
| DR-005 | Test | Derived API base URL matches specified browser-based composition. |

## 9. Traceability Matrix

| ID | Requirement | Type | Source | Evidence Type | Verification | Confidence |
|---|---|---|---|---|---|---|
| FR-001 | Provide RESTful API service | Functional | E004 | explicit | Inspection | High |
| FR-002 | Provide user settings route | Functional | E001 | explicit | Demonstration | High |
| FR-003 | Load user-management client modules for user settings route | Functional | E001, E002 | explicit | Inspection | High |
| FR-004 | Provide contact settings route | Functional | E005 | explicit | Demonstration | High |
| FR-005 | Load tariff/category/contact-related client modules for contact settings route | Functional | E005 | explicit | Inspection | Medium |
| FR-006 | Resolve API base path from current browser location | Functional | E003 | explicit | Test | High |
| NFR-001 | Same-origin `/api/` deployment compatibility | Non-functional | E003 | explicit | Test | High |
| NFR-002 | Linux and Windows development portability | Non-functional | E004 | explicit | Inspection | High |
| NFR-003 | Docker installation support | Non-functional | E004 | explicit | Inspection | High |
| NFR-004 | Lazy-loaded modular UI | Non-functional | E001, E005 | explicit | Inspection | Medium |
| DR-001 | User data support | Data | E001, E002 | inferred | Inspection | Medium |
| DR-002 | Contact settings data support | Data | E005 | inferred | Inspection | Medium |
| DR-003 | Tariff data support | Data | E005 | inferred | Inspection | Medium |
| DR-004 | Category data support | Data | E005 | inferred | Inspection | Medium |
| DR-005 | API base URL value | Data | E003 | explicit | Test | High |
| C-001 | Python dependency constraint | Constraint | E004 | explicit | Inspection | High |
| C-002 | Reverse-proxy and same-origin constraint | Constraint | E003 | explicit | Inspection | High |
| C-003 | Admin lazy-loading constraint | Constraint | E001, E005 | explicit | Inspection | Medium |
