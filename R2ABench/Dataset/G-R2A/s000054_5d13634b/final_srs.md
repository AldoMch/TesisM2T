# Software Requirements Specification

## 1. Introduction

### Purpose
This SRS defines evidence-backed requirements for the `tokencard/contracts` repository at commit `bc0f072277770488e2c428c255785b186bd73589`. The scope is limited to behaviors and interfaces directly supported by the provided repository evidence.

### Product scope
The repository provides smart-contract-facing components for a TokenCard system centered on a `Consumer Contract Wallet`, associated controller and whitelist contracts, and contract bindings that support read-only calls and paid transactions on Ethereum.

### Intended audience
This document is for maintainers, integrators, testers, auditors, and other stakeholders who need a concise, traceable statement of repository-supported requirements.

### References
- Repository: `tokencard/contracts`
- Repository URL: https://github.com/tokencard/contracts
- Snapshot: `bc0f072277770488e2c428c255785b186bd73589`
- Primary evidence sources: `README.md`, `pkg/bindings/internals/controller.go`, `pkg/bindings/mocks/oraclize-connector.go`

## 2. Overall Description

### Product perspective
The product is an Ethereum-based contract system. A `Consumer Contract Wallet` interacts with the Ethereum network and resolves supporting contract locations through ENS, including an exchange-rate oracle, a controller contract, and a token whitelist contract. Generated bindings expose contract methods as read-only calls and paid transactions. Source: `E001`, `E003`, `E004`.

### Product functions summary
- Hold user ETH and ERC20 assets in a `Consumer Contract Wallet`. Source: `E002`.
- Use exchange-rate data to secure user tokens. Source: `E001`.
- Resolve oracle, controller, and token whitelist contract locations via ENS. Source: `E001`.
- Enforce a token whitelist that includes exchange-rate information and determines which tokens can be used to load TokenCard. Source: `E001`.
- Expose read-only controller counts and paid transaction methods through bindings. Source: `E003`, `E005`, `E006`.

### User classes
- `Owner`: the externally owned address that owns the user’s smart contracts. Source: `E002`.
- Token Group Ltd operated service addresses: addresses used to provide services to the end user. Source: `E002`.
- Integrators/developers using Go bindings to call or transact with contracts. Source: `E003`, `E004`.

### Operating environment
- Ethereum network. Source: `E001`.
- Ethereum Name Service (ENS) for contract location resolution. Source: `E001`.
- Go-based contract bindings exposing `Call`, `Transact`, and `Transfer` methods. Source: `E003`, `E004`.

### Assumptions and dependencies
- The wallet depends on ENS to resolve oracle, controller, and token whitelist addresses. Source: `E001`.
- Exchange-rate information from the oracle and token whitelist is required for token security decisions. Source: `E001`.
- Gas-payment ETH is held outside the wallet contract and is not covered by wallet security features. Source: `E002`.

## 3. External Interface Requirements

### User interfaces
No end-user UI is evidenced in the provided material.

### Software/API interfaces
| Interface | Requirement summary | Source |
|---|---|---|
| Ethereum network | The wallet and contract bindings shall interact with Ethereum for contract calls and transactions. | `E001`, `E003`, `E004` |
| ENS | The wallet shall resolve oracle, controller, and token whitelist locations through ENS. | `E001` |
| Oracle contract | The wallet shall obtain exchange-rate data needed to secure user tokens. | `E001` |
| Controller contract | The system shall expose controller interactions including paid transactions and read-only count retrieval. | `E003`, `E005`, `E006` |
| Token whitelist contract | The system shall use whitelist and exchange-rate data to determine eligible tokens. | `E001` |

### Communication interfaces
| Interface | Description | Source |
|---|---|---|
| Contract call | Read-only invocation returning output values without a paid transaction. | `E003`, `E004`, `E005`, `E006` |
| Contract transact | Paid invocation with method name and input parameters. | `E003`, `E004` |
| Transfer | Plain transaction to a contract default method when available. | `E003`, `E004` |

### Data exchange formats
| Data | Format evidenced | Source |
|---|---|---|
| Contract addresses | Ethereum addresses resolved through ENS | `E001`, `E002` |
| Token holdings | ETH and ERC20 token assets | `E002` |
| Exchange rates | Oracle and whitelist-provided rate data | `E001` |
| Count values | `uint256` for `adminCount` and `controllerCount` | `E005`, `E006` |
| Contract method input | Method name plus variadic parameters | `E003`, `E004` |

