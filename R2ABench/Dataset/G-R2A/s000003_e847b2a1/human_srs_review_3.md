# Human SRS Review Sheet

## Metadata

- Sample directory: `s000003_e847b2a1`
- Generated SRS: `final_srs.md`
- Evidence pack: `evidence_pack.json`
- Review model: `claude-opus-4-8`
- Generated at: `2026-06-05T15:28:27.708804Z`
- Raw model response: `model_srs_review_raw.md`
- Parse status: `parsed`

## Overall Model Opinion

- Recommendation: `revise`
- Confidence: `0.78`
- Rationale: The SRS is well-structured and evidence-backed, but contains several missing architectural details verifiable from the ground-truth diagram, ambiguous scope boundaries, and unsupported terminology. Key issues include missing smart-contract detail, unclear oracle lifecycle behavior, and the absence of prediction-resolution workflow that may be visible in the architecture diagram.

## Overall Human Decision

- [ ] Accept
- [ ] Reject
- [x] Partial accept

Reason:
> SRS 严格基于 6 个证据 chunk、追溯性强、措辞保守,整体可接受但需修订。此前多项 major/critical(R001/R002/R004/R005/R008/R009)被判 PARTIAL_ACCEPT 是因为架构图不在证据包;现已读取 selected_candidates.csv 中 image_url 指向的架构图并据图重判:R009(三组件数据流,critical)、R002(prediction resolution/settlement 工作流)、R008(用户目标场景)由图坐实,改为 ACCEPT;R001(链上合约 + oracle 交互)、R004(oracle 查询源 coingecko 与 higher/lower 响应)、R005(card 对应链上 NFT 实体)图证实其架构/实体关系、改为 PARTIAL_ACCEPT(实现语言、字段级结构仍需源码)。仍为 PARTIAL_ACCEPT 的只剩 R003(oracle "extension" 是否指 TTL,需核源码)与 R010(convertDate 具体转换规则,需核源码),二者图未涵盖。可直接修的 R006(.env 属性截断)、R007(FR-005 验收标准)及 R011(nginx 为测试夹具,部分接受)维持原判。

## Positive Observations

- The SRS strictly adheres to evidence-backed requirements and avoids speculation, maintaining high traceability confidence (all requirements cite specific evidence IDs).
- The traceability matrix is complete and well-structured, providing clear evidence type and verification method for each requirement.
- The SRS correctly identifies the multi-component nature of the system (oracle service, frontend API, smart contract integration) and documents the technology stack (Quarkus, React, Aeternity SDK) with evidence support.
- Functional requirements are testable and include clear acceptance criteria tied to verification methods (Inspection, Demonstration, Test).
- The SRS correctly flags medium-confidence items (e.g., NFR-005) where evidence is indirect, demonstrating appropriate conservatism.
- CORS configuration detail from E002 is precisely documented with specific allowed methods and headers, providing a concrete integration boundary specification.

## Candidate Issues

### R001: architecture_detail

- Severity: `major`
- Suggested action: `needs_human_check`
- SRS location: Section 2 (Product perspective), Section 4 (FR-006)
- Evidence IDs: E004

**Claim or gap**

The SRS describes contract interaction but does not specify the smart-contract language, deployment model, or whether the contract is on-chain. Evidence E004 shows interaction with a contract instance via AENS name resolution, but no evidence clarifies the contract's implementation technology or architecture layer.

**Model opinion**

The ground-truth architecture diagram likely shows whether the prediction-cards contract is a deployed Sophia contract, how it relates to the oracle service, and the data flow between frontend–contract–oracle. The SRS should state the contract technology if the diagram or additional evidence supports it.

**Recommended human check**

Review the architecture.png diagram at https://github.com/kryptokrauts/ae-prediction-cards/blob/main/images/architecture.png to determine: (1) whether the prediction-cards contract is a Sophia smart contract, (2) how the oracle service interacts with the contract, and (3) the architectural layer boundaries.

**Model proposed SRS change**

