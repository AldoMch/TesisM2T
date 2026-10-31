# Human SRS Review Sheet

## Metadata

- Sample directory: `s000009_ff7318d0`
- Generated SRS: `final_srs.md`
- Evidence pack: `evidence_pack.json`
- Review model: `claude-opus-4-8`
- Generated at: `2026-06-05T15:35:22.041477Z`
- Raw model response: `model_srs_review_raw.md`
- Parse status: `parsed`

## Overall Model Opinion

- Recommendation: `revise`
- Confidence: `0.78`
- Rationale: The SRS is well-traced and conservative for most functional and deployment claims. However, the repository name and README emphasize a 'chatbot' and 'live streaming' capability that the SRS omits, and several requirements (predictions, screenings, reminders) are described with more implementation certainty than the README's high-level prose supports. A few traceability and architecture-diagram checks are needed.

## Overall Human Decision

- [ ] Accept
- [ ] Reject
- [ ] Partial accept

Reason:
> 

## Positive Observations

- API I/O requirements (FR-006, NFR-002, C-004) are accurately and conservatively grounded in code evidence (E003, E004), including JSON defaults and execute-api SigV4 configuration.
- The deployment/technology constraints (C-001 through C-005, NFR-003) faithfully reflect the README technology stack (E005).
- The SRS clearly distinguishes explicit vs. inferred evidence types and provides a traceability matrix with confidence levels, supporting human adjudication.
- Verification methods are reasonable and mapped per requirement in Section 8.

## Candidate Issues

### R001: missing_requirement

- Severity: `major`
- Suggested action: `needs_human_check`
- SRS location: Section 1 Product Scope; Section 4 Functional Requirements
- Evidence IDs: none

**Claim or gap**

The repository name explicitly includes 'chatbot' (foot365-live-streaming-chatbot-prediction-app), but the SRS never mentions any chatbot/conversational feature.

**Model opinion**

A chatbot is named prominently in the repository identity. If the repo implements a chatbot (e.g., Lex/Lambda), it is a significant functional capability missing from the SRS. The provided evidence pack does not contain a chatbot chunk, so this needs verification rather than assertion.

**Recommended human check**

Search the repository for a chatbot implementation (e.g., Amazon Lex, dialogflow, chat UI, or Lambda intents). Confirm whether a chatbot feature exists and should be a functional requirement.

**Model proposed SRS change**

If verified, add FR-009: 'The system shall provide a chatbot/conversational interface for football information queries.' and update Section 1 Product Scope to mention the chatbot capability. If not implemented, add a scope note explaining the repository name references a planned-but-unimplemented chatbot.

Optional human revised fix:
> 

**Human decision**

- [ ] Accept
- [ ] Reject
- [x] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> 除了仓库名字，没有证据表明当前方法还有chatbot功能。证据不足，不接受

### R002: missing_requirement

- Severity: `major`
- Suggested action: `needs_human_check`
- SRS location: Section 1 Product Scope; Section 4 Functional Requirements
- Evidence IDs: E005

**Claim or gap**

The repository name includes 'live-streaming' and README mentions 'live match screenings', but the SRS treats live score updates (Kafka/Avro) and screening recommendations separately and never addresses live streaming as a distinct capability.

**Model opinion**

'Live streaming' in the repo name may refer to the Kafka live-score pipeline rather than video streaming, but the distinction is ambiguous. The SRS should clarify what 'live streaming' means here to avoid scope misrepresentation.

**Recommended human check**

Verify whether 'live streaming' refers to the Kafka live-score update pipeline (E005) or an actual video/streaming feature. Inspect README full text and architecture diagram.

**Model proposed SRS change**

Add a clarifying note to Section 1 Product Scope: 'The term "live streaming" in the project name refers to the real-time live-score update pipeline (Kafka/Apache Avro on EC2), not video streaming.' Adjust if verification shows otherwise.

Optional human revised fix:
> 建议改为证据限定表述：当前证据仅支持 live score update pipeline（Kafka/Apache Avro on EC2）和 live match screening recommendations；未提供视频流媒体功能证据。

**Human decision**

- [✅️] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> Issue 成立。E005 明确支持 Kafka/Avro live score update，E001 支持 live match screenings；但 SRS 没有解释仓库名中 live-streaming 与这两类能力的关系，容易被误读为视频流。应添加证据限定的范围说明。

### R003: unsupported_claim

- Severity: `minor`
- Suggested action: `needs_human_check`
- SRS location: Section 2 Product Functions Summary; FR-002; FR-005; FR-003; FR-004
- Evidence IDs: E001, E005

**Claim or gap**

