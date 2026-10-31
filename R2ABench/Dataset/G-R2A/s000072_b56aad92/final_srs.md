# Software Requirements Specification (SRS)

## 1. Introduction

### Purpose
This SRS defines evidence-backed requirements for the communication, integration, and verification behaviors visible in the provided repository evidence for ParaStation/psmpi at commit `48893b32e1f1753cbc49d90282368c0c6727b018`.

### Product scope
Based on the available evidence, the covered scope is limited to:
- manual verification workflows for embedded `hwloc` testing,
- communication subsystem control and progress interfaces,
- send-path behavior for packetized data transfer,
- integration constraints for the Libfabric verbs provider.

### Intended audience
- Maintainers and integrators of psmpi communication components
- Test engineers validating embedded `hwloc` packaging and communication behavior
- Build and deployment engineers integrating verbs-based network transport dependencies

### References
- Repository: https://github.com/ParaStation/psmpi
- Snapshot: https://github.com/ParaStation/psmpi/tree/48893b32e1f1753cbc49d90282368c0c6727b018
- Evidence sources:
  - `mpich2/modules/hwloc/tests/hwloc/embedded/README.txt` (`E001`)
  - `mpich2/src/pm/hydra/tools/topo/hwloc/hwloc/tests/hwloc/embedded/README.txt` (`E002`)
  - `mpich2/modules/libfabric/README.md` (`E003`)
  - `mpich2/doc/notes/coll/collective.txt` (`E004`)
  - `mpich2/doc/notes/agent/send-sm.txt` (`E005`, `E006`)

## 2. Overall Description

### Product perspective
The evidence shows psmpi as a communication-oriented software stack with:
- a communication subsystem using VC-oriented progress and connection operations,
- packet-based send behavior with flow control and direct/packed data handling,
- optional integration with Libfabric verbs support over the Linux Verbs API,
- manually executed embedded `hwloc` verification workflows.

### Product functions summary
- Run embedded `hwloc` verification against a distribution tarball
- Support manual build-and-test workflow for embedded `hwloc`
- Provide communication lifecycle and progress operations
- Support one-to-many transfer/scatter behavior
- Apply flow control before posting data sends
- Send data either by direct access to pinned user data or by packet-buffer packing
- Integrate verbs transport through `libibverbs` and `librdmacm`

### User classes
- Developer/tester running embedded `hwloc` tests manually (`E001`, `E002`)
- Integrator building verbs-enabled transport with external libraries (`E003`)
- Communication subsystem integrator using progress/connect/scatter interfaces (`E004`)

### Operating environment
Supported by evidence:
- Build/test execution from a shell environment using scripts and autotools-style commands such as `./autogen.sh`, `./configure`, and `make` (`E001`, `E002`)
- Verbs transport integration using the Linux Verbs API with `libibverbs` and `librdmacm` (`E003`)

### Assumptions and dependencies
- Verbs provider support depends on `libibverbs` version `1.1.8` or newer and `librdmacm` version `1.0.16` or newer (`E003`)
- Matching header files are required when compiling Libfabric from source with verbs support (`E003`)
- Non-default library/header locations must be supplied through `CFLAGS`, `LDFLAGS`, and `LD_LIBRARY_PATH` (`E003`)
- Embedded `hwloc` tests are manual and are not part of `make check` (`E001`, `E002`)

## 3. External Interface Requirements

### User interfaces
- Command-line/script interface for embedded test execution via `./run-embedded-tests.sh <tarball>` (`E001`, `E002`)
- Command-line build interface via `./autogen.sh`, `./configure`, and `make` for manual embedded verification (`E001`, `E002`)

### Software/API interfaces
- Verbs provider interface to the Linux Verbs API (`E003`)
- Communication management through `librdmacm` and control/data transfer through `libibverbs` (`E003`)
- Communication subsystem operations:
  - `Init()`
  - `Finalize()`
  - `Make_progress(VC)`
  - `Make_progress_blocking()`
  - `Connect(VC, rank, comm or BNR_Group, &request)` (`E004`)

### Communication interfaces
- One-to-many scatter-style transfer interface is identified in the communication notes (`E004`)
- Packet sending interacts with a network device and network send descriptors (`E005`, `E006`)

### Data exchange formats
Supported message/data forms include:
- packet buffer contents carrying envelope and `LIBA(OD)` for `rndv-rts`,
- two `LIBAs` for `rndv-cts`,
- one `LIBA` for `rndv-data`,
- payload data packed from a data descriptor into a packet buffer when direct access is not used (`E006`)

## 4. Functional Requirements

