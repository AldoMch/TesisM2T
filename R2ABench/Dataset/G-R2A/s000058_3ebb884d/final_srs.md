# Software Requirements Specification

## 1. Introduction

### Purpose
This SRS defines evidence-backed requirements for the `macpro-appian-connector` repository at commit `6f5047f26d6ee51450baa17a614ac671cb3a7224`. It covers the repository behaviors directly supported by the evidence pack: connector configuration, AWS stage listing, alert routing, and deployment metrics collection.

### Product scope
The repository provides AWS-based operational capabilities for:
- listing currently running stages in the current AWS account,
- configuring and restarting connector definitions for a target service,
- routing matching service events through EventBridge to SNS,
- collecting deployment and pull request metrics from GitHub.

### Intended audience
This document is intended for:
- developers onboarding to or extending the repository,
- operators running repository workflows in AWS,
- reviewers validating behavior against repository evidence.

### References
- Repository: `Enterprise-CMCS/macpro-appian-connector`
- Repository URL: https://github.com/Enterprise-CMCS/macpro-appian-connector
- Snapshot URL: https://github.com/Enterprise-CMCS/macpro-appian-connector/tree/6f5047f26d6ee51450baa17a614ac671cb3a7224
- Evidence sources: `E001`-`E006`

## 2. Overall Description

### Product perspective
The product is an AWS-integrated service and operations repository. Evidence shows integration with AWS ECS-related connector operations, EventBridge, SNS, AWS CLI-based stage operations, and GitHub Actions and GitHub API-based reporting.

### Product functions summary
The repository supports these functions:
- list currently running stages for the project in the current AWS account,
- apply connector configuration changes to a target cluster and service and restart affected connectors,
- route matching events from EventBridge rules to an SNS topic,
- keep SNS subscription management outside deployment automation,
- calculate deployment success/failure counts for a branch from GitHub Actions workflow runs,
- calculate average pull request merge time to a branch.

### User classes
- Developers: perform onboarding, run stage-listing scripts, and use repository workflows.
- Operators/DevOps users: provide AWS credentials, run AWS-account-scoped operations, and observe alerts.
- Repository maintainers: manage connector definitions and deployment metrics.
- Notification administrators: add or remove SNS subscriptions manually.

### Operating environment
Supported environment evidence includes:
- an AWS account with AWS CLI credentials available (`E001`),
- terminal-based local execution during onboarding and script use (`E002`, `E001`),
- GitHub Actions as the CI/CD tool (`E001`),
- AWS EventBridge and SNS for alert routing (`E003`),
- GitHub API access for workflow and pull request metrics (`E005`, `E006`).

### Assumptions and dependencies
- Users have completed onboarding before running stage-listing procedures (`E001`).
- AWS CLI credentials must be obtained and set before AWS stage-listing operations (`E001`).
- Connector operations depend on configured `cluster` and `service` environment values and a defined connector set (`E004`).
- Deployment metrics depend on GitHub workflow run and pull request data being available through GitHub API pagination (`E005`, `E006`).

## 3. External Interface Requirements

### User interfaces
| Interface | Requirement |
|---|---|
| Terminal/script interface | The system shall support a run-script-based procedure for listing currently running stages after onboarding and AWS credential setup. Source: `E001` |
| Manual subscription administration | SNS subscription membership shall be managed manually rather than through deployment. Source: `E003` |

### Software/API interfaces
| Interface | Requirement |
|---|---|
| AWS CLI | Stage-listing operations shall rely on AWS CLI credentials being set in the current environment. Source: `E001` |
| AWS EventBridge | The system shall receive matching events through EventBridge rules defined with event filtering criteria. Source: `E003` |
| AWS SNS | The system shall publish matching EventBridge-triggered events to an SNS topic authorized for EventBridge invocation. Source: `E003` |
| Connector management library | Connector configuration shall invoke connector put, delete, and restart operations for a target cluster and service. Source: `E004` |
| GitHub Actions API | Deployment metrics shall query workflow runs for `deploy.yml`. Source: `E005` |
| GitHub Pull Requests API | Pull request metrics shall query closed pull requests for a specified base branch. Source: `E006` |

