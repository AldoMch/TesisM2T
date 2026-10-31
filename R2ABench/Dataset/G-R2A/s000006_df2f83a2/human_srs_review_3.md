# Human SRS Review Sheet

## Metadata

- Sample directory: `s000006_df2f83a2`
- Generated SRS: `final_srs.md`
- Evidence pack: `evidence_pack.json`
- Review model: `claude-opus-4-8`
- Generated at: `2026-06-05T15:33:07.816884Z`
- Raw model response: `model_srs_review_raw.md`
- Parse status: `parsed`

## Overall Model Opinion

- Recommendation: `revise`
- Confidence: `0.78`
- Rationale: The SRS is well-traced and conservative, with most claims directly supported by evidence. However, the reinforcement-learning training capability is mentioned in evidence but omitted from functional/scope requirements, the egocentric vision/perception detail is underused, and a few DR/FR claims slightly overstate or imprecisely characterize the evidence (e.g., motor vs muscle clip semantics, 'checkpoints' existence). Targeted fixes are needed.

## Overall Human Decision

- [ ] Accept
- [ ] Reject
- [x] Partial accept

Reason:
> SRS 可追溯性强、措辞保守，整体可接受但需修订。需补 RL 训练能力（R001）、点名感知模态（R002）、补动作日志 FR（R005）、加两阶段构建细节（R006 仅文字部分）、收紧 FR-004/NFR-003 可验证性（R007）；R003 拒绝（DR-004 与 E005 一致，不构成 contradiction），R004 需查看完整 evaluator.py 后再定。

## Positive Observations

- Strong, conservative traceability: each FR/NFR/DR/Constraint cites specific evidence IDs and verification methods.
- Correctly captured numeric constraints from code: action input range [-1,1] (DR-003) and control clip [0,1] (DR-004) are grounded in E005.
- Appropriately notes absence of GUI and network interfaces rather than inventing them.
- Evaluation workflow (run_folder, evaluate directory creation) is accurately derived from E002 in FR-005/DR-005.

## Candidate Issues

### R001: missing_requirement

- Severity: `major`
- Suggested action: `needs_human_check`
- SRS location: Section 2 Product functions summary; Section 4 Functional Requirements
- Evidence IDs: E001, E003

**Claim or gap**

Evidence E001/E003 explicitly states the user 'is trained with reinforcement learning to solve the interaction task,' but no functional requirement or scope statement captures the RL training workflow.

**Model opinion**

Training via reinforcement learning is a core capability stated in the README. The SRS mentions RL only in passing in the product scope sentence but provides no FR, NFR, or scope item for training. This is an evidence-supported behavior missing from the functional requirements. Caution: the evidence does not detail the training entrypoint, so the requirement should be stated at the capability level only.

**Recommended human check**

Check the repository for a training script/module (e.g., uitb/train) to confirm scope and whether a verifiable FR can be written; confirm the RL workflow is in-scope for the SRS.

**Model proposed SRS change**

Add FR-006 to Section 4: 'FR-006 | Train user models with reinforcement learning | A configured simulator is available | The system shall support training the biomechanical user model with reinforcement learning to solve the configured interaction task | A trained model/checkpoint | Medium | Demonstration | E001, E003'. Conditional: if no training entrypoint is found in the repo, instead add a scope note acknowledging RL training as evidenced capability without a verifiable FR.

Optional human revised fix:
> 采用模型的条件性兜底而非其主 FR：以能力级表述补充 RL 训练（cite E001, E003），不要写成需要 Demonstration 验证的 FR-006，因为证据未含训练入口。验证方法建议用 Inspection/Analysis。

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> Issue 成立（major）。E001/E003 明确写了用户 "is trained with reinforcement learning"，RL 训练是核心能力，但 SRS 仅在产品范围句顺带提及，功能/范围需求中无对应条目，影响完整性。缺口可定位、有证据，应接受。

### R002: missing_requirement

- Severity: `minor`
- Suggested action: `accept_as_issue`
- SRS location: Section 2 Product functions summary; Section 3 Software/API interfaces
- Evidence IDs: E001, E004

**Claim or gap**

Egocentric vision / perception modalities (vision, proprioception) are explicitly evidenced (E001, E004) but the SRS only generically references 'perception capabilities' without naming the evidenced modalities.

**Model opinion**

