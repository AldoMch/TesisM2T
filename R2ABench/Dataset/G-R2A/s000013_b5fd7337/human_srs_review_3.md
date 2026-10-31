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
- [x] Partial accept

Reason:
> 核心架构主张(React/FastAPI/Elasticsearch+Kibana/Genius/每层一容器)有 E003 扎实支撑,整体可接受但需修订。R001(把"mood 分类"当既有功能,但证据只证存储/检索已分类的 mood)为成立的 major:接受加 caveat 并降级分类相关项,推测性的 FR-007 暂缓待证;R003(FR-005/NFR-002 误标 explicit)、R004(English scope 被写成运行时强制)、R005(FR-003 "downstream processing" 模糊)、R006(E002 为 CRA 样板)为成立的 minor,接受;R002(架构图)已读取 architecture_highlevel.png 完成核对,四层/每层一容器与服务间数据流均被证实,改为接受。

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
> 采用模型的 caveat 部分,暂缓 FR-007:在 Product Functions Summary 与 FR-004 处加注——"mood 分类机制仅由 E003 的 'after an initial classification' 间接提及,检索到的证据未含分类器实现,分类步骤系从存储行为推断"。同时把涉及 "classified/classification" 的措辞(FR-004 触发条件、DR-003、Product Scope)从隐含"系统执行分类"软化为"存储已分类的 mood"。新增 FR-007 属推测,需先在 backend 源码确认分类实现后再以证据补,不现在写入。

**Human decision**

- [ ] Accept
- [ ] Reject
- [x] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> 部分接受(major)。成立:E003 只说 "songs will be stored alongside their according moods, so that after an initial classification, the mood ... can be retrieved",全程未描述分类器(模型/算法/输入输出),而 SRS 在 FR-004/DR-003/Product Functions 中把"分类"当作已确立的系统功能,属过度断言;应加 caveat 并软化措辞。不接受:模型条件式新增的 FR-007("Mood classification of song lyrics")在证据确认前仍是推测,暂缓,待核 backend 源码后再以证据补。存储/检索行为本身有据,保留。

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
> 定论前查看 architecture_highlevel.png 与 docker-compose/部署配置。E003 文本已证 "Each tier is hosted on a docker container" 且点名 React/FastAPI/Elasticsearch/Kibana/Genius,故 NFR-001/C-005 的"每层一容器"主张本身有据;但确切的层数与服务间数据流(use case 1/2 图)在证据中被截断、未分析。可按模型建议把 NFR-001 验收写成"对照架构图与 compose 文件确认各层映射到独立容器",措辞保持条件式直到核图。

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> 

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
> 采用模型建议:把 NFR-002 及 FR-005/NFR-002 的 Evidence Type 从 explicit 改为 inferred,或改写为"支持快速检索已存储的 mood(E003)"而不断言"不再重新分类"。E003 只说 "can be retrieved very quickly","不会重新分类"是合理推断但非显式。

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> Issue 成立(minor)。检索行为有据,但"绕过/不重复分类"的保证是从 "retrieved very quickly" 推断而来,标 explicit 夸大了证据强度,应降为 inferred 或改写为不断言非重分类的措辞。

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
> 采用模型建议:把 FR-006 从功能需求("The system shall operate within ... English-song scope" + 运行时数据验收)改写为数据范围约束——"项目数据集限定为英文歌曲(E005);SRS 未发现运行时语言强制过滤的证据",或并入 C-006/DR-004 这类约束项。C-006、DR-004 已以约束/数据范围方式正确表述,FR-006 与之重复且把范围决定误升为运行时强制行为,应降格或移除。

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> Issue 成立(minor)。E005 原文 "We will limit the project to English songs, as this simplifies the mood classification" 是数据探索阶段的项目/数据集决定,而非运行时输入过滤。FR-006 写成 "shall operate within ... scope" 且验收 "Accepted/processed data limited to English songs",把范围决定误述为已强制的运行时行为。应改为数据范围约束;C-006/DR-004 已正确表述,FR-006 宜降格或合并。

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
> 采用模型的"暂标 underspecified"部分:E003 证实未命中时用 Genius API 搜索歌曲,但从搜索结果到分类/存储的链路无证据,FR-003 的 "Search result used for downstream processing" 不可独立验证。先在 FR-003 验收旁注明 "downstream processing 待明确"。模型给出的具体改写("retrieves song/lyric data ... proceeds to classification and storage")须等 backend 流程确认后再写,不现在落地。

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> Issue 成立(minor)。FR-003 输出/验收依赖未定义的 "downstream processing / further handling",E003 未说明搜索结果之后的链路(取词、分类、存储),不可独立验证。应先标注 underspecified;具体可验证结果待核 backend 代码路径后再补,避免引入推测。

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
> 采用模型建议:在 NFR-003 与 FR-001 处加证据注记——"E002 为 Create React App 自动生成的样板 README,支持'浏览器可访问 + 使用 React'这类通用结论,但不描述本产品特有的 UI 行为;需以前端源码证据加强"。不需改动 FR-001/NFR-003 的结论本身(浏览器访问/React 有据),仅标注证据强度低。

**Human decision**

- [ ] Accept
- [x] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> Issue 成立(minor,低影响)。E002 是 CRA 样板文本,合法支持 "browser-accessible""React frontend" 这类通用主张,但不应据以支撑产品特有 UI 需求。追溯技术上有效但信号弱,加注提示以前端源码加强即可,结论无需推翻。
