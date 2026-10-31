# Human SRS Review Sheet

## Metadata

- Sample directory: `s000353_eb501ff3`
- Generated SRS: `final_srs.md`
- Evidence pack: `evidence_pack.json`
- Review model: `claude-opus-4-8`
- Generated at: `2026-06-05T16:11:41.547226Z`
- Raw model response: `model_srs_review_raw.md`
- Parse status: `parsed`

## Overall Model Opinion

- Recommendation: `revise`
- Confidence: `0.78`
- Rationale: The SRS is well-structured and most requirements trace cleanly to evidence. However, several traceability and verification issues exist: E004 evidence supports middleware existence (not configurable 'support' as a security control), FR-003 error response 400 is described differently in evidence, and some requirements are stated as testable but the evidence only supports existence/structural inspection. A few claims (Jaeger 'for requests', port configurability) are slightly overstated relative to the terse evidence.

## Overall Human Decision

- [ ] Accept
- [ ] Reject
- [x] Partial accept

Reason:
> 七条均成立。最值得改:R005(E005 明含"201: successfully saved ensembler"与 put/UpdateEnsembler,SRS 漏掉 create/update 两个 FR,低估了 ensembler API 范围,应补 FR-006/FR-007)、R001(FR-003 把 400 笼统当通用失败,E006 明确 400=被其他实体占用/404=未找到/500=删除失败,应枚举具体语义)、R002(NFR-001 据 E004 的"/turing/middleware ... e.g. authorization and request validation"目录描述,把目录存在写成"shall support"安全控制并标 Security 过度,应降为含中间件层 + 例子,verify 改 Inspection、confidence 降 Medium)。R003(Jaeger 初始化≠每请求都 trace)、R004(8080 可配但配置字段名被截)、R006(HTTP_JSON/UPI_V1 协议未捕获)、R007(FR-005 verify 用 Demonstration 但 E004 仅目录职责)为小修。全部接受。

## Positive Observations

- Functional requirements FR-001 through FR-003 are precisely traced to OpenAPI evidence (E003, E005, E006) with correct paths, methods, and response content types.
- The SRS appropriately scopes out unsupported areas (Section 6.3 explicitly notes absence of retention/privacy/migration evidence) rather than inventing requirements.
- Evidence IDs are consistently attached to each requirement and the traceability matrix includes confidence levels, supporting auditability.
- OpenAPI 3.0.3 conformance (NFR-004) and the timeout pattern constraint are accurately captured directly from E003.

## Candidate Issues

### R001: contradiction

- Severity: `minor`
- Suggested action: `accept_as_issue`
- SRS location: FR-003; Section 8 (FR-003 acceptance); Data Requirements 6.1 (EnsemblerId)
- Evidence IDs: E006

**Claim or gap**

FR-003 lists `400` as a generic failure response, but evidence E006 specifies `400` means 'Ensembler is used by other entity' (a specific semantic), not a generic bad-request error.

**Model opinion**

The SRS generalizes the documented error codes. E006 gives precise meanings: 400 = used by other entity, 404 = not found, 500 = failed to delete. Collapsing these into 'documented error responses including 400, 404, or 500' loses verifiable semantics and slightly mischaracterizes 400.

**Recommended human check**

Confirm in api/api/specs/ensemblers.yaml that 400/404/500 descriptions match the evidence and decide whether SRS should enumerate the specific meanings.

**Model proposed SRS change**

In FR-003 Output column, replace 'documented error responses including 400, 404, or 500' with 'documented error responses: `400` (ensembler is used by another entity), `404` (ensembler not found), `500` (failed to delete ensembler)'. Mirror this in Section 8 acceptance basis.

Optional human revised fix:
> 采用。E006 明确 400="Ensembler is used by other entity"、404="Ensembler not found"、500="Failed to delete ensembler";SRS 把 400 当通用 bad-request 丢失了可验证语义,应逐码枚举。

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> 已据 E006 逐码核对,语义准确。

### R002: unsupported_claim

- Severity: `major`
- Suggested action: `needs_human_check`
- SRS location: NFR-001; Section 8 (NFR-001)
- Evidence IDs: E004

