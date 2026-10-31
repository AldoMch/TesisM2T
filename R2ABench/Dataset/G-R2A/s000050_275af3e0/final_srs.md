# Software Requirements Specification

## 1. Introduction

### Purpose
This SRS defines evidence-backed requirements for the repository snapshot `SafeBreach-Labs/hAFL2` at commit `64e1bfab4a63a3515fcbbbfce2a5837a2c71bafa`. The scope supported by the evidence is the repository’s fuzzing support workflows for:
- `kAFL-Fuzzer` test execution
- Linux userspace fuzzing launch scripts
- Windows fuzzing helper binaries and setup steps

### Product Scope
Based on the evidence, the repository provides:
- A standalone entry point for running `kAFL-Fuzzer` test suites
- Sample scripts for launching Linux userspace binaries in kAFL via an `initrd`
- An embedded forkserver that maps kAFL hypercalls to AFL-style guest I/O
- Windows-target fuzzing binaries and a setup workflow involving harness and crash-monitoring drivers

### Intended Audience
- Fuzzing operators using kAFL/hAFL2 workflows
- Developers maintaining test and launch workflows
- Integrators preparing Linux userspace or Windows VM fuzzing environments

### References
- Repository: https://github.com/SafeBreach-Labs/hAFL2
- Snapshot: https://github.com/SafeBreach-Labs/hAFL2/tree/64e1bfab4a63a3515fcbbbfce2a5837a2c71bafa
- Evidence sources: `kAFL-Fuzzer/test.py`, `tests/user_bench/README.md`, `tutorial.md`, `kAFL-Fuzzer/tests/test_deterministic.py`

## 2. Overall Description

### Product Perspective
The evidenced component is a fuzzing support toolset rather than a standalone end-user application. It includes test-running utilities, Linux userspace launch scripts, and Windows-target build/setup artifacts.

### Product Functions Summary
- Execute regular `kAFL-Fuzzer` test suites from a standalone script.
- Launch selected Linux userspace binaries by packaging them into an `initrd`.
- Use an embedded forkserver to translate kAFL hypercalls into AFL-style I/O within the guest.
- Copy required shared libraries from the host into the `initrd`.
- Provide Windows helper binaries where `packet_sender.exe` triggers a packet-sending IOCTL and `loader.exe` creates a fuzzing snapshot, loads, and executes `packet_sender.exe`.

### User Classes
- Developers running or extending `kAFL-Fuzzer` tests
- Fuzzing users launching Linux userspace targets
- Windows fuzzing operators preparing harnesses, drivers, and VM configuration

### Operating Environment
- Python 3 is used for the standalone test entry point. `pytest` is used to execute regular tests. `bash` is used to compile fuzzing binaries. Evidence also references Visual Studio, IDA Pro, elevated Windows command prompts, and child/root partition VMs.  
Source: `E001`, `E003`, `E004`

### Assumptions and Dependencies
- Linux userspace fuzzing assumes the target binary can be packaged into an `initrd`.  
Source: `E002`
- Shared libraries required by the target are available on the host for copying into the `initrd`.  
Source: `E002`
- Windows setup depends on compiling helper binaries and drivers, and on Windows-build-specific offset configuration.  
Source: `E003`, `E004`

## 3. External Interface Requirements

### User Interfaces
- Command-line execution of the standalone test runner and fuzzing/build scripts is supported.  
Source: `E001`, `E003`

### Software/API Interfaces
- Linux userspace fuzzing interfaces with guest execution through an embedded forkserver that maps kAFL hypercalls to AFL-style I/O.  
Source: `E002`
- Windows fuzzing helpers interface with a packet-sending IOCTL and a fuzzing snapshot loader workflow.  
Source: `E003`

### Communication Interfaces
- In the Windows workflow, `packet_sender.exe` triggers packet-sending through an IOCTL.  
Source: `E003`

### Data Exchange Formats
- Linux launch workflows construct an `initrd` containing the selected target binary and required shared libraries.  
Source: `E002`
- Deterministic mutation tests operate on mutable byte payloads and optional effector maps.  
Source: `E005`, `E006`

## 4. Functional Requirements