FR-002 (predictions presented to user), FR-003 (screening recommendations), FR-004 (schedule management/reminders), and FR-005 (email/SMS reminders) are stated as implemented system behaviors, but evidence is only high-level README aspirational prose ('We aim to serve...', 'We manage their teams' schedule').

**Model opinion**

The README phrasing is goal-oriented ('We aim to', 'provide them reminders', 'suggest recommendations') and may describe intended rather than fully implemented behavior. The SRS converts these into firm 'shall' requirements. This is acceptable for a requirements doc but the confidence/traceability should reflect that these come from problem-statement prose, not code.

**Recommended human check**

Confirm whether code exists implementing predictions display, screening recommendations, schedule management, and SMS/email reminder delivery (SNS/SQS Lambda handlers). Adjust confidence in the traceability matrix accordingly.

**Model proposed SRS change**

In Section 9 Traceability Matrix, lower confidence for FR-003 and FR-004 to reflect problem-statement-only sourcing, and add a note that these requirements derive from README objectives rather than verified implementation.

Optional human revised fix:
> 

**Human decision**

- [ ] Accept
- [ ] Reject
- [✅️] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> FR-002 的 ML prediction 还有 E002/E006 中 SageMaker 预测说明支持，不应该被标明是证据来源于README 中的高层目标性文字
### R004: architecture_detail

- Severity: `minor`
- Suggested action: `needs_human_check`
- SRS location: Section 2 Operating Environment; FR-008; C-005
- Evidence IDs: E005

**Claim or gap**

The SRS asserts the Kafka/Avro live-score pipeline runs on EC2 and describes the full AWS service interplay, but the architecture diagram (architecture.jpg) was not provided as analyzable evidence.

**Model opinion**

The EC2/Kafka claim is supported by E005 text. However, the data-flow relationships (e.g., how SQS/SNS, Lambda, SageMaker, and DynamoDB/Elasticsearch interconnect) are inferred from a service list, not a verified diagram. The ground-truth architecture diagram should be checked to confirm component relationships.

**Recommended human check**

Open Snapshots/architecture.jpg and verify the described component relationships and data flow match the SRS Operating Environment and FR-008 descriptions.

**Model proposed SRS change**

No text change required if the diagram confirms relationships; otherwise add a note in Section 2 distinguishing verified components from inferred data-flow relationships pending diagram confirmation.

Optional human revised fix:
> 

**Human decision**

- [✅️] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
>  EC2/Kafka/Avro 本身由 E005 明确支持；但服务间关系和数据流需要架构图确认。

### R005: traceability

- Severity: `minor`
- Suggested action: `accept_as_issue`
- SRS location: Assumptions and Dependencies (prediction final-week assumption)
- Evidence IDs: E005

**Claim or gap**

The assumption 'Match prediction depends on data from matches already played in the current season except the final week' is cited to E005, but E005's text is the final-week prediction assumption fragment ('Our predictions for the final week of season assumes that all the matches played in the current season barring the last week are considered'). The wording in the SRS slightly reframes this.

**Model opinion**

The citation is correct, but the SRS rephrasing ('depends on data ... except the final week') is a near-inversion of the source ('predictions for the final week assume all matches barring the last week are considered'). This could mislead readers about which week is predicted vs. excluded.

**Recommended human check**

Re-read the E005 sentence and confirm the SRS paraphrase preserves the intended meaning (final-week prediction uses all-but-last-week data).

**Model proposed SRS change**

Revise Assumptions and Dependencies bullet to: 'Final-week season predictions assume that all matches played in the current season except the last week are used as input data. (E005)'

Optional human revised fix:
> 明确是“final-week predictions”使用“除最后一周外的本赛季已赛比赛”作为输入

**Human decision**

- [✅️] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> 可采取模型建议，SRS 引用的证据正确。

### R006: non_verifiable

- Severity: `minor`
- Suggested action: `probably_ignore`
- SRS location: NFR-004
- Evidence IDs: E002, E006

**Claim or gap**

NFR-004 (scalability via DynamoDB/Elasticsearch) is explicitly labeled inferred and has no measurable acceptance criterion (no throughput, latency, or data-volume target).

**Model opinion**

The SRS appropriately flags this as inferred, which is good. However, as written it remains non-verifiable beyond an architecture review. This is acceptable given evidence limits but should be acknowledged as not testable to a service level.

**Recommended human check**

Confirm no performance/scale targets exist in the repository. If none, keep NFR-004 as architecture-review-only.

**Model proposed SRS change**

Append to NFR-004 acceptance basis: 'No quantitative scale target is defined in repository evidence; verification is limited to confirming the use of DynamoDB and Elasticsearch.'

Optional human revised fix:
> 

**Human decision**

- [✅️] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> Issue 成立。SRS 已降低为 inferred，但验收依据仍缺少明确的可观察标准。
