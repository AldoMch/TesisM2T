# 软件需求规格说明书

## 1. 引言

### 目的
本 SRS 定义了针对仓库组件的、基于证据支持的需求。该组件打包了一个包含 PySpark 和嵌入式 Spark 2.4.5 发行版的 Airflow 环境，从而支持在 Airflow 机器上以及通过 Spark 提供的命令行入口点执行 Spark。

### 产品范围
根据仓库证据，产品范围限定为一个 Docker 化的 Airflow 环境，该环境包含 `pyspark`，因此 `spark-submit` 可以在 Airflow 机器内部工作；此外还包含一个捆绑的 Spark 发行版，用于暴露 Python shell 和 Spark 示例执行接口。证据中明确引用的受支持执行目标包括本地模式、Spark standalone、Mesos 和 YARN。

### 预期读者
本文档面向：
- 将 Airflow 与 Spark 执行集成的工程师
- 为打包环境配置 Spark master 目标的运维人员
- 验证打包 Spark 执行接口的测试人员

### 参考资料
- 仓库：`cordon-thiago/airflow-spark`
- 提交：`a8533d1aa50d74db29c0edf9cfa692fcd256f5bf`
- 仓库 URL：<https://github.com/cordon-thiago/airflow-spark>
- 证据来源：
  - `docker/docker-airflow/requirements.txt` (`E002`)
  - `docker/docker-airflow/spark_files/spark-2.4.5-bin-hadoop2.6/README.md` (`E001`)
  - `docker/docker-airflow/spark_files/spark-2.4.5-bin-hadoop2.6/examples/src/main/java/org/apache/spark/examples/ml/JavaBisectingKMeansExample.java` (`E005`)
  - `docker/docker-airflow/spark_files/spark-2.4.5-bin-hadoop2.6/examples/src/main/java/org/apache/spark/examples/ml/JavaGaussianMixtureExample.java` (`E006`)

## 2. 总体说明

### 产品视角
该仓库在 `docker/docker-airflow` 内打包了 Spark 工件，包括为 Hadoop `2.6` 构建的 Spark `2.4.5`，并声明了从 Airflow 机器执行 Spark 所需的 Python 侧和 Airflow 侧依赖项。

### 产品功能概述
证据支持以下产品功能：
- 通过 `./bin/pyspark` 提供 Python Spark shell
- 通过 `./bin/run-example` 提供示例执行
- 通过 `MASTER` 环境变量允许选择集群目标
- 通过包含 `pyspark` 支持从 Airflow 机器执行 Spark
- 通过 Spark 读取器以 `libsvm` 格式加载 ML 示例数据集

### 用户类别
- 从 Airflow 机器运行 Spark 作业的 Airflow 操作人员或平台工程师
- 调用 Spark shell 和捆绑示例程序的开发人员或测试人员
- 配置 `MASTER` 目标的集群运维人员

### 运行环境
- 位于 `docker/docker-airflow` 下的 Docker 化 Airflow 环境
- 包含 `pyspark` 的 Python 环境
- 为 Hadoop `2.6` 捆绑的 Spark `2.4.5`
- 证据引用的执行目标：`local`、`local[N]`、`spark://`、`mesos://` 和 `yarn`

### 假设与依赖
- `pyspark` 是 `spark-submit` 在 Airflow 机器内部工作的必需项（`E002`）
- 当目标为集群模式时，Spark 执行依赖于有效的 `MASTER` 设置（`E001`）
- ML 示例数据加载假定输入文件在提供给 Spark 读取器的路径上可用（`E005`、`E006`）

## 3. 外部接口需求

### 用户接口
证据仅支持命令行接口。

| 接口 | 需求 |
|---|---|
| Python shell | 系统应通过 `./bin/pyspark` 暴露一个 Python Spark shell。 |
| 示例运行器 | 系统应通过 `./bin/run-example` 暴露 Spark 示例执行功能。 |
| 环境配置 | 系统应接受 `MASTER` 环境变量以选择执行目标。 |

