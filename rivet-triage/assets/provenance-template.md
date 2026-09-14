# Provenance Audit

This audit accounts for every source finding and maps it to its final RivetTriage disposition.

## Artifact classification

| Artifact | Role | Revision/date | Notes |
|---|---|---|---|
| | `PRIMARY CURRENT INPUT` | | |
| | `HISTORICAL COMPARISON` | | |
| | `REMEDIATION/CLOSURE CONTEXT` | | |

## Source finding mapping

| Source artifact | Source ID | Source title | Evidence origin / lineage | Independence | Derived/shared origin | Final mapping | Relationship/disposition | Current-state status | Provenance | Notes |
|---|---|---|---|---|---|---|---|---|---|---|
| | | | | `INDEPENDENT / DERIVATIVE / SHARED ORIGIN / INDEPENDENCE UNKNOWN` | | `RT-001` | `EXACT DUPLICATE` | `CURRENT` | `KNOWN FROM OTHER REVIEW` | |

Every source finding must appear in this table at least once.

If one compound source finding is split, repeat it on multiple rows and map each row to the relevant `RT-*` ID.

Lineage is about the evidence supporting the claim, not file count. Copied, reformatted, summarized, quoted, and shared-origin artifacts remain accounted for but do not count as independent corroboration. Independent current verification may establish current state even when historical sources are derivative. Do not use lineage as a vote, and do not infer independence when it is unknown.

## Exact duplicate groups

### Group D-001

- Members:
- Canonical finding:
- Identity basis:
  - same operation:
  - same root mechanism:
  - same invariant:
  - same bad outcome:
  - one root-cause fix eliminates all:
- Verification performed:

## Partial overlaps

### Overlap O-001

- Findings:
- Shared mechanism/context:
- Why they remain distinct:
- Canonical mappings:

## Compound finding splits

### Split S-001

- Source finding:
- Original combined claim:
- Canonical findings produced:
- Why independent actionability requires a split:

## Historical comparison

| Canonical ID | Historical match | Historical source family | Prior remediation/closure context | Provenance decision | Basis |
|---|---|---|---|---|---|
| | | | | | |

## Rejected / non-current source candidates

| Source ID | Validity decision | Final disposition | Verification / gate basis | Canonical mapping |
|---|---|---|---|---|
| | | | | |

Use this table for every source candidate that is rejected, fixed, stale, unverified, or unresolved. State which validity-gate condition failed or remains unverified and retain the source mapping even when no `RT-*` finding is produced.

## Accounting check

- Total source findings:
- Total source findings represented in mapping:
- Silent omissions: **0**
- Accounting status: **PASS / FAIL**
