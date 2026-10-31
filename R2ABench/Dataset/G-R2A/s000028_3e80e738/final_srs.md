# Software Requirements Specification

## 1. Introduction

### Purpose
This SRS defines evidence-backed requirements for the `pn-infra` repository components represented in the provided evidence pack: infrastructure templates and scripts for Cognito authentication resources, API Gateway exposure, VPC endpoints, and installation/deployment support.

### Product scope
The evidenced scope covers:
- AWS CloudFormation-based creation of Cognito user-pool and identity-pool resources
- API Gateway deployment and response-header exposure for role verification
- VPC interface endpoint configuration for Amazon SQS
- Installation-time provisioning inputs and environment-specific parameters

### Intended audience
This document is intended for:
- Infrastructure engineers deploying or reviewing the provided templates
- Integrators consuming the exposed API Gateway endpoint
- Security and operations reviewers validating network and identity configuration

### References
- Repository: `pagopa/pn-infra`
- Repository URL: https://github.com/pagopa/pn-infra
- Commit: `3898c35e634efe1527655e90a586ee6247de24f4`
- Evidence sources: `E001` to `E006`

## 2. Overall Description

### Product perspective
The evidenced product is an AWS infrastructure layer composed of CloudFormation templates and installation scripts. It provisions Cognito authentication resources, API Gateway deployment artifacts, and VPC interface connectivity to AWS services. Sources: `E001`, `E002`, `E003`, `E004`, `E005`.

### Product functions summary
- Create a Cognito user pool and identity pool through CloudFormation (`E002`)
- Associate a Cognito identity pool with a Cognito user-pool client/provider (`E001`)
- Permit unauthenticated identities in the identity pool (`E001`)
- Create a limited-access IAM role for unauthorized access paths tied to the identity pool (`E001`)
- Deploy an API Gateway stage and publish a callback endpoint URL (`E004`)
- Return a role-related response header from the `WhoAmI` API method (`E004`)
- Provision an SQS VPC interface endpoint with private DNS in specified subnets and VPC (`E003`)

### User classes
- Infrastructure operators invoking installation/setup commands and deploying templates (`E005`)
- API clients consuming the API Gateway callback endpoint and response headers (`E004`)
- Cognito-backed identities, including unauthenticated identities supported by the identity pool (`E001`)

### Operating environment
- AWS CloudFormation (`E002`)
- AWS Cognito User Pool and Identity Pool (`E001`, `E002`)
- AWS IAM roles (`E001`)
- AWS API Gateway (`E004`)
- AWS VPC, subnets, security groups, and VPC interface endpoints (`E003`)
- Amazon SQS via regional service endpoint naming (`E003`)

### Assumptions and dependencies
- Deployment depends on AWS account and region context supplied to CloudFormation and installation scripts (`E002`, `E003`, `E005`)
- API Gateway deployment depends on the `WhoAmI` and `ECS` methods being defined before deployment (`E004`)
- The VPC endpoint depends on an existing VPC, VPC CIDR, and target subnets being provided (`E003`)

## 3. External Interface Requirements

### User interfaces
No graphical user interface is evidenced. The repository exposes script- and template-driven operational interfaces through command execution and CloudFormation parameters. Source: `E002`, `E005`.

### Software/API interfaces

| Interface | Requirement |
|---|---|
| Cognito | The system uses AWS Cognito User Pool and Identity Pool resources and binds the identity pool to a Cognito provider using `ClientId` and `ProviderName`. Source: `E001`, `E002` |
| API Gateway | The system exposes an API Gateway deployment with a stage name parameter and a callback URL output. Source: `E004` |
| SQS via VPC Endpoint | The system integrates with Amazon SQS through an AWS VPC interface endpoint using the regional service name `com.amazonaws.${AWS::Region}.sqs`. Source: `E003` |
| IAM | The system creates IAM role resources for unauthorized access associated with the identity pool. Source: `E001` |

### Communication interfaces
- Private AWS network communication to SQS shall occur through an interface VPC endpoint with private DNS enabled. Source: `E003`
- API responses shall include the `x-pagopa-pn-cx-role` header on the evidenced `WhoAmI` method response. Source: `E004`

