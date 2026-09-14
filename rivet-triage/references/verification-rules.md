# Verification Rules

## Purpose

RivetTriage may inspect current code, config, tests, runtime evidence, or historical artifacts only to answer bounded triage questions.

> Verification is question-scoped, not discovery-scoped.

## Permitted questions

Examples:

- Are findings A and B the same root mechanism?
- Does a named compensating control actually invalidate the finding?
- Is the current route/job/service/path still present?
- Is the defect reachable in the current supported operation?
- Does the historical defect still exist?
- Was the defect demonstrably absent after an earlier remediation?
- Does one source finding contain multiple independent defects?
- What current impact supports canonical severity?
- Does a test actually prove the relevant invariant/mechanism?

## Prohibited expansion

Do not:

- browse a subsystem broadly for additional issues;
- create discovery coverage maps;
- launch specialist agents to hunt defects;
- convert unrelated suspicious code into an `RT-*` finding;
- “check the rest of the repository” merely because a triage path was opened.

Incidental unrelated risks may be recorded only as `OUT-OF-SCOPE DISCOVERY SIGNAL`.

## Current-state evidence preference

Prefer evidence that directly answers the triage question:

1. current implementation/config/schema/runtime registration;
2. current tests that directly establish the relevant invariant/mechanism;
3. current reproducible runtime/command evidence;
4. current authoritative contract material;
5. historical evidence for comparison only.

## Historical closure rule

Words such as closed, fixed, remediated, deployed, resolved, or verified inside an old report are claims, not present-state proof.

To classify `FIXED`, verify that the current defect mechanism/violated behavior is absent.

To classify `REOPENED DEFECT`, historical verified absence is also required.

## Source-finding validity gate

Before admitting a source `FINDING` as a `CURRENT` canonical finding, independently verify:

1. the claimed implementation condition exists now;
2. it violates a current supported invariant;
3. it produces the concrete undesirable behavior claimed;
4. mandatory framework, runtime, database, queue, transaction, retry, or redelivery controls do not prevent or recover that behavior; and
5. the operation is reachable under the current supported repository/runtime assumptions.

Agreement among sources, a missing preferred control, or a plausible mechanism does not satisfy this gate. A historical validator or remediation report may identify a question, but current evidence decides it. If the gate fails, preserve the source mapping and use an explicit rejected/non-finding, `FIXED`, `STALE`, `UNVERIFIED CURRENT STATE`, or unresolved disposition.

For create/dispatch claims, inspect actual transaction and queue semantics rather than inferring failure from the absence of local atomicity. For cleanup/reconciliation claims, inspect retry, redelivery, acknowledgement, and failure handling before declaring work stuck. An architectural preference is not itself a violated invariant.

## Control challenge

When one source reports a defect and another source cites a control, verify:

1. same operation?
2. same authoritative state/boundary?
3. control acts before/at the failure point?
4. same concurrency/failure lifecycle?
5. control mandatory on the reachable path?
6. no bypass/fail-open path that preserves the defect?

A nearby control is not automatically compensating.

## Framework/runtime semantics

When a dispute depends on database, queue, filesystem, browser, framework, or process semantics:

- inspect repository configuration and actual usage;
- rely on established runtime semantics where appropriate;
- do not invent deployment topology;
- distinguish ordinary supported request concurrency from hypothetical multi-instance deployment;
- use `UNVERIFIED CURRENT STATE` when topology is genuinely required and unavailable.

## Current-state labels

Use only:

- `CURRENT`
- `FIXED`
- `STALE`
- `UNVERIFIED CURRENT STATE`
- `SUPERSEDED`

`SUPERSEDED` means a source representation was replaced by better canonical decomposition/merge. It says nothing by itself about repair.

## Rejection discipline

A source candidate may be rejected only when bounded verification establishes why.

Possible reasons:

- claimed invariant is not part of current supported contract;
- alleged path is unreachable;
- source misunderstood framework/database semantics;
- a mandatory control fully prevents the behavior;
- a compound source claim contains an unsupported subclaim.

Always account for the rejected source in the provenance audit.

## Severity verification

Inspect only what is needed to establish practical current impact:

- blast radius;
- per-operation consequence;
- recoverability;
- supported limits;
- affected data/trust boundary;
- controls;
- ordinary reachability.

For `CURRENT` findings, treat `P3` as the default for a real bounded defect. Require independent evidence for `P2` or higher: material per-instance security/privacy/state/lifecycle harm, deterministic materially significant supported-operation failure, durable corruption/loss, meaningful authorization/trust-boundary violation, or demonstrated/strongly supported operational/resource impact beyond bounded inefficiency. Unknown production magnitude, reviewer count, architectural importance, core-workflow status, AI/provider usage, or growth potential are not independent P2 evidence. Quantitative uncertainty limits severity amplification but does not invalidate a verified defect.

Lack of production incidents does not invalidate deterministic current defects.

Do not launch a broad benchmark or penetration test merely to optimize severity.

## Test evidence

A passing test is relevant only if it exercises the same invariant and mechanism.

Beware:

- self-referential generator/contract tests;
- consumer-only tests for producer defects;
- serialized tests for production-concurrent paths;
- wrong actor/guard;
- fixture-only behavior presented as production evidence.

A failing test proves only the behavior it actually demonstrates.

## Verification budget

Prefer the smallest evidence path that resolves the question.

Stop once sufficiently answered.

If resolution requires broad discovery, mark the candidate unresolved and send it back to discovery rather than turning RivetTriage into RivetSpec.
