---
name: rivet-chaos
description: "Evidence-based adversarial persona and abuse-case audit for software repositories. Use to discover concrete product, state, quota, concurrency, ownership, recovery, and misuse defects by reviewing the system through confused, curious, chaotic, and limit-abusing user behaviors. Discovery-only: do not fix findings during the audit."
metadata:
  display-name: RivetChaos
  version: "0.2.4"
  family: Rivet
---

# RivetChaos

Run an evidence-based adversarial persona and abuse-case audit against the current software repository.

The purpose is not to invent attacks or produce a long generic checklist. The purpose is to discover concrete defects that realistic problematic users can trigger through confusion, curiosity, impatience, repeated actions, unusual sequencing, stale state, boundary pressure, or deliberate abuse.

## Supported repository scope

RivetChaos is an adversarial behavioral review skill for established software repositories with an identifiable product/system contract. Extensive documentation is not required, but repository evidence must identify the important actors, workflows, states and lifecycle, authorization/ownership boundaries, explicit limits, business invariants, and user-visible expectations. The contract may be established across documentation, UI/routes, tests, schemas/configuration, validation/state rules, and existing review material.

RivetChaos may inspect implementation code deeply to verify an identifiable contract. It is not responsible for reconstructing an undocumented product specification from raw code alone.

## Core operating rule

This is a **discovery-only** skill.

Do not modify application code, tests, configuration, migrations, deployment files, or documentation in order to fix a finding while this skill is running.

Do not refactor opportunistically.

Do not turn a suspected issue into a remediation task until it has been evidenced and recorded.

If the repository is dirty before the audit, preserve the existing state and do not mix audit work with unrelated edits.

## Required audit lenses

Always evaluate these four core personas:

1. **CU — Confused User**
   - Misunderstands labels, workflow order, prerequisites, or current state.
   - Repeats an action because feedback is unclear.
   - Navigates backward, refreshes, abandons and resumes, or acts from stale UI.
   - Supplies plausible but incorrect inputs.

2. **CR — Curious User**
   - Explores URLs, IDs, parameters, hidden states, alternate sequences, and boundaries.
   - Tries actions the normal UI does not encourage.
   - Tests whether ownership, visibility, and state rules are actually enforced.
   - Is not assumed to be a sophisticated security attacker.

3. **CH — Chaos User**
   - Clicks rapidly, retries, duplicates, opens multiple tabs/devices, interrupts flows, changes order, races actions, or creates concurrent requests.
   - Exposes idempotency, replay, stale-state, transactional, queue, and lifecycle defects.

4. **LA — Limit-Abuse User**
   - Pushes quotas, batch sizes, upload limits, rate limits, repeated freebies, plan boundaries, resource consumption, and expensive operations.
   - Looks for ways to receive more service than the business rules intend.

These are behavioral lenses, not fixed scripts. Adapt the concrete scenarios to the product.

After repository reconnaissance, add project-specific sub-scenarios when clearly justified. Do not create extra personas merely to increase coverage.

Read [references/persona-method.md](references/persona-method.md) before generating scenarios.

## Phase 0 — Establish the baseline

Before adversarial exploration:

1. Read the repository guidance and product documentation that materially defines behavior.
2. Identify:
   - major user-facing surfaces;
   - authentication/session model;
   - roles and ownership boundaries;
   - important state machines and lifecycle transitions;
   - money, credits, quotas, subscriptions, inventory, or other scarce resources;
   - uploads/downloads and expensive processing;
   - asynchronous work, queues, retries, callbacks, webhooks, realtime paths, or background workers;
   - existing tests around high-risk flows.
3. If previous audit/closure reports are intentionally part of the repository, use them only as baseline context:
   - distinguish previously fixed issues from new findings;
   - preserve explicitly deferred/external items;
   - do not re-report a closed issue unless current code evidence shows regression;
   - do not assume a remediated area is safe merely because a closure report says it was fixed;
   - remember that later fixes/remediation can introduce new secondary defects;
   - treat prior remediation reports as likely high-value re-audit surfaces, especially where a fix may have added idempotency while leaving side effects outside its boundary, added caching/fingerprinting with an incomplete identity model, validated only a non-authoritative layer, or introduced a lifecycle, recovery, or concurrency gap.
