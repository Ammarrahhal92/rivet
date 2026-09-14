# Remediation Rules

This reference governs how RivetClose changes implementation for canonical READY findings.

## Canonical scope

The RivetTriage canonical finding defines the remediation claim. Do not broaden the defect from source-review wording and do not repair unrelated code simply because it is nearby.

## Minimal complete fix

Prefer the smallest implementation change that fully restores the canonical invariant.

A complete fix must:

1. remove or neutralize the root cause;
2. prevent or safely recover the canonical bad state;
3. preserve legitimate behavior.

A one-line patch is not inherently better than a multi-file fix. A broad rewrite is not inherently safer than a bounded control.

## Closure contract

Before implementation, identify:

- canonical claim;
- invariant;
- root mechanism;
- authoritative state/boundary;
- required control;
- non-goals;
- expected post-fix behavior;
- regression risks;
- verification plan.

If these cannot be determined from READY triage evidence, stop rather than inventing product policy.

## Remediation classes

### PREVENTIVE CONTROL

Examples: strict validation, authorization policy, state precondition, rate/admission limit, uniqueness constraint.

### TRANSACTIONAL / ATOMIC CONTROL

Examples: transaction, lock, compare-and-set, optimistic version condition, idempotency boundary, outbox.

### RECOVERY CONTROL

Examples: retry/resume, reconciliation, failure state, cleanup/watchdog, compensating action.

### BOUNDARY ALIGNMENT

Examples: timeout alignment, API contract correction, serializer separation, CORS policy correction, lifecycle ownership clarification.

## Shared implementation

One implementation may support several canonical findings. Do not merge finding identity during remediation. Verify each finding independently.

## Dependency ordering

Order implementation by technical dependency, not RT number or severity.

Examples:

- establish authoritative state transition before adding recovery;
- add durable idempotency before exactly-once side effects;
- add schema invariant before application-level assumptions.

## Existing changes

Never destroy user modifications. Record pre-existing changes and distinguish them from RivetClose changes. Do not use destructive Git cleanup operations.

## Refactoring

Refactoring is permitted only when needed to implement the canonical fix safely.

A remediation may extract a shared function or policy when the same defective mechanism has multiple canonical paths or correct enforcement requires one authoritative boundary.

Avoid style-only cleanup, renames, dependency churn, or architecture changes unrelated to closure.

## Tests

Add/update tests to encode the corrected contract.

Do not remove failing coverage, skip the scenario, weaken assertions, replace real control testing with mocks that bypass the mechanism, make a race serial, or change expected behavior solely to match the pre-fix implementation.

## Migrations

RivetClose may author repository migrations.

Do not run them against production unless explicitly requested.

Distinguish migration authored, migration exercised in local/test environment, and production migration not run.

## External systems

Use test/sandbox integration when it exercises the same contract. Mocks are acceptable for local code behavior, but not as proof of external live behavior when the canonical finding depends on provider runtime semantics.

## Stop conditions

Stop or block instead of improvising when:

- contract is ambiguous;
- production-only destructive operation is required;
- credentials/secrets are required and unavailable;
- the fix unexpectedly requires a broad rewrite;
- another unresolved finding is a prerequisite;
- bounded current evidence contradicts the triaged canonical defect.

## Out-of-scope discovery

An unrelated newly observed issue is not a remediation target. Record an out-of-scope signal only. Do not assign severity, provenance, or RT id.

## Diff discipline

Every changed file must map to an admitted finding.

Before finalizing:

- remove only RivetClose-introduced unrelated changes;
- preserve pre-existing changes;
- confirm no temporary debug code remains;
- confirm no control has been weakened.
