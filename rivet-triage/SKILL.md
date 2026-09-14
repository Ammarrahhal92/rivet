---
name: rivet-triage
description: "Discovery-following triage and reconciliation for software review findings. Normalizes findings from RivetChaos, RivetPay, and other explicit review artifacts; determines defect identity, duplicates, overlaps, provenance, current-state status, canonical severity, and RivetClose handoff readiness without remediation or broad new discovery."
metadata:
  display-name: RivetTriage
  version: "0.1.1"
  family: Rivet
---

# RivetTriage

RivetTriage is the canonicalization and reconciliation stage of the Rivet family. It operates after discovery, accepts findings from RivetChaos, RivetPay, other explicit reviews, and relevant historical/remediation/closure artifacts, and produces one evidence-backed canonical register for RivetClose.

The current publication scope contains exactly four family members:

```text
RivetChaos / RivetPay → RivetTriage → RivetClose
```

Chaos and Pay are independent discovery/review producers. RivetTriage owns
family-level canonical identity and deduplication; RivetClose consumes its
canonical READY handoff.

It does not perform broad independent discovery and does not remediate product code.

## Core pipeline

`Normalize → Establish defect identity → Relate / deduplicate → Resolve disputed questions → Determine current state → Determine provenance → Reconcile severity → Produce canonical register`

Governing principles:

1. Every source finding must be accounted for.
2. Similar wording does not establish duplicate identity.
3. Historical conclusions provide context; current evidence decides current state.
4. Verification is question-scoped, not discovery-scoped.
5. Canonicalization may merge, split, preserve, or decompose source findings.
6. Incidental new discovery is never promoted into the canonical register.

Read:
- [references/identity-and-dedup.md](references/identity-and-dedup.md)
- [references/provenance-rules.md](references/provenance-rules.md)
- [references/verification-rules.md](references/verification-rules.md)

## Supported inputs

Primary current inputs may include RivetChaos reports, RivetPay reports, another explicit review system, or issue/audit documents intentionally supplied as current review inputs.

Historical comparison/context may include older review rounds, prior audits, remediation reports, closure reports, issue history, defect ledgers, and deployment/remediation evidence.

Classify artifacts before use:

- `PRIMARY CURRENT INPUT`
- `HISTORICAL COMPARISON`
- `REMEDIATION/CLOSURE CONTEXT`
- `NON-FINDING REVIEW MATERIAL`

Do not treat every file under a reviews directory as a finding source.

## Scope gate

Determine whether meaningful triage work exists. A single finding from one current report may still be normalized, but do not manufacture duplicate or provenance complexity where none exists. If inputs are too incomplete to identify or compare findings meaningfully, report the limitation.

## Hard boundaries

RivetTriage must not:

- perform broad new defect discovery;
- rerun discovery/review skills internally;
- modify product/application code, configuration, migrations, tests, infrastructure, deployment files, or data;
- remediate findings;
- suppress a source finding without accounting for it;
- use reviewer voting;
- merge findings because they share a subsystem, title, topic, severity, or remediation direction;
- declare `FIXED` solely because a historical report says closed/resolved/remediated/deployed;
- use historical findings as current implementation evidence;
- promote incidental new defects found during verification into `RT-*` findings.

If an unrelated defect is noticed while resolving a triage question, optionally record `OUT-OF-SCOPE DISCOVERY SIGNAL` and recommend a separate discovery review.

## Step 1 — Inventory and normalize source findings

For each source finding capture, when available:

- source artifact and review family/type;
- source finding ID/title/severity/outcome/status;
- claimed invariant;
- actor or trigger;
- operation/workflow;
- root mechanism;
- authoritative state or boundary affected;
- code path/evidence;
- concrete bad behavior/state;
- reachability/preconditions;
- impact;
- remediation direction;
- source revision/baseline;
- evidence origin/lineage for the claim, when available;
- independence classification: `INDEPENDENT`, `DERIVATIVE`, `SHARED ORIGIN`, or `INDEPENDENCE UNKNOWN`.

Do not silently repair missing source evidence. Record unknown fields as unknown.

Every source finding must later map to one or more of:

- a canonical finding;
- multiple canonical findings after a justified split;
- an unresolved candidate;
- a historical-only/fixed/stale disposition;
- an explicit rejected/non-finding disposition supported by bounded current verification.

## Step 2 — Build Defect Identity Fingerprints

