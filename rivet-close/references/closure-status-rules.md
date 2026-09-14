# Closure Status Rules

Use the following vocabulary exactly.

## CLOSED VERIFIED

Use only when implementation is complete, exact canonical regression verification passes, behavior is exercised when the claim is behavior-sensitive, invariant verification passes, relevant regressions do not contradict the fix, the required authoritative runtime/persistence/database/provider/infrastructure/deployment/schema/config state is verified at the authoritative verification boundary, and a fresh independent closure challenge finds no demonstrated material bypass. No material contradiction may remain.

This is the only true closure state.

A `CREDIBLE BUT UNVERIFIED BYPASS` uses the existing incomplete-verification or blocking rules according to whether the missing evidence is material. Suspicion without current evidence is not by itself a veto.

## FIXED — VERIFICATION INCOMPLETE

Use when implementation appears complete but required evidence is unavailable or incomplete.

Examples: migration authored but required deployed schema not exercised; PostgreSQL behavior changed but only an in-memory test passes; physical-device behavior unavailable; provider behavior required but unavailable; concurrency control implemented without adequate race verification; retry or double-action behavior supported only by static/source assertions.

Do not describe this as closed.

## Authoritative verification boundary

If the canonical claim or remediation materially depends on a runtime, persistence, database, external-provider, infrastructure, or deployment path that was not actually verified, do not use `CLOSED VERIFIED` unless deterministic evidence directly proves that same path. Classify an otherwise complete implementation as `FIXED — VERIFICATION INCOMPLETE`.

This does not over-block a canonical claim that Triage explicitly narrowed to process-local, in-memory, or structural behavior and whose narrower authoritative boundary was verified.

## PARTIALLY REMEDIATED

Use when some canonical consequences are addressed but the root cause remains reachable, another canonical path remains defective, or only part of the invariant is restored.

## NOT FIXED

Use when attempted remediation does not address the root cause, the fix was reverted, or verification shows the bad path still exists.

## BLOCKED — ENVIRONMENT

Use when implementation or verification depends on unavailable runtime, service, provider, hardware, credentials, database mode, deployment environment, or equivalent external state.

## BLOCKED — CONTRACT

Use when safe remediation requires a product/behavior decision that cannot be derived from the READY canonical finding and current contract.

Do not invent policy.

## BLOCKED — DEPENDENCY

Use when another incomplete control, migration, finding, or prerequisite must be completed first.

## BLOCKED — TRIAGE CONTRADICTION

Use when bounded current evidence materially contradicts the canonical finding.

Examples: mechanism does not exist at current revision, mandatory control already prevents the claimed state, finding has already been fixed, or canonical root mechanism differs from actual implementation.

Do not re-triage in RivetClose. Return the contradiction to RivetTriage.

## NOT ATTEMPTED

Use when a READY finding is intentionally outside the user-requested remediation subset.

## NOT ADMITTED — TRIAGE BLOCKED

Use when RivetTriage did not hand the finding off as `READY`. Do not remediate it in RivetClose.

## Severity and provenance

Do not lower or change canonical severity after remediation. Do not change provenance.

Severity describes the pre-remediation defect. Closure status describes the remediation result.

## Atomicity

Each canonical RT finding receives one closure status. A shared implementation patch does not imply a shared closure result. Each finding must satisfy its own closure contract.
