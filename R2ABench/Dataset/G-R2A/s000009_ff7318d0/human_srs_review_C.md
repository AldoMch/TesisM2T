<!-- human_srs_review_A.md 由审阅者 A 生成。保留原始 human_srs_review.md。所有人类的判断都是英语的。 -->

# 人类 SRS 审查表

## 元数据

- 示例目录：`s000009_ff7318d0`
- 生成SRS：`final_srs.md`
- 证据包：`evidence_pack.json`
- 评测型号：`claude-opus-4-8`
- 生成于：`2026-06-05T15:35:22.041477Z`
- 原始模型响应：`model_srs_review_raw.md`
- 解析状态：`parsed`

## 总体模型意见

- 推荐：`revise`
- 置信度：`0.78`
- 理由：SRS 对于大多数功能和部署声明来说都是经过严格追踪且保守的。然而，存储库名称和 README 强调了 SRS 省略的“聊天机器人”和“实时流媒体”功能，并且比 README 的高级散文支持的更多实现确定性描述了一些要求（预测、筛选、提醒）。需要进行一些可追溯性和架构图检查。

## 人类整体决策

- [ ] 接受
- [ ] 拒绝
- [x] 部分接受

原因：
> ACCEPT=3，PARTIAL_ACCEPT=1，REJECT=2，PARTIAL_ACCEPT=0。

## 积极的观察

- API I/O 要求（FR-006、NFR-002、C-004）准确且保守地基于代码证据（E003、E004），包括 JSON 默认值和执行 api SigV4配置。
- 部署/技术约束（C-001 到 C-005、NFR-003）如实反映了 README 技术堆栈 (E005)。
- SRS 清楚地区分显式证据类型与推断证据类型，并提供具有置信水平的可追溯性矩阵，支持人工裁决。
- 验证方法合理并按照第 8 节中的要求进行映射。

## 候选人问题

### R001：缺少需求

- 严重性：`major`
- 建议采取的措施：`partial_accept_as_issue`
- SRS 位置：第 1 部分产品范围；第 4 节 功能要求
- 证据 IDs：无

**索赔或差距**

存储库名称明确包含“chatbot”（foot365-live-streaming-chatbot-prediction-app），但 SRS 从未提及任何聊天机器人/对话功能。

**模型意见**

聊天机器人在存储库标识中突出显示。如果存储库实现了聊天机器人（e.g.、Lex/Lambda），则 SRS 缺少一项重要的功能。提供的证据包不包含聊天机器人块，因此这需要验证而不是断言。

**推荐人工检查**

在存储库中搜索聊天机器人实现（e.g、Amazon Lex、对话流、聊天 UI 或 Lambda 意图）。确认聊天机器人功能是否存在并且应该成为功能要求。

**型号建议更改 SRS**

如果通过验证，请添加 FR-009：“系统应提供用于足球信息查询的聊天机器人/对话界面。”并更新第 1 节产品范围以提及聊天机器人功能。如果未实现，请添加范围注释，解释存储库名称引用了计划但未实现的聊天机器人。

可选的人工修订修复：
> 添加 FR-009：“系统应提供聊天机器人/对话界面，使用户能够通过文本消息查询足球赛程、比赛结果以及比赛放映地点推荐，并由后端对话/意图处理逻辑返回响应。”并更新第 1 节产品范围以提及聊天机器人功能。

**人为决定**

- [x] 接受
- [ ] 拒绝
- [ ] 部分接受（`PARTIAL_ACCEPT`：混合声明；有些有效，有些无效）

可选的人工注释：
> 来源检查已完成，README.md 明确提到用户可与应用对话、speech-to-text、Amazon Lex、Chatbot recommendations，并说明 Lex 用于语音/文本对话接口和意图识别。FrontEnd/index.html 嵌入 chat.html；FrontEnd/chat.html 有 “Chat Bot” UI、消息输入框和发送按钮。FrontEnd/js/main.js 会读取用户消息并调用 apigClient.recommendPost(...)；FrontEnd/js/apigClient.js 定义了 POST /recommend。
Lambda Functions/LF1.py 是 Lex 风格的 intent handler：读取 currentIntent.slots，分发 Greetings、fixture、matchresult、Footsuggest、uberintent 等 intent，并返回 dialogAction。

### R002：缺少需求

- 严重性：`major`
- 建议采取的措施：`accept_as_issue`
- SRS 位置：第 1 部分产品范围；第 4 节 功能要求
- 证据IDs：E005

**索赔或差距**

