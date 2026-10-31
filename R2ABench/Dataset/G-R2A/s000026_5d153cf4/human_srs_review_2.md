# Human SRS Review Sheet

## Metadata

- Sample directory: `s000026_5d153cf4`
- Generated SRS: `final_srs.md`
- Evidence pack: `evidence_pack.json`
- Review model: `claude-opus-4-8`
- Generated at: `2026-06-05T15:40:36.937167Z`
- Raw model response: `model_srs_review_raw.md`
- Parse status: `parsed`

## Overall Model Opinion

- Recommendation: `revise`
- Confidence: `0.78`
- Rationale: The SRS is well-traced to the evidence pack and most requirements are evidence-backed. However, several items overstate verifiability/confidence (autoscaling and load-balancing are documented intent but not configured in the visible evidence; no HPA/Deployment manifest is present), the WebSocket implementation (websocketd + pulltop) is under-specified, and the architecture diagram has not been cross-checked. These warrant human adjudication before acceptance.

## Overall Human Decision

- [ ] Accept
- [ ] Reject
- [ ] Partial accept

Reason:
> 

## Positive Observations

- Strong, consistent traceability: each FR/NFR cites specific evidence IDs that match the evidence pack contents.
- Port mapping (Service port 80/TCP -> targetPort 8080, container EXPOSE 8080) is accurately captured in FR-008, NFR-004, and C-004 directly from E003 and E001.
- The 10-message cache (FR-006/NFR-003) and single-subscription multiplexing are faithfully drawn from README evidence (E004/E006).
- Appropriately conservative on payload format, noting it is 'not specified in evidence' rather than inventing a schema.

## Candidate Issues

### R001: traceability

- Severity: `major`
- Suggested action: `needs_human_check`
- SRS location: FR-002, NFR-001, Section 9 Traceability (autoscaling)
- Evidence IDs: E004

**Claim or gap**

Autoscaling 'based on the number of clients connected' is marked as explicit/High confidence and verified by Demonstration, but the only evidence is a README narrative sentence. No HPA, Deployment, or scaling manifest is present in the evidence pack.

**Model opinion**

The README does state autoscaling on connected clients, so the requirement is supported as documented intent. However, classifying it as High-confidence and Demonstration-verifiable overstates what the evidence supports, since no scaling configuration (HPA metric, custom metric adapter) is in the evidence. Connection-count-based autoscaling typically requires custom metrics, which are not evidenced.

**Recommended human check**

Search the repository for HPA manifests, Deployment specs, or custom metric adapters that implement connection-based autoscaling. Confirm whether autoscaling is configured or only described aspirationally.

**Model proposed SRS change**

In NFR-001 and FR-002, lower Confidence to Medium and change Verification from Demonstration to Inspection, with acceptance note: 'README documents autoscaling on connected client count; implementing manifest not present in evidence pack.' Conditional: if an HPA/custom-metric manifest is found, restore High/Demonstration and cite its evidence ID.

Optional human revised fix:
> 

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> Issue 成立。E004 支持“文档声称 autoscaling”，但没有代码实现，建议采纳修改建议。

### R002: missing_requirement

- Severity: `minor`
- Suggested action: `needs_human_check`
- SRS location: Section 2.4 / Section 4 (runtime composition)
- Evidence IDs: E001, E005

**Claim or gap**

The Dockerfile (E001) shows the WebSocket bridge is implemented via 'websocketd' piped to a 'pulltop' Node.js process (exec.sh $SYMBOL). The SRS does not capture that the adapter is realized by websocketd + pulltop, nor the SYMBOL/topic environment binding mechanism.

**Model opinion**

These are concrete, evidenced implementation details that affect how the topic config maps to runtime behavior (the CMD uses $SYMBOL, not directly the ConfigMap 'topic' key). The disconnect between ConfigMap key 'topic' and the runtime env var 'SYMBOL' is worth noting for traceability of FR-007.

**Recommended human check**

Inspect exec.sh and deployment manifests to confirm how ConfigMap 'topic' is injected into the container ($SYMBOL env). Verify whether websocketd/pulltop should be named as architectural components.

**Model proposed SRS change**

Add to Section 2.4 (Operating environment) or a new architecture note: 'The runtime composes websocketd with a Node.js process (pulltop), invoked via exec.sh with a topic/symbol parameter (container CMD uses $SYMBOL). (E001)' Add a check under FR-007 acceptance that the ConfigMap 'topic' value is mapped to the runtime parameter.

