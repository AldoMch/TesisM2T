# Human SRS Review Sheet

## Metadata

- Sample directory: `s000025_9ba1413f`
- Generated SRS: `final_srs.md`
- Evidence pack: `evidence_pack.json`
- Review model: `claude-opus-4-8`
- Generated at: `2026-06-05T15:39:59.738084Z`
- Raw model response: `model_srs_review_raw.md`
- Parse status: `parsed`

## Overall Model Opinion

- Recommendation: `revise`
- Confidence: `0.78`
- Rationale: The SRS is well-traced and conservative for most claims, but several requirements overstate the evidence: FR-005 asserts token verification is invoked when E005 only imports verifyIdToken without showing the call; the cookie-storage claim is from a code comment, not behavior; and FR-007/return-400 details slightly exceed what the truncated evidence shows.

## Overall Human Decision

- [ ] Accept
- [ ] Reject
- [ ] Partial accept

Reason:
> 

## Positive Observations

- Strong, accurate traceability of FR-001/FR-002 to the exact fetch calls in E001/E003, including method, content-type, and same-origin credentials.
- SRS is appropriately conservative in noting logout has no request body and that no direct end-user UI is described in evidence.
- Firebase environment-variable externalization (FR-006/NFR-003/DR-004) is precisely grounded in next.config.js (E006).
- Verification methods and acceptance criteria are concrete for the request/response behaviors.

## Candidate Issues

### R001: unsupported_claim

- Severity: `major`
- Suggested action: `needs_human_check`
- SRS location: FR-005; Section 8; Traceability FR-005
- Evidence IDs: E005

**Claim or gap**

FR-005 states the login API 'shall invoke Firebase token verification as part of processing the login request.' E005 imports `verifyIdToken` and contains a comment about decoding the token, but the handler text shown is truncated and does not actually display a call to `verifyIdToken(token)`.

**Model opinion**

The presence of an import and an explanatory comment is weaker evidence than an observed invocation. The handler body shown only extracts `token` and returns 400 on missing body; the verification call is not visible in the chunk. This claim may be partially aspirational (the comment describes intended approach).

**Recommended human check**

Open pages/api/login.js at the commit and confirm whether `verifyIdToken(token)` (or equivalent) is actually called within the handler, not just imported.

**Model proposed SRS change**

If the call is not present in code, reword FR-005 to: 'The login API imports Firebase ID token verification (`verifyIdToken`) for use during login processing.' and lower Traceability confidence to Low. If the call is present, add the specific line as evidence.

Optional human revised fix:
> 

**Human decision**

- [ ] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> 

### R002: unsupported_claim

- Severity: `major`
- Suggested action: `needs_human_check`
- SRS location: Section 6 Data Requirements – Storage row ('Session storage')
- Evidence IDs: E005

**Claim or gap**

The SRS states 'the user's Firebase token is decoded and stored in a cookie' citing E005. E005 shows this only as a code comment ('// Here, we decode the user's Firebase token and store it in a cookie'), not implemented behavior.

**Model opinion**

Treating a descriptive/aspirational comment as a system behavior is a misattribution. The comment even suggests using express-session 'or similar' as guidance, implying it is not yet implemented.

**Recommended human check**

Verify whether cookie/session storage is actually implemented in login.js or commonMiddleware, or whether it exists only as a planning comment.

**Model proposed SRS change**

Replace the Session storage statement with: 'A code comment indicates an intended design to decode the Firebase token and store it in a cookie; actual cookie/session storage is not demonstrated in the available evidence.' Mark confidence Low.

Optional human revised fix:
> 

**Human decision**

- [ ] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> 

### R003: ambiguity

- Severity: `minor`
- Suggested action: `probably_ignore`
- SRS location: FR-003; Section 8
- Evidence IDs: E005

**Claim or gap**

FR-003 says the API returns 'HTTP status 400' on missing body. E005 shows `return res.status(400);` which sets status but may not send a complete response (no `.end()`/`.send()`/`.json()`).

**Model opinion**

The acceptance criterion 'returns HTTP 400' is observable, but the underlying code may not properly terminate the response. This is a minor verifiability nuance worth noting but the externally observable 400 status is likely acceptable.

**Recommended human check**

Confirm res.status(400) actually emits a response to the client in the runtime framework (Next.js API routes).

**Model proposed SRS change**

Optionally append to FR-003 verification note: 'Acceptance verified by observed HTTP 400 status; confirm response is fully terminated.'

Optional human revised fix:
> 

**Human decision**

- [ ] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> 

### R004: non_verifiable

- Severity: `minor`
- Suggested action: `needs_human_check`
- SRS location: FR-007 / NFR-004
- Evidence IDs: E002, E004

**Claim or gap**

FR-007 enumerates run modes (frontend+backend, frontend only, backend only) but E002/E004 README text has the actual commands truncated/blank ('will start both...'). NFR-004 ('remain compatible with...OnFleet') is not objectively testable.

**Model opinion**

Run modes are plausibly real but the specific commands are not in evidence, so the demonstration acceptance is weakly supported. NFR-004 is a vague compatibility statement without a measurable criterion.

**Recommended human check**

Check README/package.json scripts for the actual start commands for each mode; assess whether NFR-004 can be given a verifiable criterion or downgraded to a constraint.

**Model proposed SRS change**

For FR-007, add 'specific start commands not captured in evidence; verify against package.json scripts.' For NFR-004, either remove or restate as constraint C-002 (already present) to avoid a non-verifiable NFR.

Optional human revised fix:
> 

**Human decision**

- [ ] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> 

### R005: architecture_detail

- Severity: `minor`
- Suggested action: `needs_human_check`
- SRS location: Section 2 Product perspective; C-002
- Evidence IDs: E002, E004

**Claim or gap**

The SRS characterizes the backend as a strict 'two-part architecture (Firebase functions + OnFleet)'. The ground-truth architecture diagram (architecture-2.png) is referenced but not incorporated; there may be additional components (database, Next.js frontend, auth) not reflected.

**Model opinion**

Calling the backend 'constrained to' two parts may understate the actual architecture shown in the diagram. The README phrasing 'broken up into two parts' refers to how the backend is run, not necessarily a complete architecture constraint.

**Recommended human check**

Review docs/images/architecture-2.png to confirm components and whether 'two-part' is an accurate, complete characterization.

**Model proposed SRS change**

Soften C-002 to: 'The backend is organized into Firebase functions (custom APIs) and OnFleet (task handling) per README; additional components may exist per the architecture diagram.'

Optional human revised fix:
> 

**Human decision**

- [ ] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> 

### R006: traceability

- Severity: `minor`
- Suggested action: `probably_ignore`
- SRS location: FR-006 / DR-004 / C-004
- Evidence IDs: E006

**Claim or gap**

FR-006 and C-004 derive from E006 (next.config.js). The asset-loader list (C-004) and env mapping are accurate to E006, but note `API_URI` is commented out — SRS correctly omits it. No issue with omission, but confidence labeling could note the limited 4 env vars only.

**Model opinion**

Traceability here is strong and accurate. Minor: SRS could explicitly note that only the four uncommented FIREBASE_* vars are exposed (API_URI commented out).

**Recommended human check**

Confirm no other env vars are exposed elsewhere in env.js (which is required by next.config.js but not in evidence).

**Model proposed SRS change**

Add note to DR-004: 'Only the four FIREBASE_* variables are exposed via next.config.js; API_URI is present but commented out.'

Optional human revised fix:
> 

**Human decision**

- [ ] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
>
