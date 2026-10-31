# Software Requirements Specification

## 1. Introduction

### Purpose
This SRS defines the software requirements for sample `s000050_275af3e0`, covering the repository’s supported fuzzing workflows, interfaces, data, constraints, and verification criteria.

### Product Scope
hAFL2 is a kAFL-based hypervisor fuzzing system. The primary supported scope includes fuzzing of the Hyper-V virtualization stack, especially the Hyper-V virtual switch (`vmswitch.sys`) path. The currently specified repository capabilities include:
- A standalone entry point for running `kAFL-Fuzzer` test suites
- A Linux userspace fuzzing workflow that packages target binaries into an `initrd`
- An embedded forkserver that maps kAFL hypercalls to AFL-style guest I/O
- Windows helper binaries used in the Hyper-V fuzzing workflow
- A harness-driver and crash-monitoring workflow used with child and root partition virtual machines

### Intended Audience
- Fuzzing operators using hAFL2 and kAFL workflows
- Developers maintaining test and launch workflows
- Integrators preparing Linux userspace or Windows Hyper-V fuzzing environments

### References
- Repository: `SafeBreach-Labs/hAFL2`
- Architecture documentation: `Architecture.png`
- Tutorial and workflow documentation: `tutorial.md`

## 2. Overall Description

### Product Perspective
hAFL2 is a hypervisor fuzzing platform built around kAFL-based workflows. The documented artifacts in scope include test-running utilities, Linux userspace launch scripts, Windows helper binaries, and supporting harness and crash-monitoring components. The Windows workflow operates across child and root partition virtual machines and targets the Hyper-V virtual switch path.

### Product Functions Summary
The system supports the following functions:
- Execute regular `kAFL-Fuzzer` test suites from a standalone script
- Launch selected Linux userspace binaries by packaging them into an `initrd`
- Use an embedded forkserver to translate kAFL hypercalls into AFL-style I/O within the guest
- Copy required shared libraries from the host into the `initrd`
- Provide Windows helper binaries where `packet_sender.exe` triggers a packet-sending IOCTL and `loader.exe` creates a fuzzing snapshot, loads, and executes `packet_sender.exe`
- Send fuzzing payloads from a child partition harness toward the root partition Hyper-V networking path
- Return crash-monitoring results from the root partition workflow to hAFL2

### User Classes
- Developers running or extending `kAFL-Fuzzer` tests
- Fuzzing users launching Linux userspace targets
- Windows Hyper-V fuzzing operators preparing harnesses, drivers, and VM configuration

### Operating Environment
- Python 3 for the standalone test entry point
- `pytest` for regular test execution
- `bash` for build and launch-related scripts
- Linux environments for userspace target packaging and launch workflows
- Windows environments for helper binaries, harness, crash monitoring, and VM-based fuzzing setup
- Root partition and child partition virtual machines for the Hyper-V fuzzing workflow

### Assumptions and Dependencies
- Linux userspace fuzzing assumes the target binary can be packaged into an `initrd`
- Shared libraries required by the target are available on the host for copying into the `initrd`
- Windows setup depends on compiling helper binaries and drivers and on Windows-build-specific offset configuration
- Hyper-V fuzzing depends on correct child partition and root partition VM setup
- The documented architecture and workflow assume VMBus or netvsc-related channels are available for the root-partition communication path

## 3. External Interface Requirements

### User Interfaces
- The system shall support command-line execution of the standalone test runner and associated fuzzing and build scripts.

### Software/API Interfaces
- The Linux userspace fuzzing workflow shall interface with guest execution through an embedded forkserver that maps kAFL hypercalls to AFL-style I/O.
- The Windows fuzzing workflow shall provide helper binaries that interact with the harness and snapshot-loading flow.
- The Windows Hyper-V fuzzing workflow shall support harness, crash-monitoring, and VM-based integration across child and root partitions.

### Communication Interfaces
- The Windows workflow shall support packet-sending through an IOCTL triggered by `packet_sender.exe`.
- The Windows Hyper-V fuzzing workflow shall support sending fuzzing payloads from the child partition harness to `VMSwitch` in the root partition.
- This communication path shall depend on netvsc or VMBus-related network channels.
- The crash-monitoring workflow shall communicate crash results back to hAFL2.

