# Software Requirements Specification

## 1. Introduction

### Purpose
This SRS defines software requirements for the `macpro-appian-connector` repository. It covers the repository behaviors supported by the reviewed project materials, including Appian-to-BigMAC data transfer support, connector configuration and runtime maintenance, AWS stage listing, service event alerting, and deployment metrics collection.

### Product scope
This repository supports transfer of Appian data changes to CMS BigMAC and related operations management. The system shall support:
- listing currently running stages in the current AWS account and region,
- configuring and restarting connector definitions for a target service,
- managing data-transfer-related topic and connector operations,
- routing matching service events through AWS event routing to an SNS notification topic,
- supporting manually maintained SNS subscription targets,
- collecting deployment metrics from GitHub Actions workflow runs, and
- collecting pull request merge-time metrics for a branch.

### Intended audience
This document is intended for:
- developers onboarding to or extending the repository,
- operators running repository workflows in AWS,
- maintainers managing connector definitions and operational metrics,
- testers validating documented repository behaviors.

## 2. Overall Description

### Product perspective
The product is an AWS-integrated service and operations repository supporting transfer of Appian-side data changes to CMS BigMAC. It includes AWS-related capabilities for connector configuration, topic management, service event alerting, runtime status observation, and GitHub-based operational reporting. The repository documentation includes an architecture diagram that may be used as a reference for later architecture modeling; this SRS records requirement-level responsibilities and external-system interactions rather than prescribing deployment topology.

### Product functions summary
The repository supports these functions:
- list currently running stages for the project in the current AWS account and region,
- apply connector configuration changes to a target cluster and service and restart affected connectors,
- route matching service events to an SNS topic,
- keep SNS subscription management outside deployment automation,
- calculate deployment success and failure counts for a branch from GitHub Actions workflow runs, and
- calculate average pull request merge time to a branch.

### User classes
- Developers: perform onboarding, run stage-listing procedures, and use repository workflows.
- Operators/DevOps users: provide AWS credentials, run AWS-account-scoped operations, observe alerts, and manually manage SNS topic subscriptions when they have subscription management access.
- Repository maintainers: manage connector definitions and deployment metrics.

### Operating environment
The system operates in:
- an AWS account with AWS CLI credentials available,
- a terminal-based local environment for onboarding and script execution,
- GitHub Actions as the CI/CD tool,
- AWS services including EventBridge and SNS for alert routing, and
- GitHub API access for workflow-run and pull-request metrics.

### Assumptions and dependencies
- Users complete onboarding before running stage-listing procedures.
- AWS CLI credentials must be obtained and set before AWS stage-listing operations.
- Connector operations depend on configured `cluster` and `service` environment values and a defined connector set.
- Deployment metrics depend on GitHub workflow-run and pull-request data being available through paginated GitHub API access.

## 3. External Interface Requirements

### User interfaces
| Interface | Requirement |
|---|---|
| Terminal/script interface | The system shall support a documented terminal procedure for listing currently running stages after onboarding and AWS credential setup. |
| Manual subscription administration | SNS subscription membership shall be managed manually rather than through deployment automation. |

### Software/API interfaces
| Interface | Requirement |
|---|---|
| AWS CLI | Stage-listing operations shall rely on AWS CLI credentials being set in the current environment. |
| AWS event routing | The system shall receive matching service events through AWS event-routing rules defined with event filtering criteria. |
| AWS SNS | The system shall publish matching routed events to an SNS topic authorized for event-routing invocation. |
| Connector management library | Connector configuration shall invoke connector put, delete, and restart operations for a target cluster and service. |
| GitHub Actions API | Deployment metrics shall query workflow runs for `deploy.yml`. |
| GitHub Pull Requests API | Pull request metrics shall query closed pull requests for a specified base branch. |

### Communication interfaces
| Interface | Requirement |
|---|---|
| Event delivery | Matching events shall flow from AWS event routing to SNS when the configured rule pattern matches. |
| GitHub API pagination | Metrics collection shall aggregate paginated GitHub API responses. |

### Data exchange formats
| Format | Requirement |
|---|---|
| Workflow run records | Deployment metrics shall consume workflow run records that include a `conclusion` field. |
| Pull request records | PR metrics shall consume pull request records including `created_at`, `merged_at`, and base-branch filtering inputs. |
| Metrics outputs | Deployment metrics shall output `failedRuns` and `passedRuns`; PR metrics shall output `averageTimeToMerge`. |
| Connector configuration data | Connector operations shall consume a connector collection together with `cluster` and `service` values. |
| Stage-listing output | Running-stage queries shall output `runningStages=<comma-separated stages>`. |

## 4. Functional Requirements

