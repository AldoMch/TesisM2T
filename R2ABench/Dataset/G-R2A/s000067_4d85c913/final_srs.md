# Software Requirements Specification

## 1. Introduction

### Purpose
This SRS defines evidence-backed requirements for TraceLeft at commit `890e67e2fc1ea0dcbdcb5164b665d6be245e5464`. The scope covers the TraceLeft library and its reference CLI for tracing Linux processes through eBPF and Kprobe-based instrumentation. Sources are limited to the repository evidence pack.

### Product scope
TraceLeft is a library and a small CLI tool that traces applications by installing Linux eBPF probes on function calls to receive callbacks for syscall, file, and network events from traced processes. It is positioned as a framework for configuration-driven system auditing and application tracing, including network and syscall monitoring. [E002][E006]

### Intended audience
This document is intended for:
- Integrators using the TraceLeft library in tracing or auditing tools.
- Operators using the CLI reference implementation.
- Maintainers validating externally observable behavior and interfaces.

### References
- Repository: `ShiftLeftSecurity/traceleft`
- Commit: `890e67e2fc1ea0dcbdcb5164b665d6be245e5464`
- Repository URL: https://github.com/ShiftLeftSecurity/traceleft
- Evidence sources: [E001], [E002], [E003], [E004], [E005], [E006]

## 2. Overall Description

### Product perspective
TraceLeft is a Linux tracing framework composed of:
- A library that installs eBPF and Kprobe/Kretprobe-based probes on Linux function calls. [E002][E006]
- A CLI entry point that executes command handlers, including a `trace` command for tracing processes. [E003][E004]
- A probe/handler model in which trace probes tail-call handler probes, and handlers emit events through a shared event map with a common event section for dispatching. [E001]

### Product functions summary
TraceLeft provides these supported functions:
- Trace Linux processes through a CLI command. [E004]
- Install probes on Linux APIs and internal functions. [E002][E006]
- Receive callbacks for syscall, file, and network events of a traced process. [E002][E006]
- Support configuration-driven tracing/auditing use cases. [E002][E006]
- Load default and process-specific handler probes. [E001]
- Emit events with a common header section so the tracer can dispatch them. [E001]

### User classes
- CLI operators who invoke TraceLeft to trace processes. [E004]
- Developers/integrators who use the library/framework to build system auditing or application tracing tools. [E002][E006]

### Operating environment
- Linux systems. [E002][E006]
- Kernel versions with eBPF support for Kprobes and Kretprobes. [E002][E006]

### Assumptions and dependencies
- TraceLeft depends on Linux eBPF, Kprobes, and Kretprobes support in the target kernel. [E002][E006]
- The implementation is built using `gobpf`. [E002][E006]
- Handler probes are expected to follow naming schemes used by the probe loader for handler-map updates. [E001]

## 3. External Interface Requirements

### User interfaces
- A command-line interface shall be provided through the executable entry point. [E003]
- The CLI shall provide a `trace` command whose purpose is to trace processes. [E004]

### Software/API interfaces
- The library shall interface with Linux eBPF and Kprobe/Kretprobe facilities to install probes on function calls. [E002][E006]
- The probe subsystem shall load default and process-specific handler probes. [E001]
- Handler probes shall emit events through a shared event map used by the tracer. [E001]

### Communication interfaces
- Kernel-to-user-space event delivery is supported through the shared event map used by handlers to send events to the tracer. [E001]

### Data exchange formats
- Event data shall begin with a common section used for event dispatching. [E001]
- Configuration data includes event argument metadata fields `position`, `type`, `name`, `suffix`, and `hash_func` in generated protobuf-backed structures. [E005]

## 4. Functional Requirements

