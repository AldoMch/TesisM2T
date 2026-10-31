<!-- human_srs_review_A.md aligned with reviewer C content. Original human_srs_review.md is preserved. All human judgments are in English. -->

# Human SRS Review Sheet

## Metadata

- Sample directory: `s000058_3ebb884d`
- Generated SRS: `final_srs.md`
- Evidence pack: `evidence_pack.json`
- Review model: `claude-opus-4-8`
- Generated at: `2026-06-05T15:55:57.552818Z`
- Raw model response: `model_srs_review_raw.md`
- Parse status: `parsed`

## Overall Model Opinion

- Recommendation: `revise`
- Confidence: `0.74`
- Rationale: The SRS is generally well-traced to the six evidence chunks and avoids most overreach. However, several requirements overstate specificity beyond what evidence shows, such as FR-002 deletion semantics and the connector "put then delete with empty array" nuance, and the architecture diagram referenced in the repository is not reflected. A few claims about user classes and operating environment are weakly supported and should be checked.

## Overall Human Decision

- [ ] Accept
- [ ] Reject
- [x] Partial accept

Reason:
> ACCEPT=4, PARTIAL_ACCEPT=2, REJECT=1.

## Positive Observations

- Strong, consistent traceability: each FR/NFR/DR maps to specific evidence IDs, E001-E006, with verification methods.
- FR-005 accurately captures the `getSuccessfulDeploys` logic, where `conclusion != success` is counted as failed and `passed = total - failed`, matching E005.
- NFR-004 correctly captures the `per_page: 100` pagination and full aggregation behavior from E005/E006.
- Manual SNS subscription decoupling, FR-004/NFR-002/C-005, is faithfully drawn from E003.
- The SRS is appropriately conservative, avoiding fabrication beyond the evidence in most requirements.

## Candidate Issues

### R001: unsupported_claim

- Severity: `major`
- Suggested action: `accept_as_issue`
- SRS location: FR-002 / Section 4; DR-002
- Evidence IDs: E004

**Claim or gap**

FR-002 states the system shall "issue connector deletion for the provided deletion set." Evidence E004 shows `deleteConnectors` is always called with an empty array, `[]`, not a "provided deletion set."

**Model opinion**

The handler calls `connect.deleteConnectors(process.env.cluster, process.env.service, [])` with a hardcoded empty array. Describing this as a "provided deletion set" overstates configurability and misrepresents the actual behavior, which deletes nothing, or operates on an empty set.

**Recommended human check**

Inspect `configureConnectors.js` and the `deleteConnectors` signature/implementation to confirm whether the empty array means "delete none" or some other semantics.

**Model proposed SRS change**

Revise FR-002 system behavior to: "apply connector definitions (put) to the target cluster and service, invoke connector deletion with an empty deletion set, and restart the configured connectors." Update the acceptance basis in Section 8 accordingly.

Optional human revised fix:
> In FR-002, DR-002, and the Section 8 acceptance criteria, change "delete connectors according to the provided deletion set" to: The system shall apply connector definitions to the target cluster/service, call connector deletion with an empty deletion set, therefore deleting no connectors in the current configuration flow, and then restart the configured connectors.

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> `configureConnectors.js` does call `deleteConnectors(..., [])`; `deleteConnectors` iterates through the passed array and deletes items one by one, so an empty array means no connector is deleted. The SRS phrase "provided deletion set" is inaccurate.

### R002: architecture_detail

- Severity: `major`
- Suggested action: `accept_as_issue`
- SRS location: Section 2 Product perspective; FR-003
- Evidence IDs: E003

**Claim or gap**

The repository contains an architecture diagram, `docs/assets/architecture.png`, and E003 references a flow diagram with "The pattern of this flow is shown below", but the SRS does not reflect or reconcile the architecture diagram.

**Model opinion**

Both the ground-truth image URL and E003 indicate a documented architecture/flow diagram for the EventBridge-to-SNS pattern. The SRS should at least note this and verify its functional claims against it.

**Recommended human check**

Open `docs/assets/architecture.png` and the alerts README diagram; confirm the EventBridge-to-SNS flow and whether additional components, such as ECS services and subscription targets, should appear in the SRS.

