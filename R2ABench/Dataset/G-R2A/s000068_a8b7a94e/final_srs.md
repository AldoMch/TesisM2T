# Software Requirements Specification (SRS)

Repository: nasa/cFS  
Repository URL: https://github.com/nasa/cFS  
Commit: `8053f8c655a6ef9f32ce1f6f6db5157cad7931b0`

## 1. Introduction

### 1.1 Purpose
This SRS defines repository-specific requirements evidenced from the available README and GitHub workflow materials for `nasa/cFS`. The scope is limited to documented build/test workflows, documented telemetry interaction, and identified external integration points.

### 1.2 Product scope
Based on the evidence, this repository provides:
- cFS build and test workflows using `make`
- a runnable cFS target executable (`core-cpu1`) used in functional testing
- a host-side command utility (`cmdUtil`) used to send commands
- telemetry interaction that can be enabled against a specified IP address
- documented related interfaces, libraries, and tools

### 1.3 Intended audience
- Integrators building or testing cFS from this repository
- Operators or testers exercising telemetry and command paths
- Maintainers reviewing repository acceptance criteria
- Tooling/CI engineers consuming the repository workflows

### 1.4 References
- Repository README.md — evidence IDs: E003, E004
- GitHub workflow `.github/workflows/build-cfs-deprecated.yml` — evidence IDs: E002, E006
- GitHub workflow `.github/workflows/changelog.yml` — evidence ID: E001
- GitHub workflow `.github/workflows/format-check.yml` — evidence ID: E005

## 2. Overall Description

### 2.1 Product perspective
The repository is evidenced as a buildable and testable cFS codebase integrated with GitHub Actions workflows. It supports local or CI-driven execution, host-to-target command interaction, and telemetry observation.

### 2.2 Product functions summary
- Prepare and install a cFS build using sample make assets
- Execute functional tests against a running `core-cpu1`
- Allow telemetry enablement to a configured IP address
- Allow sending commands such as no-ops and observing command counter increments
- Generate a categorized changelog artifact from repository history/issues metadata

### 2.3 User classes
- Developer/build user
- CI operator/maintainer
- Functional tester
- Telemetry/ground test user

### 2.4 Operating environment
Evidence supports the following environments:
- GitHub Actions runners on `ubuntu-latest` and `ubuntu-18.04` (E001, E005, E006)
- Build variants: `debug` and `release` (E002, E006)
- Networked execution where a user enters the IP address of the system executing cFS, including `127.0.0.1` for local execution (E004)

### 2.5 Assumptions and dependencies
- Source checkout includes Git submodules (E002)
- Build preparation depends on provided `Makefile.sample` and `sample_defs` assets (E002)
- Functional testing depends on the presence of `core-cpu1` and `../host/cmdUtil` (E006)
- Related external elements are documented, including SIL, ECI, `cFS_IO_LIB`, `cFS_LIB`, CCDD, Perfutils-java, and `gen_sch_tbl` (E003)

## 3. External Interface Requirements

### 3.1 User interfaces
| Interface | Requirement | Evidence |
|---|---|---|
| Telemetry enablement UI | The system documentation shall support a user flow in which telemetry is enabled and the IP address of the system executing cFS is entered, including `127.0.0.1` for local execution. | E004 |

### 3.2 Software/API interfaces
| Interface | Requirement | Evidence |
|---|---|---|
| Build interface | The repository shall support build preparation and installation through `make prep` and `make install`. | E002 |
| Host command interface | The repository shall support host-side command transmission using `cmdUtil` with packet and command parameters. | E006 |
| External related interfaces | The repository shall document related interfaces/libraries/tools including SIL, ECI, `cFS_IO_LIB`, `cFS_LIB`, CCDD, Perfutils-java, and `gen_sch_tbl`. | E003 |