| ID | Requirement | Trigger/Input | System Behavior | Output | Priority | Verification | Source Evidence |
|---|---|---|---|---|---|---|---|
| FR-001 | The system shall provide a CLI entry point that executes TraceLeft commands. | User invokes the CLI executable. | The executable shall start the command dispatcher. | Command processing begins. | High | Demonstration | E003 |
| FR-002 | The system shall provide a `trace` CLI command for tracing processes. | User invokes the `trace` command. | The command shall initiate process tracing behavior. | Process tracing session starts or command validation is performed. | High | Demonstration | E004 |
| FR-003 | The system shall install Linux eBPF probes on function calls, including APIs and internal functions, for traced applications. | A tracing session is started for a target process/application. | The system shall use eBPF with Kprobes to instrument relevant Linux function calls. | Probes become active for the traced process. | High | Test | E002, E006 |
| FR-004 | The system shall receive callbacks for syscall, file, and network events of a traced process. | Instrumented syscall, file, or network activity occurs in a traced process. | The system shall capture the callback/event generated by the installed probes. | Trace event data is made available to the tracer. | High | Test | E002, E006 |
| FR-005 | The system shall support configuration-driven tracing/auditing use cases. | Integrator supplies tracing configuration to build an auditing or tracing tool. | The framework shall operate as a basis for configuration-driven system auditing or application tracing. | A configured tracing/auditing workflow can be built on the library. | Medium | Inspection | E002, E006 |
| FR-006 | The system shall load default handler probes and process-specific handler probes. | Probe loading is initiated for a traced process. | The probe loader shall load both default handlers and process-specific handlers when available. | Appropriate handler probes are installed for the trace session. | High | Test | E001 |
| FR-007 | If no handler probe is set for a trace probe, the trace probe shall perform no handler action and return `0`. | A trace probe is triggered without a configured handler probe. | The trace probe shall not invoke handler logic and shall return `0`. | No handler event is emitted for that probe invocation. | Medium | Test | E001 |
| FR-008 | Handler probes shall send events through the shared event map, and each event shall begin with a common section that enables tracer dispatch. | A handler probe emits an event. | The handler shall write the event to the shared event map and include the common event section first. | The tracer receives dispatchable event data. | High | Test | E001 |
| FR-009 | The probe loader shall use handler-probe naming conventions to determine which handler map to update. | Handler probes are loaded. | The system shall interpret kprobe/kretprobe handler names according to the documented naming scheme. | The corresponding handler map is updated for the traced function. | Medium | Inspection | E001 |

## 5. Non-Functional Requirements

| ID | Requirement | Quality Attribute | Statement | Priority | Verification | Source Evidence | Confidence |
|---|---|---|---|---|---|---|---|
| NFR-001 | The system shall operate only on Linux environments whose kernels support eBPF Kprobes and Kretprobes. | Compatibility | TraceLeft shall require Linux kernel support for eBPF, Kprobes, and Kretprobes. | High | Inspection | E002, E006 | Explicit |
| NFR-002 | The system shall maintain a dispatchable event structure by placing a common section at the start of each emitted event. | Interoperability | All emitted events shall start with the common section required by the tracer for dispatch. | High | Test | E001 | Explicit |
| NFR-003 | The system should be usable across kernel versions that provide the required eBPF probe support. | Portability | TraceLeft has been tested on kernel versions with eBPF support for Kprobes and Kretprobes. | Medium | Analysis | E002, E006 | Explicit |
| NFR-004 | The system should support maintainable extension through configuration-driven tracing rather than per-tool hardcoding. | Maintainability | The framework should allow tracing/auditing tools to be built from configuration-driven behavior. | Medium | Inspection | E002, E006 | Inferred |

## 6. Data Requirements

| ID | Data Item | Description | Source/Consumer | Constraints | Source Evidence |
|---|---|---|---|---|---|
| DR-001 | Trace event common section | Common leading section present in all emitted events to enable dispatching. | Produced by handler probes; consumed by tracer. | Must be present at the start of every event. | E001 |
| DR-002 | Shared event map | Shared map used by handler probes to send events. | Produced by handler probes; consumed by tracer. | Single shared event channel for handler output. | E001 |
| DR-003 | Event argument metadata | Configuration-backed event argument fields include `position`, `type`, `name`, `suffix`, and `hash_func`. | Defined in generated configuration structures. | Field names and types follow protobuf-generated schema. | E005 |
| DR-004 | Trace command event selection data | CLI-side event structure includes `ProgramID`, `Pids`, and `ELFPath`. | Used by CLI tracing flow. | Structure fields are present in the CLI event model. | E004 |

