---
name: rivet-close
description: "Controlled remediation and evidence-based closure for canonical READY software findings produced by RivetTriage. Repairs known defects, verifies restored invariants, and produces auditable closure evidence without broad rediscovery, deployment, or unrelated refactoring."
metadata:
  display-name: RivetClose
  version: "0.1.1"
  family: Rivet
---

# RivetClose

RivetClose is the remediation and closure stage of the Rivet review family.

```text
RivetChaos ─┐
            ├─→ RivetTriage ─→ RivetClose
RivetPay ───┘
```

It consumes canonical findings that RivetTriage marked ready for remediation, implements bounded fixes, verifies the exact restored invariant, and records auditable closure evidence.

RivetClose is not a discovery skill and is not a second triage pass.

## Core principles

> Fix the canonical defect, not the surrounding codebase.

> A code change is not closure; verified restoration of the invariant is closure.

> Never claim `CLOSED VERIFIED` when required evidence is missing.

## Invocation

```text
$rivet-close Close the ready findings in this repository.
```

## Authoritative inputs

Use the current RivetTriage canonical register as the authoritative defect input.

Preferred authority order:

1. `docs/reviews/triage/canonical-findings.md`
2. current implementation
3. repository contract/specification
4. source review findings for bounded reproduction/evidence context
5. historical remediation/closure material

Do not expand a canonical claim using discarded speculation from source reviews.

## Closure admission gate

Admit only canonical findings whose RivetTriage handoff is `READY`.

Do not remediate findings marked:

- `BLOCKED — CURRENT STATE UNVERIFIED`
- `BLOCKED — CONTRACT AMBIGUOUS`
- `BLOCKED — DUPLICATE RELATION UNRESOLVED`
- `BLOCKED — INSUFFICIENT EVIDENCE`

Classify those as `NOT ADMITTED — TRIAGE BLOCKED`.

If the user explicitly scopes the run to a subset of READY findings, mark the other READY findings `NOT ATTEMPTED`.

## Hard boundaries

RivetClose MUST NOT:

- perform broad independent discovery;
- rerun discovery/review skills internally;
- redo RivetTriage deduplication or provenance;
- change canonical severity or provenance;
- broaden a canonical claim because an older source finding was wider;
- refactor unrelated code;
- change unrelated dependencies;
- deploy to production unless explicitly requested;
- run production migrations unless explicitly requested;
- modify production data unless explicitly requested;
- rotate secrets or credentials unless explicitly requested;
- restart production services unless explicitly requested;
- change DNS, TLS, firewall, load-balancer, or host state unless explicitly requested;
- commit, push, reset, clean, checkout, or rewrite Git history unless explicitly requested;
- suppress tests merely to make the suite green.

If a new unrelated defect is noticed during remediation, record only an `OUT-OF-SCOPE DISCOVERY SIGNAL`. Do not assign it an RT id, severity, provenance, or remediation unless explicitly requested later.

## Implementation ownership

Use one write-owning orchestrator for implementation.

Optional bounded subagents may assist with:

- code-path tracing;
- test analysis;
- independent closure verification.

No competing implementation writers. No nested delegation. Maximum delegation depth: 1.

## Required output directory

Write closure artifacts under:

```text
docs/reviews/closure/
├── 00-rivet-close-summary.md
├── closure-register.md
├── verification-evidence.md
└── blocked-findings.md       # only when needed
```

Do not overwrite RivetTriage reports.

## Closure status vocabulary

Use only:

- `CLOSED VERIFIED`
- `FIXED — VERIFICATION INCOMPLETE`
- `PARTIALLY REMEDIATED`
- `NOT FIXED`
- `BLOCKED — ENVIRONMENT`
- `BLOCKED — CONTRACT`
- `BLOCKED — DEPENDENCY`
- `BLOCKED — TRIAGE CONTRADICTION`
- `NOT ATTEMPTED`
- `NOT ADMITTED — TRIAGE BLOCKED`

Do not invent synonyms such as `RESOLVED`, `DONE`, `MOSTLY FIXED`, or `CLOSED WITH CAVEATS`.

`FIXED` is not equivalent to `CLOSED VERIFIED`.