### 3.3 Communication interfaces
| Interface | Requirement | Evidence |
|---|---|---|
| Telemetry over IP | The system shall accept a configured IP address for telemetry connection to the system executing cFS. | E004 |
| Command path | The system shall accept command packets from the host utility during functional testing. | E006 |

### 3.4 Data exchange formats
| Format | Requirement | Evidence |
|---|---|---|
| Command-line command packet fields | The host command interface shall accept parameters including `pktid`, `cmdcode`, `endian`, and `uint32` values. | E006 |
| Changelog sections | Generated changelog content shall categorize entries under labeled sections for closed issues, breaking changes, enhancements, bugs, deprecated items, removed items, and security fixes. | E001 |

## 4. Functional Requirements

| ID | Description | Trigger/Input | System Behavior | Output | Priority | Verification | Source Evidence |
|---|---|---|---|---|---|---|---|
| FR-001 | Build preparation and installation | A build user invokes repository build steps using the provided sample make assets. | The system shall support copying `Makefile.sample` to `Makefile`, copying `sample_defs`, running `make prep`, and running `make install`. | Prepared and installed build artifacts for the selected build type. | High | Test | E002 |
| FR-002 | Functional execution target | A tester starts functional testing. | The system shall provide a runnable `core-cpu1` executable for functional test execution. | Running cFS target process. | High | Demonstration | E006 |
| FR-003 | Host command submission | A tester invokes `cmdUtil` with packet and command parameters during functional testing. | The system shall accept commands from `cmdUtil` to the running cFS target. | Command transmission to cFS for test actions. | High | Test | E006 |
| FR-004 | Telemetry enablement and observation | A user selects telemetry enablement and enters the IP address of the system executing cFS. | The system shall support telemetry connection to the entered IP address and permit observation of telemetry. | Visible telemetry data. | High | Demonstration | E004 |
| FR-005 | No-op command response visibility | A user sends no-op commands after telemetry is enabled. | The system shall allow no-op commands to be sent and shall expose command counter increments observable by the user. | Incremented command counters observable with telemetry. | High | Demonstration | E004 |
| FR-006 | Changelog generation | A maintainer manually triggers the changelog workflow. | The system shall generate a changelog organized by configured labels for issues and changes, and upload the resulting changelog artifact. | Uploaded changelog artifact. | Medium | Test | E001 |

## 5. Non-Functional Requirements

| ID | Quality Attribute | Requirement | Priority | Verification | Evidence Type | Source Evidence |
|---|---|---|---|---|---|---|
| NFR-001 | Portability | The repository build and test workflows shall execute on Ubuntu-based GitHub Actions runners, specifically `ubuntu-latest` and `ubuntu-18.04` as used in the evidence. | High | Inspection | explicit | E001, E005, E006 |
| NFR-002 | Configuration compatibility | The repository shall support both `debug` and `release` build variants in its evidenced CI build and test workflows. | High | Test | explicit | E002, E006 |
| NFR-003 | Test boundedness | The functional test workflow shall complete within a 15-minute CI timeout when executed in the evidenced deprecated functional test job. | Medium | Test | explicit | E006 |
| NFR-004 | Maintainability | Repository validation shall include an automated format check on `push`, `pull_request`, and `workflow_call` events. | Medium | Inspection | explicit | E005 |

## 6. Data Requirements

| ID | Data Requirement | Type | Details | Source Evidence |
|---|---|---|---|---|
| DR-001 | Telemetry data | Output data | The system shall produce telemetry visible to a user after telemetry is enabled to the configured IP address. | E004 |
| DR-002 | Command counter data | Output data | The system shall expose command counters whose increments can be observed after sending no-op commands. | E004 |
| DR-003 | Command packet parameters | Input data | Host command submission shall include packet-oriented parameters such as `pktid`, `cmdcode`, `endian`, and `uint32` fields. | E006 |
| DR-004 | Changelog content categories | Generated data | Changelog data shall be organized under the labels `Closed issues`, `Breaking changes`, `Implemented enhancements`, `Fixed bugs`, `Deprecated`, `Removed`, and `Security fixes`. | E001 |

