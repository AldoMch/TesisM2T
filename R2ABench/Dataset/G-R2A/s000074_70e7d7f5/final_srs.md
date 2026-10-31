# Software Requirements Specification

## 1. Introduction

### Purpose
This SRS specifies evidence-backed requirements for `OAID/Tengine` at commit `2375c98f6ad2cd45d65364efe5ac7538425da7d5`, focusing on the documented example workflows, exposed APIs, model serialization/conversion behavior, and supported build/deployment characteristics.

### Product scope
Tengine Lite is evidenced as an inference-oriented software product that provides:
- Example applications for classification, detection, segmentation, pose estimation, landmark detection, and character recognition tasks.
- C, C++, and Python-facing API surfaces.
- A serializer that decodes binary `tmfile` model data.
- Model conversion tooling, including a Linux pre-compiled tool and a browser-local WebAssembly-based online converter.
- Quick cross-platform compilation based on CMake.

### Intended audience
This document is intended for:
- Developers integrating Tengine Lite through C, C++, or Python APIs.
- Users running the provided example applications.
- Evaluators verifying repository-supported product behavior.

### References
- Repository: `OAID/Tengine`
- Commit: `2375c98f6ad2cd45d65364efe5ac7538425da7d5`
- Evidence sources: `E001` to `E006`

## 2. Overall Description

### Product perspective
The repository evidence presents Tengine Lite as a library/toolkit with example applications, API documentation, a serializer for `tmfile` model decoding, and model conversion utilities. The examples demonstrate end-to-end execution of common neural network tasks using supplied models and images. Sources: `E001`, `E005`, `E006`.

### Product functions summary
- Provide runnable examples for multiple AI vision and OCR tasks. `E001`, `E002`, `E006`
- Support use through the original Tengine-compatible C API. `E001`, `E006`
- Provide C++ API documentation. `E003`
- Provide Python API documentation. `E004`
- Decode binary `tmfile` model format through the serializer module. `E005`
- Provide model conversion tools on Linux and through a browser-local online converter. `E005`

### User classes
- C API integrators using Tengine Lite in native applications. `E001`, `E006`
- C++ API users. `E003`
- Python API users. `E004`
- Example users validating supported tasks with provided models and images. `E001`, `E002`, `E006`

### Operating environment
- Cross-platform build environment using CMake for compilation. `E005`
- Linux environment for the pre-compiled model convert tool. `E005`
- Web browser environment with WebAssembly support for the online model convert tool. `E005`

### Assumptions and dependencies
- Example execution depends on placing images and models under the project root folder before running examples. `E002`
- Model conversion availability depends on either Linux prebuilt tooling or a browser capable of local WebAssembly execution. `E005`

## 3. External Interface Requirements

| Interface area | Requirement summary | Source evidence |
|---|---|---|
| User interfaces | The product shall expose runnable example programs for documented tasks; examples are run with local images and models and produce task-specific outputs. | `E001`, `E002`, `E006` |
| Software/API interfaces | The product shall expose a C API compatible with original Tengine usage patterns, and documented C++ and Python APIs. | `E001`, `E003`, `E004`, `E006` |
| Communication interfaces | No network communication interface is directly specified in the evidence. The online model converter is browser-based and performs conversion locally. | `E005` |
| Data exchange formats | The serializer shall decode binary `tmfile` model format into serialized model parameters. Example workflows use model files and image inputs. | `E002`, `E005` |

## 4. Functional Requirements

| ID | Description | Trigger/Input | System behavior | Output | Priority | Verification | Source evidence |
|---|---|---|---|---|---|---|---|
| FR-001 | The system shall provide example applications for the documented tasks: classification, facial landmark detection, SSD object detection, RetinaFace face detection, Yolact instance segmentation, U-Net image segmentation, YoloV3, YoloV4-tiny, YoloV5s, NanoDet, EfficientDet, OpenPose, HRNet, and CRNN Chinese character recognition. | User selects a documented example task. | The system makes a corresponding example program available for execution. | Executable example workflow for the selected task. | High | Inspection | `E001`, `E006` |
| FR-002 | The system shall allow the classification example to run MobileNet v1 using the original Tengine-compatible C API. | User runs `tm_classification.c` with the required model/input assets. | The system executes the classification example through the compatible C API. | Classification task output. | High | Demonstration | `E001`, `E006` |
| FR-003 | The system shall support execution of documented example tasks using local images and model files placed under the project root folder. | User places images and models under the root folder and runs an example. | The system reads the local assets and executes the selected example. | Task-specific output for the example. | High | Demonstration | `E002` |
| FR-004 | The system shall provide a documented C++ API interface. | Developer consults the C++ API documentation. | The system exposes a C++ API reference as part of product documentation. | C++ API documentation. | Medium | Inspection | `E003` |
| FR-005 | The system shall provide a documented Python API interface. | Developer consults the Python API documentation. | The system exposes a Python API reference as part of product documentation. | Python API documentation. | Medium | Inspection | `E004` |
| FR-006 | The system shall decode binary `tmfile` model data through the serializer module into serialized model parameters. | User or integrator supplies a binary `tmfile` model to the serializer path. | The serializer decodes the binary `tmfile` format. | Serialized model parameters usable by the product. | High | Analysis | `E005` |
| FR-007 | The system shall provide model conversion tooling as both a pre-compiled Linux tool and an online WebAssembly-based converter. | User requests model conversion. | The system offers conversion through the Linux pre-compiled tool or the online converter. | Converted model artifact. | Medium | Inspection | `E005` |
| FR-008 | The online model conversion workflow shall convert models locally within the browser. | User uses the online conversion tool. | The system performs model conversion in the browser via WebAssembly rather than remote processing. | Locally converted model artifact. | Medium | Demonstration | `E005` |

