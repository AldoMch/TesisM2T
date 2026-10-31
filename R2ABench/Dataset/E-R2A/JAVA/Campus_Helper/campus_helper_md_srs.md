# BUAA Campus Helper Platform Software Requirements Specification (Standard SRS Extract)

## 1. Introduction

### Purpose

This document extracts verifiable requirements from `Campus_Helper_origin.md` and rewrites them according to the compact SRS standard in `architectural_views_rep-pkg/script/templates/SRS.md`. Its purpose is to provide structured input for architecture generation, test design, and requirements traceability for the BUAA Campus Helper platform. Source evidence is listed in `campus_helper_md_evidence_pack.json`. (Source: CH-001)

### Product Scope

The BUAA Campus Helper platform is a campus trading platform based on a WeChat Mini Program. It serves BUAA campus takeout/express pickup, immediate takeout transfer, and second-hand information publishing. Through a publish-and-accept-order model, the platform supports information flow for errand products and second-hand product transactions and aims to provide a more standardized and reliable way to obtain transaction information. (Source: CH-001, CH-002)

This document follows the source document definitions of platform, product, errand product, second-hand product, user, guest, seller, customer, order, errand order, second-hand order, tag, administrator, log, order status, publish product, search product, and QPS. (Source: CH-002)

### Intended Audience

This document is intended for platform users, software developers, requirements analysts, testers, architecture generation workflows, and requirements review workflows. Target end users include BUAA students, BUAA teachers, and family members; management users are platform administrators. (Source: CH-001, CH-002)

### References

| Ref | Source |
| --- | --- |
| REF-001 | GB/T 9385-2008, Computer Software Requirements Specification |
| REF-002 | GB/T 8567-2006, Computer Software Documentation Specification |
| REF-003 | GB/T 20918-2007, Information Technology, Software Life Cycle Process and Risk Management |
| REF-004 | GB/T 15532-2008, Software Testing Specification |
| REF-005 | GB/T 20917-2007, Software Engineering and Software Measurement Process |
| REF-006 | WeChat Mini Program Platform Operation Specification, WeChat Mini Program Platform Terms of Service, Tencent WeChat Software License and Service Agreement |
| REF-007 | Web coding specification: https://www.html.cn/archives/5361 |

## 2. Overall Description

### Product Perspective

The system is a WeChat Mini Program trading platform. The source document designs it as a four-layer architecture: presentation layer, business layer, data layer, and data entity layer (database). Overall, the system is divided into six functional categories: product information viewing, order module, personal center, product management, order management, and user management. The source document does not provide server deployment topology, API protocol, or database table structure. (Source: CH-003)

### Product Functions Summary

| Capability | Summary | Source |
| --- | --- | --- |
| Product browsing | Users or guests can view popular products, browse products by category, and enter detail pages; registered users can further favorite or place orders. | CH-004 |
| User orders | Logged-in users can create orders, modify order remarks, confirm orders, and cancel orders. | CH-005 |
| Personal center | Logged-in users can view favorites and their own order records. | CH-006 |
| Administrator product management | Administrators can view overall platform product status, view product details, search products, modify products, and delete products. | CH-007 |
| Administrator order management | Administrators can view all orders, view a single order, and modify order details. | CH-008 |
| Administrator user management | Administrators can view all users, view a single user, and modify user information. | CH-009 |

### User Classes

| User Class | Responsibilities / Needs | Source |
| --- | --- | --- |
| Guest | Has no platform account and can view products, but core functions such as favorites and ordering are restricted. | CH-002, CH-004 |
| Registered user | Has a platform account and can browse, publish, and favorite products, and participate in transactions as customer or seller. | CH-002 |
| Customer | Browses products and places orders for desired products. | CH-002, CH-005 |
| Seller | Publishes errand products or second-hand products and acts as the product publisher in transactions. | CH-002 |
| Administrator | Supervises violations, manages violating product information, and views and modifies product, order, and user information. | CH-002, CH-007, CH-008, CH-009 |

### Operating Environment

