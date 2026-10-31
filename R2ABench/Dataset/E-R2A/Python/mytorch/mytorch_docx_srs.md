# MyTorch Software Requirements Specification (Standard SRS Extract)

## 1. Introduction

### Purpose

This document extracts verifiable requirements from `Group 24G Software Requirements Specification v1.4.docx` and rewrites them according to the compact SRS standard in `architectural_views_rep-pkg/script/templates/SRS.md`. The goal is to provide structured input for architecture generation, test design, and requirements tracing for the MyTorch deep learning framework extension and visual training/inference system. Source evidence is recorded in `mytorch_docx_evidence_pack.json`. (Source: MYT-001)

### Product Scope

The MyTorch project targets deep learning learners. By continuously improving and extending the MyTorch/NNE framework, it provides framework enhancement capabilities and a visual training/inference system. The system scope includes model configuration, data loading, model training, model inference, GPU acceleration, model weight initialization, classic model introduction, preset datasets, back-end interfaces, front-end interfaces, and local database persistence. (Source: MYT-002, MYT-005, MYT-009)

This document follows the terminology definitions in the source requirements document for deep learning, neural networks, data augmentation, data loaders, model structures, loss functions, optimizers, learning rates, weight initialization, GPU acceleration, batches, and model deployment. (Source: MYT-003)

### Intended Audience

This document is intended for developers, team members, teachers, classmates, project stakeholders, and later architecture generation and test review workflows. The source document particularly emphasizes unifying understanding during development and testing, communicating requirements, and evaluating project progress. (Source: MYT-001)

### References

| Ref | Source |
| --- | --- |
| REF-001 | GB/T 8567-1988 Computer Software Requirements Specification |

## 2. Overall Description

### Product Perspective

The system consists of MyTorch/NNE framework extension, visual front end, system back end, and SQLite local database. The front end provides a main interface, configuration interface, training interface, and inference interface. The back end calls the MyTorch deep learning framework and provides interfaces for model initialization, model training, task inference, and model management. The database persists deep learning models, training datasets, training logs, and inference logs. The source document does not expand the concrete Web framework, API paths, database table structure, or front-end technology stack. (Source: MYT-005, MYT-006, MYT-007, MYT-018)

### Product Functions Summary

| Capability | Summary | Source |
| --- | --- | --- |
| Model configuration | Supports users customizing models through the configuration interface and parameter adjustment; RUCM details are images in the source DOCX. | MYT-006, MYT-010 |
| Data loading | Uses deployed preset datasets and defines preprocessing, data augmentation, and dataset splitting methods. | MYT-011 |
| Model training | Trains models according to configuration, evaluates and saves models and evaluation results after training, and allows manual termination during training. | MYT-012 |
| Model inference | Loads a model according to model address, executes `forward()` inference, and returns inference results to the user. | MYT-013 |
| Framework extension | Supports GPU acceleration, weight initialization methods, classic models, and preset datasets. | MYT-014, MYT-015, MYT-016, MYT-017 |
| Data persistence | Uses SQLite local storage for models, training datasets, training logs, and inference logs, and supports backup and recovery. | MYT-018 |

### User Classes

| User Class | Responsibilities / Needs | Source |
| --- | --- | --- |
| Deep learning beginner | Completes model construction, training, and inference through a simple and intuitive interface, and understands neural network components, parameters, and training results. | MYT-021 |
| Developer / team member | Implements framework extension, system back end, front-end interface, database, and quality constraints according to requirements. | MYT-001, MYT-005 |
| Project participant / stakeholder | Understands project goals, boundaries, progress, and delivery requirements. | MYT-001 |

### Operating Environment

| Environment | Requirement | Source |
| --- | --- | --- |
| Development and test device | Computer devices that support deep learning tasks, including at least one computer with a GPU for GPU acceleration function development and testing. | MYT-008 |
| Base code | Uses existing NNE framework code as the basis for function enhancement. | MYT-008 |
| Dataset | Uses publicly available datasets or datasets satisfying course requirements to verify new functions and models. | MYT-008 |
| Supporting software | Python 3.8.x or above with corresponding libraries; concrete configuration and library versions are listed in `requirements.txt`. | MYT-024 |

### Assumptions and Dependencies

