# Checked Software Requirements Specification: Airflow Spark Docker Integration

## 1. Introduction

### 1.1 Purpose
This Software Requirements Specification defines normalized requirements for an Airflow and Spark integration environment packaged with Docker Compose. The system enables a data engineer to run and observe Spark workloads from Airflow, use an interactive Jupyter/PySpark environment, and run selected bundled Spark distribution commands.

### 1.2 Scope
The product is an integrated Docker environment for Airflow-driven Spark job orchestration. Its core scope includes:
- Docker Compose deployment of Airflow, Postgres, Spark standalone master, Spark workers, and Jupyter/PySpark.
- Airflow DAG-driven Spark job submission to the Spark standalone cluster.
- Shared access to DAG files, Spark application files, notebooks, and input data files across the relevant containers.
- Airflow, Spark master, Jupyter, Spark cluster, and Postgres access through configured ports.
- Inclusion of PySpark in the Airflow image so Spark submission can run from the Airflow machine.

The packaged Spark distribution also provides inherited Spark capabilities, including the Python Spark shell, bundled example runner, Spark-supported master URL forms, and ML examples that load `libsvm` data. These inherited capabilities are retained as secondary requirements and should not be treated as the system's primary product differentiator.

### 1.3 Intended Audience
- Data engineers scheduling Spark jobs through Airflow.
- Platform engineers operating the Docker Compose environment.
- Developers using Jupyter/PySpark for interactive Spark work.
- Testers validating Spark job submission, container startup, and exposed service ports.
- Architecture-generation tools consuming a clean SRS without review metadata.

### 1.4 Definitions and Abbreviations
| Term | Definition |
|---|---|
| Airflow | Workflow scheduler used to define and run DAGs that submit Spark jobs. |
| DAG | Directed acyclic graph defining an Airflow workflow. |
| Spark standalone cluster | Spark deployment mode with a master and worker services. |
| Spark master | Cluster manager endpoint reachable at `spark://spark:7077`. |
| Spark worker | Service that executes Spark workloads assigned by the Spark master. |
| `SparkSubmitOperator` | Airflow operator used to submit Spark applications. |
| `spark_default` | Airflow Spark connection used by the DAG to reach the Spark cluster. |
| PySpark | Python interface for Spark. |
| `MASTER` | Environment variable used by Spark commands to select an execution backend. |
| `libsvm` | Dataset format used by bundled Spark ML examples. |

## 2. Overall Description

### 2.1 Product Perspective
The system is a local containerized data-processing environment. A data engineer interacts with Airflow for scheduled Spark jobs, Jupyter for interactive PySpark work, and service UIs for inspection. Airflow stores metadata in Postgres and submits configured Spark applications to the Spark standalone master. The Spark master coordinates one or more Spark workers that execute the workloads.

### 2.2 Function Summary
The system shall provide:
- Docker Compose startup for the required service set.
- An Airflow webserver and scheduler environment that can run Spark DAGs.
- A Spark standalone master and multiple Spark worker services.
- A Jupyter/PySpark service for interactive development.
- Shared mounted directories for DAGs, Spark applications, notebooks, and data files.
- Airflow Spark connection setup for the configured Spark standalone endpoint.
- Airflow DAG execution that submits Spark applications and exposes task logs.
- Spark master UI visibility for submitted Spark applications.
- Secondary access to bundled Spark shell and example execution commands.

### 2.3 User Classes
| User class | Description |
|---|---|
| Data engineer | Configures Airflow, runs DAGs, reviews Airflow logs, and checks Spark application execution. |
| Platform engineer | Builds the Airflow image and operates the Docker Compose environment. |
| Spark developer | Develops Spark applications and tests them through Airflow or Jupyter. |
| Notebook user | Runs interactive PySpark workloads through Jupyter. |
| Tester | Verifies container topology, service ports, Spark submission, and bundled Spark commands. |

