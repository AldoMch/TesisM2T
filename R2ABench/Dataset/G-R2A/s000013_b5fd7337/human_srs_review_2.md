# Human SRS Review Sheet

## Metadata

- Sample directory: `s000013_b5fd7337`
- Generated SRS: `final_srs.md`
- Evidence pack: `evidence_pack.json`
- Review model: `claude-opus-4-8`
- Generated at: `2026-06-05T15:37:39.402242Z`
- Raw model response: `model_srs_review_raw.md`
- Parse status: `parsed`

## Overall Model Opinion

- Recommendation: `revise`
- Confidence: `0.72`
- Rationale: The SRS is well-structured and most requirements are traceable to evidence. However, several requirements (FR-004, FR-005, mood classification itself) infer a classification capability that the evidence only describes as storage/retrieval of already-classified moods, with no evidence of the classification algorithm or model itself. The architecture diagram is not directly verified, and some 'explicit' evidence-type labels overstate confidence for inferred items.

## Overall Human Decision

- [ ] Accept
- [ ] Reject
- [ ] Partial accept

Reason:
> 

## Positive Observations

- Core architecture claims (React frontend, FastAPI backend, Elasticsearch + Kibana storage, Genius API dependency, tier-per-container Docker deployment) are well-supported by E003 with accurate quoting.
- Data requirements DR-001/DR-002 correctly map to the field-level dataset descriptions in E006 (song name, SLink, Lyric, language, Artist, Genres, Songs).
- The SRS is appropriately conservative in labeling inferred items (e.g., service-to-service protocol detail explicitly flagged as inferred in Communication Interfaces).
- Traceability matrix is comprehensive, with every requirement carrying evidence IDs and verification methods.
- English-song scope limitation is correctly attributed to E005, the data exploration README.

## Candidate Issues

### R001: unsupported_claim

- Severity: `major`
- Suggested action: `needs_human_check`
- SRS location: FR-004, DR-003, Product Functions Summary
- Evidence IDs: E003

**Claim or gap**

The SRS asserts the system performs mood classification ('A song has undergone initial classification', 'classified moods'), but the evidence only states that songs are stored alongside their moods and retrieved quickly after 'an initial classification'. The actual classification mechanism (model, algorithm, API, input/output) is not described in any cited evidence chunk.

**Model opinion**

E003 references 'after an initial classification, the mood of a song can be retrieved' but never describes how classification happens. The repository name implies sentiment/mood classification exists, but the evidence pack does not include the classifier component. Requirements treating classification as an established system function may be partially unsupported. The storage/retrieval behavior is supported; the classification act itself is inferred.

**Recommended human check**

Inspect the backend code (e.g., FastAPI routes, model/inference modules) and data_exploration notebooks to confirm whether and how mood classification is implemented, and add an explicit FR for the classification step if evidence exists.

**Model proposed SRS change**

Add a note to FR-004 Source Evidence column and a caveat in Product Functions Summary: 'The mood classification mechanism is referenced in evidence ([E003], 'initial classification') but the classifier implementation is not evidenced in the retrieved chunks; the classification step is inferred from storage behavior.' Conditionally, after verification, add a new FR-007 'Mood classification of song lyrics' with verified input/output and evidence ID.

Optional human revised fix:
> 仅保留“存储已分类歌曲及其 mood、后续可检索”作为证据支持内容；将“系统执行分类算法/模型推理”的表述标为 inferred 或待证实。不要在没有后端/模型证据前新增分类 FR。

**Human decision**

- [ ] Accept
- [ ] Reject
- [✅️] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> 部分成立。E003 直接支持“歌曲与 mood 一起存储”和“初次分类后可快速检索”，这部分issue不成立；但分类机制、分类输入/输出和系统主动执行分类的能力没有证据，应标为推断或待补证，这部分issue成立。

### R002: architecture_detail

- Severity: `major`
- Suggested action: `needs_human_check`
- SRS location: Section 2 Product Perspective, NFR-001, C-005, References
- Evidence IDs: E003

**Claim or gap**

The SRS describes a multi-tier Docker architecture and references a ground-truth architecture diagram (architecture_highlevel.png), but the diagram itself is not in the evidence pack and was not directly examined to confirm the tier composition or service-to-service flows.

**Model opinion**

E003 text confirms 'Each tier is hosted on a docker container' and names React/FastAPI/Elasticsearch/Kibana/Genius. The tier-per-container claim is supported by text. However, the specific architectural flows (use case 1/2 diagrams) are cut off in evidence and the architecture_highlevel.png is not analyzed. The number of tiers and exact data flows should be cross-checked against the diagram.

**Recommended human check**

Open architecture_highlevel.png and the docker-compose/deployment_config files to confirm the exact set of containers/tiers and inter-service communication, then validate NFR-001 and C-005 against them.

**Model proposed SRS change**

In NFR-001 acceptance criterion add: 'Verify against architecture_highlevel.png and docker-compose configuration that each named tier (frontend, backend, Elasticsearch, Kibana) maps to a distinct container.' Keep wording conditional until diagram/compose file is confirmed.

Optional human revised fix:
> 

**Human decision**

- [✅️] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> 可采纳模型建议

### R003: traceability

- Severity: `minor`
- Suggested action: `needs_human_check`
- SRS location: FR-005, NFR-002 (Evidence Type 'explicit')
- Evidence IDs: E003

