# Human SRS Review Sheet

## Metadata

- Sample directory: `s000061_2eb4d99c`
- Generated SRS: `final_srs.md`
- Evidence pack: `evidence_pack.json`
- Review model: `claude-opus-4-8`
- Generated at: `2026-06-05T15:57:29.065765Z`
- Raw model response: `model_srs_review_raw.md`
- Parse status: `parsed`

## Overall Model Opinion

- Recommendation: `revise`
- Confidence: `0.72`
- Rationale: The SRS is well-structured and most requirements are traceable to the evidence chunks. However, the evidence pack is narrow (6 chunks from a much larger repo with 38 documents and a documented architecture diagram), and the SRS understates the actual scope (IoT device simulation, MQTT/IoT Core, device types, UI). Several constraints and a couple of FRs lean on partial code fragments; some claims (e.g., CORS status 200 behavior, ROUTE_BUCKET env constraint scope) need verification. The C-005 license constraint and the STACK_NAME/SOLUTION_ID env claims are correctly scoped only to evidenced files, which is good.

## Overall Human Decision

- [ ] Accept
- [ ] Reject
- [x] Partial accept

Reason:
> 证据仅取自 38 文档大库的 6 块切片，SRS 的保守限定本身没错，但范围说明、CORS 验证方式、env 归属等需修订。R001/R002/R004/R005/R006/R007 接受，R003 因 apiEndpoint 赋值被截断保留待核。

## Positive Observations

- Requirements are consistently traced to specific evidence IDs with a dedicated traceability matrix and verification/acceptance section.
- The SRS appropriately limits scope to evidenced behavior and uses cautious confidence levels (e.g., Medium for custom-resource items).
- C-005 (license) is correctly scoped to 'repository source files in evidence' rather than overclaiming repository-wide licensing.
- Data requirements (DR-001/002/003) closely mirror the concrete fields visible in E001 and E005, making them readily verifiable.
- Non-functional requirements (logging level, tracing, REGIONAL endpoint, JSON access logs) map directly to explicit config values in E004.

## Candidate Issues

### R001: scope

- Severity: `major`
- Suggested action: `needs_human_check`
- SRS location: 1.2 Product scope; 2.1 Product perspective
- Evidence IDs: E003, E005

**Claim or gap**

The SRS scopes the product to an API Gateway REST API, a CloudFormation custom resource, and S3 vehicle-route loading only. The repository is an IoT Device Simulator (per name, README, and architecture.png) whose core function is simulating IoT devices and publishing telemetry, likely to AWS IoT Core via MQTT, with a UI.

**Model opinion**

The evidence pack is a thin slice (6 chunks) of a 38-document repo and does not surface the central simulation/IoT publishing behavior or UI. The SRS correctly limits itself to provided evidence, but the resulting scope statement materially understates the repository. The architecture.png ground-truth diagram should be checked to confirm omitted components (IoT Core, device generators, simulation engine, web console).

**Recommended human check**

Open architecture.png and README to enumerate top-level components (IoT Core/MQTT, simulation engine, device types, web UI, DynamoDB). Decide whether SRS scope should explicitly note these are out of scope of the evidence pack vs. expand the SRS.

**Model proposed SRS change**

In 1.2 add a scope-limitation note: 'This SRS reflects only the subset of repository behavior present in the evidence pack. The repository is an IoT Device Simulator that also includes device simulation, telemetry publishing to AWS IoT Core, and a management UI, which are not covered by the provided evidence and are out of scope for this document.'

Optional human revised fix:
> 

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> 证据确实只覆盖 API/自定义资源/S3 路由三块,SRS 范围陈述偏窄,补一句限定说明合理且不越界。

### R002: non_verifiable

- Severity: `major`
- Suggested action: `needs_human_check`
- SRS location: FR-002; Section 8 (FR-002 acceptance)
- Evidence IDs: E004

**Claim or gap**

