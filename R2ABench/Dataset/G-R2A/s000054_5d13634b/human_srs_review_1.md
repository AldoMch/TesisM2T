<!-- human_srs_review_A.md aligned with reviewer C content. Original human_srs_review.md is preserved. All human judgments are in English. -->

# Human SRS Review Sheet

## Metadata

- Sample directory: `s000054_5d13634b`
- Generated SRS: `final_srs.md`
- Evidence pack: `evidence_pack.json`
- Review model: `claude-opus-4-8`
- Generated at: `2026-06-05T15:52:43.482253Z`
- Raw model response: `model_srs_review_raw.md`
- Parse status: `parsed`

## Overall Model Opinion

- Recommendation: `revise`
- Confidence: `0.74`
- Rationale: The SRS is well-structured and most requirements trace to the six evidence chunks. However, several requirements overstate or interpolate beyond what the truncated evidence actually supports, such as `load TokenCard` eligibility, FR-003 specificity, and the user classes derived from a truncated bullet list. The architecture diagram, the ground-truth SVG, is also not examined. A focused revision plus human checks on a few interpolated claims is warranted.

## Overall Human Decision

- [ ] Accept
- [ ] Reject
- [x] Partial accept

Reason:
> ACCEPT=3, PARTIAL_ACCEPT=2, REJECT=2.

## Positive Observations

- Strong, consistent traceability: each FR/NFR cites specific evidence IDs, and a traceability matrix with confidence levels is provided.
- FR-007/FR-008, `adminCount`/`controllerCount` returning `uint256`, are precisely and correctly grounded in E005/E006, including method signatures.
- The SRS appropriately states that no end-user UI is evidenced, avoiding fabrication.
- The clear separation of read-only Call vs paid Transact/Transfer interaction patterns is accurately drawn from the Go bindings in E003/E004.

## Candidate Issues

### R001: unsupported_claim

- Severity: `major`
- Suggested action: `partial_accept_as_issue`
- SRS location: Section 2 User classes; Data entities (Owner, Token Group Ltd service addresses)
- Evidence IDs: E002

**Claim or gap**

The SRS asserts specific user classes: `Owner` as an externally owned address that owns the user's smart contracts, and `Token Group Ltd operated service addresses`. These are derived from E002, but E002 is a truncated bullet list with broken sentences, such as "This will own all of the user's Smart Contracts" and "The - Is a set of Addresses, owned and operated by Token Group Ltd".

**Model opinion**

E002 supports that an Owner / Externally Owned Address concept exists and that Token Group Ltd operates a set of service addresses, but the bullets are fragmentary. The precise role definitions and responsibilities are inferred. The Owner role claim is plausibly supported, and the specific phrasing "owns the user's smart contracts" is directly in the text. The Token Group Ltd "service addresses" label is a reasonable but partly interpolated reconstruction.

**Recommended human check**

Open `README.md` at the commit and read the full Requirements/roles section to confirm role names, definitions, and whether additional roles, such as controllers or admins, are defined.

**Model proposed SRS change**

In Section 2 User classes, soften to: "Token Group Ltd operated service addresses: a set of addresses, owned and operated by Token Group Ltd, used to provide services to the end user (role definition partially evidenced; see README Requirements section). Source: E002." Confirm or expand after reading the full README.

Optional human revised fix:
> In Section 2 User Classes and Section 6 Data Entities, revise to: Controller: a set of addresses owned and operated by Token Group Ltd, used to provide services to end users and participate in control/confirmation operations. Source: E002 plus the full README Requirements section. Keep Owner, but write it as: Owner: the user's Owner Address / externally owned address, which owns that user's smart contracts.

**Human decision**

- [ ] Accept
- [ ] Reject
- [x] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> The full README confirms the definitions of Owner Address and Controller, so the issue is not completely unsupported. However, the SRS phrases "Token Group Ltd operated service addresses" too broadly; the original text is more accurately Controller, a set of addresses owned and operated by Token Group Ltd.

### R002: unsupported_claim

- Severity: `major`
- Suggested action: `partial_accept_as_issue`
- SRS location: FR-003, Product functions summary, C-003
- Evidence IDs: E001

**Claim or gap**

FR-003 and related claims state the whitelist "determines which tokens can be used to load TokenCard" as a firm requirement, but E001 is truncated mid-sentence: "...also determines which tokens can be used to load the TokenCard and which...". This leaves the full constraint incomplete.

**Model opinion**

The `load TokenCard` eligibility statement is directly present in E001, but the sentence is cut off, so the full set of conditions governed by the whitelist is unknown. The requirement is supported in spirit but should not be stated as complete. Mapping it to a verifiable eligibility-decision output is somewhat speculative given the truncation.

**Recommended human check**

