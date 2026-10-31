# Software Requirements Specification

## 1. Introduction

### 1.1 Purpose
This SRS defines the final checked requirements for the User-in-the-box simulator framework. It is prepared as a clean requirements input for downstream architecture diagram generation.

### 1.2 Product Scope
User-in-the-box is a framework for modeling, building, training, packaging, and evaluating MuJoCo-based simulators for HCI interaction tasks. The system supports:
- Muscle-actuated biomechanical user models.
- Perception modalities including egocentric vision and proprioception.
- Interaction tasks assembled with biomechanical and perception components.
- Reinforcement-learning training of biomechanical user models or control policies for configured interaction tasks.
- Simulator construction from YAML configuration files.
- MuJoCo XML integration for biomechanical models and interaction-task environments.
- OpenAI Gym-compatible simulator packages.
- Evaluation of trained simulator runs from stored run folders.

### 1.3 Intended Audience
- Developers extending biomechanical models, perception modules, or interaction tasks.
- Integrators assembling simulators from configuration.
- Researchers or engineers training user models with reinforcement learning.
- Evaluators running stored simulator outputs for assessment.
- Architecture reviewers generating or validating architecture diagrams.

### 1.4 Terminology
| Term | Definition |
|---|---|
| Simulator | A standalone package produced by the framework that implements the OpenAI Gym interface. |
| Biomechanical model | A MuJoCo-based model representing the user body and actuation behavior. |
| Perception module | A component that provides a perception modality, such as egocentric vision or proprioception. |
| Interaction task | The task environment the user model is trained or evaluated to solve. |
| Run folder | A stored run directory used by evaluation, including checkpoint and evaluation-output locations. |
| Action log | Evaluation-time output recording actions when logging is enabled. |

## 2. Overall Description

### 2.1 Product Perspective
The system is a modular simulator composition framework for HCI interaction tasks in MuJoCo. It combines biomechanical models, perception modules, and interaction tasks into standalone simulator packages. Produced simulators implement the OpenAI Gym interface and can be trained or evaluated using reinforcement-learning workflows.

### 2.2 Architecture Context
The architecture context for diagram generation includes:
- YAML simulator configuration.
- Simulator builder.
- MuJoCo XML integration layer.
- Biomechanical model modules.
- Perception modules organized by modality.
- Interaction task modules.
- Reinforcement-learning training workflow.
- Standalone Gym-compatible simulator package.
- Evaluation runner.
- Run-folder artifacts, including checkpoint and evaluation-output directories.

### 2.3 Product Functions
- Build simulators from YAML configuration files.
- Integrate biomechanical MuJoCo XML with interaction-task MuJoCo XML as part of simulator construction.
- Initialize selected biomechanical model, task, and perception wrapper components.
- Expose produced simulators through the OpenAI Gym interface.
- Support modular extension with new biomechanical models, perception modules, and interaction tasks.
- Support perception modalities including egocentric vision and proprioception.
- Train biomechanical user models or control policies with reinforcement learning for configured interaction tasks.
- Package built simulators as self-contained standalone packages.
- Evaluate stored training runs from a run folder.
- Create an evaluation output directory when needed.
- Load specified or latest model checkpoints during evaluation.
- Write action logs when evaluation logging is enabled.

### 2.4 User Classes
| User Class | Description |
|---|---|
| Simulator builder | Configures and assembles simulators from YAML files. |
| Module developer | Adds or modifies biomechanical models, perception modules, or interaction tasks. |
| Training user | Runs reinforcement-learning workflows for configured simulators. |
| Evaluator | Runs evaluation using stored training outputs and generated evaluation artifacts. |

### 2.5 Operating Environment
- MuJoCo-based simulation environment.
- OpenAI Gym-compatible runtime interface.
- File-system access to YAML configuration files.
- File-system access to run folders, checkpoint directories, and evaluation-output directories.
- Python execution environment for simulator building, training, and evaluation.

### 2.6 Assumptions and Dependencies
- Simulator construction depends on YAML configuration.
- Simulator construction depends on MuJoCo XML integration.
- Perception module extensions follow the framework's modality-based organization and base-class inheritance contract.
- Evaluation depends on a run folder containing the artifacts needed to load a simulator and model checkpoint.
- Action logging occurs only when evaluation logging is enabled.

## 3. External Interface Requirements

### 3.1 User Interfaces
No graphical user interface is required by this SRS.

The system shall provide command-line or script-based evaluation inputs including:
- Run folder path.
- Optional checkpoint selection.
- Optional action log file name.
- Logging and recording options where supported.

