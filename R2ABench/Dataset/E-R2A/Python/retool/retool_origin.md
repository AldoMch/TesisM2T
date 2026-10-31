# I组-ReTool-需求规格说明书

| 版本   | 提交日期   | 修改说明                                                 | 编制人员                                                     | 审核人员 |
| ------ | ---------- | -------------------------------------------------------- | ------------------------------------------------------------ | -------- |
| v1.0.0 | 2022.03.17 | 文档初稿                                                 | 管政、刘泽华、王正达、郭映秀、付佳辉、郭瑞宇、倪正泽（I组全体人员） | 管政     |
| v1.1.0 | 2022.03.24 | 增加活动图，增加术语和缩略语，需求功能细化，调整文档结构 | 管政、刘泽华、王正达、郭映秀、付佳辉、郭瑞宇、倪正泽（I组全体人员） | 管政     |
| v1.2.0 | 2022.03.29 | 按照评审意见对需求规格说明书进行修改                     | 管政、刘泽华、王正达、郭映秀、付佳辉、郭瑞宇、倪正泽（I组全体人员） | 管政     |
| v1.3.0 |            | 按照评审意见对需求规格说明书进行修改                     | 管政、刘泽华、王正达、郭映秀、付佳辉、郭瑞宇、倪正泽（I组全体人员） | 管政     |

**注：本规格说明书是使用Typora软件书写的，若有任何格式问题可能是gitlab渲染问题，建议先用Typora打开文件查看。**

# 目录

