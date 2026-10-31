# Human SRS Review Sheet

## Metadata

- Sample directory: `s000075_7722edce`
- Generated SRS: `final_srs.md`
- Evidence pack: `evidence_pack.json`
- Review model: `claude-opus-4-8`
- Generated at: `2026-06-05T16:05:46.752387Z`
- Raw model response: `model_srs_review_raw.md`
- Parse status: `parsed`

## Overall Model Opinion

- Recommendation: `revise`
- Confidence: `0.72`
- Rationale: The SRS is well-structured and mostly evidence-traceable, but it contains field-level contradictions, including Display fields and Gauge field types relative to the evidence, several inferred claims presented as explicit, and missing architecture detail because the Redux client state and TypeScript editor implementation from E003/E004 are underused. Targeted fixes are needed before acceptance.

## Overall Human Decision

- [ ] Accept
- [ ] Reject
- [x] Partial accept

Reason:
> ACCEPT=2, PARTIAL_ACCEPT=2, REJECT=2.

## Positive Observations

- Functional and data requirements are closely tied to concrete schema/model evidence (E004, E005, E006), with accurate field listings for Gauge, Display, and Layout.
- The SRS appropriately marks several items as inferred, including communication interfaces and wire format, rather than overstating them, and it explicitly notes the absence of privacy, retention, and migration evidence.
- Constraints C-001 through C-005 are well-grounded in the Dockerfile (E001) and README (E002), including the client-build-before-server-packaging dependency.
- The traceability matrix provides evidence IDs, evidence type, and confidence for each requirement, and is mostly consistent with the evidence pack.

## Candidate Issues

### R001: contradiction

- Severity: `major`
- Suggested action: `partial_accept_as_issue`
- SRS location: Section 3 Software/API interfaces - Display resource; FR-002/FR-003; Section 6 Data entities - Display
- Evidence IDs: E004, E005, E006

**Claim or gap**

The SRS lists the Display resource with field `key`, but the client Models.ts (E004) defines Display fields as `key, available, resolution_x, resolution_y, display_data, rotation` with no `current_layout`, while the server serializer (E005) includes `current_layout`. The SRS Display field list mixes server-only fields without flagging the client/server divergence.

**Model opinion**

E004 (client) and E005 (server) define divergent Display field sets: the client has no `current_layout`; the server serializer has `current_layout`, but client Models.ts lacks it. The SRS presents a single unified field list attributed to [E005] and [E006], which obscures a real discrepancy. This is a traceability/contradiction concern worth surfacing.

**Recommended human check**

Compare client/src/Models.ts (E004), the server serializer (E005), and models.py (E006) field by field for the Display entity, and confirm whether `current_layout` is intentionally absent from the client.

**Model proposed SRS change**

In Section 3 Display resource and Section 6 Display entity, add a note: "The server-side Display model/serializer (E005, E006) includes `current_layout` (FK to Layout, nullable, SET_NULL on delete); the client-side Display interface (E004) omits `current_layout`. This client/server field divergence should be reconciled." Attribute client-derived fields to [E004] and server-derived fields to [E005]/[E006] separately.

Optional human revised fix:
> In Section 3 Software/API interfaces - Display resource and Section 6 Display data entity, add: "The server-side Display model/serializer includes the current_layout layout reference field; the client-side Display interface only contains key, available, resolution_x, resolution_y, display_data, and rotation, and does not include this layout reference field. When the SRS discusses API/server-side resources, server-side fields should be used as the reference; when it discusses client-side state, the client-side field set should be noted separately." Also, the source for `current_layout` in FR-003 should be attributed only to server-side evidence.

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> The server-side Display model/serializer includes current_layout, but the client-side Display interface in Models.ts does not have this field. The current SRS writes the Display fields together as one unified list, which can hide the client/server field difference.

### R002: unsupported_claim

- Severity: `minor`
- Suggested action: `probably_ignore`
- SRS location: Section 6 Data entities - Gauge (`value` max length 600); Layout (`data` is binary; `display_positions` is text)
- Evidence IDs: E006

**Claim or gap**