4. Do not treat README claims or comments as proof of runtime enforcement.

Before scenario generation, perform a lightweight **Minimum Review Baseline** gate. Assemble enough evidence, from multiple repository sources when useful, to identify at least where relevant:

- actors and trust levels;
- primary workflows;
- important state transitions;
- ownership and authorization rules;
- explicit limits or resource boundaries;
- high-value side effects;
- lifecycle, deletion, and recovery expectations.

Implementation evidence may clarify an already identifiable contract, but do not reconstruct an undocumented product specification from raw code. Classify expectations as:

- **EXPLICIT INVARIANT** — directly supported by product documentation, UI contract, tests, schema/configuration, explicit validation/state rules, or authoritative behavior;
- **STRONGLY SUPPORTED INVARIANT** — not formally documented but clearly implied by multiple consistent repository signals and necessary for coherent system behavior;
- **UNKNOWN PRODUCT INTENT** — requires a product/business decision that repository evidence cannot establish.

Findings may rely on explicit invariants and clearly reasoned strongly supported invariants. Do not invent numeric limits, lifecycle or entitlement rules, or intended UX. If critical contract information is missing, use `INSUFFICIENT REVIEW BASELINE`: explain what is known and what requires product intent, do not manufacture findings, and do not attempt full reverse-engineering. If the repository has enough contract overall, continue and mark isolated policy-dependent scenarios `UNVERIFIED`.

## Phase 1 — Build the attack surface from product behavior

Map realistic behaviors before looking for bugs.

Before detailed adversarial testing, build a concise, risk-weighted coverage map of important contract surfaces. For each relevant workflow, record the actor, important invariant, primary state or side effect, and applicable persona lenses. At minimum consider authentication/authorization, ownership, destructive actions, state transitions, privileged actions, quotas/resources, repeated/concurrent mutations, idempotency/retries, deletion/retention, side effects, and externally visible or financially/security-sensitive behavior. This is a coverage aid, not line-by-line code coverage.

For each important workflow, identify:

- entry conditions;
- authoritative server-side guards;
- client-side guards that could be bypassed;
- mutable IDs/parameters;
- state transitions;
- duplicate/replay behavior;
- concurrent behavior;
- rollback/recovery behavior;
- partial-success and interruption recovery behavior;
- resource or quota consumption;
- ownership/authorization boundaries;
- user-visible feedback after partial failure.

For quota, resource, authorization, financial, lifecycle, ownership, and safety invariants, identify the authoritative enforcement point. UI guards, disabled buttons, browser limits, and frontend validation do not prove enforcement. If only a client-side guard is visible, inspect whether the API can bypass it; report a finding only when that bypass is evidenced.

For plausible representation mismatches across UI/API/language boundaries, inspect boolean versus string boolean, number versus numeric string, null versus omitted, empty versus missing, enum casing, duplicated IDs, and stale or reused identifiers only when loose coercion or ambiguity could materially change persistent state, authorization, lifecycle, quota/resource state, financial/business state, or operational behavior. Do not turn harmless parser differences into findings.

Prioritize workflows where a defect could corrupt:

- state;
- money;
- credits/quota;
- ownership;
- access;
- irreversible user data;
- cross-user consistency;
- background processing;
- recovery after failure.

## Phase 2 — Generate persona scenarios

Generate concrete repository-specific scenarios for CU, CR, CH, and LA.

Each scenario must state:

- persona ID;
- target workflow;
- adversarial or mistaken behavior;
- why a real user could perform it;
- expected invariant;
- evidence path to inspect.

Prefer scenarios such as:

