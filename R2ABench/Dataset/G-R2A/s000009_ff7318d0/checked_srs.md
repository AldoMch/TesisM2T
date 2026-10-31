# Software Requirements Specification

## 1. Introduction

### 1.1 Purpose
This SRS defines the final checked requirements for Foot365, an AWS-based football information web application. The document is prepared as a clean requirements input for downstream architecture diagram generation.

### 1.2 Product Scope
Foot365 provides football match information, live score updates, machine-learning match predictions, nearby match-screening recommendations, conversational football queries, and request-based SMS reminders.

The term "live streaming" in the product context shall mean real-time live-score updates through the streaming data pipeline and live match-screening recommendations. The system shall not be treated as providing in-application video streaming unless a separate video-streaming requirement is added.

The in-scope capabilities are:
- Viewing fixtures, standings, schedules, results, and live scores.
- Viewing match prediction probabilities.
- Finding nearby places that screen live football matches.
- Asking football information questions through a chatbot interface.
- Viewing or requesting fixture reminders.
- Requesting SMS reminder notifications.
- Exchanging frontend/backend data through AWS API Gateway.
- Persisting and searching match results, statistics, and fixture data.
- Processing live score updates through Kafka and Apache Avro on EC2.
- Deploying the frontend, backend, data, notification, prediction, and streaming components on AWS services.

### 1.3 Intended Audience
- Product owners defining Foot365 behavior.
- Developers implementing frontend, backend, chatbot, prediction, notification, data, and deployment components.
- Testers validating user-facing football workflows and AWS integrations.
- Architecture reviewers generating or validating architecture diagrams.
- Deployers configuring the AWS runtime environment.

### 1.4 Terminology
| Term | Definition |
|---|---|
| Fixture | A scheduled football match. |
| Standing | A team's ranking or table position within a competition. |
| Live score | A real-time score update for a match. |
| Screening recommendation | A nearby venue recommendation where users can watch a live match. |
| Chatbot | A conversational interface that accepts text messages and returns football information responses. |
| Prediction | A machine-learning output indicating likely match outcomes such as home win, draw, or away win. |
| Reminder | A user-requested notification about an upcoming game. |

## 2. Overall Description

### 2.1 Product Perspective
Foot365 is a web application with a frontend hosted on AWS and backend services exposed through API Gateway and Lambda. The frontend uses HTML, CSS, Bootstrap, and jQuery. Backend logic uses Python and Node. Authentication and protected access use Cognito and IAM. Match data is stored in DynamoDB and connected to Elasticsearch for retrieval. Prediction workflows use SageMaker. Reminder workflows use SQS and SNS. Live score updates use Kafka with Apache Avro on EC2.

The architecture shall include the AWS services and major components required by these requirements. Detailed service-to-service data-flow relationships shall be modeled only where the requirements specify the interaction.

### 2.2 Product Functions
- Present match fixtures, standings, schedules, results, and live scores.
- Generate and display match prediction probabilities.
- Recommend nearby live match-screening venues.
- Provide a chatbot for football fixtures, results, and screening-location questions.
- Allow users to view fixtures and request reminder support.
- Send request-based SMS reminders.
- Build and send API Gateway requests with JSON defaults.
- Store and retrieve match results, statistics, and fixtures.
- Process live score updates through a Kafka/Avro streaming pipeline.
- Use AWS services for authentication, storage, routing, notifications, predictions, streaming, and hosting.

### 2.3 User Classes
| User Class | Description |
|---|---|
| Football enthusiast | Views football information, predictions, live scores, and screening recommendations. |
| Chatbot user | Sends football-related text queries and receives conversational responses. |
| Reminder requester | Requests SMS reminders for upcoming fixtures. |
| Application maintainer | Configures AWS services, APIs, data stores, prediction services, and streaming infrastructure. |

### 2.4 Operating Environment
- Web frontend hosted on Amazon S3.
- Backend services exposed through Amazon API Gateway and AWS Lambda.
- Authentication and security management through Amazon Cognito and IAM.
- Match data storage in DynamoDB and match data search through Elasticsearch.
- Prediction service using Amazon SageMaker.
- Notification workflow using SQS and SNS.
- Live score update pipeline on EC2 using Kafka with Apache Avro.
- API calls using AWS Signature Version 4 and the `execute-api` service configuration.

### 2.5 Assumptions and Dependencies
- The system depends on the configured AWS service stack for hosting, routing, authentication, prediction, notification, storage, search, and streaming.
- API requests and responses use `application/json` by default unless explicitly overridden.
- Final-week season predictions assume that all matches played in the current season except the last week are used as input data.
- Match-screening recommendations depend on available location or city information supplied by the user.
- SMS reminder delivery depends on notification service configuration.

## 3. External Interface Requirements

