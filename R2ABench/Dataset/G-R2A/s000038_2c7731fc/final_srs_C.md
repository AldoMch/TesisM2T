# 软件需求规格说明书 (SRS)

Repository: IceFireDB/IceFireDB  
Commit: `80a568fdb7f7cbde63084e9d74bcf617830a747e`

## 1. 引言

### 1.1 目的
本 SRS 定义了由证据支持的、针对打包中已证明的仓库组件的需求，主要包括：
- IceFireDB-Redis-Proxy
- IceFireDB-PubSub
- 在 IceFireDB-SQLite 中可见的 protocol/data handling

### 1.2 产品范围
IceFireDB 被描述为一个由多个子项目组成的去中心化数据库基础设施项目，包括 Redis proxy、PubSub、SQLite、SQLProxy 和 NoSQL 组件。此处已证明的范围涵盖：
- 一个去中心化的 Redis 代理，可在联网代理之间同步 Redis 指令，并写入独立或集群 Redis 存储，
- 一个兼容 Redis publish/subscribe 用法的去中心化 Pub/Sub 系统，
- 在与 SQLite 相关的 MySQL 协议客户端代码中可见的、面向数据包和行的 SQL 结果处理。

### 1.3 目标读者
- IceFireDB 组件的产品负责人和维护者
- 部署基于 Redis 或兼容 Redis 协议服务的集成人员
- 验证仓库行为的测试和 QA 工程师
- 评估去中心化数据库基础设施能力的架构师

### 1.4 参考资料
- Repository: https://github.com/IceFireDB/IceFireDB
- Snapshot: https://github.com/IceFireDB/IceFireDB/tree/80a568fdb7f7cbde63084e9d74bcf617830a747e
- Evidence: E001, E002, E003, E004, E005, E006

## 2. 总体描述

### 2.1 产品视角
该仓库是一个多组件的去中心化数据库基础设施项目。证据显示，其包含围绕去中心化网络构建的、以 Redis 为重点的中间件和 Pub/Sub 能力，以及另一个组件中的 SQL 结果协议处理。Redis Proxy 和 PubSub 组件是证据最直接支持的、面向运行时的系统。

### 2.2 产品功能概述
仓库中已证明支持的功能包括：
- 面向独立和集群 Redis 数据源的 Redis 代理
- 联网 Redis 代理之间的指令自动同步
- 将代理数据写入集群或单点 Redis 存储
- 面向基于 Redis 应用的去中心化数据同步
- 跨去中心化 P2P 节点的、兼容 Redis-protocol 的 publish/subscribe
- 在同一网络、不同网络以及 NAT/private-network 条件下的节点通信
- 通过 Kademlia DHT 和 IPFS 网络发现进行对等节点发现和路由
- 在客户端响应路径中解析 SQL/MySQL 风格的结果字段、行、警告和状态

### 2.3 用户类别
- 将基于 Redis 的 Web2 应用迁移到去中心化基础设施的应用集成人员
- Redis 独立或集群部署的运维人员
- 多节点 Pub/Sub 网络的运维人员
- 通过协议客户端消费 SQL 结果数据的开发人员

### 2.4 运行环境
证据支持其运行于：
- Redis 独立部署
- Redis 集群部署
- 同一网络或不同网络上的多节点网络
- PubSub 节点所在的 private-network/NAT 环境

### 2.5 假设和依赖
- 对于代理和协议兼容性使用场景，Redis 是外部依赖。 (E001, E002)
- PubSub 节点发现/路由依赖 Kademlia DHT 和 IPFS 网络发现。 (E002)
- 该仓库在已证明的源文件中使用 Apache License 2.0 许可。 (E003, E004)

## 3. 外部接口需求

### 3.1 用户界面
没有证据表明存在面向最终用户的图形界面。

### 3.2 软件/API 接口
| Interface | Requirement summary | Source |
|---|---|---|
| Redis data source interface | Redis Proxy 应与独立和集群 Redis 存储模式互操作。 | E001 |
| Redis command/proxy interface | Redis Proxy 应接受 Redis 指令/命令以进行同步和存储转发。 | E001 |
| Redis publish/subscribe interface | PubSub 应支持 Redis publish/subscribe 协议，以便应用可以像使用 Redis Pub/Sub 一样使用它。 | E002 |
| SQL/MySQL result interface | 与 SQL 相关的客户端路径应处理来自数据包的结果字段、字段名映射、行、警告和状态值。 | E005 |

