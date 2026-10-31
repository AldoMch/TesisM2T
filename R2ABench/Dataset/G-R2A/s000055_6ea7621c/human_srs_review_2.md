# Human SRS Review Sheet

## Metadata

- Sample directory: `s000055_6ea7621c`
- Generated SRS: `final_srs.md`
- Evidence pack: `evidence_pack.json`
- Review model: `claude-opus-4-8`
- Generated at: `2026-06-05T15:53:34.853729Z`
- Raw model response: `model_srs_review_raw.md`
- Parse status: `parsed`

## Overall Model Opinion

- Recommendation: `revise`
- Confidence: `0.78`
- Rationale: The SRS is well-grounded and traceable for most claims, but it misattributes the search route handler (router delegates to algorithm.serveHints, not handler), introduces a deployment/Heroku constraint omission, and includes several inferred or partially supported claims (e.g., FR-002 'sensible suggestions', FR-007 not-found logging specifics) that need tightening. A few traceability and architecture details (architecture-diagram.png) should be checked.

## Overall Human Decision

- [ ] Accept
- [ ] Reject
- [ ] Partial accept

Reason:
> 

## Positive Observations

- Strong traceability: most FRs/DRs cite specific evidence IDs that map cleanly to README, router.js, handler.js, and test files.
- Correctly distinguishes supported vs unsupported items (e.g., search response payload marked 'unsupported', NFR-003 marked 'inferred').
- Accurate extraction of the MIME-type extension mapping (html/css/js/jpg/ico) directly from E004.
- Constraints section captures concrete code-level facts (CommonJS, filesystem reads from public, substring routing) with appropriate evidence.

## Candidate Issues

### R001: contradiction

- Severity: `major`
- Suggested action: `accept_as_issue`
- SRS location: Section 2 Product perspective; FR-004; Section 3 Software/API interfaces
- Evidence IDs: E003, E004, E006

**Claim or gap**

The SRS repeatedly states the router delegates search requests to a 'handler' / 'autocomplete handler', but the evidence shows the router delegates to a separate module: algorithm.serveHints (require('./algorithm.js')), not handler.js.

**Model opinion**

E003 shows `algorithm.serveHints(req, res)` for URLs containing 'search', while handler.js (E004) only contains serveHome/servePublic/notFound. The SRS conflates handler.js and algorithm.js. FR-004 saying 'router delegates the request to the autocomplete handler' is imprecise; the autocomplete logic lives in algorithm.js. This should be corrected for accuracy.

**Recommended human check**

Confirm in src/router.js and src/algorithm.js that search requests are served by algorithm.serveHints, distinct from handler.js.

**Model proposed SRS change**

In FR-004 and Section 3, replace 'autocomplete handler' with 'the autocomplete module (`algorithm.serveHints`)'. Update Section 2 to note three modules: router (`router.js`), handler (`handler.js`, home/public/notFound), and algorithm (`algorithm.js`, search hints).

Optional human revised fix:
> 

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> Issue 成立。E003 直接显示 search 分支调用的是 `algorithm.serveHints`，应当说明。建议采纳。

### R002: missing_requirement

- Severity: `minor`
- Suggested action: `needs_human_check`
- SRS location: Section 2 Operating environment; Section 7 Constraints
- Evidence IDs: E001

**Claim or gap**

README (E001) explicitly mentions 'Deploying on Heroku' as part of the project approach, but the SRS does not capture any deployment constraint/environment, and the evidence pack lists 'deployment' as a covered category.

**Model opinion**

Deployment to Heroku is weakly evidenced (mentioned as an approach goal, not implementation detail). It may warrant a low-priority assumption/constraint rather than a firm requirement. Given category coverage includes deployment, an explicit (even tentative) entry improves completeness.

**Recommended human check**

Check repository for Procfile, package.json start script, or Heroku config confirming actual deployment target.

**Model proposed SRS change**

Add to Section 2 Assumptions/Section 7 Constraints: 'C-005 (inferred/low): The application is intended for deployment on Heroku per README approach notes [E001]; confirm with Procfile/package.json.'

Optional human revised fix:
> 

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> issue不成立。E001 只说明团队考虑/规划 “Deploying on Heroku”，不足以证明系统具有 Heroku 部署能力或部署约束。属于过度推断。

### R003: non_verifiable

- Severity: `minor`
- Suggested action: `accept_as_issue`
- SRS location: FR-002
- Evidence IDs: E001, E005, E006

**Claim or gap**

FR-002 states the system returns 'sensible suggestions or a list of Nobel Prize laureates matching the entered string', but 'sensible' is subjective and the matching semantics are not specified by evidence.

**Model opinion**

The word 'sensible' is copied from the README user story (E001) and is not testable. E006 only confirms autocomplete returns an Array, not matching correctness. The acceptance criterion should reference the observable behavior (returns an array of laureate values) rather than 'sensible'.

**Recommended human check**

Inspect algorithm.autocomplete implementation/tests to determine what matching guarantee, if any, is verifiable.

**Model proposed SRS change**

Reword FR-002 system behavior to: 'The system returns an array of Nobel Prize laureate values for the entered string (matching correctness beyond array return type is not specified in evidence).' Remove 'sensible'.