If the diagram confirms a Sophia contract: Add to Section 2 (Product perspective): 'The system includes a Sophia smart contract deployed on the Aeternity blockchain, resolved via AENS name `predictioncards.chain`, which manages prediction lifecycle and oracle interaction.' Update C-002 to include contract technology constraint. If the diagram shows oracle–contract interaction: Add FR or NFR describing this interaction path.

Optional human revised fix:
> 定论前需查看 architecture.png。该图不在 evidence pack 中,合约语言(Sophia)、部署模型、oracle↔合约交互均无证据支持,不能直接写入。模型的修改是条件式的("if the diagram confirms"),方向可接受,但必须先核图再改。E004 只证实经 AENS 名 `predictioncards.chain` 调用某合约的 `create_prediction`,SRS 现有表述已与此一致。

**Human decision**

- [ ] Accept
- [ ] Reject
- [x] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> 图标注的是 "Smart Contract",并未写出实现语言;"Sophia" 虽是 Aeternity 合约的惯例语言,但图未显式标注,故合约语言仍应标 inferred,不写成 explicit。模型条件式建议中"on-chain + oracle 交互"部分采纳,"Sophia 语言"部分保持推断标注。

### R002: missing_requirement

- Severity: `major`
- Suggested action: `needs_human_check`
- SRS location: Section 4 (Functional Requirements)
- Evidence IDs: E001

**Claim or gap**

The SRS documents prediction creation (FR-006) but does not describe prediction resolution, settlement, or outcome determination. The repository is named 'prediction-cards' and evidence shows oracle request/response handling (FR-001, FR-002), suggesting the oracle may answer prediction queries or resolve outcomes. No functional requirement captures this workflow.

**Model opinion**

The oracle service likely plays a role in resolving predictions (answering 'which outcome occurred'), but the SRS does not document this behavior. The ground-truth diagram may show the prediction lifecycle including resolution/settlement flow.

**Recommended human check**

Review the architecture diagram and oracle-service README (E001) to determine whether the oracle service resolves predictions, how prediction outcomes are determined, and whether there is a settlement or payout step.

**Model proposed SRS change**

If evidence supports prediction resolution: Add FR-010: 'Prediction outcome resolution: When a prediction reaches its resolution time, the oracle service shall query external data sources or on-chain state, determine the outcome, and submit the result to the smart contract.' Add DR-007: 'Prediction outcome data: The system shall determine and record the actual outcome (higher/lower) for each prediction.' Cite E001 and any additional README/contract evidence.

Optional human revised fix:
> 不要按模型给出的 FR-010/DR-007 文本写入——其内容("query external data sources or on-chain state、determine outcome、submit result、higher/lower")全是推测,E001 只说 oracle 周期性检查并回答 oracle 请求,未提及 prediction resolution/settlement/payout。若后续在 oracle-service 源码/完整 README 中确认有结算流程,再以证据为准补 FR。

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> 

### R003: missing_requirement

- Severity: `minor`
- Suggested action: `needs_human_check`
- SRS location: Section 4 (FR-003)
- Evidence IDs: E001

**Claim or gap**

FR-003 states 'The system shall periodically check whether an oracle extension is necessary' but does not define what 'extension' means (TTL extension? query lifetime extension?) or what action is taken when extension is necessary.

**Model opinion**

Aeternity oracles have a time-to-live (TTL) parameter. The oracle service likely monitors TTL and extends the oracle registration before expiry to keep it active. The SRS should clarify this behavior and the corresponding action.

**Recommended human check**

Check the oracle-service README or source code to confirm whether 'extension' refers to extending the oracle TTL, and what action the service takes (e.g., submitting an OracleExtendTransaction).

**Model proposed SRS change**

If TTL extension is confirmed: Replace FR-003 description with: 'The system shall periodically check the oracle TTL and, if the TTL is approaching expiry, submit an oracle-extension transaction to maintain oracle availability.' Add NFR-006: 'Oracle availability: The oracle service shall maintain continuous availability by extending its TTL before expiry.'

