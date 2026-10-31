# Checked Software Requirements Specification: PN Infra Cognito, API Gateway, and VPC Endpoint Infrastructure

## 1. Introduction

### 1.1 Purpose

This Software Requirements Specification defines the checked requirements for AWS infrastructure templates and installation support that create Cognito authentication objects, expose API Gateway endpoints, configure private SQS connectivity through a VPC endpoint, and accept environment-specific installation inputs.

The document is prepared for architecture view generation and omits review notes, provenance fields, and supporting-material identifiers.

### 1.2 Product Scope

The checked scope includes:

- AWS CloudFormation stacks for Cognito user-pool and identity-pool setup.
- Cross-account authentication structure where Cognito is provisioned in a Cognito account and API Gateway is provisioned in an API Gateway account.
- API Gateway deployment with Cognito user-pool authorization and role-header handling.
- VPC interface endpoint configuration for Amazon SQS.
- Installation-time operational inputs such as AWS profiles, DNS/domain values, API keys, and environment names.

The installation guide also mentions broader orchestration such as DNS delegation, certificate setup, service-linked role creation, SPID hub installation, and data-vault stacks. Those broader installation steps are acknowledged as surrounding setup, but this checked SRS specifies only the Cognito, API Gateway, SQS VPC endpoint, and directly related installation-input requirements.

### 1.3 Intended Audience

The intended audience includes infrastructure engineers, AWS operators, API integrators, security reviewers, operations reviewers, and architecture evaluators.

### 1.4 Definitions and Abbreviations

- API: Application Programming Interface.
- ARN: AWS ARN identifier.
- CIDR: Classless Inter-Domain Routing.
- IAM: Identity and Access Management.
- SQS: Amazon Simple Queue Service.
- VPC: Virtual Private Cloud.

## 2. Overall Description

### 2.1 Product Perspective

The product is an AWS infrastructure layer defined through CloudFormation templates and installation scripts. It provisions Cognito authentication objects, IAM roles, API Gateway methods and deployment outputs, and a VPC interface endpoint for private SQS access.

The authentication flow spans two AWS accounts:

- The Cognito account hosts the Cognito user pool, user-pool client, identity pool, and identity-pool role mapping.
- The API Gateway account hosts the API Gateway, Cognito authorizer, `WhoAmI` method, ECS proxy method, VPC link, and callback endpoint output.

The API Gateway account receives the Cognito user-pool ARN as an input and uses it to configure the Cognito user-pool authorizer.

### 2.2 Product Functions

The product shall provide the following high-level functions:

- Create Cognito user-pool and identity-pool objects.
- Configure token validity unit parameters.
- Bind an identity pool to a Cognito user-pool client and provider.
- Permit unauthenticated identities where configured.
- Create IAM roles for identity-pool access paths.
- Configure writable Cognito user attributes.
- Deploy an API Gateway stage.
- Configure Cognito authorization for API Gateway methods.
- Declare and map a role-related API response header.
- Publish an API Gateway callback endpoint output.
- Create a private SQS VPC interface endpoint.
- Restrict VPC endpoint ingress by VPC CIDR.

### 2.3 User Classes

- Infrastructure operators run installation commands and deploy CloudFormation stacks.
- API clients call the API Gateway endpoint and consume response metadata.
- Security reviewers inspect Cognito, IAM, API Gateway, and VPC endpoint configuration.
- Operations reviewers validate environment profiles, DNS/domain setup, and network parameters.
- Cognito-backed identities access downstream AWS paths through identity-pool role mapping.

### 2.4 Operating Environment

The product shall operate in AWS accounts with CloudFormation, Cognito, IAM, API Gateway, VPC networking, security groups, subnets, and Amazon SQS available. Installation procedures require AWS CLI profile configuration and environment-specific operational inputs.

### 2.5 Assumptions and Dependencies

- The deployment has valid AWS account and region context.
- The Cognito stack and API Gateway stack may be deployed in separate AWS accounts.
- The API Gateway account can receive the Cognito user-pool ARN.
- The API Gateway deployment depends on the `WhoAmI` and `ECS` methods being defined before deployment.
- The VPC endpoint configuration depends on an existing VPC, VPC CIDR, target subnets, and security group setup.

## 3. External Interface Requirements

### 3.1 Operational Interface Requirements

#### OI-001 CloudFormation Template Interface

