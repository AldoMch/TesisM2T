# Human SRS Review Sheet

## Metadata

- Sample directory: `s000060_935731a2`
- Generated SRS: `final_srs.md`
- Evidence pack: `evidence_pack.json`
- Review model: `claude-opus-4-8`
- Generated at: `2026-06-05T15:56:42.873547Z`
- Raw model response: `model_srs_review_raw.md`
- Parse status: `parsed`

## Overall Model Opinion

- Recommendation: `revise`
- Confidence: `0.7`
- Rationale: The SRS is well-structured and most functional requirements trace cleanly to test evidence. However, several claims (Kafka/messaging publication, deserialization 'compatibility' as a payload guarantee, UPDATED-only event types, JVM/Kotlin operating environment) are partially inferred or overstated relative to the truncated evidence, and FR-003/inclusion-filter semantics are stated more precisely than the evidence demonstrates. The architecture diagram referenced in the candidate is not reflected in any architecture detail in the SRS.

## Overall Human Decision

- [ ] Accept
- [ ] Reject
- [x] Partial accept

Reason:
> R003/R004 接受，R002 部分接受（图引用接受、Kafka 传输暂缓），R001 需讨论（查 EventType 枚举），R005/R006 拒绝（JVM 已标 inferred；NFR-001 已限定范围）。

## Positive Observations

- Functional requirements FR-001/FR-002 are tightly and correctly traced to concrete test assertions (EventType.UPDATED, element name/updatedValue/previousValue/metadata.fqdn, overridden applicationName).
- The SRS appropriately distinguishes Explicit vs Inferred confidence and avoids fabricating UI or deployment claims where evidence is absent.
- Data requirements DR-003/DR-004 accurately reflect AuditorEventConfig fields and the example Item domain models, including UUID/map/list/nested structures.
- Scope constraints (C-001..C-003) sensibly bound the product as a Kotlin client library dependent on external publisher/logger implementations, consistent with E003.

## Candidate Issues

### R001: unsupported_claim

- Severity: `major`
- Suggested action: `needs_human_check`
- SRS location: FR-001 / DR-002 / Section 8 FR-001 acceptance
- Evidence IDs: E002

**Claim or gap**

FR-001 states the system creates an AuditEvent with event type UPDATED, implying UPDATED is the only/representative event type. Evidence only shows one test asserting type == UPDATED for an integer change.

**Model opinion**

EventType is clearly an enum (EventType.UPDATED), strongly implying other types (e.g., CREATED/DELETED) exist. The SRS does not claim exclusivity, but a reader may infer UPDATED is the only behavior. The single piece of evidence supports UPDATED only; other types are unverified. This is acceptable as scoped but should be flagged so a human confirms whether the auditor also emits CREATED/DELETED events that are missing from the SRS.

**Recommended human check**

Inspect EventType enum and Auditor.kt logic in the repo to confirm whether CREATED/DELETED (or similar) event types exist and should be documented as additional functional requirements.

**Model proposed SRS change**

Add a note under FR-001: 'Evidence demonstrates the UPDATED event type only; other EventType values (if present in the EventType enum) are not covered by this SRS and should be added as separate requirements after verification.' If additional types are confirmed, add FR-001a/FR-001b for those types.

Optional human revised fix:
> 暂不新增 FR-001a/b（会引入 unsupported claim）。可选地在 FR-001 加一句"证据仅覆盖 UPDATED"。需查 EventType 枚举与 Auditor.kt 确认是否真有 CREATED/DELETED 后再决定补需求。

**Human decision**

- [ ] Accept
- [ ] Reject
- [x] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> E002 只断言 type==EventType.UPDATED。"枚举→强烈暗示存在 CREATED/DELETED"属规则告诫的"strongly imply"，无直接证据，不能据此 ACCEPT 新增需求。SRS 现状只记 UPDATED、未声称排他，问题不严重。

### R002: architecture_detail