Optional human revised fix:
> 定论前查看 oracle-service README/源码。E001 仅说 "periodically checks if an extension is necessary",未说明 extension 指 oracle TTL 还是别的;"submit OracleExtendTransaction""maintain availability" 属推测。确认是 TTL 延展后,可采用模型措辞;在此之前 FR-003 保持现有保守表述即可。

**Human decision**

- [ ] Accept
- [ ] Reject
- [x] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> 证据不足,需讨论(minor)。"extension" 的具体含义在 E001 中未定义,模型对 TTL 的解释合理但属推断。需核 oracle-service 源码确认后再细化 FR-003,不宜直接接受推测性改写。

### R004: ambiguity

- Severity: `minor`
- Suggested action: `needs_human_check`
- SRS location: Section 4 (FR-001, FR-002)
- Evidence IDs: E001

**Claim or gap**

FR-001 and FR-002 describe checking for and answering oracle requests, but do not specify the oracle query format, query source, or response format. It is unclear what data the oracle provides or who/what submits oracle queries.

**Model opinion**

The oracle likely receives queries from the smart contract (e.g., 'what is the outcome of event X?') and responds with outcome data. The SRS should clarify the query–response data model and the interaction flow.

**Recommended human check**

Review the oracle-service source code and the architecture diagram to determine: (1) what entity submits oracle queries (contract? user?), (2) the query and response data structure, and (3) the external data source the oracle consults (API? blockchain state?).

**Model proposed SRS change**

If evidence supports contract-initiated oracle queries: Update FR-001 description: 'The system shall periodically poll the Aeternity blockchain for oracle queries submitted by the prediction-cards contract.' Update FR-002 description: 'The system shall process each oracle query, retrieve the required event outcome data from [data source, if known], and submit an oracle-response transaction containing the outcome.' Add DR-008: 'Oracle query/response format: Oracle queries shall contain [query structure]. Oracle responses shall contain [response structure].'

Optional human revised fix:
> 定论前查看 oracle-service 源码。查询发起方(合约? 用户?)、查询/响应数据结构、外部数据源都无证据,模型改写里的 "[data source, if known]""[query structure]" 等占位符本身说明证据缺失,不能写入。确认后再以证据填充 FR-001/FR-002 与 DR。

**Human decision**

- [ ] Accept
- [ ] Reject
- [x] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> query 的发起方与 query/response 的精确字段结构图中未给出,DR-008 的 "[query structure]/[response structure]" 占位符仍无证据,需核源码后再填,不要现在写入。

### R005: unsupported_claim

- Severity: `minor`
- Suggested action: `needs_human_check`
- SRS location: Section 1 (Product scope), Section 2 (Product functions summary)
- Evidence IDs: none

**Claim or gap**

The SRS uses the phrase 'prediction cards smart-contract interface' and 'prediction-cards API' without evidence that 'cards' is a meaningful architectural or domain concept. Evidence shows 'prediction' creation but no explicit 'card' entity or multi-prediction card container.

**Model opinion**

The repository name includes 'prediction-cards', but evidence E003 and E004 show 'PredictionCardsApi' and 'PredictionEvent' without defining 'card'. The SRS should avoid unsupported terminology unless evidence or the diagram clarifies the domain model.

**Recommended human check**

Review the architecture diagram, smart-contract source (if available in the repository), and frontend domain model to determine whether 'card' is a defined entity (e.g., a card containing multiple predictions, or a UI metaphor) or simply a branding/naming choice without architectural meaning.

**Model proposed SRS change**

If 'card' is not a defined entity: Replace references to 'prediction cards smart-contract interface' with 'prediction smart contract' or 'prediction management contract'. Update Section 2 Product scope and FR-005, FR-006 descriptions to use 'prediction API' instead of 'prediction-cards API' unless evidence supports 'cards' as a domain concept. If 'card' is confirmed as an entity: Add DR for card structure and update the domain model section.

Optional human revised fix:
> 定论前查看前端领域模型/合约源码。需注意 "PredictionCards" 是 E003/E004 中实际出现的类名(`PredictionCardsApi`、`PredictionCardsProvider`),SRS 用它作专有名并不算无据;模型担心的是把 "cards" 当作有结构的领域实体。若核查确认 "card" 非实体,可按模型建议在叙述性文字中改用 "prediction API";但不应改动代码中真实存在的类名引用。