E004 names concrete modalities ('vision', 'proprioception') under uitb/perception/[modality] and E001 cites egocentric vision. The SRS abstracts this away. Naming the evidenced modalities improves specificity and traceability without overstating scope.

**Recommended human check**

Confirm in uitb/perception/ which modality subpackages exist at the pinned commit.

**Model proposed SRS change**

In Section 2 Product functions summary, revise the perception bullet to: 'Represent the user with a muscle-actuated biomechanical model and perception modalities (e.g., egocentric vision, proprioception) [E001, E004]'.

Optional human revised fix:
> 采用模型建议：把感知条目改为点名 egocentric vision、proprioception，并 cite E001/E004。改动范围小、用 "e.g." 措辞，未夸大范围。

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> Issue 成立（minor）。E004 明确点名 vision/proprioception，E001 提到 egocentric vision，而 SRS 仅泛称 "perception capabilities"。点名有证据的模态提升具体性与可追溯性，且不夸大范围。

### R003: contradiction

- Severity: `major`
- Suggested action: `accept_as_issue`
- SRS location: Section 6 DR-004; Section 8/9 DR-004
- Evidence IDs: E005

**Claim or gap**

DR-004 states control values 'for motor and muscle actuators shall be constrained to the range [0, 1].' E005 shows both motor and muscle controls are np.clip(..., 0, 1), but the values clipped are smoothed motor average + action and muscle act + action respectively, not the raw action. The requirement is roughly correct on the [0,1] output bound but conflates input action ([-1,1]) and computed control.

**Model opinion**

The [0,1] clip on data.ctrl is accurate per E005, so DR-004 is largely supported. The risk is implying control values equal the action; they are derived (smoothed/accumulated) then clipped. Minor clarification avoids a misleading claim. Not a hard contradiction but should be precise.

**Recommended human check**

Re-read E005 set_ctrl logic to confirm both actuator types are clipped to [0,1] and that control is derived from action plus internal state.

**Model proposed SRS change**

Revise DR-004 to: 'Applied control values for motor and muscle actuators (computed from action plus internal actuation state) shall be clipped to the range [0, 1].'

Optional human revised fix:
> 不需要修改 SRS。

**Human decision**

- [ ] Accept
- [x] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> Issue 不成立。DR-004 写的是 "applied control values 约束在 [0,1]"，与 E005 的 `np.clip(...,0,1)` 完全一致；action 的 [-1,1] 已由 DR-003 单独覆盖，两行各司其职，SRS 未将 action 与控制值混淆，不构成 contradiction。模型自承 "not a hard contradiction"，所提修改仅为可选润色，不采纳。

### R004: traceability

- Severity: `minor`
- Suggested action: `needs_human_check`
- SRS location: Section 6 DR-005; FR-005
- Evidence IDs: E002

**Claim or gap**

DR-005 asserts the run folder 'containing checkpoints' and that evaluation 'shall use a run folder containing checkpoints.' E002 only constructs checkpoint_dir = os.path.join(run_folder, 'checkpoints') and creates evaluate_dir; it does not verify checkpoints exist before use within the shown snippet.

**Model opinion**

The 'checkpoints' path is defined in E002, so referencing the checkpoints directory is supported. The stronger claim that the run folder 'contains' checkpoints (as a precondition guarantee) is a reasonable inference but not fully shown in the snippet. Mild traceability/over-assertion concern.

**Recommended human check**

Inspect the full evaluator.py to confirm checkpoint loading and whether existence is validated.

**Model proposed SRS change**

Revise DR-005 to: 'Evaluation runs shall reference a run folder with a checkpoints directory and shall write outputs under an evaluate directory created if absent.'

Optional human revised fix:
> 定论前先查看完整 evaluator.py（"Load latest model if..." 之后的 checkpoint 加载逻辑、缺失 checkpoint 时的行为、run folder 实际结构）。模型软化 DR-005 措辞的方向合理，但应在核实后再改。

**Human decision**

- [ ] Accept
- [ ] Reject
- [x] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> 证据被截断，需讨论。E002 确实构造了 `checkpoint_dir = os.path.join(run_folder,'checkpoints')`，但片段在 "Load latest model if..." 处截断，无法确认是否校验 checkpoints 存在性。故 DR-005 "containing checkpoints" 是否过度断言无法定论，需查看完整文件。注："checkpoints" 路径本身已可证，即便成立也属轻微措辞问题。

### R005: missing_requirement