### Communication interfaces
| Interface | Requirement |
|---|---|
| Event delivery | Matching events shall flow from EventBridge to SNS when the rule pattern matches. Source: `E003` |
| GitHub API pagination | Metrics collection shall aggregate paginated GitHub API responses. Source: `E005`, `E006` |

### Data exchange formats
| Format | Requirement |
|---|---|
| Workflow run records | Deployment metrics shall consume workflow run records that include a `conclusion` field. Source: `E005` |
| Pull request records | PR metrics shall consume pull request records including `created_at`, `merged_at`, and `base` branch filtering inputs. Source: `E006` |
| Metrics outputs | Deployment metrics shall output `failedRuns` and `passedRuns`; PR metrics shall output `averageTimeToMerge`. Source: `E005`, `E006` |
| Connector configuration data | Connector operations shall consume a connector collection together with `cluster` and `service` values. Source: `E004` |

## 4. Functional Requirements

| ID | Description | Trigger / Input | System behavior | Output | Priority | Verification | Source evidence |
|---|---|---|---|---|---|---|---|
| FR-001 | List running stages | A user who has completed onboarding sets AWS CLI credentials and runs the stage-listing script. | The system shall return a list of currently running stages for the project in the current AWS account. | List of currently running stages. | High | Demonstration | `E001` |
| FR-002 | Configure connectors for a target service | Invocation of the connector configuration handler with `cluster`, `service`, and defined connectors available. | The system shall apply connector definitions to the target cluster and service, issue connector deletion for the provided deletion set, and restart the configured connectors. | Updated connector state for the target cluster/service. | High | Test | `E004` |
| FR-003 | Route matching events to SNS | An event matches an EventBridge rule pattern associated with project services. | The system shall deliver the matching event from EventBridge to the SNS topic and authorize EventBridge to invoke that topic. | SNS delivery of matching events. | High | Test | `E003` |
| FR-004 | Support manual SNS subscription management | A notification administrator adds or removes subscribers. | The system shall allow SNS subscription services associated with the topic to be managed manually without requiring deployment. | Subscription changes applied independently of deployment. | Medium | Inspection | `E003` |
| FR-005 | Report successful and failed deploy counts | A branch name is provided for deployment metrics collection. | The system shall query GitHub Actions workflow runs for `deploy.yml`, count runs with `conclusion != success` as failed, and compute passed runs as total minus failed. | `failedRuns` and `passedRuns` values for the branch. | Medium | Test | `E005` |
| FR-006 | Report average PR merge time to a branch | A branch name is provided for PR metrics collection. | The system shall query closed pull requests for the branch, keep items with both `created_at` and `merged_at`, compute hour differences, and calculate the average merge time, defaulting to `0` when no qualifying PRs exist. | `averageTimeToMerge` value for the branch. | Medium | Test | `E006` |

## 5. Non-Functional Requirements

| ID | Quality attribute | Requirement | Priority | Verification | Evidence | Evidence type |
|---|---|---|---|---|---|---|
| NFR-001 | Operability | AWS-account stage listing shall operate only after onboarding completion and AWS CLI credential setup. | High | Inspection | `E001` | explicit |
| NFR-002 | Deployability / maintainability | SNS subscription membership management shall remain decoupled from deployment so users can be added or removed without redeployment. | Medium | Inspection | `E003` | explicit |
| NFR-003 | Compatibility | CI/CD-related repository workflows shall use GitHub Actions. | Medium | Inspection | `E001` | explicit |
| NFR-004 | Scalability | GitHub metrics collection shall support paginated retrieval with `per_page: 100` and aggregate all returned pages before computing metrics. | Medium | Test | `E005`, `E006` | explicit |

## 6. Data Requirements

| ID | Data entity / object | Requirement | Source evidence |
|---|---|---|---|
| DR-001 | Running stage list | The system shall produce a list representing currently running stages for the project in the current AWS account. | `E001` |
| DR-002 | Connector configuration set | The system shall consume connector definitions together with `cluster` and `service` environment values when configuring connectors. | `E004` |
| DR-003 | Event pattern and SNS topic | The alert flow shall use EventBridge rule filtering criteria (`EventPattern`) and an SNS topic target with permission for EventBridge invocation. | `E003` |
| DR-004 | Workflow run data | Deployment metrics shall consume workflow run records and use the `conclusion` field to classify runs as passed or failed. | `E005` |
| DR-005 | Pull request timing data | PR metrics shall consume `created_at` and `merged_at` timestamps from closed pull requests and calculate hour-based merge durations. | `E006` |
| DR-006 | Metrics results | The system shall output deployment metrics as `failedRuns` and `passedRuns`, and PR metrics as `averageTimeToMerge`. | `E005`, `E006` |

