# Software Requirements Specification

## 1. Introduction

### 1.1 Purpose
This SRS defines the final checked requirements for the Prediction Cards system. It is structured as a clean requirements input for downstream architecture diagram generation.

### 1.2 Product Scope
Prediction Cards is a blockchain-backed prediction market and NFT application. The system includes:
- A frontend application for wallet-connected prediction creation, prediction viewing, outcome NFT fund operations, withdrawal, and reward claiming.
- An on-chain PredictionCards smart contract deployed on the Aeternity blockchain and located through an AENS name.
- An oracle service that registers and maintains an Aeternity oracle, checks pending oracle queries, obtains price-comparison results, and submits oracle responses.
- A prediction-processing service that drives closed predictions into the outcome determination workflow and completes result processing after oracle responses are available.
- Prediction media storage for outcome NFT images or animations.
- A local contract integration-test environment with CORS/proxy support for browser-style contract testing.

### 1.3 Intended Audience
- Product owners and maintainers.
- Frontend and smart-contract developers.
- Oracle-service and prediction-processing-service developers.
- Test engineers and integration engineers.
- Architecture reviewers generating or validating system diagrams.

### 1.4 Terminology
| Term | Definition |
|---|---|
| Prediction Cards | Product and codebase name; "card" is treated as a product/UI/NFT metaphor, not as a separate multi-prediction domain entity. |
| Prediction | A market-like event with an asset, target price, prediction time range, and two possible outcome NFTs. |
| Outcome NFT | One of the prediction outcome assets, represented by result categories such as `higher` and `lower_or_equal`. |
| Prediction participant | A wallet-connected user who creates, views, funds, rents, withdraws from, or claims rewards related to predictions and outcome NFTs. |
| Oracle service | The service responsible for maintaining the Aeternity oracle and submitting result responses for oracle queries. |
| Prediction-processing service | The service responsible for initiating oracle queries for closed predictions and driving on-chain result processing after oracle responses are available. |
| AENS name | The Aeternity naming mechanism used to locate the deployed contract. |

## 2. Overall Description

### 2.1 Product Perspective
The system is a multi-component decentralized application. The frontend application interacts with an on-chain contract through a connected Aeternity wallet. The on-chain contract maintains prediction and outcome state. The prediction-processing service and oracle service cooperate to determine prediction outcomes after predictions close. Prediction media is stored outside the contract and referenced by the frontend and contract workflow.

The system consists of:
- User frontend.
- On-chain PredictionCards smart contract.
- Aeternity wallet and SDK integration.
- Oracle service.
- Prediction-processing service.
- External price provider.
- Prediction media storage.
- Local contract integration-test stack.

### 2.2 System Architecture and Data Flow
The user frontend is responsible for prediction creation, prediction viewing, and fund/reward operations. The on-chain contract is responsible for maintaining prediction and outcome NFT state. The prediction-processing service is responsible for driving closed predictions into the outcome determination workflow. The oracle service is responsible for providing the external price-comparison response required for outcome determination.

The main lifecycle is:
1. A prediction participant connects a wallet through the frontend.
2. The prediction participant creates a prediction by submitting asset, target price, time range, and outcome NFT media information.
3. The frontend submits the prediction creation request to the on-chain contract through the connected wallet.
4. Prediction participants view prediction state and perform outcome NFT fund operations through frontend-to-contract interactions.
5. After a prediction reaches the closed state, the prediction-processing service initiates the oracle query required for outcome determination.
6. The oracle service checks pending oracle queries, obtains the relevant external price information, compares actual price with target price, and submits the result response.
7. After the oracle response is available, the prediction-processing service drives on-chain result processing.
8. The on-chain contract determines the winning outcome and opens the reward-claiming path according to the processed result.

### 2.3 Product Functions
- Provide a wallet-backed frontend API to child frontend components.
- Create predictions through the on-chain contract.
- Convert prediction time inputs before contract submission.
- Store and display prediction and outcome NFT media references.
- Allow prediction participants to view ongoing and processed predictions.
- Support fund, rent, withdrawal, and reward-claiming operations for prediction outcome NFTs.
- Periodically check pending oracle queries.
- Answer oracle queries with price-comparison results.
- Maintain oracle registration validity.
- Process closed predictions through oracle query and result-processing workflows.
- Support local contract integration testing with configured CORS behavior.

