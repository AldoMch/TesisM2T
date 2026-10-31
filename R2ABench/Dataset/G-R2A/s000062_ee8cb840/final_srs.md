# Software Requirements Specification

## 1. Introduction

### Purpose
This SRS defines evidence-backed requirements for the repository component represented by the Udacity Self-Driving Car Engineer Capstone system integration project. It focuses on launch, simulation execution, waypoint following, speed compliance, and real-world test workflow supported by the repository evidence. Sources: `E001`, `E002`.

### Product scope
The product is a self-driving car project submission intended to run through provided launch files in simulator mode and site mode, follow waypoints smoothly in the simulator, respect waypoint-defined target speed, and support real-world testing with a recorded training bag and traffic light detection validation. Sources: `E001`, `E002`.

### Intended audience
This document is intended for evaluators, developers, and operators who build, launch, test, or assess the repository in simulator or site mode. Sources: `E001`, `E002`.

### References
- Repository: `KuangRD/Autonomous-Driving`
- Commit: `01c3dbd42c52edf3cbca56f724fdf1e48abf2908`
- Evidence source: `Self-DrivingCarND/Projects/Term3/CarND-Capstone/README.md` (`E001`, `E002`)

## 2. Overall Description

### Product perspective
The repository provides a project workflow around a ROS-based capstone environment launched from predefined launch files and exercised either through the Udacity simulator or through recorded real-world bag playback. The documented setup uses Docker and ROS as execution dependencies. Sources: `E001`, `E002`.

### Product functions summary
- Launch the system using repository-provided launch files for simulator and vehicle/site modes. `E001`
- Follow waypoints smoothly in the simulator. `E001`
- Respect target top speed carried in waypoint `twist.twist.linear.x` values. `E001`
- Support simulator execution after ROS launch. `E002`
- Support real-world testing using a downloaded and unzipped training bag played back in site mode. `E002`
- Validate traffic light detection on real-life images during site-mode testing. `E002`

### User classes
- `Evaluator`: runs the provided launch files to test the submission in simulator and site modes. `E001`
- `Developer/Operator`: builds Docker, launches ROS, runs the simulator, and performs bag-based real-world testing. `E002`

### Operating environment
- Docker environment for project build and execution. `E002`
- ROS environment inside the container. `E002`
- Udacity Capstone Project Simulator for simulator-based execution. `E002`
- Site mode with recorded training bag for real-world test playback. `E002`

### Assumptions and dependencies
- Docker must be installed before building and running the project container. `E002`
- The Udacity simulator must be downloaded, extracted, and made runnable before simulator testing. `E002`
- Real-world testing depends on availability of the recorded training bag and bag playback tooling. `E002`
- Evaluation uses `launch/styx.launch` for simulator testing and `launch/site.launch` for vehicle/site testing. `E001`

## 3. External Interface Requirements

| Interface area | Requirement summary | Source evidence |
|---|---|---|
| User interfaces | The system shall be operable through documented command-line launch steps after entering the Docker container and launching ROS. | `E002` |
| Software/API interfaces | The system shall integrate with Docker, ROS, and the Udacity Capstone Project Simulator. | `E002` |
| Software/API interfaces | The system shall expose execution entry points through `launch/styx.launch` and `launch/site.launch`. | `E001` |
| Communication interfaces | The system shall support playback-based interaction with a recorded training bag during real-world testing. | `E002` |
| Data exchange formats | The system shall consume waypoint data containing target speed in `twist.twist.linear.x`. | `E001` |
| Data exchange formats | The system shall support compressed/distributed training bag content that is downloaded and unzipped before playback. | `E002` |

## 4. Functional Requirements

| ID | Description | Trigger/Input | System behavior | Output | Priority | Verification | Source evidence |
|---|---|---|---|---|---|---|---|
| FR-001 | Launch using provided entry points | Operator launches the project for evaluation | The system shall launch correctly using the repository-provided launch files without requiring special launch instructions or additional download scripts. | Running system in the selected mode | High | Demonstration | `E001` |
| FR-002 | Support simulator mode | Operator starts simulator testing | The system shall support execution via `launch/styx.launch` for simulator-based testing. | Active simulator-mode run | High | Demonstration | `E001` |
| FR-003 | Support site mode | Operator starts site/vehicle testing | The system shall support execution via `launch/site.launch` for site-mode testing. | Active site-mode run | High | Demonstration | `E001` |
| FR-004 | Follow waypoints in simulator | Simulator provides waypoint path | The system shall smoothly follow the provided waypoints in the simulator. | Vehicle remains on waypoint path in simulation | High | Test | `E001` |
| FR-005 | Respect waypoint target speed | Waypoint data includes `twist.twist.linear.x` target speed values | The system shall respect the target top speed defined in waypoint `twist.twist.linear.x`. | Vehicle speed remains consistent with waypoint target top speed | High | Test | `E001` |
| FR-006 | Support ROS launch workflow | Operator enters the Docker container and executes ROS launch steps | The system shall be launchable after ROS startup in the documented container workflow. | ROS-based project execution begins | Medium | Demonstration | `E002` |
| FR-007 | Support simulator application workflow | Operator downloads, extracts, and runs the simulator | The system shall interoperate with the Udacity Capstone Project Simulator during testing. | Connected simulator-based test session | Medium | Demonstration | `E002` |
| FR-008 | Support recorded bag playback in site mode | Operator downloads, unzips, and plays the recorded training bag | The system shall operate in site mode during playback of the recorded Udacity self-driving car training bag. | Active site-mode test using recorded data | Medium | Demonstration | `E002` |
| FR-009 | Detect traffic lights on real-life images during real-world testing | Real-world bag playback provides real-life image data | The system shall support traffic light detection validation on real-life images in site mode. | Observable traffic light detection during playback | High | Test | `E002` |

