# Evidence Rules

RivetChaos is evidence-first.

## Evidence hierarchy

Prefer, roughly in this order:

1. Reproducible test/runtime result.
2. Database constraint/query/transaction evidence.
3. Authoritative backend policy/service/controller/domain logic.
4. Queue/worker/job state and logs for asynchronous paths.
5. Existing automated tests.
6. Frontend behavior.
7. Documentation/comments.

Lower-ranked evidence can be useful, but it must not override contradictory authoritative behavior.

## Minimum review baseline

RivetChaos expects an established repository with an identifiable product/system contract. Missing documentation, tests, Git, or runtime access is not itself a finding, but the review must have enough evidence to identify the relevant actors/trust levels, primary workflows, important states, ownership/authorization rules, explicit limits, high-value side effects, and lifecycle/deletion/recovery expectations.

Assemble this minimum baseline from available repository sources without requiring formal documentation for every point. Classify expectations as:

- `EXPLICIT INVARIANT` — directly supported by product documentation, UI contract, tests, schema/configuration, explicit validation/state rules, or authoritative behavior;
- `STRONGLY SUPPORTED INVARIANT` — clearly implied by multiple consistent repository signals and necessary for coherent system behavior;
- `UNKNOWN PRODUCT INTENT` — requires a product/business decision not established by repository evidence.

If critical contract information is missing, report `INSUFFICIENT REVIEW BASELINE`, explain what is known and what requires product intent, and do not attempt full reverse-engineering. If the overall baseline is adequate, continue and mark isolated policy-dependent scenarios `UNVERIFIED`. Implementation evidence may clarify an identifiable contract but must not invent one.

Git history is optional context, not a baseline prerequisite. If it is absent, record provenance as `UNKNOWN` and review the current state only; do not reconstruct history by default.

When tests do not exist, use safe runtime reproduction if available, static control-flow traces, database constraints, transaction/locking behavior, authoritative backend checks, configuration, and persistence behavior. If runtime reproduction is unavailable, state that clearly. A defect or defense proven statically remains `FINDING` or `ALREADY RESILIENT`; use `UNVERIFIED` when material confirmation genuinely depends on unavailable evidence.

## A valid finding needs a failure chain

Show the complete adversarial path:

`actor action -> reachable implementation/state mechanism -> violated invariant -> supported consequence`

Each material edge must be supported by current repository, runtime, test, or authoritative contract evidence. If an edge is missing, narrow the consequence or classify the scenario as `UNVERIFIED` rather than increasing severity.

## Adversarial path closure gate

Before finalizing any scenario as `FINDING`, close the literal path written in the report. Establish, where materially relevant:

1. the exact initial state;
2. the exact actor or actors and each actor's capability envelope;
3. the exact target object or objects;
4. the reads and preconditions before mutation;
5. the exact mutations and side effects;
6. the resulting state;
7. the violated invariant; and
8. the supported consequence.

The number and identity of effective mutations must be sufficient to produce the claimed result. Preserve actor identity, object identity, cardinality, transition order, and final state when they determine validity. Two requests against one object are not two independent mutations; two retries by one actor are not two actors; duplicate delivery is not duplicate durable effect without evidence.

For concurrency, explicitly distinguish same-target operations from distinct targets sharing an invariant. Same-target analysis may require affected-row semantics, stale models, idempotency, uniqueness, duplicate side effects, and serialization. Distinct-target analysis may require aggregate lock scope, shared preconditions, transaction boundaries, and whether independent commits combine into an invalid aggregate state. Do not infer aggregate failure merely from same-target duplicate requests.

Account for state transitions as `S0 -> operation A -> operation B -> Sn`, or the equivalent exact sequence. The counterfactual challenge is mandatory: if the exact actors perform the exact operations against the exact objects described in the finding, and nothing unstated happens, does the claimed final state actually follow? If not, correct the path only when current evidence supports the correction; otherwise narrow, classify `UNVERIFIED`, or reject it.

A real root mechanism does not validate every proposed reproduction path. The mechanism defect, the literal path, and the claimed consequence are judged independently. The consequence must follow from the exact resulting state; mechanism weakness alone does not prove corruption, privilege gain, resource exhaustion, or privacy loss. This gate applies to CU, CR, CH, and LA, including siblings found during a bounded sweep.

Do not write:
- "might be vulnerable";
- "could potentially";
- "probably unsafe";

unless the outcome is `UNVERIFIED`.

