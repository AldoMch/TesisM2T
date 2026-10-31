# Software Requirements Specification

## 1. Introduction

### 1.1 Purpose
This SRS defines checked requirements for the QAPM Android component in `qunarcorp/m_adr_qapm_open_source`. It is intended to provide a clean requirements input for downstream architecture diagram generation, implementation review, and verification planning.

### 1.2 Product Scope
QAPM is an Android application performance monitoring SDK. Its broader product context includes performance data collection and reporting for concerns such as network behavior, frame rate, memory, CPU, and battery usage.

This SRS covers only the reviewed subset of behavior:
- Background handler threads and work scheduling.
- Upload scheduling and local upload-file processing.
- Data sending using file-content and context-derived parameters.
- Apache `HttpClient` response-handler and entity instrumentation wrappers.

This SRS does not fully specify the complete QAPM collection, storage, reporting, plugin-injection, metric schema, or remote reporting pipeline.

### 1.3 Intended Audience
- QAPM SDK maintainers.
- Android application integrators using QAPM scheduling, upload, or network instrumentation behavior.
- Test engineers verifying background scheduling, upload, and HTTP wrapper behavior.
- Architecture reviewers generating or checking architecture artifacts from requirements.

## 2. Overall Description

### 2.1 Product Perspective
The overall product is an Android APM SDK integrated into a host application. At the architecture-context level, the application imports the QAPM SDK, the SDK connects collection, storage, and reporting modules through internal APIs, and a QAPM plugin may participate in build-time or initialization behavior.

The scope of this document is narrower than the whole SDK. It specifies the behavior of background work dispatch, upload processing, and Apache `HttpClient` instrumentation that can be checked independently. It treats collection modules, storage internals, report endpoint protocols, and plugin transformation details as outside the present scope unless explicitly mentioned in these requirements.

### 2.2 Product Functions Summary
| Capability | Summary |
|---|---|
| Background handler support | Maintain a default background handler thread and a main-thread handler for component dispatch. |
| Work handler initialization | Initialize upload/work scheduling with a `HandlerThread` looper and a handler bound to that looper. |
| Asynchronous work scheduling | Post runnable tasks and upload requests to the work handler instead of running them inline on the caller thread. |
| Network-gated upload processing | Check network connectivity before processing upload files. |
| Forced-send storage handling | Pop locally stored pending data before upload-directory scanning when forced sending is requested. |
| Upload-file processing | Enumerate upload files, read file content as `bParam`, derive `cParam` from Android context, and submit both parameters to the configured sender. |
| Upload success/failure handling | Delete the corresponding upload file after successful send and log send failure when sending fails. |
| Apache response-handler instrumentation | Inspect and instrument a transaction state during response handling, then delegate to the wrapped `ResponseHandler`. |
| Apache response-entity instrumentation | Wrap non-null HTTP entities, expose `getContent()` through a cached counting input stream, and delegate `writeTo(OutputStream)` to the wrapped entity. |

### 2.3 User Classes
| User Class | Responsibilities / Needs |
|---|---|
| Android application integrator | Integrates QAPM SDK behavior into an Android application and relies on background execution for upload work. |
| QAPM maintainer | Maintains scheduling, upload, and network instrumentation components. |
| Network instrumentation integrator | Uses Apache `HttpClient` wrappers for transaction-aware response handling and response entity access. |
| Test engineer | Verifies background dispatch, network-gated upload, file processing, sender callbacks, and HTTP wrapper behavior. |

### 2.4 Operating Environment
| Environment | Requirement |
|---|---|
| Android runtime | The component shall run in an Android environment providing `Handler`, `HandlerThread`, `Looper`, and `Context`. |
| Background scheduling runtime | Upload and runnable work shall use a work handler bound to a background `HandlerThread` looper after work-handler initialization. |
| Network state environment | Upload processing shall be able to query current network connectivity. |
| Local file environment | Upload processing shall be able to access an upload directory and upload files when present. |
| Apache HttpClient environment | HTTP instrumentation shall integrate with Apache `HttpClient` abstractions such as `ResponseHandler`, `HttpResponse`, and `HttpEntity`. |

### 2.5 Assumptions and Dependencies
| ID | Assumption / Dependency |
|---|---|
| AD-001 | Upload processing depends on network connectivity being available at execution time. |
| AD-002 | Upload processing depends on an upload directory and files being available when there is queued upload data. |
| AD-003 | Data sending depends on a configured sender available through QAPM configuration management. |
| AD-004 | The HTTP instrumentation wrapper depends on host application code using Apache `HttpClient` abstractions. |
| AD-005 | The full APM collection and reporting pipeline exists outside this checked SRS scope and should be specified separately if needed. |

## 3. External Interface Requirements

### 3.1 User Interfaces
No end-user graphical interface is specified for the reviewed component behavior.

