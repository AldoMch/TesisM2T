# MyTorch Software Requirements Specification (Standard SRS Extract)

## 1. Introduction

### Product Scope

The MyTorch project targets deep learning learners. By continuously improving and extending the MyTorch/NNE framework, it provides framework enhancement capabilities and a visual training/inference system. The system scope includes model configuration, data loading, model training, model inference, GPU acceleration, model weight initialization, classic model introduction, preset datasets, back-end interfaces, front-end interfaces, and local database persistence.

This document follows the terminology definitions in the requirements specification for deep learning, neural networks, data augmentation, data loaders, model structures, loss functions, optimizers, learning rates, weight initialization, GPU acceleration, batches, and model deployment.

### Intended Audience

This document is intended for developers, team members, teachers, classmates, project stakeholders, and later architecture generation and test review workflows. The specification particularly emphasizes unifying understanding during development and testing, communicating requirements, and evaluating project progress.

## 2. Overall Description

### Product Perspective

The system consists of MyTorch/NNE framework extension, visual front end, system back end, and SQLite local database. The front end provides a main interface, configuration interface, training interface, and inference interface. The back end calls the MyTorch deep learning framework and provides interfaces for model initialization, model training, task inference, and model management. The database persists deep learning models, training datasets, training logs, and inference logs. The specification does not expand the concrete Web framework, API paths, database table structure, or front-end technology stack.

### Product Functions Summary

| Capability | Summary |
| --- | --- |
| Model configuration | Supports users customizing models through the configuration interface and parameter adjustment; RUCM details are images in the source DOCX. |
| Data loading | Uses deployed preset datasets and defines preprocessing, data augmentation, and dataset splitting methods. |
| Model training | Trains models according to configuration, evaluates and saves models and evaluation results after training, and allows manual termination during training. |
| Model inference | Loads a model according to model address, executes `forward()` inference, and returns inference results to the user. |
| Framework extension | Supports GPU acceleration, weight initialization methods, classic models, and preset datasets. |
| Data persistence | Uses SQLite local storage for models, training datasets, training logs, and inference logs, and supports backup and recovery. |

### User Classes

| User Class | Responsibilities / Needs |
| --- | --- |
| Deep learning beginner | Completes model construction, training, and inference through a simple and intuitive interface, and understands neural network components, parameters, and training results. |
| Developer / team member | Implements framework extension, system back end, front-end interface, database, and quality constraints according to requirements. |
| Project participant / stakeholder | Understands project goals, boundaries, progress, and delivery requirements. |

### Operating Environment

| Environment | Requirement |
| --- | --- |
| Development and test device | Computer devices that support deep learning tasks, including at least one computer with a GPU for GPU acceleration function development and testing. |
| Base code | Uses existing NNE framework code as the basis for function enhancement. |
| Dataset | Uses publicly available datasets or datasets satisfying course requirements to verify new functions and models. |
| Supporting software | Python 3.8.x or above with corresponding libraries; concrete configuration and library versions are listed in `requirements.txt`. |

### Assumptions and Dependencies

| ID | Assumption / Dependency |
| --- | --- |
| AD-001 | Project development and testing depend on computer devices that support deep learning tasks and at least one GPU computer. |
| AD-002 | The project enhances existing NNE framework code. |
| AD-003 | The project is constrained by course schedule and semester end date. |
| AD-004 | Developers shall have basic deep learning, programming, teamwork, and communication skills. |
| AD-005 | RUCM details for model configuration and training, and the database E-R diagram, are mainly images in the source DOCX, and the body text does not expand complete fields or event flows. |

## 3. External Interface Requirements

### User Interfaces

| UI Area | Requirement Summary |
| --- | --- |
| Main interface | The front end shall include a main interface for entering major system functions. |
| Configuration interface | Supports users adjusting parameters, customizing models, and understanding component and parameter roles through an intuitive interface. |
| Training interface | Visualizes the model training process and provides real-time feedback such as loss decrease and accuracy improvement. |
| Inference interface | Displays model inference results and helps users understand model performance and effect. |
| Guidance and help | Provides step guidance, prompts, examples, suggestions, and help documents. |

### Software/API Interfaces

| Interface | Requirement Summary |
| --- | --- |
| MyTorch / NNE framework interface | The back end calls the MyTorch deep learning framework and uses existing NNE code for framework extension. |
| GPU API | Provides easy-to-use APIs to access and utilize GPU resources and remain compatible with the original framework. |
| Data loading interface | Supports preset dataset loading, data preprocessing, data augmentation, and dataset splitting. |
| Model training interface | Supports starting training according to configuration, manually terminating training, and saving evaluation results and trained models. |
| Model inference interface | The inferencer initializes the model loader and data loader, loads a model by model address, and calls `forward()` for inference. |
| SQLite database interface | The system uses SQLite as the local database and provides automatic backup and recovery capability. |

