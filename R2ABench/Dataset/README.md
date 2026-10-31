# Dataset inputs

E-R2A contains 17 projects; G-R2A contains 51. Project/sample IDs are stable.
Reference `AD/ad.puml` files express the structural comparison targets.
`checked_srs.md` is the current SRS. Original documents, evidence packs and
reference-image provenance already present in the repository are retained.

Each `req_final.jsonl` is a UTF-8 JSON Lines curated requirement list. The release
contains 480 records across 68 files. `req_id` is the stable scoring key;
`requirement` and any retained source fields describe the item.
`category` records the primary concern of each requirement:

- Domain functionality
- Identity and security
- Data management
- Deployment and operations
- Execution and resources
- User interaction
- Recovery and consistency

The curated records in `req_final.jsonl` supply the requirement identities and
content for the released coverage analyses. Older `req.jsonl` files are
construction intermediates and do not define the scoring denominator.

SRS review files and `G-R2A/_agreement/` remain part of the dataset construction
record. They are separate from the old architecture-score human ratings, which
are excluded from this release.
