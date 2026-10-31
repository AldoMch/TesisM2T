# Software Requirements Specification

## 1. Introduction

### Purpose
This SRS defines evidence-backed software requirements for the `ae-prediction-cards` repository snapshot at commit `99dae5686d1542aae88bc67a22370ec6c6a567a0`. The specification is limited to behavior and interfaces supported by the provided repository evidence.

### Product scope
The repository contains:
- An oracle service that periodically checks for oracle requests, answers them, and checks whether an extension is necessary.
- A frontend API layer that uses an Aeternity wallet client to interact with a prediction cards smart-contract interface, including creation of predictions.
- Test and deployment artifacts showing HTTP CORS handling and Aeternity transaction-domain integrations.

### Intended audience
This document is intended for:
- Maintainers of the oracle service and frontend integration
- Test engineers validating repository-supported behaviors
- Integrators working with the frontend API and blockchain/oracle environment

### References
- Repository: `kryptokrauts/ae-prediction-cards`
- Commit: `99dae5686d1542aae88bc67a22370ec6c6a567a0`
- Evidence sources: `E001` to `E006`

## 2. Overall Description

### Product perspective
The product is a multi-component system comprising:
- A Quarkus-based oracle service with scheduled background processing (`E001`)
- A React-based frontend provider/API layer bound to an Aeternity wallet (`E003`, `E004`)
- Test infrastructure tied to HTTP CORS behavior and Aeternity blockchain transaction types (`E002`, `E005`, `E006`)

### Product functions summary
Supported functions evidenced in the repository are:
- Periodically checking for oracle requests (`E001`)
- Answering oracle requests (`E001`)
- Periodically checking whether oracle extension is necessary (`E001`)
- Creating prediction records through a frontend API method that submits event and image data through an interactive blockchain instance (`E004`)
- Providing the prediction-cards API to frontend components through context and wallet binding (`E003`)
- Accepting browser cross-origin requests using `GET`, `POST`, and `OPTIONS` with defined headers (`E002`)

### User classes
| User class | Description | Evidence |
|---|---|---|
| Frontend user with wallet | User operating the frontend through a connected wallet-backed API context | E003, E004 |
| Service operator | User or operator responsible for running the oracle service with mandatory environment configuration | E001 |
| Integration/test operator | User validating blockchain and HTTP integration behavior in test infrastructure | E002, E005, E006 |

### Operating environment
| Environment aspect | Supported statement | Evidence |
|---|---|---|
| Oracle runtime | The oracle service uses Quarkus and supports dev mode and packaged execution | E001 |
| Frontend runtime | The frontend uses React and an Aeternity wallet client/provider model | E003, E004 |
| Blockchain integration | The system integrates with Aeternity SDK types and services | E004, E005, E006 |
| HTTP boundary | CORS configuration is present for browser-style cross-origin requests | E002 |

### Assumptions and dependencies
| Item | Statement | Evidence | Evidence type |
|---|---|---|---|
| A1 | The oracle service depends on a mandatory `.env` file containing required properties. | E001 | explicit |
| A2 | Frontend contract interaction depends on an available wallet client. | E003, E004 | explicit |
| A3 | Prediction contract interaction depends on resolution of or interaction with `predictioncards.chain`. | E004 | explicit |
| A4 | Blockchain operation depends on Aeternity network/service components. | E004, E005, E006 | explicit |

## 3. External Interface Requirements

### User interfaces
| Interface | Requirement summary | Evidence |
|---|---|---|
| Frontend API context | The frontend shall expose a prediction-cards API to child components through a context provider bound to the current wallet. | E003 |
| Service runtime interface | The oracle service shall be runnable in development and packaged modes, with environment-based configuration. | E001 |

### Software/API interfaces
| Interface | Requirement summary | Evidence |
|---|---|---|
| Wallet interface | The frontend prediction API shall use a wallet client as its integration point for blockchain interaction. | E003, E004 |
| Smart-contract method interface | The frontend prediction API shall invoke a contract method named `create_prediction` through an interactive instance. | E004 |
| AENS name reference | The frontend API uses the AENS name `predictioncards.chain`. | E004 |
| Aeternity service/test interfaces | Test infrastructure uses Aeternity service, transaction, oracle, and AENS domain models. | E005, E006 |

### Communication interfaces
| Interface | Requirement summary | Evidence |
|---|---|---|
| HTTP CORS | Cross-origin HTTP access shall allow `GET`, `POST`, and `OPTIONS` methods. | E002 |
| HTTP headers | Cross-origin HTTP access shall allow and expose configured request/response headers including `Content-Type`, `Cache-Control`, `Range`, and related headers shown in configuration. | E002 |