- repeated/double/concurrent submits;
- refresh/back/resume after partial completion;
- stale-state actions;
- replaying a previously valid request;
- changing object IDs or route parameters;
- using actions out of intended order;
- exhausting quota boundaries;
- attempting one extra unit beyond a limit;
- parallel tabs/devices;
- interrupted async work followed by retry;
- a durable early step followed by later failure, interruption, termination, lost response, retry, or resume;
- plausible representation mismatches at UI/API/language boundaries when materially relevant;
- invalid-but-plausible file or input boundaries;
- reuse of expired, revoked, consumed, or already-finalized resources.

Do not mechanically test irrelevant scenarios, and do not let a possible compensating control or later `UNVERIFIED` outcome suppress a relevant scenario during discovery. Discovery breadth comes before precision filtering.

## Phase 3 — Evidence each scenario

Use the repository and available runtime/test tooling to determine what actually happens.

Follow [references/evidence-rules.md](references/evidence-rules.md).

For each scenario:

1. Trace the user action from entry point to authoritative enforcement.
2. Follow enough surrounding execution context to establish the real runtime path when stack behavior may matter. Conceptually trace request, global or route middleware, request normalization, controller/handler, service/model behavior, ORM hooks/casts, database behavior, and exception/response handling as relevant. This is framework-agnostic, not a mandatory architecture. If material framework semantics cannot be established from repository evidence, lower confidence or use `UNVERIFIED` rather than guessing.
3. Identify exact files/functions/queries/constraints involved.
4. Inspect existing tests.
5. When safe and feasible, reproduce using existing test/runtime mechanisms without altering production data.
6. For concurrency/state issues, inspect all relevant layers rather than stopping at one guard:
   - application validation;
   - authorization/policy;
   - transaction boundaries;
   - database constraints/locking;
   - idempotency/replay protection;
   - queue/job uniqueness;
   - state transition enforcement.
7. For sequential guards such as "at least one privileged actor must remain", "only one first event may establish state", count/check-then-mutate, read-await-append/update, or mutations of a shared global invariant through different targets, challenge simultaneous requests. Inspect transaction boundaries, row/table/advisory locks, database constraints, serialization, and compare-and-set or conditional updates.
8. For multi-step workflows, trace the case where an early step succeeds durably, a later step fails or is interrupted, the process/browser/client/worker/application terminates or loses its response, and the user later retries or resumes. Determine whether the system can discover authoritative current state, resume incomplete work, reconcile uncertain success, safely replay, avoid a second logical entity, and distinguish completed, partial, and abandoned work. Do not assume that persistence of the first step makes the workflow recoverable.
9. When idempotency or fingerprinting is present, distinguish replay of the same logical request from a different logical source/action that happens to share client metadata. Check whether identity binds to the authoritative object or source rather than only mutable or client-supplied metadata. Consider relevant inputs such as durable object ID, staged/upload source ID, operation key, content hash, actor ID, target resource ID, and materially defining request fields; do not assume one universal fingerprint design.
10. Inspect side effects before and after idempotent transactional boundaries, including notifications, events, emails, webhooks, audit rows, cache mutation, and async dispatch. Verify that replay cannot preserve one durable primary mutation while duplicating secondary effects.
11. For asynchronous behavior, compare requested action, persisted state, queue/job state, worker/service behavior, and logs/timestamps when available.
12. After broad scenario generation and only when a candidate finding exists, perform one proportional self-challenge: **try to disprove this finding**. Check only relevant surrounding controls, such as middleware, normalization, framework pipelines, interceptors/filters/decorators, model casts/mutators/observers, service providers, policies, route constraints, exception handling, database triggers/constraints, transaction semantics, cache reconciliation, alternate paths, lifecycle/type guards, cleanup, and upstream validation. Do not use a possible defense, unavailable runtime, bounded race, or possible `UNVERIFIED` result to suppress scenario generation. If a defense preserves the invariant, record `ALREADY RESILIENT`; if material behavior depends on unavailable runtime/framework/product evidence, use `UNVERIFIED`. A local trace alone is insufficient when surrounding execution layers could change the behavior.
13. Before finalizing impact or severity, verify reachability: actor, UI/API/background path, normal/stale/crafted/privileged/internal access, object/resource types, state/type guards, required permissions, and whether the effect is local or broader. Do not dismiss real stale or direct-request defects merely because the normal UI hides them, but do not claim theoretical maximum scope beyond the reachable evidence.
14. Record relevant compensating controls and their effect on exploitability, persistence, blast radius, resource cost, user impact, and recovery. Distinguish a violated invariant from the severity of its practical impact; controls may bound impact without eliminating the finding.

