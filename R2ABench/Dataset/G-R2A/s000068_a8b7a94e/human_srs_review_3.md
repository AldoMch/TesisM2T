# Human SRS Review Sheet

## Metadata

- Sample directory: `s000068_a8b7a94e`
- Generated SRS: `final_srs.md`
- Evidence pack: `evidence_pack.json`
- Review model: `claude-opus-4-8`
- Generated at: `2026-06-05T16:02:20.589396Z`
- Raw model response: `model_srs_review_raw.md`
- Parse status: `parsed`

## Overall Model Opinion

- Recommendation: `revise`
- Confidence: `0.78`
- Rationale: The SRS is well-structured and mostly traceable to evidence, but several requirements overstate what the evidence supports (notably FR-005 command-counter increments and the cmdUtil packet parameter semantics), conflate README documentation with system behavior, and present CI-job timeouts as system NFRs. The repository is a large flight software framework (cFS), yet the SRS scope is narrowly drawn from a handful of workflow/README chunks, which risks understating scope. These need human adjudication rather than acceptance as-is.

## Overall Human Decision

- [ ] Accept
- [ ] Reject
- [x] Partial accept

Reason:
> 八条均成立。核心问题:把 README 教程口吻("should see ... counters increment")当成 shall 需求(R001),把 CI 的 timeout-minutes:15 当成性能 SLA(R003),把单条 cmdUtil 调用泛化成包结构(R004),以及基于 [DEPRECATED] 工作流推导 NFR 未加标注(R008)。R007 属可选完整性补充,低优先。全部接受。

## Positive Observations

- Every requirement carries an explicit evidence ID and a traceability matrix with confidence ratings, making adjudication efficient.
- The SRS is appropriately conservative in places (e.g., FR-001 build steps, FR-006 changelog categories) and accurately reflects the literal content of E001, E002, and E005.
- Verification methods and acceptance bases are provided per requirement, supporting testability for the CI-derived items.
- The introduction honestly states the scope is limited to evidenced README/workflow materials rather than overclaiming full-framework coverage.

## Candidate Issues

### R001: unsupported_claim

- Severity: `major`
- Suggested action: `needs_human_check`
- SRS location: FR-005, DR-002, Section 8 (FR-005 acceptance)
- Evidence IDs: E004

**Claim or gap**

FR-005 states the system 'shall expose command counter increments observable by the user' as a firm functional requirement, and DR-002 treats command counters as guaranteed output data.

**Model opinion**

E004 only says 'Should see telemetry, can send noops and see command counters increment.' This is README prose describing an expected behavior in a tutorial flow, not a normative system specification. The word 'should' is observational, not a binding requirement. Promoting it to a 'shall' functional requirement with High priority overstates the evidence.

**Recommended human check**

Re-read E004 full context in README. Decide whether the no-op/counter behavior is a tutorial expectation or a specifiable requirement; downgrade priority/verifiability if it is descriptive only.

**Model proposed SRS change**

Reword FR-005 System Behavior to: 'The README documents that after telemetry is enabled, no-op commands can be sent and command counter increments should be observable.' Change verification to 'Demonstration (documentation-based expectation)' and lower priority to Medium, or annotate as derived/observational rather than 'shall'.

Optional human revised fix:
> 采用。E004 原文"Should see telemetry, can send noops and see command counters increment."是教程预期口吻,提升为 High 优先级的 shall 功能需求过头,改为文档化预期并降级。

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> 

### R002: scope

- Severity: `major`
- Suggested action: `needs_human_check`
- SRS location: Section 1.2, 2.1, overall
- Evidence IDs: E002, E003, E006

**Claim or gap**

The SRS scope is limited to build/test workflows, telemetry interaction, and external integration points, derived from 6 evidence chunks. nasa/cFS is the Core Flight System framework (a flight software product with cFE, OSAL, PSP, and apps).

**Model opinion**

The repository is a substantial flight software framework. Restricting the product scope to CI workflows and a telemetry tutorial understates the repository scope. The SRS explicitly disclaims this ('scope is limited to documented build/test workflows...'), which is honest, but a reader could mistake this for the full product. The ground-truth diagram is a Reusable-Workflows-Architecture diagram, suggesting CI architecture is more elaborate than captured.

**Recommended human check**

Confirm whether the evidence pack genuinely lacks cFE/OSAL/PSP architectural content, or whether the retrieval under-sampled the README. Decide if a scope-limitation note should be made more prominent.

**Model proposed SRS change**

Add a bold limitation statement to Section 1.2: 'NOTE: This SRS captures only the subset of cFS behavior evidenced by the retrieved README and CI workflow chunks. The broader cFS framework (cFE, OSAL, PSP, bundled apps) is out of scope of the current evidence and not specified here.'