### Communication Interfaces

The specification does not explicitly define network protocols, external service protocols, or distributed communication interfaces. At minimum, the system contains call relationships among the front end, back end, MyTorch framework, and SQLite database, but concrete communication protocols are not provided in the body text.

### Data Exchange Formats

| Data Group | Fields / Content |
| --- | --- |
| Model configuration | Model structure, initialization method, parameters, and user-customized configuration; concrete fields are not expanded in the images. |
| Data loading configuration | Preprocessing method, data augmentation method, and dataset splitting method. |
| Training data | Preset or custom datasets, training task configuration, and training termination state. |
| Inference data | Model address, model instance, dataset to infer, and inference result. |
| GPU computation data | Necessary data in GPU memory, matrix operation inputs, and GPU computation results. |
| Weight initialization configuration | Activation function, initialization method, and weight initialization distribution. |
| Logs and history | Training logs, inference logs, and user training/inference history information. |
| Local database backup | SQLite database file and backup files. |

## 4. Functional Requirements

| ID | Description | Trigger / Input | System Behavior | Output | Priority | Verification |
| --- | --- | --- | --- | --- | --- | --- |
| FR-001 | The system shall provide model configuration capability. | A user enters the configuration interface and adjusts parameters or customizes a model. | The system supports users configuring models through the visual front end; concrete fields and event flows are in source DOCX images and are not expanded in the body text. | Model configuration result. | High | Demonstration |
| FR-002 | The system shall support loading preset datasets. | A user enters the data loading flow and selects a system-deployed preset dataset. | The system loads the selected preset dataset. | Dataset usable for training or testing. | High | Test |
| FR-003 | The system shall allow users to define data loading methods. | A user configures the data loading method. | The system receives and applies the data preprocessing method, data augmentation method, and dataset splitting method. | Data loading configuration. | High | Test |
| FR-004 | The system shall train models according to user configuration. | A user starts a training task. | The system trains the model according to configuration. | Running training task or training completion state. | High | Test |
| FR-005 | The system shall evaluate and save the model after training completes. | The training task completes. | The system evaluates the trained model and saves evaluation results and the trained model. | Trained model and evaluation result. | High | Test |
| FR-006 | The system shall allow users to manually terminate training. | A user initiates termination during training. | The system stops the training task and keeps the state recoverable or explainable. | Terminated training state. | Medium | Test |
| FR-007 | The system shall support creating an inferencer instance and initializing loaders. | A user initiates the model inference flow. | The inferencer initializes the model loader and data loader. | Inferencer instance that can execute inference. | High | Test |
| FR-008 | The system shall load a model according to the model address entered by the user. | A user enters a model from a specified address. | The inferencer loads the model and creates a model instance; if the address is wrong, it does not create a model instance and returns exception information. | Model instance or exception information. | High | Test |
| FR-009 | The system shall execute model inference and return results. | A user sends an inference request to the inferencer. | The inferencer calls the model `forward()` method, performs inference on the dataset to be inferred, adds inference results to the data loader, and returns them to the user. | Inference result. | High | Test |
| FR-010 | The system shall provide GPU-accelerated matrix computation capability. | A user or training process calls matrix operations that require acceleration. | The system initializes GPU computation, copies necessary data to GPU memory, lets the CPU invoke GPU multi-core computation, supports asynchronous CPU/GPU computation, and copies results back to the host. | GPU-accelerated computation result. | High | Test |
| FR-011 | The system shall support target matrix operations accelerated by GPU. | A user executes matrix addition, matrix multiplication, matrix scalar multiplication, matrix mean, matrix extremum, or matrix element-wise function application. | The system provides GPU-accelerated implementations for these matrix operations. | Corresponding matrix operation result. | High | Test |
| FR-012 | The system shall automatically detect and configure GPU resources. | The system starts training or needs to use GPU resources. | The system automatically performs resource management, reduces user hardware configuration work, and allocates suitable resources for training tasks. | GPU resource configuration result. | Medium | Test |
| FR-013 | The system shall provide easy-to-use GPU APIs. | A user needs to call GPU resources. | The system provides simple APIs so users can use GPUs without deeply understanding low-level hardware details. | GPU API call result. | Medium | Demonstration |
| FR-014 | The system shall ensure GPU acceleration is compatible with the original framework. | A user migrates existing framework code to the GPU acceleration flow. | The system integrates seamlessly into the existing framework and avoids requiring users to rewrite or substantially modify existing code. | Compatible executable GPU acceleration flow. | High | Test |
| FR-015 | The system shall define GPU acceleration errors and handling methods. | Compatibility, memory overflow, or runtime errors occur during GPU acceleration. | The system helps users respond quickly according to predefined error handling methods. | Error handling result and prompt. | High | Test |
| FR-016 | The system shall support selecting model weight initialization methods. | A user configures model weight initialization. | The system provides He, Lecun, Xavier, and other initialization methods for common activation functions. | Weight initialization configuration or initialized model weights. | High | Test |
| FR-017 | The system shall integrate classic deep learning models. | A user selects a preset model. | The system provides structure definitions and forward processes for models such as ResNet, VGG, and Transformer, and adds new models to the NNE API. | Preset model that can be created, configured, and trained. | High | Test |
| FR-018 | The system shall provide preset dataset download links and loading methods. | A user selects a preset dataset. | The system provides download links and loading methods for datasets such as CIFAR, ImageNet, COCO, Fashion-MNIST, IMDB, Penn Treebank, SVHN, and EMNIST. | Dataset that can be deployed locally and loaded. | Medium | Inspection |
| FR-019 | The system back end shall provide business and service interfaces for the visualization system. | The front end or user flow requests model initialization, training, inference, or model management. | The back end calls the MyTorch deep learning framework and provides business/service interfaces. | Back-end processing result or interface response. | High | Inspection |
| FR-020 | The system shall persist models, datasets, and logs. | Training, inference, or model management produces records. | The system saves deep learning models, training datasets, training logs, inference logs, and history information to the database. | Persistent data records. | High | Test |
| FR-021 | The system shall back up and recover the SQLite database. | The system runs normally, a database exception occurs, or the user selects backup recovery. | The system automatically backs up the database; when an exception occurs, it attempts automatic recovery, and the user may also manually recover using a backup database file. | Backup file, recovery result, or error prompt. | High | Test |
| FR-022 | The system interface shall provide real-time training and inference feedback and visualization. | A user executes model training or inference. | The system visually displays training loss decrease, accuracy improvement, and inference results. | Real-time feedback and visualization results. | High | Demonstration |