- Severity: `major`
- Suggested action: `needs_human_check`
- SRS location: Section 3 Communication Interfaces / FR-004 / Section 2 Product Perspective
- Evidence IDs: E001, E002, E003

**Claim or gap**

The SRS describes 'serialized event messages' and a generic EventPublisher but does not identify the messaging transport (e.g., Kafka) suggested by StepVerifier/consumer patterns and the referenced architecture diagram.

**Model opinion**

The evidence uses reactive consumer/StepVerifier semantics and a serialized message value (it.value()), which is consistent with a Kafka/streaming transport, and there is a ground-truth architecture diagram (auditor-v1-architecture.png) referenced in the candidate metadata. The SRS keeps the transport abstract, which is conservative and defensible, but it omits any reference to the architecture diagram. A human should confirm whether a concrete transport (Kafka/Reactor) is a documented design constraint worth capturing.

**Recommended human check**

Open docs/auditor-v1-architecture.png and AuditEventProducerConfig/AuditEventModule to determine if Kafka or a specific reactive messaging system is the intended publishing transport, and whether it should be recorded as an architecture constraint.

**Model proposed SRS change**

Add to Section 2 Product Perspective or C-002: 'The reference architecture (docs/auditor-v1-architecture.png) and producer configuration may specify a concrete transport (e.g., Kafka). If confirmed, document the transport as an architecture constraint; otherwise retain the abstract EventPublisher description.'

Optional human revised fix:
> 接受"加图引用"：第 2 节/C-002 引用 docs/auditor-v1-architecture.png。拒绝写死 Kafka：6 块证据未明确传输，需开图并查 AuditEventProducerConfig/AuditEventModule 确认后再作为架构约束；否则维持抽象 EventPublisher。

**Human decision**

- [ ] Accept
- [ ] Reject
- [x] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> selected_candidates.csv 确认 auditor-v1-architecture.png 存在(cached)，SRS 无图引用 → 真实缺口（接受补引用）；但"传输=Kafka"仅由 StepVerifier/it.value() 暗示，证据不足，SRS 保持抽象是正确的（暂缓）。

### R003: non_verifiable

- Severity: `minor`
- Suggested action: `needs_human_check`
- SRS location: NFR-002 / Section 8 NFR-002
- Evidence IDs: E001, E002

**Claim or gap**

NFR-002 states the payload 'shall be compatible with deserialization into the AuditEvent data structure.' This is a restatement of a test mechanism rather than an independently verifiable quality attribute.

**Model opinion**

The evidence shows tests deserialize message values into AuditEvent. Phrasing this as a non-functional requirement is borderline; it is verifiable via the existing test, so it is not strictly non-verifiable, but it reads more like a data/interface contract than an NFR. Consider relocating to Data Requirements or tightening to an interface requirement to avoid ambiguity about what 'compatible' means.

**Recommended human check**

Decide whether payload/AuditEvent deserialization is better expressed as a data contract (DR) or interface requirement rather than an NFR; confirm the serialization format (JSON via objectMapper).

**Model proposed SRS change**

Reword NFR-002 to: 'The published event payload shall serialize to a format (JSON via the configured ObjectMapper, per tests) that deserializes without error into the AuditEvent structure.' Alternatively move this to DR-001 as an explicit data contract.

Optional human revised fix:
> 

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> NFR-002"compatible with deserialization"措辞含糊，但 E001 实有 objectMapper.readValue(it.value(), AuditEvent::class.java)，可据此把"compatible"收紧为可验证、有据的表述。

### R004: ambiguity

- Severity: `minor`
- Suggested action: `needs_human_check`
- SRS location: FR-003 / DR-003 / C-003
- Evidence IDs: E001, E002

**Claim or gap**

FR-003 asserts the system restricts content to elements matching the includes list, but the evidence (E001) shows the filter configuration (enabled, types=['InclusionFilter'], includes=[...]) without an assertion isolating the include-filtered output.