| ID | Assumption / Dependency | Evidence Type | Source |
| --- | --- | --- | --- |
| AD-001 | Project development and testing depend on computer devices that support deep learning tasks and at least one GPU computer. | explicit | MYT-008 |
| AD-002 | The project enhances existing NNE framework code. | explicit | MYT-008 |
| AD-003 | The project is constrained by course schedule and semester end date. | explicit | MYT-008 |
| AD-004 | Developers shall have basic deep learning, programming, teamwork, and communication skills. | explicit | MYT-008 |
| AD-005 | RUCM details for model configuration and training, and the database E-R diagram, are mainly images in the source DOCX, and the body text does not expand complete fields or event flows. | inferred | MYT-010, MYT-012, MYT-018 |

## 3. External Interface Requirements

### User Interfaces

| UI Area | Requirement Summary | Source |
| --- | --- | --- |
| Main interface | The front end shall include a main interface for entering major system functions. | MYT-006 |
| Configuration interface | Supports users adjusting parameters, customizing models, and understanding component and parameter roles through an intuitive interface. | MYT-006, MYT-021 |
| Training interface | Visualizes the model training process and provides real-time feedback such as loss decrease and accuracy improvement. | MYT-006, MYT-021 |
| Inference interface | Displays model inference results and helps users understand model performance and effect. | MYT-006, MYT-013, MYT-021 |
| Guidance and help | Provides step guidance, prompts, examples, suggestions, and help documents. | MYT-021 |

### Software/API Interfaces

| Interface | Requirement Summary | Source |
| --- | --- | --- |
| MyTorch / NNE framework interface | The back end calls the MyTorch deep learning framework and uses existing NNE code for framework extension. | MYT-006, MYT-008 |
| GPU API | Provides easy-to-use APIs to access and utilize GPU resources and remain compatible with the original framework. | MYT-014 |
| Data loading interface | Supports preset dataset loading, data preprocessing, data augmentation, and dataset splitting. | MYT-011 |
| Model training interface | Supports starting training according to configuration, manually terminating training, and saving evaluation results and trained models. | MYT-012 |
| Model inference interface | The inferencer initializes the model loader and data loader, loads a model by model address, and calls `forward()` for inference. | MYT-013 |
| SQLite database interface | The system uses SQLite as the local database and provides automatic backup and recovery capability. | MYT-018 |

### Communication Interfaces

The source document does not explicitly define network protocols, external service protocols, or distributed communication interfaces. At minimum, the system contains call relationships among the front end, back end, MyTorch framework, and SQLite database, but concrete communication protocols are not provided in the body text. (Source: MYT-005, MYT-006, MYT-018)

### Data Exchange Formats

| Data Group | Fields / Content | Source |
| --- | --- | --- |
| Model configuration | Model structure, initialization method, parameters, and user-customized configuration; concrete fields are not expanded in the images. | MYT-006, MYT-010 |
| Data loading configuration | Preprocessing method, data augmentation method, and dataset splitting method. | MYT-011 |
| Training data | Preset or custom datasets, training task configuration, and training termination state. | MYT-011, MYT-012 |
| Inference data | Model address, model instance, dataset to infer, and inference result. | MYT-013 |
| GPU computation data | Necessary data in GPU memory, matrix operation inputs, and GPU computation results. | MYT-014 |
| Weight initialization configuration | Activation function, initialization method, and weight initialization distribution. | MYT-015 |
| Logs and history | Training logs, inference logs, and user training/inference history information. | MYT-007 |
| Local database backup | SQLite database file and backup files. | MYT-018 |

## 4. Functional Requirements

