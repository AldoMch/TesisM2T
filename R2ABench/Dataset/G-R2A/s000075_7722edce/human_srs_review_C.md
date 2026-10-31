<!-- human_srs_review_A.md 由审阅者 A 生成。保留原始 human_srs_review.md。所有人类的判断都是英语的。 -->

# 人类 SRS 审查表

## 元数据

- 示例目录：`s000075_7722edce`
- 生成SRS：`final_srs.md`
- 证据包：`evidence_pack.json`
- 评测型号：`claude-opus-4-8`
- 生成于：`2026-06-05T16:05:46.752387Z`
- 原始模型响应：`model_srs_review_raw.md`
- 解析状态：`parsed`

## 总体模型意见

- 推荐：`revise`
- 置信度：`0.72`
- 理由：SRS 结构良好且大部分证据可追踪，但它包含字段级矛盾（显示字段和计量字段类型与证据）、一些看似明确的推断声明，以及缺少架构细节（E003/E004 的 Redux 客户端状态/TypeScript 编辑器实现未得到充分利用）。在验收之前需要进行有针对性的修复。

## 人类整体决策

- [ ] 接受
- [ ] 拒绝
- [x] 部分接受

原因：
> ACCEPT=2，PARTIAL_ACCEPT=2，REJECT=2，PARTIAL_ACCEPT=0。

## 积极的观察

- 功能和数据要求与具体模式/模型证据（E004、E005、E006）密切相关，并具有仪表、显示和布局的准确字段列表。
- SRS 适当地将几个项目标记为“推断”（通信接口、有线格式）而不是夸大其词，并明确指出缺乏隐私/保留/迁移证据。
- C-001 到 C-005 的约束在 Dockerfile (E001) 和 README (E002) 中都有很好的基础，包括 client-build-before-server-packaging 依赖项。
- 提供了具有每个要求证据 IDs、证据类型和置信度的可追溯性矩阵，并且与证据包基本一致。

## 候选人问题

### R001：矛盾

- 严重性：`major`
- 建议采取的措施：`partial_accept_as_issue`
- SRS位置：第3节软件/API接口-显示资源； FR-002/FR-003；第 6 节 数据实体 - 显示
- 证据 IDs：E004、E005、E006

**索赔或差距**

SRS 列出带有字段 `key` 的显示资源，但客户端 Models.ts (E004) 将显示字段定义为 `key, available, resolution_x, resolution_y, display_data, rotation`（无 `current_layout`），而服务器序列化程序 (E005) 包括 `current_layout`并没有遗漏任何内容。 SRS 显示字段列表混合了仅服务器字段，而不标记客户端/服务器差异。

**模型意见**

E004（客户端）和E005（服务器）定义不同的显示字段集：客户端没有`current_layout`；服务器序列化程序有 `current_layout` 但客户端 Models.ts 缺少它。 SRS 提供了一个归因于 [E005] 和 [E006] 的统一字段列表，这掩盖了真正的差异。这是一个值得关注的可追溯性/矛盾问题。

**推荐人工检查**

逐个字段比较 Display 实体的 client/src/Models.ts (E004)、服务器序列化程序 (E005) 和 models.py (E006)，并确认 `current_layout` 是否有意客户端缺席。

**型号建议更改 SRS**

在第 3 节显示资源和第 6 节显示实体中，添加注释：“服务器端显示模型/序列化器（E005、E006）包括 `current_layout`（FK 到布局、可为空、SET_NULL 删除）；客户端显示接口 (E004) 省略 `current_layout`。应该协调客户端/服务器字段的差异。”将客户端派生字段分别归属于 [E004]，将服务器派生字段分别归属于 [E005]/[E006]。

可选的人工修订修复：
> 在 第 3 节 Software/API interfaces 的 Display 资源 和 第 6 节 Display 数据实体 增加说明：“服务端 Display 模型/序列化器包含 current_layout 布局引用字段；客户端 Display 接口仅包含 key、available、resolution_x、resolution_y、display_data、rotation，未包含该布局引用字段。SRS 中涉及 API/服务端资源时以服务端字段为准，涉及客户端状态时应单独注明。”同时 FR-003 中 “current_layout” 的来源只应归到服务端证据。

**人为决定**

- [ ] 接受
- [ ] 拒绝
- [x] 部分接受（`PARTIAL_ACCEPT`：混合声明；有些有效，有些无效）

可选的人工注释：
> 服务端 Display 模型/序列化器包含 current_layout，但客户端 Models.ts 的 Display 接口没有该字段。SRS 现在把 Display 字段统一写在一起，容易掩盖客户端/服务端字段差异。

### R002：不支持的声明

- 严重性：`minor`
- 建议采取的措施：`probably_ignore`
- SRS 位置：第 6 节数据实体 - 仪表（'值最大长度 600'）；布局（'数据是二进制'；'display_positions 是文本'）
- 证据IDs：E006

**索赔或差距**

