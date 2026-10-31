# Human SRS Review Sheet

## Metadata

- Sample directory: `s000002_0f72cc9f`
- Generated SRS: `final_srs.md`
- Evidence pack: `evidence_pack.json`
- Review model: `claude-opus-4-8`
- Generated at: `2026-06-05T15:27:37.075021Z`
- Raw model response: `model_srs_review_raw.md`
- Parse status: `parsed`

## Overall Model Opinion

- Recommendation: `revise`
- Confidence: `0.72`
- Rationale: The SRS is generally well-traced to evidence and conservative in most claims. However, several requirements overstate or misattribute behavior (e.g., credential submission flow, NFR-002 deterministic phrasing), the VR/scene-based content domain (Lobby, Louvre, Berlin, etc.) is understated, and the architecture diagram is not referenced despite being available. A few traceability tags are weak. Targeted revisions are warranted before acceptance.

## Overall Human Decision

- [ ] Accept
- [ ] Reject
- [x] Partial accept

Reason:
> ACCEPT=4, PARTIAL_ACCEPT=1, REJECT=2.

## Positive Observations

- Server-side user controller requirements (FR-003 create, FR-004 findAll/findOne, FR-005 comparePassword) are accurately and directly traced to E001/E002.
- NFR-001 (bcrypt comparison instead of plaintext equality) is a strong, evidence-backed security requirement.
- The SRS appropriately records explicit absence of privacy/retention/migration evidence rather than inventing requirements.
- Verification methods and acceptance bases are largely observable and tied to concrete UI/code behaviors (e.g., .error element display, recursion termination).
- Traceability matrix with confidence levels is present and mostly well-aligned to evidence chunks.

## Candidate Issues

### R001: scope

- Severity: `major`
- Suggested action: `needs_human_check`
- SRS location: Section 1 Product scope; Section 2 Product functions summary
- Evidence IDs: E006

**Claim or gap**

The SRS describes the product narrowly as 'authentication and client interaction capabilities' and 'paragraph-oriented content,' but E006 shows the client imports many scene components (Lobby, SF, Louvre, Berlin, Milan, Rome, Hack, Camera, Sky, Plane, TextPlane) indicating a VR/immersive multi-scene experience that is the apparent core product.

**Model opinion**

The repository name (escape-reality), the architecture diagram, and the extensive A-Frame scene imports strongly suggest the product's primary purpose is a VR/immersive multi-location experience, not merely authentication. The SRS understates the core domain and frames it as incidental.

**Recommended human check**

Inspect react-client/src/components/App.js and the referenced scene components (Lobby, Louvre, Berlin, etc.) to confirm the product is a multi-scene VR experience. Review architecture1.png.

**Model proposed SRS change**

In Section 1 Product scope, add a bullet: 'A multi-scene A-Frame/VR client composed of distinct location scenes (e.g., Lobby, Louvre, Berlin, Milan, Rome, SF, Hack) rendered via aframe-react (E006).' Adjust the Purpose sentence to acknowledge the immersive scene-based experience as a primary capability rather than secondary.

Optional human revised fix:
> Agree with the proposed change.

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> App.js, Lobby.js, and architecture1.png have been checked, confirming that the SRS product scope is too narrow.

### R002: architecture_detail

- Severity: `major`
- Suggested action: `needs_human_check`
- SRS location: Section 2 Product perspective; References
- Evidence IDs: none

**Claim or gap**

A ground-truth architecture diagram exists (diagrams/architecture1.png) but is neither referenced nor reconciled against the SRS's client-server description.

**Model opinion**

The SRS infers a client-server architecture from controller code, but does not cite or validate against the provided architecture diagram. Architectural claims (e.g., what server endpoints exist, how the React client communicates) should be checked against the diagram.

**Recommended human check**

Open diagrams/architecture1.png and confirm the described client-server structure, the communication mechanism between React client and the user controller, and whether any components (DB, API routes, VR scene server) are missing from the SRS.

**Model proposed SRS change**

Add to Section 1 References: 'Architecture diagram: diagrams/architecture1.png.' Add a note in Section 2 Product perspective stating the client-server topology should be validated against architecture1.png, and list any additional components shown there.

Optional human revised fix:
> Add to Section 1 References: "Architecture diagram: diagrams/architecture1.png." In Section 2 Product perspective, add that the system includes a Web Client (A-Frame, React, React-Router), Web Server (Node, Express, DigitalOcean deployment), AWS S3 image service, Redis Cache, and MariaDB Database (Users, Likes, Photos, Comments).

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> Accepted. architecture1.png has been checked, confirming that the architecture diagram should be added as an SRS reference and that the product perspective should include the architecture elements shown in the diagram, including Web Client, Web Server, AWS S3, Redis Cache, and MariaDB/Database.