For each candidate build a semantic fingerprint from:

1. operation/workflow;
2. actor/trigger;
3. violated invariant;
4. root mechanism;
5. authoritative state/boundary affected;
6. primary code path;
7. concrete bad outcome;
8. practical remediation class.

Titles, severity labels, specialist names, and wording are not identity.

## Step 3 — Classify relationships

Use only:

- `EXACT DUPLICATE`
- `PARTIAL OVERLAP`
- `RELATED DISTINCT`
- `INDEPENDENT`
- `INSUFFICIENT EVIDENCE TO RELATE`

### Exact duplicate gate

Classify `EXACT DUPLICATE` only when findings materially share:

- the same operation;
- the same root mechanism;
- the same violated invariant;
- the same concrete bad outcome;

and one root-cause fix would eliminate both.

Shared remediation direction alone is insufficient.

### Partial overlap

Use when findings share a mechanism, lifecycle phase, state, or failure boundary but differ materially in invariant, bad outcome, or necessary remediation. Do not merge merely to reduce count.

### Related distinct

Use for separate defects in the same workflow/subsystem that remain independently actionable.

### Independent

Use when no meaningful defect-identity relationship exists.

### Insufficient evidence to relate

Use when source/current evidence cannot support a defensible relationship decision.

## Step 4 — Split compound findings

One source finding may contain multiple independent defects. Split when distinct violated invariants or root mechanisms require independently testable remediation.

Do not split multiple consequences of the same root mechanism merely because the report lists several effects.

## Step 5 — Canonicalize conservatively

Canonicalization is evidence reconciliation, not claim accumulation.

Before a source `FINDING` may be admitted as a `CURRENT` canonical `RT-*` finding, apply the source-finding validity gate below. Upstream authority, agreement between sources, a superficially present mechanism, or absence of a preferred control is not enough.

### Source-finding validity gate

Independently establish all of the following for the current supported operation before admitting the finding as `CURRENT`:

- **A — implementation condition:** the claimed implementation condition exists in the current code, configuration, schema, runtime registration, or other authoritative current evidence;
- **B — violated invariant:** the condition violates a current supported product, API, data, security, lifecycle, or operational invariant;
- **C — concrete behavior:** the condition produces the concrete undesirable behavior claimed by the source, not merely a code smell or architectural preference;
- **D — controls:** framework, runtime, database, queue, transaction, retry, redelivery, or other mandatory controls do not already prevent or recover the claimed defect on the reachable path;
- **E — reachability:** the operation and preconditions are reachable under current supported repository/runtime assumptions required for the claim.

Use current evidence to decide the gate. Historical validity audits, remediation reports, and prior validators are leads or comparison context only. A source candidate that fails or cannot pass the gate must not become a `CURRENT` canonical finding. Preserve its source accounting and assign the supported disposition, such as rejected/non-finding with an explicit reason, `FIXED`, `STALE`, `UNVERIFIED CURRENT STATE`, or an unresolved candidate.

Apply the gate explicitly when:

- a source claims missing create/dispatch atomicity: inspect actual framework and queue semantics, including transaction coupling and failure recovery; a missing local transaction or preferred pattern does not prove the claimed bad outcome;
- a source claims missing cleanup or reconciliation: inspect retry, redelivery, acknowledgement, dead-letter, and failure semantics before declaring work stuck; existing queue recovery may invalidate the claim;
- a source points only to the absence of a preferred control: identify the invariant and concrete bad behavior independently; control absence alone is not a finding.

Architectural preference remains insufficient to establish validity. If evidence supports only the condition but not the violated invariant, concrete behavior, controls analysis, or reachability, keep the candidate non-current and record what remains unverified.

For an exact-duplicate group:

- preserve every source mapping;
- use the strongest current evidence available;
- narrow the canonical claim to what current evidence supports;
- retain source-specific differences in reconciliation notes;
- do not union unsupported claims.

Canonicalization may produce many→one, one→many, many→many, or one→one mappings.

## Step 6 — Question-scoped verification

Current repository inspection is allowed only to answer concrete triage questions, such as whether two findings share the same mechanism, whether a claimed control really prevents the defect, whether a historical defect still exists, whether it was demonstrably absent after remediation, whether a path remains reachable, whether a compound finding should split, or what current impact supports severity.

Do not expand verification into broad discovery.

Follow [references/verification-rules.md](references/verification-rules.md).