| ID | Description | Trigger / Input | System Behavior | Output | Priority | Verification | Source Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| FR-001 | The system shall provide model configuration capability. | A user enters the configuration interface and adjusts parameters or customizes a model. | The system supports users configuring models through the visual front end; concrete fields and event flows are in source DOCX images and are not expanded in the body text. | Model configuration result. | High | Demonstration | MYT-006, MYT-009, MYT-010 |
| FR-002 | The system shall support loading preset datasets. | A user enters the data loading flow and selects a system-deployed preset dataset. | The system loads the selected preset dataset. | Dataset usable for training or testing. | High | Test | MYT-011 |
| FR-003 | The system shall allow users to define data loading methods. | A user configures the data loading method. | The system receives and applies the data preprocessing method, data augmentation method, and dataset splitting method. | Data loading configuration. | High | Test | MYT-011 |
| FR-004 | The system shall train models according to user configuration. | A user starts a training task. | The system trains the model according to configuration. | Running training task or training completion state. | High | Test | MYT-012 |
| FR-005 | The system shall evaluate and save the model after training completes. | The training task completes. | The system evaluates the trained model and saves evaluation results and the trained model. | Trained model and evaluation result. | High | Test | MYT-012 |
| FR-006 | The system shall allow users to manually terminate training. | A user initiates termination during training. | The system stops the training task and keeps the state recoverable or explainable. | Terminated training state. | Medium | Test | MYT-012 |
| FR-007 | The system shall support creating an inferencer instance and initializing loaders. | A user initiates the model inference flow. | The inferencer initializes the model loader and data loader. | Inferencer instance that can execute inference. | High | Test | MYT-013 |
| FR-008 | The system shall load a model according to the model address entered by the user. | A user enters a model from a specified address. | The inferencer loads the model and creates a model instance; if the address is wrong, it does not create a model instance and returns exception information. | Model instance or exception information. | High | Test | MYT-013 |
| FR-009 | The system shall execute model inference and return results. | A user sends an inference request to the inferencer. | The inferencer calls the model `forward()` method, performs inference on the dataset to be inferred, adds inference results to the data loader, and returns them to the user. | Inference result. | High | Test | MYT-013 |
| FR-010 | The system shall provide GPU-accelerated matrix computation capability. | A user or training process calls matrix operations that require acceleration. | The system initializes GPU computation, copies necessary data to GPU memory, lets the CPU invoke GPU multi-core computation, supports asynchronous CPU/GPU computation, and copies results back to the host. | GPU-accelerated computation result. | High | Test | MYT-014 |
| FR-011 | The system shall support target matrix operations accelerated by GPU. | A user executes matrix addition, matrix multiplication, matrix scalar multiplication, matrix mean, matrix extremum, or matrix element-wise function application. | The system provides GPU-accelerated implementations for these matrix operations. | Corresponding matrix operation result. | High | Test | MYT-014 |
| FR-012 | The system shall automatically detect and configure GPU resources. | The system starts training or needs to use GPU resources. | The system automatically performs resource management, reduces user hardware configuration work, and allocates suitable resources for training tasks. | GPU resource configuration result. | Medium | Test | MYT-014 |
| FR-013 | The system shall provide easy-to-use GPU APIs. | A user needs to call GPU resources. | The system provides simple APIs so users can use GPUs without deeply understanding low-level hardware details. | GPU API call result. | Medium | Demonstration | MYT-014 |
| FR-014 | The system shall ensure GPU acceleration is compatible with the original framework. | A user migrates existing framework code to the GPU acceleration flow. | The system integrates seamlessly into the existing framework and avoids requiring users to rewrite or substantially modify existing code. | Compatible executable GPU acceleration flow. | High | Test | MYT-014 |
| FR-015 | The system shall define GPU acceleration errors and handling methods. | Compatibility, memory overflow, or runtime errors occur during GPU acceleration. | The system helps users respond quickly according to predefined error handling methods. | Error handling result and prompt. | High | Test | MYT-014 |
| FR-016 | The system shall support selecting model weight initialization methods. | A user configures model weight initialization. | The system provides He, Lecun, Xavier, and other initialization methods for common activation functions. | Weight initialization configuration or initialized model weights. | High | Test | MYT-015 |
| FR-017 | The system shall integrate classic deep learning models. | A user selects a preset model. | The system provides structure definitions and forward processes for models such as ResNet, VGG, and Transformer, and adds new models to the NNE API. | Preset model that can be created, configured, and trained. | High | Test | MYT-016 |
| FR-018 | The system shall provide preset dataset download links and loading methods. | A user selects a preset dataset. | The system provides download links and loading methods for datasets such as CIFAR, ImageNet, COCO, Fashion-MNIST, IMDB, Penn Treebank, SVHN, and EMNIST. | Dataset that can be deployed locally and loaded. | Medium | Inspection | MYT-017 |
| FR-019 | The system back end shall provide business and service interfaces for the visualization system. | The front end or user flow requests model initialization, training, inference, or model management. | The back end calls the MyTorch deep learning framework and provides business/service interfaces. | Back-end processing result or interface response. | High | Inspection | MYT-006 |
| FR-020 | The system shall persist models, datasets, and logs. | Training, inference, or model management produces records. | The system saves deep learning models, training datasets, training logs, inference logs, and history information to the database. | Persistent data records. | High | Test | MYT-007, MYT-018 |
| FR-021 | The system shall back up and recover the SQLite database. | The system runs normally, a database exception occurs, or the user selects backup recovery. | The system automatically backs up the database; when an exception occurs, it attempts automatic recovery, and the user may also manually recover using a backup database file. | Backup file, recovery result, or error prompt. | High | Test | MYT-018 |
| FR-022 | The system interface shall provide real-time training and inference feedback and visualization. | A user executes model training or inference. | The system visually displays training loss decrease, accuracy improvement, and inference results. | Real-time feedback and visualization results. | High | Demonstration | MYT-021 |

