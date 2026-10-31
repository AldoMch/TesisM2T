# Software Requirements Specification

## 1. Introduction

### 1.1 Purpose
This SRS defines the final checked requirements for a containerized song mood storage, retrieval, and search web application. It is prepared as a clean requirements input for downstream architecture diagram generation.

### 1.2 Product Scope
The system is a multi-tier web application that allows users to request song mood information. It provides:
- A browser-accessible React frontend.
- A FastAPI backend for song lookup and storage workflows.
- Elasticsearch storage for song records and associated mood values.
- Kibana as an auxiliary UI for inspecting stored Elasticsearch data.
- Genius API integration for searching songs that are not already stored.
- Dockerized deployment with separate container services for frontend, backend, Elasticsearch, and Kibana.

The system stores and retrieves song-mood associations for songs whose mood is already available. A runtime mood classification or model-inference component is not specified as an in-scope requirement unless added separately.

The project dataset scope is English songs. This is a dataset and project-scope constraint, not a runtime language-rejection requirement.

### 1.3 Intended Audience
- End users requesting song mood information through the web application.
- Developers maintaining the React frontend and FastAPI backend.
- Operators deploying and updating the containerized services.
- Testers validating lookup, storage, and external API behavior.
- Architecture reviewers generating or validating architecture diagrams.

### 1.4 Terminology
| Term | Definition |
|---|---|
| Song record | A stored song data item containing song identity and lyric metadata. |
| Mood association | A stored relationship between a song and an already available mood value. |
| Known song | A song that already has a stored record in Elasticsearch. |
| Missing song | A requested song that is not found in Elasticsearch and must be searched through the Genius API. |
| Auxiliary data UI | Kibana, used for inspecting data stored in Elasticsearch. |

## 2. Overall Description

### 2.1 Product Perspective
The system is a Dockerized multi-tier application. The React frontend provides browser access for users. The FastAPI backend handles song lookup requests, interacts with Elasticsearch for stored song and mood data, and calls the Genius API when a requested song is not present in storage. Elasticsearch stores song records and mood associations. Kibana provides a supporting UI for inspecting stored data.

The deployment architecture shall include four named container services: frontend, backend, Elasticsearch, and Kibana. The Genius API is an external dependency and shall not be modeled as an internal container service.

### 2.2 Product Functions
- Render a browser-accessible web frontend.
- Accept song lookup requests from users.
- Retrieve stored mood values for known songs from Elasticsearch.
- Search for missing songs through the Genius API.
- Store already available song-mood associations in Elasticsearch.
- Retrieve stored mood associations quickly for later requests.
- Provide Kibana access for stored data inspection.
- Deploy each named tier as a separate Docker container service.

### 2.3 User Classes
| User Class | Description |
|---|---|
| End user | Uses the web frontend to request mood information for songs. |
| Developer | Builds and maintains frontend, backend, and container configuration. |
| Operator | Runs, updates, and inspects the containerized application stack. |
| Data inspector | Uses Kibana to inspect song and mood data in Elasticsearch. |

### 2.4 Operating Environment
- Web browser for frontend access.
- Docker-based runtime for the application stack.
- React frontend container.
- FastAPI backend container.
- Elasticsearch container.
- Kibana container.
- External network access from the backend to the Genius API.

### 2.5 Assumptions and Dependencies
- Elasticsearch is required for stored song and mood retrieval.
- The Genius API is required for searching songs that are not stored.
- Kibana depends on Elasticsearch availability.
- The backend depends on Elasticsearch availability for known-song lookup.
- The backend depends on Genius API availability for missing-song search.
- English-only scope applies to the project dataset used by the application and analysis.

## 3. External Interface Requirements

### 3.1 User Interfaces
| ID | Interface | Requirement |
|---|---|---|
| UI-001 | Web frontend | The system shall provide a browser-accessible frontend for song mood lookup interaction. |
| UI-002 | Kibana data UI | The system shall provide Kibana as an auxiliary UI for inspecting stored Elasticsearch data. |

### 3.2 Software and API Interfaces
| ID | Interface | Requirement |
|---|---|---|
| API-001 | Frontend-to-backend interface | The React frontend shall communicate with the FastAPI backend for song lookup requests. |
| API-002 | Backend-to-storage interface | The FastAPI backend shall query and write Elasticsearch song and mood data. |
| API-003 | Backend-to-Genius interface | The FastAPI backend shall call the Genius API to search for songs not found in Elasticsearch. |
| API-004 | Kibana-to-storage interface | Kibana shall connect to Elasticsearch for stored data inspection. |

### 3.3 Communication Interfaces
| ID | Interface | Requirement |
|---|---|---|
| COM-001 | Browser access | Users shall access the frontend through standard browser web access. |
| COM-002 | Internal service communication | Frontend, backend, Elasticsearch, and Kibana shall communicate across the Dockerized application network according to their configured endpoints. |
| COM-003 | External API communication | The backend shall communicate with the Genius API as an external service. |

