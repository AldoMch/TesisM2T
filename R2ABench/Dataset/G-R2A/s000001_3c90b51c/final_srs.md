# Software Requirements Specification

## 1. Introduction

### Purpose
This SRS defines the evidenced requirements for `JSeats`, a Java library and command-line tool for electoral seat allocation, based only on the repository evidence for commit `3e4c0686a09ed12b6024d264168e317eebe678a4`.

### Product scope
`JSeats` provides electoral seat allocation algorithms through a Java API and a command-line launcher. The documented scope includes majority, ranked, equal proportions, largest remainder, and highest averages method families, with named variants such as D'Hondt, Sainte-Lague (Webster), Hare, Droop, Imperiali, and Danish. [E004]

### Intended audience
The intended audience includes:
- Java developers integrating seat allocation into software via the Java API. [E004, E002]
- Command-line users running seat allocation from a terminal. [E004]

### References
- Repository: `pau-minoves/jseats`
- Repository URL: https://github.com/pau-minoves/jseats
- Snapshot: https://github.com/pau-minoves/jseats/tree/3e4c0686a09ed12b6024d264168e317eebe678a4
- Primary evidence: [E001], [E002], [E003], [E004], [E005], [E006]

## 2. Overall Description

### Product perspective
`JSeats` is an electoral seat allocation component implemented in Java. It exposes a programmatic processing interface that accepts a tally plus method properties and returns a result, and it also provides a command-line launcher. [E004, E002]

### Product functions summary
The product supports:
- Allocation of seats using common electoral methods. [E004]
- Processing of a tally into a result through a Java API. [E001, E002]
- Method-specific parameterization through `Properties`. [E002, E005]
- Result decoration through a separate decorator interface. [E003]
- XML-based tally loading indicated by `Tally.fromXML()`. [E001]

### User classes
- Application developers using the Java API. [E004, E002]
- Operators or analysts using the command-line launcher. [E004]

### Operating environment
- Java runtime environment. [E004]
- Command-line shell environment for launcher use. [E004]

### Assumptions and dependencies
- Seat allocation processing depends on a caller-supplied tally and method properties. [E002]
- Some methods depend on tally-derived values such as potential votes and number of candidates. [E005, E006]

## 3. External Interface Requirements

### User interfaces
| Interface | Requirement |
|---|---|
| Command line | The system shall provide a command-line launcher for invoking seat allocation functions. [E004] |

### Software/API interfaces
| Interface | Requirement |
|---|---|
| Java processing API | The system shall provide a Java API for seat allocation processing. The processing interface accepts an immutable tally and method properties, and returns a result or raises a seat allocation exception. [E004, E002] |
| Result decoration API | The system shall provide an interface for post-processing a result into a decorated result. [E003] |

### Communication interfaces
No network or inter-process communication interface is evidenced in the provided material.

### Data exchange formats
| Format | Usage |
|---|---|
| In-memory Java objects | Tally, candidate, result, and properties are exchanged through the Java API. [E001, E002] |
| XML | A tally may be loaded from XML using `Tally.fromXML()`. [E001] |

## 4. Functional Requirements

| ID | Description | Trigger/Input | System behavior | Output | Priority | Verification | Source evidence |
|---|---|---|---|---|---|---|---|
| FR-001 | Provide seat allocation through a Java API. | A caller invokes the processing API with a tally and properties. | The system shall process the supplied tally using the selected seat allocation method. | A `Result`, or a `SeatAllocationException` if processing fails. | High | Test | [E004, E002] |
| FR-002 | Support construction of tally data from candidate vote totals. | A caller creates a tally and adds candidates with vote counts. | The system shall accept candidate entries and use them as allocation input. | A populated tally suitable for processing. | High | Test | [E001] |
| FR-003 | Support multiple electoral method families and listed variants. | A user selects a supported allocation method. | The system shall make available the supported methods documented in the repository: Majority, Ranked, Equal Proportions, Largest Remainder, and Highest Averages families, including the listed variants. | Allocation performed according to the selected supported method. | High | Inspection | [E004] |
| FR-004 | Support method-specific properties during allocation. | A caller supplies method properties with a tally. | The system shall accept method properties as part of processing and apply them during allocation. | A result produced using the supplied properties. | Medium | Test | [E002, E005] |
| FR-005 | Derive the absolute-majority threshold from tally votes. | Absolute majority processing is requested for a tally. | The system shall compute the minimum votes as `(potentialVotes / 2) + 1` and use that value as the `minimumVotes` property for the underlying qualified-majority processing. | A result based on the computed threshold. | Medium | Test | [E005] |
| FR-006 | Support highest-averages seat allocation rounds based on candidate count and divisors. | A highest-averages method is invoked with a tally. | The system shall process the tally using the number of candidates and a method-specific divisor progression. | A result for the selected highest-averages method. | Medium | Test | [E006] |
| FR-007 | Support result decoration. | A caller passes a result to a decorator implementation. | The system shall allow a decorator to transform a result into a decorated result. | A decorated `Result`. | Low | Demonstration | [E003] |
| FR-008 | Support XML-based tally loading. | A user requests tally loading from XML. | The system shall provide XML-based tally loading through `Tally.fromXML()`. | A tally object loaded from XML data. | Medium | Test | [E001] |
| FR-009 | Surface allocation failures as seat allocation exceptions. | Processing encounters an allocation error. | The system shall signal the failure by throwing `SeatAllocationException`. | Exception notification to the caller. | High | Test | [E002, E001] |