## 5. Non-Functional Requirements

| ID | Quality | Requirement | Fit Criterion | Priority | Verification | Source Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| NFR-001 | Numerical Precision | System floating-point calculation precision shall meet the specified standard. | All floating-point calculation precision is the same as or higher than `numpy.float32`, with at least 7 decimal significant digits. | High | Test | MYT-019 |
| NFR-002 | Time Precision | System time-related records shall reach second-level precision. | Log time and other time-related precision is accurate to the second. | Medium | Inspection | MYT-019 |
| NFR-003 | UI Response Time | On recommended hardware configuration, the interaction interface shall respond promptly to user instructions. | Maximum response time is less than 1 second, and average response time is less than 0.75 seconds. | High | Test | MYT-020 |
| NFR-004 | Training Engine Response Time | On recommended hardware configuration, the training engine shall respond promptly to training or data-loading instructions. | Maximum response time is less than 3 seconds, and average response time is less than 2.5 seconds. | High | Test | MYT-020 |
| NFR-005 | Training Efficiency | System training time shall improve with device performance and GPU acceleration capability. | When processor performance is higher or higher-performance GPU acceleration is used for training, the system shall have correspondingly higher training efficiency. | Medium | Analysis | MYT-020 |
| NFR-006 | Device Variability | Under non-recommended hardware configuration, system response time may vary with device performance. | The test report shall explain that response time under non-recommended configuration is related to device performance. | Low | Analysis | MYT-020 |
| NFR-007 | UI Intuitiveness | The interface shall be as simple and intuitive as possible to reduce the learning curve for beginners. | Clear icons, symbols, and workflows are used, and functional areas are reasonably laid out. | High | Inspection | MYT-021 |
| NFR-008 | Guidance and Help | The interface shall provide step guidance, prompts, examples, and suggestions. | Users can view explanations of components and parameter roles, as well as help needed to build neural networks. | High | Demonstration | MYT-021 |
| NFR-009 | Real-Time Feedback | The interface shall provide real-time feedback and detailed visualization. | After parameter changes or component additions, the interface updates immediately; when waiting for framework response, it shows a loading animation or progress bar. | High | Demonstration | MYT-021 |
| NFR-010 | UI Consistency | Interface design shall remain consistent and concise. | Colors, fonts, buttons, and icon styles are consistent, reducing visual fatigue. | Medium | Inspection | MYT-021 |
| NFR-011 | Fault Monitoring | The system shall monitor training and inference runtime exceptions. | It monitors exceptions such as gradient explosion and inference memory overflow. | High | Test | MYT-022 |
| NFR-012 | Resource Monitoring | The system shall monitor key performance indicators. | It monitors GPU utilization, memory usage, and training speed. | High | Test | MYT-022 |
| NFR-013 | Fault Handling | The system shall define fault handling strategies. | Training faults such as gradient explosion shall trigger strategies such as automatic training termination. | High | Test | MYT-022 |
| NFR-014 | Recovery | The system shall support model backup and automatic recovery mechanisms. | When hardware failure occurs, model availability can be guaranteed through backup and recovery mechanisms. | High | Test | MYT-022 |
| NFR-015 | Error Reporting | The system shall record and report error information and provide troubleshooting suggestions. | Users can understand problems and perform troubleshooting. | Medium | Demonstration | MYT-022 |
| NFR-016 | Security and Privacy | The system shall protect user data and models from potential security threats. | Security and privacy protection mechanisms are adopted to prevent potential vulnerabilities or attacks. | High | Inspection | MYT-023 |
| NFR-017 | Confidentiality and Integrity | The system shall ensure confidentiality and integrity of user data. | Unauthorized access or tampering shall not compromise user data and models. | High | Test | MYT-023 |
| NFR-018 | Privacy Compliance | The system shall comply with relevant privacy regulations and standards. | Privacy protection design conforms to applicable regulations and standards. | High | Inspection | MYT-023 |