## Step 7 — Resolve finding-vs-resilient conflicts

When one source says `FINDING` and another says `ALREADY RESILIENT`, do not vote. Identify the exact disputed control and determine whether it covers the same operation, authoritative state, lifecycle phase, failure mode, and reachable path.

Internal resolution may be:

- `FINDING SURVIVES`
- `CONTROL INVALIDATES FINDING`
- `CURRENT STATE UNVERIFIED`

These are reconciliation results, not canonical current-state labels.

## Step 8 — Determine current-state status

Current-state status is separate from provenance.

Use only:

- `CURRENT`
- `FIXED`
- `STALE`
- `UNVERIFIED CURRENT STATE`
- `SUPERSEDED`

`CURRENT` means current implementation evidence supports the defect now.

`FIXED` requires current verification that the defect mechanism/violated behavior is no longer present.

`STALE` means the source relies on a no-longer-current path, operation, configuration, or contract without enough evidence to characterize it as a verified remediation.

`UNVERIFIED CURRENT STATE` means current state cannot be established sufficiently.

`SUPERSEDED` means the source representation was replaced by a better canonical merge/decomposition; it is not a synonym for fixed.

## Step 9 — Determine provenance

Use only:

- `GENUINELY NEW`
- `KNOWN FROM OTHER REVIEW`
- `OLD SAME-FAMILY FINDING`
- `POSSIBLE REGRESSION`
- `REOPENED DEFECT`
- `HISTORICAL ONLY`
- `INSUFFICIENT EVIDENCE`

Follow [references/provenance-rules.md](references/provenance-rules.md). Do not infer provenance from title similarity.

### Evidence lineage and independent corroboration

Source count is not independent corroboration. Multiple artifacts may carry one evidentiary lineage, including copied, reformatted, summarized, quoted, or scanner-derived reports. Record the evidence origin and classify each relevant evidence contribution as:

- `INDEPENDENT` when the claim was materially re-established through an independent evidentiary path;
- `DERIVATIVE` when it copies, reformats, summarizes, quotes, or materially depends on another known source or evidence origin;
- `SHARED ORIGIN` when separate artifacts depend on the same scanner output, test result, trace, or other underlying evidence;
- `INDEPENDENCE UNKNOWN` when available material cannot establish independence or derivation.

Do not force certainty. Preserve derivative and shared-origin sources in source accounting and provenance, but do not count them as independent corroboration. Different files do not create independence, and one file may contain multiple independent evidence contributions. Independent corroboration may strengthen confidence in a currently supported finding, but source count does not establish existence, current state, identity, severity, or resolution of authoritative contradictions. Current authoritative evidence still controls those decisions.

Lineage is separate from finding identity: derivative sources may describe distinct findings, and independent sources may describe one exact duplicate. Lineage also does not change severity or require multiple independent sources for `READY`.

## Step 10 — Reconcile severity

Source severities are inputs, not votes.

Use the shared Rivet P0–P3 scale:

- `P0` catastrophic/system-wide failure;
- `P1` severe failure with substantial blast radius or difficult recovery;
- `P2` material state, security, privacy, lifecycle, operational, or resource defect;
- `P3` real but bounded defect with narrow scope, capped impact, straightforward recovery, or limited operational/UX consequence.

Assign canonical severity from current reachable impact after controls. Record source severities, canonical severity, and reason for material differences.

For `CURRENT` canonical findings, default a real bounded defect to `P3`. `P2` requires independent evidence of material impact, such as:

- material per-instance security, privacy, state, or lifecycle harm;
- deterministic supported-operation failure with materially significant consequence;
- durable data corruption or loss;
- meaningful authorization or trust-boundary violation;
- demonstrated or strongly supported operational/resource impact beyond a bounded inefficiency.

Do not assign `P2` merely because the defect affects a core workflow, can grow with usage, was found by multiple reviewers, has unknown production magnitude, involves AI/provider/resource usage, is architectural, or affects an important feature. For performance/resource findings, deterministic structural inefficiency may remain a real `P3`; absent measurements or supported-limit failure generally prevents amplification to `P2` when the impact is only latency, memory, query, token, or cost growth. Quantitative uncertainty affects severity amplification, not defect validity.

