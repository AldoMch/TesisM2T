# Human SRS Review Sheet

## Metadata

- Sample directory: `s000062_ee8cb840`
- Generated SRS: `final_srs.md`
- Evidence pack: `evidence_pack.json`
- Review model: `claude-opus-4-8`
- Generated at: `2026-06-05T15:58:19.127038Z`
- Raw model response: `model_srs_review_raw.md`
- Parse status: `parsed`

## Overall Model Opinion

- Recommendation: `revise`
- Confidence: `0.78`
- Rationale: The SRS is well-grounded in the two relevant evidence chunks (E001, E002) from the CarND-Capstone README and is internally traceable. However, the README is a Udacity project rubric/checklist, not a system specification; the SRS overstates several rubric goals as verifiable system requirements and omits architectural detail (the ground-truth architecture diagram and ROS node structure) that is referenced for this repository. Some requirements are non-verifiable as written, and FR-001/NFR-003 conflate a submission-evaluation constraint with a system capability.

## Overall Human Decision

- [ ] Accept
- [ ] Reject
- [x] Partial accept

Reason:
> 证据是 Udacity 项目 rubric 加环境 setup,不是系统规格,SRS 把评分目标当成已实现能力是主要问题。R002/R003/R004/R005/R006/R007 接受,R001 架构小节因证据无节点定义只接受补图引用、具体分解待开图。

## Positive Observations

- Every requirement is traced to a specific evidence ID, and the traceability matrix records confidence and evidence type consistently.
- The SRS correctly restricts itself to the two relevant evidence chunks (E001, E002) and does not draw requirements from the irrelevant Eigen/Behavioral-Cloning chunks (E003-E006).
- Launch-file interfaces (styx.launch, site.launch), Docker/ROS environment, simulator vs. site modes, and the recorded training bag workflow are accurately and verifiably captured.
- Verification methods (Demonstration/Test/Inspection) and acceptance bases are provided for each requirement, supporting later auditability.

## Candidate Issues

### R001: architecture_detail

- Severity: `major`
- Suggested action: `needs_human_check`
- SRS location: Section 2 Product perspective; Section 3 External Interfaces; overall
- Evidence IDs: E002

**Claim or gap**

The SRS describes a ROS-based capstone system but contains no architectural decomposition (ROS nodes, topics, perception/planning/control subsystems), despite a ground-truth architecture diagram existing for this repository.

**Model opinion**

A ground-truth architecture image is provided (doc/architecture/architecture.png) and the project is a ROS multi-node system. The SRS omits all node/topic-level architecture, which is a significant gap for a system integration project. This should be checked against the diagram and any node source.

**Recommended human check**

Open doc/architecture/architecture.png and inspect launch/styx.launch and launch/site.launch plus ros/src nodes to identify components (waypoint_updater, dbw_node, tl_detector, etc.) and confirm whether the SRS should include an architecture section.

**Model proposed SRS change**

Add a new subsection 'Section 2.x System Architecture' summarizing the ROS node decomposition and key topics as depicted in doc/architecture/architecture.png, e.g.: 'The system comprises ROS nodes for perception (traffic light detection), planning (waypoint updater), and control (drive-by-wire), communicating over ROS topics.' Conditional on confirming node names from the architecture diagram and ros/src before finalizing.

Optional human revised fix:
> 部分接受。architecture.png 已缓存确实存在,SRS 通篇无架构分解是真实缺口,先在第 2 节加图引用;但 E001/E002 是 README,不含节点定义,waypoint_updater/dbw_node/tl_detector 等具体节点需开图加 ros/src 确认后再写,不能凭项目类型推断。

**Human decision**

- [ ] Accept
- [ ] Reject
- [x] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> 图存在 → 缺口成立,补引用;节点级分解待开图,当前环境读不到图片内容。

### R002: scope

- Severity: `major`
- Suggested action: `accept_as_issue`
- SRS location: Section 1 Purpose/Product scope; throughout
- Evidence IDs: E001, E002

**Claim or gap**

Evidence E001/E002 are a project rubric (grading goals) and an environment-setup checklist, not statements of implemented system behavior. The SRS presents rubric goals as confirmed system requirements/capabilities.

**Model opinion**

The README text is explicitly titled 'Project Rubrics' and lists 'goals of this project.' Treating these as the system's actual requirements is defensible for an SRS but risks overstating that the implementation does these things. The framing should make clear these derive from the project rubric/acceptance criteria, not verified behavior.

**Recommended human check**

Confirm whether the README content is rubric/acceptance criteria vs. implementation description, and decide if requirements should be framed as 'acceptance goals' rather than asserted capabilities.

**Model proposed SRS change**

In Section 1 Purpose, add: 'Requirements in this document are derived from the project rubric and setup instructions in the CarND-Capstone README and represent evaluation/acceptance goals rather than independently verified implemented behavior.'

Optional human revised fix:
> 

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> E001 标题即"Project Rubrics""goals of this project",这些是评分/验收目标,SRS 当成已验证实现行为属定性夸大,加一句来源澄清是对的。

### R003: non_verifiable

- Severity: `major`
- Suggested action: `needs_human_check`
- SRS location: FR-004, NFR-004; Section 8 acceptance
- Evidence IDs: E001

**Claim or gap**

'Smoothly follow waypoints' / 'motion shall be smooth' has no measurable threshold or observable acceptance criterion.

**Model opinion**

The evidence says 'Smoothly follow waypoints in the simulator' but provides no metric. As written, 'smooth' is subjective and not testable. The acceptance basis 'waypoint following is smooth' restates the ambiguity rather than resolving it.

**Recommended human check**

