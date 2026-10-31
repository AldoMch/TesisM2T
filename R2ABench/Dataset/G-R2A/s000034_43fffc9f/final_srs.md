# Software Requirements Specification (SRS)

Repository: IBM/torc_py  
Repository URL: https://github.com/IBM/torc_py  
Commit: `cbd7199aad06f7bff7e8e089ebec2cd1b0265c8a`

## 1. Introduction

### 1.1 Purpose
This SRS defines evidence-backed software requirements for `torc_py`, a Python library for task-based parallelism. The document is derived only from the provided repository evidence and is intended to describe externally observable behavior, interfaces, constraints, and verifiable qualities.

### 1.2 Product scope
`torc_py` is described as a platform-agnostic adaptive load balancing library that orchestrates scheduling of multiple function evaluations on shared-memory and distributed-memory platforms. It provides a parallel computing framework for expressing and executing task-based parallelism, uses MPI internally in a way that is transparent to the user, allows legacy MPI use at the application level, and supports parallel nested loops and map functions. Sources: E004, E001, E003.

### 1.3 Intended audience
- Application developers using Python for task-based parallel execution
- Users running workloads across worker threads, MPI processes, or cluster nodes
- Testers and maintainers validating library behavior against examples and tests

### 1.4 References
- Repository README: evidence IDs E001, E003, E004, E005, E006
- Repository test: evidence ID E002
- Repository metadata: IBM/torc_py, commit `cbd7199aad06f7bff7e8e089ebec2cd1b0265c8a`

## 2. Overall Description

### 2.1 Product perspective
`torc_py` is a Python tasking library used by Python applications to submit function evaluations for parallel execution. It operates across worker threads and MPI processes, including distributed cluster nodes, while presenting a unified task-based programming model. Sources: E004, E001, E003, E002.

### 2.2 Product functions summary
The evidence supports the following product functions:
- Submit function-evaluation tasks for parallel execution and wait for completion
- Return task input and result values to the application
- Provide parallel map behavior
- Execute callback tasks when parent tasks complete
- Distribute work across available workers
- Allow idle workers to steal tasks from other queues
- Support use on shared-memory and distributed-memory platforms
- Use MPI internally while permitting legacy MPI at the application level

Sources: E001, E002, E003, E004, E006.

### 2.3 User classes
- Python developers parallelizing function evaluations
- HPC users running tasks on multiple worker threads and MPI processes
- Users preprocessing image datasets or running numerical/optimization workloads on clusters

Sources: E004, E005, E002.

### 2.4 Operating environment
Supported or evidenced execution environments include:
- Python applications importing `torc`
- Worker-thread execution within a process
- MPI-based multi-process execution
- Shared-memory and distributed-memory platforms
- Cluster-node execution
- Configurations using `TORC_WORKERS` environment variable in tests

Sources: E004, E003, E005, E002.

### 2.5 Assumptions and dependencies
- MPI is used internally by the library. Source: E004.
- Applications may also use legacy MPI code at the application level. Source: E004.
- Some callback examples assume a single worker thread per MPI process. Source: E003.
- Task execution depends on the availability of workers. Sources: E001, E006.

## 3. External Interface Requirements

### 3.1 User interfaces
No graphical user interface is evidenced. Interaction is through a Python programming interface and program output. Sources: E002, E004.

### 3.2 Software/API interfaces
The evidence shows the following Python-facing interfaces:

| Interface | Observed behavior | Source |
|---|---|---|
| `torc.submit(function, input)` | Submits a task for asynchronous execution and returns a task handle | E002 |
| `torc.wait()` | Waits for submitted tasks to complete before proceeding | E002, E001 |
| `torc.gettime()` | Obtains timing values used to measure elapsed execution time | E002 |
| `task.input()` | Returns the input associated with a task | E002 |
| `task.result()` | Returns the completed task result | E002 |

The README also evidences map-style operation and callback-based execution behavior, but does not expose exact API signatures in the provided excerpts. Sources: E001, E003, E006.

### 3.3 Communication interfaces
- Internal MPI-based communication is used by the library. Source: E004.
- Idle workers may issue steal requests to retrieve tasks from another rank's queue. Source: E003.

### 3.4 Data exchange formats
- Task inputs and outputs are exchanged as Python function arguments and results. Source: E002.
- An image-preprocessing example transforms image datasets organized in labeled subfolders into a single HDF5 file. Source: E005.

## 4. Functional Requirements

