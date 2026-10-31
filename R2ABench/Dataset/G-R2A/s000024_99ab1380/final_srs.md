# Software Requirements Specification (SRS)

## 1. Introduction

### Purpose
This SRS defines evidence-backed requirements for the `oracle-quickstart/oci-jenkins` repository at commit `50abb3190215f8f8f34d5a7afe37581b5d1bfcd2`. The documented scope is the repository-supported deployment workflow for a Jenkins environment on Oracle Cloud Infrastructure (OCI), including standard configuration inputs and the existing-infrastructure example.

### Product scope
Based on the repository evidence, the product provides a Terraform-driven deployment workflow that:
- accepts OCI tenancy and identity inputs,
- accepts SSH access inputs,
- accepts Jenkins master deployment parameters,
- supports deployment into pre-existing OCI network infrastructure, and
- uses example configuration files such as `inputs_config.json` and `terraform.tfvars`.

### Intended audience
- Cloud operators deploying Jenkins on OCI
- DevOps engineers using the Terraform examples
- Reviewers validating configuration, network prerequisites, and access setup

### References
- Repository: `oracle-quickstart/oci-jenkins`
- Repository URL: https://github.com/oracle-quickstart/oci-jenkins
- Snapshot: https://github.com/oracle-quickstart/oci-jenkins/tree/50abb3190215f8f8f34d5a7afe37581b5d1bfcd2
- Evidence sources: `E001`–`E006`

## 2. Overall Description

### Product perspective
The repository is a deployment asset for OCI. Evidence shows it relies on Terraform inputs, OCI identifiers, SSH keys, and OCI virtual networking prerequisites rather than providing a standalone end-user application.

### Product functions summary
The supported functions evidenced in the repository are:
- capture OCI deployment inputs such as tenancy, compartment, user, region, fingerprint, and private key path (`E001`, `E003`);
- capture SSH authorized and private key paths for instance access (`E001`, `E003`);
- capture Jenkins master deployment parameters such as availability domain, subnet, display name, image, shape, and optional cloud-init user data (`E002`, `E005`);
- place the provided SSH public key into the default user’s `~/.ssh/authorized_keys` on the instance (`E002`, `E005`);
- support deployment using pre-existing OCI network infrastructure with route table, DHCP options, security list, and subnets (`E004`, `E006`);
- support a private-network example that depends on NAT, bastion host, and load balancer information (`E004`, `E006`);
- deploy from operator-supplied values in `terraform.tfvars` after Terraform initialization (`E004`, `E006`).

### User classes
- Deployment operator: prepares configuration values and runs the example deployment.
- Infrastructure administrator: prepares or supplies required OCI networking components for the existing-infrastructure scenario.

### Operating environment
Supported environment details evidenced in the repository:
- Oracle Cloud Infrastructure tenancy and compartments (`E001`, `E003`)
- OCI virtual cloud network constructs including route tables, DHCP options, security lists, subnets, and VNIC-attached instances (`E004`, `E006`)
- Terraform-based deployment workflow using variable files (`E003`, `E004`)

### Assumptions and dependencies
- The operator has valid OCI identifiers and credentials, including tenancy OCID, compartment OCID, user OCID, fingerprint, region, and private key path (`E001`, `E003`).
- SSH key material is available to authorize and access deployed instances (`E001`, `E002`, `E003`).
- For the existing-infrastructure example, the OCI virtual network is already set up with route table, DHCP options, security list, and subnets (`E004`, `E006`).
- For private-network use, NAT, bastion host, and load balancer prerequisites are already set up (`E004`, `E006`).

## 3. External Interface Requirements

### User interfaces
No graphical user interface is evidenced. The user-facing interfaces shown are configuration files and Terraform variable inputs:
- `inputs_config.json` (`E001`)
- `terraform.tfvars` (`E004`, `E006`)

### Software/API interfaces
- OCI account and infrastructure identifiers are supplied as input values (`E001`, `E003`).
- Terraform consumes variables including tenancy, user, fingerprint, region, compartment, and SSH paths (`E003`).
- Jenkins master deployment parameters include subnet, image, shape, display name, and cloud-init user data (`E002`, `E005`).

