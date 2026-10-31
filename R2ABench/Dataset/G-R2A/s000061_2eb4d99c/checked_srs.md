# Software Requirements Specification

## 1. Introduction

### 1.1 Purpose
This Software Requirements Specification defines the requirements for the `aws-solutions/iot-device-simulator` system as represented by the provided project materials and reviewed source artifacts. It is intended to support downstream architecture generation and verification planning.

### 1.2 Product Scope
The system is an AWS-based IoT Device Simulator. It provides:
- a web management console,
- simulation and device-type management APIs,
- device simulation execution,
- route data loading for simulation,
- publication of generated simulated-device messages to AWS IoT topics,
- deployment-time custom-resource processing for initialization and supporting resources.

The reviewed materials directly confirm API Gateway configuration, custom-resource response construction, and S3-backed route loading behavior. Broader platform capabilities are included here as product scope context.

### 1.3 Intended Audience
This document is intended for:
- solution architects designing or reviewing the system architecture,
- developers and maintainers implementing or extending the system,
- integrators deploying the solution into AWS environments,
- testers validating API, route-loading, and deployment-related behavior.

### 1.4 References
- Repository: `aws-solutions/iot-device-simulator`

## 2. Overall Description

### 2.1 Product Perspective
The product is a multi-component AWS-hosted IoT simulation system comprising:
- a web management console,
- API Gateway REST APIs,
- Lambda-based service integrations,
- deployment-time CloudFormation custom-resource handling,
- simulation components that load route data from Amazon S3,
- AWS-managed services supporting identity, persistence, orchestration, messaging, and device-message publication.

### 2.2 Product Functions Summary
The system supports:
- exposing deployed REST API endpoints and API identifiers,
- accepting REST methods including `GET`, `POST`, `PUT`, `DELETE`, and `OPTIONS`,
- validating request parameters and request bodies,
- configuring cross-origin request handling for supported headers,
- constructing CloudFormation custom-resource response bodies,
- loading route data from Amazon S3 and assembling route state for simulation,
- executing simulated device behavior,
- publishing generated simulated-device messages to AWS IoT topics.

### 2.3 User Classes
- Administrators and operators using the web console to manage simulations and device types
- API clients invoking simulator management APIs
- AWS deployment workflows invoking custom-resource processing
- Simulator components that load route state and execute device simulations

### 2.4 Operating Environment
The system operates in an AWS-managed environment that includes:
- web console hosting and distribution,
- identity and authentication services,
- Amazon API Gateway,
- AWS Lambda,
- Amazon DynamoDB,
- AWS Step Functions,
- Amazon S3,
- AWS IoT,
- AWS CloudFormation custom resources.

Component-specific runtime context includes:
- API Gateway configured as a regional REST API,
- simulator route loading that depends on an S3 bucket identified by `ROUTE_BUCKET`,
- custom-resource processing that depends on CloudFormation events, Lambda context, and solution versioning configuration.

### 2.5 Assumptions and Dependencies
- Route retrieval depends on an S3 bucket identified by `ROUTE_BUCKET`.
- Route loading depends on a route object key derived from either an input `routeName` or a generated default route key.
- API behavior depends on API Gateway request-validation and CORS configuration.
- Custom-resource processing depends on CloudFormation invocation context and solution configuration values.
- Device simulation and message publication depend on AWS service integrations available in the deployed environment.

## 3. External Interface Requirements

### 3.1 User Interfaces
The system shall provide a web-based management console for simulation and device-type management.

### 3.2 Software and API Interfaces
- The system shall expose an API Gateway REST API with a deployed endpoint and API ID.
- The API layer shall integrate with Lambda-backed service functionality.
- The system shall validate API request parameters and request bodies through configured request-validation mechanisms.
- The system shall construct a response body for CloudFormation custom-resource processing.
- The simulator shall retrieve route JSON data from Amazon S3 using the configured route bucket and resolved route object key.
- The system shall publish generated simulated-device messages to AWS IoT topics.

### 3.3 Communication Interfaces
- The API shall support HTTP methods `GET`, `POST`, `PUT`, `DELETE`, and `OPTIONS`.
- The API shall configure CORS preflight behavior for supported methods and headers.
- Allowed CORS request headers shall include `Authorization`, `Content-Type`, `X-Amz-Date`, `X-Amz-Security-Token`, and `X-Api-Key`.

### 3.4 Data Exchange Formats
- Route data shall be stored and exchanged as JSON.
- API access logs shall use JSON format.
- Custom-resource processing shall construct a CloudFormation response body.
- Simulated device messages shall be formatted for publication to AWS IoT topics.

## 4. Functional Requirements

### FR-001 API Deployment
The system shall create and deploy an API Gateway REST API and shall provide an API endpoint and API ID.

Verification: Inspection

### FR-002 CORS Preflight Configuration
The system shall configure CORS preflight options to:
- allow methods `GET`, `POST`, `PUT`, `DELETE`, and `OPTIONS`,
- allow request headers `Authorization`, `Content-Type`, `X-Amz-Date`, `X-Amz-Security-Token`, and `X-Api-Key`,
- set the preflight configuration `statusCode` to `200`.

Verification: Inspection

### FR-003 API Request Validation
The system shall validate request parameters and request bodies using configured API request-validation mechanisms.

Verification: Inspection

### FR-004 Custom-Resource Response Construction
The system shall construct a response body for CloudFormation custom-resource processing using the invocation context and configured solution values.

Verification: Test

