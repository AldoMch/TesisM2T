# Human SRS Review Sheet

## Metadata

- Sample directory: `s000066_a314f8cb`
- Generated SRS: `final_srs.md`
- Evidence pack: `evidence_pack.json`
- Review model: `claude-opus-4-8`
- Generated at: `2026-06-05T16:00:59.288024Z`
- Raw model response: `model_srs_review_raw.md`
- Parse status: `parsed`

## Overall Model Opinion

- Recommendation: `revise`
- Confidence: `0.78`
- Rationale: The SRS is well-grounded in evidence and traceable for most claims, but several requirements over-interpret reconnect behavior, conflate explicit vs inferred evidence, and FR-007's 'displayed' player count is partly unsupported. A few minor traceability and verifiability tightenings are warranted before keeping.

## Overall Human Decision

- [ ] Accept
- [ ] Reject
- [x] Partial accept

Reason:
> 七条 issue 均成立,主要是把代码语义(reAddShipFromScene、setPlayers)和 README 标语(single-player)读过头,以及把不可测的并发通信当 explicit NFR。全部接受,多为贴近证据的措辞收紧。

## Positive Observations

- Strong, direct evidence backing for the WebSocket-over-HTTP transport and the P2P-not-supported constraint (E002), correctly cited in FR-002, C-002, C-003, NFR-004.
- Inbound action handling (game_reconnect, room_players_number, servers_list, servers_list_redirect, server_error, pong) is accurately enumerated from the onMessage switch (E004, E006) and mapped to discrete functional requirements.
- Outbound message format `[event, data]` and ping/null heartbeat are precisely traced to the send/resetHeartBeat code (E003).
- The SRS appropriately marks latency bounds and screen layouts as not supported by evidence, avoiding overreach.
- Traceability matrix distinguishes explicit vs inferred evidence (e.g., NFR-003 marked inferred), which aids adjudication.

## Candidate Issues

### R001: unsupported_claim

- Severity: `major`
- Suggested action: `needs_human_check`
- SRS location: FR-006 / Section 4; Verification FR-006
- Evidence IDs: E004

**Claim or gap**

FR-006 says the client shall 'restore the ship in the scene and restart the game' on `game_reconnect`. The evidence shows `this.game.reAddShipFromScene(data); this.game.start();` which re-adds a ship and starts the game, but the SRS phrasing ('restore the ship') and the verification basis ('restores the ship and restarts gameplay') assume semantics not fully confirmed by the snippet.

**Model opinion**

The behavior is roughly correct, but 'restore the ship in the scene' is a slight interpretation. The method name suggests re-adding a ship object from provided data; whether it 'restores' a prior ship state is not evidenced. This is acceptable but should be worded closer to the evidence.

**Recommended human check**

Inspect `reAddShipFromScene` implementation to confirm whether it restores prior state or adds a new ship object; confirm `game.start()` semantics.

**Model proposed SRS change**

FR-006: Replace 'restore the ship in the scene and restart the game' with 'add a ship to the scene using the provided data (reAddShipFromScene) and start the game (game.start())'. Update the Verification basis accordingly.

Optional human revised fix:
> 

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> 证据是 reAddShipFromScene(data)+game.start();"restore prior state"是方法名引申的解读,改成贴近代码的表述。

### R002: non_verifiable

- Severity: `major`
- Suggested action: `needs_human_check`
- SRS location: FR-004 / Section 4; DR-003
- Evidence IDs: E003

**Claim or gap**

FR-004 requires `ping` to be sent 'at the heartbeat interval' / 'at the configured heartbeat interval', and DR-003 references a heartbeat. The evidence shows `this.heartBeatInterval` used in setTimeout but does not provide the interval value or that it is configurable, so 'configured' is not fully verifiable.

**Model opinion**

The heartbeat send of `ping` with `null` is well supported (E003). However, calling it 'configured' implies external configurability not shown in evidence. The acceptance test references a 'configured heartbeat interval' that has no observable value in evidence, weakening verifiability.

**Recommended human check**

Verify where `heartBeatInterval` is initialized and whether it is configurable; capture its default value to make the acceptance criterion observable.

**Model proposed SRS change**

FR-004 and Verification: Replace 'at the configured heartbeat interval' with 'at the client heartbeat interval (heartBeatInterval)'; add a note that the concrete interval value should be confirmed from the client initialization code.

Optional human revised fix:
> 

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> ping+null 心跳由 E003 充分支撑,但 heartBeatInterval 的值与是否可配置未见,"configured"暗示外部可配置性,去掉并标值待核。

### R003: ambiguity

- Severity: `minor`
- Suggested action: `accept_as_issue`
- SRS location: FR-007 / Section 4; DR-006
- Evidence IDs: E004

**Claim or gap**

FR-007 states the client shall 'update the displayed or tracked player count'. Evidence (`this.game.setPlayers(data)`) confirms updating tracked player count but does not confirm a displayed UI element.

**Model opinion**

The 'displayed' wording introduces a UI claim not in evidence. Restrict to game-state update to stay evidence-backed.

**Recommended human check**

Check whether setPlayers updates any visible UI count or only internal game state.

**Model proposed SRS change**

FR-007: Replace 'update the displayed or tracked player count for the room' with 'update the tracked player count in game state (game.setPlayers(data))'.