### Communication interfaces
- SSH is used for instance access through authorized and private key inputs (`E001`, `E002`, `E003`).
- OCI networking interfaces include subnets and VNIC attachment to instances (`E004`, `E006`).
- In private-network scenarios, communication depends on NAT, bastion host, and load balancer setup (`E004`, `E006`).

### Data exchange formats
- JSON input format is evidenced by `inputs_config.json` (`E001`).
- Terraform variable file format is evidenced by `terraform.tfvars` usage (`E004`, `E006`).
- `master_user_data` must be base64-encoded when supplied (`E002`, `E005`).

## 4. Functional Requirements

| ID | Requirement | Trigger / Input | System behavior | Output | Priority | Verification | Source evidence |
|---|---|---|---|---|---|---|---|
| FR-001 | The deployment workflow shall accept OCI access configuration values for `tenancy_ocid`, `compartment_ocid`, `user_ocid`, `region`, `fingerprint`, and `private_key_path`. | Operator provides deployment variables. | The system accepts these values as deployment inputs. | Terraform variable set populated with OCI access values. | High | Inspection | `E001`, `E003` |
| FR-002 | The deployment workflow shall accept SSH access inputs for `ssh_authorized_keys` and `ssh_private_key`. | Operator provides SSH key paths. | The system accepts the public-key and private-key paths as deployment inputs. | Terraform variable set populated with SSH access values. | High | Inspection | `E001`, `E003` |
| FR-003 | The system shall place the supplied SSH authorized public key in the default user’s `~/.ssh/authorized_keys` file on the instance. | Operator supplies `ssh_authorized_keys`. | The system uses the provided public key for default-user instance authorization. | Deployed instance configured for SSH login by the supplied key. | High | Inspection | `E002`, `E005` |
| FR-004 | The deployment workflow shall accept Jenkins master configuration values including `label_prefix`, `master_ad`, `master_subnet_id`, `master_display_name`, `master_image_id`, `master_shape`, and optional `master_user_data`. | Operator provides Jenkins master settings. | The system accepts the supplied master deployment parameters. | Terraform variable set populated with master configuration. | High | Inspection | `E002`, `E005` |
| FR-005 | When `master_user_data` is provided, the system shall accept it as base64-encoded data for Cloud-Init custom scripts or configuration. | Operator provides `master_user_data`. | The system accepts the encoded user data for Cloud-Init use on the master instance. | Master instance receives supplied Cloud-Init data. | Medium | Inspection | `E002`, `E005` |
| FR-006 | The existing-infrastructure deployment workflow shall support deployment only after the operator updates `terraform.tfvars` with the required information. | Operator selects the existing-infrastructure example. | The system uses operator-supplied values from `terraform.tfvars` as deployment inputs. | Example deployment configuration is ready for initialization and deployment. | High | Demonstration | `E004`, `E006` |
| FR-007 | The existing-infrastructure deployment workflow shall require a preconfigured OCI virtual network including default route table, DHCP options, security list, and subnets. | Operator selects the existing-infrastructure example. | The system depends on the listed network components being present before deployment. | Deployment proceeds against existing OCI network resources. | High | Inspection | `E004`, `E006` |
| FR-008 | For private-network deployment, the workflow shall require a NAT gateway for the subnet used by Jenkins nodes. | Operator deploys using a private network. | The system depends on node subnets using NAT-enabled connectivity. | Node deployment target subnet satisfies the documented prerequisite. | High | Inspection | `E004`, `E006` |
| FR-009 | For private-network deployment, the workflow shall require a bastion machine with public IP provided as `bation_host`. | Operator deploys using a private network. | The system depends on a bastion host prerequisite identified by public IP. | Bastion prerequisite is available for the deployment scenario. | Medium | Inspection | `E004`, `E006` |
| FR-010 | For private-network deployment, the workflow shall require a load balancer with public IP provided as `lb_public_ip`. | Operator deploys using a private network. | The system depends on a load balancer prerequisite identified by public IP. | Load balancer prerequisite is available for the deployment scenario. | Medium | Inspection | `E004`, `E006` |
| FR-011 | The deployment workflow shall support Terraform initialization before cluster deployment. | Operator follows the example deployment steps. | The system is deployable through a Terraform initialization step followed by deployment execution. | Initialized Terraform working directory for cluster deployment. | Medium | Demonstration | `E004`, `E006` |

