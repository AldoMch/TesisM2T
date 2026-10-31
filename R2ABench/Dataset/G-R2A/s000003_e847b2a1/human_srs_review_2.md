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
- [ ] Partial accept

Reason:
> 

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
> 

**Human decision**

- [✅️] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> 推断合理，E004中证据充足，可采用模型建议

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
> 

**Human decision**

- [ ] Accept
- [ ] Reject
- [x] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> 此处的evidence只表明系统会periodically checks for oracle requests and answers them，无法支撑issue中的the oracle may answer prediction queries or resolve outcomes。

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
> 

**Human decision**

- [✅️] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> 模型不采纳，改法中引入TTL这一没有证据支撑的概念。应该改为Replace FR-003 description with: The system shall periodically evaluate whether the oracle requires extension and perform the appropriate extension action according to the defined oracle lifecycle policy.此外，应当明确oracle extension的定义、触发条件和执行措施。

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
> 

**Human decision**

- [✅️] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> 在当前修改建议的基础上加入若不支持contract-initiated oracle queries之后该如何修改FR

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
> 

**Human decision**

- [✅️] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> 证据中出现了prediction-cards API，不应该修改其命名。

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
> 

**Human decision**

- [✅️] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> 可采用模型建议

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
> 

**Human decision**

- [✅️] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> 可采用模型建议，E003证据能够支撑change

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
> 在修改建议部分引入unsupported claim。模型建议改为Prediction participant：Prediction participant: User who interacts with the system via the frontend UI to create and manage prediction-related operations using a connected wallet.并在Section 2 or a new Section 2.5中国列举出用户使用场景：User creates a prediction by submitting event-related data through the frontend interface；Additional user interactions (e.g., viewing predictions, participating, claiming outcomes) shall be specified if supported by the system.

**Human decision**

- [✅️] Accept
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
> The interaction flow between the frontend, smart contract, and oracle service shall be defined and aligned with the system architecture documentation (e.g., architecture diagram).

The SRS shall describe, at an appropriate level of abstraction:

the sequence of interactions between components
the triggering conditions for oracle processing
the flow of prediction-related data across system components

**Human decision**

- [✅️] Accept
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
> 

**Human decision**

- [✅️] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> 证据充分，建议合理，可采用模型建议

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
> 

**Human decision**

- [ ] Accept
- [ ] Reject
- [x] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
>E002中的配置是测试环境中的。现有的 NFR-004 已经明确涵盖了对“HTTP-facing test/deployment configuration”的 CORS 支持要求，该需求在 SRS 中已得到妥善处理，无需额外引入关于 Nginx 的架构约束。
