---
name: rivet-pay
description: "Use for provider-neutral adversarial review of payment integrations, billing or subscription state, webhooks, refunds, cancellation or dunning, paid plans, seats, licenses, credits, quota, usage, and entitlement authority."
metadata:
  display-name: RivetPay
  version: "0.1.0"
  family: Rivet
---

# RivetPay

RivetPay performs discovery-only, provider-neutral adversarial review of commercial-value authority and enforcement. It is for repositories with payment, billing, grant, quota, license, seat, order, or entitlement behavior.

## Non-negotiable boundary

Default mode is `READ-ONLY / DISCOVERY-ONLY`.

- Review authorized repositories and controlled test systems only.
- Do not modify product code, tests, databases, deployment, provider infrastructure, or live customer state.
- Do not make purchases, refunds, chargebacks, webhook calls, secret rotations, or deployments.
- Create review artifacts only under the reviewed repository’s `_rivetpay/` directory and `docs/reviews/payments/`.
- Run only safe, explicitly authorized local or sandbox validation.
- Do not turn a review into remediation; hand confirmed findings to the remediation workflow.

## Core invariant

Commercial value must never exist, persist, increase, restore, or be consumed beyond the exact entitlement authorized by its authoritative grant source. Payment-backed value additionally requires the corresponding authoritative payment state.

Model value as:

```text
authority → evidence → interpretation → grant state → entitlement → enforcement → consumption
```

Keep entitlement and consumption separate. Classify grant sources rather than assuming every grant is provider-backed: payment-backed, trial, administrative, promotional, migration/legacy, or another explicit source.

## Outcomes

Every material branch receives exactly one outcome:

`FINDING`, `DEFENDED`, `UNVERIFIED`, `NOT APPLICABLE`, `INSUFFICIENT EVIDENCE`, or `HARDENING ONLY`.

Only a demonstrated current commercial-value invariant violation is a `FINDING`. `NOT APPLICABLE` requires positive contract or product-model evidence. Ambiguity is not permission to invent policy, authority, provider behavior, or a vulnerability.

## Runtime workflow

Use the bundled standard-library-only gate:

```text
python -X utf8 -B scripts/rivetpay_gate.py <command> --workdir <review-root>
```

The gate owns artifact validation, generation-bound freeze integrity, final aggregation, deterministic rendering, and status. The command sequence is:

### 0. Init / pre-flight

Run `init`. Record repository, branch, revision, dirty state, review mode, provider/grant model, and live-system scope in `_rivetpay/context.json`. Initialize `_rivetpay/policy-contract.json`, `branches.json`, `candidates/`, and `judgments/`.

Read [references/context-and-contract.md](references/context-and-contract.md). This phase records authority, value, states, predicates, product-policy evidence, provider-contract facts, contradictions, assumptions, guarantees, unknowns, and open questions. It emits no candidate, finding ID, severity, or remediation.

### 1. Context and contract

Produce only context and policy artifacts. Keep product policy separate from provider contract. Use explicit policy states such as `EXPLICIT`, `STRONGLY_RECONSTRUCTED`, `AMBIGUOUS`, and `UNSPECIFIED`. Do not use provider capability alone as local product intent.

Read [references/authority-and-lifecycle.md](references/authority-and-lifecycle.md) for the Value Authority Graph, grant authority, lifecycle, consumption, lineage, and supersession model.

Run `validate-context` before discovery.

### 2. High-recall discovery

Read [references/discovery-and-variants.md](references/discovery-and-variants.md). Write every plausible material candidate to `_rivetpay/candidates/RPC-###.json` and material predicate branch to `_rivetpay/branches.json`.

Discovery does not assign severity or final finding/false-positive judgment. A candidate may later be confirmed, rejected, marked `NEEDS_REVIEW`, or deduplicated, but it must never disappear silently.

### 3. Variant and branch expansion

For each material seed, record root cause and exact seed, then expand one meaningful axis at a time: identity/lineage, lifecycle, freshness, grant source, state, retry, concurrency, or enforcement. Explicitly invert security-bearing predicates and partition differing identities into `CURRENT`, `PRIOR / SUPERSEDED`, `GENUINELY NEW / NEVER-CURRENT`, and `UNKNOWN LINEAGE`.

Avoid Cartesian matrices. Stop and record the reason when further expansion is immaterial, impossible, or redundant. Update candidates and branches rather than replacing earlier evidence.

Run `validate-context` again if context or policy was revised, then `freeze-discovery`. Freeze creates an immutable logical `GEN-####` archive, hashes raw bytes, and records a deterministic generation root. Judgment validates against the archive, not a mutable active-freeze file. Do not proceed if frozen evidence changes or a frozen candidate is deleted.

If judgment discovers a genuinely new candidate, stop judgment and run `reopen-discovery --reason "<non-empty reason>"`. This archives the complete current generation, records the reason, clears active judgments/coverage/final state, returns to DISCOVERY, increments the generation, and requires fresh judgments for every candidate.