## 4. Functional Requirements

| ID | Description | Trigger / Input | System behavior | Output | Priority | Verification | Source evidence |
|---|---|---|---|---|---|---|---|
| FR-001 | Obtain exchange-rate data for token security | A wallet operation requires exchange-rate information to secure a user’s tokens | The system shall interact with an exchange-rate oracle on Ethereum to obtain the exchange rates needed to secure the user’s tokens | Exchange-rate data available to the wallet security logic | High | Test | `E001` |
| FR-002 | Resolve supporting contract locations through ENS | A wallet operation requires the oracle, controller, or token whitelist contract | The system shall use ENS to resolve the location of the oracle, controller, and token whitelist contracts before interacting with them | Resolved contract addresses | High | Test | `E001` |
| FR-003 | Enforce token whitelist eligibility | A token is evaluated for wallet security or TokenCard loading | The system shall use the token whitelist as the source of allowed tokens and associated exchange rates, and shall determine whether a token can be used to load TokenCard | Eligibility decision and associated rate data | High | Test | `E001` |
| FR-004 | Hold user ETH and ERC20 assets in the wallet | User assets are placed under wallet custody | The system shall maintain the user’s ETH and ERC20 token assets within the `Consumer Contract Wallet` | Wallet-held ETH and ERC20 balances | High | Inspection | `E002` |
| FR-005 | Segregate gas-payment ETH from protected wallet assets | ETH is allocated for gas payment | The system shall represent gas-payment ETH as a `Gas Tank` outside the smart contract wallet rather than as a protected wallet asset | Gas-payment ETH treated separately from protected wallet holdings | High | Inspection | `E002` |
| FR-006 | Support controller paid transactions | An integrator submits a controller transaction or transfer request | The system shall provide controller interfaces that support `Transact` with a method name and parameters, and `Transfer` to the contract default method when available | Transaction object or transfer result | Medium | Demonstration | `E003` |
| FR-007 | Expose read-only `adminCount` retrieval | A caller requests the controller admin count | The system shall provide a free data retrieval call for `adminCount` returning a `uint256` value | `adminCount` value | Medium | Test | `E005` |
| FR-008 | Expose read-only `controllerCount` retrieval | A caller requests the controller count | The system shall provide a free data retrieval call for `controllerCount` returning a `uint256` value | `controllerCount` value | Medium | Test | `E006` |
| FR-009 | Support generic read-only and paid contract interaction patterns | An integrator invokes a contract binding method | The system shall expose `Call` for constant methods and `Transact`/`Transfer` for paid interactions on supported contract bindings | Returned call data or transaction result | Medium | Demonstration | `E003`, `E004` |

## 5. Non-Functional Requirements

| ID | Quality attribute | Requirement | Priority | Verification | Source evidence |
|---|---|---|---|---|---|
| NFR-001 | Compatibility | The system shall operate against the Ethereum network and use ENS for contract resolution. | High | Inspection | `E001` |
| NFR-002 | Security boundary | The system shall distinguish protected wallet assets from gas-payment ETH by keeping the `Gas Tank` outside the wallet security protections. | High | Inspection | `E002` |
| NFR-003 | Interface consistency | Supported contract bindings shall provide separate read-only call paths and paid transaction paths. | Medium | Inspection | `E003`, `E004`, `E005`, `E006` |

## 6. Data Requirements

### Data entities or objects
| Entity / Object | Description | Source |
|---|---|---|
| Consumer Contract Wallet | Contract wallet holding user ETH and ERC20 assets | `E001`, `E002` |
| Owner | Externally owned address that owns the user’s smart contracts | `E002` |
| Gas Tank | ETH used to pay gas, represented outside the smart contract wallet | `E002` |
| Oracle | Contract providing exchange rates used to secure user tokens | `E001` |
| Controller | Contract resolved through ENS and exposed through bindings | `E001`, `E003`, `E005`, `E006` |
| Token whitelist | Whitelist of tokens and exchange rates used for security and load eligibility | `E001` |
| Admin count | `uint256` count returned by the controller | `E005` |
| Controller count | `uint256` count returned by the controller | `E006` |

