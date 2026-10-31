# Human SRS Review Sheet

## Metadata

- Sample directory: `s000032_0a49a326`
- Generated SRS: `final_srs.md`
- Evidence pack: `evidence_pack.json`
- Review model: `claude-opus-4-8`
- Generated at: `2026-06-05T15:42:15.436589Z`
- Raw model response: `model_srs_review_raw.md`
- Parse status: `parsed`

## Overall Model Opinion

- Recommendation: `revise`
- Confidence: `0.74`
- Rationale: The SRS is generally well-traced and conservative, but it overstates the repository's nature by framing a documentation/example guide as a testable 'system,' attaches NFR-004 (Spring version alignment) to repository artifacts that are not actually in this guide repo, and includes a few claims (e.g., FR-006 human-actor process executability, NFR-002 performance improvement) that go slightly beyond what the evidence verifiably supports. Several issues need human verification but none are fatal.

## Overall Human Decision

- [ ] Accept
- [ ] Reject
- [ ] Partial accept

Reason:
> 

## Positive Observations

- Strong, explicit traceability: every FR/NFR/DR/Constraint maps to a specific evidence ID, and the traceability matrix labels evidence type and confidence.
- Conservative handling of the performance claim (NFR-002 explicitly noted as not quantitatively bounded) and of UI scope (Section 3.1 correctly states no GUI is evidenced).
- Role-based access requirement (FR-005/C-002) is precisely grounded in E003 including the exact ROLE_ACTIVITI_USER authority.
- Token expiration behavior (FR-001/NFR-001/DR-001) is well-supported by the explicit E001 statement about time-sensitive, auto-invalidated tokens.

## Candidate Issues

### R001: scope

- Severity: `major`
- Suggested action: `needs_human_check`
- SRS location: Section 1.2, 2.1, and Functional Requirements (FR-001..FR-007)
- Evidence IDs: E001, E002, E003, E004, E005, E006

**Claim or gap**

The SRS treats a developer documentation/tutorial repository as a deliverable software 'system' that 'shall' enforce behaviors (e.g., require tokens, restrict roles, route ingress). The repository is a guide describing Activiti behavior, not the implementation of that behavior.

**Model opinion**

The evidence (E001-E006) is documentation: readme, tutorial_guide, release_notes, deployment_config. The behaviors described belong to Activiti Cloud / Keycloak / Kubernetes, not to this repo. Phrasing requirements as 'The system shall...' risks attributing platform behavior to the guide repository and inflates scope. This is a recurring framing issue rather than a single-line error.

**Recommended human check**

Confirm whether the SRS is intended to specify the documented Activiti platform behavior (as demonstrated by the guide) or the guide content itself, and decide which subject the 'shall' statements bind to.

**Model proposed SRS change**

Add a scoping sentence in Section 1.2: 'The requirements below describe the platform behaviors and deployment patterns that the guide documents and demonstrates; they are not commitments implemented by this documentation repository.' Optionally reword FR statements to 'The documented platform shall...' to disambiguate subject.

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
- SRS location: NFR-004, C-004, Section 2.4 (Spring Boot 2.0.0.RELEASE / Spring Cloud Finchley.M9)
- Evidence IDs: E006

**Claim or gap**

NFR-004 states 'Repository artifacts shall remain aligned with Spring Boot 2.0.0.RELEASE and Spring Cloud Finchley.M9.' E006 is a release note stating that Activiti project artifacts (across other repositories) were aligned, not the developer-guide repository's artifacts.

**Model opinion**

E006 says 'we aligned our artifacts with Spring Boot 2.0.0.RELEASE and Spring Cloud Finchley.M9' referring to Activiti projects generally. The developer-guide repo is documentation and likely has no such build artifacts. Phrasing it as a requirement on 'repository artifacts' is an unsupported attribution. Also 'shall remain aligned' is a forward-looking constraint not stated in the evidence (which is a past, release-specific note).

**Recommended human check**

Check whether the developer-guide repository contains POM/build artifacts pinned to these versions, or whether E006 only describes other Activiti repos. Verify the 'remain aligned' (ongoing) framing against the point-in-time release note.

**Model proposed SRS change**

Revise NFR-004 to: 'As of release 7.0.0-EA-201802, Activiti project artifacts were aligned with Spring Boot 2.0.0.RELEASE and Spring Cloud Finchley.M9 (release-stated, point-in-time).' Adjust C-004 similarly and remove the 'remain aligned' ongoing obligation unless build evidence is found.

Optional human revised fix:
> 