### 软件/API 接口
| 接口 | 需求 |
|---|---|
| PySpark | 打包的 Airflow 环境应包含 `pyspark`，以便 Spark 提交可以在 Airflow 机器内部运行。 |
| SparkSession reader | 捆绑的 Spark 环境应支持通过 `spark.read().format("libsvm").load(...)` 为包含的 ML 示例读取数据集。 |

### 通信接口
| 接口 | 需求 |
|---|---|
| Spark master 选择 | 系统应接受以下形式的 master 目标：`mesos://...`、`spark://...`、`yarn`、`local` 和 `local[N]`。 |

### 数据交换格式
| 格式 | 用途 |
|---|---|
| `libsvm` | 捆绑 ML 示例程序使用的输入数据集格式（`E005`、`E006`） |
| 环境变量字符串 | 用于选择执行后端的 `MASTER` 值（`E001`） |

## 4. 功能需求

| ID | 描述 | 触发器/输入 | 系统行为 | 输出 | 优先级 | 验证 | 来源证据 |
|---|---|---|---|---|---|---|---|
| FR-001 | 提供一个 Python Spark shell。 | 用户调用 `./bin/pyspark`。 | 系统应启动 Python Spark shell，并使 Spark 上下文可用于交互式执行。 | 可运行 Spark 命令（如 `sc.parallelize(range(1000)).count()`）的交互式 Python shell。 | 高 | 演示 | `E001` |
| FR-002 | 支持从打包发行版执行 Spark 示例。 | 用户调用 `./bin/run-example <example>`。 | 系统应通过 Spark 示例运行器执行捆绑的 Spark 示例程序。 | 示例程序结果输出到标准输出；对于 `SparkPi`，支持本地执行。 | 中 | 演示 | `E001` |
| FR-003 | 允许运行时选择 Spark 执行目标。 | 用户在运行示例前设置 `MASTER` 环境变量。 | 系统应使用 `MASTER` 值将工作提交到所选后端。 | 执行被定向到指定的 `mesos://`、`spark://`、`yarn`、`local` 或 `local[N]` 目标。 | 高 | 测试 | `E001` |
| FR-004 | 启用从 Airflow 机器提交 Spark。 | 使用声明的依赖项构建 Airflow 侧环境。 | 系统应在 Airflow 环境中包含 `pyspark`，以便 `spark-submit` 可以在该机器内部工作。 | Airflow 机器具有 Spark 提交所需的依赖项。 | 高 | 检查 | `E002` |
| FR-005 | 支持在捆绑的 ML 示例中加载 `libsvm` 数据集。 | Spark ML 示例通过 `spark.read().format("libsvm").load(path)` 读取数据集。 | 系统应接受 `libsvm` 作为包含的 ML 示例工作流的输入数据集格式。 | 数据集被加载到 Spark `Dataset` 中用于模型训练/评估。 | 中 | 测试 | `E005`、`E006` |

## 5. 非功能需求

| ID | 需求 | 质量属性 | 优先级 | 验证 | 来源证据 |
|---|---|---|---|---|---|
| NFR-001 | 打包的 Spark 运行时应与为 Hadoop `2.6` 构建的 Spark `2.4.5` 兼容。 | 兼容性 | 高 | 检查 | `E001` |
| NFR-002 | Airflow 侧 Python 环境应包含 `celery==4.1.1`、`kombu==4.2.0`、`tornado==5.1.1`、`werkzeug==0.16.0` 和 `SQLAlchemy==1.3.15` 的显式依赖版本；还应包含 `pyspark`。 | 可维护性和可复现性 | 中 | 检查 | `E002` |
| NFR-003 | 系统应至少支持五种示例提交流向的执行目标形式：`mesos://...`、`spark://...`、`yarn`、`local` 和 `local[N]`。 | 可移植性 | 中 | 测试 | `E001` |

## 6. 数据需求

