# Checked Software Requirements Specification: OCI Jenkins Terraform Deployment

## 1. Introduction

### 1.1 Purpose

This Software Requirements Specification defines the checked requirements for a Terraform-driven workflow that deploys a Jenkins environment on Oracle Cloud Infrastructure (OCI). The document is intended for architecture view generation and excludes review notes, provenance fields, commit metadata, and supporting-material identifiers.

### 1.2 Product Scope

The system covered by this SRS is an infrastructure-as-code deployment workflow for Jenkins on OCI. It shall support:

- OCI tenancy, identity, region, and compartment configuration.
- SSH key configuration for instance authorization and access.
- Jenkins master instance configuration.
- Jenkins slave or agent instance configuration.
- Deployment into pre-existing OCI networking.
- Private-network deployment prerequisites for Jenkins nodes.
- Terraform variable-file based configuration.
- Terraform initialization, planning, and apply execution.

The system is not a standalone end-user application and does not provide a graphical user interface.

### 1.3 Intended Audience

The intended audience includes cloud operators, DevOps engineers, infrastructure administrators, testers, and architecture evaluators who need a clean requirement set for the OCI Jenkins deployment workflow.

### 1.4 Definitions and Abbreviations

- AD: Availability Domain.
- API: Application Programming Interface.
- Cloud-Init: Instance initialization mechanism for custom scripts and configuration.
- JNLP: Jenkins remoting protocol used for master-to-agent communication.
- OCI: Oracle Cloud Infrastructure.
- OCID: Oracle Cloud Identifier.
- SRS: Software Requirements Specification.
- VCN: Virtual Cloud Network.
- VNIC: Virtual Network Interface Card.

## 2. Overall Description

### 2.1 Product Perspective

The product is a Terraform-based deployment asset for provisioning a Jenkins cluster on OCI. It uses operator-provided variable values, OCI identifiers, SSH key paths, and network object identifiers to configure and deploy Jenkins components.

The deployment topology shall account for an OCI tenancy, compartment, VCN, one or more availability domains, a Jenkins master instance, and Jenkins slave or agent instances. The master instance may be placed in a public subnet, while slave or agent instances may be placed in private subnets. Private-network operation depends on prepared NAT, bastion, and load-balancing arrangements.

### 2.2 Product Functions

The product shall provide the following high-level functions:

- Collect OCI access and identity configuration.
- Collect SSH public-key and private-key paths.
- Collect Jenkins master deployment parameters.
- Collect Jenkins slave or agent deployment parameters.
- Configure Jenkins master-to-slave communication.
- Support deployment into existing OCI network objects.
- Support private-network deployment prerequisites.
- Execute the Terraform workflow through initialization, plan review, and apply.

### 2.3 User Classes

- Deployment operators prepare variable values and run Terraform commands.
- Infrastructure administrators prepare OCI network objects and private-network prerequisites.
- DevOps engineers configure Jenkins master and slave or agent sizing, images, ports, plugins, and credentials.
- Testers verify variable handling, Terraform execution, and deployed topology.

### 2.4 Operating Environment

The deployment workflow shall operate in an environment with Terraform installed and access to an OCI tenancy. The OCI environment shall include a compartment and the required VCN, subnets, route tables, DHCP options, security lists, and VNIC-capable compute instances.

Private-network deployments shall use prepared NAT connectivity for Jenkins node subnets, a bastion host for controlled SSH access, and a load-balancing arrangement where public access to the Jenkins service is required.

### 2.5 Assumptions and Dependencies

- The operator has valid OCI identifiers and credentials.
- The operator has SSH key material for instance authorization and access.
- The operator updates `terraform.tfvars` or equivalent variable files before running Terraform.
- Existing-infrastructure deployments rely on network objects prepared outside the workflow.
- The checked Terraform interface name for the bastion host is `bastion_host`; misspelled variants are not treated as the canonical interface.

## 3. External Interface Requirements

### 3.1 User Interface Requirements

#### UI-001 Configuration File Interface

The workflow shall expose user-facing configuration through files such as JSON input files and Terraform variable files.

#### UI-002 Command-Line Deployment Interface

The workflow shall be operated through Terraform command-line execution.

### 3.2 Software Interface Requirements

#### SI-001 OCI Credential Inputs

The workflow shall accept OCI access values including `tenancy_ocid`, `compartment_ocid`, `user_ocid`, `region`, `fingerprint`, and `private_key_path`.

#### SI-002 SSH Access Inputs