Field-level details such as `value` max length 600, `data` stored as binary, and `display_positions` stored as text are stated as facts. These are supported by E006 (models.py), though the E006 text is truncated; Gauge max_length=600 and the binary/text fields are visible. This is largely supported, but the SRS should cite E006 specifically for these claims rather than co-citing E005.

**Model opinion**

E006 actually supports the detailed type claims: models.py shows max_length=600, BinaryField, and TextField. The issue is minor traceability: these model-specific details should cite E006 alone, not the serializer E005. The content itself is accurate.

**Recommended human check**

Confirm that models.py (E006) shows value max_length=600, data=BinaryField, and display_positions=TextField; ensure citations point to E006 for these type details.

**Model proposed SRS change**

In Section 6, change the Notes-column citations for type-specific details to cite [E006] only.

Optional human revised fix:
>

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> models.py clearly supports these field types: Gauge value has max length 600, Layout data is a binary field, and display_positions is a text field. The content itself is not wrong.

### R003: architecture_detail

- Severity: `major`
- Suggested action: `accept_as_issue`
- SRS location: Section 2 Product perspective; Section 3 User interfaces; FR-004/FR-005
- Evidence IDs: E003, E004

**Claim or gap**

Evidence E003 (client/src/Store.tsx) and E004 (Models.ts) show that the editor is a TypeScript/React + Redux single-page client with defined actions such as CONTROL_ADDED, ELEMENT_ADDED, SET_LAYOUTS, SET_GAUGES, SET_DISPLAYS, REQUEST_CANVAS_RENDER, and others, as well as a canvas rendering model. The SRS describes the editor only abstractly as a wizard that creates layouts, and never cites E003 or uses E004 for the editor architecture.

**Model opinion**

There is concrete evidence of the editor's client-side architecture, including Redux store, canvas render/delete actions, and gauge/layout/display state, that the SRS underuses. This is relevant for the architecture diagram check and would strengthen FR-004/FR-005. The wizard description from E002 is acceptable but thin given the richer code evidence.

**Recommended human check**

Review Store.tsx (E003) and Models.ts (E004) to confirm the Redux-based client with canvas rendering and the listed action types; compare with docs/architecture.png for the editor/viewer/server topology.

**Model proposed SRS change**

In Section 2 Product perspective, refine: "The client/editor is a TypeScript/React single-page application using a Redux store (E003) with actions for adding/updating controls and elements, setting layouts/gauges/displays, and requesting canvas render/delete operations (E003, E004)." Add [E003] citation to FR-004/FR-005 traceability.

Optional human revised fix:
> In Section 2 Product perspective, add: "The client/editor is a TypeScript/React single-page application that uses a Redux store to manage controls, elements, layouts, gauges, and display device state, and supports layout editing, render requests, and delete requests through canvas-related operations." Add sources [E003] and [E004] to FR-004/FR-005 and Section 9 Traceability.

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> Store.tsx and Models.ts show that the client/editor is not merely a generic wizard. It is a TypeScript/React + Redux single-page client that maintains layouts, gauges, displays, controls/elements, and canvas render/delete actions. The current SRS describes this architecture too thinly.

### R004: non_verifiable

- Severity: `minor`
- Suggested action: `partial_accept_as_issue`
- SRS location: FR-007; Section 8 acceptance for FR-007
- Evidence IDs: E002

**Claim or gap**

FR-007 ("viewer subsystem shall render what each display sees") and its acceptance criterion ("a reviewer can show per-display rendered output") rely solely on README prose (E002), which is itself incomplete ("Th..." is truncated), and the README notes that the docker image is not 100% standalone/ready. The viewer is described aspirationally; no code evidence for headless-browser rendering is provided in the cited evidence.

**Model opinion**

The viewer requirement is supported only by truncated README prose and there is no code/deployment evidence of an implemented headless-browser viewer in the cited evidence. Given the README's own "not 100% ready" caveat, FR-007 may overstate implemented scope. The acceptance criterion is demonstration-based but may not be demonstrable in the current state.

**Recommended human check**

Search the repository for any viewer/headless-browser implementation code; verify whether the viewer is implemented or only conceptual at this commit.

**Model proposed SRS change**