Read the complete `tokenWhitelist` description in `README.md` to capture all functions the whitelist governs, including security, load eligibility, and the truncated "and which..." clause.

**Model proposed SRS change**

In FR-003 System Behavior, append a note: "Whitelist scope is partially evidenced; the README sentence describing TokenCard load eligibility is truncated in the evidence pack and should be completed against full source." Keep the requirement but flag incompleteness.

Optional human revised fix:
> In Product Functions Summary, FR-003, C-003, and the Token Whitelist data entity, revise to: The system shall use the token whitelist to record token exchange rates, whether tokens may be used for TokenCard loading, and whether tokens may be burned by the TKN Holder Contract, and shall use this information to support wallet security and load-eligibility decisions.

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> The model's concern about E001 truncation is correct. After the full README is restored, the whitelist not only determines which tokens may be used to load TokenCard, but also determines which tokens may be burned by the TKN Holder Contract; `tokenWhitelist.sol` also has `loadable` and `burnable` fields.

### R003: scope

- Severity: `major`
- Suggested action: `accept_as_issue`
- SRS location: Whole SRS; Section 1 Product scope
- Evidence IDs: E001, E005, E006

**Claim or gap**

The repository contains 40 documents, including Solidity contracts referenced in the README (`wallet.sol`, `oracle.sol`, `controller.sol`, `tokenWhitelist.sol`) and many Go bindings/tests, but the SRS draws functional detail almost exclusively from six evidence chunks: README plus selected controller binding and oracle mock material. Significant contract behavior, such as whitelist add/remove, controller admin management, and oracle update flows, is likely present but not represented.

**Model opinion**

The SRS is honest about being limited to provided evidence, but it presents itself as a requirements statement for the repository while only covering a thin slice. `adminCount`/`controllerCount` imply admin and controller management functions that are not captured. This is an understatement of scope risk rather than a false claim.

**Recommended human check**

Inspect `controller.sol` / `controller.go` for state-changing methods such as `addAdmin` and `removeController`, and inspect `tokenWhitelist.sol` for add/remove token operations to determine whether material functional requirements are missing.

**Model proposed SRS change**

Add a scope-limitation note to Section 1 Product Scope: "This SRS is derived from a limited evidence subset (README and selected Go bindings). State-changing controller/whitelist/oracle operations present in the contracts are not fully represented and require source review before treating this SRS as complete."

Optional human revised fix:
> In Section 1 Product Scope, add: Scope limitation: This SRS is mainly generated from README and selected Go binding evidence. It does not yet fully cover state-changing behavior in the Solidity contracts, including controller management, token whitelist management, oracle exchange-rate updates, wallet whitelist and limit configuration, Gas Tank top-up, and TokenCard load workflows. Source-level review should be added before treating this SRS as a complete requirements document.

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> The full source shows that the SRS coverage is clearly too narrow. It misses a large amount of core behavior, including controller admin/controller add/remove, tokenWhitelist token add/remove and rate updates, oracle rate update flows, wallet address whitelists, daily limits, Gas Tank top-up, and TokenCard load.

### R004: traceability

- Severity: `minor`
- Suggested action: `probably_ignore`
- SRS location: FR-006, Communication interfaces, Section 3 Controller contract
- Evidence IDs: E003, E004

**Claim or gap**

FR-006 cites only E003 for controller Transact/Transfer, but the Transfer/Transact semantics are evidenced identically in both E003, controller, and E004, oracle mock. The generic binding pattern, FR-009, is the better home for E004; FR-006 about controller specifically should be careful that E003 is the controller-specific source.

**Model opinion**

This is minor traceability cleanup. E003 does cover controller Transact and Transfer, so FR-006 is correctly sourced. There is no contradiction; just ensure E004, the oracle mock, is not used to justify controller-specific claims elsewhere.

**Recommended human check**

Confirm E003 alone substantiates controller Transact/Transfer and that no controller claim relies solely on the oracle mock in E004.

**Model proposed SRS change**

No change required if E003 is confirmed; optionally annotate FR-009 to clarify that E004 is the oracle-mock binding example and not a controller source.

Optional human revised fix:
> 

**Human decision**

- [ ] Accept
- [x] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> FR-006 correctly cites E003. E003 alone proves the controller Transact / Transfer behavior. E004 is an oracle mock binding example and is more appropriate for proving the generic binding pattern, but this does not constitute a required SRS defect.

### R005: architecture_detail

- Severity: `major`
- Suggested action: `accept_as_issue`
- SRS location: Section 2 Product perspective; architecture
- Evidence IDs: E001, E002

**Claim or gap**

A ground-truth high-level architecture diagram, `docs/high_level_architecture.svg`, exists but was not used. The SRS architecture narrative, wallet -> ENS -> oracle/controller/whitelist, should be cross-checked against the diagram, which may show additional components or relationships, such as Gas Tank, Owner, controller-admin relationships, oraclize connector.