**Claim or gap**

NFR-001 states 'The API shall support authorization and request validation middleware'. E004 only lists a /turing/middleware package described as 'HTTP server middlewares e.g. authorization and request validation' — i.e., examples of middleware, not a guaranteed/required behavior.

**Model opinion**

Evidence supports that a middleware package exists with these examples, but phrasing it as a requirement ('shall support') with Security as the quality attribute overstates a directory description. The 'e.g.' indicates these are illustrative examples. This is verifiable only by code inspection of the package's existence, not by a security behavior test.

**Recommended human check**

Inspect /turing/middleware to confirm authorization and request validation middleware are actually implemented and wired into the HTTP server, not just example listings.

**Model proposed SRS change**

Revise NFR-001 to: 'The API server shall include an HTTP middleware layer; the repository documents authorization and request validation as middleware examples.' Lower confidence to Medium and keep verification as Inspection of the /turing/middleware package.

Optional human revised fix:
> 采用。E004 仅列"/turing/middleware | HTTP server middlewares e.g. authorization and request validation",是目录说明 + 举例("e.g."),不是保证的安全行为;写成"shall support 授权/校验"且标 Security 过度,应改为含中间件层 + 文档化示例,verify=Inspection,confidence=Medium。

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> 应查 /turing/middleware 是否真正实现并接入 HTTP server,而非仅示例列举。

### R003: ambiguity

- Severity: `minor`
- Suggested action: `accept_as_issue`
- SRS location: NFR-002; Section 8 (NFR-002)
- Evidence IDs: E002

**Claim or gap**

NFR-002 states the router 'shall support request tracing through Jaeger client initialization for requests'. E002 says 'Jaeger client is initialised to trace all requests... However, the tracer's methods determine whether the app adds the trace' — i.e., initialization does not guarantee tracing of every request.

**Model opinion**

The evidence explicitly qualifies that the tracer's methods decide whether traces are added. The SRS phrasing 'for requests' risks implying all requests are traced. Should reflect the conditional nature.

**Recommended human check**

Verify in engines/router code whether Jaeger tracing is unconditional or conditional/sampled per the README note.

**Model proposed SRS change**

Revise NFR-002 to: 'The router component shall initialize a Jaeger client for request tracing; whether a trace is added to a given request is determined by the tracer configuration/methods.'

Optional human revised fix:
> 采用。E002 原文"Jaeger client is initialised to trace all requests ... However, the tracer's methods determine whether the app adds the trace to the requests";初始化≠每请求都被 trace,SRS 的"for requests"易误读为全量,应反映条件性。

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> 

### R004: non_verifiable

- Severity: `minor`
- Suggested action: `needs_human_check`
- SRS location: NFR-003 / C-004; Section 8 (NFR-003)
- Evidence IDs: E002

**Claim or gap**

NFR-003 claims port 8080 default 'and allow this port to be configured'. E002 is fragmentary ('8080 of the user container by default. This can be configured by setting field. Refer to PR.') — the configuration field name is not captured, making the configurability claim hard to verify as written.

**Model opinion**

The default port 8080 is supported. Configurability is asserted in the evidence but the specific configuration field is elided ('setting field'). The acceptance basis 'can be configured to use another port' is testable in principle but lacks the field reference, weakening precision.

**Recommended human check**

Locate the actual values-file field used to configure the user container port in engines/router and confirm 8080 is the default.

**Model proposed SRS change**

Add a note to NFR-003/C-004 referencing the specific configuration field once identified; if not identifiable from evidence, mark configurability claim as 'documented but field unspecified in evidence pack'.

Optional human revised fix:
> 采用。E002 片段"8080 of the user container by default. This can be configured by setting field. Refer to PR."中配置字段名被省略;默认 8080 有据,可配性有声明但缺字段名,应定位 values 文件实际字段或标"字段在证据中未指明"。

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> 待查 engines/router 的 values 文件确认端口配置字段。

### R005: missing_requirement

- Severity: `minor`
- Suggested action: `accept_as_issue`
- SRS location: Section 4 Functional Requirements; FR list
- Evidence IDs: E005

**Claim or gap**