The product shall expose deployment behavior through CloudFormation YAML templates.

#### OI-002 Installation Command Interface

The product shall accept installation-time inputs through scripts, AWS CLI profiles, DNS/domain values, service API keys, and environment names.

### 3.2 Software Interface Requirements

#### SI-001 Cognito Interface

The product shall use AWS Cognito user-pool and identity-pool services for authentication and identity federation.

#### SI-002 IAM Interface

The product shall create IAM roles for identity-pool access paths and attach those roles to the identity pool.

#### SI-003 API Gateway Interface

The product shall expose API Gateway methods protected by a Cognito user-pool authorizer.

#### SI-004 API Gateway VPC Link Interface

The ECS proxy method shall support integration through an API Gateway VPC link to a network load balancer ARN provided as input.

#### SI-005 SQS VPC Endpoint Interface

The product shall integrate privately with Amazon SQS through an AWS VPC interface endpoint using regional SQS service naming.

### 3.3 Communication Interface Requirements

#### CI-001 API Role Header Communication

The `WhoAmI` API method shall define role-header handling for `x-pagopa-pn-cx-role`. The method response declaration shall treat the header as optional, and the integration response shall map the header value from the Cognito authorizer role claim.

#### CI-002 ECS Proxy Header Forwarding

The ECS proxy method shall forward the Cognito authorizer role claim to the integration request header `x-pagopa-pn-cx-role`.

#### CI-003 Private SQS Communication

Private AWS network communication to SQS shall occur through an interface VPC endpoint with private DNS enabled.

### 3.4 Data Exchange Requirements

#### DI-001 CloudFormation Template Format

The infrastructure shall be declared in CloudFormation YAML format.

#### DI-002 API Role Header

API Gateway method and integration configuration shall use the HTTP header `x-pagopa-pn-cx-role` for role-related metadata.

#### DI-003 Callback Endpoint Output

The API Gateway deployment shall publish a `CallbackURL` output identified as the API Gateway endpoint.

## 4. Functional Requirements

### FR-001 Provision Cognito Authentication Objects

The Cognito stack shall create a Cognito user pool and Cognito identity pool.

**Priority:** High

**Verification:** Inspection.

**Acceptance Criteria:**

- The CloudFormation stack defines a Cognito user pool.
- The CloudFormation stack defines a Cognito identity pool.
- The created identity pool is named from the authentication name parameter.

### FR-002 Configure Token Validity Units

The Cognito stack shall accept token validity unit parameters for access tokens, ID tokens, and refresh tokens. Each parameter shall be limited to `days`, `hours`, `minutes`, or `seconds`.

**Priority:** Medium

**Verification:** Inspection.

**Acceptance Criteria:**

- `AccessTokenValidityUnits` allows only the enumerated unit values.
- `IdTokenValidityUnits` allows only the enumerated unit values.
- `RefreshTokenValidityUnits` allows only the enumerated unit values.

### FR-003 Configure User-Pool Client Attributes

The Cognito user-pool client shall support readable and writable user attributes including `custom:Role` and `email`.

**Priority:** Medium

**Verification:** Inspection.

**Acceptance Criteria:**

- The user-pool client includes `custom:Role` in readable and writable attributes.
- The user-pool client includes `email` in readable and writable attributes.

### FR-004 Bind Identity Pool to Cognito Provider

The identity pool shall be configured with a Cognito identity provider using a user-pool client identifier and provider name.

**Priority:** High

**Verification:** Inspection.

**Acceptance Criteria:**

- The identity-pool configuration includes `ClientId`.
- The identity-pool configuration includes `ProviderName`.
- The provider values are derived from the Cognito user-pool client and user pool.

### FR-005 Permit Unauthenticated Identities

The identity pool shall permit unauthenticated identities.

**Priority:** High

**Verification:** Inspection.

**Acceptance Criteria:**

- The identity-pool configuration enables unauthenticated identities.
- The unauthenticated access path has a mapped IAM role.

### FR-006 Create Unauthenticated IAM Role

The Cognito stack shall create an unauthenticated IAM role assumable only by web-identity federated identities from the created identity pool with unauthenticated authentication-method context.

**Priority:** High

**Verification:** Inspection.

**Acceptance Criteria:**