## 5. Non-Functional Requirements

| ID | Quality attribute | Requirement | Priority | Verification | Source evidence | Evidence type |
|---|---|---|---|---|---|---|
| NFR-001 | Compatibility | The system shall be compatible with the repository-provided launch files used by evaluation: `launch/styx.launch` and `launch/site.launch`. | High | Inspection | `E001` | explicit |
| NFR-002 | Deployability | The system shall be deployable within a Docker-based environment as documented by the setup workflow. | High | Demonstration | `E002` | explicit |
| NFR-003 | Usability | The system shall not require evaluators to perform special launch instructions or run additional scripts to download files beyond the documented workflow. | High | Inspection | `E001` | explicit |
| NFR-004 | Performance/behavioral quality | In simulator operation, motion behavior shall be smooth while following waypoints. | High | Test | `E001` | explicit |
| NFR-005 | Capacity constraint | The project submission artifact shall not exceed 2 GB. | Medium | Inspection | `E001` | explicit |

## 6. Data Requirements

| ID | Data item/entity | Requirement | Source evidence |
|---|---|---|---|
| DR-001 | Waypoints | Waypoint data shall include target speed values in `twist.twist.linear.x`, and the system shall consume these values for speed control behavior. | `E001` |
| DR-002 | Training bag | Real-world testing shall use a recorded training bag from the Udacity self-driving car, obtained by download and unzip prior to playback. | `E002` |
| DR-003 | Real-life image data | Site-mode validation shall use real-life images from the recorded data to confirm traffic light detection behavior. | `E002` |

## 7. Constraints

| ID | Constraint | Source evidence |
|---|---|---|
| C-001 | Evaluation is constrained to the provided launch files; alternative launch procedures are not assumed. | `E001` |
| C-002 | Additional scripts for downloading files are not accommodated in evaluation. | `E001` |
| C-003 | Docker installation is a prerequisite for environment setup. | `E002` |
| C-004 | ROS must be launched from within the prepared container workflow. | `E002` |
| C-005 | Simulator testing depends on the Udacity Capstone Project Simulator being downloaded, extracted, and made runnable. | `E002` |
| C-006 | Real-world testing depends on obtaining and playing back the recorded training bag in site mode. | `E002` |
| C-007 | Submission size is limited to 2 GB. | `E001` |

## 8. Verification and Acceptance

| Requirement ID | Verification method | Acceptance basis |
|---|---|---|
| FR-001 | Demonstration | Project launches successfully using provided launch files only. |
| FR-002 | Demonstration | `launch/styx.launch` starts a simulator-mode run. |
| FR-003 | Demonstration | `launch/site.launch` starts a site-mode run. |
| FR-004 | Test | In simulator execution, waypoint following is smooth. |
| FR-005 | Test | Observed top speed conforms to waypoint `twist.twist.linear.x` targets. |
| FR-006 | Demonstration | ROS launch workflow operates inside the Docker container. |
| FR-007 | Demonstration | System runs with the Udacity simulator. |
| FR-008 | Demonstration | System runs in site mode while a recorded bag is played back. |
| FR-009 | Test | Traffic light detection can be confirmed on real-life images during site-mode playback. |
| NFR-001 | Inspection | Required launch files are the supported evaluation interfaces. |
| NFR-002 | Demonstration | Documented Docker setup produces a runnable environment. |
| NFR-003 | Inspection | No extra launch/download scripts are required beyond documented workflow. |
| NFR-004 | Test | Simulator motion is smooth during waypoint following. |
| NFR-005 | Inspection | Submission size is at or below 2 GB. |

## 9. Traceability Matrix

| ID | Requirement | Type | Source | Evidence Type | Verification | Confidence |
|---|---|---|---|---|---|---|
| FR-001 | Launch using provided entry points only | Functional | `E001` | explicit | Demonstration | High |
| FR-002 | Support simulator mode through `launch/styx.launch` | Functional | `E001` | explicit | Demonstration | High |
| FR-003 | Support site mode through `launch/site.launch` | Functional | `E001` | explicit | Demonstration | High |
| FR-004 | Smoothly follow waypoints in simulator | Functional | `E001` | explicit | Test | High |
| FR-005 | Respect waypoint target top speed | Functional | `E001` | explicit | Test | Medium |
| FR-006 | Support ROS launch workflow in container | Functional | `E002` | explicit | Demonstration | Medium |
| FR-007 | Interoperate with Udacity simulator | Functional | `E002` | explicit | Demonstration | Medium |
| FR-008 | Support recorded bag playback in site mode | Functional | `E002` | explicit | Demonstration | Medium |
| FR-009 | Support traffic light detection validation on real-life images | Functional | `E002` | explicit | Test | Medium |
| NFR-001 | Compatibility with provided launch files | Non-functional | `E001` | explicit | Inspection | High |
| NFR-002 | Docker-based deployability | Non-functional | `E002` | explicit | Demonstration | High |
| NFR-003 | No special launch instructions or extra download scripts | Non-functional | `E001` | explicit | Inspection | High |
| NFR-004 | Smooth motion quality in simulator | Non-functional | `E001` | explicit | Test | High |
| NFR-005 | Submission size at or below 2 GB | Non-functional | `E001` | explicit | Inspection | High |
| DR-001 | Waypoint target speed data in `twist.twist.linear.x` | Data | `E001` | explicit | Inspection | Medium |
| DR-002 | Recorded training bag for real-world testing | Data | `E002` | explicit | Inspection | High |
| DR-003 | Real-life image data for traffic light detection validation | Data | `E002` | explicit | Inspection | Medium |
