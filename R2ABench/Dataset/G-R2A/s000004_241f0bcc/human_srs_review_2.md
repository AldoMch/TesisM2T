# Human SRS Review Sheet

## Metadata

- Sample directory: `s000004_241f0bcc`
- Generated SRS: `final_srs.md`
- Evidence pack: `evidence_pack.json`
- Review model: `claude-opus-4-8`
- Generated at: `2026-06-05T15:32:04.952075Z`
- Raw model response: `model_srs_review_raw.md`
- Parse status: `parsed`

## Overall Model Opinion

- Recommendation: `revise`
- Confidence: `0.72`
- Rationale: The SRS is generally well-traced to the limited evidence pack and conservatively scoped to front-end, store, and SQL-script behavior. However, a few requirements overstate or sharpen evidence (e.g., FR-003 'logged in' state precision, controlled-list characterized as an API endpoint, three 'tokens' inferred from truncated text), and there is an unexamined architecture-diagram dimension (a broader system with backend services) that the SRS does not flag as out-of-scope/unverified. Targeted revisions are warranted before acceptance.

## Overall Human Decision

- [ ] Accept
- [ ] Reject
- [ ] Partial accept

Reason:
> 

## Positive Observations

- Strong, disciplined traceability: nearly every FR/NFR/DR/CON cites specific evidence IDs (E001-E006) and the traceability matrix is consistent with the body.
- Conservative scoping: the SRS explicitly notes where the evidence does not define payload schemas/message formats rather than inventing them (Section 3 Data exchange formats).
- FR-003, FR-004, and the guard/interceptor functional requirements are accurately and faithfully derived from E004's core README description.
- SQL-script requirements (DR-004, DR-005, CON-004, CON-005) are precise and well-anchored to E006, including the Volunteer.Active=0 by Id behavior and transaction/backup precautions.
- Verification methods are assigned per requirement and aggregated in Section 8, supporting testability for most items.

## Candidate Issues

### R001: scope

- Severity: `major`
- Suggested action: `needs_human_check`
- SRS location: Section 1 Product scope; Section 2 Product perspective; overall SRS
- Evidence IDs: E001

**Claim or gap**

The SRS scopes the product almost entirely to the front-end ClientApp, NgRx store, and SQL scripts, but the repository name (embc-ess) and the ground-truth architecture diagram imply a larger system including a backend API/server that is repeatedly referenced ('mandatory that the front-end have an API to consume').

**Model opinion**

The evidence pack provided is heavily front-end-weighted (5 of 6 chunks from ClientApp/store, 1 from sql-scripts), so the SRS scoping is defensible given the pack. But the architecture diagram and the repeated API dependency suggest backend components exist and are not represented. The SRS should explicitly state this is a front-end-focused subset and that backend/server components are out of scope for this evidence pack, to avoid understating repository scope.

**Recommended human check**

Open the architecture-diagram.png and repository tree to confirm whether backend/server projects exist (e.g., an ASP.NET/embc-app server). Confirm whether the SRS should declare them out of scope.

**Model proposed SRS change**

In Section 1 Product scope, add: 'This SRS is limited to the front-end ClientApp, its NgRx store, and the repository SQL scripts as represented in the evidence pack. Backend/API server components referenced as dependencies are out of scope for this document and were not provided as evidence.'

Optional human revised fix:
> 

**Human decision**

- [✅️] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> 可采用模型建议

### R002: unsupported_claim

- Severity: `major`
- Suggested action: `accept_as_issue`
- SRS location: Section 3 Software/API interfaces — `controlled-list` row; FR-005; DR-002
- Evidence IDs: E003

**Claim or gap**

The SRS lists `controlled-list` as an 'endpoint/data source' in the Software/API interfaces table. Evidence E003 describes controlled-list only as 'Load infrequently changing data at init time. Puts things into the ngrx store' — it does not characterize it as an HTTP endpoint with parameters like the evacuee/incident-task/etc. services.