字段级详细信息（例如 `value` 最大长度 600、以二进制形式存储的 `data`、以文本形式存储的 `display_positions`）均被陈述为事实。 E006 (models.py) 支持这些，但 E006 的文本被截断，并且仪表 max_length=600 可见；二进制/文本可见。这在很大程度上得到了支持，但 SRS 应根据权利要求具体引用 E006，而不是共同引用 E005。

**模型意见**

E006 实际上支持详细的类型声明（models.py 显示 max_length=600、BinaryField、TextField）。问题是次要的可追溯性：这些特定于模型的详细信息应单独引用 E006，而不是序列化器 E005。内容本身是准确的。

**推荐人工检查**

确认models.py（E006）显示值max_length=600，data=BinaryField，display_positions=TextField；确保这些类型详细信息的引用指向 E006。

**型号建议更改 SRS**

在第 6 节中，将注释列引用更改为仅引用 [E006]。

可选的人工修订修复：
> 

**人为决定**

- [ ] 接受
- [x] 拒绝
- [ ] 部分接受（`PARTIAL_ACCEPT`：混合声明；有些有效，有些无效）

可选的人工注释：
> models.py 明确支持这些字段类型：Gauge 的 value 最大长度 600，Layout 的 data 是二进制字段，display_positions 是文本字段。内容本身没有错。

### R003：架构_详细信息

- 严重性：`major`
- 建议采取的措施：`accept_as_issue`
- SRS 位置：第二部分产品视角；第 3 节 用户界面； FR-004/FR-005
- 证据 IDs：E003、E004

**索赔或差距**

证据 E003 (client/src/Store.tsx) 和 E004 (Models.ts) 显示编辑器是一个 TypeScript/React + Redux 单页客户端，具有定义的操作（CONTROL_ADDED、ELEMENT_ADDED、 SET_LAYOUTS、SET_GAUGES、SET_DISPLAYS、REQUEST_CANVAS_RENDER 等）和画布渲染模型。 SRS 仅抽象地描述了编辑器（“向导”、“创建布局”），并且从未引用 E003 或使用 E004 作为编辑器架构。

**模型意见**

有具体证据表明 SRS 未充分利用编辑器的客户端架构（Redux 存储、画布渲染/删除操作、仪表/布局/显示状态）。这与架构图检查相关，并将加强 FR-004/FR-005。 E002 中的“向导”描述很好，但鉴于更丰富的代码证据，内容很薄弱。

**推荐人工检查**

查看 Store.tsx (E003) 和 Models.ts (E004) 以确认基于 Redux 的客户端具有画布渲染和列出的操作类型；与编辑器/查看器/服务器拓扑的 docs/architecture.png 真实图进行比较。

**型号建议更改 SRS**

在第 2 节“产品”视角中，细化：“客户端/编辑器是使用 Redux 存储 (E003) 的 TypeScript/React 单页应用程序，具有添加/更新控件和元素、设置布局/仪表/显示以及请求画布渲染/删除操作（E003、E004）的操作。”将 [E003] 引用添加到 FR-004/FR-005 可追溯性中。

可选的人工修订修复：
> 在 第 2 节 Product perspective 增加：“客户端/编辑器是一个 TypeScript/React 单页应用，使用 Redux store 管理控件、元素、布局、仪表和显示设备状态，并通过 canvas 相关操作支持布局编辑、渲染请求和删除请求。” 在 FR-004/FR-005 和第 9 节 Traceability 中补充来源 [E003]、[E004]。

**人为决定**

- [x] 接受
- [ ] 拒绝
- [ ] 部分接受（`PARTIAL_ACCEPT`：混合声明；有些有效，有些无效）

可选的人工注释：
> Store.tsx 和 Models.ts 证明客户端/编辑器不是普通“向导”而已，而是 TypeScript/React + Redux 的单页客户端，维护 layouts、gauges、displays、controls/elements，并有 canvas render/delete 相关动作。SRS 当前对这部分架构描述偏薄。

### R004：不可验证

- 严重性：`minor`
- 建议采取的措施：`partial_accept_as_issue`
- SRS 位置：FR-007； FR-007 第 8 节验收
- 证据IDs：E002

**索赔或差距**

FR-007（“查看器子系统应渲染每个显示器所看到的内容”）及其接受度（“审阅者可以显示每个显示器渲染的输出”）仅依赖于 README 散文（E002），其本身不完整（“Th...”被截断），并且 README 指出 Docker 图像“不是 100%”独立/就绪”。观众被描述得充满渴望；没有提供无头浏览器渲染的代码证据。

**模型意见**

查看器要求仅由截断的 README 散文支持，并且没有已实现的无头浏览器查看器的代码/部署证据。鉴于 README 自己的“未 100% 准备就绪”警告，FR-007 可能夸大了实施范围。验收标准是基于演示的，但在当前状态下可能无法演示。

**推荐人工检查**

在存储库中搜索任何查看器/无头浏览器实现代码；验证查看器在此提交时是否已实现或仅是概念性的。

