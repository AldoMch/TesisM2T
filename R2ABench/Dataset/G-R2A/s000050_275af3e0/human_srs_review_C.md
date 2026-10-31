<!-- human_srs_review_A.md 由审阅者 A 生成。保留原始 human_srs_review.md。所有人类的判断都是英语的。 -->

# 人类 SRS 审查表

## 元数据

- 示例目录：`s000050_275af3e0`
- 生成SRS：`final_srs.md`
- 证据包：`evidence_pack.json`
- 评测型号：`claude-opus-4-8`
- 生成于：`2026-06-05T15:51:08.828418Z`
- 原始模型响应：`model_srs_review_raw.md`
- 解析状态：`parsed`

## 总体模型意见

- 推荐：`revise`
- 置信度：`0.72`
- 理由：SRS 通常可以很好地追踪到证据包，并且范围保守，但它错过了项目的核心身份（根据架构图和存储库名称，hAFL2 作为 Hyper-V 虚拟机管理程序/分布式云模糊器），并且包含一些支持比断言更弱的声明。追溯到 E003 的几个约束实际上属于 E004，反之亦然，并且 C-005“重新启动 VM”细节是部分推断的。范围中引用的架构图根本没有在 SRS 中表示。

## 人类整体决策

- [ ] 接受
- [ ] 拒绝
- [x] 部分接受

原因：
> ACCEPT=3，PARTIAL_ACCEPT=1，REJECT=3，PARTIAL_ACCEPT=0。

## 积极的观察

- 要求的范围保守地限定为检索到的证据块，并且大多数声明都带有明确的证据 IDs。
- 强大的可追溯性矩阵将 FR/NFR/DR/C 项目与具有置信度评级的证据联系起来。
- 确定性突变不变量（NFR-002 有效负载恢复、NFR-003 汉明距离）是从 E005/E006 中的测试代码准确导出的，并且是真正可验证的。
- 验证和验收部分为每个要求提供了具体的、大部分可测试的标准。
- 从 E003 中准确捕获 Windows 帮助程序二进制角色 (packet_sender.exe / loader.exe)。

## 候选人问题

### R001：范围

- 严重性：`major`
- 建议采取的措施：`accept_as_issue`
- SRS 位置：第 1 节产品范围/第 2 节产品视角
- 证据 IDs：E003、E004

**索赔或差距**

SRS 将 hAFL2 狭义地定义为“模糊测试支持工具集”（测试运行程序、Linux 启动脚本、Windows 二进制文件），并忽略了该项目作为 Hyper-V 虚拟机管理程序/分布式云模糊测试系统的核心身份，这由存储库名称 (hAFL2)、根/子分区 VM 术语和引用的术语暗示Architecture.png。

**模型意见**

证据包块（E003、E004）重复引用根分区VM、子分区VM、发送到根分区的netvsc数据包以及Hyper-V风格的虚拟化。地面实况图像 URL 是一个架构图。 SRS 通过将其视为支持工具集而不是虚拟机管理程序模糊平台来低估系统范围。尽管可用的文本块在整体架构上很少，但这是一个有意义的范围轻描淡写。

**推荐人工检查**

打开存储库 README 和 Architecture.png 以确认 hAFL2 是 Hyper-V/分布式云管理程序模糊器。如果得到确认，请扩大产品范围/视角来描述虚拟机管理程序模糊测试架构（根分区与子分区、netvsc 目标）。

**型号建议更改 SRS**

在第 2 节“产品视角”中，添加：“hAFL2 是一个针对 Hyper-V 虚拟化堆栈的模糊测试系统，跨根分区和子分区 VMs 运行，并对根分区的 netvsc 网络路径进行模糊测试。已证实的工件（测试运行程序、Linux 启动脚本、Windows 帮助程序二进制文件/驱动程序）是这个更大的模糊测试平台的组件。以图表/README 确认为条件。

