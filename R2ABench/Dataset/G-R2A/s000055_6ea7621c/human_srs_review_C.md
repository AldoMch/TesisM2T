<!-- human_srs_review_A.md 由审阅者 A 生成。保留原始 human_srs_review.md。所有人类的判断都是英语的。 -->

# 人类 SRS 审查表

## 元数据

- 示例目录：`s000055_6ea7621c`
- 生成SRS：`final_srs.md`
- 证据包：`evidence_pack.json`
- 评测型号：`claude-opus-4-8`
- 生成于：`2026-06-05T15:53:34.853729Z`
- 原始模型响应：`model_srs_review_raw.md`
- 解析状态：`parsed`

## 总体模型意见

- 推荐：`revise`
- 置信度：`0.78`
- 理由：SRS 对于大多数声明来说都是有充分依据且可追踪的，但它错误地分配了搜索路由处理程序（路由器委托给 algorithm.serveHints，而不是处理程序），引入了部署/Heroku 约束遗漏，并包含几个推断或部分支持的声明（e.g.、FR-002“合理建议”、 FR-007 未找到需要加强的日志记录细节）。应检查一些可追溯性和架构细节（架构-diagram.png）。

## 人类整体决策

- [ ] 接受
- [ ] 拒绝
- [x] 部分接受

原因：
> ACCEPT=5，PARTIAL_ACCEPT=0，REJECT=2，PARTIAL_ACCEPT=0。

## 积极的观察

- 可追溯性强：大多数 FRs/DRs 引用了具体证据 IDs，这些证据清晰地映射到 README、router.js、handler.js 和测试文件。
- 正确区分支持与不支持的项目（e.g.，搜索响应负载标记为“不支持”，NFR-003 标记为“推断”）。
- 直接从E004中准确提取MIME类型的扩展映射（html/css/js/jpg/ico）。
- 约束部分使用适当的证据捕获具体的代码级事实（CommonJS、文件系统从公共读取、子字符串路由）。

## 候选人问题

### R001：矛盾

- 严重性：`major`
- 建议采取的措施：`accept_as_issue`
- SRS 位置：第二部分产品视角； FR-004；第三节 软件/API 接口
- 证据 IDs：E003、E004、E006

**索赔或差距**

SRS 反复声明路由器将搜索请求委托给“处理程序”/“自动完成处理程序”，但证据显示路由器委托给一个单独的模块：algorithm.serveHints (require('./algorithm.js'))，而不是 handler.js。

**模型意见**

E003 显示包含“搜索”的 URLs 的 `algorithm.serveHints(req, res)`，而 handler.js (E004) 仅包含serveHome/servePublic/notFound。 SRS 合并了 handler.js 和 algorithm.js。 FR-004 说“路由器将请求委托给自动完成处理程序”是不准确的；自动完成逻辑位于 algorithm.js 中。为了准确性，应该对此进行更正。

**推荐人工检查**

在 src/router.js 和 src/algorithm.js 中确认搜索请求由 algorithm.serveHints 提供服务，与 handler.js 不同。

**型号建议更改 SRS**

在 FR-004 和第 3 部分中，将“自动完成处理程序”替换为“自动完成模块 (`algorithm.serveHints`)”。更新第 2 节以注意三个模块：路由器（`router.js`）、处理程序（`handler.js`、home/public/notFound）和算法（`algorithm.js`、搜索提示）。

可选的人工修订修复：
> Section 2 Product perspective、FR-004、Section 3 Software/API interfaces、Traceability Matrix。建议改成：router 将包含 search 的请求委托给搜索提示/自动完成算法模块处理；handler 模块负责首页、静态资源和 not-found 响应。FR-004 中把 autocomplete handler 改为 autocomplete/search-hint algorithm module。

**人为决定**

- [x] 接受
- [ ] 拒绝
- [ ] 部分接受（`PARTIAL_ACCEPT`：混合声明；有些有效，有些无效）

可选的人工注释：
> 模型判断正确。router.js 中搜索请求不是交给 handler.js，而是交给独立的搜索算法模块；handler.js 只负责 home/public/notFound。

### R002：缺少需求

- 严重性：`minor`
- 建议采取的措施：`accept_as_issue`
- SRS 位置：第 2 节 运行环境；第 7 节 限制
- 证据IDs：E001

**索赔或差距**

README (E001) 明确提到“在 Heroku 上部署”作为项目方法的一部分，但 SRS 没有捕获任何部署约束/环境，并且证据包将“部署”列为涵盖的类别。

**模型意见**

部署到 Heroku 的证据很弱（作为方法目标提及，而不是实现细节）。它可能需要低优先级的假设/约束，而不是严格的要求。鉴于类别覆盖范围包括部署，明确的（甚至是暂时的）条目可以提高完整性。