| Environment | Requirement | Source |
| --- | --- | --- |
| Client operating system | Android 5.0 or above. | CH-015 |
| Client hardware | 4GB or more RAM and 64GB or more disk capacity. | CH-015 |
| WeChat version | WeChat 8.0 or above. | CH-015 |
| Server environment | The source document does not specify server operating system, database product, cloud service, or deployment method. | CH-015 |

### Assumptions and Dependencies

| ID | Assumption / Dependency | Evidence Type | Source |
| --- | --- | --- | --- |
| AD-001 | Platform operation depends on the WeChat Mini Program framework and WeChat 8.0 or above client. | explicit | CH-001, CH-015 |
| AD-002 | Popular product sorting depends on predefined popularity rules and accurate product information such as time and amount. | explicit | CH-004 |
| AD-003 | Product category browsing depends on accurate information such as actual product demand, amount, location, and item type. | explicit | CH-004 |
| AD-004 | Administrator functions depend on login with an account that has administrator permissions. | explicit | CH-007, CH-008, CH-009 |
| AD-005 | Payment, offline transaction fulfillment, and dispute handling rules are not expanded in the source document; later design must not assume automatic payment or arbitration capability. | explicit | CH-002, CH-005 |

## 3. External Interface Requirements

### User Interfaces

| Interface | Requirement | Source |
| --- | --- | --- |
| Homepage / popular products interface | Display products sorted by popularity rules and support entering product details. | CH-004 |
| Product category interface | Support displaying product lists by product location, amount, item type, and other categories. | CH-004 |
| Product detail interface | Support browsing product information; registered users can favorite products or perform order-related operations. | CH-004, CH-005 |
| Order interface | Support creating orders, modifying order remarks, confirming orders, and canceling orders. | CH-005 |
| Personal center interface | Support viewing favorites and order records. | CH-006 |
| Administrator product management interface | Support product overview, product detail viewing, product search, product modification, and deletion. | CH-007 |
| Administrator order management interface | Support viewing all orders, viewing a single order, and modifying orders. | CH-008 |
| Administrator user management interface | Support viewing all users, viewing a single user, and modifying user information. | CH-009 |

### Software/API Interfaces

| Interface | Requirement | Source |
| --- | --- | --- |
| WeChat Mini Program runtime interface | The client shall run in WeChat 8.0 or above. | CH-015 |
| Database interface | The system architecture includes a data entity layer (database), and operations such as order creation, remark modification, confirmation, and cancellation need to write or update database records. | CH-003, CH-005 |
| Administration backend interface | The administration backend needs to support management operations related to products, orders, users, and logs. The source document does not provide API paths or protocols. | CH-002, CH-007, CH-008, CH-009 |

### Communication Interfaces

The source document does not specify HTTP, HTTPS, WebSocket, RPC, message queues, or other communication protocols. It can only be determined that the client carrier is a WeChat Mini Program and that the references include WeChat Mini Program platform specifications and Web coding specifications. (Source: CH-001, CH-015)

### Data Exchange Formats

The system needs to process user information, personal information, product information, product categories, tags, product location, product amount, favorite relationships, order information, order remarks, order status, administrator logs, search conditions, and fault monitoring metrics. The source document does not specify JSON schemas, file upload formats, database schemas, interface error codes, or authentication token formats. (Source: CH-002, CH-004, CH-005, CH-014)

## 4. Functional Requirements

