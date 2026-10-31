# Software Requirements Specification

## 1. Introduction

### Purpose
This SRS defines checked software requirements for TraceLeft. The specification is limited to repository-supported behavior for the TraceLeft library, probe-loading and event-delivery model, configuration-driven handler generation, and the reference CLI used to trace Linux processes.

### Product scope
TraceLeft is a Linux tracing framework composed of a reusable library and a reference command-line tool. It traces applications by installing Linux eBPF probes on function calls and delivering syscall, file, and network events for traced processes. The repository also supports configuration-driven generation of eBPF handler source code from event configuration metadata.

### Intended audience
This document is intended for:
- Maintainers of the TraceLeft library and CLI
- Architects deriving runtime structure and interfaces
- Integrators building tracing or auditing tools on TraceLeft
- Test engineers validating observable behavior

## 2. Overall Description

### Product perspective
TraceLeft is a Linux tracing framework composed of:
- A library that installs eBPF probes on Linux function calls
- A CLI entry point that executes commands, including a `trace` command
- A runtime architecture in which a main eBPF program attaches to `kprobe` and `kretprobe` hooks
- Program maps and return-program maps keyed by process context to select handler eBPF programs
- Handler eBPF programs that emit events to userspace through a perf-based event channel
- A common event header section used by the userspace tracer to dispatch received events

### Product functions summary
TraceLeft supports:
- Tracing Linux processes through a CLI command
- Installing Linux probes on APIs and internal functions
- Receiving syscall, file, and network events from traced processes
- Loading default handler probes and process-specific handler probes
- Selecting handler programs through handler maps
- Emitting dispatchable events from kernel-space handlers to the userspace tracer
- Generating eBPF handler source code from configuration metadata

### User classes
- CLI operators who invoke TraceLeft to trace processes
- Developers and integrators who embed TraceLeft in tracing or auditing tools
- Maintainers who define event configuration and generate handler code

### Operating environment
- Linux environments
- Linux kernels with support for eBPF, `kprobe`, and `kretprobe`
- Userspace environments capable of running the TraceLeft CLI and consuming tracer events

### Assumptions and dependencies
- TraceLeft depends on Linux eBPF facilities and probe support in the target kernel.
- The implementation depends on `gobpf`.
- Handler integration depends on documented naming rules for handler maps and handler probes.
- Configuration-driven generation depends on event configuration metadata being available in the expected schema.

## 3. External Interface Requirements

### User interfaces
- The system shall provide a command-line interface through an executable entry point.
- The CLI shall provide a `trace` command for tracing processes.

### Software and API interfaces
- The library shall interface with Linux eBPF and `kprobe`/`kretprobe` facilities to install probes on function calls.
- The probe subsystem shall load default and process-specific handler probes.
- The probe loader shall use documented naming schemes for handler maps and handler probes.
- The generator subsystem shall read event configuration metadata and generate eBPF handler source code.

### Communication interfaces
- Kernel-space handler programs shall deliver events to the userspace tracer through a perf-based event channel.
- Emitted events shall contain a common leading section so the userspace tracer can dispatch them.

### Data exchange formats
- Event data shall begin with a common header section used for dispatching.
- Event configuration metadata shall support argument fields including `position`, `type`, `name`, `suffix`, and `hash_func`.
- CLI trace command inputs shall be parsed into an event registration structure containing program and process selection data.

## 4. Functional Requirements

### FR-001 CLI entry point
The system shall provide a CLI entry point that executes TraceLeft commands.

Verification method: Demonstration  
Acceptance criteria:
- Invoking the CLI executable starts command handling.
- The executable dispatches to registered commands.

### FR-002 Trace command
The system shall provide a `trace` CLI command for tracing processes.

Verification method: Demonstration  
Acceptance criteria:
- Invoking the `trace` command starts the trace command flow.
- The command accepts process-tracing inputs and initiates tracing behavior or performs input validation.

### FR-003 Probe installation
The system shall install Linux eBPF probes on function calls, including APIs and internal functions, for traced applications.

Verification method: Test  
Acceptance criteria:
- Starting a tracing session activates probe installation on the target Linux environment.
- Installed probes attach through Linux probe facilities used by the product.

### FR-004 Event capture
The system shall receive syscall, file, and network events for a traced process.

Verification method: Test  
Acceptance criteria:
- Syscall activity in a traced process produces trace events.
- File activity in a traced process produces trace events.
- Network activity in a traced process produces trace events.

### FR-005 Configuration-driven handler generation
The system shall support configuration-driven handler generation by reading Proto/JSON event configuration and generating eBPF handler source code for configured events and arguments.

Verification method: Test  
Acceptance criteria:
- Given an event configuration containing event argument metadata, the generator reads the configuration.
- The generator produces handler source code for the configured events and arguments.

### FR-006 Handler loading
The system shall load default handler probes and process-specific handler probes.

Verification method: Test  
Acceptance criteria:
- When probe loading is initiated, default handler probes are loaded.
- When process-specific handlers are available, those handlers are also loaded for the trace session.

### FR-007 No-op behavior for missing handler
If no handler probe is set for a trace probe, the trace probe shall perform no handler action and return `0`.

Verification method: Test  
Acceptance criteria:
- When a trace probe is triggered without a configured handler, no handler logic is invoked.
- The trace probe returns `0`.

### FR-008 Event delivery and dispatch format
Handler eBPF programs shall emit events through the perf-based event channel, and each event shall begin with the common event section that enables userspace tracer dispatch.

