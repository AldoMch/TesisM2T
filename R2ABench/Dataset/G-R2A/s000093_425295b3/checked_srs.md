# Software Requirements Specification

## 1. Introduction

### Purpose
This SRS defines the checked software requirements for `VirtualMotionTracker`. It is intended to support downstream architecture generation and verification planning for the repository’s core product behavior and its primary external dependencies.

### Product scope
`VirtualMotionTracker` is a virtual motion tracking system that connects:
- a User Application that provides external control input,
- a VMT Manager component,
- a VMT Driver component, and
- the OpenVR/SteamVR runtime.

Within this scope:
- the User Application provides control input to VMT Manager,
- VMT Manager and VMT Driver exchange JSON messages through shared memory,
- VMT Driver integrates with SteamVR through the OpenVR driver interface, and
- a legacy controller binding file is provided for a controller type named `mycontroller`.

OpenVR SDK initialization behavior, interface-version checks, shutdown behavior, path constants, and SDK data structures are treated in this SRS as dependency context and constraints rather than as core repository-authored product functionality.

### Intended audience
This document is intended for:
- developers and maintainers of `VirtualMotionTracker`,
- architects generating component and interface views,
- test engineers validating integration behavior,
- integrators working with SteamVR/OpenVR and external control applications.

## 2. Overall Description

### Product perspective
The system is a multi-component virtual tracking solution composed of:
- a User Application that supplies external control input,
- a VMT Manager that receives that input and manages communication,
- a VMT Driver that exposes virtual motion tracking capability to SteamVR/OpenVR, and
- shared-memory communication between manager and driver using JSON messages.

The product depends on OpenVR/SteamVR runtime facilities and related SDK artifacts, but those SDK behaviors are not the primary functional scope of this specification.

### Product functions summary
The system supports the following product-level functions:
- receive external control input on the VMT management side,
- exchange JSON messages bidirectionally between VMT Manager and VMT Driver through shared memory,
- provide a VMT driver artifact loadable by OpenVR/SteamVR,
- provide a legacy binding definition for `mycontroller` with specified right-hand mappings and binding-mode metadata.

### User classes
- External control application integrator: provides motion-tracking control input to the system.
- Runtime integrator/operator: installs or runs the VMT Driver with SteamVR/OpenVR.
- Test/configuration engineer: validates shared-memory messaging, driver loading, and controller binding behavior.

### Operating environment
- SteamVR/OpenVR runtime environment
- Host environment capable of shared-memory inter-process communication
- User application environment capable of providing external control input to VMT Manager

### Assumptions and dependencies
- The system depends on SteamVR/OpenVR to load and host the VMT Driver.
- The system depends on OpenVR driver-interface compatibility.
- The architecture identifies external control input as OSC, but this SRS does not specify a port number or a complete command set.
- OpenVR SDK constants, structures, and runtime initialization/shutdown semantics are dependency details rather than standalone product requirements.

## 3. External Interface Requirements

### User interfaces
No end-user graphical interface requirements are defined in the checked scope.

### Software interfaces
- The system shall integrate with the SteamVR/OpenVR runtime through the OpenVR driver interface.
- The system shall provide a driver-side integration point usable by SteamVR/OpenVR to expose virtual motion tracking capability.
- The system shall provide a legacy controller binding file for controller type `mycontroller`.

### Communication interfaces

#### External control input interface
- The system shall support external control input from the User Application to VMT Manager.
- The architecture identifies this external control interface as OSC.
- No specific network port, transport configuration, or full command set is specified in this SRS.

#### Internal inter-process communication interface
- The system shall exchange JSON strings between VMT Manager and VMT Driver through shared memory.
- The shared-memory interface shall support bidirectional channels:
  - manager-to-driver, and
  - driver-to-manager.
- The shared-memory interface shall include synchronization/control fields for send count, handshake count, and message length.

#### Runtime interface
- The VMT Driver shall interface with the SteamVR/OpenVR runtime through the OpenVR driver interface.

### Data exchange formats
- External control data from the User Application to VMT Manager shall be accepted through the control-input interface identified by the architecture.
- Messages exchanged between VMT Manager and VMT Driver shall be encoded as JSON strings.
- The controller binding definition shall be represented as JSON.

## 4. Functional Requirements

### Core product requirements