## 6. Data Requirements

| ID | Data Object | Requirement | Privacy / Integrity Notes | Verification | Source Evidence |
| --- | --- | --- | --- | --- | --- |
| DR-001 | Model configuration | The system shall save model structure, initialization method, parameter customization, and other model configuration results; field details are not expanded in the source DOCX. | Configuration affects training and inference results. | Inspection | MYT-006, MYT-010 |
| DR-002 | Data loading configuration | The system shall record data preprocessing methods, data augmentation methods, and dataset splitting methods. | Data splitting and augmentation affect training quality. | Test | MYT-011 |
| DR-003 | Preset datasets | The system shall maintain download links and loading methods for preset datasets such as CIFAR, ImageNet, COCO, Fashion-MNIST, IMDB, Penn Treebank, SVHN, and EMNIST. | Datasets shall be publicly available or satisfy course requirements. | Inspection | MYT-017, MYT-008 |
| DR-004 | Training task | The system shall record training task configuration, running state, manual termination state, trained model, and evaluation result. | Training state is used for history review and fault handling. | Test | MYT-012, MYT-007 |
| DR-005 | Inference task | The system shall record model address, model instance creation result, dataset to infer, inference request, and inference result. | Address errors shall record exception information. | Test | MYT-013 |
| DR-006 | GPU computation data | The system shall process necessary data in GPU memory, matrix operation inputs, and computation results. | GPU exceptions need to enter fault handling strategies. | Test | MYT-014, MYT-022 |
| DR-007 | Weight initialization configuration | The system shall record activation functions, initialization methods, and corresponding weight initialization distributions. | Initialization strategy affects training speed and convergence. | Inspection | MYT-015 |
| DR-008 | Classic model definition | The system shall maintain preset model structure definitions and forward processes for ResNet, VGG, Transformer, and similar models. | New models shall be added to the NNE API. | Inspection | MYT-016 |
| DR-009 | Log data | The system shall persist training logs, inference logs, and user training/inference history information. | Time precision shall be accurate to the second. | Test | MYT-007, MYT-019 |
| DR-010 | SQLite database | The system shall use a SQLite local database to save system data. | The database shall be automatically backed up and automatically or manually recovered on exception. | Test | MYT-018 |
| DR-011 | Error and fault records | The system shall record training/inference exceptions, performance metrics, error information, and troubleshooting suggestions. | Supports user troubleshooting and system stability analysis. | Test | MYT-022 |
| DR-012 | User data and model data | The system shall protect the confidentiality and integrity of user data and model data. | It shall satisfy security and privacy protection mechanism requirements. | Inspection | MYT-023 |

## 7. Constraints

| ID | Constraint | Evidence Type | Source |
| --- | --- | --- | --- |
| C-001 | The project enhances the existing NNE framework code. | explicit | MYT-008 |
| C-002 | Project development and testing shall be performed on computer devices that support deep learning tasks and include at least one computer with a GPU. | explicit | MYT-008 |
| C-003 | The project uses publicly available datasets or datasets satisfying course requirements for development and testing. | explicit | MYT-008 |
| C-004 | Project development progress and delivery are constrained by the course semester end date. | explicit | MYT-008 |
| C-005 | Developers shall have basic deep learning, programming, teamwork, and communication skills. | explicit | MYT-008 |
| C-006 | The supporting software environment is Python 3.8.x or above with corresponding libraries. | explicit | MYT-024 |
| C-007 | Concrete library versions and configuration shall be listed in `requirements.txt`. | explicit | MYT-024 |
| C-008 | The database is SQLite and is deployed in the user's local storage space with the system. | explicit | MYT-018 |
| C-009 | The system shall automatically back up the SQLite database and support automatic recovery on exception and manual recovery by users. | explicit | MYT-018 |
| C-010 | All floating-point computation precision must be no lower than `numpy.float32`. | explicit | MYT-019 |
| C-011 | Time precision shall be accurate to the second. | explicit | MYT-019 |
| C-012 | System security design shall comply with relevant privacy regulations and standards. | explicit | MYT-023 |
| C-013 | This document references GB/T 8567-1988 Computer Software Requirements Specification. | explicit | MYT-004 |