- The role trust policy uses `sts:AssumeRoleWithWebIdentity`.
- The role trust policy uses `cognito-identity.amazonaws.com` as the federated principal.
- The role trust policy restricts the audience to the created identity pool.
- The role trust policy restricts the authentication method to unauthenticated identities.
- The attached policy permits only the unauthenticated-access actions listed in the template.

### FR-007 Attach Identity-Pool Roles

The Cognito stack shall attach authenticated and unauthenticated IAM roles to the identity pool.

**Priority:** High

**Verification:** Inspection.

**Acceptance Criteria:**

- The identity-pool role attachment maps an authenticated role.
- The identity-pool role attachment maps an unauthenticated role.

### FR-008 Deploy API Gateway Stage

The API Gateway stack shall create an API Gateway deployment using the provided stage name.

**Priority:** High

**Verification:** Inspection.

**Acceptance Criteria:**

- The API Gateway deployment uses the configured stage name.
- The deployment depends on the required API methods being defined.

### FR-009 Configure Cognito Authorizer

The API Gateway stack shall configure a Cognito user-pool authorizer using the Cognito user-pool ARN provided from the Cognito account.

**Priority:** High

**Verification:** Inspection.

**Acceptance Criteria:**

- The authorizer type is Cognito user pools.
- The authorizer uses the provided Cognito user-pool ARN.
- API methods requiring authentication are configured to use the authorizer.

### FR-010 Configure Role Header Handling for WhoAmI

The `WhoAmI` method shall declare the `x-pagopa-pn-cx-role` response header as optional and shall map the response header value from the Cognito authorizer `custom:Role` claim through the integration response.

**Priority:** High

**Verification:** Inspection.

**Acceptance Criteria:**

- The method response declares `x-pagopa-pn-cx-role`.
- The method response marks the header as optional.
- The integration response maps `x-pagopa-pn-cx-role` from the Cognito authorizer role claim.
- The method response path is defined for HTTP status `200`.

### FR-011 Forward Role Header to ECS Integration

The ECS proxy method shall forward the Cognito authorizer role claim to the integration request header `x-pagopa-pn-cx-role`.

**Priority:** Medium

**Verification:** Inspection.

**Acceptance Criteria:**

- The ECS method uses Cognito user-pool authorization.
- The ECS integration request maps the role claim into `x-pagopa-pn-cx-role`.
- The ECS integration uses the configured API integration URI and VPC link settings.

### FR-012 Publish API Callback Endpoint

The API Gateway deployment shall publish a `CallbackURL` output identified as the API Gateway endpoint.

**Priority:** Medium

**Verification:** Inspection.

**Acceptance Criteria:**

- The stack output includes `CallbackURL`.
- The output is described as the API Gateway endpoint.
- The output is built from the API Gateway identifier, AWS region, and configured stage name.

### FR-013 Create Private SQS VPC Endpoint

The VPC endpoint template shall create an interface VPC endpoint for Amazon SQS in the specified VPC and subnets.

**Priority:** High

**Verification:** Inspection.

**Acceptance Criteria:**

- The endpoint type is interface.
- The endpoint uses the configured VPC identifier.
- The endpoint uses the configured subnet list.
- The endpoint uses the regional Amazon SQS service name.

### FR-014 Configure VPC Endpoint Security Group

The VPC endpoint template shall create a security group for the SQS interface endpoint and restrict inbound TCP access to the configured VPC CIDR.

**Priority:** High

**Verification:** Inspection.

**Acceptance Criteria:**

- The endpoint security group is associated with the configured VPC.
- The ingress rule uses TCP.
- The ingress rule covers ports `0` through `65535`.
- The allowed CIDR is the configured VPC CIDR.

## 5. Non-Functional Requirements

### NFR-001 Private DNS for SQS

The SQS VPC endpoint shall have private DNS enabled.

**Metric:** The endpoint configuration sets private DNS to true.

### NFR-002 VPC-Bounded Endpoint Access

Access to the SQS interface endpoint shall be restricted to the configured VPC CIDR through the endpoint security group.

**Metric:** The endpoint security group allows inbound TCP only from the configured VPC CIDR.

### NFR-003 Token Unit Configuration Integrity

Token validity unit parameters shall be constrained to the enumerated values `days`, `hours`, `minutes`, and `seconds`.

**Metric:** Each token unit parameter uses the same allowed-value set.

### NFR-004 Unauthenticated Role Security Boundary

