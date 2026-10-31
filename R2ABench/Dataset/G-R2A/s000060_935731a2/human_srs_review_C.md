<!-- human_srs_review_A.md 由审阅者 A 生成。保留原始 human_srs_review.md。所有人类的判断都是英语的。 -->

# 人类 SRS 审查表

## 元数据

- 示例目录：`s000060_935731a2`
- 生成SRS：`final_srs.md`
- 证据包：`evidence_pack.json`
- 评测型号：`claude-opus-4-8`
- 生成于：`2026-06-05T15:56:42.873547Z`
- 原始模型响应：`model_srs_review_raw.md`
- 解析状态：`parsed`

## 总体模型意见

- 推荐：`revise`
- 置信度：`0.7`
- 理由：SRS 结构良好，大多数功能需求都可以清晰地追踪到测试证据。然而，一些声明（Kafka/消息发布、反序列化“兼容性”作为有效负载保证、仅 UPDATED 事件类型、JVM/Kotlin 操作环境）相对于截断的证据被部分推断或夸大，并且 FR-003/包含过滤器语义的表述比证据证明的更准确。候选中引用的架构图未反映在 SRS 中的任何架构细节中。

## 人类整体决策

- [ ] 接受
- [ ] 拒绝
- [x] 部分接受

原因：
> ACCEPT=4，PARTIAL_ACCEPT=1，REJECT=1，PARTIAL_ACCEPT=0。

## 积极的观察

- 功能需求 FR-001/FR-002 紧密且正确地跟踪到具体的测试断言（EventType.UPDATED、元素名称/updatedValue/previousValue/metadata.fqdn、覆盖的 applicationName）。
- SRS 适当区分显式置信度与推断置信度，并避免在缺乏证据的情况下伪造 UI 或部署声明。
- 数据要求 DR-003/DR-004 准确反映 AuditorEventConfig 字段和示例 Item 域模型，包括 UUID/map/list/nested 结构。
- 范围约束 (C-001..C-003) 合理地将产品绑定为依赖于外部发布者/记录器实现的 Kotlin 客户端库，与 E003 一致。

## 候选人问题

### R001：不支持的声明

- 严重性：`major`
- 建议采取的措施：`partial_accept_as_issue`
- SRS地点：FR-001 / DR-002 /第8节FR-001验收
- 证据IDs：E002

**索赔或差距**

FR-001 表示系统创建事件类型为 UPDATED 的 AuditEvent，这意味着 UPDATED 是唯一/代表性的事件类型。证据仅显示一项测试断言 type == UPDATED 进行整数更改。

**模型意见**

EventType 显然是一个枚举 (EventType.UPDATED)，强烈暗示存在其他类型 (e.g.、CREATED/DELETED)。 SRS 并不声称具有排他性，但读者可能会推断 UPDATED 是唯一的行为。单一证据仅支持UPDATED；其他类型未经验证。这在范围内是可以接受的，但应进行标记，以便人员确认审核员是否也发出 SRS 中缺少的 CREATED/DELETED 事件。

**推荐人工检查**

检查存储库中的 EventType 枚举和 Auditor.kt 逻辑，以确认 CREATED/DELETED（或类似）事件类型是否存在，并且应记录为附加功能要求。

**型号建议更改 SRS**

在 FR-001 下添加注释：“证据仅证明 UPDATED 事件类型；其他 EventType 值（如果存在于 EventType 枚举中）不在此 SRS 范围内，应在验证后作为单独的要求添加。如果确认了其他类型，请为这些类型添加 FR-001a/FR-001b。

可选的人工修订修复：
> FR-001 改为：系统应根据 oldObject 与 newObject 的差异生成对应类型的 AuditEvent：字段值变化时为 UPDATED；新对象相对旧对象新增时为 CREATED；旧对象相对新对象删除时为 DELETED。事件元素应包含字段名、previousValue、updatedValue 和 metadata.fqdn。 同时第 8 节 FR-001 验收说明也补充 CREATED/DELETED。

**人为决定**

- [x] 接受
- [ ] 拒绝
- [ ] 部分接受（`PARTIAL_ACCEPT`：混合声明；有些有效，有些无效）

可选的人工注释：
> 测试中不仅有 UPDATED，还有 CREATED、DELETED。当前 FR-001 只写 updated fields，会让 SRS 看起来只支持更新事件。

### R002：架构_详细信息

- 严重性：`major`
- 建议采取的措施：`accept_as_issue`
- SRS 位置：第 3 节通信接口 / FR-004 / 第 2 节产品视角
- 证据 IDs：E001、E002、E003

**索赔或差距**