The workflow shall accept `ssh_authorized_keys` and `ssh_private_key` values for instance authorization and access.

#### SI-003 Terraform Variable Inputs

The workflow shall consume operator-supplied Terraform variables for OCI access, SSH access, Jenkins master configuration, Jenkins slave or agent configuration, bastion access, and deployment execution.

### 3.3 Communication Interface Requirements

#### CI-001 SSH Communication

The workflow shall use SSH key configuration to enable authorized access to provisioned instances.

#### CI-002 Jenkins Master-to-Slave Communication

The workflow shall configure Jenkins master-to-slave communication using the configured Jenkins service ports and master address information.

#### CI-003 Bastion-Mediated Access

For private-network deployment, the workflow shall support bastion-mediated access using `bastion_host`, `bastion_user`, and `bastion_private_key`.

#### CI-004 OCI Network Attachment

The workflow shall attach Jenkins instances to OCI subnets through VNIC-based instance networking.

### 3.4 Data Exchange Formats

#### DI-001 JSON Input Format

The workflow may use JSON files to provide test or example input values.

#### DI-002 Terraform Variable Format

The workflow shall use Terraform variable-file format for deployment input values.

#### DI-003 Cloud-Init Data Encoding

When custom Cloud-Init data is provided for master or slave instances, the data shall be provided in base64-encoded form.

## 4. Functional Requirements

### FR-001 Accept OCI Access Configuration

The deployment workflow shall accept OCI access configuration values for `tenancy_ocid`, `compartment_ocid`, `user_ocid`, `region`, `fingerprint`, and `private_key_path`.

**Priority:** High

**Verification:** Inspection of accepted variables and Terraform input mapping.

**Acceptance Criteria:**

- All required OCI access fields can be supplied by the operator.
- The supplied values are available to the Terraform execution context.

### FR-002 Accept SSH Access Configuration

The deployment workflow shall accept SSH access inputs for `ssh_authorized_keys` and `ssh_private_key`.

**Priority:** High

**Verification:** Inspection of accepted variables and Terraform input mapping.

**Acceptance Criteria:**

- The public-key path is accepted for instance authorization.
- The private-key path is accepted for instance access.

### FR-003 Configure Authorized SSH Keys

The deployment workflow shall include the supplied `ssh_authorized_keys` public key in the default user's `~/.ssh/authorized_keys` configuration for provisioned Jenkins instances where SSH access is configured.

**Priority:** High

**Verification:** Inspection of instance metadata, rendered configuration, or deployed instance state.

**Acceptance Criteria:**

- The configured public key is associated with the default user on provisioned Jenkins instances.
- SSH login can be attempted using the matching private key under the configured access path.

### FR-004 Accept Jenkins Cluster Configuration

The deployment workflow shall accept Jenkins cluster-level configuration values including `label_prefix`, `jenkins_version`, `jenkins_password`, `http_port`, `jnlp_port`, and `plugins`.

**Priority:** High

**Verification:** Inspection of accepted variables and Terraform module inputs.

**Acceptance Criteria:**

- The cluster can be given a label prefix for unique naming.
- Jenkins version, initial password, HTTP port, JNLP port, and plugin list can be supplied or defaulted.

### FR-005 Accept Jenkins Master Configuration

The deployment workflow shall accept Jenkins master configuration values including `master_ad`, `master_subnet_id`, `master_display_name`, `master_image_id`, `master_shape`, and optional `master_user_data`.

**Priority:** High

**Verification:** Inspection of accepted variables and master module inputs.

**Acceptance Criteria:**

- The master availability domain and subnet can be supplied.
- The master display name, image, and shape can be supplied or defaulted.
- Optional master Cloud-Init data can be supplied.

### FR-006 Accept Jenkins Slave or Agent Configuration

The deployment workflow shall accept Jenkins slave or agent configuration values including `slave_count`, `slave_ads`, `slave_subnet_ids`, `slave_display_name`, `slave_image_id`, `slave_shape`, and optional `slave_user_data`.

**Priority:** High

**Verification:** Inspection of accepted variables and slave module inputs.

**Acceptance Criteria:**

- The number of slave or agent instances can be configured.
- Slave or agent availability domains and subnet identifiers can be supplied.
- Slave or agent display name, image, and shape can be supplied or defaulted.
- Optional slave Cloud-Init data can be supplied.

### FR-007 Provision Jenkins Master and Slave Instances

The deployment workflow shall provision a Jenkins cluster composed of one master instance and the configured number of slave or agent instances.

**Priority:** High

