# RivetChaos Report Template

Use this template structurally; omit empty optional sections rather than filling them with generic text.

---

# [Persona or Summary Title]

## Scope

- Repository/revision:
- Persona/lens:
- Surfaces reviewed:
- Discovery-only confirmation: **No remediation performed**

## Executive assessment

Concise evidence-based assessment.

## Coverage

| Workflow / surface | Scenario | Outcome | Finding ID |
|---|---|---|---|
| ... | ... | FINDING / ALREADY RESILIENT / UNVERIFIED / NOT APPLICABLE | ... |

Use the coverage table to account for every important workflow/invariant identified in the review baseline. Each should have a conscious outcome; do not force a finding.

## Findings

### [CU/CR/CH/LA]-001 — [Short defect title]

- **Severity:** P0 / P1 / P2 / P3
- **Area:** [...]
- **Behavior attempted:** [...]
- **Why realistic:** [...]
- **Expected invariant:** [...]
- **Actual behavior:** [...]
- **Reproduction / trace path:** [...]
- **Evidence:** exact files, functions, constraints, tests, runtime observations
- **Reachability (optional):** actor, entry path, object/resource types, permissions, and normal/stale/crafted scope
- **Compensating controls (optional):** controls that bound exploitability, persistence, blast radius, cost, user impact, or recovery
- **Scope / blast radius (optional):** actual reachable actors/resources and practical impact
- **Impact:** [...]
- **Smallest remediation direction:** [...]
- **Verification criteria:** [...]
- **Overlap:** none / possible overlap with [...]
- **Status:** `NOT FIXED — DISCOVERY STAGE`
- **Prior status hint (optional):** `NEW` / `KNOWN` / `POSSIBLE REGRESSION` / `UNKNOWN`

## Already resilient attempts

### [Scenario title]

- **Behavior attempted:** [...]
- **Expected invariant:** [...]
- **Observed result:** `ALREADY RESILIENT`
- **Defenses/evidence:** [...]

## Unverified scenarios

### [Scenario title]

- **Why credible:** [...]
- **Evidence inspected:** [...]
- **Missing evidence:** [...]
- **Outcome:** `UNVERIFIED`

## Not applicable

Only include meaningful scenarios that were considered and rejected as irrelevant.

## Handoff notes

Record overlap clues for RivetTriage. Do not merge findings here. Include a prior status hint only when it is obvious from reports already read; do not perform a separate provenance audit.