### 3.2 Software and API Interfaces
| Interface | Requirement |
|---|---|
| Android scheduling APIs | The component shall use Android `Handler`, `HandlerThread`, and `Looper` APIs for asynchronous work dispatch. |
| Android context API | Upload processing shall use Android `Context` to obtain context-derived upload parameters and environment-dependent paths. |
| Upload sender interface | Upload processing shall submit file-content and context-derived parameters to the configured sender through the QAPM configuration manager. |
| Apache response handler interface | The instrumentation layer shall wrap Apache `ResponseHandler` instances while retaining transaction-state association. |
| Apache HTTP entity interface | The instrumentation layer shall wrap Apache `HttpEntity` instances while preserving compatible entity operations. |

### 3.3 Communication Interfaces
| Interface | Requirement |
|---|---|
| Network connectivity gate | Upload processing shall check network connectivity before scanning and processing upload files. |
| Sender callback communication | Upload processing shall respond to sender success and failure callbacks by deleting successfully sent files or logging failures. |
| HTTP response handling | Instrumented response handling shall inspect/instrument the transaction state for the response and then delegate response handling to the wrapped handler. |

### 3.4 Data Exchange Formats
| Data Item | Requirement |
|---|---|
| Upload file content | Upload file content shall be read as a string parameter named `bParam`. |
| Context-derived upload parameter | Android context shall be used to derive a string parameter named `cParam`. |
| Sender parameters | The sender shall receive the `bParam` and `cParam` parameter pair for each processed upload file. |
| HTTP response body input stream | `getContent()` on the wrapped entity shall return or reuse a counting input stream over the underlying HTTP entity content. |
| HTTP response body output stream | `writeTo(OutputStream)` on the wrapped entity shall delegate writing to the underlying entity. |
| Transaction state | Response-handler instrumentation shall maintain a transaction-state object associated with wrapped response processing. |

## 4. Functional Requirements

| ID | Requirement | Trigger / Input | System Behavior | Output | Priority | Verification |
|---|---|---|---|---|---|---|
| FR-001 | Initialize background work handling. | The work-handler manager is initialized. | The system shall create a background `HandlerThread`, start it, and create the work handler from that background looper. | A work handler bound to a background looper is available. | High | Inspection / Test |
| FR-002 | Schedule work asynchronously. | A caller submits a runnable or upload request after work-handler initialization. | The system shall post runnable or upload work to the background work handler rather than executing it inline on the caller thread. | Work is enqueued for background execution. | High | Inspection / Test |
| FR-003 | Gate upload processing by network connectivity. | A caller requests upload processing with Android `Context` and an upload mode flag. | The system shall check network connectivity before processing upload work and shall stop before file processing when no network connection is available. | No upload-file processing occurs while disconnected. | High | Test |
| FR-004 | Pop stored data for forced send. | A caller requests upload processing with forced sending enabled. | The system shall invoke storage pop behavior before scanning the upload directory. | Pending stored data is popped before file-based upload processing continues. | Medium | Inspection / Test |
| FR-005 | Discover and read upload files. | Upload processing starts while network connectivity is available. | The system shall obtain the upload directory, enumerate matching upload files, and read each file's content as `bParam`. | Per-file content strings are available for sender submission. | High | Inspection / Test |
| FR-006 | Derive and send upload parameters. | Upload processing handles an upload file. | The system shall derive `cParam` from Android context and submit the `bParam`/`cParam` pair to the configured sender. | The file-content and context-derived parameter pair is submitted to the sender. | High | Test / Inspection |
| FR-007 | Handle upload sender callbacks. | The configured sender reports success or failure for a submitted upload file. | The system shall delete the corresponding upload file after successful sending and shall log failures when sending fails. | Successful upload files are removed; send failures are recorded. | Medium | Test / Inspection |
| FR-008 | Perform transaction-aware response handling. | A wrapped Apache `ResponseHandler` handles an `HttpResponse` with an associated transaction state. | The system shall inspect and instrument the transaction state for the response and then delegate response handling to the wrapped handler. | Response handling result from the wrapped handler with transaction-state instrumentation applied. | Medium | Inspection / Test |
| FR-009 | Wrap HTTP entities for content buffering. | A caller constructs a content-buffering response entity with a non-null wrapped `HttpEntity`. | The system shall wrap the provided entity; `getContent()` shall return or reuse a counting input stream over the underlying entity content; `writeTo(OutputStream)` shall delegate to the wrapped entity. | A wrapped entity provides counted input-stream access and delegated output writing. | Medium | Inspection / Test |
| FR-010 | Provide default QAPM handlers. | The QAPM handler-thread component is initialized or accessed. | The system shall maintain a default background handler thread and a main-thread handler for dispatching component work. | Default background and main-thread handlers are available. | Medium | Inspection |

## 5. Non-Functional Requirements

