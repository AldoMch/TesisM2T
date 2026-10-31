# Software Requirements Specification

## 1. Introduction

### Purpose
This SRS defines the checked software requirements for `OAID/Tengine`. It covers the documented example workflows, exposed APIs, model serialization and conversion behavior, core module structure, and supported build and deployment characteristics.

### Product Scope
Tengine Lite is an inference-oriented software product that provides:
- Example applications for classification, detection, segmentation, pose estimation, landmark detection, and character recognition tasks
- C, C++, and Python-facing API surfaces
- Core architecture modules for device, scheduler, operator, and serializer responsibilities
- A serializer that decodes binary `tmfile` model data
- Model conversion tooling, including a Linux pre-compiled tool and a browser-local WebAssembly-based online converter
- Cross-platform compilation based on CMake

### Intended Audience
This document is intended for:
- Developers integrating Tengine Lite through C, C++, or Python APIs
- Users running the provided example applications
- Architects and maintainers deriving system structure from the repository
- Test engineers validating documented product behavior

## 2. Overall Description

### Product Perspective
Tengine Lite is a library and toolkit with example applications, API documentation surfaces, a serializer for `tmfile` model decoding, and model conversion utilities.

Tengine Lite's core architecture includes four module categories:
- `device`, which provides the NN Operators backend
- `scheduler`, which is responsible for scheduling and executing NNIR, computation graphs, hardware resources, and the model serializer
- `operator`, which is responsible for registering and initializing NN Operators
- `serializer`, which is responsible for decoding the binary `tmfile` model format

The repository also presents example-driven end-to-end execution of common neural-network tasks using supplied models and images.

### Product Functions Summary
The product supports:
- Runnable examples for multiple AI vision and OCR tasks
- Use through the original Tengine-compatible C API
- Presence of C++ API and Python API documentation entry points
- Binary `tmfile` decoding through the serializer module
- Model conversion through a Linux pre-compiled tool and a browser-local online converter
- Cross-platform build through CMake-based compilation

### User Classes
- **C API integrators**: developers using Tengine Lite in native applications
- **C++ API users**: developers using or inspecting the C++ API surface
- **Python API users**: developers using or inspecting the Python API surface
- **Example users**: users validating supported tasks with provided models and images
- **Tool users**: users converting models through Linux or browser-based tooling

### Operating Environment
- Cross-platform build environments using CMake
- Linux environments for the pre-compiled model conversion tool
- Web browsers with WebAssembly support for the online model conversion tool
- Local execution environments with access to required model and image assets

### Assumptions and Dependencies
- Example execution depends on required image and model assets being available in the expected local project paths
- Model conversion depends on either the Linux prebuilt tool or a browser capable of local WebAssembly execution
- Native integration depends on the provided library and API surfaces being available in the build environment

## 3. External Interface Requirements

### User Interfaces
- The system shall provide runnable example programs for the documented tasks.
- The system shall provide a browser-based online model conversion interface that performs conversion locally in the browser.

### Software and API Interfaces
- The system shall expose a C API compatible with original Tengine usage patterns.
- The system shall provide C++ API documentation entry points.
- The system shall provide Python API documentation entry points.
- The system shall provide serializer interfaces for decoding binary `tmfile` model data.
- The system shall provide model conversion tooling through Linux and browser-based interfaces.

### Communication Interfaces
- No external network communication interface is required for the online model conversion workflow.
- The browser-based conversion workflow shall execute locally in the browser through WebAssembly.

### Data Exchange Formats
- Example workflows shall consume local model files and image files.
- The serializer shall accept binary `tmfile` model input.
- Model conversion workflows shall produce converted model artifacts.

## 4. Functional Requirements

