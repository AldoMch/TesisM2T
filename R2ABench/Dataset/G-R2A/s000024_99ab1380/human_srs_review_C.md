<!-- human_srs_review_A.md 由审阅者 A 生成。保留原始 human_srs_review.md。所有人类的判断都是英语的。 -->

# 人类 SRS 审查表

## 元数据

- 示例目录：`s000024_99ab1380`
- 生成SRS：`final_srs.md`
- 证据包：`evidence_pack.json`
- 评测型号：`claude-opus-4-8`
- 生成于：`2026-06-05T15:39:10.632130Z`
- 原始模型响应：`model_srs_review_raw.md`
- 解析状态：`parsed`

## 总体模型意见

- 推荐：`revise`
- 置信度：`0.72`
- 理由：SRS 在证据包中具有良好的基础，大多数要求都可以清晰地追溯到 E001-E006。然而，一些要求夸大了证据：堡垒/负载平衡器/NAT先决条件在README中记录为变量名称，但SRS将它们断言为强制系统要求；未引用架构图（真实图像）；一些功能声明（e.g.、FR-003 默认用户密钥放置、FR-011 部署执行）依赖于截断的证据文本。有针对性的修改和人工检查是必要的。

## 人类整体决策

- [ ] 接受
- [ ] 拒绝
- [x] 部分接受

原因：
> ACCEPT=2，PARTIAL_ACCEPT=2，REJECT=2，PARTIAL_ACCEPT=0。

## 积极的观察

- FR-001、FR-002 和 FR-004 可以紧密追溯到具体证据（E001 inputs_config.json 和 E003 地形变量图），并具有匹配的变量名称。
- FR-005 / C-004 直接从 E002/E005 正确捕获 base64 编码的 master_user_data 约束。
- 可追溯性矩阵始终将证据标记为显式证据与推断证据（NFR-004 标记为推断证据），这有助于裁决。
- 范围适当地限制为 Terraform 驱动的 OCI 部署资产，没有捏造的 GUI 或应用程序层声明。

## 候选人问题

### R001：架构_详细信息

- 严重性：`major`
- 建议采取的措施：`accept_as_issue`
- SRS 位置：第 1 节参考资料/第 2 节产品视角
- 证据 IDs：无

**索赔或差距**

尽管描述了主实例、子网、堡垒、NAT 和负载均衡器拓扑，但真实架构图 (images/architecture.png) 并未在 SRS 中的任何位置引用或反映。

**模型意见**

该存储库提供了一个架构图，可能描述了预期的拓扑（主节点、代理/节点、网络、堡垒、负载均衡器）。 SRS 拓扑声明（FR-007 到 FR-010、NFR-004）应对照此图进行交叉检查，并且应引用该图作为证据。它的缺失削弱了建筑的可追溯性。

**推荐人工检查**

打开 https://github.com/oracle-quickstart/oci-jenkins/blob/master/images/architecture.png 并验证 SRS 拓扑（主节点、代理/工作节点、NAT、堡垒、负载均衡器、子网）匹配。添加图表作为参考。

**型号建议更改 SRS**

添加到第 1 节参考文献：“架构图：https://github.com/oracle-quickstart/oci-jenkins/blob/master/images/architecture.png”。经过人工验证后，向图中添加简短的第 2 节子注释跟踪拓扑要求 (FR-007–FR-010)。

可选的人工修订修复：
> SRS 应加入架构图引用。图能支持 master/slave、VCN、AD、public/private subnet 拓扑；但不应说该图证明 NAT/bastion/LB。

**人为决定**

- [x] 接受
- [ ] 拒绝
- [ ] 部分接受（`PARTIAL_ACCEPT`：混合声明；有些有效，有些无效）

可选的人工注释：
> SRS 应加入架构图引用。图能支持 master/slave、VCN、AD、public/private subnet 拓扑；但不应说该图证明 NAT/bastion/LB。

### R002：不支持的声明