E005 shows a `201` response for a successfully saved ensembler (create) and a `put`/UpdateEnsembler operation, but the SRS omits create and update ensembler operations from the functional requirements.

**Model opinion**

Evidence E005 explicitly references '201: A JSON representation of a successfully saved ensembler' and 'put... operationId: UpdateEn...'. These create/update operations are evidenced but absent from FRs. The SRS only covers retrieve and delete, understating ensembler API scope.

**Recommended human check**

Confirm in api/api/specs/ensemblers.yaml that create (POST, 201) and update (PUT, UpdateEnsembler) operations exist and decide whether to add corresponding FRs.

**Model proposed SRS change**

Add FR-006 'Create ensembler' (POST returning 201 with Ensembler JSON, source E005) and FR-007 'Update ensembler' (PUT, operationId UpdateEnsembler, source E005), with corresponding traceability and acceptance rows.

Optional human revised fix:
> 采用。E005 明含"201: A JSON representation of a successfully saved ensembler"及"put ... operationId: UpdateEn...";SRS 只覆盖 retrieve/delete,漏掉 create(POST 201)与 update(PUT),低估 ensembler API 范围,应补 FR-006/FR-007 及对应溯源/验收行。

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> create 的 HTTP 方法/路径(POST /projects/{project_id}/ensemblers?)与 update 完整 operationId 待据全 ensemblers.yaml 确认。

### R006: scope

- Severity: `minor`
- Suggested action: `needs_human_check`
- SRS location: Section 3.4 / 6.1 (Timeout)
- Evidence IDs: E003

**Claim or gap**

The Timeout schema and the HTTP_JSON/UPI_V1 protocol details appear in E003 but the SRS only captures the timeout pattern and omits the protocol distinction (HTTP_JSON vs UPI_V1) that is part of router configuration semantics.

**Model opinion**

E003 text mentions 'For HTTP_JSON protocol, the valid are... Whereas, for UPI_V1 protocol...'. This indicates router protocol options that are part of the evidenced API but not represented. Minor since the excerpt is fragmentary, but worth a human check on completeness.

**Recommended human check**

Review routers.yaml to determine whether HTTP_JSON/UPI_V1 protocol selection is a documented router data field worth a data requirement entry.

**Model proposed SRS change**

Optionally add a Data Requirements row for router 'protocol' field (HTTP_JSON | UPI_V1) sourced to E003 once confirmed; otherwise leave as out-of-scope with a noted rationale.

Optional human revised fix:
> 采用(可选)。E003 含"For HTTP_JSON protocol, the valid are... Whereas, for UPI_V1 protocol...",表明 router 有 protocol 选项;摘录较碎,建议据全 routers.yaml 确认后补 protocol 数据需求行,或注明 out-of-scope 理由。

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> 低优先;证据片段较碎,确认后再补。

### R007: traceability

- Severity: `minor`
- Suggested action: `probably_ignore`
- SRS location: FR-005; Traceability matrix (FR-005)
- Evidence IDs: E004

**Claim or gap**

FR-005 is verified by 'Demonstration' and traced to E004, which is a directory/package description ('Packages for creating, updating and deleting Turing router deployment in Kubernetes cluster'). The evidence supports existence of such packages but not a demonstrable runtime behavior without further code.

**Model opinion**

The traceability is reasonable but the verification method 'Demonstration' implies running deployments, whereas E004 only documents package responsibilities. Inspection may be the more honest near-term verification given the evidence pack.

**Recommended human check**

Decide whether FR-005 verification should be 'Inspection' (of cluster packages) given current evidence, or whether deployment demonstration is feasible/in-scope.

**Model proposed SRS change**

Consider changing FR-005 verification from 'Demonstration' to 'Inspection/Demonstration' and note that E004 evidences package responsibilities rather than observed runtime behavior.

Optional human revised fix:
> 采用。FR-005 引 E004("/turing/cluster | Packages for creating, updating and deleting Turing router deployment in Kubernetes cluster")是目录/包职责描述,不足以支撑"Demonstration"运行时验证;就现有证据 Inspection 更诚实,可标 Inspection/Demonstration。

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> 