| ID | Description | Trigger / Input | System behavior | Output | Priority | Verification | Source evidence |
|---|---|---|---|---|---|---|---|
| FR-001 | Provide preferred embedded `hwloc` verification execution | User invokes `./run-embedded-tests.sh <tarball>` from the embedded test directory | The system shall execute a battery of tests against the specified distribution tarball to verify embedding behavior | Test results from the battery of embedded tests | High | Demonstration | E001, E002 |
| FR-002 | Provide manual embedded `hwloc` verification workflow | User expands a distribution `hwloc` tarball, renames the top-level directory to `hwloc-tree/`, and runs `./autogen.sh`, `./configure`, and `make` | The system shall support manual embedded verification using the renamed source tree and autotools build sequence | Built testable tree for manual verification activities | Medium | Demonstration | E001, E002 |
| FR-003 | Provide communication lifecycle and progress operations | Communication subsystem is initialized or needs progress/connect handling | The system shall provide `Init()`, `Finalize()`, `Make_progress(VC)`, `Make_progress_blocking()`, and `Connect(VC, rank, comm or BNR_Group, &request)` operations | Initialized/finalized subsystem state, progress result, or connection request handling | High | Inspection | E004 |
| FR-004 | Support one-to-many transfer behavior | A communication path requires one-to-many data movement | The system shall support a scatter-style transfer interface for one-to-many communication | Transfer request handled as scatter communication | Medium | Inspection | E004 |
| FR-005 | Enforce flow control before posting data sends | Data packet send is requested and flow status is checked | The system shall defer data sending when flow is restricted and shall transition to awaiting-flow behavior until flow is enabled; when flow is enabled, it shall post the data send | Deferred send state or posted data send | High | Test | E005 |
| FR-006 | Support direct-access sending for pinned user data | A send of type `short`, `eager`, or `rndv-data` occurs and the direct access flag is set | The system shall point the network send descriptor at the pinned user data instead of packing payload into the packet buffer | Network send descriptor referencing pinned user data | High | Test | E005, E006 |
| FR-007 | Support packet-buffer packing when direct access is not used | A send of type `short`, `eager`, or `rndv-data` occurs and direct access is not used | The system shall pack payload data from the data descriptor into the packet buffer before posting the send to the network device | Packet buffer containing payload data for transmission | High | Test | E005, E006 |
| FR-008 | Populate control information according to rendezvous packet type | A send is prepared for `rndv-rts`, `rndv-cts`, or `rndv-data` | The system shall place the documented control information into the packet buffer: envelope and `LIBA(OD)` for `rndv-rts`, two `LIBAs` for `rndv-cts`, and one `LIBA` for `rndv-data` | Packet buffer populated with type-specific control data | Medium | Test | E006 |

## 5. Non-Functional Requirements

| ID | Requirement | Quality attribute | Priority | Verification | Evidence | Evidence type |
|---|---|---|---|---|---|---|
| NFR-001 | Verbs-provider integration shall require `libibverbs` version `1.1.8` or newer and `librdmacm` version `1.0.16` or newer. | Compatibility | High | Inspection | E003 | explicit |
| NFR-002 | When compiling verbs support from source, the build environment shall provide matching header files for `libibverbs` and `librdmacm`. | Build compatibility | High | Inspection | E003 | explicit |
| NFR-003 | When required libraries or headers are not in default paths, the build/deployment environment shall allow their locations to be supplied through `CFLAGS`, `LDFLAGS`, and `LD_LIBRARY_PATH`. | Portability / deployability | Medium | Demonstration | E003 | explicit |
| NFR-004 | Embedded `hwloc` verification shall be executable manually and shall not depend on inclusion in `make check`. | Verifiability | Medium | Demonstration | E001, E002 | explicit |
| NFR-005 | The communication subsystem shall support both polling and blocking progress implementations. | Operational flexibility | Medium | Inspection | E004 | explicit |

## 6. Data Requirements

| ID | Data entity / object | Requirement | Source evidence |
|---|---|---|---|
| DR-001 | Packet buffer | The system shall use a packet buffer to carry control information and, when direct access is not used, payload data for outgoing packets. | E005, E006 |
| DR-002 | Network send descriptor | The system shall prepare a network send descriptor for posted sends and, when direct access is enabled, bind it to pinned user data. | E005, E006 |
| DR-003 | User data / data descriptor | Payload data shall be sourced either directly from pinned user data or from a data descriptor for packet-buffer packing. | E005, E006 |
| DR-004 | Rendezvous control fields | For rendezvous packet types, the packet buffer shall hold the type-specific control fields described in the evidence: envelope, `LIBA(OD)`, or two `LIBAs` depending on packet type. | E006 |
| DR-005 | Flow-control state | The send path shall maintain flow-related state distinguishing flow-restricted and flow-enabled conditions for data packets. | E005 |

