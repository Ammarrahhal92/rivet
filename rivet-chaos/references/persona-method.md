# Persona Method

RivetChaos uses behavioral personas to force the reviewer out of the normal happy path.

The personas are not demographic profiles and are not intended to predict individual users. They are controlled lenses for exploring classes of failure.

## CU — Confused User

Goal: expose flows that fail when a user misunderstands the product but behaves plausibly.

Look for:
- ambiguous completion/failure feedback;
- accidental resubmission;
- wrong ordering;
- stale form/page state;
- refresh/back/resume;
- partial completion;
- plausible malformed input;
- user recovery after mistakes;
- client/server disagreement about current state.

Do not report ordinary UX preference as a defect unless it can cause incorrect state, duplicate work, loss, unexpected billing/credit use, or an unrecoverable flow.

## CR — Curious User

Goal: expose assumptions that only hold when users stay inside the intended UI path.

Look for:
- direct routes/endpoints;
- mutable IDs;
- alternate object ownership;
- hidden/disabled actions;
- state parameters;
- replay of old links/tokens/actions;
- read/write boundaries;
- actions invoked before/after their intended lifecycle point.

Curiosity is not equivalent to advanced exploitation. Prefer simple manipulations a normal technically curious person could try.

## CH — Chaos User

Goal: expose race, replay, duplicate, lifecycle, and recovery defects.

Look for:
- double click;
- rapid repeat;
- concurrent requests;
- two tabs;
- two devices;
- slow response followed by retry;
- network interruption;
- timeout followed by retry;
- cancel and complete racing;
- create and delete racing;
- duplicate webhooks/callbacks/jobs;
- stale UI action after another actor/process changed state.

A single application-level `if` is not sufficient evidence of resilience when concurrency matters. Trace transactionality and database enforcement.

## LA — Limit-Abuse User

Goal: expose economic/resource abuse and business-rule bypass.

Look for:
- exact boundary minus/at/plus one;
- quota reset/reuse;
- concurrent quota consumption;
- batch-vs-item accounting;
- retries that consume zero or multiple credits incorrectly;
- multiple identities/sessions where relevant;
- expensive processing before eligibility checks;
- oversized or pathological inputs;
- abandoned jobs that retain reservations;
- trial/free-plan repeatability;
- plan downgrade/upgrade boundary behavior.

Distinguish:
- security vulnerability;
- business-rule defect;
- cost-amplification defect;
- intended product policy.

Do not label a product policy as an exploit merely because it is generous.

## Actor capability envelope

Keep each persona within the capabilities of a realistic actor. Establish authentication/session level, reachable actions, client-controlled inputs or state, visible identifiers, and ordinary repeat, concurrency, interruption, retry, or navigation behavior before confirming a scenario.

- CU may misunderstand or misuse reachable behavior, but does not gain privileged or malicious capabilities by confusion.
- CR may probe reachable routes, identifiers, parameters, and client-visible boundaries, but is not assumed able to forge trusted server/provider authority.
- CH may repeat, race, replay, reorder, interrupt, or retry client-observable operations, but does not control infrastructure or server internals without repository evidence.
- LA may submit high volume, large inputs, repeated expensive operations, or reachable quota/admission requests, but cannot bypass an authoritative limit without an evidenced path.

Unsupported capability requirements must be narrowed, rejected, or classified with the existing `UNVERIFIED` outcome.

## Adaptive scenario generation

After the four core lenses, derive scenarios from the repository's actual risk centers.

Use only risk centers evidenced by the repository, such as multi-step lifecycle transitions, data processing, resource allocation, or shared-state workflows. Derive concrete scenarios from the actual state transitions, ownership rules, resource boundaries, retry behavior, and recovery paths rather than importing domain-specific assumptions.

Never assume a domain or feature that the repository does not implement.

## Cross-persona overlap

The same underlying defect may be reachable by several personas.

During RivetChaos:
- record overlap hints;
- keep the clearest primary evidence;
- prefer one clear primary finding when the violated invariant is the same;
- do not duplicate the same underlying defect under multiple personas;
- do not prematurely merge unrelated behavior.

Cross-persona recurrence is useful discovery evidence, corroboration, and a clue for a bounded same-mechanism sibling sweep. It is not proof of validity or exploitability, a reason to increase severity, a reason to upgrade `UNVERIFIED` to `FINDING`, or a substitute for implementation and reachability evidence.

Formal deduplication and PRIMARY/MERGED/FALSE-POSITIVE disposition belongs to RivetTriage, not this skill.