## Closure contract

Before changing code for each admitted finding, establish:

- Finding ID
- Canonical claim
- Invariant to restore
- Root cause
- Authoritative state or boundary
- Authoritative verification boundary
- Required control
- Non-goals
- Expected behavior after fix
- Regression risks
- Required verification

The closure contract constrains implementation scope.

## Repository baseline

Before remediation, establish a bounded baseline.

When Git is available, record:

- current revision;
- current branch;
- `git status`;
- pre-existing modifications.

Also record relevant tests, finding reproduction/evidence, configuration, and affected files/boundaries.

Never destroy or reset pre-existing user changes. Do not use destructive cleanup to obtain a clean tree.

## Pre-fix evidence

Before implementation, establish the canonical bad path when practical.

Classify the basis as one of:

- `REPRODUCED`
- `DETERMINISTICALLY ESTABLISHED`
- `NOT SAFELY REPRODUCIBLE`

Use `REPRODUCED` only when the exact defect was actually demonstrated.

Use `DETERMINISTICALLY ESTABLISHED` when current code/database/framework semantics directly establish the defect without needing an additional runtime demonstration.

Use `NOT SAFELY REPRODUCIBLE` when reproduction would require production mutation, real money, destructive data changes, unavailable hardware/provider state, unsafe load, or another prohibited action.

Never fabricate reproduction evidence.

## Minimal complete remediation

Prefer the smallest change that completely restores the canonical invariant.

Minimal does not mean smallest diff.

A remediation is complete only when:

1. the root cause is addressed;
2. the canonical bad behavior is prevented or safely recoverable;
3. the expected invariant is enforced.

Do not accept a symptom-only patch when the root mechanism remains reachable.

## Remediation classes

Use one or more high-level classes:

- `PREVENTIVE CONTROL`
- `TRANSACTIONAL / ATOMIC CONTROL`
- `RECOVERY CONTROL`
- `BOUNDARY ALIGNMENT`

These are implementation-planning labels, not finding taxonomy.

## Dependency-aware ordering

When multiple READY findings are in scope, determine whether they are:

- independent;
- implementation-dependent;
- shared-root;
- potentially conflicting.

Dependency order takes priority over RT number or severity.

One implementation change may support multiple findings, but every RT finding requires independent closure verification and status.

## Implementation rules

During remediation:

- preserve unrelated behavior;
- preserve public contracts except where the canonical finding requires correction;
- avoid opportunistic cleanup or dependency upgrades;
- add migrations only when required by the canonical defect;
- add/update tests to encode the corrected contract;
- do not weaken security, validation, idempotency, durability, or state checks merely to make tests pass.

If the fix unexpectedly becomes a broad architectural rewrite, stop and classify the finding appropriately rather than silently expanding scope.

## Anti-test-gaming rule

Do not claim remediation by:

- deleting the failing test;
- skipping/disabling the failing test;
- weakening assertions until broken behavior passes;
- mocking away the defective mechanism;
- bypassing authorization or middleware;
- swallowing the relevant exception;
- disabling validation;
- removing concurrency from a race test;
- changing expected output solely to match broken behavior.

A test may change when the canonical contract legitimately changes. Document why.

## Verification stack

### Layer 1 — Exact regression verification

Verify the exact canonical defect no longer occurs. Mandatory for `CLOSED VERIFIED`.

When the canonical claim describes runtime, user-visible, request, state-machine, retry, concurrency, lifecycle, or asynchronous behavior, exercise that behavior whenever practical. Static/source-contract assertions alone are insufficient for `CLOSED VERIFIED` merely because the expected code structure exists.

Static evidence may be sufficient only when the canonical claim is itself structural, or when the verified structure deterministically establishes the behavior with no material framework or runtime semantics left untested. If implementation is complete but only static evidence exists for a behavior-sensitive canonical claim, use `FIXED — VERIFICATION INCOMPLETE`. Do not force unsafe, destructive, production-only, real-money, or unavailable-hardware reproduction.

### Layer 2 — Invariant verification

Verify meaningful positive/negative cases around the restored invariant.

### Layer 3 — Relevant existing regression suite

Run the tests most likely to detect regression in the affected subsystem.

