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
- [x] Partial accept

Reason:
> 代码类需求（FR-006/NFR-002/C-004）扎实，整体可接受但需修订。R005（预测假设被改写近反义）、R006（NFR-004 不可验证）为成立的 minor 需修；R003（愿景文案转硬性需求）部分接受、降置信；R001（chatbot）、R002（live-streaming 语义）、R004（架构数据流）因证据不在包内需讨论。

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
> 证据不足，需讨论。evidence pack 中没有任何 chatbot chunk（本条 Evidence IDs 为 none），不能仅凭仓库名断言缺失需求。建议先在仓库搜索 chatbot 实现（Amazon Lex / Lambda intents / chat UI 等）：若存在则按模型建议加 FR-009 并更新 Product Scope；若未实现则加一条说明该名称指向尚未实现的 chatbot。

**Human decision**

- [ ] Accept
- [ ] Reject
- [x] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> 需讨论。仓库名显著包含 'chatbot'，但 evidence pack 无任何相关证据。是否为缺失需求需先在仓库核查是否存在 chatbot 实现，不能凭名称直接 ACCEPT，也不宜直接 REJECT。

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
> 证据不足，需讨论。E005 仅显示 Kafka/Avro 实时比分管线，"live streaming"是否指视频流无法从现有证据确定。模型加的澄清注本身是合理推断，但仍属推测，应先核 README 全文/架构图确认其含义后再写入。

**Human decision**

- [ ] Accept
- [ ] Reject
- [x] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> 需讨论。仓库名含 'live-streaming'，README 提到 'live match screenings'，但 E005 仅证实 Kafka/Apache Avro 的实时比分更新管线。'live streaming' 究竟指比分管线还是视频流存在歧义，需查看 README 全文与架构图后澄清，避免范围误述。

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
> 采用模型建议并限定范围：在 Traceability Matrix 中下调 FR-003（screening 推荐）、FR-004（日程/提醒）的置信度，并注明源自 README 目标性文案而非已验证实现。FR-002（预测）有 E002/E006 的 SageMaker 证据佐证，可保留较高置信；可进一步核查 SNS/SQS/Lambda 是否实现 reminder 投递。

**Human decision**

- [ ] Accept
- [ ] Reject
- [x] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> 部分接受。E001 多为目标性文案（"We aim to / provide / suggest"），SRS 把 FR-002/003/004/005 全部写成硬性"shall"。其中 FR-002（预测）有 E002/E006 SageMaker 代码佐证、较实；而 screening 推荐、schedule/reminder 仅愿景文案支撑。故接受"降低 FR-003/FR-004 置信、标注源自 README 目标"，预测类不必降级。

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
> 证据不足，需讨论。EC2/Kafka 由 E005 文本支持，但各 AWS 服务（SQS/SNS、Lambda、SageMaker、DynamoDB/Elasticsearch）的互连数据流是从服务清单推断、非验证图。架构图 architecture.jpg 不在证据包中，需先核图：若图确认关系则不改，否则按模型建议在 Section 2 区分"已验证组件"与"推断的数据流关系"。

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> 

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
> 采用模型建议：把该假设改回与 E005 原义一致——"最后一周的赛季预测假设使用本赛季除最后一周外已进行的所有比赛作为输入数据 (E005)"，避免现版本"除 final week 外"的近反义改写造成误导。

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> Issue 成立（minor）。E005 原文为"predictions for the final week assume all matches barring the last week are considered"，SRS 改写成"prediction depends on data ... except the final week"，把"预测哪一周/排除哪一周"语义近乎倒置，可能误导读者。引用正确但措辞应恢复原义。

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
> 采用模型建议：在 NFR-004 验收基础追加"仓库证据未定义量化扩展指标；验证仅限于确认使用 DynamoDB 与 Elasticsearch"，使其在证据受限下仍诚实可读。

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> Issue 成立（minor）。NFR-004 已恰当标为 inferred，但无可测量的验收标准（无吞吐/延迟/数据量目标）。在证据限制下应明确其不可测到服务级，仅限架构审查确认使用了 DynamoDB/Elasticsearch。
