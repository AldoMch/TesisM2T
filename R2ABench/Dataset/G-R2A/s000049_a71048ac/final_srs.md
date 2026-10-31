# Software Requirements Specification

## 1. Introduction

### Purpose
This SRS defines evidence-backed software requirements for `attic-nlp4l` at commit `26890e655f93e2486a51f0b033074e83951351c3`. The scope is limited to capabilities explicitly supported by the repository evidence.

### Product scope
NLP4L is a natural language processing tool for Apache Lucene written in Scala. Its stated purpose is to improve Lucene users' search experience using NLP techniques. It also supports collaboration with existing machine learning tools by creating document vectors from a Lucene index and writing them in LIBSVM format. The tutorial evidence additionally shows an experimental chart display capability for visualizing word count data. Sources: `E002`, `E003`, `E004`, `E001`.

### Intended audience
The evidence identifies the product as relevant to:
- Apache Lucene, Solr, and Elasticsearch users.
- Users preparing document vectors for existing machine learning tools such as Apache Spark and Apache Mahout.
- Users performing interactive, ad hoc processing in Scala.
Sources: `E002`, `E004`.

### References
- Repository: `NLP4L/attic-nlp4l`
- Commit: `26890e655f93e2486a51f0b033074e83951351c3`
- Evidence sources:
  - `README.md` (`E002`, `E003`)
  - `README_ja.md` (`E004`)
  - `docs/tutorial.md` (`E001`)
  - `src/main/scala/org/nlp4l/core/SchemaLoader.scala` (`E005`)
  - `src/main/scala/org/nlp4l/core/Schema.scala` (`E006`)

## 2. Overall Description

### Product perspective
The product is a Scala-based NLP tool built for the Apache Lucene ecosystem. It operates on document data stored in a Lucene index and leverages Lucene analyzer-normalized word data. It is positioned as a tool for search-related NLP workflows and for exchanging data with external machine learning tools. Sources: `E002`, `E003`, `E004`.

### Product functions summary
- Process document data registered in a Lucene index. Source: `E002`, `E004`.
- Provide direct access to analyzer-normalized word data and convenient search functions over indexed data. Source: `E002`, `E004`.
- Create document vectors from a Lucene index and write them as LIBSVM format files for machine learning workflows. Source: `E002`, `E003`, `E004`.
- Support interactive and ad hoc processing in Scala. Source: `E002`, `E004`.
- Provide an experimental chart display tool for visualizing word count data. Source: `E001`.

### User classes
| User class | Description | Source |
|---|---|---|
| Lucene ecosystem user | Users of Apache Lucene, Solr, or Elasticsearch seeking improved search-related NLP processing | `E004` |
| Machine learning workflow user | Users preparing document vectors for tools such as Apache Spark or Apache Mahout | `E004` |
| Scala interactive user | Users performing conversational or ad hoc processing in Scala | `E002`, `E004` |

### Operating environment
| Item | Requirement / Characterization | Evidence |
|---|---|---|
| Implementation language | The product is written in Scala | `E002`, `E004` |
| Primary platform | The product is for Apache Lucene | `E002`, `E003`, `E004` |
| Data source environment | The product processes document data registered in a Lucene index | `E002`, `E004` |

### Assumptions and dependencies
| Item | Statement | Evidence type | Source |
|---|---|---|---|
| Lucene index dependency | Product use assumes the availability of document data in a Lucene index | explicit | `E002`, `E004` |
| Analyzer-normalized data dependency | Access to normalized word data depends on Lucene analyzers having produced such normalized data in the index environment | explicit | `E002`, `E004` |
| ML tool integration context | LIBSVM export is intended for interoperability with existing machine learning tools | explicit | `E002`, `E003`, `E004` |
| Charting stability | Chart display capability is experimental and may change | explicit | `E001` |

## 3. External Interface Requirements

### User interfaces
| Interface | Requirement | Source |
|---|---|---|
| Scala interactive usage | The product shall support interactive and ad hoc processing in Scala | `E002`, `E004` |
| Chart presentation | The product may provide a presentation-oriented chart display interface for visualizing word count data; this interface is experimental | `E001` |

