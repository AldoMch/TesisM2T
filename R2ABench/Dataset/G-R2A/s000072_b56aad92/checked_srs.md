# Software Requirements Specification

## 1. Introduction

### Purpose
This SRS defines the checked software requirements for selected communication, build, and verification behaviors documented in the `ParaStation/psmpi` repository for sample `s000072_b56aad92`.

### Product scope
This specification covers:
- manual verification workflows for embedded `hwloc` testing,
- documented communication-subsystem design responsibilities for progress, connection establishment, and one-to-many transfer,
- documented behavior of the specific send-state-machine path described in `send-sm` notes,
- conditional build and dependency constraints for the embedded Libfabric verbs provider.

This specification does not treat design-discussion notes as confirmed implemented public APIs unless separately verified.

### Intended audience
- Maintainers and integrators of psmpi communication components
- Test engineers validating embedded `hwloc` packaging and communication behavior
- Build and deployment engineers integrating optional verbs-based transport dependencies

## 2. Overall Description

### Product perspective
The repository includes:
- manually executed embedded `hwloc` verification workflows,
- communication design notes describing subsystem responsibilities such as initialization/termination, progress advancement, connection establishment, and one-to-many transfer,
- a prototype send state-machine note describing flow-control checks, direct-access send behavior, packet-buffer packing, and rendezvous control-field handling,
- an embedded Libfabric module whose verbs provider documentation defines optional build-time dependency constraints,
- CH4 network-module integration context that can involve network libraries such as OFI/libfabric or UCX.

### Product functions summary
The documented functions and responsibilities in scope are:
- run embedded `hwloc` verification against a distribution tarball,
- support a manual build-and-test workflow for embedded `hwloc`,
- document communication-subsystem responsibilities for initialization, termination, progress, connection establishment, and one-to-many transfer,
- in the specific send path described by the send state-machine note, perform flow-control checks before posting data sends,
- in that same send path, send payload either by direct access to pinned user data or by packing payload into a packet buffer,
- when the embedded Libfabric verbs provider is enabled, support build integration with Linux Verbs libraries.

### User classes
- Developer or tester running embedded `hwloc` verification manually
- Integrator building or enabling the embedded Libfabric verbs provider
- Communication-subsystem maintainer reviewing communication and send-path design behavior

### Operating environment
- Shell-based build and test environment using commands such as `./run-embedded-tests.sh`, `./autogen.sh`, `./configure`, and `make`
- Linux Verbs environment when the embedded Libfabric verbs provider is built or enabled
- Communication stack context that may integrate with transport layers such as OFI/libfabric or UCX

### Assumptions and dependencies
- Embedded `hwloc` verification is manual and is not part of `make check`.
- The alternative embedded `hwloc` workflow assumes the extracted top-level source directory is renamed to `hwloc-tree/`.
- The verbs-related constraints in this SRS apply only when building or enabling the embedded Libfabric verbs provider.
- Non-default library and header locations may need to be supplied through build and runtime environment variables.

## 3. External Interface Requirements

### User interfaces
- Command-line interface for embedded test execution via `./run-embedded-tests.sh <tarball>`
- Command-line build interface via `./autogen.sh`, `./configure`, and `make` for manual embedded verification

### Software interfaces
- When the embedded Libfabric verbs provider is enabled, interface with the Linux Verbs API
- When the embedded Libfabric verbs provider is enabled, use `librdmacm` for communication management and `libibverbs` for control and data transfer
- The communication design notes describe responsibilities for initialization, finalization, progress advancement, blocking progress, connection establishment, and one-to-many transfer; these are documented design responsibilities rather than confirmed implemented public APIs

### Communication interfaces
- One-to-many scatter-style transfer is documented in the communication design notes
- The specific send-state-machine path interacts with a network device and network send descriptors