### 3.1 User Interfaces
| ID | Interface | Requirement |
|---|---|---|
| UI-001 | Web application | The system shall provide a web-based user interface implemented with HTML, CSS, Bootstrap, and jQuery. |
| UI-002 | Football information pages | The system shall provide pages or views for fixtures, standings, schedules, results, live scores, and predictions. |
| UI-003 | Chatbot interface | The system shall provide a chatbot UI with message input and response display for football information queries. |
| UI-004 | Reminder request interface | The system shall allow users to request reminder notifications for upcoming games. |

### 3.2 Software and API Interfaces
| ID | Interface | Requirement |
|---|---|---|
| API-001 | API Gateway client | The frontend shall invoke backend endpoints through AWS API Gateway. |
| API-002 | Chatbot recommendation endpoint | The frontend shall submit chatbot messages to a backend recommendation endpoint. |
| API-003 | Conversation handler | The backend shall process chatbot intents and return conversational responses. |
| API-004 | Authentication services | The system shall integrate with Cognito and IAM for authentication and protected access. |
| API-005 | Notification services | The system shall integrate with SQS and SNS for queued reminder handling and SMS delivery. |
| API-006 | Prediction services | The system shall integrate with SageMaker for match prediction generation. |
| API-007 | Data services | The system shall integrate with DynamoDB and Elasticsearch for match data storage and retrieval. |

### 3.3 Communication Interfaces
| ID | Interface | Requirement |
|---|---|---|
| COM-001 | HTTP API requests | API requests shall support HTTP verb, path, query parameters, headers, and body content. |
| COM-002 | Signed AWS API calls | API requests to backend services shall support AWS Signature Version 4 with `execute-api` as the service name. |
| COM-003 | Streaming score updates | Live score events shall be processed through Kafka messages encoded with Apache Avro. |
| COM-004 | Notification queueing | Reminder requests shall be queued before SMS notification delivery. |

### 3.4 Data Exchange Formats
| ID | Format | Required Content |
|---|---|---|
| DEF-001 | JSON API payload | Default API request and response bodies shall use `application/json`. |
| DEF-002 | Match information payload | Fixtures, standings, schedules, results, live scores, and related match details. |
| DEF-003 | Prediction payload | Match outcome probabilities, including home win, draw, and away win or equivalent win/draw values. |
| DEF-004 | Screening recommendation payload | Venue or location recommendations for watching matches. |
| DEF-005 | Chatbot request | User text message and any collected intent slot values. |
| DEF-006 | Chatbot response | Conversation response returned by the backend handler. |
| DEF-007 | Reminder request | Game or team reminder context and phone number for SMS delivery. |
| DEF-008 | Streaming update payload | Live score update data encoded through Apache Avro. |

## 4. Functional Requirements

| ID | Requirement | Trigger/Input | System Behavior | Output | Priority | Verification |
|---|---|---|---|---|---|---|
| FR-001 | The system shall present football match information. | User requests match-related information. | The web application displays fixtures, standings, schedules, results, and live scores. | Match information view or data. | High | Demonstration |
| FR-002 | The system shall provide machine-learning match predictions. | User requests prediction output for a supported match or season prediction workflow. | The system obtains prediction values and presents probabilities for match outcomes such as home win, draw, and away win. | Prediction values shown to the user. | High | Demonstration |
| FR-003 | The system shall recommend nearby live match-screening venues. | User requests screening recommendations and provides location or city context. | The system searches or derives venue recommendations for live football match screenings near the user. | Screening recommendation list. | Medium | Demonstration |
| FR-004 | The system shall allow users to view fixtures and request reminders for upcoming games. | User views fixture data or requests reminder support. | The system presents upcoming game information and accepts reminder requests for those games. | Fixture view and reminder request confirmation. | Medium | Demonstration |
| FR-005 | The system shall send request-based SMS reminders. | User submits a valid reminder request with SMS delivery details. | The system queues the reminder request and sends the SMS notification through the notification workflow. | SMS reminder delivery or delivery-handling acknowledgment. | High | Test |
| FR-006 | The system shall exchange application data through API Gateway APIs. | Frontend submits an API request. | The system sends backend requests with HTTP method, path, optional query parameters, headers, and body through API Gateway using JSON defaults. | API request/response payload. | High | Inspection |
| FR-007 | The system shall persist and retrieve match data. | Match results, statistics, fixtures, or related data are created, updated, or queried. | The system stores match results, statistics, and fixtures in DynamoDB and connects the data to Elasticsearch for retrieval. | Stored and retrievable match data. | High | Test |
| FR-008 | The system shall process live score updates through streaming infrastructure. | Live score events are produced. | The system processes live score updates using Kafka with Apache Avro on EC2. | Updated live score data stream. | Medium | Analysis |
| FR-009 | The system shall provide a chatbot conversational interface for football information queries. | User enters a text message in the chatbot UI. | The frontend submits the message to the backend recommendation endpoint, and backend conversation or intent-handling logic returns a response. | Chatbot response message. | High | Test |
| FR-010 | The chatbot shall support football fixtures, match results, and match-screening location recommendations. | User asks about fixtures, results, or screening locations. | The conversation handler identifies the requested intent and returns the appropriate football information or recommendation response. | Fixture, result, or screening-location response. | High | Test |