**Human decision**

- [ ] Accept
- [ ] Reject
- [x] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> NFT 字段级数据结构(属性、与 prediction 的精确绑定关系)图未细化,如需 DR 仍应核合约/前端源码;对真实类名 `PredictionCardsApi` 的引用本就无需改动。故由原"术语无据"转为"术语有实体支撑",部分接受。

### R006: traceability

- Severity: `minor`
- Suggested action: `needs_human_check`
- SRS location: Section 4 (FR-004)
- Evidence IDs: E001

**Claim or gap**

FR-004 states the oracle service requires a '.env file containing the properties needed for proper running' but does not list or reference the specific required properties. E001 states 'the following properties' but the evidence snippet is truncated and does not show the property list.

**Model opinion**

The evidence is incomplete. The SRS should either list the required properties (if available in the full E001 document) or state that the property list is documented in the oracle-service README and defer to that source.

**Recommended human check**

Review the full oracle-service README.md to extract the list of required .env properties. Verify whether these include Aeternity node URLs, keypairs, oracle configuration, etc.

**Model proposed SRS change**

If the full property list is available: Update FR-004 description to: 'The system shall require a .env file containing the following properties: [list properties from E001]. Service startup shall fail if required properties are missing.' Add DR for each critical configuration property (node URL, keypair, etc.). If the list is not available in evidence: Update FR-004 to: 'The system shall require a .env file containing required runtime properties as documented in oracle-service/README.md. Service startup shall validate the presence of mandatory properties.'

Optional human revised fix:
> 采用模型的"列表不可用"分支:E001 片段在 "contains the following properties" 处截断,具体属性清单不可见。把 FR-004 改为引用 oracle-service/README.md 中记载的必需属性,不要凭空列举 node URL/keypair 等(那是模型推测的例子)。也不要新增 "startup shall fail/validate" 这类证据未支持的行为,除非核实。

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> Issue 成立(minor)。E001 明确说 .env 是 mandatory 且 "contains the following properties",但片段截断、未展示属性清单,FR-004 却泛称 "the properties needed"。应注明具体属性以完整 README 为准,提升可追溯性。注意仅采用"引用 README"的保守分支,不写入推测的属性名或启动校验行为。

### R007: non_verifiable

- Severity: `minor`
- Suggested action: `accept_as_issue`
- SRS location: Section 4 (FR-005)
- Evidence IDs: E003

**Claim or gap**

FR-005 verification criterion is 'Demonstration: Rendering the provider makes the API obtainable from context by child components.' This is underspecified—no concrete test steps, inputs, or expected observable outputs are defined.

**Model opinion**

The acceptance criterion should specify how to verify the behavior (e.g., render a test child component, call usePredictionCardsApi(), verify the returned object has the expected methods).

**Recommended human check**

Define a concrete test scenario: (1) render PredictionCardsProvider with a mock wallet, (2) render a child component that calls usePredictionCardsApi(), (3) verify the returned API instance is defined and has method createPrediction.

**Model proposed SRS change**

Update Section 8 verification table for FR-005 acceptance criterion: 'Render PredictionCardsProvider with a test wallet. Render a child component that calls usePredictionCardsApi(). Verify the returned API object is defined and exposes the createPrediction method.'

Optional human revised fix:
> 采用模型建议:把 FR-005 验收改为可观察步骤——渲染 `PredictionCardsProvider`(注入测试 wallet),子组件调用 `usePredictionCardsApi()`,断言返回的 API 实例已定义且暴露 `createPrediction` 方法。这些都锚定在 E003/E004 已有的标识符上,未超出证据。

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> Issue 成立(minor)。FR-005 现有验收 "Rendering the provider makes the API obtainable from context" 缺少具体步骤/可观察输出。改为基于 E003/E004 真实标识符的具体测试场景,提升可验证性,且不引入证据外内容。

### R008: scope