### Data exchange formats and terminology
- Packet buffers may carry control information and, when direct access is not used, packed payload data
- `DD` denotes a data descriptor
- `OD` denotes an object or control descriptor term used in the source design note
- `LIBA` is a rendezvous control-information identifier used in the source note; this SRS preserves the term without expanding it into an unsupported concrete structure
- `envelope` denotes message-matching information such as communicator or context, source rank, tag, and related fields

## 4. Functional Requirements

| ID | Description | Trigger / Input | System behavior | Output | Priority | Verification |
|---|---|---|---|---|---|---|
| FR-001 | Provide preferred embedded `hwloc` verification execution | User invokes `./run-embedded-tests.sh <tarball>` from the embedded test directory | The system shall execute the embedded verification workflow against the specified distribution tarball. | Verification steps are executed and a success or failure result is returned. | High | Demonstration |
| FR-002 | Provide manual embedded `hwloc` verification workflow | User expands a distribution `hwloc` tarball, renames the top-level directory to `hwloc-tree/`, and runs `./autogen.sh`, `./configure`, and `make` | The system shall support manual embedded verification using the renamed source tree and autotools build sequence. | Built and testable tree for manual verification activities. | Medium | Demonstration |
| FR-003 | Document communication lifecycle and progress responsibilities | Communication design documentation is reviewed | The system documentation shall describe communication-subsystem responsibilities for initialization, finalization, progress advancement, blocking progress, and connection establishment. | Documented communication design responsibilities are available for inspection. | Medium | Inspection |
| FR-004 | Document one-to-many transfer responsibility | Communication design documentation is reviewed for transfer behavior | The system documentation shall describe one-to-many scatter-style transfer responsibility in the communication design notes. | Documented one-to-many transfer responsibility is available for inspection. | Low | Inspection |
| FR-005 | Document flow control before posting data sends | The send state-machine design is reviewed for a requested data-packet send | The documented send state-machine behavior shall check flow status before posting a data send and shall defer sending while flow is restricted. | Documented send-path logic shows deferred or posted-send behavior based on flow state. | High | Inspection |
| FR-006 | Document direct-access sending for pinned user data | The send state-machine design is reviewed for a `short`, `eager`, or `rndv-data` send with direct access enabled | The documented send state-machine behavior shall reference pinned user data from the network send descriptor instead of packing payload into the packet buffer. | Documented send-path logic shows descriptor binding to pinned user data. | High | Inspection |
| FR-007 | Document packet-buffer packing when direct access is not used | The send state-machine design is reviewed for a `short`, `eager`, or `rndv-data` send without direct access | The documented send state-machine behavior shall pack payload data from the data descriptor into the packet buffer before posting the send. | Documented send-path logic shows packet-buffer packing from the data descriptor. | High | Inspection |
| FR-008 | Document rendezvous control-field handling by packet type | The send state-machine design is reviewed for `rndv-rts`, `rndv-cts`, or `rndv-data` packet preparation | The documented send state-machine behavior shall place the source-note terms into the packet buffer as follows: envelope and `LIBA(OD)` for `rndv-rts`, two `LIBAs` for `rndv-cts`, and one `LIBA` for `rndv-data`. | Documented packet preparation logic shows type-specific control-field population. | Medium | Inspection |

## 5. Non-Functional Requirements

| ID | Quality attribute | Requirement | Priority | Verification |
|---|---|---|---|---|
| NFR-001 | Compatibility | When building or enabling the embedded Libfabric verbs provider, the build shall require `libibverbs` version `1.1.8` or newer and `librdmacm` version `1.0.16` or newer. | High | Inspection |
| NFR-002 | Build compatibility | When compiling the embedded Libfabric verbs provider from source, the build environment shall provide matching header files for `libibverbs` and `librdmacm`. | High | Inspection |
| NFR-003 | Deployability | When required libraries or headers are not in default paths, the build and deployment environment shall allow their locations to be supplied through `CFLAGS`, `LDFLAGS`, and `LD_LIBRARY_PATH`. | Medium | Demonstration |
| NFR-004 | Verifiability | Embedded `hwloc` verification shall be executable manually and shall not depend on inclusion in `make check`. | Medium | Demonstration |
| NFR-005 | Documentation clarity | Design-note-derived communication behaviors shall be treated as documented design responsibilities unless implementation is separately confirmed. | Medium | Inspection |