### 2.4 User Classes
| User Class | Description |
|---|---|
| Prediction participant | A user who uses a connected wallet through the frontend application to create predictions, view predictions, provide or rent funds for prediction outcome NFTs, withdraw funds, and claim rewards after the prediction outcome is determined. |
| Service operator | A maintainer responsible for configuring and running the oracle service and prediction-processing service. |
| Integration/test operator | A developer or tester responsible for validating contract, oracle, wallet, and local integration-test behavior. |

### 2.5 User Scenarios
- A prediction participant selects an asset, target price, prediction time range, and outcome NFT media to create a prediction.
- A prediction participant views ongoing and processed predictions.
- A prediction participant provides funds for, rents, withdraws from, or claims rewards for prediction outcome NFTs.
- A service operator configures and runs oracle-related services so prediction outcome determination can proceed.
- An integration/test operator validates local contract interactions and browser-style CORS behavior in the contract-test environment.

### 2.6 Operating Environment
- Browser frontend using React and Aeternity wallet integration.
- Aeternity blockchain runtime for the on-chain PredictionCards contract.
- AENS contract-location mechanism for resolving the deployed contract.
- Quarkus-based oracle service.
- Prediction-processing service for scheduled closed-prediction handling.
- External price provider used by oracle outcome determination.
- Prediction media storage, such as IPFS-compatible storage.
- Local contract integration-test environment with Aeternity node, compiler, index, debug endpoint, and test proxy/CORS configuration.

### 2.7 Assumptions and Dependencies
- Prediction participants have access to a compatible wallet.
- On-chain contract interaction depends on the Aeternity SDK and wallet client.
- The deployed contract is reachable through its AENS name.
- The oracle service has complete runtime configuration before startup.
- The prediction-processing service can discover closed predictions and invoke on-chain outcome processing.
- The external price provider is available when oracle responses are required.
- Prediction media is available from media storage when prediction details are displayed.

## 3. External Interface Requirements

### 3.1 User Interfaces
| Interface | Requirement |
|---|---|
| Wallet-connected frontend | The frontend shall allow a prediction participant to use a connected wallet for prediction and outcome NFT operations. |
| Prediction creation interface | The frontend shall allow a prediction participant to provide asset, target price, time range, and outcome NFT media inputs for prediction creation. |
| Prediction viewing interface | The frontend shall allow a prediction participant to view ongoing and processed predictions. |
| Outcome NFT operation interface | The frontend shall allow a prediction participant to perform supported fund, rent, withdrawal, and reward-claiming operations. |

### 3.2 Software/API Interfaces
| Interface | Requirement |
|---|---|
| Frontend wallet interface | The frontend prediction API shall use a connected wallet as its contract interaction dependency. |
| Frontend context interface | The frontend shall provide prediction operation capabilities to child components through a provider/context mechanism. |
| Frontend-contract interface | The frontend shall submit prediction creation, read prediction state, and perform fund/reward operations through the on-chain contract. |
| AENS contract-location interface | The frontend and services shall locate the deployed on-chain contract through the configured AENS name. |
| Prediction-processing-service contract interface | The prediction-processing service shall initiate oracle queries for closed predictions and complete result processing after oracle responses are available. |
| Oracle-service Aeternity oracle interface | The oracle service shall maintain the Aeternity oracle and submit result responses for pending oracle queries. |
| Oracle-service price-provider interface | The oracle service shall obtain external price information needed for price-comparison outcome determination. |
| Frontend media-storage interface | The frontend shall load or reference prediction outcome NFT media from prediction media storage. |
| Local test proxy interface | The local contract integration-test environment shall expose the configured test services with browser-compatible CORS behavior. |

### 3.3 Communication Interfaces
| Interface | Requirement |
|---|---|
| Wallet-mediated blockchain calls | Frontend contract operations shall be submitted through wallet-mediated Aeternity interactions. |
| Scheduled service processing | Oracle and prediction-processing service behavior shall run periodically according to runtime configuration. |
| Oracle query/response communication | The oracle service shall read pending oracle queries and submit result responses in the expected oracle response format. |
| Media retrieval | Prediction media references shall be retrievable by the frontend from media storage. |
| Local CORS communication | The local integration-test proxy shall allow configured browser cross-origin methods and headers for test flows. |