**Model opinion**

The other services in E003 are explicitly described as 'Http service to perform [CRUD] with params on the endpoint', but controlled-list is described differently (a loader into the store). Listing it under Software/API interfaces alongside HTTP endpoints overstates evidence. The functional behavior (load at init into store, FR-005/DR-002) is supported; the API-endpoint classification is not.

**Recommended human check**

Inspect the controlled-list service source to confirm whether it makes HTTP calls to a 'controlled-list' endpoint or aggregates other data. Decide whether it belongs in the API interface table.

**Model proposed SRS change**

In Section 3 Software/API interfaces, change the `controlled-list` row description to: 'Controlled-list loader (not characterized as a parameterized HTTP endpoint in evidence) — loads infrequently changing data at initialization into the client store.' Alternatively move this row out of the API interfaces table into the data-loading description.

Optional human revised fix:
> 

**Human decision**

- [✅️] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> 可以采纳修改建议

### R003: ambiguity

- Severity: `minor`
- Suggested action: `needs_human_check`
- SRS location: FR-003; CON-002; Section 2 Assumptions; NFR-001
- Evidence IDs: E001

**Claim or gap**

Evidence E001 text is truncated ('There are three different s that are needed', 'set the proxy and token in the file in a way similar to seen in') and the word for the 'three different' items is missing. The SRS infers 'three role-paired tokens', but the actual noun is not visible in the evidence.

**Model opinion**

FR-003 'while application state is logged in' is well-supported by E004 ('a 401 when the application state is logged in'). However the 'three role-paired tokens' claim in CON-002 and Assumptions rests on a truncated sentence where the noun ('s') was cut off. The pairing-to-roles is plausibly supported ('The tokens are paired to front-end roles'), but the count 'three' attaches to an unclear noun. This is a low-risk inference that should be flagged.

**Recommended human check**

Read the full ClientApp/README.md to confirm that exactly three tokens (not users/views/roles) are required and that they are role-paired.

**Model proposed SRS change**

In CON-002 and Section 2 Assumptions, soften to: 'Local development requires proxy configuration and a set of role-paired tokens (evidence indicates three items are needed; exact noun obscured by evidence truncation — verify).' Or confirm and keep 'three tokens'.

Optional human revised fix:
> 

**Human decision**

- [✅️] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> 

### R004: non_verifiable

- Severity: `minor`
- Suggested action: `needs_human_check`
- SRS location: NFR-004; DR-001
- Evidence IDs: E005

**Claim or gap**

NFR-004 ('client store usage shall be limited to models where significant benefit is found') and the framing of DR-001 derive from E005 ('Due to time constraints the Ngrx store is established for a limited number of models and only used when significant benefit is found'), which describes a past design decision/rationale rather than an enforceable, testable requirement.

**Model opinion**

This is a descriptive observation of historical scoping ('due to time constraints'), not a prescriptive requirement with an observable acceptance criterion. 'Significant benefit' is subjective and not verifiable by inspection in a repeatable way. Consider re-labeling as a design note/constraint rather than a maintainability NFR, or rewrite with a measurable criterion.

**Recommended human check**

Confirm whether this should be a requirement at all, or recorded as a design rationale/assumption. Determine an observable acceptance criterion if it remains an NFR.

**Model proposed SRS change**

Reclassify NFR-004 as a design note/assumption: 'Design note (E005): NgRx store usage is intentionally limited to a subset of models where significant benefit is identified; universal store adoption was not pursued due to time constraints.' Remove from the verifiable NFR table or add a concrete inspection criterion.

Optional human revised fix:
> 

**Human decision**

- [✅️] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> 可采用模型建议

### R005: missing_requirement

- Severity: `minor`
- Suggested action: `needs_human_check`
- SRS location: Section 3 Software/API interfaces; Section 4 Functional Requirements
- Evidence IDs: E003, E004

**Claim or gap**