**Verification:** Terraform plan inspection and deployment demonstration.

**Acceptance Criteria:**

- The plan includes a Jenkins master instance.
- The plan includes slave or agent instances according to `slave_count`.
- Slave or agent provisioning receives the configured master address and service port values needed for Jenkins communication.

### FR-008 Support Existing-Infrastructure Deployment

The existing-infrastructure workflow shall use operator-supplied values from `terraform.tfvars` or equivalent Terraform variable files.

**Priority:** High

**Verification:** Demonstration using the existing-infrastructure example.

**Acceptance Criteria:**

- The operator can update the variable file before execution.
- Terraform consumes the updated values during planning and apply.

### FR-009 Use Existing OCI Network Objects

For the existing-infrastructure workflow, the deployment shall target pre-existing OCI network objects, including route tables, DHCP options, security lists, and subnets.

**Priority:** High

**Verification:** Inspection of variable values and Terraform plan output.

**Acceptance Criteria:**

- Subnet identifiers can be provided for the master and slave or agent instances.
- The deployment does not assume that all network objects are created by this workflow in the existing-infrastructure scenario.

### FR-010 Support NAT-Enabled Private Node Subnets

For private-network deployment, the operator shall provide slave or agent subnets with NAT-enabled outbound connectivity.

**Priority:** Medium

**Verification:** Inspection of deployment prerequisites and subnet configuration.

**Acceptance Criteria:**

- Slave or agent subnet identifiers refer to subnets suitable for private-node deployment.
- NAT connectivity is treated as a deployment prerequisite rather than a Terraform-enforced validation unless explicit validation is configured.

### FR-011 Support Bastion Host Inputs

For private-network deployment, the workflow shall accept bastion access values including `bastion_host`, `bastion_user`, and `bastion_private_key`.

**Priority:** Medium

**Verification:** Inspection of accepted variables and module input mapping.

**Acceptance Criteria:**

- The `bastion_host` input is available to the master and slave provisioning modules where private access is configured.
- Bastion user and private-key values can be supplied.

### FR-012 Support Load-Balanced Public Access Prerequisite

For private-network deployment scenarios that expose Jenkins through a load balancer, the operator shall provide the required public load-balancer address information before deployment validation or operational handoff.

**Priority:** Medium

**Verification:** Inspection of deployment prerequisites and operational configuration.

**Acceptance Criteria:**

- The load-balancer public address is recorded for the private-network scenario when that scenario is used.
- The load-balancer prerequisite is not treated as a Terraform-enforced validation unless explicit validation is configured.

### FR-013 Support Terraform Deployment Sequence

The workflow shall support a Terraform deployment sequence consisting of initialization, plan review, and apply execution.

**Priority:** High

**Verification:** Demonstration of `terraform init`, `terraform plan`, and `terraform apply`.

**Acceptance Criteria:**

- `terraform init` initializes the working directory.
- `terraform plan` shows planned changes before execution.
- `terraform apply` provisions the configured Jenkins cluster on OCI.

## 5. Non-Functional Requirements

### NFR-001 OCI Platform Compatibility

The workflow shall be compatible with OCI tenancy, compartment, availability-domain, subnet, VCN, VNIC, and compute-instance concepts.

**Metric:** A valid Terraform plan can be generated using OCI identifiers for the configured deployment scenario.

### NFR-002 SSH Key-Based Access Security

The workflow shall use SSH key-based authorization and access rather than password-based instance access.

**Metric:** Instance access configuration includes a public key for authorization and a private key path for access.

### NFR-003 Cluster Coexistence

The workflow shall support unique naming for multiple Jenkins clusters in one compartment through `label_prefix`.

**Metric:** The cluster label prefix can be supplied and propagated to deployed object names where configured.

### NFR-004 Configuration Repeatability

The workflow shall support repeatable deployment by using Terraform variable files and the Terraform init, plan, and apply sequence.

**Metric:** Re-running the deployment with the same variable set produces a consistent Terraform plan subject to current OCI state.

### NFR-005 Network Exposure Control

Private-network deployments shall avoid unmanaged direct exposure of Jenkins slave or agent nodes by relying on private subnets, NAT-enabled outbound connectivity, bastion-mediated access, and load-balancer-based public entry where needed.

**Metric:** Private-network plans and operational configuration place slave or agent nodes in private subnets and document the required NAT, bastion, and load-balancer arrangements.

### NFR-006 Modifiability

The workflow shall allow operators to adjust Jenkins image, shape, count, ports, plugins, and Cloud-Init content through variables rather than direct code modification.

