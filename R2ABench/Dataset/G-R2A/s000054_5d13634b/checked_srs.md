# Software Requirements Specification

## 1. Introduction

### Purpose
This SRS defines the software requirements for the `tokencard/contracts` product. It captures the externally relevant behavior and interfaces supported by the reviewed repository materials and is intended as a normalized input for downstream architecture and design activities.

### Product scope
The product is an Ethereum-based smart-contract system centered on a Consumer Contract Wallet and related contract integrations. It includes wallet-related contract behavior, ENS-based contract resolution, token whitelist and exchange-rate usage, and generated Go bindings for contract interaction.

Scope limitation: this SRS is derived mainly from README content, architecture material, and selected Go binding artifacts. It does not fully cover all state-changing Solidity-contract behavior, including controller management, token whitelist management, oracle exchange-rate update flows, wallet whitelist and limit configuration, Gas Tank top-up, and complete TokenCard load workflows. Additional source-level review is required before treating this document as a complete specification of all repository behavior.

### Intended audience
This document is intended for:
- Architects and designers generating system and component views
- Maintainers of the smart-contract and binding layers
- Integrators using contract bindings and Ethereum/ENS interactions
- Test engineers validating supported behaviors

### References
- Repository: `tokencard/contracts`
- Architecture artifact: `docs/high_level_architecture.svg`

## 2. Overall Description

### Product perspective
The system centers on a Consumer Contract Wallet on Ethereum. The Owner Address controls the wallet. The wallet resolves supporting contracts through ENS, including controller, token whitelist, and licence/oracle-related components. The token whitelist and oracle-related components provide token support status and exchange-rate information used by wallet operations. Controller addresses participate in control and confirmation operations. The Gas Tank represents gas-payment ETH on the Owner Address and remains outside the wallet contract.

Generated Go bindings provide contract interaction patterns for read-only calls and paid transactions.

### Product functions summary
The product supports the following functions:
- Hold user ETH and ERC20 assets in the Consumer Contract Wallet.
- Resolve supporting contract locations through ENS.
- Obtain and use exchange-rate data for wallet-related token operations.
- Use the token whitelist to record token exchange rates, whether tokens may be used for TokenCard loading, and whether tokens may be burned by the TKN Holder Contract.
- Support controller-related contract interaction through generated bindings.
- Expose read-only retrieval of controller `adminCount` and `controllerCount`.
- Expose generic contract interaction patterns for read-only calls, paid transactions, and transfers.
- Keep gas-payment ETH separate from protected wallet assets.

### User classes
- `Owner`: the user's Owner Address / externally owned address, which owns that user's smart contracts.
- `Controller`: a set of addresses owned and operated to provide services to end users and participate in control or confirmation operations.
- `Integrator/Developer`: a user of the generated Go bindings for contract calls and transactions.

### Operating environment
- Ethereum network
- Ethereum Name Service (ENS)
- Solidity smart contracts
- Go-based generated contract bindings

### Assumptions and dependencies
- ENS is available for resolution of supporting contract addresses.
- Wallet-related token decisions depend on token whitelist and exchange-rate information.
- Gas-payment ETH is maintained outside the Consumer Contract Wallet.
- Some repository behaviors depend on additional contracts and flows not fully specified in this document.

## 3. External Interface Requirements

### User interfaces
No end-user graphical interface is specified in this SRS.

### Software/API interfaces
| Interface | Requirement summary |
|---|---|
| Ethereum network | The system shall interact with Ethereum for contract calls and transactions. |
| ENS | The system shall resolve supporting contract addresses through ENS before interacting with those contracts. |
| Oracle or rate-provider interface | The system shall obtain exchange-rate data required for wallet-related token operations. |
| Controller contract interface | The system shall expose controller interactions through generated bindings, including read-only calls and paid transactions. |
| Token whitelist interface | The system shall use token whitelist data for token support, exchange-rate, loadability, and burnability decisions. |

### Communication interfaces
| Interface | Description |
|---|---|
| Contract call | Read-only invocation that returns output values without creating a paid transaction. |
| Contract transact | Paid invocation using a method name and input parameters. |
| Transfer | Paid transfer to a contract default method when supported. |

### Data exchange formats
| Data item | Requirement summary |
|---|---|
| Contract addresses | Supporting contract addresses shall be represented as Ethereum addresses resolved through ENS. |
| Asset holdings | Wallet-managed assets shall include ETH and ERC20 tokens. |
| Exchange-rate data | Exchange-rate data shall be consumable by wallet-related token operations. |
| Controller counts | `adminCount` and `controllerCount` values shall be represented as `uint256`. |
| Contract invocation input | Paid contract interaction shall accept a method name and parameters. |

## 4. Functional Requirements