- 严重性：`major`
- 建议采取的措施：`partial_accept_as_issue`
- SRS 位置：FR-008、FR-009、FR-010、C-003
- 证据 IDs：E004、E006

**索赔或差距**

这些被表述为系统“应要求”强制先决条件，但证据（E004/E006）是非正式的 README 注释（“如果使用专用网络，请遵循：... Nat 门已设置... 堡垒机已设置... Loadbanance 已设置”）。该文本记录了手动设置指南，而不是经部署验证的系统强制要求。

**模型意见**

README 用散文描述了操作员先决条件，没有证据表明 Terraform 工作流程验证或强制执行 NAT/bastion/LB。 “工作流程应要求”这一措辞意味着没有证据证明的强制执行。这些是有条件的运算符先决条件，而不是可验证的系统行为。

**推荐人工检查**

检查现有的_infra Terraform 模块是否实际验证或使用 bation_host / lb_public_ip / NAT，或者它们是否仅仅是文档。确认是否存在强制执行。

**型号建议更改 SRS**

将 FR-008/FR-009/FR-010 从“工作流程应要求...”改写为“对于专用网络部署，运营商必须为节点子网提供预先存在的 NAT 网关（已记录的先决条件）”和“必须通过 bation_host 提供堡垒主机公共 IP”/ “必须通过 lb_public_ip 提供公共负载均衡器 IP”。将验证标记为文档检查，而不是暗示系统强制执行。

可选的人工修订修复：
> NAT/LB 不应写成系统会强制验证；bastion 不是纯文档项，Terraform 实际消费 bastion_host 做 SSH provision。建议把 FR-008/010 降级为“文档化前提/运营依赖”，FR-009 改成实际 bastion_host 输入依赖。

**人为决定**

- [ ] 接受
- [ ] 拒绝
- [x] 部分接受（`PARTIAL_ACCEPT`：混合声明；有些有效，有些无效）

可选的人工注释：
> 来源检查已完成，部分接受该问题。

### R003：矛盾

- 严重性：`minor`
- 建议采取的措施：`partial_accept_as_issue`
- SRS 位置：FR-009、数据实体 (`bation_host`)、C-003
- 证据 IDs：E004、E006

**索赔或差距**

SRS 重现变量名称 `bation_host`，但不会将其标记为可能的 `bastion_host` 拼写错误，并使用 `bation_host`，就好像它是稳定的接口名称一样。

**模型意见**

证据字面上显示 `bation_host`（源 README 中的拼写错误）。 SRS 正确地镜像了源，但需求文档应注意该标识符是逐字来自源的并且可能存在拼写错误，因此实现者不会假定 `bastion_host`。

**推荐人工检查**

确认现有_infra Terraform 变量文件中使用的确切变量名称（可能是 .tf/variables.tf），以确定接口名称是 `bation_host` 还是 `bastion_host`。

**型号建议更改 SRS**

向 `bation_host` 数据实体添加脚注：“标识符是从存储库文档中逐字复制的 (E004/E006)；拼写可能与实际的 Terraform 变量名称不同 - 根据 variables.tf 进行验证。

可选的人工修订修复：
> SRS 应把 FR-009、数据实体、C-003 中的 bation_host 改为 bastion_host。

**人为决定**

- [x] 接受
- [ ] 拒绝
- [ ] 部分接受（`PARTIAL_ACCEPT`：混合声明；有些有效，有些无效）

可选的人工注释：
> README 写错为 bation_host，实际变量是 bastion_host。

### R004：范围

- 严重性：`major`
- 建议采取的措施：`partial_accept_as_issue`
- SRS 位置：第一节产品范围/第二节产品功能概述
- 证据 IDs：E002、E004、E005、E006

**索赔或差距**

尽管反复引用“jenkins 节点”(E004/E006) 和“多个集群”(label_prefix、E002/E005)，SRS 仅描述 Jenkins 主部署并省略 Jenkins 代理/工作节点配置。

**模型意见**