### Data exchange formats
- CloudFormation YAML templates are used for infrastructure declaration. Source: `E002`, `E003`, `E004`
- API Gateway response metadata includes HTTP header `x-pagopa-pn-cx-role`. Source: `E004`

## 4. Functional Requirements

| ID | Description | Trigger/Input | System behavior | Output | Priority | Verification | Source evidence |
|---|---|---|---|---|---|---|---|
| FR-001 | Provision Cognito authentication resources | Deployment of the Cognito CloudFormation stack with required parameters | The system shall create Cognito user-pool and identity-pool resources as part of the stack. | Created Cognito authentication resources | High | Inspection | `E002` |
| FR-002 | Support configurable token validity units | Stack parameters `AccessTokenValidityUnits`, `IdTokenValidityUnits`, `RefreshTokenValidityUnits` | The system shall accept token validity unit values only from `days`, `hours`, `minutes`, or `seconds` for the evidenced token unit parameters. | Parameterized token validity configuration | Medium | Inspection | `E002` |
| FR-003 | Bind identity pool to Cognito provider | Identity-pool creation with user-pool client and provider references | The system shall configure the identity pool with a Cognito identity provider using the specified `ClientId` and `ProviderName`. | Identity pool associated with Cognito provider | High | Inspection | `E001` |
| FR-004 | Permit unauthenticated identities | Identity-pool deployment | The system shall allow unauthenticated identities in the created identity pool. | Identity pool accepts unauthenticated identities | High | Inspection | `E001` |
| FR-005 | Create limited unauthorized-access role | Identity-pool deployment | The system shall create an IAM role for unauthorized access associated with the created identity pool. | Unauthorized-access IAM role | High | Inspection | `E001` |
| FR-006 | Expose user attributes for writes | User-pool client configuration | The system shall configure write access for the attributes `custom:Role` and `email`. | Writable user attributes include role and email | Medium | Inspection | `E001` |
| FR-007 | Deploy API Gateway stage | API Gateway deployment with `ApiGatewayStageName` | The system shall create an API Gateway deployment using the provided stage name. | Deployed API Gateway stage | High | Inspection | `E004` |
| FR-008 | Publish API callback endpoint | Successful API Gateway deployment | The system shall output a callback URL identified as the API Gateway endpoint. | `CallbackURL` output | Medium | Inspection | `E004` |
| FR-009 | Return role header on `WhoAmI` response | Invocation of the evidenced `WhoAmI` method with HTTP 200 response path | The system shall define the response header `x-pagopa-pn-cx-role` on the method response for role-header verification. | HTTP response header `x-pagopa-pn-cx-role` available in method response definition | High | Inspection | `E004` |
| FR-010 | Provide private SQS connectivity inside VPC | Deployment of VPC endpoint template with VPC, subnet, and security-group parameters | The system shall create an interface VPC endpoint for Amazon SQS in the specified VPC and subnets. | SQS interface endpoint | High | Inspection | `E003` |

## 5. Non-Functional Requirements

| ID | Requirement | Quality attribute | Priority | Verification | Source evidence | Confidence |
|---|---|---|---|---|---|---|
| NFR-001 | The SQS VPC endpoint shall have `PrivateDnsEnabled` set to `true`. | Compatibility / network integration | High | Inspection | `E003` | Explicit |
| NFR-002 | Access to the interface endpoint shall be restricted by a security group whose ingress source is the configured VPC CIDR. | Security | High | Inspection | `E003` | Explicit |
| NFR-003 | Token validity unit parameters shall be constrained to enumerated values `days`, `hours`, `minutes`, or `seconds` to ensure configuration consistency. | Maintainability / configuration integrity | Medium | Inspection | `E002` | Explicit |
| NFR-004 | Unauthorized access through the identity-pool role shall be limited in scope as described by the template. | Security | Medium | Inspection | `E001` | Inferred |

## 6. Data Requirements