**Human decision**

- [ ] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> 

### R003: non_verifiable

- Severity: `minor`
- Suggested action: `accept_as_issue`
- SRS location: NFR-002
- Evidence IDs: E005

**Claim or gap**

NFR-002 ('Cloud connector transaction handling shall support improved performance relative to prior behavior') is acknowledged as not quantitatively bounded, making it non-verifiable as a requirement.

**Model opinion**

E005 states connector transaction management was improved to improve performance, but no baseline, metric, or threshold exists. The SRS already flags this, but as written it remains a 'shall' requirement with an Analysis verification that only confirms the release claim, not measurable behavior. Better to demote to a release note / informative statement.

**Recommended human check**

Decide whether to keep NFR-002 as a requirement or reclassify it as an informational release observation given the absence of measurable criteria.

**Model proposed SRS change**

Reclassify NFR-002 as informational: 'Release note (E005): cloud connector transaction handling was changed with the stated intent of improving performance. No quantitative target is specified; this is recorded for traceability, not as a verifiable requirement.'

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
- SRS location: FR-006 / Section 3.2 ProcessRuntime API row
- Evidence IDs: E002

**Claim or gap**

FR-006 claims the system 'shall support process examples that combine ProcessRuntime and TaskRuntime APIs for processes involving a human actor' citing E002, but E002 only states such a full example exists in the 'activiti-api-basic-full-example' maven module; it does not establish executability as a requirement.

**Model opinion**

E002 is descriptive ('You can find an example using both... the process relies on a Human Actor'). Mapping this to a 'shall support' functional requirement with a Demonstration acceptance ('the documented full example executes') overstates what the chunk verifies—the chunk does not assert successful execution, only existence of the example.

**Recommended human check**

Confirm whether the full-example maven module's executability is something this guide repo verifies, or only references. Adjust verification method accordingly.

**Model proposed SRS change**

Soften FR-006 to: 'The guide shall document an example (activiti-api-basic-full-example) combining ProcessRuntime and TaskRuntime APIs for a process involving a human actor.' Change acceptance criterion to 'The documented example referencing both APIs and a human actor is present.'

Optional human revised fix:
> 

**Human decision**

- [ ] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> 

### R005: architecture_detail

- Severity: `minor`
- Suggested action: `needs_human_check`
- SRS location: Section 2 / Operating environment (cloud architecture)
- Evidence IDs: E001, E004

**Claim or gap**

The repository includes a ground-truth architecture diagram (activiti-cloud-architecture.png) describing the Activiti Cloud component topology (runtime bundle, query/audit services, gateway, identity), but the SRS does not reference or reconcile any architectural overview against it.

**Model opinion**

The evidence pack references a ground-truth image of the cloud architecture. The SRS enumerates components piecemeal (Keycloak, runtime bundle, audit, ingress) but does not present an architectural view or cite the diagram. A brief architecture subsection cross-checked to the diagram would strengthen completeness and catch missing components (e.g., query service, gateway).

**Recommended human check**

Open .gitbook/assets/activiti-cloud-architecture.png and verify whether SRS-mentioned components match, and whether components (gateway, query service, identity management) are missing.

**Model proposed SRS change**

Add Section 2.6 'Architectural context' citing the activiti-cloud-architecture diagram and listing the documented components (runtime bundle, audit service, query/gateway, Keycloak identity, ingress), marking any not covered by retrieved evidence as out of current scope.

Optional human revised fix:
> 

**Human decision**

- [ ] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> 

### R006: ambiguity

- Severity: `minor`
- Suggested action: `needs_human_check`
- SRS location: FR-004 / NFR / Verification rows for FR-004
- Evidence IDs: E001

**Claim or gap**

E001 is truncated ('You can check that the audit service contains the events associat...') and FR-004/DR-004 assert audit events 'associated with the relevant process instance/activity' without the evidence fully specifying which events or association semantics.

**Model opinion**

The audit claim is reasonable but rests on a truncated sentence. The association ('events associated with process activity') is underspecified—what event types, what scope. Acceptance criterion 'shows events associated with the executed process activity' is loose. Low risk because the example is demonstrative.

**Recommended human check**

Read the full README section to confirm what audit events are demonstrated (e.g., process started, task created) and tighten FR-004 accordingly.

**Model proposed SRS change**

Once full text is reviewed, qualify FR-004 to enumerate the demonstrated audit event types (e.g., 'process instance started' events) rather than the generic 'events associated with process activity.'

Optional human revised fix:
> 

**Human decision**

- [ ] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
>