| ID | Description | Trigger/Input | System Behavior | Output | Priority | Verification | Source Evidence |
|---|---|---|---|---|---|---|---|
| FR-001 | The system shall provide a standalone test entry point for `kAFL-Fuzzer` regular tests. | User invokes `kAFL-Fuzzer/test.py` as a script. | The system shall run the random, deterministic, and havoc test routines and print start and completion status. | Test execution of the three suites and console status output. | High | Test | `E001` |
| FR-002 | The Linux userspace fuzzing workflow shall package a selected target binary into an `initrd` and launch it in kAFL. | User selects a Linux userspace target binary and runs the provided launch scripts. | The system shall build an `initrd` containing the selected binary and use it for launch. | A launchable `initrd`-based target execution workflow. | High | Demonstration | `E002` |
| FR-003 | During Linux userspace fuzzing, the system shall map kAFL hypercalls to AFL-style I/O inside the guest. | A userspace fuzzing target is launched through the provided workflow. | The embedded forkserver shall translate kAFL hypercalls into AFL-style guest I/O. | Guest-side AFL-style I/O behavior during fuzzing. | High | Demonstration | `E002` |
| FR-004 | The Linux userspace fuzzing workflow shall automatically copy required shared libraries from the host system into the `initrd`. | A target binary requiring shared libraries is packaged for launch. | The system shall identify and copy required shared libraries from the host into the `initrd`. | `initrd` includes target dependencies needed for launch. | High | Inspection | `E002` |
| FR-005 | The Windows fuzzing workflow shall provide helper binaries with distinct execution roles. | User compiles the fuzzing binaries from the repository. | The system shall provide `packet_sender.exe` for triggering the packet-sending IOCTL and `loader.exe` for creating a fuzzing snapshot, loading, and executing `packet_sender.exe`. | Executable binaries supporting the documented Windows fuzzing flow. | High | Demonstration | `E003` |

## 5. Non-Functional Requirements

| ID | Quality Attribute | Requirement | Priority | Verification | Source Evidence | Evidence Type |
|---|---|---|---|---|---|---|
| NFR-001 | Verifiability | The system shall support execution of regular `kAFL-Fuzzer` tests via `pytest` from the `kAFL-Fuzzer/` directory and via a standalone script entry point. | High | Test | `E001` | explicit |
| NFR-002 | Data integrity | Deterministic mutation routines shall restore the original payload contents on exit, even when mutating the payload directly during processing. | High | Test | `E005` | explicit |
| NFR-003 | Mutation correctness | Deterministic bitflip mutators shall produce outputs whose Hamming-distance change matches the mutator’s expected flipped-bit count under test. | High | Test | `E005` | explicit |

## 6. Data Requirements

| ID | Data Requirement | Type | Description | Source Evidence |
|---|---|---|---|---|
| DR-001 | Target binary package | Input/Runtime artifact | A selected Linux userspace target binary shall be packaged into an `initrd` for launch. | `E002` |
| DR-002 | Shared library set | Dependency data | Required shared libraries for the target shall be copied from the host system into the `initrd`. | `E002` |
| DR-003 | Mutation payload | Input object | Deterministic mutation processing operates on mutable payload data represented as byte arrays. | `E005`, `E006` |
| DR-004 | Effector map | Optional control data | Mutation processing may use an effector map composed of boolean values over payload length. | `E005`, `E006` |
| DR-005 | Windows offset value | Configuration data | For different Windows builds, the relevant global-list offset must be identified and updated in source before compilation. | `E004` |

## 7. Constraints

| ID | Constraint | Type | Source Evidence |
|---|---|---|---|
| C-001 | The repository artifacts in evidence are licensed under `AGPL-3.0-or-later`. | License | `E001`, `E006` |
| C-002 | Windows fuzzing binaries must be compiled by running `bash ./hAFL2/targets/windows_86_64/compile.sh`. | Build/Tooling | `E003` |
| C-003 | The Windows harness and crash-monitoring drivers must be compiled with Visual Studio. | Build/Tooling | `E003` |
| C-004 | For Windows builds different from the documented one, the operator must obtain the required offset using IDA Pro and update the corresponding source value before compilation. | Platform compatibility | `E004` |
| C-005 | Child Partition DSE must be disabled from an elevated command prompt, and the child partition VM must be restarted afterward. | Operational | `E003` |
| C-006 | Child partition VM configuration steps require the child partition VM to be turned off before configuration begins. | Operational | `E004` |

## 8. Verification and Acceptance