| ID | 数据实体/对象 | 需求 | 来源证据 |
|---|---|---|---|
| DR-001 | `MASTER` 环境变量 | 系统应接受 `MASTER` 作为输入配置值，用于表示 Spark 执行后端。 | `E001` |
| DR-002 | `libsvm` 数据集 | 系统应接受 `libsvm` 格式的数据集，用于捆绑的 ML 示例处理。 | `E005`、`E006` |
| DR-003 | 示例数据集路径 | 捆绑的 ML 示例应能够从诸如 `data/mllib/sample_kmeans_data.txt` 之类的文件路径加载数据。 | `E005`、`E006` |

## 7. 约束

| ID | 约束 | 来源证据 |
|---|---|---|
| C-001 | 打包的 Spark 发行版被约束为 Spark `2.4.5` 和 Hadoop `2.6`。 | `E001` |
| C-002 | Airflow 机器内部的 Spark 提交依赖于包含 `pyspark`。 | `E002` |
| C-003 | 受支持的执行目标标识符仅限于明确有证据支持的这些：`mesos://`、`spark://`、`yarn`、`local` 和 `local[N]`。 | `E001` |
| C-004 | 文档化的 CLI 入口点是 `./bin/pyspark` 和 `./bin/run-example`。 | `E001` |

## 8. 验证与验收

| Requirement ID | Verification method | Acceptance criteria |
|---|---|---|
| FR-001 | 演示 | 运行 `./bin/pyspark` 允许执行 `sc.parallelize(range(1000)).count()` 并返回 `1000`。 |
| FR-002 | 演示 | 运行 `./bin/run-example SparkPi` 可启动并完成捆绑示例。 |
| FR-003 | 测试 | 将 `MASTER` 设置为每种受支持形式时，会导致提交使用对应目标语法，且接口不会拒绝。 |
| FR-004 | 检查 | 依赖声明显示 `pyspark` 存在于 Airflow 环境需求中。 |
| FR-005 | 测试 | 一个捆绑的 ML 示例使用 `format("libsvm").load(...)` 加载输入，并生成一个用于处理的 Spark 数据集。 |
| NFR-001 | 检查 | 打包 Spark 的路径/版本标识符指示 Spark `2.4.5` 和 Hadoop `2.6`。 |
| NFR-002 | 检查 | Airflow 需求文件包含指定的固定版本依赖项并包含 `pyspark`。 |
| NFR-003 | 测试 | 该接口接受全部五种有证据支持的执行目标形式。 |

## 9. 可追溯性矩阵

| ID | 需求 | 类型 | 来源 | 证据类型 | 验证 | 置信度 |
|---|---|---|---|---|---|---|
| FR-001 | 提供一个 Python Spark shell | 功能 | `E001` | 显式 | 演示 | 高 |
| FR-002 | 支持从打包发行版执行 Spark 示例 | 功能 | `E001` | 显式 | 演示 | 高 |
| FR-003 | 允许运行时选择 Spark 执行目标 | 功能 | `E001` | 显式 | 测试 | 高 |
| FR-004 | 启用从 Airflow 机器提交 Spark | 功能 | `E002` | 显式 | 检查 | 高 |
| FR-005 | 支持在捆绑的 ML 示例中加载 `libsvm` 数据集 | 功能 | `E005`、`E006` | 显式 | 测试 | 中 |
| NFR-001 | 与 Spark `2.4.5` 和 Hadoop `2.6` 的兼容性 | 非功能 | `E001` | 显式 | 检查 | 高 |
| NFR-002 | Airflow 侧环境的显式依赖版本 | 非功能 | `E002` | 显式 | 检查 | 高 |
| NFR-003 | 至少支持五种执行目标形式 | 非功能 | `E001` | 显式 | 测试 | 高 |
| DR-001 | 接受 `MASTER` 作为后端选择输入 | 数据 | `E001` | 显式 | 检查 | 高 |
| DR-002 | 接受 `libsvm` 数据集 | 数据 | `E005`、`E006` | 显式 | 检查 | 中 |
| DR-003 | 加载诸如 `data/mllib/sample_kmeans_data.txt` 之类的示例数据集路径 | 数据 | `E005`、`E006` | 显式 | 检查 | 中 |