### Software/API interfaces
| Interface | Requirement | Source |
|---|---|---|
| Apache Lucene | The product shall operate on document data stored in Lucene indexes and use Lucene analyzer-normalized word data | `E002`, `E003`, `E004` |
| Machine learning tools | The product shall interoperate with external machine learning tools through document vector export in LIBSVM format | `E002`, `E003`, `E004` |
| Schema configuration loading | The product shall accept schema configuration from a resource or file path | `E005` |

### Communication interfaces
No network or protocol-level communication interface is explicitly supported by the evidence pack.

### Data exchange formats
| Format | Use | Source |
|---|---|---|
| Lucene index data | Input corpus and word data source | `E002`, `E004` |
| LIBSVM format file | Output format for document vector export | `E002`, `E003`, `E004` |
| Schema configuration with root object `schema` | Configuration input for schema loading | `E005` |

## 4. Functional Requirements

| ID | Description | Trigger / Input | System behavior | Output | Priority | Verification | Source evidence |
|---|---|---|---|---|---|---|---|
| FR-001 | Process Lucene-indexed document data for NLP use | User provides or selects document data registered in a Lucene index | The system shall process document data stored in a Lucene index as the primary corpus for NLP operations | Processed index-backed data made available for downstream use | High | Demonstration | `E002`, `E004` |
| FR-002 | Provide access to analyzer-normalized word data and search functionality | User operates on a Lucene index containing analyzer-normalized word data | The system shall provide access to normalized word data derived through Lucene analyzers and shall make search functions available over the indexed data | Word-level data and search results accessible to the user or downstream workflow | High | Demonstration | `E002`, `E004` |
| FR-003 | Export document vectors for ML interoperability | User requests document vector generation from a Lucene index | The system shall create document vectors from a Lucene index and write them to a LIBSVM format file for use by external machine learning tools | LIBSVM-format document vector file | High | Test | `E002`, `E003`, `E004` |
| FR-004 | Support interactive ad hoc Scala processing | User uses the product from a Scala-based interactive context | The system shall support interactive, conversational, or ad hoc processing in Scala | Immediate execution results in the Scala interaction context | Medium | Demonstration | `E002`, `E004` |
| FR-005 | Visualize word count data using chart display | User supplies previously obtained word count data to the chart display workflow | The system shall provide a chart display capability for visualizing word count data | Chart presentation of word count data | Low | Demonstration | `E001` |
| FR-006 | Load schema configuration from a resource or file path | User supplies a schema resource name or file path | The system shall load schema configuration from the specified resource or file path | In-memory schema representation, or an invalid schema error if the file is not found | Medium | Test | `E005` |

## 5. Non-Functional Requirements

| ID | Quality attribute | Requirement | Priority | Verification | Evidence type | Source evidence |
|---|---|---|---|---|---|---|
| NFR-001 | Compatibility | The system shall be compatible with Apache Lucene as its primary operating ecosystem | High | Inspection | explicit | `E002`, `E003`, `E004` |
| NFR-002 | Interoperability | The system shall produce document vector output in LIBSVM format to enable use with existing machine learning tools | High | Test | explicit | `E002`, `E003`, `E004` |
| NFR-003 | Usability | The system shall support interactive and ad hoc use in Scala to enable conversational experimentation | Medium | Demonstration | explicit | `E002`, `E004` |
| NFR-004 | Change stability | The chart display capability shall be treated as experimental, and compatibility of its functions and usage is not guaranteed across future revisions | Low | Inspection | explicit | `E001` |

## 6. Data Requirements

| ID | Data item / entity | Requirement | Source evidence |
|---|---|---|---|
| DR-001 | Lucene index document data | The primary input data shall be document data registered in a Lucene index | `E002`, `E004` |
| DR-002 | Analyzer-normalized word data | The system shall use word data normalized by Lucene analyzers as an accessible data source | `E002`, `E004` |
| DR-003 | Document vector output | Document vector output shall be representable as a LIBSVM format file | `E002`, `E003`, `E004` |
| DR-004 | Word count data | Word count results shall be usable as input to the chart display workflow | `E001` |
| DR-005 | Schema configuration | Schema configuration input shall support a root object named `schema`; if the root object is absent, the configuration is invalid | `E005` |
| DR-006 | Schema loading source | Schema configuration data shall be loadable from either a named resource or a file path | `E005` |