可选的人工修订修复：
> 第 1 节 Product Scope / 第 2 节 Product Perspective。建议改成：hAFL2 是一个基于 kAFL 的 hypervisor fuzzing 系统，主要证据显示其用于 fuzz Hyper-V 虚拟化栈，尤其是 Hyper-V virtual switch / VMSwitch 路径。当前证据覆盖的测试入口、Linux userspace launch workflow、Windows helper binaries、harness driver 和 crash monitoring driver 都是该 fuzzing 平台的组成部分。

**人为决定**

- [x] 接受
- [ ] 拒绝
- [ ] 部分接受（`PARTIAL_ACCEPT`：混合声明；有些有效，有些无效）

可选的人工注释：
> 当前 SRS 把 hAFL2 写成“fuzzing support toolset”，确实低估了范围。README 明确说 hAFL2 是基于 kAFL 的 hypervisor fuzzer，tutorial 明确聚焦 Hyper-V / vmswitch.sys。

### R002：架构_详细信息

- 严重性：`major`
- 建议采取的措施：`accept_as_issue`
- SRS 位置：第 1 节参考资料/第 3 节外部接口
- 证据IDs：E004

**索赔或差距**

命名为真实图像的架构图 (Architecture.png) 未在 SRS 中的任何位置引用或反映，并且 netvsc 到根分区数据包路径 (E004) 未捕获为接口/数据流要求。

**模型意见**

E004 明确提到“使用它通过 netvsc 全局列表指针将数据包发送到根分区”。这是 Windows/Hyper-V 模糊测试路径的核心数据流细节，SRS 仅将其间接捕获为“数据包发送 IOCTL”。应检查架构图以确认通信拓扑。

**推荐人工检查**

检查 Architecture.png 和 tutorial.md 以确认 netvsc->root-partition 数据包流以及它是否应该是显式通信接口要求。

**型号建议更改 SRS**

在第 3 节通信接口中，添加：“Windows 模糊测试工作流程定位 netvsc 全局列表指针，以将数据包从子分区发送到根分区。来源：E004。将架构图 URL 添加到第 1 节参考中，并注意架构拓扑记录在 Architecture.png 中。

可选的人工修订修复：
> 第 3 节 Communication Interfaces建议新增：Windows Hyper-V fuzzing workflow 应支持从 child partition harness 向 root partition 中的 VMSwitch 发送 fuzzing payload；该路径依赖 netvsc / VMBus 相关网络通道，并由 root partition crash monitoring 将崩溃信息反馈给 hAFL2。

**人为决定**

- [x] 接受
- [ ] 拒绝
- [ ] 部分接受（`PARTIAL_ACCEPT`：混合声明；有些有效，有些无效）

可选的人工注释：
> 架构图和 tutorial 都确认 root partition、child partition、VMSwitch、harness、crash monitoring 与 hAFL2 的数据流关系；当前 SRS 只写了 packet-sending IOCTL，没有表达“child partition 向 root partition / VMSwitch 发送 fuzzing payload”的核心路径。

### R003：可追溯性

- 严重性：`major`
- 建议采取的措施：`accept_as_issue`
- SRS 位置：C-005、C-006（第 7 节）和追溯矩阵
- 证据 IDs：E003、E004

**索赔或差距**

约束 C-005（DSE 禁用 + VM 重新启动）追踪到 E003，但“完成后重新启动子分区 VM”文本出现在 E003 中，而配置关闭状态详细信息属于E004。 C-006 已正确追溯到 E004，但应重新检查 C-005 和 C-006 之间的证据分配的准确性。

**模型意见**

E003 确实包含“禁用子分区 DSE ...（完成后重新启动子分区 VM）”，因此 C-005 的 E003 跟踪是支持的。但是，C-005 的 SRS 验证表断言“DSE 禁用是从提升的命令提示符执行的，并且子分区 VM 已重新启动” - 提升的命令提示符详细信息位于 E003 中，并且没有问题。这是临界点；主要关注的是确保没有交叉归因错误。低至中风险。

**推荐人工检查**

重新读取 E003 和 E004 以确认 C-005 映射到 E003（DSE + 提升的提示 + 重新启动），C-006 映射到 E004（VM 在配置前关闭）。确认没有捏造任何细节。