### Data Exchange Formats
- Linux launch workflows shall construct an `initrd` containing the selected target binary and required shared libraries.
- Deterministic mutation tests shall operate on mutable byte payloads and optional effector maps.
- Windows configuration shall include a build-specific offset value when required by the target Windows build.

## 4. Functional Requirements

| ID | Description | Trigger/Input | System Behavior | Output | Priority | Verification |
|---|---|---|---|---|---|---|
| FR-001 | Standalone test execution | User invokes `kAFL-Fuzzer/test.py` as a script. | The system shall run the random, deterministic, and havoc test routines and print start and completion status. | Test execution of the three suites and console status output. | High | Test |
| FR-002 | Linux userspace target packaging and launch | User selects a Linux userspace target binary and runs the provided launch scripts. | The system shall build an `initrd` containing the selected binary and use it for launch in the documented kAFL workflow. | A launchable `initrd`-based target execution workflow. | High | Demonstration |
| FR-003 | Guest-side forkserver I/O mapping | A userspace fuzzing target is launched through the provided workflow. | The embedded forkserver shall translate kAFL hypercalls into AFL-style guest I/O. | Observable fuzzing iteration or coverage feedback during target execution. | High | Demonstration |
| FR-004 | Linux shared-library packaging | A target binary requiring shared libraries is packaged for launch. | The system shall identify and copy required shared libraries from the host into the `initrd`. | `initrd` includes target dependencies needed for launch. | High | Inspection |
| FR-005 | Windows helper-binary roles | User compiles the fuzzing binaries from the repository. | The system shall provide `packet_sender.exe` for triggering the packet-sending IOCTL and `loader.exe` for creating a fuzzing snapshot, loading, and executing `packet_sender.exe`. | Executable binaries supporting the documented Windows fuzzing flow. | High | Demonstration |
| FR-006 | Child-to-root Hyper-V fuzzing path | The Windows Hyper-V fuzzing workflow is executed. | The system shall support sending fuzzing payloads from the child partition harness to the root partition `VMSwitch` path. | Fuzzing payloads reach the root partition networking target path. | High | Demonstration |
| FR-007 | Crash monitoring feedback | A root-partition crash occurs during the Windows fuzzing workflow. | The system shall provide crash-monitoring feedback from the root partition workflow back to hAFL2. | Crash status or equivalent monitoring result is returned to the fuzzing workflow. | Medium | Demonstration |

## 5. Non-Functional Requirements

| ID | Quality Attribute | Requirement | Priority | Verification |
|---|---|---|---|---|
| NFR-001 | Verifiability | The system shall support execution of regular `kAFL-Fuzzer` tests via `pytest` from the `kAFL-Fuzzer/` directory and via a standalone script entry point. | High | Test |
| NFR-002 | Data integrity | Deterministic mutation routines shall restore the original payload contents on exit, even when mutating the payload directly during processing. | High | Test |
| NFR-003 | Mutation correctness | Deterministic bitflip mutators shall produce outputs whose Hamming-distance change matches the mutator’s expected flipped-bit count under test. | High | Test |
| NFR-004 | Interoperability | The Windows fuzzing workflow shall operate across child partition and root partition virtual-machine roles. | High | Demonstration |
| NFR-005 | Configurability | The Windows workflow shall allow Windows-build-specific offset configuration when required for the target build. | Medium | Inspection |

## 6. Data Requirements

| ID | Data Requirement | Description |
|---|---|---|
| DR-001 | Target binary package | A selected Linux userspace target binary shall be packaged into an `initrd` for launch. |
| DR-002 | Shared library set | Required shared libraries for the target shall be copied from the host system into the `initrd`. |
| DR-003 | Mutation payload | Deterministic mutation processing shall operate on mutable payload data represented as byte arrays. |
| DR-004 | Effector map | Mutation processing may use an effector map composed of boolean values over payload length. |
| DR-005 | Windows offset value | For different Windows builds, the relevant offset shall be identified and updated in source before compilation when required. |
| DR-006 | Fuzzing payload | The Windows Hyper-V workflow shall transmit fuzzing payloads from the child partition toward the root partition target path. |
| DR-007 | Crash-monitoring result | The system shall handle crash status or equivalent monitoring output returned from the root partition workflow. |

