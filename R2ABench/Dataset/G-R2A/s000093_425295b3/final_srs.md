# Software Requirements Specification

## 1. Introduction

### Purpose
This SRS specifies the externally observable requirements evidenced for the `VirtualMotionTracker` repository snapshot at commit `f0210012a9772dc0cf324cccac6596e3658d573d`. The scope is limited to the OpenVR-facing initialization/shutdown behavior, path exposure, and input binding artifacts present in the evidence pack.

### Product scope
The evidenced component integrates with OpenVR as a scene application, validates the `IVRSystem` interface at startup, exposes standardized OpenVR path strings for tracked user/body locations, and provides a legacy controller binding for a controller type named `mycontroller`. Sources also expose OpenVR data structures used by the integration.

### Intended audience
This document is intended for:
- Developers integrating the repository with OpenVR
- Test engineers verifying OpenVR startup, shutdown, and bindings
- Maintainers reviewing interface and data compatibility

### References
- Repository: `gpsnmeajp/VirtualMotionTracker`
- Repository URL: <https://github.com/gpsnmeajp/VirtualMotionTracker>
- Snapshot: <https://github.com/gpsnmeajp/VirtualMotionTracker/tree/f0210012a9772dc0cf324cccac6596e3658d573d>
- Evidence sources: `E001` to `E006`

## 2. Overall Description

### Product perspective
The evidenced product portion is an OpenVR-integrated component. It initializes through OpenVR as `VRApplication_Scene`, checks interface-version compatibility, and shuts down through the OpenVR runtime. It also includes OpenVR path constants and a JSON controller binding file. Source evidence: `E001`, `E002`, `E003`, `E004`.

### Product functions summary
- Initialize against OpenVR and return a system interface when startup succeeds. (`E003`)
- Reject initialization when the required OpenVR interface version is unavailable. (`E003`)
- Shut down the OpenVR runtime and invalidate previously obtained interface pointers. (`E003`)
- Expose standardized path strings for user/body locations and related OpenVR paths. (`E001`, `E002`)
- Provide a legacy binding mapping `mycontroller` right-hand inputs to legacy action outputs. (`E004`)

### User classes
- OpenVR application integrators using the runtime initialization and shutdown entry points. (`E003`)
- Configuration/integration users who consume controller binding JSON and OpenVR path identifiers. (`E001`, `E002`, `E004`)

### Operating environment
- OpenVR runtime environment using `vrclient.dll` and `IVRSystem`. (`E003`)
- OpenVR application type `VRApplication_Scene`. (`E003`)

### Assumptions and dependencies
- The component depends on OpenVR interface version validity for successful startup. (`E003`)
- Binding behavior depends on a controller type named `mycontroller` and OpenVR action paths under `/actions/legacy`. (`E004`)

## 3. External Interface Requirements

### User interfaces
No end-user graphical or command-line interface is evidenced in the provided materials.

### Software/API interfaces
| Interface | Requirement summary | Source |
|---|---|---|
| OpenVR initialization API | The system uses OpenVR initialization for application type `VRApplication_Scene`, validates `IVRSystem_Version`, and returns `OpenVR.System` on success or `null` on failure. | `E003` |
| OpenVR shutdown API | The system exposes shutdown behavior that unloads `vrclient.dll`; interface pointers are invalid after shutdown. | `E003` |
| OpenVR path identifiers | The system exposes OpenVR path strings including `/user/foot/left`, `/user/foot/right`, `/user/shoulder/left`, `/user/shoulder/right`, `/user/elbow/left`, `/user/elbow/right`, `/user/knee/left`, `/user/knee/right`, `/user/waist`, `/user/chest`, `/user/camera`, `/user/keyboard`, and `/client_info/app_key`. | `E001`, `E002` |

### Communication interfaces
No network or inter-process communication protocol is directly evidenced beyond local OpenVR runtime/library interaction.

### Data exchange formats
| Format | Usage | Source |
|---|---|---|
| JSON | Controller binding definition with action paths, input paths, controller type, and binding metadata. | `E004` |
| String path identifiers | OpenVR path values representing user/body locations and client metadata paths. | `E001`, `E002` |

## 4. Functional Requirements

| ID | Description | Trigger/Input | System behavior | Output | Priority | Verification | Source evidence |
|---|---|---|---|---|---|---|---|
| FR-001 | Initialize as an OpenVR scene application. | A caller requests initialization. | The system shall initialize OpenVR with application type `VRApplication_Scene`. | An OpenVR system handle is made available when initialization succeeds. | High | Test | `E003` |
| FR-002 | Reject startup when the required OpenVR interface version is unavailable. | OpenVR initialization completes but `IVRSystem_Version` is not valid. | The system shall shut down the OpenVR runtime, set the initialization error to `Init_InterfaceNotFound`, and return `null`. | Failure indication via `null` and interface-not-found error. | High | Test | `E003` |
| FR-003 | Provide runtime shutdown. | A caller requests shutdown. | The system shall invoke OpenVR shutdown behavior and unload the runtime module. | The runtime is shut down and previously obtained interface pointers become invalid. | High | Demonstration | `E003` |
| FR-004 | Expose standardized OpenVR user/body path identifiers. | A consuming component requests OpenVR path constants. | The system shall provide path strings for left/right foot, left/right shoulder, left/right elbow, left/right knee, waist, chest, camera, keyboard, and client app key. | OpenVR-compatible string identifiers are available for integration use. | Medium | Inspection | `E001`, `E002` |
| FR-005 | Provide legacy bindings for controller type `mycontroller`. | OpenVR loads the legacy binding definition for `mycontroller`. | The system shall map `/user/hand/right/input/a` to `/actions/legacy/in/right_axis1_press`, `/user/hand/right/input/c` to `/actions/legacy/in/right_a_press`, and `/user/hand/right/input/b` to `/actions/legacy/in/right_grip_press`. | A JSON binding definition consumable by OpenVR. | Medium | Test | `E004` |

