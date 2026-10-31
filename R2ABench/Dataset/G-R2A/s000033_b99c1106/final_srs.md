# Software Requirements Specification

## 1. Introduction

### Purpose
This SRS defines the evidence-backed requirements for the repository component that packages an Airflow environment with PySpark and an embedded Spark 2.4.5 distribution, enabling Spark execution from the Airflow machine and through Spark-provided command-line entry points.

### Product scope
Based on the repository evidence, the product scope is limited to a Dockerized Airflow environment that includes `pyspark` so `spark-submit` can work inside the Airflow machine, plus a bundled Spark distribution that exposes the Python shell and Spark example execution interfaces. Supported execution targets explicitly referenced in evidence are local mode, Spark standalone, Mesos, and YARN.

### Intended audience
This document is intended for:
- Engineers integrating Airflow with Spark execution
- Operators configuring Spark master targets for the packaged environment
- Testers validating the packaged Spark execution interfaces

### References
- Repository: `cordon-thiago/airflow-spark`
- Commit: `a8533d1aa50d74db29c0edf9cfa692fcd256f5bf`
- Repository URL: <https://github.com/cordon-thiago/airflow-spark>
- Evidence sources:
  - `docker/docker-airflow/requirements.txt` (`E002`)
  - `docker/docker-airflow/spark_files/spark-2.4.5-bin-hadoop2.6/README.md` (`E001`)
  - `docker/docker-airflow/spark_files/spark-2.4.5-bin-hadoop2.6/examples/src/main/java/org/apache/spark/examples/ml/JavaBisectingKMeansExample.java` (`E005`)
  - `docker/docker-airflow/spark_files/spark-2.4.5-bin-hadoop2.6/examples/src/main/java/org/apache/spark/examples/ml/JavaGaussianMixtureExample.java` (`E006`)

## 2. Overall Description

### Product perspective
The repository packages Spark artifacts inside `docker/docker-airflow`, including Spark `2.4.5` built for Hadoop `2.6`, and declares Python and Airflow-side dependencies needed for Spark execution from the Airflow machine.

### Product functions summary
The evidence supports the following product functions:
- Provide a Python Spark shell through `./bin/pyspark`
- Provide example execution through `./bin/run-example`
- Allow cluster target selection through the `MASTER` environment variable
- Support Spark execution from the Airflow machine by including `pyspark`
- Load ML example datasets in `libsvm` format through Spark readers

### User classes
- Airflow operators or platform engineers running Spark jobs from the Airflow machine
- Developers or testers invoking Spark shells and bundled example programs
- Cluster operators configuring a `MASTER` target

### Operating environment
- Dockerized Airflow environment under `docker/docker-airflow`
- Python environment with `pyspark`
- Bundled Spark `2.4.5` for Hadoop `2.6`
- Execution targets referenced by evidence: `local`, `local[N]`, `spark://`, `mesos://`, and `yarn`

### Assumptions and dependencies
- `pyspark` is required for `spark-submit` to work inside the Airflow machine (`E002`)
- Spark execution depends on a valid `MASTER` setting when targeting cluster modes (`E001`)
- ML example data loading assumes input files are available at paths supplied to Spark readers (`E005`, `E006`)

## 3. External Interface Requirements

### User interfaces
The evidence supports command-line interfaces only.

| Interface | Requirement |
|---|---|
| Python shell | The system shall expose a Python Spark shell through `./bin/pyspark`. |
| Example runner | The system shall expose Spark example execution through `./bin/run-example`. |
| Environment configuration | The system shall accept the `MASTER` environment variable to select an execution target. |

### Software/API interfaces
| Interface | Requirement |
|---|---|
| PySpark | The packaged Airflow environment shall include `pyspark` so Spark submission can run inside the Airflow machine. |
| SparkSession reader | The bundled Spark environment shall support reading datasets via `spark.read().format("libsvm").load(...)` for the included ML examples. |

### Communication interfaces
| Interface | Requirement |
|---|---|
| Spark master selection | The system shall accept master targets in the forms `mesos://...`, `spark://...`, `yarn`, `local`, and `local[N]`. |

### Data exchange formats
| Format | Usage |
|---|---|
| `libsvm` | Input dataset format used by bundled ML example programs (`E005`, `E006`) |
| Environment variable string | `MASTER` value used to select execution backend (`E001`) |

## 4. Functional Requirements

| ID | Description | Trigger/Input | System behavior | Output | Priority | Verification | Source evidence |
|---|---|---|---|---|---|---|---|
| FR-001 | Provide a Python Spark shell. | User invokes `./bin/pyspark`. | The system shall start the Python Spark shell and make a Spark context available for interactive execution. | Interactive Python shell capable of running Spark commands such as `sc.parallelize(range(1000)).count()`. | High | Demonstration | `E001` |
| FR-002 | Support Spark example execution from the packaged distribution. | User invokes `./bin/run-example <example>`. | The system shall execute bundled Spark example programs through the Spark example runner. | Example program result on standard output; for `SparkPi`, local execution is supported. | Medium | Demonstration | `E001` |
| FR-003 | Allow runtime selection of Spark execution target. | User sets `MASTER` environment variable before running examples. | The system shall use the `MASTER` value to submit work to the selected backend. | Execution is directed to the specified `mesos://`, `spark://`, `yarn`, `local`, or `local[N]` target. | High | Test | `E001` |
| FR-004 | Enable Spark submission from the Airflow machine. | Airflow-side environment is built with declared dependencies. | The system shall include `pyspark` in the Airflow environment so `spark-submit` can work inside that machine. | Airflow machine has the dependency required for Spark submission. | High | Inspection | `E002` |
| FR-005 | Support loading `libsvm` datasets in bundled ML examples. | Spark ML example reads a dataset via `spark.read().format("libsvm").load(path)`. | The system shall accept `libsvm` as an input dataset format for the included ML example workflows. | Dataset is loaded into a Spark `Dataset` for model training/evaluation. | Medium | Test | `E005`, `E006` |