Optional human revised fix:
> 采用。证据仅 6 块(全是 workflow/README),cFS 是大型飞控框架,SRS 已诚实声明限定但应更醒目,避免被误读为完整产品规格。

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> 证据 doc_type 仅 readme/deployment_config,确无 cFE/OSAL/PSP 内容,限定说明合理。

### R003: non_verifiable

- Severity: `major`
- Suggested action: `accept_as_issue`
- SRS location: NFR-003, Section 8 (NFR-003)
- Evidence IDs: E006

**Claim or gap**

NFR-003 'Test boundedness' requires the functional test workflow to 'complete within a 15-minute CI timeout.' This is a CI job configuration (timeout-minutes: 15), not a system performance requirement, and a timeout is a kill ceiling, not a completion-time guarantee.

**Model opinion**

E006 shows 'timeout-minutes: 15' which is the maximum allowed time before the job is killed, not an asserted bound on actual completion. Stating the test 'shall complete within' 15 minutes is non-verifiable as written because the timeout does not guarantee completion; a job could fail or be killed at 15 minutes. This conflates a CI safety limit with a performance requirement.

**Recommended human check**

Verify whether 15 minutes is a completion SLA or merely a CI kill-switch. Reframe NFR-003 to reflect a configuration constraint rather than a performance guarantee.

**Model proposed SRS change**

Reword NFR-003 to: 'The deprecated functional test CI job shall be configured with a 15-minute timeout ceiling (timeout-minutes: 15); jobs exceeding this are terminated.' Acceptance basis: 'Workflow definition shows timeout-minutes: 15.' Verification: Inspection (not Test).

Optional human revised fix:
> 采用。E006 的 timeout-minutes:15 是超时即杀的上限,不是完成时间保证,"shall complete within"不可验证,改为配置约束并用 Inspection 验证。

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> 

### R004: ambiguity

- Severity: `minor`
- Suggested action: `needs_human_check`
- SRS location: DR-003, FR-003, Section 3.4
- Evidence IDs: E006

**Claim or gap**

Command packet parameters are described as fields 'pktid, cmdcode, endian, uint32'. The evidence shows these as cmdUtil CLI flags for one specific command (--pktid=0x1806 --cmdcode=17 --endian=LE --uint32=3 --uint32=0x40000000), not a general specification of command packet structure.

**Model opinion**

The SRS generalizes a single concrete cmdUtil invocation into a data-format requirement. 'endian' and 'uint32' are CLI argument types, not packet fields per se, and the example sends two --uint32 values. Calling these 'packet-oriented parameters' is a reasonable abstraction but slightly imprecise; the evidence supports only that cmdUtil accepts these flags, not a complete packet field schema.

**Recommended human check**

Confirm cmdUtil's actual parameter set from repository tooling; decide whether DR-003 should be scoped to 'cmdUtil accepts these CLI flags' rather than a packet schema.

**Model proposed SRS change**

Reword DR-003 to: 'The cmdUtil host utility accepts command-line flags including --pktid, --cmdcode, --endian, and one or more --uint32 arguments, as evidenced by a single functional-test invocation. This does not constitute a complete command packet schema.'

Optional human revised fix:
> 采用。E006 只有一条具体调用(--pktid=0x1806 --cmdcode=17 --endian=LE --uint32=3 --uint32=0x40000000),endian/uint32 是 CLI 参数类型而非包字段,且发了两个 --uint32,泛化成包结构 schema 不准确。

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> DR-003/FR-003/3.4 同源,一并按"cmdUtil 接受这些 flag"收窄。

### R005: ambiguity

- Severity: `minor`
- Suggested action: `needs_human_check`
- SRS location: Section 3.1, FR-004
- Evidence IDs: E004

**Claim or gap**

The 'Telemetry enablement UI' requirement says 'The system documentation shall support a user flow...' mixing documentation and system behavior. It is unclear whether this is a requirement on the system or on the README.

**Model opinion**

E004 is a README walkthrough ('Select Enable Tlm', 'Enter IP address...'). The SRS phrasing 'system documentation shall support a user flow' is muddled — documentation describes a flow; it does not 'support' it. This is an ambiguity between specifying the UI behavior versus specifying that documentation exists.

**Recommended human check**

Decide whether to specify the telemetry-enable UI behavior or to specify that the README documents the procedure, and rephrase consistently.

**Model proposed SRS change**

Reword Section 3.1 requirement to: 'The README shall document a telemetry-enable procedure in which the operator enables telemetry and enters the IP address of the system executing cFS (127.0.0.1 for local execution).'

Optional human revised fix:
> 采用。E004 是 README 操作步骤,"system documentation shall support a user flow"混淆了"文档描述流程"与"系统支持流程",按文档化过程表述更清楚。

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> 