- Severity: `minor`
- Suggested action: `needs_human_check`
- SRS location: Section 2 (User classes)
- Evidence IDs: E003, E004

**Claim or gap**

The SRS defines three user classes but does not describe direct end-user behavior (e.g., a participant who creates a prediction via the frontend UI, views predictions, or claims payouts). The 'Frontend user with wallet' class is described only as 'operating the frontend through a connected wallet-backed API context', which is implementation-focused rather than user-goal-focused.

**Model opinion**

The repository appears to support end-user prediction creation and interaction, but the SRS does not document user-facing goals or scenarios (e.g., 'User creates a prediction on event X with a wager'). The user-class table should describe user roles and goals, not just technical interfaces.

**Recommended human check**

Review the frontend UI (if available in the repository) and the architecture diagram to understand end-user workflows. Determine whether users can: create predictions, view predictions, participate in predictions, claim rewards, etc.

**Model proposed SRS change**

If end-user workflows are supported: Replace 'Frontend user with wallet' row with: 'Prediction participant: User who creates, views, and interacts with predictions via the frontend UI, using a connected Aeternity wallet for blockchain transactions.' Add user scenarios in Section 2 or a new Section 2.5: 'User creates a prediction by selecting an event, choosing higher/lower, and submitting via wallet signature. User views active predictions and their outcomes. User claims payout for correct predictions (if supported).' Cite E003, E004, and any UI evidence.

Optional human revised fix:
> 定论前查看前端 UI/架构图。证据仅证实 createPrediction 这一前端 API 操作(E004);"view predictions""choose higher/lower""claim payout" 等用户场景无证据。模型建议的 "User creates a prediction by selecting an event..." 是推测,不能直接写入。可保留现有以 wallet API 为中心的 user class 描述,待 UI 证据补充后再加用户目标场景。

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> 

### R009: architecture_detail

- Severity: `critical`
- Suggested action: `needs_human_check`
- SRS location: Section 2 (Product perspective), Section 3 (Software/API interfaces)
- Evidence IDs: none

**Claim or gap**

The SRS does not describe the data flow or interaction sequence between the three main components (frontend, smart contract, oracle service). It is unclear whether the oracle service monitors the contract, whether the contract emits events, or how prediction lifecycle state transitions occur.

**Model opinion**

The architecture diagram at https://github.com/kryptokrauts/ae-prediction-cards/blob/main/images/architecture.png is explicitly referenced and likely shows component interaction, data flow, and the prediction lifecycle. The SRS should document this architecture based on the diagram.

**Recommended human check**

Review the architecture.png diagram to extract: (1) component interaction flow (frontend → contract → oracle → contract?), (2) event triggers (contract events? scheduled polling?), (3) data flow for prediction creation, oracle query, and outcome resolution, and (4) any external data sources the oracle consults.

**Model proposed SRS change**

Add Section 2.6 'System Architecture and Data Flow': 'The system architecture comprises three primary components: [describe based on diagram]. Prediction lifecycle: (1) User submits prediction via frontend, (2) Frontend calls contract create_prediction method, (3) [Contract emits oracle query / Oracle polls contract state], (4) Oracle service detects query and retrieves outcome data from [source], (5) Oracle submits response to contract, (6) Contract finalizes prediction outcome and [settlement logic]. See architecture diagram at [URL].' Update Section 3 to reference this flow. Cite architecture diagram as primary evidence source for this section.

Optional human revised fix:
> 不按模型给出的数据流文本写入。该 "lifecycle (1)–(6)" 几乎全是占位符与推测(`[describe based on diagram]`、`[settlement logic]`、`[source]`),架构图不在证据包,组件间交互序列在文本证据中不可见。严重级别标为 critical 但定性为 architecture_detail/Evidence IDs=none——本质是"图未提供"。需先获取并分析架构图,再以其为证据补 Section 2 数据流。

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> 

### R010: missing_requirement

- Severity: `minor`
- Suggested action: `needs_human_check`
- SRS location: Section 4 (Functional Requirements)
- Evidence IDs: E004

**Claim or gap**