## 7. Constraints

| ID | Constraint | Source evidence |
|---|---|---|
| C-001 | The product is constrained to Scala as its implementation and user interaction language context | `E002`, `E004` |
| C-002 | The product is constrained to operation on Apache Lucene ecosystem data structures, specifically Lucene indexes and analyzer-normalized data | `E002`, `E003`, `E004` |
| C-003 | Machine learning interchange is constrained to the LIBSVM file format where document vector export is used | `E002`, `E003`, `E004` |
| C-004 | Chart display functionality is experimental and may change in function and usage | `E001` |
| C-005 | Schema configuration is constrained to include a root object named `schema` | `E005` |

## 8. Verification and Acceptance

| Requirement ID | Verification method | Acceptance basis |
|---|---|---|
| FR-001 | Demonstration | A Lucene index is processed and used as the operating corpus |
| FR-002 | Demonstration | Analyzer-normalized word data and search functionality are shown against Lucene-indexed data |
| FR-003 | Test | A document vector export operation produces a LIBSVM-format file from a Lucene index |
| FR-004 | Demonstration | An interactive Scala session performs ad hoc processing with observable results |
| FR-005 | Demonstration | Word count data is rendered as a chart presentation |
| FR-006 | Test | Schema configuration loads from resource and file path, and invalid file absence produces an invalid schema error |
| NFR-001 | Inspection | Product interfaces and scope remain aligned with Apache Lucene |
| NFR-002 | Test | Output files conform to LIBSVM usage expectations for external ML workflows |
| NFR-003 | Demonstration | Interactive Scala usage is available for ad hoc operation |
| NFR-004 | Inspection | Documentation and interface treatment identify chart display as experimental |

## 9. Traceability Matrix

| ID | Requirement | Type | Source | Evidence Type | Verification | Confidence |
|---|---|---|---|---|---|---|
| FR-001 | Process Lucene-indexed document data for NLP use | Functional | `E002`, `E004` | explicit | Demonstration | High |
| FR-002 | Provide access to analyzer-normalized word data and search functionality | Functional | `E002`, `E004` | explicit | Demonstration | Medium |
| FR-003 | Export document vectors for ML interoperability | Functional | `E002`, `E003`, `E004` | explicit | Test | High |
| FR-004 | Support interactive ad hoc Scala processing | Functional | `E002`, `E004` | explicit | Demonstration | High |
| FR-005 | Visualize word count data using chart display | Functional | `E001` | explicit | Demonstration | Medium |
| FR-006 | Load schema configuration from a resource or file path | Functional | `E005` | explicit | Test | Medium |
| NFR-001 | Compatibility with Apache Lucene ecosystem | Non-functional | `E002`, `E003`, `E004` | explicit | Inspection | High |
| NFR-002 | LIBSVM interoperability for ML workflows | Non-functional | `E002`, `E003`, `E004` | explicit | Test | High |
| NFR-003 | Interactive Scala usability | Non-functional | `E002`, `E004` | explicit | Demonstration | High |
| NFR-004 | Experimental stability status of chart display | Non-functional | `E001` | explicit | Inspection | High |
| DR-001 | Lucene index document data as primary input | Data | `E002`, `E004` | explicit | Inspection | High |
| DR-002 | Analyzer-normalized word data | Data | `E002`, `E004` | explicit | Inspection | Medium |
| DR-003 | LIBSVM document vector output | Data | `E002`, `E003`, `E004` | explicit | Inspection | High |
| DR-004 | Word count data as chart input | Data | `E001` | explicit | Inspection | Medium |
| DR-005 | Schema root object `schema` | Data | `E005` | explicit | Inspection | High |
| DR-006 | Schema loading from resource or file path | Data | `E005` | explicit | Inspection | High |
