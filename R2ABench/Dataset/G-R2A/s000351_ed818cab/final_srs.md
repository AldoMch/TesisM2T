# Software Requirements Specification

## 1. Introduction

### Purpose
This SRS specifies the externally observable requirements for `Kangrand`, a command-line Pollard's kangaroo interval ECDLP solver for `SECP256K1`, based only on the repository evidence at commit `7a8099ad352668fce4f0dfc7ebd0354b29b7f301`.

### Product Scope
The product solves interval discrete logarithm problems on `SECP256K1` using Pollard's kangaroo with distinguished points, supports resumable work through saved work files, and supports a simple server/client distributed execution mode. Source support is limited to the repository README evidence.

### Intended Audience
This document is for operators running the solver, integrators using its file or network interfaces, and reviewers verifying supported behavior against repository evidence.

### References
- Repository: `iceland2k14/Kangrand`
- Snapshot: `7a8099ad352668fce4f0dfc7ebd0354b29b7f301`
- Primary evidence source: `README.md` (`E001`-`E006`)

## 2. Overall Description

### Product Perspective
`Kangrand` is a standalone command-line solver for interval ECDLP on `SECP256K1`. It uses the distinguished point method to store selected walk points and detect collisions. It also supports saving, resuming, inspecting, and merging work files, plus a simple distributed server/client mode. (`E001`, `E002`, `E004`, `E005`, `E006`)

### Product Functions Summary
- Accept an input ASCII file containing hexadecimal values and public keys in compressed or uncompressed form. (`E004`, `E005`)
- Solve interval ECDLP on `SECP256K1` using Pollard's kangaroo with tame and wild herds. (`E002`, `E004`)
- Save work periodically and resume from saved work files. (`E001`, `E003`, `E006`)
- Inspect work-file information and merge work files offline, including cases where merge solves the key. (`E001`, `E006`)
- Support `wsplit`-style backups that reset the in-memory hash table after each backup. (`E001`, `E006`)
- Support a simple server/client distributed mode, including a server started with backup interval, distinguished bits, and a config file, and clients that connect to a named server. (`E002`)

### User Classes
- Local operator: runs the solver from the command line with input files and work-file options. (`E003`, `E004`)
- Distributed operator: runs the simple server and one or more clients. (`E002`)
- Offline analyst: inspects and merges saved work files. (`E001`, `E006`)

### Operating Environment
- Command-line execution environment. (`E002`, `E003`, `E004`)
- File-based operation using ASCII input and work files. (`E001`, `E003`, `E004`, `E005`, `E006`)
- Optional networked server/client environment. (`E002`)
- Optional GPU-backed client execution is referenced in usage text. (`E002`)

### Assumptions and Dependencies
- The solver is specific to `SECP256K1`. (`E004`, `E005`)
- Distributed deployments depend on an operator-managed network because the server has no authentication mechanism. (`E002`)
- Work-file continuation on changed hardware or changed distinguished-point settings is supported but may not be performance-optimal. This is inferred from README guidance. (`E003`, evidence type: inferred)

## 3. External Interface Requirements

### User Interfaces
The product shall provide a command-line interface with options for input files, work-file save/resume behavior, distinguished-point sizing, and distributed server/client operation. (`E002`, `E003`, `E004`)

### Software/API Interfaces
No programmatic API is evidenced. The supported interfaces are:
- ASCII input files for problem definition. (`E004`, `E005`)
- Work files for persistence, inspection, and merge workflows. (`E001`, `E003`, `E006`)
- A config file used when starting the server. (`E002`)

### Communication Interfaces
The product supports a simple client/server communication model in which clients connect to a server. The server has no authentication mechanism. (`E002`)

### Data Exchange Formats
- Input ASCII file: hexadecimal values; public keys may be compressed or uncompressed. (`E004`, `E005`)
- Work files: binary or structured file format not specified in evidence, used for save/resume/info/merge workflows. (`E001`, `E003`, `E006`)
- Server config file: format unspecified in evidence. (`E002`)

## 4. Functional Requirements

