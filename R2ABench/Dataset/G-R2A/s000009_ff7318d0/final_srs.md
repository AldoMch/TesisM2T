# Software Requirements Specification

## 1. Introduction

### Purpose
This SRS defines evidence-backed software requirements for `foot365-live-streaming-chatbot-prediction-app-on-aws` at commit `3f424fa0347bf989489aeafbfae03266d70cf0c0`. It captures the externally observable behavior and operating constraints supported by the repository evidence.

### Product Scope
Foot365 is an AWS-based web application for football enthusiasts that provides match information including fixtures, standings, schedules, live scores, results, match predictions, and nearby live match screenings. The application also supports team schedule management and request-based reminders through email and SMS. Sources: `E001`, `E005`, `E006`.

### Intended Audience
This document is intended for product owners, developers, testers, reviewers, and deployers working on or evaluating the Foot365 application. Scope is limited to behavior and constraints supported by repository evidence.

### References
- Repository: `adityajain10/foot365-live-streaming-chatbot-prediction-app-on-aws`
- Commit: `3f424fa0347bf989489aeafbfae03266d70cf0c0`
- Evidence sources: `README.md`, `FrontEnd/js/apigClient.js`, `FrontEnd/js/lib/apiGatewayCore/simpleHttpClient.js`

## 2. Overall Description

### Product Perspective
The product is a web application with a frontend built using HTML, CSS, Bootstrap, and jQuery, and a backend using Python and Node on AWS services including S3, API Gateway, Lambda, Cognito, IAM, SQS, SNS, SageMaker, EC2, DynamoDB, and Elasticsearch. Sources: `E003`, `E004`, `E005`, `E006`.

### Product Functions Summary
- Provide football match fixtures, standings, schedules, results, and live scores. `E001`
- Provide match outcome predictions using machine learning. `E002`, `E006`
- Suggest sports screening recommendations near the user. `E001`
- Manage team schedules and provide upcoming game reminders. `E001`
- Support user-requested email and SMS reminders. `E001`, `E005`
- Exchange data with backend APIs using JSON over API Gateway. `E003`, `E004`

### User Classes
- Football enthusiasts seeking match information, predictions, and screenings. `E001`
- Users requesting reminder notifications by email or SMS. `E001`

### Operating Environment
- Web frontend hosted on Amazon S3. `E005`
- Backend services exposed through Amazon API Gateway and Lambda. `E005`
- Authentication and security management through Amazon Cognito and IAM. `E005`
- Data storage in DynamoDB with connection to Elasticsearch. `E002`, `E006`
- Prediction services using Amazon SageMaker. `E002`, `E006`
- Live score update pipeline on EC2 using Kafka with Apache Avro. `E005`

### Assumptions and Dependencies
- The application depends on AWS managed and hosted services listed in the technology stack. `E005`
- API interactions use `application/json` by default. `E003`, `E004`
- Match prediction depends on data from matches already played in the current season except the final week, as stated for the described prediction setup. `E005`

## 3. External Interface Requirements

### User Interfaces
The system shall provide a web-based user interface implemented with HTML, CSS, Bootstrap, and jQuery. `E005`

### Software/API Interfaces
- The frontend shall invoke backend endpoints through Amazon API Gateway. `E003`, `E004`, `E005`
- The system shall integrate with Cognito and IAM for authentication and security management. `E005`
- The system shall integrate with SNS and SQS for notifications and queuing. `E005`
- The system shall integrate with SageMaker for match prediction generation. `E002`, `E006`
- The system shall integrate with DynamoDB and Elasticsearch for match data storage and retrieval. `E002`, `E006`

### Communication Interfaces
- API requests shall support HTTP verb, path, query parameters, headers, and body content. `E004`
- API requests to backend services shall use AWS Signature Version 4 configuration with `execute-api` as the service name. `E003`

### Data Exchange Formats
- Default request and response content types for API interactions shall be `application/json` unless explicitly overridden. `E003`, `E004`
- Live score update infrastructure uses Kafka with Apache Avro. `E005`

## 4. Functional Requirements

| ID | Description | Trigger/Input | System Behavior | Output | Priority | Verification | Source Evidence |
|---|---|---|---|---|---|---|---|
| FR-001 | Provide football match information | User requests match-related information | The system shall present match fixtures, standings, schedules, results, and live scores to users through the web application. | Match information view/data | High | Demonstration | `E001` |
| FR-002 | Provide match predictions | User requests a prediction for a match or season outcome supported by the prediction workflow | The system shall obtain and present machine-learning-based predictions including probability of draw and win. | Prediction values presented to user | High | Demonstration | `E002`, `E006` |
| FR-003 | Recommend nearby live screenings | User requests screening information | The system shall suggest sports screening recommendations near the user. | Screening recommendations | Medium | Demonstration | `E001` |
| FR-004 | Support team schedule management and reminders | User manages team schedule or requests reminder support | The system shall manage team schedules and provide reminders about upcoming games. | Updated schedule state and reminder confirmation | Medium | Demonstration | `E001` |
| FR-005 | Send request-based email and SMS reminders | User requests notification delivery | The system shall support reminder notifications through email and SMS on a request basis. | Email or SMS reminder delivery/request acknowledgment | High | Test | `E001`, `E005` |
| FR-006 | Exchange application data through API Gateway APIs | Frontend submits an API request | The system shall send backend requests with HTTP method, path, optional query parameters, headers, and body through API Gateway using JSON defaults. | API request/response payload | High | Inspection | `E003`, `E004` |
| FR-007 | Persist and retrieve match data | Match data is created, updated, or queried | The system shall store match results, stats, and fixtures in DynamoDB and connect that data with Elasticsearch. | Stored and retrievable match data | High | Test | `E002`, `E006` |
| FR-008 | Process live score updates through streaming infrastructure | Live score events are produced | The system shall use Kafka with Apache Avro on EC2 for live score updates. | Updated live score data stream | Medium | Analysis | `E005` |