**Model opinion**

The diagram is the authoritative architecture source and could reveal missing components or correct mischaracterizations. Not consulting it is a notable gap for the architecture sections.

**Recommended human check**

Open `docs/high_level_architecture.svg` and compare its components and edges against Section 2 and the Data Entities table; add any missing components/relationships.

**Model proposed SRS change**

Add to References and Section 2: cite `docs/high_level_architecture.svg` as the architecture source, and reconcile the component list/relationships after review.

Optional human revised fix:
> In References, Section 2 Product Perspective, and Section 6 Data Entities, add: The architecture source includes `docs/high_level_architecture.svg`. The system centers on the Consumer Contract Wallet. The Owner Address controls the wallet. The wallet resolves supporting contracts such as controller, token whitelist, and licence through ENS. The token whitelist and oracle provide token support status and exchange rates. Controller addresses participate in 2FA/control operations. The Gas Tank represents gas ETH on the Owner Address, outside the wallet contract.

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> `docs/high_level_architecture.svg` exists, and the README architecture section plus contract relationship descriptions support supplementing the architecture section. The current SRS says too little about the relationships among wallet, ENS, oracle, controller, and tokenWhitelist, and it also omits relationships involving Gas Tank, Owner, Controller, Licence/TKN Holder/CryptoFloat, and the loading flow.

### R006: non_verifiable

- Severity: `minor`
- Suggested action: `partial_accept_as_issue`
- SRS location: FR-001, FR-002, FR-003 verification rows; Section 8
- Evidence IDs: E001

**Claim or gap**

FR-001/002/003 are assigned verification method `Test` with acceptance such as "Demonstrate that a wallet security-related operation retrieves oracle exchange-rate data", but the underlying evidence, README prose, does not specify observable interfaces or test harnesses for these wallet flows. The evidenced bindings are for controller/oracle, not the wallet's oracle-fetch flow.

**Model opinion**

These acceptance criteria are framed as testable, but no evidenced interface exposes the wallet's oracle retrieval as a measurable output. Marking them `Test` may overstate verifiability given only README prose. Inspection or source-derived test targets would be more honest until `wallet.sol` is examined.

**Recommended human check**

Check `wallet.sol` / wallet bindings for an observable oracle-rate retrieval or ENS-resolution interface that can serve as a concrete acceptance target; otherwise downgrade the verification method.

**Model proposed SRS change**

For FR-001/FR-002/FR-003, change Verification from `Test` to `Inspection`, or add a precondition: "pending identification of an observable wallet interface in wallet.sol", until a concrete test target is confirmed.

Optional human revised fix:
> FR-001 acceptance: Verify through the wallet conversion interface that token/stablecoin/ETH exchange-rate data is used for amount conversion, and verify that the operation fails when the rate is 0 or the token is unavailable. FR-002 acceptance: Verify in an ENS test environment that controller, token whitelist, oracle/licence, and related nodes can be registered and resolved to target contract addresses. FR-003 acceptance: Verify through TokenCard load tests that token `loadable` status controls load success/failure and produces the corresponding load event or failure result.

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> The model is reasonable that "Test" cannot be justified from README alone. However, the full source and tests provide observable interfaces such as `ConvertToEther`, `ConvertToStablecoin`, `LoadTokenCard`, and ENS registration/resolution setup. Therefore the requirement should not simply be downgraded to Inspection; the test basis and acceptance targets should be supplemented.

### R007: ambiguity

- Severity: `minor`
- Suggested action: `probably_ignore`
- SRS location: FR-005 / NFR-002 (Gas Tank)
- Evidence IDs: E002

**Claim or gap**

E002 text is fragmentary: "The Gas Tank is a representation of the ETH on the user's ." The sentence is truncated. FR-005 states gas ETH is represented as a Gas Tank outside the smart contract wallet, which is supported, but the precise location/representation, "on the user's ...", is unresolved.

**Model opinion**

The core claim, gas ETH not protected and outside the wallet, is well supported. The exact representation of where the Gas Tank ETH resides is ambiguous due to truncation. The risk is low but worth clarifying.

**Recommended human check**

Read the complete Gas Tank sentence in the README to determine where the gas ETH resides, such as on the user's externally owned address.

**Model proposed SRS change**

In FR-005, optionally complete the description once verified: "gas-payment ETH represented as a Gas Tank residing outside the wallet contract (e.g., on the user's externally owned address; confirm exact wording from README)."

Optional human revised fix:
> 

**Human decision**

- [ ] Accept
- [x] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> The full README clearly states that the Gas Tank is ETH on the user's Owner Address and is outside the smart contract wallet, not protected by the wallet security features. The current SRS core statement is correct, although it could be more precise.