| ID | Requirement | Trigger / Input | System Behavior | Output | Priority | Verification | Source |
| --- | --- | --- | --- | --- | --- | --- | --- |
| FR-001 | The system shall support users or guests viewing popular products. | A user or guest enters the main interface to view popular products. | The system sorts products according to predefined popularity rules, displays the popular product list, and allows entry to product detail pages. | Popular product list and product details. | High | Test | CH-004 |
| FR-002 | The system shall support users or guests viewing products by category. | A user or guest enters the product category entry and selects category conditions. | The system displays product lists by product location, amount, item type, and other categories, and allows browsing detail pages. | Categorized product list and product details. | High | Test | CH-004 |
| FR-003 | The system shall support logged-in users creating orders. | A user selects a product to check out, fills in product attributes, delivery address, contact information, and other information, and submits. | The system validates input validity. If valid, it inserts an order record into the database; if invalid, it displays an error. | New order record or input error prompt. | High | Test | CH-005 |
| FR-004 | The system shall support logged-in users modifying order remarks. | A user selects an order before it has been delivered or completed and submits a remark modification. | The system validates the remark input. If valid, it updates the database order record; if invalid, it displays an error. | Updated order remark or input error prompt. | Medium | Test | CH-005 |
| FR-005 | The system shall support logged-in users confirming orders. | A user receives a delivered order, selects an incomplete order, and clicks confirm. | The system updates the order status in the database. | Updated order status. | High | Test | CH-005 |
| FR-006 | The system shall support logged-in users canceling orders. | A user selects an order before it has been delivered and clicks cancel. | The system updates the order status in the database and marks the order as canceled or an equivalent cancellation status. | Updated order status. | High | Test | CH-005 |
| FR-007 | The system shall support logged-in users viewing favorites. | A user enters the personal center and clicks the favorites entry. | The system displays product entries favorited by the user and supports returning to the personal center. | Favorite product list. | Medium | Test | CH-006 |
| FR-008 | The system shall support logged-in users viewing their own order records. | A user enters the personal center and clicks the order records entry. | The system displays all order records for that user and supports returning to the personal center. | User order record list. | Medium | Test | CH-006 |
| FR-009 | The system shall support administrators viewing overall platform product status. | An administrator logs in with an account that has administrator permissions and enters the administrator interface. | The system displays total product count, express pickup listing count, takeout pickup listing count, and second-hand product count, and supports pull-down or paged browsing. | Platform product statistics and browsing results. | High | Test | CH-007 |
| FR-010 | The system shall support administrators viewing single product information. | An administrator enters the product list and clicks a product entry, or searches by publisher, product name, product status, or other keywords. | The system navigates to and displays the product details. | Product detail page. | High | Test | CH-007 |
| FR-011 | The system shall support administrators modifying single product information. | An administrator clicks modify on the product detail page, edits product information, and confirms. | The system validates input validity. If valid, it saves the modification and displays success; if invalid, it displays an input nonconformance message. | Updated product details or error prompt. | High | Test | CH-007 |
| FR-012 | The system shall support administrators deleting products. | An administrator clicks the delete button for a single product in the product list, or batch-selects products and clicks delete. | The system prompts for second confirmation; after confirmation, it deletes the corresponding products and refreshes the product list. | Deletion success prompt and refreshed product list. | High | Test | CH-007 |
| FR-013 | The system shall support administrators viewing all orders. | An administrator logs in, enters order management, and clicks view all orders. | The system displays all orders on the platform. | All-order list. | High | Test | CH-008 |
| FR-014 | The system shall support administrators viewing a single order. | An administrator selects or queries an order in the order list. | The system displays detailed information for that order. | Order detail page. | High | Test | CH-008 |
| FR-015 | The system shall support administrators modifying orders. | An administrator enters order details, edits order status, receiving address, contact information, and other data, and confirms. | The system saves the order modification and updates order details. | Updated order details. | High | Test | CH-008 |
| FR-016 | The system shall support administrators viewing all user information. | An administrator logs in, enters user management, and clicks view all users. | The system displays all platform user information in descending creation-time order. | All-user list. | High | Test | CH-009 |
| FR-017 | The system shall support administrators viewing single user information. | An administrator clicks query or selects a user in the user list. | The system navigates to and displays that user's details. | User detail page. | High | Test | CH-009 |
| FR-018 | The system shall support administrators modifying user information. | An administrator searches for a user by key fields, edits allowed user information, and submits. | If the system finds the user, it displays and updates user information; if it does not find the user, it displays an error. | Updated user information or not-found prompt. | High | Test | CH-009 |

## 5. Non-Functional Requirements

