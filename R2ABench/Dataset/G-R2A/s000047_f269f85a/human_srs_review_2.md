# Human SRS Review Sheet

## Metadata

- Sample directory: `s000047_f269f85a`
- Generated SRS: `final_srs.md`
- Evidence pack: `evidence_pack.json`
- Review model: `claude-opus-4-8`
- Generated at: `2026-06-05T15:49:32.929316Z`
- Raw model response: `model_srs_review_raw.md`
- Parse status: `parsed`

## Overall Model Opinion

- Recommendation: `revise`
- Confidence: `0.78`
- Rationale: The SRS is well-grounded in the six evidence chunks and traces requirements cleanly. However, it overstates scope in places (the repo is a larger Electron desktop application than the six chunks suggest), makes a few inferences beyond evidence (e.g., RESIP map/filter details, language propagation framed as a requirement), and includes some non-verifiable or weakly-supported NFR claims. Targeted edits are needed before acceptance.

## Overall Human Decision

- [ ] Accept
- [ ] Reject
- [ ] Partial accept

Reason:
> 

## Positive Observations

- Functional requirements FR-001 through FR-009 are each cleanly traced to a single primary evidence chunk, and the traceability matrix is consistent with the functional requirements table.
- FR-001/FR-002 settings sanitization requirements are precisely and verifiably specified, directly matching the test assertions in E001 (defaults isTrackingEnabled: true, isMonitoringEnabled: true, language: 'en').
- Data requirements correctly enumerate the export input fields (aliases, comments, files/folders, metadata, tags, hashes) consistent with the GenerateCsvExportOptions interface in E005.
- The SRS appropriately distinguishes 'Explicit' vs 'Inferred' confidence (e.g., NFR-004 marked Inferred), showing reasonable evidence discipline.
- Hash debug output file names (hash-result-debug, hash-error-debug) and the userData path are accurately reflected from E004.

## Candidate Issues

### R001: scope

- Severity: `major`
- Suggested action: `needs_human_check`
- SRS location: Section 1 Product Scope; Section 2 Overall Description
- Evidence IDs: none

**Claim or gap**

The SRS scopes the product to only six narrow behaviors (settings sanitization, four export types, hash computation), but the evidence pack indicates 40 documents and a much broader Electron desktop application (archifiltre-docs) for archival file-tree analysis.

**Model opinion**

The SRS is honest in saying it covers 'evidenced' behavior, but a reader could mistake this for the full product scope. The product is an archive-documentation/visualization desktop tool; exports and hashing are sub-features. The scope statement should explicitly note that only a retrieved subset of repository behavior is covered.

**Recommended human check**

Inspect the repository README and src tree to confirm the overall product purpose (archival file system visualization/documentation) and add a scope-limitation disclaimer.

**Model proposed SRS change**

In Section 1 Product Scope, add: 'This SRS covers only the subset of repository behavior captured in evidence chunks E001-E006 (settings sanitization, export generation, and hash computation). The broader archifiltre-docs desktop application functionality (file-tree loading, visualization, tagging UI, etc.) is out of scope for this evidence-bound document.'

Optional human revised fix:
> 

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> 没有直接证据给出了完整产品目的的具体描述，属于过度推断。issue不成立。

### R002: unsupported_claim

- Severity: `major`
- Suggested action: `needs_human_check`
- SRS location: FR-005; Section 3 Software/API Interfaces (RESIP); Section 9 traceability
- Evidence IDs: E003

**Claim or gap**

FR-005 states the system 'map/filter worker results into RESIP export progress and output' with 'progress updates and final export result', but the E003 chunk is truncated and only shows imports, the ResipExportProgress interface declaration, and use of map/filterResults — the actual emission/progress behavior is not fully shown.

**Model opinion**

The map and filterResults imports and ResipExportProgress interface partially support the claim, but the precise progress/result emission semantics are inferred from truncated text. The claim is plausible but should be softened or verified against full source.

**Recommended human check**

Open src/exporters/resip/resip-export.controller.ts at the commit and confirm the observable emits progress updates and a final RESIP result via map/filterResults.

**Model proposed SRS change**

In FR-005 System Behavior, change to: 'Start background worker processing and transform worker results using map/filter operators.' Mark the progress/final-result emission detail as 'to be confirmed against full source' until verified.

Optional human revised fix:
> 

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> Issue 成立。SRS 对 RESIP progress/final result 的表述强于截断证据，建议采纳。

### R003: ambiguity

- Severity: `minor`
- Suggested action: `needs_human_check`
- SRS location: FR-004; FR-006; FR-007
- Evidence IDs: E002, E005, E006

**Claim or gap**

FR-004 frames 'propagate the current language into export generation' as a distinct requirement, but the evidence (E002, E005, E006) shows language is simply read from a shared `translations` singleton and passed into the worker payload — not a configurable propagation mechanism.

**Model opinion**

The behavior is real (language is included in worker input across exporters), but the wording 'propagate the current language' suggests a richer feature than a static read of `translations.language`. Acceptable as a low-level functional detail, but could mislead on configurability/locale-switching capability.

**Recommended human check**

Confirm whether `translations.language` is dynamically updatable at runtime or a static value, to decide whether 'current language' is accurate.

**Model proposed SRS change**

In FR-004, clarify Description to: 'The system shall include the language value from the translations module in the tree CSV export worker input.' Apply analogous clarification to FR-006/FR-007 language statements.

Optional human revised fix:
> 

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> issue成立，当前的证据只支持读取并传入 `translations.language`，建议采纳意见。

### R004: non_verifiable

- Severity: `minor`
- Suggested action: `accept_as_issue`
- SRS location: NFR-001
- Evidence IDs: E002, E003, E005, E006

