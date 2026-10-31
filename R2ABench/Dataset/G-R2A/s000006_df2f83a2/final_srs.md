# Software Requirements Specification

## 1. Introduction

### Purpose
This SRS defines evidence-backed requirements for the `user-in-the-box` repository at commit `5a4bb88b7ad8462173923808ab30c58224ef40d0`. The specification covers the supported simulator-building, integration, and evaluation capabilities evidenced in the repository.

### Product scope
`user-in-the-box` provides source code for modeling and simulating HCI interaction tasks in MuJoCo. It supports user models with biomechanical actuation and perception capabilities, uses reinforcement learning in the overall workflow, and provides a modular way to assemble simulators as standalone packages that implement the OpenAI Gym interface. Simulators are built from YAML configuration files that select and integrate models and tasks. [E001, E003, E004]

### Intended audience
This document is intended for:
- Developers extending biomechanical, perception, or task modules
- Integrators building simulators from configuration
- Users evaluating trained simulator runs

### References
- Repository: `aikkala/user-in-the-box`
- Commit: `5a4bb88b7ad8462173923808ab30c58224ef40d0`
- Evidence sources:
  - `README.md` [E001, E003, E004]
  - `uitb/test/evaluator.py` [E002]
  - `uitb/bm_models/base.py` [E005, E006]

## 2. Overall Description

### Product perspective
The product is a simulator framework for HCI interaction tasks in MuJoCo. It is designed as a modular composition system where biomechanical models, perception modules, and interaction tasks are combined into standalone simulators. The resulting simulators expose the OpenAI Gym interface. [E001, E003, E004]

### Product functions summary
- Model and simulate HCI interaction tasks in MuJoCo [E001]
- Represent the user with a muscle-actuated biomechanical model and perception capabilities [E001]
- Support modular addition of new biomechanical models, perception models, and interaction tasks [E001, E004]
- Build simulators from YAML configuration files [E004]
- Package simulators as standalone shareable units [E001]
- Support evaluation runs from a stored run folder with evaluation output generation [E002]

### User classes
- Simulator builders configuring and assembling simulators from YAML [E004]
- Module developers creating new perception modules and other model/task extensions [E001, E004]
- Evaluators running stored training outputs for assessment [E002]

### Operating environment
- MuJoCo-based simulation environment [E001, E003]
- OpenAI Gym-compatible simulator interface [E001, E003]
- File-system environment capable of reading YAML configuration files and creating output directories [E002, E004]

### Assumptions and dependencies
- Simulator construction depends on a YAML configuration file that defines selected models to integrate. [E004]
- Simulators depend on MuJoCo XML integration during build. [E004]
- Evaluation depends on a run folder containing simulator artifacts and checkpoints. [E002]

## 3. External Interface Requirements

### User interfaces
No graphical user interface is evidenced. A command-line evaluation workflow is evidenced through arguments including `run_folder` and optional action-log output naming. [E002]

### Software/API interfaces
- Simulators shall implement the OpenAI Gym interface. [E001, E003]
- Perception extensions shall conform to the repository’s perception module structure and base-class contract when such modules are added. [E004]

### Communication interfaces
No network or inter-process communication interface is evidenced.

### Data exchange formats
- YAML shall be used for simulator configuration files. [E004]
- MuJoCo XML shall be used for simulator and biomechanical model integration during build. [E004]

## 4. Functional Requirements

| ID | Description | Trigger / Input | System behavior | Output | Priority | Verification | Source evidence |
|---|---|---|---|---|---|---|---|
| FR-001 | Build simulators from configuration | A YAML simulator configuration file is provided | The system shall build a simulator according to the YAML configuration by selecting and integrating the defined models and task components | A constructed simulator | High | Demonstration | E004 |
| FR-002 | Expose a Gym-compatible simulator interface | A simulator is produced by the system | The system shall provide the produced simulator as an implementation of the OpenAI Gym interface | A simulator usable through the Gym interface | High | Inspection | E001, E003 |
| FR-003 | Support modular extension of simulator components | A developer adds new biomechanical models, perception models, or interaction tasks | The system shall support adding these components through its modular structure so they can be integrated into simulator builds | Extendable simulator composition capability | Medium | Inspection | E001, E004 |
| FR-004 | Package simulators as standalone shareable units | A simulator has been built | The system shall produce simulators as standalone packages intended to be easily shared with others | Standalone simulator package | Medium | Demonstration | E001 |
| FR-005 | Support evaluation from a stored run folder | An evaluation is invoked with a `run_folder` | The system shall load a simulator from the specified run folder using evaluation run parameters and ensure an `evaluate` output directory exists under that run folder | Evaluation-ready simulator instance and evaluation output directory | Medium | Test | E002 |

## 5. Non-Functional Requirements

| ID | Quality attribute | Requirement | Priority | Verification | Evidence type | Source evidence |
|---|---|---|---|---|---|---|
| NFR-001 | Portability / interoperability | Produced simulators shall be interoperable with software expecting the OpenAI Gym interface. | High | Inspection | explicit | E001, E003 |
| NFR-002 | Modifiability | The system shall provide a modular structure for adding new biomechanical models, perception models, and interaction tasks without redefining the entire simulator workflow. | Medium | Inspection | explicit | E001, E004 |
| NFR-003 | Deployability | Produced simulators shall be organized as standalone packages suitable for sharing with other users. | Medium | Demonstration | explicit | E001 |