15. When a candidate is sufficiently evidenced to identify the violated invariant, the root mechanism or enforcement omission, and the affected trust/state/resource boundary, perform a **bounded same-mechanism sibling sweep** before final classification. Trigger this only for a confirmed finding or a strongly evidenced candidate whose directly analogous surfaces need inspection; do not sweep from a vague suspicion or unsupported policy assumption.
    - A sibling qualifies only when it materially shares **both** the violated invariant and the root mechanism/enforcement omission.
    - Inspect only directly related surfaces such as alternate entry points, sibling handlers or object types, equivalent lifecycle/state guards, projections, queue boundaries, replay/idempotency paths, secondary effects, or quota/authorization enforcement points when the repository makes that relationship concrete.
    - Stop when the invariant or mechanism changes, only superficial similarity remains, the path is unrelated, a new product assumption is required, or exploration becomes generic repository-wide review. Similar names, directories, framework primitives, or table families are not enough.
    - Classify every sibling actually inspected independently as `FINDING`, `ALREADY RESILIENT`, `UNVERIFIED`, or `NOT APPLICABLE`, and apply the adversarial path closure gate to that sibling independently. A vulnerable primary path does not transfer validity, severity, reachability, impact, or uncertainty to a sibling.
    - Record shared mechanism and overlap for later handoff, but do not canonicalize, merge, assign RivetTriage states, reconcile provenance, or suppress an independently actionable manifestation.

16. Before promoting a scenario to `FINDING`, establish the actor capability envelope. Record the capabilities materially relevant to reachability: authentication/session level, legitimately reachable actions, client-controlled inputs/state, visible identifiers, ordinary repeats/concurrency/interruption, and any browser/API manipulation naturally available to that actor. Do not assume the actor can write authoritative state, forge authorization or trusted provider payloads, possess administrator credentials, control infrastructure, or cross a trust domain unless repository evidence establishes that path. If a material edge requires unsupported power, narrow, reject, or classify the scenario as `UNVERIFIED`.

17. Keep **research scope** separate from **reporting scope**. RivetChaos may inspect adjacent source, helpers, configuration, tests, models, enforcement paths, and sibling implementations when needed to confirm or refute a scenario, establish reachability, locate controls, or perform the bounded sibling sweep. `INSPECTED` does not mean `REPORTABLE`; an unrelated defect-like pattern without relevant persona scope and evidence must not become an opportunistic finding.

18. Treat cross-persona recurrence as discovery evidence and possible corroboration, not proof. Repetition of an unsupported claim by CU, CR, CH, or LA does not establish validity or exploitability, increase severity, upgrade `UNVERIFIED` to `FINDING`, replace implementation/reachability evidence, or perform canonical deduplication.

19. Every confirmed finding must support the concise adversarial path: **actor action → reachable implementation/state mechanism → violated invariant → supported consequence**. If a material edge is missing, preserve uncertainty, narrow the consequence, or reject the scenario; do not compensate by increasing severity.