SRS 描述了“序列化事件消息”和通用 EventPublisher，但未识别 StepVerifier/消费者模式和引用的架构图建议的消息传输（e.g.、Kafka）。

**模型意见**

证据使用反应式消费者/StepVerifier 语义和序列化消息值 (it.value())，这与 Kafka/流传输一致，并且候选元数据中引用了真实架构图 (auditor-v1-architecture.png)。 SRS 保留了传输抽象，这是保守且站得住脚的，但它省略了对架构图的任何引用。人类应该确认具体的传输（Kafka/Reactor）是否是值得捕获的记录设计约束。

**推荐人工检查**

打开 docs/auditor-v1-architecture.png 和 AuditEventProducerConfig/AuditEventModule 以确定 Kafka 或特定反应式消息系统是否是预期的发布传输，以及是否应将其记录为架构约束。

**型号建议更改 SRS**

添加到第 2 节产品视角或 C-002：“参考架构 (docs/auditor-v1-architecture.png) 和生产者配置可以指定具体传输 (e.g., Kafka)。如果得到确认，请将传输记录为架构约束；否则保留抽象 EventPublisher 描述。

可选的人工修订修复：
> 在第 2 节 Product Perspective 和第 3 节 Communication Interfaces 补充：系统应作为 JVM 应用内的审计客户端库生成 audit/log 事件，并通过可配置的事件发布接口发送到事件流；默认发布实现基于 Kafka，事件由下游审计服务消费并持久化到后端存储。 在 FR-004 改成：系统应通过 EventPublisher 发布生成的审计事件；默认实现应使用 Kafka producer configuration 将序列化事件发送到配置的 topic。

**人为决定**

- [x] 接受
- [ ] 拒绝
- [ ] 部分接受（`PARTIAL_ACCEPT`：混合声明；有些有效，有些无效）

可选的人工注释：
> 架构图和实现都表明默认事件流是 Kafka：多个 application 内的 auditor-v1 client 发到 Kafka，再由 auditor-v1 app server 消费并写入数据库/文件存储类后端。但不建议把架构图逐盒翻译进 SRS。

### R003：不可验证

- 严重性：`minor`
- 建议采取的措施：`accept_as_issue`
- SRS 位置：NFR-002 / 第 8 节 NFR-002
- 证据 IDs：E001、E002

**索赔或差距**

NFR-002 声明有效负载“应与 AuditEvent 数据结构的反序列化兼容”。这是测试机制的重述，而不是独立可验证的质量属性。

**模型意见**

证据显示测试将消息值反序列化为 AuditEvent。将其表述为非功能性需求是边缘性的；它可以通过现有测试进行验证，因此它并不是严格意义上不可验证的，但它读起来更像是数据/接口合约，而不是 NFR。考虑重新定位到数据要求或严格到接口要求，以避免“兼容”含义的含糊不清。

**推荐人工检查**

决定是否将有效负载/AuditEvent 反序列化更好地表示为数据协定 (DR) 或接口要求，而不是 NFR；确认序列化格式（通过 objectMapper 的 JSON）。

**型号建议更改 SRS**

将 NFR-002 改写为：“已发布的事件负载应序列化为一种格式（根据测试，通过配置的 ObjectMapper 实现 JSON），该格式可以无错误地反序列化为 AuditEvent 结构。”或者将其作为显式数据协定移至 DR-001。

可选的人工修订修复：
> 把 NFR-002移到第 3 节 Data Exchange Formats 或第 6 节 DR-001：发布的事件 payload 应为 JSON 字符串，并应能被消费者反序列化为 AuditEvent。 第 8 节验收保留为数据格式验收。

**人为决定**

- [x] 接受
- [ ] 拒绝
- [ ] 部分接受（`PARTIAL_ACCEPT`：混合声明；有些有效，有些无效）

可选的人工注释：
> “payload 可反序列化为 AuditEvent”更像数据格式/接口契约，不是非功能需求。源码和测试确实验证了 JSON payload 可读成 AuditEvent。

### R004：歧义

- 严重性：`minor`
- 建议采取的措施：`accept_as_issue`
- SRS 位置：FR-003 / DR-003 / C-003
- 证据 IDs：E001、E002

**索赔或差距**

FR-003 断言系统将内容限制为与包含列表匹配的元素，但证据 (E001) 显示过滤器配置（启用、类型=['InclusionFilter']、包含=[...]），而没有断言隔离包含过滤的输出。

**模型意见**

E001 显示带有包含过滤器集的 AuditorEventConfig，E002 显示单元素结果，但截断的文本并未清楚地显示过滤将多元素候选集减少为仅包含元素。 “仅包含包含的元素”的行为主张是合理的，但在提供的块中并未得到充分证明。标记以根据完整的测试断言进行验证。

