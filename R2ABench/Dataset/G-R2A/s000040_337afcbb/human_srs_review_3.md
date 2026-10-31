# Human SRS Review Sheet

## Metadata

- Sample directory: `s000040_337afcbb`
- Generated SRS: `final_srs.md`
- Evidence pack: `evidence_pack.json`
- Review model: `claude-opus-4-8`
- Generated at: `2026-06-05T15:47:09.933033Z`
- Raw model response: `model_srs_review_raw.md`
- Parse status: `parsed`

## Overall Model Opinion

- Recommendation: `revise`
- Confidence: `0.74`
- Rationale: The SRS is well-traced to the six evidence chunks and mostly conservative. However, several mail-processing details (DR-003 token format, DR-005 hash substring, FR-006 logic) are stated more precisely than the truncated evidence supports, and the architecture_overview.png diagram is never reconciled with the SRS architecture. The Proxy API and isolation claims (FR-003) rest on marketing-style README text and should be flagged. A few requirements are non-verifiable as written.

## Overall Human Decision

- [ ] Accept
- [ ] Reject
- [ ] Partial accept

Reason:
> 

## Positive Observations

- Every functional, non-functional, data, and constraint requirement carries explicit evidence IDs and a traceability matrix, which is strong practice.
- The SRS is appropriately conservative in flagging that UI layouts and interaction patterns are not defined in the evidence (Section 3.1).
- Mail-processing requirements (FR-005/FR-006) correctly capture the observable success/delete and reject/discard behaviors visible in the code evidence.
- Verification methods and acceptance criteria are provided per requirement, improving testability for most items.

## Candidate Issues

### R001: architecture_detail

- Severity: `major`
- Suggested action: `needs_human_check`
- SRS location: Section 2.1 Product perspective; Section 3 External Interfaces
- Evidence IDs: E003, E004

**Claim or gap**

The ground-truth architecture diagram (architecture_overview.png) is never referenced or reconciled. The SRS describes a Proxy API, services, database, and mail intake but provides no architectural overview of how these components connect.

**Model opinion**

The repository advertises an architecture_overview.png. The SRS captures discrete interfaces but omits the overall component topology (e.g., how Proxy sits between services and clients). This is a meaningful architecture gap that should be checked against the diagram.

**Recommended human check**

Open architecture_overview.png and verify whether the Proxy API / service / client / database relationships described in Sections 2.1 and 3 match the diagram; add a component overview if the diagram reveals undocumented components.

**Model proposed SRS change**

Add to Section 2.1 a short architecture overview paragraph reconciled with architecture_overview.png, e.g., 'PlugIt comprises a Proxy that mediates between end-user clients and one or more PlugIt services; services expose their API via the Proxy and maintain isolated data stores.' Mark as conditional pending diagram verification.

Optional human revised fix:
> 

**Human decision**

- [×] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> SRS 未引用架构图/拓扑

### R002: unsupported_claim

- Severity: `major`
- Suggested action: `needs_human_check`
- SRS location: FR-003; Section 2.2; Section 3.1
- Evidence IDs: E004

**Claim or gap**

FR-003 asserts the system 'shall support combining multiple micro-services into a single experience and user interface while maintaining data and process isolation' as a verifiable functional requirement, but evidence E004 is README marketing prose, not a specification of implemented behavior.

**Model opinion**

The isolation and 'single experience' claims derive solely from promotional README language and the README explicitly labels the project a 'draft'. Treating this as a Demonstration-verifiable functional requirement overstates evidentiary support; the actual mechanism for isolation is not shown in evidence.

**Recommended human check**

Confirm whether code/evidence beyond the README demonstrates an actual isolation/unified-experience mechanism; otherwise reclassify FR-003 as a product objective rather than a testable functional requirement.

**Model proposed SRS change**

Reword FR-003 to a product goal: 'PlugIt is intended to combine multiple micro-services behind a single user experience while preserving data/process isolation (stated product objective per README draft; underlying mechanism not specified in evidence).' Lower confidence and remove the Demonstration acceptance criterion or mark it conditional.

Optional human revised fix:
> 把 FR-003 改成 product objective / architecture goal

**Human decision**

- [×] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> “single UX + isolation” 来自 README 目标性描述，且 README 标注 draft；不应写成强 Demonstration FR

### R003: non_verifiable

- Severity: `major`
- Suggested action: `needs_human_check`
- SRS location: FR-004; Section 3.2
- Evidence IDs: E003

**Claim or gap**

FR-004 states the system 'shall provide programmatic access to the PlugIt API,' but evidence E003 only shows a `PlugItAPI.__init__(self, url)` constructor; no actual API operations are present in the evidence.

**Model opinion**

The evidence supports only that a PlugItAPI class exists and is initialized with a URL. The breadth implied by 'programmatic access to the PlugIt API' is not demonstrated. The acceptance criterion ('initialized API access instance') is verifiable but trivial and understates/overstates the real interface.

**Recommended human check**

Inspect plugit/api.py beyond the truncated chunk to enumerate actual API methods; either narrow FR-004 to instance creation or expand it with the real operations.

**Model proposed SRS change**

Narrow FR-004 to evidenced behavior: 'The system shall provide a PlugItAPI client class that is instantiated with the main endpoint URL.' If additional methods are confirmed, add them explicitly with evidence IDs.

Optional human revised fix:
> 

**Human decision**

- [ ] Accept
- [ ] Reject
- [x] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> 完整 plugit/api.py 不只有 constructor，还有 _request、user、orga、members、mail、forum 等方法