## Execution context and self-challenge

Trace beyond the immediate controller or function when surrounding stack behavior could change the result. Inspect relevant request middleware, normalization, route constraints, handler/service/model behavior, ORM hooks/casts, database behavior, and exception/response handling. This is conceptual and framework-agnostic; do not require every layer when it is irrelevant.

Before recording `FINDING`, make one proportional attempt to disprove it: **try to disprove this finding**. Check only relevant compensating paths such as policies, filters, decorators, observers/hooks, alternate service paths, lifecycle/type guards, cleanup, upstream validation, transaction semantics, database triggers/constraints, or cache reconciliation. If a defense preserves the invariant, record `ALREADY RESILIENT`. If confirmation depends materially on unavailable framework/runtime/product evidence, use `UNVERIFIED`; do not guess. Do not use unavailable runtime execution to demote a defect already proven by static code or schema evidence; runtime would strengthen the evidence but is not required to establish it.

Do not discard a real finding merely because the original hypothesis was broad. Narrow the actors, resources, mechanism, impact, and severity to the smallest failure supported by evidence.

## Reachability, controls, and practical scope

Before finalizing impact or severity, verify which actor can invoke the behavior, through which UI/API/background path, with what permissions, object/resource types, lifecycle or type guards, and normal, stale, crafted, privileged, or internal access. A hidden normal-UI path does not disprove a reachable direct-request defect, but a local code fragment does not prove its theoretical maximum scope.

Record relevant controls such as request-size limits, per-object caps, throttling, authentication, ownership checks, finite batches, database constraints, bounded retries, narrow actor/resource scope, existing privilege, reversibility, and cleanup/recovery. Controls may reduce exploitability, persistence, blast radius, resource cost, user impact, or severity without eliminating a real invariant violation. Distinguish the fact of the violation from the severity of its practical impact.

Before confirming a scenario, establish the actor capability envelope. Reason about the actor's authentication/session level, reachable actions, client-controlled inputs/state, visible identifiers, and ordinary repetition, concurrency, interruption, retry, or navigation. Do not assume direct authoritative database writes, forged authorization or provider signatures, administrator credentials, infrastructure control, or an unproven cross-trust-domain path. If a material edge depends on unsupported actor power, narrow, reject, or classify the scenario as `UNVERIFIED`.

## Research scope versus reporting scope

RivetChaos may inspect adjacent source, helpers, configuration, tests, models, enforcement paths, and sibling implementations when needed to establish reachability, find compensating controls, confirm authoritative behavior, or execute a bounded sibling sweep. `INSPECTED` is not `REPORTABLE`: unrelated code or a defect-like pattern outside the relevant adversarial surface must not become an opportunistic finding merely because it was read.

## Already resilient

Use `ALREADY RESILIENT` when a meaningful adversarial attempt is blocked correctly.

Record layered defenses when present, for example:
- idempotency key;
- active-state guard;
- authorization policy;
- transaction;
- row lock;
- partial/unique database constraint;
- replay check.

This is important: the audit measures resilience, not finding count.

Actively record meaningful `ALREADY RESILIENT` scenarios. Do not manufacture a weaker finding when layered controls preserve the invariant, and do not require every possible layer when the authoritative evidence is sufficient. If several personas reach the same failure, use overlap notes and keep one clear primary finding for the shared violated invariant.

## Bounded same-mechanism sibling sweep

After a candidate is sufficiently evidenced to identify the violated invariant, root mechanism or enforcement omission, and affected trust/state/resource boundary, inspect directly analogous sibling surfaces before final classification. Do not trigger this sweep from a vague suspicion or unsupported policy assumption.

A sibling qualifies only when it materially shares both:

- the same violated invariant; and
- the same root mechanism or enforcement omission.

The sweep may inspect concrete alternate entry points, sibling handlers or object types, equivalent lifecycle/state guards, projections, queue boundaries, replay/idempotency paths, secondary effects, or quota/authorization enforcement points. Do not force every dimension onto every repository.

Stop when the invariant or mechanism changes, only superficial similarity remains, the path is unrelated, a new product assumption is required, or the work becomes generic repository-wide review. Similar names, directories, framework primitives, or table families do not establish sibling identity.

Every sibling actually inspected receives an independent `FINDING`, `ALREADY RESILIENT`, `UNVERIFIED`, or `NOT APPLICABLE` outcome. A vulnerable primary does not transfer validity, severity, reachability, impact, or uncertainty. Record shared mechanism and overlap for RivetTriage, but do not canonicalize, merge, assign canonical triage states, reconcile provenance, or suppress an independently actionable manifestation.

