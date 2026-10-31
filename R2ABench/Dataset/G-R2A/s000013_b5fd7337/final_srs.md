# Software Requirements Specification

## 1. Introduction

### Purpose
This SRS defines evidence-backed software requirements for the `ta_lyrics_sentiment_classification` repository at commit `53071f940166ffe52565206c25a6769a35b02e0f`. The document covers the observable system behavior and supported deployment/data scope shown in the repository evidence.

### Product Scope
The product is a containerized web application for song mood classification and retrieval. It uses a React frontend, a FastAPI backend, Elasticsearch for song and mood storage, Kibana as a supporting UI for stored data, and the Genius API to search for songs not already present in the database. The project scope is limited to English songs in its explored dataset. [E003][E005][E006]

### Intended Audience
This document is intended for:
- Project maintainers and developers
- Testers and reviewers
- Users operating the web application
- Deployers of the containerized system

### References
- Repository: `Simon-0711/ta_lyrics_sentiment_classification`
- Commit: `53071f940166ffe52565206c25a6769a35b02e0f`
- Evidence sources:
  - `README.md` [E001][E003][E004]
  - `frontend/mood_classification/README.md` [E002]
  - `data_exploration/readme.md` [E005][E006]

## 2. Overall Description

### Product Perspective
The system is a multi-tier application in which each tier is hosted in a Docker container. The frontend is implemented with React, the backend with FastAPI, persistent song/mood storage uses Elasticsearch, and Kibana is used as a better UI for stored data inspection. The backend also depends on the Genius API to search for songs that are not yet in Elasticsearch. [E003]

### Product Functions Summary
- Provide a browser-accessible frontend for interacting with the application. [E002][E003]
- Accept song lookup/classification requests. [E003]
- Retrieve a previously stored song mood from Elasticsearch when the song is already present. [E003]
- Search for songs through the Genius API when the song is not already stored. [E003]
- Store songs together with their classified moods in Elasticsearch to support later retrieval. [E003]
- Operate on English songs within the project data scope. [E005]

### User Classes
- End users: submit song-related requests through the web frontend and receive mood results. [E002][E003]
- Developers/operators: build, run, update containerized components, and inspect stored data using Kibana. [E001][E003][E004]

### Operating Environment
- Web browser for frontend access. [E002]
- Docker-based container environment, with each tier hosted in a container. [E003]
- Backend runtime supporting FastAPI. [E003]
- Elasticsearch and Kibana services. [E003]

### Assumptions and Dependencies
- The system depends on the Genius API for songs not already present in Elasticsearch. [E003]
- The system depends on Elasticsearch for stored song and mood retrieval. [E003]
- Project data scope is limited to English songs. [E005]
- Windows environments may experience slow startup depending on repository location, per project troubleshooting guidance. [E001]

## 3. External Interface Requirements

### User Interfaces
- The system shall provide a browser-accessible web frontend. [E002][E003]
- Kibana shall be available as a UI for interacting with stored Elasticsearch data. [E003]

### Software/API Interfaces
- The frontend shall interact with a FastAPI backend. [E003]
- The backend shall interface with Elasticsearch for song and mood storage/retrieval. [E003]
- The backend shall interface with the Genius API to search for songs not already stored. [E003]

### Communication Interfaces
- Browser-to-frontend communication shall occur through standard web access in a browser. [E002]
- Service-to-service API communication between backend, Elasticsearch, and Genius API is required by the architecture. This protocol detail is inferred from the identified components and APIs. [E003]

### Data Exchange Formats
Supported data objects evidenced in the repository include:
- Song name [E006]
- Song link representation (`SLink`) [E006]
- Lyrics (`Lyric`) [E006]
- Language [E006]
- Artist name [E006]
- Artist genres [E006]
- Artist song count [E006]
- Song mood classification result [E003]

## 4. Functional Requirements

| ID | Description | Trigger / Input | System Behavior | Output | Priority | Verification | Source Evidence |
|---|---|---|---|---|---|---|---|
| FR-001 | Browser-based access | A user opens the application in a browser | The system shall make the frontend available for use in a web browser | Rendered frontend page | High | Demonstration | E002, E003 |
| FR-002 | Song mood retrieval from storage | A user requests a song that is already present in the database | The system shall retrieve the stored mood for the song from Elasticsearch | Returned mood result for the requested song | High | Test | E003 |
| FR-003 | Song search fallback | A user requests a song that is not present in the database | The system shall search for the song using the Genius API | Search result used for downstream processing | High | Test | E003 |
| FR-004 | Persist classified songs | A song has undergone initial classification | The system shall store the song together with its mood in Elasticsearch | Persisted song-and-mood record | High | Test | E003 |
| FR-005 | Reuse stored classifications | A user later requests a song that has already been classified and stored | The system shall use the stored Elasticsearch record instead of requiring a new initial classification step | Retrieved mood result from stored data | Medium | Test | E003 |
| FR-006 | English-song scope enforcement | Song data is prepared or selected for project use | The system shall operate within the project’s English-song scope | Accepted/processed data limited to English songs | Medium | Inspection | E005 |

## 5. Non-Functional Requirements

| ID | Quality Attribute | Requirement | Priority | Verification | Source Evidence | Evidence Type |
|---|---|---|---|---|---|---|
| NFR-001 | Deployability / Portability | The system shall be deployable as a multi-tier Dockerized application with each tier hosted in its own container. | High | Inspection | E003 | explicit |
| NFR-002 | Retrieval efficiency | After a song has been initially classified and stored, the system shall support later mood retrieval from Elasticsearch rather than repeating initial classification for that stored song. | Medium | Test | E003 | explicit |
| NFR-003 | Browser compatibility | The frontend shall be usable through a web browser in development operation. | Medium | Demonstration | E002 | explicit |