Examples: duplicate or unpaginated per-user reads without measured severe impact are usually `P3`; unbounded input before expensive provider work with unknown magnitude is usually `P3`; material unauthenticated disclosure of user-owned data may be `P2`; deterministic transaction rollback or data corruption may be `P2`; a workflow blocked while failing closed is `P3`. Do not lower a real material defect merely because it is bounded to one user or record.

Do not inflate severity because multiple reviewers found the same defect. Do not lower severity because a defect was previously known.

## Step 11 — Assign canonical IDs

Use `RT-001`, `RT-002`, `RT-003`, ...

Do not reuse source IDs as canonical IDs. Preserve all source IDs in mappings.

## Step 12 — Determine RivetClose readiness

For current canonical findings assign exactly one:

- `READY`
- `BLOCKED — CURRENT STATE UNVERIFIED`
- `BLOCKED — CONTRACT AMBIGUOUS`
- `BLOCKED — DUPLICATE RELATION UNRESOLVED`
- `BLOCKED — INSUFFICIENT EVIDENCE`

`READY` means the canonical finding is sufficiently identified and evidenced for RivetClose. RivetClose should default to `READY` findings only.

## Canonical finding schema

Each `RT-*` finding should include:

- ID/title;
- current-state status;
- canonical severity;
- provenance;
- canonical claim;
- source-finding validity decision and basis;
- expected invariant and invariant basis;
- current mechanism/evidence;
- reachability/preconditions;
- compensating controls;
- scope/blast radius;
- impact;
- severity basis, including the independent evidence required for any `P2` or higher classification;
- source findings;
- evidence lineage/independence conclusion where relevant (detailed mappings belong in the provenance audit);
- relationship classification;
- differences reconciled;
- historical context where relevant;
- current-state verification;
- remediation class/direction;
- RivetClose handoff state;
- status `NOT FIXED — TRIAGED` for current unresolved defects.

Do not write detailed implementation steps; RivetClose owns remediation.

## Reports

Write under `docs/reviews/triage/`.

Required:

- `00-rivet-triage-summary.md`
- `canonical-findings.md`
- `provenance-audit.md`

Conditional:

- `unresolved-candidates.md` only when unresolved candidates exist.

Use the templates under `assets/`.

## Summary requirements

Report:

- repository/revision or current-tree basis;
- current input artifacts;
- historical/context artifacts;
- source finding count;
- canonical current finding count;
- exact-duplicate groups;
- split compound findings;
- partial overlaps;
- current-state totals;
- provenance totals;
- severity totals for current canonical findings;
- RivetClose-ready count;
- blocked/unresolved count;
- no-remediation confirmation;
- explicit statement that every source finding was accounted for.

## Completion gates

Do not finish until all applicable checks pass:

- [ ] Input artifacts classified by role.
- [ ] Every source finding inventoried and accounted for.
- [ ] Every canonical finding maps to at least one source finding.
- [ ] Exact duplicates are based on defect identity, not wording/title/topic.
- [ ] No exact duplicate remains duplicated without an explicit unresolved reason.
- [ ] Partial overlaps and related-distinct defects were not incorrectly merged.
- [ ] Compound source findings were split when independently actionable defects were combined.
- [ ] Canonical claims were narrowed to supported evidence.
- [ ] Every source `FINDING` admitted as `CURRENT` passed validity checks for implementation condition, invariant, concrete behavior, controls, and reachability.
- [ ] Rejected or non-current source findings retained explicit dispositions and source accounting.
- [ ] Historical closure/remediation prose was not used alone to declare `FIXED`.
- [ ] Current-state status and provenance were treated separately.
- [ ] Severity was reconciled from current impact, not voting.
- [ ] `P3` was the default for bounded current defects; any `P2` or higher severity has independent material-impact basis.
- [ ] No incidental new discovery was promoted into the canonical register.
- [ ] No remediation/product modification occurred.
- [ ] Every current canonical finding has a RivetClose handoff state.
- [ ] Required reports exist; unresolved report exists only when needed.
- [ ] Summary confirms source-accounting completeness.

## Execution model

Use one orchestrating reasoning pass with full visibility of all triage inputs.

Subagents are optional only for large artifact sets and must be restricted to bounded normalization, evidence extraction, or historical comparison. Final identity/provenance decisions remain with the orchestrator. No nested delegation.

## Non-goals

RivetTriage is not a new specialist review, scanner, remediation agent, provenance-by-Git-history system, test generator, voting system, generic issue tracker, or replacement for discovery or closure skills.
