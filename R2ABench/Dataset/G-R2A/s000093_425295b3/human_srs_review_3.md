# Human SRS Review Sheet

## Metadata

- Sample directory: `s000093_425295b3`
- Generated SRS: `final_srs.md`
- Evidence pack: `evidence_pack.json`
- Review model: `claude-opus-4-8`
- Generated at: `2026-06-05T16:07:23.704956Z`
- Raw model response: `model_srs_review_raw.md`
- Parse status: `parsed`

## Overall Model Opinion

- Recommendation: `revise`
- Confidence: `0.78`
- Rationale: The SRS is internally consistent and well-traced to the provided evidence chunks, but the evidence pack is almost entirely OpenVR SDK header/binding boilerplate (openvr_api.cs/.json) that is vendored, not authored by this repository. The SRS therefore describes the OpenVR SDK rather than VirtualMotionTracker's actual product (a virtual tracker driver controlled via OSC, per the repo name and architecture). This is a significant scope problem: the core product functionality is missing, and several requirements are attributed to the repo when they belong to the upstream SDK.

## Overall Human Decision

- [ ] Accept
- [ ] Reject
- [x] Partial accept

Reason:
> 五条全部成立,且属本批最严重的 scope 错位。E001/E002/E003/E005/E006 全部来自 vendored 的 Valve OpenVR SDK 头文件(openvr/headers/openvr_api.cs / .json),只有 E004(vmt_driver/.../legacy_binding_mycontroller.json)是本仓真正作者所写。结果是 SRS 在描述 OpenVR SDK 自身的 init/shutdown/path/struct,而非 VirtualMotionTracker 的核心产品(经 OSC/网络接收外部输入、向 SteamVR 注入虚拟 tracker 位姿)。total_score=100 但 FR-001~004、DR-001/003/004、C-001/002/004 多被误归属于本仓。R001/R002(critical)、R003/R005(major)需重做溯源与补核心需求;R004(minor)标注非穷尽。建议重检索 vmt_driver/ 与 README/Architecture.png 后实质性返工。

## Positive Observations

- Requirements that are present (FR-001..FR-005, NFRs, DRs) are each tied to specific evidence IDs with quoted-consistent content, and the traceability matrix is complete and internally coherent.
- The init/shutdown error semantics (Init_InterfaceNotFound, null return, pointer invalidation) in FR-002/FR-003 accurately reflect the E003 code snippet.
- The SRS appropriately uses verifiable acceptance criteria (Test/Inspection/Demonstration) for the requirements it does state.

## Candidate Issues

### R001: scope

- Severity: `critical`
- Suggested action: `needs_human_check`
- SRS location: Section 2 Product perspective; Section 4 FR-001..FR-003
- Evidence IDs: E003

**Claim or gap**

The SRS frames the product as an OpenVR scene application that initializes/validates/shuts down IVRSystem, but all of this behavior (E003) comes from `openvr/headers/openvr_api.cs`, which is the vendored Valve OpenVR SDK, not code authored by VirtualMotionTracker.

**Model opinion**

VirtualMotionTracker is, by repository name and architecture diagram, a virtual tracker driver that receives external input (OSC/network) and presents virtual trackers to SteamVR. The evidence pack retrieved only SDK header boilerplate, so the SRS describes OpenVR's own init/shutdown semantics and attributes them to this repository. FR-001/FR-002/FR-003 are SDK behaviors, not product requirements of this repo.

**Recommended human check**

Open `openvr/headers/openvr_api.cs` and confirm it is the upstream Valve OpenVR C# binding. Inspect the actual product source under `vmt_driver/` and the README to identify VMT's real functions (driver registration, OSC input, virtual device pose injection).

**Model proposed SRS change**

In Section 2 Product perspective and Section 1 Product scope, add a scoping note: 'Evidence E001-E003, E005-E006 originate from the vendored OpenVR SDK (openvr/headers/*) and describe upstream SDK behavior, not requirements authored by this repository.' Demote FR-001..FR-003 to a clearly labeled 'OpenVR SDK dependency behavior' subsection, or mark them as dependency assumptions rather than product functional requirements.

