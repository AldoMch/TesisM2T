<!-- human_srs_review_A.md 由审阅者 A 生成。保留原始 human_srs_review.md。所有人类的判断都是英语的。 -->

# 人类 SRS 审查表

## 元数据

- 示例目录：`s000093_425295b3`
- 生成SRS：`final_srs.md`
- 证据包：`evidence_pack.json`
- 评测型号：`claude-opus-4-8`
- 生成于：`2026-06-05T16:07:23.704956Z`
- 原始模型响应：`model_srs_review_raw.md`
- 解析状态：`parsed`

## 总体模型意见

- 推荐：`revise`
- 置信度：`0.78`
- 理由：SRS 内部一致，并且可以很好地追踪到所提供的证据块，但证据包几乎完全是由此存储库提供而非创作的 OpenVR SDK 标头/绑定样板文件 (openvr_api.cs/.json)。因此，SRS 描述的是 OpenVR SDK，而不是 VirtualMotionTracker 的实际产品（根据存储库名称和架构，通过 OSC 控制的虚拟跟踪器驱动程序）。这是一个重大的范围问题：核心产品功能缺失，并且当某些需求属于上游 SDK 时，它们会归因于存储库。

## 人类整体决策

- [ ] 接受
- [ ] 拒绝
- [x] 部分接受

原因：
> ACCEPT=4，PARTIAL_ACCEPT=1，REJECT=0，PARTIAL_ACCEPT=0。

## 积极的观察

- 存在的要求（FR-001..FR-005、NFRs、DRs）均与具有引用一致内容的具体证据 IDs 相关联，并且可追溯性矩阵是完整且内部一致的。
- FR-002/FR-003 中的初始化/关闭错误语义（Init_InterfaceNotFound、空返回、指针失效）准确反映了 E003 代码片段。
- SRS 对其规定的要求适当地使用可验证的验收标准（测试/检查/演示）。

## 候选人问题

### R001：范围

- 严重性：`critical`
- 建议采取的措施：`partial_accept_as_issue`
- SRS 位置：第二部分产品视角；第 4 节 FR-001..FR-003
- 证据IDs：E003

**索赔或差距**

SRS 将产品设计为 OpenVR 场景应用程序，用于初始化/验证/关闭 IVRSystem，但所有这些行为 (E003) 来自 `openvr/headers/openvr_api.cs`，即供应商的 Valve OpenVR SDK，而不是代码作者：VirtualMotionTracker。

**模型意见**

根据存储库名称和架构图，VirtualMotionTracker 是一个虚拟跟踪器驱动程序，用于接收外部输入（OSC/网络）并向 SteamVR 提供虚拟跟踪器。证据包仅检索 SDK 标头样板，因此 SRS 描述了 OpenVR 自己的 init/shutdown 语义并将其归因于此存储库。 FR-001/FR-002/FR-003 是 SDK 行为，而不是此存储库的产品要求。

**推荐人工检查**

打开 `openvr/headers/openvr_api.cs` 并确认它是上游 Valve OpenVR C# 绑定。检查 `vmt_driver/` 和 README 下的实际产品源，以识别 VMT 的真实功能（驱动程序注册、OSC 输入、虚拟设备位姿注入）。

**型号建议更改 SRS**

