# Checked Software Requirements Specification: torc_py Task-Based Parallelism Library

## 1. Introduction

### 1.1 Purpose
This Software Requirements Specification defines normalized requirements for `torc_py`, a Python library for task-based parallelism. The library enables Python applications to express function evaluations as tasks, execute those tasks across worker threads and MPI processes, collect results, use callbacks, switch between task-parallel and SPMD execution, and apply adaptive load balancing through task stealing.

### 1.2 Scope
The system scope includes:
- a Python package imported as `torc`,
- task submission, waiting, result retrieval, and completion iteration,
- parallel map behavior,
- callback tasks associated with completed parent tasks,
- cyclic worker assignment when no target worker is specified,
- directed submission to a worker queue when a target queue identifier is specified,
- optional task stealing between MPI processes,
- use on shared-memory and distributed-memory platforms,
- internal MPI and multithreading support,
- compatibility with application-level MPI routines,
- configuration through environment variables,
- documented examples for master-worker execution, SPMD switching, numerical optimization, image preprocessing, and task stealing.

This SRS specifies requirements and runtime concepts. Architecture generation should derive structure from this document rather than rely on a pre-specified topology.

### 1.3 Intended Audience
- Python developers parallelizing function evaluations.
- HPC users running workloads across worker threads, MPI processes, or cluster nodes.
- Testers validating task execution, result retrieval, map behavior, callback behavior, and task stealing.
- Maintainers extending the Python tasking package and example suite.
- Architecture-generation tools consuming a clean SRS without review metadata.

### 1.4 Definitions and Abbreviations
| Term | Definition |
|---|---|
| Task | A submitted asynchronous function evaluation. |
| Future | Task descriptor that provides access to task input and result values. |
| Primary application task | The main application task launched on MPI rank 0. |
| Worker thread | Thread that executes task functions. |
| MPI process | Process participating in MPI-based execution. |
| Rank | MPI process identifier. |
| Queue identifier (`qid`) | Target worker identifier for task submission; `-1` means cyclic assignment. |
| SPMD | Single Program Multiple Data execution mode. |
| Task stealing | Mechanism allowing idle workers to retrieve tasks from another queue. |
| HDF5 | File format used by the image preprocessing example output. |

## 2. Overall Description

### 2.1 Product Perspective
`torc_py` is a Python tasking package used by Python applications that need task-based parallel execution. Applications submit task functions to the library, wait for task completion, retrieve task inputs and results, and optionally use callbacks or SPMD routines. The package is implemented on top of MPI and Python multithreading while exposing a single Python-facing programming model.

### 2.2 Function Summary
The system shall provide:
- asynchronous task submission for Python functions,
- waiting for child tasks to finish,
- retrieval of task input and computed result values,
- parallel map execution with configurable chunk size,
- callback execution when submitted tasks complete,
- cyclic task distribution across available workers,
- directed submission to a specific worker queue,
- task stealing from overloaded queues by idle workers,
- initialization and shutdown routines for library lifecycle control,
- switching from task-parallel execution to SPMD execution,
- runtime query calls for worker and node identifiers,
- timing support for examples and tests.

### 2.3 User Classes
| User class | Description |
|---|---|
| Python application developer | Uses `torc` APIs to submit functions and collect results. |
| HPC application developer | Runs task-parallel Python workloads across MPI processes and worker threads. |
| MPI application developer | Combines task-based parallelism with existing application-level MPI routines. |
| Data preprocessing user | Uses map-style parallelism to preprocess images and write HDF5 output. |
| Tester | Validates examples, environment variables, result correctness, and timing behavior. |

### 2.4 Operating Environment
| Environment aspect | Requirement context |
|---|---|
| Python runtime | The library is imported and used from Python applications. |
| MPI runtime | Multi-process execution uses MPI and `mpi4py`. |
| Worker threads | Each MPI process may use one or more worker threads. |
| Shared-memory platform | The same tasking model is intended to run on shared-memory systems. |
| Distributed-memory platform | The same tasking model is intended to run across MPI processes and cluster nodes. |
| Environment variables | Runtime behavior is configured through `TORC_WORKERS`, `TORC_STEALING`, `TORC_SERVER_YIELDTIME`, and `TORC_WORKER_YIELDTIME`. |
| Optional packages | Some examples require packages such as `numpy`, `cma`, `h5py`, and `pillow`. |