## 7. Constraints

| ID | Constraint | Type | Source Evidence |
|---|---|---|---|
| C-001 | The product is constrained to Linux environments. | Platform | E002, E006 |
| C-002 | The product requires kernel support for eBPF Kprobes and Kretprobes. | Technical | E002, E006 |
| C-003 | The implementation is built using `gobpf`. | Technology | E002, E006 |
| C-004 | Handler probe integration is constrained by documented naming conventions used by the probe loader. | Integration | E001 |

## 8. Verification and Acceptance

| Requirement ID | Verification Method | Acceptance Basis |
|---|---|---|
| FR-001 | Demonstration | Invoking the CLI executable starts command handling. |
| FR-002 | Demonstration | Invoking `trace` starts the trace command flow for processes. |
| FR-003 | Test | A trace session activates eBPF/Kprobe instrumentation on Linux function calls. |
| FR-004 | Test | Syscall, file, and network activity from a traced process produces callbacks/events. |
| FR-005 | Inspection | Repository evidence shows the framework is intended for configuration-driven auditing/tracing use. |
| FR-006 | Test | Probe loading installs default and process-specific handlers when applicable. |
| FR-007 | Test | A trace probe without a configured handler returns `0` and emits no handler action. |
| FR-008 | Test | Handler output is sent through the shared event map and contains the common event section first. |
| FR-009 | Inspection | Handler naming scheme determines handler-map updates as documented. |
| NFR-001 | Inspection | Deployment target is Linux with required kernel probe support. |
| NFR-002 | Test | Event records are dispatchable because the common section is present first. |
| NFR-003 | Analysis | Supported kernels are limited to those with the required eBPF/Kprobe features. |
| NFR-004 | Inspection | Configuration-driven positioning is documented in repository evidence. |

## 9. Traceability Matrix

| ID | Requirement | Type | Source | Evidence Type | Verification | Confidence |
|---|---|---|---|---|---|---|
| FR-001 | Provide a CLI entry point that executes commands. | Functional | E003 | Explicit | Demonstration | High |
| FR-002 | Provide a `trace` CLI command for tracing processes. | Functional | E004 | Explicit | Demonstration | High |
| FR-003 | Install eBPF probes on Linux APIs/internal functions. | Functional | E002, E006 | Explicit | Test | High |
| FR-004 | Receive syscall, file, and network event callbacks for traced processes. | Functional | E002, E006 | Explicit | Test | High |
| FR-005 | Support configuration-driven tracing/auditing use cases. | Functional | E002, E006 | Explicit | Inspection | Medium |
| FR-006 | Load default and process-specific handler probes. | Functional | E001 | Explicit | Test | High |
| FR-007 | Return `0` and do nothing when no handler probe is set. | Functional | E001 | Explicit | Test | High |
| FR-008 | Send events through a shared event map with a common dispatch section first. | Functional | E001 | Explicit | Test | High |
| FR-009 | Use handler naming conventions to update the correct handler map. | Functional | E001 | Explicit | Inspection | Medium |
| NFR-001 | Operate only on Linux kernels with eBPF/Kprobe/Kretprobe support. | Non-functional | E002, E006 | Explicit | Inspection | High |
| NFR-002 | Preserve dispatchable event structure via a common leading event section. | Non-functional | E001 | Explicit | Test | High |
| NFR-003 | Be usable on kernel versions that provide required probe support. | Non-functional | E002, E006 | Explicit | Analysis | Medium |
| NFR-004 | Support maintainable configuration-driven extension. | Non-functional | E002, E006 | Inferred | Inspection | Low |