Mark FR-007 priority/status as planned or conceptual: append to FR-007 Requirement text, "This describes intended viewer behavior per the README architecture section (E002); implementation evidence at this commit is limited." Lower confidence to Low in Section 9.

Optional human revised fix:
> In FR-007, add: "This requirement describes the viewer behavior in the README; the source code contains a viewer page and browser/canvas rendering path, but headless-browser rendering and deployment maturity in this commit remain limited." In Section 8 FR-007 acceptance basis, revise to: "A reviewer can inspect that the viewer route and browser rendering path can read display data and generate a black-and-white pixel view rendered at the display resolution; complete headless-browser automated rendering requires separate verification." In Section 9, recommend lowering FR-007 confidence from "Medium" to "Medium/Low".

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> The model's statement that there is no viewer code evidence is not fully accurate; the source includes a /viewer/ route, ViewOnlyCanvas.tsx, and loadCanvas.js/puppeteer-related implementation. However, the viewer still has prototype/development traces, such as hard-coded display keys in scripts, and the README and Docker deployment are not fully mature. Therefore, the acceptance criterion should not be written too strongly.

### R005: scope

- Severity: `minor`
- Suggested action: `accept_as_issue`
- SRS location: Section 1 Product scope; NFR-001/Constraints C-005
- Evidence IDs: E001, E002

**Claim or gap**

The SRS does not surface the README's explicit caveat that the docker image is "building, but not 100% standalone/ready" (E002) and the Dockerfile's TODOs, including fixed npm version, real WSGI server, and runserver used as CMD (E001). These indicate that the deployment is development-grade/incomplete, which affects operational scope claims.

**Model opinion**

Both E001 and E002 contain explicit incompleteness signals, including TODOs, "not 100% ready", and `runserver` not being a production WSGI server. The SRS presents deployment constraints neutrally without noting that these constraints are development-stage. Including this point helps avoid overstating production readiness.

**Recommended human check**

Confirm that the Dockerfile uses `manage.py runserver` as a development server and that the README includes the standalone caveat; decide whether to add a maturity/limitations note.

**Model proposed SRS change**

Add to Section 7 a constraint C-006: "The supplied deployment is development-grade: the Dockerfile uses Django `runserver` (not a production WSGI server) and the README states the docker image is not yet fully standalone (E001, E002)."

Optional human revised fix:
> In Section 7 Constraints, add: "C-006: The provided containerized deployment is development-grade and not fully production-ready; the Dockerfile starts Django using the development server, and the README also states that the docker image is not fully standalone/ready." In Section 1 Product scope or NFR-001, add: "The current deployment evidence does not support a production-grade runtime maturity claim."

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> The README explicitly says the docker image is not 100% standalone/ready. The Dockerfile also has TODOs, including fixed npm version, using a real WSGI server, and the current CMD being Django runserver. The SRS should mark this as development-grade deployment and should not imply production readiness.

### R006: ambiguity

- Severity: `minor`
- Suggested action: `probably_ignore`
- SRS location: FR-002; Section 3 "unique name and resolution"
- Evidence IDs: E002, E006

**Claim or gap**

FR-002 states that displays are registered with a "unique key". README (E002) says "unique name"; the model (E006) uses `key` as primary key (CharField max_length=100). The SRS conflates "name" and "key". Whether the display's human-facing "name" equals the primary-key `key` is not stated.

**Model opinion**

Minor ambiguity: README's "unique name" versus the model's primary-key `key`. They are likely the same field, but the SRS should state this mapping explicitly to be verifiable.

**Recommended human check**

Confirm that the README "unique name" maps to the model `key` primary key field.

**Model proposed SRS change**

In FR-002 add: "The unique display identifier (README 'name') corresponds to the model `key` primary key field (E006)."

Optional human revised fix:
>

**Human decision**

- [x] Accept
- [ ] Reject
- [ ] Partial accept (`PARTIAL_ACCEPT`: mixed claims; some are valid and some are invalid)

Optional human note:
> The README's "unique name" appears in the API path, the server model uses key as the primary key, and the client also uses newDisplay.key when creating a display. Writing it as a unique key does not cause a substantive error.