**Claim or gap**

NFR-001 asserts 'non-blocking progress or result delivery mechanisms' and is marked 'Explicit', but the evidence shows use of observables/background worker forks — non-blocking is an inference, not an explicitly tested property.

**Model opinion**

The use of backgroundWorkerProcess$ and observables strongly implies async/non-blocking behavior, but labeling it 'Explicit' overstates the evidence. The acceptance basis ('Inspection') is reasonable, but the confidence tag should be 'Inferred' for the non-blocking claim.

**Recommended human check**

Verify backgroundWorkerProcess$ runs on a worker thread/fork (off the main thread) to substantiate the non-blocking claim.

**Model proposed SRS change**

In NFR-001, change Confidence from 'Explicit' to 'Inferred' and rephrase: 'Export workflows use background worker processes and observable result delivery, which are expected to provide non-blocking behavior (to be confirmed).'

Optional human revised fix:
> 

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> issue成立，建议采纳修改意见。

### R005: unsupported_claim

- Severity: `minor`
- Suggested action: `probably_ignore`
- SRS location: NFR-004; C-001
- Evidence IDs: E004

**Claim or gap**

NFR-004 claims debug artifacts are placed in the user data directory 'to preserve environment portability across installations.' The rationale (portability intent) is an inference; evidence only shows the path is `remote.app.getPath('userData')`.

**Model opinion**

The fact (debug files written under userData) is supported by E004 and the SRS correctly marks NFR-004 as 'Inferred'. The portability rationale is editorializing but harmless. Acceptable as low-severity; the 'Inferred' tag mitigates the risk.

**Recommended human check**

Optional: confirm whether any code comment or doc states portability intent; otherwise treat rationale as inferred.

**Model proposed SRS change**

In NFR-004, soften to: 'Hash debug artifacts shall be stored under the runtime-provided application user data directory (remote.app.getPath("userData")).' Remove or qualify the portability rationale as 'inferred'.

Optional human revised fix:
> 建议采纳，可删除 “to preserve environment portability” 或明确标注该动机只是 inferred。

**Human decision**

- [ ] Accept
- [x] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> issue成立，没有直接证据支持。

### R006: traceability

- Severity: `minor`
- Suggested action: `accept_as_issue`
- SRS location: Section 3 Communication Interfaces (Observable/data stream row, E004)
- Evidence IDs: E004

**Claim or gap**

The Observable/data stream delivery row cites E004 alongside E002/E003/E006, but E004 returns a 'DataProcessingStream' for hashes, not a tree/CSV/Excel observable — the grouping conflates hash streaming with export observables.

**Model opinion**

E004 does involve a stream (DataProcessingStream / computeBatch$), so the citation is not wrong, but the row text says 'Tree CSV, RESIP, and Excel/CSV-related workflows' which does not include hashing — yet E004 is listed. The evidence-to-claim mapping is slightly inconsistent.

**Recommended human check**

Decide whether to add hash computation to the observable/stream row text, or remove E004 from that row for consistency.

**Model proposed SRS change**

In the Observable/data stream delivery row, either add 'and hash computation' to the workflow list, or remove E004 from the Evidence cell so the citation matches the listed workflows.

Optional human revised fix:
> 应当直接从证据中删除E004.

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> issue成立，E004 支持 hash stream，不应该放在这一行当中，应当删除。

### R007: non_verifiable

- Severity: `minor`
- Suggested action: `probably_ignore`
- SRS location: NFR-002; Section 8 (NFR-002 acceptance)
- Evidence IDs: E004

**Claim or gap**

NFR-002 acceptance basis is 'Source inspection confirms batch size configuration', referring to BATCH_SIZE in E004, but the evidence chunk shows `batchSize: BATCH_SIZE` without the constant's value, so the actual batch granularity is unverifiable from evidence.

**Model opinion**

The batch-processing requirement itself is supported (computeBatch$ with batchSize). The acceptance criterion is verifiable by inspection of the BATCH_SIZE constant, so this is a minor traceability/specificity gap rather than a true defect.

**Recommended human check**

Locate the BATCH_SIZE constant definition to confirm a concrete value, and consider citing it for full verifiability.

**Model proposed SRS change**

In NFR-002 acceptance basis, add: 'and BATCH_SIZE constant defines the partition size (value to be cited from source).'

Optional human revised fix:
> 

**Human decision**

- [ ] Accept
- [x] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> 当前证据已经能够支持batch-size configuration，常量值不是必然要求，属于过度要求，issue不成立。

### R008: architecture_detail

- Severity: `minor`
- Suggested action: `needs_human_check`
- SRS location: Section 2 Operating Environment; Section 7 Constraints
- Evidence IDs: E004

**Claim or gap**

The SRS does not reference or reconcile against the ground-truth architecture diagram (docs/architecture.png), which may show additional components (renderer/main process split, IPC, redux reducers referenced in imports).

**Model opinion**

Evidence imports reference reducers (files-and-folders, tags, hashes, metadata) and Electron `remote`, suggesting a renderer/main process architecture not captured in the SRS. The architecture diagram should be checked to confirm whether the SRS understates the component structure.

**Recommended human check**

Review docs/architecture.png and confirm whether the SRS should mention the Electron main/renderer process model and the reducer-based state layer.

**Model proposed SRS change**

In Section 2 Product Perspective, add (after diagram review) a note describing the Electron main/renderer architecture and redux-style reducer state layer if confirmed by the architecture diagram.

Optional human revised fix:
> 

**Human decision**

- [ ] Accept
- [x] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> 当前证据不涉及架构图，issue不成立。