### 2.4 Operating Environment
| Environment element | Required configuration |
|---|---|
| Docker Compose | Uses Compose file format `3.7` to run the multi-container environment. |
| Postgres | Runs PostgreSQL `9.6`, stores Airflow metadata, and exposes port `5432`. |
| Airflow webserver | Runs the `docker-airflow-spark:latest` image, uses LocalExecutor mode, depends on Postgres, and exposes port `8282`. |
| Spark master | Runs `bitnami/spark:latest`, uses `SPARK_MODE=master`, exposes web UI port `8181` and cluster port `7077`. |
| Spark workers | Run `bitnami/spark:latest`, use `SPARK_MODE=worker`, connect to `spark://spark:7077`, and use configured worker memory and core settings. |
| Jupyter/PySpark | Runs `jupyter/pyspark-notebook`, exposes notebook port `8888`, and exposes Spark application UI ports `4040-4080`. |
| Airflow Python environment | Includes pinned Airflow-side dependencies and `pyspark`. |
| Bundled Spark runtime | Includes Spark `2.4.5` built for Hadoop `2.6`. |

### 2.5 Architecture Context
The architecture contains:
- A Data Engineer actor.
- Postgres for Airflow metadata persistence.
- Airflow acting as the Spark driver and DAG scheduler.
- Jupyter Notebook with PySpark for interactive workloads.
- A Spark standalone cluster manager.
- Spark workers `spark-worker-1`, `spark-worker-2`, `spark-worker-3`, and an extensible worker pattern for additional workers.

Primary relationships:
- The Data Engineer accesses Airflow, Jupyter, and Postgres-facing capabilities.
- Airflow depends on Postgres for metadata.
- Airflow submits Spark applications to the Spark master at `spark://spark:7077`.
- The Spark master dispatches work to Spark workers.
- Jupyter can run interactive PySpark workloads against available Spark capabilities.
- Shared mounted directories make DAGs, Spark applications, notebooks, and input data available to the services that need them.

### 2.6 Assumptions and Dependencies
| ID | Assumption or dependency |
|---|---|
| AD-001 | Docker and Docker Compose are available on the host machine. |
| AD-002 | The Airflow Docker image is built before starting the Compose environment. |
| AD-003 | The `spark_default` Airflow connection is configured with host `spark://spark` and port `7077` before the Spark DAG is run. |
| AD-004 | Mounted directories provide consistent paths for DAGs, Spark applications, notebooks, and input data across Airflow, Spark, and Jupyter containers. |
| AD-005 | Spark worker services can reach the Spark master through the Compose network. |
| AD-006 | Jupyter token retrieval depends on the Jupyter container logs. |

## 3. External Interface Requirements

### 3.1 User Interfaces
| ID | Interface | Requirement |
|---|---|---|
| UI-001 | Airflow web UI | The system shall expose the Airflow web UI on host port `8282`. |
| UI-002 | Spark master UI | The system shall expose the Spark master web UI on host port `8181`. |
| UI-003 | Jupyter Notebook UI | The system shall expose Jupyter Notebook on host port `8888`. |
| UI-004 | Spark application UIs | The Jupyter/PySpark service shall expose Spark application UI ports `4040-4080`. |

### 3.2 Software and API Interfaces
| ID | Interface | Requirement |
|---|---|---|
| API-001 | Airflow DAG interface | The system shall load DAG definitions from the mounted DAG directory. |
| API-002 | `SparkSubmitOperator` | Airflow DAGs shall submit Spark applications through `SparkSubmitOperator`. |
| API-003 | Airflow Spark connection | Spark submission shall use the `spark_default` connection to reach the Spark standalone endpoint. |
| API-004 | Spark standalone endpoint | The Spark master shall accept application submission through `spark://spark:7077`. |
| API-005 | PySpark in Airflow | The Airflow environment shall include `pyspark` so Spark submission can run inside the Airflow container. |
| API-006 | PySpark notebook interface | The Jupyter service shall support interactive PySpark notebooks. |
| API-007 | Bundled Spark shell | The bundled Spark distribution shall expose `./bin/pyspark` as an inherited Spark capability. |
| API-008 | Bundled Spark example runner | The bundled Spark distribution shall expose `./bin/run-example` as an inherited Spark capability. |
| API-009 | Spark ML reader | Bundled ML examples shall be able to read `libsvm` datasets through Spark readers. |