有证据提到将“jenkins 节点”部署到 NAT 子网和“多个集群”中，这意味着代理/节点部署超出了主节点。 SRS 彻底捕获主参数，但不记录节点/代理配置，可能低估了范围。

**推荐人工检查**

检查 README 和 Terraform 变量的节点/代理/从属参数（e.g.、node_count、node_ad、node_subnet_id）。确定代理配置是否在范围内。

**型号建议更改 SRS**

如果存在节点配置，请添加功能要求：“FR-012 部署工作流程应接受 Jenkins 节点/代理参数并将 node(s) 部署到启用 NAT 的子网 (E004/E006)。”否则添加范围注释，仅澄清 Jenkins master 的工作流程规定。

可选的人工修订修复：
> 在“产品范围”中建议修改为：接受 Jenkins master 与 Jenkins slave/agent 节点的部署参数，并支持通过 Terraform 部署由一个 master 节点和一个或多个 slave/agent 节点组成的 Jenkins cluster。

**人为决定**

- [ ] 接受
- [ ] 拒绝
- [x] 部分接受（`PARTIAL_ACCEPT`：混合声明；有些有效，有些无效）

可选的人工注释：
> SRS 目前过度偏向 Jenkins master，应补充 slave/agent 范围：slave_count、slave_ads、slave_subnet_ids、slave image/shape/display name，以及部署 Jenkins slave instances。

### R005：不可验证

- 严重性：`minor`
- 建议采取的措施：`accept_as_issue`
- SRS 位置: FR-011
- 证据 IDs：E004、E006

**索赔或差距**

FR-011 在 Terraform init 之后引用“部署执行”，但证据文本 (E004/E006) 在“初始化 Terraform：”处被截断，并且不显示后续的应用/部署命令。

**模型意见**

init步骤被证明； “接下来是部署执行”/“集群部署”部分是从截断的文本中推断出来的。接受基础（“部署前的 Terraform 初始化”）部分超出了所显示的证据。

**推荐人工检查**

阅读完整的现有_infra/README.md 部署部分，以确认确切的初始化后命令（terraform plan/apply）。

**型号建议更改 SRS**

将 FR-011 缩小到已证明的内容：“部署工作流程应支持 Terraform 初始化作为第一个部署步骤。”仅在确认完整的 README 文本后添加应用/部署步骤。

可选的人工修订修复：
> 

**人为决定**

- [ ] 接受
- [x] 拒绝
- [ ] 部分接受（`PARTIAL_ACCEPT`：混合声明；有些有效，有些无效）

可选的人工注释：
> 完整 README 已确认 terraform init 后还有 terraform plan 和 terraform apply。

### R006：可追溯性

- 严重性：`minor`
- 建议采取的措施：`probably_ignore`
- SRS 位置：FR-003 / 第二节产品功能
- 证据 IDs：E002、E005

**索赔或差距**

FR-003 声称密钥放置在“默认用户”authorized_keys 中，但 E002/E005 证据被截断（“...包含在实例上默认用户的 ~/.ssh/authorized_keys 文件中”），使其成为描述 ssh_authorized_keys 变量的片段，而不是确认的运行时行为。

**模型意见**

该主张似乎得到了支持，但证据是变量描述片段，而不是运行时放置的证明。文档上的验证方法“检查”是可以接受的，但置信度应反映截断的来源。

**推荐人工检查**

确认完整的 README 句子和/或将公钥放入默认用户的authorized_keys 的 cloud-init/instance 配置。

**型号建议更改 SRS**

将 FR-003 改写为：“提供的 ssh_authorized_keys 公钥应包含在实例上默认用户的 ~/.ssh/authorized_keys 文件中（根据文档）。”保持信心中等。

可选的人工修订修复：
> 

**人为决定**

- [ ] 接受
- [x] 拒绝
- [ ] 部分接受（`PARTIAL_ACCEPT`：混合声明；有些有效，有些无效）

可选的人工注释：
> 变量说明和模块 metadata 都支持 SSH public key 写入 instance metadata/authorized_keys 语义。可选增强：说明适用于 master 和 slave instances。
