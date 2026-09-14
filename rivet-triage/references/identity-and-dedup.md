# Defect Identity and Deduplication Rules

## Purpose

This reference defines how RivetTriage decides whether source findings are the same defect, overlapping defects, or independent defects.

The unit of deduplication is the defect mechanism and violated behavior, not report wording.

## Defect Identity Fingerprint

Build a fingerprint for every candidate from:

1. **Operation/workflow**
2. **Actor/trigger**
3. **Violated invariant**
4. **Root mechanism**
5. **Authoritative state/boundary**
6. **Primary code path**
7. **Concrete bad outcome**
8. **Practical remediation class**

No single field is sufficient by itself.

## Closed relationship vocabulary

Use only:

- `EXACT DUPLICATE`
- `PARTIAL OVERLAP`
- `RELATED DISTINCT`
- `INDEPENDENT`
- `INSUFFICIENT EVIDENCE TO RELATE`

## Exact Duplicate Gate

Treat two findings as exact duplicates only when all material identity dimensions align.

Answer materially yes to:

1. Same operation or concrete operation boundary?
2. Same root defect mechanism?
3. Same violated invariant?
4. Same primary bad outcome?
5. Would one root-cause fix eliminate both?

If 5 is yes but 2–4 are not, use `PARTIAL OVERLAP` or `RELATED DISTINCT`.

### Likely exact duplicate

Security: a legacy endpoint lacks authentication.

Boundary: the same route is publicly mounted without its required guard.

Same route, same missing enforcement, same unauthorized access, same root fix.

### Not automatically duplicate

Reliability: an export record can remain stuck before dispatch.

Performance: the export worker can exhaust memory at the supported maximum.

Same workflow, different lifecycle phase and mechanism.

## Partial Overlap

Use when findings share a meaningful mechanism, lifecycle phase, state, or failure boundary but remain independently actionable.

Examples:

- uniqueness failure versus outer-transaction rollback caused by that failure;
- file creation before commit versus missing rollback/cleanup;
- missing authentication versus overly broad response content.

Do not merge merely to reduce count.

## Related Distinct

Use for separate defects in the same subsystem/workflow with independent root causes.

Example: synchronous import blocking and raw exception disclosure are both import defects but remain distinct.

## Independent

Use when shared context is incidental and there is no meaningful defect-identity relationship.

## Insufficient Evidence to Relate

Use when:

- source reports omit code path/mechanism;
- current path cannot be located;
- one source claim is too broad;
- the invariant cannot be distinguished;
- historical evidence is incomplete.

Do not force a relationship decision for cleaner output.

## Shared remediation is not identity

Two defects may both be improved by a transaction, pagination, authentication middleware, a queue, or an index. That does not make them duplicates.

Ask whether one root-cause fix eliminates the same violated behavior.

## Compound finding split

Split a source finding when it contains multiple independently actionable defects with distinct invariants, mechanisms, bad outcomes, or independently verifiable fixes.

### Split example

“Public endpoint has no authentication and returns raw provider stack traces.”

Possible canonicalization:

- missing authentication;
- diagnostic disclosure.

### Do not split example

“A check-then-insert uniqueness race throws a constraint violation and aborts the enclosing business transaction.”

The exception and rollback may be consequences of one race mechanism and one required conflict-safe write.

## Canonical claim construction

For exact duplicates:

1. prefer current implementation evidence over historical wording;
2. include only the narrowest fully supported claim;
3. preserve source-specific extra claims under `Differences reconciled`;
4. mark unsupported expansions;
5. preserve all source mappings.

Canonicalization intersects with evidence; it does not accumulate speculation.

## Source-accounting rules

Every source finding must map to one or more final dispositions:

- `RT-*` canonical finding;
- `UNRESOLVED-*` candidate;
- fixed/stale/historical disposition;
- explicit rejected/non-finding disposition supported by bounded verification;
- multiple `RT-*` findings after a compound split.

No silent dropping.

## Stable canonical IDs

Use `RT-001`, `RT-002`, ...

IDs identify the canonical register, not the source review family.

## Anti-patterns

Never deduplicate because:

- titles match;
- same file/class appears;
- severity matches;
- both say “race condition”;
- both involve the same subsystem;
- both recommend the same remediation;
- several reviewers agree.

Never refuse a duplicate because:

- specialists differ;
- wording differs;
- severities differ.

Identity is semantic and mechanism-based.