## 7. Constraints

| ID | Constraint | Source Evidence |
|---|---|---|
| C-001 | Source checkout for build workflows is constrained to include Git submodules. | E002 |
| C-002 | Build preparation is constrained to use the provided `Makefile.sample` and `sample_defs` assets. | E002 |
| C-003 | Functional test execution is constrained to the presence of `core-cpu1` and the host utility `../host/cmdUtil`. | E006 |
| C-004 | Repository CI processes are constrained to GitHub Actions workflow execution. | E001, E005, E006 |

## 8. Verification and Acceptance

| Requirement ID | Verification Method | Acceptance Basis |
|---|---|---|
| FR-001 | Test | A build run successfully performs the evidenced copy, `make prep`, and `make install` steps. |
| FR-002 | Demonstration | `core-cpu1` is startable in the functional test scenario. |
| FR-003 | Test | `cmdUtil` invocation is accepted by the running cFS target during testing. |
| FR-004 | Demonstration | After telemetry is enabled and the IP address is entered, telemetry is visible. |
| FR-005 | Demonstration | Sending no-ops results in observable command counter increments. |
| FR-006 | Test | Manual workflow trigger produces an uploaded changelog artifact with the configured categories. |
| NFR-001 | Inspection | Workflow definitions show Ubuntu runner use as specified. |
| NFR-002 | Test | CI matrix execution covers both `debug` and `release`. |
| NFR-003 | Test | Functional test job is configured and observed within a 15-minute timeout bound. |
| NFR-004 | Inspection | Workflow definitions show format-check execution on the stated events. |

## 9. Traceability Matrix

| ID | Requirement | Type | Source | Evidence Type | Verification | Confidence |
|---|---|---|---|---|---|---|
| FR-001 | Support build preparation and installation via sample make assets and `make` steps | Functional | E002 | explicit | Test | High |
| FR-002 | Provide runnable `core-cpu1` for functional testing | Functional | E006 | explicit | Demonstration | Medium |
| FR-003 | Accept host commands via `cmdUtil` during functional testing | Functional | E006 | explicit | Test | Medium |
| FR-004 | Support telemetry enablement to a configured IP address and telemetry visibility | Functional | E004 | explicit | Demonstration | High |
| FR-005 | Allow no-op commands and observable command counter increments | Functional | E004 | explicit | Demonstration | High |
| FR-006 | Generate and upload categorized changelog artifact on manual trigger | Functional | E001 | explicit | Test | High |
| NFR-001 | Execute evidenced workflows on Ubuntu GitHub Actions runners | Non-functional | E001, E005, E006 | explicit | Inspection | High |
| NFR-002 | Support `debug` and `release` build variants | Non-functional | E002, E006 | explicit | Test | High |
| NFR-003 | Bound functional test job to 15 minutes | Non-functional | E006 | explicit | Test | Medium |
| NFR-004 | Run automated format checks on push, pull request, and workflow call | Non-functional | E005 | explicit | Inspection | High |
| DR-001 | Produce visible telemetry after enablement | Data | E004 | explicit | Demonstration | High |
| DR-002 | Expose observable command counter data | Data | E004 | explicit | Demonstration | High |
| DR-003 | Accept packet-oriented command parameters | Data | E006 | explicit | Test | Medium |
| DR-004 | Organize changelog data by configured categories | Data | E001 | explicit | Inspection | High |
| C-001 | Require Git submodules in source checkout | Constraint | E002 | explicit | Inspection | High |
| C-002 | Use provided sample make assets for build prep | Constraint | E002 | explicit | Inspection | High |
| C-003 | Depend on `core-cpu1` and `cmdUtil` for functional tests | Constraint | E006 | explicit | Inspection | Medium |
| C-004 | Use GitHub Actions as the evidenced CI/deployment mechanism | Constraint | E001, E005, E006 | explicit | Inspection | High |