| ID | Description | Trigger/Input | System behavior | Output | Priority | Verification | Source evidence |
|---|---|---|---|---|---|---|---|
| FR-001 | Parallel task submission and completion waiting | The application submits one or more function-evaluation tasks and invokes a wait operation | The system shall accept submitted tasks for parallel execution on available workers and shall block completion of the wait operation until the submitted tasks have completed | Completed tasks available for result retrieval after wait returns | High | Test | E002, E001 |
| FR-002 | Task result retrieval | A completed task handle is available | The system shall expose the original task input and the computed task result through the task handle | Task input value and task result value retrievable by the application | High | Test | E002 |
| FR-003 | Parallel map execution | The application invokes map-style parallel evaluation | The system shall support parallel map behavior equivalent to submitting tasks individually; the documented default chunk size in the example is 1 | Collection of mapped function results | Medium | Demonstration | E001, E006 |
| FR-004 | Callback task execution on completion | A task completes and a callback task is associated with it | The system shall pass the completed task as an argument to a callback task and execute that callback task on worker threads of the node/process where the parent task is active | Callback task execution and any callback-produced application-visible effects | Medium | Demonstration | E001, E003 |
| FR-005 | Cyclic distribution across available workers | A primary task spawns multiple child tasks for available workers | The system shall distribute spawned tasks across available workers, including cyclic distribution as documented in the example | Tasks assigned across workers for execution | Medium | Demonstration | E001, E006 |
| FR-006 | Work stealing for idle workers | A worker finds its local queue empty while tasks remain queued elsewhere | The system shall allow the idle worker to issue a steal request and retrieve a task from another worker or rank queue | Retrieved task assigned to the idle worker for execution | Medium | Demonstration | E003 |
| FR-007 | Unified execution across shared and distributed memory platforms | The application uses the library for task-based parallelism | The system shall provide a unified approach for expressing and executing task-based parallelism on both shared-memory and distributed-memory platforms | Parallel execution using the same task-based approach across supported platform types | High | Inspection | E004 |
| FR-008 | Transparent internal MPI use with application-level legacy MPI compatibility | The application runs under the library in an MPI-capable environment, with or without its own MPI code | The system shall use MPI internally in a manner transparent to the user and shall allow legacy MPI code at the application level | Parallel operation without requiring users to manage internal MPI details, while preserving application-level MPI use | High | Inspection | E004 |

## 5. Non-Functional Requirements

| ID | Quality | Requirement | Priority | Verification | Evidence | Confidence |
|---|---|---|---|---|---|---|
| NFR-001 | Portability | The system shall operate on both shared-memory and distributed-memory platforms. | High | Inspection | E004 | Explicit |
| NFR-002 | Compatibility | The system shall remain compatible with application-level legacy MPI code while using MPI internally. | High | Inspection | E004 | Explicit |
| NFR-003 | Performance (demonstrated capability) | The system shall support parallel execution patterns that can reduce elapsed runtime relative to serial execution; repository evidence demonstrates a 4x faster example when four workers each execute one task. | Medium | Demonstration | E001 | Explicit |
| NFR-004 | Scalability (demonstrated capability) | The system shall support cluster-scale execution; repository evidence reports TMCMC scheduling with overall parallel efficiency greater than 90% on 1024 compute nodes in a documented use case. | Medium | Analysis | E005 | Explicit |
| NFR-005 | Load balancing | The system shall support adaptive load balancing behavior through work stealing when idle workers detect empty local queues. | Medium | Demonstration | E003, E004 | Explicit |

## 6. Data Requirements

| ID | Data entity/object | Requirement | Source evidence |
|---|---|---|---|
| DR-001 | Task | A task shall encapsulate a submitted function evaluation and preserve access to its associated input and computed result. | E002 |
| DR-002 | Task input/output | The system shall accept Python function inputs as task input data and produce function return values as task result data. | E002 |
| DR-003 | Callback argument | For callback execution, the completed task shall be passed as the callback task argument. | E001, E003 |
| DR-004 | Worker queues | The system shall maintain task queues sufficient to support local execution and task stealing between workers or ranks. | E003 |
| DR-005 | Image preprocessing data | In the documented image-preprocessing use case, the input dataset consists of images organized in subfolders where each subfolder name denotes the label, and the output is a single HDF5 file. | E005 |

## 7. Constraints

