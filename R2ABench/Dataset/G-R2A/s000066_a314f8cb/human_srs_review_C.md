<!-- human_srs_review_A.md 由审阅者 A 生成。保留原始 human_srs_review.md。所有人类的判断都是英语的。 -->

# 人类 SRS 审查表

## 元数据

- 示例目录：`s000066_a314f8cb`
- 生成SRS：`final_srs.md`
- 证据包：`evidence_pack.json`
- 评测型号：`claude-opus-4-8`
- 生成于：`2026-06-05T16:00:59.288024Z`
- 原始模型响应：`model_srs_review_raw.md`
- 解析状态：`parsed`

## 总体模型意见

- 推荐：`revise`
- 置信度：`0.78`
- 理由：SRS 证据充足，大多数声明都是可追溯的，但一些要求过度解释了重新连接行为，混淆了显式证据与推断证据，并且 FR-007 的“显示”玩家数量部分不受支持。在保留之前，需要进行一些小的可追溯性和可验证性加强。

## 人类整体决策

- [ ] 接受
- [ ] 拒绝
- [x] 部分接受

原因：
> ACCEPT=2，PARTIAL_ACCEPT=3，REJECT=2，PARTIAL_ACCEPT=0。

## 积极的观察

- 强有力的直接证据支持 WebSocket-over-HTTP 传输和 P2P 不支持的约束 (E002)，在 FR-002、C-002、C-003 中正确引用， NFR-004。
- 入站操作处理（game_reconnect、room_players_number、servers_list、servers_list_redirect、server_error、pong）从 onMessage 开关（E004、E006）准确枚举并映射到离散的功能需求。
- 出站消息格式 `[event, data]` 和 ping/null 心跳精确追踪到发送/重置HeartBeat 代码 (E003)。
- SRS 适当地将延迟界限和屏幕布局标记为没有证据支持，从而避免了过度范围。
- 可追溯性矩阵区分显式证据和推断证据（e.g.、NFR-003 标记为推断），这有助于裁决。

## 候选人问题

### R001：不支持的声明

- 严重性：`major`
- 建议采取的措施：`partial_accept_as_issue`
- SRS 位置：FR-006 / 第 4 区；验证 FR-006
- 证据IDs：E004

**索赔或差距**

FR-006 表示客户端应在 `game_reconnect` 上“恢复场景中的船只并重新启动游戏”。证据显示 `this.game.reAddShipFromScene(data); this.game.start();` 重新添加了一艘船并开始游戏，但 SRS 措辞（“恢复船”）和验证基础（“恢复船并重新启动游戏”）假设片段未完全确认语义。

**模型意见**

该行为大致正确，但“在场景中恢复船只”是一个轻微的解释。方法名称建议从提供的数据中重新添加船舶对象；没有证据表明它是否“恢复”了先前的船舶状态。这是可以接受的，但措辞应该更接近证据。

**推荐人工检查**

检查 `reAddShipFromScene` 实现以确认它是否恢复之前的状态或添加新的船舶对象；确认 `game.start()` 语义。

**型号建议更改 SRS**

FR-006：将“恢复场景中的船只并重新启动游戏”替换为“使用提供的数据 (reAddShipFromScene) 将船只添加到场景并开始游戏 (game.start())”。相应地更新验证基础。

可选的人工修订修复：
> 第 4 节 FR-006；第 8 节 FR-006 验收。把：restore the ship in the scene and restart the game 改为：根据服务器返回的数据将对应飞船重新加入场景，并启动/恢复游戏流程。验收也改为：收到 game_reconnect 后，客户端将对应飞船重新加入场景并继续游戏流程。

**人为决定**

- [ ] 接受
- [ ] 拒绝
- [x] 部分接受（`PARTIAL_ACCEPT`：混合声明；有些有效，有些无效）

可选的人工注释：
> game_reconnect 后代码确实会把对应飞船重新加入场景并启动游戏流程，但“恢复船只状态”这个说法偏强，源码只支持“重新加入场景”。

### R002：不可验证

- 严重性：`major`
- 建议采取的措施：`accept_as_issue`
- SRS 位置：FR-004 / 第 4 区； DR-003
- 证据IDs：E003

**索赔或差距**

FR-004 要求 `ping` “以心跳间隔”/“以配置的心跳间隔”发送，并且 DR-003 引用心跳。证据显示 `this.heartBeatInterval` 在 setTimeout 中使用，但未提供间隔值或它是可配置的，因此“已配置”无法完全验证。

**模型意见**

很好地支持`ping`与`null`的心跳发送（E003）。然而，称其为“已配置”意味着没有证据显示的外部可配置性。验收测试引用了“配置的心跳间隔”，该间隔没有明显的证据价值，削弱了可验证性。

**推荐人工检查**

验证`heartBeatInterval`在哪里初始化，是否可配置；捕获其默认值以使接受标准可观察。

