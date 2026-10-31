# Software Requirements Specification

## 1. Introduction

### 1.1 Purpose
This SRS specifies evidenced requirements for the repository snapshot of `aws-solutions/iot-device-simulator` at commit `6ee7b0261b9ba2a045f533e54be603d3af939e9b`. It is limited to behaviors and interfaces directly supported by the repository evidence pack.

### 1.2 Product scope
The evidenced system scope includes:
- an AWS API Gateway REST API construct for the IoT Device Simulator,
- a CloudFormation custom-resource interaction path,
- vehicle route data loading for simulation from Amazon S3.

### 1.3 Intended audience
- Deployers and operators integrating the solution into AWS environments
- API integrators consuming the REST API
- Testers verifying deployment and route-loading behaviors
- Maintainers assessing traceable functional and interface requirements

### 1.4 References
- Repository: `aws-solutions/iot-device-simulator`
- Repository URL: https://github.com/aws-solutions/iot-device-simulator
- Snapshot URL: https://github.com/aws-solutions/iot-device-simulator/tree/6ee7b0261b9ba2a045f533e54be603d3af939e9b
- Evidence sources:
  - `source/infrastructure/lib/api.ts` (E003, E004)
  - `source/custom-resource/test/index.test.ts` (E002)
  - `source/simulator/lib/device/generators/vehicle/dynamics/dynamics-model.js` (E005, E006)
  - `source/resources/routes/route-b.json` (E001)

## 2. Overall Description

### 2.1 Product perspective
The product is an AWS-hosted solution component set. Evidence shows:
- an API Gateway REST API front end,
- Lambda-backed microservice integration,
- CloudFormation custom-resource handling,
- S3-backed route data retrieval for a vehicle simulator.

### 2.2 Product functions summary
- Expose a deployed REST API endpoint and API identifier
- Accept REST methods including `GET`, `POST`, `PUT`, `DELETE`, and `OPTIONS`
- Validate request parameters and request bodies
- Support CORS headers including `X-Api-Key`
- Build and return a CloudFormation custom-resource response body
- Load route data from S3 and assemble route state for simulation

### 2.3 User classes
- API clients invoking the simulator REST API
- AWS deployment workflows invoking the custom resource
- Simulator components loading vehicle route state from S3

### 2.4 Operating environment
- AWS API Gateway REST API (`REGIONAL` endpoint type)
- AWS Lambda
- Amazon S3
- AWS CloudFormation custom-resource execution context
- Environment variables including `AWS_REGION`, `SOLUTION_ID`, `SOLUTION_VERSION`, `STACK_NAME`, and `ROUTE_BUCKET`

### 2.5 Assumptions and dependencies
- Route retrieval depends on an S3 bucket identified by `ROUTE_BUCKET` and an object key derived from `routeName`. (E005)
- API deployment depends on API Gateway request validation and stage deployment configuration. (E004)
- Custom-resource behavior depends on AWS-provided invocation context and solution environment variables. (E002)

## 3. External Interface Requirements

### 3.1 User interfaces
No end-user graphical interface is evidenced in the provided materials.

### 3.2 Software/API interfaces

| Interface | Requirement summary | Source |
|---|---|---|
| REST API | The system exposes an API Gateway REST API with a deployed endpoint and API ID. | E003, E004 |
| Request validation | The API validates request parameters and request bodies. | E004 |
| CloudFormation custom resource | The system builds a CloudFormation response body during custom-resource handling. | E002 |
| S3 route retrieval | The simulator retrieves route JSON from S3 using bucket `ROUTE_BUCKET` and object key `routeName`. | E005 |

### 3.3 Communication interfaces

| Interface | Requirement summary | Source |
|---|---|---|
| API methods | Supported methods include `GET`, `POST`, `PUT`, `DELETE`, and `OPTIONS`. | E004 |
| CORS headers | Allowed headers include `Content-Type`, `X-Amz-Date`, `Authorization`, and `X-Api-Key`. | E004 |

### 3.4 Data exchange formats

| Format | Description | Source |
|---|---|---|
| JSON route file | Route data is JSON-parsed from S3 and includes staged route segments. | E001, E005 |
| JSON access log | API access logs use JSON with standard fields. | E004 |
| CloudFormation response body | Custom-resource handling constructs a response body for CloudFormation. | E002 |