| ID | Constraint | Source evidence |
|---|---|---|
| C-001 | The product is a Python library consumed through a Python module interface (`import torc`). | E002 |
| C-002 | The product depends on MPI for internal operation. | E004 |
| C-003 | Some documented callback behavior assumes a single worker thread per MPI process. | E003 |
| C-004 | Worker-count configuration is evidenced through the `TORC_WORKERS` environment variable in tests. | E002 |
| C-005 | Repository materials include Eclipse Public License v1.0 notices in test sources. | E002 |

## 8. Verification and Acceptance

| Requirement ID | Verification method | Acceptance basis |
|---|---|---|
| FR-001 | Test | Submitted tasks complete and `wait` returns only after completion |
| FR-002 | Test | For each completed task, `input()` and `result()` return expected values |
| FR-003 | Demonstration | Map-style execution produces the expected parallel evaluation behavior |
| FR-004 | Demonstration | Completed task is supplied to callback task and callback executes on the parent task's node/process |
| FR-005 | Demonstration | Multiple tasks are distributed across available workers as documented |
| FR-006 | Demonstration | Idle workers with empty local queues issue steal requests and execute stolen tasks |
| FR-007 | Inspection | Documentation and examples show one task-based approach across shared/distributed memory platforms |
| FR-008 | Inspection | Documentation states transparent internal MPI use and application-level legacy MPI allowance |
| NFR-001 | Inspection | Documentation states operation on shared and distributed memory platforms |
| NFR-002 | Inspection | Documentation states compatibility with legacy MPI code |
| NFR-003 | Demonstration | Example shows reduced elapsed runtime under parallel execution |
| NFR-004 | Analysis | Documented use case reports >90% efficiency on 1024 nodes |
| NFR-005 | Demonstration | Work-stealing example shows idle workers retrieving tasks from another queue |

## 9. Traceability Matrix

| ID | Requirement | Type | Source | Evidence Type | Verification | Confidence |
|---|---|---|---|---|---|---|
| FR-001 | Accept submitted tasks for parallel execution and wait for completion | Functional | E002, E001 | explicit | Test | High |
| FR-002 | Expose task input and result via task handle | Functional | E002 | explicit | Test | High |
| FR-003 | Support parallel map behavior | Functional | E001, E006 | explicit | Demonstration | Medium |
| FR-004 | Execute callback task with completed task argument on parent node/process | Functional | E001, E003 | explicit | Demonstration | Medium |
| FR-005 | Distribute tasks across available workers | Functional | E001, E006 | explicit | Demonstration | Medium |
| FR-006 | Support work stealing from non-empty queues | Functional | E003 | explicit | Demonstration | High |
| FR-007 | Provide unified task-based execution on shared/distributed memory platforms | Functional | E004 | explicit | Inspection | High |
| FR-008 | Use MPI internally transparently and allow legacy MPI at application level | Functional | E004 | explicit | Inspection | High |
| NFR-001 | Operate on shared-memory and distributed-memory platforms | Non-functional | E004 | explicit | Inspection | High |
| NFR-002 | Remain compatible with legacy MPI code | Non-functional | E004 | explicit | Inspection | High |
| NFR-003 | Support runtime reduction under parallel execution; 4x faster example demonstrated | Non-functional | E001 | explicit | Demonstration | Medium |
| NFR-004 | Support cluster-scale execution; >90% efficiency on 1024 nodes demonstrated in use case | Non-functional | E005 | explicit | Analysis | Medium |
| NFR-005 | Support adaptive load balancing through work stealing | Non-functional | E003, E004 | explicit | Demonstration | High |
| DR-001 | Task stores input and result | Data | E002 | explicit | Inspection | High |
| DR-002 | Task I/O consists of Python function arguments and return values | Data | E002 | explicit | Inspection | High |
| DR-003 | Completed task is callback input | Data | E001, E003 | explicit | Inspection | Medium |
| DR-004 | Queues support local execution and stealing | Data | E003 | inferred | Inspection | Medium |
| DR-005 | Image dataset folders with labels transformed to HDF5 output | Data | E005 | explicit | Inspection | Medium |
| C-001 | Python module interface constraint | Constraint | E002 | explicit | Inspection | High |
| C-002 | Internal MPI dependency | Constraint | E004 | explicit | Inspection | High |
| C-003 | Single-worker-per-process assumption for some callback examples | Constraint | E003 | explicit | Inspection | Medium |
| C-004 | Worker count configured via `TORC_WORKERS` in tests | Constraint | E002 | explicit | Inspection | Medium |
| C-005 | EPL v1.0 license notice present in repository test source | Constraint | E002 | explicit | Inspection | Medium |
