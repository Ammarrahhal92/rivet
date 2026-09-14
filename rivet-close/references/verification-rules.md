# Verification Rules

RivetClose closes findings through evidence, not intention.

## Closure evidence hierarchy

Prefer evidence that directly exercises the canonical invariant and its authoritative verification boundary:

1. exact regression reproduction/test;
2. invariant-level positive and negative cases;
3. relevant subsystem regression suite;
4. broader repository validation.

A full-suite pass without exact regression coverage is insufficient for `CLOSED VERIFIED`.

## Authoritative-path verification gate

For each finding, identify the `Authoritative verification boundary`: the exact runtime, persistence, database, external-provider, infrastructure, or deployment path whose semantics determine the canonical claim or remediation.

A finding MUST NOT be classified `CLOSED VERIFIED` when that authoritative path was not actually verified, unless deterministic evidence directly proves the same path. Examples:

- An in-memory store test does not verify changed PostgreSQL persistence behavior.
- A persisted notification fix requires verification of the database-backed notification path.
- A repository configuration change does not prove that the live deployment or service state was applied.
- A provider mock does not prove provider-specific live runtime behavior when that behavior is part of the canonical claim.

If implementation appears complete but authoritative-path evidence is missing, classify `FIXED — VERIFICATION INCOMPLETE`. Do not over-block a canonical claim that Triage explicitly narrowed to process-local or in-memory behavior; unavailable PostgreSQL or multi-instance evidence is irrelevant when that environment is outside the narrowed claim.

## Pre-fix evidence classifications

Use:

- `REPRODUCED`
- `DETERMINISTICALLY ESTABLISHED`
- `NOT SAFELY REPRODUCIBLE`

Never claim reproduction that was not run.

## Required closure properties

For `CLOSED VERIFIED`, establish:

1. root cause addressed;
2. canonical bad behavior no longer reachable on the verified path;
3. expected invariant demonstrated;
4. exact regression evidence passes;
5. relevant regression evidence does not contradict closure;
6. no known contradictory runtime result remains;
7. the required authoritative runtime, persistence, database, provider, infrastructure, deployment, migration, schema, or configuration state is verified at the authoritative verification boundary, or deterministically proven for that same path.

When the canonical claim is runtime, user-visible, request, state-machine, retry, concurrency, lifecycle, or asynchronous behavior, Layer 1 must exercise that behavior whenever practical. Static/source-contract assertions alone are insufficient for `CLOSED VERIFIED` merely because the expected code structure exists.

Static evidence may be sufficient only when the claim is structural, or when the verified structure deterministically establishes the behavior with no material framework/runtime semantics left untested. If implementation is complete but only static evidence exists for a behavior-sensitive claim, use `FIXED — VERIFICATION INCOMPLETE`. Never force unsafe, destructive, production-only, real-money, or unavailable-hardware reproduction.

## Bounded same-mechanism challenge

After the primary test passes, inspect directly related sibling paths sharing the same authority/mechanism.

Examples: multiple routes calling the same authorization policy, all candidate-facing serializers named in the canonical finding, create/update paths sharing the same state invariant, or retry/replay paths sharing the same idempotency key.

Do not expand into repository-wide discovery.

## Fresh independent closure challenge

After remediation and exact regression verification, perform a fresh read-only challenge before finalizing `CLOSED VERIFIED`. Re-examine the post-fix state from the admitted canonical finding and violated invariant, without relying on the remediation author's justification or desired conclusion.

Where available, prefer an independent reviewer or context that receives only the canonical finding, invariant, current post-fix repository state, and permitted closure scope. If isolation is unavailable, perform a logically separate pass that re-reads the authoritative path and searches for equivalent bypasses without treating prior remediation reasoning as evidence. Multi-agent capability is not required.

The challenge is bounded to the admitted invariant, authoritative mechanism, and material in-scope siblings or variants. Consider alternate entry points, equivalent representations, parser/normalization differences, retry/replay, concurrency, direct backend/API paths, stale enforcement, equivalent state transitions, and legitimate behavior broken by the repair. Stop when the concern becomes unrelated discovery or a different canonical mechanism.

Classify the result as:

- `DEMONSTRATED BYPASS`: current evidence proves the canonical invariant remains reachable through a materially equivalent path; `CLOSED VERIFIED` is forbidden and the existing repair/verification loop continues.
- `CREDIBLE BUT UNVERIFIED BYPASS`: relevant concern without sufficient current evidence; apply existing incomplete-verification or blocking rules as appropriate, without automatically calling it a defect.
- `ALREADY RESILIENT / NO MATERIAL BYPASS`: inspected equivalent paths are closed or defended.
- `UNRELATED NEW ISSUE`: record only an `OUT-OF-SCOPE DISCOVERY SIGNAL`.

Suspicion alone is not a veto. A bypass concern must have current evidence for path, reachability, mechanism, invariant, and consequence. This fresh challenge is independent in reasoning, not a duplicate full suite or a replacement for the existing same-mechanism fix challenge.

## Authorization verification

Use relevant cases:

- owner/authorized actor allowed;
- non-owner denied;
- unauthenticated denied;
- cross-tenant denied;
- public recipient allowed only when the canonical contract is public.

## State verification

Verify valid transition, invalid transition rejection, correct final persisted state, and replay/concurrent mutation handling when relevant.

## Concurrency verification

Do not use a serial test as proof that a race is closed.

Prefer controlled parallel requests, deterministic scheduler/barrier/interleaving tests, database locking/uniqueness/CAS semantics, and direct concurrent testing where practical.

When concurrency proof cannot be obtained, use `FIXED — VERIFICATION INCOMPLETE` or `BLOCKED — ENVIRONMENT`.

## Idempotency verification

Verify all material effects:

- first request;
- same-key replay;
- same-key concurrent replay when applicable;
- different-key request;
- state changes;
- notifications/outbox/events.

## Recovery verification

A recovery fix should prove relevant failure, actionable state after failure, retry/resume success, no duplicate logical work, and successful normal path.

## Performance/resource verification

When the canonical finding is structural, structural proof may close it.

Examples: pagination imposes a bound, projection avoids heavy columns, input cap is enforced, or duplicate query path is removed.

Do not claim measured latency/memory/cost improvement unless measured.

## External systems

Mocks prove only the mocked boundary. Use provider test mode/sandbox or contract-level evidence when live semantics are required.

Provider-specific live behavior that is part of the canonical claim requires evidence at that provider boundary; a mock alone cannot support `CLOSED VERIFIED`.

## Deployment-sensitive findings

Repository code/config changes are not equivalent to production closure.

If closure depends on deployed migration, service reload, live config, DNS, TLS, or infrastructure state and that state was not applied, do not report production closure.

When implementation appears complete but the required live authoritative path was not verified, use `FIXED — VERIFICATION INCOMPLETE`.

## Failure attribution

Classify test/build failures:

- `PRE-EXISTING FAILURE`
- `REMEDIATION-INTRODUCED FAILURE`
- `UNRELATED/UNRESOLVED`

A remediation-introduced failure affecting the same subsystem prevents `CLOSED VERIFIED`.

## Anti-test-gaming

A passing test does not count if the test bypasses the repaired mechanism.

Reject evidence produced by mocked-away authorization, disabled middleware, swallowed errors, skipped concurrency, relaxed assertions, removed tests, disabled validation, or test-only paths that production never uses.

## Fix challenge stop rule

Stop after the canonical mechanism and directly relevant siblings have been checked. If broader review becomes necessary, record an out-of-scope signal or return to a discovery skill.
