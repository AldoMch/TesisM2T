# Human SRS Review Sheet

## Metadata

- Sample directory: `s000034_43fffc9f`
- Generated SRS: `final_srs.md`
- Evidence pack: `evidence_pack.json`
- Review model: `claude-opus-4-8`
- Generated at: `2026-06-05T15:43:54.204506Z`
- Raw model response: `model_srs_review_raw.md`
- Parse status: `parsed`

## Overall Model Opinion

- Recommendation: `revise`
- Confidence: `0.78`
- Rationale: The SRS is well-structured and largely evidence-backed with strong traceability. However, several claims overstate or misattribute evidence: the '4x faster' performance claim is conflated with the cyclic distribution example, the TMCMC efficiency figure source needs verification, the cyclic vs. node-1 distribution detail in FR-005 is imprecise, and the architecture diagram (ground-truth image) is never referenced or analyzed. A few API and configuration claims are partially inferred beyond the excerpts.

## Overall Human Decision

- [ ] Accept
- [ ] Reject
- [ ] Partial accept

Reason:
> 

## Positive Observations

- Strong, consistent traceability matrix mapping each requirement to specific evidence IDs with confidence and verification method.
- Conservative handling of API signatures: the SRS explicitly notes that map and callback APIs lack exact signatures in the excerpts rather than inventing them.
- Concrete, test-derived functional requirements (FR-001, FR-002) accurately reflect the test code in E002 (submit/wait/input/result).
- Constraints section appropriately captures the EPL v1.0 license and Python-module interface from observable evidence.
- Confidence and 'Explicit vs inferred' labeling (e.g., DR-004 marked inferred) shows good discipline in distinguishing direct evidence from inference.

## Candidate Issues

### R001: architecture_detail

- Severity: `minor`
- Suggested action: `needs_human_check`
- SRS location: Section 2 / overall; no architecture section
- Evidence IDs: none

**Claim or gap**

The repository provides a ground-truth architecture diagram (doc/torc_architecture.png) but the SRS contains no architecture description and does not reference or reconcile with it.

**Model opinion**

An architecture diagram exists and likely documents the master-worker model, worker threads, MPI ranks, and queues. The SRS infers some of these (queues, ranks, worker threads) from README text but never reconciles against the diagram, missing a verification opportunity and potentially omitting structural detail.

**Recommended human check**

Open doc/torc_architecture.png and check whether it depicts components (master/primary task, worker threads per rank, per-worker queues, MPI layer) that should be captured as architectural constraints or product perspective in the SRS.

**Model proposed SRS change**

Add a short subsection under 2.1 Product perspective summarizing the master-worker architecture (primary task, worker threads per MPI rank, per-worker queues, transparent MPI layer) with a citation to the architecture diagram, after confirming the diagram contents.

Optional human revised fix:
> 

**Human decision**

- [ ] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> 

### R002: unsupported_claim

- Severity: `major`
- Suggested action: `needs_human_check`
- SRS location: NFR-003; Section 9 traceability; Section 5
- Evidence IDs: E001, E006

**Claim or gap**

NFR-003 states '4x faster example when four workers each execute one task' citing E001, but E001/E006 describe the cyclic distribution example (10 tasks) and the 4x figure appears in a fragment about tasks being sent to node 1 where 'every worker executes one task and the application is executed 4x times faster' — the binding of '4x' to a specific worker/task configuration is reconstructed.

**Model opinion**

The evidence fragment does support '4x times faster' and 'every worker executes one task', but the SRS phrase 'when four workers each execute one task' is a reconstruction; the number of workers is not stated in the excerpt. This is a minor over-precision rather than fabrication.

**Recommended human check**

Read the full README section preceding example 3.1 to confirm the exact worker count and task configuration associated with the 4x speedup claim.

**Model proposed SRS change**

Revise NFR-003 to: 'repository evidence describes an example in which every worker executes one task and the application runs 4x faster than serial execution.' Remove the unverified 'four workers' specificity unless confirmed.

Optional human revised fix:
> 

**Human decision**

- [ ] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> 

### R003: ambiguity

- Severity: `major`
- Suggested action: `needs_human_check`
- SRS location: FR-005; Section 4
- Evidence IDs: E001, E006

**Claim or gap**

FR-005 describes 'cyclic distribution across available workers' and references the example, but E001 example 3.1 says tasks are 'distributed cyclically 10 tasks to the available workers', while the 4x fragment mentions tasks 'send to node 1'. The interaction between cyclic distribution and node assignment is unclear in the SRS.

**Model opinion**

The functional requirement conflates two distinct evidence fragments (cyclic distribution of 10 tasks in 3.1, and a separate scenario sending tasks to node 1). The mechanism of distribution (round-robin/cyclic vs. directed to a node) should be stated precisely to be verifiable.