| ID | Quality | Requirement | Metric / Acceptance | Priority | Verification | Source |
| --- | --- | --- | --- | --- | --- | --- |
| NFR-001 | Security | The system shall provide program security protection capability and identify human-machine and malicious behavior. | Human-machine and malicious behavior recognition rate is greater than 98%. | High | Test | CH-010 |
| NFR-002 | Security | The system shall prevent SQL injection and validate input parameters on the server side. | SQL injection attacks are blocked; client bots cannot easily obtain data. | High | Test | CH-010 |
| NFR-003 | Security | The system shall require user login authentication and implement permission control by user type. | Unauthenticated or unauthorized users cannot illegally access data. | High | Test | CH-010 |
| NFR-004 | Privacy / Integrity | The system shall protect user privacy information and personalized information, and review data stored in the database. | A review mechanism exists before or during data storage; privacy data must not be accessed by unauthorized users. | High | Inspection | CH-010 |
| NFR-005 | Performance | The system shall support concurrent requests during peak periods. | It supports more than 500 to 3000 people simultaneously initiating upload, browse, download, and other requests. | High | Test | CH-011 |
| NFR-006 | Performance | The system shall satisfy response time requirements. | In 95% of cases, normal-period response time is no more than 1.5 seconds and peak-period response time is no more than 4 seconds. | High | Test | CH-011 |
| NFR-007 | Performance | The system shall satisfy off-peak search response time requirements. | Off-peak searches by specific number and name conditions return results within 3 seconds. | Medium | Test | CH-011 |
| NFR-008 | Capacity | The system shall satisfy user volume, data volume, and storage capacity requirements. | It supports 10,000 users and GB-level data; database table rows do not exceed 100,000, maximum database capacity does not exceed 100GB, and disk capacity is at least 20GB. | High | Analysis | CH-011 |
| NFR-009 | Usability | The system interface shall maintain a unified overall style. | Icons are concise and intuitive, colors balance warm and cool tones while highlighting key points, and font size, spacing, and color fit reading habits. | Medium | Inspection | CH-012 |
| NFR-010 | Usability | System function entries shall be easy to find. | Functional operations must not be hidden too deeply, and users can easily find expected operations. | Medium | Demonstration | CH-012 |
| NFR-011 | Learnability | The system shall support user self-learning. | Online help, navigation, wizards, and similar means help users learn to use the system. | Medium | Inspection | CH-012 |
| NFR-012 | Usability | System interaction logic shall be simple and clear. | Skilled users can complete operations more quickly. | Medium | Demonstration | CH-012 |
| NFR-013 | Reliability | The system shall identify illegal input and try to keep other modules running during unexpected faults. | Illegal input is identified; a single module fault should not make all functions unavailable. | High | Test | CH-013 |
| NFR-014 | Maintainability | System module integration shall be decoupled, and documentation shall be clear, readable, standardized, and unified. | Module responsibility boundaries are inspectable, and documentation complies with project norms. | Medium | Inspection | CH-013 |
| NFR-015 | Testability | The system shall allow product function tests with a small dataset. | Testers can cover core functional flows with small-scale data. | Medium | Test | CH-013 |
| NFR-016 | Scalability | The product shall leave upgrade interfaces and upgrade space. | Architecture and interface design preserve upgrade extension points. | Medium | Analysis | CH-013 |
| NFR-017 | Fault Recovery | The system shall satisfy hardware fault handling time limits. | If the server crashes, restart the server and system within 30 minutes; if disk, CPU, host, or other hardware is damaged, replace related parts within 12 hours. | High | Inspection | CH-014 |
| NFR-018 | Fault Recovery | The system shall satisfy software fault handling time limits. | If the system has an error, handle it, fix the bug, and redeploy within 2 hours; if memory is insufficient, scale capacity within 6 hours according to resource conditions. | High | Inspection | CH-014 |
| NFR-019 | Observability | The system shall support monitoring and logs needed for fault localization. | CPU, memory, I/O, connection count, file descriptors, service logs, interface response time, QPS, error codes, database load, slow queries, cache, message queue, and storage metrics can be monitored. | High | Inspection | CH-014 |
| NFR-020 | Incident Management | The system shall support fault recovery and retrospective processes. | Service rollback, restart, and emergency update are supported; difficult faults require a caseStudy document. | Medium | Inspection | CH-014 |

## 6. Data Requirements