## 6. Data Requirements

| ID | Data item | Requirement |
|---|---|---|
| DR-001 | Packet buffer | The system shall use a packet buffer in the documented send path to carry control information and, when direct access is not used, payload data for outgoing packets. |
| DR-002 | Network send descriptor | The documented send path shall prepare a network send descriptor for posted sends and, when direct access is enabled, bind it to pinned user data. |
| DR-003 | User data and data descriptor | Payload data in the documented send path shall be sourced either directly from pinned user data or from a data descriptor for packet-buffer packing. |
| DR-004 | Rendezvous control fields | For the documented rendezvous packet types, the packet buffer shall hold the source-note control terms appropriate to packet type: envelope, `LIBA(OD)`, one `LIBA`, or two `LIBAs`, without assuming unsupported concrete field definitions. |
| DR-005 | Flow-control state | The documented send path shall maintain flow-related state distinguishing flow-restricted and flow-enabled conditions for data packets. |

## 7. System Constraints

| ID | Constraint |
|---|---|
| C-001 | Embedded `hwloc` tests are manual and are not part of `make check`. |
| C-002 | The preferred embedded `hwloc` test entry point is `./run-embedded-tests.sh <tarball>`. |
| C-003 | The alternative embedded verification workflow requires renaming the extracted top-level directory to `hwloc-tree/` before running `./autogen.sh`, `./configure`, and `make`. |
| C-004 | When the embedded Libfabric verbs provider is enabled, verbs transport uses the Linux Verbs API and depends on `librdmacm` for communication management and `libibverbs` for control and data transfer operations. |
| C-005 | When the embedded Libfabric verbs provider is enabled, verbs-provider support requires `libibverbs >= 1.1.8` and `librdmacm >= 1.0.16`. |

## 8. Verification and Acceptance Criteria

| Requirement ID | Verification method | Acceptance criterion |
|---|---|---|
| FR-001 | Demonstration | After executing `run-embedded-tests.sh <tarball>`, the script exits with a successful status and completes embedded verification steps such as configure, make, make check, clean, and distclean; on failure, the script returns a nonzero status. |
| FR-002 | Demonstration | The renamed `hwloc-tree/` source can be processed with `./autogen.sh`, `./configure`, and `make` for manual verification. |
| FR-003 | Inspection | Documentation shows communication-subsystem design responsibilities for initialization, finalization, progress handling, blocking progress, and connection establishment. |
| FR-004 | Inspection | Documentation shows one-to-many scatter-style transfer responsibility in the communication design notes. |
| FR-005 | Inspection | Inspection of the send state-machine design note or implemented code confirms flow-control checks and deferred-send behavior before send posting. |
| FR-006 | Inspection | Inspection of the send state-machine design note or implemented code confirms that, with direct access enabled, the send descriptor references pinned user data. |
| FR-007 | Inspection | Inspection of the send state-machine design note or implemented code confirms that, without direct access, payload is packed from the data descriptor into the packet buffer before send posting. |
| FR-008 | Inspection | Inspection of the send state-machine design note or implemented code confirms that each rendezvous packet type populates the documented source-note control terms in the packet buffer. |
| NFR-001 | Inspection | Build documentation for the embedded Libfabric verbs provider specifies minimum versions for `libibverbs` and `librdmacm`. |
| NFR-002 | Inspection | Build documentation for the embedded Libfabric verbs provider requires matching header files for verbs support from source. |
| NFR-003 | Demonstration | Non-default include and library locations can be supplied via `CFLAGS`, `LDFLAGS`, and `LD_LIBRARY_PATH`. |
| NFR-004 | Demonstration | Embedded verification can be executed manually without `make check`. |
| NFR-005 | Inspection | Design-note-derived behaviors are presented as documented responsibilities rather than as confirmed implemented public APIs unless separately verified. |