Optional human revised fix:
> 建议采纳第一部分。SRS 应增加 `websocketd`、`pulltop`、`exec.sh $SYMBOL` 的 runtime composition；但 `topic` 到 `$SYMBOL` 的映射目前没有足够的证据来写成完整需求。

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> Issue 成立。E001 直接展示 base image 安装 websocketd、复制 pulltop、CMD 执行 `/project/exec.sh $SYMBOL`，这些是当前 SRS 漏掉的可追踪 runtime 细节。

### R003: architecture_detail

- Severity: `major`
- Suggested action: `needs_human_check`
- SRS location: Section 2.1 / Section 4 (overall architecture)
- Evidence IDs: E004

**Claim or gap**

The SRS architecture has not been cross-checked against the ground-truth architecture.svg. Components such as the Pub/Sub subscription lifecycle, websocketd bridge, and per-VM subscription model are asserted from README prose only.

**Model opinion**

The diagram likely depicts the data flow (Pub/Sub topic -> subscription per VM -> websocketd -> WebSocket clients -> load balancer). Confirming against the diagram would validate FR-004, FR-005, and the per-VM subscription claim with stronger evidence.

**Recommended human check**

Open architecture.svg and verify the depicted components and flows match FR-003/FR-004/FR-005 and the per-VM subscription model. Add the diagram as an evidence reference.

**Model proposed SRS change**

Add architecture.svg to Section 1.4 References and add a sentence in Section 2.1: 'See architecture.svg for the reference data flow.' Reconcile any component discrepancies surfaced by the diagram.

Optional human revised fix:
> 

**Human decision**

- [ ] Accept
- [x] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> 证据包未包含图内容，issue不成立。

### R004: non_verifiable

- Severity: `minor`
- Suggested action: `accept_as_issue`
- SRS location: FR-005 / NFR-002 ('one subscription per VM')
- Evidence IDs: E004

**Claim or gap**

The requirement 'consuming a single subscription per VM' is verified by Analysis but no observable acceptance criterion (e.g., how to count subscriptions per VM) is given.

**Model opinion**

The claim is evidence-supported by E004 wording, but 'single subscription per VM' needs a concrete observable check to be verifiable (e.g., inspect created subscriptions vs. VM count, or process inspection). As written it is hard to test objectively.

**Recommended human check**

Determine an observable method to count Pub/Sub subscriptions relative to VMs/pods at runtime, and add it as acceptance criterion.

**Model proposed SRS change**

In Section 8 for FR-005/NFR-002, add acceptance basis: 'Verify via Pub/Sub subscription listing that the number of active subscriptions equals the number of VMs/pods regardless of connected client count.'

Optional human revised fix:
> 建议采纳。待确认后进一步细化验收标准。

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> Issue 成立，当前 Analysis 验收标准太抽象，无法稳定验证。

### R005: ambiguity

- Severity: `minor`
- Suggested action: `needs_human_check`
- SRS location: FR-003 / Section 3.3 (single endpoint per topic)
- Evidence IDs: E004, E005

**Claim or gap**

The SRS states the system exposes 'a single client endpoint that maps to an individual Pub/Sub topic' but does not clarify whether the deployment is fixed to exactly one topic instance or whether multiple topic deployments are supported.

**Model opinion**

Evidence (E004/E005) supports a one-endpoint-to-one-topic mapping per deployment, but the SRS could be read as a system-wide single-topic limitation. Clarifying scope avoids misinterpretation about multi-topic deployments.

**Recommended human check**

Confirm from README/manifests whether multiple independent deployments (one per topic) are intended, or strictly one topic.

**Model proposed SRS change**

In FR-003, append: 'Each deployment instance binds one endpoint to one configured topic; multiple topics require separate deployments.' Mark conditional pending README confirmation.

Optional human revised fix:
> 建议将 FR-003 改为“per deployment instance”。

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> Issue 成立，确实表意不清，应写明是per deployment instance。

### R006: missing_requirement

- Severity: `minor`
- Suggested action: `probably_ignore`
- SRS location: Section 7 Constraints (base image / OS)
- Evidence IDs: E001

**Claim or gap**

The Dockerfile uses 'archlinux/base:latest' and downloads websocketd at build time; this base-image and external-download dependency is a real constraint not captured in the SRS.

**Model opinion**

Minor but evidenced. The dependency on a rolling 'latest' Arch base and an external websocketd download is a build/runtime constraint relevant to reproducibility and supply-chain considerations.

**Recommended human check**

Confirm the base image and external download remain as shown; decide whether to record as a constraint.

**Model proposed SRS change**

Add C-006: 'The container image is built from archlinux/base:latest and downloads websocketd at build time, introducing an external build-time dependency. (E001)'

Optional human revised fix:
> 

**Human decision**

- [ ] Accept
- [x] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
>Issue 成立，建议采纳修改意见。