**型号建议更改 SRS**

如果痕迹验证，则不会有任何变化。如果归属错误，请相应更正 C-005/C-006 的源证据列。

可选的人工修订修复：
> 

**人为决定**

- [ ] 接受
- [x] 拒绝
- [ ] 部分接受（`PARTIAL_ACCEPT`：混合声明；有些有效，有些无效）

可选的人工注释：
> 重新核对后，C-005 和 C-006 的证据分配基本正确：DSE、elevated command prompt、restart child partition VM 都在 E003 / tutorial 对应段落中；child partition VM 配置前需关闭属于 E004。没有发现明显交叉归因错误。

### R004：歧义

- 严重性：`minor`
- 建议采取的措施：`probably_ignore`
- SRS 位置：FR-002 / E002
- 证据IDs：E002

**索赔或差距**

FR-002 和 E002 声明二进制文件“通过 [空白] 启动”——证据文本显示启动机制被截断/缺失（“通过 . 启动”）。 SRS 并未标记具体的发射机制从证据中未知。

**模型意见**

证据块 E002 有一个空白：“打包到 initrd 中并通过 启动。”发射传输（可能是 QEMU/kAFL）被省略。 SRS 合理地抽象为“在 kAFL 中启动”，但不应暗示超出 E002 提供的经过验证的启动机制。

**推荐人工检查**

检查完整的tests/user_bench/README.md以恢复删除的启动机制（e.g.、QEMU/kAFL调用）。

**型号建议更改 SRS**

在 FR-002 系统行为中，软化为：“系统应构建一个包含所选二进制文件的 initrd，并在 kAFL 中启动它（每个 user_bench 启动脚本的特定启动传输）。” （可选）添加一个假设，即在启动脚本中定义了确切的启动命令。

可选的人工修订修复：
> 

**人为决定**

- [ ] 接受
- [x] 拒绝
- [ ] 部分接受（`PARTIAL_ACCEPT`：混合声明；有些有效，有些无效）

可选的人工注释：
> 完整 tests/user_bench/README.md 恢复了被证据块截断的内容：目标 binary 被打包进 initrd，并通过 qemu -kernel -initrd 启动；当前 SRS 写“launch it in kAFL”并不错误，只是不够具体。

### R005：不支持的声明

- 严重性：`minor`
- 建议采取的措施：`partial_accept_as_issue`
- SRS 位置：C-001（许可证）追溯到 E001、E006
- 证据 IDs：E001、E006

**索赔或差距**

C-001 声明存储库工件已获得基于 E001/E006 的 AGPL-3.0 或更高版本的许可，两者都带有 Intel Corporation 版权标头。 SRS 没有注意到这些是继承的 kAFL/Intel 文件，这可能会误导存储库自己的许可。

**模型意见**

E001 和 E006 均标有“版权所有 (C) 2019-2020 Intel Corporation SPDX-许可证标识符：AGPL-3.0-或更高版本”。这些是继承的 kAFL 文件。从两个 Intel 主导的测试文件断言整个存储库是 AGPL-3.0 或更高版本是一种轻微的过度概括。该约束可能是正确的，但痕迹证据很窄。

**推荐人工检查**

检查存储库根 LICENSE 文件以确认项目范围的许可证，而不是依赖继承的 kAFL 文件中的每个文件标头。

**型号建议更改 SRS**

将 C-001 改写为：“有证据的源文件（kAFL-Fuzzer 测试实用程序）携带 AGPL-3.0 或更高版本的 SPDX 标头（英特尔公司）。根据根 LICENSE 文件确认存储库范围的许可证。来源：E001、E006。

可选的人工修订修复：
> C-001 和 Traceability Matrix 中 C-001建议改成：仓库根许可证为 BSD 3-Clause；证据中的 kAFL-derived 测试文件保留 AGPL-3.0-or-later SPDX 文件头。使用或再分发时应同时遵守仓库级许可证和相关子文件许可证声明。

**人为决定**

- [ ] 接受
- [ ] 拒绝
- [x] 部分接受（`PARTIAL_ACCEPT`：混合声明；有些有效，有些无效）

