# RivetTriage v0.1.0

> Historical release note. This 0.1.0 description predates the current
> four-skill publication scope. Its earlier family references are historical
> context only and are not current dependencies or publication claims.

## Initial frozen methodology baseline

RivetTriage is the canonicalization and reconciliation stage between discovery
material and RivetClose remediation handoff.

The methodology was validated through internal repository benchmarks before
being frozen for this release. Benchmark artifacts are not packaged as
independently inspectable public evidence, and no benchmark findings or
project-specific confidential details are included here.

### Major capabilities

- Inventory and account for every source finding.
- Establish defect identity and classify exact duplicates, partial overlaps, related-distinct findings, independent findings, and unresolved relationships.
- Verify source-finding validity against current implementation, supported invariants, concrete behavior, controls, and reachability.
- Reconcile current-state status and provenance without treating historical conclusions as current proof.
- Assign canonical `RT-*` findings and reconcile severity from current reachable impact.
- Produce evidence-backed reports and explicit RivetClose handoff readiness.

### Boundaries

RivetTriage is not a new specialist review, broad scanner, remediation agent,
voting system, or replacement for discovery or closure skills. It does not
modify product code or other application artifacts, and it does not promote
incidental discovery into the canonical register.
