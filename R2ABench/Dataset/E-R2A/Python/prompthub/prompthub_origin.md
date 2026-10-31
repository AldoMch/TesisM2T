# PromptHub——软件需求规格说明书

|  版本  | 变更时间  | 修改人 |  审核人 | 版本说明   |
| :----------: | :----------: | :----------: | :----------: | :----------: |
| v1.0.0 | 2023.3.7 | 吴晨灿，侯雨霏，陈力，黄新，许羽晟，王梓竣，刘桢炜 | 吴晨灿，侯雨霏，陈力，黄新，许羽晟，王梓竣，刘桢炜 | 初稿|
| v1.1.0 | 2023.3.14 | 吴晨灿，侯雨霏，陈力，黄新，刘桢炜 | 吴晨灿，侯雨霏，陈力，黄新，许羽晟，王梓竣，刘桢炜 | 1. 黄新：引言部分，更新术语和缩略语，新增文档说明<br />2. 陈力：总体要求，新增用户特点分析<br />3. 侯雨霏：需求分析，对三类人群的需求进行更准确的定位<br />4. 刘桢炜：功能需求，新增管理员系统对评论/回复的操作，运行环境规定：整理为服务器和客户端配置需求<br />5. 吴晨灿：新增通知系统，统一图片格式，修复文字和序号问题 |
| v1.1.1 | 2023.3.15 | 吴晨灿 | 吴晨灿，侯雨霏，陈力，黄新，许羽晟，王梓竣，刘桢炜 | 根据交叉审核，统一修改内容 |
| v1.1.2 | 2023.3.22 | 吴晨灿，侯雨霏，陈力，刘桢炜，许羽晟 | 吴晨灿，侯雨霏，陈力，刘桢炜，许羽晟 | 1. 吴晨灿：添加sqlite使用原因，修复4.3.4查询作品描述<br />2. 侯雨霏：修改3需求分析中的用户用例图、管理员用例图及文字描述<br />3. 陈力：修改2.1产品描述，2.2产品功能<br />4. 许羽晟: 修复表述问题和错别字<br /> 5. 黄新: 修复错别字和标点符号 <br /> 6.刘桢炜：修复用户注册与忘记密码分支路径，统一游客称呼 <br />|
| v1.1.3 | 2023.3.28 | 吴晨灿，侯雨霏，陈力，刘桢炜，许羽晟，王梓竣 | 吴晨灿，侯雨霏，陈力，刘桢炜，许羽晟，王梓竣 | 1. 吴晨灿：修改图表格式，修改图4.8，修改标点；<br />2. 侯雨霏：修改图3.1游客用例图，修改3.1游客需求分条顺序；<br /> 3. 陈力：修改大标题，修改2.3标点符号<br /> 4. 黄新：标点更改、修改目录标题；<br/> 5. 刘桢炜：删除四级目录，修改4.1.1，4.1.2，4.1.5活动图，修正6运行环境规定中Firefox首字母未大写问题；<br />7. 许羽晟: 修改第五节的标点符号问题;|
## 目录