## 5. Non-Functional Requirements

| ID | Quality attribute | Requirement | Priority | Verification | Source evidence | Evidence type |
|---|---|---|---|---|---|---|
| NFR-001 | Extensibility | The system should support introduction of additional allocation methods through a common processing contract that accepts a tally and properties and returns a result. | Medium | Inspection | [E002] | inferred |
| NFR-002 | Extensibility | The system should support optional result post-processing through a separate result-decoration contract. | Low | Inspection | [E003] | inferred |
| NFR-003 | Fault handling | When processing cannot be completed, the API shall report failure by raising `SeatAllocationException` rather than returning a normal result. | High | Test | [E002, E001] | explicit |
| NFR-004 | Usability | The product shall be usable through both a Java API and a command-line launcher. | Medium | Demonstration | [E004] | explicit |

## 6. Data Requirements

| ID | Data item | Requirement | Source evidence |
|---|---|---|---|
| DR-001 | Tally | The system shall use a tally as the primary input object for seat allocation processing. | [E001, E002] |
| DR-002 | Candidate | The tally shall contain candidate entries with associated vote counts. | [E001] |
| DR-003 | Properties | The system shall accept method parameters as Java `Properties`. | [E002, E005] |
| DR-004 | Result | The system shall return allocation output as a `Result` object. | [E001, E002] |
| DR-005 | Minimum votes | For absolute majority processing, the system shall derive `minimumVotes` from tally potential votes using `(potentialVotes / 2) + 1`. | [E005] |
| DR-006 | XML tally input | The system shall support tally input from XML through `Tally.fromXML()`. | [E001] |

## 7. Constraints

| ID | Constraint | Source evidence |
|---|---|---|
| C-001 | The product is constrained to a Java implementation. | [E004] |
| C-002 | The public processing contract is constrained to inputs of an immutable tally and Java `Properties`, with output as `Result` or `SeatAllocationException`. | [E002] |
| C-003 | Supported method scope is limited to the methods documented in the repository evidence. | [E004] |

## 8. Verification and Acceptance

| Requirement set | Verification method | Acceptance basis |
|---|---|---|
| FR-001, FR-002, FR-004, FR-005, FR-006, FR-008, FR-009 | Test | Confirm processing behavior, input handling, method properties, XML loading, and exception signaling through automated tests. |
| FR-003, NFR-001, NFR-002, C-001, C-002, C-003 | Inspection | Confirm documented supported methods, contracts, and architectural constraints from repository artifacts. |
| FR-007, NFR-004 | Demonstration | Show result decoration and operation through both Java API and command-line entry points. |
| DR-001 to DR-006 | Inspection or Test | Confirm data objects and transformations through API signatures and usage examples/tests. |

## 9. Traceability Matrix

| ID | Requirement | Type | Source | Evidence Type | Verification | Confidence |
|---|---|---|---|---|---|---|
| FR-001 | Provide seat allocation through a Java API | Functional | E004, E002 | explicit | Test | High |
| FR-002 | Support construction of tally data from candidate vote totals | Functional | E001 | explicit | Test | High |
| FR-003 | Support documented method families and variants | Functional | E004 | explicit | Inspection | High |
| FR-004 | Support method-specific properties during allocation | Functional | E002, E005 | explicit | Test | High |
| FR-005 | Derive the absolute-majority threshold from tally votes | Functional | E005 | explicit | Test | High |
| FR-006 | Support highest-averages allocation using candidate count and divisors | Functional | E006 | explicit | Test | Medium |
| FR-007 | Support result decoration | Functional | E003 | explicit | Demonstration | Medium |
| FR-008 | Support XML-based tally loading | Functional | E001 | explicit | Test | Medium |
| FR-009 | Surface allocation failures as seat allocation exceptions | Functional | E002, E001 | explicit | Test | High |
| NFR-001 | Support addition of methods through a common contract | Non-functional | E002 | inferred | Inspection | Medium |
| NFR-002 | Support optional result post-processing through decorators | Non-functional | E003 | inferred | Inspection | Medium |
| NFR-003 | Report processing failure via exception | Non-functional | E002, E001 | explicit | Test | High |
| NFR-004 | Provide both Java API and command-line usability | Non-functional | E004 | explicit | Demonstration | High |
| DR-001 | Use tally as primary processing input | Data | E001, E002 | explicit | Inspection | High |
| DR-002 | Represent candidates with vote counts in tally | Data | E001 | explicit | Inspection | High |
| DR-003 | Accept method parameters as `Properties` | Data | E002, E005 | explicit | Inspection | High |
| DR-004 | Return output as `Result` | Data | E001, E002 | explicit | Inspection | High |
| DR-005 | Derive `minimumVotes` from potential votes for absolute majority | Data | E005 | explicit | Inspection | High |
| DR-006 | Support XML tally input | Data | E001 | explicit | Test | Medium |
| C-001 | Java implementation constraint | Constraint | E004 | explicit | Inspection | High |
| C-002 | Processing contract constrained to tally, properties, result, exception | Constraint | E002 | explicit | Inspection | High |
| C-003 | Supported method scope limited to documented methods | Constraint | E004 | explicit | Inspection | High |