可选的人工注释：
> E001/E006 中的 kAFL 测试文件确实带有 AGPL-3.0-or-later SPDX 头；但根 LICENSE 是 BSD 3-Clause，当前 C-001 和 traceability 中“Use is constrained by AGPL”容易误导为整个仓库都是 AGPL。

### R006：缺少需求

- 严重性：`minor`
- 建议采取的措施：`probably_ignore`
- SRS 位置：第 4 节功能要求 / FR-001
- 证据 IDs：E001、E005

**索赔或差距**

E001 导入并运行随机、确定性 AND 破坏测试模块（rand_main、deter_main、havoc_main），但仅捕获确定性突变行为 (NFR-002/003) 作为详细的非功能需求。 FR-001 中提到了 havoc 和 random 测试套件，但没有相应的正确性要求。

**模型意见**

这是一个较小的完整性差距。 FR-001涵盖了所有三个套件的运行，这在功能层面上已经足够了。确定性细节之所以存在，是因为 E005/E006 提供了它；随机/破坏内部结构不在证据包中，因此无法得出进一步的要求。保持原样是可以接受的，但值得注意的是不对称性。

**推荐人工检查**

确认没有可用的 test_random.py / test_havoc_handler.py 证据来支持额外的 NFRs；如果存在，请考虑对称 NFRs。

**型号建议更改 SRS**

除非检索到随机/破坏性测试证据，否则不需要进行更改。如果检索到，请为这些套件添加 NFRs 镜像 NFR-002/003。

可选的人工修订修复：
> 

**人为决定**

- [ ] 接受
- [x] 拒绝
- [ ] 部分接受（`PARTIAL_ACCEPT`：混合声明；有些有效，有些无效）

可选的人工注释：
> 我拒绝将此作为必需的 SRS 缺陷。该模型并未表明第 4 节功能需求 / FR-001 中的声明对正确性、可验证性、范围或可追溯性造成重大损害，或者所关注的只是低价值的措辞偏好。证据依据：E001、E005。对于此问题，无需进行必要的 SRS 更改。

### R007：不可验证

- 严重性：`minor`
- 建议采取的措施：`accept_as_issue`
- SRS 位置：FR-003 / 验证“演示”
- 证据IDs：E002

**索赔或差距**

FR-003 验收标准（“通过嵌入式 forkserver 在来宾内部展示 AFL 风格的 I/O”）很难作为具体的、可测试的验收检查来观察； “AFL-style I/O”未在操作上定义。

**模型意见**

证据 (E002) 表明 forkserver 将 kAFL 超级调用映射到 AFL 样式的 I/O，因此支持该要求，但验收标准很难客观验证。考虑将其与可观察的结果（成功的模糊测试运行/覆盖反馈）联系起来，而不是抽象的“AFL 式 I/O”。

**推荐人工检查**

确定演示 forkserver 操作的可观察信号（e.g.，在 kAFL 下成功启动目标并具有覆盖反馈）。

**型号建议更改 SRS**

将 FR-003 接受修改为：“用户空间目标在 kAFL 下启动并运行，并且 forkserver 处于活动状态，这通过成功的模糊测试迭代/覆盖反馈得到了证明。”保留来源 E002。

可选的人工修订修复：
> 第 8 节 FR-003 验收标准建议改成：用户空间目标能够在 kAFL workflow 下启动并执行，forkserver 处于活动状态；通过成功 fuzzing iteration、覆盖反馈或等价运行反馈证明 guest-side I/O 映射生效。同时 FR-003 Output 可改成：可观察的 fuzzing iteration / coverage feedback，而不是仅写 “AFL-style I/O behavior”。

**人为决定**

- [x] 接受
- [ ] 拒绝
- [ ] 部分接受（`PARTIAL_ACCEPT`：混合声明；有些有效，有些无效）

可选的人工注释：
> FR-003 的“exhibits AFL-style I/O”太抽象，不容易验收；证据支持 forkserver 映射行为，但验收标准应绑定到可观察结果。