### Data exchange formats
| Format/item | Supported statement | Evidence |
|---|---|---|
| Prediction creation inputs | Prediction creation accepts an event object plus two image string values: `img_higher` and `img_lower`. | E004 |
| Date conversion input | Prediction creation converts the event start timestamp before contract submission. | E004 |
| Environment configuration | Oracle-service runtime configuration is supplied through `.env` properties. | E001 |

## 4. Functional Requirements

| ID | Description | Trigger/Input | System behavior | Output | Priority | Verification | Source evidence |
|---|---|---|---|---|---|---|---|
| FR-001 | Oracle request polling | Scheduled runtime execution in the oracle service | The system shall periodically check for oracle requests. | Oracle requests are detected for further handling. | High | Inspection | E001 |
| FR-002 | Oracle response handling | Oracle requests identified by the periodic check | The system shall answer oracle requests. | Oracle responses are submitted. | High | Inspection | E001 |
| FR-003 | Oracle extension check | Scheduled runtime execution in the oracle service | The system shall periodically check whether an oracle extension is necessary. | Extension necessity is determined and acted on by the service workflow. | Medium | Inspection | E001 |
| FR-004 | Mandatory oracle-service configuration | Oracle service startup | The system shall require an `.env` file containing the properties needed for proper running. | Service startup is configuration-backed. | High | Inspection | E001 |
| FR-005 | Frontend API provisioning | Rendering of the prediction-cards provider with child components | The system shall create a prediction-cards API instance from the current wallet and provide it through React context to children. | Child components can obtain the API from context. | High | Demonstration | E003 |
| FR-006 | Prediction creation submission | Call to `createPrediction(event, img_higher, img_lower)` | The system shall obtain an interactive instance and invoke the contract method `create_prediction` using the event start timestamp conversion and supplied image strings. | A prediction-creation contract call is submitted. | High | Inspection | E004 |
| FR-007 | Wallet-backed contract interaction | Frontend API initialization and usage | The system shall use the wallet client as the contract interaction dependency for prediction-card operations. | Blockchain interactions are performed through the wallet-backed API. | High | Inspection | E003, E004 |
| FR-008 | CORS method support | Cross-origin HTTP request | The system shall allow `GET`, `POST`, and `OPTIONS` methods for cross-origin access. | Requests using the allowed methods pass CORS method validation. | Medium | Test | E002 |
| FR-009 | CORS header support | Cross-origin HTTP request with configured headers | The system shall allow and expose the configured CORS headers, including `Content-Type`, `Cache-Control`, `Content-Range`, and `Range`. | Browser clients can send and read the configured headers in cross-origin flows. | Medium | Test | E002 |

## 5. Non-Functional Requirements

| ID | Quality attribute | Requirement | Priority | Verification | Source evidence | Confidence |
|---|---|---|---|---|---|---|
| NFR-001 | Interoperability | The frontend integration shall operate with an Aeternity wallet client and Aeternity SDK-based contract interaction components. | High | Inspection | E003, E004, E005, E006 | High |
| NFR-002 | Portability | The oracle service shall support both development-mode execution and packaged execution. | Medium | Demonstration | E001 | High |
| NFR-003 | Configurability | The oracle service shall externalize required runtime properties through a mandatory `.env` file. | High | Inspection | E001 | High |
| NFR-004 | Web compatibility | The HTTP-facing test/deployment configuration shall support browser cross-origin access with the explicitly configured methods and headers. | Medium | Test | E002 | High |
| NFR-005 | Availability of scheduled processing | The oracle service shall perform its oracle-checking and extension-checking behavior periodically rather than only on manual invocation. | High | Inspection | E001 | Medium |

## 6. Data Requirements

| ID | Data item/entity | Requirement | Source evidence | Evidence type |
|---|---|---|---|---|
| DR-001 | Prediction event | The system shall accept a `PredictionEvent` object as input to prediction creation. | E004 | explicit |
| DR-002 | Prediction images | The system shall accept two image string inputs for prediction creation: `img_higher` and `img_lower`. | E004 | explicit |
| DR-003 | Event start timestamp | The system shall use the event start timestamp as data for prediction creation and convert it before contract submission. | E004 | explicit |
| DR-004 | AENS name | The frontend API shall reference the AENS name `predictioncards.chain` for contract-related interaction. | E004 | explicit |
| DR-005 | Environment properties | The oracle service shall consume required runtime properties from an `.env` file. | E001 | explicit |
| DR-006 | Blockchain transaction/oracle objects | Test and integration behavior shall be compatible with Aeternity transaction, oracle, and AENS-related domain objects present in the repository tests. | E005, E006 | explicit |