### 3.3 Communication Interfaces
| ID | Interface | Requirement |
|---|---|---|
| CI-001 | Airflow to Postgres | Airflow shall depend on and communicate with Postgres for metadata persistence. |
| CI-002 | Airflow to Spark master | Airflow shall submit Spark jobs to the Spark master at `spark://spark:7077`. |
| CI-003 | Spark master to workers | Spark workers shall register with and receive work from the Spark master. |
| CI-004 | Host to service UIs | The host shall access Airflow, Spark master, Jupyter, and Spark application UIs through mapped ports. |
| CI-005 | Spark command target selection | Inherited Spark commands shall accept supported master target strings through the `MASTER` variable. |

### 3.4 Data Exchange Items
| ID | Data item | Description |
|---|---|---|
| DE-001 | Airflow metadata | DAG run, task, and scheduler metadata stored in Postgres. |
| DE-002 | DAG definition files | Workflow definitions loaded by Airflow. |
| DE-003 | Spark application files | Python Spark applications submitted by Airflow or used by Spark services. |
| DE-004 | Input data files | Data files mounted for Spark application processing. |
| DE-005 | Notebook files | Interactive notebook files mounted for Jupyter users. |
| DE-006 | Airflow Spark connection values | Connection host and port used for Spark submission. |
| DE-007 | Spark task logs | Airflow task output used to inspect Spark job results. |
| DE-008 | `MASTER` target value | Runtime backend selector used by inherited Spark commands. |
| DE-009 | `libsvm` datasets | Dataset format loaded by bundled ML examples. |

## 4. Functional Requirements