### FR-005 Route Loading from S3
When a simulation snapshot provides `routeInfo.routeName`, the system shall use that value as the S3 object key. When `routeInfo.routeName` is absent, the system shall generate a default route key in the format `route-{random route identifier}.json`. The system shall then read the route object from the S3 bucket specified by `ROUTE_BUCKET`, parse the JSON payload, and assemble route state including route metadata and snapshot-derived fields.

Verification: Test

### FR-006 Route-Loading Error Propagation
If route retrieval from Amazon S3 fails, the system shall propagate the encountered error to the caller.

Verification: Test

### FR-007 Device Simulation Execution
The system shall execute simulated device behavior for managed device simulations.

Verification: Demonstration

### FR-008 Simulated Message Publication
The system shall publish generated simulated-device messages to AWS IoT topics.

Verification: Demonstration

## 5. Non-Functional Requirements

### NFR-001 Access Logging
The API deployment shall emit access logs to a log destination using JSON with standard fields.

Verification: Inspection

### NFR-002 Operational Logging Level
The API deployment shall use method logging level `INFO`.

Verification: Inspection

### NFR-003 Tracing
The API deployment shall have tracing enabled.

Verification: Inspection

### NFR-004 API Endpoint Type
The API endpoint type shall be `REGIONAL`.

Verification: Inspection

## 6. Data Requirements

### DR-001 Route Segment Structure
Route data shall support staged segments containing:
- `stage`,
- `start`,
- `end`,
- `km`.

The `start` and `end` fields shall be coordinate arrays.

### DR-002 Route State Output
Route-loading output shall include:
- `routeName`,
- `odometer`,
- `routeStage`,
- `burndown`,
- `burndownCalc`,
- `routeEnded`,
- `route`,
- `randomTriggers`.

The `routeName` value shall be either the input route name or the generated default route key.

### DR-003 Route Source Format
The route payload shall be stored as a JSON object in Amazon S3 and parsed from UTF-8 text.

### DR-004 Custom-Resource Input Context
Custom-resource processing shall use CloudFormation event data, Lambda context, and solution configuration values. Stack name shall be handled as a custom-resource input property.

## 7. System Constraints

### C-001 API Deployment Platform
The REST API is constrained to Amazon API Gateway deployment with stage name `prod`.

### C-002 Allowed HTTP Methods
The API configuration is constrained to methods `GET`, `POST`, `PUT`, `DELETE`, and `OPTIONS`.

### C-003 Route Storage Constraint
Route loading is constrained to Amazon S3 object retrieval using the bucket identified by `ROUTE_BUCKET` and a route key resolved from either the provided route name or the generated default route key.

### C-004 Custom-Resource Processing Context
Custom-resource processing is constrained by CloudFormation events, Lambda execution context, and solution ID/version configuration. Stack name shall be supplied as a custom-resource input property.

## 8. Verification and Acceptance Criteria

| Requirement ID | Verification Method | Acceptance Criteria |
|---|---|---|
| FR-001 | Inspection | API construct definitions show a deployed REST API with exposed API endpoint and API ID. |
| FR-002 | Inspection | API construct CORS preflight options specify methods `GET`, `POST`, `PUT`, `DELETE`, and `OPTIONS`; headers `Authorization`, `Content-Type`, `X-Amz-Date`, `X-Amz-Security-Token`, and `X-Api-Key`; and preflight `statusCode` `200`. |
| FR-003 | Inspection | API configuration includes validation for both request parameters and request body content. |
| FR-004 | Test | Custom-resource processing constructs a CloudFormation response body under the provided invocation context. |
| FR-005 | Test | Given a snapshot with `routeInfo.routeName`, the system uses that key for S3 retrieval; when `routeInfo.routeName` is absent, the system generates a default key in the required format, retrieves the route object from `ROUTE_BUCKET`, parses the JSON, and returns route state with the required fields. |
| FR-006 | Test | An S3 retrieval failure causes the route-loading operation to return or throw the encountered error to the caller. |
| FR-007 | Demonstration | The system runs managed device simulations and produces simulated device activity. |
| FR-008 | Demonstration | The system publishes generated simulated-device messages to AWS IoT topics during simulation execution. |
| NFR-001 | Inspection | API deployment configuration shows JSON-formatted access logging with standard fields enabled. |
| NFR-002 | Inspection | API deployment configuration specifies method logging level `INFO`. |
| NFR-003 | Inspection | API deployment configuration shows tracing enabled. |
| NFR-004 | Inspection | API configuration specifies endpoint type `REGIONAL`. |
| DR-001 | Inspection | Sample route data contains `stage`, `start`, `end`, and `km` fields, and `start` and `end` are coordinate arrays. |
| DR-002 | Inspection | Route-loading logic returns the listed route-state fields and sets `routeName` from either the input route name or the generated default key. |
| DR-003 | Inspection | Route-loading logic parses an Amazon S3 object body as UTF-8 JSON text. |
| DR-004 | Inspection | Custom-resource handling uses CloudFormation event data and Lambda context, and treats stack name as an input property. |
| C-001 | Inspection | API deployment configuration specifies stage `prod`. |
| C-002 | Inspection | API configuration restricts methods to `GET`, `POST`, `PUT`, `DELETE`, and `OPTIONS`. |
| C-003 | Inspection | Route-loading logic uses `ROUTE_BUCKET` and a resolved route key for S3 retrieval. |
| C-004 | Inspection | Custom-resource processing uses CloudFormation invocation context and solution ID/version configuration, with stack name supplied through input properties. |