Optional human revised fix:
> 

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> 证据只到 game.setPlayers(data),确认更新游戏状态,未见可见 UI 元素,"displayed"是无据的 UI 推断,删去。

### R004: traceability

- Severity: `minor`
- Suggested action: `needs_human_check`
- SRS location: FR-005 reconnect / Section 4; Section 3 reconnect context
- Evidence IDs: E004, E005

**Claim or gap**

Reconnect-on-close (FR-005) and the reconnect context (DR-004: room ID, player ID, index) are cited to E004/E005. The snippet shows `onClose` calling `this.reconnect()` and a send of `[..roomId, playerId, index]`, but the surrounding `reconnect()` function body is truncated, so the full reconnect flow is only partially evidenced.

**Model opinion**

The atomic facts (onClose -> reconnect; send array with roomId/playerId/index) are present, but the SRS implies a complete reconnect flow. Traceability is acceptable for the close-triggered reconnect, but the reconnect-context message assembly is shown only partially.

**Recommended human check**

Review the full `reconnect()` and connection-open handler to confirm the reconnect context message is sent on reconnect and the index semantics.

**Model proposed SRS change**

Section 3 Data exchange formats / DR-004: Add qualifier that the reconnect context array (roomId, playerId, index) is sent during the reconnect/open flow as observed in gameClient.js, pending confirmation of the full reconnect handler.

Optional human revised fix:
> 

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> onClose→reconnect 与 send [roomId, playerId, index] 是确证的原子事实,但 reconnect() 函数体截断,完整重连流程只能部分溯源,加待确认 qualifier。

### R005: unsupported_claim

- Severity: `minor`
- Suggested action: `needs_human_check`
- SRS location: Product functions summary / NFR-002 / C-001
- Evidence IDs: E001

**Claim or gap**

The SRS repeatedly states single-player support (Section 2: 'supports single-player and multiplayer play', User classes: 'single-player or multiplayer modes'). The only evidence is the README tagline 'single/multiplayer game' (E001); no single-player functional behavior is evidenced.

**Model opinion**

Single-player is mentioned in the README title but no functional evidence describes single-player flows. The SRS should attribute single-player only to the README description and avoid implying tested single-player functionality.

**Recommended human check**

Confirm whether any single-player mode logic exists in the codebase beyond the README tagline.

**Model proposed SRS change**

Section 2 User classes: Qualify single-player references as 'described in the README' only; or remove single-player claims from functional/user-class statements where no behavioral evidence exists.

Optional human revised fix:
> 

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> 唯一证据是 E001 标语"single/multiplayer game",无任何 single-player 功能流程证据,应标明仅出自 README、不暗示已测的单人功能。

### R006: architecture_detail

- Severity: `minor`
- Suggested action: `needs_human_check`
- SRS location: Section 2 Product perspective / C-003
- Evidence IDs: E002

**Claim or gap**

The SRS asserts the general client/server architecture and P2P-not-supported constraint, citing the README. The ground-truth architecture diagram (GeneralArchitecture.png) is referenced in README (E002 mentions 'Above in the image is illustrated the general architecture') but is not in the evidence pack, so architectural details (e.g., master/slave topology, message routing) are not independently verified.

**Model opinion**

The P2P limitation and WebSocket-over-HTTP are well supported textually. However, claims about the overall topology and slave/replica role would benefit from cross-checking the diagram, which was not provided in the evidence chunks.

**Recommended human check**

Open documentation/img/GeneralArchitecture.png and verify the SRS architecture/topology statements (client/server roles, slave/replica relationship) match the diagram.

**Model proposed SRS change**

Section 2: Add a note that architectural topology details should be confirmed against documentation/img/GeneralArchitecture.png; no text change required if the diagram confirms current claims.

Optional human revised fix:
> 

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> 图存在但不在证据包,拓扑细节未独立核实,补图引用加待确认 note;具体 topology 待开图。

### R007: traceability

- Severity: `minor`
- Suggested action: `probably_ignore`
- SRS location: Traceability Matrix NFR-005 vs NFR-005 in Section 5
- Evidence IDs: E002

**Claim or gap**

NFR-005 (asynchronous concurrent communication) is cited to E002 in the traceability matrix but Section 5 lists the same; the underlying README phrase is 'asynchronous communication that can occur concurrently' (E002). This is supported, but labeling it 'explicit' as a measurable NFR is weak since no concurrency metric is testable.

**Model opinion**

The claim is textually supported but is non-measurable as a quality attribute. Consider reclassifying as a design characteristic rather than a verifiable NFR, or add an observable acceptance criterion.

**Recommended human check**

Decide whether asynchronous/concurrent communication should be an NFR with an observable test or a design statement.

**Model proposed SRS change**

NFR-005: Either move to Section 7 Constraints/Design characteristics, or add an acceptance criterion such as 'multiple clients can communicate concurrently with the server without blocking', verified by Demonstration.

Optional human revised fix:
> 采用,加可观察验收准则。E002"asynchronous communication that can occur concurrently"有文本支撑但不可测,补一条可演示的并发验收即可,不必移走。

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> 标 explicit 没问题,但作为质量属性无 metric,加"多客户端可并发通信不阻塞"的演示准则使其可验证。