- [PromptHub——软件需求规格说明书](#prompthub软件需求规格说明书)
  - [目录](#目录)
  - [1. 引言](#1-引言)
    - [1.1 文档说明](#11-文档说明)
    - [1.2 术语和缩略语](#12-术语和缩略语)
      - [1.2.1 AI Generated Content（AIGC）](#121-ai-generated-contentaigc)
      - [1.2.2 Prompt](#122-prompt)
      - [1.2.3 Vue.js框架](#123-vuejs框架)
      - [1.2.4 Django框架](#124-django框架)
      - [1.2.5 SQLite](#125-sqlite)
      - [1.2.6 Docker容器](#126-docker容器)
    - [1.3 参考文献](#13-参考文献)
  - [2. 总体要求](#2-总体要求)
    - [2.1 产品描述](#21-产品描述)
    - [2.2 产品功能](#22-产品功能)
    - [2.3 用户特点分析](#23-用户特点分析)
    - [2.3 竞品分析](#23-竞品分析)
    - [2.4 约束](#24-约束)
    - [2.5 假设和依赖关系](#25-假设和依赖关系)
      - [2.5.1 运行环境](#251-运行环境)
      - [2.5.2 网络](#252-网络)
  - [3. 需求分析](#3-需求分析)
    - [3.1 游客角度](#31-游客角度)
    - [3.2 用户角度](#32-用户角度)
    - [3.3 管理员角度](#33-管理员角度)
    - [3.4 总体用例](#34-总体用例)
  - [4. 功能需求](#4-功能需求)
    - [4.1 用户系统](#41-用户系统)
      - [4.1.1 用户注册](#411-用户注册)
      - [4.1.2 用户登录](#412-用户登录)
      - [4.1.3 用户登出](#413-用户登出)
      - [4.1.4 修改密码](#414-修改密码)
      - [4.1.5 找回密码](#415-找回密码)
      - [4.1.6 查看个人主页](#416-查看个人主页)
      - [4.1.7 查看其它用户主页](#417-查看其它用户主页)
      - [4.1.8 查看用户上传作品](#418-查看用户上传作品)
      - [4.1.9 查看个人收藏夹](#419-查看个人收藏夹)
      - [4.1.10 查看其它用户收藏夹](#4110-查看其它用户收藏夹)
      - [4.1.11 查看个人浏览历史](#4111-查看个人浏览历史)
      - [4.1.12 查看用户关注列表](#4112-查看用户关注列表)
      - [4.1.13 查看用户粉丝列表](#4113-查看用户粉丝列表)
      - [4.1.14 关注用户](#4114-关注用户)
      - [4.1.15 取消关注用户](#4115-取消关注用户)
      - [4.1.16 修改个人头像](#4116-修改个人头像)
      - [4.1.17 修改个人用户名](#4117-修改个人用户名)
    - [4.2 管理员系统](#42-管理员系统)
      - [4.2.1 管理员登录](#421-管理员登录)
      - [4.2.2 管理员登出](#422-管理员登出)
      - [4.2.3 查看用户列表](#423-查看用户列表)
      - [4.2.4 查看作品列表](#424-查看作品列表)
      - [4.2.5 审核上传作品](#425-审核上传作品)
      - [4.2.6 管理员查看评论](#426-管理员查看评论)
      - [4.2.7 管理员查看回复](#427-管理员查看回复)
      - [4.2.8 管理员删除评论](#428-管理员删除评论)
      - [4.2.9 管理员删除回复](#429-管理员删除回复)
    - [4.3 展示系统](#43-展示系统)
      - [4.3.1 上传作品](#431-上传作品)
      - [4.3.2 编辑作品](#432-编辑作品)
      - [4.3.3 删除作品](#433-删除作品)
      - [4.3.4 查询作品](#434-查询作品)
      - [4.3.5 查看作品详情](#435-查看作品详情)
      - [4.3.6 查询上传作品审核进度](#436-查询上传作品审核进度)
    - [4.4 收藏系统](#44-收藏系统)
      - [4.4.1 添加收藏](#441-添加收藏)
      - [4.4.2 收藏分类](#442-收藏分类)
        - [4.4.2.1 Public](#4421-public)
        - [4.4.2.2 Private](#4422-private)
      - [4.4.3 查看收藏](#443-查看收藏)
      - [4.4.4 取消收藏](#444-取消收藏)
      - [4.4.5 查询收藏](#445-查询收藏)
      - [4.4.6 新建收藏分类](#446-新建收藏分类)
      - [4.4.7 删除收藏分类](#447-删除收藏分类)
      - [4.4.8 修改收藏分类](#448-修改收藏分类)
        - [4.4.8.1 命名](#4481-命名)
        - [4.4.8.2 可见性](#4482-可见性)
    - [4.5 评论系统](#45-评论系统)
      - [4.5.1 评论作品](#451-评论作品)
      - [4.5.2 删除评论](#452-删除评论)
      - [4.5.3 评论回复](#453-评论回复)
      - [4.5.4 删除回复](#454-删除回复)
    - [4.6 推荐系统](#46-推荐系统)
      - [4.6.1 热门推荐](#461-热门推荐)
      - [4.6.2 个性化推荐](#462-个性化推荐)
      - [4.6.3 关闭推荐](#463-关闭推荐)
    - [4.7 通知系统](#47-通知系统)
      - [4.7.1 新增消息](#471-新增消息)
      - [4.7.2 消息已读](#472-消息已读)
      - [4.7.3 删除消息](#473-删除消息)
  - [5. 非功能需求](#5-非功能需求)
    - [5.1 响应时间](#51-响应时间)
    - [5.2 可靠性](#52-可靠性)
    - [5.3 安全保密性](#53-安全保密性)
    - [5.4 可维护性](#54-可维护性)
    - [5.5 交互设计需求](#55-交互设计需求)
    - [5.6 界面设计需求](#56-界面设计需求)
  - [6. 运行环境规定](#6-运行环境规定)


## 1. 引言

### 1.1 文档说明

文档主要分为6个部分：引言、总体描述、需求分析、功能需求、非功能需求设计、运行环境规定。各部分的作用分别如下：

- 引言：该部分将对项目中所涉及的专业术语、技术栈进行解释和介绍

- 总体描述：该部分我们会对本项目的产品定位及功能进行介绍，同时还会和已有的产品进行对比分析

- 需求分析：该部分我们会从游客、用户、管理员的角度来分析不同群体在使用本产品的过程中存在的需求和诉求

- 功能需求：该部分我们会根据需求分析设计出产品所需要实现的功能，并以RUCM表的形式进行呈现，对部分用例绘制活动图

- 非功能需求：该部分我们会对产品的安全性、可靠性、互操作性、健壮性等方面的需求进行要求和介绍

- 运行环境规定：该部分主要是针对部署该项目所需要的软硬件设施进行规约，以保证项目的正常运转

### 1.2 术语和缩略语

#### 1.2.1 AI Generated Content（AIGC）

AIGC即AI Generated Content，是指利用人工智能技术来生成内容，AIGC也被认为是继UGC (User Generated Content, 用户原创内容)、PGC (Professional Generated Content, 专业生产内容)之后的新型内容生产方式，AI绘画、AI写作等都属于AIGC的分支。其中DALL-E、Midjourney、Stable Diffusion是AI绘图较为知名的模型。

##### 1.2.1.1 DALL-E

DALL-E是一个从文本描述（Prompt）中创建图像的人工智能程序，由OpenAI在2021年1月5日发布。它使用120亿参数版本的GPT-3转化器模型来解释自然语言输入（如 "一个绿色皮包，形状像五边形"或 "一个悲伤的水豚的等距视图"）并生成相应的图像。

##### 1.2.1.2 Midjourney

MidJourney 是一个由同名研究实验室开发的人工智能程序，可根据文本生成图像，该程序于2022年7月12日进入公开测试阶段。

##### 1.2.1.3 Stable Diffusion

Stable Diffusion是2022年发布的一个从文本到图像的深度学习模型。该模型主要用于以文本描述（Prompt）作为输入从而生成对应图片的任务。除此之外，该模型还能用于其他的任务，例如：在文本描述（Prompt）的帮助下生成从图像到文本描述（Prompt）的任务。

#### 1.2.2 Prompt

在AIGC模型中，其相当于提示符的意思，通过给AI模型输入若干的提示符（Prompt），让AI模型能够通过分析这些Prompt生成对应的图片。

#### 1.2.3 Vue.js框架

Vue 是一款用于构建用户界面的 JavaScript 框架。它基于标准 HTML、CSS 和 JavaScript 构建，并提供了一套声明式的、组件化的编程模型，帮助开发者高效地开发用户界面。 

#### 1.2.4 Django框架

Django是一个免费的、开源的、基于Python的网络框架。采用了MTV的框架模式，即模型M，视图V和模版T。它最初是被开发来用于管理劳伦斯出版集团旗下的一些以新闻内容为主的网站的，即是CMS（内容管理系统）软件。 

#### 1.2.5 SQLite

SQLite是一个用C编程语言编写的轻型数据库引擎。它的设计目标是嵌入式，因此它占用的资源非常低，在嵌入式设备中，可能只需要几百K的内存就能支持其运行。并且，其处理速度相较于Mysql，PostgreSQL而言都要快，因此其受到很多开发人员的青睐，并已经在他们的应用程序中嵌入了SQLite作为其程序的数据库管理系统。 

> 在本次项目中，因为运行环境限制，所以采用轻量化的数据库作为后端数据库进行开发，在后续迭代中，为了应对高并发等使用场景，会进行数据库迁移，使用更合适的数据库，如Mysql等

#### 1.2.6 Docker容器

Docker是一种轻量级的虚拟化技术，同时是一个开源的应用容器运行环境搭建平台，可以让开发者以便捷方式打包应用到一个可移植的容器中，然后安装至任何运行Linux或Windows等系统的服务器上。 相较于传统虚拟机，Docker容器提供轻量化的虚拟化方式、并且具有安装便捷、启停速度快的特点。

### 1.3 参考文献

1. GB/T 9385-2008《计算机软件需求规格说明规范》
2. GB/T 20918-2007《信息技术、软件生存周期过程及风险管理》
3. GB/T 15532 -2008《计算机软件测试规范》
4. GB/T 20917-2007《软件工程及软件测量过程》
5. 王珊，萨师煊 著，数据库系统概论，高等教育出版社，2015 
6. 吕云翔 著，软件工程实用教程，清华大学出版社，2017 
7. Django官方网站：https://www.djangoproject.com
8. SQLite官方网站：https://www.sqlite.org
9. Vue.js官方网站：https://cn.vuejs.org
10. Docker官方网站：https://www.docker.com

## 2. 总体要求

### 2.1 产品描述

PromptHub是一款关于AI画作以及其Prompt分享的社区类Web应用，旨在在AI绘画越来越发达的时代为广大AI绘画创作者以及爱好者提供一个方便快捷且有效的AI画作的Prompt分享平台。用户可在平台内分享自己利用不同Prompt和模型所创作的AI作品、以及相关模型信息，供其他用户浏览，以便于创作者们能够在创作时选择更加精确的Prompt，绘制出更加符合需求的作品。

PromptHub的初衷是：探索AI绘画的精妙，为广大用户提供富有想象力的AI画作分享社区。

### 2.2 产品功能

PromptHub主要包括以下功能：

1. AI画作的浏览和讨论：主页提供大量AI画作供用户和游客浏览，点击图片可查看其对应的Prompt以及其创作者，并且设有评论区，可供用户对该作品进行讨论和点赞；
2. AI画作的分类和检索：用户可根据喜欢的Prompt来检索包含该Prompt的AI画作，也可根据类别来找到符合喜好的AI画作；
3. AI画作的上传和审核：用户可自行上传AI画作以及其对应的Prompt，由管理员审核通过后可供其他用户浏览；
4. 用户相关： 系统提供用户各方面信息的记录和展现的功能，并根据用户信息提供相关个性化服务，如收藏，个人信息管理等功能。 网站用户主要分为以下三类：
   - 游客：浏览和下载AI画作以及其对应的Prompt
   - 用户：除游客的功能外，还能收藏、评论以及上传AI画作，订阅其他用户，编辑自己的账户
   - 管理员：对用户进行管理，对上传的AI画作进行审核

### 2.3 用户特点分析

PromptHub的目标用户群体主要包括：AI绘画的创作者、喜爱AI画作的浏览者以及有兴趣接触AI绘画的新人。

- PromptHub为AI绘画的创作者提供了上传平台，可供创作者们上传自己的作品以及其Prompt
- PromptHub为喜爱AI画作的浏览者提供了大量AI画作的浏览服务，用户可在PromptHub的主页浏览大量的AI画作，也可根据主页的分类索引功能快速找到符合自身口味的作品
- PromptHub为有兴趣接触AI绘画的新人提供了评论区，用户可在评论区进行提问以及交流，以便用户更好地了解AI绘画

### 2.3 竞品分析

<div align="left">
  <p><strong>表2.1 竞品分析</strong></p>
</div>

|            | 包含Prompt | 多级检索功能 | 相似推荐功能 |   评论功能   | 浏览其它用户 |
| :----------: | :----------: | :----------: | :----------: | :----------: | :----------: |
| PromptHero | √ | × | × | √ | √ |
|   Draft    | √ | × | √ | × | √ |
|   Lexica   | √ | √ | √ | × | √ |
| FlagStudio | √ | × | √ | √ | × |
| PromptHub  | √ | √ | √ | √ | √ |


### 2.4 约束

我们做出以下假设与约定，以保证软件项目能够按时开发完成和投入运行、维护： 

1.  变更需求需要严格按照需求变更流程执行，并对需求规格说明书进行合理的修改与审核；
2.  项目开发进程严格按照实验计划执行；
3. 在系统运行时，需要限制同一时刻的访问量，以保证系统安全稳定运行；
4. 本项目包括前端、后端和算法支持三大模块：
   -  前端使用 HTML、CSS、JavaScript 语言和 Vue、JQuery 等框架进行开发；
   -  后端使用 Python、Java 语言和Django框架进行开发；
   -  算法支持模块使用 Python 语言及PyTorch、Tensorflow等框架进行开发。

### 2.5 假设和依赖关系

#### 2.5.1 运行环境

1.  操作系统：基于Windows7、macOS 8.0及以上版本内核的图形界面操作系统；
2.  浏览器：Firefox内核119.0版本及以上浏览器、其他基于Chromium内核110.0版本及以上开发的浏览器。

#### 2.5.2 网络

 如果用户无法进行网络连接，则所有需求无法实现。

## 3. 需求分析

### 3.1 游客角度
游客作为对AIGC内容有兴趣的人群，在浏览平台时，主要需求是希望看到优秀的作品，或者根据自己的偏好自行探索，还可能选择注册从而加入社区进行互动。综上所述，游客需求分条列出如下：

1. 游客可以注册为新用户
2. 游客可以查看当前热门推荐
3. 游客可以查询作品，可以选择不同的排序方式陈列，可以查看作品详情

**相关图**

![游客用例图](imgs/游客用例图.png)

<div align="center">
  <p><strong>图3.1 游客用例图</strong></p>
</div>


### 3.2 用户角度
游客在注册后成为平台的用户。
作为社区的主要人群，用户的主要需求是对喜欢的作品进行收藏管理方便查看、发送评论和回复与其他用户进一步交流互动，关注自己感兴趣的用户，并且获得依据自己收藏、关注等个性化偏好行为计算出的其他推荐作品；除此之外，每一位用户也都可以化身为AI绘画的创作者，方便地上传自己的AI绘画作品及其详细说明。在用户收到互动或作品审核进度变化时也需要得到相应的通知。综上所述，用户需求分条列出如下：

1. 用户可以登录、登出系统，可以修改、找回密码，可以修改基础信息，包括用户名、头像，可以查看自己的浏览历史
2. 用户可以对自己的作品增删改查，可以查看作品的审核进度
3. 用户可以查询作品，可以选择不同的排序方式陈列，可以查看作品详情
4. 用户可以收藏作品，可以建立收藏分类，可以增删改查自己的收藏和自己建立的收藏分类
5. 用户可以评论作品，可以回复其他人的评论，可以删除自己的评论和回复
6. 用户可以关注其他用户，可以查看其上传的作品和建立的收藏夹
7. 用户可以查看当前热门推荐，可以选择开启或关闭个性化推荐
8. 用户可以收到系统通知，包括收到评论、收到回复、以及作品审核进度变更时

**相关图**

![用户用例图](imgs/用户用例图.png)

<div align="center">
  <p><strong>图3.2 用户用例图</strong></p>
</div>

### 3.3 管理员角度
管理员作为平台的管理者，任务是对社区内容和社区环境进行维护。
在内容维护方面，管理员需要定期查看当前的全部用户和全部作品的情况，对用户新上传的作品进行审核，过滤掉不符合规定的低劣作品；在环境维护方面，管理员需要全面管理社区内的发言，范围覆盖用户发出的评论和回复，及时删除社区内的不良言论。综上所述，管理员需求分条列出如下：

1. 管理员可以登录、登出系统
2. 管理员可以查看用户列表
3. 管理员可以查看作品列表
4. 管理员可以查看作品下的评论，可以选择删除评论和回复
5. 管理员可以审核用户上传的图片作品，决定是通过或是拒绝

**相关图**

![管理员用例图](imgs/管理员用例图.png)

<div align="center">
  <p><strong>图3.3 管理员用例图</strong></p>
</div>

### 3.4 总体用例

![总体用例图](imgs/总体用例图.png)

<div align="center">
  <p><strong>图3.4 总体用例图</strong></p>
</div>

## 4. 功能需求

功能需求中，我们将游客、用户和管理员的需求按照模块划分，抽象为了用户系统、管理员系统、展示系统、收藏系统、评论系统、推荐系统和通知系统，并使用RUCM表对所有的功能进行了具体描述，对比较复杂的功能通过活动图的方式进行了流程绘制。

### 4.1 用户系统 

#### 4.1.1 用户注册
<div align="left">
  <p><strong>表4.1 用户注册RUCM表</strong></p>
</div>
<table><tbody>
        <tr >
            <td>作者：刘桢炜</td>
            <td>日期：2023年3月22日</td>
            <td>版本：1.1.2
        </tr>
        <tr>
            <td>用例名</td>
            <td colspan="2">用户注册</td>
        </tr>
        <tr>
            <td>用例ID</td>
            <td colspan="2">A01</td>
        </tr>
        <tr>
            <td>简要描述</td>
            <td colspan="2">游客通过注册获取用户账号</td>
        </tr>
        <tr>
            <td>参与者</td>
            <td colspan="2">游客</td>
        </tr>
        <tr>
            <td>涉众</td>
            <td colspan="2">无</td>
        </tr>
        <tr>
            <td>相关用例</td>
            <td colspan="2">登录A02</td>
        </tr>
        <tr>
            <td>前置条件</td>
            <td colspan="2">该用户未登录</td>
        </tr>
        <tr>
            <td>后置条件</td>
            <td colspan="2">
                游客通过注册获取用户账号，且游客登录成为用户；数据库中新增用户条例
                </td>
    </tr>
    <tr>
        <td colspan="3">基本事件流 <br>
        <ol> 
            <li>游客在首页点击注册账号进入注册界面</li>
            <li>游客输入邮箱，账号名，密码以及确认密码后，点击“注册”按钮</li>
            <li>系统发送验证码至邮箱</li>
            <li>用户填写邮箱中接收的验证码，点击“验证个人身份”按钮</li>
            <li>系统验证信息</li>
            <li>信息验证通过后，进入初始页面</li>
        </ol>
    </td>
</tr>
<tr>
    <td colspan="3">备选事件流 <br>
    	<ol>
            <li>邮箱、用户名、密码、确认密码有漏填，显示"信息不完整"</li>
            <li>邮箱已被使用，显示"邮箱已被注册"</li>
            <li>用户名已被使用，显示“请更换用户名”</li>
            <li>密码与确认密码不一致，显示“密码与确认密码不一致”</li>
            <li>验证码错误，显示“验证码错误”</li>
        </ol>
    </td>
</tr>
<tr>
    <td colspan="3">补充约束 <br>
        无</td>
</tr>
<tr>
    <td colspan="3">待解决问题 <br>
    无 </td>
</tr>
</tbody></table>

![需求分析A01](imgs/需求分析A01.png)

<div align="center">
  <p><strong>图4.1 用户注册活动图</strong></p>
</div>

#### 4.1.2 用户登录

<div align="left">
  <p><strong>表4.2 用户登录RUCM表</strong></p>
</div>

<table><tbody>
        <tr >
            <td>作者：刘桢炜</td>
            <td>日期：2023年3月22日</td>
            <td>版本：1.1.2
        </tr>
        <tr>
            <td>用例名</td>
            <td colspan="2">用户登录</td>
        </tr>
        <tr>
            <td>用例ID</td>
            <td colspan="2">A02</td>
        </tr>
        <tr>
            <td>简要描述</td>
            <td colspan="2">游客通过登录成为用户</td>
        </tr>
        <tr>
            <td>参与者</td>
            <td colspan="2">用户</td>
        </tr>
        <tr>
            <td>涉众</td>
            <td colspan="2">无</td>
        </tr>
        <tr>
            <td>相关用例</td>
            <td colspan="2">登出A03</td>
        </tr>
        <tr>
            <td>前置条件</td>
            <td colspan="2">该用户未登录</td>
        </tr>
        <tr>
            <td>后置条件</td>
            <td colspan="2">游客通过登录成为用户</td>
        </tr>
        <tr>
            <td colspan="3">基本事件流 <br>
            <ol> 
                <li>游客在首页点击登录进入登录界面</li>
                <li>游客输入账号名，密码后，点击“登录”按钮</li>
                <li>系统验证信息</li>
                <li>信息验证通过后，进入初始页面</li>
            </ol>
        </td>
    </tr>
    <tr>
        <td colspan="3">备选事件流 <br>
        	<ol>
                <li>用户名不存在，显示“用户不存在”</li>
                <li>密码错误，显示“用户名与密码不匹配”</li>
            </ol>
        </td>
    </tr>
    <tr>
        <td colspan="3">补充约束 <br>
            无</td>
    </tr>
    <tr>
        <td colspan="3">待解决问题 <br>
        无 </td>
    </tr>
    </tbody>
</table>


![需求分析A02](imgs/需求分析A02.png)

<div align="center">
  <p><strong>图4.2 用户登录活动图</strong></p>
</div>

#### 4.1.3 用户登出

<div align="left">
  <p><strong>表4.3 用户登出RUCM表</strong></p>
</div>

<table><tbody>
        <tr >
            <td>作者：刘桢炜</td>
            <td>日期：2023年3月22日</td>
            <td>版本：1.1.2
        </tr>
        <tr>
            <td>用例名</td>
            <td colspan="2">用户登出</td>
        </tr>
        <tr>
            <td>用例ID</td>
            <td colspan="2">A03</td>
        </tr>
        <tr>
            <td>简要描述</td>
            <td colspan="2">用户通过登出变为游客</td>
        </tr>
        <tr>
            <td>参与者</td>
            <td colspan="2">用户</td>
        </tr>
        <tr>
            <td>涉众</td>
            <td colspan="2">无</td>
        </tr>
        <tr>
            <td>相关用例</td>
            <td colspan="2">无</td>
        </tr>
        <tr>
            <td>前置条件</td>
            <td colspan="2">该用户已登录</td>
        </tr>
        <tr>
            <td>后置条件</td>
            <td colspan="2">用户通过登出变为游客</td>
        </tr>
        <tr>
            <td colspan="3">基本事件流 <br>
            <ol> 
                <li>用户在导航栏中点击用户头像</li>
                <li>在展开页中点击“登出”按钮</li>
                <li>系统验证信息</li>
                <li>信息验证通过后，用户登出变为游客</li>
            </ol>
        </td>
    </tr>
    <tr>
        <td colspan="3">备选事件流 <br>
        无</td>
    </tr>
    <tr>
        <td colspan="3">补充约束 <br>
            无</td>
    </tr>
    <tr>
        <td colspan="3">待解决问题 <br>
        无 </td>
    </tr>
    </tbody>
</table>

#### 4.1.4 修改密码

<div align="left">
  <p><strong>表4.4 修改密码RUCM表</strong></p>
</div>

<table><tbody>
        <tr >
            <td>作者：刘桢炜</td>
            <td>日期：2023年3月6日</td>
            <td>版本：1.0.0
        </tr>
        <tr>
            <td>用例名</td>
            <td colspan="2">修改密码</td>
        </tr>
        <tr>
            <td>用例ID</td>
            <td colspan="2">A04</td>
        </tr>
        <tr>
            <td>简要描述</td>
            <td colspan="2">用户修改个人登录密码</td>
        </tr>
        <tr>
            <td>参与者</td>
            <td colspan="2">用户</td>
        </tr>
        <tr>
            <td>涉众</td>
            <td colspan="2">无</td>
        </tr>
        <tr>
            <td>相关用例</td>
            <td colspan="2">无</td>
        </tr>
        <tr>
            <td>前置条件</td>
            <td colspan="2">用户已登录</td>
        </tr>
        <tr>
            <td>后置条件</td>
            <td colspan="2">数据库中用户密码被修改</td>
        </tr>
        <tr>
            <td colspan="3">基本事件流 <br>
            <ol> 
                <li>用户在导航栏中点击用户头像</li>
                <li>在展开页中点击“修改密码”按钮</li>
                <li>系统跳转至修改密码页</li>
                <li>用户填写原密码，并填写新密码与确认新密码信息，点击确认修改按钮</li>
                <li>系统验证信息</li>
                <li>验证通过后，显示密码成功修改</li>
            </ol>
        </td>
    </tr>
    <tr>
        <td colspan="3">备选事件流 <br>
        	<ol>
                <li>原密码填写错误，显示“原密码错误”错误信息</li>
                <li>新密码与原密码一致，显示“新密码与原密码一致”错误信息</li>
                <li>新密码与确认新密码不一致，显示“新密码与确认新密码不一致”错误信息</li>
            </ol>
        </td>
    </tr>
    <tr>
    <tr>
        <td colspan="3">补充约束 <br>
            无</td>
    </tr>
    <tr>
        <td colspan="3">待解决问题 <br>
        无 </td>
    </tr>
    </tbody>
</table>

#### 4.1.5 找回密码

<div align="left">
  <p><strong>表4.5 找回密码RUCM表</strong></p>
</div>

<table><tbody>
        <tr >
            <td>作者：刘桢炜</td>
            <td>日期：2023年3月6日</td>
            <td>版本：1.0.0
        </tr>
        <tr>
            <td>用例名</td>
            <td colspan="2">找回密码</td>
        </tr>
        <tr>
            <td>用例ID</td>
            <td colspan="2">A05</td>
        </tr>
        <tr>
            <td>简要描述</td>
            <td colspan="2">用户找回个人登录密码</td>
        </tr>
        <tr>
            <td>参与者</td>
            <td colspan="2">用户</td>
        </tr>
        <tr>
            <td>涉众</td>
            <td colspan="2">无</td>
        </tr>
        <tr>
            <td>相关用例</td>
            <td colspan="2">无</td>
        </tr>
        <tr>
            <td>前置条件</td>
            <td colspan="2">用户未登录</td>
        </tr>
        <tr>
            <td>后置条件</td>
            <td colspan="2">数据库中用户密码被修改</td>
        </tr>
        <tr>
            <td colspan="3">基本事件流 <br>
            <ol> 
                <li>用户在登录页面点击“忘记密码”按钮</li>
                <li>系统进入忘记密码页</li>
                <li>用户填写注册时使用的邮箱，新密码与确认新密码，点击“验证”按钮</li>
                <li>系统发送验证码至邮箱</li>
                <li>用户填写邮箱中接受的验证码，点击“确认修改”按钮</li>
                <li>系统验证</li>
                <li>验证通过后，数据库中更改用户密码，用户进入主页</li>
            </ol>
        </td>
    </tr>
    <tr>
        <td colspan="3">备选事件流 <br>
        	<ol>
                <li>邮箱、密码、确认密码有漏填，显示"信息不完整"</li>
                <li>邮箱不存在，显示“邮箱不存在”</li>
                <li>验证码填写错误，显示“验证码错误”错误信息</li>
                <li>新密码与确认新密码不一致，显示“新密码与确认新密码不一致”错误信息</li>
            </ol>
        </td>
    </tr>
    <tr>
    <tr>
        <td colspan="3">补充约束 <br>
            无</td>
    </tr>
    <tr>
        <td colspan="3">待解决问题 <br>
        无 </td>
    </tr>
    </tbody>
</table>

![需求分析A05](imgs/需求分析A05.png)

<div align="center">
  <p><strong>图4.3 找回密码活动图</strong></p>
</div>

#### 4.1.6 查看个人主页

<div align="left">
  <p><strong>表4.6 查看个人主页RUCM表</strong></p>
</div>

<table><tbody>
        <tr >
            <td>作者：刘桢炜</td>
            <td>日期：2023年3月6日</td>
            <td>版本：1.0.0
        </tr>
        <tr>
            <td>用例名</td>
            <td colspan="2">查看个人主页</td>
        </tr>
        <tr>
            <td>用例ID</td>
            <td colspan="2">A06</td>
        </tr>
        <tr>
            <td>简要描述</td>
            <td colspan="2">用户查看个人主页</td>
        </tr>
        <tr>
            <td>参与者</td>
            <td colspan="2">用户</td>
        </tr>
        <tr>
            <td>涉众</td>
            <td colspan="2">无</td>
        </tr>
        <tr>
            <td>相关用例</td>
            <td colspan="2">无</td>
        </tr>
        <tr>
            <td>前置条件</td>
            <td colspan="2">用户已登录</td>
        </tr>
        <tr>
            <td>后置条件</td>
            <td colspan="2">用户进入个人主页</td>
        </tr>
        <tr>
            <td colspan="3">基本事件流 <br>
            <ol> 
                <li>用户在导航栏点击个人头像</li>
                <li>用户在展开页点击“个人主页”按钮</li>
                <li>系统切换至个人主页页</li>
            </ol>
        </td>
    </tr>
    <tr>
        <td colspan="3">备选事件流 <br>
        无</td>
    </tr>
    <tr>
    <tr>
        <td colspan="3">补充约束 <br>
            无</td>
    </tr>
    <tr>
        <td colspan="3">待解决问题 <br>
        无 </td>
    </tr>
    </tbody>
</table>

#### 4.1.7 查看其它用户主页

<div align="left">
  <p><strong>表4.7 查看其他用户主页RUCM表</strong></p>
</div>

<table><tbody>
        <tr >
            <td>作者：刘桢炜</td>
            <td>日期：2023年3月6日</td>
            <td>版本：1.0.0
        </tr>
        <tr>
            <td>用例名</td>
            <td colspan="2">查看其它用户主页</td>
        </tr>
        <tr>
            <td>用例ID</td>
            <td colspan="2">A07</td>
        </tr>
        <tr>
            <td>简要描述</td>
            <td colspan="2">查看其它用户主页</td>
        </tr>
        <tr>
            <td>参与者</td>
            <td colspan="2">用户</td>
        </tr>
        <tr>
            <td>涉众</td>
            <td colspan="2">无</td>
        </tr>
        <tr>
            <td>相关用例</td>
            <td colspan="2">无</td>
        </tr>
        <tr>
            <td>前置条件</td>
            <td colspan="2">无</td>
        </tr>
        <tr>
            <td>后置条件</td>
            <td colspan="2">前端进入用户主页页</td>
        </tr>
        <tr>
            <td colspan="3">基本事件流 <br>
            <ol> 
                <li>点击其它用户头像或用户名</li>
                <li>在弹出页点击“主页”按钮</li>
                <li>系统跳转至该用户个人主页</li>
            </ol>
        </td>
    </tr>
    <tr>
        <td colspan="3">备选事件流 <br>
        无</td>
    </tr>
    <tr>
    <tr>
        <td colspan="3">补充约束 <br>
            无</td>
    </tr>
    <tr>
        <td colspan="3">待解决问题 <br>
        无 </td>
    </tr>
    </tbody>
</table>

#### 4.1.8 查看用户上传作品

<div align="left">
  <p><strong>表4.8 查看用户上传作品RUCM表</strong></p>
</div>

<table><tbody>
        <tr >
            <td>作者：刘桢炜</td>
            <td>日期：2023年3月6日</td>
            <td>版本：1.0.0
        </tr>
        <tr>
            <td>用例名</td>
            <td colspan="2">查看用户上传作品</td>
        </tr>
        <tr>
            <td>用例ID</td>
            <td colspan="2">A08</td>
        </tr>
        <tr>
            <td>简要描述</td>
            <td colspan="2">查看用户上传作品</td>
        </tr>
        <tr>
            <td>参与者</td>
            <td colspan="2">用户</td>
        </tr>
        <tr>
            <td>涉众</td>
            <td colspan="2">无</td>
        </tr>
        <tr>
            <td>相关用例</td>
            <td colspan="2">无</td>
        </tr>
        <tr>
            <td>前置条件</td>
            <td colspan="2">无</td>
        </tr>
        <tr>
            <td>后置条件</td>
            <td colspan="2">前端展示用户上传作品</td>
        </tr>
        <tr>
            <td colspan="3">基本事件流 <br>
            <ol> 
                <li>在用户主页点击“上传作品栏”中的“更多”选项</li>
                <li>系统跳转至该用户上传作品页</li>
            </ol>
        </td>
    </tr>
    <tr>
        <td colspan="3">备选事件流 <br>
        无</td>
    </tr>
    <tr>
    <tr>
        <td colspan="3">补充约束 <br>
            无</td>
    </tr>
    <tr>
        <td colspan="3">待解决问题 <br>
        无 </td>
    </tr>
    </tbody>
</table>

#### 4.1.9 查看个人收藏夹

<div align="left">
  <p><strong>表4.9 查看个人收藏夹RUCM表</strong></p>
</div>

<table><tbody>
        <tr >
            <td>作者：刘桢炜</td>
            <td>日期：2023年3月6日</td>
            <td>版本：1.0.0
        </tr>
        <tr>
            <td>用例名</td>
            <td colspan="2">查看个人收藏夹</td>
        </tr>
        <tr>
            <td>用例ID</td>
            <td colspan="2">A09</td>
        </tr>
        <tr>
            <td>简要描述</td>
            <td colspan="2">查看个人收藏夹</td>
        </tr>
        <tr>
            <td>参与者</td>
            <td colspan="2">用户</td>
        </tr>
        <tr>
            <td>涉众</td>
            <td colspan="2">无</td>
        </tr>
        <tr>
            <td>相关用例</td>
            <td colspan="2">无</td>
        </tr>
        <tr>
            <td>前置条件</td>
            <td colspan="2">用户已登录</td>
        </tr>
        <tr>
            <td>后置条件</td>
            <td colspan="2">前端展示用户收藏夹</td>
        </tr>
        <tr>
            <td colspan="3">基本事件流 <br>
            <ol> 
                <li>在个人主页点击“收藏夹”中的“更多”选项</li>
                <li>系统跳转至该用户收藏夹，且展示private与public两种收藏内容</li>
            </ol>
        </td>
    </tr>
    <tr>
        <td colspan="3">备选事件流 <br>
        无</td>
    </tr>
    <tr>
    <tr>
        <td colspan="3">补充约束 <br>
            无</td>
    </tr>
    <tr>
        <td colspan="3">待解决问题 <br>
        无 </td>
    </tr>
    </tbody>
</table>

#### 4.1.10 查看其它用户收藏夹

<div align="left">
  <p><strong>表4.10 查看其它用户收藏夹RUCM表</strong></p>
</div>

<table><tbody>
        <tr >
            <td>作者：刘桢炜</td>
            <td>日期：2023年3月6日</td>
            <td>版本：1.0.0
        </tr>
        <tr>
            <td>用例名</td>
            <td colspan="2">查看其它用户收藏夹</td>
        </tr>
        <tr>
            <td>用例ID</td>
            <td colspan="2">A10</td>
        </tr>
        <tr>
            <td>简要描述</td>
            <td colspan="2">查看其他用户收藏夹</td>
        </tr>
        <tr>
            <td>参与者</td>
            <td colspan="2">用户</td>
        </tr>
        <tr>
            <td>涉众</td>
            <td colspan="2">无</td>
        </tr>
        <tr>
            <td>相关用例</td>
            <td colspan="2">无</td>
        </tr>
        <tr>
            <td>前置条件</td>
            <td colspan="2">无</td>
        </tr>
        <tr>
            <td>后置条件</td>
            <td colspan="2">前端展示用户收藏夹</td>
        </tr>
        <tr>
            <td colspan="3">基本事件流 <br>
            <ol> 
                <li>在用户主页点击“收藏夹”中的“更多”选项</li>
                <li>系统跳转至该用户收藏夹，且只展示public收藏内容</li>
            </ol>
        </td>
    </tr>
    <tr>
        <td colspan="3">备选事件流 <br>
        无</td>
    </tr>
    <tr>
    <tr>
        <td colspan="3">补充约束 <br>
            无</td>
    </tr>
    <tr>
        <td colspan="3">待解决问题 <br>
        无 </td>
    </tr>
    </tbody>
</table>

#### 4.1.11 查看个人浏览历史

<div align="left">
  <p><strong>表4.11 查看个人浏览历史RUCM表</strong></p>
</div>

<table><tbody>
        <tr >
            <td>作者：刘桢炜</td>
            <td>日期：2023年3月6日</td>
            <td>版本：1.0.0
        </tr>
        <tr>
            <td>用例名</td>
            <td colspan="2">查看个人浏览历史</td>
        </tr>
        <tr>
            <td>用例ID</td>
            <td colspan="2">A11</td>
        </tr>
        <tr>
            <td>简要描述</td>
            <td colspan="2">查看个人浏览历史</td>
        </tr>
        <tr>
            <td>参与者</td>
            <td colspan="2">用户</td>
        </tr>
        <tr>
            <td>涉众</td>
            <td colspan="2">无</td>
        </tr>
        <tr>
            <td>相关用例</td>
            <td colspan="2">无</td>
        </tr>
        <tr>
            <td>前置条件</td>
            <td colspan="2">用户已登录</td>
        </tr>
        <tr>
            <td>后置条件</td>
            <td colspan="2">前端展示用户个人浏览历史</td>
        </tr>
        <tr>
            <td colspan="3">基本事件流 <br>
            <ol> 
                <li>在个人主页点击“浏览历史”栏的“更多”按钮</li>
                <li>系统跳转至该用户浏览历史页</li>
            </ol>
        </td>
    </tr>
    <tr>
        <td colspan="3">备选事件流 <br>
        无</td>
    </tr>
    <tr>
    <tr>
        <td colspan="3">补充约束 <br>
            无</td>
    </tr>
    <tr>
        <td colspan="3">待解决问题 <br>
        无 </td>
    </tr>
    </tbody>
</table>

#### 4.1.12 查看用户关注列表

<div align="left">
  <p><strong>表4.12 查看用户关注列表RUCM表</strong></p>
</div>

<table><tbody>
        <tr >
            <td>作者：刘桢炜</td>
            <td>日期：2023年3月6日</td>
            <td>版本：1.0.0
        </tr>
        <tr>
            <td>用例名</td>
            <td colspan="2">查看用户关注列表</td>
        </tr>
        <tr>
            <td>用例ID</td>
            <td colspan="2">A12</td>
        </tr>
        <tr>
            <td>简要描述</td>
            <td colspan="2">查看用户关注列表</td>
        </tr>
        <tr>
            <td>参与者</td>
            <td colspan="2">用户</td>
        </tr>
        <tr>
            <td>涉众</td>
            <td colspan="2">无</td>
        </tr>
        <tr>
            <td>相关用例</td>
            <td colspan="2">无</td>
        </tr>
        <tr>
            <td>前置条件</td>
            <td colspan="2">无</td>
        </tr>
        <tr>
            <td>后置条件</td>
            <td colspan="2">前端展示用户关注列表</td>
        </tr>
        <tr>
            <td colspan="3">基本事件流 <br>
            <ol> 
                <li>在用户主页点击“following”选项</li>
                <li>系统展示用户关注列表</li>
            </ol>
        </td>
    </tr>
    <tr>
        <td colspan="3">备选事件流 <br>
        无</td>
    </tr>
    <tr>
    <tr>
        <td colspan="3">补充约束 <br>
            无</td>
    </tr>
    <tr>
        <td colspan="3">待解决问题 <br>
        无 </td>
    </tr>
    </tbody>
</table>

#### 4.1.13 查看用户粉丝列表

<div align="left">
  <p><strong>表4.13 查看用户粉丝列表RUCM表</strong></p>
</div>

<table><tbody>
        <tr >
            <td>作者：刘桢炜</td>
            <td>日期：2023年3月6日</td>
            <td>版本：1.0.0
        </tr>
        <tr>
            <td>用例名</td>
            <td colspan="2">查看用户粉丝列表</td>
        </tr>
        <tr>
            <td>用例ID</td>
            <td colspan="2">A13</td>
        </tr>
        <tr>
            <td>简要描述</td>
            <td colspan="2">查看用户粉丝列表</td>
        </tr>
        <tr>
            <td>参与者</td>
            <td colspan="2">用户</td>
        </tr>
        <tr>
            <td>涉众</td>
            <td colspan="2">无</td>
        </tr>
        <tr>
            <td>相关用例</td>
            <td colspan="2">无</td>
        </tr>
        <tr>
            <td>前置条件</td>
            <td colspan="2">无</td>
        </tr>
        <tr>
            <td>后置条件</td>
            <td colspan="2">前端展示用户粉丝列表</td>
        </tr>
        <tr>
            <td colspan="3">基本事件流 <br>
            <ol> 
                <li>在用户主页点击“follower”选项</li>
                <li>系统展示用户粉丝列表</li>
            </ol>
        </td>
    </tr>
    <tr>
        <td colspan="3">备选事件流 <br>
        无</td>
    </tr>
    <tr>
    <tr>
        <td colspan="3">补充约束 <br>
            无</td>
    </tr>
    <tr>
        <td colspan="3">待解决问题 <br>
        无 </td>
    </tr>
    </tbody>
</table>

#### 4.1.14 关注用户

<div align="left">
  <p><strong>表4.14 关注用户RUCM表</strong></p>
</div>

<table><tbody>
        <tr >
            <td>作者：刘桢炜</td>
            <td>日期：2023年3月6日</td>
            <td>版本：1.0.0
        </tr>
        <tr>
            <td>用例名</td>
            <td colspan="2">关注用户</td>
        </tr>
        <tr>
            <td>用例ID</td>
            <td colspan="2">A14</td>
        </tr>
        <tr>
            <td>简要描述</td>
            <td colspan="2">关注用户</td>
        </tr>
        <tr>
            <td>参与者</td>
            <td colspan="2">用户</td>
        </tr>
        <tr>
            <td>涉众</td>
            <td colspan="2">用户</td>
        </tr>
        <tr>
            <td>相关用例</td>
            <td colspan="2">A15取消关注用户</td>
        </tr>
        <tr>
            <td>前置条件</td>
            <td colspan="2">
            	<ol>
                	<li>用户已登录</li>
                    <li>数据库中不存在关注的记录</li>
                </ol>
            </td>
        </tr>
        <tr>
            <td>后置条件</td>
            <td colspan="2">数据库中新添用户关注记录，刷新前端，该用户显示为已关注</td>
        </tr>
        <tr>
            <td colspan="3">基本事件流<br>
            <ol> 
                <li>在用户主页点击“关注按钮”/或点击用户头像，在弹出页点击“关注”按钮</li>
                <li>数据库中新添用户关注记录，刷新前端，该用户显示为已关注</li>
                <li>提示被关注用户有新增粉丝</li>
            </ol>
        </td>
    </tr>
    <tr>
        <td colspan="3">备选事件流 <br>
        无</td>
    </tr>
    <tr>
    <tr>
        <td colspan="3">补充约束 <br>
            无</td>
    </tr>
    <tr>
        <td colspan="3">待解决问题 <br>
        无 </td>
    </tr>
    </tbody>
</table>

#### 4.1.15 取消关注用户

<div align="left">
  <p><strong>表4.15 取消关注用户RUCM表</strong></p>
</div>

<table><tbody>
        <tr >
            <td>作者：刘桢炜</td>
            <td>日期：2023年3月6日</td>
            <td>版本：1.0.0
        </tr>
        <tr>
            <td>用例名</td>
            <td colspan="2">取消关注用户</td>
        </tr>
        <tr>
            <td>用例ID</td>
            <td colspan="2">A15</td>
        </tr>
        <tr>
            <td>简要描述</td>
            <td colspan="2">取消关注用户</td>
        </tr>
        <tr>
            <td>参与者</td>
            <td colspan="2">用户</td>
        </tr>
        <tr>
            <td>涉众</td>
            <td colspan="2">用户</td>
        </tr>
        <tr>
            <td>相关用例</td>
            <td colspan="2">A14 关注用户</td>
        </tr>
        <tr>
            <td>前置条件</td>
            <td colspan="2">
            	<ol>
                	<li>用户已登录</li>
                    <li>数据库中存在关注的记录</li>
                </ol>
            </td>
        </tr>
        <tr>
            <td>后置条件</td>
            <td colspan="2">数据库中删除用户关注记录，刷新前端，该用户显示为未关注</td>
        </tr>
        <tr>
            <td colspan="3">基本事件流<br>
            <ol> 
                <li>
                    <p>
                        在用户主页点击“取消关注按钮”
                    </p>
                    <p>或点击用户头像，在弹出页点击“取消关注”按钮</p>
                    <p>或在个人关注列表对应用户栏中点击“取消关注”按钮</p>
                </li>
                <li>数据库中删除用户关注记录，刷新前端，该用户显示为未关注</li>
            </ol>
        </td>
    </tr>
    <tr>
        <td colspan="3">备选事件流 <br>
        无</td>
    </tr>
    <tr>
    <tr>
        <td colspan="3">补充约束 <br>
            无</td>
    </tr>
    <tr>
        <td colspan="3">待解决问题 <br>
        无 </td>
    </tr>
    </tbody>
</table>

#### 4.1.16 修改个人头像

<div align="left">
  <p><strong>表4.16 修改个人头像RUCM表</strong></p>
</div>

<table><tbody>
        <tr >
            <td>作者：刘桢炜</td>
            <td>日期：2023年3月6日</td>
            <td>版本：1.0.0
        </tr>
        <tr>
            <td>用例名</td>
            <td colspan="2">修改个人头像</td>
        </tr>
        <tr>
            <td>用例ID</td>
            <td colspan="2">A16</td>
        </tr>
        <tr>
            <td>简要描述</td>
            <td colspan="2">用户修改个人头像</td>
        </tr>
        <tr>
            <td>参与者</td>
            <td colspan="2">用户</td>
        </tr>
        <tr>
            <td>涉众</td>
            <td colspan="2">无</td>
        </tr>
        <tr>
            <td>相关用例</td>
            <td colspan="2">无</td>
        </tr>
        <tr>
            <td>前置条件</td>
            <td colspan="2">用户已登录</td>
        </tr>
        <tr>
            <td>后置条件</td>
            <td colspan="2">数据库中用户头像被修改</td>
        </tr>
        <tr>
            <td colspan="3">基本事件流 <br>
            <ol> 
                <li>用户在个人主页中点击“修改个人信息”选项</li>
                <li>在修改个人信息页上传新的头像，点击“确认”</li>
                <li>数据库中修改头像，刷新前端，显示新头像</li>
            </ol>
        </td>
    </tr>
    <tr>
        <td colspan="3">备选事件流 <br>
        	无
        </td>
    </tr>
    <tr>
    <tr>
        <td colspan="3">补充约束 <br>
            无</td>
    </tr>
    <tr>
        <td colspan="3">待解决问题 <br>
        无 </td>
    </tr>
    </tbody>
</table>

#### 4.1.17 修改个人用户名

<div align="left">
  <p><strong>表4.17 修改个人用户名RUCM表</strong></p>
</div>

<table><tbody>
        <tr >
            <td>作者：刘桢炜</td>
            <td>日期：2023年3月6日</td>
            <td>版本：1.0.0
        </tr>
        <tr>
            <td>用例名</td>
            <td colspan="2">修改个人用户名</td>
        </tr>
        <tr>
            <td>用例ID</td>
            <td colspan="2">A17</td>
        </tr>
        <tr>
            <td>简要描述</td>
            <td colspan="2">用户修改个人用户名</td>
        </tr>
        <tr>
            <td>参与者</td>
            <td colspan="2">用户</td>
        </tr>
        <tr>
            <td>涉众</td>
            <td colspan="2">无</td>
        </tr>
        <tr>
            <td>相关用例</td>
            <td colspan="2">无</td>
        </tr>
        <tr>
            <td>前置条件</td>
            <td colspan="2">用户已登录</td>
        </tr>
        <tr>
            <td>后置条件</td>
            <td colspan="2">数据库中用户用户名被修改</td>
        </tr>
        <tr>
            <td colspan="3">基本事件流 <br>
            <ol> 
                <li>用户在个人主页中点击“修改个人信息”选项</li>
                <li>在修改个人信息页填写新的用户名，点击“确认”</li>
                <li>数据库中修改用户名，刷新前端，显示新用户名</li>
            </ol>
        </td>
    </tr>
    <tr>
        <td colspan="3">备选事件流 <br>
        	<ol>
                <li>用户名重复，提示“用户名已被使用”错误信息</li>
            </ol>
        </td>
    </tr>
    <tr>
    <tr>
        <td colspan="3">补充约束 <br>
            无</td>
    </tr>
    <tr>
        <td colspan="3">待解决问题 <br>
        无 </td>
    </tr>
    </tbody>
</table>

### 4.2 管理员系统

#### 4.2.1 管理员登录

<div align="left">
  <p><strong>表4.18 管理员登录RUCM表</strong></p>
</div>

<table><tbody>
        <tr >
            <td>作者：刘桢炜</td>
            <td>日期：2023年3月22日</td>
            <td>版本：1.1.2
        </tr>
        <tr>
            <td>用例名</td>
            <td colspan="2">管理员登录</td>
        </tr>
        <tr>
            <td>用例ID</td>
            <td colspan="2">B01</td>
        </tr>
        <tr>
            <td>简要描述</td>
            <td colspan="2">通过登录成为管理员</td>
        </tr>
        <tr>
            <td>参与者</td>
            <td colspan="2">游客</td>
        </tr>
        <tr>
            <td>涉众</td>
            <td colspan="2">管理员</td>
        </tr>
        <tr>
            <td>相关用例</td>
            <td colspan="2">管理员登出A02</td>
        </tr>
        <tr>
            <td>前置条件</td>
            <td colspan="2">该管理员未登录</td>
        </tr>
        <tr>
            <td>后置条件</td>
            <td colspan="2">游客通过登录成为管理员</td>
        </tr>
        <tr>
            <td colspan="3">基本事件流 <br>
            <ol> 
                <li>游客在首页点击登录进入登录界面</li>
                <li>游客输入账号名，密码后，点击“登录”按钮</li>
                <li>系统验证信息</li>
                <li>信息验证通过后，进入初始页面</li>
            </ol>
        </td>
    </tr>
    <tr>
        <td colspan="3">备选事件流 <br>
        	<ol>
                <li>账号或密码错误，显示“账户或密码错误”</li>
            </ol>
        </td>
    </tr>
    <tr>
        <td colspan="3">补充约束 <br>
            无</td>
    </tr>
    <tr>
        <td colspan="3">待解决问题 <br>
        无 </td>
    </tr>
    </tbody>
</table>

#### 4.2.2 管理员登出

<div align="left">
  <p><strong>表4.19 管理员登出RUCM表</strong></p>
</div>

<table><tbody>
        <tr >
            <td>作者：刘桢炜</td>
            <td>日期：2023年3月6日</td>
            <td>版本：1.0.0
        </tr>
        <tr>
            <td>用例名</td>
            <td colspan="2">管理员登出</td>
        </tr>
        <tr>
            <td>用例ID</td>
            <td colspan="2">B02</td>
        </tr>
        <tr>
            <td>简要描述</td>
            <td colspan="2">管理员登出</td>
        </tr>
        <tr>
            <td>参与者</td>
            <td colspan="2">管理员</td>
        </tr>
        <tr>
            <td>涉众</td>
            <td colspan="2">管理员</td>
        </tr>
        <tr>
            <td>相关用例</td>
            <td colspan="2">无</td>
        </tr>
        <tr>
            <td>前置条件</td>
            <td colspan="2">该管理员已登录</td>
        </tr>
        <tr>
            <td>后置条件</td>
            <td colspan="2">管理员登出</td>
        </tr>
        <tr>
            <td colspan="3">基本事件流 <br>
            <ol> 
                <li>管理员在导航栏中点击用户头像</li>
                <li>在展开页中点击“登出”按钮</li>
                <li>系统验证信息</li>
                <li>信息验证通过后，管理员登出</li>
            </ol>
        </td>
    </tr>
    <tr>
        <td colspan="3">备选事件流 <br>
        无</td>
    </tr>
    <tr>
        <td colspan="3">补充约束 <br>
            无</td>
    </tr>
    <tr>
        <td colspan="3">待解决问题 <br>
        无 </td>
    </tr>
    </tbody>
</table>

#### 4.2.3 查看用户列表

<div align="left">
  <p><strong>表4.20 查看用户列表RUCM表</strong></p>
</div>

<table><tbody>
        <tr >
            <td>作者：刘桢炜</td>
            <td>日期：2023年3月6日</td>
            <td>版本：1.0.0
        </tr>
        <tr>
            <td>用例名</td>
            <td colspan="2">查看用户列表</td>
        </tr>
        <tr>
            <td>用例ID</td>
            <td colspan="2">B03</td>
        </tr>
        <tr>
            <td>简要描述</td>
            <td colspan="2">管理员查看用户列表</td>
        </tr>
        <tr>
            <td>参与者</td>
            <td colspan="2">管理员</td>
        </tr>
        <tr>
            <td>涉众</td>
            <td colspan="2">无</td>
        </tr>
        <tr>
            <td>相关用例</td>
            <td colspan="2">无</td>
        </tr>
        <tr>
            <td>前置条件</td>
            <td colspan="2">该管理员已登录</td>
        </tr>
        <tr>
            <td>后置条件</td>
            <td colspan="2">系统显示用户列表</td>
        </tr>
        <tr>
            <td colspan="3">基本事件流 <br>
            <ol> 
                <li>管理员在主页中点击“管理用户”按钮</li>
                <li>系统跳转至用户列表页</li>
            </ol>
        </td>
    </tr>
    <tr>
        <td colspan="3">备选事件流 <br>
        无</td>
    </tr>
    <tr>
        <td colspan="3">补充约束 <br>
            无</td>
    </tr>
    <tr>
        <td colspan="3">待解决问题 <br>
        无 </td>
    </tr>
    </tbody>
</table>

#### 4.2.4 查看作品列表

<div align="left">
  <p><strong>表4.21 查看作品列表RUCM表</strong></p>
</div>

<table><tbody>
        <tr >
            <td>作者：刘桢炜</td>
            <td>日期：2023年3月6日</td>
            <td>版本：1.0.0
        </tr>
        <tr>
            <td>用例名</td>
            <td colspan="2">查看作品列表</td>
        </tr>
        <tr>
            <td>用例ID</td>
            <td colspan="2">B04</td>
        </tr>
        <tr>
            <td>简要描述</td>
            <td colspan="2">管理员查看作品列表</td>
        </tr>
        <tr>
            <td>参与者</td>
            <td colspan="2">管理员</td>
        </tr>
        <tr>
            <td>涉众</td>
            <td colspan="2">无</td>
        </tr>
        <tr>
            <td>相关用例</td>
            <td colspan="2">无</td>
        </tr>
        <tr>
            <td>前置条件</td>
            <td colspan="2">该管理员已登录</td>
        </tr>
        <tr>
            <td>后置条件</td>
            <td colspan="2">系统显示作品列表</td>
        </tr>
        <tr>
            <td colspan="3">基本事件流 <br>
            <ol> 
                <li>管理员在主页中点击“管理作品”按钮</li>
                <li>系统跳转至用户列表页</li>
            </ol>
        </td>
    </tr>
    <tr>
        <td colspan="3">备选事件流 <br>
        无</td>
    </tr>
    <tr>
        <td colspan="3">补充约束 <br>
            无</td>
    </tr>
    <tr>
        <td colspan="3">待解决问题 <br>
        无 </td>
    </tr>
    </tbody>
</table>

#### 4.2.5 审核上传作品

<div align="left">
  <p><strong>表4.22 审核上传作品RUCM表</strong></p>
</div>

<table><tbody>
        <tr >
            <td>作者：刘桢炜</td>
            <td>日期：2023年3月6日</td>
            <td>版本：1.0.0
        </tr>
        <tr>
            <td>用例名</td>
            <td colspan="2">审核上传作品</td>
        </tr>
        <tr>
            <td>用例ID</td>
            <td colspan="2">B05</td>
        </tr>
        <tr>
            <td>简要描述</td>
            <td colspan="2">管理员审核上传作品</td>
        </tr>
        <tr>
            <td>参与者</td>
            <td colspan="2">管理员</td>
        </tr>
        <tr>
            <td>涉众</td>
            <td colspan="2">用户</td>
        </tr>
        <tr>
            <td>相关用例</td>
            <td colspan="2">无</td>
        </tr>
        <tr>
            <td>前置条件</td>
            <td colspan="2">该管理员已登录</td>
        </tr>
        <tr>
            <td>后置条件</td>
            <td colspan="2">作品被标记为审核通过或不通过</td>
        </tr>
        <tr>
            <td colspan="3">基本事件流 <br>
            <ol> 
                <li>管理员在主页中点击“待审核列表”按钮</li>
                <li>系统跳转至待审核列表页</li>
                <li>管理员对任意作品选择审核通过或不通过</li>
                <li>系统通知用户上传作品的审核状态</li>
                <li>审核不通过的作品，用户可以选择取消上传，或者修改后重新上传</li>
                <li>重新上传的作品重新加入待审核队列</li>
            </ol>
        </td>
    </tr>
    <tr>
        <td colspan="3">备选事件流 <br>
        无</td>
    </tr>
    <tr>
        <td colspan="3">补充约束 <br>
            无</td>
    </tr>
    <tr>
        <td colspan="3">待解决问题 <br>
        无 </td>
    </tr>
    </tbody>
</table>

![需求分析B05](imgs/需求分析B05.png)

<div align="center">
  <p><strong>图4.4 审核上传作品活动图</strong></p>
</div>

#### 4.2.6 管理员查看评论

<div align="left">
  <p><strong>表4.23 管理员查看评论RUCM表</strong></p>
</div>

<table><tbody>
        <tr >
            <td>作者：刘桢炜</td>
            <td>日期：2023年3月6日</td>
            <td>版本：1.1.0
        </tr>
        <tr>
            <td>用例名</td>
            <td colspan="2">管理员查看评论</td>
        </tr>
        <tr>
            <td>用例ID</td>
            <td colspan="2">B06</td>
        </tr>
        <tr>
            <td>简要描述</td>
            <td colspan="2">管理员查看评论</td>
        </tr>
        <tr>
            <td>参与者</td>
            <td colspan="2">管理员</td>
        </tr>
        <tr>
            <td>涉众</td>
            <td colspan="2">无</td>
        </tr>
        <tr>
            <td>相关用例</td>
            <td colspan="2">无</td>
        </tr>
        <tr>
            <td>前置条件</td>
            <td colspan="2">该管理员已登录</td>
        </tr>
        <tr>
            <td>后置条件</td>
            <td colspan="2">无</td>
        </tr>
        <tr>
            <td colspan="3">基本事件流 <br>
            <ol> 
                <li>管理员在主页中点击作品</li>
                <li>系统跳转至作品详情页</li>
                <li>管理员在作品详情页查看评论</li>
            </ol>
        </td>
    </tr>
    <tr>
        <td colspan="3">备选事件流 <br>
        无</td>
    </tr>
    <tr>
        <td colspan="3">补充约束 <br>
            无</td>
    </tr>
    <tr>
        <td colspan="3">待解决问题 <br>
        无 </td>
    </tr>
    </tbody>
</table>

#### 4.2.7 管理员查看回复

<div align="left">
  <p><strong>表4.24 管理员查看回复RUCM表</strong></p>
</div>

<table><tbody>
        <tr >
            <td>作者：刘桢炜</td>
            <td>日期：2023年3月6日</td>
            <td>版本：1.1.0
        </tr>
        <tr>
            <td>用例名</td>
            <td colspan="2">管理员查看回复</td>
        </tr>
        <tr>
            <td>用例ID</td>
            <td colspan="2">B07</td>
        </tr>
        <tr>
            <td>简要描述</td>
            <td colspan="2">管理员查看回复</td>
        </tr>
        <tr>
            <td>参与者</td>
            <td colspan="2">管理员</td>
        </tr>
        <tr>
            <td>涉众</td>
            <td colspan="2">无</td>
        </tr>
        <tr>
            <td>相关用例</td>
            <td colspan="2">无</td>
        </tr>
        <tr>
            <td>前置条件</td>
            <td colspan="2">该管理员已登录</td>
        </tr>
        <tr>
            <td>后置条件</td>
            <td colspan="2">无</td>
        </tr>
        <tr>
            <td colspan="3">基本事件流 <br>
            <ol> 
                <li>管理员在主页中点击作品</li>
                <li>系统跳转至作品详情页</li>
                <li>管理员在作品详情页查看回复</li>
            </ol>
        </td>
    </tr>
    <tr>
        <td colspan="3">备选事件流 <br>
        无</td>
    </tr>
    <tr>
        <td colspan="3">补充约束 <br>
            无</td>
    </tr>
    <tr>
        <td colspan="3">待解决问题 <br>
        无 </td>
    </tr>
    </tbody>
</table>

#### 4.2.8 管理员删除评论

<div align="left">
  <p><strong>表4.25 管理员删除评论RUCM表</strong></p>
</div>

<table><tbody>
        <tr >
            <td>作者：刘桢炜</td>
            <td>日期：2023年3月6日</td>
            <td>版本：1.1.0
        </tr>
        <tr>
            <td>用例名</td>
            <td colspan="2">管理员删除评论</td>
        </tr>
        <tr>
            <td>用例ID</td>
            <td colspan="2">B08</td>
        </tr>
        <tr>
            <td>简要描述</td>
            <td colspan="2">管理员删除评论</td>
        </tr>
        <tr>
            <td>参与者</td>
            <td colspan="2">管理员</td>
        </tr>
        <tr>
            <td>涉众</td>
            <td colspan="2">无</td>
        </tr>
        <tr>
            <td>相关用例</td>
            <td colspan="2">无</td>
        </tr>
        <tr>
            <td>前置条件</td>
            <td colspan="2">该管理员已登录</td>
        </tr>
        <tr>
            <td>后置条件</td>
            <td colspan="2">数据库中该评论记录被删除，刷新前端，删除该条评论</td>
        </tr>
        <tr>
            <td colspan="3">基本事件流 <br>
            <ol> 
                <li>管理员在主页中点击作品</li>
                <li>系统跳转至作品详情页</li>
                <li>管理员在作品详情页查看评论</li>
                <li>管理员选中评论，点击“删除评论”按钮</li>
                <li>管理员在弹窗中点击“确认删除”按钮</li>
            </ol>
        </td>
    </tr>
    <tr>
        <td colspan="3">备选事件流 <br>
        无</td>
    </tr>
    <tr>
        <td colspan="3">补充约束 <br>
            无</td>
    </tr>
    <tr>
        <td colspan="3">待解决问题 <br>
        无 </td>
    </tr>
    </tbody>
</table>

#### 4.2.9 管理员删除回复

<div align="left">
  <p><strong>表4.26 管理员删除回复RUCM表</strong></p>
</div>

<table><tbody>
        <tr >
            <td>作者：刘桢炜</td>
            <td>日期：2023年3月6日</td>
            <td>版本：1.1.0
        </tr>
        <tr>
            <td>用例名</td>
            <td colspan="2">管理员删除回复</td>
        </tr>
        <tr>
            <td>用例ID</td>
            <td colspan="2">B09</td>
        </tr>
        <tr>
            <td>简要描述</td>
            <td colspan="2">管理员删除回复</td>
        </tr>
        <tr>
            <td>参与者</td>
            <td colspan="2">管理员</td>
        </tr>
        <tr>
            <td>涉众</td>
            <td colspan="2">无</td>
        </tr>
        <tr>
            <td>相关用例</td>
            <td colspan="2">无</td>
        </tr>
        <tr>
            <td>前置条件</td>
            <td colspan="2">该管理员已登录</td>
        </tr>
        <tr>
            <td>后置条件</td>
            <td colspan="2">数据库中该回复记录被删除，刷新前端，删除该条回复</td>
        </tr>
        <tr>
            <td colspan="3">基本事件流 <br>
            <ol> 
                <li>管理员在主页中点击作品</li>
                <li>系统跳转至作品详情页</li>
                <li>管理员在作品详情页查看回复</li>
                <li>管理员选中回复，点击“删除回复”按钮</li>
                <li>管理员在弹窗中点击“确认删除”按钮</li>
            </ol>
        </td>
    </tr>
    <tr>
        <td colspan="3">备选事件流 <br>
        无</td>
    </tr>
    <tr>
        <td colspan="3">补充约束 <br>
            无</td>
    </tr>
    <tr>
        <td colspan="3">待解决问题 <br>
        无 </td>
    </tr>
    </tbody>
</table>

### 4.3 展示系统

#### 4.3.1 上传作品

<div align="left">
  <p><strong>表4.27 上传作品RUCM表</strong></p>
</div>

<table><tbody>
        <tr >
            <td>作者：吴晨灿</td>
            <td>日期：2023年3月6日</td>
            <td>版本：1.0.0</td>
        </tr>
        <tr>
            <td>用例名</td>
            <td colspan="2">用户上传作品</td>
        </tr>
        <tr>
            <td>用例ID</td>
            <td colspan="2">C01</td>
        </tr>
        <tr>
            <td>简要描述</td>
            <td colspan="2">用户上传AI生成图像，Prompt，模型，分类以及附加信息</td>
        </tr>
        <tr>
            <td>参与者</td>
            <td colspan="2">用户</td>
        </tr>
        <tr>
            <td>涉众</td>
            <td colspan="2">管理员</td>
        </tr>
        <tr>
            <td>相关用例</td>
            <td colspan="2">管理员审核上传作品B05</td>
        </tr>
        <tr>
            <td>前置条件</td>
            <td colspan="2">该用户已经登录</td>
        </tr>
        <tr>
            <td>后置条件</td>
            <td colspan="2">无</td>
        </tr>
        <tr>
            <td colspan="3">基本事件流 <br>
            <ol> 
                <li>用户进入上传作品页面</li>
                <li>用户上传作品图像及其相关信息</li>
                <li>用户点击“上传作品”按钮</li>
                <li>系统将用户上传作品信息插入管理员可见的作品审核队列</li>
                <li>用户该作品的审核记录标注为“进行中”</li>
            </ol>
        </td>
    </tr>
    <tr>
        <td colspan="3">备选事件流 <br>
			无
        </td>
    </tr>
    <tr>
        <td colspan="3">补充约束 <br>
            无
        </td>
    </tr>
    <tr>
        <td colspan="3">待解决问题 <br>
        无
        </td>
    </tr>
    </tbody>
</table>


![需求分析C01](imgs/需求分析C01.png)

<div align="center">
  <p><strong>图4.5 上传作品活动图</strong></p>
</div>

#### 4.3.2 编辑作品

<div align="left">
  <p><strong>表4.28 编辑作品RUCM表</strong></p>
</div>

<table><tbody>
        <tr >
            <td>作者：吴晨灿</td>
            <td>日期：2023年3月6日</td>
            <td>版本：1.0.0</td>
        </tr>
        <tr>
            <td>用例名</td>
            <td colspan="2">用户编辑已上传作品</td>
        </tr>
        <tr>
            <td>用例ID</td>
            <td colspan="2">C02</td>
        </tr>
        <tr>
            <td>简要描述</td>
            <td colspan="2">用户修改自己上传的作品的相关内容</td>
        </tr>
        <tr>
            <td>参与者</td>
            <td colspan="2">用户</td>
        </tr>
        <tr>
            <td>涉众</td>
            <td colspan="2">管理员</td>
        </tr>
        <tr>
            <td>相关用例</td>
            <td colspan="2">管理员审核上传作品B05</td>
        </tr>
        <tr>
            <td>前置条件</td>
            <td colspan="2">该用户已经登录</td>
        </tr>
        <tr>
            <td>后置条件</td>
            <td colspan="2">无</td>
        </tr>
        <tr>
            <td colspan="3">基本事件流 <br>
            <ol> 
                <li>用户点击“编辑作品”按钮，进入作品编辑页面</li>
                <li>用户编辑作品内容，可编辑AI生成图像，Prompt等信息</li>
                <li>用户点击“编辑完成”按钮</li>
                <li>系统将作品插入管理员可见的作品审核队列</li>
                <li>用户该作品的审核记录标注为“进行中”</li>
            </ol>
        </td>
    </tr>
    <tr>
        <td colspan="3">备选事件流 <br>
			无
        </td>
    </tr>
    <tr>
        <td colspan="3">补充约束 <br>
            <ol>
                <li>用户只能编辑自己上传成功的作品信息</li>
            </ol>
        </td>
    </tr>
    <tr>
        <td colspan="3">待解决问题 <br>
        无 </td>
    </tr>
    </tbody>
</table>

![需求分析C02](imgs/需求分析C02.png)

<div align="center">
  <p><strong>图4.6 编辑作品活动图</strong></p>
</div>

#### 4.3.3 删除作品

<div align="left">
  <p><strong>表4.29 删除作品RUCM表</strong></p>
</div>

<table><tbody>
        <tr >
            <td>作者：吴晨灿</td>
            <td>日期：2023年3月6日</td>
            <td>版本：1.0.0</td>
        </tr>
        <tr>
            <td>用例名</td>
            <td colspan="2">用户删除已上传作品</td>
        </tr>
        <tr>
            <td>用例ID</td>
            <td colspan="2">C03</td>
        </tr>
        <tr>
            <td>简要描述</td>
            <td colspan="2">用户删除自己上传的作品的相关内容</td>
        </tr>
        <tr>
            <td>参与者</td>
            <td colspan="2">用户</td>
        </tr>
        <tr>
            <td>涉众</td>
            <td colspan="2">无</td>
        </tr>
        <tr>
            <td>相关用例</td>
            <td colspan="2">用户上传作品C01</td>
        </tr>
        <tr>
            <td>前置条件</td>
            <td colspan="2">该用户已经登录</td>
        </tr>
        <tr>
            <td>后置条件</td>
            <td colspan="2">无</td>
        </tr>
        <tr>
            <td colspan="3">基本事件流 <br>
            <ol> 
                <li>用户点击“删除作品”按钮，进入删除作品确认界面</li>
                <li>用户确认删除作品</li>
                <li>系统从数据库中删除用户已上传的作品</li>
            </ol>
        </td>
    </tr>
    <tr>
        <td colspan="3">备选事件流 <br>
			无
        </td>
    </tr>
    <tr>
        <td colspan="3">补充约束 <br>
            <ol>
                <li>用户只能删除自己上传成功的作品</li>
            </ol>
        </td>
    </tr>
    <tr>
        <td colspan="3">待解决问题 <br>
        无 </td>
    </tr>
    </tbody>
</table>

#### 4.3.4 查询作品

<div align="left">
  <p><strong>表4.30 查询作品RUCM表</strong></p>
</div>

<table><tbody>
        <tr >
            <td>作者：吴晨灿</td>
            <td>日期：2023年3月22日</td>
            <td>版本：1.1.2</td>
        </tr>
        <tr>
            <td>用例名</td>
            <td colspan="2">用户查询作品</td>
        </tr>
        <tr>
            <td>用例ID</td>
            <td colspan="2">C04</td>
        </tr>
        <tr>
            <td>简要描述</td>
            <td colspan="2">游客或用户通过“关键字”或者标签查询已上传的作品，同时可以通过热度、上传时间等信息对作品进行排序，通过使用的模型等信息对作品进行过滤</td>
        </tr>
        <tr>
            <td>参与者</td>
            <td colspan="2">游客，用户</td>
        </tr>
        <tr>
            <td>涉众</td>
            <td colspan="2">无</td>
        </tr>
        <tr>
            <td>相关用例</td>
            <td colspan="2">用户上传作品C01，用户关注关系A09</td>
        </tr>
        <tr>
            <td>前置条件</td>
            <td colspan="2">无</td>
        </tr>
        <tr>
            <td>后置条件</td>
            <td colspan="2">无</td>
        </tr>
        <tr>
            <td colspan="3">基本事件流 <br>
            <ol> 
                <li>用户在搜索栏中输入Prompt关键字或者标签信息</li>
                <li>（可选）用户在排序选项中对排序规则进行选择</li>
                <li>（可选）用户在过滤选项中对过滤规则进行选择</li>
                <li>用户点击搜索栏中“搜索”按钮</li>
                <li>系统根据用户输入信息以及排序和过滤规则从数据库中获取相应数据</li>
            </ol>
        </td>
    </tr>
    <tr>
        <td colspan="3">备选事件流 <br>
			无
        </td>
    </tr>
    <tr>
        <td colspan="3">补充约束 <br>
            无
        </td>
    </tr>
    <tr>
        <td colspan="3">待解决问题 <br>
        无 </td>
    </tr>
    </tbody>
</table>


![需求分析C04](imgs/需求分析C04.png)

<div align="center">
  <p><strong>图4.7 查询作品活动图</strong></p>
</div>

#### 4.3.5 查看作品详情

<div align="left">
  <p><strong>表4.31 查看作品详情RUCM表</strong></p>
</div>

<table><tbody>
        <tr >
            <td>作者：吴晨灿</td>
            <td>日期：2023年3月6日</td>
            <td>版本：1.0.0</td>
        </tr>
        <tr>
            <td>用例名</td>
            <td colspan="2">用户查看作品详情</td>
        </tr>
        <tr>
            <td>用例ID</td>
            <td colspan="2">C05</td>
        </tr>
        <tr>
            <td>简要描述</td>
            <td colspan="2">游客或用户查看作品具体详情，包括作品图像、作品Prompt、使用的AI模型、标签分类、上传作者以及附加其他信息，同时查询与该作品相关的用户评论和评论回复</td>
        </tr>
        <tr>
            <td>参与者</td>
            <td colspan="2">游客，用户</td>
        </tr>
        <tr>
            <td>涉众</td>
            <td colspan="2">无</td>
        </tr>
        <tr>
            <td>相关用例</td>
            <td colspan="2">用户上传作品C01，用户评论作品E01，用户回复评论E03</td>
        </tr>
        <tr>
            <td>前置条件</td>
            <td colspan="2">无</td>
        </tr>
        <tr>
            <td>后置条件</td>
            <td colspan="2">无</td>
        </tr>
        <tr>
            <td colspan="3">基本事件流 <br>
            <ol> 
                <li>用户点击进入作品详情界面</li>
                <li>系统从数据库中获取关于该作品的详细信息</li>
                <li>用户成功查看到作品的详细信息</li>
            </ol>
        </td>
    </tr>
    <tr>
        <td colspan="3">备选事件流 <br>
			<ol>
                <li>代替3，如果该作品的用户删除了该作品，那么进入404页面，显示”未查询到该作品详情“</li>
            </ol>
        </td>
    </tr>
    <tr>
        <td colspan="3">补充约束 <br>
            无
        </td>
    </tr>
    <tr>
        <td colspan="3">待解决问题 <br>
        无 </td>
    </tr>
    </tbody>
</table>

#### 4.3.6 查询上传作品审核进度

<div align="left">
  <p><strong>表4.32 查询上传作品审核进度RUCM表</strong></p>
</div>

<table><tbody>
        <tr >
            <td>作者：吴晨灿</td>
            <td>日期：2023年3月6日</td>
            <td>版本：1.0.0</td>
        </tr>
        <tr>
            <td>用例名</td>
            <td colspan="2">用户查看上传作品审核进度</td>
        </tr>
        <tr>
            <td>用例ID</td>
            <td colspan="2">C06</td>
        </tr>
        <tr>
            <td>简要描述</td>
            <td colspan="2">用户查看其上传作品的审核进度</td>
        </tr>
        <tr>
            <td>参与者</td>
            <td colspan="2">用户</td>
        </tr>
        <tr>
            <td>涉众</td>
            <td colspan="2">管理员</td>
        </tr>
        <tr>
            <td>相关用例</td>
            <td colspan="2">用户上传作品C01，管理员审核上传作品B05</td>
        </tr>
        <tr>
            <td>前置条件</td>
            <td colspan="2">该用户已经登录</td>
        </tr>
        <tr>
            <td>后置条件</td>
            <td colspan="2">无</td>
        </tr>
        <tr>
            <td colspan="3">基本事件流 <br>
            <ol> 
                <li>用户点击进入作品审核进度查询界面</li>
                <li>（可选）用户在过滤条件中选择全部/通过/进行中/拒绝来筛选审核进度信息</li>
                <li>系统从数据库中获取关于该用户上传的作品的审核信息</li>
                <li>用户成功查看到自己上传作品审核信息</li>
            </ol>
        </td>
    </tr>
    <tr>
        <td colspan="3">备选事件流 <br>
            无
        </td>
    </tr>
    <tr>
        <td colspan="3">补充约束 <br>
            无
        </td>
    </tr>
    <tr>
        <td colspan="3">待解决问题 <br>
        无 </td>
    </tr>
    </tbody>
</table>

![需求分析C06](imgs/需求分析C06.png)

<div align="center">
  <p><strong>图4.8 查询上传作品审核进度活动图</strong></p>
</div>

### 4.4 收藏系统

本系统一个非常重要的部分是收藏系统。用户可以收藏喜欢的图片，也可以将自己的收藏分享给别人看。在该模块中，主要包含管理自己的收藏、分享收藏、查询收藏等功能。

#### 4.4.1 添加收藏

<div align="left">
  <p><strong>表4.33 添加收藏RUCM表</strong></p>
</div>

<table><tbody>
        <tr >
            <td>作者：许羽晟</td>
            <td>日期：2023年3月22日</td>
            <td>版本：1.1.2
        </tr>
        <tr>
            <td>用例名</td>
            <td colspan="2">添加收藏</td>
        </tr>
        <tr>
            <td>用例ID</td>
            <td colspan="2">D01</td>
        </tr>
        <tr>
            <td>简要描述</td>
            <td colspan="2">用户登录后，选择喜欢的图并添加至收藏</td>
        </tr>
        <tr>
            <td>参与者</td>
            <td colspan="2">用户</td>
        </tr>
        <tr>
            <td>涉众</td>
            <td colspan="2">无</td>
        </tr>
        <tr>
            <td>相关用例</td>
            <td colspan="2">无</td>
        </tr>
        <tr>
            <td>前置条件</td>
            <td colspan="2">该用户已经登录</td>
        </tr>
        <tr>
            <td>后置条件</td>
            <td colspan="2">数据库中存储该图片至收藏</td>
    </tr>
    <tr>
        <td colspan="3">基本事件流 <br>
        <ol> 
            <li>用户在图片预览页面寻找喜欢的图片</li>
            <li>用户点击图片预览中的收藏功能，存储到某一收藏分类</li>
            <li>系统将对应的信息写入数据库</li>
            <li>系统提示收藏成功</li>
        </ol>
    </td>
</tr>
<tr>
    <td colspan="3">备选事件流 <br>
    	<ol>
            <li>代替2，显示该图片已经被收藏过了</li>
            <li>代替2，提示用户无法重复收藏相同图片</li>
        </ol>
    </td>
</tr>
<tr>
    <td colspan="3">补充约束 <br>
        无
    </td>
</tr>
<tr>
    <td colspan="3">待解决问题 <br>
    无 </td>
</tr>
</tbody></table>

#### 4.4.2 收藏分类

##### 4.4.2.1 Public

<div align="left">
  <p><strong>表4.34 创建公开收藏RUCM表</strong></p>
</div>

<table><tbody>
        <tr >
            <td>作者：许羽晟</td>
            <td>日期：2023年3月22日</td>
            <td>版本：1.1.2
        </tr>
        <tr>
            <td>用例名</td>
            <td colspan="2">添加公开收藏</td>
        </tr>
        <tr>
            <td>用例ID</td>
            <td colspan="2">D02</td>
        </tr>
        <tr>
            <td>简要描述</td>
            <td colspan="2">用户登录后，创建一个新的公开收藏</td>
        </tr>
        <tr>
            <td>参与者</td>
            <td colspan="2">用户</td>
        </tr>
        <tr>
            <td>涉众</td>
            <td colspan="2">无</td>
        </tr>
        <tr>
            <td>相关用例</td>
            <td colspan="2">无</td>
        </tr>
        <tr>
            <td>前置条件</td>
            <td colspan="2">该用户已经登录</td>
        </tr>
        <tr>
            <td>后置条件</td>
            <td colspan="2">数据库中创建一个新的收藏分类</td>
    </tr>
    <tr>
        <td colspan="3">基本事件流 <br>
        <ol> 
            <li>用户进入收藏管理页面</li>
            <li>用户选择创建一个新的收藏</li>
            <li>用户填写收藏的分类等信息</li>
            <li>系统将对应的信息写入数据库</li>
            <li>系统提示收藏成功</li>
        </ol>
    </td>
</tr>
<tr>
    <td colspan="3">备选事件流 <br>
    	<ol>
            <li>代替4，系统检测到用户创建了过多的收藏或者重复名</li>
            <li>代替4，提示用户删掉多余的收藏或者改名</li>
        </ol>
    </td>
</tr>
<tr>
    <td colspan="3">补充约束 <br>
        无
    </td>
</tr>
<tr>
    <td colspan="3">待解决问题 <br>
    无 </td>
</tr>
</tbody></table>


![需求分析D02](imgs/需求分析D02.png)

<div align="center">
  <p><strong>图4.9 创建公开收藏活动图</strong></p>
</div>

##### 4.4.2.2 Private

<div align="left">
  <p><strong>表4.35 创建私有收藏RUCM表</strong></p>
</div>

<table><tbody>
        <tr >
            <td>作者：许羽晟</td>
            <td>日期：2023年3月22日</td>
            <td>版本：1.1.2
        </tr>
        <tr>
            <td>用例名</td>
            <td colspan="2">添加私有收藏</td>
        </tr>
        <tr>
            <td>用例ID</td>
            <td colspan="2">D03</td>
        </tr>
        <tr>
            <td>简要描述</td>
            <td colspan="2">用户登录后，创建一个新的私有收藏</td>
        </tr>
        <tr>
            <td>参与者</td>
            <td colspan="2">用户</td>
        </tr>
        <tr>
            <td>涉众</td>
            <td colspan="2">无</td>
        </tr>
        <tr>
            <td>相关用例</td>
            <td colspan="2">无</td>
        </tr>
        <tr>
            <td>前置条件</td>
            <td colspan="2">该用户已经登录</td>
        </tr>
        <tr>
            <td>后置条件</td>
            <td colspan="2">数据库中创建一个新的收藏分类</td>
    </tr>
    <tr>
        <td colspan="3">基本事件流 <br>
        <ol> 
            <li>用户进入收藏管理页面</li>
            <li>用户选择创建一个新的收藏</li>
            <li>用户填写收藏的分类等信息</li>
            <li>系统将对应的信息写入数据库</li>
            <li>系统提示收藏成功</li>
        </ol>
    </td>
</tr>
<tr>
    <td colspan="3">备选事件流 <br>
    	<ol>
            <li>代替4，系统检测到用户创建了过多的收藏或者重复名</li>
            <li>代替4，提示用户删掉多余的收藏或者改名</li>
        </ol>
    </td>
</tr>
<tr>
    <td colspan="3">补充约束 <br>
        无
    </td>
</tr>
<tr>
    <td colspan="3">待解决问题 <br>
    无 </td>
</tr>
</tbody></table>

![需求分析D03](imgs/需求分析D03.png)

<div align="center">
  <p><strong>图4.10 创建私有收藏活动图</strong></p>
</div>

#### 4.4.3 查看收藏

<div align="left">
  <p><strong>表4.36 查看收藏RUCM表</strong></p>
</div>

<table><tbody>
        <tr >
            <td>作者：许羽晟</td>
            <td>日期：2023年3月22日</td>
            <td>版本：1.1.2
        </tr>
        <tr>
            <td>用例名</td>
            <td colspan="2">查看收藏</td>
        </tr>
        <tr>
            <td>用例ID</td>
            <td colspan="2">D04</td>
        </tr>
        <tr>
            <td>简要描述</td>
            <td colspan="2">用户登录后，查看收藏</td>
        </tr>
        <tr>
            <td>参与者</td>
            <td colspan="2">用户</td>
        </tr>
        <tr>
            <td>涉众</td>
            <td colspan="2">无</td>
        </tr>
        <tr>
            <td>相关用例</td>
            <td colspan="2">无</td>
        </tr>
        <tr>
            <td>前置条件</td>
            <td colspan="2">该用户已经登录</td>
        </tr>
        <tr>
            <td>后置条件</td>
            <td colspan="2">无</td>
    </tr>
    <tr>
        <td colspan="3">基本事件流 <br>
        <ol> 
            <li>用户进入收藏管理页面</li>
            <li>用户选择收藏的分类</li>
            <li>系统显示该类的所有收藏</li>
        </ol>
    </td>
</tr>
<tr>
    <td colspan="3">备选事件流 <br>
    无
    </td>
</tr>
<tr>
    <td colspan="3">补充约束 <br>
        无
    </td>
</tr>
<tr>
    <td colspan="3">待解决问题 <br>
    无 </td>
</tr>
</tbody></table>

#### 4.4.4 取消收藏

<div align="left">
  <p><strong>表4.37 取消收藏RUCM表</strong></p>
</div>

<table><tbody>
        <tr >
            <td>作者：许羽晟</td>
            <td>日期：2023年3月22日</td>
            <td>版本：1.1.2
        </tr>
        <tr>
            <td>用例名</td>
            <td colspan="2">取消收藏</td>
        </tr>
        <tr>
            <td>用例ID</td>
            <td colspan="2">D05</td>
        </tr>
        <tr>
            <td>简要描述</td>
            <td colspan="2">用户登录后，取消收藏</td>
        </tr>
        <tr>
            <td>参与者</td>
            <td colspan="2">用户</td>
        </tr>
        <tr>
            <td>涉众</td>
            <td colspan="2">无</td>
        </tr>
        <tr>
            <td>相关用例</td>
            <td colspan="2">添加收藏D01</td>
        </tr>
        <tr>
            <td>前置条件</td>
            <td colspan="2">该用户已经登录</td>
        </tr>
        <tr>
            <td>后置条件</td>
            <td colspan="2">在数据库中删除对应的收藏信息</td>
    </tr>
    <tr>
        <td colspan="3">基本事件流 <br>
        <ol> 
            <li>用户进入收藏管理页面</li>
            <li>用户选择删除该条收藏</li>
            <li>系统将根据条件从数据库删除收藏</li>
            <li>系统提示用户成功删除</li>
        </ol>
    </td>
</tr>
<tr>
    <td colspan="3">备选事件流 <br>
    无
    </td>
</tr>
<tr>
    <td colspan="3">补充约束 <br>
        无
    </td>
</tr>
<tr>
    <td colspan="3">待解决问题 <br>
    无 </td>
</tr>
</tbody></table>

#### 4.4.5 查询收藏

<div align="left">
  <p><strong>表4.38 查询收藏RUCM表</strong></p>
</div>

<table><tbody>
        <tr >
            <td>作者：许羽晟</td>
            <td>日期：2023年3月22日</td>
            <td>版本：1.1.2
        </tr>
        <tr>
            <td>用例名</td>
            <td colspan="2">查询收藏</td>
        </tr>
        <tr>
            <td>用例ID</td>
            <td colspan="2">D06</td>
        </tr>
        <tr>
            <td>简要描述</td>
            <td colspan="2">用户登录后，查询收藏</td>
        </tr>
        <tr>
            <td>参与者</td>
            <td colspan="2">用户</td>
        </tr>
        <tr>
            <td>涉众</td>
            <td colspan="2">无</td>
        </tr>
        <tr>
            <td>相关用例</td>
            <td colspan="2">添加收藏D01，新建收藏D07</td>
        </tr>
        <tr>
            <td>前置条件</td>
            <td colspan="2">该用户已经登录</td>
        </tr>
        <tr>
            <td>后置条件</td>
            <td colspan="2">无</td>
    </tr>
    <tr>
        <td colspan="3">基本事件流 <br>
        <ol> 
            <li>用户进入收藏管理页面</li>
            <li>用户输入查询的关键字</li>
            <li>系统从数据库中查询所有符合条件的收藏</li>
            <li>系统显示所有符合条件的收藏</li>
        </ol>
    </td>
</tr>
<tr>
    <td colspan="3">备选事件流 <br>
    无
    </td>
</tr>
<tr>
    <td colspan="3">补充约束 <br>
        无
    </td>
</tr>
<tr>
    <td colspan="3">待解决问题 <br>
    无 </td>
</tr>
</tbody></table>

#### 4.4.6 新建收藏分类

<div align="left">
  <p><strong>表4.39 新建收藏分类RUCM表</strong></p>
</div>

<table><tbody>
        <tr >
            <td>作者：许羽晟</td>
            <td>日期：2023年3月22日</td>
            <td>版本：1.1.2
        </tr>
        <tr>
            <td>用例名</td>
            <td colspan="2">新建收藏分类</td>
        </tr>
        <tr>
            <td>用例ID</td>
            <td colspan="2">D07</td>
        </tr>
        <tr>
            <td>简要描述</td>
            <td colspan="2">用户登录后，新建收藏分类</td>
        </tr>
        <tr>
            <td>参与者</td>
            <td colspan="2">用户</td>
        </tr>
        <tr>
            <td>涉众</td>
            <td colspan="2">无</td>
        </tr>
        <tr>
            <td>相关用例</td>
            <td colspan="2">无</td>
        </tr>
        <tr>
            <td>前置条件</td>
            <td colspan="2">该用户已经登录</td>
        </tr>
        <tr>
            <td>后置条件</td>
            <td colspan="2">数据库中记录有一个新的收藏分类</td>
    </tr>
    <tr>
        <td colspan="3">基本事件流 <br>
        <ol> 
            <li>用户进入收藏管理页面</li>
            <li>用户选择新建一个收藏分类</li>
            <li>系统在数据库中新建收藏分类</li>
            <li>系统提示操作成功</li>
        </ol>
    </td>
</tr>
<tr>
    <td colspan="3">备选事件流 <br>
    	<ol>
            <li>代替3，用户的收藏分类达到系统设定的上限</li>
            <li>代替3，系统提示用户删除不需要的收藏分类</li>
        </ol>
    </td>
</tr>
<tr>
    <td colspan="3">补充约束 <br>
        无
    </td>
</tr>
<tr>
    <td colspan="3">待解决问题 <br>
    无 </td>
</tr>
</tbody></table>

#### 4.4.7 删除收藏分类

<div align="left">
  <p><strong>表4.40 删除收藏分类RUCM表</strong></p>
</div>

<table><tbody>
        <tr >
            <td>作者：许羽晟</td>
            <td>日期：2023年3月22日</td>
            <td>版本：1.1.2
        </tr>
        <tr>
            <td>用例名</td>
            <td colspan="2">删除收藏分类</td>
        </tr>
        <tr>
            <td>用例ID</td>
            <td colspan="2">D08</td>
        </tr>
        <tr>
            <td>简要描述</td>
            <td colspan="2">用户登录后，删除收藏分类</td>
        </tr>
        <tr>
            <td>参与者</td>
            <td colspan="2">用户</td>
        </tr>
        <tr>
            <td>涉众</td>
            <td colspan="2">无</td>
        </tr>
        <tr>
            <td>相关用例</td>
            <td colspan="2">新建收藏D07</td>
        </tr>
        <tr>
            <td>前置条件</td>
            <td colspan="2">该用户已经登录</td>
        </tr>
        <tr>
            <td>后置条件</td>
            <td colspan="2">数据库中删除一个已有的收藏分类</td>
    </tr>
    <tr>
        <td colspan="3">基本事件流 <br>
        <ol> 
            <li>用户进入收藏管理页面</li>
            <li>用户选择新删除一个收藏分类</li>
            <li>系统在数据库中删除收藏分类</li>
            <li>系统提示操作成功</li>
        </ol>
    </td>
</tr>
<tr>
    <td colspan="3">备选事件流 <br>
    无
    </td>
</tr>
<tr>
    <td colspan="3">补充约束 <br>
        无
    </td>
</tr>
<tr>
    <td colspan="3">待解决问题 <br>
    无 </td>
</tr>
</tbody></table> 

#### 4.4.8 修改收藏分类

##### 4.4.8.1 命名

<div align="left">
  <p><strong>表4.41 修改收藏分类命名RUCM表</strong></p>
</div>

<table><tbody>
        <tr >
            <td>作者：许羽晟</td>
            <td>日期：2023年3月22日</td>
            <td>版本：1.1.2
        </tr>
        <tr>
            <td>用例名</td>
            <td colspan="2">修改命名</td>
        </tr>
        <tr>
            <td>用例ID</td>
            <td colspan="2">D09</td>
        </tr>
        <tr>
            <td>简要描述</td>
            <td colspan="2">用户登录后，修改收藏分类的名字</td>
        </tr>
        <tr>
            <td>参与者</td>
            <td colspan="2">用户</td>
        </tr>
        <tr>
            <td>涉众</td>
            <td colspan="2">无</td>
        </tr>
        <tr>
            <td>相关用例</td>
            <td colspan="2">新建收藏D07</td>
        </tr>
        <tr>
            <td>前置条件</td>
            <td colspan="2">该用户已经登录</td>
        </tr>
        <tr>
            <td>后置条件</td>
            <td colspan="2">数据库中修改已有收藏分类的名字</td>
    </tr>
    <tr>
        <td colspan="3">基本事件流 <br>
        <ol> 
            <li>用户进入收藏管理页面</li>
            <li>用户选择新修改一个收藏分类的名字</li>
            <li>系统在数据库中修改收藏分类</li>
            <li>系统提示操作成功</li>
        </ol>
    </td>
</tr>
<tr>
    <td colspan="3">备选事件流 <br>
    	<ol>
            <li>用户输入了不合法的名字</li>
            <li>系统提示用户更换一个名字</li>
        </ol>
    </td>
</tr>
<tr>
    <td colspan="3">补充约束 <br>
        无
    </td>
</tr>
<tr>
    <td colspan="3">待解决问题 <br>
    无 </td>
</tr>
</tbody></table> 

![需求分析D09](imgs/需求分析D09.png)

<div align="center">
  <p><strong>图4.11 修改收藏分类命名活动图</strong></p>
</div>

##### 4.4.8.2 可见性

<div align="left">
  <p><strong>表4.42 修改收藏分类可见性RUCM表</strong></p>
</div>

<table><tbody>
        <tr >
            <td>作者：许羽晟</td>
            <td>日期：2023年3月22日</td>
            <td>版本：1.1.2
        </tr>
        <tr>
            <td>用例名</td>
            <td colspan="2">修改可见性</td>
        </tr>
        <tr>
            <td>用例ID</td>
            <td colspan="2">D10</td>
        </tr>
        <tr>
            <td>简要描述</td>
            <td colspan="2">用户登录后，修改收藏分类的可见性</td>
        </tr>
        <tr>
            <td>参与者</td>
            <td colspan="2">用户</td>
        </tr>
        <tr>
            <td>涉众</td>
            <td colspan="2">无</td>
        </tr>
        <tr>
            <td>相关用例</td>
            <td colspan="2">新建收藏D07</td>
        </tr>
        <tr>
            <td>前置条件</td>
            <td colspan="2">该用户已经登录</td>
        </tr>
        <tr>
            <td>后置条件</td>
            <td colspan="2">数据库中修改已有收藏分类的可见性</td>
    </tr>
    <tr>
        <td colspan="3">基本事件流 <br>
        <ol> 
            <li>用户进入收藏管理页面</li>
            <li>用户选择新修改一个收藏分类的可见性</li>
            <li>系统在数据库中修改收藏分类</li>
            <li>系统提示操作成功</li>
        </ol>
    </td>
</tr>
<tr>
    <td colspan="3">备选事件流 <br>
    无
    </td>
</tr>
<tr>
    <td colspan="3">补充约束 <br>
        无
    </td>
</tr>
<tr>
    <td colspan="3">待解决问题 <br>
    无 </td>
</tr>
</tbody></table>

![需求分析D10-1](imgs/需求分析D10-1.png)

<div align="center">
  <p><strong>图4.12 修改收藏分类可见性活动图(Public)</strong></p>
</div>

![需求分析D10-2](imgs/需求分析D10-2.png)

<div align="center">
  <p><strong>图4.13 修改收藏分类可见性活动图(Private)</strong></p>
</div>

### 4.5 评论系统

#### 4.5.1 评论作品

<div align="left">
  <p><strong>表4.43 评论作品RUCM表</strong></p>
</div>

<table><tbody>
        <tr >
            <td>作者：吴晨灿</td>
            <td>日期：2023年3月6日</td>
            <td>版本：1.0.0</td>
        </tr>
        <tr>
            <td>用例名</td>
            <td colspan="2">用户评论作品</td>
        </tr>
        <tr>
            <td>用例ID</td>
            <td colspan="2">E01</td>
        </tr>
        <tr>
            <td>简要描述</td>
            <td colspan="2">用户评论已上传的作品</td>
        </tr>
        <tr>
            <td>参与者</td>
            <td colspan="2">用户</td>
        </tr>
        <tr>
            <td>涉众</td>
            <td colspan="2">游客，用户，管理员</td>
        </tr>
        <tr>
            <td>相关用例</td>
            <td colspan="2">用户上传作品C01，用户回复评论E03</td>
        </tr>
        <tr>
            <td>前置条件</td>
            <td colspan="2">该用户已经登录，评论作品存在</td>
        </tr>
        <tr>
            <td>后置条件</td>
            <td colspan="2">无</td>
        </tr>
        <tr>
            <td colspan="3">基本事件流 <br>
            <ol> 
                <li>用户在作品详情页面评论作品</li>
                <li>系统将用户评价内容与该作品关联，存入数据库</li>
                <li>用户成功在作品详情页面查看到刚刚的评价内容</li>
            </ol>
        </td>
    </tr>
    <tr>
        <td colspan="3">备选事件流 <br>
			<ol>
                <li>代替3，如果该作品的用户删除了该作品，那么作品评论失败</li>
            </ol>
        </td>
    </tr>
    <tr>
        <td colspan="3">补充约束 <br>
            无
        </td>
    </tr>
    <tr>
        <td colspan="3">待解决问题 <br>
        无 </td>
    </tr>
    </tbody>
</table>

![需求分析E01](imgs/需求分析E01.png)

<div align="center">
  <p><strong>图4.14 评论作品活动图</strong></p>
</div>

#### 4.5.2 删除评论

<div align="left">
  <p><strong>表4.44 删除评论RUCM表</strong></p>
</div>

<table><tbody>
        <tr >
            <td>作者：吴晨灿</td>
            <td>日期：2023年3月6日</td>
            <td>版本：1.0.0</td>
        </tr>
        <tr>
            <td>用例名</td>
            <td colspan="2">用户删除作品评论</td>
        </tr>
        <tr>
            <td>用例ID</td>
            <td colspan="2">E02</td>
        </tr>
        <tr>
            <td>简要描述</td>
            <td colspan="2">用户删除自己之前的评论</td>
        </tr>
        <tr>
            <td>参与者</td>
            <td colspan="2">用户</td>
        </tr>
        <tr>
            <td>涉众</td>
            <td colspan="2">游客</td>
        </tr>
        <tr>
            <td>相关用例</td>
            <td colspan="2">用户上传作品C01，用户评论作品E01，用户回复评论E03</td>
        </tr>
        <tr>
            <td>前置条件</td>
            <td colspan="2">该用户已经登录，作品存在，评论作品存在</td>
        </tr>
        <tr>
            <td>后置条件</td>
            <td colspan="2">无</td>
        </tr>
        <tr>
            <td colspan="3">基本事件流 <br>
            <ol> 
                <li>用户在作品详情页面，对自己之前的评论点击“删除”</li>
                <li>系统将用户评论从数据库中删除</li>
                <li>用户在作品详情页面看不到之前的评论，以及评论相关的回复（如果之前有回复的话）</li>
            </ol>
        </td>
    </tr>
    <tr>
        <td colspan="3">备选事件流 <br>
			<ol>
                <li>代替3，如果该作品的用户删除了该作品，那么评论删除失败</li>
            </ol>
        </td>
    </tr>
    <tr>
        <td colspan="3">补充约束 <br>
            无
        </td>
    </tr>
    <tr>
        <td colspan="3">待解决问题 <br>
        无 </td>
    </tr>
    </tbody>
</table>

#### 4.5.3 评论回复

<div align="left">
  <p><strong>表4.45 评论回复RUCM表</strong></p>
</div>

<table><tbody>
        <tr >
            <td>作者：吴晨灿</td>
            <td>日期：2023年3月6日</td>
            <td>版本：1.0.0</td>
        </tr>
        <tr>
            <td>用例名</td>
            <td colspan="2">用户回复评论</td>
        </tr>
        <tr>
            <td>用例ID</td>
            <td colspan="2">E03</td>
        </tr>
        <tr>
            <td>简要描述</td>
            <td colspan="2">用户回复作品下的相关评论或者其他回复</td>
        </tr>
        <tr>
            <td>参与者</td>
            <td colspan="2">用户</td>
        </tr>
        <tr>
            <td>涉众</td>
            <td colspan="2">游客</td>
        </tr>
        <tr>
            <td>相关用例</td>
            <td colspan="2">用户上传作品C01，用户评论作品E01，用户删除评论E02</td>
        </tr>
        <tr>
            <td>前置条件</td>
            <td colspan="2">该用户已经登录，评论作品存在，评论存在</td>
        </tr>
        <tr>
            <td>后置条件</td>
            <td colspan="2">无</td>
        </tr>
        <tr>
            <td colspan="3">基本事件流 <br>
            <ol> 
                <li>用户在作品详情页面回复作品下的评论</li>
                <li>系统将用户回复内容与该评论关联，存入数据库</li>
                <li>用户成功在作品详情页面查看到刚刚的回复内容</li>
            </ol>
        </td>
    </tr>
    <tr>
        <td colspan="3">备选事件流 <br>
			<ol>
                <li>代替3，如果该作品的用户删除了该作品，或者作品评论用户删除了该评论，那么回复失败</li>
            </ol>
        </td>
    </tr>
    <tr>
        <td colspan="3">补充约束 <br>
            无
        </td>
    </tr>
    <tr>
        <td colspan="3">待解决问题 <br>
        无 </td>
    </tr>
    </tbody>
</table>

#### 4.5.4 删除回复

<div align="left">
  <p><strong>表4.46 删除回复RUCM表</strong></p>
</div>

<table><tbody>
        <tr >
            <td>作者：吴晨灿</td>
            <td>日期：2023年3月6日</td>
            <td>版本：1.0.0</td>
        </tr>
        <tr>
            <td>用例名</td>
            <td colspan="2">用户删除回复</td>
        </tr>
        <tr>
            <td>用例ID</td>
            <td colspan="2">E04</td>
        </tr>
        <tr>
            <td>简要描述</td>
            <td colspan="2">用户删除自己之前的回复</td>
        </tr>
        <tr>
            <td>参与者</td>
            <td colspan="2">用户</td>
        </tr>
        <tr>
            <td>涉众</td>
            <td colspan="2">游客</td>
        </tr>
        <tr>
            <td>相关用例</td>
            <td colspan="2">用户上传作品C01，用户评论作品E01，用户删除评论E02，用户回复评论E03</td>
        </tr>
        <tr>
            <td>前置条件</td>
            <td colspan="2">该用户已经登录，评论作品存在，评论存在，回复存在</td>
        </tr>
        <tr>
            <td>后置条件</td>
            <td colspan="2">无</td>
        </tr>
        <tr>
            <td colspan="3">基本事件流 <br>
            <ol> 
                <li>用户在作品详情页面，对自己之前的回复点击“删除”</li>
                <li>系统将用户回复从数据库中删除</li>
                <li>用户在作品详情页面无法看到自己的回复内容</li>
            </ol>
        </td>
    </tr>
    <tr>
        <td colspan="3">备选事件流 <br>
			<ol>
                <li>代替3，如果该作品的用户删除了该作品，或者作品评论用户删除了该评论，那么回复不存在，删除失败</li>
            </ol>
        </td>
    </tr>
    <tr>
        <td colspan="3">补充约束 <br>
            无
        </td>
    </tr>
    <tr>
        <td colspan="3">待解决问题 <br>
        无 </td>
    </tr>
    </tbody>
</table>

### 4.6 推荐系统

#### 4.6.1 热门推荐

<div align="left">
  <p><strong>表4.47 热门推荐RUCM表</strong></p>
</div>

<table><tbody>
        <tr >
            <td>作者：王梓竣</td>
            <td>日期：2023年3月5日</td>
            <td>版本：1.0.0</td>
        </tr>
        <tr>
            <td>用例名</td>
            <td colspan="2">推荐热门作品</td>
        </tr>
        <tr>
            <td>用例ID</td>
            <td colspan="2">F01</td>
        </tr>
        <tr>
            <td>简要描述</td>
            <td colspan="2">向用户和游客按热度降序推荐作品</td>
        </tr>
        <tr>
            <td>参与者</td>
            <td colspan="2">用户、游客</td>
        </tr>
        <tr>
            <td>涉众</td>
            <td colspan="2">无</td>
        </tr>
        <tr>
            <td>相关用例</td>
            <td colspan="2">推荐热度最高作品B05</td>
        </tr>
        <tr>
            <td>前置条件</td>
            <td colspan="2">无</td>
        </tr>
        <tr>
            <td>后置条件</td>
            <td colspan="2">无</td>
        </tr>
        <tr>
            <td colspan="3">基本事件流 <br>
            <ol> 
                <li>用户进入系统主界面</li>
                <li>用户点击“热门推荐”按钮</li>
                <li>系统将近期作品按热度降序排序</li>
                <li>系统展示按热度降序展示作品</li>
            </ol>
            </td>
        </tr>
        <tr>
            <td colspan="3">备选事件流 <br>
            无
            </td>
        </tr>
        <tr>
            <td colspan="3">补充约束 <br>
            无</td>
        </tr>
        <tr>
            <td colspan="3">待解决问题 <br>
            无 </td>
        </tr>
        <tr>
            <td colspan="3">相关图 <br>
            无 </td>
        </tr>
</table> 

#### 4.6.2 个性化推荐

<div align="left">
  <p><strong>表4.48 个性化推荐RUCM表</strong></p>
</div>

<table><tbody>
        <tr >
            <td>作者：王梓竣</td>
            <td>日期：2023年3月5日</td>
            <td>版本：1.0.0</td>
        </tr>
        <tr>
            <td>用例名</td>
            <td colspan="2">推荐个性化作品</td>
        </tr>
        <tr>
            <td>用例ID</td>
            <td colspan="2">F02</td>
        </tr>
        <tr>
            <td>简要描述</td>
            <td colspan="2">向用户个性化推荐作品</td>
        </tr>
        <tr>
            <td>参与者</td>
            <td colspan="2">用户</td>
        </tr>
        <tr>
            <td>涉众</td>
            <td colspan="2">无</td>
        </tr>
        <tr>
            <td>相关用例</td>
            <td colspan="2">根据用户收藏的Prompt推荐作品B05、用户的follow关系推荐作品B06、浏览历史推荐作品B07</td>
        </tr>
        <tr>
            <td>前置条件</td>
            <td colspan="2">用户已经注册并登录</td>
        </tr>
        <tr>
            <td>后置条件</td>
            <td colspan="2">无</td>
        </tr>
        <tr>
            <td colspan="3">基本事件流 <br>
            <ol> 
                <li>用户进入系统主界面</li>
                <li>用户点击“个性化推荐”按钮</li>
                <li>系统执行推荐算法</li>
                <li>系统展示个性化推荐作品</li>
            </ol>
            </td>
        </tr>
        <tr>
            <td colspan="3">备选事件流 <br>
            <ol> 
                <li>代替3. 系统提示用户未登录，跳转到登录界面</li>
                <li>代替3. 系统提示用户未开启个性化推荐功能</li>
            </ol>
            </td>
        </tr>
        <tr>
            <td colspan="3">补充约束 <br>
            无</td>
        </tr>
        <tr>
            <td colspan="3">待解决问题 <br>
            无 </td>
        </tr>
        <tr>
            <td colspan="3">相关图 <br>
            无 </td>
        </tr>
</table> 

![需求分析F02](imgs/需求分析F02.png)

<div align="center">
  <p><strong>图4.15 个性化推荐活动图</strong></p>
</div>

#### 4.6.3 关闭推荐

<div align="left">
  <p><strong>表4.49 关闭推荐RUCM表</strong></p>
</div>

<table><tbody>
        <tr >
            <td>作者：王梓竣</td>
            <td>日期：2023年3月5日</td>
            <td>版本：1.0.0</td>
        </tr>
        <tr>
            <td>用例名</td>
            <td colspan="2">关闭个性化推荐</td>
        </tr>
        <tr>
            <td>用例ID</td>
            <td colspan="2">F03</td>
        </tr>
        <tr>
            <td>简要描述</td>
            <td colspan="2">用户关闭个性化推荐功能</td>
        </tr>
        <tr>
            <td>参与者</td>
            <td colspan="2">用户</td>
        </tr>
        <tr>
            <td>涉众</td>
            <td colspan="2">无</td>
        </tr>
        <tr>
            <td>相关用例</td>
            <td colspan="2">无</td>
        </tr>
        <tr>
            <td>前置条件</td>
            <td colspan="2">用户已经注册并登录并开启个性化推荐</td>
        </tr>
        <tr>
            <td>后置条件</td>
            <td colspan="2">无</td>
        </tr>
        <tr>
            <td colspan="3">基本事件流 <br>
            <ol> 
                <li>用户进入系统主界面</li>
                <li>用户点击“个性化推荐”按钮</li>
                <li>用户“关闭个性化推荐”按钮</li>
                <li>系统关闭个性化推荐功能</li>
            </ol>
            </td>
        </tr>
        <tr>
            <td colspan="3">备选事件流 <br>
            <ol> 
                <li>代替3. 系统提示用户未登录，跳转到登录界面</li>
                <li>代替3. 系统提示用户已关闭个性化推荐功能</li>
            </ol>
            </td>
        </tr>
        <tr>
            <td colspan="3">补充约束 <br>
            无</td>
        </tr>
        <tr>
            <td colspan="3">待解决问题 <br>
            无 </td>
        </tr>
        <tr>
            <td colspan="3">相关图 <br>
            无 </td>
        </tr>
</table> 

### 4.7 通知系统

#### 4.7.1 新增消息

<div align="left">
  <p><strong>表4.50 新增消息RUCM表</strong></p>
</div>

<table><tbody>
        <tr >
            <td>作者：吴晨灿</td>
            <td>日期：2023年3月14日</td>
            <td>版本：1.0.0</td>
        </tr>
        <tr>
            <td>用例名</td>
            <td colspan="2">通知系统新增消息</td>
        </tr>
        <tr>
            <td>用例ID</td>
            <td colspan="2">G01</td>
        </tr>
        <tr>
            <td>简要描述</td>
            <td colspan="2">用户评论作品，用户回复评论，作品审核进度更新，对应用户的通知系统会更新一条消息</td>
        </tr>
        <tr>
            <td>参与者</td>
            <td colspan="2">用户，管理员</td>
        </tr>
        <tr>
            <td>涉众</td>
            <td colspan="2">无</td>
        </tr>
        <tr>
            <td>相关用例</td>
            <td colspan="2">管理员审核上传作品B05，用户评论作品E01，用户回复评论E03</td>
        </tr>
        <tr>
            <td>前置条件</td>
            <td colspan="2">用户已经注册，用户已经登录，对应事件先完成再触发通知</td>
        </tr>
        <tr>
            <td>后置条件</td>
            <td colspan="2">无</td>
        </tr>
        <tr>
            <td colspan="3">基本事件流 <br>
            <ol> 
                <li>发生用户评论作品，用户回复评论，作品审核进度更新事件</li>
                <li>系统监听到以上事件</li>
                <li>系统往通知系统中更新一条未读通知，并将通知与对应用户关联</li>
                <li>用户通知系统中未读通知数量加1</li>
            </ol>
        </td>
    </tr>
    <tr>
        <td colspan="3">备选事件流 <br>
			无
        </td>
    </tr>
    <tr>
        <td colspan="3">补充约束 <br>
            <ol>
                <li>评论作品对应作品存在，评论完成再触发通知</li>
                <li>回复评论对应回复存在，回复完成再触发通知</li>
                <li>作品审核进度更新对应审核事件存在，审核完成再触发通知</li>
            </ol>
        </td>
    </tr>
    <tr>
        <td colspan="3">待解决问题 <br>
        无
        </td>
    </tr>
    </tbody>
</table>

![需求分析G01](imgs/需求分析G01.png)

<div align="center">
  <p><strong>图4.16 新增消息活动图</strong></p>
</div>

#### 4.7.2 消息已读

<div align="left">
  <p><strong>表4.51 消息已读RUCM表</strong></p>
</div>

<table><tbody>
        <tr >
            <td>作者：吴晨灿</td>
            <td>日期：2023年3月14日</td>
            <td>版本：1.0.0</td>
        </tr>
        <tr>
            <td>用例名</td>
            <td colspan="2">通知系统消息已读</td>
        </tr>
        <tr>
            <td>用例ID</td>
            <td colspan="2">G02</td>
        </tr>
        <tr>
            <td>简要描述</td>
            <td colspan="2">用户查看通知系统消息，查看完成后消息状态更新为已读</td>
        </tr>
        <tr>
            <td>参与者</td>
            <td colspan="2">用户</td>
        </tr>
        <tr>
            <td>涉众</td>
            <td colspan="2">无</td>
        </tr>
        <tr>
            <td>相关用例</td>
            <td colspan="2">通知系统新增消息G01</td>
        </tr>
        <tr>
            <td>前置条件</td>
            <td colspan="2">用户已经注册，用户已经登录，通知系统中该消息存在且状态为未读</td>
        </tr>
        <tr>
            <td>后置条件</td>
            <td colspan="2">无</td>
        </tr>
        <tr>
            <td colspan="3">基本事件流 <br>
            <ol> 
                <li>用户查看通知系统中状态为未读的消息</li>
                <li>系统得知用户已经点开过该未读消息</li>
                <li>系统将数据库中该消息的状态更新为已读</li>
                <li>用户通知系统中未读消息数量减1</li>
            </ol>
        </td>
    </tr>
    <tr>
        <td colspan="3">备选事件流 <br>
			无
        </td>
    </tr>
    <tr>
        <td colspan="3">补充约束 <br>
            无
        </td>
    </tr>
    <tr>
        <td colspan="3">待解决问题 <br>
        无
        </td>
    </tr>
    </tbody>
</table>

#### 4.7.3 删除消息

<div align="left">
  <p><strong>表4.52 删除消息RUCM表</strong></p>
</div>

<table><tbody>
        <tr >
            <td>作者：吴晨灿</td>
            <td>日期：2023年3月14日</td>
            <td>版本：1.0.0</td>
        </tr>
        <tr>
            <td>用例名</td>
            <td colspan="2">通知系统删除消息</td>
        </tr>
        <tr>
            <td>用例ID</td>
            <td colspan="2">G03</td>
        </tr>
        <tr>
            <td>简要描述</td>
            <td colspan="2">用户评论作品，用户回复评论，作品审核进度更新，对应用户的通知系统会更新一条消息</td>
        </tr>
        <tr>
            <td>参与者</td>
            <td colspan="2">用户</td>
        </tr>
        <tr>
            <td>涉众</td>
            <td colspan="2">无</td>
        </tr>
        <tr>
            <td>相关用例</td>
            <td colspan="2">通知系统新增消息G01</td>
        </tr>
        <tr>
            <td>前置条件</td>
            <td colspan="2">用户已经注册，用户已经登录，通知系统中该消息存在</td>
        </tr>
        <tr>
            <td>后置条件</td>
            <td colspan="2">无</td>
        </tr>
        <tr>
            <td colspan="3">基本事件流 <br>
            <ol> 
                <li>用户进入通知系统界面</li>
                <li>选择一条通知系统中的消息删除</li>
                <li>系统从数据库中删除该消息</li>
                <li>用户通知系统界面中该通知消失</li>
            </ol>
        </td>
    </tr>
    <tr>
        <td colspan="3">备选事件流 <br>
			无
        </td>
    </tr>
    <tr>
        <td colspan="3">补充约束 <br>
			无
        </td>
    </tr>
    <tr>
        <td colspan="3">待解决问题 <br>
        无
        </td>
    </tr>
    </tbody>
</table>

## 5. 非功能需求

非功能性需求，是指软件产品为满足用户业务需求而必须具有且除功能需求以外的特性，包括安全性、可靠性、互操作性、健壮性等，在正常情况下这些条件都需要满足。

### 5.1 响应时间

1. 响应时间指功能完成的时间，和客户机器及服务器的带宽、请求的数据量、服务的重要性有关
2. 确定响应时间需要考虑到用户的感受和带宽的需求，如登录、点赞、评论，这类服务需要快速响应。对于可以流式加载且不需要一下子全部显示的图片，可以有较长的加载时间
3. 考虑到服务的带宽需求，登录、注册、点赞等账号管理、收藏管理等服务需要在0.5秒内响应，图片的显示应保持每张在0.5秒以内

### 5.2 可靠性

1. 软件采用Docker部署，单点失效的平均发生时间应该大于720小时，失效后不应丢失超过1%的数据

2. 在发生错误后，Docker应该能够自动重新启动，同时邮件报警给开发人员

3. 用户的数据持久化存储后，应该提供异地容灾备份

4. 在产品运行的过程中，服务器的磁盘占用率应小于80%，达到阈值后提醒运维人员进行扩容

### 5.3 安全保密性

1. 网页使用安全的HTTP请求，对用户的操作进行鉴权

2. 服务器正确开启防火墙和跨域访问，禁止非法链接，XSS攻击，SQL注入等功能

3. 使用知名的漏洞检测工具对源码进行检测，禁止使用有安全漏洞的包

4. 端到端加密，在服务端和客户端均加密存储用户的敏感数据

5. 前端使用混淆、压缩源码等方式发布，所有数据在后端重新验证，以防恶意篡改数据

6. 内部安全：禁止开发人员对源代码和用户数据进行传播

### 5.4 可维护性

1. 以科学的方法设计软件，科学管理开发人员，确保每个流程符合预期

2. 所有文档应该清晰可读、书写规范统一

3. 所有日志进行备份存储，保证出现问题时可以根据日志定位到错误发生的时间

4. 产品的开发严格按照模块进行，每个模块高内聚低耦合，便于扩展

### 5.5 交互设计需求

产品的交互设计应满足在展示表所列的信息和功能的同时，满足表5.1所示的交互设计需求。

<div align="left">
  <p><strong>表5.1 产品交互设计需求</strong></p>
</div>

| **需求描述** | **详细要求**                                                                                                     |
| -------- | ------------------------------------------------------------------------------------------------------------ |
| 主观需求     | （1）基于每个功能用户的访问频次，网页更符合人体工程学。<br />（2）考虑到用户的喜好和易读性，提供多种配色方案供用户选择。                                             |
| 功能需求     | （1）结合美学，设计出合适的信息、图标等元素的布局。重要功能应摆放在明显部位或易于联想到的部位。<br />（2）对于需求信息的呈现应有逻辑性和清晰性，结合图形与颜色的运用，使页面有层次感和轻重感。          |
| 习惯性需求    | （1）操作少，避免嵌套过多层级，要求用户点击三下及以下次数即可获得想要的信息。<br />（2）减少用户的键盘鼠标切换过程，大多数操作可以只通过鼠标完成。  <br />（3）存储Cookie等，便于记录用户的习惯。 |
| 增强粘性     | （1）根据用户访问过的图片、喜欢的图片，个性化推荐给用户可能喜欢的图片。<br />（2）鼓励用户进行分享，多多交流不同的使用AIGC的技巧。                                      |

### 5.6 界面设计需求

结合产品特点及交互性要求，产品的界面设计具体要考虑的内容如表所示：

<div align="left">
  <p><strong>表5.2 产品界面设计需求</strong></p>
</div>

| **名称** | **详细要求**                                   |
| ------ | ------------------------------------------ |
| 主题     | （1）风格统一。<br />（2）响应式布局。   <br />（3）信息有层次感。 |
| 图标     | 功能性图标：简洁、直观。                               |
| 色彩     | 色彩一致，颜色和谐。                                 |
| 文字     | 使用成熟的开源字体。                                 |


## 6. 运行环境规定

<div align="left">
  <p><strong>表6.1 运行环境规定</strong></p>
</div>

<table>
<tbody>
<tr>
    <td rowspan="2"><b>客户端</b></td>
    <td><b>硬件</b></td>
    <td>
    <b>最低配置：</b>
    <p/>
    <ol>
        <li>CPU: 8th Generation Intel® Core™ i7 Processors</li>
        <li>GPU: NVIDIA GeForce MX250 Graphics Card</li>
        <li>内存: 4GB</li>
    </ol>
    <b>推荐配置：</b>
    <p/>
    <ol>
        <li>CPU: Intel® Core™ i5-10600K Processor及以上</li>
        <li>GPU: NVIDIA GeForce GTX 1060 Graphics Cards及以上</li>
        <li>内存: 16GB及以上</li>
    </ol>
    </td>
</tr>
<tr>
    <td><b>软件</b></td>
    <td>
    <b>推荐配置：</b>
    <p/>
    <ol>
        <li>Chrome浏览器:  内核版本110.0.5481.178及以上</li>
        <li>Safari浏览器:  15.3版本及以上</li>
        <li>Firefox浏览器: 119.0版本及以上</li>
    </ol>
    </td>
</tr>
<tr>
    <td rowspan="2"><b>服务端</b></td>
    <td><b>硬件</b></td>
    <td>
    <b>推荐配置：</b>
    <p/>
    <ol>
        <li>CPU: Intel® Core™ i5-10600K Processor及以上</li>
        <li>GPU: NVIDIA GeForce GTX 2060 Graphics Cards及以上</li>
        <li>内存: 32GB及以上</li>
    </ol>
    </td>
</tr>
<tr>
    <td><b>软件</b></td>
    <td>
    <ol>
        <li>操作系统： Ubuntu 22.0.4</li>
        <li>Docker版本:  20.10.17版本</li>
    </ol>
    </td>
</tr>
</tboby>
</table>
