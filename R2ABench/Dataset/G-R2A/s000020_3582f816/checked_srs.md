# Checked Software Requirements Specification: MyEMS REST API and Admin Routing

## 1. Introduction

### 1.1 Purpose

This Software Requirements Specification defines the checked requirements for the MyEMS REST API service and the related MyEMS Admin routing behavior needed for architecture view generation. It consolidates the reviewed requirements into a standard SRS format and omits review notes, provenance details, and supporting-material identifiers.

### 1.2 Product Scope

The system covered by this SRS consists of:

- A RESTful API service intended for MyEMS components and third-party applications.
- A browser-based MyEMS Admin application that provides settings routes for user management and contact settings.
- Admin-side API endpoint resolution under the `/api/` path of the current browser origin.
- Lazy-loaded client modules used by the Admin routing configuration.
- Deployment and runtime support for the API service, including Python dependencies, development quick-run modes, and Docker-based installation.

This SRS does not expand the checked scope to every MyEMS platform component unless a requirement below states that component explicitly.

### 1.3 Intended Audience

The intended audience includes architecture designers, developers, deployers, testers, and evaluators who need a concise requirement set for generating or checking architecture views.

### 1.4 Definitions and Abbreviations

- API: Application Programming Interface.
- Admin application: The browser-based MyEMS administration client.
- REST: Representational State Transfer.
- SRS: Software Requirements Specification.
- UI: User Interface.

## 2. Overall Description

### 2.1 Product Perspective

The product includes a web administration client and an API service. The Admin application runs in a browser, defines client-side routes, and resolves the API base path from the current browser protocol, host name, and port. The API service exposes RESTful behavior for MyEMS components and third-party applications.

The Admin application and API service are expected to operate together through a same-origin `/api/` path. A deployment may use a reverse proxy such as Nginx to route `/api/` traffic and avoid browser cross-origin restrictions, but this SRS does not require Nginx as the only valid mechanism.

### 2.2 Product Functions

The system shall provide the following high-level functions:

- RESTful API access for MyEMS components and third-party applications.
- Admin navigation to user settings through `/user`.
- Admin navigation to contact settings through `/contact`.
- Lazy loading of route-specific Admin modules.
- API base-path calculation from the current browser origin.
- Development execution paths for Linux and Windows environments.
- Docker-based installation support for the API service.

### 2.3 User Classes

- Administrators use the Admin application to navigate settings workflows.
- MyEMS components use the API service to exchange operational data with the system.
- Third-party applications use the API service for integration.
- Developers and deployers configure, run, and install the API service.
- Testers verify route behavior, API path resolution, and deployment readiness.

### 2.4 Operating Environment

The Admin application shall operate in a browser environment capable of running the client-side routing configuration and lazy-loaded modules.

The API service shall operate in a Python environment with the required Python packages installed. Development quick-run guidance shall support Linux and Windows execution. Docker-based installation shall be available for deployment preparation or reproducible setup.

Where API features rely on persistent data, the deployment shall provide a compatible database configuration for the API runtime dependencies.

### 2.5 Design and Implementation Constraints

- The Admin application shall calculate API access under the `/api/` path of the current browser origin.
- Route-specific Admin modules shall be lazy-loaded according to the routing configuration.
- The API runtime shall include its declared Python dependency set.
- Deployments that use MySQL-backed API features shall provide a MySQL-compatible database configuration.
- A reverse proxy may be used to route `/api/` requests and avoid browser cross-origin restrictions.

### 2.6 Assumptions and Dependencies

- The detailed REST endpoint inventory and payload schemas are outside the checked scope of this SRS.
- The detailed production hardening requirements for the API service are outside the checked scope of this SRS.
- The Admin route titles may be represented by localization keys.
- The runtime environment is responsible for providing required Python packages, network configuration, and any required database connectivity.

## 3. External Interface Requirements

### 3.1 User Interface Requirements

#### UI-001 User Settings Route

The Admin application shall provide a `/user` route for the user settings view. The route title shall use the localization key `MENU.USERSETTING.USER`.

#### UI-002 Contact Settings Route

The Admin application shall provide a `/contact` route for the contact settings view. The route title shall use the localization key `MENU.SETTINGS.CONTACT`.

#### UI-003 Lazy-Loaded Route Modules