### Layer 4 — Broader repository validation

When practical, run appropriate broader validation such as full tests, lint, typecheck, build, or static analysis.

A full-suite pass alone does not replace Layer 1.

## Authoritative-path verification gate

The closure contract must identify the `Authoritative verification boundary`: the exact runtime, persistence, database, external-provider, infrastructure, or deployment path whose semantics determine the canonical claim.

A finding MUST NOT be classified `CLOSED VERIFIED` when the canonical claim or remediation materially depends on an authoritative path that was not actually verified, unless deterministic evidence directly proves that same authoritative path. An in-memory test does not verify changed PostgreSQL behavior; a provider mock does not verify provider-specific live behavior; and a repository configuration change does not prove deployed production state.

When implementation appears complete but authoritative-path verification is missing, use `FIXED — VERIFICATION INCOMPLETE`. If Triage explicitly narrowed the canonical claim to process-local or in-memory behavior, judge only that narrower boundary; unavailable PostgreSQL, multi-instance, or other excluded environment evidence does not block its closure.

## Closure evidence rule

A finding is `CLOSED VERIFIED` only when all are true:

1. root cause addressed;
2. canonical bad behavior no longer reachable on the verified path;
3. expected invariant demonstrated;
4. exact regression evidence passes;
5. relevant regression evidence passes or unrelated failures are clearly classified;
6. no known contradictory result remains;
7. required authoritative runtime, persistence, database, provider, infrastructure, deployment, migration, schema, or configuration state for the claimed closure is actually verified at the `Authoritative verification boundary`, or deterministic evidence directly proves that same path;
8. the fresh independent closure challenge is performed and finds no `DEMONSTRATED BYPASS` for the admitted mechanism.

If required evidence is missing, do not claim `CLOSED VERIFIED`.

If implementation appears complete but a behavior-sensitive claim has only static evidence, or the authoritative verification boundary is unavailable, classify it as `FIXED — VERIFICATION INCOMPLETE`. Do not over-block a claim that Triage explicitly narrowed to a verified process-local or structural boundary.

## Fix challenge

After the implementation and exact regression pass, challenge the same canonical mechanism.

Consider only relevant same-mechanism variants such as:

- alternate endpoint;
- alternate actor;
- replay;
- concurrency;
- retry;
- stale cache;
- background worker;
- alternate serializer;
- failed transaction;
- rollback;
- duplicate callback.

This is bounded closure verification, not broad discovery.

## Fresh independent closure challenge

After remediation and exact regression verification, and before finalizing a finding as `CLOSED VERIFIED`, perform a fresh read-only challenge of the current post-fix repository state.

Start from the admitted canonical finding and violated invariant, not from the remediation rationale. Ask:

> Given the admitted finding and the current post-fix repository state, can the same violated invariant still be reached through a materially equivalent supported path?

Where the environment supports an independent reviewer, prefer a fresh read-only reviewer or context that receives the canonical finding, invariant, current post-fix state, and permitted closure scope, but not the remediation author's justification, desired conclusion, or patch-defense reasoning.

If an isolated reviewer is unavailable, perform a logically separate fresh pass. Re-read the post-fix authoritative path, search for equivalent bypass paths, and do not treat earlier remediation reasoning as evidence. RivetClose remains usable without multi-agent capability.

Keep this challenge bounded to the admitted finding, its violated invariant, its authoritative mechanism, and material siblings or variants already within closure scope. Check relevant alternate entry points, equivalent representations, parser or normalization differences, retry/replay and concurrency variants, direct backend/API paths, stale enforcement paths, equivalent state transitions, and legitimate behavior that the repair may have broken. Stop when the concern becomes a different mechanism, subsystem, canonical finding, or general discovery.

Classify the result as one of:

- `DEMONSTRATED BYPASS`: current evidence proves the same invariant remains violable through a materially equivalent path. Do not finalize `CLOSED VERIFIED`; return to the existing repair and verification loop.
- `CREDIBLE BUT UNVERIFIED BYPASS`: a relevant concern exists but current evidence is insufficient. Apply existing incomplete-verification or blocking rules as appropriate; do not automatically call it a defect.
- `ALREADY RESILIENT / NO MATERIAL BYPASS`: inspected equivalent paths are closed or defended.
- `UNRELATED NEW ISSUE`: record only an `OUT-OF-SCOPE DISCOVERY SIGNAL`; do not expand the finding or block closure unless it actually contradicts the admitted repair.