| ID | Description | Trigger/Input | System behavior | Output | Priority | Verification |
|---|---|---|---|---|---|---|
| FR-001 | Receive external control input | External control input is sent from the User Application | The system shall, on the VMT management side, receive external control input and use it as the data source for virtual motion tracking state updates. | Control input is made available to VMT processing logic. | High | Inspection |
| FR-002 | Shared-memory JSON communication | Manager and driver exchange operational messages | The system shall exchange JSON messages between VMT Manager and VMT Driver through shared memory. | JSON message data is transferred between manager and driver. | High | Inspection |
| FR-003 | Bidirectional communication channels | Shared-memory communication is established | The system shall support bidirectional message channels from manager to driver and from driver to manager. | Messages can be sent in both directions. | High | Inspection |
| FR-004 | Shared-memory synchronization metadata | A shared-memory message transfer occurs | The system shall control shared-memory message exchange using send count, handshake count, and message length fields. | Message transfer state and payload length are synchronized across the channel. | Medium | Inspection |
| FR-005 | SteamVR/OpenVR driver availability | The runtime attempts to load the VMT driver | The system shall provide a VMT driver artifact loadable by OpenVR/SteamVR so that virtual motion tracking capability can be exposed through the OpenVR driver interface. | The driver is available for runtime integration. | High | Demonstration |
| FR-006 | Legacy binding for `mycontroller` | The legacy binding file is loaded for controller type `mycontroller` | For the `mycontroller` legacy binding, the system shall map three right-hand inputs to legacy actions using button mode and complex sub-mode. The mappings shall be: `/user/hand/right/input/a` to `/actions/legacy/in/right_axis1_press`, `/user/hand/right/input/c` to `/actions/legacy/in/right_a_press`, and `/user/hand/right/input/b` to `/actions/legacy/in/right_grip_press`. | A legacy JSON binding definition is available for OpenVR consumption. | Medium | Inspection |

### Dependency behavior
The following behaviors are relevant dependency context but are not treated as core repository-authored functional requirements:
- OpenVR runtime initialization as a scene application
- OpenVR interface-version validation
- OpenVR runtime shutdown behavior
- OpenVR SDK path constants and SDK structure definitions

## 5. Non-Functional Requirements

| ID | Quality attribute | Requirement | Priority | Verification |
|---|---|---|---|---|
| NFR-001 | Interoperability | The system shall interoperate with SteamVR/OpenVR through the OpenVR driver interface. | High | Demonstration |
| NFR-002 | Inter-process interoperability | Shared-memory communication between VMT Manager and VMT Driver shall use JSON in both communication directions. | High | Inspection |
| NFR-003 | Compatibility | The controller binding artifact shall be encoded as JSON using OpenVR-style action and input path strings. | Medium | Inspection |
| NFR-004 | Architectural separation | The system shall maintain separation between external control input handling, manager-driver shared-memory communication, and runtime driver integration. | Medium | Inspection |

## 6. Data Requirements

| ID | Data item/entity | Requirement | Verification |
|---|---|---|---|
| DR-001 | External control input | The system shall accept external control input as data for virtual motion tracking state updates. | Inspection |
| DR-002 | Shared-memory message payload | The system shall encode manager-driver exchanged messages as JSON strings. | Inspection |
| DR-003 | Shared-memory control metadata | The system shall maintain send count, handshake count, and message length fields for shared-memory communication control. | Inspection |
| DR-004 | Controller binding document | The system shall store a JSON controller binding document containing controller type, action paths, input paths, and binding metadata. | Inspection |
| DR-005 | Legacy binding metadata | The `mycontroller` legacy binding shall include button mode and `sub_mode` set to `complex` for each of the specified mappings. | Inspection |

## 7. System Constraints

| ID | Constraint |
|---|---|
| C-001 | The VMT Driver is constrained to integration with the SteamVR/OpenVR runtime through the OpenVR driver interface. |
| C-002 | Manager-driver inter-process communication is constrained to shared-memory JSON exchange. |
| C-003 | The external control input interface is identified architecturally as OSC, but this specification does not define a fixed port, transport configuration, or complete command set. |
| C-004 | OpenVR SDK runtime behaviors, constants, and structures are dependency constraints and context, not core product requirements. |
| C-005 | The controller binding requirement in this SRS applies specifically to the legacy binding for `mycontroller`, not to all possible controller binding files. |

## 8. Verification and Acceptance Criteria

| Requirement ID | Verification method | Acceptance criterion |
|---|---|---|
| FR-001 | Inspection | The architecture and implementation define receipt of external control input by the VMT management side for use in virtual motion tracking updates. |
| FR-002 | Inspection | The implementation defines JSON message exchange between VMT Manager and VMT Driver through shared memory. |
| FR-003 | Inspection | The implementation defines both manager-to-driver and driver-to-manager message channels. |
| FR-004 | Inspection | The shared-memory message mechanism includes send count, handshake count, and message length fields. |
| FR-005 | Demonstration | The VMT driver artifact can be loaded by SteamVR/OpenVR for runtime integration through the OpenVR driver interface. |
| FR-006 | Inspection | The complete legacy binding JSON confirms `controller_type` is `mycontroller`, contains the three specified right-hand mappings, and each mapping uses mode `button` with `parameters.sub_mode` set to `complex`. |
| NFR-001 | Demonstration | Integration with SteamVR/OpenVR occurs through the OpenVR driver interface. |
| NFR-002 | Inspection | Shared-memory communication uses JSON consistently in both directions. |
| NFR-003 | Inspection | The binding artifact is JSON and uses OpenVR-style action and input path strings. |
| NFR-004 | Inspection | The architecture separates external input handling, shared-memory manager-driver communication, and runtime driver integration into distinct responsibilities. |