## 5. Non-Functional Requirements

| ID | Requirement | Quality attribute | Priority | Verification | Evidence type | Source evidence |
|---|---|---|---|---|---|---|
| NFR-001 | The system shall support operator-defined `label_prefix` values to create unique identifiers for multiple clusters within one compartment. | Compatibility / coexistence | Medium | Inspection | explicit | `E002`, `E005` |
| NFR-002 | The system shall use SSH key-based instance access, with authorization via a supplied public key and access via a supplied private key path. | Security | High | Inspection | explicit | `E001`, `E002`, `E003` |
| NFR-003 | The system shall support deployment into OCI-specific networking constructs including subnets and VNIC-attached instances. | Portability constraint / platform compatibility | High | Inspection | explicit | `E004`, `E006` |
| NFR-004 | For private-network scenarios, the deployment shall depend on NAT, bastion host, and load balancer prerequisites rather than direct unmanaged node exposure. | Security, inferred from documented topology prerequisites | Medium | Analysis | inferred | `E004`, `E006` |

## 6. Data Requirements

### Data entities / objects

| Data item | Description | Source evidence |
|---|---|---|
| `tenancy_ocid` | OCI tenancy identifier input | `E001`, `E003` |
| `compartment_ocid` | OCI compartment identifier input | `E001`, `E003` |
| `user_ocid` | OCI user identifier input | `E001`, `E003` |
| `region` | OCI region input | `E001`, `E003` |
| `fingerprint` | OCI credential fingerprint input | `E001`, `E003` |
| `private_key_path` | OCI API private key path input | `E001`, `E003` |
| `ssh_authorized_keys` | Public key path to authorize instance access | `E001`, `E002`, `E003`, `E005` |
| `ssh_private_key` | Private key path to access the instance | `E001`, `E002`, `E003`, `E005` |
| `label_prefix` | Unique identifier prefix for multiple clusters in a compartment | `E002`, `E005` |
| `master_ad` | Jenkins master availability domain | `E002`, `E005` |
| `master_subnet_id` | OCID of the master subnet used to create the VNIC | `E002`, `E005` |
| `master_display_name` | Jenkins master instance name | `E002`, `E005` |
| `master_image_id` | OCID of the image used for the master instance | `E002`, `E005` |
| `master_shape` | Compute shape for the master instance | `E002`, `E005` |
| `master_user_data` | Base64-encoded Cloud-Init data for custom scripts/configuration | `E002`, `E005` |
| `bation_host` | Bastion machine public IP for private-network example | `E004`, `E006` |
| `lb_public_ip` | Load balancer public IP for private-network example | `E004`, `E006` |

### Input/output data
- Inputs are provided through JSON and Terraform variable files (`E001`, `E004`, `E006`).
- Outputs evidenced are configured deployment resources and instance access enablement through SSH key placement (`E002`, `E005`).

### Storage, privacy, integrity, retention, migration
- The evidence shows storage of credential and key-path inputs in configuration files (`E001`).
- No explicit retention, migration, or privacy policy is evidenced in the repository materials provided.

## 7. Constraints

| ID | Constraint | Source evidence |
|---|---|---|
| C-001 | Deployment is constrained to Oracle Cloud Infrastructure concepts and identifiers such as tenancy, compartment, region, subnets, and VNICs. | `E001`, `E003`, `E004`, `E006` |
| C-002 | The existing-infrastructure example requires a pre-existing OCI virtual network with default route table, DHCP options, security list, and subnets. | `E004`, `E006` |
| C-003 | Private-network deployment requires NAT for the node subnet, a bastion machine public IP, and a load balancer public IP. | `E004`, `E006` |
| C-004 | Cloud-Init custom data for the master instance must be provided in base64-encoded form. | `E002`, `E005` |
| C-005 | Deployment is performed through Terraform configuration and variable inputs. | `E003`, `E004`, `E006` |