**型号建议更改 SRS**

FR-004 和验证：将“按照配置的心跳间隔”替换为“按照客户端心跳间隔（heartBeatInterval）”；添加注释，具体间隔值应从客户端初始化代码中确认。

可选的人工修订修复：
> R-004、DR-003、第 8 节 FR-004 验收。把：at the configured heartbeat interval 改为：at the client heartbeat interval initialized to 60 seconds FR-004 建议写成：连接保持打开时，客户端应按 60 秒的客户端心跳间隔发送 ping 消息，消息数据为 null，并重置下一次心跳计时。

**人为决定**

- [x] 接受
- [ ] 拒绝
- [ ] 部分接受（`PARTIAL_ACCEPT`：混合声明；有些有效，有些无效）

可选的人工注释：
> 源码确认心跳间隔是固定初始化值 60000 ms，不是外部“configured heartbeat interval”。当前“configured”不可验证。

### R003：歧义

- 严重性：`minor`
- 建议采取的措施：`accept_as_issue`
- SRS 位置：FR-007 / 第 4 区； DR-006
- 证据IDs：E004

**索赔或差距**

FR-007 规定客户端应“更新显示或跟踪的玩家数量”。证据 (`this.game.setPlayers(data)`) 确认更新了跟踪的玩家计数，但未确认显示的 UI 元素。

**模型意见**

“显示”的措辞引入了 UI 索赔，但该索赔没有证据。限制游戏状态更新以保持证据支持。

**推荐人工检查**

检查 setPlayers 是否更新任何可见的 UI 计数或仅更新内部游戏状态。

**型号建议更改 SRS**

FR-007：将“更新房间中显示或跟踪的玩家计数”替换为“更新游戏状态下跟踪的玩家计数 (game.setPlayers(数据))”。

可选的人工修订修复：
> 

**人为决定**

- [ ] 接受
- [x] 拒绝
- [ ] 部分接受（`PARTIAL_ACCEPT`：混合声明；有些有效，有些无效）

可选的人工注释：
> 检查后发现 setPlayers 不只是更新内部状态，还会调用 DOM handler，把 players 元素内容更新为玩家数量。因此“displayed or tracked player count”是有源码支持的。

### R004：可追溯性

- 严重性：`minor`
- 建议采取的措施：`partial_accept_as_issue`
- SRS 位置：FR-005 重新连接/第 4 节；第 3 节 重新连接上下文
- 证据 IDs：E004、E005

**索赔或差距**

关闭时重新连接 (FR-005) 和重新连接上下文（DR-004：房间 ID，玩家 ID，索引）被引用到 E004/E005。该代码片段显示 `onClose` 调用 `this.reconnect()` 并发送 `[..roomId, playerId, index]`，但周围的 `reconnect()` 函数体被截断，因此仅部分证明了完整的重新连接流程。

**模型意见**

存在原子事实（onClose -> 重新连接；发送带有 roomId/playerId/index 的数组），但 SRS 意味着完整的重新连接流程。对于关闭触发的重新连接，可跟踪性是可以接受的，但仅部分显示重新连接上下文消息组件。

**推荐人工检查**

查看完整的 `reconnect()` 和连接打开处理程序，以确认在重新连接时发送重新连接上下文消息和索引语义。

**型号建议更改 SRS**

第 3 节数据交换格式 / DR-004：添加在重新连接/打开流程期间发送重新连接上下文数组（roomId、playerId、索引）的限定符，如 gameClient.js 中观察到的，等待完整重新连接处理程序的确认。

可选的人工修订修复：
> 把 DR-004 改为：当连接重新打开且客户端已有房间 ID 与玩家 ID 时，客户端应发送重连上下文数组，包含 room ID、player ID 和客户端/飞船索引，用于恢复多人房间会话。FR-005 验收可补充：连接关闭后客户端发起重连；连接重新打开后，在已有房间/玩家上下文时发送重连上下文。

**人为决定**

- [ ] 接受
- [ ] 拒绝
- [x] 部分接受（`PARTIAL_ACCEPT`：混合声明；有些有效，有些无效）

可选的人工注释：
> 完整源码确认了重连流程：关闭连接后触发 reconnect；重新打开连接时，如果已有 roomId 和 playerId，会发送包含 room ID、player ID、索引的重连上下文。当前 SRS 大体正确，但 DR-004 可更精确。

### R005：不支持的声明

- 严重性：`minor`
- 建议采取的措施：`partial_accept_as_issue`
- SRS 当前位置：产品功能汇总 / NFR-002 / C-001
- 证据IDs：E001

**索赔或差距**

SRS 反复声明单人游戏支持（第 2 节：“支持单人游戏和多人游戏”，用户类别：“单人游戏或多人游戏模式”）。唯一的证据是 README 标语“单人/多人游戏”(E001)；没有证据表明单人功能行为。