- Severity: `minor`
- Suggested action: `needs_human_check`
- SRS location: Section 3 User interfaces; FR-005
- Evidence IDs: E002

**Claim or gap**

E002 evidences a configurable action_log_file argument and 'if logging is enabled' behavior; the SRS mentions 'optional action-log output naming' in interfaces but no functional requirement captures action logging during evaluation.

**Model opinion**

Action logging is an evidenced evaluation feature controllable via CLI. It is acknowledged in External Interfaces but not represented as a functional/data requirement, leaving the behavior under-specified for verification.

**Recommended human check**

Confirm in evaluator.py the conditions under which action logging is enabled and the output file format.

**Model proposed SRS change**

Add to Section 4: 'FR-007 | Log actions during evaluation | Evaluation is invoked with logging enabled | The system shall write an action log to the configured action_log_file when logging is enabled | Action log file | Low | Test | E002'.

Optional human revised fix:
> 采用模型的 FR-007（cite E002），但保持能力级措辞、不要加入证据未展示的日志格式或触发细节。验证用 Test 或 Inspection。

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> Issue 成立（minor）。E002 含 `action_log_file` 参数及 "if logging is enabled" 的 help 文本，SRS 仅在外部接口提及，未形成功能需求。补一条低优先级 FR 有证据支撑、提升完整性。

### R006: architecture_detail

- Severity: `minor`
- Suggested action: `needs_human_check`
- SRS location: Section 2 Product perspective; Section 4 FR-001
- Evidence IDs: E004

**Claim or gap**

E004 describes a two-phase build process where the biomechanical model XML is integrated into a simulator XML; the ground-truth architecture diagram (figs/architecture.svg) likely depicts module composition. The SRS does not capture the two-phase XML integration build detail.

**Model opinion**

The two-phase build (integrating biomechanical model XML into simulator XML, then adding tasks/perception) is an evidenced architectural detail that strengthens FR-001 and DR-002. Worth cross-checking against the architecture diagram before adding.

**Recommended human check**

Compare figs/architecture.svg and the full Building-a-simulator README section to confirm the build phases and whether to encode them.

**Model proposed SRS change**

Augment FR-001 system behavior with: '... integrating the biomechanical model MuJoCo XML into the simulator MuJoCo XML and then adding the selected task and perception components (two-phase build per E004).'

Optional human revised fix:
> 仅在 FR-001 系统行为补充两阶段构建一句并 cite E004（先把生物力学模型 MuJoCo XML 集成进仿真器 XML，再加入任务/感知组件）。不要加入任何基于架构图的内容。

**Human decision**

- [ ] Accept
- [ ] Reject
- [x] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> 部分接受。① 成立：E004 明确写了 "build process contains two phases"，两阶段 XML 集成是显式证据，SRS 的 FR-001/DR-002 未点出，应补充。② 不成立：issue 里 "架构图 likely depicts 模块组合" 属推测，且 figs/architecture.svg 不在证据包内，不能据此增改。故仅接受两阶段构建部分，拒绝架构图部分。

### R007: non_verifiable

- Severity: `minor`
- Suggested action: `needs_human_check`
- SRS location: FR-004 / NFR-003
- Evidence IDs: E001

**Claim or gap**

FR-004 'standalone shareable units' and NFR-003 'suitable for sharing' use subjective qualifiers ('easily shared', 'suitable for sharing') that lack an observable acceptance criterion.

**Model opinion**

Evidence (E001) does support standalone packaging, but 'easily shared'/'suitable for sharing' is not directly testable. Tighten the acceptance criterion to an observable property (e.g., simulator runs as a self-contained importable package from its run/build folder).

**Recommended human check**

Confirm what artifact constitutes the standalone package (directory layout, importability) to phrase a verifiable criterion.

**Model proposed SRS change**

Revise FR-004/NFR-003 acceptance criterion to: 'A built simulator is produced as a self-contained package directory that can be loaded/imported and run without the source repository.'

Optional human revised fix:
> 采用模型方向：把 FR-004/NFR-003 的验收标准从主观词改为可观察属性（自包含、可独立加载/运行、实现 OpenAI Gym 接口）。验收锚定在 E001 的 "standalone" 即可，不要写超出证据的导入/安装机制。

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> Issue 成立（minor）。E001 支持 "standalone package"，但 FR-004/NFR-003 用 "easily/suitable for sharing" 等主观词，不可测，违反 SRS 标准自身的措辞规则，应收紧为可观察标准。