Cross-persona recurrence is discovery evidence and possible corroboration only. Repeated unsupported claims do not establish validity, exploitability, severity, or an upgrade from `UNVERIFIED` to `FINDING`, and do not replace implementation or reachability evidence.

## Concurrency

For race-sensitive behavior, inspect whether correctness survives simultaneous requests.

Application checks without locking/constraints may be TOCTOU-prone.

Challenge sequential invariants explicitly: for example, retaining at least one privileged actor, allowing only one first event to establish state, count/check-then-mutate, read-current-state then await then append/update, or two targets mutating one shared global invariant. Trace transaction boundaries, row/table/advisory locks, database constraints, serialization, and compare-and-set or conditional updates.

Do not casually equate concurrent requests with independent mutations, two operations with two distinct targets, or stale reads with an invariant violation. Where relevant, account for actor count, target count, shared versus independent rows, initial aggregate state, read timing, lock domain, transaction boundary, mutation target, affected-row behavior, uniqueness/idempotency, and final aggregate state.

When possible, reproduce concurrency rather than inferring it.

If reproduction is not feasible, classify as `UNVERIFIED` unless the code proves the invariant one way or the other.

## Partial-success and interruption recovery

For multi-step workflows, trace an early durable success followed by later failure, interruption, termination, or lost response, then a retry or resume. Check whether authoritative current state is discoverable, incomplete work is resumable, uncertain success is reconcilable, replay is safe, a second logical entity is prevented, and completed/partial/abandoned states are distinguishable. Persistence of an early step alone does not prove end-to-end recoverability.

## Representation and type boundaries

Inspect plausible UI/API/language representation mismatches—such as boolean/string boolean, number/numeric string, null/omitted, empty/missing, enum casing, duplicated IDs, or stale/reused identifiers—only when loose coercion or ambiguity can materially affect persistent state, authorization, lifecycle, quota/resource state, financial/business state, or operational behavior. Harmless parser differences are not findings.

## Runtime operations

When a test depends on operational state, capture relevant before/after evidence such as:
- persisted records;
- queue/job state;
- worker/service health;
- heartbeat;
- logs/journal;
- timestamps.

Do not confuse:
- no record created;
- record queued;
- job running;
- job failed;
- worker unavailable.

## Authoritative boundaries

For quota, resource, authorization, financial, lifecycle, ownership, and safety limits, identify the server/backend/database point that owns the invariant. Client-side validation, disabled controls, browser limits, and UI guards are evidence of intended behavior only. If they are the only visible guard, inspect whether a direct API request bypasses them, but do not promote the possibility to a finding without evidence.

## Idempotency and secondary effects

When a fix or feature adds idempotency, caching, or fingerprinting:

- distinguish replay of the same logical request from a different authoritative source/action that shares mutable or client-supplied metadata;
- inspect whether identity binds to the authoritative object/source and materially defining operation fields, using relevant durable IDs, source IDs, operation keys, hashes, actor IDs, or target IDs as evidence suggests;
- inspect notifications, events, emails, webhooks, audit rows, cache mutation, and async dispatch before and after the idempotent boundary;
- check whether replay can keep one durable primary mutation while duplicating secondary effects.

Do not assume a closure report proves the remediation is safe. Re-audit the changed boundary for incomplete identity, non-authoritative validation, duplicate secondary effects, and new lifecycle, recovery, or concurrency gaps.

## Baseline discipline

If prior reports exist:
- closed issue with current proof intact → baseline, not a new finding;
- closed issue that regressed → new finding, explicitly marked regression;
- deferred external/configuration item → preserve its status unless new evidence changes it;
- inaccessible environment dependency → `UNVERIFIED` or environment-blocked context, not invented failure.

Provenance remains lightweight: use `NEW`, `KNOWN`, `POSSIBLE REGRESSION`, or `UNKNOWN` only when obvious from reports encountered naturally. Do not perform extensive git archaeology, spend substantial audit time proving history, suppress known findings, or perform formal cross-report deduplication; those responsibilities belong to RivetTriage.

## Smallest remediation direction

RivetChaos does not fix findings, but each finding should point toward the smallest credible remediation direction so later triage/remediation can act efficiently.

Do not prescribe a broad rewrite unless evidence shows a narrow fix cannot preserve the invariant.