## 8. Verification and Acceptance

| ID | Verification Method | Acceptance Focus |
| --- | --- | --- |
| FR-001 | Demonstration | Users can adjust parameters through the configuration interface and form model configurations. |
| FR-002 | Test | Users can load preset datasets deployed by the system. |
| FR-003 | Test | Data preprocessing, augmentation, and splitting configurations can be saved and used for data loading. |
| FR-004 | Test | After a user starts training, the system executes the training task according to configuration. |
| FR-005 | Test | After training completes, the system saves the trained model and evaluation results. |
| FR-006 | Test | Users can manually terminate training during training. |
| FR-007 | Test | After the inferencer instance is created, the model loader and data loader initialize successfully. |
| FR-008 | Test | A correct model address returns a model instance, and an incorrect address returns exception information. |
| FR-009 | Test | The inferencer returns inference results after calling `forward()`. |
| FR-010 | Test | The GPU acceleration flow completes GPU memory copy, GPU computation, and result copy-back. |
| FR-011 | Test | Target matrix operations return correct results on the GPU acceleration path. |
| FR-012 | Test | The system can automatically detect and configure GPU resources. |
| FR-013 | Demonstration | Users can call GPU resources through simple APIs. |
| FR-014 | Test | Existing framework code can use GPU acceleration without substantial modification. |
| FR-015 | Test | GPU compatibility, memory overflow, or runtime errors trigger defined handling methods. |
| FR-016 | Test | He, Lecun, and Xavier initialization can be selected for ReLU/tanh and similar scenarios. |
| FR-017 | Test | ResNet, VGG, and Transformer can be created, configured, and trained. |
| FR-018 | Inspection | Preset datasets have download links and loading methods. |
| FR-019 | Inspection | Back-end interfaces cover model initialization, training, inference, and model management. |
| FR-020 | Test | Models, datasets, training logs, inference logs, and history records can be persisted. |
| FR-021 | Test | The SQLite database can be automatically backed up and recovered automatically or manually after exception. |
| FR-022 | Demonstration | Training and inference interfaces display real-time feedback and visualization results. |
| NFR-001 | Test | Floating-point calculation precision reaches `numpy.float32` or higher. |
| NFR-002 | Inspection | Log time and similar records are accurate to the second. |
| NFR-003 | Test | On recommended hardware, interaction interface maximum response < 1 second and average < 0.75 seconds. |
| NFR-004 | Test | On recommended hardware, training engine maximum response < 3 seconds and average < 2.5 seconds. |
| NFR-005 | Analysis | Training efficiency improves when using higher-performance processors or GPUs. |
| NFR-006 | Analysis | Response-time differences under non-recommended configuration are recorded and explained. |
| NFR-007 | Inspection | Interface icons, symbols, workflows, and functional layouts are intuitive and clear. |
| NFR-008 | Demonstration | Users can view component/parameter explanations, examples, suggestions, and help. |
| NFR-009 | Demonstration | Parameter changes, component additions, and response waiting have instant feedback or progress prompts. |
| NFR-010 | Inspection | Interface colors, fonts, buttons, and icon styles remain consistent. |
| NFR-011 | Test | The system can detect exceptions such as gradient explosion and inference memory overflow. |
| NFR-012 | Test | GPU utilization, memory usage, and training speed can be monitored. |
| NFR-013 | Test | Exceptions such as gradient explosion trigger fault handling strategies such as automatic termination. |
| NFR-014 | Test | Model backup and recovery mechanisms can recover after hardware failure. |
| NFR-015 | Demonstration | Error information and troubleshooting suggestions are visible to users. |
| NFR-016 | Inspection | Security and privacy protection mechanisms exist. |
| NFR-017 | Test | User data and model data are not accessed or tampered with without authorization. |
| NFR-018 | Inspection | Privacy design conforms to relevant regulations and standards. |
| DR-001 | Inspection | Model configuration data structures can support saving configuration results. |
| DR-002 | Test | Data loading configuration can be saved and drive data loading. |
| DR-003 | Inspection | Preset dataset download links and loading methods exist. |
| DR-004 | Test | Training task state, model, and evaluation results can be saved. |
| DR-005 | Test | Inference task inputs, exceptions, and results can be recorded. |
| DR-006 | Test | GPU input/output data is processed correctly in the acceleration flow. |
| DR-007 | Inspection | Weight initialization configuration covers activation functions and initialization methods. |
| DR-008 | Inspection | Classic model definitions are added to the NNE API. |
| DR-009 | Test | Training logs, inference logs, and history records can be persisted. |
| DR-010 | Test | SQLite database read/write, backup, and recovery are available. |
| DR-011 | Test | Error and fault records can be generated and used for troubleshooting. |
| DR-012 | Inspection | User data and model data have confidentiality and integrity protection design. |
| C-001 | Inspection | Project code is based on the existing NNE framework. |
| C-002 | Inspection | Development/test devices satisfy deep learning and GPU conditions. |
| C-003 | Inspection | Development and test dataset sources are publicly available or satisfy course requirements. |
| C-004 | Inspection | Project plan reflects course time constraints. |
| C-005 | Inspection | Team skills satisfy basic deep learning and programming requirements. |
| C-006 | Inspection | Python version is 3.8.x or above. |
| C-007 | Inspection | `requirements.txt` records concrete library configuration. |
| C-008 | Inspection | SQLite is deployed in local storage space with the system. |
| C-009 | Test | Database automatic backup and recovery mechanism is effective. |
| C-010 | Test | Floating-point precision is no lower than `numpy.float32`. |
| C-011 | Inspection | Time records are accurate to the second. |
| C-012 | Inspection | Security design complies with relevant privacy regulations and standards. |
| C-013 | Inspection | The document follows the referenced specification. |