存储库名称包括“实时流媒体”，README 提到“实时比赛筛选”，但 SRS 单独对待实时比分更新 (Kafka/Avro) 和筛选建议，并且从不将实时流媒体视为一种独特的功能。

**模型意见**

存储库名称中的“实时流”可能指的是 Kafka 实时比分管道而不是视频流，但区别并不明确。 SRS 应澄清此处“实时流媒体”的含义，以避免范围误述。

**推荐人工检查**

验证“实时流媒体”是指 Kafka 实时比分更新管道 (E005) 还是实际的视频/流媒体功能。检查 README 全文和架构图。

**型号建议更改 SRS**

在第 1 节产品范围中添加澄清说明：“项目名称中的术语“实时流媒体”是指实时比分更新管道（EC2 上的 Kafka/Apache Avro），而不是视频流。”如果验证显示其他情况，请进行调整。

可选的人工修订修复：
> 在第 1 节产品范围中添加澄清说明：“项目名称中的术语“实时流媒体”是指实时比分更新管道（EC2 上的 Kafka/Apache Avro），而不是视频流。

**人为决定**

- [x] 接受
- [ ] 拒绝
- [ ] 部分接受（`PARTIAL_ACCEPT`：混合声明；有些有效，有些无效）

可选的人工注释：
> 来源检查已完成，接受该问题。README 的 “live match screenings near them” 指的是附近酒吧/餐厅的比赛放映地点推荐，不是应用内视频直播。

### R003：不支持的声明

- 严重性：`minor`
- 建议采取的措施：`partial_accept_as_issue`
- SRS 位置：第二部分产品功能汇总； FR-002； FR-005； FR-003； FR-004
- 证据 IDs：E001、E005

**索赔或差距**

FR-002（向用户呈现的预测）、FR-003（筛查建议）、FR-004（日程管理/提醒）和 FR-005（电子邮件/SMS 提醒）被声明为已实现的系统行为，但证据只是高级别的 README雄心勃勃的散文（“我们的目标是服务......”，“我们管理他们团队的日程安排”）。

**模型意见**

README 措辞是目标导向的（“我们的目标是”、“向他们提供提醒”、“提出建议”），并且可能描述预期的行为，而不是完全实施的行为。 SRS 将这些转化为严格的“必须”要求。这对于需求文档来说是可以接受的，但置信度/可追溯性应该反映出这些来自问题陈述散文，而不是代码。

**推荐人工检查**

确认代码是否存在实现预测显示、筛选建议、计划管理和 SMS/电子邮件提醒传送（SNS/SQS Lambda 处理程序）。相应地调整可追溯性矩阵的置信度。

**型号建议更改 SRS**

在第 9 节可追溯性矩阵中，降低 FR-003 和 FR-004 的置信度以反映仅问题陈述的来源，并添加注释，表明这些要求源自 README 目标而不是经过验证的实现。

可选的人工修订修复：
> 保留 FR-002/FR-003；把 FR-004 降级或改窄为“查看/请求赛程提醒”；把 FR-005 改为“短信提醒”，不要写成“电子邮件和短信提醒”，除非只作为 README 目标且低置信度标注。

**人为决定**

- [ ] 接受
- [ ] 拒绝
- [x] 部分接受（`PARTIAL_ACCEPT`：混合声明；有些有效，有些无效）

可选的人工注释：
> 来源检查已完成，部分接受该问题。FR-002 预测显示：有前端实现证据。FrontEnd/predict.html 调用 /predictions 并展示 Home Wins / Draws / Away Wins。但仓库中没有清晰看到 SageMaker 推理 Lambda；SageMaker 主要来自 README 声明。
FR-003 放映点推荐：有代码证据。Lambda Functions/LF1.py 的 Footsuggest / dining_suggestion_intent 调 Google Places 查询 Football match screening in <city>。FR-004 赛程管理/提醒：部分有证据。fixture.html 展示 standings/fixtures/results；LF1.py 可把 team/date/phone 放入 SQS；LF2.py 从 SQS 取出并用 SNS 发短信。但没有看到“用户管理球队赛程/收藏球队日程”的完整实现。
FR-005 邮件/SMS 提醒：SMS 有代码证据，email 没有实现证据。搜索到的 email 只有页面页脚 mailto 和 README 文案；没有 SES、邮件发送 API 或 email publish 代码。

### R004：架构_详细信息

- 严重性：`minor`
- 建议采取的措施：`accept_as_issue`
- SRS 位置：第 2 节操作环境； FR-008； C-005
- 证据IDs：E005