FR-002 states 'CORS status code 200' as an output and acceptance criterion. E004 shows `statusCode: 200` inside the CORS preflight config (defaultCorsPreflightOptions), which is a configuration value, not an observable runtime CORS status guarantee phrased as written.

**Model opinion**

The '200 CORS status behavior' is verifiable by inspection of config, but phrasing it as a 'Test' acceptance for response status may overstate what's evidenced. The verification method (Test) and acceptance text mix configuration inspection with runtime behavior. Recommend aligning verification to inspection of the CORS preflight config unless a runtime test exists.

**Recommended human check**

Confirm whether `statusCode: 200` is the CORS preflight option in api.ts and whether any test exercises a live OPTIONS request. Adjust verification method accordingly.

**Model proposed SRS change**

In FR-002 change Verification to 'Inspection' and acceptance to: 'API construct CORS preflight options specify allowMethods [GET, POST, PUT, DELETE, OPTIONS], allowHeaders [Content-Type, X-Amz-Date, Authorization, X-Api-Key], and statusCode 200.'

Optional human revised fix:
> 

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> E004 里 statusCode:200 是 defaultCorsPreflightOptions 的配置项,不是运行时响应状态,用 Test 当验收名不副实,改 Inspection 更贴证据。

### R003: traceability

- Severity: `minor`
- Suggested action: `needs_human_check`
- SRS location: FR-001; 3.2 REST API; Section 8 FR-001
- Evidence IDs: E003, E004

**Claim or gap**

FR-001 asserts the system 'provide an API endpoint and API ID.' E004 shows `this.apiEndpoint = ;` (truncated/empty in the chunk) and `this.apiId = api.restApiId;`. The apiEndpoint assignment value is not visible in evidence.

**Model opinion**

apiId is clearly evidenced; apiEndpoint assignment is truncated, so the endpoint claim rests on a partially visible fragment. This is a weak-traceability concern rather than a contradiction. Low severity but worth a human glance.

**Recommended human check**

Inspect api.ts to confirm apiEndpoint is assigned to a real URL expression (not empty), supporting the 'API endpoint' claim.

**Model proposed SRS change**

If endpoint assignment is confirmed, keep FR-001 as is. If not confirmed, narrow FR-001 output to 'an API ID (restApiId)' and mark the endpoint claim as needs-verification.

Optional human revised fix:
> 部分接受。E003 已声明 `public apiEndpoint: string`,字段确实存在,FR-001 不必收窄;但 E004 里赋值 `this.apiEndpoint = ;` 被截断,在 FR-001/3.2 加一句"endpoint 赋值表达式在证据中被截断,待 api.ts 核实"即可。

**Human decision**

- [ ] Accept
- [x] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> apiId 有确证;apiEndpoint 字段已声明但赋值被截断,属弱溯源,标注待核而非删改。

### R004: unsupported_claim

- Severity: `minor`
- Suggested action: `needs_human_check`
- SRS location: 2.1 Product perspective; 2.2 ('Lambda-backed microservice integration')
- Evidence IDs: E003

**Claim or gap**

The SRS states 'Lambda-backed microservice integration.' E003 references `microservicesLambda: LambdaFunction` and `microservicesLambdaFunction` as a property, but the evidence does not show the integration wiring (i.e., methods routed to the Lambda).

**Model opinion**

The presence of a microservices Lambda property is evidenced; actual API-to-Lambda integration behavior is inferred. The claim is plausible but the integration mechanics are not in the chunks. Keep but tie strictly to the property declaration, or mark as inferred.

**Recommended human check**

Verify in api.ts whether REST methods are integrated with microservicesLambda (LambdaIntegration). If yes, evidence is sufficient.

**Model proposed SRS change**

In 2.1 reword to 'a microservices Lambda construct associated with the API (LambdaFunction property)' unless integration wiring is confirmed in api.ts.

Optional human revised fix:
> 

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> E003 只见 microservicesLambda 属性声明,未见方法到 Lambda 的集成接线,"Lambda-backed integration"是推断,收紧到属性声明层面。