## 5. Non-Functional Requirements

| ID | Requirement | Quality attribute | Priority | Verification | Evidence type | Source evidence |
|---|---|---|---|---|---|---|
| NFR-001 | The system shall support quick cross-platform compilation based on CMake. | Portability | High | Inspection | explicit | `E005` |
| NFR-002 | Tengine Lite shall remain compatible with the original Tengine C API for documented example usage. | Compatibility | High | Demonstration | explicit | `E001`, `E006` |
| NFR-003 | The online model conversion tool shall process models locally in the browser through WebAssembly. | Privacy / deployment behavior | Medium | Demonstration | explicit | `E005` |
| NFR-004 | The pre-compiled model conversion tool shall be provided on Linux systems. | Platform compatibility | Medium | Inspection | explicit | `E005` |

## 6. Data Requirements

| Area | Requirement / description | Source evidence |
|---|---|---|
| Data entities | Model files, image files, serialized model parameters, and binary `tmfile` models are product-relevant data objects. | `E002`, `E005` |
| Input data | Example workflows require local images and models placed under the project root folder. | `E002` |
| Output data | Example workflows produce task-specific outputs; model conversion produces converted model artifacts. | `E002`, `E005` |
| Serialization format | The serializer shall decode binary `tmfile` format into serialized model parameters. | `E005` |
| Privacy / data handling | The online conversion tool converts models locally in the browser, indicating local handling of uploaded models during that workflow. | `E005` |

## 7. Constraints

| ID | Constraint | Source evidence |
|---|---|---|
| C-001 | Compilation is constrained to a CMake-based build approach for the documented quick cross-platform compilation path. | `E005` |
| C-002 | The pre-compiled model convert tool is constrained to Linux systems. | `E005` |
| C-003 | The online model convert tool depends on WebAssembly execution in the browser and performs local conversion there. | `E005` |
| C-004 | Example execution depends on the presence of local image and model assets under the project root folder. | `E002` |

## 8. Verification and Acceptance

| Requirement ID | Verification method | Acceptance basis |
|---|---|---|
| FR-001 | Inspection | Documented example programs exist for each listed task. |
| FR-002 | Demonstration | Running the classification example with required assets produces classification output via the compatible C API path. |
| FR-003 | Demonstration | An example runs successfully when images and models are placed under the root folder. |
| FR-004 | Inspection | C++ API documentation is present. |
| FR-005 | Inspection | Python API documentation is present. |
| FR-006 | Analysis | Serializer behavior and documentation show decoding of binary `tmfile` into serialized model parameters. |
| FR-007 | Inspection | Both Linux pre-compiled and online converter options are documented. |
| FR-008 | Demonstration | Online converter behavior shows model conversion occurs locally in-browser. |
| NFR-001 | Inspection | Build documentation states quick cross-platform compilation based on CMake. |
| NFR-002 | Demonstration | Documented example usage confirms compatibility with the original Tengine C API. |
| NFR-003 | Demonstration | Online conversion path is shown to be browser-local via WebAssembly. |
| NFR-004 | Inspection | Documentation identifies Linux as the platform for the pre-compiled converter. |

## 9. Traceability Matrix

| ID | Requirement | Type | Source | Evidence Type | Verification | Confidence |
|---|---|---|---|---|---|---|
| FR-001 | Provide documented example applications for listed tasks | Functional | `E001`, `E006` | explicit | Inspection | High |
| FR-002 | Run MobileNet v1 classification via original Tengine-compatible C API | Functional | `E001`, `E006` | explicit | Demonstration | High |
| FR-003 | Execute examples using local images and models under project root | Functional | `E002` | explicit | Demonstration | Medium |
| FR-004 | Provide documented C++ API | Functional | `E003` | explicit | Inspection | High |
| FR-005 | Provide documented Python API | Functional | `E004` | explicit | Inspection | High |
| FR-006 | Decode binary `tmfile` into serialized model parameters | Functional | `E005` | explicit | Analysis | High |
| FR-007 | Provide Linux and online model conversion tooling | Functional | `E005` | explicit | Inspection | High |
| FR-008 | Convert models locally in-browser through WebAssembly | Functional | `E005` | explicit | Demonstration | High |
| NFR-001 | Support quick cross-platform CMake compilation | Non-functional | `E005` | explicit | Inspection | High |
| NFR-002 | Maintain compatibility with original Tengine C API | Non-functional | `E001`, `E006` | explicit | Demonstration | High |
| NFR-003 | Perform online conversion locally in browser | Non-functional | `E005` | explicit | Demonstration | High |
| NFR-004 | Provide pre-compiled converter on Linux | Non-functional | `E005` | explicit | Inspection | High |