## 5. Non-Functional Requirements

| ID | Quality attribute | Requirement | Priority | Verification | Evidence type | Source evidence |
|---|---|---|---|---|---|---|
| NFR-001 | Compatibility | The system shall validate compatibility with `IVRSystem_Version` before exposing the OpenVR system interface. | High | Test | explicit | `E003` |
| NFR-002 | Reliability | After shutdown, the system shall not require previously obtained OpenVR interface pointers to remain valid. | High | Demonstration | explicit | `E003` |
| NFR-003 | Interoperability | Controller bindings shall be represented in JSON using OpenVR-style action and input path strings. | Medium | Inspection | explicit | `E004` |

## 6. Data Requirements

| ID | Data item/entity | Requirement | Source evidence |
|---|---|---|---|
| DR-001 | OpenVR path identifiers | The system uses string path identifiers for user/body locations and client metadata, including `/user/foot/left`, `/user/foot/right`, `/user/shoulder/left`, `/user/shoulder/right`, `/user/elbow/left`, `/user/elbow/right`, `/user/knee/left`, `/user/knee/right`, `/user/waist`, `/user/chest`, `/user/camera`, `/user/keyboard`, and `/client_info/app_key`. | `E001`, `E002` |
| DR-002 | Controller binding document | The system stores a JSON object containing `bindings`, action paths under `/actions/legacy`, controller input paths, `controller_type`, `description`, and `name`. | `E004` |
| DR-003 | OpenVR runtime pose/timing data | The integration uses OpenVR data structures that include tracked pose and timing fields such as `TrackedDevicePose_t`, compositor benchmark values, and frame timing fields. | `E005` |
| DR-004 | Native/render device data | The integration uses OpenVR device and render-model structures including native device handles, device type, vertex position/normal/texture coordinates, and texture dimensions. | `E006` |

## 7. Constraints

| ID | Constraint | Source evidence |
|---|---|---|
| C-001 | The integration is constrained to the OpenVR runtime and its interface versioning model. | `E003` |
| C-002 | Initialization is constrained to OpenVR application type `VRApplication_Scene`. | `E003` |
| C-003 | Controller input mapping is constrained to OpenVR action-path and input-path conventions expressed in JSON. | `E004` |
| C-004 | Body-location identifiers are constrained to the OpenVR path namespace represented by `/user/...` and related path constants. | `E001`, `E002` |

## 8. Verification and Acceptance

| Requirement ID | Verification method | Acceptance basis |
|---|---|---|
| FR-001 | Test | Initialization as `VRApplication_Scene` returns a non-null system interface when OpenVR and interface version are valid. |
| FR-002 | Test | Invalid `IVRSystem_Version` causes shutdown, `Init_InterfaceNotFound`, and a `null` return. |
| FR-003 | Demonstration | After shutdown, the runtime is unloaded and prior interface pointers are no longer valid for use. |
| FR-004 | Inspection | The exposed constants match the evidenced OpenVR path strings. |
| FR-005 | Test | Loading the binding file exposes the evidenced right-hand input mappings for controller type `mycontroller`. |
| NFR-001 | Test | Startup rejects an invalid `IVRSystem_Version` before exposing the system interface. |
| NFR-002 | Demonstration | Shutdown leaves prior interface pointers invalid. |
| NFR-003 | Inspection | Binding data is encoded as JSON with OpenVR-style path fields. |

## 9. Traceability Matrix

| ID | Requirement | Type | Source | Evidence Type | Verification | Confidence |
|---|---|---|---|---|---|---|
| FR-001 | Initialize as an OpenVR scene application | Functional | `E003` | explicit | Test | High |
| FR-002 | Reject startup on invalid `IVRSystem_Version` | Functional | `E003` | explicit | Test | High |
| FR-003 | Provide runtime shutdown and invalidate pointers | Functional | `E003` | explicit | Demonstration | High |
| FR-004 | Expose standardized OpenVR user/body path identifiers | Functional | `E001`, `E002` | explicit | Inspection | High |
| FR-005 | Provide legacy bindings for `mycontroller` | Functional | `E004` | explicit | Test | High |
| NFR-001 | Validate OpenVR interface compatibility before use | Non-functional | `E003` | explicit | Test | High |
| NFR-002 | Do not rely on interface pointer validity after shutdown | Non-functional | `E003` | explicit | Demonstration | High |
| NFR-003 | Represent bindings in JSON with OpenVR path strings | Non-functional | `E004` | explicit | Inspection | High |
| DR-001 | Use OpenVR path string data items | Data | `E001`, `E002` | explicit | Inspection | High |
| DR-002 | Store controller binding JSON data | Data | `E004` | explicit | Inspection | High |
| DR-003 | Use OpenVR pose and timing structures | Data | `E005` | explicit | Inspection | Medium |
| DR-004 | Use native/render device structures | Data | `E006` | explicit | Inspection | Medium |
| C-001 | OpenVR runtime/interface-version dependency | Constraint | `E003` | explicit | Inspection | High |
| C-002 | `VRApplication_Scene` application-type constraint | Constraint | `E003` | explicit | Inspection | High |
| C-003 | OpenVR JSON action/input path constraint | Constraint | `E004` | explicit | Inspection | High |
| C-004 | OpenVR `/user/...` path namespace constraint | Constraint | `E001`, `E002` | explicit | Inspection | High |