**型号建议更改 SRS**

将 FR-007 优先级/状态标记为计划或概念：附加到 FR-007 要求文本“这描述了每个 README 架构部分 (E002) 的预期观看者行为；此次提交的实施证据有限。在第 9 节中将置信度降低至“低”。

可选的人工修订修复：
> 在 FR-007 后补充：“该需求描述 README 中的 viewer 行为；源码存在 viewer 页面与浏览器/canvas 渲染路径，但该提交中的无头浏览器渲染与部署成熟度仍有限。” 在 第 8 节 FR-007 验收依据 改为：“可检查 viewer 路由和浏览器渲染路径能够读取显示数据并生成按显示分辨率呈现的黑白像素视图；完整无头浏览器自动化渲染需另行验证。” 第 9 节 FR-007 置信度建议从“中”降为“中/低”。

**人为决定**

- [ ] 接受
- [ ] 拒绝
- [x] 部分接受（`PARTIAL_ACCEPT`：混合声明；有些有效，有些无效）

可选的人工注释：
> 模型说“没有 viewer 代码证据”不完全准确；源码里有 /viewer/ 路由、ViewOnlyCanvas.tsx 和 loadCanvas.js/puppeteer 相关实现。但 viewer 仍带有原型/开发痕迹，例如脚本硬编码显示 key，README 和 Docker 部署也未完全成熟，所以验收标准确实不宜写得太满。

### R005：范围

- 严重性：`minor`
- 建议采取的措施：`accept_as_issue`
- SRS 位置：第1节产品范围； NFR-001/约束 C-005
- 证据 IDs：E001、E002

**索赔或差距**

SRS 没有显示 README 的明确警告，即 docker 映像正在“构建，但不是 100% 独立/就绪”(E002) 和 Dockerfile 的 TODOs（固定的 npm 版本，真正的 WSGI 服务器，runserver 用作CMD）（E001）。这些表明部署是开发级/不完整的，这会影响操作范围声明。

**模型意见**

E001 和 E002 都包含显式不完整性信号（TODOs，“未 100% 就绪”，`runserver` 不是生产 WSGI 服务器）。 SRS 中立地提出部署约束，而没有指出这些约束处于开发阶段。包括这一点可以防止夸大生产准备情况。

**推荐人工检查**

确认 Dockerfile 使用 `manage.py runserver`（开发服务器）和 README 的独立警告；决定是否添加到期/限制说明。

**型号建议更改 SRS**

在第 7 节中添加约束 C-006：“提供的部署是开发级的：Dockerfile 使用 Django `runserver`（不是生产 WSGI 服务器），并且 README 声明 Docker 映像尚未完全独立（E001、E002）。”

可选的人工修订修复：
> 在 第 7 节 Constraints 新增：“C-006：提供的容器化部署属于开发级/未完全生产就绪部署；Dockerfile 使用 Django 开发服务器启动，README 也说明 docker image 尚未完全 standalone/ready。” 在 第 1 节 Product scope 或 NFR-001 可补一句：“当前部署证据不支持生产级运行时成熟度声明。”

**人为决定**

- [x] 接受
- [ ] 拒绝
- [ ] 部分接受（`PARTIAL_ACCEPT`：混合声明；有些有效，有些无效）

可选的人工注释：
> README 明确写 docker image 还不是 100% standalone/ready；Dockerfile 也有 TODO，包括固定 npm 版本、使用真实 WSGI server，并且当前 CMD 是 Django runserver。SRS 应标注这是开发级部署，不应暗示生产就绪。

### R006：歧义

- 严重性：`minor`
- 建议采取的措施：`probably_ignore`
- SRS 位置：FR-002；第 3 节“唯一名称和分辨率”
- 证据 IDs：E002、E006

**索赔或差距**

FR-002 表示显示器已使用“唯一密钥”注册。 README (E002) 表示“唯一名称”；模型 (E006) 使用 `key` 作为主键 (CharField max_length=100)。 SRS 合并了“名称”和“密钥”。显示器的人性化“名称”是否等于主键 `key` 尚未说明。

**模型意见**

轻微歧义：README 的“唯一名称”与模型的主键 `key`。它们可能是相同的字段，但 SRS 应明确声明此映射以便可验证。

**推荐人工检查**

确认 README“唯一名称”映射到模型 `key` 主键字段。

**型号建议更改 SRS**

在 FR-002 中添加：“唯一显示标识符（README“名称”）对应于模型 `key` 主键字段（E006）。”

可选的人工修订修复：
> 

**人为决定**

- [ ] 接受
- [x] 拒绝
- [ ] 部分接受（`PARTIAL_ACCEPT`：混合声明；有些有效，有些无效）

可选的人工注释：
> README 的 “unique name” 体现在 API 路径里，服务端模型使用 key 作为主键，客户端创建 display 时也使用 newDisplay.key；把它写成唯一键并没有造成实质性错误。