Suspicion alone is not a veto. A bypass concern must have current evidence for the relevant path, reachability, mechanism, invariant, and consequence. This challenge is distinct from the existing fix challenge: the existing challenge tests whether the proposed remediation closes the known mechanism and bounded variants; this fresh challenge re-examines post-fix behavior without relying on the author's rationale. Do not turn either challenge into a second full review.

## Bounded sibling sweep

Inspect same-mechanism siblings only when they share the canonical authoritative boundary.

Examples:

- candidate-facing serializer used by incoming/detail/event;
- same authorization policy exposed through route aliases;
- same state transition invoked by HTTP and job paths.

Do not sweep the entire repository for similar code.

## Special verification rules

### Authorization

Verify as applicable:

- authorized actor succeeds;
- unauthorized actor is denied;
- cross-tenant actor is denied;
- public actor behavior matches the canonical public/private contract.

Adding middleware alone is not closure evidence.

### State machine

Verify:

- allowed transition succeeds;
- invalid transition is rejected;
- replayed/concurrent invalid transition remains rejected when relevant;
- authoritative final state is correct.

### Concurrency

A serial unit test alone does not close a concurrency finding.

Prefer parallel integration tests, deterministic interleaving, or direct lock/CAS/uniqueness proof at the authoritative state boundary.

### Idempotency

Verify as relevant:

- first operation;
- same-key replay;
- concurrent same-key replay;
- different-key independent operation;
- all material side effects such as notifications/outbox/events.

### Recovery

Verify:

- failure occurs or is simulated at the relevant boundary;
- state becomes actionable;
- retry/resume works;
- duplicate work is not introduced;
- normal success still works.

### Performance/resource findings

For structural findings, structural closure may be sufficient when the canonical claim is structural.

Do not invent quantitative improvement unless measured evidence is part of the closure requirement.

## Database and migration rules

RivetClose may author migrations or local/test schema changes when required.

Do not automatically run them against production, destructively backfill live data, delete live rows, or rewrite live history.

If repository code/migration is fixed but the required deployed schema is not in effect, closure must reflect that limitation.

## Infrastructure and deployment rules

Repository-level infrastructure/config fixes are allowed when part of a READY finding.

Do not automatically deploy, restart/reload production services, modify live Nginx/systemd/Supervisor/firewall, change DNS, rotate certificates, or rebuild hosts.

Repository changes alone are not live production closure when live state is required.

## External-provider rules

For payment, email, AI, OAuth, push, cloud storage, or other providers, use sandbox/test-mode/mocks/provider-contract evidence only when it exercises the canonical mechanism adequately.

Do not claim live closure from a mock when the defect depends on live provider behavior that remains unverified.

## Triage contradiction rule

If bounded remediation inspection establishes strong evidence that the canonical finding is materially invalid, already fixed, impossible under the current implementation, or based on a different mechanism than stated:

Do not silently re-triage it.

Classify `BLOCKED — TRIAGE CONTRADICTION` and record the contradictory evidence for RivetTriage reconsideration.

Do not alter provenance or severity.

## Out-of-scope discovery signals

When unrelated evidence appears during remediation, record only:

```text
OUT-OF-SCOPE DISCOVERY SIGNAL

Location:
Observation:
Why unrelated to admitted finding:
Recommended next review step:
```

Do not assign a canonical RT id or severity and do not remediate unless required for the admitted closure or explicitly requested.

## Regression risk

For each remediation, record:

- Behavioral regression risk: `LOW` / `MEDIUM` / `HIGH`
- Data migration risk: `LOW` / `MEDIUM` / `HIGH`
- Compatibility risk: `LOW` / `MEDIUM` / `HIGH`
- Concurrency risk: `LOW` / `MEDIUM` / `HIGH`
- Deployment risk: `LOW` / `MEDIUM` / `HIGH`
- Rollback complexity: `LOW` / `MEDIUM` / `HIGH`

