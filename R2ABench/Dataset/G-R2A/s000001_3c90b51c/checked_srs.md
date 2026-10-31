# Software Requirements Specification

## 1. Introduction

### 1.1 Purpose

This document specifies the externally observable behavior of JSeats for electoral seat allocation. It provides a basis for development, review, and acceptance testing.

The functional scope consists of the five reviewed capabilities recorded in [req_final.jsonl](req_final.jsonl). This specification organizes those capabilities with their inputs, outputs, operating context, data needs, and verification criteria.

### 1.2 Product scope

JSeats calculates electoral seat allocations from candidate vote totals. Users enter or import election data, select a supported electoral method, configure the calculation, obtain the allocation outcome, and save requested output files.

The product can be used from a command line or within another application.

### 1.3 Intended audience

- Operators and analysts who prepare election data and calculate allocations.
- Application integrators who use the allocation capability within other software.
- Developers, testers, and reviewers who implement or verify the specified behavior.

### 1.4 Terms and conventions

| Term | Meaning in this document |
|---|---|
| Tally data | Candidate names and their corresponding vote totals used for allocation. |
| Allocation method | A supported electoral method that determines the allocation from the supplied data. |
| Allocation settings | User-supplied parameters and processing choices applied to a calculation. |
| Allocation result | The outcome of a completed seat-allocation calculation. |
| Calling application | Software that submits allocation inputs and receives the result or failure feedback. |
| Shall | A required behavior within the reviewed scope. |
| TBD | A specification detail that the available material does not establish and that still needs confirmation. |

## 2. Overall Description

### 2.1 Product perspective and boundary

JSeats receives election data and allocation settings, performs seat calculation, and delivers a result or failure feedback. Users interact through the command line; other applications can use the same allocation capability.

The system boundary includes data input, method selection, settings, calculation, and output. Users or calling applications supply the election data and requested settings.

### 2.2 User classes

| User class | Main tasks |
|---|---|
| Operator or analyst | Prepare tally data, select a method and settings, run the calculation, inspect the outcome, and save output files. |
| Application integrator | Supply election data and settings from another application and handle the resulting allocation or failure feedback. |

### 2.3 Operating environment

The documented product uses a Java runtime. Command-line operation also requires a command-line environment. Specific Java versions, operating-system versions, and hardware requirements are not established by the reviewed source and are recorded under TBD-003.

### 2.4 Assumptions and dependencies

- A calculation depends on the supplied tally data, selected electoral method, and applicable allocation settings.
- File-based operations depend on input files conforming to a supported format.
- The caller or user supplies the information needed by the selected calculation.

### 2.5 Main operating scenario

1. Enter candidate names and vote totals, or import tally data from an XML file.
2. View available electoral methods and select one.
3. View available processing options and set or load allocation settings.
4. Run the calculation using the supplied data and settings.
5. View the allocation result and save the requested output.
6. If the allocation cannot be completed, receive failure feedback.

## 3. External Interface Requirements

### 3.1 User interaction

| ID | Requirement |
|---|---|
| EI-001 | The command-line user shall be able to submit election data, view available methods and processing options, choose a method, supply settings, run a calculation, and obtain the requested output. |

### 3.2 Interaction with other applications

| ID | Requirement |
|---|---|
| EI-002 | A calling application shall be able to submit tally data, the selected electoral method, and allocation settings, and receive the calculated outcome or allocation-failure feedback. |

### 3.3 File exchange

| ID | Requirement |
|---|---|
| EI-003 | The system shall support importing tally data from XML files and loading allocation settings from configuration files. |
| EI-004 | The system shall support saving tally data, allocation results, and settings to output files, including supported XML output. |

These requirements specify the interaction visible to users and calling applications. The exact supported file specifications require confirmation as recorded in TBD-001.

## 4. Functional Requirements

### 4.1 FR-001 — Election data entry and import

**Requirement:** The system shall allow users to enter candidate names and their vote totals or import tally data from XML files, and use the submitted data for electoral seat allocation.