20. Before finalizing any scenario as `FINDING`, apply the mandatory **Adversarial Path Closure Gate** to the literal path written in the finding. Establish, where materially relevant: the initial state; the exact actor or actors and their capabilities; the exact target object or objects; the reads and preconditions before mutation; the exact mutations and side effects; the resulting state; the violated invariant; and the supported consequence. Every material edge must close. If the written path is not supported, correct it only when current evidence supports the correction, narrow the claim, classify it as `UNVERIFIED`, or reject it. Do not retain an incorrect example merely because a related root defect exists.
    - Preserve actor identity, object identity, effective mutation count, transition order, and final state whenever they determine validity. Two requests against one object do not establish two independent mutations; two retries by one actor do not establish two actors; duplicate delivery does not establish duplicate durable effects without evidence.
    - For concurrency, distinguish same-target operations from distinct targets sharing an aggregate invariant. Inspect the relevant row/aggregate lock domain, transaction boundary, affected-row behavior, uniqueness/idempotency, read timing, mutation target, and final aggregate state rather than equating concurrent requests with independent mutations.
    - Validate the starting state and account for transitions as `S0 → operation A → operation B → Sn` or the equivalent exact sequence. Before finalizing, ask: “If these exact actors perform these exact operations against these exact objects, and nothing unstated happens, does the claimed final state actually follow?” If not, the path is not closed.
    - A real root mechanism does not validate every proposed reproduction path, and a mechanism weakness does not by itself prove corruption, privilege gain, resource exhaustion, or privacy loss. The claimed consequence must follow from the exact resulting state. This gate applies to all four personas, not only CH.

Never infer a defect only because a guard is absent from the UI.

Never infer safety only because one guard exists in application code.

## Phase 4 — Classify the outcome

Every attempted scenario must end in one of these outcomes:

### `FINDING`
A concrete defect or missing invariant is supported by evidence.

### `ALREADY RESILIENT`
The scenario was meaningful, but existing defenses correctly preserve the invariant.

RivetChaos quality is not measured by finding count. Actively record meaningful `ALREADY RESILIENT` scenarios and the defenses that preserve the invariant; do not manufacture a weaker finding when layered controls work. Relevant defenses may include authoritative validation, authorization, transaction boundaries, locking, conditional updates, database constraints, durable idempotency, and replay handling, but do not require every layer in every case.

### `UNVERIFIED`
The scenario is credible but available evidence/runtime access is insufficient to prove either failure or resilience.

State exactly what evidence is missing.

### `NOT APPLICABLE`
The scenario does not apply to this product or implementation.

Do not force a finding.

## Finding quality bar

A finding is valid only when it includes:

- stable ID using persona prefix (`CU-###`, `CR-###`, `CH-###`, `LA-###`);
- severity;
- affected workflow/subsystem;
- behavior attempted;
- reproducible or traceable path;
- expected invariant;
- actual behavior;
- exact evidence;
- concise adversarial path from actor action through reachable mechanism and violated invariant to supported consequence;
- impact;
- smallest credible remediation direction;
- verification criteria;
- overlap with any other finding if known;
- status: `NOT FIXED — DISCOVERY STAGE`.

If prior reports clearly provide the context, optionally include one provenance hint: `NEW`, `KNOWN`, `POSSIBLE REGRESSION`, or `UNKNOWN`. Use only evidence already read; do not perform extensive git archaeology or a full provenance audit, spend substantial audit time proving history, or suppress a valid current finding because it is known. Formal provenance and deduplication belong to RivetTriage.

If multiple personas reach the same or overlapping mechanism, use overlap notes and prefer one clear primary finding with the strongest evidence. Recurrence is corroboration or a clue for bounded sibling inspection, not proof of validity, exploitability, severity, or a replacement for implementation and reachability evidence. Do not duplicate the same underlying defect under several personas merely to increase coverage.

Severity prioritizes remediation. It must not be used to silently discard a valid finding.

Avoid speculative security language. Describe the concrete failure first.

If a candidate defect is real but the original hypothesis is broader than the evidence supports, keep the finding and narrow its title, affected actors/resources, mechanism, impact, and severity to the smallest defensible failure. Avoid speculative blast-radius language.

## Severity

Use impact first:

- **P0** — catastrophic compromise or similarly extreme system-wide failure.
- **P1** — severe security, privacy, integrity, availability, governance, or major business failure with substantial blast radius or difficult recovery.
- **P2** — material defect affecting important state correctness, authorization, privacy, durable data, meaningful resource consumption, business invariants, lifecycle integrity, or significant user recovery.
- **P3** — real but bounded defect where scope is narrow, durable impact is small or capped, no meaningful authorization/privacy/financial boundary is crossed, resource amplification is tightly bounded, recovery is straightforward, or impact is primarily operational/UX/retry noise.