### 3.2 Software/API Interfaces
| Interface | Requirement |
|---|---|
| OpenAI Gym interface | Produced simulators shall implement the OpenAI Gym interface. |
| Simulator builder interface | The framework shall accept YAML simulator configuration files and construct simulators from them. |
| Perception extension interface | New perception modules shall follow the modality-based module organization and inherit from the required base module contract. |
| Biomechanical model interface | Biomechanical models shall support MuJoCo XML integration and control-value application. |
| Evaluation runner interface | Evaluation shall accept a stored run folder and evaluation parameters. |

### 3.3 Communication Interfaces
No network or inter-process communication interface is required by this SRS.

### 3.4 Data Exchange Formats
| Format | Requirement |
|---|---|
| YAML | Simulator build definitions shall use YAML configuration. |
| MuJoCo XML | Biomechanical model and simulator environment integration shall use MuJoCo XML. |
| OpenAI Gym API | Runtime simulator interaction shall follow the Gym-compatible API contract. |
| File-system artifacts | Evaluation shall read run-folder artifacts and write evaluation outputs under the run folder. |

## 4. Functional Requirements

| ID | Requirement | Trigger/Input | System Behavior | Output | Priority | Verification |
|---|---|---|---|---|---|---|
| FR-001 | Build simulators from configuration | A YAML simulator configuration file is provided. | The system shall build a simulator by selecting and integrating the configured model and task components. The build process shall first integrate the biomechanical model's MuJoCo XML into the interaction task environment's MuJoCo XML to generate a standalone MuJoCo XML, and then call the relevant wrapper classes to initialize the selected biomechanical model, task, and perception components. | Constructed simulator. | High | Demonstration |
| FR-002 | Expose Gym-compatible simulator interface | A simulator is produced by the system. | The system shall provide the produced simulator as an implementation of the OpenAI Gym interface. | Simulator usable through the Gym interface. | High | Inspection |
| FR-003 | Support modular extension of simulator components | A developer adds a new biomechanical model, perception module, or interaction task. | The system shall support adding these components through the modular framework structure so they can be integrated into simulator builds. | Extendable simulator composition capability. | Medium | Inspection |
| FR-004 | Package simulators as standalone units | A simulator has been built. | The system shall produce the simulator as a self-contained package that can be independently loaded and run as a Gym-compatible simulator. | Standalone simulator package. | Medium | Demonstration |
| FR-005 | Support evaluation from a stored run folder | Evaluation is invoked with a run folder. | The system shall load a simulator from the run folder using evaluation run parameters, reference the checkpoint directory under that run folder to load the specified or latest model checkpoint, and ensure an `evaluate` directory exists under the run folder. | Evaluation-ready simulator instance and evaluation output directory. | Medium | Test |
| FR-006 | Train user models with reinforcement learning | A YAML simulator configuration file containing training configuration is provided. | The system shall build the simulator from configuration and train the biomechanical user model or control policy with the configured reinforcement-learning algorithm to solve the interaction task. | Training run output and model checkpoint artifacts. | Medium | Demonstration |
| FR-007 | Log actions during evaluation | Evaluation is invoked with logging enabled. | The system shall write an action log to the configured action log file when logging is enabled. | Action log file. | Low | Test |

## 5. Non-Functional Requirements

| ID | Quality Attribute | Requirement | Priority | Verification |
|---|---|---|---|---|
| NFR-001 | Interoperability | Produced simulators shall be interoperable with software expecting the OpenAI Gym interface. | High | Inspection |
| NFR-002 | Modifiability | The system shall provide a modular structure for adding new biomechanical models, perception modules, and interaction tasks without redefining the entire simulator workflow. | Medium | Inspection |
| NFR-003 | Deployability | Produced simulators shall be self-contained standalone packages that can be independently loaded and run as Gym-compatible simulators. | Medium | Demonstration |
| NFR-004 | Evaluation reproducibility | Evaluation shall use run-folder artifacts and deterministic evaluation parameters where configured by the evaluation workflow. | Medium | Test |

## 6. Data Requirements

### 6.1 Data Entities and Artifacts
| ID | Data Item | Requirement |
|---|---|---|
| DR-001 | Simulator configuration | The system shall accept simulator build definitions in YAML format. |
| DR-002 | MuJoCo model definitions | The build process shall use MuJoCo XML content for integrating biomechanical model and simulator environment definitions. |
| DR-003 | Action input values | Biomechanical action input values shall be represented in the range `[-1, 1]`. |
| DR-004 | Control signal values | Applied control values for motor and muscle actuators shall be constrained to the range `[0, 1]`. |
| DR-005 | Evaluation artifacts | An evaluation run shall take a run folder as input, reference the `checkpoints` directory under that run folder to load the specified or latest model checkpoint, and ensure that an `evaluate` directory exists under that run folder. When logging or recording is enabled, evaluation outputs shall be written to the `evaluate` directory. |
| DR-006 | Action log | When evaluation logging is enabled, action data shall be written to the configured action log file. |
| DR-007 | Perception modality data | Perception components shall support modality-specific data paths for modalities such as vision and proprioception. |
| DR-008 | Training artifacts | Reinforcement-learning training shall produce training run artifacts and model checkpoint artifacts. |