**Claim or gap**

FR-005 and NFR-002 distinguish 'reuse stored classification instead of requiring a new initial classification step' as explicit, but E003 only states moods 'can be retrieved very quickly' after initial classification. The non-reclassification guarantee (i.e., that the system will NOT reclassify) is an inference, not an explicit statement.

**Model opinion**

The retrieval-from-storage behavior is supported. The stronger claim that reclassification is avoided is reasonable but inferential. Labeling it 'explicit' overstates evidence strength.

**Recommended human check**

Confirm in backend code whether a cache/lookup-first branch exists that bypasses classification for stored songs; downgrade evidence type to 'inferred' if not explicitly stated.

**Model proposed SRS change**

Change Evidence Type for NFR-002 (Section 5) and the Traceability Matrix row for FR-005/NFR-002 from 'explicit' to 'inferred', or reword to 'support fast retrieval of stored moods ([E003])' without asserting non-reclassification.

Optional human revised fix:
> 可采用模型建议。保留“stored mood retrieval”作为显式内容，将“不重新分类/绕过分类”标为 inferred。

**Human decision**

- [✅️] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> Issue 成立。E003 明确支持快速检索已存 mood，但没有直接说系统禁止或跳过重新分类。

### R004: scope

- Severity: `minor`
- Suggested action: `needs_human_check`
- SRS location: Section 1 Product Scope; FR-006; DR-004; C-006
- Evidence IDs: E005

**Claim or gap**

The English-song limitation is framed in some places as a system-enforced runtime constraint (FR-006: 'The system shall operate within the project's English-song scope'; acceptance: 'Accepted/processed data limited to English songs'), but E005 describes it as a dataset/project decision ('We will limit the project to English songs') made during data exploration, not a runtime enforcement mechanism.

**Model opinion**

E005 supports a project/dataset scoping decision, not necessarily an enforced input filter in the running application. FR-006 phrased as a 'shall operate' functional requirement with acceptance via runtime data handling may overstate this as enforced behavior.

**Recommended human check**

Check whether the backend/data pipeline actually filters or rejects non-English songs at runtime, or whether English-only is purely a dataset preparation decision.

**Model proposed SRS change**

Reword FR-006 to a constraint/data-scope statement: 'The project dataset is limited to English songs ([E005]); the SRS does not evidence a runtime language-enforcement filter.' Or reclassify FR-006 as a design constraint rather than a functional requirement pending verification.

Optional human revised fix:
> 可采用模型建议。

**Human decision**

- [✅️] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> Issue 成立。E005 证明的是数据集范围选择，而非运行时语言过滤；当前 FR-006/acceptance 的“accepted/processed data limited”表述过强。

### R005: ambiguity

- Severity: `minor`
- Suggested action: `needs_human_check`
- SRS location: FR-003 / Section 8 acceptance for FR-003
- Evidence IDs: E003

**Claim or gap**

FR-003 output is 'Search result used for downstream processing' and acceptance is 'produces a search result for further handling' — the downstream processing (lyrics fetch, classification, storage) is left undefined, making the requirement's end-to-end behavior ambiguous.

**Model opinion**

E003 confirms Genius API is used to search for songs not in Elasticsearch, but the chain from search result to classified/stored mood is not specified. 'Downstream processing' is vague and not independently verifiable.

**Recommended human check**

Trace backend code path after Genius search to determine what 'downstream processing' entails (lyric retrieval, classification, persistence) and specify the observable outcome.

**Model proposed SRS change**

Refine FR-003 acceptance to a verifiable outcome once the flow is confirmed, e.g., 'For a song not in Elasticsearch, the system retrieves song/lyric data via the Genius API and proceeds to classification and storage (FR-004).' Until verified, flag 'downstream processing' as underspecified.

Optional human revised fix:
> 可采纳模型建议。在确认前，先将验收标准改为“Genius API search is invoked and returns a search result”，并注明后续处理未在证据中定义。

**Human decision**

- [✅️] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> Issue 成立。E003 支持 Genius API search，但不支持未定义的 “downstream processing” 作为可验证输出；当前验收标准过于模糊。

### R006: traceability

- Severity: `minor`
- Suggested action: `probably_ignore`
- SRS location: NFR-003 / Section 1 Product Scope ('web application')
- Evidence IDs: E002

**Claim or gap**

NFR-003 and several scope statements lean on E002, which is the default Create React App boilerplate README. This evidence supports that React/CRA tooling exists and the app runs in a browser in dev mode, but it is generic boilerplate and does not describe this product's specific frontend behavior.

**Model opinion**

E002 is weak, generic evidence (auto-generated CRA text). It legitimately supports 'browser-accessible' and 'React frontend' but should not be over-relied upon for product-specific UI requirements. Traceability is technically valid but low-signal.

**Recommended human check**

Inspect frontend/mood_classification/src for actual UI components to support product-specific UI requirements rather than the boilerplate README.

**Model proposed SRS change**

Annotate NFR-003 and FR-001 evidence note: 'E002 is Create React App boilerplate; it supports browser access and React usage but not product-specific UI behavior. Strengthen with frontend source evidence.'

Optional human revised fix:
> 

**Human decision**

- [ ] Accept
- [x] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> Issue 不构成必改缺陷。
