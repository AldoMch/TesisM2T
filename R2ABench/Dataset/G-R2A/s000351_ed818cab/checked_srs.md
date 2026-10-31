# Software Requirements Specification

## 1. Introduction

### Purpose
This SRS specifies the externally observable requirements for Kangrand, a command-line Pollard's kangaroo interval ECDLP solver for SECP256K1. The specification is limited to behavior and interfaces supported by the available repository documentation and architecture materials.

### Product Scope
The product solves interval discrete logarithm problems on SECP256K1 using Pollard's kangaroo with distinguished points, supports resumable work through saved work files, and supports distributed execution with servers, clients, and offline work-file merging.

### Intended Audience
This document is intended for:
- Operators running the solver locally or in distributed mode
- Integrators using its file or network interfaces
- Test engineers validating documented behavior
- Architects deriving system structure from repository-supported behavior

### References
- Repository: `iceland2k14/Kangrand`
- Repository documentation: `README.md`
- Architecture diagram: `DOC/architecture.jpg`

## 2. Overall Description

### Product Perspective
Kangrand is a standalone command-line solver for interval ECDLP on SECP256K1. It uses Pollard's kangaroo algorithm with distinguished points to store selected walk points and detect collisions.

The documented architecture shows that distributed execution can be coordinated by one or more wsplit-enabled servers and multiple clients. Clients perform kangaroo computation and produce local kangaroo or work data, while servers periodically output work files, hash-table data, and result files. An offline merger can combine multiple work files into a master work file or hash table and may discover solving results during the merge process.

### Product Functions Summary
The system supports:
- Accepting an input ASCII file containing hexadecimal values and public keys in compressed or uncompressed form
- Solving interval ECDLP on SECP256K1 using Pollard's kangaroo with tame and wild herds and distinguished points
- Saving work periodically and resuming from saved work files
- Saving work files that include kangaroo state
- Inspecting work-file information and merging work files offline
- Supporting wsplit-style backups that reset the in-memory hash table after each backup
- Supporting distributed execution with servers and clients
- Supporting GPU-enabled execution through command-line options

### User Classes
- Local operator: runs the solver from the command line with input files and work-file options
- Distributed operator: runs distributed servers and one or more clients
- Offline analyst: inspects and merges saved work files

### Operating Environment
- Command-line execution environment
- File-based operation using ASCII input files and work files
- Optional networked distributed environment with servers and clients
- CPU or GPU-enabled command-line execution environments

### Assumptions and Dependencies
- The solver is specific to SECP256K1.
- Distributed deployments depend on an operator-managed network because the server has no authentication mechanism.
- Continued use of a saved work file across different hardware or different distinguished-point settings is supported for the same key and range, but may introduce additional overhead.

## 3. External Interface Requirements

### User Interfaces
The system shall provide a command-line interface with options for:
- Input file selection
- Work-file save and resume behavior
- Distinguished-point sizing
- Distributed server and client operation
- GPU-related execution options

### Software and File Interfaces
The supported external interfaces are:
- ASCII input files for problem definition
- Work files for persistence, resume, inspection, and merge workflows
- A configuration file used when starting a distributed server
- Result and intermediate files produced by distributed processing and merge workflows

### Communication Interfaces
The system shall support a client/server communication model in which clients connect to a specified server for distributed execution.

The distributed server shall have no built-in authentication mechanism.

### Data Exchange Formats
- Input ASCII files shall contain hexadecimal values.
- Public keys in the input file may be provided in compressed or uncompressed form.
- Work files shall persist solver state for later resume, inspection, or merge.
- Server configuration file format is implementation-defined by the documented command-line workflow.
- Distributed execution may produce result files and server-side work or hash-table artifacts.

## 4. Functional Requirements

| ID | Description | Trigger / Input | System Behavior | Output | Priority | Verification |
|---|---|---|---|---|---|---|
| FR-001 | Input file acceptance | User provides an input file. | The system shall read an input ASCII file defining an interval ECDLP instance on SECP256K1. | Solver starts from the provided problem definition. | High | Test |
| FR-002 | Hex and public-key parsing | User provides values and public keys in the input file. | The system shall parse hexadecimal input values and accept public keys in compressed or uncompressed form. | Parsed problem instance. | High | Test |
| FR-003 | Interval ECDLP solving | User starts a solve operation. | The system shall solve an interval discrete logarithm problem on SECP256K1 using Pollard's kangaroo with tame and wild herds and distinguished points. | Solved key or ongoing search state. | High | Demonstration |
| FR-004 | Periodic work-file saving | User specifies `-w` and `-wi`. | The system shall support using `-w` to specify a work file and `-wi` to specify a periodic save interval. The README includes 30 seconds as an example interval. | One or more saved work files at the configured interval. | High | Test |
| FR-005 | Resume from work file | User provides `-i` with a saved work file. | The system shall support resuming a search from a saved work file using `-i`, without requiring the original input ASCII file. | Resumed search execution. | High | Test |
| FR-006 | Save kangaroo state | User specifies `-ws`; operator may also specify `-d`. | The system shall support using `-ws` to save kangaroo state into a work file. The system shall support using `-d` to manually specify the distinguished-point bit count. | Work file including kangaroo state, suitable for continued use under compatible problem settings. | Medium | Test |
| FR-007 | Work-file information retrieval | User requests work-file information. | The system shall read a specified work file and return its information. | Display or report of work-file information. | Medium | Demonstration |
| FR-008 | Offline work-file merge | User provides two or more work files for merge. | The system shall support merging work files offline. If the merge reveals a solved key, the system shall report that result. | Merged work result and, when applicable, solved key. | High | Test |
| FR-009 | Wsplit backup behavior | User enables wsplit-style operation. | The system shall save prefixed backup work files and reset the in-memory hash table after each backup cycle. | Sequence of prefixed work files and reset hash-table state across cycles. | Medium | Test |
| FR-010 | Distributed server startup | Operator starts a server with documented parameters. | The system shall support starting a distributed server using a backup interval, a distinguished-point setting, and a configuration file. | Running distributed server instance. | Medium | Demonstration |
| FR-011 | Distributed client connection | Operator starts a client and specifies a server. | The system shall support clients connecting to a specified server to participate in distributed execution. Clients may run with GPU computation options through command-line parameters. | Active distributed client/server session. | Medium | Demonstration |
| FR-012 | Offline merger topology support | Operator collects work from distributed execution. | The system shall support an offline merge workflow in which multiple work files from distributed processing are combined into a master work file or hash table. | Consolidated work state and any merge-discovered result. | Medium | Demonstration |

