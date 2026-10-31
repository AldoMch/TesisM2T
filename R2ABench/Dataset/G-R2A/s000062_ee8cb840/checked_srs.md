# Software Requirements Specification

## 1. Introduction

### Purpose
This SRS defines repository-backed software requirements for the Udacity Self-Driving Car Engineer Capstone system integration project. The requirements are derived from the project rubric and documented setup workflow and therefore represent evaluation and acceptance goals supported by the repository materials, rather than independently verified claims of implemented performance.

### Product scope
The product is a ROS-based self-driving car system integration project intended to:
- launch in simulator mode and site mode through repository-provided launch entry points,
- operate within the documented Docker and ROS workflow,
- follow provided waypoints in the simulator,
- respect waypoint-defined target speed,
- detect and classify traffic lights on real images during site-mode playback,
- produce stop-related behavior for red or yellow traffic lights through traffic waypoint outputs,
- support real-world testing using a recorded training bag.

### Intended audience
This document is intended for:
- developers maintaining or extending the project,
- evaluators validating rubric-aligned behavior,
- operators running simulator-mode or site-mode demonstrations.

## 2. Overall Description

### Product perspective
The repository provides a ROS-based capstone environment launched from predefined launch files and exercised either through the Udacity simulator or through recorded real-world bag playback. The documented setup uses Docker and ROS as execution dependencies.

### System architecture
The system uses a ROS multi-node architecture organized around perception, planning, and control subsystems.
- The perception subsystem is responsible for traffic light detection and classification and for producing stop-related waypoint information.
- The planning subsystem generates final waypoints using waypoint loading and waypoint updating functions.
- The control subsystem generates throttle, steering, and brake commands through waypoint-following and drive-by-wire control nodes.
- Nodes exchange data through ROS topics including current pose, base waypoints, traffic waypoint, final waypoints, twist command, and vehicle command.

### Product functions summary
- Launch the system using repository-provided launch files for simulator and site modes.
- Follow waypoints during simulator operation.
- Respect target top speed carried in waypoint `twist.twist.linear.x` values.
- Support simulator execution after ROS launch.
- Support real-world testing using a downloaded and unzipped training bag played back in site mode.
- Detect and classify traffic lights on real-life images during site-mode testing.
- Produce stop-related waypoint output when a red or yellow light requires stopping.

### User classes
- `Evaluator`: runs the provided launch files to assess simulator-mode and site-mode behavior.
- `Developer/Operator`: builds Docker, launches ROS, runs the simulator, and performs bag-based real-world testing.

### Operating environment
- Docker environment for project build and execution.
- ROS environment inside the container.
- Udacity Capstone Project Simulator for simulator-based execution.
- Site mode with recorded training bag for real-world test playback.

### Assumptions and dependencies
- Docker must be installed before building and running the project container.
- The simulator must be downloaded, extracted, and made runnable before simulator testing.
- Real-world testing depends on availability of the recorded training bag and bag playback tooling.
- Evaluation uses `launch/styx.launch` for simulator testing and `launch/site.launch` for site-mode testing.

## 3. External Interface Requirements

### User interfaces
- The system shall be operable through documented command-line launch steps after entering the Docker container and launching ROS.

### Software and API interfaces
- The system shall integrate with Docker, ROS, and the Udacity Capstone Project Simulator.
- The system shall expose execution entry points through `launch/styx.launch` and `launch/site.launch`.
- The system shall provide ROS-node interfaces for perception, planning, and control functions.
- The system shall exchange data across ROS topics including current pose, base waypoints, traffic waypoint, final waypoints, twist command, and vehicle command.

### Communication interfaces
- The system shall support playback-based interaction with a recorded training bag during site-mode testing.

### Data exchange formats
- The system shall consume waypoint data containing target speed in `twist.twist.linear.x`.
- The system shall support training bag content that is downloaded and unzipped before playback.
- The system shall process real-image traffic light inputs and produce traffic light state classification and stop-related waypoint outputs.

## 4. Functional Requirements

### FR-001 Launch through repository-provided entry points
The system shall launch the corresponding runtime mode through the simulator and site launch entry points provided by the repository.

Verification: Demonstration  
Acceptance criteria: `launch/styx.launch` starts simulator mode and `launch/site.launch` starts site mode.

### FR-002 Support simulator mode
The system shall support execution via `launch/styx.launch` for simulator-based testing.

Verification: Demonstration  
Acceptance criteria: A simulator-mode run can be started through `launch/styx.launch`.

### FR-003 Support site mode
The system shall support execution via `launch/site.launch` for site-mode testing.

Verification: Demonstration  
Acceptance criteria: A site-mode run can be started through `launch/site.launch`.

### FR-004 Follow waypoints during simulator operation
During simulation demonstration, the system shall be able to drive along the provided waypoints.