## 8. Verification and Acceptance

| Requirement ID | Verification method | Acceptance basis |
|---|---|---|
| FR-001 | Inspection | Deployment inputs include all required OCI access fields. |
| FR-002 | Inspection | Deployment inputs include both SSH public-key and private-key paths. |
| FR-003 | Inspection | Documentation/configuration states the public key is included in the default user’s `authorized_keys`. |
| FR-004 | Inspection | Documented master parameters are accepted as configurable inputs. |
| FR-005 | Inspection | `master_user_data` is documented as base64-encoded Cloud-Init data. |
| FR-006 | Demonstration | Example workflow uses updated `terraform.tfvars` as required input. |
| FR-007 | Inspection | Example documents the required existing OCI network components. |
| FR-008 | Inspection | Example documents NAT requirement for node subnet in private-network deployments. |
| FR-009 | Inspection | Example documents bastion host public IP prerequisite. |
| FR-010 | Inspection | Example documents load balancer public IP prerequisite. |
| FR-011 | Demonstration | Example documents Terraform initialization before deployment. |
| NFR-001 | Inspection | `label_prefix` is documented for unique identifiers across multiple clusters in one compartment. |
| NFR-002 | Inspection | SSH key-based authorization and access inputs are documented. |
| NFR-003 | Inspection | OCI networking and VNIC-based deployment context is documented. |
| NFR-004 | Analysis | Private-network prerequisites collectively support controlled network access architecture. |

## 9. Traceability Matrix

| ID | Requirement | Type | Source | Evidence Type | Verification | Confidence |
|---|---|---|---|---|---|---|
| FR-001 | Accept OCI access configuration values | Functional | `E001`, `E003` | explicit | Inspection | High |
| FR-002 | Accept SSH access inputs | Functional | `E001`, `E003` | explicit | Inspection | High |
| FR-003 | Place supplied public key in default user `authorized_keys` | Functional | `E002`, `E005` | explicit | Inspection | Medium |
| FR-004 | Accept Jenkins master deployment parameters | Functional | `E002`, `E005` | explicit | Inspection | High |
| FR-005 | Accept base64-encoded Cloud-Init user data | Functional | `E002`, `E005` | explicit | Inspection | Medium |
| FR-006 | Use `terraform.tfvars` for existing-infrastructure deployment input | Functional | `E004`, `E006` | explicit | Demonstration | Medium |
| FR-007 | Require preconfigured OCI virtual network for existing-infrastructure example | Functional | `E004`, `E006` | explicit | Inspection | High |
| FR-008 | Require NAT for private-network node subnet | Functional | `E004`, `E006` | explicit | Inspection | High |
| FR-009 | Require bastion host public IP for private-network deployment | Functional | `E004`, `E006` | explicit | Inspection | Medium |
| FR-010 | Require load balancer public IP for private-network deployment | Functional | `E004`, `E006` | explicit | Inspection | Medium |
| FR-011 | Support Terraform initialization before deployment | Functional | `E004`, `E006` | explicit | Demonstration | Medium |
| NFR-001 | Support unique identifiers for multiple clusters via `label_prefix` | Non-functional | `E002`, `E005` | explicit | Inspection | Medium |
| NFR-002 | Use SSH key-based access model | Non-functional | `E001`, `E002`, `E003` | explicit | Inspection | High |
| NFR-003 | Support OCI networking and VNIC deployment context | Non-functional | `E004`, `E006` | explicit | Inspection | Medium |
| NFR-004 | Depend on NAT, bastion, and load balancer in private-network scenarios | Non-functional | `E004`, `E006` | inferred | Analysis | Medium |