## 5. Non-Functional Requirements

| ID | Quality Attribute | Requirement | Priority | Verification |
|---|---|---|---|---|
| NFR-001 | Memory efficiency | The system shall use the distinguished-point method to reduce stored walk data by storing only distinguished points selected by the configured criterion. | High | Inspection |
| NFR-002 | Resource tunability | The system shall allow operators to trade memory use against computational overhead through distinguished-point sizing. | Medium | Analysis |
| NFR-003 | Memory management | When wsplit mode is used, the system shall bound in-memory hash-table growth by resetting the hash table after each backup cycle. | Medium | Test |
| NFR-004 | Security | The distributed server shall not be relied on to authenticate clients or protect exposure on public networks. | High | Inspection |
| NFR-005 | Portability of saved work | The system shall allow a work file to be resumed or merged for the same key and range across different hardware, different distinguished-point bit counts, or different kangaroo-count configurations. Any resulting overhead is an operational note and not an acceptance criterion. | Low | Demonstration |

## 6. Data Requirements

| ID | Data Item | Requirement |
|---|---|---|
| DR-001 | Input ASCII file | The input file shall contain problem values in hexadecimal format. |
| DR-002 | Public key | The input file shall allow public keys in compressed or uncompressed form. |
| DR-003 | Work file | The system shall persist search state in work files for later resume, inspection, or merge. |
| DR-004 | Work file with kangaroo state | When `-ws` is used, the work file shall include kangaroo state. |
| DR-005 | Split-work backup files | In wsplit mode, the system shall emit prefixed work files at each backup point. |
| DR-006 | Server configuration file | Distributed server startup shall accept a configuration file. |
| DR-007 | Distributed merge artifacts | Distributed execution and merge workflows shall support multiple work files being combined into a master work file or hash-table state. |
| DR-008 | Result file | Distributed or merged execution may produce a result file containing solving output. |

## 7. System Constraints

| ID | Constraint |
|---|---|
| C-001 | The supported cryptographic problem scope is interval ECDLP on SECP256K1. |
| C-002 | The product is operated through command-line options and files; no graphical interface is specified. |
| C-003 | Distributed deployment has no authentication mechanism and therefore must be operator-controlled if network exposure is a concern. |
| C-004 | Merging split work files may require the expected RAM at merge time even if wsplit reduced RAM during collection. |
| C-005 | When a distributed server is restarted with a different configuration, especially when the solving range or target key changes, the operator must stop existing clients; otherwise clients may automatically reconnect and submit wrong points that do not match the new configuration. |

## 8. Verification and Acceptance Criteria

| Requirement ID | Verification Method | Acceptance Criterion |
|---|---|---|
| FR-001 | Test | A valid input ASCII file starts a solve run. |
| FR-002 | Test | Hexadecimal values and both public-key encodings are parsed successfully. |
| FR-003 | Demonstration | A solve run performs kangaroo search for an interval ECDLP instance on SECP256K1 and reports a result or ongoing search state. |
| FR-004 | Test | When `-w` and `-wi` are provided, work files are created at the user-configured save interval. |
| FR-005 | Test | A run resumes from a saved work file using `-i` without requiring the original input ASCII file. |
| FR-006 | Test | When `-ws` is used, the saved work file includes kangaroo state; when `-d` is used, the distinguished-point bit count is manually set. |
| FR-007 | Demonstration | Work-file information can be retrieved from a specified saved work file. |
| FR-008 | Test | Two or more work files can be merged offline, and a solved key is reported when the merge reveals one. |
| FR-009 | Test | Wsplit operation writes prefixed backup files and resets the in-memory hash table after each backup cycle. |
| FR-010 | Demonstration | The server starts using the documented backup interval, distinguished-point setting, and configuration file inputs. |
| FR-011 | Demonstration | A client connects to a specified server and participates in distributed execution; GPU-related command-line options are accepted when used. |
| FR-012 | Demonstration | Multiple distributed work files can be consolidated into a master work file or hash-table state through an offline merge workflow. |
| NFR-001 | Inspection | Documentation and observable behavior show that only distinguished points are retained for collision detection storage. |
| NFR-002 | Analysis | Changing the distinguished-point setting changes the documented time/memory tradeoff available to operators. |
| NFR-003 | Test | In wsplit mode, hash-table memory is reset across backup cycles. |
| NFR-004 | Inspection | The distributed server provides no built-in authentication mechanism. |
| NFR-005 | Demonstration | A saved work file can be successfully resumed or merged after hardware or distinguished-point-setting changes for the same key and range; performance variation is informational only. |
| C-005 | Inspection | Distributed-operation documentation records that clients must be stopped when a server is restarted with changed configuration to prevent submission of wrong points. |