### 3.3 通信接口
| Interface | Requirement summary | Source |
|---|---|---|
| Decentralized agent network | Redis 代理应在联网拓扑中同步指令。 | E001 |
| P2P Pub/Sub network | PubSub 节点应能在同网、跨网以及 NAT/private-network 条件下通信。 | E002 |
| Peer discovery/routing | PubSub 应使用 Kademlia DHT 和 IPFS 网络发现进行对等节点发现和路由。 | E002 |

### 3.4 数据交换格式
| Format | Evidence-backed details | Source |
|---|---|---|
| Redis protocol commands | Redis 命令/指令兼容性由 Redis 代理和 Redis Pub/Sub 支持所隐含。 | E001, E002 |
| Pub/Sub messages | 发布/订阅消息遵循 Redis publish/subscribe 语义。 | E002 |
| Packetized SQL results | 结果数据包包括字段、行、警告和状态值。 | E005 |

## 4. 功能需求

| ID | Description | Trigger / Input | System behavior | Output | Priority | Verification | Source evidence |
|---|---|---|---|---|---|---|---|
| FR-001 | 支持 Redis 数据源模式 | 针对 Redis 存储的配置或部署 | Redis Proxy 应同时支持独立和集群 Redis 数据源模式。 | 代理使用所选 Redis 模式运行。 | 高 | 测试 | E001 |
| FR-002 | 在代理之间同步 Redis 指令 | 联网 Redis 代理接收到一条 Redis 指令 | Redis Proxy 应自动在联网 Redis 代理之间同步指令。 | 参与代理之间的同步指令。 | 高 | 测试 | E001 |
| FR-003 | 将写入转发到 Redis 存储 | 发出同步或代理写操作 | Redis Proxy 应将数据写入集群 Redis 存储或单点 Redis 存储。 | 数据持久化到已配置的 Redis 存储目标。 | 高 | 测试 | E001 |
| FR-004 | 提供去中心化 Redis 数据同步 | 基于 Redis 的应用使用代理中间件 | Redis Proxy 应为应用使用的 Redis 数据库启用去中心化数据同步。 | 去中心化中间件网络中的 Redis 数据同步。 | 高 | 演示 | E001 |
| FR-005 | 支持 Redis publish/subscribe 协议 | 客户端使用 Redis 发布或订阅语义 | PubSub 应支持 Redis publish/subscribe 协议。 | 兼容的发布/订阅交互。 | 高 | 测试 | E002 |
| FR-006 | 为 Pub/Sub 客户端保留类 Redis 用法 | 基于 Redis 的应用迁移到 PubSub | PubSub 应允许客户端像使用 Redis publish/subscribe 一样使用该服务。 | Redis 风格的 Pub/Sub 应用交互。 | 高 | 演示 | E002 |
| FR-007 | 支持多节点去中心化 Pub/Sub 运行 | 部署多个节点 | PubSub 应能在同一网络或不同网络上的多个节点中运行。 | 参与节点之间的分布式 Pub/Sub 网络运行。 | 高 | 测试 | E002 |
| FR-008 | 支持 NAT/private-network 节点通信 | PubSub 节点位于 private network 中且处于 NAT 后 | PubSub 应允许位于 private network 中且处于 NAT 后的节点彼此通信。 | NAT/private-network 场景下成功的节点间通信。 | 高 | 测试 | E002 |
| FR-009 | 提供对等节点发现和路由 | PubSub 节点加入或参与网络 | PubSub 应使用 Kademlia DHT 和 IPFS 网络发现进行对等节点发现和路由。 | 可发现的对等节点和可路由的 Pub/Sub 网络路径。 | 中 | 检查 | E002 |
| FR-010 | 管理集群状态和故障转移 | Redis Proxy 针对集群 Redis 运行 | Redis Proxy 应为基于集群的部署提供集群状态管理和故障转移行为。 | 在节点/状态变化期间持续保持集群感知的代理行为。 | 中 | 测试 | E001 |
| FR-011 | 解析分包 SQL 结果元数据 | 接收到 SQL/MySQL 风格的结果数据包 | 与 SQL 相关的客户端路径应解析结果字段并填充字段名映射。 | 已解析的字段和字段名索引映射。 | 中 | 测试 | E005 |
| FR-012 | 解析分包 SQL 结果行和状态 | 接收到结果行数据包和 EOF/状态数据包 | 与 SQL 相关的客户端路径应读取结果行，并从 EOF/状态数据包中提取警告和状态值。 | 结果行以及警告/状态值。 | 中 | 测试 | E005 |