## 4. Functional Requirements

| ID | Description | Trigger/Input | System behavior | Output | Priority | Verification | Source evidence |
|---|---|---|---|---|---|---|---|
| FR-001 | Expose a deployed REST API for the IoT Device Simulator. | Deployment or initialization of the API construct | The system shall create an API Gateway REST API, deploy it, and provide an API endpoint and API ID. | Reachable API deployment metadata including endpoint and API ID | High | Inspection | E003, E004 |
| FR-002 | Support core REST methods and CORS headers for API access. | Client request or CORS preflight request | The system shall allow methods `GET`, `POST`, `PUT`, `DELETE`, and `OPTIONS`, and shall allow headers `Content-Type`, `X-Amz-Date`, `Authorization`, and `X-Api-Key`. | API responses compatible with the allowed methods and headers; CORS status code `200` | High | Test | E004 |
| FR-003 | Validate incoming API requests. | Client request containing parameters and/or body | The system shall validate request parameters and request bodies through the configured API request validator. | Accepted requests proceed; invalid requests are rejected by API Gateway validation | High | Inspection | E004 |
| FR-004 | Build a CloudFormation custom-resource response body. | CloudFormation custom-resource invocation | The system shall construct a response body for the custom-resource response using the invocation context and configured environment. | CloudFormation response body | Medium | Test | E002 |
| FR-005 | Load route data from S3 for vehicle simulation. | A snapshot containing `routeInfo.routeName` | The system shall read the route object from the S3 bucket named by `ROUTE_BUCKET` using the `routeName` key, parse the JSON payload, and assemble route state including route metadata and snapshot-derived fields. | Route state object containing route data and route-related state | High | Test | E005 |
| FR-006 | Propagate route-loading failures. | Failure during S3 route retrieval | The system shall throw the encountered error when route retrieval from S3 fails. | Error returned to the caller | Medium | Test | E005 |

## 5. Non-Functional Requirements

| ID | Quality attribute | Requirement | Priority | Verification | Source evidence | Evidence type |
|---|---|---|---|---|---|---|
| NFR-001 | Maintainability / observability | The API deployment shall emit access logs to a log destination using JSON with standard fields. | Medium | Inspection | E004 | explicit |
| NFR-002 | Operability | The API deployment shall use `INFO` method logging level. | Medium | Inspection | E004 | explicit |
| NFR-003 | Traceability / observability | The API deployment shall have tracing enabled. | Medium | Inspection | E004 | explicit |
| NFR-004 | Compatibility | The API endpoint type shall be `REGIONAL`. | Medium | Inspection | E004 | explicit |

## 6. Data Requirements

### 6.1 Data entities and objects

| ID | Data entity | Requirement | Source evidence |
|---|---|---|---|
| DR-001 | Route segment | Route data shall support staged segments containing `stage`, `start`, `end`, and `km` fields; `start` and `end` are coordinate arrays. | E001 |
| DR-002 | Route state | Route-loading output shall include `routeName`, `odometer`, `routeStage`, `burndown`, `burndownCalc`, `routeEnded`, `route`, and `randomTriggers`. | E005 |
| DR-003 | Route source object | The route payload shall be stored as a JSON object in S3 and parsed from UTF-8 text. | E005 |

### 6.2 Input/output data

| Data flow | Input | Output | Source evidence |
|---|---|---|---|
| API request validation | Request parameters and request body | Validation pass/fail at API Gateway | E004 |
| Custom resource | Invocation context and environment variables | CloudFormation response body | E002 |
| Route loading | `routeInfo.routeName`, `ROUTE_BUCKET`, snapshot fields | Parsed route state object or thrown error | E005 |

## 7. Constraints

| ID | Constraint | Source evidence |
|---|---|---|
| C-001 | The REST API is constrained to API Gateway deployment with stage name `prod`. | E004 |
| C-002 | The API configuration is constrained to allowed methods `GET`, `POST`, `PUT`, `DELETE`, and `OPTIONS`. | E004 |
| C-003 | Route loading is constrained to S3 object retrieval using bucket environment variable `ROUTE_BUCKET` and key `routeName`. | E005 |
| C-004 | Custom-resource execution is constrained by environment variables `AWS_REGION`, `SOLUTION_ID`, `SOLUTION_VERSION`, and `STACK_NAME`. | E002 |
| C-005 | Repository source files in evidence declare SPDX license identifier `Apache-2.0`. | E006 |