Verification method: Test  
Acceptance criteria:
- A handler program writes event output to the perf-based event channel.
- Each emitted event begins with the common leading section required for dispatch.
- The userspace tracer can dispatch received events using that common section.

### FR-009 Handler naming scheme
The probe loader shall use documented handler naming schemes:
- Handler maps shall follow `handle_NAME_progs` and `handle_NAME_progs_ret`
- Handler probes shall follow `kprobe/handle_NAME` and `kretprobe/handle_NAME`
- `NAME` shall identify the traced function

Verification method: Inspection  
Acceptance criteria:
- Probe-loading logic recognizes the documented handler map names.
- Probe-loading logic recognizes the documented handler probe names.
- The corresponding handler map is updated based on the traced function name.

## 5. Non-Functional Requirements

### NFR-001 Platform targeting
TraceLeft shall target Linux environments with kernel support for eBPF, `kprobe`, and `kretprobe`. The documented tested environment is Linux kernel v4.11+ with such support.

Verification method: Inspection  
Acceptance criteria:
- Product documentation identifies Linux with eBPF, `kprobe`, and `kretprobe` support as the target environment.
- The documented tested environment includes Linux kernel v4.11+ with the required probe support.

### NFR-002 Event interoperability
All emitted events shall start with the common event section required by the userspace tracer for dispatch.

Verification method: Test  
Acceptance criteria:
- Emitted event records contain the common leading section.
- Event consumers can dispatch records based on that section.

### NFR-003 Technology compatibility
The implementation shall remain compatible with the `gobpf`-based integration used by the product.

Verification method: Inspection  
Acceptance criteria:
- Repository implementation uses `gobpf` as the eBPF integration technology.
- Interfaces and build assumptions remain consistent with that dependency.

### NFR-004 Configurability
The system shall support configuration-driven generation of tracing handlers from structured event metadata rather than requiring per-handler hardcoding.

Verification method: Test  
Acceptance criteria:
- Structured event metadata can be supplied to the generator.
- Handler source generation reflects the supplied configuration.

## 6. Data Requirements

### DR-001 Trace event common section
The system shall define a common leading section for emitted trace events so the userspace tracer can dispatch them.

### DR-002 Event delivery channel
The system shall use a perf-based event channel to transfer handler-generated events from kernel space to userspace.

### DR-003 Event argument metadata
The system shall support event argument metadata fields including:
- `position`
- `type`
- `name`
- `suffix`
- `hash_func`

### DR-004 CLI event registration structure
CLI trace command arguments shall be parsed into an event registration structure containing:
- `ProgramID`
- `Pids`
- `ELFPath`

This structure shall be used by the trace command to register handler programs for selected program IDs and process IDs.

## 7. System Constraints

### C-001 Platform constraint
The product is constrained to Linux target environments.

### C-002 Kernel capability constraint
The product is constrained by the availability of kernel support for eBPF, `kprobe`, and `kretprobe`.

### C-003 Technology constraint
The implementation is constrained to the `gobpf`-based integration used by the product.

### C-004 Handler naming constraint
Handler integration is constrained by the documented naming rules:
- Handler maps use `handle_NAME_progs` and `handle_NAME_progs_ret`
- Handler probes use `kprobe/handle_NAME` and `kretprobe/handle_NAME`

## 8. Verification and Acceptance Criteria

| Requirement ID | Verification method | Acceptance criteria |
|---|---|---|
| FR-001 | Demonstration | Invoking the CLI executable starts command handling and command dispatch. |
| FR-002 | Demonstration | Invoking `trace` starts the trace command flow for process tracing or input validation. |
| FR-003 | Test | A tracing session installs Linux probes on target function calls. |
| FR-004 | Test | Traced syscall, file, and network activity produces trace events. |
| FR-005 | Test | Given Proto/JSON event configuration with argument metadata, the generator reads the configuration and produces handler source code. |
| FR-006 | Test | Probe loading installs default handlers and available process-specific handlers. |
| FR-007 | Test | A trace probe without a configured handler performs no handler action and returns `0`. |
| FR-008 | Test | Handler programs emit events through the perf-based channel, and each event begins with the common dispatch section. |
| FR-009 | Inspection | Probe-loading logic applies the documented handler map and handler probe naming rules. |
| NFR-001 | Inspection | Documentation identifies Linux with eBPF, `kprobe`, and `kretprobe` support as the target environment and documents testing on Linux kernel v4.11+. |
| NFR-002 | Test | Event records are dispatchable because the common section is present first. |
| NFR-003 | Inspection | Implementation artifacts remain consistent with `gobpf` usage. |
| NFR-004 | Test | Structured event metadata drives handler source generation without per-handler hardcoding. |
| DR-001 | Inspection | A common leading event section is defined for emitted trace events. |
| DR-002 | Inspection | Event delivery from handlers to userspace uses the perf-based channel. |
| DR-003 | Inspection | Event metadata definitions include `position`, `type`, `name`, `suffix`, and `hash_func`. |
| DR-004 | Inspection | CLI arguments are parsed into a structure containing `ProgramID`, `Pids`, and `ELFPath`, and that structure is used by the trace command for handler registration. |
| C-001 | Inspection | Deployment target is Linux. |
| C-002 | Inspection | Operation depends on kernel support for eBPF, `kprobe`, and `kretprobe`. |
| C-003 | Inspection | Implementation remains based on `gobpf`. |
| C-004 | Inspection | Handler integration follows the documented naming rules for maps and probes. |