- [1 引言](#1-%E5%BC%95%E8%A8%80)
  - [1.1 目的](#11-%E7%9B%AE%E7%9A%84)
  - [1.2 范围](#12-%E8%8C%83%E5%9B%B4)
  - [1.3 术语和缩略语](#13-%E6%9C%AF%E8%AF%AD%E5%92%8C%E7%BC%A9%E7%95%A5%E8%AF%AD)
    - [1.3.1 微服务](#131-%E5%BE%AE%E6%9C%8D%E5%8A%A1)
    - [1.3.2 Flask](#132-flask)
    - [1.3.3 NLP](#133-nlp)
    - [1.3.4 PyTorch](#134-pytorch)
    - [1.3.5 Vue.js框架](#135-vuejs%E6%A1%86%E6%9E%B6)
    - [1.3.6 MongoDB数据库](#136-mongodb%E6%95%B0%E6%8D%AE%E5%BA%93)
  - [1.4 引用文件](#14-%E5%BC%95%E7%94%A8%E6%96%87%E4%BB%B6)
  - [1.5 综述](#15-%E7%BB%BC%E8%BF%B0)
  
- [2 总体描述](#2-%E6%80%BB%E4%BD%93%E6%8F%8F%E8%BF%B0)
  - [2.1 产品描述](#21-%E4%BA%A7%E5%93%81%E6%8F%8F%E8%BF%B0)
  - [2.2 产品功能](#22-%E4%BA%A7%E5%93%81%E5%8A%9F%E8%83%BD)
  - [2.3 用户特点](#23-%E7%94%A8%E6%88%B7%E7%89%B9%E7%82%B9)
  - [2.4 约束](#24-%E7%BA%A6%E6%9D%9F)
  - [2.5 假设和依赖关系](#25-%E5%81%87%E8%AE%BE%E5%92%8C%E4%BE%9D%E8%B5%96%E5%85%B3%E7%B3%BB)
    - [2.5.1 运行环境](#251-%E8%BF%90%E8%A1%8C%E7%8E%AF%E5%A2%83)
    - [2.5.2 网络](#252-%E7%BD%91%E7%BB%9C)
  
- [3  具体需求](#3--%E5%85%B7%E4%BD%93%E9%9C%80%E6%B1%82)
  - [3.1 功能性需求](#31-%E5%8A%9F%E8%83%BD%E6%80%A7%E9%9C%80%E6%B1%82)
    - [3.1.1 用户管理模块相关需求](#311-%E7%94%A8%E6%88%B7%E7%AE%A1%E7%90%86%E6%A8%A1%E5%9D%97%E7%9B%B8%E5%85%B3%E9%9C%80%E6%B1%82)
      - [3.1.1.1 用户注册](#3111-%E7%94%A8%E6%88%B7%E6%B3%A8%E5%86%8C)
      - [3.1.1.2 用户登录](#3112-%E7%94%A8%E6%88%B7%E7%99%BB%E5%BD%95)
      - [3.1.1.3 用户登出](#3113-%E7%94%A8%E6%88%B7%E7%99%BB%E5%87%BA)
      - [3.1.1.4 删除用户](#3.1.1.4 删除用户)
      - [3.1.1.5 修改用户密码](#3115-%E4%BF%AE%E6%94%B9%E7%94%A8%E6%88%B7%E5%AF%86%E7%A0%81)
      - [3.1.1.6 查看用户列表](#3116-%E6%9F%A5%E7%9C%8B%E7%94%A8%E6%88%B7%E5%88%97%E8%A1%A8)
      - [3.1.1.7 查看用户个人信息](#3117-%E6%9F%A5%E7%9C%8B%E7%94%A8%E6%88%B7%E4%B8%AA%E4%BA%BA%E4%BF%A1%E6%81%AF)
      - [3.1.1.8 重置用户密码](#3118-%E9%87%8D%E7%BD%AE%E7%94%A8%E6%88%B7%E5%AF%86%E7%A0%81)
      - [3.1.1.9 修改用户角色](#3119-%E4%BF%AE%E6%94%B9%E7%94%A8%E6%88%B7%E8%A7%92%E8%89%B2)
      - [3.1.1.10 添加用户](#31110-%E6%B7%BB%E5%8A%A0%E7%94%A8%E6%88%B7)
    - [3.1.2 项目管理模块相关需求](#312-%E9%A1%B9%E7%9B%AE%E7%AE%A1%E7%90%86%E6%A8%A1%E5%9D%97%E7%9B%B8%E5%85%B3%E9%9C%80%E6%B1%82)
      - [3.1.2.1 创建项目](#3121-%E5%88%9B%E5%BB%BA%E9%A1%B9%E7%9B%AE)
      - [3.1.2.2 删除项目](#3122-%E5%88%A0%E9%99%A4%E9%A1%B9%E7%9B%AE)
      - [3.1.2.3 修改项目](#3123-%E4%BF%AE%E6%94%B9%E9%A1%B9%E7%9B%AE)
      - [3.1.2.4 查看项目](#3124-%E6%9F%A5%E7%9C%8B%E9%A1%B9%E7%9B%AE)
      - [3.1.2.5 查看项目列表](#3125-%E6%9F%A5%E7%9C%8B%E9%A1%B9%E7%9B%AE%E5%88%97%E8%A1%A8)
      - [3.1.2.6 创建项目基线节点](#3126-%E5%88%9B%E5%BB%BA%E9%A1%B9%E7%9B%AE%E5%9F%BA%E7%BA%BF%E8%8A%82%E7%82%B9)
      - [3.1.2.7 查看项目基线节点](#3127-%E6%9F%A5%E7%9C%8B%E9%A1%B9%E7%9B%AE%E5%9F%BA%E7%BA%BF%E8%8A%82%E7%82%B9)
      - [3.1.2.8 修改项目信息](#3128-%E4%BF%AE%E6%94%B9%E9%A1%B9%E7%9B%AE%E4%BF%A1%E6%81%AF)
      - [3.1.2.9 修改项目成员](#3129-%E4%BF%AE%E6%94%B9%E9%A1%B9%E7%9B%AE%E6%88%90%E5%91%98)
      - [3.1.2.10 查看项目信息](#31210-%E6%9F%A5%E7%9C%8B%E9%A1%B9%E7%9B%AE%E4%BF%A1%E6%81%AF)
      - [3.1.2.11 查看项目成员](#31211-%E6%9F%A5%E7%9C%8B%E9%A1%B9%E7%9B%AE%E6%88%90%E5%91%98)
      - [3.1.2.12 添加项目成员](#31212-%E6%B7%BB%E5%8A%A0%E9%A1%B9%E7%9B%AE%E6%88%90%E5%91%98)
      - [3.1.2.13 删除项目成员](#31213-%E5%88%A0%E9%99%A4%E9%A1%B9%E7%9B%AE%E6%88%90%E5%91%98)
      - [3.1.2.14 修改项目角色](#31214-%E4%BF%AE%E6%94%B9%E9%A1%B9%E7%9B%AE%E8%A7%92%E8%89%B2)
    - [3.1.3 “需求管理”相关需求](#313-%E9%9C%80%E6%B1%82%E7%AE%A1%E7%90%86%E7%9B%B8%E5%85%B3%E9%9C%80%E6%B1%82)
      - [3.1.3.1 创建需求条目](#3131-%E5%88%9B%E5%BB%BA%E9%9C%80%E6%B1%82%E6%9D%A1%E7%9B%AE)
      - [3.1.3.2 创建单条需求条目](#3132-%E5%88%9B%E5%BB%BA%E5%8D%95%E6%9D%A1%E9%9C%80%E6%B1%82%E6%9D%A1%E7%9B%AE)
      - [3.1.3.3 从word导入需求条目](#3133-%E4%BB%8Eword%E5%AF%BC%E5%85%A5%E9%9C%80%E6%B1%82%E6%9D%A1%E7%9B%AE)
      - [3.1.3.4 需求条目化](#3134-%E9%9C%80%E6%B1%82%E6%9D%A1%E7%9B%AE%E5%8C%96)
      - [3.1.3.5 删除需求条目](#3135-%E5%88%A0%E9%99%A4%E9%9C%80%E6%B1%82%E6%9D%A1%E7%9B%AE)
      - [3.1.3.6 修改需求条目](#3136-%E4%BF%AE%E6%94%B9%E9%9C%80%E6%B1%82%E6%9D%A1%E7%9B%AE)
      - [3.1.3.7 修改需求条目内容](#3137-%E4%BF%AE%E6%94%B9%E9%9C%80%E6%B1%82%E6%9D%A1%E7%9B%AE%E5%86%85%E5%AE%B9)
      - [3.1.3.8 移动需求条目位置](#3138-%E7%A7%BB%E5%8A%A8%E9%9C%80%E6%B1%82%E6%9D%A1%E7%9B%AE%E4%BD%8D%E7%BD%AE)
      - [3.1.3.9 建立需求正向追踪](#3139-%E5%BB%BA%E7%AB%8B%E9%9C%80%E6%B1%82%E6%AD%A3%E5%90%91%E8%BF%BD%E8%B8%AA)
      - [3.1.3.10 需求分析](#31310-%E9%9C%80%E6%B1%82%E5%88%86%E6%9E%90)
      - [3.1.3.11 需求结构化](#31311-%E9%9C%80%E6%B1%82%E7%BB%93%E6%9E%84%E5%8C%96)
      - [3.1.3.12 共性需求识别](#31312-%E5%85%B1%E6%80%A7%E9%9C%80%E6%B1%82%E8%AF%86%E5%88%AB)
      - [3.1.3.13 需求冲突检测](#31313-%E9%9C%80%E6%B1%82%E5%86%B2%E7%AA%81%E6%A3%80%E6%B5%8B)
      - [3.1.3.14 需求关联关系分析](#31314-%E9%9C%80%E6%B1%82%E5%85%B3%E8%81%94%E5%85%B3%E7%B3%BB%E5%88%86%E6%9E%90)
      - [3.1.1.15 查看需求条目树](#31115-%E6%9F%A5%E7%9C%8B%E9%9C%80%E6%B1%82%E6%9D%A1%E7%9B%AE%E6%A0%91)
      - [3.1.1.16 查看需求条目内容](#31116-%E6%9F%A5%E7%9C%8B%E9%9C%80%E6%B1%82%E6%9D%A1%E7%9B%AE%E5%86%85%E5%AE%B9)
      - [3.1.1.17 查看需求正向追踪](#31117-%E6%9F%A5%E7%9C%8B%E9%9C%80%E6%B1%82%E6%AD%A3%E5%90%91%E8%BF%BD%E8%B8%AA)
    
  - [3.2 设计约束](#32-%E8%AE%BE%E8%AE%A1%E7%BA%A6%E6%9D%9F)
  
  - [3.3 非功能性需求](#33-%E9%9D%9E%E5%8A%9F%E8%83%BD%E6%80%A7%E9%9C%80%E6%B1%82)
    - [3.3.1 响应时间](#331-%E5%93%8D%E5%BA%94%E6%97%B6%E9%97%B4)
    - [3.3.2 可靠性](#332-%E5%8F%AF%E9%9D%A0%E6%80%A7)
    - [3.3.3 安全保密性](#333-%E5%AE%89%E5%85%A8%E4%BF%9D%E5%AF%86%E6%80%A7)
    - [3.3.4 可维护性](#334-%E5%8F%AF%E7%BB%B4%E6%8A%A4%E6%80%A7)
    
    - [3.3.5 交互设计需求](#335-%E4%BA%A4%E4%BA%92%E8%AE%BE%E8%AE%A1%E9%9C%80%E6%B1%82)
    - [3.3.6 界面设计需求](#336-%E7%95%8C%E9%9D%A2%E8%AE%BE%E8%AE%A1%E9%9C%80%E6%B1%82)



## 1 引言

### 1.1 目的

本文档首先给出项目的概述，由此从总体架构上给出整个系统的轮廓；同时对功能性需求、非功能性需求进行了详细的描述，以简化用户、开发人员的理解和交流，反映出用户问题的核心；最后，本文档可作为软件开发工作的基础和依据以及确认测试和验收的依据。

### 1.2 范围

本文档主要阐述了项目的背景、用户类型、开发规范、主要内容与范围、人员职责及详细功能，文档整体按照：引言、总体描述、具体需求三个方面对阐述内容进行结构性组织。

### 1.3 术语和缩略语

#### 1.3.1 微服务

微服务并没有统一和严格的定义，而是指一种新的软件架构模式。在微服务的架构设计下，系统被拆分成一些协同工作的小而自治的服务。与传统单体架构中常用的模块化的代码组织不同，微服务架构将系统拆分成多个服务，每个服务都是一个独立的实体。服务可以单独地进行开发、修改、部署和升级。服务之间通过网络通信进行交互，增强了服务之间的隔离性，降低了耦合性。

#### 1.3.2 Flask

Flask是一款由Python语言编写的Web框架。与Apache、Django等大型Web框架相比，Flask的最大特点就是轻量级。正如Flask官方文档的介绍Flask是一个“微框架”。“微框架”中的“微”并不是说 Flask缺少某些功能，而是指 Flask 的理念是使核心保持简单但可扩展。
Flask 本身只依赖两个模块，一个是用于开发调试、处理HTTP事务的Werkzeug库，一个是模板引擎Jinjia2库。除此之外，Flask并不包含数据库集成、表单验证、身份验证等功能，但是我们可以根据实际需求进行灵活地扩展。这也意味着Flask这一“微框架”足以满足各种需求的生产用途。
Flask的配置和使用也非常的简单，最简单的Flask只需一个Python文件即可运行，正因为 Flask 的“微框架”特性，使得它不仅容易上手，还可以根据我们实际的项目需求进行灵活的扩展，非常适合微服务架构下服务端代码的编写。

#### 1.3.3 NLP

自然语言处理（Natural Language Processing， NLP）是计算机科学领域与人工智能领域中的一个重要方向。它研究能实现人与计算机之间用自然语言进行有效通信的各种理论和方法。

#### 1.3.4 PyTorch

PyTorch是一个基于Torch的Python开源机器学习库，用于自然语言处理等应用程序。它主要由Facebook的人工智能小组开发，不仅能够支持强大的GPU加速，同时还支持动态神经网络。

#### 1.3.5 Vue.js框架

Vue.js（以下简称Vue）是一个由我国前端开发者尤雨溪开源的，用于构建用户界面的轻量级渐进式框架。与其他自上而下的大型框架相比，Vue采用了自下而上的开发设计模式。开发者可以从底部开始构建，并逐层引用，具有很高的灵活性。

#### 1.3.6 MongoDB数据库
MongoDB是MongoDB公司的前身10gen公司于2009年开源的一款面向文档的NoSQL（Not Only SQL）数据库，该数据库采用C++语言编写。

### 1.4 引用文件

1. GB/T 9385-2008《计算机软件需求规格说明规范》
2. GB/T 20918-2007《信息技术、软件生存周期过程及风险管理》
3. GB/T 15532 -2008《计算机软件测试规范》
4. GB/T 20917-2007《软件工程及软件测量过程》

### 1.5 综述

本篇需求规格说明书主要分为三个部分。

第一章引言简要介绍了本文档的目的、范围、术语和缩略语及引用文件。

第二章总体描述主要对产品的总体和功能进行了描述，同时分析了用户的特点、约束及假设和依赖关系。

第三章具体需求首先介绍了系统的整体设计，随后分功能模块，分别介绍了用户管理模块、项目管理模块、需求管理模块的相关功能。最后从设计约束、性能需求、软件系统属性及其他需求几方面描述了非功能性需求。

## 2 总体描述

### 2.1 产品描述

近年来，伴随着信息技术的快速发展，软件行业的规模不断扩大，软件的复杂度也越来越高，软件的需求很难在开发前完全确定下来，软件项目往往处于持续演化的过程中。需求的不断变化会引起软件设计、代码实现、测试用例等一系列变化。对于需求变化的不当管理，不仅浪费了不必要的人力、财力与物力，还可能导致项目的延期和失败。

如表2-1所示，目前市面上流行的几款软件需求管理工具，虽然可以在软件持续演化的过程中对需求的变化进行管理，但是仍存在着需求的导入和分析不够自动化、功能过于繁杂、用户学习成本过高等不足。

<center>表2-1 三款主流软件需求管理工具功能对比</center>

| **工具名称** | **将导入的需求文本条目化** | **需求的结构化**     | **需求间冲突识别与分析**    | **共性需求的识别与分析** | **需求间的关联关系分析**                       |
| ------------------ | ------------------ |  ------------------ | ------------------ |------------------ |------------------------------------------------ |
| IBM Rational RequisitePro           | 无   | 无| 无| 无          | 手动建立关联关系，可创建层次关系、追踪关系,当子需求或追踪需求变更后，自动分析可疑关系                   |
| IBM Rational DOORS           | 对大段的需求描述文本拆分，以条目的形式展示             | 无  | 无| 无| 手动建立关联关系，可创建需求间的追踪关系               |
| Borland CaliberRM     | 无      | 无| 无| 无       | 手动建立关联关系，可创建需求间的追踪关系                           |

我们集成了需求条目化、需求结构化、需求冲突检测和需求关联关系分析等算法，并在需求结构化处理结果的基础上，基于 Word2vec 模型提出共性需求识别算法，最终需要实现一款面向持续演化的软件需求管理工具。此外，设计了需求的正向追踪功能，允许用户设置并管理需求到设计模块及测试用例的追踪。工具整体上采用前后端分离的模式，客户端使用 Vue.js 框架开发出了一套简洁美观的网页用户界面，服务端使用了微服务作为设计架构，具有很高的灵活性和很强的扩展性。

工具通过需求条目化算法，可以自动化地从导入的需求文本中获取清晰明确的需求条目；通过共性需求识别、需求冲突检测以及需求关联关系分析算法，可以自动化地进行需求分析，进而能够对需求变更的影响进行提前分析和预判，具有创新意义；通过正向追踪，辅助面向变更需求的开发与测试工作，加速了软件项目的演化进程。

### 2.2 产品功能

系统应当包括三个主要方面：

1. 用户管理，包括添加用户、删除用户、修改用户信息、搜索用户等。
2. 项目管理，包括创建项目、删除项目、修改项目信息、搜索项目等。
3. 需求管理，创建需求条目、删除需求条目、修改需求条目、获取需求条目内容和需求分析等。

### 2.3 用户特点

本系统面向的主要用户有项目组成员和ReTool团队成员。

其中，项目组成员主要有项目经理、项目组长和项目组普通成员，项目经理和项目组长需要使用项目管理工具进行需求的变更，需求变更主要包括创建需求和修改需求，而项目组普通成员则需要根据需求来完成开发和测试。每个用户可以参与不同的项目，在不同的项目中可以承担不同的角色，并拥有不同的权限。

ReTool团队成员则需要维护软件的正常运行，因为具有添加新用户、删除用户、修改用户系统角色、重置密码的权限。

<center>表2-2 用户职责描述</center>

| **角色名称** | **所属组织** | **职责描述**                               |
| ------------------ | ------------------ | ------------------------------------------------ |
| 项目经理           | 项目组             | 项目总负责人，通过使用工具来创建需求和修改需求                   |
| 项目组长           | 项目组             | 通过使用工具来创建需求和修改需求                 |
| 项目组普通成员     | 项目组             | 根据需求进行开发和测试                           |
| 系统管理员         | ReTool团队         | 维护软件的正常运行，并收集其他用户对该软件的建议 |

### 2.4 约束

我们做出以下约束，以保证软件项目能够按时开发完成和投入运行、维护：

1. 变更需求需要严格按照需求变更流程执行，并对需求规格说明书进行合理的修改与审核。
2. 工具整体上采用了前后端分离的模式，为便于维护，前端应使用一种轻量、社区环境优秀、易于维护的框架。
3. 在系统运行时，需要限制同一时刻的访问量，以保证系统安全稳定运行。如果超出同时访问的峰值，则系统会对其中一些用户进程进行阻塞等待，直到系统的当前承载量可以处理新的用户进程时，会继续执行被阻塞的操作。

### 2.5 假设和依赖关系

#### 2.5.1 运行环境

服务端中，网关、用户管理服务、项目管理服务和需求管理服务均运行在本地计算机上，算法服务由于对机器性能要求较高，所以运行在服务器上。

#### 2.5.2 网络

如果用户无法进行网络连接，则所有需求无法实现。

## 3  具体需求

### 3.1 功能性需求

本节将给出详细的功能性需求，共分为三个模块的需求：用户管理模块、项目管理模块和“需求管理”模块。我们为每个模块绘制了用例图，对具体需求采用RUCM表格和文字的方式进行描述，并针对复杂需求绘制了活动图，在此给出活动图泳道说明。

活动图泳道说明：

- 活动图包括参与者、处理逻辑和数据库三个泳道
- 系统在活动图被拆解为两个部分：**处理逻辑**和**数据库**
- 处理逻辑代表本系统的前后端、算法等模块，接收用户的指令并进行响应，但需要依赖数据库才能接触到数据
- 数据库代表本系统使用的MongoDB数据库，接受处理逻辑的指令，对数据进行增删改查，并将数据或执行结果呈递给处理逻辑

| 需求模块               | 需求场景                                                     | 举例                                                         |
| ---------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| 用户管理模块相关需求   | 由于本系统需要用户在登录后才能使用，因此用户管理模块是本系统的基础需求。<br />该模块面向普通用户需要登录本系统以及查看和修改个人信息的场景，同时面向管理员管理用户的场景。 | 以“重置用户密码”为例，用户可能由于种种原因忘记自己的登录密码，因而需要管理员具有重置用户密码的权限。 |
| 项目管理模块相关需求   | 该模块面向不同角色的用户提供管理和查看项目的场景。           | 以“创建项目”为例，当因为业务要求需要开展新项目时，项目经理需要创建新项目进行管理。 |
| “需求管理”模块相关需求 | 该模块面向不同角色的用户提供管理、查看和分析需求的场景。     | 以“需求分析”为例，项目经理或项目组长为更好地把握需求要求，需要借助需求冲突检测等需求分析技术进行辅助。 |

#### 3.1.1 用户管理模块相关需求

由于本系统需要用户在登录后才能使用，因此用户管理模块是本系统的基础需求。该模块主要面向普通用户登录本系统以及查看和修改个人信息的场景，同时面向管理员管理用户的场景。以重置用户密码为例，用户可能由于种种原因忘记自己的登录密码，因而需要管理员具有重置用户密码的权限。

1. 用户角色定义

工具中的用户角色共分为两类：系统角色和项目角色。

系统角色是用户在工具内的角色，包括系统管理员和系统用户。其中，系统管理员是软件运维人员的固有账号，具有添加新用户、删除用户、修改用户系统角色，而系统用户没有上述权限。

而系统用户又存在不同的项目角色，项目角色共分为：项目经理、项目组长和普通成员。每个用户可以参与不同的项目，在不同的项目中可以承担不同的角色，并拥有不同的权限。

2. 用户管理模块用例图

用户管理功能的用例图如图3-1：

![用户管理功能用例图.jpg](./images/用户管理模块用例图.jpg)
<center>图3-1 用户管理模块用例图</center>

##### 3.1.1.1 用户注册

用户访问系统主界面，进入注册界面后完成用户注册。

具体的UML活动图如图3-2：

![需求管理功能用例图.jpg](./images/用户注册活动图.jpg)
<center>图3-2 用户注册活动图</center>

<center>表3-1 用户注册RUCM</center>

<table border=0 cellpadding=0 cellspacing=0 width=627 style='border-collapse:
 collapse;table-layout:auto;'>
 <col width=150 style='mso-width-source:userset;mso-width-alt:5120;'>
 <col width=67 style='mso-width-source:userset;mso-width-alt:2269;'>
 <col width=68 style=''>
 <col width=342 style='mso-width-source:userset;mso-width-alt:11656;'>
 <tr height=21 style='height:15.75pt'>
  <td colspan=4 height=21 class=xl74 width=627 style='border-right:1.0pt ;
  height:15.75pt;'>Use Case Specification</td>
 </tr>
 <tr height=22 style='height:16.15pt'>
  <td height=22 class=xl65 width=150 style='height:16.15pt;'>Use
  Case Name</td>
  <td colspan=3 class=xl71 style='border-right:1.0pt ;border-left:
  none'>用户注册</td>
 </tr>
 <tr height=96 style='mso-height-source:userset;height:72.0pt'>
  <td height=96 class=xl65 width=150 style='height:72.0pt;'>Brief
  Description</td>
  <td colspan=3 class=xl71 style='border-right:1.0pt ;border-left:
  none'>用户注册用户名和密码</td>
 </tr>
 <tr height=96 style='mso-height-source:userset;height:72.0pt'>
  <td height=96 class=xl65 width=150 style='height:72.0pt;'>Precondition</td>
  <td colspan=3 class=xl71 style='border-right:1.0pt ;border-left:
  none'>无</td>
 </tr>
 <tr height=22 style='height:16.15pt'>
  <td height=22 class=xl65 width=150 style='height:16.15pt;'>Primary
  Actor</td>
  <td colspan=3 class=xl71 style='border-right:1.0pt ;border-left:
  none'>系统用户</td>
 </tr>
 <tr height=22 style='height:16.15pt'>
  <td height=22 class=xl65 width=150 style='height:16.15pt;'>Secondary
  Actors</td>
  <td colspan=3 class=xl71 style='border-right:1.0pt ;border-left:
  none'>无</td>
 </tr>
 <tr height=22 style='height:16.15pt'>
  <td height=22 class=xl65 width=150 style='height:16.15pt;'>Dependency</td>
  <td colspan=3 class=xl71 style='border-right:1.0pt ;border-left:
  none'>无</td>
 </tr>
 <tr height=22 style='height:16.15pt'>
  <td height=22 class=xl65 width=150 style='height:16.15pt;'>Generalization<span
  style='mso-spacerun:yes'> </span></td>
  <td colspan=3 class=xl71 style='border-right:1.0pt ;border-left:
  none'>无</td>
 </tr>
 <tr height=21 style='height:15.4pt'>
  <td rowspan=7 height=469 class=xl77 width=150 style='border-bottom:1.0pt ;
  height:351.05pt;border-top:none;'>Basic Flow</td>
  <td colspan=3 class=xl79 style='border-right:1.0pt ;border-left:
  none'>Steps</td>
 </tr>
 <tr height=96 style='mso-height-source:userset;height:72.0pt'>
  <td height=96 class=xl69 style='height:72.0pt'>1</td>
  <td colspan=2 class=xl71 style='border-right:1.0pt ;border-left:
  none'>用户访问主界面</td>
 </tr>
 <tr height=96 style='mso-height-source:userset;height:72.0pt'>
  <td height=96 class=xl69 style='height:72.0pt'>2</td>
  <td colspan=2 class=xl82 width=410 style='border-right:1.0pt ;
  border-left:none;'>用户点击用户注册跳转至注册界面</td>
 </tr>
 <tr height=96 style='mso-height-source:userset;height:72.0pt'>
  <td height=96 class=xl69 style='height:72.0pt'>3</td>
  <td colspan=2 class=xl84 width=410 style='border-right:1.0pt ;
  border-left:none;'>用户在用户注册界面填写用户名和密码</td>
 </tr>
 <tr height=96 style='mso-height-source:userset;height:72.0pt'>
  <td height=96 class=xl69 style='height:72.0pt'>4</td>
  <td colspan=2 class=xl71 style='border-right:1.0pt ;border-left:
  none'>用户点击注册按钮</td>
 </tr>
 <tr height=96 style='mso-height-source:userset;height:72.0pt'>
  <td height=96 class=xl69 style='height:72.0pt'>5</td>
  <td colspan=2 class=xl71 style='border-right:1.0pt ;border-left:
  none'>提示用户注册成功并自动跳转到登录界面</td>
 </tr>
 <tr height=64 style='height:47.65pt'>
  <td colspan=2 height=64 class=xl79 style='border-right:1.0pt ;
  height:47.65pt;border-left:none'>PostCondition</td>
  <td class=xl70>用户成功注册，数据库成功保存用户用户名和密码</td>
 </tr>
 <tr height=21 style='height:15.4pt'>
  <td rowspan=4 height=65 class=xl77 width=150 style='border-bottom:1.0pt ;
  height:47.7pt;border-top:none;'>Specific Alternative Flow</td>
  <td class=xl68 width=67 style='border-top:none;'>RFS</td>
  <td colspan=2 class=xl86 width=410 style='border-right:1.0pt ;
  border-left:none;'>5</td>
 </tr>
 <tr height=22 style='height:16.15pt'>
  <td height=22 class=xl66 width=67 style='height:16.15pt;'>1</td>
  <td colspan=2 class=xl88 width=410 style='border-right:1.0pt ;
  border-left:none;'>系统提示用户名重复</td>
 </tr>
 <tr height=22 style='height:16.15pt'>
  <td height=22 class=xl66 width=67 style='height:16.15pt;'>2</td>
  <td colspan=2 class=xl88 width=410 style='border-right:1.0pt ;
  border-left:none;'>RESUME STEP</td>
 </tr>
 <tr height=22 style='height:16.15pt'>
  <td colspan=2 height=22 class=xl90 width=135 style='border-right:1.0pt ;
  height:16.15pt;border-left:none;'>PostCondition</td>
  <td class=xl67 width=342 style=''>系统回到注册界面</td>
 </tr>
 <tr height=21 style='height:15.4pt'>
  <td rowspan=5 height=87 class=xl77 width=150 style='border-bottom:1.0pt ;
  height:63.85pt;border-top:none;'>Specific Alternative Flow</td>
  <td class=xl68 width=67 style='border-top:none;'>RFS</td>
  <td colspan=2 class=xl86 width=410 style='border-right:1.0pt ;
  border-left:none;'>5</td>
 </tr>
 <tr height=22 style='height:16.15pt'>
  <td height=22 class=xl66 width=67 style='height:16.15pt;'>1</td>
  <td colspan=2 class=xl88 width=410 style='border-right:1.0pt ;
  border-left:none;'>系统提示密码不符合要求</td>
 </tr>
 <tr height=22 style='height:16.15pt'>
  <td height=22 class=xl66 width=67 style='height:16.15pt;'>2</td>
  <td colspan=2 class=xl88 width=410 style='border-right:1.0pt ;
  border-left:none;'>系统提示密码具体要求</td>
 </tr>
 <tr height=22 style='height:16.15pt'>
  <td height=22 class=xl66 width=67 style='height:16.15pt;'>3</td>
  <td colspan=2 class=xl88 width=410 style='border-right:1.0pt ;
  border-left:none;'>RESUME STEP</td>
 </tr>
 <tr height=22 style='height:16.15pt'>
  <td colspan=2 height=22 class=xl90 width=135 style='border-right:1.0pt ;
  height:16.15pt;border-left:none;'>PostCondition</td>
  <td class=xl67 width=342 style=''>系统回到注册界面</td>
 </tr>
</table>




##### 3.1.1.2 用户登录

用户访问系统主页面，通过用户名和密码登录系统。

具体的UML活动图如图3-3：

![需求管理功能用例图.jpg](./images/用户登录活动图.jpg)
<center>图3-3 用户登录活动图</center>

<center>表3-2 用户登录RUCM</center>

<table border=0 cellpadding=0 cellspacing=0 width=627 style='border-collapse:
 collapse;table-layout:auto;'>
 <col width=150 style='mso-width-source:userset;mso-width-alt:5120;'>
 <col width=67 style='mso-width-source:userset;mso-width-alt:2269;'>
 <col width=68 style=''>
 <col width=342 style='mso-width-source:userset;mso-width-alt:11656;'>
 <tr height=21 style='height:15.75pt'>
  <td colspan=4 height=21 class=xl74 width=627 style='border-right:1.0pt ;
  height:15.75pt;'>Use Case Specification</td>
 </tr>
 <tr height=22 style='height:16.15pt'>
  <td height=22 class=xl65 width=150 style='height:16.15pt;'>Use
  Case Name</td>
  <td colspan=3 class=xl71 style='border-right:1.0pt ;border-left:
  none'>用户登录</td>
 </tr>
 <tr height=96 style='mso-height-source:userset;height:72.0pt'>
  <td height=96 class=xl65 width=150 style='height:72.0pt;'>Brief
  Description</td>
  <td colspan=3 class=xl71 style='border-right:1.0pt ;border-left:
  none'>用户使用用户名和密码登录系统</td>
 </tr>
 <tr height=96 style='mso-height-source:userset;height:72.0pt'>
  <td height=96 class=xl65 width=150 style='height:72.0pt;'>Precondition</td>
  <td colspan=3 class=xl71 style='border-right:1.0pt ;border-left:
  none'>用户已注册</td>
 </tr>
 <tr height=22 style='height:16.15pt'>
  <td height=22 class=xl65 width=150 style='height:16.15pt;'>Primary
  Actor</td>
  <td colspan=3 class=xl71 style='border-right:1.0pt ;border-left:
  none'>系统管理员、系统用户</td>
 </tr>
 <tr height=22 style='height:16.15pt'>
  <td height=22 class=xl65 width=150 style='height:16.15pt;'>Secondary
  Actors</td>
  <td colspan=3 class=xl71 style='border-right:1.0pt ;border-left:
  none'>无</td>
 </tr>
 <tr height=22 style='height:16.15pt'>
  <td height=22 class=xl65 width=150 style='height:16.15pt;'>Dependency</td>
  <td colspan=3 class=xl71 style='border-right:1.0pt ;border-left:
  none'>无</td>
 </tr>
 <tr height=22 style='height:16.15pt'>
  <td height=22 class=xl65 width=150 style='height:16.15pt;'>Generalization<span
  style='mso-spacerun:yes'> </span></td>
  <td colspan=3 class=xl71 style='border-right:1.0pt ;border-left:
  none'>无</td>
 </tr>
 <tr height=21 style='height:15.4pt'>
  <td rowspan=6 height=469 class=xl77 width=150 style='border-bottom:1.0pt ;
  height:351.05pt;border-top:none;'>Basic Flow</td>
  <td colspan=3 class=xl79 style='border-right:1.0pt ;border-left:
  none'>Steps</td>
 </tr>
 <tr height=96 style='mso-height-source:userset;height:72.0pt'>
  <td height=96 class=xl69 style='height:72.0pt'>1</td>
  <td colspan=2 class=xl71 style='border-right:1.0pt ;border-left:
  none'>用户访问系统主界面</td>
 </tr>
 <tr height=96 style='mso-height-source:userset;height:72.0pt'>
  <td height=96 class=xl69 style='height:72.0pt'>2</td>
  <td colspan=2 class=xl82 width=410 style='border-right:1.0pt ;
  border-left:none;'>用户输入用户名和密码</td>
 </tr>
 <tr height=96 style='mso-height-source:userset;height:72.0pt'>
  <td height=96 class=xl69 style='height:72.0pt'>3</td>
  <td colspan=2 class=xl84 width=410 style='border-right:1.0pt ;
  border-left:none;'>系统确认用户名存在并且密码正确</td>
 </tr>
 <tr height=96 style='mso-height-source:userset;height:72.0pt'>
  <td height=96 class=xl69 style='height:72.0pt'>4</td>
  <td colspan=2 class=xl71 style='border-right:1.0pt ;border-left:
  none'>系统提示用户登录成功</td>
 </tr>
 <tr height=64 style='height:47.65pt'>
  <td colspan=2 height=64 class=xl79 style='border-right:1.0pt ;
  height:47.65pt;border-left:none'>PostCondition</td>
  <td class=xl70>用户成功登录，保持登录状态，直至清楚数据缓存、保持登录时间超时，浏览器关闭</td>
 </tr>
 <tr height=21 style='height:15.4pt'>
  <td rowspan=4 height=65 class=xl77 width=150 style='border-bottom:1.0pt ;
  height:47.7pt;border-top:none;'>Specific Alternative Flow</td>
  <td class=xl68 width=67 style='border-top:none;'>RFS</td>
  <td colspan=2 class=xl86 width=410 style='border-right:1.0pt ;
  border-left:none;'>3</td>
 </tr>
 <tr height=22 style='height:16.15pt'>
  <td height=22 class=xl66 width=67 style='height:16.15pt;'>1</td>
  <td colspan=2 class=xl88 width=410 style='border-right:1.0pt ;
  border-left:none;'>系统提示用户不存在或密码错误</td>
 </tr>
 <tr height=22 style='height:16.15pt'>
  <td height=22 class=xl66 width=67 style='height:16.15pt;'>2</td>
  <td colspan=2 class=xl88 width=410 style='border-right:1.0pt ;
  border-left:none;'>RESUME STEP</td>
 </tr>
 <tr height=22 style='height:16.15pt'>
  <td colspan=2 height=22 class=xl90 width=135 style='border-right:1.0pt ;
  height:16.15pt;border-left:none;'>PostCondition</td>
  <td class=xl67 width=342 style=''>系统回到主界面</td>
 </tr>
</table>




##### 3.1.1.3 用户登出

已登录的用户在系统界面中通过登出按钮从系统中登出。

<center>表3-3 用户登出RUCM</center>

<table border=0 cellpadding=0 cellspacing=0 width=627 style='border-collapse:
 collapse;table-layout:auto;'>
 <col width=150 style='mso-width-source:userset;mso-width-alt:5120;'>
 <col width=67 style='mso-width-source:userset;mso-width-alt:2269;'>
 <col width=68 style=''>
 <col width=342 style='mso-width-source:userset;mso-width-alt:11656;'>
 <tr height=21 style='height:15.75pt'>
  <td colspan=4 height=21 class=xl74 width=627 style='border-right:1.0pt ;
  height:15.75pt;'>Use Case Specification</td>
 </tr>
 <tr height=22 style='height:16.15pt'>
  <td height=22 class=xl65 width=150 style='height:16.15pt;'>Use
  Case Name</td>
  <td colspan=3 class=xl71 style='border-right:1.0pt ;border-left:
  none'>用户登出</td>
 </tr>
 <tr height=96 style='mso-height-source:userset;height:72.0pt'>
  <td height=96 class=xl65 width=150 style='height:72.0pt;'>Brief
  Description</td>
  <td colspan=3 class=xl71 style='border-right:1.0pt ;border-left:
  none'>用户通过登出按钮从系统中登出</td>
 </tr>
 <tr height=96 style='mso-height-source:userset;height:72.0pt'>
  <td height=96 class=xl65 width=150 style='height:72.0pt;'>Precondition</td>
  <td colspan=3 class=xl71 style='border-right:1.0pt ;border-left:
  none'>用户已登录</td>
 </tr>
 <tr height=22 style='height:16.15pt'>
  <td height=22 class=xl65 width=150 style='height:16.15pt;'>Primary
  Actor</td>
  <td colspan=3 class=xl71 style='border-right:1.0pt ;border-left:
  none'>系统管理员，系统用户</td>
 </tr>
 <tr height=22 style='height:16.15pt'>
  <td height=22 class=xl65 width=150 style='height:16.15pt;'>Secondary
  Actors</td>
  <td colspan=3 class=xl71 style='border-right:1.0pt ;border-left:
  none'>无</td>
 </tr>
 <tr height=22 style='height:16.15pt'>
  <td height=22 class=xl65 width=150 style='height:16.15pt;'>Dependency</td>
  <td colspan=3 class=xl71 style='border-right:1.0pt ;border-left:
  none'>无</td>
 </tr>
 <tr height=22 style='height:16.15pt'>
  <td height=22 class=xl65 width=150 style='height:16.15pt;'>Generalization<span
  style='mso-spacerun:yes'> </span></td>
  <td colspan=3 class=xl71 style='border-right:1.0pt ;border-left:
  none'>无</td>
 </tr>
 <tr height=21 style='height:15.4pt'>
  <td rowspan=5 height=469 class=xl77 width=150 style='border-bottom:1.0pt ;
  height:351.05pt;border-top:none;'>Basic Flow</td>
  <td colspan=3 class=xl79 style='border-right:1.0pt ;border-left:
  none'>Steps</td>
 </tr>
 <tr height=96 style='mso-height-source:userset;height:72.0pt'>
  <td height=96 class=xl69 style='height:72.0pt'>1</td>
  <td colspan=2 class=xl71 style='border-right:1.0pt ;border-left:
  none'>用户点击界面中的登出按钮</td>
 </tr>
 <tr height=96 style='mso-height-source:userset;height:72.0pt'>
  <td height=96 class=xl69 style='height:72.0pt'>2</td>
  <td colspan=2 class=xl82 width=410 style='border-right:1.0pt ;
  border-left:none;'>系统提示用户成功登出系统</td>
 </tr>
 <tr height=96 style='mso-height-source:userset;height:72.0pt'>
  <td height=96 class=xl69 style='height:72.0pt'>3</td>
  <td colspan=2 class=xl84 width=410 style='border-right:1.0pt ;
  border-left:none;'>系统跳转至主页面</td>
 </tr>
 <tr height=64 style='height:47.65pt'>
  <td colspan=2 height=64 class=xl79 style='border-right:1.0pt ;
  height:47.65pt;border-left:none'>PostCondition</td>
  <td class=xl70>用户成功登出，失去系统中的各项权限</td>
 </tr>
</table>


##### 3.1.1.4 删除用户

管理员用户可以删除用户。

<center>表3-4 删除用户RUCM</center>

<table border=0 cellpadding=0 cellspacing=0 width=627 style='border-collapse:
 collapse;table-layout:auto;'>
 <col width=150 style='mso-width-source:userset;mso-width-alt:5120;'>
 <col width=67 style='mso-width-source:userset;mso-width-alt:2269;'>
 <col width=68 style=''>
 <col width=342 style='mso-width-source:userset;mso-width-alt:11656;'>
 <tr height=21 style='height:15.75pt'>
  <td colspan=4 height=21 class=xl74 width=627 style='border-right:1.0pt ;
  height:15.75pt;'>Use Case Specification</td>
 </tr>
 <tr height=22 style='height:16.15pt'>
  <td height=22 class=xl65 width=150 style='height:16.15pt;'>Use
  Case Name</td>
  <td colspan=3 class=xl71 style='border-right:1.0pt ;border-left:
  none'>删除用户</td>
 </tr>
 <tr height=96 style='mso-height-source:userset;height:72.0pt'>
  <td height=96 class=xl65 width=150 style='height:72.0pt;'>Brief
  Description</td>
  <td colspan=3 class=xl71 style='border-right:1.0pt ;border-left:
  none'>系统用户在用户列表中删除用户</td>
 </tr>
 <tr height=96 style='mso-height-source:userset;height:72.0pt'>
  <td height=96 class=xl65 width=150 style='height:72.0pt;'>Precondition</td>
  <td colspan=3 class=xl71 style='border-right:1.0pt ;border-left:
  none'>用户已登录</td>
 </tr>
 <tr height=22 style='height:16.15pt'>
  <td height=22 class=xl65 width=150 style='height:16.15pt;'>Primary
  Actor</td>
  <td colspan=3 class=xl71 style='border-right:1.0pt ;border-left:
  none'>系统管理员</td>
 </tr>
 <tr height=22 style='height:16.15pt'>
  <td height=22 class=xl65 width=150 style='height:16.15pt;'>Secondary
  Actors</td>
  <td colspan=3 class=xl71 style='border-right:1.0pt ;border-left:
  none'>无</td>
 </tr>
 <tr height=22 style='height:16.15pt'>
  <td height=22 class=xl65 width=150 style='height:16.15pt;'>Dependency</td>
  <td colspan=3 class=xl71 style='border-right:1.0pt ;border-left:
  none'>无</td>
 </tr>
 <tr height=22 style='height:16.15pt'>
  <td height=22 class=xl65 width=150 style='height:16.15pt;'>Generalization<span
  style='mso-spacerun:yes'> </span></td>
  <td colspan=3 class=xl71 style='border-right:1.0pt ;border-left:
  none'>无</td>
 </tr>
 <tr height=21 style='height:15.4pt'>
  <td rowspan=4 height=469 class=xl77 width=150 style='border-bottom:1.0pt ;
  height:351.05pt;border-top:none;'>Basic Flow</td>
  <td colspan=3 class=xl79 style='border-right:1.0pt ;border-left:
  none'>Steps</td>
 </tr>
 <tr height=96 style='mso-height-source:userset;height:72.0pt'>
  <td height=96 class=xl69 style='height:72.0pt'>1</td>
  <td colspan=2 class=xl71 style='border-right:1.0pt ;border-left:
  none'>系统管理员进入用户列表界面</td>
 </tr>
 <tr height=96 style='mso-height-source:userset;height:72.0pt'>
  <td height=96 class=xl69 style='height:72.0pt'>2</td>
  <td colspan=2 class=xl82 width=410 style='border-right:1.0pt ;
  border-left:none;'>系统管理员删除用户</td>
 </tr>
 <tr height=96 style='mso-height-source:userset;height:72.0pt'>
  <td height=96 class=xl69 style='height:72.0pt'>3</td>
  <td colspan=2 class=xl84 width=410 style='border-right:1.0pt ;
  border-left:none;'>系统提示用户删除成功</td>
 <tr height=21 style='height:15.4pt'>

</table>



##### 3.1.1.5 修改用户密码

所有用户均可以修改自己的用户密码。

<center>表3-5 修改用户密码RUCM</center>

<table border=0 cellpadding=0 cellspacing=0 width=627 style='border-collapse:
 collapse;table-layout:auto;'>
 <col width=150 style='mso-width-source:userset;mso-width-alt:5120;'>
 <col width=67 style='mso-width-source:userset;mso-width-alt:2269;'>
 <col width=68 style=''>
 <col width=342 style='mso-width-source:userset;mso-width-alt:11656;'>
 <tr height=21 style='height:15.75pt'>
  <td colspan=4 height=21 class=xl74 width=627 style='border-right:1.0pt ;
  height:15.75pt;'>Use Case Specification</td>
 </tr>
 <tr height=22 style='height:16.15pt'>
  <td height=22 class=xl65 width=150 style='height:16.15pt;'>Use
  Case Name</td>
  <td colspan=3 class=xl71 style='border-right:1.0pt ;border-left:
  none'>修改用户密码</td>
 </tr>
 <tr height=96 style='mso-height-source:userset;height:72.0pt'>
  <td height=96 class=xl65 width=150 style='height:72.0pt;'>Brief
  Description</td>
  <td colspan=3 class=xl71 style='border-right:1.0pt ;border-left:
  none'>用户在个人信息界面中修改用户密码</td>
 </tr>
 <tr height=96 style='mso-height-source:userset;height:72.0pt'>
  <td height=96 class=xl65 width=150 style='height:72.0pt;'>Precondition</td>
  <td colspan=3 class=xl71 style='border-right:1.0pt ;border-left:
  none'>用户已登录</td>
 </tr>
 <tr height=22 style='height:16.15pt'>
  <td height=22 class=xl65 width=150 style='height:16.15pt;'>Primary
  Actor</td>
  <td colspan=3 class=xl71 style='border-right:1.0pt ;border-left:
  none'>系统管理员，系统用户</td>
 </tr>
 <tr height=22 style='height:16.15pt'>
  <td height=22 class=xl65 width=150 style='height:16.15pt;'>Secondary
  Actors</td>
  <td colspan=3 class=xl71 style='border-right:1.0pt ;border-left:
  none'>无</td>
 </tr>
 <tr height=22 style='height:16.15pt'>
  <td height=22 class=xl65 width=150 style='height:16.15pt;'>Dependency</td>
  <td colspan=3 class=xl71 style='border-right:1.0pt ;border-left:
  none'>无</td>
 </tr>
 <tr height=22 style='height:16.15pt'>
  <td height=22 class=xl65 width=150 style='height:16.15pt;'>Generalization<span
  style='mso-spacerun:yes'> </span></td>
  <td colspan=3 class=xl71 style='border-right:1.0pt ;border-left:
  none'>无</td>
 </tr>
 <tr height=21 style='height:15.4pt'>
  <td rowspan=4 height=469 class=xl77 width=150 style='border-bottom:1.0pt ;
  height:351.05pt;border-top:none;'>Basic Flow</td>
  <td colspan=3 class=xl79 style='border-right:1.0pt ;border-left:
  none'>Steps</td>
 </tr>
 <tr height=96 style='mso-height-source:userset;height:72.0pt'>
  <td height=96 class=xl69 style='height:72.0pt'>1</td>
  <td colspan=2 class=xl71 style='border-right:1.0pt ;border-left:
  none'>用户进入个人信息界面</td>
 </tr>
 <tr height=96 style='mso-height-source:userset;height:72.0pt'>
  <td height=96 class=xl69 style='height:72.0pt'>2</td>
  <td colspan=2 class=xl82 width=410 style='border-right:1.0pt ;
  border-left:none;'>用户更改密码</td>
 </tr>
 <tr height=96 style='mso-height-source:userset;height:72.0pt'>
  <td height=96 class=xl69 style='height:72.0pt'>3</td>
  <td colspan=2 class=xl84 width=410 style='border-right:1.0pt ;
  border-left:none;'>系统提示用户更改成功</td>
 <tr height=21 style='height:15.4pt'>
  <td rowspan=5 height=87 class=xl77 width=150 style='border-bottom:1.0pt ;
  height:63.85pt;border-top:none;'>Specific Alternative Flow</td>
  <td class=xl68 width=67 style='border-top:none;'>RFS</td>
  <td colspan=2 class=xl86 width=410 style='border-right:1.0pt ;
  border-left:none;'>3</td>
 </tr>
 <tr height=22 style='height:16.15pt'>
  <td height=22 class=xl66 width=67 style='height:16.15pt;'>1</td>
  <td colspan=2 class=xl88 width=410 style='border-right:1.0pt ;
  border-left:none;'>系统提示密码不符合要求</td>
 </tr>
 <tr height=22 style='height:16.15pt'>
  <td height=22 class=xl66 width=67 style='height:16.15pt;'>2</td>
  <td colspan=2 class=xl88 width=410 style='border-right:1.0pt ;
  border-left:none;'>系统提示密码具体要求</td>
 </tr>
 <tr height=22 style='height:16.15pt'>
  <td height=22 class=xl66 width=67 style='height:16.15pt;'>3</td>
  <td colspan=2 class=xl88 width=410 style='border-right:1.0pt ;
  border-left:none;'>RESUME STEP</td>
 </tr>
 <tr height=22 style='height:16.15pt'>
  <td colspan=2 height=22 class=xl90 width=135 style='border-right:1.0pt ;
  height:16.15pt;border-left:none;'>PostCondition</td>
  <td class=xl67 width=342 style=''>系统回到注册界面</td>
 </tr>
</table>



##### 3.1.1.6 查看用户列表

系统管理员可以在用户管理界面查看系统用户列表。

<center>表3-6 查看用户列表RUCM</center>

<table border=0 cellpadding=0 cellspacing=0 width=627 style='border-collapse:
 collapse;table-layout:auto;'>
 <col width=150 style='mso-width-source:userset;mso-width-alt:5120;'>
 <col width=67 style='mso-width-source:userset;mso-width-alt:2269;'>
 <col width=68 style=''>
 <col width=342 style='mso-width-source:userset;mso-width-alt:11656;'>
 <tr height=21 style='height:15.75pt'>
  <td colspan=4 height=21 class=xl74 width=627 style='border-right:1.0pt ;
  height:15.75pt;'>Use Case Specification</td>
 </tr>
 <tr height=22 style='height:16.15pt'>
  <td height=22 class=xl65 width=150 style='height:16.15pt;'>Use
  Case Name</td>
  <td colspan=3 class=xl71 style='border-right:1.0pt ;border-left:
  none'>查看用户列表</td>
 </tr>
 <tr height=96 style='mso-height-source:userset;height:72.0pt'>
  <td height=96 class=xl65 width=150 style='height:72.0pt;'>Brief
  Description</td>
  <td colspan=3 class=xl71 style='border-right:1.0pt ;border-left:
  none'>系统管理员在用户管理界面查看系统用户列表</td>
 </tr>
 <tr height=96 style='mso-height-source:userset;height:72.0pt'>
  <td height=96 class=xl65 width=150 style='height:72.0pt;'>Precondition</td>
  <td colspan=3 class=xl71 style='border-right:1.0pt ;border-left:
  none'>用户已登录</td>
 </tr>
 <tr height=22 style='height:16.15pt'>
  <td height=22 class=xl65 width=150 style='height:16.15pt;'>Primary
  Actor</td>
  <td colspan=3 class=xl71 style='border-right:1.0pt ;border-left:
  none'>系统管理员</td>
 </tr>
 <tr height=22 style='height:16.15pt'>
  <td height=22 class=xl65 width=150 style='height:16.15pt;'>Secondary
  Actors</td>
  <td colspan=3 class=xl71 style='border-right:1.0pt ;border-left:
  none'>无</td>
 </tr>
 <tr height=22 style='height:16.15pt'>
  <td height=22 class=xl65 width=150 style='height:16.15pt;'>Dependency</td>
  <td colspan=3 class=xl71 style='border-right:1.0pt ;border-left:
  none'>无</td>
 </tr>
 <tr height=22 style='height:16.15pt'>
  <td height=22 class=xl65 width=150 style='height:16.15pt;'>Generalization<span
  style='mso-spacerun:yes'> </span></td>
  <td colspan=3 class=xl71 style='border-right:1.0pt ;border-left:
  none'>无</td>
 </tr>
 <tr height=21 style='height:15.4pt'>
  <td rowspan=3 height=469 class=xl77 width=150 style='border-bottom:1.0pt ;
  height:351.05pt;border-top:none;'>Basic Flow</td>
  <td colspan=3 class=xl79 style='border-right:1.0pt ;border-left:
  none'>Steps</td>
 </tr>
 <tr height=96 style='mso-height-source:userset;height:72.0pt'>
  <td height=96 class=xl69 style='height:72.0pt'>1</td>
  <td colspan=2 class=xl71 style='border-right:1.0pt ;border-left:
  none'>系统管理员进入用户管理界面</td>
 </tr>
 <tr height=96 style='mso-height-source:userset;height:72.0pt'>
  <td height=96 class=xl69 style='height:72.0pt'>2</td>
  <td colspan=2 class=xl82 width=410 style='border-right:1.0pt ;
  border-left:none;'>系统管理员查看系统用户列表</td>
 </tr>
</table>


##### 3.1.1.7 查看用户个人信息

用户可以在个人信息界面查看用户自身信息。

<center>表3-7 查看用户个人信息RUCM</center>

<table border=0 cellpadding=0 cellspacing=0 width=627 style='border-collapse:
 collapse;table-layout:auto;'>
 <col width=150 style='mso-width-source:userset;mso-width-alt:5120;'>
 <col width=67 style='mso-width-source:userset;mso-width-alt:2269;'>
 <col width=68 style=''>
 <col width=342 style='mso-width-source:userset;mso-width-alt:11656;'>
 <tr height=21 style='height:15.75pt'>
  <td colspan=4 height=21 class=xl74 width=627 style='border-right:1.0pt ;
  height:15.75pt;'>Use Case Specification</td>
 </tr>
 <tr height=22 style='height:16.15pt'>
  <td height=22 class=xl65 width=150 style='height:16.15pt;'>Use
  Case Name</td>
  <td colspan=3 class=xl71 style='border-right:1.0pt ;border-left:
  none'>查看用户个人信息</td>
 </tr>
 <tr height=96 style='mso-height-source:userset;height:72.0pt'>
  <td height=96 class=xl65 width=150 style='height:72.0pt;'>Brief
  Description</td>
  <td colspan=3 class=xl71 style='border-right:1.0pt ;border-left:
  none'>用户可以在个人信息界面查看用户自身信息</td>
 </tr>
 <tr height=96 style='mso-height-source:userset;height:72.0pt'>
  <td height=96 class=xl65 width=150 style='height:72.0pt;'>Precondition</td>
  <td colspan=3 class=xl71 style='border-right:1.0pt ;border-left:
  none'>用户已登录</td>
 </tr>
 <tr height=22 style='height:16.15pt'>
  <td height=22 class=xl65 width=150 style='height:16.15pt;'>Primary
  Actor</td>
  <td colspan=3 class=xl71 style='border-right:1.0pt ;border-left:
  none'>系统管理员，系统用户</td>
 </tr>
 <tr height=22 style='height:16.15pt'>
  <td height=22 class=xl65 width=150 style='height:16.15pt;'>Secondary
  Actors</td>
  <td colspan=3 class=xl71 style='border-right:1.0pt ;border-left:
  none'>无</td>
 </tr>
 <tr height=22 style='height:16.15pt'>
  <td height=22 class=xl65 width=150 style='height:16.15pt;'>Dependency</td>
  <td colspan=3 class=xl71 style='border-right:1.0pt ;border-left:
  none'>无</td>
 </tr>
 <tr height=22 style='height:16.15pt'>
  <td height=22 class=xl65 width=150 style='height:16.15pt;'>Generalization<span
  style='mso-spacerun:yes'> </span></td>
  <td colspan=3 class=xl71 style='border-right:1.0pt ;border-left:
  none'>无</td>
 </tr>
 <tr height=21 style='height:15.4pt'>
  <td rowspan=3 height=469 class=xl77 width=150 style='border-bottom:1.0pt ;
  height:351.05pt;border-top:none;'>Basic Flow</td>
  <td colspan=3 class=xl79 style='border-right:1.0pt ;border-left:
  none'>Steps</td>
 </tr>
 <tr height=96 style='mso-height-source:userset;height:72.0pt'>
  <td height=96 class=xl69 style='height:72.0pt'>1</td>
  <td colspan=2 class=xl71 style='border-right:1.0pt ;border-left:
  none'>用户进入个人信息界面</td>
 </tr>
 <tr height=96 style='mso-height-source:userset;height:72.0pt'>
  <td height=96 class=xl69 style='height:72.0pt'>2</td>
  <td colspan=2 class=xl82 width=410 style='border-right:1.0pt ;
  border-left:none;'>用户可以查看自身个人信息，例如电话，邮箱等</td>
 </tr>
</table>



##### 3.1.1.8 重置用户密码

系统管理员可以在用户管理界面重置列表中任一用户的密码。

<center>表3-8 重置用户密码RUCM</center>

<table border=0 cellpadding=0 cellspacing=0 width=627 style='border-collapse:
 collapse;table-layout:auto;'>
 <col width=150 style='mso-width-source:userset;mso-width-alt:5120;'>
 <col width=67 style='mso-width-source:userset;mso-width-alt:2269;'>
 <col width=68 style=''>
 <col width=342 style='mso-width-source:userset;mso-width-alt:11656;'>
 <tr height=21 style='height:15.75pt'>
  <td colspan=4 height=21 class=xl74 width=627 style='border-right:1.0pt ;
  height:15.75pt;'>Use Case Specification</td>
 </tr>
 <tr height=22 style='height:16.15pt'>
  <td height=22 class=xl65 width=150 style='height:16.15pt;'>Use
  Case Name</td>
  <td colspan=3 class=xl71 style='border-right:1.0pt ;border-left:
  none'>重置用户密码</td>
 </tr>
 <tr height=96 style='mso-height-source:userset;height:72.0pt'>
  <td height=96 class=xl65 width=150 style='height:72.0pt;'>Brief
  Description</td>
  <td colspan=3 class=xl71 style='border-right:1.0pt ;border-left:
  none'>系统管理员可以重置系统用户列表中任一用户的密码</td>
 </tr>
 <tr height=96 style='mso-height-source:userset;height:72.0pt'>
  <td height=96 class=xl65 width=150 style='height:72.0pt;'>Precondition</td>
  <td colspan=3 class=xl71 style='border-right:1.0pt ;border-left:
  none'>用户已登录</td>
 </tr>
 <tr height=22 style='height:16.15pt'>
  <td height=22 class=xl65 width=150 style='height:16.15pt;'>Primary
  Actor</td>
  <td colspan=3 class=xl71 style='border-right:1.0pt ;border-left:
  none'>系统管理员</td>
 </tr>
 <tr height=22 style='height:16.15pt'>
  <td height=22 class=xl65 width=150 style='height:16.15pt;'>Secondary
  Actors</td>
  <td colspan=3 class=xl71 style='border-right:1.0pt ;border-left:
  none'>无</td>
 </tr>
 <tr height=22 style='height:16.15pt'>
  <td height=22 class=xl65 width=150 style='height:16.15pt;'>Dependency</td>
  <td colspan=3 class=xl71 style='border-right:1.0pt ;border-left:
  none'>无</td>
 </tr>
 <tr height=22 style='height:16.15pt'>
  <td height=22 class=xl65 width=150 style='height:16.15pt;'>Generalization<span
  style='mso-spacerun:yes'> </span></td>
  <td colspan=3 class=xl71 style='border-right:1.0pt ;border-left:
  none'>无</td>
 </tr>
 <tr height=21 style='height:15.4pt'>
  <td rowspan=4 height=469 class=xl77 width=150 style='border-bottom:1.0pt ;
  height:351.05pt;border-top:none;'>Basic Flow</td>
  <td colspan=3 class=xl79 style='border-right:1.0pt ;border-left:
  none'>Steps</td>
 </tr>
 <tr height=96 style='mso-height-source:userset;height:72.0pt'>
  <td height=96 class=xl69 style='height:72.0pt'>1</td>
  <td colspan=2 class=xl71 style='border-right:1.0pt ;border-left:
  none'>系统管理员进入用户管理界面</td>
 </tr>
 <tr height=96 style='mso-height-source:userset;height:72.0pt'>
  <td height=96 class=xl69 style='height:72.0pt'>2</td>
  <td colspan=2 class=xl82 width=410 style='border-right:1.0pt ;
  border-left:none;'>系统管理员点击用户管理界面中用户列表的任一项的重置密码</td>
 </tr>
 <tr height=96 style='mso-height-source:userset;height:72.0pt'>
  <td height=96 class=xl69 style='height:72.0pt'>3</td>
  <td colspan=2 class=xl84 width=410 style='border-right:1.0pt ;
  border-left:none;'>系统重置该用户密码为初始默认密码</td>
 </tr>
</table>


##### 3.1.1.9 修改用户角色

系统管理员可以在用户管理界面修改列表中任一用户的系统角色。

<center>表3-9 修改用户角色RUCM</center>

<table border=0 cellpadding=0 cellspacing=0 width=627 style='border-collapse:
 collapse;table-layout:auto;'>
 <col width=150 style='mso-width-source:userset;mso-width-alt:5120;'>
 <col width=67 style='mso-width-source:userset;mso-width-alt:2269;'>
 <col width=68 style=''>
 <col width=342 style='mso-width-source:userset;mso-width-alt:11656;'>
 <tr height=21 style='height:15.75pt'>
  <td colspan=4 height=21 class=xl74 width=627 style='border-right:1.0pt ;
  height:15.75pt;'>Use Case Specification</td>
 </tr>
 <tr height=22 style='height:16.15pt'>
  <td height=22 class=xl65 width=150 style='height:16.15pt;'>Use
  Case Name</td>
  <td colspan=3 class=xl71 style='border-right:1.0pt ;border-left:
  none'>修改用户角色</td>
 </tr>
 <tr height=96 style='mso-height-source:userset;height:72.0pt'>
  <td height=96 class=xl65 width=150 style='height:72.0pt;'>Brief
  Description</td>
  <td colspan=3 class=xl71 style='border-right:1.0pt ;border-left:
  none'>系统管理员可以将系统用户列表中任一用户修改为管理员角色</td>
 </tr>
 <tr height=96 style='mso-height-source:userset;height:72.0pt'>
  <td height=96 class=xl65 width=150 style='height:72.0pt;'>Precondition</td>
  <td colspan=3 class=xl71 style='border-right:1.0pt ;border-left:
  none'>用户已登录</td>
 </tr>
 <tr height=22 style='height:16.15pt'>
  <td height=22 class=xl65 width=150 style='height:16.15pt;'>Primary
  Actor</td>
  <td colspan=3 class=xl71 style='border-right:1.0pt ;border-left:
  none'>系统管理员</td>
 </tr>
 <tr height=22 style='height:16.15pt'>
  <td height=22 class=xl65 width=150 style='height:16.15pt;'>Secondary
  Actors</td>
  <td colspan=3 class=xl71 style='border-right:1.0pt ;border-left:
  none'>无</td>
 </tr>
 <tr height=22 style='height:16.15pt'>
  <td height=22 class=xl65 width=150 style='height:16.15pt;'>Dependency</td>
  <td colspan=3 class=xl71 style='border-right:1.0pt ;border-left:
  none'>无</td>
 </tr>
 <tr height=22 style='height:16.15pt'>
  <td height=22 class=xl65 width=150 style='height:16.15pt;'>Generalization<span
  style='mso-spacerun:yes'> </span></td>
  <td colspan=3 class=xl71 style='border-right:1.0pt ;border-left:
  none'>无</td>
 </tr>
 <tr height=21 style='height:15.4pt'>
  <td rowspan=4 height=469 class=xl77 width=150 style='border-bottom:1.0pt ;
  height:351.05pt;border-top:none;'>Basic Flow</td>
  <td colspan=3 class=xl79 style='border-right:1.0pt ;border-left:
  none'>Steps</td>
 </tr>
 <tr height=96 style='mso-height-source:userset;height:72.0pt'>
  <td height=96 class=xl69 style='height:72.0pt'>1</td>
  <td colspan=2 class=xl71 style='border-right:1.0pt ;border-left:
  none'>系统管理员进入用户管理界面</td>
 </tr>
 <tr height=96 style='mso-height-source:userset;height:72.0pt'>
  <td height=96 class=xl69 style='height:72.0pt'>2</td>
  <td colspan=2 class=xl82 width=410 style='border-right:1.0pt ;
  border-left:none;'>系统管理员点击用户管理界面中用户列表的任一项的修改为管理员</td>
 </tr>
 <tr height=96 style='mso-height-source:userset;height:72.0pt'>
  <td height=96 class=xl69 style='height:72.0pt'>3</td>
  <td colspan=2 class=xl84 width=410 style='border-right:1.0pt ;
  border-left:none;'>系统更改该用户的角色和权限</td>
 </tr>
</table>


##### 3.1.1.10 添加用户

系统管理员可以添加用户。添加时需要指定用户名、系统角色和初始密码。

<center>表3-10 添加用户RUCM</center>

<table border=0 cellpadding=0 cellspacing=0 width=627 style='border-collapse:
 collapse;table-layout:auto;'>
 <col width=150 style='mso-width-source:userset;mso-width-alt:5120;'>
 <col width=67 style='mso-width-source:userset;mso-width-alt:2269;'>
 <col width=68 style=''>
 <col width=342 style='mso-width-source:userset;mso-width-alt:11656;'>
 <tr height=21 style='height:15.75pt'>
  <td colspan=4 height=21 class=xl74 width=627 style='border-right:1.0pt ;
  height:15.75pt;'>Use Case Specification</td>
 </tr>
 <tr height=22 style='height:16.15pt'>
  <td height=22 class=xl65 width=150 style='height:16.15pt;'>Use
  Case Name</td>
  <td colspan=3 class=xl71 style='border-right:1.0pt ;border-left:
  none'>添加用户</td>
 </tr>
 <tr height=96 style='mso-height-source:userset;height:72.0pt'>
  <td height=96 class=xl65 width=150 style='height:72.0pt;'>Brief
  Description</td>
  <td colspan=3 class=xl71 style='border-right:1.0pt ;border-left:
  none'>系统管理员添加新用户</td>
 </tr>
 <tr height=96 style='mso-height-source:userset;height:72.0pt'>
  <td height=96 class=xl65 width=150 style='height:72.0pt;'>Precondition</td>
  <td colspan=3 class=xl71 style='border-right:1.0pt ;border-left:
  none'>用户已登录</td>
 </tr>
 <tr height=22 style='height:16.15pt'>
  <td height=22 class=xl65 width=150 style='height:16.15pt;'>Primary
  Actor</td>
  <td colspan=3 class=xl71 style='border-right:1.0pt ;border-left:
  none'>系统管理员</td>
 </tr>
 <tr height=22 style='height:16.15pt'>
  <td height=22 class=xl65 width=150 style='height:16.15pt;'>Secondary
  Actors</td>
  <td colspan=3 class=xl71 style='border-right:1.0pt ;border-left:
  none'>无</td>
 </tr>
 <tr height=22 style='height:16.15pt'>
  <td height=22 class=xl65 width=150 style='height:16.15pt;'>Dependency</td>
  <td colspan=3 class=xl71 style='border-right:1.0pt ;border-left:
  none'>无</td>
 </tr>
 <tr height=22 style='height:16.15pt'>
  <td height=22 class=xl65 width=150 style='height:16.15pt;'>Generalization<span
  style='mso-spacerun:yes'> </span></td>
  <td colspan=3 class=xl71 style='border-right:1.0pt ;border-left:
  none'>无</td>
 </tr>
 <tr height=21 style='height:15.4pt'>
  <td rowspan=6 height=469 class=xl77 width=150 style='border-bottom:1.0pt ;
  height:351.05pt;border-top:none;'>Basic Flow</td>
  <td colspan=3 class=xl79 style='border-right:1.0pt ;border-left:
  none'>Steps</td>
 </tr>
 <tr height=96 style='mso-height-source:userset;height:72.0pt'>
  <td height=96 class=xl69 style='height:72.0pt'>1</td>
  <td colspan=2 class=xl71 style='border-right:1.0pt ;border-left:
  none'>系统管理员进入用户管理界面</td>
 </tr>
 <tr height=96 style='mso-height-source:userset;height:72.0pt'>
  <td height=96 class=xl69 style='height:72.0pt'>2</td>
  <td colspan=2 class=xl82 width=410 style='border-right:1.0pt ;
  border-left:none;'>系统管理员点击添加用户跳转至用户添加界面</td>
 </tr>
 <tr height=96 style='mso-height-source:userset;height:72.0pt'>
  <td height=96 class=xl69 style='height:72.0pt'>3</td>
  <td colspan=2 class=xl84 width=410 style='border-right:1.0pt ;
  border-left:none;'>系统管理员输入用户名和密码，并选择系统角色类型</td>
 </tr>
 <tr height=96 style='mso-height-source:userset;height:72.0pt'>
  <td height=96 class=xl69 style='height:72.0pt'>4</td>
  <td colspan=2 class=xl71 style='border-right:1.0pt ;border-left:
  none'>系统提示添加成功并返回用户管理界面</td>
 </tr>
 <tr height=64 style='height:47.65pt'>
  <td colspan=2 height=64 class=xl79 style='border-right:1.0pt ;
  height:47.65pt;border-left:none'>PostCondition</td>
  <td class=xl70>成功添加新用户，数据库成功保存用户名和密码</td>
 </tr>
 <tr height=21 style='height:15.4pt'>
  <td rowspan=4 height=65 class=xl77 width=150 style='border-bottom:1.0pt ;
  height:47.7pt;border-top:none;'>Specific Alternative Flow</td>
  <td class=xl68 width=67 style='border-top:none;'>RFS</td>
  <td colspan=2 class=xl86 width=410 style='border-right:1.0pt ;
  border-left:none;'>4</td>
 </tr>
 <tr height=22 style='height:16.15pt'>
  <td height=22 class=xl66 width=67 style='height:16.15pt;'>1</td>
  <td colspan=2 class=xl88 width=410 style='border-right:1.0pt ;
  border-left:none;'>系统提示用户名重复</td>
 </tr>
 <tr height=22 style='height:16.15pt'>
  <td height=22 class=xl66 width=67 style='height:16.15pt;'>2</td>
  <td colspan=2 class=xl88 width=410 style='border-right:1.0pt ;
  border-left:none;'>RESUME STEP</td>
 </tr>
 <tr height=22 style='height:16.15pt'>
  <td colspan=2 height=22 class=xl90 width=135 style='border-right:1.0pt ;
  height:16.15pt;border-left:none;'>PostCondition</td>
  <td class=xl67 width=342 style=''>系统回到用户添加界面</td>
 </tr>
 <tr height=21 style='height:15.4pt'>
  <td rowspan=5 height=87 class=xl77 width=150 style='border-bottom:1.0pt ;
  height:63.85pt;border-top:none;'>Specific Alternative Flow</td>
  <td class=xl68 width=67 style='border-top:none;'>RFS</td>
  <td colspan=2 class=xl86 width=410 style='border-right:1.0pt ;
  border-left:none;'>4</td>
 </tr>
 <tr height=22 style='height:16.15pt'>
  <td height=22 class=xl66 width=67 style='height:16.15pt;'>1</td>
  <td colspan=2 class=xl88 width=410 style='border-right:1.0pt ;
  border-left:none;'>系统提示密码不符合要求</td>
 </tr>
 <tr height=22 style='height:16.15pt'>
  <td height=22 class=xl66 width=67 style='height:16.15pt;'>2</td>
  <td colspan=2 class=xl88 width=410 style='border-right:1.0pt ;
  border-left:none;'>系统提示密码具体要求</td>
 </tr>
 <tr height=22 style='height:16.15pt'>
  <td height=22 class=xl66 width=67 style='height:16.15pt;'>3</td>
  <td colspan=2 class=xl88 width=410 style='border-right:1.0pt ;
  border-left:none;'>RESUME STEP</td>
 </tr>
 <tr height=22 style='height:16.15pt'>
  <td colspan=2 height=22 class=xl90 width=135 style='border-right:1.0pt ;
  height:16.15pt;border-left:none;'>PostCondition</td>
  <td class=xl67 width=342 style=''>系统回到注册界面</td>
 </tr>
</table>


#### 3.1.2 项目管理模块相关需求

项目管理模块面向不同角色的用户提供管理和查看项目的场景。以“创建项目”为例，当因为业务要求需要开展新项目时，项目经理需要创建新项目进行管理。

项目管理模块的用例图如图3-4：

<img src="./images/%E9%A1%B9%E7%9B%AE%E7%AE%A1%E7%90%86%E6%A8%A1%E5%9D%97%E7%94%A8%E4%BE%8B%E5%9B%BE.jpg" style="zoom:67%;" />
<center>图3-4 项目管理模块用例图</center>

其中，“创建项目”和“查看项目列表”两个功能不针对某个特定的项目，故所有用户均有权限操作。其余功能均是针对某个特定项目而言，所以在每个项目中，不同项目角色的用户有着不同的权限， 具体权限如图3-5所示：

<img src="./images/%E9%A1%B9%E7%9B%AE%E8%A7%92%E8%89%B2%E9%92%88%E5%AF%B9%E7%89%B9%E5%AE%9A%E5%AF%B9%E5%BA%94%E7%9A%84%E6%9D%83%E9%99%90.jpg"  />

<center>图3-5 用户针对特定项目权限示意图</center>

##### 3.1.2.1 创建项目

所有用户都可以在项目管理模块创建新的项目。

具体的UML活动图如图3-6：

![](./images/%E5%88%9B%E5%BB%BA%E9%A1%B9%E7%9B%AE%E6%B4%BB%E5%8A%A8%E5%9B%BE.jpg)

<center>图3-6 创建项目活动图</center>

<center>表3-11 创建项目RUCM</center>

<table border="0" cellpadding="0" cellspacing="0"  >
 <colgroup><col  >
 <col  span="2" >
 <col  >
 </colgroup><tbody><tr  >
  <td colspan="4"    >Use
  Case Specification</td>
 </tr>
 <tr  >
  <td    >Use Case Name</td>
  <td colspan="3"   >创建项目</td>
 </tr>
 <tr  >
  <td    >Brief Description</td>
  <td colspan="3"   >用户创建新项目，填写项目信息并添加项目成员，为每个项目成员设置项目角色。</td>
 </tr>
 <tr  >
  <td    >Precondition</td>
  <td colspan="3"   >用户进入到项目列表界面。</td>
 </tr>
 <tr  >
  <td    >Primary Actor</td>
  <td colspan="3"   >所有用户</td>
 </tr>
 <tr  >
  <td    >Secondary Actors</td>
  <td colspan="3"   >无</td>
 </tr>
 <tr  >
  <td    >Dependency</td>
  <td colspan="3"   >无</td>
 </tr>
 <tr  >
  <td    >Generalization</td>
  <td colspan="3"   >无</td>
 </tr>
 <tr  >
  <td rowspan="8"    >Basic Flow</td>
  <td colspan="3"   >steps</td>
 </tr>
 <tr  >
  <td    >1</td>
  <td colspan="2"   >用户进入项目列表界面</td>
 </tr>
 <tr  >
  <td    >2</td>
  <td colspan="2"   >用户按下“创建项目”按钮</td>
 </tr>
 <tr  >
  <td    >3</td>
  <td colspan="2"   >用户填写项目名称、项目描述和项目状态信息，然后按下“下一步”按钮</td>
 </tr>
 <tr  >
  <td    >4</td>
  <td colspan="2"   >用户为该项目添加其他项目成员，并设置相应的项目角色</td>
 </tr>
 <tr  >
  <td    >5</td>
  <td colspan="2"   >用户按下“创建项目”按钮</td>
 </tr>
 <tr  >
  <td    >6</td>
  <td colspan="2"   >提示“创建成功”，自动跳转到项目列表界面</td>
 </tr>
 <tr  >
  <td colspan="2"    >PostCondition</td>
  <td   >用户创建项目成功，在项目列表界面能够看到新创建的项目</td>
 </tr>
 <tr  >
  <td rowspan="5"    >Specific Alternative Flow</td>
  <td   >RFS</td>
  <td colspan="2"   >3</td>
 </tr>
 <tr  >
  <td    >1</td>
  <td colspan="2"   >用户没有填写必填的项目名称信息</td>
 </tr>
 <tr  >
  <td    >2</td>
  <td colspan="2"   >提示“请输入项目名称，完成项目信息”</td>
 </tr>
 <tr  >
  <td    >3</td>
  <td colspan="2"   >RESUME STEP</td>
 </tr>
 <tr  >
  <td colspan="2"    >PostCondition</td>
  <td   >无</td>
 </tr>
</tbody></table>

##### 3.1.2.2 删除项目

项目经理可以在项目管理模块删除项目。

具体的UML活动图如图3-7：

![](./images/%E5%88%A0%E9%99%A4%E9%A1%B9%E7%9B%AE%E6%B4%BB%E5%8A%A8%E5%9B%BE.jpg)

<center>图3-7 删除项目活动图</center>


<center>表3-12 删除项目RUCM</center>

<table border="0" cellpadding="0" cellspacing="0"  >
 <colgroup><col  >
 <col  span="2" >
 <col  >
 </colgroup><tbody><tr  >
  <td colspan="4"    >Use
  Case Specification</td>
 </tr>
 <tr  >
  <td    >Use Case Name</td>
  <td colspan="3"   >删除项目</td>
 </tr>
 <tr  >
  <td    >Brief Description</td>
  <td colspan="3"   >项目经理在项目列表页删除项目。</td>
 </tr>
 <tr  >
  <td    >Precondition</td>
  <td colspan="3"   >用户进入到项目列表界面。</td>
 </tr>
 <tr  >
  <td    >Primary Actor</td>
  <td colspan="3"   >项目经理</td>
 </tr>
 <tr  >
  <td    >Secondary Actors</td>
  <td colspan="3"   >无</td>
 </tr>
 <tr  >
  <td    >Dependency</td>
  <td colspan="3"   >无</td>
 </tr>
 <tr  >
  <td    >Generalization</td>
  <td colspan="3"   >无</td>
 </tr>
 <tr  >
  <td rowspan="7"    >Basic Flow</td>
  <td colspan="3"   >steps</td>
 </tr>
 <tr  >
  <td    >1</td>
  <td colspan="2"   >用户进入项目列表界面</td>
 </tr>
 <tr  >
  <td    >2</td>
  <td colspan="2"   >用户点击对应项目“删除项目”按钮</td>
 </tr>
 <tr  >
  <td    >3</td>
  <td colspan="2"   >跳出弹窗，提示是否删除该项目</td>
 </tr>
 <tr  >
  <td    >4</td>
  <td colspan="2"   >用户点击“确定”按钮删除该项目</td>
 </tr>
 <tr  >
  <td    >5</td>
  <td colspan="2"   >提示“删除成功”，自动刷新项目列表界面</td>
 </tr>
 <tr  >
  <td colspan="2"    >PostCondition</td>
  <td   >用户删除项目成功，在项目列表界面已经看不到刚刚删除的项目</td>
 </tr>
 <tr  >
  <td rowspan="5"    >Specific Alternative Flow</td>
  <td   >RFS</td>
  <td colspan="2"   >3</td>
 </tr>
 <tr  >
  <td    >1</td>
  <td colspan="2"   >用户点击“取消”按钮</td>
 </tr>
 <tr  >
  <td    >2</td>
  <td colspan="2"   >提示“已取消删除”</td>
 </tr>
 <tr  >
  <td    >3</td>
  <td colspan="2"   >RESUME STEP</td>
 </tr>
 <tr  >
  <td colspan="2"    >PostCondition</td>
  <td   >无</td>
 </tr>
</tbody></table>

##### 3.1.2.3 修改项目

项目经理可以在项目管理模块修改项目。修改项目包含两个内容，一是修改项目信息，二是修改项目成员。

具体的UML活动图如图3-8：

![](./images/%E4%BF%AE%E6%94%B9%E9%A1%B9%E7%9B%AE%E6%B4%BB%E5%8A%A8%E5%9B%BE.png)

<center>图3-8 修改项目活动图</center>

<center>表3-13 修改项目RUCM</center>

<table border="0" cellpadding="0" cellspacing="0"  >
 <colgroup><col  >
 <col  span="2" >
 <col  >
 </colgroup><tbody><tr  >
  <td colspan="4"    >Use
  Case Specification</td>
 </tr>
 <tr  >
  <td    >Use Case Name</td>
  <td colspan="3"   >修改项目</td>
 </tr>
 <tr  >
  <td    >Brief Description</td>
  <td colspan="3"   >项目经理在项目列表界面修改已有项目信息或项目成员。</td>
 </tr>
 <tr  >
  <td    >Precondition</td>
  <td colspan="3"   >用户进入到项目列表界面。</td>
 </tr>
 <tr  >
  <td    >Primary Actor</td>
  <td colspan="3"   >项目经理</td>
 </tr>
 <tr  >
  <td    >Secondary Actors</td>
  <td colspan="3"   >无</td>
 </tr>
 <tr  >
  <td    >Dependency</td>
  <td colspan="3"   >include-修改项目信息、include-修改项目成员</td>
 </tr>
 <tr  >
  <td    >Generalization</td>
  <td colspan="3"   >无</td>
 </tr>
 <tr  >
  <td rowspan="8"    >Basic Flow</td>
  <td colspan="3"   >steps</td>
 </tr>
 <tr  >
  <td    >1</td>
  <td colspan="2"   >用户进入项目列表界面</td>
 </tr>
 <tr  >
  <td    >2</td>
  <td colspan="2"   >用户点击对应项目的“项目信息”按钮</td>
 </tr>
 <tr  >
  <td    >3</td>
  <td colspan="2"   >跳转到项目信息界面，默认展示该项目的当前信息</td>
 </tr>
 <tr  >
  <td    >4</td>
  <td colspan="2"   >用户可以在左侧选择“项目信息”（即当前界面）或“成员管理”，修改相应的信息</td>
 </tr>
 <tr  >
  <td    >5</td>
  <td colspan="2"   >用户点击“保存”按钮</td>
 </tr>
 <tr  >
  <td    >6</td>
  <td colspan="2"   >提示“修改成功”</td>
 </tr>
 <tr  >
  <td colspan="2"    >PostCondition</td>
  <td   >无</td>
 </tr>
 <tr  >
  <td rowspan="5"    >Specific Alternative Flow</td>
  <td   >RFS</td>
  <td colspan="2"   >5</td>
 </tr>
 <tr  >
  <td    >1</td>
  <td colspan="2"   >用户不是该项目的项目经理，没有修改权限</td>
 </tr>
 <tr  >
  <td    >2</td>
  <td colspan="2"   >提示“失败！没有权限操作！”</td>
 </tr>
 <tr  >
  <td    >3</td>
  <td colspan="2"   >RESUME STEP</td>
 </tr>
 <tr  >
  <td colspan="2"    >PostCondition</td>
  <td   >无</td>
 </tr>
</tbody></table>

##### 3.1.2.4 查看项目

所有用户均可以查看参与的项目 （“参与的项目”指用户在该项目的成员之中）的内容，包括项目信息和项目成员。

<center>表3-14 查看项目RUCM</center>

<table border="0" cellpadding="0" cellspacing="0"  >
 <colgroup><col  >
 <col  span="2" >
 <col  >
 </colgroup><tbody><tr  >
  <td colspan="4"    >Use
  Case Specification</td>
 </tr>
 <tr  >
  <td    >Use Case Name</td>
  <td colspan="3"   >查看项目</td>
 </tr>
 <tr  >
  <td    >Brief Description</td>
  <td colspan="3"   >用户在项目列表界面查看某个项目的具体信息和项目成员。</td>
 </tr>
 <tr  >
  <td    >Precondition</td>
  <td colspan="3"   >用户进入到项目列表界面。</td>
 </tr>
 <tr  >
  <td    >Primary Actor</td>
  <td colspan="3"   >所有用户</td>
 </tr>
 <tr  >
  <td    >Secondary Actors</td>
  <td colspan="3"   >无</td>
 </tr>
 <tr  >
  <td    >Dependency</td>
  <td colspan="3"   >include-查看项目信息、include-查看项目成员</td>
 </tr>
 <tr  >
  <td    >Generalization</td>
  <td colspan="3"   >无</td>
 </tr>
 <tr  >
  <td rowspan="5"    >Basic Flow</td>
  <td colspan="3"   >steps</td>
 </tr>
 <tr  >
  <td    >1</td>
  <td colspan="2"   >用户进入项目列表界面</td>
 </tr>
 <tr  >
  <td    >2</td>
  <td colspan="2"   >用户点击对应项目的“项目信息”按钮</td>
 </tr>
 <tr  >
  <td    >3</td>
  <td colspan="2"   >用户可以在左侧选择“项目信息”（即当前界面）或“成员管理”，查看相应的信息</td>
 </tr>
 <tr  >
  <td colspan="2"    >PostCondition</td>
  <td   >无</td>
 </tr>
</tbody></table>

##### 3.1.2.5 查看项目列表

所有用户均可以查看项目列表。项目列表中包含该用户所参与的所有项目。

<center>表3-15 查看项目列表RUCM</center>

<table border="0" cellpadding="0" cellspacing="0"  >
 <colgroup><col  >
 <col  span="2" >
 <col  >
 </colgroup><tbody><tr  >
  <td colspan="4"    >Use
  Case Specification</td>
 </tr>
 <tr  >
  <td    >Use Case Name</td>
  <td colspan="3"   >查看项目列表</td>
 </tr>
 <tr  >
  <td    >Brief Description</td>
  <td colspan="3"   >用户在项目列表界面内可以查看到自己所参与的所有项目。</td>
 </tr>
 <tr  >
  <td    >Precondition</td>
  <td colspan="3"   >用户登录成功。</td>
 </tr>
 <tr  >
  <td    >Primary Actor</td>
  <td colspan="3"   >所有用户</td>
 </tr>
 <tr  >
  <td    >Secondary Actors</td>
  <td colspan="3"   >无</td>
 </tr>
 <tr  >
  <td    >Dependency</td>
  <td colspan="3"   >无</td>
 </tr>
 <tr  >
  <td    >Generalization</td>
  <td colspan="3"   >无</td>
 </tr>
 <tr  >
  <td rowspan="5"    >Basic Flow</td>
  <td colspan="3"   >steps</td>
 </tr>
 <tr  >
  <td    >1</td>
  <td colspan="2"   >用户登录成功</td>
 </tr>
 <tr  >
  <td    >2</td>
  <td colspan="2"   >用户点击左侧项目管理的“项目列表”按钮</td>
 </tr>
 <tr  >
  <td    >3</td>
  <td colspan="2"   >系统展示当前用户所参与的所有项目</td>
 </tr>
 <tr  >
  <td colspan="2"    >PostCondition</td>
  <td   >无</td>
 </tr>
</tbody></table>

##### 3.1.2.6 创建项目基线节点

项目经理可以创建项目基线节点。

项目基线是项目内需求条目的归档。基线中的每一个节点都代表一个归档节点的描述信息包含了节点名称和节点描述。整体工作流程如下图3-9所示：

<img src="images/%E5%88%9B%E5%BB%BA%E9%A1%B9%E7%9B%AE%E5%9F%BA%E7%BA%BF%E8%8A%82%E7%82%B9%E7%A4%BA%E6%84%8F.jpg" style="zoom:67%;" />

<center>图3-9 创建项目基线节点状态图</center>

<center>表3-16 创建项目基线节点RUCM</center>

<table border="0" cellpadding="0" cellspacing="0"  >
 <colgroup><col  >
 <col  span="2" >
 <col  >
 </colgroup><tbody><tr  >
  <td colspan="4"    >Use
  Case Specification</td>
 </tr>
 <tr  >
  <td    >Use Case Name</td>
  <td colspan="3"   >创建项目基线节点</td>
 </tr>
 <tr  >
  <td    >Brief Description</td>
  <td colspan="3"   >用户先在当前项目内进行需求变更，当需求变更进行到一定程度，需求已经处于稳定的状态时，可以通过创建项目基线节点将当前项目内的需求条目进行归档，并添加节点名称和描述（例如版本号和对应修改的描述 。 基线是项目的里程碑，基线节点一旦创建，节点内的需求条目就无法继续改动。</td>
 </tr>
 <tr  >
  <td    >Precondition</td>
  <td colspan="3"   >用户进入到具体的项目信息界面。</td>
 </tr>
 <tr  >
  <td    >Primary Actor</td>
  <td colspan="3"   >项目经理</td>
 </tr>
 <tr  >
  <td    >Secondary Actors</td>
  <td colspan="3"   >无</td>
 </tr>
 <tr  >
  <td    >Dependency</td>
  <td colspan="3"   >无</td>
 </tr>
 <tr  >
  <td    >Generalization</td>
  <td colspan="3"   >无</td>
 </tr>
 <tr  >
  <td rowspan="6"    >Basic Flow</td>
  <td colspan="3"   >steps</td>
 </tr>
 <tr  >
  <td    >1</td>
  <td colspan="2"   >用户查看项目</td>
 </tr>
 <tr  >
  <td    >2</td>
  <td colspan="2"   >用户切换到左侧基线管理，点击“创建基线节点”按钮</td>
 </tr>
 <tr  >
  <td    >3</td>
  <td colspan="2"   >用户填写版本名称和版本描述信息，然后点击“确定”按钮</td>
 </tr>
 <tr  >
  <td    >4</td>
  <td colspan="2"   >提示“创建成功”，跳转到当前项目的基线列表</td>
 </tr>
 <tr  >
  <td colspan="2"    >PostCondition</td>
  <td   >无</td>
 </tr>
 <tr  >
  <td rowspan="5"    >Specific Alternative Flow</td>
  <td   >RFS</td>
  <td colspan="2"   >3</td>
 </tr>
 <tr  >
  <td    >1</td>
  <td colspan="2"   >用户没有填写必填的版本名称信息</td>
 </tr>
 <tr  >
  <td    >2</td>
  <td colspan="2"   >提示“请输入归档版本名称”</td>
 </tr>
 <tr  >
  <td    >3</td>
  <td colspan="2"   >RESUME STEP</td>
 </tr>
 <tr  >
  <td colspan="2"    >PostCondition</td>
  <td   >无</td>
 </tr>
</tbody></table>


##### 3.1.2.7 查看项目基线节点

所有用户均可以查看自己参与项目的基线节点 ，包括查看节点名称、描述以及对应节点中归档的需求条目内容。

<center>表3-17 查看项目基线节点RUCM</center>

<table border="0" cellpadding="0" cellspacing="0"  >
 <colgroup><col  >
 <col  span="2" >
 <col  >
 </colgroup><tbody><tr  >
  <td colspan="4"    >Use
  Case Specification</td>
 </tr>
 <tr  >
  <td    >Use Case Name</td>
  <td colspan="3"   >查看项目基线节点</td>
 </tr>
 <tr  >
  <td    >Brief Description</td>
  <td colspan="3"   >用户查看当前项目的所有基线节点，也可以查看某个节点的具体信息。</td>
 </tr>
 <tr  >
  <td    >Precondition</td>
  <td colspan="3"   >用户进入到具体的项目信息界面。</td>
 </tr>
 <tr  >
  <td    >Primary Actor</td>
  <td colspan="3"   >所有用户</td>
 </tr>
 <tr  >
  <td    >Secondary Actors</td>
  <td colspan="3"   >无</td>
 </tr>
 <tr  >
  <td    >Dependency</td>
  <td colspan="3"   >无</td>
 </tr>
 <tr  >
  <td    >Generalization</td>
  <td colspan="3"   >无</td>
 </tr>
 <tr  >
  <td rowspan="5"    >Basic Flow</td>
  <td colspan="3"   >steps</td>
 </tr>
 <tr  >
  <td    >1</td>
  <td colspan="2"   >用户查看项目</td>
 </tr>
 <tr  >
  <td    >2</td>
  <td colspan="2"   >用户切换到左侧基线管理，可以看到当前项目下的所有基线节点</td>
 </tr>
 <tr  >
  <td    >3</td>
  <td colspan="2"   >用户点击某个基线版本查看具体信息</td>
 </tr>
 <tr  >
  <td colspan="2"    >PostCondition</td>
  <td   >无</td>
 </tr>
</tbody></table>

##### 3.1.2.8 修改项目信息

项目经理可以在项目管理模块修改项目信息。

具体UML活动图可见 `3.1.2.3 修改项目`。

<center>表3-18 修改项目信息RUCM</center>

<table border="0" cellpadding="0" cellspacing="0"  >
 <colgroup><col  >
 <col  span="2" >
 <col  >
 </colgroup><tbody><tr  >
  <td colspan="4"    >Use
  Case Specification</td>
 </tr>
 <tr  >
  <td    >Use Case Name</td>
  <td colspan="3"   >修改项目</td>
 </tr>
 <tr  >
  <td    >Brief Description</td>
  <td colspan="3"   >项目经理在项目列表界面修改已有项目信息。</td>
 </tr>
 <tr  >
  <td    >Precondition</td>
  <td colspan="3"   >用户进入到项目列表界面。</td>
 </tr>
 <tr  >
  <td    >Primary Actor</td>
  <td colspan="3"   >项目经理</td>
 </tr>
 <tr  >
  <td    >Secondary Actors</td>
  <td colspan="3"   >无</td>
 </tr>
 <tr  >
  <td    >Dependency</td>
  <td colspan="3"   >修改项目-include</td>
 </tr>
 <tr  >
  <td    >Generalization</td>
  <td colspan="3"   >无</td>
 </tr>
 <tr  >
  <td rowspan="8"    >Basic Flow</td>
  <td colspan="3"   >steps</td>
 </tr>
 <tr  >
  <td    >1</td>
  <td colspan="2"   >用户进入项目列表界面</td>
 </tr>
 <tr  >
  <td    >2</td>
  <td colspan="2"   >用户点击对应项目的“项目信息”按钮</td>
 </tr>
 <tr  >
  <td    >3</td>
  <td colspan="2"   >跳转到项目信息界面，默认展示该项目的当前信息</td>
 </tr>
 <tr  >
  <td    >4</td>
  <td colspan="2"   >用户在对应位置的文本框输入要修改的相应信息</td>
 </tr>
 <tr  >
  <td    >5</td>
  <td colspan="2"   >用户点击“保存”按钮</td>
 </tr>
 <tr  >
  <td    >6</td>
  <td colspan="2"   >提示“修改成功”</td>
 </tr>
 <tr  >
  <td colspan="2"    >PostCondition</td>
  <td   >无</td>
 </tr>
 <tr  >
  <td rowspan="5"    >Specific Alternative Flow</td>
  <td   >RFS</td>
  <td colspan="2"   >5</td>
 </tr>
 <tr  >
  <td    >1</td>
  <td colspan="2"   >用户不是该项目的项目经理，没有修改权限</td>
 </tr>
 <tr  >
  <td    >2</td>
  <td colspan="2"   >提示“失败！没有权限操作！”</td>
 </tr>
 <tr  >
  <td    >3</td>
  <td colspan="2"   >ABORT</td>
 </tr>
 <tr  >
  <td colspan="2"    >PostCondition</td>
  <td   >无</td>
 </tr>
</tbody></table>


##### 3.1.2.9 修改项目成员

项目经理可以在项目管理模块修改项目成员。修改项目成员可以添加新成员或删除已有成员（新成员只能是系统内已有的用户）， 也可以修改已有成员的项目角色。

具体UML活动图可见 `3.1.2.3 修改项目`。

<center>表3-19 修改项目成员RUCM</center>

<table border="0" cellpadding="0" cellspacing="0"  >
 <colgroup><col  >
 <col  span="2" >
 <col  >
 </colgroup><tbody><tr  >
  <td colspan="4"    >Use
  Case Specification</td>
 </tr>
 <tr  >
  <td    >Use Case Name</td>
  <td colspan="3"   >修改项目成员</td>
 </tr>
 <tr  >
  <td    >Brief Description</td>
  <td colspan="3"   >项目经理在项目列表界面修改已有项目成员。</td>
 </tr>
 <tr  >
  <td    >Precondition</td>
  <td colspan="3"   >用户进入到项目列表界面。</td>
 </tr>
 <tr  >
  <td    >Primary Actor</td>
  <td colspan="3"   >项目经理</td>
 </tr>
 <tr  >
  <td    >Secondary Actors</td>
  <td colspan="3"   >无</td>
 </tr>
 <tr  >
  <td    >Dependency</td>
  <td colspan="3"   >修改项目-include、include-添加用户、include-修改项目角色、include-删除用户</td>
 </tr>
 <tr  >
  <td    >Generalization</td>
  <td colspan="3"   >无</td>
 </tr>
 <tr  >
  <td rowspan="11"    >Basic Flow</td>
  <td colspan="3"   >steps</td>
 </tr>
 <tr  >
  <td    >1</td>
  <td colspan="2"   >用户进入项目列表界面</td>
 </tr>
 <tr  >
  <td    >2</td>
  <td colspan="2"   >用户点击对应项目的“项目信息”按钮</td>
 </tr>
 <tr  >
  <td    >3</td>
  <td colspan="2"   >跳转到项目信息界面，默认展示该项目的当前信息</td>
 </tr>
 <tr  >
  <td    >4</td>
  <td colspan="2"   >点击当前界面左侧菜单栏的“成员管理”切换界面</td>
 </tr>
 <tr  >
  <td    >5</td>
  <td colspan="2"   >INCLUDE CASE 添加项目成员</td>
 </tr>
  <tr  >
  <td    >6</td>
  <td colspan="2"   >INCLUDE CASE 删除项目成员</td>
 </tr>
  <tr  >
  <td    >7</td>
  <td colspan="2"   >INCLUDE CASE 修改项目角色</td>
 </tr>
 <tr  >
  <td    >8</td>
  <td colspan="2"   >用户点击“保存”按钮</td>
 </tr>
 <tr  >
  <td    >9</td>
  <td colspan="2"   >提示“修改成功”</td>
 </tr>
 <tr  >
  <td colspan="2"    >PostCondition</td>
  <td   >无</td>
 </tr>
 <tr  >
  <td rowspan="5"    >Specific Alternative Flow</td>
  <td   >RFS</td>
  <td colspan="2"   >6</td>
 </tr>
 <tr  >
  <td    >1</td>
  <td colspan="2"   >用户不是该项目的项目经理，没有修改权限</td>
 </tr>
 <tr  >
  <td    >2</td>
  <td colspan="2"   >提示“失败！没有权限操作！”</td>
 </tr>
 <tr  >
  <td    >3</td>
  <td colspan="2"   >ABORT</td>
 </tr>
 <tr  >
  <td colspan="2"    >PostCondition</td>
  <td   >无</td>
 </tr>
</tbody></table>

##### 3.1.2.10 查看项目信息

所有用户均可以查看参与的项目 （“参与的项目”指用户在该项目的成员之中）的项目信息。

<center>表3-20 查看项目信息RUCM</center>

<table border="0" cellpadding="0" cellspacing="0"  >
 <colgroup><col  >
 <col  span="2" >
 <col  >
 </colgroup><tbody><tr  >
  <td colspan="4"    >Use
  Case Specification</td>
 </tr>
 <tr  >
  <td    >Use Case Name</td>
  <td colspan="3"   >查看项目信息</td>
 </tr>
 <tr  >
  <td    >Brief Description</td>
  <td colspan="3"   >用户在项目列表界面查看某个项目的具体信息。</td>
 </tr>
 <tr  >
  <td    >Precondition</td>
  <td colspan="3"   >用户进入到项目列表界面。</td>
 </tr>
 <tr  >
  <td    >Primary Actor</td>
  <td colspan="3"   >所有用户</td>
 </tr>
 <tr  >
  <td    >Secondary Actors</td>
  <td colspan="3"   >无</td>
 </tr>
 <tr  >
  <td    >Dependency</td>
  <td colspan="3"   >查看项目-include</td>
 </tr>
 <tr  >
  <td    >Generalization</td>
  <td colspan="3"   >无</td>
 </tr>
 <tr  >
  <td rowspan="5"    >Basic Flow</td>
  <td colspan="3"   >steps</td>
 </tr>
 <tr  >
  <td    >1</td>
  <td colspan="2"   >用户进入项目列表界面</td>
 </tr>
 <tr  >
  <td    >2</td>
  <td colspan="2"   >用户点击对应项目的“项目信息”按钮</td>
 </tr>
 <tr  >
  <td    >3</td>
  <td colspan="2"   >系统默认展示当前项目的具体信息</td>
 </tr>
 <tr  >
  <td colspan="2"    >PostCondition</td>
  <td   >无</td>
 </tr>
</tbody></table>

##### 3.1.2.11 查看项目成员

所有用户均可以查看参与的项目 （“参与的项目”指用户在该项目的成员之中）的项目成员。

<center>表3-21 查看项目成员RUCM</center>

<table border="0" cellpadding="0" cellspacing="0"  >
 <colgroup><col  >
 <col  span="2" >
 <col  >
 </colgroup><tbody><tr  >
  <td colspan="4"    >Use
  Case Specification</td>
 </tr>
 <tr  >
  <td    >Use Case Name</td>
  <td colspan="3"   >查看项目成员</td>
 </tr>
 <tr  >
  <td    >Brief Description</td>
  <td colspan="3"   >用户在项目列表界面查看某个项目的项目成员。</td>
 </tr>
 <tr  >
  <td    >Precondition</td>
  <td colspan="3"   >用户进入到项目列表界面。</td>
 </tr>
 <tr  >
  <td    >Primary Actor</td>
  <td colspan="3"   >所有用户</td>
 </tr>
 <tr  >
  <td    >Secondary Actors</td>
  <td colspan="3"   >无</td>
 </tr>
 <tr  >
  <td    >Dependency</td>
  <td colspan="3"   >查看项目-include</td>
 </tr>
 <tr  >
  <td    >Generalization</td>
  <td colspan="3"   >无</td>
 </tr>
 <tr  >
  <td rowspan="6"    >Basic Flow</td>
  <td colspan="3"   >steps</td>
 </tr>
 <tr  >
  <td    >1</td>
  <td colspan="2"   >用户进入项目列表界面</td>
 </tr>
 <tr  >
  <td    >2</td>
  <td colspan="2"   >用户点击对应项目的“项目信息”按钮</td>
 </tr>
 <tr  >
  <td    >3</td>
  <td colspan="2"   >用户点击左侧菜单栏的“成员管理”按钮</td>
 </tr>
 <tr  >
  <td    >4</td>
  <td colspan="2"   >系统切换到该项目的项目成员界面</td>
 </tr>   
 <tr  >
  <td colspan="2"    >PostCondition</td>
  <td   >无</td>
 </tr>
</tbody></table>

##### 3.1.2.12 添加项目成员

项目经理可以在项目管理模块为已有项目添加新成员。

具体UML活动图可见 `3.1.2.3 修改项目`。

<center>表3-22 添加项目成员RUCM</center>

<table border="0" cellpadding="0" cellspacing="0"  >
 <colgroup><col  >
 <col  span="2" >
 <col  >
 </colgroup><tbody><tr  >
  <td colspan="4"    >Use
  Case Specification</td>
 </tr>
 <tr  >
  <td    >Use Case Name</td>
  <td colspan="3"   >添加项目成员</td>
 </tr>
 <tr  >
  <td    >Brief Description</td>
  <td colspan="3"   >项目经理在项目列表的成员管理界面为该项目添加新成员。</td>
 </tr>
 <tr  >
  <td    >Precondition</td>
  <td colspan="3"   >用户进入到项目列表界面。</td>
 </tr>
 <tr  >
  <td    >Primary Actor</td>
  <td colspan="3"   >项目经理</td>
 </tr>
 <tr  >
  <td    >Secondary Actors</td>
  <td colspan="3"   >无</td>
 </tr>
 <tr  >
  <td    >Dependency</td>
  <td colspan="3"   >修改项目成员-include</td>
 </tr>
 <tr  >
  <td    >Generalization</td>
  <td colspan="3"   >无</td>
 </tr>
 <tr  >
  <td rowspan="9"    >Basic Flow</td>
  <td colspan="3"   >steps</td>
 </tr>
 <tr  >
  <td    >1</td>
  <td colspan="2"   >用户进入项目列表界面</td>
 </tr>
 <tr  >
  <td    >2</td>
  <td colspan="2"   >用户点击对应项目的“项目信息”按钮</td>
 </tr>
 <tr  >
  <td    >3</td>
  <td colspan="2"   >跳转到项目信息界面，默认展示该项目的当前信息</td>
 </tr>
 <tr  >
  <td    >4</td>
  <td colspan="2"   >点击当前界面左侧菜单栏的“成员管理”切换界面</td>
 </tr>
 <tr  >
  <td    >5</td>
  <td colspan="2"   >用户在“添加用户”旁边的搜索框中选择新用户，然后点击“添加用户”按钮</td>
 </tr>
 <tr  >
  <td    >6</td>
  <td colspan="2"   >用户点击“保存”按钮</td>
 </tr>
 <tr  >
  <td    >7</td>
  <td colspan="2"   >提示“修改成功”</td>
 </tr>
 <tr  >
  <td colspan="2"    >PostCondition</td>
  <td   >无</td>
 </tr>
 <tr  >
  <td rowspan="5"    >Specific Alternative Flow</td>
  <td   >RFS</td>
  <td colspan="2"   >6</td>
 </tr>
 <tr  >
  <td    >1</td>
  <td colspan="2"   >用户不是该项目的项目经理，没有修改权限</td>
 </tr>
 <tr  >
  <td    >2</td>
  <td colspan="2"   >提示“失败！没有权限操作！”</td>
 </tr>
 <tr  >
  <td    >3</td>
  <td colspan="2"   >ABORT</td>
 </tr>
 <tr  >
  <td colspan="2"    >PostCondition</td>
  <td   >无</td>
 </tr>
</tbody></table>


##### 3.1.2.13 删除项目成员

项目经理可以在项目管理模块为已有项目删除已有成员。

具体UML活动图可见 `3.1.2.3 修改项目`。

<center>表3-23 删除项目成员RUCM</center>

<table border="0" cellpadding="0" cellspacing="0"  >
 <colgroup><col  >
 <col  span="2" >
 <col  >
 </colgroup><tbody><tr  >
  <td colspan="4"    >Use
  Case Specification</td>
 </tr>
 <tr  >
  <td    >Use Case Name</td>
  <td colspan="3"   >删除项目成员</td>
 </tr>
 <tr  >
  <td    >Brief Description</td>
  <td colspan="3"   >项目经理在项目列表的成员管理界面为该项目删除已有成员。</td>
 </tr>
 <tr  >
  <td    >Precondition</td>
  <td colspan="3"   >用户进入到项目列表界面。</td>
 </tr>
 <tr  >
  <td    >Primary Actor</td>
  <td colspan="3"   >项目经理</td>
 </tr>
 <tr  >
  <td    >Secondary Actors</td>
  <td colspan="3"   >无</td>
 </tr>
 <tr  >
  <td    >Dependency</td>
  <td colspan="3"   >修改项目成员-include</td>
 </tr>
 <tr  >
  <td    >Generalization</td>
  <td colspan="3"   >无</td>
 </tr>
 <tr  >
  <td rowspan="9"    >Basic Flow</td>
  <td colspan="3"   >steps</td>
 </tr>
 <tr  >
  <td    >1</td>
  <td colspan="2"   >用户进入项目列表界面</td>
 </tr>
 <tr  >
  <td    >2</td>
  <td colspan="2"   >用户点击对应项目的“项目信息”按钮</td>
 </tr>
 <tr  >
  <td    >3</td>
  <td colspan="2"   >跳转到项目信息界面，默认展示该项目的当前信息</td>
 </tr>
 <tr  >
  <td    >4</td>
  <td colspan="2"   >点击当前界面左侧菜单栏的“成员管理”切换界面</td>
 </tr>
 <tr  >
  <td    >5</td>
  <td colspan="2"   >用户选择对应的用户点击“删除用户”按钮</td>
 </tr>
 <tr  >
  <td    >6</td>
  <td colspan="2"   >用户点击“保存”按钮</td>
 </tr>
 <tr  >
  <td    >7</td>
  <td colspan="2"   >提示“修改成功”</td>
 </tr>
 <tr  >
  <td colspan="2"    >PostCondition</td>
  <td   >无</td>
 </tr>
 <tr  >
  <td rowspan="5"    >Specific Alternative Flow</td>
  <td   >RFS</td>
  <td colspan="2"   >6</td>
 </tr>
 <tr  >
  <td    >1</td>
  <td colspan="2"   >用户不是该项目的项目经理，没有修改权限</td>
 </tr>
 <tr  >
  <td    >2</td>
  <td colspan="2"   >提示“失败！没有权限操作！”</td>
 </tr>
 <tr  >
  <td    >3</td>
  <td colspan="2"   >ABORT</td>
 </tr>
 <tr  >
  <td colspan="2"    >PostCondition</td>
  <td   >无</td>
 </tr>
</tbody></table>


##### 3.1.2.14 修改项目角色

项目经理可以在项目管理模块为已有项目的成员修改项目角色。

具体UML活动图可见 `3.1.2.3 修改项目`。

<center>表3-24 修改项目角色RUCM</center>

<table border="0" cellpadding="0" cellspacing="0"  >
 <colgroup><col  >
 <col  span="2" >
 <col  >
 </colgroup><tbody><tr  >
  <td colspan="4"    >Use
  Case Specification</td>
 </tr>
 <tr  >
  <td    >Use Case Name</td>
  <td colspan="3"   >修改项目角色</td>
 </tr>
 <tr  >
  <td    >Brief Description</td>
  <td colspan="3"   >项目经理在项目列表的成员管理界面修改该项目成员的角色。</td>
 </tr>
 <tr  >
  <td    >Precondition</td>
  <td colspan="3"   >用户进入到项目列表界面。</td>
 </tr>
 <tr  >
  <td    >Primary Actor</td>
  <td colspan="3"   >项目经理</td>
 </tr>
 <tr  >
  <td    >Secondary Actors</td>
  <td colspan="3"   >无</td>
 </tr>
 <tr  >
  <td    >Dependency</td>
  <td colspan="3"   >修改项目成员-include</td>
 </tr>
 <tr  >
  <td    >Generalization</td>
  <td colspan="3"   >无</td>
 </tr>
 <tr  >
  <td rowspan="9"    >Basic Flow</td>
  <td colspan="3"   >steps</td>
 </tr>
 <tr  >
  <td    >1</td>
  <td colspan="2"   >用户进入项目列表界面</td>
 </tr>
 <tr  >
  <td    >2</td>
  <td colspan="2"   >用户点击对应项目的“项目信息”按钮</td>
 </tr>
 <tr  >
  <td    >3</td>
  <td colspan="2"   >跳转到项目信息界面，默认展示该项目的当前信息</td>
 </tr>
 <tr  >
  <td    >4</td>
  <td colspan="2"   >点击当前界面左侧菜单栏的“成员管理”切换界面</td>
 </tr>
 <tr  >
  <td    >5</td>
  <td colspan="2"   >用户选择对应的用户点击“修改项目角色”按钮</td>
 </tr>
 <tr  >
  <td    >6</td>
  <td colspan="2"   >用户点击“保存”按钮</td>
 </tr>
 <tr  >
  <td    >7</td>
  <td colspan="2"   >提示“修改成功”</td>
 </tr>
 <tr  >
  <td colspan="2"    >PostCondition</td>
  <td   >无</td>
 </tr>
 <tr  >
  <td rowspan="5"    >Specific Alternative Flow</td>
  <td   >RFS</td>
  <td colspan="2"   >6</td>
 </tr>
 <tr  >
  <td    >1</td>
  <td colspan="2"   >用户不是该项目的项目经理，没有修改权限</td>
 </tr>
 <tr  >
  <td    >2</td>
  <td colspan="2"   >提示“失败！没有权限操作！”</td>
 </tr>
 <tr  >
  <td    >3</td>
  <td colspan="2"   >ABORT</td>
 </tr>
 <tr  >
  <td colspan="2"    >PostCondition</td>
  <td   >无</td>
 </tr>
</tbody></table>


#### 3.1.3 “需求管理”模块相关需求

需求模块面向不同角色的用户提供管理、查看和分析需求的场景。以“需求分析”为例，项目经理或项目组长为更好地把握需求要求，需要借助需求冲突检测等需求分析技术进行辅助。

需求管理模块的用例图如图3-10：

![需求管理功能用例图.jpg](./images/需求管理功能用例图.jpg)

<center>图3-10 需求管理模块用例图</center>



##### 3.1.3.1 创建需求条目

用户在项目管理界面点击相应的项目，进入需求管理页面，点击添加按钮，填写相关信息即可完成需求条目的创建。

具体的UML活动图如图3-11：

![需求管理功能用例图.jpg](./images/创建需求条目活动图.jpg)

<center>图3-11 创建需求条目活动图</center>

<center>表3-25 创建需求条目RUCM</center>

<table border=0 cellpadding=0 cellspacing=0 width=627 style='border-collapse:
 collapse;table-layout:auto;'>
 <col width=150 style='mso-width-source:userset;mso-width-alt:5120;'>
 <col width=67 style='mso-width-source:userset;mso-width-alt:2269;'>
 <col width=68 style=''>
 <col width=342 style='mso-width-source:userset;mso-width-alt:11656;'>
 <tr height=21 style='height:15.75pt'>
  <td colspan=4 height=21 class=xl74 width=627 style='border-right:1.0pt ;
  height:15.75pt;'>Use Case Specification</td>
 </tr>
 <tr height=22 style='height:16.15pt'>
  <td height=22 class=xl65 width=150 style='height:16.15pt;'>Use
  Case Name</td>
  <td colspan=3 class=xl71 style='border-right:1.0pt ;border-left:
  none'>创建需求条目</td>
 </tr>
 <tr height=96 style='mso-height-source:userset;height:72.0pt'>
  <td height=96 class=xl65 width=150 style='height:72.0pt;'>Brief
  Description</td>
  <td colspan=3 class=xl71 style='border-right:1.0pt ;border-left:
  none'>用户使用需求管理功能在对应项目里添加新的需求</td>
 </tr>
 <tr height=96 style='mso-height-source:userset;height:72.0pt'>
  <td height=96 class=xl65 width=150 style='height:72.0pt;'>Precondition</td>
  <td colspan=3 class=xl71 style='border-right:1.0pt ;border-left:
  none'>用户创建项目并点击相应的项目进入需求管理界面</td>
 </tr>
 <tr height=22 style='height:16.15pt'>
  <td height=22 class=xl65 width=150 style='height:16.15pt;'>Primary
  Actor</td>
  <td colspan=3 class=xl71 style='border-right:1.0pt ;border-left:
  none'>项目经理、项目组长</td>
 </tr>
 <tr height=22 style='height:16.15pt'>
  <td height=22 class=xl65 width=150 style='height:16.15pt;'>Secondary
  Actors</td>
  <td colspan=3 class=xl71 style='border-right:1.0pt ;border-left:
  none'>无</td>
 </tr>
 <tr height=22 style='height:16.15pt'>
  <td height=22 class=xl65 width=150 style='height:16.15pt;'>Dependency</td>
  <td colspan=3 class=xl71 style='border-right:1.0pt ;border-left:
  none'>include-创建单条需求条目、include-从word导入需求条目</td>
 </tr>
 <tr height=22 style='height:16.15pt'>
  <td height=22 class=xl65 width=150 style='height:16.15pt;'>Generalization<span
  style='mso-spacerun:yes'> </span></td>
  <td colspan=3 class=xl71 style='border-right:1.0pt ;border-left:
  none'>无</td>
 </tr>
 <tr height=21 style='height:15.4pt'>
  <td rowspan=7 height=469 class=xl77 width=150 style='border-bottom:1.0pt ;
  height:351.05pt;border-top:none;'>Basic Flow</td>
  <td colspan=3 class=xl79 style='border-right:1.0pt ;border-left:
  none'>Steps</td>
 </tr>
 <tr height=96 style='mso-height-source:userset;height:72.0pt'>
  <td height=96 class=xl69 style='height:72.0pt'>1</td>
  <td colspan=2 class=xl71 style='border-right:1.0pt ;border-left:
  none'>系统展示当前已有的需求条目</td>
 </tr>
 <tr height=96 style='mso-height-source:userset;height:72.0pt'>
  <td height=96 class=xl69 style='height:72.0pt'>2</td>
  <td colspan=2 class=xl82 width=410 style='border-right:1.0pt ;
  border-left:none;'>用户在左侧选择要操作的需求条目</td>
 </tr>
 <tr height=96 style='mso-height-source:userset;height:72.0pt'>
  <td height=96 class=xl69 style='height:72.0pt'>3</td>
  <td colspan=2 class=xl84 width=410 style='border-right:1.0pt ;
  border-left:none;'>用户点击添加按钮，并在下拉列表中选择添加需求条目的位置</td>
 </tr>
 <tr height=96 style='mso-height-source:userset;height:72.0pt'>
  <td height=96 class=xl69 style='height:72.0pt'>4</td>
  <td colspan=2 class=xl71 style='border-right:1.0pt ;border-left:
  none'>用户选择创建需求的方式，并完成相关信息填写或导入文件操作</td>
 </tr>
  <tr height=96 style='mso-height-source:userset;height:72.0pt'>
  <td height=96 class=xl69 style='height:72.0pt'>5</td>
  <td colspan=2 class=xl71 style='border-right:1.0pt ;border-left:
  none'>用户点击创建按钮，确认创建需求条目</td>
 </tr>
 <tr height=64 style='height:47.65pt'>
  <td colspan=2 height=64 class=xl79 style='border-right:1.0pt ;
  height:47.65pt;border-left:none'>PostCondition</td>
  <td class=xl70>用户创建需求条目成功，在相应项目的需求管理界面能够看到正确的需求条目并完成相应信息的查看或其他操作</td>
 </tr>
 <tr  >
  <td rowspan="5"    >Specific Alternative Flow</td>
  <td   >RFS</td>
  <td colspan="2"   >3</td>
 </tr>
 <tr  >
  <td    >1</td>
  <td colspan="2"   >用户在根需求条目上添加同层次的需求条目</td>
 </tr>
 <tr  >
  <td    >2</td>
  <td colspan="2"   >系统提示位置选择错误</td>
 </tr>
  <tr  >
  <td    >3</td>
  <td colspan="2"   >RESUME STEP</td>
 </tr>
 <tr  >
  <td colspan="2"    >PostCondition</td>
  <td   >无</td>
 </tr>
</table>


##### 3.1.3.2 创建单条需求条目

用户在添加按钮的下拉列表中选择除了“从文本导入”的其他选项，填写系统设定好的需求条目信息，填写完相关信息后点击创建即可完成单条需求条目的创建。

<center>表3-26 创建单条需求条目RUCM</center>

<table border=0 cellpadding=0 cellspacing=0 width=628 style='border-collapse:
 collapse;table-layout:auto;'>
 <col width=150 style='mso-width-source:userset;mso-width-alt:5120;'>
 <col width=68 span=2 style=''>
 <col width=342 style='mso-width-source:userset;mso-width-alt:11656;'>
 <tr height=21 style='height:15.75pt'>
  <td colspan=4 height=21 class=xl74 width=628 style='border-right:1.0pt ;
  height:15.75pt;'>Use Case Specification</td>
 </tr>
 <tr height=22 style='height:16.15pt'>
  <td height=22 class=xl65 width=150 style='height:16.15pt;'>Use
  Case Name</td>
  <td colspan=3 class=xl71 style='border-right:1.0pt ;border-left:
  none'>创建单条需求条目</td>
 </tr>
 <tr height=96 style='mso-height-source:userset;height:72.0pt'>
  <td height=96 class=xl65 width=150 style='height:72.0pt;'>Brief
  Description</td>
  <td colspan=3 class=xl71 style='border-right:1.0pt ;border-left:
  none'>选择合适的位置，填写系统预先设定的需求条目信息，完成单条需求条目的创建</td>
 </tr>
 <tr height=96 style='mso-height-source:userset;height:72.0pt'>
  <td height=96 class=xl65 width=150 style='height:72.0pt;'>Precondition</td>
  <td colspan=3 class=xl71 style='border-right:1.0pt ;border-left:
  none'>用户创建项目并点击相应的项目进入需求管理界面</td>
 </tr>
 <tr height=22 style='height:16.15pt'>
  <td height=22 class=xl65 width=150 style='height:16.15pt;'>Primary
  Actor</td>
  <td colspan=3 class=xl71 style='border-right:1.0pt ;border-left:
  none'>项目经理、项目组长</td>
 </tr>
 <tr height=22 style='height:16.15pt'>
  <td height=22 class=xl65 width=150 style='height:16.15pt;'>Secondary
  Actors</td>
  <td colspan=3 class=xl71 style='border-right:1.0pt ;border-left:
  none'>无</td>
 </tr>
 <tr height=22 style='height:16.15pt'>
  <td height=22 class=xl65 width=150 style='height:16.15pt;'>Dependency</td>
  <td colspan=3 class=xl71 style='border-right:1.0pt ;border-left:
  none'>创建需求条目-include</td>
 </tr>
 <tr height=22 style='height:16.15pt'>
  <td height=22 class=xl65 width=150 style='height:16.15pt;'>Generalization<span
  style='mso-spacerun:yes'> </span></td>
  <td colspan=3 class=xl71 style='border-right:1.0pt ;border-left:
  none'>无</td>
 </tr>
 <tr height=21 style='height:15.4pt'>
  <td rowspan=7 height=256 class=xl77 width=150 style='border-bottom:1.0pt ;
  height:191.3pt;border-top:none;'>Basic Flow</td>
  <td colspan=3 class=xl79 style='border-right:1.0pt ;border-left:
  none'>Steps</td>
 </tr>
 <tr height=96 style='mso-height-source:userset;height:72.0pt'>
  <td height=96 class=xl69 style='height:72.0pt'>1</td>
  <td colspan=2 class=xl71 style='border-right:1.0pt ;border-left:
  none'>用户选择合适的添加位置，点击添加按钮下拉列表中除了“从文本导入”的其他选项</td>
 </tr>
 <tr height=96 style='mso-height-source:userset;height:72.0pt'>
  <td height=96 class=xl69 style='height:72.0pt'>2</td>
  <td colspan=2 class=xl82 width=410 style='border-right:1.0pt ;
  border-left:none;'>用户填写需求条目的主要信息，包括名称和描述</td>
 </tr>
 <tr height=96 style='mso-height-source:userset;height:72.0pt'>
  <td height=96 class=xl69 style='height:72.0pt'>3</td>
  <td colspan=2 class=xl82 width=410 style='border-right:1.0pt ;
  border-left:none;'>用户填写需求条目的基本信息，包括状态、优先级和预计的开始结束时间</td>
 </tr>
 <tr height=96 style='mso-height-source:userset;height:72.0pt'>
  <td height=96 class=xl69 style='height:72.0pt'>4</td>
  <td colspan=2 class=xl82 width=410 style='border-right:1.0pt ;
  border-left:none;'>用户进行需求分析</td>
 </tr>
 <tr height=96 style='mso-height-source:userset;height:72.0pt'>
  <td height=96 class=xl69 style='height:72.0pt'>5</td>
  <td colspan=2 class=xl82 width=410 style='border-right:1.0pt ;
  border-left:none;'>用户点击创建按钮，完成单调需求条目的创建</td>
 </tr>
 <tr height=43 style='height:31.9pt'>
  <td colspan=2 height=43 class=xl79 style='border-right:1.0pt ;
  height:31.9pt;border-left:none'>PostCondition</td>
  <td class=xl70>用户创建单条需求条目成功，在相应项目的需求管理界面能够看到正确的需求条目并完成相应信息的查看或其他操作</td>
 </tr>
</table>

##### 3.1.3.3 从word导入需求条目

用户在添加按钮的下拉列表中选择“从文本导入”选项，从word文件中导入需求条目。

<center>表3-27 从word导入需求条目RUCM</center>

<table border=0 cellpadding=0 cellspacing=0 width=628 style='border-collapse:
 collapse;table-layout:auto;'>
 <col width=150 style='mso-width-source:userset;mso-width-alt:5120;'>
 <col width=68 span=2 style=''>
 <col width=342 style='mso-width-source:userset;mso-width-alt:11656;'>
 <tr height=21 style='height:15.75pt'>
  <td colspan=4 height=21 class=xl74 width=628 style='border-right:1.0pt ;
  height:15.75pt;'>Use Case Specification</td>
 </tr>
 <tr height=22 style='height:16.15pt'>
  <td height=22 class=xl65 width=150 style='height:16.15pt;'>Use
  Case Name</td>
  <td colspan=3 class=xl71 style='border-right:1.0pt ;border-left:
  none'>从word导入需求条目</td>
 </tr>
 <tr height=96 style='mso-height-source:userset;height:72.0pt'>
  <td height=96 class=xl65 width=150 style='height:72.0pt;'>Brief
  Description</td>
  <td colspan=3 class=xl71 style='border-right:1.0pt ;border-left:
  none'>用户在添加按钮的下拉列表中选择“从文本导入”选项，从word文件中导入需求条目</td>
 </tr>
 <tr height=96 style='mso-height-source:userset;height:72.0pt'>
  <td height=96 class=xl65 width=150 style='height:72.0pt;'>Precondition</td>
  <td colspan=3 class=xl71 style='border-right:1.0pt ;border-left:
  none'>用户创建项目并点击相应的项目进入需求管理界面</td>
 </tr>
 <tr height=22 style='height:16.15pt'>
  <td height=22 class=xl65 width=150 style='height:16.15pt;'>Primary
  Actor</td>
  <td colspan=3 class=xl71 style='border-right:1.0pt ;border-left:
  none'>项目经理、项目组长</td>
 </tr>
 <tr height=22 style='height:16.15pt'>
  <td height=22 class=xl65 width=150 style='height:16.15pt;'>Secondary
  Actors</td>
  <td colspan=3 class=xl71 style='border-right:1.0pt ;border-left:
  none'>无</td>
 </tr>
 <tr height=22 style='height:16.15pt'>
  <td height=22 class=xl65 width=150 style='height:16.15pt;'>Dependency</td>
  <td colspan=3 class=xl71 style='border-right:1.0pt ;border-left:
  none'>创建需求条目-include、include-需求条目化算法</td>
 </tr>
 <tr height=22 style='height:16.15pt'>
  <td height=22 class=xl65 width=150 style='height:16.15pt;'>Generalization<span
  style='mso-spacerun:yes'> </span></td>
  <td colspan=3 class=xl71 style='border-right:1.0pt ;border-left:
  none'>无</td>
 </tr>
 <tr height=21 style='height:15.4pt'>
  <td rowspan=7 height=331 class=xl77 width=150 style='border-bottom:1.0pt ;
  height:247.55pt;border-top:none;'>Basic Flow</td>
  <td colspan=3 class=xl79 style='border-right:1.0pt ;border-left:
  none'>Steps</td>
 </tr>
 <tr height=96 style='mso-height-source:userset;height:72.0pt'>
  <td height=96 class=xl69 style='height:72.0pt'>1</td>
  <td colspan=2 class=xl71 style='border-right:1.0pt ;border-left:
  none'>用户点击添加按钮下拉列表中的“从文本导入”选项</td>
 </tr>
 <tr height=96 style='mso-height-source:userset;height:72.0pt'>
  <td height=96 class=xl69 style='height:72.0pt'>2</td>
  <td colspan=2 class=xl82 width=410 style='border-right:1.0pt ;
  border-left:none;'>用户选择要上传的word文档，上传至服务器进行分析，点击下一步</td>
 </tr>
 <tr height=96 style='mso-height-source:userset;height:72.0pt'>
  <td height=96 class=xl69 style='height:72.0pt'>3</td>
  <td colspan=2 class=xl82 width=410 style='border-right:1.0pt ;
  border-left:none;'>用户点击开始条目化按钮，将word文档条目化</td>
 </tr>
 <tr height=96 style='mso-height-source:userset;height:72.0pt'>
  <td height=96 class=xl69 style='height:72.0pt'>4</td>
  <td colspan=2 class=xl82 width=410 style='border-right:1.0pt ;
  border-left:none;'>用户进行需求分析</td>
 </tr>
 <tr height=96 style='mso-height-source:userset;height:72.0pt'>
  <td height=96 class=xl69 style='height:72.0pt'>5</td>
  <td colspan=2 class=xl82 width=410 style='border-right:1.0pt ;
  border-left:none;'>用户点击创建按钮，完成需求条目的创建</td>
 </tr>
 <tr height=22 style='height:16.15pt'>
  <td colspan=2 height=22 class=xl79 style='border-right:1.0pt;
  height:16.15pt;border-left:none'>PostCondition</td>
  <td class=xl70>用户从word导入需求条目成功，在相应项目的需求管理界面能够看到正确的需求条目并完成相应信息的查看或其他操作</td>
 </tr>
 <tr  >
  <td rowspan="5"    >Specific Alternative Flow</td>
  <td   >RFS</td>
  <td colspan="2"   >3</td>
 </tr>
 <tr  >
  <td    >1</td>
  <td colspan="2"   >用户未上传word文档或需求条目化失败</td>
 </tr>
 <tr  >
  <td    >2</td>
  <td colspan="2"   >系统提示操作错误，无法进行下一步</td>
 </tr>
 <tr  >
  <td    >3</td>
  <td colspan="2"   >RESUME STEP</td>
 </tr>
 <tr  >
  <td colspan="2"    >PostCondition</td>
  <td   >无</td>
 </tr>
</table>



##### 3.1.3.4 需求条目化

用户在导入word文档后，系统需要将文档中的内容条目化为相应的需求。

<center>表3-28 需求条目化算法RUCM</center>

<table border=0 cellpadding=0 cellspacing=0 width=628 style='border-collapse:
 collapse;table-layout:auto;'>
 <col width=150 style='mso-width-source:userset;mso-width-alt:5120;'>
 <col width=68 span=2 style=''>
 <col width=342 style='mso-width-source:userset;mso-width-alt:11656;'>
 <tr height=21 style='height:15.75pt'>
  <td colspan=4 height=21 class=xl74 width=628 style='border-right:1.0pt ;
  height:15.75pt;'>Use Case Specification</td>
 </tr>
 <tr height=22 style='height:16.15pt'>
  <td height=22 class=xl65 width=150 style='height:16.15pt;'>Use
  Case Name</td>
  <td colspan=3 class=xl71 style='border-right:1.0pt ;border-left:
  none'>需求条目化</td>
 </tr>
 <tr height=96 style='mso-height-source:userset;height:72.0pt'>
  <td height=96 class=xl65 width=150 style='height:72.0pt;'>Brief
  Description</td>
  <td colspan=3 class=xl71 style='border-right:1.0pt ;border-left:
  none'>用户在导入word文档后，系统需要将文档中的内容条目化为对应的需求<span style='mso-spacerun:yes'> </span></td>
 </tr>
 <tr height=96 style='mso-height-source:userset;height:72.0pt'>
  <td height=96 class=xl65 width=150 style='height:72.0pt;'>Precondition</td>
  <td colspan=3 class=xl71 style='border-right:1.0pt ;border-left:
  none'>用户通过导入word文档增加需求，并将文件上传到服务器</td>
 </tr>
 <tr height=22 style='height:16.15pt'>
  <td height=22 class=xl65 width=150 style='height:16.15pt;'>Primary
  Actor</td>
  <td colspan=3 class=xl71 style='border-right:1.0pt ;border-left:
  none'>项目经理、项目组长</td>
 </tr>
 <tr height=22 style='height:16.15pt'>
  <td height=22 class=xl65 width=150 style='height:16.15pt;'>Secondary
  Actors</td>
  <td colspan=3 class=xl71 style='border-right:1.0pt ;border-left:
  none'>无</td>
 </tr>
 <tr height=22 style='height:16.15pt'>
  <td height=22 class=xl65 width=150 style='height:16.15pt;'>Dependency</td>
  <td colspan=3 class=xl71 style='border-right:1.0pt ;border-left:
  none'>从word导入需求条目-include</td>
 </tr>
 <tr height=22 style='height:16.15pt'>
  <td height=22 class=xl65 width=150 style='height:16.15pt;'>Generalization<span
  style='mso-spacerun:yes'> </span></td>
  <td colspan=3 class=xl71 style='border-right:1.0pt ;border-left:
  none'>无</td>
 </tr>
 <tr height=21 style='height:15.4pt'>
  <td rowspan=4 height=235 class=xl77 width=150 style='border-bottom:1.0pt ;
  height:175.55pt;border-top:none;'>Basic Flow</td>
  <td colspan=3 class=xl79 style='border-right:1.0pt ;border-left:
  none'>Steps</td>
 </tr>
 <tr height=96 style='mso-height-source:userset;height:72.0pt'>
  <td height=96 class=xl69 style='height:72.0pt'>1</td>
  <td colspan=2 class=xl71 style='border-right:1.0pt ;border-left:
  none'>用户点击“开始条目化”按钮</td>
 </tr>
 <tr height=96 style='mso-height-source:userset;height:72.0pt'>
  <td height=96 class=xl69 style='height:72.0pt'>2</td>
  <td colspan=2 class=xl82 width=410 style='border-right:1.0pt ;
  border-left:none;'>服务器对文档进行条目化分析并返回结果</td>
 </tr>
 <tr height=22 style='height:16.15pt'>
  <td colspan=2 height=22 class=xl79 style='border-right:1.0pt ;
  height:16.15pt;border-left:none'>PostCondition</td>
  <td class=xl70>无</td>
 </tr>
 <tr  >
  <td rowspan="5"    >Specific Alternative Flow</td>
  <td   >RFS</td>
  <td colspan="2"   >2</td>
 </tr>
 <tr  >
  <td    >1</td>
  <td colspan="2"   >服务器对上传的文档条目化操作失败</td>
 </tr>
 <tr  >
  <td    >2</td>
  <td colspan="2"   >系统反馈条目化失败的信息</td>
 </tr>
 <tr  >
  <td    >3</td>
  <td colspan="2"   >RESUME STEP</td>
 </tr>
 <tr  >
  <td colspan="2"    >PostCondition</td>
  <td   >无</td>
 </tr>
</table>


##### 3.1.3.5 删除需求条目

用户根据项目进度安排，选择需要删除的需求条目完成删除操作。

具体的UML活动图如图3-12：

![需求管理功能用例图.jpg](./images/删除需求条目活动图.jpg)

<center>图3-12 删除需求条目活动图</center>

<center>表3-29 删除需求条目RUCM</center>

<table border=0 cellpadding=0 cellspacing=0 width=628 style='border-collapse:
 collapse;table-layout:auto;'>
 <col width=150 style='mso-width-source:userset;mso-width-alt:5120;'>
 <col width=68 span=2 style=''>
 <col width=342 style='mso-width-source:userset;mso-width-alt:11656;'>
 <tr height=21 style='height:15.75pt'>
  <td colspan=4 height=21 class=xl74 width=628 style='border-right:1.0pt ;
  height:15.75pt;'>Use Case Specification</td>
 </tr>
 <tr height=22 style='height:16.15pt'>
  <td height=22 class=xl65 width=150 style='height:16.15pt;'>Use
  Case Name</td>
  <td colspan=3 class=xl71 style='border-right:1.0pt ;border-left:
  none'>删除需求条目</td>
 </tr>
 <tr height=96 style='mso-height-source:userset;height:72.0pt'>
  <td height=96 class=xl65 width=150 style='height:72.0pt;'>Brief
  Description</td>
  <td colspan=3 class=xl71 style='border-right:1.0pt ;border-left:
  none'>用户根据项目进度安排，选择需要删除的需求条目完成删除操作</td>
 </tr>
 <tr height=96 style='mso-height-source:userset;height:72.0pt'>
  <td height=96 class=xl65 width=150 style='height:72.0pt;'>Precondition</td>
  <td colspan=3 class=xl71 style='border-right:1.0pt ;border-left:
  none'>用户已创建了要删除的需求条目</td>
 </tr>
 <tr height=22 style='height:16.15pt'>
  <td height=22 class=xl65 width=150 style='height:16.15pt;'>Primary
  Actor</td>
  <td colspan=3 class=xl71 style='border-right:1.0pt ;border-left:
  none'>项目经理、项目组长</td>
 </tr>
 <tr height=22 style='height:16.15pt'>
  <td height=22 class=xl65 width=150 style='height:16.15pt;'>Secondary
  Actors</td>
  <td colspan=3 class=xl71 style='border-right:1.0pt ;border-left:
  none'>无</td>
 </tr>
 <tr height=22 style='height:16.15pt'>
  <td height=22 class=xl65 width=150 style='height:16.15pt;'>Dependency</td>
  <td colspan=3 class=xl71 style='border-right:1.0pt ;border-left:
  none'>无</td>
 </tr>
 <tr height=22 style='height:16.15pt'>
  <td height=22 class=xl65 width=150 style='height:16.15pt;'>Generalization<span
  style='mso-spacerun:yes'> </span></td>
  <td colspan=3 class=xl71 style='border-right:1.0pt ;border-left:
  none'>无</td>
 </tr>
 <tr height=21 style='height:15.4pt'>
  <td rowspan=6 height=235 class=xl77 width=150 style='border-bottom:1.0pt ;
  height:175.55pt;border-top:none;'>Basic Flow</td>
  <td colspan=3 class=xl79 style='border-right:1.0pt ;border-left:
  none'>Steps</td>
 </tr>
 <tr height=96 style='mso-height-source:userset;height:72.0pt'>
  <td height=96 class=xl69 style='height:72.0pt'>1</td>
  <td colspan=2 class=xl71 style='border-right:1.0pt ;border-left:
  none'>用户选中要删除的需求条目</td>
 </tr>
 <tr height=96 style='mso-height-source:userset;height:72.0pt'>
  <td height=96 class=xl69 style='height:72.0pt'>2</td>
  <td colspan=2 class=xl82 width=410 style='border-right:1.0pt ;
  border-left:none;'>用户点击删除按钮</td>
 </tr>
 <tr height=96 style='mso-height-source:userset;height:72.0pt'>
  <td height=96 class=xl69 style='height:72.0pt'>3</td>
  <td colspan=2 class=xl82 width=410 style='border-right:1.0pt ;
  border-left:none;'>系统提示是否确认删除</td>
 </tr>
 <tr height=96 style='mso-height-source:userset;height:72.0pt'>
  <td height=96 class=xl69 style='height:72.0pt'>4</td>
  <td colspan=2 class=xl82 width=410 style='border-right:1.0pt ;
  border-left:none;'>用户点击确认按钮，完成删除操作</td>
 </tr>
 <tr height=22 style='height:16.15pt'>
  <td colspan=2 height=22 class=xl79 style='border-right:1.0pt ;
  height:16.15pt;border-left:none'>PostCondition</td>
  <td class=xl70>被删除的需求条目在条目树中消失</td>
 </tr>
 <tr  >
  <td rowspan="5"    >Specific Alternative Flow</td>
  <td   >RFS</td>
  <td colspan="2"   >1</td>
 </tr>
 <tr  >
  <td    >1</td>
  <td colspan="2"   >用户选择了根需求条目</td>
 </tr>
 <tr  >
  <td    >2</td>
  <td colspan="2"   >系统提示无法删除此类型的需求条目</td>
 </tr>
 <tr  >
  <td    >3</td>
  <td colspan="2"   >RESUME STEP</td>
 </tr>
 <tr  >
  <td colspan="2"    >PostCondition</td>
  <td   >无</td>
 </tr>
 <tr  >
  <td rowspan="5"    >Specific Alternative Flow</td>
  <td   >RFS</td>
  <td colspan="2"   >4</td>
 </tr>
 <tr  >
  <td    >1</td>
  <td colspan="2"   >用户点击取消删除按钮</td>
 </tr>
 <tr  >
  <td    >2</td>
  <td colspan="2"   >系统反馈取消删除的信息，并取消删除操作</td>
 </tr>
 <tr  >
  <td    >3</td>
  <td colspan="2"   >ABORT</td>
 </tr>
 <tr  >
  <td colspan="2"    >PostCondition</td>
  <td   >无</td>
 </tr>
</table>


##### 3.1.3.6 修改需求条目

用户根据实际工作需要对需求条目进行修改，包括修改需求条目内容以及移动需求条目位置。

具体的UML活动图如图3-13：

![需求管理功能用例图.jpg](./images/修改需求条目活动图.jpg)

<center>图3-13 修改需求条目活动图</center>

<center>表3-30 修改需求条目RUCM</center>

<table border=0 cellpadding=0 cellspacing=0 width=628 style='border-collapse:
 collapse;table-layout:auto;'>
 <col width=150 style='mso-width-source:userset;mso-width-alt:5120;'>
 <col width=68 span=2 style=''>
 <col width=342 style='mso-width-source:userset;mso-width-alt:11656;'>
 <tr height=21 style='height:15.75pt'>
  <td colspan=4 height=21 class=xl74 width=628 style='border-right:1.0pt ;
  height:15.75pt;'>Use Case Specification</td>
 </tr>
 <tr height=22 style='height:16.15pt'>
  <td height=22 class=xl65 width=150 style='height:16.15pt;'>Use
  Case Name</td>
  <td colspan=3 class=xl71 style='border-right:1.0pt ;border-left:
  none'>修改需求条目</td>
 </tr>
 <tr height=96 style='mso-height-source:userset;height:72.0pt'>
  <td height=96 class=xl65 width=150 style='height:72.0pt;'>Brief
  Description</td>
  <td colspan=3 class=xl71 style='border-right:1.0pt ;border-left:
  none'>用户根据实际工作需要对需求条目进行修改，包括修改需求条目内容以及移动需求条目位置</td>
 </tr>
 <tr height=96 style='mso-height-source:userset;height:72.0pt'>
  <td height=96 class=xl65 width=150 style='height:72.0pt;'>Precondition</td>
  <td colspan=3 class=xl71 style='border-right:1.0pt ;border-left:
  none'>用户已创建需要修改的需求条目</td>
 </tr>
 <tr height=22 style='height:16.15pt'>
  <td height=22 class=xl65 width=150 style='height:16.15pt;'>Primary
  Actor</td>
  <td colspan=3 class=xl71 style='border-right:1.0pt ;border-left:
  none'>项目经理、项目组长</td>
 </tr>
 <tr height=22 style='height:16.15pt'>
  <td height=22 class=xl65 width=150 style='height:16.15pt;'>Secondary
  Actors</td>
  <td colspan=3 class=xl71 style='border-right:1.0pt ;border-left:
  none'>无</td>
 </tr>
 <tr height=22 style='height:16.15pt'>
  <td height=22 class=xl65 width=150 style='height:16.15pt;'>Dependency</td>
  <td colspan=3 class=xl71 style='border-right:1.0pt ;border-left:
  none'>include-修改需求条目内容、include-移动需求条目位置</td>
 </tr>
 <tr height=22 style='height:16.15pt'>
  <td height=22 class=xl65 width=150 style='height:16.15pt;'>Generalization<span
  style='mso-spacerun:yes'> </span></td>
  <td colspan=3 class=xl71 style='border-right:1.0pt ;border-left:
  none'>无</td>
 </tr>
 <tr height=21 style='height:15.4pt'>
  <td rowspan=5 height=235 class=xl77 width=150 style='border-bottom:1.0pt ;
  height:175.55pt;border-top:none;'>Basic Flow</td>
  <td colspan=3 class=xl79 style='border-right:1.0pt ;border-left:
  none'>Steps</td>
 </tr>
 <tr height=96 style='mso-height-source:userset;height:72.0pt'>
  <td height=96 class=xl69 style='height:72.0pt'>1</td>
  <td colspan=2 class=xl71 style='border-right:1.0pt ;border-left:
  none'>用户选择要修改的需求条目</td>
 </tr>
 <tr height=96 style='mso-height-source:userset;height:72.0pt'>
  <td height=96 class=xl69 style='height:72.0pt'>2</td>
  <td colspan=2 class=xl82 width=410 style='border-right:1.0pt ;
  border-left:none;'>用户点击修改按钮，进入修改界面，完成相关修改操作</td>
 </tr>
 <tr height=96 style='mso-height-source:userset;height:72.0pt'>
  <td height=96 class=xl69 style='height:72.0pt'>3</td>
  <td colspan=2 class=xl82 width=410 style='border-right:1.0pt ;
  border-left:none;'>用户点击保存按钮，完成修改操作</td>
 </tr>
 <tr height=22 style='height:16.15pt'>
  <td colspan=2 height=22 class=xl79 style='border-right:1.0pt ;
  height:16.15pt;border-left:none'>PostCondition</td>
  <td class=xl70>用户修改后的内容正确呈现在需求条目树中</td>
 </tr>
 </table>


##### 3.1.3.7 修改需求条目内容

用户对需求条目的主要信息、基本信息以及需求追踪信息进行修改。

<center>表3-31 修改需求条目内容RUCM</center>

<table border=0 cellpadding=0 cellspacing=0 width=627 style='border-collapse:
 collapse;table-layout:auto;'>
 <col width=150 style='mso-width-source:userset;mso-width-alt:5120;'>
 <col width=67 style='mso-width-source:userset;mso-width-alt:2269;'>
 <col width=68 style=''>
 <col width=342 style='mso-width-source:userset;mso-width-alt:11656;'>
 <tr height=21 style='height:15.75pt'>
  <td colspan=4 height=21 class=xl74 width=627 style='border-right:1.0pt ;
  height:15.75pt;'>Use Case Specification</td>
 </tr>
 <tr height=22 style='height:16.15pt'>
  <td height=22 class=xl65 width=150 style='height:16.15pt;'>Use
  Case Name</td>
  <td colspan=3 class=xl71 style='border-right:1.0pt ;border-left:
  none'>修改需求条目内容</td>
 </tr>
 <tr height=96 style='mso-height-source:userset;height:72.0pt'>
  <td height=96 class=xl65 width=150 style='height:72.0pt;'>Brief
  Description</td>
  <td colspan=3 class=xl71 style='border-right:1.0pt ;border-left:
  none'>用户对需求条目的主要信息、基本信息进行修改</td>
 </tr>
 <tr height=96 style='mso-height-source:userset;height:72.0pt'>
  <td height=96 class=xl65 width=150 style='height:72.0pt;'>Precondition</td>
  <td colspan=3 class=xl71 style='border-right:1.0pt ;border-left:
  none'>用户已创建需要修改的需求条目</td>
 </tr>
 <tr height=22 style='height:16.15pt'>
  <td height=22 class=xl65 width=150 style='height:16.15pt;'>Primary
  Actor</td>
  <td colspan=3 class=xl71 style='border-right:1.0pt ;border-left:
  none'>项目经理、项目组长</td>
 </tr>
 <tr height=22 style='height:16.15pt'>
  <td height=22 class=xl65 width=150 style='height:16.15pt;'>Secondary
  Actors</td>
  <td colspan=3 class=xl71 style='border-right:1.0pt ;border-left:
  none'>无</td>
 </tr>
 <tr height=22 style='height:16.15pt'>
  <td height=22 class=xl65 width=150 style='height:16.15pt;'>Dependency</td>
  <td colspan=3 class=xl71 style='border-right:1.0pt ;border-left:
  none'>修改需求条目-include</td>
 </tr>
 <tr height=22 style='height:16.15pt'>
  <td height=22 class=xl65 width=150 style='height:16.15pt;'>Generalization<span
  style='mso-spacerun:yes'> </span></td>
  <td colspan=3 class=xl71 style='border-right:1.0pt ;border-left:
  none'>无</td>
 </tr>
 <tr height=21 style='height:15.4pt'>
  <td rowspan=8 height=427 class=xl77 width=150 style='border-bottom:1.0pt ;
  height:319.55pt;border-top:none;'>Basic Flow</td>
  <td colspan=3 class=xl79 style='border-right:1.0pt ;border-left:
  none'>Steps</td>
 </tr>
 <tr height=96 style='mso-height-source:userset;height:72.0pt'>
  <td height=96 class=xl69 style='height:72.0pt'>1</td>
  <td colspan=2 class=xl71 style='border-right:1.0pt ;border-left:
  none'>用户选择需要修改的需求条目</td>
 </tr>
 <tr height=96 style='mso-height-source:userset;height:72.0pt'>
  <td height=96 class=xl69 style='height:72.0pt'>2</td>
  <td colspan=2 class=xl82 width=410 style='border-right:1.0pt ;
  border-left:none;'>用户点击相应需求条目的主要信息、基本信息页签</td>
 </tr>
 <tr height=96 style='mso-height-source:userset;height:72.0pt'>
  <td height=96 class=xl69 style='height:72.0pt'>3</td>
  <td colspan=2 class=xl84 width=410 style='border-right:1.0pt ;
  border-left:none;'>用户手动编辑对相关内容进行修改</td>
 </tr>
 <tr height=96 style='mso-height-source:userset;height:72.0pt'>
  <td height=96 class=xl69 style='height:72.0pt'>4</td>
  <td colspan=2 class=xl71 style='border-right:1.0pt ;border-left:
  none'>用户点击保存按钮</td>
 </tr>
 <tr height=96 style='mso-height-source:userset;height:72.0pt'>
  <td height=96 class=xl69 style='height:72.0pt'>5</td>
  <td colspan=2 class=xl71 style='border-right:1.0pt ;border-left:
  none'>系统提示用户是否进行需求分析</td>
 </tr>
 <tr height=96 style='mso-height-source:userset;height:72.0pt'>
  <td height=96 class=xl69 style='height:72.0pt'>6</td>
  <td colspan=2 class=xl71 style='border-right:1.0pt ;border-left:
  none'>用户选择直接保存</td>
 </tr>
 <tr height=22 style='height:16.15pt'>
  <td colspan=2 height=22 class=xl79 style='border-right:1.0pt ;
  height:16.15pt;border-left:none'>PostCondition</td>
  <td class=xl70>用户修改后的内容正确呈现在需求条目树中</td>
 </tr>
 <tr height=21 style='height:15.4pt'>
  <td rowspan=5 height=65 class=xl77 width=150 style='border-bottom:1.0pt ;
  height:47.7pt;border-top:none;'>Specific Alternative Flow</td>
  <td class=xl68 width=67 style='border-top:none;'>RFS</td>
  <td colspan=3 class=xl86 width=410 style='border-right:1.0pt ;
  border-left:none;'>5</td>
 </tr>
 <tr height=22 style='height:16.15pt'>
  <td height=22 class=xl66 width=67 style='height:16.15pt;'>1</td>
  <td colspan=2 class=xl88 width=410 style='border-right:1.0pt ;
  border-left:none;'>用户选择进行需求分析</td>
 </tr>
 <tr height=22 style='height:16.15pt'>
  <td height=22 class=xl66 width=67 style='height:16.15pt;'>2</td>
  <td colspan=2 class=xl88 width=410 style='border-right:1.0pt ;
  border-left:none;'>系统跳转到需求分析页签</td>
 </tr>
 <tr height=22 style='height:16.15pt'>
  <td height=22 class=xl66 width=67 style='height:16.15pt;'>3</td>
  <td colspan=2 class=xl88 width=410 style='border-right:1.0pt ;
  border-left:none;'>RESUME STEP</td>
 </tr>
 <tr height=22 style='height:16.15pt'>
  <td colspan=2 height=22 class=xl90 width=135 style='border-right:1.0pt ;
  height:16.15pt;border-left:none;'>PostCondition</td>
  <td class=xl67 width=342 style=''>无</td>
 </tr>
</table>


##### 3.1.3.8 移动需求条目位置

用户调整需求条目在需求条目树中的位置。

<center>表3-32 移动需求条目位置RUCM</center>

<table border=0 cellpadding=0 cellspacing=0 width=666 style='border-collapse:
 collapse;table-layout:auto;'>
 <col width=160 style='mso-width-source:userset;mso-width-alt:5120;'>
 <col width=71 span=2 style=''>
 <col width=364 style='mso-width-source:userset;mso-width-alt:11648;'>
 <tr height=23 style='height:17.0pt'>
  <td colspan=4 height=23 class=xl74 width=666 style='border-right:1.0pt ;
  height:17.0pt;'>Use Case Specification</td>
 </tr>
 <tr height=24 style='height:18.0pt'>
  <td height=24 class=xl65 width=160 style='height:18.0pt;'>Use Case
  Name</td>
  <td colspan=3 class=xl71 style='border-right:1.0pt ;border-left:
  none'>移动需求条目位置</td>
 </tr>
 <tr height=96 style='mso-height-source:userset;height:72.0pt'>
  <td height=96 class=xl65 width=160 style='height:72.0pt;'>Brief
  Description</td>
  <td colspan=3 class=xl71 style='border-right:1.0pt ;border-left:
  none'>用户调整需求在需求条目树中的位置</td>
 </tr>
 <tr height=96 style='mso-height-source:userset;height:72.0pt'>
  <td height=96 class=xl65 width=160 style='height:72.0pt;'>Precondition</td>
  <td colspan=3 class=xl71 style='border-right:1.0pt ;border-left:
  none'>用户已创建需要调整位置的需求条目</td>
 </tr>
 <tr height=24 style='height:18.0pt'>
  <td height=24 class=xl65 width=160 style='height:18.0pt;'>Primary
  Actor</td>
  <td colspan=3 class=xl71 style='border-right:1.0pt ;border-left:
  none'>项目经理、项目组长</td>
 </tr>
 <tr height=24 style='height:18.0pt'>
  <td height=24 class=xl65 width=160 style='height:18.0pt;'>Secondary
  Actors</td>
  <td colspan=3 class=xl71 style='border-right:1.0pt ;border-left:
  none'>无</td>
 </tr>
 <tr height=24 style='height:18.0pt'>
  <td height=24 class=xl65 width=160 style='height:18.0pt;'>Dependency</td>
  <td colspan=3 class=xl71 style='border-right:1.0pt ;border-left:
  none'>修改需求条目内容-inculde</td>
 </tr>
 <tr height=24 style='height:18.0pt'>
  <td height=24 class=xl65 width=160 style='height:18.0pt;'>Generalization<span
  style='mso-spacerun:yes'> </span></td>
  <td colspan=3 class=xl71 style='border-right:1.0pt ;border-left:
  none'>无</td>
 </tr>
 <tr height=23 style='height:17.0pt'>
  <td rowspan=5 height=238 class=xl77 width=160 style='border-bottom:1.0pt ;
  height:178.0pt;border-top:none;'>Basic Flow</td>
  <td colspan=3 class=xl79 style='border-right:1.0pt ;border-left:
  none'>Steps</td>
 </tr>
 <tr height=96 style='mso-height-source:userset;height:72.0pt'>
  <td height=96 class=xl69 style='height:72.0pt'>1</td>
  <td colspan=2 class=xl71 style='border-right:1.0pt ;border-left:
  none'>用户点击移动按钮，进入需求条目位置调整界面</td>
 </tr>
 <tr height=96 style='mso-height-source:userset;height:72.0pt'>
  <td height=96 class=xl69 style='height:72.0pt'>2</td>
  <td colspan=2 class=xl82 width=435 style='border-right:1.0pt ;
  border-left:none;'>用户根据需要对需求条目进行推拽放置在合适的位置</td>
 </tr>
 <tr height=96 style='mso-height-source:userset;height:72.0pt'>
  <td height=96 class=xl69 style='height:72.0pt'>3</td>
  <td colspan=2 class=xl82 width=435 style='border-right:1.0pt ;
  border-left:none;'>用户点击保存</td>
 </tr>
 <tr height=23 style='height:17.0pt'>
  <td colspan=2 height=23 class=xl79 style='border-right:1.0pt ;
  height:17.0pt;border-left:none'>PostCondition</td>
  <td class=xl70>用户调整后的需求条目位置正确呈现在需求条目树中</td>
 </tr>
 <tr height=21 style='height:15.4pt'>
  <td rowspan=5 height=65 class=xl77 width=150 style='border-bottom:1.0pt ;
  height:47.7pt;border-top:none;'>Specific Alternative Flow</td>
  <td class=xl68 width=67 style='border-top:none;'>RFS</td>
  <td colspan=3 class=xl86 width=410 style='border-right:1.0pt ;
  border-left:none;'>3</td>
 </tr>
 <tr height=22 style='height:16.15pt'>
  <td height=22 class=xl66 width=67 style='height:16.15pt;'>1</td>
  <td colspan=2 class=xl88 width=410 style='border-right:1.0pt ;
  border-left:none;'>用户点击取消按钮</td>
 </tr>
 <tr height=22 style='height:16.15pt'>
  <td height=22 class=xl66 width=67 style='height:16.15pt;'>2</td>
  <td colspan=2 class=xl88 width=410 style='border-right:1.0pt ;
  border-left:none;'>系统回到之前的界面</td>
 </tr>
 <tr height=22 style='height:16.15pt'>
  <td height=22 class=xl66 width=67 style='height:16.15pt;'>3</td>
  <td colspan=2 class=xl88 width=410 style='border-right:1.0pt ;
  border-left:none;'>ABORT</td>
 </tr>
 <tr height=22 style='height:16.15pt'>
  <td colspan=2 height=22 class=xl90 width=135 style='border-right:1.0pt ;
  height:16.15pt;border-left:none;'>PostCondition</td>
  <td class=xl67 width=342 style=''>取消之前的移动操作</td>
 </tr>
</table>


##### 3.1.3.9 建立需求正向追踪

用户对需求进行追踪，包括代码、测试用例以及相应的开发人员。

具体的UML活动图如图3-14：

![需求管理功能用例图.jpg](./images/建立需求正向追踪活动图.jpg)

<center>图3-14 建立需求正向追踪活动图</center>

<center>表3-33 建立需求正向追踪RUCM</center>

<table border=0 cellpadding=0 cellspacing=0 width=666 style='border-collapse:
 collapse;table-layout:auto;'>
 <col width=160 style='mso-width-source:userset;mso-width-alt:5120;'>
 <col width=71 span=2 style=''>
 <col width=364 style='mso-width-source:userset;mso-width-alt:11648;'>
 <tr height=23 style='height:17.0pt'>
  <td colspan=4 height=23 class=xl74 width=666 style='border-right:1.0pt ;
  height:17.0pt;'>Use Case Specification</td>
 </tr>
 <tr height=24 style='height:18.0pt'>
  <td height=24 class=xl65 width=160 style='height:18.0pt;'>Use Case
  Name</td>
  <td colspan=3 class=xl71 style='border-right:1.0pt ;border-left:
  none'>建立需求正向追踪</td>
 </tr>
 <tr height=96 style='mso-height-source:userset;height:72.0pt'>
  <td height=96 class=xl65 width=160 style='height:72.0pt;'>Brief
  Description</td>
  <td colspan=3 class=xl71 style='border-right:1.0pt ;border-left:
  none'>用户对需求进行追踪，包括代码、测试用例以及相应的开发人员</td>
 </tr>
 <tr height=96 style='mso-height-source:userset;height:72.0pt'>
  <td height=96 class=xl65 width=160 style='height:72.0pt;'>Precondition</td>
  <td colspan=3 class=xl71 style='border-right:1.0pt ;border-left:
  none'>用户已创建需要正向追踪的需求条目</td>
 </tr>
 <tr height=24 style='height:18.0pt'>
  <td height=24 class=xl65 width=160 style='height:18.0pt;'>Primary
  Actor</td>
  <td colspan=3 class=xl71 style='border-right:1.0pt ;border-left:
  none'>项目经理、项目组长</td>
 </tr>
 <tr height=24 style='height:18.0pt'>
  <td height=24 class=xl65 width=160 style='height:18.0pt;'>Secondary
  Actors</td>
  <td colspan=3 class=xl71 style='border-right:1.0pt ;border-left:
  none'>无</td>
 </tr>
 <tr height=24 style='height:18.0pt'>
  <td height=24 class=xl65 width=160 style='height:18.0pt;'>Dependency</td>
  <td colspan=3 class=xl71 style='border-right:1.0pt ;border-left:
  none'>无</td>
 </tr>
 <tr height=24 style='height:18.0pt'>
  <td height=24 class=xl65 width=160 style='height:18.0pt;'>Generalization<span
  style='mso-spacerun:yes'> </span></td>
  <td colspan=3 class=xl71 style='border-right:1.0pt ;border-left:
  none'>无</td>
 </tr>
 <tr height=23 style='height:17.0pt'>
  <td rowspan=7 height=238 class=xl77 width=160 style='border-bottom:1.0pt ;
  height:178.0pt;border-top:none;'>Basic Flow</td>
  <td colspan=3 class=xl79 style='border-right:1.0pt ;border-left:
  none'>Steps</td>
 </tr>
 <tr height=96 style='mso-height-source:userset;height:72.0pt'>
  <td height=96 class=xl69 style='height:72.0pt'>1</td>
  <td colspan=2 class=xl71 style='border-right:1.0pt ;border-left:
  none'>用户选择要追踪的需求条目</td>
 </tr>
 <tr height=96 style='mso-height-source:userset;height:72.0pt'>
  <td height=96 class=xl69 style='height:72.0pt'>2</td>
  <td colspan=2 class=xl82 width=435 style='border-right:1.0pt ;
  border-left:none;'>用户点击需求追踪页签</td>
 </tr>
 <tr height=96 style='mso-height-source:userset;height:72.0pt'>
  <td height=96 class=xl69 style='height:72.0pt'>3</td>
  <td colspan=2 class=xl82 width=435 style='border-right:1.0pt ;
  border-left:none;'>用户填入相应的追踪代码、追踪测试用例以及追踪人员信息</td>
 </tr>
 <tr height=96 style='mso-height-source:userset;height:72.0pt'>
  <td height=96 class=xl69 style='height:72.0pt'>4</td>
  <td colspan=2 class=xl82 width=435 style='border-right:1.0pt ;
  border-left:none;'>用户点击保存按钮</td>
 </tr>
 <tr height=96 style='mso-height-source:userset;height:72.0pt'>
  <td height=96 class=xl69 style='height:72.0pt'>5</td>
  <td colspan=2 class=xl82 width=435 style='border-right:1.0pt ;
  border-left:none;'>系统反馈操作成功的信息</td>
 </tr>
 <tr height=23 style='height:17.0pt'>
  <td colspan=2 height=23 class=xl79 style='border-right:1.0pt ;
  height:17.0pt;border-left:none'>PostCondition</td>
  <td class=xl70>用户建立的正向追踪内容能够正确呈现在需求条目的信息中</td>
 </tr>
</table>

##### 3.1.3.10 需求分析

用户可以对每个项目的所有需求条目进行需求结构化、需求模糊检测、需求冲突检测以及需求关联关系分析等分析操作。

<center>表3-34 需求分析RUCM</center>

<table border="0" cellpadding="0" cellspacing="0"  >
 <colgroup><col  >
 <col  span="2" >
 <col  >
 </colgroup>
 <tbody>
 <tr  >
  <td colspan="4"    >Use Case Specification</td>
 </tr>
 <tr  >
  <td    >Use Case Name</td>
  <td colspan="3"   >需求分析</td>
 </tr>
 <tr  >
  <td    >Brief Description</td>
  <td colspan="3"   >包括多种具体的需求分析服务，辅助项目人员理解需求。</td>
 </tr>
 <tr  >
  <td    >Precondition</td>
  <td colspan="3"   >需求条目已经录入到系统中。</td>
 </tr>
 <tr  >
  <td    >Primary Actor</td>
  <td colspan="3"   >项目经理、项目组长</td>
 </tr>
 <tr  >
  <td    >Secondary Actors</td>
  <td colspan="3"   >无</td>
 </tr>
 <tr  >
  <td    >Dependency</td>
  <td colspan="3"   >include-需求结构化、include-共性需求识别、include-需求冲突检测、include-需求关联关系分析</td>
 </tr>
 <tr  >
  <td    >Generalization</td>
  <td colspan="3"   >无</td>
 </tr>
 <tr  >
  <td rowspan="4"    >Basic Flow</td>
  <td colspan="3"   >steps</td>
 </tr>
 <tr  >
  <td    >1</td>
  <td colspan="2"   >用户进入项目主界面</td>
 </tr>
 <tr  >
  <td    >2</td>
  <td colspan="2"   >点击需求分析</td>
 </tr>
 <tr  >
  <td colspan="2"    >PostCondition</td>
  <td   >成功进入需求分析标签页，页面展示可以选择的具体功能</td>
 </tr>
 <tr  >
  <td rowspan="6"    >Specific Alternative Flow</td>
  <td   >RFS</td>
  <td colspan="2"   >1</td>
 </tr>
 <tr  >
  <td    >1</td>
  <td colspan="2"   >用户创建单条需求条目完毕</td>
 </tr>
  <tr  >
  <td    >2</td>
  <td colspan="2"   >用户选择需求分析范围</td>
 </tr>
  <tr  >
  <td    >3</td>
  <td colspan="2"   >用户点击开始分析</td>
 </tr>
  <tr  >
  <td    >4</td>
  <td colspan="2"   >RESUME STEP</td>
 </tr>
 <tr  >
  <td colspan="2"    >PostCondition</td>
  <td   >界面成功显示可以选择的具体功能</td>
 </tr>
</tbody></table>



图3-15为需求分析功能活动图，需要说明的是，该图适用于包括共性需求识别、需求冲突检测等在内的所有需求分析功能。

![需求分析功能活动图.jpg](./images/需求分析活动图.jpg)

<center>图3-15 需求分析活动图</center>


##### 3.1.3.11 需求结构化

需求结构化是其他算法服务的基础，通过需求结构化可以将需求条目拆分为更细粒度的语法单元。

<center>表3-35 需求结构化RUCM</center>

<table border="0" cellpadding="0" cellspacing="0"  >
 <colgroup><col  >
 <col  span="2" >
 <col  >
 </colgroup>
 <tbody>
 <tr  >
  <td colspan="4"    >Use Case Specification</td>
 </tr>
 <tr  >
  <td    >Use Case Name</td>
  <td colspan="3"   >需求结构化</td>
 </tr>
 <tr  >
  <td    >Brief Description</td>
  <td colspan="3"   >通过NLP工具以及事先制定好的启发式规则对于需求条目进行分析，提取出更细粒度的语法元素，为其他算法服务奠定基础。</td>
 </tr>
 <tr  >
  <td    >Precondition</td>
  <td colspan="3"   >需求条目已经录入到系统中。</td>
 </tr>
 <tr  >
  <td    >Primary Actor</td>
  <td colspan="3"   >项目经理、项目组长</td>
 </tr>
 <tr  >
  <td    >Secondary Actors</td>
  <td colspan="3"   >无</td>
 </tr>
 <tr  >
  <td    >Dependency</td>
  <td colspan="3"   >需求分析-include</td>
 </tr>
 <tr  >
  <td    >Generalization</td>
  <td colspan="3"   >无</td>
 </tr>
 <tr  >
  <td rowspan="5"    >Basic Flow</td>
  <td colspan="3"   >steps</td>
 </tr>
 <tr  >
  <td    >1</td>
  <td colspan="2"   >用户点击需求分析</td>
 </tr>
 <tr  >
  <td    >2</td>
  <td colspan="2"   >执行结构化算法</td>
 </tr>
  <tr  >
  <td    >3</td>
  <td colspan="2"   >保存结构化结果，以供后续具体算法使用</td>
 </tr>
 <tr  >
  <td colspan="2"    >PostCondition</td>
  <td   >无</td>
 </tr>
 <tr  >
  <td rowspan="5"    >Specific Alternative Flow</td>
  <td   >RFS</td>
  <td colspan="2"   >3</td>
 </tr>
 <tr  >
  <td    >1</td>
  <td colspan="2"   >结构化失败，界面显示提示</td>
 </tr>
 <tr  >
  <td    >2</td>
  <td colspan="2"   >ABORT</td>
 </tr>
 <tr  >
  <td colspan="2"    >PostCondition</td>
  <td   >无</td>
 </tr>
</tbody></table>



##### 3.1.3.12 共性需求识别

共性需求识别可以识别出语义基本相同的需求，从而辅助需求创建与变更过程中的查重。

<center>表3-36 共性需求识别RUCM</center>

<table border="0" cellpadding="0" cellspacing="0"  >
 <colgroup><col  >
 <col  span="2" >
 <col  >
 </colgroup>
 <tbody>
 <tr  >
  <td colspan="4"    >Use Case Specification</td>
 </tr>
 <tr  >
  <td    >Use Case Name</td>
  <td colspan="3"   >共性需求识别</td>
 </tr>
 <tr  >
  <td    >Brief Description</td>
  <td colspan="3"   >通过训练好的Word2vec模型对于需求条目进行共性需求识别，检测出语义基本相同的需求。</td>
 </tr>
 <tr  >
  <td rowspan="2"   >Precondition </td>
  <td colspan="3"   >1. 需求条目已经录入到系统中。</td>
 </tr>
<tr  >
  <td colspan="3"   >2. 已经提前训练好Word2vec模型。</td>
 </tr>
 <tr  >
  <td    >Primary Actor</td>
  <td colspan="3"   >项目经理、项目组长</td>
 </tr>
 <tr  >
  <td    >Secondary Actors</td>
  <td colspan="3"   >无</td>
 </tr>
 <tr  >
  <td    >Dependency</td>
  <td colspan="3"   >无</td>
 </tr>
 <tr  >
  <td    >Generalization</td>
  <td colspan="3"   >需求分析-include</td>
 </tr>
 <tr  >
  <td rowspan="4"    >Basic Flow</td>
  <td colspan="3"   >steps</td>
 </tr>
 <tr  >
  <td    >1</td>
  <td colspan="2"   >用户点击共性需求识别</td>
 </tr>
 <tr  >
  <td    >2</td>
  <td colspan="2"   >存在共性需求，界面显示共性需求编号及内容</td>
 </tr>
 <tr  >
  <td colspan="2"    >PostCondition</td>
  <td   >无</td>
 </tr>
 <tr  >
  <td rowspan="5"    >Specific Alternative Flow</td>
  <td   >RFS</td>
  <td colspan="2"   >2</td>
 </tr>
 <tr  >
  <td    >1</td>
  <td colspan="2"   >不存在共性需求，界面提示需求条目中共性需求</td>
 </tr>
 <tr  >
  <td    >2</td>
  <td colspan="2"   >ABORT</td>
 </tr>
 <tr  >
  <td colspan="2"    >PostCondition</td>
  <td   >无</td>
 </tr>
</tbody></table>



##### 3.1.3.13 需求冲突检测

需求冲突检测可以检测出需求条目中存在的冲突并对其进行准确的定位与展示，以方便需求编写人员后续对其进行处理。

<center>表3-37 需求冲突检测RUCM</center>

<table border="0" cellpadding="0" cellspacing="0"  >
 <colgroup><col  >
 <col  span="2" >
 <col  >
 </colgroup>
 <tbody>
 <tr  >
  <td colspan="4"    >Use Case Specification</td>
 </tr>
 <tr  >
  <td    >Use Case Name</td>
  <td colspan="3"   >需求冲突检测</td>
 </tr>
 <tr  >
  <td    >Brief Description</td>
  <td colspan="3"   >通过NLP工具以及事先制定好的启发式规则对于需求条目进行冲突检测，检测出需求条目中存在的冲突。</td>
 </tr>
 <tr  >
  <td >Precondition </td>
  <td colspan="3"   >需求条目已经录入到系统中。</td>
 </tr>
 <tr  >
  <td    >Primary Actor</td>
  <td colspan="3"   >项目经理、项目组长</td>
 </tr>
 <tr  >
  <td    >Secondary Actors</td>
  <td colspan="3"   >无</td>
 </tr>
 <tr  >
  <td    >Dependency</td>
  <td colspan="3"   >需求分析-include</td>
 </tr>
 <tr  >
  <td    >Generalization</td>
  <td colspan="3"   >无</td>
 </tr>
 <tr  >
  <td rowspan="4"    >Basic Flow</td>
  <td colspan="3"   >steps</td>
 </tr>
 <tr  >
  <td    >1</td>
  <td colspan="2"   >用户点击冲突检测</td>
 </tr>
 <tr  >
  <td    >2</td>
  <td colspan="2"   >存在冲突，界面显示冲突具体内容</td>
 </tr>
 <tr  >
  <td colspan="2"    >PostCondition</td>
  <td   >无</td>
 </tr>
  <tr  >
  <td rowspan="5"    >Specific Alternative Flow</td>
  <td   >RFS</td>
  <td colspan="2"   >2</td>
 </tr>
 <tr  >
  <td    >1</td>
  <td colspan="2"   >不存在冲突，界面提示需求条目中无冲突</td>
 </tr>
 <tr  >
  <td    >2</td>
  <td colspan="2"   >ABORT</td>
 </tr>
 <tr  >
  <td colspan="2"    >PostCondition</td>
  <td   >无</td>
 </tr>
</tbody></table>

##### 3.1.3.14 需求关联关系分析

需求关联关系分析可以检测出需求条目之间存在的关联关系，这对于后续的需求结构分析以及需求实现都有着重大价值。

<center>表3-38 需求关联关系分析RUCM</center>

<table border="0" cellpadding="0" cellspacing="0"  >
 <colgroup><col  >
 <col  span="2" >
 <col  >
 </colgroup>
 <tbody>
 <tr  >
  <td colspan="4"    >Use Case Specification</td>
 </tr>
 <tr  >
  <td    >Use Case Name</td>
  <td colspan="3"   >需求关联关系分析</td>
 </tr>
 <tr  >
  <td    >Brief Description</td>
  <td colspan="3"   >通过NLP工具以及事先制定好的启发式规则对于需求条目进行关联关系分析，检测出需求条目间存在的关联关系。</td>
 </tr>
 <tr  >
  <td >Precondition </td>
  <td colspan="3"   >需求条目已经录入到系统中。</td>
 </tr>
 <tr  >
  <td    >Primary Actor</td>
  <td colspan="3"   >项目经理、项目组长</td>
 </tr>
 <tr  >
  <td    >Secondary Actors</td>
  <td colspan="3"   >无</td>
 </tr>
 <tr  >
  <td    >Dependency</td>
  <td colspan="3"   >需求分析-include</td>
 </tr>
 <tr  >
  <td    >Generalization</td>
  <td colspan="3"   >无</td>
 </tr>
 <tr  >
  <td rowspan="4"    >Basic Flow</td>
  <td colspan="3"   >steps</td>
 </tr>
 <tr  >
  <td    >1</td>
  <td colspan="2"   >用户点击关联关系分析</td>
 </tr>
 <tr  >
  <td    >2</td>
  <td colspan="2"   >存在关联关系，界面显示每一条关联关系的类型以及两端的需求条目</td>
 </tr>
 <tr  >
  <td colspan="2"    >PostCondition</td>
  <td   >无</td>
 </tr>
 <tr  >
  <td rowspan="5"    >Specific Alternative Flow</td>
  <td   >RFS</td>
  <td colspan="2"   >2</td>
 </tr>
 <tr  >
  <td    >1</td>
  <td colspan="2"   >不存在关联关系，界面提示需求条目间不存在关联关系</td>
 </tr>
 <tr  >
  <td    >2</td>
  <td colspan="2"   >ABORT</td>
 </tr>
 <tr  >
  <td colspan="2"    >PostCondition</td>
  <td   >无</td>
 </tr>
</tbody></table>


##### 3.1.1.15 查看需求条目树

所有用户均可以查看需求条目树。

<center>表3-39 查看需求条目树RUCM</center>

<table border="0" cellpadding="0" cellspacing="0"  >
 <colgroup><col  >
 <col  span="2" >
 <col  >
 </colgroup><tbody><tr  >
  <td colspan="4"    >Use
  Case Specification</td>
 </tr>
 <tr  >
  <td    >Use Case Name</td>
  <td colspan="3"   >查看需求条目树</td>
 </tr>
 <tr  >
  <td    >Brief Description</td>
  <td colspan="3"   >系统根据需求条目之间的层次关系，将一个项目的所有需求条目渲染成树状显示在页面中。</td>
 </tr>
 <tr  >
  <td rowspan="2"   >Precondition </td>
  <td colspan="3"   >1. 需求条目已经全部录入到系统中。</td>
 </tr>
<tr  >
  <td colspan="3"   >2. 已经建立好需求条目之间层次关系。</td>
 </tr>
 <tr  >
  <td    >Primary Actor</td>
  <td colspan="3"   >所有用户</td>
 </tr>
 <tr  >
  <td    >Secondary Actors</td>
  <td colspan="3"   >无</td>
 </tr>
 <tr  >
  <td    >Dependency</td>
  <td colspan="3"   >无</td>
 </tr>
 <tr  >
  <td    >Generalization</td>
  <td colspan="3"   >无</td>
 </tr>
 <tr  >
  <td rowspan="5"    >Basic Flow</td>
  <td colspan="3"   >steps</td>
 </tr>
 <tr  >
  <td    >1</td>
  <td colspan="2"   >用户点击项目名称</td>
 </tr>
 <tr  >
  <td    >2</td>
  <td colspan="2"   >进入项目主页</td>
 </tr>
  <tr  >
  <td    >3</td>
  <td colspan="2"   >系统确定用户有相应权限</td>
 </tr>
 <tr  >
  <td colspan="2"    >PostCondition</td>
  <td   >主界面以树状结构显示所有需求条目</td>
 </tr>
  <tr  >
  <td rowspan="5"    >Specific Alternative Flow</td>
  <td   >RFS</td>
  <td colspan="2"   >3</td>
 </tr>
 <tr  >
  <td    >1</td>
  <td colspan="2"   >系统确定用户无相应权限</td>
 </tr>
  <tr  >
  <td    >2</td>
  <td colspan="2"   >系统提示无权限</td>
 </tr>
 <tr  >
  <td    >3</td>
  <td colspan="2"   >ABORT</td>
 </tr>
 <tr  >
  <td colspan="2"    >PostCondition</td>
  <td   >无</td>
 </tr>
</tbody></table>


图3-16为查看需求条目树功能活动图。

![查看需求条目树功能活动图.jpg](./images/查看需求条目树活动图.jpg)

<center>图3-16 查看需求条目树活动图</center>


##### 3.1.1.16 查看需求条目内容

所有用户均可以查看需求条目的具体内容。

<center>表3-40 查看需求条目内容RUCM</center>

<table border="0" cellpadding="0" cellspacing="0"  >
 <colgroup><col  >
 <col  span="2" >
 <col  >
 </colgroup><tbody><tr  >
  <td colspan="4"    >Use
  Case Specification</td>
 </tr>
 <tr  >
  <td    >Use Case Name</td>
  <td colspan="3"   >查看需求条目内容</td>
 </tr>
 <tr  >
  <td    >Brief Description</td>
  <td colspan="3"   >查看需求条目的名称、描述等具体信息。</td>
 </tr>
 <tr  >
  <td    >Precondition</td>
  <td colspan="3"   >需求条目已经录入到系统中。</td>
 </tr>
 <tr  >
  <td    >Primary Actor</td>
  <td colspan="3"   >所有用户</td>
 </tr>
 <tr  >
  <td    >Secondary Actors</td>
  <td colspan="3"   >无</td>
 </tr>
 <tr  >
  <td    >Dependency</td>
  <td colspan="3"   >无</td>
 </tr>
 <tr  >
  <td    >Generalization</td>
  <td colspan="3"   >无</td>
 </tr>
 <tr  >
  <td rowspan="4"    >Basic Flow</td>
  <td colspan="3"   >steps</td>
 </tr>
 <tr  >
  <td    >1</td>
  <td colspan="2"   >用户点击某具体需求条目</td>
 </tr>
 <tr  >
  <td colspan="2"    >PostCondition</td>
  <td   >页面中展示该需求条目的详细内容</td>
 </tr>
</tbody></table>

##### 3.1.1.17 查看需求正向追踪

所有用户均可以查看需求条目正向追踪的具体内容，可能包括追踪代码、追踪测试以及追踪人员。

<center>表3-41 查看需求正向追踪RUCM</center>

<table border="0" cellpadding="0" cellspacing="0"  >
 <colgroup><col  >
 <col  span="2" >
 <col  >
 </colgroup><tbody><tr  >
  <td colspan="4"    >Use
  Case Specification</td>
 </tr>
 <tr  >
  <td    >Use Case Name</td>
  <td colspan="3"   >查看需求正向追踪</td>
 </tr>
 <tr  >
  <td    >Brief Description</td>
  <td colspan="3"   >查看需求条目正向追踪的具体内容，可能包括追踪代码、追踪测试以及追踪人员。</td>
 </tr>
 <tr  >
  <td    >Precondition</td>
  <td colspan="3"   >需求条目已经录入到系统中。</td>
 </tr>
 <tr  >
  <td    >Primary Actor</td>
  <td colspan="3"   >所有用户</td>
 </tr>
 <tr  >
  <td    >Secondary Actors</td>
  <td colspan="3"   >无</td>
 </tr>
 <tr  >
  <td    >Dependency</td>
  <td colspan="3"   >无</td>
 </tr>
 <tr  >
  <td    >Generalization</td>
  <td colspan="3"   >无</td>
 </tr>
 <tr  >
  <td rowspan="4"    >Basic Flow</td>
  <td colspan="3"   >steps</td>
 </tr>
 <tr  >
  <td    >1</td>
  <td colspan="2"   >用户点击某具体需求条目</td>
 </tr>
 <tr  >
  <td    >2</td>
  <td colspan="2"   >用户点击需求追踪标签页</td>
 </tr>
 <tr  >
  <td colspan="2"    >PostCondition</td>
  <td   >页面中展示该需求条目拥有的所有正向追踪内容</td>
 </tr>
</tbody></table>

### 3.2 设计约束

<center>表3-42 产品设计约束</center>

| **类别** | **约束**                                                                                                                                         |
| -------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------ |
| 客户端硬件     | Intel(R) Core(TM) i7-6700HQ CPU @ 2.60GHz<br />100MB 以上可用存储空间<br />完整网络支持<br />内存 >= 8GB<br />Windows 10 64 位操作系统                 |
| 客户端软件     | Google Chrome浏览器<br />81.0版本及以上                                                                                                                |
| 服务器硬件     | **推荐配置**：<br />- EC2 类型： t2.xlarge  <br />- vCPU： 4 <br />- 内存：16GB  <br />- 网络带宽：最高 5Gbps  <br />- 操作系统：Amazon Linux 2 |

### 3.3 非功能性需求

结合上述分析，本文列出理想情况下的非功能性需求（现实受到服务器硬件配置限制）：

#### 3.3.1 响应时间

1. 响应时间指功能完成的时间，和客观环境、数据量级、用户的主观感受等都有关系。
2. 确定响应时间的指标需要根据实际所需的数量级来要求。另外，还要考虑用户的可接受度。
3. 考虑到在用户大多在需要用到需求管理服务时才会访问系统，因此用户对响应时间的感受是苛刻的；系统从点击到第一个界面显示出来所需要的时间不得超过1秒。

#### 3.3.2 可靠性

1. 平均失效时间 > 720h，平均修复时间<30min，失效后数据丢失率<99%。
2. 在发生错误后，系统应具有一定自动解脱和排除故障的能力。
3. 用户数据持久化保存，对于用户上传的信息保存到硬盘时间<1s。
4. 在产品运行中，内存使用率应<80%，CPU使用率<80%。
5. 数据库定时备份，三副本备份异地容灾。

#### 3.3.3 安全保密性

1. 工具登录体系依赖网页接口，需要根据网页的安全规范实施。
2. 保护用户的隐私信息和个性化信息。
3. 能够识别用户的非法输入，对恶意行为进行识别并记录。
4. 限制用户对于需求的输入内容，防止数据库注入攻击。
5. 前端代码保护：使用精简、混合等策略，避免工具的请求包被监听和破解，导致需求信息被复制篡改。
6. 功能模块安全：网络传输、数据存储、文件存储、网页开放接口等。
7. 内部安全：对开发人员和敏感命令设立权限。

#### 3.3.4 可维护性

1. 以科学的方法设计软件，使之有良好的结构和完备的文档，系统性能易于调整。
2. 文档应该清晰可读、书写规范统一。
3. 服务端部署流程简洁规范，持久化保存日志，日志易读，问题易溯源。
4. 产品应留有升级接口和升级空间。

#### 3.3.5 交互设计需求

产品的交互设计应满足在展示表所列的信息和功能的同时，满足表3-43所示的交互设计约束。

<center>表3-43 产品交互设计约束</center>

| **需求描述**                       | **详细要求**                                                                                                                                                                                                                                                                                                              |
| ---------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 了解用户并给用户想要的                   | （1）基于对用户的分析，将提供给用户的信息及功能按主次排序，融入界面的设计中。<br />（2）考虑到用户的喜好，选择合适的界面风格等。                                                                                                                                                                                                |
| 功能让用户一目了然                       | （1）结合用户的阅读习惯和抽象能力，设计出合适的信息、图标等元素的布局。重要功能应摆放在明显部位或易于联想到的部位（如搜索功能往往在界面的最上端，评价往往要点开才能看到等）。<br />（2）对于需求信息的呈现应有逻辑性和清晰性，结合图形与颜色的运用，让用户可以对于需求一目了然。                                                |
| 操作上减少用户的思考时间，符合用户的习惯 | （1）操作少，避免嵌套过多层级，要求用户点击三下及以下次数即可获得想要的信息。这要求在产品在主界面就应该呈现重要信息，而不是功能选择、欢迎界面等过渡环节。<br />（2）尽量减少用户的输入，采用选择列表、搜索输入自动补全列表等方法提升用户的使用体验。  <br />（3）记录用户的个性化信息，实现再次访问的直接登入，方便用户的使用。 |
| 让用户有很强的参与感，增强用户与产品粘性 | （1）增加用户对软件的反馈渠道，同时这个反馈渠道应该尽量简便。<br />（2）记录用户的个性化设置并突出显示，让用户时刻体会到产品的个性化功能。                                                                                                                                                                                      |
| 节省用户的开支                           | （1）考虑到产品可以减少用户对于需求管理的时间开支，因此需求条目等信息应该直接、明显呈现给用户，而不是设置单独的按钮单独获得。<br />（2）对于数据的组织方式应契合用户的预期方式。                                                                                                                                                |

#### 3.3.6 界面设计需求

结合产品特点及交互性要求，产品的界面设计具体要考虑的内容如表3-44所示

<center>表3-44 产品界面设计需求</center>

| **名称** | **详细要求**                                                                                                                                                     |
| -------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 整体要素       | （1）风格统一（扁平化风格）。<br />（2）自适应屏幕尺寸。  <br />（3）考虑各操作系统呈现效果。  <br />（4）遵守网页设计规范，自定义内容与图标及文字等视觉效果和谐一致。 |
| 图标           | 功能性图标：简洁、直观，与流行图标相统一。                                                                                                                             |
| 色彩           | 冷暖平衡、比例得当、重点突出，优先考虑蓝色配色，因为北航相关的色彩联想为蓝色，可以将蓝色融入色彩搭配中。                                                               |
| 文字           | 字体美观、大小和间距得当、颜色协调且符合阅读习惯。                                                                                                                     |