**Model opinion**

E001 shows the AuditorEventConfig with an inclusion filter set, and E002 shows a single-element result, but the truncated text does not clearly show that filtering reduced a multi-element candidate set to only the included element. The behavioral claim 'containing only included elements' is plausible but not fully demonstrated in the provided chunk. Mark for verification against the full test assertions.

**Recommended human check**

Review the full AuditorTest.kt assertion that exercises the inclusion filter to confirm that non-included elements are excluded from the emitted AuditEvent.

**Model proposed SRS change**

Soften FR-003 System Behavior to: 'The system shall apply the configured element inclusion filter so that emitted elements are constrained to the configured includes list (to be confirmed against the inclusion-filter test assertion).' Restore the strong wording once the assertion is verified.

Optional human revised fix:
> 

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> E001 有 InclusionFilter 配置(enabled/types/includes)，E002 结果只含一个 element，但截断文本未断言"非 includes 元素被排除"，FR-003"containing only included elements"略强于已证内容，宜软化。

### R005: traceability

- Severity: `minor`
- Suggested action: `probably_ignore`
- SRS location: Operating Environment / C-001
- Evidence IDs: E003, E005, E006

**Claim or gap**

JVM operating environment is labeled 'inferred' but cited as if evidence-backed; E003/E005/E006 confirm Kotlin source but do not explicitly state JVM target or supported runtime/build tooling.

**Model opinion**

The Kotlin + java.util.UUID imports reasonably imply JVM, and the SRS correctly tags it as inferred. This is low risk. However, no evidence pins a Kotlin/JVM version or build system, so any future version-specific requirement would be unsupported. The current wording is acceptable but should remain explicitly inferred.

**Recommended human check**

Confirm build.gradle/Kotlin version and target JVM in the repository if any runtime/version requirement is needed; otherwise leave as inferred.

**Model proposed SRS change**

No change required if left explicitly inferred. Optional: append '(no specific JVM/Kotlin version evidenced)' to the Operating Environment note.

Optional human revised fix:
> 不采用（无需改动）。可选追加"(无具体 JVM/Kotlin 版本证据)"。

**Human decision**

- [ ] Accept
- [x] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> Operating Environment 已明确标"Evidence type: inferred for JVM environment"；E005/E006 import java.util.UUID，JVM 推断合理且已正确标 inferred，无缺陷；模型亦自标 probably_ignore。

### R006: unsupported_claim

- Severity: `minor`
- Suggested action: `probably_ignore`
- SRS location: NFR-001
- Evidence IDs: E001, E002

**Claim or gap**

NFR-001 generalizes 'exactly one matching audit event and no additional event' from a single test using expectNoEvent(noEventDuration), presenting it as a system-wide non-functional guarantee.

**Model opinion**

The evidence (E002) shows expectNextMatches followed by expectNoEvent for one tested scenario. The SRS carefully scopes this to 'a single audited update operation verified in the functional tests,' which is appropriate. The risk is that NFR-001 reads like a general one-event-per-operation guarantee. Keep scoped phrasing; flag for human to confirm whether single-event-per-change is a genuine system invariant or just a per-test observation.

**Recommended human check**

Determine whether one-event-per-change is an intended system invariant (design) or merely an observed test outcome; adjust NFR-001 scope accordingly.

**Model proposed SRS change**

Retain current scoped wording. If one-event-per-change is confirmed as a design invariant, broaden NFR-001 and re-tag confidence as Explicit; otherwise keep it test-scoped.

Optional human revised fix:
> 不采用（无需改动）。

**Human decision**

- [ ] Accept
- [x] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> NFR-001 本就限定"For a single audited update operation verified in the functional tests... during the observed no-event verification interval"，与 E002 的 expectNextMatches(...).expectNoEvent(noEventDuration) 完全吻合，未过度泛化为系统级保证，无缺陷。