| ID | Description | Trigger/Input | System behavior | Output | Priority | Verification |
|---|---|---|---|---|---|---|
| FR-001 | Obtain exchange-rate data for wallet token operations | A wallet operation requires token or value conversion data | The system shall obtain exchange-rate data required for wallet-related token operations and conversions. | Exchange-rate data is made available to the invoking operation. | High | Test |
| FR-002 | Resolve supporting contract locations through ENS | A wallet or contract operation requires a dependent contract address | The system shall resolve supporting contract locations through ENS before interacting with controller, token whitelist, oracle/licence, or related contracts. | Resolved contract addresses | High | Test |
| FR-003 | Apply token whitelist rules | A token is evaluated for wallet or TokenCard-related use | The system shall use the token whitelist to record token exchange rates, whether tokens may be used for TokenCard loading, and whether tokens may be burned by the TKN Holder Contract, and shall use this information to support wallet security and load-eligibility decisions. | Token eligibility, rate, and related support status are available to the invoking operation. | High | Test |
| FR-004 | Hold user ETH and ERC20 assets in the wallet | User assets are deposited or maintained under wallet custody | The system shall maintain user ETH and ERC20 assets within the Consumer Contract Wallet. | Wallet-held ETH and ERC20 balances | High | Inspection |
| FR-005 | Segregate gas-payment ETH from protected wallet assets | ETH is allocated for gas payment | The system shall maintain gas-payment ETH as the Gas Tank on the user's Owner Address, outside the Consumer Contract Wallet and outside wallet security protections. | Gas-payment ETH remains logically and operationally separate from protected wallet assets. | High | Inspection |
| FR-006 | Support controller paid transactions | An integrator submits a controller transaction or transfer request | The system shall provide controller binding interfaces that support `Transact` with a method name and parameters, and `Transfer` when supported. | Transaction or transfer result | Medium | Demonstration |
| FR-007 | Expose read-only `adminCount` retrieval | A caller requests the controller admin count | The system shall provide a read-only call for `adminCount` that returns a `uint256` value. | `adminCount` value | Medium | Test |
| FR-008 | Expose read-only `controllerCount` retrieval | A caller requests the controller count | The system shall provide a read-only call for `controllerCount` that returns a `uint256` value. | `controllerCount` value | Medium | Test |
| FR-009 | Support generic read-only and paid contract interaction patterns | An integrator invokes a supported contract binding | The system shall expose `Call` for read-only methods and `Transact` or `Transfer` for paid interactions on supported contract bindings. | Returned call data or transaction result | Medium | Demonstration |

## 5. Non-Functional Requirements

| ID | Quality attribute | Requirement | Priority | Verification |
|---|---|---|---|---|
| NFR-001 | Compatibility | The system shall operate with the Ethereum network and ENS-based contract resolution. | High | Inspection |
| NFR-002 | Security boundary | The system shall keep gas-payment ETH outside the Consumer Contract Wallet and outside wallet security protections. | High | Inspection |
| NFR-003 | Interface consistency | Supported generated contract bindings shall provide distinct read-only call paths and paid transaction paths. | Medium | Inspection |

## 6. Data Requirements

| ID | Data item/entity | Requirement |
|---|---|---|
| DR-001 | Consumer Contract Wallet | The system shall define a Consumer Contract Wallet that holds user ETH and ERC20 assets. |
| DR-002 | Owner | The system shall represent the Owner as the user's externally owned address that owns that user's smart contracts. |
| DR-003 | Controller | The system shall represent Controller as a set of addresses used for service and control or confirmation operations. |
| DR-004 | Gas Tank | The system shall represent the Gas Tank as gas-payment ETH on the Owner Address and outside the wallet contract. |
| DR-005 | Token whitelist | The system shall store or reference token whitelist data including exchange rate, loadability, and burnability attributes. |
| DR-006 | Exchange-rate data | The system shall consume exchange-rate data for wallet-related token operations. |
| DR-007 | ENS-resolved contract address | The system shall use ENS-resolved Ethereum addresses for supporting contract integration. |
| DR-008 | Controller counts | The system shall represent `adminCount` and `controllerCount` as `uint256` values. |

## 7. System Constraints

| ID | Constraint |
|---|---|
| C-001 | The product is constrained to Ethereum-based smart-contract operation. |
| C-002 | Supporting contract locations are constrained to ENS-based resolution. |
| C-003 | Token use is constrained by token whitelist data, including loadability and burnability status. |
| C-004 | Gas-payment ETH is constrained to remain outside the Consumer Contract Wallet and outside wallet security protections. |
| C-005 | The Owner role is constrained to an externally owned address. |

## 8. Verification and Acceptance Criteria

| Requirement ID | Verification method | Acceptance criterion |
|---|---|---|
| FR-001 | Test | Verify through a wallet conversion or related wallet operation that exchange-rate data is used for amount conversion, and verify that the operation fails when the required rate is zero or the token is unavailable. |
| FR-002 | Test | Verify in an ENS-enabled test environment that controller, token whitelist, oracle/licence, and related nodes can be registered and resolved to target contract addresses before use. |
| FR-003 | Test | Verify through token-loading or equivalent token-operation tests that token whitelist `loadable` status controls success or failure, and that whitelist rate and burnability data are available for the corresponding operation. |
| FR-004 | Inspection | Confirm that the Consumer Contract Wallet is defined to hold user ETH and ERC20 assets. |
| FR-005 | Inspection | Confirm that gas-payment ETH is defined as the Gas Tank on the Owner Address and is outside the wallet contract and its security protections. |
| FR-006 | Demonstration | Demonstrate controller binding support for `Transact` with method name and parameters and for `Transfer` when supported. |
| FR-007 | Test | Demonstrate that a read-only `adminCount` call returns a `uint256` value. |
| FR-008 | Test | Demonstrate that a read-only `controllerCount` call returns a `uint256` value. |
| FR-009 | Demonstration | Demonstrate that supported bindings provide `Call` for read-only interactions and `Transact` or `Transfer` for paid interactions. |
| NFR-001 | Inspection | Confirm that Ethereum and ENS are required runtime dependencies. |
| NFR-002 | Inspection | Confirm the documented separation between protected wallet assets and gas-payment ETH. |
| NFR-003 | Inspection | Confirm that bindings separate read-only and paid interaction paths. |
