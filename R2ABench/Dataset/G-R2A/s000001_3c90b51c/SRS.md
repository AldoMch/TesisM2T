# Software Requirements Specification

## 1. Introduction

### Purpose
This SRS defines the software requirements for `JSeats`, a Java library and command-line tool for electoral seat allocation.

### Product scope
`JSeats` provides electoral seat allocation algorithms through a Java API and a command-line launcher. The documented scope includes majority methods (simple, qualified, absolute), ranked methods (by votes), equal proportions (Huntington-Hill), largest remainder methods (Hare, Droop, Imperiali), and highest averages methods (D'Hondt, Sainte-Lague/Webster with support for a user-provided first divisor, Imperiali, Danish).

No web-interface requirements are included because implemented web-interface functionality is outside the current system scope. Planned web-interface functionality is outside the current system capability described by this SRS.

### Intended audience
The intended audience includes:
- Java developers integrating seat allocation into software through the Java API.
- Command-line users running seat allocation from a terminal.

## 2. Overall Description

### Product perspective
`JSeats` is an electoral seat allocation component implemented in Java. It exposes two related API surfaces:
- A caller-facing allocation entry point that lets callers provide tally data, select an allocation method, provide configuration parameters, and receive either an allocation result or an allocation error.
- A per-method processing contract that each allocation method must satisfy. The allocation method receives a protected view of tally data and configuration parameters, then returns an allocation result or reports an allocation error.

`JSeats` also provides a command-line launcher for invoking allocation-related functions from a shell.

### Configurable allocation workflow
The system shall support a configurable seat-allocation workflow: a user or caller can provide tally data and configure allocation parameters, the allocation method, tally filtering rules, tie-breaking rules, and result output decoration rules. The system shall process the tally data according to that configuration, execute the selected seat-allocation method, and generate the final allocation result that conforms to the configuration.

### Product functions summary
The product supports:
- Allocation of seats using documented electoral method families and variants.
- Processing of tally data through a caller-facing Java entry point.
- Definition of a per-method allocation contract based on a protected tally view and configuration properties.
- Method-specific parameterization through `Properties`.
- Optional tally filtering before allocation and optional result decoration after allocation.
- Command-line listing of built-in methods, filters, and decorators; command-line input of candidates or files; method selection; processor properties; and optional tally, result, or configuration output.
- XML-based tally loading indicated by `Tally.fromXML()`, plus XML input/output for processor configuration and results where supported by the launcher and model objects.

### User classes
- Application developers using the Java API.
- Operators or analysts using the command-line launcher.

### Operating environment
- Java runtime environment.
- Command-line shell environment for launcher use.

### Assumptions and dependencies
- Seat allocation processing depends on caller- or user-supplied tally data, an allocation method, and configuration parameters.
- Some methods depend on tally-derived values such as potential votes and number of candidates.
- Optional pre-processing and post-processing depend on configured tally filters and result decorators.

## 3. External Interface Requirements

### User interfaces
| Interface | Requirement |
|---|---|
| Command line | The system shall provide a command-line interface that supports users querying available allocation methods and related extensions, submitting candidate vote totals or reading tally/configuration files, selecting an allocation method and setting processing parameters, and generating tally, allocation-result, or configuration output when output options are specified. Verification shall be confirmed through demonstration or testing. |

### Software/API interfaces
| Interface | Requirement |
|---|---|
| Caller-facing allocation API | The system shall provide a Java entry point that allows callers to submit tally data, select an allocation method, provide configuration parameters, and receive an allocation result or allocation error. |
| Allocation-method contract | The system shall define a processing contract that each allocation method must satisfy: an allocation method receives a protected tally-data view and configuration parameters, and returns an allocation result or reports an allocation error. The immutable tally constraint applies only to this allocation-method contract. |
| Tally filtering API | The system shall allow configured tally filters to transform tally data before the selected allocation method is executed. |
| Result decoration API | The system shall provide an interface for post-processing an allocation result into a decorated result. |

### Communication interfaces
No network or inter-process communication interface is specified for this system.

### Data exchange formats
| Format | Usage |
|---|---|
| In-memory Java objects | Tally, candidate, result, processor configuration, properties, filters, and decorators are exchanged through Java APIs. |
| XML | A tally may be loaded from XML using `Tally.fromXML()`. The launcher and processor configuration also support XML files for configuration, tally, and result input/output where the corresponding options are used. |
| Command-line arguments | CLI arguments may provide candidate vote totals in `Name:Votes` format, potential votes, method name, processor properties, and input/output file paths. |

## 4. Functional Requirements

| ID | Description | Trigger/Input | System behavior | Output | Priority | Verification |
|---|---|---|---|---|---|---|
| FR-001A | Provide a caller-facing seat allocation entry point. | A caller submits tally data, selects an allocation method, and provides configuration parameters. | The system shall process the submitted tally data using the selected allocation method and provided configuration. | An allocation `Result`, or an allocation error such as `SeatAllocationException` if processing fails. | High | Test |
| FR-001B | Define the processing contract for allocation methods. | The processor invokes a selected allocation method. | The allocation method shall receive a protected view of tally data and configuration parameters, and shall return an allocation result or report an allocation error. | A `Result`, or a `SeatAllocationException` if processing fails. | High | Inspection, Test |
| FR-002 | Support construction of tally data from candidate vote totals. | A caller creates a tally and adds candidates with vote counts. | The system shall accept candidate entries and use them as allocation input. | A populated tally suitable for processing. | High | Test |
| FR-003 | Support the documented electoral method families and variants. | A user or caller selects a supported allocation method. | The system shall make available the methods documented in the repository: majority (simple, qualified, absolute), ranked (by votes), equal proportions (Huntington-Hill), largest remainder (Hare, Droop, Imperiali), and highest averages (D'Hondt, Sainte-Lague/Webster with user-provided first divisor support, Imperiali, Danish). | Allocation performed according to the selected supported method. | High | Inspection |
| FR-004 | Support method-specific properties during allocation. | A caller or CLI user supplies method properties with a tally and selected method. | The system shall accept method properties as part of processing and apply them during allocation. | A result produced using the supplied properties. | Medium | Test |
| FR-005 | Derive the absolute-majority threshold from tally votes. | Absolute majority processing is requested for a tally. | The system shall compute the minimum votes as `(potentialVotes / 2) + 1` and use that value as the `minimumVotes` property for the underlying qualified-majority processing. | A result based on the computed threshold. | Medium | Test |
| FR-006 | Support highest-averages allocation through variant-specific divisor sequences. | A highest-averages method is invoked with a tally. | The highest-averages allocation function shall support divisor sequences defined by the specific variant and shall calculate each candidate's priority in each seat-allocation round according to that variant's divisor rule. Different highest-averages variants shall be able to produce their corresponding seat-allocation results through their respective divisor sequences. | A result for the selected highest-averages method. | Medium | Test |
| FR-007 | Support result decoration. | A caller or configured processor passes a result to a decorator implementation. | The system shall allow a result decorator to transform a result into a decorated result after allocation. | A decorated `Result`. | Low | Demonstration |
| FR-008 | Support XML-based tally loading. | A user or caller requests tally loading from XML. | The system shall provide XML-based tally loading through `Tally.fromXML()`. | A tally object loaded from XML data. | Medium | Test |
| FR-009 | Surface allocation failures as seat allocation exceptions. | Processing encounters an allocation error. | The system shall signal the failure by throwing `SeatAllocationException`. | Exception notification to the caller or launcher. | High | Test |
| FR-010 | Provide command-line allocation capabilities. | A command-line user invokes `JSeats` with options. | The system shall support querying available allocation methods and related extensions, submitting candidate vote totals or reading tally/configuration files, selecting an allocation method, setting processing parameters, and generating tally, allocation-result, or configuration output when output options are specified. | Method/filter/decorator listings, allocation results, output files, or error messages depending on the invoked options. | High | Demonstration, Test |
| FR-011 | Support the configured processor workflow. | A caller or CLI user provides tally data and processor configuration. | The system shall process tally data according to configured parameters, allocation method, tally filters, tie-breaking rules, and result decorators; it shall execute filtering, allocation, and decoration steps before returning the final allocation result. | A final allocation result that conforms to the supplied configuration. | Medium | Demonstration, Test |

## 5. Non-Functional Requirements

| ID | Quality attribute | Requirement | Priority | Verification |
|---|---|---|---|---|
| NFR-001 | Extensibility | The system should support introduction of additional allocation methods through a common allocation-method processing contract. Highest-averages variants should be expressible through their respective divisor sequences. | Medium | Inspection |
| NFR-002 | Extensibility | The system should support optional result post-processing through a separate result-decoration contract. | Low | Inspection |
| NFR-003 | Fault handling | When processing cannot be completed, the API shall report failure by raising `SeatAllocationException` rather than returning a normal result. | High | Test |
| NFR-004 | Usability | The product shall be usable through both a Java API and a command-line launcher. The CLI shall provide demonstrable options for listing available methods/extensions, providing tally/configuration input, selecting methods, setting parameters, and writing requested output files. | Medium | Demonstration, Test |

## 6. Data Requirements

| ID | Data item | Requirement |
|---|---|---|
| DR-001 | Tally | The system shall use tally data as the primary input for seat allocation processing. The caller-facing entry point may accept or set tally data, while allocation methods receive a protected tally view. |
| DR-002 | Candidate | The tally shall contain candidate entries with associated vote counts. |
| DR-003 | Properties | The system shall accept method and processor parameters as Java `Properties` or command-line processor-property inputs. |
| DR-004 | Result | The system shall return allocation output as a `Result` object and may write the result to an output file through the CLI when requested. |
| DR-005 | Minimum votes | For absolute majority processing, the system shall derive `minimumVotes` from tally potential votes using `(potentialVotes / 2) + 1`. |
| DR-006 | XML tally input | The system shall support tally input from XML through `Tally.fromXML()`. |
| DR-007 | Processor configuration | Processor configuration shall be able to include properties, selected method, tally data, tally filters, and result decorators. The architecture diagram also identifies tie-breaking rules as a configuration element. |
| DR-008 | CLI input and output data | The CLI shall accept candidate vote totals in `Name:Votes` form, optional potential-vote values, method names, processor properties, and input/output file paths for tally, configuration, and result data. |

## 7. Constraints

| ID | Constraint |
|---|---|
| C-001 | The product is constrained to a Java implementation. |
| C-002 | The immutable tally constraint applies only to the allocation-method contract and must not be extended into a global constraint on the caller-facing entry-point API. The caller-facing entry point may accept or set tally data before invoking an allocation method. |
| C-003 | Supported method scope is limited to the methods documented in the repository: majority (simple, qualified, absolute), ranked (by votes), equal proportions (Huntington-Hill), largest remainder (Hare, Droop, Imperiali), and highest averages (D'Hondt, Sainte-Lague/Webster with user-provided first divisor support, Imperiali, Danish). |
| C-004 | Web-interface-related requirements are excluded because no implemented web interface is in scope for this commit. |

## 8. Verification and Acceptance

| Requirement set | Verification method | Acceptance basis |
|---|---|---|
| FR-001A, FR-002, FR-004, FR-005, FR-006, FR-008, FR-009, FR-011 | Test | Confirm processing behavior, input handling, method properties, divisor-sequence behavior, XML loading, configured processor workflow, and exception signaling through automated tests. |
| FR-001B, FR-003, NFR-001, NFR-002, C-001, C-002, C-003, C-004 | Inspection | Confirm supported methods, API contracts, immutable-tally constraint scope, extensibility contracts, and excluded web-interface scope. |
| FR-007, FR-010, NFR-004 | Demonstration or Test | Demonstrate result decoration and command-line operation, including listing methods/extensions, accepting candidate or file input, selecting a method, setting parameters, and producing requested outputs. |
| DR-001 to DR-008 | Inspection or Test | Confirm data objects, command-line inputs, XML transformations, processor configuration fields, and output forms through API signatures, source inspection, and usage examples/tests. |