| ID | Verification Method | Acceptance Criteria |
|---|---|---|
| FR-001 | Test | Invoking the standalone script executes random, deterministic, and havoc tests and emits start/completion console messages. |
| FR-002 | Demonstration | Running the userspace launch workflow shows that the selected binary is packaged into an `initrd` and launched through kAFL. |
| FR-003 | Demonstration | The userspace fuzzing workflow exhibits AFL-style I/O inside the guest via the embedded forkserver. |
| FR-004 | Inspection | The produced `initrd` contains the target’s required shared libraries copied from the host. |
| FR-005 | Demonstration | Compiled Windows binaries exist and perform the documented roles of IOCTL triggering and snapshot loading/execution. |
| NFR-001 | Test | Test execution is possible both through `pytest` in `kAFL-Fuzzer/` and through the standalone script. |
| NFR-002 | Test | After deterministic mutation routines return, the payload matches its original value. |
| NFR-003 | Test | Mutation outputs satisfy the expected Hamming-distance invariant for the relevant bitflip mutator. |
| DR-001 | Inspection | The launch artifact includes the selected target binary inside an `initrd`. |
| DR-002 | Inspection | The launch artifact includes required target shared libraries sourced from the host. |
| DR-003 | Test | Mutation tests accept and process byte-array payload objects. |
| DR-004 | Test | Mutation tests accept optional boolean effector maps sized to payload length. |
| DR-005 | Inspection | The Windows-source offset is set to the operator-identified value before compilation for the target Windows build. |
| C-001 | Inspection | Distributed artifacts retain `AGPL-3.0-or-later` licensing notices where evidenced. |
| C-002 | Demonstration | The documented compile script is used to build the Windows fuzzing binaries. |
| C-003 | Demonstration | Visual Studio is used to build the Windows harness and crash-monitoring drivers. |
| C-004 | Inspection | A Windows-build-specific offset is identified and updated in source prior to compilation when required. |
| C-005 | Demonstration | DSE disablement is executed from an elevated command prompt and the child partition VM is restarted. |
| C-006 | Demonstration | Configuration begins only while the child partition VM is powered off. |

## 9. Traceability Matrix

| ID | Requirement | Type | Source | Evidence Type | Verification | Confidence |
|---|---|---|---|---|---|---|
| FR-001 | Standalone entry point runs random, deterministic, and havoc tests. | Functional | `E001` | explicit | Test | High |
| FR-002 | Selected Linux userspace binary is packaged into an `initrd` and launched. | Functional | `E002` | explicit | Demonstration | High |
| FR-003 | Embedded forkserver maps kAFL hypercalls to AFL-style guest I/O. | Functional | `E002` | explicit | Demonstration | High |
| FR-004 | Required shared libraries are automatically copied from host into the `initrd`. | Functional | `E002` | explicit | Inspection | High |
| FR-005 | Windows helper binaries provide IOCTL-trigger and snapshot-load/execute roles. | Functional | `E003` | explicit | Demonstration | Medium |
| NFR-001 | Tests are executable by `pytest` and by standalone entry point. | Non-functional | `E001` | explicit | Test | High |
| NFR-002 | Deterministic mutation routines restore original payload contents on exit. | Non-functional | `E005` | explicit | Test | High |
| NFR-003 | Bitflip mutators maintain expected Hamming-distance behavior. | Non-functional | `E005` | explicit | Test | High |
| DR-001 | Target binary is stored in an `initrd` launch artifact. | Data | `E002` | explicit | Inspection | High |
| DR-002 | Required shared libraries are included as dependency data in the `initrd`. | Data | `E002` | explicit | Inspection | High |
| DR-003 | Mutation payload is represented as mutable byte-array data. | Data | `E005`, `E006` | explicit | Test | High |
| DR-004 | Effector map is optional boolean control data over payload length. | Data | `E005`, `E006` | explicit | Test | High |
| DR-005 | Windows-build-specific offset is configuration data that must be updated before compile. | Data | `E004` | explicit | Inspection | Medium |
| C-001 | Use is constrained by `AGPL-3.0-or-later` licensing. | Constraint | `E001`, `E006` | explicit | Inspection | High |
| C-002 | Windows fuzzing binaries are built via the documented shell script. | Constraint | `E003` | explicit | Demonstration | High |
| C-003 | Windows harness and crash-monitoring drivers require Visual Studio. | Constraint | `E003` | explicit | Demonstration | High |
| C-004 | Different Windows builds require IDA Pro-based offset discovery and source update. | Constraint | `E004` | explicit | Inspection | Medium |
| C-005 | DSE disablement and VM restart are required operational steps. | Constraint | `E003` | explicit | Demonstration | Medium |
| C-006 | Child partition VM must be off before configuration. | Constraint | `E004` | explicit | Demonstration | High |