The unauthenticated IAM role shall be assumable only by unauthenticated web-identity federated identities from the created identity pool and shall allow only the unauthenticated-access actions listed in the template.

**Metric:** The trust policy audience and authentication-method conditions match the created identity pool and unauthenticated identity path; the attached policy action list is limited to the template-defined unauthenticated actions.

## 6. Data Requirements

### DR-001 Cognito Configuration Parameters

The Cognito stack shall accept configuration parameters including `AuthName`, `CognitoUserPoolName`, `AccessTokenValidityUnits`, `IdTokenValidityUnits`, and `RefreshTokenValidityUnits`.

### DR-002 Cognito Identity Link Data

The Cognito identity-pool configuration shall use `UserPoolId`, `ClientId`, and `ProviderName` values to establish the Cognito provider link.

### DR-003 User Attribute Data

The Cognito configuration shall include user attributes `custom:Role` and `email`.

### DR-004 Role Header Data

The API Gateway method and integration configuration shall use `x-pagopa-pn-cx-role` for role-related HTTP metadata.

### DR-005 API Deployment Output Data

The API Gateway deployment shall provide a `CallbackURL` output.

### DR-006 Network Configuration Data

The VPC endpoint configuration shall use `VpcId`, `Subnets`, `VpcCidr`, and a regional SQS service name.

### DR-007 Installation Input Data

Installation procedures may require environment names, AWS profile names, DNS/domain values, API keys, account identifiers, certificate identifiers, and environment-specific configuration values.

## 7. System Constraints

### CON-001 CloudFormation Template Constraint

The infrastructure shall be defined through AWS CloudFormation templates using template format version `2010-09-09`.

### CON-002 Cognito Service Constraint

The authentication setup shall use AWS Cognito user-pool and identity-pool services.

### CON-003 Cross-Account Authentication Constraint

The Cognito account shall provide the user-pool ARN needed by the API Gateway account for Cognito user-pool authorizer configuration.

### CON-004 API Gateway Dependency Constraint

API Gateway deployment shall depend on the `WhoAmI` and `ECS` methods being defined before deployment.

### CON-005 Private SQS Connectivity Constraint

Private SQS connectivity shall use an AWS VPC interface endpoint and regional AWS SQS service naming.

### CON-006 Installation Scope Constraint

Installation orchestration mentions additional environment setup such as DNS delegation, certificates, service-linked roles, SPID hub installation, and data-vault stacks. Those items are surrounding installation activities unless explicitly represented by the requirements in this SRS.

## 8. Verification and Acceptance Criteria

| Requirement | Verification Method | Expected Result |
| --- | --- | --- |
| FR-001 | Inspection | Cognito user pool and identity pool are defined |
| FR-002 | Inspection | Access, ID, and refresh token unit parameters use the allowed unit set |
| FR-003 | Inspection | `custom:Role` and `email` are readable and writable user-pool client attributes |
| FR-004 | Inspection | Identity pool is linked to the Cognito provider through client and provider identifiers |
| FR-005 | Inspection | Identity pool allows unauthenticated identities and maps an unauthenticated role |
| FR-006 | Inspection | Unauthenticated IAM role trust and policy match identity-pool and unauthenticated access restrictions |
| FR-007 | Inspection | Identity-pool role attachment maps authenticated and unauthenticated roles |
| FR-008 | Inspection | API Gateway deployment uses the configured stage and depends on required methods |
| FR-009 | Inspection | API Gateway authorizer uses the supplied Cognito user-pool ARN |
| FR-010 | Inspection | `WhoAmI` declares optional role header and maps it from the authorizer role claim |
| FR-011 | Inspection | ECS integration forwards the authorizer role claim through the request header |
| FR-012 | Inspection | `CallbackURL` output is present and identifies the API Gateway endpoint |
| FR-013 | Inspection | SQS interface endpoint is defined for configured VPC and subnets |
| FR-014 | Inspection | Endpoint security group restricts TCP ingress to configured VPC CIDR |
| NFR-001 | Inspection | Private DNS is enabled on the SQS VPC endpoint |
| NFR-002 | Inspection | Endpoint ingress is bounded by configured VPC CIDR |
| NFR-003 | Inspection | Token unit values are constrained consistently |
| NFR-004 | Inspection | Unauthenticated role trust and action scope are concretely checkable |