## 7. System Constraints

| ID | Constraint | Type |
|---|---|---|
| C-001 | Use or redistribution shall comply with the repository-level BSD 3-Clause license and any applicable subfile license notices, including AGPL-3.0-or-later headers present in kAFL-derived files. | License |
| C-002 | Windows fuzzing binaries must be compiled by running `bash ./hAFL2/targets/windows_86_64/compile.sh`. | Build/Tooling |
| C-003 | The Windows harness and crash-monitoring drivers must be compiled with Visual Studio. | Build/Tooling |
| C-004 | For Windows builds different from the documented one, the operator must obtain the required offset and update the corresponding source value before compilation. | Platform compatibility |
| C-005 | Child Partition DSE must be disabled from an elevated command prompt, and the child partition VM must be restarted afterward. | Operational |
| C-006 | Child partition VM configuration steps require the child partition VM to be turned off before configuration begins. | Operational |

## 8. Verification and Acceptance Criteria

| Requirement ID | Verification Method | Acceptance Criteria |
|---|---|---|
| FR-001 | Test | Invoking the standalone script executes random, deterministic, and havoc tests and emits start and completion console messages. |
| FR-002 | Demonstration | Running the userspace launch workflow shows that the selected binary is packaged into an `initrd` and launched through the documented kAFL workflow. |
| FR-003 | Demonstration | A userspace target can launch and execute under the kAFL workflow with the forkserver active; guest-side I/O mapping is demonstrated by successful fuzzing iterations, coverage feedback, or equivalent runtime feedback. |
| FR-004 | Inspection | The produced `initrd` contains the target’s required shared libraries copied from the host. |
| FR-005 | Demonstration | Compiled Windows binaries exist and perform the documented roles of IOCTL triggering and snapshot loading/execution. |
| FR-006 | Demonstration | The Windows Hyper-V fuzzing workflow sends payloads from the child partition harness to the root partition `VMSwitch` path. |
| FR-007 | Demonstration | When a monitored crash condition occurs in the root partition workflow, crash status or equivalent monitoring output is returned to hAFL2. |
| NFR-001 | Test | Test execution is possible both through `pytest` in `kAFL-Fuzzer/` and through the standalone script. |
| NFR-002 | Test | After deterministic mutation routines return, the payload matches its original value. |
| NFR-003 | Test | Mutation outputs satisfy the expected Hamming-distance invariant for the relevant bitflip mutator. |
| NFR-004 | Demonstration | The Windows fuzzing workflow operates with distinct child partition and root partition roles. |
| NFR-005 | Inspection | A Windows-build-specific offset can be set in source prior to compilation when required. |
| DR-001 | Inspection | The launch artifact includes the selected target binary inside an `initrd`. |
| DR-002 | Inspection | The launch artifact includes required target shared libraries sourced from the host. |
| DR-003 | Test | Mutation tests accept and process byte-array payload objects. |
| DR-004 | Test | Mutation tests accept optional boolean effector maps sized to payload length. |
| DR-005 | Inspection | The Windows-source offset is set to the operator-identified value before compilation for the target Windows build when required. |
| DR-006 | Demonstration | A fuzzing payload is transmitted from the child partition workflow toward the root partition target path. |
| DR-007 | Demonstration | Crash-monitoring output is returned from the root partition workflow to the fuzzing controller. |
| C-001 | Inspection | Distributed use and redistribution materials comply with the repository-level license and applicable file-level license notices. |
| C-002 | Demonstration | The documented compile script is used to build the Windows fuzzing binaries. |
| C-003 | Demonstration | Visual Studio is used to build the Windows harness and crash-monitoring drivers. |
| C-004 | Inspection | A Windows-build-specific offset is identified and updated in source prior to compilation when required. |
| C-005 | Demonstration | DSE disablement is executed from an elevated command prompt and the child partition VM is restarted afterward. |
| C-006 | Demonstration | Configuration begins only while the child partition VM is powered off. |