## 9. Traceability Matrix

| ID | Requirement | Type | Source | Evidence Type | Verification | Confidence |
| --- | --- | --- | --- | --- | --- | --- |
| FR-001 | Model configuration | Functional | MYT-006, MYT-009, MYT-010 | explicit | Demonstration | Medium |
| FR-002 | Load preset dataset | Functional | MYT-011 | explicit | Test | High |
| FR-003 | Define data loading method | Functional | MYT-011 | explicit | Test | High |
| FR-004 | Train model according to configuration | Functional | MYT-012 | explicit | Test | High |
| FR-005 | Evaluate and save trained model | Functional | MYT-012 | explicit | Test | High |
| FR-006 | Manually terminate training | Functional | MYT-012 | explicit | Test | High |
| FR-007 | Create inferencer and initialize loaders | Functional | MYT-013 | explicit | Test | High |
| FR-008 | Load model by model address | Functional | MYT-013 | explicit | Test | High |
| FR-009 | Execute inference and return result | Functional | MYT-013 | explicit | Test | High |
| FR-010 | GPU-accelerated computation flow | Functional | MYT-014 | explicit | Test | High |
| FR-011 | GPU-accelerated matrix operations | Functional | MYT-014 | explicit | Test | High |
| FR-012 | Automatically detect and configure GPU | Functional | MYT-014 | explicit | Test | High |
| FR-013 | Easy-to-use GPU API | Functional | MYT-014 | explicit | Demonstration | High |
| FR-014 | GPU acceleration compatible with original framework | Functional | MYT-014 | explicit | Test | High |
| FR-015 | GPU error handling | Functional | MYT-014 | explicit | Test | High |
| FR-016 | Weight initialization methods | Functional | MYT-015 | explicit | Test | High |
| FR-017 | Classic model integration | Functional | MYT-016 | explicit | Test | High |
| FR-018 | Preset dataset links and loading | Functional | MYT-017 | explicit | Inspection | High |
| FR-019 | Back-end business and service interfaces | Functional | MYT-006 | explicit | Inspection | High |
| FR-020 | Persist models, datasets, and logs | Functional | MYT-007, MYT-018 | explicit | Test | High |
| FR-021 | SQLite backup and recovery | Functional | MYT-018 | explicit | Test | High |
| FR-022 | Real-time feedback and visualization | Functional | MYT-021 | explicit | Demonstration | High |
| NFR-001 | Floating-point calculation precision | Non-functional | MYT-019 | explicit | Test | High |
| NFR-002 | Time precision | Non-functional | MYT-019 | explicit | Inspection | High |
| NFR-003 | UI response time | Non-functional | MYT-020 | explicit | Test | High |
| NFR-004 | Training engine response time | Non-functional | MYT-020 | explicit | Test | High |
| NFR-005 | Training efficiency improves with device/GPU | Non-functional | MYT-020 | explicit | Analysis | Medium |
| NFR-006 | Non-recommended configuration response difference | Non-functional | MYT-020 | explicit | Analysis | Medium |
| NFR-007 | Interface intuitiveness | Non-functional | MYT-021 | explicit | Inspection | High |
| NFR-008 | Guidance and help | Non-functional | MYT-021 | explicit | Demonstration | High |
| NFR-009 | Real-time feedback | Non-functional | MYT-021 | explicit | Demonstration | High |
| NFR-010 | Interface consistency | Non-functional | MYT-021 | explicit | Inspection | High |
| NFR-011 | Exception monitoring | Non-functional | MYT-022 | explicit | Test | High |
| NFR-012 | Resource monitoring | Non-functional | MYT-022 | explicit | Test | High |
| NFR-013 | Fault handling strategy | Non-functional | MYT-022 | explicit | Test | High |
| NFR-014 | Backup and recovery | Non-functional | MYT-022 | explicit | Test | High |
| NFR-015 | Error reporting and troubleshooting suggestions | Non-functional | MYT-022 | explicit | Demonstration | High |
| NFR-016 | Security and privacy protection | Non-functional | MYT-023 | explicit | Inspection | High |
| NFR-017 | Confidentiality and integrity | Non-functional | MYT-023 | explicit | Test | High |
| NFR-018 | Privacy regulations and standards | Non-functional | MYT-023 | explicit | Inspection | High |
| DR-001 | Model configuration data | Data | MYT-006, MYT-010 | explicit | Inspection | Medium |
| DR-002 | Data loading configuration | Data | MYT-011 | explicit | Test | High |
| DR-003 | Preset datasets | Data | MYT-017, MYT-008 | explicit | Inspection | High |
| DR-004 | Training task data | Data | MYT-012, MYT-007 | explicit | Test | High |
| DR-005 | Inference task data | Data | MYT-013 | explicit | Test | High |
| DR-006 | GPU computation data | Data | MYT-014, MYT-022 | explicit | Test | High |
| DR-007 | Weight initialization configuration | Data | MYT-015 | explicit | Inspection | High |
| DR-008 | Classic model definition | Data | MYT-016 | explicit | Inspection | High |
| DR-009 | Logs and history records | Data | MYT-007, MYT-019 | explicit | Test | High |
| DR-010 | SQLite database | Data | MYT-018 | explicit | Test | High |
| DR-011 | Error and fault records | Data | MYT-022 | explicit | Test | High |
| DR-012 | User and model security data | Data | MYT-023 | explicit | Inspection | High |
| C-001 | Based on NNE framework | Constraint | MYT-008 | explicit | Inspection | High |
| C-002 | GPU development and test device | Constraint | MYT-008 | explicit | Inspection | High |
| C-003 | Dataset source constraint | Constraint | MYT-008 | explicit | Inspection | High |
| C-004 | Course time constraint | Constraint | MYT-008 | explicit | Inspection | High |
| C-005 | Developer skill constraint | Constraint | MYT-008 | explicit | Inspection | High |
| C-006 | Python 3.8.x+ | Constraint | MYT-024 | explicit | Inspection | High |
| C-007 | requirements.txt records library versions | Constraint | MYT-024 | explicit | Inspection | High |
| C-008 | SQLite local deployment | Constraint | MYT-018 | explicit | Inspection | High |
| C-009 | SQLite backup and recovery | Constraint | MYT-018 | explicit | Test | High |
| C-010 | numpy.float32 precision lower bound | Constraint | MYT-019 | explicit | Test | High |
| C-011 | Second-level time precision | Constraint | MYT-019 | explicit | Inspection | High |
| C-012 | Privacy regulations and standards | Constraint | MYT-023 | explicit | Inspection | High |
| C-013 | GB/T 8567-1988 reference specification | Constraint | MYT-004 | explicit | Inspection | High |