Optional human revised fix:
> 采用。E003 取自 openvr/headers/openvr_api.cs(Valve OpenVR C# binding 的 InitInternal2/IsInterfaceVersionValid/ShutdownInternal),是上游 SDK 的初始化/关闭语义,把它当作本仓 FR-001~003 属误归属。应加 scoping note 并把这些降级为依赖假设/SDK 行为子节,核心产品需求另立。

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> 路径 openvr/headers/* 已强烈表明 vendored;doc/Architecture.png 待开图确认 VMT 真实拓扑。

### R002: missing_requirement

- Severity: `critical`
- Suggested action: `needs_human_check`
- SRS location: Section 4 Functional Requirements (whole)
- Evidence IDs: none

**Claim or gap**

The SRS omits the core VirtualMotionTracker functionality: creating/driving virtual trackers and receiving external control input (the architecture diagram and repo name strongly imply an OSC/network-driven virtual tracker driver).

**Model opinion**

Given the repository is named VirtualMotionTracker and ships `vmt_driver/`, the central evidenced behavior should be virtual device pose injection driven by external commands. None of this appears in the SRS because retrieval surfaced only SDK headers and one binding file. This is the most important gap.

**Recommended human check**

Review README.md, the architecture diagram (doc/Architecture.png), and source under `vmt_driver/` to enumerate the real functional requirements (e.g., OSC command set, virtual tracker creation, pose updates, room-setup). Confirm whether OSC/UDP is the control interface.

**Model proposed SRS change**

Add functional requirements for the core product after human verification, e.g., FR-006 'The system shall create and drive virtual trackers in SteamVR based on external control input', and FR-007 'The system shall accept control commands over [OSC/UDP — verify] to set tracker pose/state'. Conditional: only add once README/driver source is reviewed.

Optional human revised fix:
> 采用。仓名 VirtualMotionTracker 且含 vmt_driver/,核心应是经外部命令注入虚拟 tracker 位姿,但检索只命中 SDK 头文件 + 一个 binding,SRS 完全缺失该核心功能。需读 README/doc/Architecture.png/vmt_driver/ 后补 OSC 命令集、虚拟 tracker 创建、位姿更新、room-setup 等真实需求。

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> 这是本样本最重要的缺口;OSC/UDP 控制接口为强假设,需代码确认。

### R003: traceability

- Severity: `major`
- Suggested action: `accept_as_issue`
- SRS location: Section 9 Traceability Matrix; DR-001/DR-004; FR-004
- Evidence IDs: E001, E002, E005, E006

**Claim or gap**

Several requirements are traced to vendored SDK header constants (E001, E002, E005, E006) as if they were product-authored data/interface requirements, giving misleadingly high confidence ('explicit', 'High').

**Model opinion**

Exposing `/user/foot/left` etc. (E001/E002) and using `TrackedDevicePose_t`/render-model structs (E005/E006) is simply the OpenVR SDK API surface. Attributing these as repository requirements inflates traceability quality. The evidence is genuine but mis-attributed to the product's scope.

**Recommended human check**

Confirm these constants/structs live only under `openvr/headers/` and are not redefined by VMT's own driver code. If so, mark them as upstream SDK surface, not product requirements.

**Model proposed SRS change**

In Section 9, add an 'Origin' column distinguishing 'repository-authored' vs 'vendored OpenVR SDK'. Mark FR-004, DR-001, DR-003, DR-004 as vendored-SDK-origin and lower their confidence/relevance accordingly, or move them to an Assumptions/Dependencies appendix.

Optional human revised fix:
> 采用。/user/foot/left 等(E001/E002)与 TrackedDevicePose_t/RenderModel_* 结构(E005/E006)都是 OpenVR SDK API 表面,标 explicit/High 会虚高溯源质量。增设 Origin 列区分"本仓所写 / vendored SDK",将 FR-004、DR-001/003/004 标为 vendored 来源并相应降权或移入依赖附录。

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> 证据真实但归属错位;Origin 列是区分 vendored 与自研的好做法,可推广到其他含 vendored 子模块的样本。

### R004: ambiguity

- Severity: `minor`
- Suggested action: `needs_human_check`
- SRS location: FR-005 / Section 8 acceptance basis
- Evidence IDs: E004

**Claim or gap**

E004 shows the binding mode 'button' and parameter sub_mode 'complex' and a 'Default binding for Sampl...' name, but FR-005 only captures three input->output mappings and omits mode/parameter semantics; the binding file is truncated.

**Model opinion**

The mapping claims are evidence-backed, but the binding file text is truncated ('Default binding for Sampl...'), so additional sources/inputs may exist. FR-005 should not be presented as exhaustive.

**Recommended human check**

Open the full `legacy_binding_mycontroller.json` to confirm whether additional input sources/mappings or left-hand bindings exist beyond the three evidenced.

**Model proposed SRS change**

In FR-005 and its acceptance basis, change wording to 'shall map at least the following right-hand inputs ...' and add a note that mode='button' with sub_mode='complex' applies; verify completeness against the full file.

Optional human revised fix:
> 采用。E004 文本在"Default binding for Sampl..."处截断,可能存在更多 input source/左手绑定;三条右手映射有据但不应呈现为穷尽,改"at least"并补 mode=button/sub_mode=complex 语义。

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> E004 是本仓唯一真正自研证据,值得据全文 legacy_binding_mycontroller.json 完整化。

### R005: architecture_detail

- Severity: `major`
- Suggested action: `needs_human_check`
- SRS location: Section 3 Communication interfaces
- Evidence IDs: none

**Claim or gap**

The SRS states 'No network or inter-process communication protocol is directly evidenced', but the repository's architecture (and ground-truth diagram doc/Architecture.png) for a virtual motion tracker driver typically centers on a network/OSC control channel.

**Model opinion**

This is likely an understatement caused by retrieval gaps. A virtual tracker driver receiving external pose data almost always exposes a network/IPC interface. The 'no communication interface evidenced' claim should be re-examined against the diagram and driver source.

**Recommended human check**

Inspect doc/Architecture.png and driver source for a UDP/OSC listener or named-pipe/shared-memory interface. If present, add a communication-interface requirement.

**Model proposed SRS change**

Replace the Section 3 'Communication interfaces' statement with verified content. Conditional: if an OSC/UDP control channel exists, add 'The system shall receive tracker control input over [protocol/port — verify].'

Optional human revised fix:
> 采用。"No network or inter-process communication protocol is directly evidenced"很可能是检索缺口所致:虚拟 tracker 驱动接收外部位姿几乎必然有 网络/OSC/IPC 通道。应据 doc/Architecture.png 与驱动源(UDP/OSC listener、named pipe、shared memory)核实后补通信接口需求。

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> 与 R002 同源:核心控制通道的缺失是检索只命中 SDK 头文件的直接后果。