| Area | Requirement | Source evidence |
|---|---|---|
| Configuration parameters | The system uses deployment parameters including `AuthName`, `CognitoUserPoolName`, and token validity unit parameters. | `E002`, `E006` |
| Identity data | The Cognito configuration includes writable attributes `custom:Role` and `email`. | `E001` |
| Identity references | The identity-pool configuration uses `UserPoolId`, `ClientId`, and `ProviderName` references. | `E001` |
| API response data | The API Gateway method response defines header `x-pagopa-pn-cx-role`. | `E004` |
| Deployment outputs | The API deployment publishes `CallbackURL` as an output. | `E004` |
| Network configuration data | The VPC endpoint requires `VpcId`, `Subnets`, `VpcCidr`, and a regional SQS service name. | `E003` |
| Environment-specific inputs | Installation artifacts reference environment/profile values and service-specific keys such as `UserRegistryApiKeyForPF` and DNS/domain inputs. | `E005` |

## 7. Constraints

| ID | Constraint | Source evidence |
|---|---|---|
| C-001 | Infrastructure is defined as AWS CloudFormation templates using template format version `2010-09-09`. | `E002` |
| C-002 | The authentication solution is constrained to AWS Cognito user-pool and identity-pool services. | `E001`, `E002` |
| C-003 | Private SQS connectivity is constrained to AWS VPC interface endpoints and regional AWS service naming. | `E003` |
| C-004 | API deployment is constrained by dependencies on `WhoAmI` and `ECS` method resources before deployment. | `E004` |
| C-005 | Installation requires environment/profile-specific operational inputs and AWS CLI/service setup steps. | `E005` |

## 8. Verification and Acceptance

| Requirement IDs | Verification method | Acceptance basis |
|---|---|---|
| `FR-001`, `FR-003`, `FR-004`, `FR-005`, `FR-006`, `FR-007`, `FR-008`, `FR-010` | Inspection | CloudFormation templates define the required resources, properties, and outputs. |
| `FR-002`, `NFR-003` | Inspection | Parameter definitions restrict token unit values to the evidenced enumeration. |
| `FR-009` | Inspection | API Gateway method response definition includes header `x-pagopa-pn-cx-role`. |
| `NFR-001`, `NFR-002`, `NFR-004` | Inspection | Endpoint and IAM/security-group properties match the evidenced configuration intent. |

## 9. Traceability Matrix

| ID | Requirement | Type | Source | Evidence Type | Verification | Confidence |
|---|---|---|---|---|---|---|
| FR-001 | Provision Cognito authentication resources | Functional | `E002` | Explicit | Inspection | High |
| FR-002 | Support configurable token validity units | Functional | `E002` | Explicit | Inspection | High |
| FR-003 | Bind identity pool to Cognito provider | Functional | `E001` | Explicit | Inspection | High |
| FR-004 | Permit unauthenticated identities | Functional | `E001` | Explicit | Inspection | High |
| FR-005 | Create limited unauthorized-access role | Functional | `E001` | Explicit | Inspection | Medium |
| FR-006 | Expose user attributes for writes | Functional | `E001` | Explicit | Inspection | High |
| FR-007 | Deploy API Gateway stage | Functional | `E004` | Explicit | Inspection | High |
| FR-008 | Publish API callback endpoint | Functional | `E004` | Explicit | Inspection | High |
| FR-009 | Return role header on `WhoAmI` response | Functional | `E004` | Explicit | Inspection | Medium |
| FR-010 | Provide private SQS connectivity inside VPC | Functional | `E003` | Explicit | Inspection | High |
| NFR-001 | Enable private DNS on SQS VPC endpoint | Non-functional | `E003` | Explicit | Inspection | High |
| NFR-002 | Restrict endpoint ingress to VPC CIDR | Non-functional | `E003` | Explicit | Inspection | High |
| NFR-003 | Constrain token validity units to enumerated values | Non-functional | `E002` | Explicit | Inspection | High |
| NFR-004 | Limit unauthorized-access role scope | Non-functional | `E001` | Inferred | Inspection | Medium |