### R003: unsupported_claim

- Severity: `major`
- Suggested action: `needs_human_check`
- SRS location: FR-001 / FR-002 (System behavior, Output)
- Evidence IDs: E003, E004, E005

**Claim or gap**

FR-001 and FR-002 claim distinct credential capture for separate sign-up vs sign-in forms with state capture, but the evidence (E003, E004) shows signup.jsx and signin.jsx are presentational components calling props.onEmailChange/onPasswordChange; the actual state capture and submitFn live in App.js (E005) shared across both. The mapping of capture to two separate forms with independent behavior is partially inferred.

**Model opinion**

E005 shows a single onEmailChange/onPasswordChange/submitFn in App.js feeding both views. The SRS's split into FR-001 and FR-002 with separate 'captured email/password state' per form may overstate separation. The credential submission behavior (submitFn) is also visible in E005 but is truncated and not captured as a requirement.

**Recommended human check**

Confirm in App.js whether email/password state and submission are shared handlers used by both signup and signin views, and whether the submission flow (submitFn) posts credentials to the server.

**Model proposed SRS change**

Revise FR-001/FR-002 system behavior to note that credential capture handlers (onEmailChange/onPasswordChange) and submission are implemented in the shared App component (E005), with signup.jsx/signin.jsx providing presentational input fields and cross-navigation (E003/E004). Consider adding FR-008 for credential submission once the submitFn target is verified.

Optional human revised fix:
> Partially accept. Narrow FR-001/FR-002 to interface input and shared input handling, and add FR-008 to describe client credential submission. Suggested SRS revision:
>
> | FR-008 | Client credential submission | The user clicks the submit button in the signup or signin view | The system shall use the shared `submitFn` to read the email and password from App component state and submit them as a JSON POST request to the current authentication route (`/signup` or `/signin`). | Server registration or authentication response; when the response contains a successful authentication status, the client navigates to `/dashboard`. | High | Test | E003, E004, E005, server/server.js |
>
> FR-008 covers only the client-side credential submission behavior; user creation, password hashing, and password comparison remain covered by FR-003 and FR-005.

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> I mark this issue as partially accepted. The review correctly identifies that FR-001/FR-002 overstate independent state capture in the signup/signin forms; they should be revised to interface input, cross-view navigation, and shared input handling. Further inspection confirms the `submitFn` target and server-side authentication routes, so FR-008 may be added to describe client credential submission to `/signup` or `/signin`. However, the proposed submission wording must remain scoped and must not expand into the full signup or authentication processing flow.

### R004: ambiguity

- Severity: `minor`
- Suggested action: `needs_human_check`
- SRS location: NFR-002 / FR-006
- Evidence IDs: E005

**Claim or gap**

NFR-002 phrases sequential content retrieval as 'deterministic' reliability with 'set the final paragraph state exactly once.' The evidence (E005) shows a recursion terminating at titleIndex === allTitles.length calling setStateParagraph(result), but does not establish determinism guarantees (e.g., ordering under async fetch races).

**Model opinion**

The recursion is sequential by construction (each fetch callback triggers the next), so ordering is plausible, but 'deterministic' and 'reliability' framing may overstate a verifiable quality attribute. The 'exactly once' claim is reasonable from the termination branch but the truncated code should be confirmed.

**Recommended human check**

Review the full recurse/fetch implementation in App.js to confirm setStateParagraph is invoked once at termination and that fetches truly run in sequence (not in parallel).

**Model proposed SRS change**

Reword NFR-002 to: 'The client shall process titles sequentially via recursive fetch callbacks, invoking the final state-setting operation once when the title index equals the title list length (E005).' Remove the unsupported 'deterministic' qualifier unless verified.

Optional human revised fix:
> Rewrite NFR-002 as: "The client shall process titles sequentially through recursive fetch callbacks and invoke the final state-setting operation once when the title index equals the title list length (E005)." Remove the unsupported "deterministic" qualifier unless verified.
> Rewrite FR-006 as:
> | FR-006 | Sequential content retrieval | The client receives a title list and starts content retrieval | The system shall request `/getWiki?exactWikiTitle=...` content one title at a time in title order; after each request succeeds, it shall continue to the next title, and after all titles have been successfully processed, it shall set the final paragraph result state once. | Accumulated paragraph/content result state; if a request fails, display the error indication according to FR-007. | Medium | Test | E005 |

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> Accepted. The complete App.js content retrieval flow has been checked: the client starts the next title retrieval only after each request succeeds, so the success path processes titles sequentially; when the title index reaches the title list length, the system invokes the final paragraph state-setting operation once. If a request fails, the code displays an error indication and does not continue retrieving later titles, so NFR-002 should not be stated as unconditional "reliability" or "continue until completion." The content should be narrowed from NFR-002 and folded into FR-006 system behavior or acceptance basis: when each content request succeeds, the system shall retrieve content in title order, accumulate results, and submit the final paragraph state once all titles have been processed; request failure is covered by FR-007.

