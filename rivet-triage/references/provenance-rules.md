# Provenance Rules

## Purpose

Provenance describes where a canonical defect sits relative to prior review history.

It is separate from current-state status.

Examples:

- `CURRENT` + `KNOWN FROM OTHER REVIEW`
- `CURRENT` + `OLD SAME-FAMILY FINDING`
- `CURRENT` + `REOPENED DEFECT`
- `FIXED` + `HISTORICAL ONLY`
- `UNVERIFIED CURRENT STATE` + `INSUFFICIENT EVIDENCE`

## Closed provenance vocabulary

Use only:

- `GENUINELY NEW`
- `KNOWN FROM OTHER REVIEW`
- `OLD SAME-FAMILY FINDING`
- `POSSIBLE REGRESSION`
- `REOPENED DEFECT`
- `HISTORICAL ONLY`
- `INSUFFICIENT EVIDENCE`

## GENUINELY NEW

Assign when the canonical defect is current and no materially equivalent earlier finding is located in the relevant historical comparison set.

Do not claim global novelty beyond the artifacts actually available.

Prefer wording such as:

`GENUINELY NEW relative to the reviewed historical finding set.`

## KNOWN FROM OTHER REVIEW

Assign when a materially equivalent defect was previously identified by a different review stream/type and remains current.

## OLD SAME-FAMILY FINDING

Assign when a materially equivalent defect appeared in an older run of the same review family and remains current.

This is persistence, not regression.

## POSSIBLE REGRESSION

Require credible evidence of:

1. historical existence;
2. an intended remediation/closure/change;
3. current appearance again;

but insufficient evidence that the defect was actually absent in an intervening verified state.

## REOPENED DEFECT

Require all three:

1. historical existence;
2. verified absence after remediation;
3. current reappearance of the materially same defect.

A closure note saying “fixed” is insufficient for verified absence.

## HISTORICAL ONLY

Use when the candidate belongs to history but current state does not support an active canonical defect.

Typical pairings:

- `FIXED` + `HISTORICAL ONLY`
- `STALE` + `HISTORICAL ONLY`

## INSUFFICIENT EVIDENCE

Use when historical ordering, identity, remediation timing, or comparison coverage is too incomplete for a defensible provenance decision.

## Historical artifact handling

Historical artifacts may establish:

- someone previously reported a defect;
- a remediation intended to address it;
- revision/date ordering;
- prior verification evidence.

They do not automatically establish:

- current existence;
- actual repair;
- regression;
- unchanged severity.

## Provenance comparison method

For each canonical current defect:

1. search the defined historical comparison set;
2. compare defect fingerprints, not titles;
3. establish temporal order where possible;
4. inspect remediation/closure context only as needed;
5. use bounded verification to distinguish persistence from regression;
6. assign one provenance label.

## Multiple historical matches

Preserve all materially equivalent historical mappings but do not multiply canonical findings.

## Same-run duplicate versus historical provenance

Relationship and provenance are different.

Example:

Current `SEC-001` and `BOUND-002` are exact duplicates and become `RT-001`.

An older Chaos report already documented the same defect.

Then:

- relationship: `EXACT DUPLICATE`
- provenance: `KNOWN FROM OTHER REVIEW` or `OLD SAME-FAMILY FINDING`, depending on source family/history.

## Provenance audit expectations

For every source finding record:

- source artifact;
- source ID;
- evidence origin or lineage, when available;
- independence classification: `INDEPENDENT`, `DERIVATIVE`, `SHARED ORIGIN`, or `INDEPENDENCE UNKNOWN`;
- derivative/shared-origin relationship where known;
- mapped canonical ID(s) or unresolved disposition;
- relationship to other current sources;
- historical match if any;
- current-state status;
- provenance;
- split/merge/rejection notes.

The audit must make every source finding traceable to its final disposition.

## Evidence lineage and corroboration

Source count is not independent corroboration. A different filename, wording, format, report family, title, or source ID does not establish a separate evidentiary path.

Classify relevant evidence contributions as:

- `INDEPENDENT`: the claim was materially re-established through an independent current inspection, reproduction, test, runtime observation, or reviewer analysis;
- `DERIVATIVE`: the source copies, reformats, summarizes, quotes, or materially depends on a known source or evidence origin;
- `SHARED ORIGIN`: separate artifacts depend on the same scanner output, test result, trace, prior report, or other underlying evidence;
- `INDEPENDENCE UNKNOWN`: the available material cannot establish whether the contribution is independent or derivative.

Two files may have one lineage, and one file may contain multiple independent contributions. Preserve every derivative and shared-origin source in the accounting table and candidate mapping, but do not count it as independent corroboration. Do not assume independence or copying when lineage is unknown, and do not use lineage as a voting model. Current authoritative evidence remains controlling for current state, identity, severity, and contradictions. Lineage is separate from finding identity and does not create a multiple-source requirement for `READY`.