## 5. Non-Functional Requirements

| ID | Requirement | Quality attribute | Priority | Verification | Source evidence |
|---|---|---|---|---|---|
| NFR-001 | The packaged Spark runtime shall be compatible with Spark `2.4.5` built for Hadoop `2.6`. | Compatibility | High | Inspection | `E001` |
| NFR-002 | The Airflow-side Python environment shall include explicit dependency versions for `celery==4.1.1`, `kombu==4.2.0`, `tornado==5.1.1`, `werkzeug==0.16.0`, and `SQLAlchemy==1.3.15`; `pyspark` shall also be included. | Maintainability and reproducibility | Medium | Inspection | `E002` |
| NFR-003 | The system shall support at least five execution target forms for example submission: `mesos://...`, `spark://...`, `yarn`, `local`, and `local[N]`. | Portability | Medium | Test | `E001` |

## 6. Data Requirements

| ID | Data entity/object | Requirement | Source evidence |
|---|---|---|---|
| DR-001 | `MASTER` environment variable | The system shall accept `MASTER` as an input configuration value representing the Spark execution backend. | `E001` |
| DR-002 | `libsvm` dataset | The system shall accept datasets in `libsvm` format for bundled ML example processing. | `E005`, `E006` |
| DR-003 | Sample dataset path | The bundled ML examples shall be able to load data from file paths such as `data/mllib/sample_kmeans_data.txt`. | `E005`, `E006` |

## 7. Constraints

| ID | Constraint | Source evidence |
|---|---|---|
| C-001 | The packaged Spark distribution is constrained to Spark `2.4.5` with Hadoop `2.6`. | `E001` |
| C-002 | Spark submission inside the Airflow machine depends on inclusion of `pyspark`. | `E002` |
| C-003 | Supported execution target identifiers are limited to those explicitly evidenced: `mesos://`, `spark://`, `yarn`, `local`, and `local[N]`. | `E001` |
| C-004 | The documented CLI entry points are `./bin/pyspark` and `./bin/run-example`. | `E001` |

## 8. Verification and Acceptance

| Requirement ID | Verification method | Acceptance criteria |
|---|---|---|
| FR-001 | Demonstration | Running `./bin/pyspark` allows execution of `sc.parallelize(range(1000)).count()` and returns `1000`. |
| FR-002 | Demonstration | Running `./bin/run-example SparkPi` starts and completes the bundled example. |
| FR-003 | Test | Setting `MASTER` to each supported form causes submission to use that target syntax without interface rejection. |
| FR-004 | Inspection | Dependency declarations show `pyspark` present in the Airflow environment requirements. |
| FR-005 | Test | A bundled ML example loads input using `format("libsvm").load(...)` and produces a Spark dataset for processing. |
| NFR-001 | Inspection | Packaged Spark path/version identifiers indicate Spark `2.4.5` and Hadoop `2.6`. |
| NFR-002 | Inspection | The Airflow requirements file contains the specified pinned dependencies and includes `pyspark`. |
| NFR-003 | Test | The interface accepts all five evidenced execution target forms. |

## 9. Traceability Matrix

| ID | Requirement | Type | Source | Evidence Type | Verification | Confidence |
|---|---|---|---|---|---|---|
| FR-001 | Provide a Python Spark shell | Functional | `E001` | explicit | Demonstration | High |
| FR-002 | Support Spark example execution from the packaged distribution | Functional | `E001` | explicit | Demonstration | High |
| FR-003 | Allow runtime selection of Spark execution target | Functional | `E001` | explicit | Test | High |
| FR-004 | Enable Spark submission from the Airflow machine | Functional | `E002` | explicit | Inspection | High |
| FR-005 | Support loading `libsvm` datasets in bundled ML examples | Functional | `E005`, `E006` | explicit | Test | Medium |
| NFR-001 | Compatibility with Spark `2.4.5` and Hadoop `2.6` | Non-functional | `E001` | explicit | Inspection | High |
| NFR-002 | Explicit dependency versions for Airflow-side environment | Non-functional | `E002` | explicit | Inspection | High |
| NFR-003 | Support at least five execution target forms | Non-functional | `E001` | explicit | Test | High |
| DR-001 | Accept `MASTER` as backend-selection input | Data | `E001` | explicit | Inspection | High |
| DR-002 | Accept `libsvm` datasets | Data | `E005`, `E006` | explicit | Inspection | Medium |
| DR-003 | Load sample dataset paths such as `data/mllib/sample_kmeans_data.txt` | Data | `E005`, `E006` | explicit | Inspection | Medium |