A durable invariant violation may still be P3 when its maximum practical effect is tightly bounded. A concurrency race is not automatically P2. An already-privileged actor's stale action is not automatically P2 when authority is unchanged and the practical effect is narrow. Compensating controls can reduce severity without eliminating a real finding.

Concurrency, persistence, idempotency, stale requests, database writes, and resource-limit bypass are not severity levels by themselves. Classify severity from reachable outcome, violated invariant, compensating controls, and material impact.

Concurrency, idempotency, retries, and replay are not severity levels by themselves. Classify severity from the violated invariant, evidence, and material impact.

If impact is uncertain, lower confidence rather than exaggerating severity.

## Output

Create five Markdown reports under:

`docs/reviews/personas/`

Use these filenames:

- `00-rivet-chaos-summary.md`
- `01-confused-user.md`
- `02-curious-user.md`
- `03-chaos-user.md`
- `04-limit-abuse-user.md`

Use [assets/report-template.md](assets/report-template.md) as the reporting contract.

The summary must contain:

- executive assessment;
- coverage map;
- finding count by persona and severity;
- all confirmed findings;
- all `UNVERIFIED` scenarios requiring later evidence;
- notable `ALREADY RESILIENT` defenses;
- overlap hints for later consolidation;
- explicit statement that no remediation was performed.

If the Minimum Review Baseline gate fails, the summary must state `INSUFFICIENT REVIEW BASELINE`, identify the missing review-critical information, distinguish known behavior from product intent, and avoid manufactured persona findings. If the overall baseline is adequate, isolated unknown-policy cases may remain `UNVERIFIED`.

## Completion checks

Before finishing:

- [ ] All four core personas were evaluated.
- [ ] Scenarios were adapted to the actual product.
- [ ] Every important workflow/invariant in the coverage map has FINDING, ALREADY RESILIENT, UNVERIFIED, or NOT APPLICABLE coverage.
- [ ] Broad relevant scenario generation occurred before self-challenge filtering.
- [ ] Findings contain concrete repository/runtime evidence.
- [ ] Each candidate finding survived a proportional "try to disprove this finding" self-challenge.
- [ ] Relevant execution context beyond the immediate function was traced when stack behavior could change the result.
- [ ] Reachability, compensating controls, and practical scope were considered before impact and severity were finalized.
- [ ] Actor capabilities and unsupported capability assumptions were bounded before impact and severity were finalized.
- [ ] Each material finding supports actor action → reachable mechanism → violated invariant → supported consequence.
- [ ] A bounded same-mechanism sibling sweep was performed when a root mechanism was sufficiently evidenced, with explicit stop conditions and independent sibling outcomes.
- [ ] Research expansion did not turn inspected-but-unrelated code into reportable findings.
- [ ] Cross-persona recurrence was not used as proof or severity inflation.
- [ ] Every confirmed finding passed the literal Adversarial Path Closure Gate.
- [ ] Actor/object identity, effective mutation count, initial state, transitions, and final state were preserved where material.
- [ ] Same-target and distinct-target concurrency were distinguished where relevant.
- [ ] The claimed consequence follows from the exact resulting state, and severity was not used to compensate for path uncertainty.
- [ ] Existing resilience was recorded where appropriate.
- [ ] Speculation is labeled `UNVERIFIED`, not promoted to a finding.
- [ ] Previously closed/deferred baseline issues were not carelessly rediscovered as new.
- [ ] Remediated areas were re-audited for secondary lifecycle, recovery, concurrency, identity, validation-boundary, and side-effect defects when relevant.
- [ ] Authoritative server/backend/database enforcement was identified for material invariants; client-only guards were not treated as proof.
- [ ] No product code or configuration was modified.
- [ ] Every confirmed finding has a stable persona-prefixed ID.
- [ ] Every finding says `NOT FIXED — DISCOVERY STAGE`.
- [ ] The five required reports exist.
