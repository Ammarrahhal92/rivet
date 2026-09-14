# Contributing to Rivet

Rivet contains four independently installable skills with distinct responsibility boundaries. Keep discovery, commercial-authority review, canonical triage, and remediation/closure within their respective packages; do not silently expand one skill into another skill's responsibility.

## Package and methodology changes

- Methodology changes require corresponding evaluation or regression evidence.
- Methodology changes require an appropriate package version change.
- Keep packaging and documentation changes separate from methodology changes.
- Preserve provider neutrality where it applies, especially in RivetPay.
- Preserve each package's standalone installability and internal links.

## Publication hygiene

- Do not include private repository, customer, benchmark, credential, or environment data.
- Keep generated caches and temporary files out of commits.
- Preserve the package's existing validation and evidence boundaries.
- Root documentation may describe family responsibilities and release operations, but package SKILL.md files remain authoritative for individual behavior.