E004 shows the frontend API converts the event start timestamp before contract submission (line: 'this.convertDate(event.start_timestamp...)'), but the SRS does not specify the conversion logic, target format, or reason for conversion (timezone? Aeternity timestamp format?).

**Model opinion**

Timestamp conversion is a data-transformation requirement with potential correctness implications (wrong timezone or format could break prediction timing). The SRS should document the conversion rule.

**Recommended human check**

Review the convertDate method implementation in PredictionCards.api.ts to determine the conversion logic (e.g., JavaScript Date to Unix timestamp, UTC normalization, etc.).

**Model proposed SRS change**

If conversion logic is available: Add DR-007 (renumber if needed): 'Event timestamp conversion: The system shall convert the event start timestamp from [source format] to [target format, e.g., Unix timestamp in milliseconds] before contract submission. Timestamps shall be normalized to UTC.' Update FR-006 to reference DR-007. Cite E004 and the convertDate implementation.

Optional human revised fix:
> 定论前查看 PredictionCards.api.ts 的 convertDate 实现。E004 仅可见调用了 `this.convertDate(event.start_timesta...)`(且片段在此截断),源/目标格式、时区归一化均无证据;模型文本里的 "[source format]""[target format]""normalized to UTC" 都是占位/推测,不能写入。确认实现后再补 DR。现有 DR-003 已记录"使用并在提交前转换 start timestamp",与证据相符。

**Human decision**

- [ ] Accept
- [ ] Reject
- [x] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> 证据不足,需讨论(minor)。E004 确实显示存在 convertDate 转换,但具体转换规则不可见。DR-003 已保守记录该转换行为;细化格式/时区需核 convertDate 源码,不能凭推测填充。

### R011: missing_requirement

- Severity: `minor`
- Suggested action: `needs_human_check`
- SRS location: Section 5 (Non-Functional Requirements)
- Evidence IDs: E002

**Claim or gap**

E002 shows CORS configuration in a test/deployment artifact (nginx-cors.conf), suggesting the system includes an HTTP server or reverse proxy. The SRS does not specify the deployment architecture, whether nginx is required, or what component serves HTTP requests.

**Model opinion**

CORS configuration implies a web server boundary, but the SRS does not document the HTTP service layer. The architecture diagram may show whether nginx is a required component or just a test fixture.

**Recommended human check**

Review the architecture diagram and deployment documentation (docker-compose, deployment scripts, etc.) to determine: (1) whether nginx is a production component or only used in tests, (2) what service(s) nginx proxies, and (3) the HTTP API surface (REST endpoints, static file serving, WebSocket, etc.).

**Model proposed SRS change**

If nginx is a required deployment component: Add C-005: 'The system HTTP boundary shall use nginx (or equivalent reverse proxy) with CORS support for cross-origin browser access.' Add NFR-006 (renumber if needed): 'Deployment model: The system shall support containerized deployment with [nginx + frontend + oracle service / other architecture from diagram].' Cite E002 and any docker-compose or deployment evidence. If nginx is test-only: Add note in Section 8 that E002 describes test infrastructure CORS policy, not production deployment.

Optional human revised fix:
> 采用模型的"test-only"分支:E002 的 CORS 配置来自 `contract-test/docker/nginx-cors.conf`,路径本身表明是测试基础设施,不能据此断言生产部署用 nginx。建议在 Section 8(或 FR-008/FR-009、NFR-004 旁)注明"E002 描述的是测试基础设施的 CORS 策略,非生产部署架构"。不要新增 C-005/NFR-006 把 nginx 作为生产必需组件,除非另有 docker-compose/部署证据。

**Human decision**

- [ ] Accept
- [ ] Reject
- [x] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> 部分接受。① 成立:E002(`contract-test/docker/nginx-cors.conf`)来自 contract-test 目录,SRS 把 CORS 写成 FR-008/FR-009/NFR-004 时未点明这是测试夹具而非生产 HTTP 边界,应加注澄清——采纳 test-only 分支。② 不成立:把 nginx 升格为生产必需部署组件(C-005/NFR-006)无证据支持,拒绝。故部分接受。