### 3.4 Data Exchange Formats
| Data Format | Requirement |
|---|---|
| Prediction creation input | Prediction creation input shall include asset identifier, target price, prediction start time, prediction end time, and outcome NFT media values. |
| Contract prediction call | The frontend shall submit converted time values and outcome media values when creating a prediction through the contract. |
| Oracle query data | Oracle query data shall include asset identifier, target price, and end time. |
| Oracle response data | Oracle response data shall use an explicit result enumeration for the price-comparison result, including `higher` and `lower_or_equal`. |
| Outcome determination data | Prediction outcome determination data shall include asset identifier, target price, end time, actual/result value, and resulting winning outcome. |
| Runtime configuration | Oracle-service configuration shall cover keys, blockchain node connection, compiler-service connection, network environment, scheduling periods, oracle fees, and oracle validity-management parameters. |

## 4. Functional Requirements

| ID | Requirement | Trigger/Input | System Behavior | Output | Priority | Verification |
|---|---|---|---|---|---|---|
| FR-001 | Pending oracle query checking | Periodic oracle-service execution. | The system shall periodically check pending oracle queries generated by the on-chain prediction workflow. | Pending oracle queries are detected for processing. | High | Inspection |
| FR-002 | Oracle result response | Pending oracle query containing asset, target price, and end time. | The system shall obtain relevant price data, compare the target price with the actual price, and submit a result response conforming to the defined response enumeration. | Oracle response containing the price-comparison result. | High | Test |
| FR-003 | Oracle registration and validity maintenance | Oracle-service startup or periodic validity check. | The system shall check oracle registration status when the oracle service starts and during periodic execution. When the oracle is not registered, the system shall register the oracle. When the remaining validity period is below the configured threshold, the system shall extend oracle validity. | Registered or extended oracle validity state. | High | Inspection |
| FR-004 | Oracle-service runtime configuration | Oracle service is started. | The system shall require complete runtime configuration before the oracle service starts. | Oracle service has the configuration required for node/compiler connectivity, scheduling, fees, keys, and validity management. | High | Inspection |
| FR-005 | Frontend API provisioning | Frontend provider mechanism is rendered with a wallet context. | The system shall create wallet-backed prediction operation capabilities and provide them to child frontend components through context. | Child components can obtain a prediction operation entry point that supports prediction-creation-related operations. | High | Demonstration |
| FR-006 | Prediction creation submission | Prediction participant submits prediction creation inputs. | The system shall convert prediction time inputs to the required millisecond-level timestamp format, obtain a wallet-backed contract interaction instance, and invoke prediction creation on the on-chain contract with event and outcome media inputs. | Prediction creation transaction or contract call is submitted. | High | Inspection |
| FR-007 | Wallet-backed contract interaction | Frontend prediction operation is executed. | The system shall use the connected wallet as the dependency for blockchain contract interactions. | Blockchain interactions are performed through the wallet-backed frontend API. | High | Inspection |
| FR-008 | Local integration-test CORS method support | Browser-style request is made in the local contract integration-test environment. | The local test proxy shall allow `GET`, `POST`, and `OPTIONS` methods for cross-origin test access. | Requests using configured methods pass local test CORS validation. | Medium | Test |
| FR-009 | Local integration-test CORS header support | Browser-style request with configured headers is made in the local contract integration-test environment. | The local test proxy shall allow and expose configured headers including `Content-Type`, `Cache-Control`, `Content-Range`, and `Range`. | Browser clients can send and read configured headers in local test flows. | Medium | Test |
| FR-010 | Prediction outcome determination | A prediction reaches the closed state. | The system shall start the prediction outcome determination workflow. The prediction-processing service shall initiate the oracle query required for outcome determination, the oracle service shall submit a result response based on an external price provider, and the on-chain contract shall determine the winning outcome and open reward claiming based on that response. | Winning outcome is determined and reward claiming becomes available according to contract rules. | High | Test |
| FR-011 | Prediction participant operations | Prediction participant uses the wallet-connected frontend. | The system shall support prediction viewing, outcome NFT fund/rent operations, fund withdrawal, and reward claiming after the prediction outcome is determined. | Updated prediction, outcome NFT, fund, rental, withdrawal, or reward state. | High | Demonstration |
| FR-012 | Prediction media access | Prediction details or outcome NFT views are displayed. | The system shall reference and load prediction outcome NFT media from prediction media storage. | Outcome NFT media is available to the frontend display workflow. | Medium | Demonstration |