## 6. Data Requirements

| ID | Data Requirement | Type | Requirement | Verification | Source Evidence |
|---|---|---|---|---|---|
| DR-001 | Song record | Data entity | The system shall handle song records containing at least song name, `SLink`, lyrics, and language. | Inspection | E006 |
| DR-002 | Artist record | Data entity | The system shall handle artist-related data containing at least artist name, genres, and song count where such metadata is used from the project dataset. | Inspection | E006 |
| DR-003 | Mood association | Data entity | The system shall store songs together with their corresponding mood classification in Elasticsearch. | Test | E003 |
| DR-004 | Language scope | Data constraint | The project data scope shall be limited to English songs. | Inspection | E005 |

## 7. Constraints

| ID | Constraint | Verification | Source Evidence |
|---|---|---|---|
| C-001 | The frontend technology is React. | Inspection | E003 |
| C-002 | The backend technology is FastAPI. | Inspection | E003 |
| C-003 | Elasticsearch is the storage solution and Kibana is used as a supporting UI. | Inspection | E003 |
| C-004 | The backend depends on the Genius API for songs not already included in Elasticsearch. | Inspection | E003 |
| C-005 | The deployed architecture hosts each tier in a Docker container. | Inspection | E003 |
| C-006 | The project scope is limited to English songs. | Inspection | E005 |

## 8. Verification and Acceptance

| Requirement ID | Verification Method | Acceptance Criterion |
|---|---|---|
| FR-001 | Demonstration | Opening the application in a browser displays the frontend. |
| FR-002 | Test | For a song known to exist in Elasticsearch, the system returns the stored mood. |
| FR-003 | Test | For a song not present in Elasticsearch, the system invokes Genius-based search behavior and produces a search result for further handling. |
| FR-004 | Test | After initial classification, the song and mood are present in Elasticsearch. |
| FR-005 | Test | A repeated request for a previously stored song returns the stored mood from Elasticsearch. |
| FR-006 | Inspection | Project data handling documentation or configuration shows operation limited to English songs. |
| NFR-001 | Inspection | Deployment artifacts and architecture show a separate Docker container per tier. |
| NFR-002 | Test | Stored songs are retrieved from Elasticsearch on later requests without requiring reclassification. |
| NFR-003 | Demonstration | The frontend can be opened and used in a browser during development operation. |
| DR-001 | Inspection | Data definitions or sample records show song name, `SLink`, lyrics, and language fields. |
| DR-002 | Inspection | Data definitions or sample records show artist name, genres, and song count fields. |
| DR-003 | Test | Stored Elasticsearch records include both song identity and mood value. |
| DR-004 | Inspection | Project data exploration/documentation shows English-only scope. |
| C-001 | Inspection | Repository evidence identifies React as the frontend framework. |
| C-002 | Inspection | Repository evidence identifies FastAPI as the backend framework. |
| C-003 | Inspection | Repository evidence identifies Elasticsearch and Kibana in the architecture. |
| C-004 | Inspection | Repository evidence identifies Genius API as a backend dependency. |
| C-005 | Inspection | Repository evidence states each tier is hosted in a Docker container. |
| C-006 | Inspection | Repository evidence states the project is limited to English songs. |

## 9. Traceability Matrix

| ID | Requirement | Type | Source | Evidence Type | Verification | Confidence |
|---|---|---|---|---|---|---|
| FR-001 | Provide browser-based frontend access | Functional | E002, E003 | explicit | Demonstration | High |
| FR-002 | Retrieve stored mood from Elasticsearch for known songs | Functional | E003 | explicit | Test | High |
| FR-003 | Search missing songs via Genius API | Functional | E003 | explicit | Test | High |
| FR-004 | Store songs with classified moods in Elasticsearch | Functional | E003 | explicit | Test | High |
| FR-005 | Reuse stored classification on later requests | Functional | E003 | explicit | Test | Medium |
| FR-006 | Operate within English-song scope | Functional | E005 | explicit | Inspection | Medium |
| NFR-001 | Deploy as multi-tier Dockerized system | Non-functional | E003 | explicit | Inspection | High |
| NFR-002 | Support later retrieval from storage rather than reclassification | Non-functional | E003 | explicit | Test | Medium |
| NFR-003 | Support browser-based frontend use | Non-functional | E002 | explicit | Demonstration | High |
| DR-001 | Handle song records with name, `SLink`, lyrics, language | Data | E006 | explicit | Inspection | High |
| DR-002 | Handle artist records with artist, genres, song count | Data | E006 | explicit | Inspection | Medium |
| DR-003 | Store song-to-mood association | Data | E003 | explicit | Test | High |
| DR-004 | Limit project data scope to English songs | Data | E005 | explicit | Inspection | High |
| C-001 | Use React frontend | Constraint | E003 | explicit | Inspection | High |
| C-002 | Use FastAPI backend | Constraint | E003 | explicit | Inspection | High |
| C-003 | Use Elasticsearch with Kibana | Constraint | E003 | explicit | Inspection | High |
| C-004 | Depend on Genius API for missing songs | Constraint | E003 | explicit | Inspection | High |
| C-005 | Host each tier in a Docker container | Constraint | E003 | explicit | Inspection | High |
| C-006 | Restrict scope to English songs | Constraint | E005 | explicit | Inspection | High |