| ID | Requirement | Trigger/Input | Required behavior | Output | Priority | Verification |
|---|---|---|---|---|---|---|
| FR-001 | The system shall start as a Docker Compose environment containing Postgres, Airflow webserver, Spark master, Spark workers, and Jupyter/PySpark services. | Operator starts the Compose environment. | Create the configured service topology on the shared Compose network. | Running service containers. | High | Demonstration |
| FR-002 | The system shall expose service interfaces on the configured host ports. | Services start successfully. | Map Postgres to `5432`, Airflow to `8282`, Spark master UI to `8181`, Spark cluster endpoint to `7077`, Jupyter to `8888`, and Spark application UIs to `4040-4080`. | Reachable service endpoints. | High | Test |
| FR-003 | The Airflow service shall load DAG definitions from the mounted DAG directory. | Airflow container starts. | Make DAGs available in the Airflow web UI and scheduler. | Listed DAGs ready for triggering or scheduling. | High | Inspection |
| FR-004 | The Airflow DAG for Spark testing shall submit a Spark application through `SparkSubmitOperator`. | User runs the Spark test DAG. | Execute the DAG flow and submit the configured Spark application to the Spark standalone cluster. | Airflow task run and Spark application submission. | High | Demonstration |
| FR-005 | Spark submission shall target the configured Spark standalone master. | Airflow runs a Spark submission task. | Use `spark_default` and `spark://spark:7077` for the configured project deployment. | Spark job reaches the Spark master. | High | Test |
| FR-006 | The system shall provide observable Spark job execution through Airflow task logs and the Spark master UI. | A Spark job is submitted. | Display task output in Airflow logs and show the Spark application in the Spark master UI. | Job log output and Spark UI application entry. | High | Demonstration |
| FR-007 | Spark workers shall register with the Spark master and execute assigned Spark workloads. | Spark worker containers start. | Connect each worker to `spark://spark:7077` with configured memory and core settings. | Registered Spark workers available for execution. | High | Test |
| FR-008 | The system shall share DAG, Spark application, notebook, and input data directories across the containers that need them. | Containers start with mounted directories. | Mount the same logical files into Airflow, Spark, and Jupyter service contexts where applicable. | Files available to job submission and notebook workflows. | High | Inspection |
| FR-009 | The Airflow environment shall include PySpark so `spark-submit` can run inside the Airflow container. | Airflow image is built with Python dependencies. | Provide the `pyspark` dependency in the Airflow-side Python environment. | Spark submission capability inside Airflow. | High | Inspection |
| FR-010 | The Jupyter/PySpark service shall support interactive notebook workloads. | User opens Jupyter through the mapped port and token. | Provide a notebook workspace with PySpark capability and mounted notebook/data directories. | Interactive notebook session. | Medium | Demonstration |
| FR-011 | The bundled Spark distribution shall provide a Python Spark shell as an inherited Spark capability. | User invokes `./bin/pyspark`. | Start the Python Spark shell and allow simple Spark commands. | Interactive PySpark shell. | Low | Demonstration |
| FR-012 | The bundled Spark distribution shall provide example execution as an inherited Spark capability. | User invokes `./bin/run-example <example>`. | Run bundled Spark examples such as `SparkPi`. | Example output. | Low | Demonstration |
| FR-013 | The bundled Spark distribution shall accept `MASTER` for Spark command target selection as an inherited Spark capability. | User sets `MASTER` before running bundled Spark examples. | Accept Spark target forms including `local`, `local[N]`, `spark://...`, `mesos://...`, and `yarn`, subject to available runtime infrastructure. | Submission target selected for Spark command. | Low | Test |
| FR-014 | Bundled ML examples shall load `libsvm` datasets. | An ML example reads a dataset with Spark readers. | Load `libsvm` input into a Spark dataset for model processing. | Loaded Spark dataset. | Low | Test |

## 5. Non-Functional Requirements

| ID | Requirement | Quality attribute | Priority | Verification |
|---|---|---|---|---|
| NFR-001 | The packaged Spark runtime shall be compatible with Spark `2.4.5` built for Hadoop `2.6`. | Compatibility | High | Inspection |
| NFR-002 | The Airflow-side Python environment shall use pinned dependency versions for `celery==4.1.1`, `kombu==4.2.0`, `tornado==5.1.1`, `werkzeug==0.16.0`, and `SQLAlchemy==1.3.15`, and shall include `pyspark`. | Reproducibility | Medium | Inspection |
| NFR-003 | The configured project deployment shall verify Spark submission against the standalone master at `spark://spark:7077`; other Spark master URL forms shall be treated as inherited Spark compatibility rather than independently deployed project targets. | Portability | Medium | Test |
| NFR-004 | The environment shall support worker-count scaling by allowing additional Spark worker services to follow the existing worker configuration pattern. | Scalability | Medium | Inspection |
| NFR-005 | The environment shall provide operational observability through Airflow task logs, the Spark master UI, and container logs. | Observability | Medium | Demonstration |
| NFR-006 | Spark RPC authentication, RPC encryption, local storage encryption, and SSL are disabled in the provided local Compose configuration; the environment shall therefore be treated as a local development/testing setup unless security settings are changed. | Security | High | Inspection |

## 6. Data Requirements

| ID | Data requirement |
|---|---|
| DR-001 | Postgres shall persist Airflow metadata using the configured Airflow database credentials. |
| DR-002 | Airflow shall load DAG definition files from the mounted DAG directory. |
| DR-003 | Spark submission tasks shall reference Spark application files available at the shared application mount. |
| DR-004 | Spark applications and notebooks shall access input data files through mounted data directories. |
| DR-005 | Jupyter shall persist or access notebooks through the mounted notebook directory. |
| DR-006 | Airflow Spark connection data shall include host `spark://spark` and port `7077` for the configured Spark standalone cluster. |
| DR-007 | Spark job results shall be observable through Airflow task logs and Spark UI application state. |
| DR-008 | Bundled ML examples shall accept `libsvm` datasets as input. |
| DR-009 | Inherited Spark commands shall accept `MASTER` as a runtime backend selector. |