## 5. Non-Functional Requirements

| ID | Quality Attribute | Requirement | Priority | Verification |
|---|---|---|---|---|
| NFR-001 | Interoperability | The frontend integration shall operate with an Aeternity wallet client and Aeternity SDK-based contract interaction components. | High | Inspection |
| NFR-002 | Portability | The oracle service shall support both development-mode execution and packaged execution. | Medium | Demonstration |
| NFR-003 | Configurability | The oracle service shall externalize required runtime properties through mandatory runtime configuration. | High | Inspection |
| NFR-004 | Local test web compatibility | The local contract integration-test environment shall support browser cross-origin access with configured methods and headers. | Medium | Test |
| NFR-005 | Scheduled processing availability | The oracle service and prediction-processing service shall perform periodic processing rather than relying only on manual invocation. | High | Inspection |
| NFR-006 | Oracle availability | The system shall maintain oracle availability before oracle registration expires by checking validity and extending it when configured thresholds are reached. | High | Test |
| NFR-007 | Time interpretation correctness | The system shall define and verify the timezone interpretation rule for frontend local-time input to avoid prediction time shifts across runtime environments. | Medium | Analysis |

## 6. Data Requirements

### 6.1 Data Entities
| ID | Data Entity | Requirement |
|---|---|---|
| DR-001 | Prediction | The system shall represent predictions with asset identifier, target price, start time, end time, outcome media, lifecycle state, and outcome information. |
| DR-002 | Prediction outcome NFT | Each prediction shall have outcome NFT data for the supported result categories, including `higher` and `lower_or_equal`. |
| DR-003 | Prediction event input | The system shall accept prediction event input for prediction creation through the frontend. |
| DR-004 | Prediction media | The system shall handle outcome NFT media references through prediction media storage. |
| DR-005 | Rental and fund data | The system shall represent deposit, rent, renter, withdrawal, and reward-claiming data required for outcome NFT operations. |
| DR-006 | Oracle query | Oracle query data shall include asset identifier, target price, and end time. |
| DR-007 | Oracle response | Oracle response data shall use an explicit result enumeration for the price-comparison result. |
| DR-008 | Prediction outcome determination data | Prediction outcome determination data shall include asset identifier, target price, end time, and result value. |
| DR-009 | Event timestamp | The prediction start time and end time submitted by the system to the on-chain contract shall use a unified millisecond-level timestamp format. |
| DR-010 | AENS contract name | The system shall maintain the AENS name used to locate the deployed on-chain contract. |
| DR-011 | Oracle-service runtime configuration | Oracle-service configuration shall cover keys, blockchain node connection, compiler-service connection, network environment, scheduling periods, oracle fees, and oracle validity-management parameters. |
| DR-012 | Blockchain transaction and oracle objects | The contract integration environment shall support Aeternity transaction, oracle, and AENS-related domain objects required by local tests and integration workflows. |

### 6.2 Input and Output Data
| Data Flow | Requirement |
|---|---|
| Prediction creation input | Asset, target price, start time, end time, and outcome media values shall be accepted from the frontend prediction creation workflow. |
| Prediction creation output | Prediction creation shall produce an on-chain transaction or contract-call result. |
| Oracle query input | The oracle service shall receive query data containing asset, target price, and end time. |
| Oracle response output | The oracle service shall output a result enumeration indicating whether the actual price is higher than or lower/equal to the target price. |
| Outcome processing output | The on-chain contract shall expose updated prediction outcome and reward-claiming state after result processing completes. |
| Media retrieval output | Prediction media storage shall provide outcome NFT media to the frontend display workflow. |