### R005: traceability

- Severity: `minor`
- Suggested action: `accept_as_issue`
- SRS location: FR-001 evidence (E003, E005); Data exchange / E005 attribution
- Evidence IDs: E003, E004, E005

**Claim or gap**

FR-001 cites E005 for sign-up capture, but E005 (App.js) contains shared handlers and content fetch logic, not sign-up-specific behavior. The evidence linkage between presentational components (E003/E004) and the App.js handlers (E005) is conflated.

**Model opinion**

The traceability is broadly correct but imprecise: E005 supports the existence of capture/submit handlers generally, not sign-up-specific capture. Tightening evidence attribution improves verifiability.

**Recommended human check**

Verify which component owns the email/password state and confirm whether sign-up and sign-in share the same handlers.

**Model proposed SRS change**

In the traceability matrix, annotate that E003/E004 support the presentational input fields and E005 supports the shared state/submission handlers, rather than implying E005 is sign-up specific.

Optional human revised fix:
>

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> I reject this as an independent issue. FR-001 reasonably uses E003 and E005 together to support signup-view input fields and shared input handling; overlapping evidence sources or cross-component attribution do not constitute a substantive SRS defect. The related wording precision issue is already covered by R003. When revising FR-001/FR-002, it is sufficient to state that E003/E004 support interface fields and navigation while E005 supports shared input handling; no separate traceability issue is needed.

### R006: missing_requirement

- Severity: `minor`
- Suggested action: `needs_human_check`
- SRS location: Section 4 Functional Requirements (credential submission)
- Evidence IDs: E005

**Claim or gap**

E005 shows a submitFn that grabs email/password and is annotated 'Submit email and password for verification,' but no functional requirement captures the client-side credential submission to the server.

**Model opinion**

Submission of captured credentials for verification is a core authentication step visible in evidence but absent from the functional requirements, which only cover capture (FR-001/002) and server-side compare (FR-005). The connecting submission step is missing.

**Recommended human check**

Inspect submitFn in App.js to determine the submission target (endpoint/route) and add a requirement for client credential submission.

**Model proposed SRS change**

Add FR-008: 'The client shall submit captured email and password values for verification upon form submission (E005).' Specify the server endpoint after verifying submitFn's request target.

Optional human revised fix:
> Apply the same revision as R003.

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> I accept this issue. App.js, signup.jsx, signin.jsx, and server/server.js have been checked, confirming that client credential submission is a missing functional requirement in the current SRS. The submit buttons in both signup and signin views call the shared `submitFn`; `submitFn` reads email and password from App state and submits them as a JSON POST request to the current authentication route (`/signup` or `/signin`). The server also provides corresponding `POST /signup` and `POST /signin` routes. FR-008 should be added to describe client credential submission; this requirement covers only client submission and authentication response handling, and does not duplicate FR-003 user creation or FR-005 password comparison.

### R007: unsupported_claim

- Severity: `minor`
- Suggested action: `probably_ignore`
- SRS location: Operating environment / NFR-001 — bcrypt naming
- Evidence IDs: E001

**Claim or gap**

The SRS sometimes refers to 'bcrypt' generically and the constraint C-003 to 'bcrypt-nodejs.' E001 explicitly uses require('bcrypt-nodejs'). Consistency is fine, but NFR-001 verification 'Inspection' relies on the comparePassword path which uses callback(isMatch) — acceptable. No contradiction, but generic 'bcrypt' wording could be tightened.

**Model opinion**

Minor wording consistency; evidence clearly supports bcrypt-nodejs. Low priority.

**Recommended human check**

Confirm bcrypt-nodejs is the only password hashing library; ensure SRS consistently names it.

**Model proposed SRS change**

Standardize references to 'bcrypt-nodejs' across Operating environment, NFR-001, and FR-005 where the specific library is meant.

Optional human revised fix:
> 

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> I reject this as a required SRS defect. The model does not show that the statement in the operating environment / NFR-001 — bcrypt naming causes significant harm to correctness, verifiability, scope, or traceability, or that the concern is only a low-value wording preference. Evidence basis: E001. For this problem, the necessary SRS changes are not required.