### R006: architecture_detail

- Severity: `minor`
- Suggested action: `needs_human_check`
- SRS location: Section 2, NFR-001/NFR-004, References
- Evidence IDs: E005

**Claim or gap**

The ground-truth image is 'Reusable-Workflows-Architecture.svg', indicating a reusable/callable workflow architecture (workflow_call appears in E005). The SRS does not describe the reusable-workflow architecture or the relationships between the build, test, format-check, and changelog workflows.

**Model opinion**

E005 shows 'workflow_call:' indicating these workflows are designed for reuse/composition. The ground-truth diagram name confirms a deliberate reusable-workflow architecture. The SRS treats each workflow as an isolated capability and omits the orchestration/reuse architecture, which appears to be a notable design feature.

**Recommended human check**

Inspect the Reusable-Workflows-Architecture.svg and the full workflow set to determine whether a reusable-workflow architecture description should be added to Section 2.

**Model proposed SRS change**

Add to Section 2.1: 'The CI workflows are designed for reuse/composition (workflow_call), consistent with the repository's reusable-workflows architecture. [Pending verification against Reusable-Workflows-Architecture.svg and the complete workflow set.]'

Optional human revised fix:
> 采用。E005 含 workflow_call,ground-truth 图名即 Reusable-Workflows-Architecture.svg(已缓存),SRS 把各 workflow 当孤立能力、漏了复用编排架构;补说明并标待对照图。

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> workflow_call 有证据,可写;具体 workflow 关系待开 SVG 确认。

### R007: traceability

- Severity: `minor`
- Suggested action: `probably_ignore`
- SRS location: Section 1.4 References / FR-006 / E001
- Evidence IDs: E001

**Claim or gap**

FR-006 and DR-004 use a specific changelog generator (heinrichreimer/github-changelog-generator-action) with pullRequests: false and author: false, and run on workflow_dispatch only. The SRS captures categories and manual trigger but omits the disabling of PRs/authors and the specific action used.

**Model opinion**

Minor traceability gap. The evidence E001 specifies pullRequests: false and author: false, which affects changelog content. This is not captured in DR-004/FR-006. Low impact but worth noting for completeness.

**Recommended human check**

Decide whether changelog generation details (PRs excluded, authors excluded, specific action) warrant inclusion.

**Model proposed SRS change**

Augment DR-004 details: 'Changelog content excludes pull requests and authors (pullRequests: false, author: false) and is generated via the github-changelog-generator action on manual (workflow_dispatch) trigger.'

Optional human revised fix:
> 采用。E001 确有 pullRequests:false / author:false,DR-004/FR-006 漏掉,补全无害;模型自标 probably_ignore,属低优先完整性补充。

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> 影响低,采纳以求完整。

### R008: traceability

- Severity: `minor`
- Suggested action: `accept_as_issue`
- SRS location: Section 1.4 References, NFR-001
- Evidence IDs: E001, E005, E006

**Claim or gap**

Section 1.4 references workflow 'build-cfs-deprecated.yml' with evidence E002/E006, and NFR-001 cites 'ubuntu-latest' for E006, but E006 (functional tests) runs on 'ubuntu-18.04'. The mix of ubuntu-latest (E001/E005) and ubuntu-18.04 (E002/E006) should be precisely attributed.

**Model opinion**

NFR-001 cites E001, E005, E006 for 'ubuntu-latest and ubuntu-18.04'. E006 only shows ubuntu-18.04 (not ubuntu-latest); ubuntu-latest comes from E001/E005. The grouped citation is mostly accurate but conflates which runner maps to which workflow. Also note these workflows are explicitly '[DEPRECATED]', which the NFRs build upon — the deprecated status should be flagged since it affects requirement currency.

**Recommended human check**

Verify runner-to-workflow mapping and confirm that basing NFRs on a workflow labeled '[DEPRECATED]' is intended; consider flagging deprecated-derived requirements.

**Model proposed SRS change**

Add a note to NFR-001/NFR-002/NFR-003: 'These requirements are derived from a workflow labeled [DEPRECATED] (build-cfs-deprecated.yml); their currency should be re-validated against the active build/test workflows.' Correct runner attribution: ubuntu-latest (E001, E005); ubuntu-18.04 (E002, E006).

Optional human revised fix:
> 采用。E006/E002 工作流名含 [DEPRECATED],基于其推导 NFR 应标注时效性;且 NFR-001 把 ubuntu-latest 与 ubuntu-18.04 合并引用,runner 与 workflow 的对应应分清(E006 只见 ubuntu-18.04)。

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> deprecated 出处确凿,标注时效性对飞控类需求尤为重要。
