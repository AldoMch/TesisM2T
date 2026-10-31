<!-- human_srs_review_A.md 由审阅者 A 生成。保留原始 human_srs_review.md。所有人类的判断都是英语的。 -->

# 人类 SRS 审查表

## 元数据

- 示例目录：`s000067_4d85c913`
- 生成SRS：`final_srs.md`
- 证据包：`evidence_pack.json`
- 评测型号：`claude-opus-4-8`
- 生成于：`2026-06-05T16:01:46.135088Z`
- 原始模型响应：`model_srs_review_raw.md`
- 解析状态：`parsed`

## 总体模型意见

- 推荐：`revise`
- 置信度：`0.74`
- 理由：SRS 对于大多数声明来说都是有迹可循且保守的，但有几个要求断言了证据被截断或薄弱的细节（Kretprobe、NFR-003“已测试”、DR-004 CLI 字段、命名方案详细信息）。一些非功能性和推断性的项目需要人工验证，并且 DR-004 引用的证据并不完全支持其规定的限制。

## 人类整体决策

- [ ] 接受
- [ ] 拒绝
- [x] 部分接受

原因：
> ACCEPT=4，PARTIAL_ACCEPT=1，REJECT=0，PARTIAL_ACCEPT=0。

## 积极的观察

- 强大、保守的可追溯性：几乎每个 FR/NFR 都引用具体证据 IDs 并区分显式置信度与推断置信度（e.g.、NFR-004 标记为推断/低）。
- FR-007（“未设置处理程序 -> 返回 0，不执行任何操作”）精确地基于 E001 并且是可测试的。
- 数据要求 DR-003 准确反映来自 E005 的 Event_Args 字段（位置/类型/名称/后缀/hash_func）。
- 范围适当地限于库和参考 CLI，而不会发明不受支持的功能。

## 候选人问题

### R001：可追溯性

- 严重性：`minor`
- 建议采取的措施：`accept_as_issue`
- SRS 位置：DR-004
- 证据IDs：E004

**索赔或差距**

DR-004 列出了 CLI 事件结构字段 `ProgramID`、`Pids`、`ELFPath` 并引用 E004；这是受支持的，但“由 CLI 跟踪流使用”约束是部分推论的。

**模型意见**

E004清楚地显示了`type Event struct { ProgramID uint64; Pids []int; ELFPath string }`，因此字段名称得到了很好的支持。功能角色（“跟踪命令事件选择数据”）是一个合理的解释，但没有在证据中明确说明。

**推荐人工检查**

在 cli/cmd/trace.go 中确认此事件结构用于跟踪事件选择而不是其他目的。

**型号建议更改 SRS**

DR-004 说明：将 cli/cmd/trace.go 中的“CLI 端事件结构”替换为“CLI 端事件结构包括...”，声明字段 ProgramID (uint64)、Pids ([]int)、ELFPath （字符串）；其功能作用是推断出来的，未经证实。

可选的人工修订修复：
> 第 6 节 DR-004。改为：CLI trace command arguments shall be parsed into an event registration structure containing ProgramID, Pids, and ELFPath; this structure is used by the trace command to register handler programs for selected program IDs and process IDs.

**人为决定**

- [x] 接受
- [ ] 拒绝
- [ ] 部分接受（`PARTIAL_ACCEPT`：混合声明；有些有效，有些无效）

可选的人工注释：
> cli/cmd/trace.go 中确实有 Event 结构，字段是 ProgramID、Pids、ELFPath；源码还确认它由 CLI 参数解析生成，并用于注册 handler。问题不在字段本身，而是 DR-004 的“event selection data”可以写得更具体。

### R002：不支持的声明

- 严重性：`minor`
- 建议采取的措施：`partial_accept_as_issue`
- SRS 位置：NFR-003 / NFR-001
- 证据 IDs：E002、E006

**索赔或差距**

NFR-001 声明系统“只能在支持 Kprobe/Kretprobe 的 Linux 内核上运行”，这是一项硬性要求；证据仅表明它“已在此类内核上进行过测试”，并且 README 句子被截断（“尽管...”）。

**模型意见**

E002/E006 将其表述为“已在具有对 Kprobes 和 Kretprobes 的 eBPF 支持的内核版本上进行了测试”，后跟截断的“尽管...”，这可能会软化约束。将“测试”提升为“仅应运行”将约束夸大为严格要求。

**推荐人工检查**

阅读以“尽管...”开头的完整 README 句子，了解是否声明或放弃了更广泛的内核支持。

**型号建议更改 SRS**

NFR-001 声明：更改为“TraceLeft 面向 Linux 内核，支持 Kprobes 和 Kretprobes 的 eBPF”； README 记录了在此类内核上进行的测试。证据中没有明确说明严格的排他性。

可选的人工修订修复：
> 第 5 节 NFR-001、第 7 节 C-001/C-002、第 8 节 NFR-001/NFR-003 验收。把 NFR-001 改为：TraceLeft targets Linux environments with kernel support for eBPF Kprobes and Kretprobes; the README documents testing on Linux kernel versions v4.11+ with such support. 把 “operate only” 删除，保留 Linux/eBPF/Kprobe/Kretprobe 作为目标环境约束。

**人为决定**

- [ ] 接受
- [ ] 拒绝
- [x] 部分接受（`PARTIAL_ACCEPT`：混合声明；有些有效，有些无效）

可选的人工注释：
> README 说 TraceLeft 使用 Linux eBPF/Kprobes，并且在 v4.11+ 且支持 Kprobes/Kretprobes 的内核上测试过；但没有说“只能运行在这些内核上”。当前 NFR-001 的 operate only 过强。