**推荐人工检查**

检查存储库中的 Procfile、package.json 启动脚本或 Heroku 配置，确认实际部署目标。

**型号建议更改 SRS**

添加到第 2 节假设/第 7 节约束：“C-005（推断/低）：该应用程序旨在根据 README 方法说明 [E001] 在 Heroku 上部署；使用 Procfile/package.json 确认。'

可选的人工修订修复：
> Section 2 Operating environment / Assumptions，Section 7 Constraints。
建议新增：C-005：应用预期部署到 Heroku；README 声明 master branch 自动部署到 Heroku，运行入口由 Node.js start script 支持。优先级低，作为部署约束/假设记录。

**人为决定**

- [x] 接受
- [ ] 拒绝
- [ ] 部分接受（`PARTIAL_ACCEPT`：混合声明；有些有效，有些无效）

可选的人工注释：
> README 明确写了 Deploying on Heroku，并且还写到 master branch 自动部署到 Heroku；package.json 也有 start: node src/server.js，但没有 Procfile。所以应作为低优先级部署约束/假设，而不是强功能需求。

### R003：不可验证

- 严重性：`minor`
- 建议采取的措施：`accept_as_issue`
- SRS 位置: FR-002
- 证据 IDs：E001、E005、E006

**索赔或差距**

FR-002 指出系统返回“合理的建议或与输入的字符串匹配的诺贝尔奖获得者列表”，但“合理”是主观的，并且匹配的语义没有由证据指定。

**模型意见**

“合理”一词是从 README 用户故事 (E001) 复制的，不可测试。 E006 仅确认自动完成返回数组，而不确认匹配正确性。接受标准应该参考可观察的行为（返回一组获奖者值）而不是“合理的”。

**推荐人工检查**

检查 algorithm.autocomplete 实施/测试以确定哪些匹配保证（如果有）是可验证的。

**型号建议更改 SRS**

将 FR-002 系统行为改写为：“系统为输入的字符串返回诺贝尔奖获得者值的数组（证据中未指定超出数组返回类型的匹配正确性）。”删除“明智”。

可选的人工修订修复：
> FR-002、Product functions summary、Section 8、Traceability Matrix。建议改成：系统应基于本地获奖者数据返回一个获奖者姓名数组；返回项应以前缀方式匹配输入字符串，结果数量最多为 10 个。删除 sensible。

**人为决定**

- [x] 接受
- [ ] 拒绝
- [ ] 部分接受（`PARTIAL_ACCEPT`：混合声明；有些有效，有些无效）

可选的人工注释：
> sensible suggestions 不可验证；但完整 algorithm.js 说明了实际匹配规则：从姓名数组中返回以前缀匹配输入字符串的结果，最多 10 个。测试只验证数组和简单长度，但源码支持更明确的行为。

### R004：不支持的声明

- 严重性：`minor`
- 建议采取的措施：`partial_accept_as_issue`
- SRS 位置：FR-007； NFR/未找到数据
- 证据IDs：E004

**索赔或差距**

FR-007 引用了“家庭或公共资产服务”的未找到处理。证据（E004）显示readFile错误路径调用handler.notFound和console.log，但E004被截断为servePublic；未完全显示完整的未找到行为/输出。

**模型意见**

可见的 readFile 主体 (E004) 支持日志记录和 notFound 委托。但是，具体的“未找到响应行为”输出和 notFound 实现并不在证据包中。该主张合理但部分未经证实；将输出标记为未指定。

**推荐人工检查**

检查 handler.notFound 实施情况以确认未发现案例的响应状态/内容。

**型号建议更改 SRS**

在 FR-007 输出列中，更改为“委托给 handler.notFound 并记录错误（特定的未找到响应内容不存在）”。

可选的人工修订修复：
> 

**人为决定**

- [ ] 接受
- [ ] 拒绝
- [x] 部分接受（`PARTIAL_ACCEPT`：混合声明；有些有效，有些无效）

可选的人工注释：
> 模型担心 evidence pack 截断后看不到 notFound 实现；但完整 handler.js 已确认 notFound 会返回 404、Content-Type: text/html 和页面找不到文本。因此 SRS 没有实质错误。

### R005：可追溯性

- 严重性：`minor`
- 建议采取的措施：`probably_ignore`
- SRS 位置：FR-001 证据； DR-004
- 证据 IDs：E001、E002、E005

**索赔或差距**

FR-001 引用 E002（前端测试）来接受文本输入。 E002 测试 getUserInput(event) 返回 event.target.value，支持输入捕获，但 FR-001 面向用户的“在输入字段中输入文本”主要来自 E001/E005。 E002 链接指向帮助程序，而不是 UI 字段。

