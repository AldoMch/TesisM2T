# 软件需求规格说明书（SRS）

## 1. 引言

### 目的
本 SRS 定义了针对提交 `50abb3190215f8f8f34d5a7afe37581b5d1bfcd2` 时 `oracle-quickstart/oci-jenkins` 仓库的、基于证据支持的需求。文档范围为该仓库支持的、面向 Oracle Cloud Infrastructure (OCI) 上 Jenkins 环境的部署工作流，包括标准配置输入和现有基础设施示例。

### 产品范围
根据仓库证据，该产品提供了一个由 Terraform 驱动的部署工作流，其功能包括：
- 接受 OCI 租户和身份输入，
- 接受 SSH 访问输入，
- 接受 Jenkins master 部署参数，
- 支持部署到预先存在的 OCI 网络基础设施中，以及
- 使用诸如 `inputs_config.json` 和 `terraform.tfvars` 等示例配置文件。

### 目标读者
- 在 OCI 上部署 Jenkins 的云运维人员
- 使用 Terraform 示例的 DevOps 工程师
- 验证配置、网络前提条件和访问设置的审查人员

### 参考资料
- 仓库：`oracle-quickstart/oci-jenkins`
- 仓库 URL: https://github.com/oracle-quickstart/oci-jenkins
- 快照：https://github.com/oracle-quickstart/oci-jenkins/tree/50abb3190215f8f8f34d5a7afe37581b5d1bfcd2
- 证据来源：`E001`–`E006`

## 2. 总体描述

### 产品视角
该仓库是 OCI 的部署资产。证据显示，它依赖 Terraform 输入、OCI 标识符、SSH 密钥以及 OCI 虚拟网络前提条件，而不是提供一个独立的终端用户应用程序。

### 产品功能概述
仓库中有证据支持的功能包括：
- 获取 OCI 部署输入，如 tenancy、compartment、user、region、fingerprint 和 private key path（`E001`, `E003`）；
- 获取用于实例访问的 SSH authorized 和 private key path（`E001`, `E003`）；
- 获取 Jenkins master 部署参数，如 availability domain、subnet、display name、image、shape，以及可选的 cloud-init user data（`E002`, `E005`）；
- 将提供的 SSH 公钥放置到实例默认用户的 `~/.ssh/authorized_keys` 中（`E002`, `E005`）；
- 支持使用预先存在的 OCI 网络基础设施进行部署，包括 route table、DHCP options、security list 和 subnets（`E004`, `E006`）；
- 支持依赖 NAT、bastion host 和 load balancer 信息的私有网络示例（`E004`, `E006`）；
- 在 Terraform 初始化之后，使用操作员在 `terraform.tfvars` 中提供的值进行部署（`E004`, `E006`）。

### 用户类别
- 部署操作员：准备配置值并运行示例部署。
- 基础设施管理员：为现有基础设施场景准备或提供所需的 OCI 网络组件。

### 运行环境
仓库中有证据支持的环境细节：
- Oracle Cloud Infrastructure 租户和 compartment（`E001`, `E003`）
- OCI 虚拟云网络构造，包括 route tables、DHCP options、security lists、subnets 和附加了 VNIC 的实例（`E004`, `E006`）
- 使用变量文件的基于 Terraform 的部署工作流（`E003`, `E004`）

### 假设与依赖
- 操作员具有有效的 OCI 标识符和凭证，包括 tenancy OCID、compartment OCID、user OCID、fingerprint、region 和 private key path（`E001`, `E003`）。
- 可用 SSH 密钥材料用于授权和访问已部署的实例（`E001`, `E002`, `E003`）。
- 对于现有基础设施示例，OCI 虚拟网络已预先配置好 route table、DHCP options、security list 和 subnets（`E004`, `E006`）。
- 对于私有网络用例，NAT、bastion host 和 load balancer 前提条件已预先配置完成（`E004`, `E006`）。

## 3. 外部接口需求

### 用户接口
没有图形用户界面的证据。展示的面向用户接口是配置文件和 Terraform 变量输入：
- `inputs_config.json`（`E001`）
- `terraform.tfvars`（`E004`, `E006`）

### 软件/API 接口
- OCI 账户和基础设施标识符作为输入值提供（`E001`, `E003`）。
- Terraform 使用变量，包括 tenancy、user、fingerprint、region、compartment 和 SSH 路径（`E003`）。
- Jenkins master 部署参数包括 subnet、image、shape、display name 和 cloud-init user data（`E002`, `E005`）。

