# SRS.md

This is the shared compact SRS generation standard. Use it together with one repository-specific `evidence_pack.json`.

## Compact SRS Standard

# Compact SRS Generation Standard

Use this compact standard as the model context for generating an SRS from repository evidence.

## Scope

Generate a Software Requirements Specification aligned with ISO/IEC/IEEE 29148:2018. The SRS must be evidence-backed, concise, and traceable. Do not invent product facts that are not supported by the evidence.

## Required Output Structure

1. Introduction
   - Purpose
   - Product scope
   - Intended audience
   - References

2. Overall Description
   - Product perspective
   - Product functions summary
   - User classes
   - Operating environment
   - Assumptions and dependencies

3. External Interface Requirements
   - User interfaces
   - Software/API interfaces
   - Communication interfaces
   - Data exchange formats

4. Functional Requirements
   - Use IDs: FR-001, FR-002, ...
   - Each requirement must include description, trigger/input, system behavior, output, priority, verification method, and source evidence.

5. Non-Functional Requirements
   - Use IDs: NFR-001, NFR-002, ...
   - Cover only qualities supported by evidence, such as performance, security, reliability, usability, maintainability, portability, compatibility, or scalability.
   - Prefer measurable statements. If evidence is weak, mark the item as inferred.

6. Data Requirements
   - Data entities or objects
   - Input/output data
   - Storage, privacy, integrity, retention, or migration requirements if supported by evidence.

7. Constraints
   - Technology, platform, deployment, protocol, legal, license, or operational constraints.

8. Verification and Acceptance
   - Map each requirement to one verification method: Test, Inspection, Analysis, or Demonstration.

9. Traceability Matrix
   - Columns: ID, Requirement, Type, Source, Evidence Type, Verification, Confidence.

## Requirement Quality Rules

- Each requirement must be necessary, unambiguous, complete enough, single-purpose, feasible, verifiable, consistent, and traceable.
- Every requirement must cite evidence from the provided evidence pack.
- Use evidence type `explicit` for direct statements and `inferred` for reasoned conclusions.
- Omit unsupported content instead of adding a separate question list.
- Avoid vague terms such as fast, user-friendly, robust, scalable, secure, or high-quality unless evidence provides a concrete meaning.
- Keep the generated SRS focused. Do not include long explanations of the standard.

## Output Style

- Write in Markdown.
- Keep sections concise.
- Prefer tables for requirements and traceability.
- Preserve repository-specific terms from evidence.
- Mark missing information clearly instead of filling gaps with assumptions.

## Generation Instruction

Generate the final SRS for one repository using this compact standard and that repository's `evidence_pack.json`.

Rules:

- Use only facts from `evidence_pack.json`.
- Every requirement must cite one or more `evidence_id` values.
- Omit unsupported content instead of adding a separate question list.
- Keep assumptions and dependencies only when they are supported by evidence.