## 8. Verification and Acceptance

| Requirement ID | Verification method | Acceptance criteria |
|---|---|---|
| FR-001 | Inspection | API construct definition shows deployed REST API with exposed endpoint and API ID. |
| FR-002 | Test | Requests and preflight interactions demonstrate the allowed methods, headers, and `200` CORS status behavior. |
| FR-003 | Inspection | API configuration includes a request validator with request parameters and request body validation enabled. |
| FR-004 | Test | Custom-resource tests confirm construction of a CloudFormation response body under the provided invocation context. |
| FR-005 | Test | Given a valid `routeName` and `ROUTE_BUCKET`, route-loading returns parsed route state with the required fields. |
| FR-006 | Test | An S3 retrieval failure causes the route-loading operation to throw the encountered error. |
| NFR-001 | Inspection | API deployment configuration shows JSON access logs with standard fields enabled. |
| NFR-002 | Inspection | API deployment configuration shows `INFO` method logging level. |
| NFR-003 | Inspection | API deployment configuration shows tracing enabled. |
| NFR-004 | Inspection | API configuration specifies endpoint type `REGIONAL`. |
| DR-001 | Inspection | Sample route data contains `stage`, `start`, `end`, and `km` fields. |
| DR-002 | Inspection | Route-loading logic returns the listed route-state fields. |
| DR-003 | Inspection | Route-loading logic parses S3 object body as UTF-8 JSON text. |
| C-001 | Inspection | API deployment configuration specifies stage `prod`. |
| C-002 | Inspection | API configuration restricts the listed HTTP methods. |
| C-003 | Inspection | Route-loading logic uses `ROUTE_BUCKET` and `routeName` for S3 retrieval. |
| C-004 | Inspection | Custom-resource test context includes the listed environment variables. |
| C-005 | Inspection | Evidence file header contains SPDX identifier `Apache-2.0`. |

## 9. Traceability Matrix

| ID | Requirement | Type | Source | Evidence Type | Verification | Confidence |
|---|---|---|---|---|---|---|
| FR-001 | Expose a deployed REST API with endpoint and API ID | Functional | E003, E004 | explicit | Inspection | High |
| FR-002 | Support listed REST methods and CORS headers | Functional | E004 | explicit | Test | High |
| FR-003 | Validate request parameters and request bodies | Functional | E004 | explicit | Inspection | High |
| FR-004 | Build a CloudFormation custom-resource response body | Functional | E002 | explicit | Test | Medium |
| FR-005 | Load route data from S3 and assemble route state | Functional | E005 | explicit | Test | High |
| FR-006 | Propagate route-loading failures | Functional | E005 | explicit | Test | High |
| NFR-001 | Emit JSON access logs with standard fields | Non-functional | E004 | explicit | Inspection | High |
| NFR-002 | Use `INFO` method logging level | Non-functional | E004 | explicit | Inspection | High |
| NFR-003 | Enable tracing | Non-functional | E004 | explicit | Inspection | High |
| NFR-004 | Use `REGIONAL` endpoint type | Non-functional | E004 | explicit | Inspection | High |
| DR-001 | Route segments contain `stage`, `start`, `end`, `km` | Data | E001 | explicit | Inspection | High |
| DR-002 | Route state includes named route and snapshot fields | Data | E005 | explicit | Inspection | High |
| DR-003 | Route payload is parsed from UTF-8 JSON in S3 | Data | E005 | explicit | Inspection | High |
| C-001 | API stage is `prod` | Constraint | E004 | explicit | Inspection | High |
| C-002 | API methods limited to listed verbs | Constraint | E004 | explicit | Inspection | High |
| C-003 | Route loading depends on `ROUTE_BUCKET` and `routeName` | Constraint | E005 | explicit | Inspection | High |
| C-004 | Custom-resource depends on AWS solution environment variables | Constraint | E002 | explicit | Inspection | Medium |
| C-005 | Source evidence declares Apache-2.0 license identifier | Constraint | E006 | explicit | Inspection | High |