### 通信接口
- SSH 用于通过 authorized 和 private key 输入进行实例访问（`E001`, `E002`, `E003`）。
- OCI 网络接口包括 subnets 以及实例的 VNIC 附加（`E004`, `E006`）。
- 在私有网络场景中，通信依赖 NAT、bastion host 和 load balancer 设置（`E004`, `E006`）。

### 数据交换格式
- `inputs_config.json` 证明使用了 JSON 输入格式（`E001`）。
- `terraform.tfvars` 的使用证明了 Terraform 变量文件格式（`E004`, `E006`）。
- 提供 `master_user_data` 时，必须采用 base64 编码（`E002`, `E005`）。

## 4. 功能需求

| ID | 需求 | 触发器 / 输入 | 系统行为 | 输出 | 优先级 | 验证 | 来源证据 |
|---|---|---|---|---|---|---|---|
| FR-001 | 部署工作流应接受 `tenancy_ocid`、`compartment_ocid`、`user_ocid`、`region`、`fingerprint` 和 `private_key_path` 的 OCI 访问配置值。 | 操作员提供部署变量。 | 系统接受这些值作为部署输入。 | 填充了 OCI 访问值的 Terraform 变量集。 | 高 | 检查 | `E001`, `E003` |
| FR-002 | 部署工作流应接受 `ssh_authorized_keys` 和 `ssh_private_key` 的 SSH 访问输入。 | 操作员提供 SSH 密钥路径。 | 系统接受公钥和私钥路径作为部署输入。 | 填充了 SSH 访问值的 Terraform 变量集。 | 高 | 检查 | `E001`, `E003` |
| FR-003 | 系统应将提供的 SSH 授权公钥放置在实例默认用户的 `~/.ssh/authorized_keys` 文件中。 | 操作员提供 `ssh_authorized_keys`。 | 系统使用提供的公钥进行默认用户实例授权。 | 已部署实例被配置为可通过提供的密钥进行 SSH 登录。 | 高 | 检查 | `E002`, `E005` |
| FR-004 | 部署工作流应接受 Jenkins master 配置值，包括 `label_prefix`、`master_ad`、`master_subnet_id`、`master_display_name`、`master_image_id`、`master_shape` 和可选的 `master_user_data`。 | 操作员提供 Jenkins master 设置。 | 系统接受提供的 master 部署参数。 | 填充了 master 配置的 Terraform 变量集。 | 高 | 检查 | `E002`, `E005` |
| FR-005 | 当提供 `master_user_data` 时，系统应将其作为 base64 编码数据接受，用于 Cloud-Init 自定义脚本或配置。 | 操作员提供 `master_user_data`。 | 系统接受编码后的 user data，以供 master 实例上的 Cloud-Init 使用。 | master 实例接收到提供的 Cloud-Init 数据。 | 中 | 检查 | `E002`, `E005` |
| FR-006 | 现有基础设施部署工作流应仅在操作员使用所需信息更新 `terraform.tfvars` 之后支持部署。 | 操作员选择现有基础设施示例。 | 系统使用 `terraform.tfvars` 中由操作员提供的值作为部署输入。 | 示例部署配置已准备好进行初始化和部署。 | 高 | 演示 | `E004`, `E006` |
| FR-007 | 现有基础设施部署工作流应要求预先配置好的 OCI 虚拟网络，包括默认 route table、DHCP options、security list 和 subnets。 | 操作员选择现有基础设施示例。 | 系统依赖于在部署前已存在所列网络组件。 | 部署针对现有 OCI 网络资源进行。 | 高 | 检查 | `E004`, `E006` |
| FR-008 | 对于私有网络部署，工作流应要求 Jenkins 节点所用 subnet 具备 NAT gateway。 | 操作员使用私有网络进行部署。 | 系统依赖节点 subnet 使用启用了 NAT 的连接。 | 节点部署目标 subnet 满足文档化前提条件。 | 高 | 检查 | `E004`, `E006` |
| FR-009 | 对于私有网络部署，工作流应要求一个公共 IP 作为 `bation_host` 提供的 bastion machine。 | 操作员使用私有网络进行部署。 | 系统依赖一个由公共 IP 标识的 bastion host 前提条件。 | 部署场景所需的 bastion 前提条件可用。 | 中 | 检查 | `E004`, `E006` |
| FR-010 | 对于私有网络部署，工作流应要求一个公共 IP 作为 `lb_public_ip` 提供的 load balancer。 | 操作员使用私有网络进行部署。 | 系统依赖一个由公共 IP 标识的 load balancer 前提条件。 | 部署场景所需的 load balancer 前提条件可用。 | 中 | 检查 | `E004`, `E006` |
| FR-011 | 部署工作流应支持在集群部署之前进行 Terraform 初始化。 | 操作员遵循示例部署步骤。 | 系统可通过先执行 Terraform 初始化步骤再执行部署来进行部署。 | 已初始化的 Terraform 工作目录可用于集群部署。 | 中 | 演示 | `E004`, `E006` |