**Model proposed SRS change**

Add to Section 2 Product Perspective a reference to the architecture diagram (`docs/assets/architecture.png`) and confirm FR-003's EventBridge-to-SNS flow matches the diagram; add any missing components after review.

Optional human revised fix:
> In Section 2 Product Perspective, add: The system supports transferring Appian-side data changes to CMS BigMAC and includes AWS-related capabilities for connector configuration, topic management, service event alerting, and runtime status observation. The architecture diagram may be used as a reference for later architecture modeling, but this SRS records requirement-level responsibilities and external-system interactions rather than directly prescribing deployment topology. In FR-003, revise to: When a project service produces a runtime event matching alerting rules, the system shall use AWS event routing capability to send that event to a notification topic and support distribution from that notification topic to manually maintained subscription targets.

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> The architecture diagram `docs/assets/architecture.png` clearly includes Appian Oracle DB, VPC peering, AWS Fargate Kafka Connect Cluster, topics Lambda, CMS BigMAC, EventBridge, SNS Topic, and subscription targets. The current SRS only describes EventBridge-to-SNS, so its architecture perspective is too narrow.

### R003: unsupported_claim

- Severity: `minor`
- Suggested action: `partial_accept_as_issue`
- SRS location: Section 2 User classes; FR-004
- Evidence IDs: E003

**Claim or gap**

The SRS defines a "Notification administrators" user class that "adds or removes SNS subscriptions manually." E003 says the subscription service is "managed manually" but does not define a distinct user role.

**Model opinion**

The manual-management statement is supported, but inventing a named user class, "Notification administrators", is an inference. It is reasonable, but not evidence-backed as a formal role.

**Recommended human check**

Confirm whether any documentation defines roles/personas for subscription management; otherwise soften to "operators/maintainers performing manual subscription management."

**Model proposed SRS change**

In Section 2 User Classes, merge "Notification administrators" into operators/maintainers, or annotate it as an inferred role. Adjust FR-004 trigger wording to "A user with subscription management access."

Optional human revised fix:
> In Section 2 User Classes, delete the standalone `Notification administrators` role. Instead write under Operators/DevOps users: Operators/DevOps users provide AWS credentials, run AWS-account-scoped operations, observe alerts, and manually manage SNS topic subscriptions when they have subscription management access. In FR-004, change the trigger condition to: A user/operator with SNS subscription management access adds or removes subscribers.

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> Manual management of SNS subscriptions is explicitly supported, but the formal user class "Notification administrators" is not defined by the documentation. It is safer to merge this into operators/maintainers.

### R004: ambiguity

- Severity: `minor`
- Suggested action: `accept_as_issue`
- SRS location: FR-001 / DR-001
- Evidence IDs: E001

**Claim or gap**

FR-001 describes a "run script" for listing stages, but E001 only states "Use the run script:" without naming or describing the script or its output format.

**Model opinion**

The procedure detail is genuinely underspecified in the evidence: the doc snippet is truncated and gives no script name or output schema. The SRS faithfully reflects this gap, but should flag it as non-verifiable beyond demonstration.

**Recommended human check**

Locate the actual run script referenced in `list-running-stages.md` to capture script name and output format for a stronger acceptance criterion.

**Model proposed SRS change**

In FR-001 and DR-001, note that the specific script and output format are not specified in evidence; after locating the script, add its name and output schema to the acceptance basis.

Optional human revised fix:
> In FR-001, DR-001, and the Section 8 acceptance criteria, replace the generic "stage-listing script" with: After onboarding and setting AWS CLI credentials, the user runs `nvm use` and `run listRunningStages`. The system shall query running stages in the current AWS account/region and output the result as `runningStages=<comma-separated stages>`.

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> The full documentation is not missing the script name. `list-running-stages.md` states to run `nvm use` and then `run listRunningStages`; `src/run.ts` also shows that the command outputs `runningStages=<comma-separated list>`.

### R005: traceability

- Severity: `minor`
- Suggested action: `probably_ignore`
- SRS location: Operating environment (Section 2); NFR-003 / C-004
- Evidence IDs: E001, E002

**Claim or gap**