E004 lists additional core guards/interceptors not captured as requirements: 'Module Import' guard (alerts a developer to a double-loaded module) and 'Redirect' guard (route to an external URL using a router). E003 also notes the registration service 'contains PDF collect...' which the SRS mentions only in passing under data exchange formats.

**Model opinion**

The SRS captured Landing, Logged In, and Role guards plus Unauthorized and Watchdog interceptors, but omitted the Module Import and Redirect guards described in the same E004 chunk. These are arguably developer-tooling/minor, but for completeness and traceability they should at least be acknowledged. The registration PDF-collection behavior is also under-specified relative to evidence.

**Recommended human check**

Confirm whether Module Import guard, Redirect guard, and registration PDF collection warrant their own requirements or an explicit note that they are intentionally excluded as developer/diagnostic features.

**Model proposed SRS change**

Add to Section 4 (or a note): 'FR-008 (optional): The system shall support a redirect guard to route to an external URL via the router (E004).' and 'Developer diagnostic: a module-import guard alerts developers to double-loaded modules (E004).' Also note registration service includes PDF collection behavior (E003) pending schema verification.

Optional human revised fix:
> 

**Human decision**

- [✅️] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> 可采用模型建议

### R006: architecture_detail

- Severity: `minor`
- Suggested action: `needs_human_check`
- SRS location: Section 2 Product perspective; whole SRS
- Evidence IDs: E001, E006

**Claim or gap**

The repository provides an architecture-diagram.png (ground-truth image URL) that is not referenced or reconciled in the SRS. Key architectural relationships (front-end ↔ API ↔ MS SQL, SiteMinder integration) may be depicted there and could confirm/extend the front-end-only view.

**Model opinion**

The SRS infers the architecture from README fragments (browser front-end, required API, MS SQL DB, SiteMinder). The ground-truth diagram should be checked to validate these relationships and to determine whether additional components (auth, backend services, queues) belong in the product perspective. Currently the diagram is unused evidence.

**Recommended human check**

View architecture-diagram.png and confirm whether the front-end/API/SiteMinder/MS SQL relationships in Section 2 match, and whether additional components should be added or noted as out of scope.

**Model proposed SRS change**

In Section 1 References, add the architecture diagram and in Section 2 Product perspective add: 'The repository architecture diagram (architecture-diagram.png) depicts the broader system context; components beyond the front-end, store, and SQL scripts are noted as dependencies and are out of scope for this evidence-based SRS pending diagram review.'

Optional human revised fix:
> 

**Human decision**

- [ ] Accept
- [ ] Reject
- [x] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> issue来自模型对图片内容的推断

### R007: traceability

- Severity: `minor`
- Suggested action: `probably_ignore`
- SRS location: Section 8 Verification; DR-005 / CON-005
- Evidence IDs: E006

**Claim or gap**

DR-005 combines two distinct E006 behaviors (target-filter variable at top of script AND running within a transaction) into one requirement, and CON-005 (backup precaution) is verification-by-inspection though it is a procedural pre-condition, not an inspectable code property.

**Model opinion**

Both DR-005 and CON-005 are well-evidenced by E006. The minor concern is that DR-005 bundles two verifiable properties (could be split for clean testing) and CON-005 ('backup target database before execution') is an operational procedure whose 'Inspection' verification is weak — it cannot be inspected from the artifact alone. These are low-severity traceability/verifiability refinements.

**Recommended human check**

Decide whether to split DR-005 into two checkable items and whether CON-005 should be re-cast as an operational/procedural pre-condition rather than an inspectable requirement.

**Model proposed SRS change**

Optionally split DR-005 into DR-005a (script includes a top-of-script filter variable) and DR-005b (script executes within a transaction). For CON-005, reword verification as 'Operational procedure check (documentation review)' rather than code Inspection.

Optional human revised fix:
> 

**Human decision**

- [ ] Accept
- [x] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> 该 issue 只是风格偏好，不影响需求质量