## 5. 非功能需求

| ID | 需求 | 质量属性 | 优先级 | 验证 | 证据类型 | 来源证据 |
|---|---|---|---|---|---|---|
| NFR-001 | 系统应支持由操作员定义的 `label_prefix` 值，以便在同一个 compartment 中为多个集群创建唯一标识符。 | 兼容性 / 共存性 | 中 | 检查 | explicit | `E002`, `E005` |
| NFR-002 | 系统应使用基于 SSH 密钥的实例访问方式，通过提供的公钥进行授权，通过提供的私钥路径进行访问。 | 安全性 | 高 | 检查 | explicit | `E001`, `E002`, `E003` |
| NFR-003 | 系统应支持部署到 OCI 特定的网络构造中，包括 subnets 和附加了 VNIC 的实例。 | 可移植性约束 / 平台兼容性 | 高 | 检查 | explicit | `E004`, `E006` |
| NFR-004 | 对于私有网络场景，部署应依赖 NAT、bastion host 和 load balancer 前提条件，而不是直接暴露未受管控的节点。 | 安全性，根据文档化拓扑前提条件推断 | 中 | 分析 | inferred | `E004`, `E006` |

## 6. 数据需求

### 数据实体 / 对象

| 数据项 | 描述 | 来源证据 |
|---|---|---|
| `tenancy_ocid` | OCI 租户标识符输入 | `E001`, `E003` |
| `compartment_ocid` | OCI compartment 标识符输入 | `E001`, `E003` |
| `user_ocid` | OCI 用户标识符输入 | `E001`, `E003` |
| `region` | OCI region 输入 | `E001`, `E003` |
| `fingerprint` | OCI 凭证 fingerprint 输入 | `E001`, `E003` |
| `private_key_path` | OCI API 私钥路径输入 | `E001`, `E003` |
| `ssh_authorized_keys` | 用于授权实例访问的公钥路径 | `E001`, `E002`, `E003`, `E005` |
| `ssh_private_key` | 用于访问实例的私钥路径 | `E001`, `E002`, `E003`, `E005` |
| `label_prefix` | 在一个 compartment 中为多个集群提供唯一标识符前缀 | `E002`, `E005` |
| `master_ad` | Jenkins master 可用性域 | `E002`, `E005` |
| `master_subnet_id` | 用于创建 VNIC 的 master subnet 的 OCID | `E002`, `E005` |
| `master_display_name` | Jenkins master 实例名称 | `E002`, `E005` |
| `master_image_id` | 用于 master 实例的镜像 OCID | `E002`, `E005` |
| `master_shape` | master 实例的计算 shape | `E002`, `E005` |
| `master_user_data` | 用于自定义脚本/配置的 base64 编码 Cloud-Init 数据 | `E002`, `E005` |
| `bation_host` | 私有网络示例中的 bastion machine 公共 IP | `E004`, `E006` |
| `lb_public_ip` | 私有网络示例中的 load balancer 公共 IP | `E004`, `E006` |

### 输入/输出数据
- 输入通过 JSON 和 Terraform 变量文件提供（`E001`, `E004`, `E006`）。
- 有证据表明的输出包括已配置的部署资源，以及通过放置 SSH 密钥实现的实例访问启用（`E002`, `E005`）。

### 存储、隐私、完整性、保留、迁移
- 证据显示凭证和密钥路径输入存储在配置文件中（`E001`）。
- 在所提供的仓库材料中，没有明确体现保留、迁移或隐私策略。

## 7. 约束

| ID | 约束 | 来源证据 |
|---|---|---|
| C-001 | 部署受限于 Oracle Cloud Infrastructure 的概念和标识符，例如 tenancy、compartment、region、subnets 和 VNICs。 | `E001`, `E003`, `E004`, `E006` |
| C-002 | 现有基础设施示例要求预先存在的 OCI 虚拟网络包含默认 route table、DHCP options、security list 和 subnets。 | `E004`, `E006` |
| C-003 | 私有网络部署要求节点 subnet 具备 NAT、一个 bastion machine 公共 IP，以及一个 load balancer 公共 IP。 | `E004`, `E006` |
| C-004 | master 实例的 Cloud-Init 自定义数据必须以 base64 编码形式提供。 | `E002`, `E005` |
| C-005 | 部署通过 Terraform 配置和变量输入执行。 | `E003`, `E004`, `E006` |