## 6. Data Requirements

| ID | Data item / entity | Requirement | Source evidence |
|---|---|---|---|
| DR-001 | Simulator configuration | The system shall accept simulator build definitions in YAML format. | E004 |
| DR-002 | MuJoCo model definitions | The build process shall use MuJoCo XML content for integrating biomechanical and simulator model definitions. | E004 |
| DR-003 | Action input values | Biomechanical action input values shall be represented in the range `[-1, 1]`. | E005 |
| DR-004 | Control signal values | Applied control values for motor and muscle actuators shall be constrained to the range `[0, 1]`. | E005 |
| DR-005 | Evaluation artifacts | Evaluation runs shall use a run folder containing checkpoints and shall write outputs under an `evaluate` directory. | E002 |

## 7. Constraints

| ID | Constraint | Source evidence |
|---|---|---|
| C-001 | The simulator domain is constrained to MuJoCo-based HCI interaction task simulation. | E001, E003 |
| C-002 | Simulator configuration is constrained to YAML-based definitions. | E004 |
| C-003 | Produced simulators are constrained to the OpenAI Gym interface contract. | E001, E003 |
| C-004 | Perception module extensions are constrained by the repository’s modality-based module organization and base-class inheritance model. | E004 |

## 8. Verification and Acceptance

| Requirement ID | Verification method | Acceptance criterion |
|---|---|---|
| FR-001 | Demonstration | A YAML configuration can be used to build a simulator composed from selected models. |
| FR-002 | Inspection | The produced simulator is shown to implement the OpenAI Gym interface. |
| FR-003 | Inspection | Repository structure and extension mechanism support adding the cited component types. |
| FR-004 | Demonstration | A built simulator is produced as a standalone package suitable for sharing. |
| FR-005 | Test | Invoking evaluation with a valid run folder creates the `evaluate` directory and loads the simulator with evaluation parameters. |
| NFR-001 | Inspection | The simulator interface is compatible with OpenAI Gym expectations. |
| NFR-002 | Inspection | The modular structure for the cited extension points is present and usable. |
| NFR-003 | Demonstration | A produced simulator can be handled as a standalone package. |
| DR-001 | Inspection | YAML is used as the simulator configuration format. |
| DR-002 | Inspection | MuJoCo XML is part of the build integration process. |
| DR-003 | Analysis | Action inputs are defined within `[-1, 1]`. |
| DR-004 | Analysis | Control outputs are constrained to `[0, 1]`. |
| DR-005 | Test | Evaluation uses checkpoint and evaluate paths under the run folder. |
| C-001 | Inspection | Product scope and interfaces remain MuJoCo-based. |
| C-002 | Inspection | Configuration input remains YAML-based. |
| C-003 | Inspection | Produced simulators remain Gym-interface implementations. |
| C-004 | Inspection | Perception extensions follow the evidenced structure and inheritance contract. |

## 9. Traceability Matrix

| ID | Requirement | Type | Source | Evidence Type | Verification | Confidence |
|---|---|---|---|---|---|---|
| FR-001 | Build simulators from YAML configuration | Functional | E004 | explicit | Demonstration | High |
| FR-002 | Expose OpenAI Gym interface | Functional | E001, E003 | explicit | Inspection | High |
| FR-003 | Support modular extension of simulator components | Functional | E001, E004 | explicit | Inspection | High |
| FR-004 | Produce standalone shareable simulator packages | Functional | E001 | explicit | Demonstration | Medium |
| FR-005 | Support evaluation from a stored run folder | Functional | E002 | explicit | Test | Medium |
| NFR-001 | Interoperate through OpenAI Gym interface | Non-functional | E001, E003 | explicit | Inspection | High |
| NFR-002 | Maintain modular extensibility | Non-functional | E001, E004 | explicit | Inspection | High |
| NFR-003 | Support standalone package sharing | Non-functional | E001 | explicit | Demonstration | Medium |
| DR-001 | Use YAML for simulator configuration | Data | E004 | explicit | Inspection | High |
| DR-002 | Use MuJoCo XML in model integration | Data | E004 | explicit | Inspection | Medium |
| DR-003 | Represent action input values in `[-1, 1]` | Data | E005 | explicit | Analysis | High |
| DR-004 | Constrain control values to `[0, 1]` | Data | E005 | explicit | Analysis | High |
| DR-005 | Use run-folder checkpoints and evaluation output directory | Data | E002 | explicit | Test | Medium |
| C-001 | Constrain product to MuJoCo-based HCI task simulation | Constraint | E001, E003 | explicit | Inspection | High |
| C-002 | Constrain configuration format to YAML | Constraint | E004 | explicit | Inspection | High |
| C-003 | Constrain simulator interface to OpenAI Gym | Constraint | E001, E003 | explicit | Inspection | High |
| C-004 | Constrain perception extensions to repository structure and base contract | Constraint | E004 | explicit | Inspection | Medium |