## 7. System Constraints

| ID | Constraint | Type |
|---|---|---|
| C-001 | The Airflow service depends on Postgres being available. | Runtime dependency |
| C-002 | Spark submission inside Airflow depends on `pyspark` being installed in the Airflow Python environment. | Runtime dependency |
| C-003 | The configured project Spark cluster target is `spark://spark:7077`. | Runtime configuration |
| C-004 | The packaged Spark distribution is constrained to Spark `2.4.5` with Hadoop `2.6`. | Compatibility |
| C-005 | Airflow web UI, Spark master UI, Jupyter, Spark application UI, Spark cluster, and Postgres access depend on the configured host port mappings. | Network |
| C-006 | The documented Spark CLI entry points inherited from the bundled Spark distribution are `./bin/pyspark` and `./bin/run-example`. | Interface |
| C-007 | Mesos, YARN, and generic `spark://...` target forms are inherited Spark target syntax unless this environment provides matching deployed infrastructure. | Scope |
| C-008 | The local Compose configuration disables several Spark security features and is therefore not suitable as-is for a hardened production deployment. | Security |

## 8. Verification and Acceptance Criteria

| Requirement ID | Verification method | Acceptance criterion |
|---|---|---|
| FR-001 | Demonstration | Docker Compose starts the required service containers. |
| FR-002 | Test | Host ports `5432`, `8282`, `8181`, `7077`, `8888`, and `4040-4080` are mapped as configured. |
| FR-003 | Inspection | Airflow lists the mounted DAGs in the web UI. |
| FR-004 | Demonstration | Running the Spark test DAG starts the `spark_job` task through `SparkSubmitOperator`. |
| FR-005 | Test | The Airflow Spark task uses `spark_default` and submits to `spark://spark:7077`; the run is visible in task logs or the Spark master UI. |
| FR-006 | Demonstration | Spark job output appears in Airflow task logs and the application appears in the Spark master UI. |
| FR-007 | Test | Spark workers register with the Spark master and are available for workload execution. |
| FR-008 | Inspection | Mounted directories expose DAG, Spark application, notebook, and input data files to the expected services. |
| FR-009 | Inspection | The Airflow Python environment includes `pyspark`. |
| FR-010 | Demonstration | Jupyter opens through the mapped port and supports interactive PySpark work. |
| FR-011 | Demonstration | Running `./bin/pyspark` allows execution of `sc.parallelize(range(1000)).count()` and returns `1000`. |
| FR-012 | Demonstration | Running `./bin/run-example SparkPi` starts and completes the bundled example. |
| FR-013 | Test | For `local` and `local[N]`, bundled Spark commands run locally; for other inherited forms, verification is limited to syntax and target forwarding unless matching infrastructure is provided. |
| FR-014 | Test | A bundled ML example loads `libsvm` input into a Spark dataset. |
| NFR-001 | Inspection | Packaged Spark identifiers show Spark `2.4.5` and Hadoop `2.6`. |
| NFR-002 | Inspection | The Airflow dependency list contains the pinned dependency versions and `pyspark`. |
| NFR-003 | Test | The project deployment verifies `spark://spark:7077`; inherited target forms are not treated as separately deployed targets. |
| NFR-004 | Inspection | Additional worker services can follow the same master URL, memory, core, and mount configuration pattern. |
| NFR-005 | Demonstration | Airflow logs, Spark master UI, and container logs can be used to inspect execution. |
| NFR-006 | Inspection | Local security-disablement settings are visible in the Spark service configuration. |
