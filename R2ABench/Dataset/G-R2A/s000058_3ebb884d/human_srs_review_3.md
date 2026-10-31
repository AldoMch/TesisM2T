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
- Rationale: The SRS is generally well-traced to the six evidence chunks and avoids most overreach. However, several requirements overstate specificity beyond what evidence shows (e.g., FR-002 deletion semantics, the connector 'put then delete with empty array' nuance), and the architecture diagram referenced in the repo is not reflected. A few claims about user classes and operating environment are weakly supported and should be checked.

## Overall Human Decision

- [ ] Accept
- [ ] Reject
- [x] Partial accept

Reason:
> R001/R002/R003/R004/R006 接受，R005/R007 拒绝（GitHub Actions 句子已在 E001；范围限定已在 Purpose）。

## Positive Observations

- Strong, consistent traceability: each FR/NFR/DR maps to specific evidence IDs (E001–E006) with verification methods.
- FR-005 accurately captures the getSuccessfulDeploys logic (conclusion != success counted as failed, passed = total - failed) matching E005.
- NFR-004 correctly captures the per_page: 100 pagination and full aggregation behavior from E005/E006.
- Manual SNS subscription decoupling (FR-004/NFR-002/C-005) is faithfully drawn from E003.
- The SRS is appropriately conservative, avoiding fabrication beyond the evidence in most requirements.

## Candidate Issues

### R001: unsupported_claim

- Severity: `major`
- Suggested action: `accept_as_issue`
- SRS location: FR-002 / Section 4; DR-002
- Evidence IDs: E004

**Claim or gap**

FR-002 states the system shall 'issue connector deletion for the provided deletion set.' Evidence E004 shows deleteConnectors is always called with an empty array (`[]`), not a 'provided deletion set.'

**Model opinion**

The handler calls `connect.deleteConnectors(process.env.cluster, process.env.service, [])` with a hardcoded empty array. Describing this as a 'provided deletion set' overstates configurability and misrepresents the actual behavior, which deletes nothing (or operates on an empty set).

**Recommended human check**

Inspect configureConnectors.js and deleteConnectors signature/implementation to confirm whether the empty array means 'delete none' or some other semantics.

**Model proposed SRS change**

Revise FR-002 system behavior to: 'apply connector definitions (put) to the target cluster and service, invoke connector deletion with an empty deletion set, and restart the configured connectors.' Update the acceptance basis in Section 8 accordingly.

Optional human revised fix:
> 

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> E004 中 deleteConnectors(cluster, service, []) 第三参恒为空数组硬编码；FR-002"issue connector deletion for the provided deletion set"夸大可配置性，应改为"空删除集"。

### R002: architecture_detail

- Severity: `major`
- Suggested action: `needs_human_check`
- SRS location: Section 2 Product perspective; FR-003
- Evidence IDs: E003

**Claim or gap**

The repository contains an architecture diagram (docs/assets/architecture.png) and E003 references a flow diagram ('The pattern of this flow is shown below'), but the SRS does not reflect or reconcile the architecture diagram.

**Model opinion**

Both the ground-truth image URL and E003 indicate a documented architecture/flow diagram for the EventBridge→SNS pattern. The SRS should at least note this and verify its functional claims against it.

**Recommended human check**

Open docs/assets/architecture.png and the alerts README diagram; confirm the EventBridge→SNS flow and whether additional components (ECS services, subscription targets) should appear in the SRS.

**Model proposed SRS change**

Add to Section 2 Product perspective a reference to the architecture diagram (docs/assets/architecture.png) and confirm FR-003's EventBridge→SNS flow matches the diagram; add any missing components after review.

Optional human revised fix:
> 

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> 虽 image_download_status=failed，但 (a) E003 正文自写"The pattern of this flow is shown below:"已引用流程图，(b) CSV image_url 确认图存在。图确实存在、SRS 仅文字描述未引用 → 真实缺口，非 PARTIAL_ACCEPT。

### R003: unsupported_claim

- Severity: `minor`
- Suggested action: `needs_human_check`
- SRS location: Section 2 User classes; FR-004
- Evidence IDs: E003

**Claim or gap**

The SRS defines a 'Notification administrators' user class that 'adds or removes SNS subscriptions manually.' E003 says subscription service is 'managed manually' but does not define a distinct user role.

**Model opinion**

The manual-management statement is supported, but inventing a named user class ('Notification administrators') is an inference. It is reasonable but not evidence-backed as a formal role.

**Recommended human check**

Confirm whether any docs define roles/personas for subscription management; otherwise soften to 'operators/maintainers performing manual subscription management.'

**Model proposed SRS change**

In Section 2 User classes, merge 'Notification administrators' into operators/maintainers, or annotate it as an inferred role. Adjust FR-004 trigger wording to 'A user with subscription management access.'

Optional human revised fix:
> 

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> E003 只说订阅"managed manually"，未定义角色。SRS 自造"Notification administrators"用户类属推断，应并入 operators/maintainers 或标 inferred。