| Attribute | Specification |
|---|---|
| Trigger and input | Candidate names and vote totals entered directly, or an XML tally file. |
| Preconditions | The user is preparing election data for a seat-allocation calculation. |
| Output | Candidate and vote data available for seat calculation. |
| Verification | Test |
| Acceptance reference | AC-001 |
| Reviewed capability | JSEATS-R001 |

### 4.2 FR-002 — Method selection and seat calculation

**Requirement:** The system shall allow users to view and select supported electoral methods and calculate seat allocations from the submitted tally data, including majority methods (simple, qualified, and absolute), ranking by votes, equal proportions (Huntington-Hill), largest remainder methods (Hare, Droop, and Imperiali), and highest averages methods (D'Hondt, Sainte-Lague/Webster, Imperiali, and Danish).

| Attribute | Specification |
|---|---|
| Trigger and input | Tally data, a selected electoral method, and the settings used for the calculation. |
| Preconditions | The tally and settings needed by the selected method have been supplied. |
| Output | A seat-allocation outcome produced according to the selected method. |
| Verification | Test and demonstration |
| Acceptance reference | AC-002 |
| Reviewed capability | JSEATS-R002 |

### 4.3 FR-003 — Allocation settings

**Requirement:** The system shall allow users to view available tally-processing and result-processing options, set allocation parameters and rules or load them from a configuration file, and apply the chosen settings when calculating results.

| Attribute | Specification |
|---|---|
| Trigger and input | A request to view processing options, entered allocation settings, or a saved configuration file. |
| Preconditions | The user is preparing the settings for an allocation calculation. |
| Output | Settings applied when calculating the allocation result. |
| Verification | Test and demonstration |
| Acceptance reference | AC-003 |
| Reviewed capability | JSEATS-R003 |

### 4.4 FR-004 — Result viewing and data export

**Requirement:** The system shall allow users to view allocation results and save tally data, allocation results, and allocation settings to output files, including the supported XML formats.

| Attribute | Specification |
|---|---|
| Trigger and input | A request to view an allocation result or save tally data, results, or settings. |
| Preconditions | The data or completed result selected for viewing or export is available. |
| Output | The requested result or output file. |
| Verification | Test and demonstration |
| Acceptance reference | AC-004 |
| Reviewed capability | JSEATS-R004 |

### 4.5 FR-005 — Allocation failure feedback

**Requirement:** The system shall notify the user or calling application when seat allocation cannot be completed, clearly distinguishing a failed calculation from a successful allocation result.

| Attribute | Specification |
|---|---|
| Trigger and input | An allocation attempt that cannot be completed. |
| Preconditions | An allocation calculation has been attempted. |
| Output | Failure feedback to the user or calling application. |
| Verification | Test |
| Acceptance reference | AC-005 |
| Reviewed capability | JSEATS-R005 |

## 5. Non-Functional Requirements

The following quality requirements qualify the reviewed functional behavior.

| ID | Quality attribute | Requirement | Verification |
|---|---|---|---|
| NFR-001 | Calculation correctness | For a supported method and valid inputs, the allocation outcome shall follow the selected electoral method and supplied settings. | Test against expected outcomes for representative methods, inputs, and settings; see AC-002 and AC-003. |
| NFR-002 | Failure identification | A failed allocation attempt shall not be reported as a successful allocation result. | Trigger an allocation failure and confirm that the observable outcome identifies failure; see AC-005. |

No numerical performance, capacity, or availability target has been established by the reviewed baseline. Such targets remain open under TBD-003. The reviewed baseline also does not establish authentication or encryption requirements.

## 6. Data Requirements

| ID | Business data | Requirement |
|---|---|---|
| DR-001 | Election tally | The system shall accept candidate names and corresponding vote totals as the basis for allocation, whether entered directly or imported from supported XML input. |
| DR-002 | Allocation settings | The system shall accept the selected method and user-supplied settings, including settings loaded from a configuration file, and apply them during calculation. |
| DR-003 | Allocation result | The system shall provide the allocation outcome for user viewing or use by a calling application and support saving the result to an output file. |
| DR-004 | Input and output files | The system shall support XML tally input and the supported file formats for loading settings and saving tally data, results, and settings. |
| DR-005 | Failure feedback | The system shall communicate that an allocation attempt failed and distinguish that outcome from a successful calculation. |

Input value limits and the detailed file specifications are identified in TBD-001 and TBD-002.

## 7. Constraints

| ID | Constraint |
|---|---|
| C-001 | The required electoral-method coverage is the set named in FR-002. |
| C-002 | The specified usage modes are command-line operation and use by calling applications, as described in EI-001 and EI-002. |

These constraints describe the reviewed product scope. The operating environment is recorded in Section 2.3.

## 8. Verification and Acceptance

### 8.1 Verification criteria

The following criteria define how the requirements are to be verified; they do not report completed product tests.

| ID | Requirements covered | Method | Acceptance criterion |
|---|---|---|---|
| AC-001 | FR-001, EI-001, EI-002, EI-003, DR-001, DR-004 | Test | Candidate names and vote totals can be supplied directly or loaded from supported XML input and used in a seat-allocation calculation. |
| AC-002 | FR-002, EI-001, EI-002, NFR-001, DR-001, DR-003, C-001 | Test and demonstration | Users can view and select the documented methods. Representative calculations produce the expected allocation for the selected method and input data. |
| AC-003 | FR-003, EI-001, EI-002, EI-003, NFR-001, DR-002 | Test and demonstration | Users can view available processing options, supply settings directly or load a configuration file, and obtain a calculation that applies the selected settings. |
| AC-004 | FR-004, EI-001, EI-002, EI-004, DR-003, DR-004, C-002 | Test and demonstration | Users and calling applications can obtain the calculated result. Requested tally, result, and configuration files can be produced in the supported formats, including supported XML output. |
| AC-005 | FR-005, EI-001, EI-002, NFR-002, DR-005 | Test | An allocation failure produces an explicit failure indication distinguishable from a successful result. |

Detailed format-compatibility and boundary tests depend on resolving TBD-001 and TBD-002. Performance acceptance limits depend on TBD-003.

### 8.2 Requirements Traceability

| SRS functional requirement | Reviewed capability | Source lines in checked_srs_before_review.md | Acceptance criterion |
|---|---|---|---|
| FR-001 | JSEATS-R001 | 59, 76, 85, 91, 110, 114, 116 | AC-001 |
| FR-002 | JSEATS-R002 | 9, 59, 83, 86, 93, 124 | AC-002 |
| FR-003 | JSEATS-R003 | 29, 59, 66, 67, 76, 87, 90, 93, 94, 111, 115, 116 | AC-003 |
| FR-004 | JSEATS-R004 | 59, 76, 93, 112, 116 | AC-004 |
| FR-005 | JSEATS-R005 | 83, 92, 93, 102 | AC-005 |

External interaction, quality, data, and scope requirements are traced to the functional capabilities through the acceptance matrix in Section 8.

The [source snapshot](checked_srs_before_review.md) preserves the text and line positions used by the original extraction in [req.jsonl](req.jsonl). The source references in req_final.jsonl point to this revised specification.

### 8.3 Items Requiring Confirmation

| ID | Unresolved detail | Affected requirements |
|---|---|---|
| TBD-001 | Exact supported XML and configuration-file specifications, including schema or version information and compatibility rules. | FR-001, FR-003, FR-004, EI-003, EI-004, DR-004 |
| TBD-002 | Allowed input ranges and sizes, handling of incomplete or invalid input, and the specific failure cases to be used for verification. | FR-001, FR-002, FR-005, DR-001 |
| TBD-003 | Supported runtime and operating-system versions, resource requirements, and any quantitative performance, capacity, or availability targets. | Operating environment and non-functional acceptance scope |

These items record gaps in the available specification. Values and additional behavior require confirmation before they become acceptance requirements.
