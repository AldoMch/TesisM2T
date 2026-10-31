<!-- human_srs_review_A.md aligned with reviewer C content. Original human_srs_review.md is preserved. All human judgments are in English. -->

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
> ACCEPT=5, PARTIAL_ACCEPT=2, REJECT=0.

## Positive Observations

- Every requirement is traced to a specific evidence ID, and the traceability matrix records confidence and evidence type consistently.
- The SRS correctly restricts itself to the two relevant evidence chunks (E001, E002) and does not draw requirements from the irrelevant Eigen/Behavioral-Cloning chunks (E003-E006).
- Launch-file interfaces (styx.launch, site.launch), Docker/ROS environment, simulator vs. site modes, and the recorded training bag workflow are accurately and verifiably captured.
- Verification methods (Demonstration/Test/Inspection) and acceptance bases are provided for each requirement, supporting later auditability.

## Candidate Issues

### R001: architecture_detail

- Severity: `major`
- Suggested action: `accept_as_issue`
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
> Add a new System Architecture subsection after Section 2 Product Perspective: The system uses a ROS multi-node architecture, mainly including perception, planning, and control subsystems. The perception side is responsible for traffic light detection/classification and for producing stop-related waypoints. The planning side generates final waypoints through the waypoint loader/updater. The control side generates throttle, steering, and brake commands through the waypoint follower and DBW control nodes. Nodes exchange data through ROS topics such as current pose, base waypoints, traffic waypoint, final waypoints, twist command, and vehicle command.

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> The architecture diagram confirms that the system is a ROS multi-node system with Perception, Planning, and Control subsystems. ros/launch/styx.launch and site.launch also confirm waypoint, DBW, traffic light detector, and related nodes. The current SRS only mentions Docker/ROS/Simulator and lacks node-level and ROS topic-level interfaces.

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
> In Product Scope, add the missing goals: stop at red lights, stop/restart PID control according to /vehicle/dbw_enabled, and publish throttle/steering/brake commands at 50 Hz.

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> The README is explicitly Project Rubrics/grading goals and environment steps, not an independently verified description of system behavior. The current SRS writes all grading goals as implemented system capabilities, which overstates the evidence type.

### R003: non_verifiable

- Severity: `major`
- Suggested action: `accept_as_issue`
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
> Revise FR-004 to remain a qualitative acceptance goal and change Verification to Demonstration / qualitative review. Revise Section 8 to state: During simulation demonstration, the vehicle shall be able to drive along the given waypoints, and reviewers shall judge observable path-following behavior; the source evidence provides no quantitative smoothness threshold. Delete or downgrade NFR-004 to avoid turning a qualitative rubric statement into an NFR.

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> The README only says "smoothly follow waypoints" and gives no threshold for lateral error, jerk, acceleration, or similar measures. The current FR-004/NFR-004 use Test, but the acceptance criterion remains "smooth" and cannot be objectively repeated.

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
> Revise FR-001 to state: The system shall launch the corresponding runtime mode through the simulator/site launch entrypoints provided by the repository. Keep "must not require special launch instructions or additional download scripts" only in C-001/C-002. Delete or rewrite NFR-003 as a submission/evaluation constraint.

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> "No special launch instructions/additional download scripts" is an evaluation-submission constraint, not a system runtime function. The current FR-001 and NFR-003 duplicate C-001/C-002 and are misclassified.

### R005: non_verifiable

- Severity: `minor`
- Suggested action: `accept_as_issue`
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
> Revise FR-009 to state: The system shall perform traffic light detection and state classification on real images during site-mode bag playback, and when stopping is required for a red/yellow light, shall output the corresponding stop waypoint. Revise Section 8 acceptance to state: During real bag playback, traffic light state classification and red-light stop-related output shall be observable; the source evidence provides no accuracy threshold. Revise DR-003 to include "real images + traffic light state classification results."

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> The complete README paragraph confirms that the traffic light detection node detects/classifies incoming traffic lights and is used to stop before red lights. The source code also has RED/YELLOW/GREEN/UNKNOWN classifications. However, there is no accuracy or pass threshold.

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
> Recommended cleanup: delete NFR-005, keep only C-007, and revise C-007 to state that the submitted deliverable size shall not exceed 2GB. Remove the corresponding NFR-005 rows from Section 8 and the traceability matrix.

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> The 2GB value is evidenced, but it is a submission package size limit, not a runtime system capacity NFR. Rejecting it as a mandatory defect in human review is also reasonable, but a small classification cleanup would make the SRS cleaner.

### R007: ambiguity

- Severity: `minor`
- Suggested action: `partial_accept_as_issue`
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
> Revise FR-005 to state: The system shall respect the target top speed set by the kph parameter in waypoint_loader; vehicle speed shall not exceed the target top speed represented by each waypoint's twist.twist.linear.x value. Revise DR-001 to state: twist.twist.linear.x in waypoint data represents the target top speed, and the system shall use it as the upper bound for speed control. Revise Section 8 to state: By changing the kph velocity parameter, reviewers shall observe whether the vehicle respects the target top speed.

**Human decision**

- [ ] Accept
- [ ] Reject
- [x] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> The complete README sentence confirms that the test should change the kph velocity parameter, and the requirement is satisfied if the vehicle respects that target top speed. The current wording "consistent with" is somewhat ambiguous and should explicitly state "not exceed / respect the top speed."