**模型意见**

README 标题中提到了单人游戏，但没有功能证据描述单人游戏流程。 SRS 应仅将单人游戏归因于 README 描述，并避免暗示已测试的单人游戏功能。

**推荐人工检查**

确认代码库中是否存在 README 标语之外的任何单人游戏模式逻辑。

**型号建议更改 SRS**

第 2 节用户类别：仅将单人游戏参考限定为“README 中描述的”；或者从不存在行为证据的功能/用户类声明中删除单人游戏声明。

可选的人工修订修复：
> 第 1 节 Product scope、第 2 节 User classes。保留单人游戏，但收敛表述：Earth Defender supports a browser game mode described as single/multiplayer; the available evidence gives detailed behavior primarily for multiplayer room-based play. User class 建议改为：Player: uses the browser client to play the game; documented interaction evidence primarily covers multiplayer room creation and joining.

**人为决定**

- [ ] 接受
- [ ] 拒绝
- [x] 部分接受（`PARTIAL_ACCEPT`：混合声明；有些有效，有些无效）

可选的人工注释：
> README 和代码都支持“存在单人/多人游戏”的高层描述；代码里有 isMultiplayer 开关。但证据主要描述多人房间流程，不能把单人模式展开成具体功能需求。

### R006：架构_详细信息

- 严重性：`minor`
- 建议采取的措施：`accept_as_issue`
- SRS 位置：第二部分 产品视角 / C-003
- 证据IDs：E002

**索赔或差距**

SRS 声明通用客户端/服务器架构和 P2P 不支持的约束，引用 README。 README 中引用了真实架构图 (GeneralArchitecture.png)（E002 提到“图中所示的是一般架构”），但不在证据包中，因此架构细节（e.g.、主/从拓扑、消息路由）未经过独立验证。

**模型意见**

P2P 限制和 WebSocket-over-HTTP 得到了很好的文本支持。然而，关于整体拓扑和从属/副本角色的声明将受益于交叉检查图表，而证据块中没有提供这一点。

**推荐人工检查**

打开 Documentation/img/GeneralArchitecture.png 并验证 SRS 架构/拓扑语句（客户端/服务器角色、从属/副本关系）是否与图表匹配。

**型号建议更改 SRS**

第2部分：添加注释，架构拓扑细节应根据documentation/img/GeneralArchitecture.png进行确认；如果图表确认了当前的声明，则无需更改文本。

可选的人工修订修复：
> 第 2 节 Product perspective；第 7 节约束可补充。在 Product perspective 增加：在多人架构中，浏览器客户端先通过 DNS/负载均衡获取 WebServer 地址并下载游戏静态资源；WebServer 仅负责提供 HTML、CSS、JavaScript 和图片等资产。随后客户端通过 WebSocket 连接 Erlang 游戏服务器。服务器侧包含 master/slave 结构，slave/replica 用于故障容错。

**人为决定**

- [x] 接受
- [ ] 拒绝
- [ ] 部分接受（`PARTIAL_ACCEPT`：混合声明；有些有效，有些无效）

可选的人工注释：
> 架构图确认了客户端、DNS、WebServer、Server Master、Server Slave 的拓扑。当前 SRS 只写了笼统客户端/服务器架构，漏了 DNS/WebServer 资产服务和 master/slave 关系。

### R007：可追溯性

- 严重性：`minor`
- 建议采取的措施：`probably_ignore`
- SRS 位置：第 5 节中的可追溯性矩阵 NFR-005 与 NFR-005
- 证据IDs：E002

**索赔或差距**

NFR-005（异步并发通信）在可追溯性矩阵中被引用到 E002，但第 5 节列出了相同的内容；底层的 README 短语是“可以同时发生的异步通信”(E002)。这是受支持的，但将其“显式”标记为可测量的 NFR 很弱，因为没有可测试的并发指标。

**模型意见**

该声明有文字支持，但作为质量属性是不可衡量的。考虑将重新分类为设计特征而不是可验证的 NFR，或添加可观察的验收标准。

**推荐人工检查**

确定异步/并发通信是否应该是具有可观察测试或设计声明的 NFR。

**型号建议更改 SRS**

NFR-005：要么移至第 7 节约束/设计特征，要么添加接受标准，例如“多个客户端可以与服务器同时通信而不会阻塞”，并通过演示进行验证。

可选的人工修订修复：
> 

**人为决定**

- [ ] 接受
- [x] 拒绝
- [ ] 部分接受（`PARTIAL_ACCEPT`：混合声明；有些有效，有些无效）

可选的人工注释：
> README 明确支持“WebSocket over HTTP for asynchronous communication that can occur concurrently”。NFR-005 虽然不够量化，但作为设计层面的非功能/通信特征并未造成明显错误。