Use concise evidence-based reasons. Do not create a numeric score.

## Test/build failure attribution

Classify failures as:

- `PRE-EXISTING FAILURE`
- `REMEDIATION-INTRODUCED FAILURE`
- `UNRELATED/UNRESOLVED`

Compare against the baseline when possible.

A remediation-introduced relevant failure prevents `CLOSED VERIFIED`.

## Diff review gate

Before final classification, review all RivetClose changes and confirm:

- every changed file maps to an admitted finding;
- no unrelated refactor was introduced;
- no debug/test bypass remains;
- no security/validation/control was weakened;
- no test was gamed;
- no source speculation was reintroduced;
- no production/deployment action occurred without explicit request.

## Closure status rules

### CLOSED VERIFIED

Implementation and all required closure evidence are complete.

### FIXED — VERIFICATION INCOMPLETE

Implementation appears complete but required verification is unavailable or incomplete. This is not closure.

### PARTIALLY REMEDIATED

Part of the canonical claim is addressed but the root defect or another canonical path remains.

### NOT FIXED

Attempted remediation failed, was reverted, or does not address the root cause.

### BLOCKED — ENVIRONMENT

Implementation or required verification depends on unavailable runtime, service, provider, hardware, credentials, database mode, or environment.

### BLOCKED — CONTRACT

Safe remediation requires a product/behavior decision not established by the canonical finding.

### BLOCKED — DEPENDENCY

Closure depends on another incomplete finding/control/migration/prerequisite.

### BLOCKED — TRIAGE CONTRADICTION

Current bounded evidence materially contradicts the canonical finding and it must return to RivetTriage.

### NOT ATTEMPTED

A READY finding was intentionally outside the requested remediation subset.

### NOT ADMITTED — TRIAGE BLOCKED

RivetTriage did not hand the finding off as `READY`.

## Atomic closure

Each canonical finding is closed independently.

Do not infer closure because another finding sharing the same code is closed, most tests passed, a shared patch exists, or reviewers agree.

## Report requirements

Use the templates under `assets/`.

### `00-rivet-close-summary.md`

Report repository/revision, input register, READY/admitted totals, closure totals, changed files, migration/deployment state, tests, broader suite status, production actions, commit/push status, and closure completeness.

### `closure-register.md`

For every relevant RT finding record original severity/provenance, pre-close status, closure status, canonical claim, closure contract, root cause, remediation, files changed, tests/evidence, fix challenge, residual risk, deployment/migration state, and final closure statement.

Do not reclassify severity or provenance.

### `verification-evidence.md`

Maintain a finding-oriented evidence ledger containing finding, verification layer/type, command/test/scenario, expected, observed, result, and notes.

### `blocked-findings.md`

Create only when at least one finding is not `CLOSED VERIFIED`.

Record status, completed work, missing evidence/work, why closure cannot be claimed, and required next step.

## Final execution algorithm

1. Establish repository baseline.
2. Locate the authoritative RivetTriage canonical register.
3. Admit `READY` findings only.
4. Respect any user-requested subset.
5. Build a closure contract for each admitted finding.
6. Identify dependencies/shared mechanisms.
7. Establish pre-fix reproduction or deterministic evidence.
8. Plan minimal complete remediation.
9. Implement through one write-owning orchestrator.
10. Add/update exact regression verification.
11. Run Layer 1 exact verification.
12. Run Layer 2 invariant verification.
13. Run bounded same-mechanism fix challenge.
14. Run the fresh independent closure challenge.
15. Run Layer 3 relevant regression suite.
16. Run Layer 4 broader validation where practical.
17. Attribute test/build failures.
18. Review the remediation diff for scope and anti-test-gaming violations.
19. Classify every relevant finding using the closed vocabulary.
20. Produce closure reports.
21. Stop without deployment, production mutation, commit, or push unless explicitly requested.

## Completion discipline

Do not end with a generic statement such as "all fixed" unless every admitted finding is `CLOSED VERIFIED`.

Always distinguish implementation complete, verification complete, and production/deployment state.

A remediation run is complete when every input finding is explicitly accounted for, even when some findings remain blocked or verification-incomplete.