| ID | Quality Attribute | Requirement | Priority | Verification |
|---|---|---|---|---|
| NFR-001 | Performance | Upload-related work shall be posted to a background `HandlerThread` handler for asynchronous execution to reduce main-thread blocking or ANR risk. | High | Inspection / Test |
| NFR-002 | Reliability | The system shall skip upload-file processing when network connectivity is unavailable. | High | Test |
| NFR-003 | Reliability | Construction of the content-buffering response entity shall reject a missing wrapped entity by throwing `IllegalArgumentException`. | Medium | Test |
| NFR-004 | Compatibility | The component shall operate in Android environments providing `Handler`, `HandlerThread`, `Looper`, and `Context`, and in applications using Apache `HttpClient` interfaces where the wrappers are applied. | High | Inspection |
| NFR-005 | Maintainability | Upload sender behavior shall separate parameter preparation, sender invocation, success cleanup, and failure logging into verifiable steps. | Medium | Inspection |

## 6. Data Requirements

| ID | Data Entity / Object | Requirement |
|---|---|---|
| DR-001 | Work handler | The component shall maintain a handler bound to a background `HandlerThread` looper for asynchronous work execution. |
| DR-002 | Main-thread handler | The component shall maintain a handler associated with the Android main looper where main-thread dispatch is needed. |
| DR-003 | Upload directory path | Upload processing shall obtain an upload directory path before file enumeration. |
| DR-004 | Upload filename | Upload processing shall enumerate matching upload filenames from the upload directory. |
| DR-005 | File-content parameter | Upload processing shall read each upload file into a string parameter named `bParam`. |
| DR-006 | Context-derived parameter | Upload processing shall derive a string parameter named `cParam` from Android context. |
| DR-007 | Sender parameter pair | Upload processing shall submit `bParam` and `cParam` together to the configured data sender. |
| DR-008 | Upload file lifecycle state | Upload processing shall delete a file after successful sender completion and log failure when sending fails. |
| DR-009 | Transaction state | The HTTP instrumentation layer shall maintain a transaction-state object associated with wrapped response handling. |
| DR-010 | Counting input stream | The wrapped response entity shall maintain or reuse a counting input stream for the `getContent()` input-stream read path. |
| DR-011 | Wrapped HTTP entity | The response-entity wrapper shall retain the underlying `HttpEntity` and delegate compatible entity operations to it where applicable. |

### 6.1 Storage, Privacy, Retention, and Migration
| Topic | Requirement |
|---|---|
| Local upload storage | Upload files remain in local upload storage until sender success permits deletion. |
| Remote payload schema | The remote reporting payload schema is not specified in this SRS. |
| Privacy and retention | Privacy controls, retention periods, and migration behavior are not specified in the reviewed component scope and should be defined separately before production use if required. |

## 7. Constraints

| ID | Constraint |
|---|---|
| C-001 | The component is constrained to Android platform services and APIs including `Handler`, `HandlerThread`, `Looper`, and `Context`. |
| C-002 | HTTP instrumentation is constrained to Apache `HttpClient` abstractions such as `ResponseHandler`, `HttpResponse`, and `HttpEntity`. |
| C-003 | Upload processing is operationally constrained by current network connectivity and the availability of an upload directory containing files. |
| C-004 | The complete APM collection, storage, reporting, metric-schema, and plugin-injection pipeline is outside this SRS unless separately specified. |

## 8. Verification and Acceptance

| Requirement Set | Verification Method | Acceptance Criteria |
|---|---|---|
| FR-001, FR-002, NFR-001, DR-001 | Inspection / Test | After work-handler initialization, the work handler is bound to a background `HandlerThread` looper and submitted runnable/upload tasks are dispatched through that handler rather than run inline on the caller thread. |
| FR-003, NFR-002 | Test | With no network connection, upload processing exits before upload-directory scanning or file processing begins. |
| FR-004 | Inspection / Test | With forced sending enabled, storage pop behavior occurs before upload-directory scanning. |
| FR-005, DR-003, DR-004, DR-005 | Inspection / Test | Connected upload processing obtains the upload directory, enumerates matching files, and reads each file into `bParam`. |
| FR-006, DR-006, DR-007 | Inspection / Test | During per-file processing, the system derives `cParam` from Android context and submits the `bParam`/`cParam` pair to the configured sender. |
| FR-007, DR-008, NFR-005 | Inspection / Test | On sender success, the corresponding upload file is deleted; on sender failure, the failure is logged. |
| FR-008, DR-009 | Inspection / Test | Wrapped response handling inspects/instruments the transaction state for the `HttpResponse` and delegates to the underlying `ResponseHandler`. |
| FR-009, NFR-003, DR-010, DR-011 | Inspection / Test | A non-null entity is wrapped; `getContent()` returns or reuses a counting input stream; `writeTo(OutputStream)` delegates to the wrapped entity; null construction raises `IllegalArgumentException`. |
| FR-010, DR-002, NFR-004 | Inspection | Default background and main-thread handlers are available, and used interfaces match Android and Apache `HttpClient` environments. |
| C-001, C-002, C-003, C-004 | Inspection | Platform constraints, HTTP client constraints, upload operating constraints, and out-of-scope APM pipeline boundaries are recorded in design or test documentation. |