### 3.4 Data Exchange Formats
| ID | Data Format | Required Content |
|---|---|---|
| DEF-001 | Song record | Song name, `SLink`, lyrics, and language. |
| DEF-002 | Artist metadata | Artist name, genres, and song count when artist metadata is used. |
| DEF-003 | Mood association | Song identity plus associated mood value. |
| DEF-004 | Song search result | Song information returned from Genius API search for a missing song. |

## 4. Functional Requirements

| ID | Requirement | Trigger/Input | System Behavior | Output | Priority | Verification |
|---|---|---|---|---|---|---|
| FR-001 | The system shall provide browser-based frontend access. | User opens the application in a browser. | The React frontend is rendered and available for song lookup interaction. | Rendered frontend page. | High | Demonstration |
| FR-002 | The system shall retrieve stored mood values for known songs. | User requests a song that exists in Elasticsearch. | The backend queries Elasticsearch and retrieves the stored mood association for the requested song. | Mood value for the requested song. | High | Test |
| FR-003 | The system shall search for missing songs through the Genius API. | User requests a song that is not found in Elasticsearch. | The backend invokes Genius API search for the requested song. | Genius search result or an error indicating search failure. | High | Test |
| FR-004 | The system shall store already available song-mood associations. | A song-mood association is available for storage. | The backend stores the song record together with the associated mood value in Elasticsearch. | Persisted song-mood record. | High | Test |
| FR-005 | The system shall support fast retrieval of stored mood associations. | User later requests a song with an existing stored mood association. | The backend retrieves the stored mood association from Elasticsearch. | Stored mood value returned from Elasticsearch. | Medium | Test |
| FR-006 | The system shall provide data inspection through Kibana. | Operator or data inspector opens Kibana. | Kibana displays stored Elasticsearch data for inspection. | Data inspection UI. | Medium | Demonstration |

## 5. Non-Functional Requirements

| ID | Requirement | Quality Attribute | Priority | Verification |
|---|---|---|---|---|
| NFR-001 | The system shall be deployable as a multi-tier Dockerized application with separate container services for frontend, backend, Elasticsearch, and Kibana. | Deployability / portability | High | Inspection |
| NFR-002 | Stored song-mood associations shall be retrievable from Elasticsearch for later requests. | Retrieval efficiency | Medium | Test |
| NFR-003 | The frontend shall be accessible through a web browser during development and operation. | Browser compatibility | Medium | Demonstration |
| NFR-004 | The backend shall use Elasticsearch as the authoritative store for persisted song-mood associations. | Data consistency | High | Inspection |

## 6. Data Requirements

| ID | Data Item | Requirement |
|---|---|---|
| DR-001 | Song record | The system shall handle song records containing at least song name, `SLink`, lyrics, and language. |
| DR-002 | Artist metadata | The system shall handle artist metadata containing at least artist name, genres, and song count when this metadata is used. |
| DR-003 | Mood association | The system shall store song identity together with its associated mood value in Elasticsearch. |
| DR-004 | Dataset language scope | The project dataset scope shall be limited to English songs; runtime rejection of non-English user input is not specified. |
| DR-005 | Search result data | Genius API search results shall provide enough song information for the backend to continue the configured lookup workflow. |

## 7. System Constraints

| ID | Constraint |
|---|---|
| C-001 | Frontend technology shall be React. |
| C-002 | Backend technology shall be FastAPI. |
| C-003 | Persistent song and mood storage shall use Elasticsearch. |
| C-004 | Kibana shall be used as the auxiliary UI for Elasticsearch data inspection. |
| C-005 | The backend shall depend on the Genius API for songs not found in Elasticsearch. |
| C-006 | The deployment shall include separate Docker container services for frontend, backend, Elasticsearch, and Kibana. |
| C-007 | The Genius API shall be modeled as an external dependency rather than an internal container service. |
| C-008 | The project dataset scope shall be English songs. |
| C-009 | A runtime classifier, model server, or inference algorithm shall not be assumed unless specified by a separate requirement. |

## 8. Verification and Acceptance Criteria

| Requirement IDs | Verification Method | Acceptance Criteria |
|---|---|---|
| FR-001, NFR-003, UI-001 | Demonstration | Opening the application in a browser displays the React frontend. |
| FR-002, FR-005, NFR-002, DR-003, NFR-004 | Test | For a known song stored in Elasticsearch, the backend returns the associated mood value from Elasticsearch. |
| FR-003, DR-005, C-005, C-007 | Test | For a missing song, the backend invokes Genius API search and returns a search result or a defined search failure response. |
| FR-004, DR-001, DR-003 | Test | A song record and its associated mood value can be persisted in Elasticsearch. |
| FR-006, UI-002, C-004 | Demonstration | Kibana connects to Elasticsearch and displays stored song or mood data for inspection. |
| NFR-001, C-001, C-002, C-003, C-006 | Inspection | Deployment configuration defines separate container services for React frontend, FastAPI backend, Elasticsearch, and Kibana. |
| DR-001, DR-002 | Inspection | Data definitions or sample records include the required song and artist metadata fields. |
| DR-004, C-008 | Inspection | Project dataset documentation or configuration limits the dataset scope to English songs without requiring runtime language rejection. |
| C-009 | Inspection | Architecture and implementation review do not assume a classifier, model server, or inference module unless such a requirement is explicitly added. |