### Input/output data
| Data flow | Input | Output | Source |
|---|---|---|---|
| ENS resolution | Contract role identifier implied by wallet interaction | Resolved contract address | `E001` |
| Oracle lookup | Request for exchange-rate data | Exchange-rate values used for token security | `E001` |
| Token eligibility check | Token identity | Whitelist decision and associated exchange-rate data | `E001` |
| Controller count retrieval | Read-only call request | `uint256` count value | `E005`, `E006` |
| Contract transaction | Method name and parameters | Transaction result | `E003`, `E004` |

### Storage, integrity, privacy, retention, migration
| Topic | Requirement | Source |
|---|---|---|
| Asset segregation | Protected wallet assets and gas-payment ETH shall remain logically distinct because the gas ETH is outside wallet security protections. | `E002` |
| Data integrity | Token-related security decisions shall depend on whitelist and exchange-rate data. | `E001` |

## 7. Constraints

| ID | Constraint | Source |
|---|---|---|
| C-001 | The product is constrained to the Ethereum network. | `E001` |
| C-002 | Supporting contract locations are resolved through ENS. | `E001` |
| C-003 | Token loading eligibility is constrained by the token whitelist. | `E001` |
| C-004 | Gas-payment ETH resides outside the wallet contract and is not protected by wallet security features. | `E002` |
| C-005 | The owner role is an externally owned address. | `E002` |

## 8. Verification and Acceptance

| Requirement ID | Verification method | Acceptance basis |
|---|---|---|
| FR-001 | Test | Demonstrate that a wallet security-related operation retrieves oracle exchange-rate data. |
| FR-002 | Test | Demonstrate resolution of oracle, controller, and token whitelist through ENS before use. |
| FR-003 | Test | Demonstrate that whitelist data governs token eligibility and associated rates. |
| FR-004 | Inspection | Confirm repository evidence states wallet custody of ETH and ERC20 assets. |
| FR-005 | Inspection | Confirm repository evidence states gas ETH is outside the wallet and not protected. |
| FR-006 | Demonstration | Demonstrate binding support for `Transact` and `Transfer` on the controller interface. |
| FR-007 | Test | Demonstrate a read-only `adminCount` call returning a `uint256`. |
| FR-008 | Test | Demonstrate a read-only `controllerCount` call returning a `uint256`. |
| FR-009 | Demonstration | Demonstrate `Call` for constant methods and `Transact`/`Transfer` for paid interactions on supported bindings. |
| NFR-001 | Inspection | Confirm Ethereum and ENS are the evidenced runtime dependencies. |
| NFR-002 | Inspection | Confirm the documented separation between protected wallet assets and gas ETH. |
| NFR-003 | Inspection | Confirm bindings separate read-only and paid interaction paths. |

## 9. Traceability Matrix

| ID | Requirement | Type | Source | Evidence Type | Verification | Confidence |
|---|---|---|---|---|---|---|
| FR-001 | Obtain exchange-rate data for token security | Functional | `E001` | explicit | Test | High |
| FR-002 | Resolve supporting contract locations through ENS | Functional | `E001` | explicit | Test | High |
| FR-003 | Enforce token whitelist eligibility | Functional | `E001` | explicit | Test | Medium |
| FR-004 | Hold user ETH and ERC20 assets in the wallet | Functional | `E002` | explicit | Inspection | Medium |
| FR-005 | Segregate gas-payment ETH from protected wallet assets | Functional | `E002` | explicit | Inspection | High |
| FR-006 | Support controller paid transactions | Functional | `E003` | explicit | Demonstration | High |
| FR-007 | Expose read-only `adminCount` retrieval | Functional | `E005` | explicit | Test | High |
| FR-008 | Expose read-only `controllerCount` retrieval | Functional | `E006` | explicit | Test | High |
| FR-009 | Support generic read-only and paid contract interaction patterns | Functional | `E003`, `E004` | explicit | Demonstration | High |
| NFR-001 | Operate against Ethereum and use ENS | Non-functional | `E001` | explicit | Inspection | High |
| NFR-002 | Preserve the documented security boundary around gas ETH | Non-functional | `E002` | explicit | Inspection | High |
| NFR-003 | Maintain separate read-only and paid contract interaction paths | Non-functional | `E003`, `E004`, `E005`, `E006` | explicit | Inspection | High |