## 5. Non-Functional Requirements

| ID | Requirement | Quality Attribute | Priority | Verification |
|---|---|---|---|---|
| NFR-001 | Protected application access shall use Cognito and IAM for authentication and security management. | Security | High | Inspection |
| NFR-002 | API interactions shall use `application/json` as the default content type and accept type unless explicitly overridden. | Interoperability | High | Test |
| NFR-003 | The system shall be deployable using AWS-managed or AWS-hosted components including S3, API Gateway, Lambda, DynamoDB, SNS, SQS, SageMaker, EC2, Cognito, IAM, and Elasticsearch. | Deployability | High | Inspection |
| NFR-004 | The system shall rely on DynamoDB and Elasticsearch to support growth in stored and requested match data, without defining a quantitative throughput, latency, or capacity target in this SRS. | Scalability | Medium | Architecture analysis |
| NFR-005 | The live score pipeline shall use a streaming data mechanism suitable for real-time score update processing. | Timeliness | Medium | Analysis |

## 6. Data Requirements

| ID | Data Item | Requirement |
|---|---|---|
| DR-001 | Match information | The system shall manage fixtures, standings, schedules, results, and live scores. |
| DR-002 | Prediction data | Prediction processing shall use prepared match data and produce match outcome probabilities. |
| DR-003 | Final-week prediction input | Final-week season prediction shall use current-season matches excluding the final week as input data. |
| DR-004 | Screening recommendation data | Screening recommendations shall include venue or location information relevant to live match viewing. |
| DR-005 | Chatbot data | Chatbot requests shall include user text and any extracted conversation intent or slot values needed for response generation. |
| DR-006 | Reminder data | Reminder requests shall include game or team reminder context and SMS delivery information. |
| DR-007 | Match storage data | Match results, statistics, and fixtures shall be stored in DynamoDB and connected to Elasticsearch for retrieval. |
| DR-008 | API payloads | API request and response payloads shall default to JSON. |
| DR-009 | Streaming payloads | Live score update data exchanged through the streaming infrastructure shall use Apache Avro. |

## 7. System Constraints

| ID | Constraint |
|---|---|
| C-001 | Frontend implementation shall use HTML, CSS, Bootstrap, and jQuery. |
| C-002 | Backend implementation shall use Python and Node. |
| C-003 | Static frontend hosting and relevant file storage shall use Amazon S3. |
| C-004 | Backend APIs shall be exposed through API Gateway and Lambda. |
| C-005 | Authentication and security management shall use Cognito and IAM. |
| C-006 | Notifications shall use SQS and SNS for queueing and SMS delivery. |
| C-007 | Match predictions shall use SageMaker. |
| C-008 | Match data storage and retrieval shall use DynamoDB and Elasticsearch. |
| C-009 | Live score update processing shall use Kafka with Apache Avro running on EC2. |
| C-010 | API integration shall use the `execute-api` service configuration and JSON content defaults. |
| C-011 | Service interaction details beyond the explicitly stated requirements shall be finalized in the architecture model rather than assumed by this SRS. |

## 8. Verification and Acceptance Criteria

| Requirement IDs | Verification Method | Acceptance Criteria |
|---|---|---|
| FR-001, DR-001 | Demonstration | A user can view fixtures, standings, schedules, results, and live scores through the web application. |
| FR-002, DR-002, DR-003, C-007 | Demonstration | A user can request and receive prediction output containing match outcome probabilities; final-week prediction input excludes the final week of the current season. |
| FR-003, DR-004 | Demonstration | A user can request and receive nearby live match-screening recommendations. |
| FR-004 | Demonstration | A user can view upcoming fixture information and submit a reminder request. |
| FR-005, DR-006, C-006 | Test | A valid reminder request is queued and handled for SMS notification delivery. |
| FR-006, DR-008, NFR-002, C-010 | Inspection and test | API request construction supports method, path, query parameters, headers, body, AWS `execute-api` configuration, and JSON defaults. |
| FR-007, DR-007, NFR-004, C-008 | Test and architecture analysis | Match results, statistics, and fixtures can be stored and retrieved through DynamoDB and Elasticsearch; no quantitative scale target is required beyond confirming the selected data services. |
| FR-008, DR-009, NFR-005, C-009 | Analysis | Live score updates are processed through Kafka and Apache Avro on EC2. |
| FR-009, FR-010, DR-005 | Test | The chatbot accepts a user text message and returns responses for fixtures, match results, and match-screening location recommendations. |
| NFR-001, C-005 | Inspection | Protected access uses Cognito and IAM integration. |
| NFR-003, C-001, C-002, C-003, C-004 | Inspection | The deployed application uses the specified frontend stack, backend stack, AWS hosting, API, and serverless components. |
| C-011 | Architecture review | The architecture model distinguishes explicitly required interactions from inferred or design-level service relationships. |