### R003：歧义

- 严重性：`minor`
- 建议采取的措施：`accept_as_issue`
- SRS 位置：FR-009 / C-004
- 证据IDs：E001

**索赔或差距**

处理程序探针命名方案被引用为“记录的命名约定”，但证据文本已被编辑（方案名称已删除：“遵循名称所在的方案...”）。

**模型意见**

E001 确认存在命名方案，并且 k{,ret} 探针名称定义要更新的处理程序映射，但块中缺少实际的方案令牌。当具体模式不明显时，FR-009/C-004 不应暗示完全指定的、可验证的约定。

**推荐人工检查**

检查 Documentation/README.md 和探针加载程序源以捕获确切的处理程序/映射命名模式。

**型号建议更改 SRS**

FR-009 验证说明：添加“证据块中未捕获的确切命名模式；在将其视为可测试约定之前，请验证来自 README/probe 源的具体方案。

可选的人工修订修复：
> FR-009 改为：The probe loader shall use documented handler naming schemes: handler maps follow handle_NAME_progs and handle_NAME_progs_ret, and handler probes follow kprobe/handle_NAME and kretprobe/handle_NAME, where NAME identifies the traced function.C-004 同步改成这条明确约束。

**人为决定**

- [x] 接受
- [ ] 拒绝
- [ ] 部分接受（`PARTIAL_ACCEPT`：混合声明；有些有效，有些无效）

可选的人工注释：
> 证据包里命名方案被截断，但完整 documentation/README.md 和 probe/probe.go 明确说明了命名规则：handler map 使用 handle_NAME_progs{,_ret}，handler probe 使用 kprobe/handle_NAME 和 kretprobe/handle_NAME。当前 SRS 只说“documented naming conventions”，不够可验证。

### R004：不可验证

- 严重性：`minor`
- 建议采取的措施：`accept_as_issue`
- SRS 位置：FR-005、NFR-004
- 证据 IDs：E002、E006

**索赔或差距**

“配置驱动的跟踪/审计”要求缺乏可观察的验收标准；他们重申了 README 的营销风格框架。

**模型意见**

E002/E006 将 TraceLeft 描述为“设计为构建配置驱动的系统审核工具的框架”。这是一种设计意图，而不是可测试的行为。 FR-005/NFR-004 所写内容无法客观验证。

**推荐人工检查**

确定是否存在具体的配置加载代码路径（e.g.，生成器/config.pb.go 用法）来锚定可测试的标准。

**型号建议更改 SRS**

FR-005 验收依据：与具体工件 e.g 相关。 “生成的配置结构（具有位置/类型/名称/后缀/hash_func 的 Event_Args）可用于驱动事件处理 [E005]。”如果未确认运行时路径，则降级为设计目标注释而不是需求。

可选的人工修订修复：
> FR-005 改为：The system shall support configuration-driven handler generation by reading Proto/JSON event configuration and generating eBPF handler source code for configured events and arguments. 验收改为：Given an event configuration containing event argument metadata, the generator reads the configuration and produces handler source code for the configured events.

**人为决定**

- [x] 接受
- [ ] 拒绝
- [ ] 部分接受（`PARTIAL_ACCEPT`：混合声明；有些有效，有些无效）

可选的人工注释：
> 原因：configuration-driven tracing/auditing 不是单纯营销语。README 和 generator/generator.go 说明配置会从 config.json/protobuf 结构生成 eBPF handler 源码。但当前 FR-005/NFR-004 的验收太泛，缺少可观察标准。

### R005：架构_详细信息

- 严重性：`minor`
- 建议采取的措施：`accept_as_issue`
- SRS 位置：第 2 部分 / FR-006、FR-008
- 证据IDs：E001

**索赔或差距**

尾部调用探针/处理程序架构和单个共享事件映射是从 README 文本中描述的，但未与真实架构图进行交叉检查。

**模型意见**

E001 支持跟踪探针、尾部调用处理程序探针和单个共享事件映射。证据包中引用了架构图 (traceleft-architecture.png)，但未以文本形式提供；应根据它确认关键数据流（内核->用户空间跟踪器调度）。

**推荐人工检查**

将第 2 节产品视角与组件和事件流的文档/traceleft-architecture.png 进行比较。

**型号建议更改 SRS**

第 2 节产品视角：添加注释“架构符合 README；尚未与traceleft-architecture.png 协调 - 根据图表验证组件/数据流名称。

可选的人工修订修复：
> 第 2 节 Product perspective，并同步 FR-006/FR-008 的描述。增加：TraceLeft’s runtime architecture consists of a main eBPF program attached to kprobe/kretprobe hooks, program maps and return-program maps keyed by PID, handler eBPF programs selected through those maps, and a perf map used to deliver generated events to the userspace traceleft tracer. FR-008 可改为：Handler eBPF programs shall emit events through the perf map; emitted events shall begin with the common event section so the userspace tracer can dispatch them.

**人为决定**

- [x] 接受
- [ ] 拒绝
- [ ] 部分接受（`PARTIAL_ACCEPT`：混合声明；有些有效，有些无效）

可选的人工注释：
> 架构图确认了 README 中的架构流：主 eBPF 程序 attach 到 kprobe/kretprobe，通过 Prog/Ret Prog map tail-call 到 handler eBPF program，handler 通过 Perf map 把事件送到 user-space traceleft。当前第 2 节只写概括，建议补齐这条高层流。