### 6.3 Storage, Integrity, Privacy, Retention, and Migration
| Topic | Requirement |
|---|---|
| On-chain state | Prediction and outcome state shall be maintained by the on-chain contract. |
| Runtime configuration integrity | Oracle-service runtime configuration shall be complete and consistent before service execution. |
| Media storage | Outcome NFT media shall be stored or referenced in prediction media storage outside the on-chain contract. |
| Test proxy configuration | CORS/proxy configuration shall be limited to the local contract integration-test environment unless a production deployment specification establishes otherwise. |
| Privacy, retention, and migration | Privacy, retention, deletion, and migration behavior are not specified and should be defined before production operation if needed. |

## 7. System Constraints

| ID | Constraint |
|---|---|
| C-001 | The oracle service is constrained to a Quarkus-based implementation and runtime model. |
| C-002 | The on-chain prediction logic is constrained by the Aeternity blockchain, the Sophia smart-contract runtime, the AENS contract-location mechanism, and the responsibility split between the oracle service and prediction-processing service. |
| C-003 | Frontend contract interaction is constrained to Aeternity wallet and SDK components. |
| C-004 | Oracle-service operation is constrained by complete runtime configuration before startup. |
| C-005 | Oracle registration, validity thresholds, validity-extension strategy, scheduling periods, oracle fees, node connection, compiler-service connection, network environment, and key configuration are constrained by runtime configuration. |
| C-006 | The local CORS/proxy configuration shall not be treated as a production nginx or production reverse-proxy requirement without additional deployment specification. |
| C-007 | The term "card" shall not be modeled as an independent data entity or multi-prediction container unless a future domain model explicitly defines such an entity. |
| C-008 | Frontend local-time input shall have an explicit timezone interpretation rule before production use. |

## 8. Verification and Acceptance Criteria

| Requirement ID | Verification Method | Acceptance Criteria |
|---|---|---|
| FR-001 | Inspection | Oracle-service scheduled behavior checks pending oracle queries generated by the on-chain prediction workflow. |
| FR-002 | Test | Given oracle query data with asset, target price, and end time, the oracle service obtains price data, compares values, and submits a valid result response. |
| FR-003 | Inspection | Oracle-service startup and periodic execution check registration status and perform registration or validity extension when required. |
| FR-004 | Inspection | Oracle-service runtime configuration covers keys, node/compiler connection, network, scheduling, oracle fees, and validity-management parameters before startup. |
| FR-005 | Demonstration | In a test wallet context, child frontend components can obtain prediction operation capabilities from the frontend provider/context mechanism. |
| FR-006 | Inspection | Prediction creation converts time inputs to the required millisecond-level timestamp format before submitting event and outcome media inputs to the on-chain contract. |
| FR-007 | Inspection | Frontend contract interactions are performed through the connected wallet dependency. |
| FR-008 | Test | Local contract integration-test requests using `GET`, `POST`, and `OPTIONS` pass the configured CORS method policy. |
| FR-009 | Test | Local contract integration-test requests can use and read configured CORS headers including `Content-Type`, `Cache-Control`, `Content-Range`, and `Range`. |
| FR-010 | Test | When a prediction is closed, the prediction-processing service initiates outcome determination, the oracle service submits the result response, and the contract exposes the determined winning outcome and reward-claiming path. |
| FR-011 | Demonstration | A wallet-connected prediction participant can view predictions and perform supported outcome NFT fund, rent, withdrawal, and reward-claiming operations. |
| FR-012 | Demonstration | Prediction outcome NFT media references load through the frontend display workflow. |
| NFR-001 | Inspection | Frontend integration points consistently use Aeternity wallet and SDK components. |
| NFR-002 | Demonstration | The oracle service can be run in development mode and packaged mode. |
| NFR-003 | Inspection | Required oracle-service runtime properties are externalized through configuration. |
| NFR-004 | Test | Local contract integration-test CORS behavior matches configured methods and headers. |
| NFR-005 | Inspection | Oracle and prediction-processing service workflows are configured for periodic execution. |
| NFR-006 | Test | Oracle validity is checked and extended before expiry when configured thresholds are reached. |
| NFR-007 | Analysis | The timezone interpretation of frontend local-time input is explicitly documented and verified before release. |