## 5. 非功能需求

| ID | Quality attribute | Requirement | Priority | Verification | Source evidence | Evidence type |
|---|---|---|---|---|---|---|
| NFR-001 | 兼容性 | Redis Proxy 应兼容独立和集群 Redis 部署。 | 高 | 测试 | E001 | 显式 |
| NFR-002 | 兼容性 | PubSub 应兼容 Redis publish/subscribe 使用模式，以便 Web2 Redis Pub/Sub 应用可以迁移到它。 | 高 | 演示 | E002 | 显式 |
| NFR-003 | 可靠性 | 对于集群 Redis 部署，Redis Proxy 应包含集群状态管理和故障转移能力。 | 高 | 测试 | E001 | 显式 |
| NFR-004 | 网络互操作性 | PubSub 应能在同网、跨网和 NAT/private-network 节点拓扑中运行。 | 高 | 测试 | E002 | 显式 |
| NFR-005 | 许可约束 | 已证明的源文件应在 Apache License 2.0 条款下保持可用。 | 中 | 检查 | E003, E004 | 显式 |

## 6. 数据需求

### 6.1 数据实体 / 对象
| ID | Data entity | Description | Source |
|---|---|---|---|
| DR-001 | Redis 指令/命令 | 在联网 Redis 代理之间同步的指令。 | E001 |
| DR-002 | Redis 存储数据 | Redis 代理写入集群或单点 Redis 存储的数据。 | E001 |
| DR-003 | Pub/Sub 消息 | 在去中心化网络中使用 Redis publish/subscribe 语义交换的消息。 | E002 |
| DR-004 | 对等节点发现/路由数据 | Kademlia DHT 和 IPFS discovery 使用的网络发现和路由信息。 | E002 |
| DR-005 | SQL 结果字段 | 已解析的结果元数据字段。 | E005 |
| DR-006 | SQL 结果行 | 从分包结果中读取的行数据。 | E005 |
| DR-007 | SQL 结果状态/警告 | 从 EOF/状态数据包中提取的警告计数和状态。 | E005 |

### 6.2 输入/输出数据
| Category | Inputs | Outputs | Source |
|---|---|---|---|
| Redis Proxy | Redis 指令；基于 Redis 的应用流量 | 已同步的指令；写入独立或集群 Redis 存储 | E001 |
| PubSub | Redis 风格的发布/订阅操作；加入的节点 | 分布式 Pub/Sub 消息投递；对等节点发现/路由行为 | E002 |
| SQL result handling | 结果数据包 | 已解析字段、字段名映射、行、警告、状态 | E005 |

### 6.3 存储、完整性、保留、迁移
| Requirement | Source | Evidence type |
|---|---|---|
| 该仓库支持将 Redis publish/subscribe Web2 应用用法迁移到去中心化 P2P 订阅网络。 | E002 | 显式 |
| 证据支持将数据写入已配置的 Redis 存储目标，但除 Redis/PubSub 兼容性之外，没有明确说明保留、隐私或迁移机制。 | E001, E002 | 推断 |

## 7. 约束

| ID | Constraint | Source | Evidence type |
|---|---|---|---|
| C-001 | Redis Proxy 部署受限于已证明为独立或集群的 Redis 支撑存储模式。 | E001 | 显式 |
| C-002 | PubSub 协议兼容性受限于 Redis publish/subscribe 语义。 | E002 | 显式 |
| C-003 | PubSub 对等节点发现和路由依赖 Kademlia DHT 和 IPFS 网络发现。 | E002 | 显式 |
| C-004 | 已证明的源文件采用 Apache License 2.0 许可。 | E003, E004 | 显式 |