### R004: ambiguity

- Severity: `minor`
- Suggested action: `accept_as_issue`
- SRS location: DR-005; FR-006
- Evidence IDs: E006

**Claim or gap**

DR-005 states 'derive an expected hash using sha512(data + secret) and compare a substring of that digest.' Evidence E006 shows the specific substring `[30:42]` of the hex digest, which the SRS abstracts away.

**Model opinion**

The substring bounds [30:42] are a concrete, testable detail present in the evidence; abstracting to 'a substring' makes the data requirement harder to verify precisely. Minor but easily fixed.

**Recommended human check**

Confirm the hex digest substring slice [30:42] in check_mail.py and include it for precise verifiability.

**Model proposed SRS change**

Amend DR-005 to: 'The system shall derive an expected hash as sha512(data + EBUIO_MAIL_SECRET_HASH).hexdigest()[30:42] and compare it against the received hash before processing.'

Optional human revised fix:
> 

**Human decision**

- [×] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> sha512(...).hexdigest()[30:42] 是明确可测试细节

### R005: missing_requirement

- Severity: `minor`
- Suggested action: `accept_as_issue`
- SRS location: FR-006; DR-003
- Evidence IDs: E006

**Claim or gap**

Evidence E006 enumerates multiple specific auto-response indicators (x-auto-response-suppress, Auto-Submitted, Auto-Autorespond, auto-submitted, precedence/x-precedence in ['auto_reply','bluk','junk']). The SRS generically says 'identify auto-response indicators' without listing the observable conditions.

**Model opinion**

The detection rule is a concrete, testable set of header checks. Summarizing it as 'auto-response indicators' reduces verifiability of FR-006/NFR-004. Listing the conditions strengthens the test acceptance criteria.

**Recommended human check**

Verify the full list of auto-response header conditions in check_mail.py and ensure FR-006 acceptance criteria reference them.

**Model proposed SRS change**

Extend FR-006 system behavior/acceptance to enumerate the detected headers: messages are dropped if any of x-auto-response-suppress, Auto-Submitted != 'no', Auto-Autorespond, auto-submitted, precedence/x-precedence in {auto_reply, bluk, junk} are present.

Optional human revised fix:
> FR-006 / acceptance 列出具体 header 条件

**Human decision**

- [×] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> auto-response header 条件是明确规则，SRS 太泛

### R006: scope

- Severity: `minor`
- Suggested action: `accept_as_issue`
- SRS location: Section 1.2; Section 4 (FR-005/FR-006)
- Evidence IDs: E005, E006

**Claim or gap**

Mail processing (FR-005, FR-006, DR-003-005) is drawn from a file under examples/standalone_proxy/.../check_mail.py, i.e., example/demo code, but is presented in core functional requirements without clearly marking it as example/optional scope.

**Model opinion**

The evidence path indicates this is example code, not core framework functionality. Presenting it among first-class FRs may overstate that mail handling is a core product capability. The SRS does call it 'example' in prose but the FR table does not preserve that qualifier.

**Recommended human check**

Confirm whether mail handling is part of the core PlugIt framework or only the standalone_proxy example, and scope FR-005/FR-006 accordingly.

**Model proposed SRS change**

Annotate FR-005 and FR-006 as '(example/standalone_proxy scope)' and note in Section 1.2 that mail-driven processing is provided as an example workflow rather than core framework functionality.

Optional human revised fix:
> 

**Human decision**

- [×] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> mail processing 来自 examples/standalone_proxy，应标明 example scope

### R007: traceability

- Severity: `minor`
- Suggested action: `accept_as_issue`
- SRS location: Section 1.4 References; E001/E002
- Evidence IDs: E001, E002

**Claim or gap**

E001 and E002 are both cited to the same file (docs/new-plugit-service.md) but as distinct evidence IDs. The distinction between them is not explained, which weakens traceability precision.

**Model opinion**

Using two evidence IDs for one document is acceptable if they reference different chunks, but the SRS does not indicate which section each covers, making it harder to audit specific claims (e.g., Alembic vs config settings).

**Recommended human check**

Confirm E001 corresponds to the database/Alembic chunk and E002 to the config.py/settings chunk, and annotate the reference list accordingly.

**Model proposed SRS change**

In Section 1.4, distinguish: '[E001] docs/new-plugit-service.md (database/Alembic setup section)' and '[E002] docs/new-plugit-service.md (config.py/settings section)'.

Optional human revised fix:
> 

**Human decision**

- [×] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> E001/E002 同文件不同 chunk，Reference 未区分具体章节

### R008: non_verifiable

- Severity: `minor`
- Suggested action: `probably_ignore`
- SRS location: C-004; NFR section
- Evidence IDs: E004

**Claim or gap**

C-004 ('adopters should treat maturity as limited') is an advisory note, not a verifiable constraint, and 'limited maturity' is subjective.

**Model opinion**

The README draft disclaimer is real (E004), but as a constraint it is non-verifiable. It is better framed as an assumption/note than a constraint with no acceptance criterion.

**Recommended human check**

Decide whether to keep the draft-status disclaimer as a note under Assumptions rather than as a Constraint.

**Model proposed SRS change**

Move C-004 to Section 2.5 Assumptions: 'The README labels the protocol and implementation a draft; adopters should expect instability/issues.' Remove it from the Constraints table where it implies a testable constraint.

Optional human revised fix:
> 

**Human decision**

- [×] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> draft-status 是真实信息，但不适合放 Constraint 表