| ID | Description | Trigger / Input | System Behavior | Output | Priority | Verification | Source Evidence |
|---|---|---|---|---|---|---|---|
| FR-001 | The system shall accept an input ASCII file for solving an interval ECDLP instance on `SECP256K1`. | User provides an input file. | The system shall read problem values from the input ASCII file. | Solver starts from the provided problem definition. | High | Test | `E004`, `E005` |
| FR-002 | The system shall accept hexadecimal input values and public keys in either compressed or uncompressed format. | User provides values and public keys in the input file. | The system shall parse all values as hex and accept either public-key encoding. | Parsed problem instance or input rejection on invalid format. | High | Test | `E004`, `E005` |
| FR-003 | The system shall solve an interval discrete logarithm problem on `SECP256K1` using Pollard's kangaroo with tame and wild herds and distinguished points. | User starts a solve operation. | The system shall run kangaroo walks and use distinguished points to detect collisions that can reveal the key. | Solved key or ongoing search state. | High | Demonstration | `E002`, `E004`, `E005` |
| FR-004 | The system shall support periodic saving of work files during execution. | User enables work-file save options and interval. | The system shall write work files at the configured interval, including the documented 30-second example workflow. | One or more saved work files. | High | Test | `E001`, `E003`, `E006` |
| FR-005 | The system shall support resuming a search from a saved work file without requiring the original input ASCII file. | User provides a work file with the resume option. | The system shall continue the saved work from the work file alone. | Resumed search execution. | High | Test | `E003` |
| FR-006 | The system shall support saving work files with kangaroo state when requested. | User saves work with the documented option that includes kangaroos. | The system shall include kangaroo state in the saved work file. | Work file suitable for same-configuration continuation with reduced lost work from distinguished-point overhead. | Medium | Test | `E003` |
| FR-007 | The system shall provide a way to obtain information from a work file. | User requests work-file information. | The system shall read the specified work file and return its information. | Display or report of work-file information. | Medium | Demonstration | `E001` |
| FR-008 | The system shall support merging two work files offline. | User provides two work files for merge. | The system shall merge the saved work states; if the merge reveals a solved key, it shall report that result. | Merged result and possibly solved key. | High | Test | `E001`, `E006` |
| FR-009 | The system shall support `wsplit`-style backups that save a prefixed work file at each backup and reset the in-memory hash table after each backup. | User enables the documented split-work option. | The system shall save backup work files with a prefix and clear the in-memory hash table after each backup cycle. | Sequence of prefixed work files and reset in-memory hash table state. | Medium | Test | `E001`, `E006` |
| FR-010 | The system shall support a distributed mode with a server that can be started with a backup interval, distinguished-point setting, and a config file. | Operator starts the server with the documented parameters. | The system shall initialize server-side distributed execution using the provided backup interval, distinguished bits, and config file. | Running server instance. | Medium | Demonstration | `E002` |
| FR-011 | The system shall support clients connecting to the distributed server, including a documented GPU client mode. | Operator starts a client and specifies the server. | The system shall connect the client to the named server and participate in distributed computation. | Active client/server distributed session. | Medium | Demonstration | `E002` |

## 5. Non-Functional Requirements

| ID | Requirement | Quality Attribute | Priority | Verification | Source Evidence | Evidence Type |
|---|---|---|---|---|---|---|
| NFR-001 | The system shall use the distinguished point method to reduce stored walk data by storing only points whose `x` value begins with the configured number of zero bits. | Memory efficiency | High | Inspection | `E004`, `E005` | explicit |
| NFR-002 | The system shall allow operators to trade memory use against computational overhead through distinguished-point sizing. | Performance / resource tuning | Medium | Analysis | `E003`, `E004` | explicit |
| NFR-003 | When `wsplit` mode is used, the system shall bound in-memory hash-table growth by resetting the hash table at each backup after writing a prefixed work file. | Memory management | Medium | Test | `E001`, `E006` | explicit |
| NFR-004 | The distributed server shall be treated as unauthenticated; it shall not be relied on to authenticate clients or protect exposure on public networks. | Security | High | Inspection | `E002` | explicit |
| NFR-005 | The system should support continuation of saved work across different hardware or changed distinguished-point settings, but performance may degrade in those cases. | Portability | Low | Demonstration | `E003` | inferred |

## 6. Data Requirements

| ID | Data Item / Entity | Requirement | Source Evidence |
|---|---|---|---|
| DR-001 | Input ASCII file | The input file shall contain problem values in hexadecimal format. | `E004`, `E005` |
| DR-002 | Public key | The input file shall allow public keys in compressed or uncompressed form. | `E004`, `E005` |
| DR-003 | Work file | The system shall persist search state in work files for later resume, inspection, or merge. | `E001`, `E003`, `E006` |
| DR-004 | Work file with kangaroo state | When the relevant save option is used, the work file shall include kangaroo state to reduce lost work when resuming on the same configuration. | `E003` |
| DR-005 | Split-work backup files | In `wsplit` mode, the system shall emit prefixed work files at each backup point. | `E001`, `E006` |
| DR-006 | Server config file | The distributed server startup shall accept a config file. The file format is not specified in evidence. | `E002` |