Check README/rubric and any project docs for quantitative smoothness criteria (max jerk, lateral deviation, speed limits). If none exist, flag as inherently qualitative.

**Model proposed SRS change**

Revise FR-004/NFR-004 acceptance basis to a measurable criterion if evidence supports it (e.g., 'lateral deviation from waypoint path remains within X m and jerk within Y m/s^3'); otherwise annotate as 'qualitative rubric criterion; no quantitative threshold available in evidence.'

Optional human revised fix:
> 采用后一选项。证据无任何量化指标,标注为"定性 rubric 准则,证据无量化阈值"即可,不要臆造 X/Y 数值。

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> "smoothly follow"无可测阈值,验收"following is smooth"只是复述歧义,标注为定性准则。

### R004: contradiction

- Severity: `major`
- Suggested action: `accept_as_issue`
- SRS location: FR-001, NFR-003, C-001, C-002
- Evidence IDs: E001

**Claim or gap**

FR-001 reframes the evaluator constraint ('we will not be able to accommodate special launch instructions or run additional scripts to download files') as a system capability ('shall launch correctly... without requiring special launch instructions').

**Model opinion**

The README statement is a submission/evaluation policy, not a system functional requirement. Encoding it as FR-001 mixes a process constraint with system behavior. C-001/C-002 already capture this correctly as constraints, so FR-001 partly duplicates and partly mischaracterizes the source.

**Recommended human check**

Confirm the README sentence is an evaluation policy; decide whether to demote FR-001's 'no special instructions' clause to a constraint reference rather than a functional requirement.

**Model proposed SRS change**

Reword FR-001 to: 'The system shall launch using the repository-provided launch files (styx.launch, site.launch).' Move the 'no special launch instructions/additional download scripts' clause to reference C-001/C-002 rather than asserting it as system behavior.

Optional human revised fix:
> 

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> README 那句"we will not be able to accommodate special launch instructions"是评审政策,C-001/C-002 已正确记为约束,FR-001 再重述成系统能力属重复加误归类。

### R005: non_verifiable

- Severity: `minor`
- Suggested action: `needs_human_check`
- SRS location: FR-009, DR-003; Section 8
- Evidence IDs: E002

**Claim or gap**

Traffic light detection 'validation' is asserted as High priority with a Test method, but evidence only says 'Confirm that traffic light detection works on real life im...' with no pass/fail criterion or accuracy threshold.

**Model opinion**

The evidence supports the existence of a confirmation step but gives no measurable criterion (e.g., detection accuracy, class set). 'Observable traffic light detection' is weakly verifiable. The truncated evidence text also limits confidence.

**Recommended human check**

Inspect full README real-world testing section and tl_detector node/docs for any accuracy or success criteria; confirm whether detection covers classification (red/yellow/green) vs. presence.

**Model proposed SRS change**

Add acceptance criterion to FR-009: 'Traffic light state (red/yellow/green) is correctly identified on played-back real-life images' if evidence confirms classification; otherwise note 'success criterion limited to visual confirmation per rubric.'

Optional human revised fix:
> 采用后一选项。E002 证据截断("works on real life im..."),无分类/精度标准,标注"验收限于按 rubric 的视觉确认"即可。

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> 证据只到"confirm ... works",无 pass/fail 或 red/yellow/green 分类,High+Test 偏重,降为视觉确认。

### R006: traceability

- Severity: `minor`
- Suggested action: `probably_ignore`
- SRS location: NFR-005, C-007 (2GB submission limit)
- Evidence IDs: E001

**Claim or gap**

The 2GB limit is correctly cited to E001, but it is a submission-size evaluation rule, classified as a 'Capacity constraint' / non-functional quality of the running system.

**Model opinion**

E001 supports the 2GB figure, so traceability is fine, but categorizing a submission-artifact size limit as a system 'Capacity constraint' (NFR) slightly misframes it. It is a process/deliverable constraint.

**Recommended human check**

Decide whether the 2GB limit belongs as a deliverable/process constraint (C-007 only) rather than also as a system NFR.

**Model proposed SRS change**

Reclassify NFR-005 description to 'The submitted project artifact (deliverable) shall not exceed 2 GB' and clarify it is a submission constraint; consider removing the duplicate NFR if C-007 suffices.

Optional human revised fix:
> 采用。2GB 是提交物大小规则,归 C-007 即可,NFR-005 作为系统 capacity 约束属误分类,可删重复项。

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> 溯源到 E001 没错,只是分类错位,属次要修订。

### R007: ambiguity

- Severity: `minor`
- Suggested action: `needs_human_check`
- SRS location: FR-005, DR-001
- Evidence IDs: E001

**Claim or gap**

Evidence text for the target speed requirement is truncated ('twist.twist.linear.x in waypo...'), so the exact constraint (e.g., respecting target top speed vs. not exceeding) is partially inferred.

**Model opinion**

The SRS interpretation ('respect target top speed') is reasonable but the source sentence is cut off, leaving uncertainty about whether it means do-not-exceed or match. Confidence is appropriately marked Medium in the matrix.

**Recommended human check**

Read the full README sentence to confirm whether 'respect the target top speed' means the vehicle must not exceed the waypoint linear.x value.

**Model proposed SRS change**

Clarify FR-005: 'The vehicle speed shall not exceed the target top speed specified in each waypoint's twist.twist.linear.x value' (conditional on confirming intent from full README).

Optional human revised fix:
> 采用,采"not exceed"措辞并标注"待全文确认"。证据句被截断("twist.twist.linear.x in waypo..."),但 README 原文"Respect the target top speed"通常指不超过,SRS 已标 Medium,合理。

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> 截断导致 do-not-exceed 与 match 有歧义,采不超过的解读并保留待核标注。