**模型意见**

这是一个微弱的可追溯性细微差别：E002 比 UI 要求 FR-001 更直接地支持 DR-004（来自事件目标值的字符串）。将 E002 保留在 FR-001 上是可以接受的，但 UI 输入和辅助捕获之间的区别应该很清楚；考虑对 FR-001 依赖 E001/E005，对 DR-004 依赖 E002。

**推荐人工检查**

确认未测试的前端代码是否定义了实际的输入字段；证据包仅显示对帮助者的测试。

**型号建议更改 SRS**

在 FR-001 中，保留 E001/E005 作为主要证据，并将 E002 注释为支持输入捕获帮助程序 (getUserInput)，而不是 UI 字段。

可选的人工修订修复：
> 

**人为决定**

- [ ] 接受
- [x] 拒绝
- [ ] 部分接受（`PARTIAL_ACCEPT`：混合声明；有些有效，有些无效）

可选的人工注释：
> 完整源码里 public/index.html 确实有输入框，public/main.js 也通过事件读取输入；E002 的测试支持 getUserInput(event) 从 event.target.value 捕获字符串。FR-001 引 E002 不算错误，只是 E002 更直接支持 DR-004。

### R006：架构_详细信息

- 严重性：`minor`
- 建议采取的措施：`accept_as_issue`
- SRS 位置：第二部分产品视角； NFR-003
- 证据 IDs：E003、E004、E006

**索赔或差距**

存在真实架构图 (public/assets/architecture-diagram.png)，但 SRS 不会根据该图引用或协调其架构。 NFR-003（模块分离）被标记为“推断”，可以通过图表确认/加强。

**模型意见**

该图可能记录了路由器/处理程序/算法/数据流，并且可以将 NFR-003 从推断升级为显式，并确认 R001 中算法与处理程序的区别。值得对图像进行人工检查。

**推荐人工检查**

打开架构-diagram.png 并验证它显示路由器 -> 处理程序/算法分离和 data.json 用法；相应地更新 NFR-003 证据类型。

**型号建议更改 SRS**

在第 1 节参考中添加对架构 diagram.png 的引用，如果得到确认，请将 NFR-003 证据类型从“推断”更改为“显式”，并以图表为源。

可选的人工修订修复：
> Section 1 References、Section 2 Product perspective、NFR-003、Traceability Matrix。建议新增引用：public/assets/architecture-diagram.png。NFR-003 改成：应用应将前端输入/请求、后端路由、请求处理、搜索算法和本地数据访问分离为不同职责模块。Evidence type 从 inferred 改为 explicit，来源加入架构图和源码证据。

**人为决定**

- [x] 接受
- [ ] 拒绝
- [ ] 部分接受（`PARTIAL_ACCEPT`：混合声明；有些有效，有些无效）

可选的人工注释：
> 架构图确实显示前端 userInput、XMLHttpRequest，后端 Router、handlers、algorithm、data.json 分离；这能加强 NFR-003，也支持 R001 中“handler 和 algorithm 不是同一个模块”的修正。

### R007：歧义

- 严重性：`minor`
- 建议采取的措施：`accept_as_issue`
- SRS 位置：C-004； FR-004
- 证据IDs：E003

**索赔或差距**

约束 C-004 正确地注意到搜索路由使用子字符串匹配 (endpoint.indexOf('search'))，但 FR-004/第 3 节说“请求 URL 包含搜索”，而没有标记任何包含子字符串“搜索”的 URL 的风险 (e.g.,名为 research.png 的静态文件）将被路由到自动完成。

**模型意见**

E003 确认子字符串匹配。这是一个准确但可能脆弱的设计；将其视为已知限制可以提高精度和可测试性。

**推荐人工检查**

确认 router.js 中的匹配是没有路径分隔的纯子字符串 (indexOf)，并决定是否记录为限制。

**型号建议更改 SRS**

向 FR-004/C-004 添加注释：“路由是通过 URL 上的纯子字符串匹配进行的；任何包含子字符串“search”的 URL 都会被路由到自动完成（可能与其他资源发生冲突）。

可选的人工修订修复：
> FR-004、C-004。建议改成：搜索路由通过 URL 子字符串匹配实现；任何包含 “search” 子字符串的 URL 都会被路由到自动完成逻辑。

**人为决定**

- [x] 接受
- [ ] 拒绝
- [ ] 部分接受（`PARTIAL_ACCEPT`：混合声明；有些有效，有些无效）

可选的人工注释：
> router.js 使用的是 endpoint.indexOf('search') !== -1，这是纯子字符串匹配，不区分路径段。因此任意 URL 只要包含 search 都会进入自动完成逻辑，确实应作为限制说明。