### 2.5 Assumptions and Dependencies
| ID | Assumption or dependency |
|---|---|
| AD-001 | MPI and `mpi4py` are available for MPI-based execution. |
| AD-002 | `termcolor` is available as a main Python package dependency. |
| AD-003 | Worker availability determines achievable parallel execution. |
| AD-004 | `TORC_WORKERS` controls the number of worker threads used by each MPI process, with default value `1`. |
| AD-005 | Some callback examples assume a single worker thread per MPI process. |
| AD-006 | Image preprocessing examples require input image files organized in labeled subfolders and packages for image/HDF5 processing. |

## 3. External Interface Requirements

### 3.1 User Interfaces
No graphical user interface is specified. Users interact with the system through Python APIs, command-line program execution, environment variables, and program output.

### 3.2 Software and API Interfaces
| ID | Interface | Requirement |
|---|---|---|
| API-001 | `torc.submit(f, *args, qid=-1, callback=None, **kwargs)` | The system shall submit a new asynchronous task for function `f` using the supplied arguments. |
| API-002 | `torc.wait(tasks=None)` | The system shall wait for all child tasks or a specified task collection to finish. |
| API-003 | `task.input()` | A completed task descriptor shall provide access to the submitted input value or values. |
| API-004 | `task.result()` | A completed task descriptor shall provide access to the computed return value. |
| API-005 | `torc.map(f, *seq, chunksize=1)` | The system shall execute function `f` over one or more sequences and return the resulting list. |
| API-006 | `torc.as_completed(tasks=None)` | The system shall provide completed child tasks in completion order. |
| API-007 | `callback` argument of `submit` | The system shall call the callback when the submitted task completes and its results are returned to the spawning rank. |
| API-008 | `torc.start(f)` | The system shall initialize the library, launch function `f` on rank 0 as the primary application task, and shut down after completion. |
| API-009 | `torc.init()` | The system shall initialize the tasking library for lower-level setup. |
| API-010 | `torc.launch(f)` | The system shall launch function `f` on rank 0 or activate worker execution on other ranks when no function is supplied. |
| API-011 | `torc.shutdown()` | The system shall shut down the tasking library after lower-level setup. |
| API-012 | `torc.spmd(f, *args)` | The system shall execute function `f` on all MPI processes to support SPMD execution and application-level MPI routines. |
| API-013 | `torc.enable_stealing()` / `torc.disable_stealing()` | The system shall enable and disable inter-process task stealing. |
| API-014 | `torc.gettime()` | The system shall return the current time as a floating-point value for timing measurements. |
| API-015 | `torc.worker_id()` / `torc.num_workers()` | The system shall expose the calling worker identifier and total worker count. |
| API-016 | `torc.node_id()` / `torc.num_nodes()` | The system shall expose the calling MPI rank and total MPI process count. |

### 3.3 Communication Interfaces
| ID | Interface | Requirement |
|---|---|---|
| CI-001 | Internal MPI communication | The system shall use MPI internally for communication across MPI processes. |
| CI-002 | Worker-thread scheduling | The system shall schedule submitted tasks on worker threads. |
| CI-003 | Task stealing requests | Idle workers shall be able to issue steal requests when local queues are empty and stealing is enabled. |
| CI-004 | Application-level MPI routines | Application code shall be able to invoke legacy MPI routines through SPMD execution without requiring users to manage the library's internal MPI details. |

### 3.4 Data Exchange Items
| ID | Data item | Description |
|---|---|---|
| DE-001 | Function arguments | Python values supplied to submitted task functions. |
| DE-002 | Function return values | Python values returned by completed task functions. |
| DE-003 | Task descriptor | Future-like object that stores task input and result values. |
| DE-004 | Callback argument | Completed task descriptor passed to callback execution. |
| DE-005 | Worker queue entries | Task entries queued for local execution or task stealing. |
| DE-006 | Image dataset files | Raw image files organized in labeled subfolders for preprocessing examples. |
| DE-007 | HDF5 output file | Single file produced by the image preprocessing example. |

## 4. Functional Requirements