## 5. Non-Functional Requirements

| ID | Quality | Requirement | Fit Criterion | Priority | Verification |
| --- | --- | --- | --- | --- | --- |
| NFR-001 | Numerical Precision | System floating-point calculation precision shall meet the specified standard. | All floating-point calculation precision is the same as or higher than `numpy.float32`, with at least 7 decimal significant digits. | High | Test |
| NFR-002 | Time Precision | System time-related records shall reach second-level precision. | Log time and other time-related precision is accurate to the second. | Medium | Inspection |
| NFR-003 | UI Response Time | On recommended hardware configuration, the interaction interface shall respond promptly to user instructions. | Maximum response time is less than 1 second, and average response time is less than 0.75 seconds. | High | Test |
| NFR-004 | Training Engine Response Time | On recommended hardware configuration, the training engine shall respond promptly to training or data-loading instructions. | Maximum response time is less than 3 seconds, and average response time is less than 2.5 seconds. | High | Test |
| NFR-005 | Training Efficiency | System training time shall improve with device performance and GPU acceleration capability. | When processor performance is higher or higher-performance GPU acceleration is used for training, the system shall have correspondingly higher training efficiency. | Medium | Analysis |
| NFR-006 | Device Variability | Under non-recommended hardware configuration, system response time may vary with device performance. | The test report shall explain that response time under non-recommended configuration is related to device performance. | Low | Analysis |
| NFR-007 | UI Intuitiveness | The interface shall be as simple and intuitive as possible to reduce the learning curve for beginners. | Clear icons, symbols, and workflows are used, and functional areas are reasonably laid out. | High | Inspection |
| NFR-008 | Guidance and Help | The interface shall provide step guidance, prompts, examples, and suggestions. | Users can view explanations of components and parameter roles, as well as help needed to build neural networks. | High | Demonstration |
| NFR-009 | Real-Time Feedback | The interface shall provide real-time feedback and detailed visualization. | After parameter changes or component additions, the interface updates immediately; when waiting for framework response, it shows a loading animation or progress bar. | High | Demonstration |
| NFR-010 | UI Consistency | Interface design shall remain consistent and concise. | Colors, fonts, buttons, and icon styles are consistent, reducing visual fatigue. | Medium | Inspection |
| NFR-011 | Fault Monitoring | The system shall monitor training and inference runtime exceptions. | It monitors exceptions such as gradient explosion and inference memory overflow. | High | Test |
| NFR-012 | Resource Monitoring | The system shall monitor key performance indicators. | It monitors GPU utilization, memory usage, and training speed. | High | Test |
| NFR-013 | Fault Handling | The system shall define fault handling strategies. | Training faults such as gradient explosion shall trigger strategies such as automatic training termination. | High | Test |
| NFR-014 | Recovery | The system shall support model backup and automatic recovery mechanisms. | When hardware failure occurs, model availability can be guaranteed through backup and recovery mechanisms. | High | Test |
| NFR-015 | Error Reporting | The system shall record and report error information and provide troubleshooting suggestions. | Users can understand problems and perform troubleshooting. | Medium | Demonstration |
| NFR-016 | Security and Privacy | The system shall protect user data and models from potential security threats. | Security and privacy protection mechanisms are adopted to prevent potential vulnerabilities or attacks. | High | Inspection |
| NFR-017 | Confidentiality and Integrity | The system shall ensure confidentiality and integrity of user data. | Unauthorized access or tampering shall not compromise user data and models. | High | Test |
| NFR-018 | Privacy Compliance | The system shall comply with relevant privacy regulations and standards. | Privacy protection design conforms to applicable regulations and standards. | High | Inspection |