### 6.2 Input and Output Data
| Data Flow | Requirement |
|---|---|
| YAML configuration input | Simulator construction shall read selected model, task, perception, and training configuration from YAML. |
| MuJoCo XML integration input | Simulator construction shall read biomechanical and interaction-task MuJoCo XML definitions. |
| Action input | Biomechanical control application shall accept action values within the defined action input range. |
| Control output | Applied actuator controls shall remain within the defined control range. |
| Evaluation input | Evaluation shall accept a run folder and optional checkpoint/logging parameters. |
| Evaluation output | Evaluation shall write enabled logs, recordings, and other evaluation artifacts under the evaluation output directory. |

### 6.3 Storage, Integrity, Privacy, Retention, and Migration
| Topic | Requirement |
|---|---|
| Run-folder structure | Run folders shall contain or reference the artifacts needed for simulator loading, checkpoint loading, and evaluation output. |
| Evaluation output organization | Evaluation outputs shall be organized under the `evaluate` directory in the run folder. |
| Standalone simulator packaging | Built simulator packages shall include the components needed to load and run the simulator independently. |
| Privacy, retention, and migration | Privacy, retention, deletion, and migration behavior are not specified in this SRS. |

## 7. System Constraints

| ID | Constraint |
|---|---|
| C-001 | The simulator domain is constrained to MuJoCo-based HCI interaction task simulation. |
| C-002 | Simulator configuration is constrained to YAML-based definitions. |
| C-003 | Produced simulators are constrained to the OpenAI Gym interface contract. |
| C-004 | Perception module extensions are constrained by modality-based module organization and base-class inheritance. |
| C-005 | Biomechanical action values are constrained to `[-1, 1]`. |
| C-006 | Applied motor and muscle actuator control values are constrained to `[0, 1]`. |
| C-007 | Evaluation depends on a valid run-folder structure. |

## 8. Verification and Acceptance Criteria

| Requirement ID | Verification Method | Acceptance Criteria |
|---|---|---|
| FR-001 | Demonstration | A YAML configuration builds a simulator by integrating MuJoCo XML and initializing the selected biomechanical, task, and perception components. |
| FR-002 | Inspection | The produced simulator implements the OpenAI Gym interface. |
| FR-003 | Inspection | The framework structure supports adding new biomechanical models, perception modules, and interaction tasks. |
| FR-004 | Demonstration | A built simulator is produced as a self-contained package that can be independently loaded and run as a Gym-compatible simulator. |
| FR-005 | Test | Evaluation with a valid run folder loads the simulator, references the checkpoint directory, and creates the `evaluate` directory if absent. |
| FR-006 | Demonstration | A configured simulator can be used in a reinforcement-learning training workflow that produces training run output and model checkpoint artifacts. |
| FR-007 | Test | Evaluation with logging enabled writes an action log to the configured file. |
| NFR-001 | Inspection | Simulator interfaces are compatible with OpenAI Gym expectations. |
| NFR-002 | Inspection | The modular extension points for biomechanical, perception, and task components are present and usable. |
| NFR-003 | Demonstration | A produced simulator can be handled as an independently loadable standalone package. |
| NFR-004 | Test | Evaluation uses run-folder artifacts and configured evaluation parameters. |
| DR-001 | Inspection | YAML is used as the simulator configuration format. |
| DR-002 | Inspection | MuJoCo XML is part of the model and simulator environment integration process. |
| DR-003 | Analysis | Action inputs are defined within `[-1, 1]`. |
| DR-004 | Analysis | Applied control outputs are constrained to `[0, 1]`. |
| DR-005 | Test | Evaluation references checkpoint artifacts and writes enabled outputs under the `evaluate` directory. |
| DR-006 | Test | Action logging produces the configured action log when logging is enabled. |
| DR-007 | Inspection | Perception modules are organized by modality, including vision and proprioception examples. |
| DR-008 | Demonstration | Reinforcement-learning training produces training run and model checkpoint artifacts. |
| C-001 | Inspection | Product scope and interfaces remain MuJoCo-based. |
| C-002 | Inspection | Configuration input remains YAML-based. |
| C-003 | Inspection | Produced simulators remain Gym-interface implementations. |
| C-004 | Inspection | Perception extensions follow modality-based organization and base-class inheritance. |
| C-005 | Analysis | Biomechanical action inputs remain within `[-1, 1]`. |
| C-006 | Analysis | Applied motor and muscle actuator controls remain within `[0, 1]`. |
| C-007 | Test | Evaluation requires a valid run-folder structure for simulator and checkpoint loading. |