| ID | Description | Trigger / Input | System behavior | Output | Priority | Verification |
|---|---|---|---|---|---|---|
| FR-001 | List running stages | A user who has completed onboarding sets AWS CLI credentials, runs `nvm use`, and runs `run listRunningStages`. | The system shall query running stages in the current AWS account and region and output the result as `runningStages=<comma-separated stages>`. | List of currently running stages. | High | Demonstration |
| FR-002 | Configure connectors for a target service | Invocation of the connector configuration handler with `cluster`, `service`, and defined connectors available. | The system shall apply connector definitions to the target cluster and service, call connector deletion with an empty deletion set so that no connectors are deleted in the current configuration flow, and then restart the configured connectors. | Updated connector state for the target cluster and service. | High | Test |
| FR-003 | Route matching service events to SNS | A project service produces a runtime event matching alerting rules. | The system shall use AWS event routing capability to send the matching event to a notification topic and support distribution from that notification topic to manually maintained subscription targets. | SNS delivery of matching events to subscribed targets. | High | Test |
| FR-004 | Support manual SNS subscription management | A user or operator with SNS subscription management access adds or removes subscribers. | The system shall allow SNS subscription services associated with the topic to be managed manually without requiring deployment. | Subscription changes applied independently of deployment. | Medium | Inspection |
| FR-005 | Report successful and failed deploy counts | A branch name is provided for deployment metrics collection. | The system shall query GitHub Actions workflow runs for `deploy.yml`, count runs with `conclusion != success` as failed, and compute passed runs as total minus failed. | `failedRuns` and `passedRuns` values for the branch. | Medium | Test |
| FR-006 | Report average PR merge time to a branch | A branch name is provided for PR metrics collection. | The system shall query closed pull requests for the branch, keep items with both `created_at` and `merged_at`, compute merge durations as whole-hour differences, and calculate the average merge time, defaulting to `0` when no qualifying PRs exist. | `averageTimeToMerge` value for the branch. | Medium | Test |

## 5. Non-Functional Requirements

| ID | Quality attribute | Requirement | Priority | Verification |
|---|---|---|---|---|
| NFR-001 | Operability | AWS-account stage listing shall operate only after onboarding completion and AWS CLI credential setup. | High | Inspection |
| NFR-002 | Deployability / maintainability | SNS subscription membership management shall remain decoupled from deployment so users can be added or removed without redeployment. | Medium | Inspection |
| NFR-003 | Compatibility | CI/CD-related repository workflows shall use GitHub Actions. | Medium | Inspection |
| NFR-004 | Scalability | GitHub metrics collection shall support paginated retrieval with `per_page: 100` and aggregate all returned pages before computing metrics. | Medium | Test |

## 6. Data Requirements

| ID | Data entity / object | Requirement |
|---|---|---|
| DR-001 | Running stage list | The system shall produce running-stage results in the form `runningStages=<comma-separated stages>` for the current AWS account and region. |
| DR-002 | Connector configuration set | The system shall consume connector definitions together with `cluster` and `service` environment values, and the current configuration flow shall call connector deletion with an empty deletion set. |
| DR-003 | Event pattern and SNS topic | The alert flow shall use event-filtering criteria and an SNS topic target with permission for event-routing invocation. |
| DR-004 | Workflow run data | Deployment metrics shall consume workflow run records and use the `conclusion` field to classify runs as passed or failed. |
| DR-005 | Pull request timing data | PR metrics shall consume `created_at` and `merged_at` timestamps from closed pull requests and calculate merge durations as whole-hour differences. |
| DR-006 | Metrics results | The system shall output deployment metrics as `failedRuns` and `passedRuns`, and PR metrics as `averageTimeToMerge`. |

## 7. System Constraints

| ID | Constraint |
|---|---|
| C-001 | Stage-listing execution is constrained to the current AWS account and region. |
| C-002 | Stage-listing requires prior onboarding completion. |
| C-003 | Stage-listing requires AWS CLI credentials to be obtained and set. |
| C-004 | The repository uses GitHub Actions as its CI/CD tool. |
| C-005 | SNS subscription services are managed manually rather than by deployment automation. |
| C-006 | Deployment metrics are constrained to GitHub workflow runs for `deploy.yml`. |
| C-007 | PR metrics are constrained to closed pull requests for a specified base branch. |

## 8. Verification and Acceptance Criteria

| Requirement ID | Verification method | Acceptance criterion |
|---|---|---|
| FR-001 | Demonstration | After onboarding and AWS credential setup, running `nvm use` and `run listRunningStages` returns running-stage output formatted as `runningStages=<comma-separated stages>`. |
| FR-002 | Test | A handler invocation issues connector put operations for the target cluster and service, calls connector deletion with an empty deletion set, deletes no connectors in that step, and restarts the configured connectors. |
| FR-003 | Test | A matching runtime event is routed to the SNS topic and becomes available to manually maintained subscription targets. |
| FR-004 | Inspection | Subscription management can be performed manually without deployment changes. |
| FR-005 | Test | For a supplied branch, workflow-run data yields `failedRuns` and `passedRuns` consistent with the rule `failed = conclusion != success` and `passed = total - failed`. |
| FR-006 | Test | For a supplied branch, merged pull-request timing data yields the expected average based on whole-hour differences, or `0` when no pull requests qualify. |
| NFR-001 | Inspection | Documentation and procedure require onboarding completion and AWS CLI credentials before stage listing. |
| NFR-002 | Inspection | Alert subscription management remains external to deployment. |
| NFR-003 | Inspection | Repository CI/CD references GitHub Actions. |
| NFR-004 | Test | Metrics retrieval aggregates paginated GitHub API results using page size 100 before metric computation. |