**索赔或差距**

SRS 断言 Kafka/Avro 实时比分管道在 EC2 上运行，并描述了完整的 AWS 服务交互，但未提供架构图 (architecture.jpg) 作为可分析的证据。

**模型意见**

EC2/Kafka 声明由 E005 文本支持。但是，数据流关系（e.g.、SQS/SNS、Lambda、SageMaker 和 DynamoDB/Elasticsearch 互连方式）是从服务列表推断的，而不是经过验证的图表。应检查真实架构图以确认组件关系。

**推荐人工检查**

打开 Snapshots/architecture.jpg 并验证所描述的组件关系和数据流是否与 SRS 操作环境和 FR-008 描述相匹配。

**型号建议更改 SRS**

如果图表确认了关系，则无需更改文本；否则，请在第 2 节中添加注释，将已验证的组件与待图表确认的推断数据流关系区分开来。

可选的人工修订修复：
> 

**人为决定**

- [ ] 接受
- [x] 拒绝
- [ ] 部分接受（`PARTIAL_ACCEPT`：混合声明；有些有效，有些无效）

可选的人工注释：
> 架构图确认了高层组件：S3、Cognito、API Gateway、Lambda、Kafka/EC2、DynamoDB、Elasticsearch、SQS、SNS、Lex、SageMaker，以及 live_score / standing / recommendation / fixtures / prediction 等功能区域。README 也明确写了 EC2 for Kafka (with Apache Avro) for live score update。

### R005：可追溯性

- 严重性：`minor`
- 建议采取的措施：`accept_as_issue`
- SRS 位置：假设和依赖性（预测最后一周的假设）
- 证据IDs：E005

**索赔或差距**

E005 引用了假设“比赛预测取决于当前赛季除最后一周之外已进行的比赛的数据”，但 E005 的文本是最后一周的预测假设片段（“我们对赛季最后一周的预测假设考虑了当前赛季中除最后一周之外的所有比赛”）。 SRS 中的措辞稍微重新解释了这一点。

**模型意见**

引文是正确的，但 SRS 的改写（“取决于数据......除了最后一周”）几乎是源的倒置（“最后一周的预测假设考虑了除上周之外的所有比赛”）。这可能会误导读者关于预测哪一周与排除哪一周。

**推荐人工检查**

重新阅读 E005 句子并确认 SRS 释义保留了预期含义（最后一周的预测使用除上周之外的所有数据）。

**型号建议更改 SRS**

将假设和依赖项修改为：“赛季最后一周预测假设当前赛季中除上周之外的所有比赛都用作输入数据。 (E005)'

可选的人工修订修复：
> 接受模型修改意见。

**人为决定**

- [x] 接受
- [ ] 拒绝
- [ ] 部分接受（`PARTIAL_ACCEPT`：混合声明；有些有效，有些无效）

可选的人工注释：
> README 原意是：赛季最后一周的预测使用当前赛季中除最后一周之外的比赛数据。当前 SRS 的表述缺少“赛季最后一周预测”这个限定，容易让人误解为所有预测都按这个数据范围处理。

### R006：不可验证

- 严重性：`minor`
- 建议采取的措施：`probably_ignore`
- SRS 位置: NFR-004
- 证据 IDs：E002、E006

**索赔或差距**

NFR-004（通过 DynamoDB/Elasticsearch 实现的可扩展性）被明确标记为推断的，并且没有可测量的接受标准（没有吞吐量、延迟或数据量目标）。

**模型意见**

SRS 适当地将其标记为推断，这很好。然而，正如所写的，除了架构审查之外，它仍然是不可验证的。考虑到证据限制，这是可以接受的，但应承认无法测试服务级别。

**推荐人工检查**

确认存储库中不存在性能/规模目标。如果没有，请将 NFR-004 保留为仅架构审查。

**型号建议更改 SRS**

在 NFR-004 验收基础上附加：“存储库证据中未定义量化规模目标；验证仅限于确认 DynamoDB 和 Elasticsearch 的使用。

可选的人工修订修复：
> 

**人为决定**

- [ ] 接受
- [x] 拒绝
- [ ] 部分接受（`PARTIAL_ACCEPT`：混合声明；有些有效，有些无效）

可选的人工注释：
> 我没有找到仓库定义明确性能/规模目标，例如吞吐量、延迟、并发数、容量阈值或 SLA。README 中的 “petabytes / tens of millions of requests per second” 是 DynamoDB 服务能力介绍，不是 Foot365 的系统验收指标。