**推荐人工检查**

查看完整的 AuditorTest.kt 断言，该断言执行包含过滤器，以确认未包含的元素已从发出的 AuditEvent 中排除。

**型号建议更改 SRS**

将 FR-003 系统行为软化为：“系统应应用配置的元素包含过滤器，以便发出的元素被限制在配置的包含列表中（根据包含过滤器测试断言进行确认）。”一旦断言得到证实，就恢复强硬的措辞。

可选的人工修订修复：
> 在 FR-003 改为：当元素过滤启用且过滤类型为 InclusionFilter 时，系统应仅在 AuditEvent 中包含 includes 列表中匹配的元素；未匹配元素不得出现在该事件中。

**人为决定**

- [x] 接受
- [ ] 拒绝
- [ ] 部分接受（`PARTIAL_ACCEPT`：混合声明；有些有效，有些无效）

可选的人工注释：
> 完整测试证明 InclusionFilter 配置 includes 后，只发布 includes 匹配的元素，其他差异元素不会出现在事件中。当前说法基本对，但可以更精确。

### R005：可追溯性

- 严重性：`minor`
- 建议采取的措施：`probably_ignore`
- SRS 位置：操作环境 / C-001
- 证据 IDs：E003、E005、E006

**索赔或差距**

JVM 操作环境被标记为“推断”，但引用时就像有证据支持一样； E003/E005/E006 确认 Kotlin 源，但未明确声明 JVM 目标或支持的运行时/构建工具。

**模型意见**

Kotlin + java.util.UUID 导入合理地暗示了 JVM，并且 SRS 正确地将其标记为推断。这是低风险的。但是，没有证据表明 Kotlin/JVM 版本或构建系统，因此任何未来版本特定的要求都将不受支持。目前的措辞是可以接受的，但应保持明确的推断。

**推荐人工检查**

如果需要任何运行时/版本要求，请确认存储库中的 build.gradle/Kotlin 版本和目标 JVM；否则按推断离开。

**型号建议更改 SRS**

如果明确推断则无需更改。可选：将“（没有证明特定的 JVM/Kotlin 版本）”附加到操作环境注释中。

可选的人工修订修复：
> 

**人为决定**

- [ ] 接受
- [x] 拒绝
- [ ] 部分接受（`PARTIAL_ACCEPT`：混合声明；有些有效，有些无效）

可选的人工注释：
> README 说明面向 JVM application，构建文件也明确主编译目标 Java 11 / JVM 11。当前 SRS 写 JVM 是合理的。

### R006：不支持的声明

- 严重性：`minor`
- 建议采取的措施：`probably_ignore`
- SRS 位置: NFR-001
- 证据 IDs：E001、E002

**索赔或差距**

NFR-001 从使用 expectNoEvent(noEventDuration) 的单个测试中概括出“恰好一个匹配的审核事件，没有其他事件”，将其呈现为系统范围的非功能性保证。

**模型意见**

证据 (E002) 显示对于一个测试场景，expectNextMatches 后跟 ExpectNoEvent。 SRS 仔细地将其范围限定为“在功能测试中验证的单个审核更新操作”，这是合适的。风险在于，NFR-001 读起来就像一般的每次操作一个事件的保证。保留范围性措辞；人类确认单事件每次变化是否是真正的系统不变量或只是每次测试观察的标志。

**推荐人工检查**

确定每次更改一个事件是预期的系统不变性（设计）还是仅仅是观察到的测试结果；相应地调整 NFR-001 范围。

**型号建议更改 SRS**

保留当前范围的措辞。如果每次更改一个事件被确认为设计不变式，则扩大 NFR-001 并将置信度重新标记为显式；否则将其保留在测试范围内。

可选的人工修订修复：
> 将 NFR-001 (line 84) 改为测试范围限定，或移到第 8 节验收：在已验证的单次普通字段更新场景中，系统应发布一个匹配的 UPDATED AuditEvent，并在 2 秒观测窗口内不发布额外事件。该验收不约束所有 audit 调用均只能产生一个事件。

**人为决定**

- [ ] 接受
- [ ] 拒绝
- [x] 部分接受（`PARTIAL_ACCEPT`：混合声明；有些有效，有些无效）

可选的人工注释：
> 测试确实多处验证一个期望事件后 2 秒内无额外事件；但源码也有场景会产生多个事件，例如 map 更新可能产生 CREATED 和 DELETED。因此不能写成全局“一次 audit 只发一个事件”。