## 5. Non-Functional Requirements

| ID | Requirement | Priority | Verification | Evidence Type | Source Evidence |
|---|---|---|---|---|---|
| NFR-001 | The system shall require authentication and security management through Amazon Cognito and IAM for protected application access. | High | Inspection | explicit | `E005` |
| NFR-002 | The system shall use `application/json` as the default content type and accept type for API interactions unless explicitly overridden. | High | Test | explicit | `E003`, `E004` |
| NFR-003 | The system shall be deployable using AWS-managed and AWS-hosted components including S3, API Gateway, Lambda, DynamoDB, SNS, SQS, SageMaker, EC2, Cognito, and IAM. | High | Inspection | explicit | `E005` |
| NFR-004 | The system should support growth in stored and requested match data by relying on DynamoDB and Elasticsearch for match results, stats, and fixtures; this scalability expectation is inferred from the selected platform capabilities rather than a repository-defined service level. | Medium | Analysis | inferred | `E002`, `E006` |

## 6. Data Requirements

| Category | Requirement | Source Evidence |
|---|---|---|
| Data entities | The system shall manage match results, match stats, fixtures, live scores, schedules, predictions, and screening recommendations. | `E001`, `E002`, `E006` |
| Prediction data | Prediction processing shall use prepared match data and produce probabilities of draw and win. | `E002`, `E005`, `E006` |
| Notification data | Reminder requests shall support user-requested email and SMS notifications. | `E001`, `E005` |
| Storage | Match results, stats, and fixtures shall be stored in DynamoDB and connected with Elasticsearch. | `E002`, `E006` |
| Exchange format | API request and response payloads shall default to JSON. | `E003`, `E004` |
| Streaming format | Live score update data exchanged through Kafka infrastructure shall use Apache Avro. | `E005` |

## 7. Constraints

| ID | Constraint | Source Evidence |
|---|---|---|
| C-001 | Frontend technology is constrained to the documented stack of HTML, CSS, Bootstrap, and jQuery. | `E005` |
| C-002 | Backend technology is constrained to Python and Node. | `E005` |
| C-003 | Deployment is constrained to the documented AWS service stack including S3, API Gateway, Lambda, Cognito, IAM, SQS, SNS, SageMaker, EC2, DynamoDB, and Elasticsearch. | `E005` |
| C-004 | API integration is constrained to AWS API Gateway using the `execute-api` service configuration and JSON content defaults. | `E003`, `E004` |
| C-005 | Live score update processing is constrained to Kafka with Apache Avro running on EC2. | `E005` |

## 8. Verification and Acceptance

| Requirement ID | Verification Method | Acceptance Basis |
|---|---|---|
| FR-001 | Demonstration | A user can view fixtures, standings, schedules, results, and live scores. |
| FR-002 | Demonstration | A user can request and receive prediction output including draw/win probabilities. |
| FR-003 | Demonstration | A user can request and receive nearby screening recommendations. |
| FR-004 | Demonstration | A user can manage schedules and receive upcoming game reminder behavior. |
| FR-005 | Test | A reminder request results in email and/or SMS notification handling. |
| FR-006 | Inspection | API request construction supports method, path, query params, headers, body, and JSON defaults. |
| FR-007 | Test | Match results, stats, and fixtures can be stored and retrieved through the documented data services. |
| FR-008 | Analysis | Live score updates are processed through the documented Kafka/Avro on EC2 pipeline. |
| NFR-001 | Inspection | Protected access uses Cognito and IAM integration. |
| NFR-002 | Test | API requests and responses default to `application/json` unless overridden. |
| NFR-003 | Inspection | Deployment architecture uses the documented AWS-managed components. |
| NFR-004 | Analysis | Architecture review shows data growth support depends on DynamoDB and Elasticsearch platform capabilities. |

## 9. Traceability Matrix

| ID | Requirement | Type | Source | Evidence Type | Verification | Confidence |
|---|---|---|---|---|---|---|
| FR-001 | Provide fixtures, standings, schedules, results, and live scores | Functional | `E001` | explicit | Demonstration | High |
| FR-002 | Provide ML-based match predictions with draw/win probabilities | Functional | `E002`, `E006` | explicit | Demonstration | High |
| FR-003 | Recommend nearby live match screenings | Functional | `E001` | explicit | Demonstration | Medium |
| FR-004 | Manage team schedules and provide upcoming game reminders | Functional | `E001` | explicit | Demonstration | Medium |
| FR-005 | Support request-based email and SMS reminders | Functional | `E001`, `E005` | explicit | Test | High |
| FR-006 | Send backend API requests through API Gateway using JSON defaults | Functional | `E003`, `E004` | explicit | Inspection | High |
| FR-007 | Store and retrieve match results, stats, and fixtures via DynamoDB and Elasticsearch | Functional | `E002`, `E006` | explicit | Test | High |
| FR-008 | Use Kafka with Apache Avro on EC2 for live score updates | Functional | `E005` | explicit | Analysis | Medium |
| NFR-001 | Use Cognito and IAM for authentication and security management | Non-functional | `E005` | explicit | Inspection | High |
| NFR-002 | Default API content and accept types to `application/json` | Non-functional | `E003`, `E004` | explicit | Test | High |
| NFR-003 | Be deployable on the documented AWS service stack | Non-functional | `E005` | explicit | Inspection | High |
| NFR-004 | Support data growth through DynamoDB and Elasticsearch platform capabilities | Non-functional | `E002`, `E006` | inferred | Analysis | Medium |