## 8. 验证与验收

| Requirement IDs | Verification method | Acceptance basis |
|---|---|---|
| FR-001, FR-003, NFR-001 | 测试 | 证明可针对独立和集群 Redis 目标成功运行。 |
| FR-002, FR-004 | 测试 / 演示 | 展示联网代理之间的指令同步和去中心化 Redis 数据同步。 |
| FR-005, FR-006, NFR-002 | 测试 / 演示 | 展示 Redis 风格的发布/订阅交互可在 PubSub 中工作。 |
| FR-007, FR-008, NFR-004 | 测试 | 证明在同网、跨网和 NAT/private-network 场景下的多节点运行。 |
| FR-009, C-003 | 检查 | 验证 Kademlia DHT 和 IPFS discovery/routing 机制的文档化或配置化使用。 |
| FR-010, NFR-003 | 测试 | 证明集群 Redis 部署中的集群状态处理和故障转移。 |
| FR-011, FR-012 | 测试 | 验证从数据包中解析结果字段、字段名映射、行、警告和状态。 |
| NFR-005, C-004 | 检查 | 验证已证明源文件中的 Apache License 2.0 声明。 |

## 9. 可追溯性矩阵

| ID | Requirement | Type | Source | Evidence Type | Verification | Confidence |
|---|---|---|---|---|---|---|
| FR-001 | 支持独立和集群 Redis 模式 | Functional | E001 | explicit | Test | High |
| FR-002 | 在代理之间同步 Redis 指令 | Functional | E001 | explicit | Test | High |
| FR-003 | 将数据写入集群或单点 Redis 存储 | Functional | E001 | explicit | Test | High |
| FR-004 | 启用去中心化 Redis 数据同步 | Functional | E001 | explicit | Demonstration | Medium |
| FR-005 | 支持 Redis publish/subscribe 协议 | Functional | E002 | explicit | Test | High |
| FR-006 | 保留类 Redis 的 Pub/Sub 用法 | Functional | E002 | explicit | Demonstration | High |
| FR-007 | 支持跨网络的多节点 Pub/Sub | Functional | E002 | explicit | Test | High |
| FR-008 | 支持 NAT/private-network 节点通信 | Functional | E002 | explicit | Test | High |
| FR-009 | 使用 Kademlia DHT 和 IPFS discovery/routing | Functional | E002 | explicit | Inspection | Medium |
| FR-010 | 提供集群状态管理和故障转移 | Functional | E001 | explicit | Test | Medium |
| FR-011 | 解析 SQL 结果字段和字段名映射 | Functional | E005 | explicit | Test | Medium |
| FR-012 | 解析 SQL 结果行、警告和状态 | Functional | E005 | explicit | Test | Medium |
| NFR-001 | 与独立和集群 Redis 的兼容性 | Non-functional | E001 | explicit | Test | High |
| NFR-002 | 与 Redis Pub/Sub 迁移/使用的兼容性 | Non-functional | E002 | explicit | Demonstration | High |
| NFR-003 | 通过集群状态管理和故障转移实现可靠性 | Non-functional | E001 | explicit | Test | Medium |
| NFR-004 | 跨不同拓扑的网络互操作性 | Non-functional | E002 | explicit | Test | High |
| NFR-005 | Apache License 2.0 许可 | Non-functional | E003, E004 | explicit | Inspection | High |
| C-001 | 基于 Redis 的部署模式仅限于独立/集群证据 | Constraint | E001 | explicit | Inspection | High |
| C-002 | PubSub 受限于 Redis publish/subscribe 语义 | Constraint | E002 | explicit | Inspection | High |
| C-003 | 依赖 Kademlia DHT 和 IPFS discovery | Constraint | E002 | explicit | Inspection | High |
| C-004 | Apache License 2.0 源码约束 | Constraint | E003, E004 | explicit | Inspection | High |