**Recommended human check**

Confirm from README whether cyclic distribution and node-targeted submission are the same mechanism or distinct, and align FR-005 wording accordingly.

**Model proposed SRS change**

Clarify FR-005 system behavior to: 'The system shall distribute spawned tasks across available workers using cyclic (round-robin) assignment as documented in the submit-and-wait example (10 tasks across available workers).' Remove conflated node-1 phrasing unless verified.

Optional human revised fix:
> 

**Human decision**

- [ ] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> 

### R004: traceability

- Severity: `minor`
- Suggested action: `needs_human_check`
- SRS location: NFR-004; Section 9; DR-005
- Evidence IDs: E005

**Claim or gap**

NFR-004 attributes the '>90% efficiency on 1024 compute nodes' to E005. E005 does contain this text, but it describes TMCMC within Π4U on Piz Daint as an external use case/application result, not necessarily a property of torc_py itself.

**Model opinion**

The figure is genuinely in E005, so traceability to E005 is correct. However, framing it as a torc_py scalability requirement (rather than a reported result of a specific application using the library) risks overstating scope. The verification method 'Analysis' is also weakly defined for a third-party-reported number.

**Recommended human check**

Confirm from README context whether the 90%/1024-node result is attributed to torc_py's scheduling or to the Π4U/TMCMC application built on it; adjust requirement framing.

**Model proposed SRS change**

Reframe NFR-004 as a documented capability example: 'The system has been used to schedule TMCMC function evaluations achieving >90% parallel efficiency on 1024 compute nodes in the Π4U use case (reported result, not a guaranteed system property).'

Optional human revised fix:
> 

**Human decision**

- [ ] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> 

### R005: unsupported_claim

- Severity: `minor`
- Suggested action: `probably_ignore`
- SRS location: C-004; Section 3 / 2.4
- Evidence IDs: E002

**Claim or gap**

C-004 and operating environment cite TORC_WORKERS as evidenced in tests (E002). The E002 excerpt is truncated at 'os.environ["TORC_WORKERS' and does not show the full usage/assignment.

**Model opinion**

The variable name clearly appears, so the existence claim is supported, but the role ('worker-count configuration') is inferred from the name and a partial line. Low risk but worth a quick check of the full test file.

**Recommended human check**

Inspect tests/test_masterworker.py to confirm TORC_WORKERS is assigned a worker count and consumed by the library at startup.

**Model proposed SRS change**

If confirmed, keep C-004 as is; if the variable controls something else, revise to: 'Worker configuration is evidenced via the TORC_WORKERS environment variable in tests (exact semantics per test_masterworker.py).'

Optional human revised fix:
> 

**Human decision**

- [ ] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> 

### R006: scope

- Severity: `minor`
- Suggested action: `needs_human_check`
- SRS location: Section 2.2 / FR-008 / NFR-002
- Evidence IDs: E004

**Claim or gap**

The SRS repeatedly elevates 'allows legacy MPI at the application level' to a functional (FR-008) and non-functional (NFR-002) requirement, but the evidence (E004) lists it as one bullet describing the library's aims, not a tested or specified behavior.

**Model opinion**

Listing the same single README bullet as both FR-008 and NFR-002 is duplicative and inflates the requirement count. The claim is supported but is a design aim, not a verifiable behavior with an observable test; both are marked Inspection of documentation only.

**Recommended human check**

Decide whether transparent-MPI/legacy-MPI compatibility warrants both a functional and a non-functional requirement, or should be consolidated as a single compatibility constraint/requirement.

**Model proposed SRS change**

Consolidate FR-008 and NFR-002 into a single compatibility requirement, or explicitly note they are documentation-stated design aims (not test-verified behaviors) to avoid double-counting.

Optional human revised fix:
> 

**Human decision**

- [ ] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> 

### R007: non_verifiable

- Severity: `minor`
- Suggested action: `needs_human_check`
- SRS location: FR-007; Section 8
- Evidence IDs: E004

**Claim or gap**

FR-007 ('unified execution across shared and distributed memory platforms') is verified only by 'Inspection' of documentation, with no observable acceptance criterion demonstrating actual cross-platform execution.

**Model opinion**

This is a legitimate evidence-limited situation: the README asserts the capability but the evidence pack provides no test demonstrating distributed-memory execution. The requirement should be flagged as documentation-derived with lower confidence rather than presented at High confidence.

**Recommended human check**

Check whether any test or example in the repo actually exercises distributed-memory/multi-node execution to support FR-007/NFR-001 verification beyond documentation inspection.

**Model proposed SRS change**

Annotate FR-007 (and NFR-001) acceptance basis as 'documentation-asserted capability; no executable cross-platform test found in evidence' and lower stated confidence accordingly.

Optional human revised fix:
> 

**Human decision**

- [ ] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
>
