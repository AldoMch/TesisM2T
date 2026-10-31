# Software Requirements Specification

## 1. Introduction

### Purpose
This SRS defines the checked software requirements for sample `s000068_a8b7a94e` based on the reviewed repository subset. It is intended to support downstream architecture generation, implementation alignment, and verification planning.

### Product scope
This specification covers the subset of repository behavior reflected in the reviewed build, test, telemetry, command, and CI workflow materials.

The product is a Core Flight System bundle composed of submodules that make up the cFS framework, including cFE, OSAL, PSP, framework applications, tools, and related components. This SRS does not attempt to specify the full framework architecture beyond the reviewed subset.

Covered behavior includes:
- cFS build preparation and installation using provided make assets
- execution of a runnable cFS target used in functional testing
- host-side command submission using `cmdUtil`
- telemetry enablement to a configured IP address
- CI-based changelog generation and repository format checking
- reusable CI workflow relationships described for cFS bundle and submodule workflows

### Intended audience
This document is intended for:
- integrators building or testing cFS from this repository subset
- operators or testers exercising telemetry and command flows
- maintainers reviewing CI and workflow-derived requirements
- architects deriving a conservative architecture view from the checked requirements

### References
- Repository: `nasa/cFS`
- Primary reviewed materials include repository README content and GitHub workflow definitions.

## 2. Overall Description

### Product perspective
The repository is a Core Flight System bundle containing framework components and related tooling. Within the reviewed subset, it is represented as:
- a buildable and testable cFS codebase
- a runnable target executable used for functional testing
- a host-side command utility for sending commands to the target
- telemetry interaction driven by operator-entered network address configuration
- CI workflows for changelog generation, format checking, and reusable workflow composition

The repository CI includes a reusable-workflow architecture. cFS bundle workflows relate to reusable workflows such as format check, static analysis, CodeQL, and reuse paths for cFS and submodules. Workflows using `workflow_call` are intended for reuse and composition across repositories.

Some build and test requirements in this SRS are derived from workflows labeled deprecated. Their current applicability should be revalidated against active workflows before relying on them as the sole implementation baseline.

### Product functions summary
The reviewed subset supports the following functions:
- prepare and install a cFS build using sample make assets and `make`
- execute functional tests against a running `core-cpu1`
- send host-originated commands to the running target with `cmdUtil`
- enable telemetry to a specified IP address and observe telemetry output
- document a walkthrough in which no-op commands are sent and command counters are expected to increase
- generate a categorized changelog artifact from CI workflow execution
- run automated format checking
- support reusable workflow invocation and composition

### User classes
- Developer or build user
- CI maintainer or workflow operator
- Functional tester
- Telemetry or ground-test operator

### Operating environment
Supported environments in the reviewed subset include:
- GitHub Actions runners, with runner usage attributed per workflow or job:
  - changelog and duplicate-check jobs use `ubuntu-latest`
  - reviewed build, run, functional-test, and format-checker jobs use `ubuntu-18.04`
- build variants: `debug` and `release`
- networked execution where the operator enters the IP address of the system executing cFS, including `127.0.0.1` for local execution

### Assumptions and dependencies
- Source checkout for reviewed build workflows includes Git submodules.
- Build preparation depends on provided `Makefile.sample` and `sample_defs` assets.
- Functional testing depends on the presence of `core-cpu1` and `../host/cmdUtil`.
- The repository documents related interfaces, libraries, and tools including SIL, ECI, `cFS_IO_LIB`, `cFS_LIB`, CCDD, Perfutils-java, and `gen_sch_tbl`.

## 3. External Interface Requirements

### User interfaces
- The system shall support telemetry enablement by allowing an operator to enter the IP address of the system executing cFS, including `127.0.0.1` for local execution.

### Software and API interfaces
- The repository shall support build preparation and installation through `make prep` and `make install`.
- The repository shall support host-side command transmission using `cmdUtil`.
- The repository shall document related interfaces, libraries, and tools including SIL, ECI, `cFS_IO_LIB`, `cFS_LIB`, CCDD, Perfutils-java, and `gen_sch_tbl`.
- CI workflows intended for reuse shall support invocation through `workflow_call`.

### Communication interfaces
- The system shall accept a configured IP address for telemetry connection to the system executing cFS.
- The running cFS target shall accept commands from the host utility during functional testing.

### Data exchange formats
- `cmdUtil` accepts command-line flags including `--pktid`, `--cmdcode`, `--endian`, and typed payload arguments such as `--uint32`, as shown in functional-test invocations. This does not define a complete command packet schema.
- Generated changelog content shall be organized under labeled sections for closed issues, breaking changes, enhancements, bugs, deprecated items, removed items, and security fixes.

## 4. Functional Requirements