## 6. Data Requirements

| ID | Data Object | Requirement | Privacy / Integrity Notes | Verification |
| --- | --- | --- | --- | --- |
| DR-001 | Model configuration | The system shall save model structure, initialization method, parameter customization, and other model configuration results; field details are not expanded in the source DOCX. | Configuration affects training and inference results. | Inspection |
| DR-002 | Data loading configuration | The system shall record data preprocessing methods, data augmentation methods, and dataset splitting methods. | Data splitting and augmentation affect training quality. | Test |
| DR-003 | Preset datasets | The system shall maintain download links and loading methods for preset datasets such as CIFAR, ImageNet, COCO, Fashion-MNIST, IMDB, Penn Treebank, SVHN, and EMNIST. | Datasets shall be publicly available or satisfy course requirements. | Inspection |
| DR-004 | Training task | The system shall record training task configuration, running state, manual termination state, trained model, and evaluation result. | Training state is used for history review and fault handling. | Test |
| DR-005 | Inference task | The system shall record model address, model instance creation result, dataset to infer, inference request, and inference result. | Address errors shall record exception information. | Test |
| DR-006 | GPU computation data | The system shall process necessary data in GPU memory, matrix operation inputs, and computation results. | GPU exceptions need to enter fault handling strategies. | Test |
| DR-007 | Weight initialization configuration | The system shall record activation functions, initialization methods, and corresponding weight initialization distributions. | Initialization strategy affects training speed and convergence. | Inspection |
| DR-008 | Classic model definition | The system shall maintain preset model structure definitions and forward processes for ResNet, VGG, Transformer, and similar models. | New models shall be added to the NNE API. | Inspection |
| DR-009 | Log data | The system shall persist training logs, inference logs, and user training/inference history information. | Time precision shall be accurate to the second. | Test |
| DR-010 | SQLite database | The system shall use a SQLite local database to save system data. | The database shall be automatically backed up and automatically or manually recovered on exception. | Test |
| DR-011 | Error and fault records | The system shall record training/inference exceptions, performance metrics, error information, and troubleshooting suggestions. | Supports user troubleshooting and system stability analysis. | Test |
| DR-012 | User data and model data | The system shall protect the confidentiality and integrity of user data and model data. | It shall satisfy security and privacy protection mechanism requirements. | Inspection |

## 7. Constraints

| ID | Constraint |
| --- | --- |
| C-001 | The project enhances the existing NNE framework code. |
| C-002 | Project development and testing shall be performed on computer devices that support deep learning tasks and include at least one computer with a GPU. |
| C-003 | The project uses publicly available datasets or datasets satisfying course requirements for development and testing. |
| C-004 | Project development progress and delivery are constrained by the course semester end date. |
| C-005 | Developers shall have basic deep learning, programming, teamwork, and communication skills. |
| C-006 | The supporting software environment is Python 3.8.x or above with corresponding libraries. |
| C-007 | Concrete library versions and configuration shall be listed in `requirements.txt`. |
| C-008 | The database is SQLite and is deployed in the user's local storage space with the system. |
| C-009 | The system shall automatically back up the SQLite database and support automatic recovery on exception and manual recovery by users. |
| C-010 | All floating-point computation precision must be no lower than `numpy.float32`. |
| C-011 | Time precision shall be accurate to the second. |
| C-012 | System security design shall comply with relevant privacy regulations and standards. |
| C-013 | This document references GB/T 8567-1988 Computer Software Requirements Specification. |

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