The Admin application shall load the client modules required by each configured route before the corresponding view is used.

### 3.2 Software Interface Requirements

#### SI-001 RESTful API Service

The API service shall provide RESTful interfaces for MyEMS components and third-party applications.

#### SI-002 Admin-to-API Base Path

The Admin application shall construct the API base path as:

```text
{current_browser_protocol}//{current_browser_hostname}:{current_browser_port}/api/
```

#### SI-003 Same-Origin API Access

The Admin application shall access API endpoints through the same browser origin and the `/api/` path unless a deployment intentionally provides an equivalent routing arrangement.

### 3.3 Communication Interface Requirements

#### CI-001 Browser-to-API Communication

The Admin application shall communicate with the API service over HTTP or HTTPS according to the current browser protocol.

#### CI-002 Reverse Proxy Compatibility

The system shall support deployment behind a reverse proxy that forwards `/api/` requests to the API service.

### 3.4 Data Interface Requirements

#### DI-001 API Payload Format

The API service shall exchange data through RESTful request and response payloads. Detailed endpoint-specific schemas are not specified in this checked SRS.

#### DI-002 Database Connectivity

When API functionality requires persistent storage, the deployment shall provide database connectivity compatible with the API runtime dependency set.

## 4. Functional Requirements

### FR-001 Provide RESTful API Service

The system shall provide a RESTful API service for MyEMS components and third-party applications.

**Priority:** High

**Acceptance Criteria:**

- The API service can be started in a configured runtime environment.
- External MyEMS components and third-party applications can be directed to the API service endpoint.
- The API service is documented as RESTful from an integration perspective.

### FR-002 Provide User Settings Route

The Admin application shall provide a `/user` route for user settings.

**Priority:** High

**Acceptance Criteria:**

- Navigating to `/user` resolves to the user settings route.
- The route title is represented by `MENU.USERSETTING.USER`.
- The route is available through the Admin routing configuration.

### FR-003 Load User Settings Modules

The Admin application shall lazy-load the modules needed by the `/user` route, including user-related services, controllers, login-related services or controllers, and required UI libraries.

**Priority:** High

**Acceptance Criteria:**

- The `/user` route declares user-related module dependencies.
- The declared modules are loaded before the user settings view is used.
- Failure to load a required module prevents the route from being considered ready.

### FR-004 Provide Contact Settings Route

The Admin application shall provide a `/contact` route for contact settings.

**Priority:** High

**Acceptance Criteria:**

- Navigating to `/contact` resolves to the contact settings route.
- The route title is represented by `MENU.SETTINGS.CONTACT`.
- The route is available through the Admin routing configuration.

### FR-005 Load Contact Settings Modules

The Admin application shall lazy-load the contact settings modules required by the `/contact` route.

**Priority:** High

**Acceptance Criteria:**

- The `/contact` route declares contact-related module dependencies.
- The declared modules are loaded before the contact settings view is used.
- Contact settings behavior is not claimed to include tariff or category workflows unless those modules are configured for the same route.

### FR-006 Provide Settings Module Coverage for Tariff and Category Workflows

The Admin application shall include settings workflow modules for tariff and category functionality where those modules are configured in the Admin settings routes.

**Priority:** Medium

**Acceptance Criteria:**

- Tariff-related settings modules are represented in the Admin routing configuration where applicable.
- Category-related settings modules are represented in the Admin routing configuration where applicable.
- Tariff and category modules are treated as separate settings workflow coverage unless route configuration combines them.

### FR-007 Resolve API Base Path from Browser Origin

The Admin application shall compute the API base path from the current browser protocol, host name, and port, then append `/api/`.

**Priority:** High

**Acceptance Criteria:**

- The computed API base path uses the current browser protocol.
- The computed API base path uses the current browser host name.
- The computed API base path uses the current browser port.
- The computed API base path ends with `/api/`.

### FR-008 Support Development Quick-Run Modes

The API service shall provide documented quick-run execution paths for Linux and Windows development environments.

**Priority:** Medium

**Acceptance Criteria:**

- A Linux development quick-run command path is available.
- A Windows development quick-run command path is available.
- Quick-run behavior is not treated as a complete production deployment requirement.

### FR-009 Support Docker-Based Installation

The API service shall support Docker-based installation or setup.

**Priority:** Medium