| ID | Description | Trigger/Input | System behavior | Output | Priority | Verification |
|---|---|---|---|---|---|---|
| FR-001 | Build preparation and installation | A build user invokes repository build steps using the provided sample make assets. | The system shall support copying `Makefile.sample` to `Makefile`, copying `sample_defs`, running `make prep`, and running `make install`. | Prepared and installed build artifacts for the selected build type. | High | Test |
| FR-002 | Functional execution target | A tester starts functional testing. | The system shall provide a runnable `core-cpu1` executable for functional test execution. | Running cFS target process. | High | Demonstration |
| FR-003 | Host command submission | A tester invokes `cmdUtil` during functional testing. | The system shall accept commands from `cmdUtil` to the running cFS target. `cmdUtil` usage may include flags such as `--pktid`, `--cmdcode`, `--endian`, and typed payload arguments. | Command transmission to cFS for test actions. | High | Test |
| FR-004 | Telemetry enablement and observation | An operator enables telemetry and enters the IP address of the system executing cFS. | The system shall support telemetry connection to the entered IP address and permit observation of telemetry. | Visible telemetry data. | High | Demonstration |
| FR-005 | Documented no-op and counter observation flow | An operator follows the documented telemetry walkthrough after telemetry is enabled. | The README documents that no-op commands can be sent and command counter increments should be observable. | Documented observable telemetry behavior during the walkthrough. | Medium | Inspection and Demonstration |
| FR-006 | Changelog generation | A maintainer manually triggers the changelog workflow. | The system shall generate a changelog organized by configured labels for issues and changes, and upload the resulting changelog artifact. | Uploaded changelog artifact. | Medium | Test |

## 5. Non-Functional Requirements

| ID | Quality attribute | Requirement | Priority | Verification |
|---|---|---|---|---|
| NFR-001 | Portability | Workflow runner usage shall be attributed per workflow or job: changelog and duplicate-check jobs use `ubuntu-latest`, while the reviewed build, run, functional-test, and format-checker jobs use `ubuntu-18.04`. | Medium | Inspection |
| NFR-002 | Configuration compatibility | The repository shall support both `debug` and `release` build variants in the reviewed CI build and test workflows. | High | Test |
| NFR-003 | Execution control | The functional-test CI job shall be configured with a 15-minute timeout ceiling; jobs exceeding this ceiling are terminated by CI. | Medium | Inspection |
| NFR-004 | Maintainability | Repository validation shall include an automated format check on `push`, `pull_request`, and `workflow_call` events. | Medium | Inspection |
| NFR-005 | Reusability | CI workflows intended for reuse shall support composition through reusable workflow mechanisms such as `workflow_call`. | Medium | Inspection |

## 6. Data Requirements

| ID | Data item/entity | Requirement |
|---|---|---|
| DR-001 | Telemetry data | The system shall produce telemetry visible to an operator after telemetry is enabled to the configured IP address. |
| DR-002 | Documented observable counter data | The README describes command counters as observable telemetry data that should increase after sending no-op commands in the walkthrough flow. |
| DR-003 | `cmdUtil` command-line inputs | The `cmdUtil` host utility accepts command-line flags including `--pktid`, `--cmdcode`, `--endian`, and typed payload arguments such as `--uint32`, as shown in CI functional-test invocations. This does not define a complete command packet schema. |
| DR-004 | Changelog content categories | Changelog data shall be organized under the labels `Closed issues`, `Breaking changes`, `Implemented enhancements`, `Fixed bugs`, `Deprecated`, `Removed`, and `Security fixes`. |

## 7. System Constraints

| ID | Constraint |
|---|---|
| C-001 | Source checkout for reviewed build workflows is constrained to include Git submodules. |
| C-002 | Build preparation is constrained to use the provided `Makefile.sample` and `sample_defs` assets. |
| C-003 | Functional test execution is constrained to the presence of `core-cpu1` and the host utility `../host/cmdUtil`. |
| C-004 | Reviewed CI processes are constrained to GitHub Actions workflow execution. |
| C-005 | Some reviewed build and test behaviors are derived from workflows labeled deprecated and should be revalidated against currently active workflows before adoption as long-term baseline requirements. |

## 8. Verification and Acceptance Criteria

| Requirement ID | Verification method | Acceptance criterion |
|---|---|---|
| FR-001 | Test | A build run successfully performs the documented copy, `make prep`, and `make install` steps. |
| FR-002 | Demonstration | `core-cpu1` is startable in the functional test scenario. |
| FR-003 | Test | `cmdUtil` invocation is accepted by the running cFS target during testing. |
| FR-004 | Demonstration | After telemetry is enabled with the entered IP address, telemetry is visible. |
| FR-005 | Inspection and Demonstration | The documented walkthrough states that no-op commands can be sent and command counter increments should be observable after telemetry is enabled. |
| FR-006 | Test | Manual workflow trigger produces an uploaded changelog artifact with the configured categories. |
| NFR-001 | Inspection | Workflow definitions show the stated runner assignments per workflow or job. |
| NFR-002 | Test | CI matrix or workflow execution covers both `debug` and `release`. |
| NFR-003 | Inspection | Workflow definition shows a 15-minute timeout ceiling for the functional-test CI job. |
| NFR-004 | Inspection | Workflow definitions show format-check execution on `push`, `pull_request`, and `workflow_call`. |
| NFR-005 | Inspection | Workflow definitions show reusable workflow support through `workflow_call` or equivalent reuse configuration. |
