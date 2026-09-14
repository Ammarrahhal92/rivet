# RivetPay Maintenance Contract

## Intent

RivetPay is a provider-neutral, discovery-only specialist for adversarial review of payment, billing, grant, quota, license, seat, order, and entitlement authority. It reconstructs commercial value and preserves plausible candidates until independent judgment.

## Scope

Review authorized application repositories and controlled test systems. Trace authority, evidence, interpretation, grant state, entitlement, enforcement, and consumption. Provider infrastructure, production mutation, real purchases, and remediation are outside the default scope.

## Non-goals

RivetPay does not deploy, contact providers, attack live systems, modify product code, decide product policy from provider capability alone, or claim that missing tests prove safety or vulnerability.

## Trigger context

Use for payment integration, billing/subscription, webhook, refund, cancellation, dunning, paid plan, seat, license, credit, quota, usage, and entitlement reviews.

## Runtime architecture

The workflow is staged:

```text
context → discovery → variants → freeze (GEN-####) → judgment → coverage → finalize → render → validate
```

`SKILL.md` orchestrates. `scripts/rivetpay_gate.py` validates and renders. Structured `_rivetpay/` artifacts are the source of truth for public reports.

## Phase ownership

- context and product/provider contract: `references/context-and-contract.md`;
- authority, invariants, lifecycle, consumption, and lineage: `references/authority-and-lifecycle.md`;
- discovery, predicates, candidates, and variants: `references/discovery-and-variants.md`;
- judgment, evidence, finding admission, and severity: `references/judgment-and-evidence.md`;
- artifact schemas, freeze, aggregation, rendering, and consistency: `references/reporting-and-artifacts.md`;
- orchestration and boundaries: `SKILL.md`;
- deterministic implementation and tests: `scripts/rivetpay_gate.py` and `scripts/test_rivetpay_gate.py`;
- maintenance/evaluation contract: this file;
- source provenance: `SOURCES.md`.

One authoritative owner exists for each behavioral rule. Other files may route to an owner but must not create competing definitions.

## Source and evidence model

Context separates product-policy evidence from external/provider contract facts. Discovery is high-recall and does not assign severity. Judgment reopens source evidence and treats every candidate as an allegation. Runtime evidence is required only when materially necessary; deterministic source proof can establish a finding without unnecessary reproduction.

## Candidate persistence invariant

Every written candidate survives discovery freeze. It may become confirmed, rejected, needs-review, or duplicate, but it is never silently deleted. Frozen context, policy, branches, and candidates are hash-checked before judgment.

## Discovery/judgment trust boundary

Judgment may not silently rewrite discovery evidence. It must reference frozen candidates and record its own status. Duplicate judgments retain the duplicate candidate and point to a canonical candidate.

## Deterministic tooling contract

The gate uses only the Python standard library. It validates JSON, IDs, schemas, containment, freeze hashes, judgment completeness, branch outcomes, aggregate family rules, finding references, final totals, and report projections. It emits no application review and does not invoke an AI model.

Commands:

```text
init
validate-context
freeze-discovery
reopen-discovery --reason "..."
validate-judgment
finalize
render
validate
status
validate-regression-corpus
```

Reports may be written only under `docs/reviews/payments/`; artifacts may be written only under `_rivetpay/` in the review root.

### Generation and reopen contract

Each freeze creates a monotonically numbered generation with an archived raw-byte snapshot and deterministic root hash. `reopen-discovery` is the only supported transition from FROZEN, JUDGMENT, or FINALIZED back to DISCOVERY. It requires a non-empty reason, archives prior judgments/coverage/final state when present, preserves the prior snapshot, clears active derived state, and requires fresh judgments for the new generation. Generation, candidate, and root bindings are mechanically checked; editing active freeze metadata cannot legitimize changed archived evidence.

## Output contract

The four public reports are deterministic projections of `final.json`, context, policy, candidates, judgments, and coverage. `findings.md` contains only confirmed canonical findings. Totals and verdicts are derived, never manually counted.

## Evaluation strategy

The 210 methodology evals remain in `evals/evals.json`. Behavioral regression cases live in `evals/regression-cases.json` and use minimal synthetic provider-neutral fixtures. The corpus validator checks structure and safety only; future fresh-agent runs provide behavioral evidence.

## Release and freeze criteria

Version 0.1.0 is release-ready and is the intended initial public release; it has not yet been published by this task. A passing validator, valid eval JSON, or one benchmark does not establish behavioral stability. Before publication, run critical regression fixtures in fresh contexts with repeated independent runs, require positive recall and negative precision, require structured validation and deterministic reports, and review policy, lineage, refund-restoration, and wrong-authority controls.

## Known limitations

The gate validates structured evidence and deterministic relationships; it does not prove that a reviewer discovered every candidate or that an external contract is correct. It cannot establish deployment configuration, provider frequency, nondeterministic scheduling, or unavailable database behavior. Those remain explicit evidence limits.

## Maintenance rules

- preserve provider neutrality and synthetic fixture names;
- keep discovery-only safety boundaries;
- preserve one owner per rule;
- update structured schemas and tests together;
- preserve existing methodology evals unless incompatibility is demonstrated;
- do not add release engineering, application code, or third-party dependencies;
- rerun unit, corpus, structural, freeze, render, and parity validation after changes;
- do not bump version until behavioral benchmarking proves the architecture stable.