## 7. Constraints

| ID | Constraint | Source evidence |
|---|---|---|
| C-001 | Stage-listing execution is constrained to the current AWS account. | `E001` |
| C-002 | Stage-listing requires prior onboarding completion. | `E001` |
| C-003 | Stage-listing requires AWS CLI credentials to be obtained and set. | `E001` |
| C-004 | The repository uses GitHub Actions as its CI/CD tool. | `E001` |
| C-005 | SNS subscription services are managed manually rather than by deployment automation. | `E003` |
| C-006 | Deployment metrics are constrained to GitHub workflow runs for `deploy.yml`. | `E005` |
| C-007 | PR metrics are constrained to closed pull requests for a specified base branch. | `E006` |

## 8. Verification and Acceptance

| Requirement ID | Verification method | Acceptance basis |
|---|---|---|
| FR-001 | Demonstration | Running the documented procedure after onboarding and AWS credential setup returns the current AWS-account stage list. |
| FR-002 | Test | A handler invocation issues connector put, delete, and restart operations for the target cluster/service. |
| FR-003 | Test | A matching event triggers EventBridge delivery to the SNS topic. |
| FR-004 | Inspection | Subscription management can be performed manually without deployment changes. |
| FR-005 | Test | For a supplied branch, workflow run data yields `failedRuns` and `passedRuns` consistent with run conclusions. |
| FR-006 | Test | For a supplied branch, merged PR timing data yields the expected `averageTimeToMerge`, or `0` when none qualify. |
| NFR-001 | Inspection | Documentation and procedure require onboarding completion and AWS CLI credentials before stage listing. |
| NFR-002 | Inspection | Alert subscription management remains external to deployment. |
| NFR-003 | Inspection | Repository CI/CD references GitHub Actions. |
| NFR-004 | Test | Metrics retrieval aggregates paginated GitHub API results using page size 100. |

## 9. Traceability Matrix

| ID | Requirement | Type | Source | Evidence Type | Verification | Confidence |
|---|---|---|---|---|---|---|
| FR-001 | List running stages in current AWS account | Functional | `E001` | explicit | Demonstration | High |
| FR-002 | Configure and restart connectors for target cluster/service | Functional | `E004` | explicit | Test | Medium |
| FR-003 | Deliver matching EventBridge events to SNS | Functional | `E003` | explicit | Test | High |
| FR-004 | Support manual SNS subscription management | Functional | `E003` | explicit | Inspection | High |
| FR-005 | Compute passed and failed deploy counts by branch | Functional | `E005` | explicit | Test | High |
| FR-006 | Compute average PR merge time by branch | Functional | `E006` | explicit | Test | High |
| NFR-001 | Require onboarding and AWS credentials for AWS stage listing | Non-functional | `E001` | explicit | Inspection | High |
| NFR-002 | Decouple SNS subscription management from deployment | Non-functional | `E003` | explicit | Inspection | High |
| NFR-003 | Use GitHub Actions for CI/CD compatibility | Non-functional | `E001` | explicit | Inspection | Medium |
| NFR-004 | Aggregate paginated GitHub API results at page size 100 | Non-functional | `E005`, `E006` | explicit | Test | High |
| DR-001 | Running stage list data object | Data | `E001` | explicit | Inspection | High |
| DR-002 | Connector configuration data | Data | `E004` | explicit | Inspection | Medium |
| DR-003 | Event pattern and SNS topic data | Data | `E003` | explicit | Inspection | High |
| DR-004 | Workflow run classification data | Data | `E005` | explicit | Inspection | High |
| DR-005 | Pull request timing data | Data | `E006` | explicit | Inspection | High |
| DR-006 | Metrics output values | Data | `E005`, `E006` | explicit | Inspection | High |