## 7. Constraints

| ID | Constraint | Source evidence | Evidence type |
|---|---|---|---|
| C-001 | The oracle service is constrained to a Quarkus-based implementation/runtime model. | E001 | explicit |
| C-002 | Frontend contract interaction is constrained to Aeternity wallet and SDK components. | E003, E004 | explicit |
| C-003 | Cross-origin HTTP behavior is constrained to the configured CORS methods and headers shown in the repository configuration. | E002 | explicit |
| C-004 | Oracle-service operation is constrained by the presence of a mandatory `.env` file. | E001 | explicit |

## 8. Verification and Acceptance

| Requirement ID | Verification method | Acceptance criterion |
|---|---|---|
| FR-001 | Inspection | Repository artifacts show scheduled logic that checks for oracle requests. |
| FR-002 | Inspection | Repository artifacts show logic that answers oracle requests. |
| FR-003 | Inspection | Repository artifacts show scheduled logic that checks whether extension is necessary. |
| FR-004 | Inspection | Service documentation/runtime setup states `.env` is mandatory for proper running. |
| FR-005 | Demonstration | Rendering the provider makes the API obtainable from context by child components. |
| FR-006 | Inspection | Code inspection shows `createPrediction` obtaining an interactive instance and calling `create_prediction` with the documented inputs. |
| FR-007 | Inspection | Code inspection shows wallet-backed dependency injection into the prediction API. |
| FR-008 | Test | Cross-origin requests using `GET`, `POST`, and `OPTIONS` succeed under the configured CORS policy. |
| FR-009 | Test | Cross-origin requests can use and expose the configured headers under the CORS policy. |
| NFR-001 | Inspection | Integration points use wallet/Aeternity SDK types consistently. |
| NFR-002 | Demonstration | Oracle service can be run in development mode and packaged mode as documented. |
| NFR-003 | Inspection | Runtime configuration is sourced from `.env` as documented. |
| NFR-004 | Test | Browser-style CORS behavior matches configured methods and headers. |
| NFR-005 | Inspection | Service behavior is defined as periodic in repository documentation. |

## 9. Traceability Matrix

| ID | Requirement | Type | Source | Evidence Type | Verification | Confidence |
|---|---|---|---|---|---|---|
| FR-001 | Periodically check for oracle requests | Functional | E001 | explicit | Inspection | High |
| FR-002 | Answer oracle requests | Functional | E001 | explicit | Inspection | High |
| FR-003 | Periodically check whether extension is necessary | Functional | E001 | explicit | Inspection | High |
| FR-004 | Require `.env` properties for proper oracle-service running | Functional | E001 | explicit | Inspection | High |
| FR-005 | Provide wallet-backed prediction API through React context | Functional | E003 | explicit | Demonstration | High |
| FR-006 | Submit prediction creation through `create_prediction` using event and image inputs | Functional | E004 | explicit | Inspection | High |
| FR-007 | Use wallet client for prediction-card blockchain interaction | Functional | E003, E004 | explicit | Inspection | High |
| FR-008 | Allow CORS methods `GET`, `POST`, `OPTIONS` | Functional | E002 | explicit | Test | High |
| FR-009 | Allow and expose configured CORS headers | Functional | E002 | explicit | Test | High |
| NFR-001 | Interoperate with Aeternity wallet and SDK components | Non-functional | E003, E004, E005, E006 | explicit | Inspection | High |
| NFR-002 | Support development and packaged oracle-service execution | Non-functional | E001 | explicit | Demonstration | High |
| NFR-003 | Externalize required oracle-service configuration via `.env` | Non-functional | E001 | explicit | Inspection | High |
| NFR-004 | Support configured browser cross-origin compatibility | Non-functional | E002 | explicit | Test | High |
| NFR-005 | Use periodic scheduled processing for oracle checks and extension checks | Non-functional | E001 | inferred from explicit periodic behavior | Inspection | Medium |
| DR-001 | Accept `PredictionEvent` for prediction creation | Data | E004 | explicit | Inspection | High |
| DR-002 | Accept `img_higher` and `img_lower` string inputs | Data | E004 | explicit | Inspection | High |
| DR-003 | Use converted event start timestamp in prediction creation | Data | E004 | explicit | Inspection | High |
| DR-004 | Reference `predictioncards.chain` AENS name | Data | E004 | explicit | Inspection | High |
| DR-005 | Consume runtime properties from `.env` | Data | E001 | explicit | Inspection | High |
| DR-006 | Support Aeternity transaction/oracle/AENS domain objects in integration tests | Data | E005, E006 | explicit | Inspection | Medium |