Verification: Demonstration / qualitative review  
Acceptance criteria: During simulator operation, reviewers can observe the vehicle following the waypoint path. No quantitative smoothness threshold is defined by the available source material.

### FR-005 Respect waypoint target speed
The system shall respect the target top speed set by the waypoint velocity parameter; vehicle speed shall not exceed the target top speed represented by each waypoint's `twist.twist.linear.x` value.

Verification: Demonstration  
Acceptance criteria: When the waypoint velocity parameter is changed, reviewers can observe that vehicle speed respects the target top speed and does not exceed the waypoint-defined upper bound.

### FR-006 Support ROS launch workflow
The system shall be launchable after ROS startup in the documented container workflow.

Verification: Demonstration  
Acceptance criteria: ROS-based project execution begins successfully inside the documented container workflow.

### FR-007 Support simulator application workflow
The system shall interoperate with the Udacity Capstone Project Simulator during testing.

Verification: Demonstration  
Acceptance criteria: The project runs with the simulator in an observable simulator test session.

### FR-008 Support recorded bag playback in site mode
The system shall operate in site mode during playback of the recorded training bag.

Verification: Demonstration  
Acceptance criteria: The system runs in site mode while the recorded bag is played back.

### FR-009 Perform traffic light detection and classification during site-mode playback
The system shall perform traffic light detection and state classification on real images during site-mode bag playback and, when stopping is required for a red or yellow light, shall output the corresponding stop-related waypoint.

Verification: Demonstration / qualitative review  
Acceptance criteria: During real bag playback, traffic light state classification and red-light or yellow-light stop-related output are observable. No quantitative detection accuracy threshold is defined by the available source material.

## 5. Non-Functional Requirements

### NFR-001 Compatibility
The system shall be compatible with the repository-provided launch files `launch/styx.launch` and `launch/site.launch`.

Verification: Inspection  
Acceptance criteria: The documented evaluation entry points are the supported launch interfaces.

### NFR-002 Deployability
The system shall be deployable within the documented Docker-based environment.

Verification: Demonstration  
Acceptance criteria: The documented Docker setup produces a runnable environment.

## 6. Data Requirements

### DR-001 Waypoint target speed data
`twist.twist.linear.x` in waypoint data shall represent the target top speed, and the system shall use it as the upper bound for speed control.

### DR-002 Training bag data
Real-world testing shall use a recorded training bag obtained by download and unzip prior to playback.

### DR-003 Traffic light image and classification data
Site-mode validation shall use real images from recorded data and shall produce traffic light state classification results and stop-related waypoint output.

## 7. System Constraints

### C-001 Launch procedure constraint
Evaluation is constrained to the repository-provided launch files; alternative launch procedures are not assumed.

### C-002 Submission workflow constraint
Evaluation does not accommodate special launch instructions or additional scripts to download files beyond the documented workflow.

### C-003 Environment prerequisite
Docker installation is a prerequisite for environment setup.

### C-004 Runtime workflow constraint
ROS must be launched from within the prepared container workflow.

### C-005 Simulator dependency
Simulator testing depends on the simulator being downloaded, extracted, and made runnable.

### C-006 Real-world test dependency
Real-world testing depends on obtaining and playing back the recorded training bag in site mode.

### C-007 Deliverable size constraint
The submitted deliverable size shall not exceed 2 GB.

## 8. Verification and Acceptance Criteria

| Requirement ID | Verification method | Acceptance criterion |
|---|---|---|
| FR-001 | Demonstration | `launch/styx.launch` starts simulator mode and `launch/site.launch` starts site mode. |
| FR-002 | Demonstration | A simulator-mode run can be started through `launch/styx.launch`. |
| FR-003 | Demonstration | A site-mode run can be started through `launch/site.launch`. |
| FR-004 | Demonstration / qualitative review | During simulator operation, reviewers can observe the vehicle following the waypoint path; no quantitative smoothness threshold is defined by the available source material. |
| FR-005 | Demonstration | When the waypoint velocity parameter is changed, vehicle speed respects the target top speed and does not exceed the waypoint-defined upper bound. |
| FR-006 | Demonstration | ROS-based project execution begins successfully inside the documented container workflow. |
| FR-007 | Demonstration | The project runs with the simulator in an observable simulator test session. |
| FR-008 | Demonstration | The system runs in site mode while the recorded bag is played back. |
| FR-009 | Demonstration / qualitative review | During real bag playback, traffic light state classification and red-light or yellow-light stop-related output are observable; no quantitative detection accuracy threshold is defined by the available source material. |
| NFR-001 | Inspection | The documented evaluation entry points are the supported launch interfaces. |
| NFR-002 | Demonstration | The documented Docker setup produces a runnable environment. |