### R004: ambiguity

- Severity: `minor`
- Suggested action: `needs_human_check`
- SRS location: FR-001 / DR-001
- Evidence IDs: E001

**Claim or gap**

FR-001 describes a 'run script' for listing stages, but E001 only states 'Use the run script:' without naming or describing the script or its output format.

**Model opinion**

The procedure detail is genuinely underspecified in the evidence (the doc snippet is truncated and gives no script name or output schema). The SRS faithfully reflects this gap but should flag it as non-verifiable beyond demonstration.

**Recommended human check**

Locate the actual run script referenced in list-running-stages.md to capture script name and output format for a stronger acceptance criterion.

**Model proposed SRS change**

In FR-001 and DR-001, note that the specific script and output format are not specified in evidence; after locating the script, add its name and output schema to the acceptance basis.

Optional human revised fix:
> 

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> E001 仅"Use the run script:"，无脚本名/输出格式（截断）。加"证据未规定"注记准确且安全。

### R005: traceability

- Severity: `minor`
- Suggested action: `probably_ignore`
- SRS location: Operating environment (Section 2); NFR-003 / C-004
- Evidence IDs: E001, E002

**Claim or gap**

Operating environment cites E002 for 'terminal-based local execution during onboarding.' E002 covers workspace setup (setup.sh, terminal) but the GitHub Actions CI/CD claim (NFR-003, C-004) is traced to E001 whose snippet only partially shows it ('This project uses GitHub Actions as its CI/CD tool. Each of our repositories...').

**Model opinion**

The GitHub Actions CI/CD claim is supported by E001 but the snippet is truncated; the trace is acceptable but borderline. The E002 terminal claim is supported. Worth a quick check that NFR-003 confidence ('Medium') is appropriate and the source line is genuine.

**Recommended human check**

Verify the full E001 text confirms GitHub Actions as CI/CD tool; confirm whether the line is in the list-running-stages doc or another file.

**Model proposed SRS change**

No change if E001 confirms the GitHub Actions statement; otherwise re-source NFR-003/C-004 to the workflow YAML or CI docs.

Optional human revised fix:
> 不采用（无需改动）。

**Human decision**

- [ ] Accept
- [x] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> E001 可见文本已直接包含"This project uses GitHub Actions as its CI/CD tool"，E002 支持 terminal/setup.sh。NFR-003/C-004 与 Operating env 溯源均站得住，无缺陷；模型亦自标 probably_ignore。

### R006: non_verifiable

- Severity: `minor`
- Suggested action: `accept_as_issue`
- SRS location: FR-006 / Section 8
- Evidence IDs: E006

**Claim or gap**

FR-006 computes average using `differenceInHours` and a `... || 0` fallback. The acceptance basis ('expected averageTimeToMerge, or 0 when none qualify') is verifiable, but the rounding/truncation behavior of differenceInHours (integer hours) is not stated.

**Model opinion**

E006 uses date-fns differenceInHours which truncates to whole hours; the SRS describes 'hour differences' without noting integer truncation, which could affect test expectations.

**Recommended human check**

Confirm differenceInHours truncation behavior and whether averages are computed on integer-hour values.

**Model proposed SRS change**

Add to FR-006 / DR-005: 'merge durations are computed as whole-hour differences (date-fns differenceInHours, truncated), and the average defaults to 0 when no qualifying PRs exist.'

Optional human revised fix:
> 

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> E006 用 date-fns differenceInHours（整小时截断）+||0。SRS"hour differences"未说明整数截断，会影响测试期望，应补明。

### R007: scope

- Severity: `minor`
- Suggested action: `needs_human_check`
- SRS location: Section 1 Product scope / Section 2
- Evidence IDs: none

**Claim or gap**

The evidence pack includes 40 documents across many types (config, deployment_config, test, tutorial), but the SRS is built from only 6 evidence chunks. Scope may understate broader repository capabilities (e.g., full deployment/serverless config, tests).

**Model opinion**

The SRS is appropriately conservative in sticking to retrieved evidence, but the 'macpro-appian-connector' name and broad document set suggest the connector deployment/serverless infrastructure may be a larger feature than represented. This is a scope-coverage caveat, not a defect.

**Recommended human check**

Review additional repository docs/serverless config to determine whether major capabilities (deployment pipeline, Appian integration specifics) are missing from scope.

**Model proposed SRS change**

Add a scope note in Section 1 that the SRS covers behaviors supported by the retrieved evidence subset and may not enumerate all repository deployment/infrastructure capabilities.

Optional human revised fix:
> 不采用（已覆盖）。如要可在 Purpose 末尾补一句"未必枚举全部部署/基础设施能力"，属可选润色，非缺陷。

**Human decision**

- [ ] Accept
- [x] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> SRS Purpose 已写"covers the repository behaviors directly supported by the evidence pack..."，范围限定已覆盖；模型拟加 caveat 价值低、无具体 evidence ID、不影响需求质量。