## 7. Constraints

| ID | Constraint | Source evidence |
|---|---|---|
| C-001 | Embedded `hwloc` tests are manual and are not part of `make check`. | E001, E002 |
| C-002 | The preferred embedded `hwloc` test entry point is `./run-embedded-tests.sh <tarball>`. | E001, E002 |
| C-003 | The alternative embedded verification workflow requires renaming the extracted top-level directory to `hwloc-tree/` before running `./autogen.sh`, `./configure`, and `make`. | E001, E002 |
| C-004 | Verbs transport uses the Linux Verbs API and depends on `librdmacm` for communication management and `libibverbs` for control and data transfer operations. | E003 |
| C-005 | Verbs provider support requires `libibverbs >= 1.1.8` and `librdmacm >= 1.0.16`. | E003 |

## 8. Verification and Acceptance

| Requirement ID | Verification method | Acceptance basis |
|---|---|---|
| FR-001 | Demonstration | Running `./run-embedded-tests.sh <tarball>` executes a battery of tests against the tarball. |
| FR-002 | Demonstration | The renamed `hwloc-tree/` source can be processed with `./autogen.sh`, `./configure`, and `make` for manual verification. |
| FR-003 | Inspection | The documented communication subsystem exposes the listed lifecycle, progress, and connect operations. |
| FR-004 | Inspection | The documented transfer interface includes one-to-many scatter behavior. |
| FR-005 | Test | Under flow restriction, sending is deferred; after flow enabled, the send is posted. |
| FR-006 | Test | With direct access enabled, the send descriptor references pinned user data. |
| FR-007 | Test | Without direct access, payload is packed from the data descriptor into the packet buffer before send. |
| FR-008 | Test | Each rendezvous packet type populates the documented control fields in the packet buffer. |
| NFR-001 | Inspection | Dependency declarations specify minimum versions for `libibverbs` and `librdmacm`. |
| NFR-002 | Inspection | Build documentation requires matching header files for verbs support from source. |
| NFR-003 | Demonstration | Non-default include/library locations can be supplied via `CFLAGS`, `LDFLAGS`, and `LD_LIBRARY_PATH`. |
| NFR-004 | Demonstration | Embedded verification can be executed manually without `make check`. |
| NFR-005 | Inspection | Documentation identifies both polling and blocking progress implementations. |

## 9. Traceability Matrix

| ID | Requirement | Type | Source | Evidence Type | Verification | Confidence |
|---|---|---|---|---|---|---|
| FR-001 | Provide preferred embedded `hwloc` verification execution | Functional | E001, E002 | explicit | Demonstration | High |
| FR-002 | Provide manual embedded `hwloc` verification workflow | Functional | E001, E002 | explicit | Demonstration | High |
| FR-003 | Provide communication lifecycle and progress operations | Functional | E004 | explicit | Inspection | Medium |
| FR-004 | Support one-to-many transfer behavior | Functional | E004 | explicit | Inspection | Medium |
| FR-005 | Enforce flow control before posting data sends | Functional | E005 | explicit | Test | High |
| FR-006 | Support direct-access sending for pinned user data | Functional | E005, E006 | explicit | Test | High |
| FR-007 | Support packet-buffer packing when direct access is not used | Functional | E005, E006 | explicit | Test | High |
| FR-008 | Populate control information according to rendezvous packet type | Functional | E006 | explicit | Test | High |
| NFR-001 | Require minimum verbs dependency versions | Non-functional | E003 | explicit | Inspection | High |
| NFR-002 | Require matching verbs header files for source builds | Non-functional | E003 | explicit | Inspection | High |
| NFR-003 | Support non-default dependency paths through environment/build flags | Non-functional | E003 | explicit | Demonstration | High |
| NFR-004 | Support manual embedded verification outside `make check` | Non-functional | E001, E002 | explicit | Demonstration | High |
| NFR-005 | Support polling and blocking progress implementations | Non-functional | E004 | explicit | Inspection | Medium |
| DR-001 | Use packet buffer for control and optional payload carriage | Data | E005, E006 | explicit | Inspection | High |
| DR-002 | Prepare network send descriptor, optionally bound to pinned user data | Data | E005, E006 | explicit | Inspection | High |
| DR-003 | Source payload from pinned user data or data descriptor | Data | E005, E006 | explicit | Inspection | High |
| DR-004 | Store rendezvous control fields by packet type | Data | E006 | explicit | Inspection | High |
| DR-005 | Maintain flow-control state for send handling | Data | E005 | explicit | Inspection | Medium |