Operating environment cites E002 for "terminal-based local execution during onboarding." E002 covers workspace setup, `setup.sh`, and terminal usage, but the GitHub Actions CI/CD claim in NFR-003/C-004 is traced to E001, whose snippet only partially shows it: "This project uses GitHub Actions as its CI/CD tool. Each of our repositories..."

**Model opinion**

The GitHub Actions CI/CD claim is supported by E001 but the snippet is truncated; the trace is acceptable but borderline. The E002 terminal claim is supported. It is worth a quick check that NFR-003 confidence, Medium, is appropriate and the source line is genuine.

**Recommended human check**

Verify the full E001 text confirms GitHub Actions as the CI/CD tool; confirm whether the line is in the list-running-stages document or another file.

**Model proposed SRS change**

No change if E001 confirms the GitHub Actions statement; otherwise re-source NFR-003/C-004 to the workflow YAML or CI docs.

Optional human revised fix:
> 

**Human decision**

- [ ] Accept
- [x] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> The full E001 document clearly says "this project uses GitHub Actions as its CI/CD tool", and the repository also has multiple workflows under `.github/workflows`. E002 also supports terminal/setup.sh onboarding. The model's concern is only a boundary issue caused by truncated evidence and is not a required SRS defect.

### R006: non_verifiable

- Severity: `minor`
- Suggested action: `accept_as_issue`
- SRS location: FR-006 / Section 8
- Evidence IDs: E006

**Claim or gap**

FR-006 computes average using `differenceInHours` and a `... || 0` fallback. The acceptance basis, "expected averageTimeToMerge, or 0 when none qualify", is verifiable, but the rounding/truncation behavior of `differenceInHours`, integer hours, is not stated.

**Model opinion**

E006 uses date-fns `differenceInHours`, which truncates to whole hours; the SRS describes "hour differences" without noting integer truncation, which could affect test expectations.

**Recommended human check**

Confirm `differenceInHours` truncation behavior and whether averages are computed on integer-hour values.

**Model proposed SRS change**

Add to FR-006 / DR-005: "merge durations are computed as whole-hour differences (date-fns differenceInHours, truncated), and the average defaults to 0 when no qualifying PRs exist."

Optional human revised fix:
> Accept the model opinion.

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> `getPrsToBranch.ts` uses `differenceInHours` from date-fns@2.29.3. That function defaults to `roundingMethod='trunc'`, meaning whole-hour truncation. The SRS only says "hour differences", which can make acceptance expectations unclear.

### R007: scope

- Severity: `minor`
- Suggested action: `partial_accept_as_issue`
- SRS location: Section 1 Product scope / Section 2
- Evidence IDs: none

**Claim or gap**

The evidence pack includes 40 documents across many types, including config, deployment_config, test, and tutorial, but the SRS is built from only six evidence chunks. Scope may understate broader repository capabilities, such as full deployment/serverless config and tests.

**Model opinion**

The SRS is appropriately conservative in sticking to retrieved evidence, but the `macpro-appian-connector` name and broad document set suggest the connector deployment/serverless infrastructure may be a larger feature than represented. This is a scope-coverage caveat, not a defect.

**Recommended human check**

Review additional repository docs/serverless config to determine whether major capabilities, such as deployment pipeline and Appian integration specifics, are missing from scope.

**Model proposed SRS change**

Add a scope note in Section 1 that the SRS covers behaviors supported by the retrieved evidence subset and may not enumerate all repository deployment/infrastructure capabilities.

Optional human revised fix:
> At the beginning of Section 1 Product Scope, add: This repository supports transfer of Appian data changes to CMS BigMAC and related operations management. The system shall support connector configuration and runtime maintenance, data topic management, service runtime event alerting, running-stage queries, deployment and PR metrics, and GitHub Actions based deployment/operations workflows.

**Human decision**

- [ ] Accept
- [x] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> The SRS indeed only covers behavior from the six evidence chunks, while the full repository documentation shows a broader core identity: Kafka Connector transfers Appian data to BigMAC and includes Serverless services, GitHub Actions CI/CD, security scanning, deployment workflows, GitHub Pages documentation, and related capabilities. There is no need to expand all 40 documents, but the scope statement and core identity should be added.