## 7. Constraints

| ID | Constraint | Source Evidence |
|---|---|---|
| C-001 | The supported cryptographic problem scope is interval ECDLP on `SECP256K1`. | `E004`, `E005` |
| C-002 | The product is operated through command-line options and files; no graphical interface is evidenced. | `E002`, `E003`, `E004` |
| C-003 | Distributed deployment has no authentication mechanism and therefore must be operator-controlled if network exposure is a concern. | `E002` |
| C-004 | Merging split work files may require the expected RAM at merge time even if `wsplit` reduced RAM during collection. | `E001`, `E006` |

## 8. Verification and Acceptance

| Requirement ID | Verification Method | Acceptance Basis |
|---|---|---|
| FR-001 | Test | A valid input ASCII file starts a solve run. |
| FR-002 | Test | Hex values and both public-key encodings are accepted. |
| FR-003 | Demonstration | A solve run performs kangaroo search and reports a result or ongoing search. |
| FR-004 | Test | Work files are created at the configured save interval. |
| FR-005 | Test | A run resumes from a work file without the original input file. |
| FR-006 | Test | Saved work includes kangaroo state when the documented option is used. |
| FR-007 | Demonstration | Work-file information can be retrieved from a saved work file. |
| FR-008 | Test | Two work files can be merged and a solved key is reported when applicable. |
| FR-009 | Test | `wsplit` mode writes prefixed backups and resets the in-memory hash table after each backup. |
| FR-010 | Demonstration | The server starts using the documented backup interval, distinguished bits, and config file inputs. |
| FR-011 | Demonstration | A client connects to the named server and participates in distributed execution. |
| NFR-001 | Inspection | Documentation and observed behavior show only distinguished points are retained. |
| NFR-002 | Analysis | Changing distinguished-point sizing changes the documented time/memory tradeoff. |
| NFR-003 | Test | Memory-bounding behavior occurs across backup cycles in `wsplit` mode. |
| NFR-004 | Inspection | No authentication mechanism is present for the distributed server. |
| NFR-005 | Demonstration | A saved work file resumes on changed hardware or settings, with possible reduced performance. |

## 9. Traceability Matrix

| ID | Requirement | Type | Source | Evidence Type | Verification | Confidence |
|---|---|---|---|---|---|---|
| FR-001 | Accept input ASCII file for `SECP256K1` interval ECDLP solving | Functional | `E004`, `E005` | explicit | Test | High |
| FR-002 | Accept hex values and compressed/uncompressed public keys | Functional | `E004`, `E005` | explicit | Test | High |
| FR-003 | Solve using Pollard's kangaroo with tame/wild herds and distinguished points | Functional | `E002`, `E004`, `E005` | explicit | Demonstration | High |
| FR-004 | Save work files periodically | Functional | `E001`, `E003`, `E006` | explicit | Test | High |
| FR-005 | Resume from work file without original input file | Functional | `E003` | explicit | Test | High |
| FR-006 | Save work including kangaroo state | Functional | `E003` | explicit | Test | Medium |
| FR-007 | Retrieve information from a work file | Functional | `E001` | explicit | Demonstration | Medium |
| FR-008 | Merge two work files offline and report solved key when found | Functional | `E001`, `E006` | explicit | Test | High |
| FR-009 | Support `wsplit` backup/reset behavior | Functional | `E001`, `E006` | explicit | Test | High |
| FR-010 | Start distributed server with backup interval, distinguished bits, and config file | Functional | `E002` | explicit | Demonstration | Medium |
| FR-011 | Connect clients, including GPU client mode, to the server | Functional | `E002` | explicit | Demonstration | Medium |
| NFR-001 | Store only distinguished points selected by `x`-bit pattern | Non-functional | `E004`, `E005` | explicit | Inspection | High |
| NFR-002 | Expose distinguished-point sizing as a time/memory tradeoff control | Non-functional | `E003`, `E004` | explicit | Analysis | Medium |
| NFR-003 | Bound RAM growth in `wsplit` mode by resetting hash table each backup | Non-functional | `E001`, `E006` | explicit | Test | High |
| NFR-004 | Operate distributed server without authentication | Non-functional | `E002` | explicit | Inspection | High |
| NFR-005 | Support resumed work across changed hardware/settings with possible performance loss | Non-functional | `E003` | inferred | Demonstration | Low |
