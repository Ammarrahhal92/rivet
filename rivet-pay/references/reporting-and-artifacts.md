# Reporting and Artifacts

This reference owns the structured artifact contract, discovery freeze, branch outcome ledger, deterministic finalization, report rendering, and consistency validation. Public Markdown is a projection of validated state, never an independent source.

## Working tree

```text
_rivetpay/
├── context.json
├── policy-contract.json
├── branches.json
├── manifest.json
├── active-freeze.json
├── candidates/RPC-###.json
├── judgments/RPC-###.json
├── coverage.json
└── final.json
history/GEN-####/
├── freeze.json
├── context.json
├── policy-contract.json
├── branches.json
├── candidates/
├── judgments/        (when present at reopen)
├── coverage.json     (when present at reopen)
├── final.json        (when present at reopen)
└── reopen.json       (when reopened)
docs/reviews/payments/
├── 00-rivet-pay-summary.md
├── authority-state-map.md
├── findings.md
└── coverage-and-defenses.md
```

The gate may create only `_rivetpay/` artifacts and the four fixed report paths below `docs/reviews/payments/`. All paths must pass containment checks.

## Artifact contracts

`context.json` and `policy-contract.json` contain facts, policy states, authorities, guarantees, contradictions, assumptions, unknowns, and open questions. They contain no final outcome, finding ID, severity, or remediation.

`branches.json` contains every material implementation-derived branch exactly once by branch ID. Each branch records family, predicate/control, condition, authority identity/state, lineage, candidate IDs, evidence questions, and materiality.

Each candidate has a unique `RPC-###` ID, source evidence, root cause, exact seed, hypothesis, target value, expected authority, invariant, preconditions, expansion axes, and branch IDs. It may not carry final severity.

Each judgment references one candidate and has exactly one status: `CONFIRMED`, `NEEDS_REVIEW`, `REJECTED`, or `DUPLICATE`. Only `CONFIRMED` may carry severity. Public IDs are generated from canonical candidate IDs at finalization. Duplicate judgments must point directly to a non-duplicate candidate.

A confirmed judgment is the canonical finding record for public semantics. It must contain non-placeholder target value, invariant, attack path, authority/grant source, realized unauthorized value, evidence basis, realized-value status, and complete value path. Finalization validates these fields before assigning a public ID; the renderer does not fill missing semantics with placeholders.

`coverage.json` contains generation/root bindings, exactly one row for every material branch, and exactly one outcome: `FINDING`, `DEFENDED`, `UNVERIFIED`, `NOT_APPLICABLE`, `INSUFFICIENT_EVIDENCE`, or `HARDENING_ONLY`. Every material branch structurally declares `family_id`, `authority_lineage`, and `lineage_sensitive`; lineage-sensitive groups cannot combine duplicate lineage classes. Family rows enumerate exact children and their status is derived, not trusted.

## Freeze

`freeze-discovery` hashes context, policy contract, branches, and every candidate in sorted relative-path order, copies them to `history/GEN-####/`, and stores a deterministic root hash over the generation ID, normalized paths, raw-byte hashes, and ID sets. `active-freeze.json` must equal the archived `freeze.json`; judgment validation uses and checks the archive. `reopen-discovery --reason ...` preserves the whole generation, writes `reopen.json`, removes active derived state, and starts a new generation in DISCOVERY. Validation fails if any archived or active frozen file changes, disappears, or is replaced under the same ID.

## Finalization rules

`finalize` requires every frozen candidate to have one generation/hash-bound judgment, every material branch to have exactly one coverage row, valid references, direct non-duplicate duplicate targets, lineage partitioning, policy/provider/runtime dependencies, and derived aggregate outcomes. Public IDs are assigned by candidate numeric order. It rejects missing judgments, changed candidates, orphan or duplicate public IDs, confirmed candidates without a finding branch, finding branches without a confirmed candidate, unresolved branches hidden by broad defense, and policy/provider/runtime dependencies that remain material and unresolved. Final state is regenerated and compared, never trusted as input.

Before finalization, the gate reconciles the canonical judgment, branch outcome, finding map, derived totals, and report projection. Non-confirmed, rejected, duplicate, or unresolved candidates cannot appear in `findings.md`; every public `RP-###` maps to exactly one confirmed canonical judgment. A suspicious intermediate condition without a realized commercial-value path remains non-confirmed.

Aggregate family status from material child branches. Any finding prevents broad `DEFENDED`; any unresolved child keeps the family `PARTIAL` or open; only all children `DEFENDED` or positively `NOT_APPLICABLE` allow broad closure. A narrow defense remains narrow.

The derived final verdict is `PASS`, `FINDINGS CONFIRMED`, `PARTIAL`, or `BLOCKED`. Counts and totals come from artifacts. Finalization fails on contradictions between ledger, coverage, judgments, findings, and summary.

## Rendering

Render only from `final.json`, context, policy, candidates, judgments, and coverage. `findings.md` includes only canonical confirmed candidates. The summary includes verdict, coverage, metadata, authority, totals, severities, unresolved limits, and confirmed findings. The authority map derives from context and policy. Coverage output includes every branch, outcome, defense, unresolved case, rejected candidate where useful, and limits.

Rendering the same unchanged state twice must produce byte-identical files. Manual edits to public reports are invalid; change structured artifacts and rerun the gate.