**Acceptance Criteria:**

- Docker-based setup instructions are available.
- Docker-based setup can prepare the API runtime environment.
- Docker-based setup is compatible with the required API dependency set.

## 5. Non-Functional Requirements

### NFR-001 Same-Origin Compatibility

The Admin application shall support same-origin API access through the `/api/` path to reduce browser cross-origin configuration needs.

**Metric:** API calls made by the Admin application use the current browser origin and the `/api/` path unless an equivalent routing configuration is intentionally provided.

### NFR-002 Modularity

The Admin application shall keep route-specific functionality modular by lazy-loading the modules needed for each route.

**Metric:** The user and contact settings routes declare route-specific module dependency lists.

### NFR-003 Deployability

The API service shall provide setup paths for development quick-run execution and Docker-based installation.

**Metric:** Setup documentation includes Linux quick-run, Windows quick-run, and Docker-based installation paths.

### NFR-004 Integration Readiness

The API service shall be suitable for integration by MyEMS components and third-party applications through RESTful interfaces.

**Metric:** Integration clients can be configured with the API endpoint base path.

### NFR-005 Runtime Dependency Availability

The API service runtime shall provide the declared Python dependencies before service startup.

**Metric:** Startup validation or setup procedures confirm that required Python packages are installed.

## 6. Data Requirements

### DR-001 User Settings Module Data

The Admin application shall maintain route configuration data that identifies the user settings path, title key, and required user-related modules.

### DR-002 Contact Settings Module Data

The Admin application shall maintain route configuration data that identifies the contact settings path, title key, and required contact-related modules.

### DR-003 Tariff Settings Module Data

The Admin application shall maintain route configuration data for tariff-related settings modules where those modules are configured.

### DR-004 Category Settings Module Data

The Admin application shall maintain route configuration data for category-related settings modules where those modules are configured.

### DR-005 API Base Path Data

The Admin application shall maintain a runtime API base-path value derived from the current browser origin and the `/api/` path.

### DR-006 Runtime Configuration Data

The API service shall use runtime configuration data for package dependencies, network access, and database connectivity where required by deployed API behavior.

## 7. System Constraints

### CON-001 Python Runtime Dependencies

The API service runtime shall include required Python packages, including REST framework support, CORS support, WSGI execution support, spreadsheet and image handling dependencies, and MySQL connector support.

### CON-002 API Path Convention

The Admin application shall use `/api/` as the API path suffix when computing the API base path.

### CON-003 Reverse Proxy Deployment Option

Deployments may use a reverse proxy such as Nginx to forward `/api/` traffic to the API service. The architecture shall not assume that Nginx is the only valid same-origin routing mechanism.

### CON-004 Lazy-Loading Route Mechanism

The Admin application shall use the configured lazy-loading mechanism for route-specific client modules.

### CON-005 Database Configuration

Deployments that enable MySQL-backed API behavior shall provide compatible database connection configuration for the API service.

## 8. Verification and Acceptance Criteria

| Requirement | Verification Method | Expected Result |
| --- | --- | --- |
| FR-001 | Inspect API startup and integration configuration | RESTful API service is available for configured clients |
| FR-002 | Inspect Admin route behavior | `/user` resolves to the user settings route |
| FR-003 | Inspect route module loading | User settings modules are declared and loaded |
| FR-004 | Inspect Admin route behavior | `/contact` resolves to the contact settings route |
| FR-005 | Inspect route module loading | Contact settings modules are declared and loaded |
| FR-006 | Inspect settings route configuration | Tariff and category modules are covered where configured |
| FR-007 | Unit or runtime test of base-path computation | API base path matches the browser origin plus `/api/` |
| FR-008 | Execute documented development commands | Linux and Windows quick-run paths can start the service in development mode |
| FR-009 | Execute Docker-based setup | Docker-based setup prepares the API runtime |
| NFR-001 | Inspect runtime API requests | Admin API calls use same-origin `/api/` routing or an equivalent configured path |
| NFR-002 | Inspect route definitions | Route-specific dependencies are separated by route |
| NFR-003 | Inspect setup documentation and execution paths | Development and Docker setup paths are present |
| NFR-004 | Integration configuration test | External clients can be configured for API access |
| NFR-005 | Dependency setup check | Required Python packages are installed before service startup |