| ID | Description | Trigger/Input | System Behavior | Output | Priority | Verification |
|---|---|---|---|---|---|---|
| FR-001 | Example application availability | User selects a documented example task | The system shall provide example applications for the documented tasks: classification, facial landmark detection, SSD object detection, RetinaFace face detection, Yolact instance segmentation, U-Net image segmentation, YoloV3, YoloV4-tiny, YoloV5s, NanoDet, EfficientDet, OpenPose, HRNet, and CRNN Chinese character recognition. The example set is continuously updated; this list reflects the scope represented by the current repository contents. | Executable example workflow for the selected task | High | Inspection |
| FR-002 | Classification example execution | User runs the classification example with required assets | The system shall allow the classification example to run MobileNet v1 using the original Tengine-compatible C API. | Classification task output | High | Demonstration |
| FR-003 | Local asset-based example execution | User places images and models in the expected local paths and runs an example | The system shall support execution of documented example tasks using local images and model files placed under the project root folder. | Task-specific example output | High | Demonstration |
| FR-004 | C++ API documentation entry point | Developer consults the C++ API documentation | The system shall provide a C++ API documentation entry point. | C++ API documentation entry point is present | Medium | Inspection |
| FR-005 | Python API documentation entry point | Developer consults the Python API documentation | The system shall provide a Python API documentation entry point. | Python API documentation entry point is present | Medium | Inspection |
| FR-006 | `tmfile` decoding | User or integrator supplies a binary `tmfile` model | The system shall decode binary `tmfile` model data through the serializer module into serialized model parameters. | Serialized model parameters | High | Analysis |
| FR-007 | Model conversion tooling availability | User requests model conversion | The system shall provide model conversion tooling as both a pre-compiled Linux tool and an online WebAssembly-based converter. | Converted model artifact | Medium | Inspection |
| FR-008 | Browser-local conversion execution | User uses the online conversion tool | The system shall perform online model conversion locally within the browser through WebAssembly. | Locally converted model artifact | Medium | Demonstration |
| FR-009 | Operator module support | System initialization or operator registration flow | The system shall provide an operator module to support registration and initialization of NN Operators. | Registered and initialized NN Operators | High | Inspection |

## 5. Non-Functional Requirements

| ID | Quality Attribute | Requirement | Priority | Verification |
|---|---|---|---|---|
| NFR-001 | Portability | The system shall support quick cross-platform compilation based on CMake. | High | Inspection |
| NFR-002 | Compatibility | Tengine Lite shall remain compatible with the original Tengine C API for documented example usage. | High | Demonstration |
| NFR-003 | Local processing behavior | The online model conversion tool shall convert models locally in the browser based on WebAssembly, and the documentation shall state that no private data will be uploaded. | Medium | Demonstration |
| NFR-004 | Platform compatibility | The pre-compiled model conversion tool shall be provided for Linux systems. | Medium | Inspection |

## 6. Data Requirements

| ID | Data Item | Requirement |
|---|---|---|
| DR-001 | Model files | The system shall accept local model files for example execution and model conversion workflows. |
| DR-002 | Image files | The system shall accept local image files for documented example workflows. |
| DR-003 | Binary `tmfile` models | The serializer shall accept binary `tmfile` model input for decoding. |
| DR-004 | Serialized model parameters | The serializer shall produce serialized model parameters from binary `tmfile` input. |
| DR-005 | Converted model artifacts | The model conversion workflows shall produce converted model artifacts. |

### Data Handling
- The online conversion tool converts models locally in the browser.
- The documentation states that no private data will be uploaded during the online conversion workflow.

## 7. System Constraints

| ID | Constraint |
|---|---|
| C-001 | Compilation is constrained to a CMake-based build approach for the documented cross-platform compilation path. |
| C-002 | The pre-compiled model conversion tool is constrained to Linux systems. |
| C-003 | The online model conversion tool depends on browser WebAssembly support and executes conversion locally in the browser. |
| C-004 | Example execution depends on the presence of required local image and model assets under the project root folder. |

## 8. Verification and Acceptance Criteria

| Requirement ID | Verification Method | Acceptance Criteria |
|---|---|---|
| FR-001 | Inspection | Example programs exist for each listed task in the current repository scope. |
| FR-002 | Demonstration | Running the classification example with required assets produces classification output through the original Tengine-compatible C API path. |
| FR-003 | Demonstration | A documented example runs successfully when images and models are placed under the expected project root paths. |
| FR-004 | Inspection | A C++ API documentation entry point is present. |
| FR-005 | Inspection | A Python API documentation entry point is present. |
| FR-006 | Analysis | Serializer behavior and documentation show decoding of binary `tmfile` into serialized model parameters. |
| FR-007 | Inspection | Documentation or repository contents show both Linux pre-compiled and browser-based converter options. |
| FR-008 | Demonstration | Online converter behavior shows model conversion occurs locally in the browser through WebAssembly. |
| FR-009 | Inspection | Product structure or documentation identifies an operator module responsible for registration and initialization of NN Operators. |
| NFR-001 | Inspection | Build documentation states cross-platform compilation based on CMake. |
| NFR-002 | Demonstration | Documented example usage confirms compatibility with the original Tengine C API. |
| NFR-003 | Demonstration | Online conversion behavior is shown as browser-local through WebAssembly, and documentation states that no private data will be uploaded. |
| NFR-004 | Inspection | Documentation identifies Linux as the platform for the pre-compiled converter. |