| ID | Requirement | Trigger/Input | Required behavior | Output | Priority | Verification |
|---|---|---|---|---|---|---|
| FR-001 | The system shall accept submitted Python function-evaluation tasks for asynchronous execution. | Application calls `torc.submit`. | Create a task descriptor and queue the function evaluation for available workers. | Task descriptor. | High | Test |
| FR-002 | The system shall wait for submitted child tasks to complete. | Application calls `torc.wait`. | Suspend the current task until the relevant child tasks finish, while releasing the worker thread for other work where applicable. | Wait operation returns after task completion. | High | Test |
| FR-003 | The system shall expose task input and result values through the task descriptor. | Application reads a completed task descriptor. | Return the submitted input and computed result through `input()` and `result()`. | Input value and result value. | High | Test |
| FR-004 | The system shall provide parallel map execution. | Application calls `torc.map` with a function and one or more sequences. | Submit map tasks with configurable chunk size and return the list of results. | Ordered result list. | High | Test |
| FR-005 | The system shall distribute submitted tasks cyclically across available workers when no target worker is specified. | Application submits tasks with default `qid=-1`. | Assign tasks in cyclic order across workers. | Tasks assigned to available workers. | High | Demonstration |
| FR-006 | The system shall support directed submission to a specific worker queue. | Application submits a task with a target `qid`. | Place the task in the queue associated with the requested worker identifier or reject invalid identifiers. | Task queued for the target worker or argument error. | Medium | Test |
| FR-007 | The system shall execute callback tasks after parent task completion. | Application submits a task with a callback. | Pass the completed task descriptor to the callback and execute the callback on the rank that spawned the parent task after results are returned. | Callback execution and callback-visible effects. | Medium | Demonstration |
| FR-008 | The system shall support task stealing when enabled. | Idle worker finds a local queue empty while another queue has tasks. | Issue steal requests and retrieve a task from another queue. | Stolen task executed by an idle worker. | Medium | Demonstration |
| FR-009 | The system shall allow switching between task-parallel execution and SPMD execution. | Application calls `torc.spmd` or uses lower-level initialization and launch routines. | Execute a specified function on all MPI processes and allow application-level MPI routines inside that function. | SPMD function execution across MPI processes. | Medium | Demonstration |
| FR-010 | The system shall initialize, launch, and shut down the tasking runtime through setup APIs. | Application calls `start`, `init`, `launch`, or `shutdown`. | Manage tasking runtime lifecycle according to the selected setup pattern. | Runtime initialized, launched, or stopped. | High | Test |
| FR-011 | The system shall expose worker and node query calls. | Application calls worker or node query APIs. | Return global worker id, total worker count, MPI rank, or total MPI process count. | Runtime identifier values. | Medium | Test |
| FR-012 | The system shall support image preprocessing through map-style parallelism. | Application invokes the image preprocessing workflow with image folders. | Parallelize preprocessing operations and collect processed image/label outputs for HDF5 writing. | Preprocessed image tensors and labels. | Low | Demonstration |

## 5. Non-Functional Requirements

| ID | Requirement | Quality attribute | Priority | Verification |
|---|---|---|---|---|
| NFR-001 | The system shall provide one Python-facing tasking model intended for both shared-memory and distributed-memory execution. Acceptance is based on product description and examples; no automated cross-platform acceptance test is specified here. | Portability | Medium | Inspection |
| NFR-002 | The system shall maintain compatibility with application-level MPI routines while hiding internal MPI communication details from normal task submission users. | Compatibility | High | Inspection |
| NFR-003 | The system shall support parallel execution patterns where four worker threads, configured as two MPI processes with two workers each, can execute four one-second tasks in approximately one task-duration. | Performance | Medium | Demonstration |
| NFR-004 | The system shall support adaptive load balancing through task stealing when idle workers detect empty local queues and another queue has pending tasks. | Load balancing | Medium | Demonstration |
| NFR-005 | The system shall support cluster-scale scheduling use cases; the reported TMCMC/Pi4U result of more than 90% parallel efficiency on 1024 compute nodes shall be treated as a documented use-case result, not a guaranteed minimum for every workload. | Scalability | Medium | Analysis |
| NFR-006 | The system shall support nested parallelism and map-style parallel loops for Python applications. | Modifiability | Medium | Demonstration |

## 6. Data Requirements

| ID | Data requirement |
|---|---|
| DR-001 | A task descriptor shall preserve access to the submitted input and computed result. |
| DR-002 | Task inputs shall be Python function arguments. |
| DR-003 | Task outputs shall be Python function return values. |
| DR-004 | Callback execution shall receive the completed task descriptor as its argument. |
| DR-005 | Worker queues shall retain tasks awaiting local execution and shall support retrieval by task stealing. |
| DR-006 | Image preprocessing input shall consist of image files organized in subfolders whose names represent labels. |
| DR-007 | Image preprocessing output shall be written into an HDF5 file for later training use. |
| DR-008 | Environment variables shall provide runtime configuration values for worker count, stealing behavior, and idle-yield timing. |

## 7. Constraints