| ID | Data Entity / Object | Requirement | Source |
| --- | --- | --- | --- |
| DR-001 | User and permission data | The system shall save user accounts, personal information, role permissions, and authentication status; guest, registered user, and administrator permissions shall be distinguishable. | CH-002, CH-010 |
| DR-002 | Product data | The system shall save takeout pickup, express pickup, and second-hand product information, including demand, amount, location, item type, publisher, product name, product status, and other searchable fields. | CH-002, CH-004, CH-007 |
| DR-003 | Tag and category data | The system shall save product tags, categories, time ranges, user-related conditions, and other data used for product viewing and search. | CH-002, CH-004 |
| DR-004 | Order data | The system shall save orders, order remarks, order status, delivery address, contact information, and other information, and support updates by users and administrators. | CH-002, CH-005, CH-008 |
| DR-005 | Favorite data | The system shall save user-product favorite relationships so users can view favorited products in favorites. | CH-002, CH-004, CH-006 |
| DR-006 | Administration log data | The system shall record administrator backend management operations and support retrieval by multiple conditions. | CH-002 |
| DR-007 | Fault and monitoring data | The system shall record or collect system, server, user service, middleware, and storage metrics needed for fault localization. | CH-014 |
| DR-008 | Data review and privacy | Data stored in the database needs to be reviewed, and user privacy information and personalized information shall be protected. | CH-010 |

## 7. Constraints

| ID | Constraint | Source |
| --- | --- | --- |
| C-001 | The platform shall provide services based on the WeChat Mini Program development framework. | CH-001 |
| C-002 | The client runtime environment shall satisfy Android 5.0 or above, 4GB or more RAM, and 64GB or more disk capacity. | CH-015 |
| C-003 | The client WeChat version shall be 8.0 or above. | CH-015 |
| C-004 | The system architecture shall follow a four-layer division: presentation layer, business layer, data layer, and data entity layer (database). | CH-003 |
| C-005 | The main service objects are limited to BUAA students, BUAA teachers, and family members. | CH-001 |
| C-006 | Requirements and testing work shall refer to the national standards, WeChat Mini Program platform specifications, and Web coding specifications listed in the source document. | CH-001 |

## 8. Verification and Acceptance

| Verification Method | Applicable Requirement IDs | Acceptance Basis |
| --- | --- | --- |
| Test | FR-001 to FR-018; NFR-001, NFR-002, NFR-003, NFR-005, NFR-006, NFR-007, NFR-013, NFR-015 | Execute functional flow, permission validation, input validation, concurrency, and response-time tests; results satisfy the outputs and metrics in the corresponding requirement tables. |
| Inspection | NFR-004, NFR-009, NFR-011, NFR-014, NFR-017, NFR-018, NFR-019, NFR-020; DR-001 to DR-008; C-001 to C-006 | Inspect design documents, interfaces, data models, logs, monitoring, fault processes, and deployment constraints for coverage of corresponding requirements. |
| Analysis | NFR-008, NFR-016 | Use capacity estimation, architecture review, and extension point review to judge whether capacity and upgrade-space requirements are met. |
| Demonstration | NFR-010, NFR-012 | Demonstrate function entry discoverability and typical user operation paths, confirming that interaction logic conforms to source document requirements. |

## 9. Traceability Matrix