### R005: ambiguity

- Severity: `minor`
- Suggested action: `needs_human_check`
- SRS location: FR-005; DR-002; C-003
- Evidence IDs: E005

**Claim or gap**

E005 shows `routeName = snapshot.routeInfo?.routeName || ` (default fallback truncated). The SRS states the S3 key is `routeName`, but if routeName is undefined the key may be empty/default. The handling of a missing routeName is not specified.

**Model opinion**

The route-loading logic uses optional chaining with a fallback default that is truncated in the evidence. The SRS does not address the empty/default routeName case, leaving behavior for missing route info ambiguous. Minor but affects FR-005/FR-006 completeness.

**Recommended human check**

Inspect dynamics-model.js to see the default value for routeName when snapshot.routeInfo.routeName is absent and whether an empty key triggers FR-006 error path.

**Model proposed SRS change**

Add to FR-005 a clause: 'If routeInfo.routeName is absent, the system shall use the implemented default key value (verify in dynamics-model.js).' Resolve exact default text after inspection.

Optional human revised fix:
> 

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> 证据确有截断,SRS 未规定 routeName 缺失时的键值,补待核条款合理。

### R006: traceability

- Severity: `minor`
- Suggested action: `needs_human_check`
- SRS location: C-004; 2.4 Operating environment
- Evidence IDs: E002, E005

**Claim or gap**

C-004 lists environment variables AWS_REGION, SOLUTION_ID, SOLUTION_VERSION, STACK_NAME as custom-resource constraints, sourced from a test file (E002) that sets process.env for mocking. 2.4 additionally lists ROUTE_BUCKET as part of the custom-resource environment context.

**Model opinion**

The env vars in E002 come from a unit-test mock (process.env = {...}), which is reasonable evidence that the code reads them, but framing them as production 'constraints' should be confirmed against the actual handler. Also ROUTE_BUCKET (E005) belongs to the simulator dynamics model, not the custom resource; mixing them in 2.4 under one environment list is slightly imprecise.

**Recommended human check**

Confirm the custom-resource handler actually reads SOLUTION_ID/SOLUTION_VERSION/STACK_NAME at runtime (not only in tests), and keep ROUTE_BUCKET attributed to the simulator component.

**Model proposed SRS change**

In 2.4 split the environment listing per component: custom resource (AWS_REGION, SOLUTION_ID, SOLUTION_VERSION, STACK_NAME) and simulator (ROUTE_BUCKET). Mark C-004 source as 'test-mock-derived; verify in handler.'

Optional human revised fix:
> 

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> C-004 的 env 出自 E002 测试 mock(process.env={...}),ROUTE_BUCKET 属 E005 模拟器组件,2.4 混为一张表不准确,应按组件拆分并标注 mock 来源待核。

### R007: architecture_detail

- Severity: `minor`
- Suggested action: `needs_human_check`
- SRS location: 2.4 Operating environment; overall
- Evidence IDs: none

**Claim or gap**

No mention of AWS IoT Core / MQTT, DynamoDB, Cognito, or other components that an IoT Device Simulator architecture typically includes and that architecture.png likely depicts.

**Model opinion**

Because the evidence pack omits these, the SRS cannot assert them; but the ground-truth architecture diagram is explicitly available and should be consulted to ensure no critical evidenced component was missed during retrieval. This is an architecture-detail completeness check rather than an asserted error.

**Recommended human check**

Review architecture.png to confirm whether IoT Core/MQTT, DynamoDB, Cognito, simulation engine, and UI are part of the system; decide if the evidence pack/SRS needs expansion.

**Model proposed SRS change**

After diagram review, optionally add an Operating Environment note enumerating diagram-confirmed AWS services that are out of evidence-pack scope, clearly flagged as not requirement-bearing in this SRS.

Optional human revised fix:
> 

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> 图存在 → 未引用是真实缺口,可补引用;具体组件待开图确认。