在第 2 节产品视角和第 1 节产品范围中，添加范围说明：“证据 E001-E003、E005-E006 源自供应商 OpenVR SDK (openvr/headers/*) 并描述上游SDK 行为，不是此存储库编写的要求。将 FR-001..FR-003 降级为明确标记的“OpenVR SDK 依赖行为”小节，或将它们标记为依赖假设而不是产品功能需求。

可选的人工修订修复：
> 在第 1 节 产品范围 和第 2 节 产品视角 中，把当前“OpenVR 场景应用初始化”为主体的描述改成：VirtualMotionTracker 的核心范围是连接用户应用、VMT Manager、VMT Driver 与 OpenVR/SteamVR：用户应用向 VMT Manager 提供外部控制输入，VMT Manager 与 VMT Driver 通过共享内存中的 JSON 消息交换数据，VMT Driver 作为 OpenVR 驱动与 SteamVR 集成。OpenVR SDK 的初始化、接口版本检查、关闭和路径常量属于外部依赖行为，不作为本仓库自身编写的核心功能需求。在第 4 节中，将 FR-001、FR-002、FR-003 从“功能需求”降级为“OpenVR SDK 依赖行为”或移动到第 7 节约束/依赖中。

**人为决定**

- [ ] 接受
- [ ] 拒绝
- [x] 部分接受（`PARTIAL_ACCEPT`：混合声明；有些有效，有些无效）

可选的人工注释：
> 部分接受。原因是 openvr/headers/openvr_api.cs 明确是 Valve OpenVR 自动生成绑定，不是 VirtualMotionTracker 自己实现的产品功能；但这些内容仍可作为外部依赖/约束保留，不能直接当作本仓库核心 FR。

### R002：缺少需求

- 严重性：`critical`
- 建议采取的措施：`accept_as_issue`
- SRS 位置：第四节功能需求（全）
- 证据 IDs：无

**索赔或差距**

SRS 省略了核心 VirtualMotionTracker 功能：创建/驱动虚拟跟踪器并接收外部控制输入（架构图和存储库名称强烈暗示 OSC/网络驱动的虚拟跟踪器驱动程序）。

**模型意见**

鉴于存储库名为 VirtualMotionTracker 并附带 `vmt_driver/`，中央证据行为应该是由外部命令驱动的虚拟设备姿势注入。这些都不会出现在 SRS 中，因为检索仅显示 SDK 标头和一个绑定文件。这是最重要的差距。

**推荐人工检查**

查看 README.md、架构图 (doc/Architecture.png) 以及 `vmt_driver/` 下的源代码，以枚举真实的功能需求（e.g.、OSC 命令集、虚拟跟踪器创建、姿势更新、房间设置）。确认OSC/UDP是否为控制接口。

**型号建议更改 SRS**

添加人工验证后核心产品的功能要求，e.g.、FR-006“系统应根据外部控制输入在SteamVR中创建并驱动虚拟跟踪器”和FR-007“系统应接受[OSC/UDP - 验证]的控制命令以设置跟踪器姿势/状态”。有条件：仅在审核 README/驱动程序源后添加。

可选的人工修订修复：
> 在第 4 节新增功能需求：FR-006：系统应作为 Virtual Motion Tracker 管理端接收来自用户应用的外部控制输入，并将其作为虚拟运动跟踪状态更新的数据来源。FR-007：系统应在 VMT Manager 与 VMT Driver 之间通过共享内存交换 JSON 消息，支持管理端到驱动端、驱动端到管理端的双向消息通道。FR-008：系统应提供可被 OpenVR/SteamVR 加载的 VMT 驱动工件，使虚拟运动跟踪能力能够通过 OpenVR 驱动接口暴露给运行时。如果要写 OSC，可放在接口说明里写“架构图标注为 OSC，端口和命令集未在当前证据中确认”。

**人为决定**

- [x] 接受
- [ ] 拒绝
- [ ] 部分接受（`PARTIAL_ACCEPT`：混合声明；有些有效，有些无效）

可选的人工注释：
> 接受，但要收窄。原因是 SRS 确实漏掉了 VMT 的核心产品范围；架构图显示 User Application → OSC → VMT Manager，Manager 与 Driver 通过共享内存 JSON 通信，Driver 连接 OpenVR/SteamVR。不过当前固定提交中未看到完整 OSC/UDP 监听实现，所以不要写具体端口或完整命令集。

### R003：可追溯性

- 严重性：`major`
- 建议采取的措施：`accept_as_issue`
- SRS 位置：第 9 节可追溯性矩阵； DR-001/DR-004； FR-004
- 证据 IDs：E001、E002、E005、E006

**索赔或差距**

一些要求可追溯到供应商的 SDK 标头常量（E001、E002、E005、E006），就好像它们是产品编写的数据/接口要求一样，从而给出了误导性的高置信度（“显式”、“高”）。

**模型意见**

公开 `/user/foot/left` 等 (E001/E002) 并使用 `TrackedDevicePose_t`/渲染模型结构 (E005/E006) 就是 OpenVR SDK API 表面。将这些归因于存储库要求会提高可追溯性质量。证据是真实的，但错误地归因于产品的范围。

**推荐人工检查**

确认这些常量/结构仅存在于 `openvr/headers/` 下，并且未被 VMT 自己的驱动程序代码重新定义。如果是这样，请将它们标记为上游 SDK 表面，而不是产品要求。

**型号建议更改 SRS**

在第 9 节中，添加“来源”列，以区分“存储库创作”与“供应商 OpenVR SDK”。将 FR-004、DR-001、DR-003、DR-004 标记为供应商 SDK-origin，并相应降低其置信度/相关性，或将其移至假设/依赖性附录。

可选的人工修订修复：
> 接受模型意见。

**人为决定**

- [x] 接受
- [ ] 拒绝
- [ ] 部分接受（`PARTIAL_ACCEPT`：混合声明；有些有效，有些无效）

可选的人工注释：
> 接受。原因是 E001、E002、E005、E006 都来自 OpenVR SDK header/json，不应作为“仓库自研产品需求”的高置信度证据。

### R004：歧义

- 严重性：`minor`
- 建议采取的措施：`accept_as_issue`
- SRS 位置：FR-005 / 第8节验收依据
- 证据IDs：E004

**索赔或差距**

E004 显示绑定模式“button”和参数 sub_mode“complex”以及“Sample... 的默认绑定”名称，但 FR-005 仅捕获三个输入->输出映射并省略模式/参数语义；绑定文件被截断。

**模型意见**

映射声明有证据支持，但绑定文件文本被截断（“样本的默认绑定...”），因此可能存在其他源/输入。 FR-005 不应呈现为详尽无遗。

**推荐人工检查**

打开完整的 `legacy_binding_mycontroller.json` 以确认除了三个证据之外是否还存在其他输入源/映射或左侧绑定。

**型号建议更改 SRS**

在 FR-005 及其验收基础中，将措辞更改为“应至少映射以下右侧输入...”并添加注释，说明 mode='button' 和 sub_mode='complex' 适用；验证完整文件的完整性。

可选的人工修订修复：
> 在 FR-005 中将系统行为改为：对于 mycontroller 的旧版绑定，系统应以 button 模式和 complex 子模式将三个右手输入映射到 legacy 动作。第 8 节 FR-005 验收依据改为：检查完整 legacy binding JSON，确认 controller_type 为 mycontroller，sources 包含上述三条映射，且每条映射的 mode 为 button、parameters.sub_mode 为 complex。

**人为决定**

- [x] 接受
- [ ] 拒绝
- [ ] 部分接受（`PARTIAL_ACCEPT`：混合声明；有些有效，有些无效）

可选的人工注释：
> 接受，但不建议简单改成“至少”。原因是完整 legacy_binding_mycontroller.json 确认该 legacy binding 文件确实只有 3 条 source 映射；问题主要是 SRS 漏掉了 mode=button、sub_mode=complex，并且没有说明该要求只覆盖 legacy binding，不覆盖其他 mycontroller 绑定文件。

### R005：架构_详细信息

- 严重性：`major`
- 建议采取的措施：`accept_as_issue`
- SRS 位置：第三节 通讯接口
- 证据 IDs：无

**索赔或差距**

SRS 声明“没有直接证明网络或进程间通信协议”，但虚拟运动跟踪器驱动程序的存储库架构（和真实图文档/Architecture.png）通常以网络/OSC 控制通道为中心。

**模型意见**

这可能是由检索差距引起的轻描淡写。接收外部姿态数据的虚拟跟踪器驱动程序几乎总是公开网络/IPC 接口。应根据图表和驱动程序源重新检查“无通信接口证据”的说法。

**推荐人工检查**

检查 UDP/OSC 侦听器或命名管道/共享内存接口的 doc/Architecture.png 和驱动程序源。如果存在，请添加通信接口要求。

**型号建议更改 SRS**

将第 3 节“通信接口”声明替换为经过验证的内容。条件：如果存在 OSC/UDP 控制通道，请添加“系统应通过 [协议/端口 — 验证]接收跟踪器控制输入。”

可选的人工修订修复：
> 将第 3 节 通信接口 替换为：外部控制输入接口：用户应用通过 OSC 向 VMT Manager 提供控制输入。内部进程间通信接口：VMT Manager 与 VMT Driver/driver mock 通过共享内存交换 JSON 字符串，使用管理端到驱动端和驱动端到管理端两个方向的通道，并通过发送计数、握手计数和消息长度字段控制同步。OpenVR 运行时接口：VMT Driver 通过 OpenVR Driver 接口与 SteamVR/OpenVR 运行时集成。

**人为决定**

- [x] 接受
- [ ] 拒绝
- [ ] 部分接受（`PARTIAL_ACCEPT`：混合声明；有些有效，有些无效）

可选的人工注释：
> 接受，但模型的 OSC/UDP 推断要修正。原因是 SRS 说“没有直接证实网络或 IPC”不准确；架构图显示 OSC 输入和共享内存 JSON，源码也证实了共享内存通道。当前源码没有确认具体 UDP 端口或 OSC 命令集。
