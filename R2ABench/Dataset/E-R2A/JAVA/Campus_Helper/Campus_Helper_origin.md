| 版本   | 提交日期   | 修改说明     | 编制人员    | 
| ------ | ---------- | ---------- | -------------- | 
| v1.0 | 2022.03.26 | 文档初稿 | H组全体人员 |
| v1.1 | 2022.03.26 | 修改文档细节，完善文档RUCM表和用例图，添加系统整体架构图和整体用例图 | H组全体人员|
| v1.2 | 2022.04.03 | 根据校历第5周的评审意见修改部分描述，重构商品管理部分  | H组全体人员 |
| v1.3 | 2022.04.03 | 补充完善自查发现的文档细节问题，更新需求评审表单  | 章哲源 |
| v1.4 | 2022.04.06 | 补充文档目录和文档版本迭代记录  | 章哲源 |

# 基于微信小程序的北航校园帮帮平台

## 目录

- [基于微信小程序的北航校园帮帮平台](#基于微信小程序的北航校园帮帮平台)
  - [目录](#目录)
  - [1 引言](#1-引言)
    - [1.1 编写目的](#11-编写目的)
    - [1.2 背景](#12-背景)
    - [1.3 目标与用户](#13-目标与用户)
    - [1.4 术语与定义](#14-术语与定义)
    - [1.5 参考资料](#15-参考资料)
    - [1.6 说明书结构](#16-说明书结构)
  - [2 总体描述](#2-总体描述)
    - [2.1 软件架构图](#21-软件架构图)
    - [2.2 系统总体用例图](#22-系统总体用例图)
    - [2.3 功能需求编号表](#23-功能需求编号表)
  - [3 功能性需求](#3-功能性需求)
    - [3.1 查看商品信息](#31-查看商品信息)
    - [3.2 订单模块](#32-订单模块)
      - [3.2.1 创建订单](#321-创建订单)
      - [3.2.2 修改订单备注](#322-修改订单备注)
      - [3.2.3 确认订单](#323-确认订单)
      - [3.2.4 取消订单](#324-取消订单)
    - [3.3 个人中心功能](#33-个人中心功能)
      - [3.3.1 用户查看收藏夹](#331-用户查看收藏夹)
      - [3.3.2 用户查看订单记录](#332-用户查看订单记录)
    - [3.4 商品管理功能](#34-商品管理功能)
      - [3.4.1 管理员查看平台商品总体情况](#341-管理员查看平台商品总体情况)
      - [3.4.2 查看单个商品信息](#342-查看单个商品信息)
      - [3.4.3 修改单个商品信息](#343-修改单个商品信息)
      - [3.4.4 删除单个商品信息](#344-删除单个商品信息)
    - [3.5 订单管理功能](#35-订单管理功能)
      - [3.5.1 管理员查看所有订单](#351-管理员查看所有订单)
      - [3.5.2 管理员查看单个订单](#352-管理员查看单个订单)
      - [3.5.3 管理员修改订单](#353-管理员修改订单)
    - [3.6 用户管理功能](#36-用户管理功能)
      - [3.6.1 管理员查看所有用户信息](#361-管理员查看所有用户信息)
      - [3.6.2 管理员查看单个用户信息](#362-管理员查看单个用户信息)
      - [3.6.3 管理员修改用户信息](#363-管理员修改用户信息)
  - [4 非功能性需求](#4-非功能性需求)
    - [4.1 安全性需求](#41-安全性需求)
    - [4.2 性能/容量需求](#42-性能容量需求)
    - [4.3 UI需求](#43-ui需求)
    - [4.4 其他需求](#44-其他需求)
    - [4.5 故障处理](#45-故障处理)
      - [4.5.1 硬件故障](#451-硬件故障)
      - [4.5.2 软件故障](#452-软件故障)
      - [4.5.3 故障处理流程](#453-故障处理流程)
  - [5 运行环境规定](#5-运行环境规定)
    - [5.1 用户硬件规定](#51-用户硬件规定)
    - [5.2 环境规定](#52-环境规定)

## 1 引言

本项目“北航校园帮帮平台”是基于微信小程序的交易平台。本软件需求规格说明书详细介绍了平台的任务目标，从多个角度分析功能需求，性能需求、故障处理等非功能性需求和支持的软硬件运行环境。

### 1.1 编写目的

编写此软件需求规格说明书是为了定制、规范软件开发的关键问题，具体化软件开发工作。本文档阐述了本项目使用背景及范围，明确本项目各项功能需求、性能需求、故障处理，旨在为用户、软件开发者及分析和测试人员对该软件的初始规定有一个共同的理解。具体而言，编写软件需求说明的目的是为所开发的软件提出：

* 软件设计总体要求，作为软件开发人员、软件测试人员相互了解的基础。
* 功能、性能要求，故障处理，运行环境，作为软件设计人员进行概要设计的依据。
* 软件确认测试的依据，项目预期功能的评估依据。

### 1.2 背景

本项目想法来源于小组成员在北航沙河校区读书期间的兼职经历。北航沙河校区地处京郊偏僻的沙河高教园，取快递以及取外卖等都需要出校门，因而也会有一些代取外卖以及代取快递甚至是送早餐的顺路小兼职。疫情期间，和沙河校区常态化封闭管理类似，北航本部校区也不再允许外卖员出入校，校内学生遇到了类似的需要到固定位置领取外卖以及快递的问题，所以迫切需要一个平台能帮忙代取快递和外卖。
另一方面，校内二手交易群虽有但杂，诸多群聊之中无用信息甚多，无法为用户提供检索等实用的信息搜寻功能，二手买卖全靠“运气”、“眼缘”等。

### 1.3 目标与用户

北航校园帮帮平台基于微信小程序开发框架，致力于为北航师生提供方便快捷的生活服务，主要目标如下：

- 通过“发布-接单”的方式为同学提供外卖以及快递的代取服务
- 提供外卖即时交易服务，帮助用户在无法及时取到外卖的情况下转让外卖
- 提供一个二手信息发布地，为用户提供一个较为规范可靠的交易信息获取方式

本平台主要面向以下两类用户：  

- 北航学生
- 北航教师以及家属


### 1.4 术语与定义

- 平台：基于微信小程序的校园帮帮平台，简称平台。
- 商品：平台上挂出的代取外卖、代取快递、待出售的二手物件统称为商品，前二者为跑腿商品，后者为二手商品。
- 用户：在校园帮帮平台拥有账号的使用者，在帮帮平台能进行浏览已挂出商品、发布商品、收藏商品等一系列操作。
  - 卖家：挂出商品的用户在某次交易中的身份称为卖家。
  - 顾客：用户在浏览商品时或看中某个商品后进行下一步操作时的身份称为顾客。
- 游客：在校园帮帮平台没有账号的使用者，在帮帮平台能进行查看商品等操作，但平台核心功能被限制，不能使用。
- 下单：用户看中某个商品后以顾客身份进行的下一步操作，下单后商品从商品列表消失，单件商品无法接受多次下单。
- 订单：某件商品在挂出后被某顾客看中并下单，则商品转化为订单。
  - 跑腿订单：跑腿商品下单后变为跑腿订单，卖家（挂出跑腿商品的用户）需要自行向顾客（实际帮助代取物品的用户）支付商品信息中明确的酬劳。
  - 二手订单：二手商品下单后变为二手订单，顾客（看中某件二手商品的用户）需要自行向卖家（挂出二手物品的用户）支付商品信息中明确的酬劳。
- 标签：描述商品相关的特性；是商品的属性之一，可以由用户新建，也可从平台已有的标签当中选取。
- 管理员：校园帮帮平台的管理者，负责对用户的违反法律法规的行为进行监督，包括违规商品信息等。
- 日志：记录管理员后台的管理操作，支持按多种条件检索。
- 注册：游客填写不重复用户名，密码和其它个人信息创建账户的过程。
- 登录：游客在登录界面填写用户名密码并经过平台身份权限验证的过程。
- 忘记密码：用户忘记了自己注册时所填写的密码，或者用户想更改自己账号的密码时，可在平台更改。
- 收藏商品：用户添加某些中意商品进入自己的收藏列表，方便日后重点查看或关注商品状态等信息。
- 取消收藏：用户将某件商品从自己的收藏列表移除的过程，表示用户不需要重点查看该商品的信息。
- 订单状态：指订单的相关状态，包括交易中、已完成等，订单在被确认后即变为交易中状态，在双方完成交易后则为已完成状态。
- 发布商品：指用户作为卖家身份时，根据自身需求编辑商品信息并在平台上发布的过程。
- 搜索用户：指游客或用户查找特定用户的过程；用户在输入用户名关键词后，平台会根据模糊匹配展示与之匹配的相关用户。
- 搜索商品：指游客或用户查找特定商品的过程；用户在输入商品关键词后，平台会根据模糊匹配展示与之相关的商品列表。
  - 按分类搜索商品：游客或用户输入/选择特定类型，系统显示该类型下所有商品内容，类型包括（代取商品、代取外卖，二手物品）；

  - 按标签搜索商品：游客或用户输入/选择特定标签，系统显示与此标签相关的所有商品，并按照时间由近及远的顺序排列；

  - 按时间搜索商品：游客或用户可以选择特定的时间段，5分钟内/半小时内/一天内/一周内，系统显示时间段发布的所有商品信息，并按时间由近及远的顺序排列；

  - 按用户搜索商品：游客或用户输入特定用户信息，系统会显示此用户发布的所有商品信息，同样按照时间顺序降序排列。

- QPS：Query Per Second 服务器的每秒请求数。

### 1.5 参考资料

[1]  中国国家标准化委员会.计算机软件需求规格说明：GB/T 9385-2008 [S]. 

[2]  中国国家标准化委员会.计算机软件文档编制规范：GB/T 8567-2006 [S]. 

[3]  中国国家标准化委员会.信息技术、软件生存周期过程及风险管理：GB/T 20918-2007[S].

[4]  中国国家标准化委员会.计算机软件测试规范：GB/T 15532-2008[S].

[5]  中国国家标准化委员会.软件工程及软件测量过程：GB/T 20917-2007[S].

[6]  微信小程序平台运营规范

[7]  微信小程序平台服务条款

[8]  腾讯微信软件许可及服务协议

[9]  Web编码规范：https://www.html.cn/archives/5361  

### 1.6 说明书结构

本项目需求规格说明书分为五个部分

- 第一章引言主要介绍软件需求说明书的编写目的，项目背景和目标，以及术语定义等。
- 第二章是对本小程序的总体描述，包括软件架构，系统的总体用例图和功能性需求编号表。
- 第三章详细介绍了本小程序开发的功能性需求，并给出用例图和对应的RUCM。
- 第四章详细介绍了本小程序开发的非功能性需求，包括安全性需求，性能/容量需求，UI需求和故障处理等。
- 第五章讲述了本项目支持的软硬件运行环境。

## 2 总体描述

### 2.1 软件架构图

为了提高开发速度，使软件有相当好的可维护性、易扩展性，我们将帮帮平台小程序设计为四层架构，分别是：展示层、业务层、数据层、数据实体层（数据库）。并绘制了北航校园帮帮平台的软件架构图,架构图如下图所示。

<div style="display:flex;justify-content:space-around">
  <img src="https://www.z4a.net/images/2022/03/23/7e0acfca8882c1940ec5c72236175930.png" />
</div>     

<center>图2-1 软件架构图</center>  

### 2.2 系统总体用例图

我们将系统划分为六大模块，系统的总体用例图如下所示。  

![](https://pad.degrowth.net/uploads/upload_eac48f5fee72c4f0dc92d1a4b12082c4.png)


<center>图2-2 系统总体用例图</center>  

### 2.3 功能需求编号表

功能性需求总体概览和编号如下表所示。

<center>表2-1 功能性编号表</center>
<table border="0" cellpadding="0" cellspacing="0">
    <tbody>
        <tr>
            <td><b>功能名称</b></td>
            <td><b>功能需求编号</b></td>
            <td><b>描述</b></td>
        </tr>
        <tr>
            <td>商品管理功能-查看商品信息</td>
            <td>ItemSelect-S1</td>
            <td>查看所有人已发布的商品</td>
        </tr>
        <tr>
            <td>订单功能-创建订单</td>
            <td>CreateOrder-O1</td>
            <td>用户选择结算商品的订单</td>
        </tr>
        <tr>
            <td>订单功能-修改订单备注</td>
            <td>UpdateOrder-O2</td>
            <td>用户在交易开始前修改订单备注</td>
        </tr>
        <tr>
            <td>订单功能-确认订单</td>
            <td>ConfirmOrder-O3</td>
            <td>用户收到订单进行确认</td>
        </tr>
        <tr>
            <td>订单功能-取消订单</td>
            <td>CancelOrder-O4</td>
            <td>在订单未被送出前取消订单</td>
        </tr>
        <tr>
            <td>个人中心功能-用户查看收藏夹</td>
            <td>SelectFavorite-F1</td>
            <td>用户查看自己添加进收藏夹的商品条目</td>
        </tr>
        <tr>
            <td>个人中心功能-用户查看订单</td>
            <td>SelectOrder-O5</td>
            <td>用户查看自己的订单记录</td>
        </tr>
        <tr>
            <td>商品管理功能-管理员查看商品总体信息</td>
            <td>AdminGeneralItemSelect-S2</td>
            <td>管理员查看平台商品总体情况</td>
        </tr>
        <tr>
            <td>商品管理功能-管理员查看商品</td>
            <td>AdminItemSelect-S3</td>
            <td>管理员查看平台商品内容</td>
        </tr>
        <tr>
            <td>商品管理功能-管理员修改订单</td>
            <td>AdminUpdateOrder-O6</td>
            <td>管理员修改单个订单信息</td>
        </tr>
        <tr>
            <td>用户管理功能-管理员修改用户信息</td>
            <td>AdminUpdateUser-U1</td>
            <td>管理员修改单个用户信息</td>
        </tr>
    </tbody>
</table>

## 3 功能性需求


### 3.1 查看商品信息
![查看商品信息用例](https://pad.degrowth.net/uploads/upload_6629fd9ffa3ff130210b25453b7eb7c1.png)







<center>图3-1 商品系统查看功能用例图</center>


<br/>
<br/>
<center>表3-1 查看热门商品RUCM表</center>

<table border="0" cellpadding="0" cellspacing="0">
  <tbody>
    <tr>
      <td colspan="4"><span lang="EN-US">Use Case Specification</span></td>
    </tr>
    <tr>
      <td><span lang="EN-US">Use Case Name</span></td>
      <td colspan="3">查看所有人已发布的热门商品</td>
    </tr>
    <tr>
      <td><span lang="EN-US">Brief Description</span></td>
      <td colspan="3">提供商品的信息，并在主页按一定的热门程度规则对商品进行排序，便于用户或游客进行查找和收藏，提升用户接单效率，其中只有注册用户拥有收藏或下单权限</td>
    </tr>
    <tr>
      <td><span lang="EN-US">Precondition</span></td>
      <td colspan="3">
        该功能需要事先定义好商品的热门度排序规则，以便于用户能快速浏览到自己想接的单，保证该规则涉及的时间、金额等信息准确，从而保证用户查看的商品信息的可靠性。</td>
    </tr>
    <tr>
      <td><span lang="EN-US">Primary Actor</span></td>
      <td colspan="3">用户、游客</td>
    </tr>
    <tr>
      <td><span lang="EN-US">Secondary Actors</span></td>
      <td colspan="3">无</td>
    </tr>
    <tr>
      <td><span lang="EN-US">Dependency</span></td>
      <td colspan="3">无</td>
    </tr>
    <tr>
      <td><span lang="EN-US">Generalization<span>&nbsp;</span></span></td>
      <td colspan="3">无</td>
    </tr>
    <tr>
      <td rowspan="6"><span lang="EN-US">Basic Flow</span></td>
      <td colspan="3"><span lang="EN-US">Steps</span></td>
    </tr>
    <tr>
      <td><span lang="EN-US">1</span></td>
      <td colspan="2">用户或游客进入主界面查看热门商品</td>
    </tr>
    <tr>
      <td>2</td>
      <td colspan="2">用户或游客进行商品选取进入详情页面</td>
    </tr>
    <tr>
      <td>3</td>
      <td colspan="2">用户或游客通过下拉、翻页等操作浏览该商品的信息</td>
    </tr>
    <tr>
      <td><span lang="EN-US">4</span></td>
      <td colspan="2">用户收藏该商品</td>
    </tr>
    <tr>
      <td colspan="2"><span lang="EN-US">PostCondition</span></td>
      <td>用户在收藏夹中能看到该商品</td>
    </tr>
    <tr>
      <td rowspan="4"><span lang="EN-US">Specific
          Alternative Flow alt1</span></td>
      <td><span lang="EN-US">RFS</span></td>
      <td colspan="2"><span lang="EN-US">1</span></td>
    </tr>
    <tr>
      <td><span lang="EN-US">1</span></td>
      <td colspan="2">用户或游客在首页热门商品界面点击返回</td>
    </tr>
    <tr>
      <td>2</td>
      <td colspan="2">ABORT</td>
    </tr>
    <tr>
      <td colspan="2"><span lang="EN-US">PostCondition</span></td>
      <td>无</td>
    </tr>
    <tr>
      <td rowspan="4"><span lang="EN-US">Specific
          Alternative Flow alt2</span></td>
      <td><span lang="EN-US">RFS</span></td>
      <td colspan="2"><span lang="EN-US">3</span></td>
    </tr>
    <tr>
      <td><span lang="EN-US">1</span></td>
      <td colspan="2">用户或游客在商品详细信息界面点击返回</td>
    </tr>
    <tr>
      <td><span lang="EN-US">2</span></td>
      <td colspan="2">RESUME STEP 1</td>
    </tr>
    <tr>
      <td colspan="2"><span lang="EN-US">PostCondition</span></td>
      <td>无</td>
    </tr>
  </tbody>
</table>

<center>表3-2 按分类查看商品RUCM表</center>

<table border="0" cellpadding="0" cellspacing="0">
  <tbody>
    <tr>
      <td colspan="4"><span lang="EN-US">Use Case Specification</span></td>
    </tr>
    <tr>
      <td><span lang="EN-US">Use Case Name</span></td>
      <td colspan="3">按分类查看所有人已发布的商品</td>
    </tr>
    <tr>
      <td><span lang="EN-US">Brief Description</span></td>
      <td colspan="3">提供商品的信息，并在主页按商品位置、金额、物品种类等对商品进行分类，便于用户进行筛选查找，提升用户接单效率，只有注册用户可以接单</td>
    </tr>
    <tr>
      <td><span lang="EN-US">Precondition</span></td>
      <td colspan="3">
        该功能需要保证所有用户发布商品的实际需求、金额、定位等信息准确无误，才能保证分类的正确性，从而保证检索到的商品信息的可靠性。</td>
    </tr>
    <tr>
      <td><span lang="EN-US">Primary Actor</span></td>
      <td colspan="3">用户、游客</td>
    </tr>
    <tr>
      <td><span lang="EN-US">Secondary Actors</span></td>
      <td colspan="3">无</td>
    </tr>
    <tr>
      <td><span lang="EN-US">Dependency</span></td>
      <td colspan="3">无</td>
    </tr>
    <tr>
      <td><span lang="EN-US">Generalization<span>&nbsp;</span></span></td>
      <td colspan="3">无</td>
    </tr>
    <tr>
      <td rowspan="7"><span lang="EN-US">Basic Flow</span></td>
      <td colspan="3"><span lang="EN-US">Steps</span></td>
    </tr>
    <tr>
      <td>1</td>
      <td colspan="2">用户或游客进入主界面，进入商品分类入口</td>
    </tr>
    <tr>
      <td>2</td>
      <td colspan="2">用户或游客选择商品分类，查看该分类下商品的列表展示</td>
    </tr>
        <tr>
      <td>3</td>
      <td colspan="2">用户或游客进行商品选取，查看该商品的详细信息展示</td>
    </tr>
    <tr>
      <td>4</td>
      <td colspan="2">用户或游客通过下拉、翻页等操作浏览该商品的信息</td>
    </tr>
    <tr>
      <td>5</td>
      <td colspan="2">用户收藏该商品</td>
    </tr>
    <tr>
      <td colspan="2"><span lang="EN-US">PostCondition</span></td>
      <td>用户收藏夹中有该商品</td>
    </tr>
    <tr>
      <td rowspan="4"><span lang="EN-US">Specific
          Alternative Flow</span></td>
      <td><span lang="EN-US">RFS</span></td>
      <td colspan="2"><span lang="EN-US">2</span></td>
    </tr>
    <tr>
      <td><span lang="EN-US">1</span></td>
      <td colspan="2">用户或游客在商品分类界面点击返回</td>
    </tr>
    <tr>
      <td><span lang="EN-US">2</span></td>
      <td colspan="2">RESUME STEP 3</td>
    </tr>
    <tr>
      <td colspan="2"><span lang="EN-US">PostCondition</span></td>
      <td>无</td>
    </tr>
    <tr>
      <td rowspan="4"><span lang="EN-US">Specific
          Alternative Flow</span></td>
      <td><span lang="EN-US">RFS</span></td>
      <td colspan="2"><span lang="EN-US">4</span></td>
    </tr>
    <tr>
      <td><span lang="EN-US">1</span></td>
      <td colspan="2">用户或游客在商品详细信息界面点击返回</td>
    </tr>
    <tr>
      <td><span lang="EN-US">2</span></td>
      <td colspan="2">RESUME STEP 2</td>
    </tr>
    <tr>
      <td colspan="2"><span lang="EN-US">PostCondition</span></td>
      <td>无</td>
    </tr>
  </tbody>
</table>  

### 3.2 订单模块   

订单功能用例图如下
![](https://pad.degrowth.net/uploads/upload_5170ffb395052e864a406dd36f7b7a29.png)

<br />
<center>图3-2 订单用例图</center>

#### 3.2.1 创建订单   

用户可以选择想要结算的商品，填写相关信息后提交订单。

<center>表3-3 创建订单RUCM表</center>

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
  <td colspan="3"   >创建订单</td>
 </tr>
 <tr  >
  <td    >Brief Description</td>
  <td colspan="3"   >用户在选择好订单相关信息（商品属性、收货地址、收货人联系方式等）后可以点击提交按钮，创建订单进而购买商品</td>
 </tr>
 <tr  >
  <td    >Precondition</td>
  <td colspan="3"   >用户已登录</td>
 </tr>
 <tr  >
  <td    >Primary Actor</td>
  <td colspan="3"   >用户</td>
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
  <td rowspan="10"    >Basic Flow</td>
  <td colspan="3"   >steps</td>
 </tr>
 <tr  >
  <td    >1</td>
  <td colspan="2"   >用户选择商品，点击购买按钮</td>
 </tr>
 <tr  >
  <td    >2</td>
  <td colspan="2"   >系统 <b style="color: purple"> VALIDATE THAT</b> 商品能被购买</td>
 </tr>
 <tr  >
  <td    >3</td>
  <td colspan="2"   >用户填写订单相关信息，点击提交按钮</td>
 </tr>
 <tr  >
  <td    >4</td>
  <td colspan="2"   >系统 <b style="color: purple">VALIDATE THAT</b> 用户输入有效</td>
 </tr>
 <tr  >
 <tr  >
  <td    >5</td>
  <td colspan="2"   >系统在数据库插入订单记录</td>
 </tr>
 <tr  >
 <tr  >
  <td    >6</td>
  <td colspan="2"   >进入订单创建成功页面</td>
 </tr>
 <tr  >
  <td  >PostCondition</td>
  <td colspan="2"  >订单创建成功，订单列表中有该订单</td>
 </tr>
 <tr  >
  <td rowspan="4"    >Specific Alternative Flow</td>
  <td   >RFS</td>
  <td colspan="2"   >2</td>
 </tr>
 <tr  >
  <td    >1</td>
  <td colspan="2"   >系统提示订单中有商品已下架/过期/售出</td>
 </tr>
    <tr  >
  <td    >2</td>
  <td colspan="2"   >RESUME STEP 1</td>
 </tr>
 <tr  >
  <td  >PostCondition</td>
  <td  colspan="2"    >无</td>
</tr>

 <tr  >
  <td rowspan="4"    >Specific Alternative Flow</td>
  <td   >RFS</td>
  <td colspan="2"   >4</td>
 </tr>
 <tr  >
  <td    >1</td>
  <td colspan="2"   >系统提示用户输入不符合规范</td>
 </tr>
    <tr  >
  <td    >2</td>
  <td colspan="2"   >RESUME STEP 3</td>
 </tr>
 <tr  >
  <td  >PostCondition</td>
  <td  colspan="2"    >无</td>
 </tr>
</tbody></table>

#### 3.2.2 修改订单备注  

用户可以在商品尚未发出/被承接时修改订单备注，添加自己的定制化需求。

<center>表3-4 修改订单备注RUCM表</center>

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
  <td colspan="3"   >修改订单备注</td>
 </tr>
 <tr  >
  <td    >Brief Description</td>
  <td colspan="3"   >在订单页面，用户通过点击某一已提交订单的编辑按钮，可以修改该订单的备注</td>
 </tr>
 <tr  >
  <td    >Precondition</td>
  <td colspan="3"   >用户已登录，有已经创建的未送出/结束订单</td>
 </tr>
 <tr  >
  <td    >Primary Actor</td>
  <td colspan="3"   >用户</td>
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
  <td rowspan="10"    >Basic Flow</td>
  <td colspan="3"   >steps</td>
 </tr>
 <tr  >
  <td    >1</td>
  <td colspan="2"   >用户在订单列表页选择订单，点击修改按钮</td>
 </tr>
 <tr  >
  <td    >2</td>
  <td colspan="2"   >系统 <b style="color: purple"> VALIDATE THAT</b> 订单未送出</td>
 </tr>
 <tr  >
  <td    >3</td>
  <td colspan="2"   >用户修改订单备注，点击确认按钮</td>
 </tr>
 <tr  >
  <td    >4</td>
  <td colspan="2"   >系统 <b style="color: purple"> VALIDATE THAT</b> 用户输入有效</td>
 </tr>
 <tr  >
 <tr  >
  <td    >5</td>
  <td colspan="2"   >系统在数据库更新订单记录</td>
 </tr>
 <tr  >
 <tr  >
  <td    >6</td>
  <td colspan="2"   >返回订单列表页面</td>
 </tr>
 <tr  >
  <td  >PostCondition</td>
  <td colspan="2"  >无</td>
 </tr>
 <tr  >
  <td rowspan="4"    >Specific Alternative Flow</td>
  <td   >RFS</td>
  <td colspan="2"   >2</td>
 </tr>
 <tr  >
  <td    >1</td>
  <td colspan="2"   >系统提示订单已送出/结束，不能修改订单</td>
 </tr>
    <tr  >
  <td    >2</td>
  <td colspan="2"   >RESUME STEP 1</td>
 </tr>
 <tr  >
  <td  >PostCondition</td>
  <td  colspan="2"    >无</td>
    </tr>

 <tr  >
  <td rowspan="4"    >Specific Alternative Flow</td>
  <td   >RFS</td>
  <td colspan="2"   >4</td>
 </tr>
 <tr  >
  <td    >1</td>
  <td colspan="2"   >系统提示用户输入不符合规范</td>
 </tr>
    <tr  >
  <td    >2</td>
  <td colspan="2"   >RESUME STEP 3</td>
 </tr>
 <tr  >
  <td  >PostCondition</td>
  <td  colspan="2"    >无</td>
 </tr>
</tbody></table>

#### 3.2.3 确认订单  

用户在收到订单中所有商品后，在系统中确认订单。  

<center>表3-5 确认订单RUCM表</center>

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
  <td colspan="3"   >确认订单</td>
 </tr>
 <tr  >
  <td    >Brief Description</td>
  <td colspan="3"   >在一个订单的详情页面，用户可以在收到商品后，确认订单已经完成</td>
 </tr>
 <tr  >
  <td    >Precondition</td>
  <td colspan="3"   >用户已登录，有已送出的订单</td>
 </tr>
 <tr  >
  <td    >Primary Actor</td>
  <td colspan="3"   >用户</td>
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
  <td colspan="2"   >用户在订单列表页选择未完成订单点击确认按钮</td>
 </tr>
 <tr  >
  <td    >2</td>
  <td colspan="2"   >系统在数据库更新订单状态</td>
 </tr>
 <tr  >
  <td    >3</td>
  <td colspan="2"   >返回订单列表页面</td>
 </tr>
 <tr  >
  <td  >PostCondition</td>
  <td colspan="2"  >无</td>
 </tr>

</tbody></table>

#### 3.2.4 取消订单  

用户在创建订单后，如果发现自己不想购买订单中的二手商品，可以在该订单未被送出前取消该订单。  

<center>表3-6 取消订单RUCM表</center>

<table border="0" cellpadding="0" cellspacing="0"  >
 <colgroup><col  >
 <col  span="2" >
 <col  >
 </colgroup><tbody>
<tr  >
  <td colspan="4"    >Use
  Case Specification</td>
 </tr>
 <tr  >
  <td    >Use Case Name</td>
  <td colspan="3"   >取消订单</td>
 </tr>
 <tr  >
  <td    >Brief Description</td>
  <td colspan="3"   >在一个订单的详情页面，用户可以在订单中商品尚未发出前，取消该订单</td>
 </tr>
 <tr  >
  <td    >Precondition</td>
  <td colspan="3"   >用户已登录，有已经创建的未送出/结束订单</td>
 </tr>
 <tr  >
  <td    >Primary Actor</td>
  <td colspan="3"   >用户</td>
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
  <td colspan="2"   >用户在订单列表页选择未送出的订单并点击取消按钮</td>
 </tr>
 <tr  >
  <td    >2</td>
  <td colspan="2"   >系统 <b style="color: purple"> VALIDATE THAT</b> 订单中商品尚未送出</td>
 </tr>
 <tr  >
  <td    >3</td>
  <td colspan="2"   >系统更新数据库中订单状态</td>
 </tr>
<tr  >
  <td    >4</td>
  <td colspan="2"   >系统提示取消订单成功</td>
 </tr>
    <tr  >
  <td    >5</td>
  <td colspan="2"   >系统返回订单列表页面</td>
 </tr>
 <tr  >
  <td  >PostCondition</td>
  <td colspan="2"  >无</td>
 </tr>
    <tr  >
  <td rowspan="4"    >Specific Alternative Flow</td>
  <td   >RFS</td>
  <td colspan="2"   >2</td>
 </tr>
 <tr  >
  <td    >1</td>
  <td colspan="2"   >系统提示订单已送出/结束，不可取消</td>
 </tr>
    <tr  >
  <td    >2</td>
  <td colspan="2"   >RESUME STEP 1</td>
 </tr>
 <tr  >
  <td  >PostCondition</td>
  <td  colspan="2"    >无</td>
</tr>

</tbody></table>



### 3.3 个人中心功能

个人中心功能用例图如下

<div style="display:flex;justify-content:space-around">
  <img src="https://www.z4a.net/images/2022/03/27/Use-Cases.png" />
</div>   

<center>图3-3 个人中心功能用例图</center>



#### 3.3.1 用户查看收藏夹

辅助用户查看自己添加进收藏夹的商品条目。

<center>表3-7 用户查看收藏夹RUCM表</center>

<table border="0" cellpadding="0" cellspacing="0"  >
 <colgroup><col  >
 <col  span="2" >
 <col  >
 </colgroup><tbody><tr  >
  <td colspan="4"    >Use Case Specification</td>
 </tr>
 <tr  >
  <td    >Use Case
  Name</td>
  <td colspan="3"  >用户查看收藏夹</td>
 </tr>
 <tr  >
  <td    >Brief
  Description</td>
  <td colspan="3"  >在个人中心页面，用户点击收藏夹图标或者文字按钮可以跳转至收藏夹页面，进而查看自己添加进收藏夹的商品条目</td>
 </tr>
 <tr  >
  <td    >Precondition</td>
  <td colspan="3"  >用户已登录</td>
 </tr>
 <tr  >
  <td    >Primary
  Actor</td>
  <td colspan="3"  >用户</td>
 </tr>
 <tr  >
  <td    >Secondary
  Actors</td>
  <td colspan="3"  >无</td>
 </tr>
 <tr  >
  <td    >Dependency</td>
  <td colspan="3"  >无</td>
 </tr>
 <tr  >
  <td    >Generalization<span >&nbsp;</span></td>
  <td colspan="3"  >无</td>
 </tr>
 <tr  >
  <td rowspan="5"    >Basic Flow</td>
  <td colspan="3"  >Steps</td>
 </tr>
 <tr  >
  <td   >1</td>
  <td colspan="2"  >用户进入个人中心页面</td>
 </tr>
 <tr  >
  <td   >2</td>
  <td colspan="2"   >用户点击收藏夹图标或者文字按钮，进入收藏夹界面。</td>
 </tr>
 <tr  >
  <td   >3</td>
  <td colspan="2"   >用户可查看收藏夹中的商品条目</td>
 </tr>
 <tr  >
  <td colspan="2"   >PostCondition</td>
  <td >无</td>
 </tr>
 <tr  >
  <td rowspan="4"    >Specific Alternative Flow</td>
  <td   >RFS</td>
  <td colspan="2"   >2</td>
 </tr>
 <tr  >
  <td    >1</td>
  <td colspan="2"   >用户在收藏夹界面点击返回</td>
 </tr>
 <tr  >
  <td    >2</td>
  <td colspan="2"   >RESUME STEP 1</td>
 </tr>
 <tr  >
  <td colspan="2"    >PostCondition</td>
  <td   >无</td>
 </tr>
</tbody></table>

#### 3.3.2 用户查看订单记录

辅助用户查看自己所有的订单记录。

<center>表3-8 用户查看订单记录RUCM表</center>

<table border="0" cellpadding="0" cellspacing="0"  >
 <colgroup><col  >
 <col  span="2" >
 <col  >
 </colgroup><tbody><tr  >
  <td colspan="4"    >Use Case Specification</td>
 </tr>
 <tr  >
  <td    >Use Case
  Name</td>
  <td colspan="3"  >用户查看订单记录</td>
 </tr>
 <tr  >
  <td    >Brief
  Description</td>
  <td colspan="3"  >在个人中心页面，用户点击订单记录按钮可以跳转至订单记录页面，进而查看自己所有的订单记录</td>
 </tr>
 <tr  >
  <td    >Precondition</td>
  <td colspan="3"  >用户已登录</td>
 </tr>
 <tr  >
  <td    >Primary
  Actor</td>
  <td colspan="3"  >用户</td>
 </tr>
 <tr  >
  <td    >Secondary
  Actors</td>
  <td colspan="3"  >无</td>
 </tr>
 <tr  >
  <td    >Dependency</td>
  <td colspan="3"  >无</td>
 </tr>
 <tr  >
  <td    >Generalization<span >&nbsp;</span></td>
  <td colspan="3"  >无</td>
 </tr>
 <tr  >
  <td rowspan="5"    >Basic Flow</td>
  <td colspan="3"  >Steps</td>
 </tr>
 <tr  >
  <td   >1</td>
  <td colspan="2"  >用户进入个人中心页面</td>
 </tr>
 <tr  >
  <td   >2</td>
  <td colspan="2"   >用户点击订单记录按钮，进入订单记录界面</td>
 </tr>
 <tr  >
  <td   >3</td>
  <td colspan="2"   >用户可查看自己所有的订单记录</td>
 </tr>
 <tr  >
  <td colspan="2"   >PostCondition</td>
  <td >无</td>
 </tr>
 <tr  >
  <td rowspan="4"    >Specific Alternative Flow</td>
  <td   >RFS</td>
  <td colspan="2"   >2</td>
 </tr>
 <tr  >
  <td    >1</td>
  <td colspan="2"   >用户在订单记录点击返回</td>
 </tr>
 <tr  >
  <td    >2</td>
  <td colspan="2"   >RESUME STEP 1</td>
 </tr>
 <tr  >
  <td colspan="2"    >PostCondition</td>
  <td   >无</td>
 </tr>
</tbody></table>







### 3.4 商品管理功能

负责校园帮帮平台的商品管理，商品主要包括平台上架的取快递/外卖请求以及二手市场上挂出的二手商品，功能内容主要包括所有商品情况的查看与检索，违规商品的删除以及商品条目内容的修改。
商品管理功能用例图如下。
![](https://pad.degrowth.net/uploads/upload_bb879d777096aed76db6af333f1a3b22.png)

<center>图3-4 商品管理功能用例图</center>


#### 3.4.1 管理员查看平台商品总体情况

管理员查看平台上架商品整体情况，包括商品总数、代取快递请求数、代取外卖请求数、待出售二手商品数目。

<center>表3-9 管理员查看平台商品总体情况RUCM表</center>

<table border="0" cellpadding="0" cellspacing="0">
  <tbody>
    <tr>
      <td colspan="4"><span lang="EN-US">Use Case Specification</span></td>
    </tr>
    <tr>
      <td><span lang="EN-US">Use Case Name</span></td>
      <td colspan="3">管理员查看平台商品总体情况</td>
    </tr>
    <tr>
      <td><span lang="EN-US">Brief Description</span></td>
      <td colspan="3">在商品管理页面，管理员查看平台上架商品整体情况，包括商品总数、代取快递挂单数、代取外卖挂单数、待出售二手商品数目</td>
    </tr>
    <tr>
      <td><span lang="EN-US">Precondition</span></td>
      <td colspan="3">
        管理员需要以拥有管理员权限的账号登录</td>
    </tr>
    <tr>
      <td><span lang="EN-US">Primary Actor</span></td>
      <td colspan="3">管理员</td>
    </tr>
    <tr>
      <td><span lang="EN-US">Secondary Actors</span></td>
      <td colspan="3">无</td>
    </tr>
    <tr>
      <td><span lang="EN-US">Dependency</span></td>
      <td colspan="3">无</td>
    </tr>
    <tr>
      <td><span lang="EN-US">Generalization<span>&nbsp;</span></span></td>
      <td colspan="3">无</td>
    </tr>
    <tr>
      <td rowspan="6"><span lang="EN-US">Basic Flow</span></td>
      <td colspan="3"><span lang="EN-US">Steps</span></td>
    </tr>
    <tr>
      <td><span lang="EN-US">1</span></td>
      <td colspan="2">管理员进入管理员界面</td>
    </tr>
    <tr>
      <td>2</td>
      <td colspan="2">管理员界面直接展示平台商品整体情况，包括商品总数、代取快递挂单数、代取外卖挂单数、待出售二手商品数目</td>
    </tr>
    <tr>
      <td>3</td>
      <td colspan="2">管理员通过下拉、翻页等操作浏览商品情况</td>
    </tr>
    <tr>
    </tr>
    <tr>
      <td colspan="2"><span lang="EN-US">PostCondition</span></td>
      <td>无</td>
    </tr>
    <tr>
      <td rowspan="4"><span lang="EN-US">Specific
          Alternative Flow</span></td>
      <td><span lang="EN-US">RFS</span></td>
      <td colspan="2"><span lang="EN-US">2</span></td>
    </tr>
    <tr>
      <td><span lang="EN-US">1</span></td>
      <td colspan="2">管理员在管理员界面点击退出</td>
    </tr>
    <tr>
      <td>2</td>
      <td colspan="2">ABORT</td>
    </tr>
    <tr>
      <td colspan="2"><span lang="EN-US">PostCondition</span></td>
      <td>无</td>
    </tr>
  </tbody>
</table>


#### 3.4.2 查看单个商品信息  
管理员查看某个上架商品的具体信息，也可以根据发布者、商品名、商品状态等关键字按类进行检索。

<center>表3-10 管理员查看单个商品信息RUCM表</center>

<table border="0" cellpadding="0" cellspacing="0">
  <tbody>
    <tr>
      <td colspan="4"><span lang="EN-US">Use Case Specification</span></td>
    </tr>
    <tr>
      <td><span lang="EN-US">Use Case Name</span></td>
      <td colspan="3">管理员查看单个商品信息</td>
    </tr>
    <tr>
      <td><span lang="EN-US">Brief Description</span></td>
      <td colspan="3">管理员可以查看某个商品的详情</td>
    </tr>
    <tr>
      <td><span lang="EN-US">Precondition</span></td>
      <td colspan="3">
        管理员需要以拥有管理员权限的账号登录，系统中商品数目大于等于1</td>
    </tr>
    <tr>
      <td><span lang="EN-US">Primary Actor</span></td>
      <td colspan="3">管理员</td>
    </tr>
    <tr>
      <td><span lang="EN-US">Secondary Actors</span></td>
      <td colspan="3">无</td>
    </tr>
    <tr>
      <td><span lang="EN-US">Dependency</span></td>
      <td colspan="3">无</td>
    </tr>
    <tr>
      <td><span lang="EN-US">Generalization<span>&nbsp;</span></span></td>
      <td colspan="3">无</td>
    </tr>
    <tr>
      <td rowspan="6"><span lang="EN-US">Basic Flow</span></td>
      <td colspan="3"><span lang="EN-US">Steps</span></td>
    </tr>
    <tr>
      <td><span lang="EN-US">1</span></td>
      <td colspan="2">管理员进入商品列表页面</td>
    </tr>
    <tr>
      <td>2</td>
      <td colspan="2">管理员点击某一商品条目</td>
    </tr>
    <tr>
      <td>3</td>
      <td colspan="2">系统跳转至该商品详情页</td>
    </tr>
    <tr>
    </tr>
    <tr>
      <td colspan="2"><span lang="EN-US">PostCondition</span></td>
      <td>无</td>
    </tr>
  </tbody>
</table>

#### 3.4.3 修改单个商品信息  
管理员在商品详情页点击修改按钮，可对商品信息进行修改。

<center>表3-11 管理员修改单个商品信息RUCM表</center>

<table border="0" cellpadding="0" cellspacing="0">
  <tbody>
    <tr>
      <td colspan="4"><span lang="EN-US">Use Case Specification</span></td>
    </tr>
    <tr>
      <td><span lang="EN-US">Use Case Name</span></td>
      <td colspan="3">管理员修改单个商品信息</td>
    </tr>
    <tr>
      <td><span lang="EN-US">Brief Description</span></td>
      <td colspan="3">管理员可以修改某个商品的详情</td>
    </tr>
    <tr>
      <td><span lang="EN-US">Precondition</span></td>
      <td colspan="3">
        管理员需要以拥有管理员权限的账号登录，系统中商品数目大于等于1</td>
    </tr>
    <tr>
      <td><span lang="EN-US">Primary Actor</span></td>
      <td colspan="3">管理员</td>
    </tr>
    <tr>
      <td><span lang="EN-US">Secondary Actors</span></td>
      <td colspan="3">无</td>
    </tr>
    <tr>
      <td><span lang="EN-US">Dependency</span></td>
      <td colspan="3">无</td>
    </tr>
    <tr>
      <td><span lang="EN-US">Generalization<span>&nbsp;</span></span></td>
      <td colspan="3">无</td>
    </tr>
    <tr>
      <td rowspan="9"><span lang="EN-US">Basic Flow</span></td>
      <td colspan="3"><span lang="EN-US">Steps</span></td>
    </tr>
    <tr>
      <td><span lang="EN-US">1</span></td>
      <td colspan="2">管理员进入商品列表页面</td>
    </tr>
    <tr>
      <td>2</td>
      <td colspan="2">管理员点击某一商品条目</td>
    </tr>
    <tr>
      <td>3</td>
      <td colspan="2">系统跳转至该商品详情页</td>
    </tr>
    <tr>
        <td>4</td>
        <td colspan="2">管理员点击修改按钮</td>
    </tr>
      <tr>
        <td>5</td>
        <td colspan="2">管理员修改商品信息，点击确认按钮</td>
    </tr>
      <tr>
        <td>6</td>
        <td colspan="2">系统<b style="color:purple">VALIDATE THAT</b>输入有效</td>
    </tr>
      <tr>
        <td>7</td>
        <td colspan="2">系统提示修改成功，返回该商品详情页面</td>
    </tr>
    <tr>
      <td colspan="2"><span lang="EN-US">PostCondition</span></td>
      <td>无</td>
    </tr>
      <tr  >
  <td rowspan="4"    >Specific Alternative Flow</td>
  <td   >RFS</td>
  <td colspan="2"   >6</td>
 </tr>
 <tr  >
  <td    >1</td>
  <td colspan="2"   >系统提示输入不符合规范</td>
 </tr>
 <tr  >
  <td    >2</td>
  <td colspan="2"   >RESUME STEP 5</td>
 </tr>
 <tr  >
  <td colspan="2"    >PostCondition</td>
  <td   >无</td>
 </tr>
  </tbody>
</table>

#### 3.4.4 删除单个商品信息  
管理员在商品列表页面可以对商品进行删除，删除操作需要二次确认。

<center>表3-12 管理员删除商品信息RUCM表</center>

<table border="0" cellpadding="0" cellspacing="0">
  <tbody>
    <tr>
      <td colspan="4"><span lang="EN-US">Use Case Specification</span></td>
    </tr>
    <tr>
      <td><span lang="EN-US">Use Case Name</span></td>
      <td colspan="3">管理员删除商品</td>
    </tr>
    <tr>
      <td><span lang="EN-US">Brief Description</span></td>
      <td colspan="3">管理员可以删除单个或一批商品</td>
    </tr>
    <tr>
      <td><span lang="EN-US">Precondition</span></td>
      <td colspan="3">
        管理员需要以拥有管理员权限的账号登录，系统中商品数目大于等于1</td>
    </tr>
    <tr>
      <td><span lang="EN-US">Primary Actor</span></td>
      <td colspan="3">管理员</td>
    </tr>
    <tr>
      <td><span lang="EN-US">Secondary Actors</span></td>
      <td colspan="3">无</td>
    </tr>
    <tr>
      <td><span lang="EN-US">Dependency</span></td>
      <td colspan="3">无</td>
    </tr>
    <tr>
      <td><span lang="EN-US">Generalization<span>&nbsp;</span></span></td>
      <td colspan="3">无</td>
    </tr>
    <tr>
      <td rowspan="7"><span lang="EN-US">Basic Flow</span></td>
      <td colspan="3"><span lang="EN-US">Steps</span></td>
    </tr>
    <tr>
      <td><span lang="EN-US">1</span></td>
      <td colspan="2">管理员进入商品列表页面</td>
    </tr>
    <tr>
      <td>2</td>
      <td colspan="2">管理员点击某一商品条目中的删除按钮或批量选择商品后点击删除按钮</td>
    </tr>
    <tr>
      <td>3</td>
      <td colspan="2">系统提示管理员二次确认删除</td>
    </tr>
    <tr>
        <td>4</td>
        <td colspan="2">管理员点击确认按钮</td>
    </tr>
      <tr>
        <td>5</td>
        <td colspan="2">系统删除对应商品，提示删除成功，刷新商品列表页面</td>
    </tr>
    <tr>
      <td colspan="2"><span lang="EN-US">PostCondition</span></td>
      <td>无</td>
    </tr>
  </tbody>
</table>



### 3.5 订单管理功能
![](https://pad.degrowth.net/uploads/upload_252e5522a92da426b9716ea1c327b0cf.png)
<center>图3-5 订单管理功能用例图</center>  

#### 3.5.1 管理员查看所有订单

<center>表3-13 管理员查看所有订单RUCM表</center>  
<br>
<table border="0" cellpadding="0" cellspacing="0">
  <tbody>
    <tr>
      <td colspan="4"><span lang="EN-US">Use Case Specification</span></td>
    </tr>
    <tr>
      <td><span lang="EN-US">Use Case Name</span></td>
      <td colspan="3">管理员查看所有订单</td>
    </tr>
    <tr>
      <td><span lang="EN-US">Brief Description</span></td>
      <td colspan="3">管理员查看所有订单</td>
    </tr>
    <tr>
      <td><span lang="EN-US">Precondition</span></td>
      <td colspan="3">
        管理员需要以拥有管理员权限的账号登录</td>
    </tr>
    <tr>
      <td><span lang="EN-US">Primary Actor</span></td>
      <td colspan="3">管理员</td>
    </tr>
    <tr>
      <td><span lang="EN-US">Secondary Actors</span></td>
      <td colspan="3">无</td>
    </tr>
    <tr>
      <td><span lang="EN-US">Dependency</span></td>
      <td colspan="3">无</td>
    </tr>
    <tr>
      <td><span lang="EN-US">Generalization<span>&nbsp;</span></span></td>
      <td colspan="3">无</td>
    </tr>
    <tr>
      <td rowspan="5"><span lang="EN-US">Basic Flow</span></td>
      <td colspan="3"><span lang="EN-US">Steps</span></td>
    </tr>
    <tr>
      <td><span lang="EN-US">1</span></td>
      <td colspan="2">管理员进入订单管理界面</td>
    </tr>
    <tr>
      <td>2</td>
      <td colspan="2">管理员点击查看平台所有订单按钮</td>
    </tr>
    <tr>
      <td>3</td>
      <td colspan="2">界面根据创建时间由后到前的顺序展示平台所有订单信息</td>
    </tr>
    <tr>
      <td colspan="2"><span lang="EN-US">PostCondition</span></td>
      <td>无</td>
    </tr>
  </tbody>
</table>   

#### 3.5.2 管理员查看单个订单  

<center>表3-14 管理员查看单个订单RUCM表</center>  
<br>
<table border="0" cellpadding="0" cellspacing="0">
  <tbody>
    <tr>
      <td colspan="4"><span lang="EN-US">Use Case Specification</span></td>
    </tr>
    <tr>
      <td><span lang="EN-US">Use Case Name</span></td>
      <td colspan="3">管理员查看单个订单</td>
    </tr>
    <tr>
      <td><span lang="EN-US">Brief Description</span></td>
      <td colspan="3">管理员查看单个订单</td>
    </tr>
    <tr>
      <td><span lang="EN-US">Precondition</span></td>
      <td colspan="3">
        管理员需要以拥有管理员权限的账号登录，系统中有数量大于等于1个订单</td>
    </tr>
    <tr>
      <td><span lang="EN-US">Primary Actor</span></td>
      <td colspan="3">管理员</td>
    </tr>
    <tr>
      <td><span lang="EN-US">Secondary Actors</span></td>
      <td colspan="3">无</td>
    </tr>
    <tr>
      <td><span lang="EN-US">Dependency</span></td>
      <td colspan="3">无</td>
    </tr>
    <tr>
      <td><span lang="EN-US">Generalization<span>&nbsp;</span></span></td>
      <td colspan="3">无</td>
    </tr>
    <tr>
      <td rowspan="5"><span lang="EN-US">Basic Flow</span></td>
      <td colspan="3"><span lang="EN-US">Steps</span></td>
    </tr>
    <tr>
      <td><span lang="EN-US">1</span></td>
      <td colspan="2">管理员进入订单列表页面</td>
    </tr>
    <tr>
      <td>2</td>
      <td colspan="2">管理员点击某一个订单的查询按钮</td>
    </tr>
    <tr>
      <td>3</td>
      <td colspan="2">系统跳转至该订单的详情页面</td>
    </tr>
    <tr>
      <td colspan="2"><span lang="EN-US">PostCondition</span></td>
      <td>无</td>
    </tr>
  </tbody>
</table>  

#### 3.5.3 管理员修改订单  

<center>表3-15 管理员修改订单RUCM表</center>
<br>
<table border="0" cellpadding="0" cellspacing="0">
  <tbody>
    <tr>
      <td colspan="4"><span lang="EN-US">Use Case Specification</span></td>
    </tr>
    <tr>
      <td><span lang="EN-US">Use Case Name</span></td>
      <td colspan="3">管理员修改订单</td>
    </tr>
    <tr>
      <td><span lang="EN-US">Brief Description</span></td>
      <td colspan="3">管理员修改订单</td>
    </tr>
    <tr>
      <td><span lang="EN-US">Precondition</span></td>
      <td colspan="3">
        管理员需要以拥有管理员权限的账号登录，系统中有数量大于等于1个订单</td>
    </tr>
    <tr>
      <td><span lang="EN-US">Primary Actor</span></td>
      <td colspan="3">管理员</td>
    </tr>
    <tr>
      <td><span lang="EN-US">Secondary Actors</span></td>
      <td colspan="3">无</td>
    </tr>
    <tr>
      <td><span lang="EN-US">Dependency</span></td>
      <td colspan="3">无</td>
    </tr>
    <tr>
      <td><span lang="EN-US">Generalization<span>&nbsp;</span></span></td>
      <td colspan="3">无</td>
    </tr>
    <tr>
      <td rowspan="6"><span lang="EN-US">Basic Flow</span></td>
      <td colspan="3"><span lang="EN-US">Steps</span></td>
    </tr>
    <tr>
      <td><span lang="EN-US">1</span></td>
      <td colspan="2">管理员进入某一订单详情页面</td>
    </tr>
    <tr>
      <td>2</td>
      <td colspan="2">管理员编辑订单详细信息，如修改订单状态、收货地址和联系方式等，并点击确认按钮</td>
    </tr>
    <tr>
      <td>3</td>
      <td colspan="2">系统 <b style="color:purple"> VALIDATE THAT</b> 输入合法</td>
    </tr>
    <tr>
      <td>4</td>
      <td colspan="2">系统提示修改订单成功，刷新页面</td>
    </tr>
    <tr>
      <td colspan="2"><span lang="EN-US">PostCondition</span></td>
      <td>无</td>
    </tr>
    <tr>
      <td rowspan="4"><span lang="EN-US">Specific
          Alternative Flow</span></td>
      <td><span lang="EN-US">RFS</span></td>
      <td colspan="2"><span lang="EN-US">3</span></td>
    </tr>
    <tr>
      <td><span lang="EN-US">1</span></td>
      <td colspan="2">系统提示输入不合法</td>
    </tr>
    <tr>
      <td>2</td>
      <td colspan="2">RESUME STEP 2</td>
    </tr>
      <tr>
      <td><span lang="EN-US">Precondition</span></td>
      <td colspan="3">
        无</td>
    </tr>
  </tbody>
</table>

### 3.6 用户管理功能

![](https://pad.degrowth.net/uploads/upload_0063471e00f86f95514918af49b753a0.png)
<center>图3-6 用户管理功能用例图</center>
<br/>

#### 3.6.1 管理员查看所有用户信息

<center>表3-16 管理员查看所有用户信息RUCM表</center>  
<br>
<table border="0" cellpadding="0" cellspacing="0">
  <tbody>
    <tr>
      <td colspan="4"><span lang="EN-US">Use Case Specification</span></td>
    </tr>
    <tr>
      <td><span lang="EN-US">Use Case Name</span></td>
      <td colspan="3">管理员查看所有用户信息</td>
    </tr>
    <tr>
      <td><span lang="EN-US">Brief Description</span></td>
      <td colspan="3">管理员查看所有用户信息</td>
    </tr>
    <tr>
      <td><span lang="EN-US">Precondition</span></td>
      <td colspan="3">
        管理员需要以拥有管理员权限的账号登录</td>
    </tr>
    <tr>
      <td><span lang="EN-US">Primary Actor</span></td>
      <td colspan="3">管理员</td>
    </tr>
    <tr>
      <td><span lang="EN-US">Secondary Actors</span></td>
      <td colspan="3">无</td>
    </tr>
    <tr>
      <td><span lang="EN-US">Dependency</span></td>
      <td colspan="3">无</td>
    </tr>
    <tr>
      <td><span lang="EN-US">Generalization<span>&nbsp;</span></span></td>
      <td colspan="3">无</td>
    </tr>
    <tr>
      <td rowspan="5"><span lang="EN-US">Basic Flow</span></td>
      <td colspan="3"><span lang="EN-US">Steps</span></td>
    </tr>
    <tr>
      <td><span lang="EN-US">1</span></td>
      <td colspan="2">管理员进入用户管理界面</td>
    </tr>
    <tr>
      <td>2</td>
      <td colspan="2">管理员点击查看平台所有用户信息按钮</td>
    </tr>
    <tr>
      <td>3</td>
      <td colspan="2">界面根据创建时间由后到前的顺序展示平台所有用户信息</td>
    </tr>
    <tr>
      <td colspan="2"><span lang="EN-US">PostCondition</span></td>
      <td>无</td>
    </tr>
  </tbody>
</table>   

#### 3.6.2 管理员查看单个用户信息  

<center>表3-17 管理员查看单个用户信息RUCM表</center>  
<br>
<table border="0" cellpadding="0" cellspacing="0">
  <tbody>
    <tr>
      <td colspan="4"><span lang="EN-US">Use Case Specification</span></td>
    </tr>
    <tr>
      <td><span lang="EN-US">Use Case Name</span></td>
      <td colspan="3">管理员查看单个用户信息</td>
    </tr>
    <tr>
      <td><span lang="EN-US">Brief Description</span></td>
      <td colspan="3">管理员查看单个用户信息</td>
    </tr>
    <tr>
      <td><span lang="EN-US">Precondition</span></td>
      <td colspan="3">
        管理员需要以拥有管理员权限的账号登录，系统中有数量大于等于1个用户</td>
    </tr>
    <tr>
      <td><span lang="EN-US">Primary Actor</span></td>
      <td colspan="3">管理员</td>
    </tr>
    <tr>
      <td><span lang="EN-US">Secondary Actors</span></td>
      <td colspan="3">无</td>
    </tr>
    <tr>
      <td><span lang="EN-US">Dependency</span></td>
      <td colspan="3">无</td>
    </tr>
    <tr>
      <td><span lang="EN-US">Generalization<span>&nbsp;</span></span></td>
      <td colspan="3">无</td>
    </tr>
    <tr>
      <td rowspan="5"><span lang="EN-US">Basic Flow</span></td>
      <td colspan="3"><span lang="EN-US">Steps</span></td>
    </tr>
    <tr>
      <td><span lang="EN-US">1</span></td>
      <td colspan="2">管理员进入用户列表页面</td>
    </tr>
    <tr>
      <td>2</td>
      <td colspan="2">管理员点击某一个用户信息的查询按钮</td>
    </tr>
    <tr>
      <td>3</td>
      <td colspan="2">系统跳转至该用户的详情页面</td>
    </tr>
    <tr>
      <td colspan="2"><span lang="EN-US">PostCondition</span></td>
      <td>无</td>
    </tr>
  </tbody>
</table>  

#### 3.6.3 管理员修改用户信息 


<center>表3-18 管理员修改用户信息RUCM表</center>

<table border="0" cellpadding="0" cellspacing="0">
  <tbody>
    <tr>
      <td colspan="4"><span lang="EN-US">Use Case Specification</span></td>
    </tr>
    <tr>
      <td><span lang="EN-US">Use Case Name</span></td>
      <td colspan="3">管理员修改用户信息</td>
    </tr>
    <tr>
      <td><span lang="EN-US">Brief Description</span></td>
      <td colspan="3">管理员查找已有的用户，对其余额、发货地址等信息进行修改</td>
    </tr>
    <tr>
      <td><span lang="EN-US">Precondition</span></td>
      <td colspan="3">
        管理员需要以拥有管理员权限的账号登录，对应用户信息需要进行修改，且对应用户信息被允许修改
      </td>
    </tr>
    <tr>
      <td><span lang="EN-US">Primary Actor</span></td>
      <td colspan="3">管理员</td>
    </tr>
    <tr>
      <td><span lang="EN-US">Secondary Actors</span></td>
      <td colspan="3">无</td>
    </tr>
    <tr>
      <td><span lang="EN-US">Dependency</span></td>
      <td colspan="3">无</td>
    </tr>
    <tr>
      <td><span lang="EN-US">Generalization<span>&nbsp;</span></span></td>
      <td colspan="3">无</td>
    </tr>
    <tr>
      <td rowspan="5"><span lang="EN-US">Basic Flow</span></td>
      <td colspan="3"><span lang="EN-US">Steps</span></td>
    </tr>
    <tr>
      <td><span lang="EN-US">1</span></td>
      <td colspan="2">管理员根据关键字段查找待修改用户</td>
    </tr>
      <tr>
      <td><span lang="EN-US">2</span></td>
      <td colspan="2">系统显示用户详细信息</td>
    </tr>
    <tr>
      <td>3</td>
      <td colspan="2">管理员修改此用户信息</td>
    </tr>
    <tr>
      <td colspan="2"><span lang="EN-US">PostCondition</span></td>
      <td>用户信息根据要求被修改</td>
    </tr>
    <tr>
      <td rowspan="5"><span lang="EN-US">Specific
          Alternative Flow</span></td>
      <td><span lang="EN-US">RFS</span></td>
      <td colspan="2"><span lang="EN-US">1</span></td>
    </tr>
    <tr>
      <td><span lang="EN-US">1</span></td>
      <td colspan="2">系统未找到待修改用户</td>
    </tr>
    <tr>
      <td><span lang="EN-US">2</span></td>
      <td colspan="2">系统显示查找结果为空</td>
    </tr>
      <tr>
      <td><span lang="EN-US">3</span></td>
      <td colspan="2">ABORT</td>
    </tr>
    <tr>
      <td colspan="2"><span lang="EN-US">PostCondition</span></td>
      <td>无</td>
    </tr>
  </tbody>
</table>

## 4 非功能性需求

非功能性需求是需求的一个重要组成部分。非功能性需求，是指软件产品为满足用户业务需求而必须具有且除功能需求以外的特性，包括安全性、可靠性、互操作性、健壮性等。考虑到该工程的非营利性和受众用户的特点，我们将非功能性需求重点分为安全需求、性能需求、UI需求以及其他需求。

### 4.1 安全性需求

安全性指产品消除潜在风险的能力和对风险的承受能力。包含保密性、可靠性和完整性三个子特性。保密性指的是数据不能被授权用户以外的任何人访问的能力。可靠性指的是授权用户可以不受阻止的访问数据、与其它软件的兼容的能力和产品的强壮度。完整性指的是安预期目标完成任务的能力。

结合系统的特点，本文列出安全需求具体要考虑的内容如下表所示：

<center>表4-1 安全性需求分析表</center>
<table border="0" cellpadding="0" cellspacing="0">
  <tbody>
    <tr>
        <td>需求名称</td>
        <td>需求解释</td>
        <td>详细要求</td>
    </tr>
    <tr>
        <td>程序安全</td>
        <td>程序安全是指开发的程序是否是安全的，程序上有没有安全的漏洞</td>
        <td>人机及恶意行为的识别率>98%；能防止SQL注入；Web开发中服务器代码需对输入的参数进行验证，防止客户端机器人轻易的获取数据等</td>
    </tr>
    <tr>
        <td>系统安全</td>
        <td>系统安全指的是系统整体的安全，需设置安全的粒度</td>
        <td>用户需登录认证，不同用户拥有不同权限，未经授权用户不可以非法访问数据</td>
    </tr>
    <tr>
        <td>数据安全</td>
        <td>数据的安全是对数据的保护</td>
        <td>保护用户的隐私信息和个性化信息。存入数据库中的数据需要被审核</td>
    </tr>
  </tbody>
</table>

### 4.2 性能/容量需求

本文列出理想情况下的性能/容量需求（现实受到服务器硬件配置限制）：
<center>表4-2 性能/容量需求分析表</center>
<table border="0" cellpadding="0" cellspacing="0">
  <tbody>
    <tr>
        <td>需求名称</td>
        <td>需求解释</td>
        <td>具体指标</td>
    </tr>
    <tr>
        <td>并发用户</td>
        <td>并发用户数用来衡量系统的同步协调能力，这里更关注当多个用户同时操作同一功能或数据时，对系统性能的影响。</td>
        <td>满足高峰时段的用户数。即同时支持500~3000人以上的同时发起请求，包括用户对数据的上传和浏览、下载等。</td>
    </tr>
    <tr>
        <td>响应时间</td>
        <td>响应时间指功能完成的时间，和客观环境、数据量级、用户的主观感受等都有关系。确定响应时间的指标需要根据实际所需的数量级来要求。另外，还要考虑用户的可接受度。</td>
        <td>在95％的情况下，一般时段响应时间不超过1.5秒，高峰时段不超过4秒。在非高峰时间根据编号和名称特定条件进行搜索，可以在3秒内得到搜索结果。</td>
    </tr>
    <tr>
        <td>系统容量</td>
        <td>可指存储数据空间大小</td>
        <td>支持1万用户，支持GB级数据。数据库表行数不超过10万行，数据库最大容量不超过100GB，磁盘空间至少需要20G以上。</td>
    </tr>
  </tbody>
</table>

### 4.3 UI需求

结合产品特点及交互性要求，产品的界面设计具体要考虑的内容如下表所示:
<center>表4-3 UI需求分析表</center>
<table border="0" cellpadding="0" cellspacing="0">
  <tbody>
    <tr>
        <td>需求名称</td>
        <td>详细要求</td>
    </tr>
    <tr>
        <td>整体性</td>
        <td>风格统一。图标：简洁、直观，与流行图标相统一；颜色：冷暖均衡、比例得当、重点突出；字体美观、大小和间距得当、颜色协调且符合阅读习惯</td>   
    </tr>
    <tr>
        <td>易见性</td>
        <td>各种功能操作不要藏得太深，用户很容易找到他们期望进行的各种操作</td>
    </tr>
    <tr>
        <td>易学性</td>
        <td>软件系统通过在线帮助，导航，向导等各种方式保证软件是可自学习的</td>
    </tr>
    <tr>
        <td>易用性</td>
        <td>交互逻辑简单明了，在软件在熟练使用后用户可以更快的进行各项操作</td>
    </tr>
  </tbody>
</table>

### 4.4 其他需求

除了上述三大非功能需求外，我们结合系统自身特点，提出系统需要满足可靠性、鲁棒性、可维护性、可测试性、可扩展性。具体要考虑的内容如下表所示:
<center>表4-4 其他需求分析表</center>
<table border="0" cellpadding="0" cellspacing="0">
  <tbody>
    <tr>
        <td>需求名称</td>
        <td>详细要求</td>
    </tr>
    <tr>
        <td>可靠性</td>
        <td>能识别用户的非法输入。在系统出现意外故障时尽量保证其他功能模块正常运行，并且能够在较短的时间内发现故障产生的原因，并用少量的工作排除故障。</td>   
    </tr>
    <tr>
        <td>可维护性</td>
        <td>(1)各个功能模块集成时进行解耦
 (2)文档应该清晰可读、书写规范统一。</td>
    </tr>
    <tr>
        <td>可测试性</td>
        <td>可以使用少量数据集完成整个产品功能的测试。</td>
    </tr>
    <tr>
        <td>可扩展性</td>
        <td>产品应留有升级接口和升级空间。</td>
    </tr>
  </tbody>
</table>

###  4.5 故障处理

&emsp; 在系统的实际运行中，会有很多故障发生，大致可以分为两类：硬件故障和软件故障。

#### 4.5.1 硬件故障

&emsp; 系统后端不可避免地会发生某些硬件故障。可能发生的硬件故障及解决方案如下表所示。
<center>表4-5 可能发生的硬件故障及解决方案</center>
<table border="0" cellpadding="0" cellspacing="0">
        <tr>
            <td>硬件故障</td>
            <td>解决方案</td>
            <td>时间要求</td>
        </tr>
        <tr>
            <td>服务器宕机	</td>
            <td>重启服务器及运行系统</td>
            <td>30min</td>
        </tr>
        <tr>
            <td>磁盘、CPU、主机等硬件损坏</td>
            <td>尽快更换相关配件</td>
            <td>12h</td>
        </tr>
 </table>


#### 4.5.2 软件故障

 <table>
	<center>表4-6 可能发生的软件故障及解决方案</center>
        <tr>
            <td>软件故障</td>
            <td>解决方案</td>
            <td>时间要求</td>
        </tr>
        <tr>
            <td>系统出错</td>
            <td>根据4.5.3故障处理流程处理故障，尽快修改bug，并重新上线系统</td>
            <td>2h</td>
        </tr>
        <tr>
            <td>内存不足</td>
            <td>根据用户增长速度和已有设备及经费，适量增加内存，提高处理和存储能力</td>
            <td>6h</td>
        </tr>
 </table>

#### 4.5.3 故障处理流程

1. ##### 确认故障

   当系统故障发生时，我们首先要做的就是定位故障。通过以下指标项迅速判断，发现可能遇到的问题

   **系统监控指标：**

   - cpu负载
   - 内存消耗
   - I/O 网络与磁盘
   - 客户端连接总数量
   - 文件描述符数量
   - ......

   **服务器监控指标：**

   - 服务日志(错误日志、抛出异常)
   - 上下文逻辑问题
   - ......

   **用户服务指标：**

   - 收集调用异常或错误信息(接口请求响应时间、接口调用QPS、返回错误内容或错误码)
   - 从错误信息确认边界，是用户使用问题，还是服务器运行异常

   **中间件监控指标(数据库、缓存、消息队列、存储):**

   - 对数据库的负载、慢查询、连接数等监控
   - 对缓存的连接数、占用内存、吞吐量、响应时间等监控
   - 消息队列的生产/消费时间、吞吐量、负载、堆积情况等监控
   - 对存储的写入时间、吞吐量、读取QPS等监控

2. ##### 故障恢复

   故障确认后，首要做的就是故障止损和恢复，恢复常用手段如下：

   <center>表4-7 恢复故障常用手段</center>
<table border="0" cellpadding="0" cellspacing="0">
        <tr>
            <td>方法名称</td>
            <td>解决方案</td>
        </tr>
        <tr>
            <td>服务回滚</td>
            <td>如果属于更新的代码BUG导致的问题，一般可通过回滚上一个程序版本来迅速恢复，不过会导致部分新功能不可用</td>
        </tr>
        <tr>
            <td>重启</td>
            <td>部分问题是可以通过重启的手段来临时恢复的，以保障系统的暂时可用，但后续还需有其他方法彻底解决问题</td>
        </tr>
		<tr>
			<td>紧急更新</td>
			<td>经常被用到，明确定位问题源后，迅速修复代码或组件，然后快速更新上线，比较依赖故障处理人技术和代码逻辑、应急处理能力</td>
		</tr>
 </table>

3. ##### 故障casestudy文档规范

   并不是所有故障都需要写casestudy，如果我们能快速恢复且对系统影响很小，就不用写。只有当比较难的故障发生时，小组成员需参与讨论并攥写该文档。

   **caseStudy-YYYYMMDD-xxx操作引起xxx服务不可用**

   ```
   故障发生时间：
   故障报告时间：
   故障恢复时间：
   故障持续时间：
   故障影响范围：
   故障等级：PN
   故障处理人：xxx、xxx、xxx
   故障责任人：xxx
   故障描述：xxx
   故障处理过程：xxx
   故障原因分析：xxx
   故障总结：xxx
   后续改进工作：xxx 
   改进任务列表(任务、执行人、Deadline)
   ```

## 5 运行环境规定

### 5.1 用户硬件规定

* 安卓5.0及以上操作系统，4GB及以上运行内存，64GB及以上磁盘容量

### 5.2 环境规定

* 8.0及以上微信版本