### 4. Independent judgment

Read [references/judgment-and-evidence.md](references/judgment-and-evidence.md). Judge every frozen candidate as an allegation using reopened source evidence, invariant, reachability, policy dependency, provider dependency, runtime dependency, lineage, compensating controls, and complete value path. A candidate is not a confirmed finding from a suspicious intermediate state alone: the canonical judgment must identify a concrete realized commercial-value consequence and a deterministic or reproduced path to it.

Write exactly one judgment per candidate under `_rivetpay/judgments/`. Judgment status is `CONFIRMED`, `NEEDS_REVIEW`, `REJECTED`, or `DUPLICATE`. Only `CONFIRMED` receives P0–P3 severity. Public `RP-###` IDs are generated at finalization from canonical `RPC-###` candidates; judgment never authors them. Every judgment, coverage record, and final state carries generation/root bindings, and confirmed judgments carry the frozen candidate hash. A blocked test is not automatically a blocker; runtime evidence is required only when materially necessary.

Run `validate-judgment`.

### 5. Branch coverage reconciliation

Write `_rivetpay/coverage.json` with exactly one row for every material branch. Each row records predicate, condition, authority identity/state, lineage, evidence, missing material evidence, and one RivetPay branch outcome.

Read [references/reporting-and-artifacts.md](references/reporting-and-artifacts.md). A branch cannot disappear because its candidate was rejected. Narrow defenses remain narrow. A family with any `FINDING` is not `DEFENDED`; a family with an unresolved material branch is `PARTIAL` or open.

### 6. Deterministic finalization

Run `finalize`. It verifies the freeze, judgment completeness, candidate finding semantics, realized-value evidence, branch coverage, candidate references, duplicate references, lineage partitioning, policy/provider/runtime dependencies, finding IDs, severity ordering, and aggregate outcomes. It derives `_rivetpay/final.json`; do not hand-author totals or verdicts.

The final verdict is `PASS` only when all material paths are closed without findings or unresolved material branches; `FINDINGS CONFIRMED` when a confirmed finding exists; `PARTIAL` when material evidence remains unresolved; and `BLOCKED` only when the baseline is too incomplete for meaningful review.

### 7. Render and validate

Run `render` only after `finalize`, then `validate`. Reports are generated from structured artifacts into `docs/reviews/payments/`:

```text
00-rivet-pay-summary.md
authority-state-map.md
findings.md
coverage-and-defenses.md
```

`findings.md` contains only canonical confirmed candidates. Render twice from unchanged artifacts and compare hashes when checking determinism. Run `status` last.

## Gates that must not be bypassed

- External-state applicability is determined from authoritative contract and product model, not missing handlers.
- Administrative grants require proof that the actor is outside intended authority; permission names are not contracts.
- Security-bearing predicates generate material branch obligations, including false branches and lineage partitions.
- Terminality does not erase supersession history; prior authority needs explicit re-authorization.
- Evidence Sufficiency distinguishes contract, application semantics, external authority, and runtime reproduction.
- Deterministic source proof can establish a finding without unnecessary runtime reproduction, but source suspicion alone cannot.
- Finding Admission requires value, authority/invariant, reachable or deterministic path, current mechanism, challenged controls, unauthorized consequence, and justified severity.
- Outcome Consistency reconciles every branch, family, finding, coverage total, and final verdict before rendering.

Reject rationalizations such as “the test could not run, so no source finding exists,” “the provider supports it, so the product policy is obvious,” “one defended example closes the family,” “a different ID is necessarily new,” or “the summary can be counted separately.”

## Direct reference ownership

- [Context and contract](references/context-and-contract.md) — context-only facts, policy, provider contract, contradictions, and unknowns.
- [Authority and lifecycle](references/authority-and-lifecycle.md) — authority graph, invariants, state, consumption, lineage, and supersession.
- [Discovery and variants](references/discovery-and-variants.md) — high-recall candidates, predicates, branch expansion, and candidate persistence.
- [Judgment and evidence](references/judgment-and-evidence.md) — independent judgment, evidence sufficiency, finding admission, and severity.
- [Reporting and artifacts](references/reporting-and-artifacts.md) — artifact schemas, freeze, branch outcomes, finalization, validation, and rendering.
- [SPEC.md](SPEC.md) — maintenance and release contract.
- [SOURCES.md](SOURCES.md) — maintainer source and decision inventory.

## Completion conditions

A review is complete only after:

- context and policy artifacts preserve contradictions and unknowns;
- every candidate survives discovery freeze and receives judgment;
- every material implementation-derived branch receives an outcome;
- lineage classes are not merged when authorization semantics differ;
- confirmed findings satisfy the evidence matrix and receive severity only after confirmation;
- final aggregates reconcile with branch and judgment artifacts;
- deterministic validation passes before rendering;
- rendered reports match final structured state.

Do not benchmark, deploy, remediate, contact providers, or modify application code as part of this skill’s default workflow.