## 8. 验证与验收

| Requirement ID | 验证方法 | 验收依据 |
|---|---|---|
| FR-001 | 检查 | 部署输入包含所有必需的 OCI 访问字段。 |
| FR-002 | 检查 | 部署输入同时包含 SSH 公钥和私钥路径。 |
| FR-003 | 检查 | 文档/配置说明公钥被包含在默认用户的 `authorized_keys` 中。 |
| FR-004 | 检查 | 文档化的 master 参数被接受为可配置输入。 |
| FR-005 | 检查 | `master_user_data` 被文档说明为 base64 编码的 Cloud-Init 数据。 |
| FR-006 | 演示 | 示例工作流按要求使用已更新的 `terraform.tfvars` 作为输入。 |
| FR-007 | 检查 | 示例文档说明了所需的现有 OCI 网络组件。 |
| FR-008 | 检查 | 示例文档说明了私有网络部署中节点 subnet 的 NAT 要求。 |
| FR-009 | 检查 | 示例文档说明了 bastion host 公共 IP 前提条件。 |
| FR-010 | 检查 | 示例文档说明了 load balancer 公共 IP 前提条件。 |
| FR-011 | 演示 | 示例文档说明了部署前需要进行 Terraform 初始化。 |
| NFR-001 | 检查 | `label_prefix` 被文档说明用于同一 compartment 中多个集群的唯一标识符。 |
| NFR-002 | 检查 | 文档说明了基于 SSH 密钥的授权和访问输入。 |
| NFR-003 | 检查 | 文档说明了 OCI 网络和基于 VNIC 的部署上下文。 |
| NFR-004 | 分析 | 私有网络前提条件共同支持受控的网络访问架构。 |

## 9. 可追踪性矩阵

| ID | 需求 | 类型 | 来源 | 证据类型 | 验证 | 置信度 |
|---|---|---|---|---|---|---|
| FR-001 | 接受 OCI 访问配置值 | Functional | `E001`, `E003` | explicit | Inspection | High |
| FR-002 | 接受 SSH 访问输入 | Functional | `E001`, `E003` | explicit | Inspection | High |
| FR-003 | 将提供的公钥放入默认用户的 `authorized_keys` | Functional | `E002`, `E005` | explicit | Inspection | Medium |
| FR-004 | 接受 Jenkins master 部署参数 | Functional | `E002`, `E005` | explicit | Inspection | High |
| FR-005 | 接受 base64 编码的 Cloud-Init user data | Functional | `E002`, `E005` | explicit | Inspection | Medium |
| FR-006 | 对现有基础设施部署输入使用 `terraform.tfvars` | Functional | `E004`, `E006` | explicit | Demonstration | Medium |
| FR-007 | 对现有基础设施示例要求预配置的 OCI 虚拟网络 | Functional | `E004`, `E006` | explicit | Inspection | High |
| FR-008 | 对私有网络节点 subnet 要求 NAT | Functional | `E004`, `E006` | explicit | Inspection | High |
| FR-009 | 对私有网络部署要求 bastion host 公共 IP | Functional | `E004`, `E006` | explicit | Inspection | Medium |
| FR-010 | 对私有网络部署要求 load balancer 公共 IP | Functional | `E004`, `E006` | explicit | Inspection | Medium |
| FR-011 | 支持部署前进行 Terraform 初始化 | Functional | `E004`, `E006` | explicit | Demonstration | Medium |
| NFR-001 | 通过 `label_prefix` 支持多个集群的唯一标识符 | Non-functional | `E002`, `E005` | explicit | Inspection | Medium |
| NFR-002 | 使用基于 SSH 密钥的访问模型 | Non-functional | `E001`, `E002`, `E003` | explicit | Inspection | High |
| NFR-003 | 支持 OCI 网络和 VNIC 部署上下文 | Non-functional | `E004`, `E006` | explicit | Inspection | Medium |
| NFR-004 | 在私有网络场景中依赖 NAT、bastion 和 load balancer | Non-functional | `E004`, `E006` | inferred | Analysis | Medium |