Optional human revised fix:
> 建议采纳。FR-002 的 System behavior 改为：“The system returns an array from the autocomplete operation for the entered string; evidence does not specify the ranking or correctness semantics beyond array return type and Nobel laureate domain.” Traceability confidence 可保留 Medium。

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> Issue 成立。“sensible” 不可验证，E006 只支持返回数组，不支持质量、排序或精确匹配语义。建议采纳。

### R004: unsupported_claim

- Severity: `minor`
- Suggested action: `needs_human_check`
- SRS location: FR-007; NFR/Data on not-found
- Evidence IDs: E004

**Claim or gap**

FR-007 references not-found handling for both 'home or public asset serving'. Evidence (E004) shows readFile error path calls handler.notFound and console.log, but E004 is truncated for servePublic; full not-found behavior/output is not fully shown.

**Model opinion**

The logging and notFound delegation are supported by the visible readFile body (E004). However the specific 'Not-found response behavior' output and the notFound implementation are not in the evidence pack. The claim is reasonable but partially unverified; mark output as unspecified.

**Recommended human check**

Inspect handler.notFound implementation to confirm response status/content for not-found cases.

**Model proposed SRS change**

In FR-007 Output column, change to 'Delegation to handler.notFound and error logging (specific not-found response content not in evidence)'.

Optional human revised fix:
> FR-007 Output 改为：“Error is logged and control is delegated to `handler.notFound`; specific response status/content is not evidenced.” 不要在没有 `handler.notFound` 实现的情况下写死响应内容。

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> Issue 成立。E004 支持 error logging 和 delegation，但不支持 not-found 响应体或状态码的具体语义。

### R005: traceability

- Severity: `minor`
- Suggested action: `probably_ignore`
- SRS location: FR-001 evidence; DR-004
- Evidence IDs: E001, E002, E005

**Claim or gap**

FR-001 cites E002 (frontend tests) for accepting text input. E002 tests getUserInput(event) returning event.target.value, which supports input capture, but FR-001's user-facing 'enter text into an input field' is primarily from E001/E005. The E002 link is to the helper, not the UI field.

**Model opinion**

This is a weak traceability nuance: E002 supports DR-004 (string from event target value) more directly than the UI requirement FR-001. Keeping E002 on FR-001 is acceptable but the distinction between UI input and helper capture should be clear; consider relying on E001/E005 for FR-001 and E002 for DR-004.

**Recommended human check**

Confirm whether frontend code beyond tests defines the actual input field; the evidence pack only shows tests for helpers.

**Model proposed SRS change**

In FR-001, keep E001/E005 as primary evidence and annotate E002 as supporting the input-capture helper (getUserInput) rather than the UI field.

Optional human revised fix:
> 

**Human decision**

- [ ] Accept
- [x] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> issue 不是必须修复的缺口，属于模型偏好。

### R006: architecture_detail

- Severity: `minor`
- Suggested action: `needs_human_check`
- SRS location: Section 2 Product perspective; NFR-003
- Evidence IDs: E003, E004, E006

**Claim or gap**

A ground-truth architecture diagram exists (public/assets/architecture-diagram.png) but the SRS does not reference or reconcile its architecture against the diagram. NFR-003 (module separation) is marked 'inferred' and could be confirmed/strengthened by the diagram.

**Model opinion**

The diagram likely documents the router/handler/algorithm/data flow and could upgrade NFR-003 from inferred to explicit, and confirm the algorithm vs handler distinction in R001. Worth a human check against the image.

**Recommended human check**

Open architecture-diagram.png and verify it shows router -> handler/algorithm separation and data.json usage; update NFR-003 evidence type accordingly.

**Model proposed SRS change**

Add reference to architecture-diagram.png in Section 1 References and, if confirmed, change NFR-003 Evidence type from 'inferred' to 'explicit' with the diagram as source.

Optional human revised fix:
> 

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> issue不成立，当前 evidence chunk 没有图像内容。

### R007: ambiguity

- Severity: `minor`
- Suggested action: `accept_as_issue`
- SRS location: C-004; FR-004
- Evidence IDs: E003

**Claim or gap**

Constraint C-004 correctly notes search routing uses substring matching (endpoint.indexOf('search')), but FR-004/Section 3 say 'request URL contains search' without flagging the risk that any URL containing the substring 'search' (e.g., a static file named research.png) would be routed to autocomplete.

**Model opinion**

E003 confirms the substring match. This is an accurate but potentially fragile design; noting it as a known limitation improves precision and testability.

**Recommended human check**

Confirm in router.js that the match is a plain substring (indexOf) with no path delimiting, and decide whether to record as a limitation.

**Model proposed SRS change**

Add note to FR-004/C-004: 'Routing is by plain substring match on the URL; any URL containing the substring "search" is routed to autocomplete (potential collision with other resources).'

Optional human revised fix:
> 在 C-004 后增加 limitation：“Routing is by plain substring match on the URL (`endpoint.indexOf('search') !== -1`); any URL containing `search` is routed to autocomplete, which may collide with other resources.” FR-004 Trigger/Input 可保留 “URL contains `search`”。

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> issue成立，SRS确实没有指出没有标出任何包含 substring `search` 的 URL（例如名为 `research.png` 的静态文件）都会被路由到 autocomplete 的风险。