| ID | Requirement | Type | Source | Evidence Type | Verification | Confidence |
| --- | --- | --- | --- | --- | --- | --- |
| FR-001 | View popular products | Functional | CH-004 | explicit | Test | High |
| FR-002 | View products by category | Functional | CH-004 | explicit | Test | High |
| FR-003 | Create order | Functional | CH-005 | explicit | Test | High |
| FR-004 | Modify order remark | Functional | CH-005 | explicit | Test | High |
| FR-005 | Confirm order | Functional | CH-005 | explicit | Test | High |
| FR-006 | Cancel order | Functional | CH-005 | explicit | Test | High |
| FR-007 | View favorites | Functional | CH-006 | explicit | Test | High |
| FR-008 | View order records | Functional | CH-006 | explicit | Test | High |
| FR-009 | Administrator views overall product status | Functional | CH-007 | explicit | Test | High |
| FR-010 | Administrator views single product | Functional | CH-007 | explicit | Test | High |
| FR-011 | Administrator modifies product | Functional | CH-007 | explicit | Test | High |
| FR-012 | Administrator deletes product | Functional | CH-007 | explicit | Test | High |
| FR-013 | Administrator views all orders | Functional | CH-008 | explicit | Test | High |
| FR-014 | Administrator views single order | Functional | CH-008 | explicit | Test | High |
| FR-015 | Administrator modifies order | Functional | CH-008 | explicit | Test | High |
| FR-016 | Administrator views all users | Functional | CH-009 | explicit | Test | High |
| FR-017 | Administrator views single user | Functional | CH-009 | explicit | Test | High |
| FR-018 | Administrator modifies user | Functional | CH-009 | explicit | Test | High |
| NFR-001 | Malicious behavior recognition rate | Non-functional | CH-010 | explicit | Test | High |
| NFR-002 | SQL injection prevention and input validation | Non-functional | CH-010 | explicit | Test | High |
| NFR-003 | Login authentication and permission control | Non-functional | CH-010 | explicit | Test | High |
| NFR-004 | Privacy protection and data review | Non-functional | CH-010 | explicit | Inspection | High |
| NFR-005 | Concurrent users | Non-functional | CH-011 | explicit | Test | High |
| NFR-006 | Response time | Non-functional | CH-011 | explicit | Test | High |
| NFR-007 | Search response time | Non-functional | CH-011 | explicit | Test | High |
| NFR-008 | Capacity | Non-functional | CH-011 | explicit | Analysis | High |
| NFR-009 | Interface consistency | Non-functional | CH-012 | explicit | Inspection | High |
| NFR-010 | Function discoverability | Non-functional | CH-012 | explicit | Demonstration | High |
| NFR-011 | Learnability | Non-functional | CH-012 | explicit | Inspection | High |
| NFR-012 | Ease of use | Non-functional | CH-012 | explicit | Demonstration | High |
| NFR-013 | Reliability | Non-functional | CH-013 | explicit | Test | High |
| NFR-014 | Maintainability | Non-functional | CH-013 | explicit | Inspection | High |
| NFR-015 | Testability | Non-functional | CH-013 | explicit | Test | High |
| NFR-016 | Scalability | Non-functional | CH-013 | explicit | Analysis | High |
| NFR-017 | Hardware fault handling | Non-functional | CH-014 | explicit | Inspection | High |
| NFR-018 | Software fault handling | Non-functional | CH-014 | explicit | Inspection | High |
| NFR-019 | Monitoring and logs | Non-functional | CH-014 | explicit | Inspection | High |
| NFR-020 | Fault recovery and retrospective | Non-functional | CH-014 | explicit | Inspection | High |
| DR-001 | User and permission data | Data | CH-002, CH-010 | explicit | Inspection | High |
| DR-002 | Product data | Data | CH-002, CH-004, CH-007 | explicit | Inspection | High |
| DR-003 | Tag and category data | Data | CH-002, CH-004 | explicit | Inspection | High |
| DR-004 | Order data | Data | CH-002, CH-005, CH-008 | explicit | Inspection | High |
| DR-005 | Favorite data | Data | CH-002, CH-004, CH-006 | explicit | Inspection | High |
| DR-006 | Administration log data | Data | CH-002 | explicit | Inspection | High |
| DR-007 | Fault and monitoring data | Data | CH-014 | explicit | Inspection | High |
| DR-008 | Data review and privacy | Data | CH-010 | explicit | Inspection | High |
| C-001 | WeChat Mini Program development framework | Constraint | CH-001 | explicit | Inspection | High |
| C-002 | Android client hardware and OS | Constraint | CH-015 | explicit | Inspection | High |
| C-003 | WeChat version | Constraint | CH-015 | explicit | Inspection | High |
| C-004 | Four-layer architecture division | Constraint | CH-003 | explicit | Inspection | High |
| C-005 | BUAA user scope | Constraint | CH-001 | explicit | Inspection | High |
| C-006 | Standards and platform specifications | Constraint | CH-001 | explicit | Inspection | High |