**Metric:** The configurable values are represented as Terraform variables or variable-file entries.

## 6. Data Requirements

### DR-001 OCI Access Data

The workflow shall maintain input values for `tenancy_ocid`, `compartment_ocid`, `user_ocid`, `region`, `fingerprint`, and `private_key_path`.

### DR-002 SSH Access Data

The workflow shall maintain input values for `ssh_authorized_keys` and `ssh_private_key`.

### DR-003 Jenkins Cluster Data

The workflow shall maintain cluster-level values for `label_prefix`, `jenkins_version`, `jenkins_password`, `http_port`, `jnlp_port`, and `plugins`.

### DR-004 Jenkins Master Data

The workflow shall maintain master instance values for `master_ad`, `master_subnet_id`, `master_display_name`, `master_image_id`, `master_shape`, and `master_user_data`.

### DR-005 Jenkins Slave or Agent Data

The workflow shall maintain slave or agent instance values for `slave_count`, `slave_ads`, `slave_subnet_ids`, `slave_display_name`, `slave_image_id`, `slave_shape`, and `slave_user_data`.

### DR-006 Bastion Access Data

The workflow shall maintain bastion access values for `bastion_host`, `bastion_user`, and `bastion_private_key`.

### DR-007 Existing-Infrastructure Variable Data

The workflow shall maintain existing-infrastructure deployment values in `terraform.tfvars` or equivalent Terraform variable files.

### DR-008 Cloud-Init Data

The workflow shall accept `master_user_data` and `slave_user_data` only as base64-encoded Cloud-Init content.

### DR-009 Private-Network Prerequisite Data

For private-network scenarios, the deployment record shall include NAT-enabled node subnet information, bastion host information, and load-balancer public address information where required.

## 7. System Constraints

### CON-001 OCI Deployment Constraint

The deployment is constrained to OCI identifiers and network concepts, including tenancy, compartment, region, availability domain, subnet, VCN, and VNIC.

### CON-002 Existing Network Constraint

The existing-infrastructure scenario requires prepared OCI network objects, including route table, DHCP options, security list, and subnets.

### CON-003 Private-Network Constraint

Private-network deployment requires prepared NAT connectivity for Jenkins node subnets, a bastion host for private access, and a load-balancing arrangement where public service access is required.

### CON-004 Terraform Constraint

Deployment shall be performed through Terraform configuration, Terraform variables, and Terraform command execution.

### CON-005 Cloud-Init Encoding Constraint

Custom Cloud-Init content for master or slave instances shall be provided as base64-encoded data.

### CON-006 Bastion Variable Constraint

The canonical bastion host variable name shall be `bastion_host`.

## 8. Verification and Acceptance Criteria

| Requirement | Verification Method | Expected Result |
| --- | --- | --- |
| FR-001 | Inspection | OCI access variables are accepted and passed into Terraform execution |
| FR-002 | Inspection | SSH public-key and private-key paths are accepted |
| FR-003 | Inspection or demonstration | The configured public key is associated with the default user on provisioned Jenkins instances |
| FR-004 | Inspection | Cluster-level Jenkins variables are accepted |
| FR-005 | Inspection | Master instance variables are accepted and passed to the master module |
| FR-006 | Inspection | Slave or agent variables are accepted and passed to the slave module |
| FR-007 | Terraform plan inspection and demonstration | One master and the configured slave or agent instances are planned or provisioned |
| FR-008 | Demonstration | Updated variable-file values are consumed by the existing-infrastructure workflow |
| FR-009 | Inspection | Existing subnet and network identifiers are used by the deployment |
| FR-010 | Inspection | Private node subnet prerequisites include NAT-enabled outbound connectivity |
| FR-011 | Inspection | Bastion inputs are accepted and passed to private-access provisioning where configured |
| FR-012 | Inspection | Load-balancer public address information is available where required |
| FR-013 | Demonstration | Terraform init, plan, and apply execute in sequence |
| NFR-001 | Terraform plan inspection | The plan uses OCI identifiers and network concepts |
| NFR-002 | Inspection | SSH key-based access fields are configured |
| NFR-003 | Inspection | `label_prefix` can be used for cluster naming |
| NFR-004 | Demonstration | Variable-file based execution can be repeated |
| NFR-005 | Analysis and inspection | Private-network deployment uses private node subnets and controlled access paths |
| NFR-006 | Inspection | Jenkins sizing, image, ports, plugins, and Cloud-Init values are configurable |