| ID | Constraint | Type |
|---|---|---|
| C-001 | The product shall be consumed through the Python module interface `import torc`. | Interface |
| C-002 | The product shall depend on MPI and `mpi4py` for MPI-based operation. | Technology |
| C-003 | The product shall use Python multithreading for worker execution. | Technology |
| C-004 | `TORC_WORKERS` shall configure the number of worker threads used by each MPI process; default value is `1`. | Runtime configuration |
| C-005 | `TORC_STEALING` shall configure whether inter-process task stealing is enabled; default value is `False`. | Runtime configuration |
| C-006 | `TORC_SERVER_YIELDTIME` and `TORC_WORKER_YIELDTIME` shall configure idle-yield timing for server and worker threads. | Runtime configuration |
| C-007 | Some callback examples require one worker thread per MPI process. | Example constraint |
| C-008 | Optional examples may require `numpy`, `cma`, `h5py`, or `pillow`. | Dependency |
| C-009 | Test and example execution may require `mpirun` and the ability to pass environment variables to MPI processes. | Execution environment |
| C-010 | Test materials include Eclipse Public License v1.0 notices. | License |

## 8. Verification and Acceptance Matrix

| Requirement ID | Verification method | Acceptance criterion |
|---|---|---|
| FR-001 | Test | Calling `torc.submit(work, x)` returns a task descriptor and schedules `work(x)` for execution. |
| FR-002 | Test | `torc.wait()` returns only after submitted child tasks have completed. |
| FR-003 | Test | `task.input()` and `task.result()` return the submitted input and expected computed result. |
| FR-004 | Test | `torc.map(work, data)` returns the same result values as applying `work` over `data`, subject to the chosen chunk size. |
| FR-005 | Demonstration | Default submission distributes tasks cyclically across available workers. |
| FR-006 | Test | A valid target `qid` queues the task for that worker; invalid target identifiers are rejected. |
| FR-007 | Demonstration | A callback receives the completed task descriptor after parent completion and can observe the parent result. |
| FR-008 | Demonstration | With stealing enabled, idle workers retrieve tasks from another queue and execute them. |
| FR-009 | Demonstration | `torc.spmd` executes a function across MPI processes and permits application-level MPI routines. |
| FR-010 | Test | `start`, `init`, `launch`, and `shutdown` manage runtime setup and teardown according to the selected pattern. |
| FR-011 | Test | Worker and node query APIs return identifiers and counts consistent with the running MPI/worker configuration. |
| FR-012 | Demonstration | Image preprocessing maps over images and produces values that can be written into HDF5 datasets. |
| NFR-001 | Inspection | Product description and examples indicate intended use on shared-memory and distributed-memory platforms. |
| NFR-002 | Inspection | Compatibility with application-level MPI is represented through SPMD support and internal-MPI transparency. |
| NFR-003 | Demonstration | Running four one-second tasks with two MPI processes and two workers per process completes in approximately one task-duration. |
| NFR-004 | Demonstration | Work-stealing execution shows idle workers retrieving tasks from a non-empty queue. |
| NFR-005 | Analysis | The TMCMC/Pi4U scalability result is recorded as a use-case capability example rather than a universal guarantee. |
| NFR-006 | Demonstration | Nested or map-style examples execute using task submission and result collection. |
| DR-001 | Inspection | Task descriptors expose input and result methods. |
| DR-002 | Inspection | Submitted tasks carry Python function arguments. |
| DR-003 | Test | Function return values are available through completed task descriptors. |
| DR-004 | Demonstration | Callback receives a completed task descriptor. |
| DR-005 | Demonstration | Queued tasks can be executed locally or retrieved through task stealing. |
| DR-006 | Inspection | Image preprocessing expects images grouped by label-named subfolders. |
| DR-007 | Inspection | Image preprocessing writes processed data to HDF5. |
| DR-008 | Inspection | Runtime environment variables configure worker count, stealing behavior, and idle-yield timing. |
| C-001 | Inspection | Applications import and call the `torc` Python package. |
| C-002 | Inspection | MPI and `mpi4py` are required for MPI-based operation. |
| C-003 | Inspection | Worker execution uses Python worker threads. |
| C-004 | Test | Setting `TORC_WORKERS=2` creates two worker threads per MPI process. |
| C-005 | Inspection | `TORC_STEALING` controls whether inter-process stealing is enabled by default. |
| C-006 | Inspection | Idle-yield timing variables are accepted as runtime configuration. |
| C-007 | Inspection | Callback examples specify one worker thread per MPI process where required. |
| C-008 | Inspection | Optional example dependencies are installed before those examples are run. |
| C-009 | Demonstration | Test execution can pass environment variables through `mpirun`. |
| C-010 | Inspection | License notice is present in test materials. |