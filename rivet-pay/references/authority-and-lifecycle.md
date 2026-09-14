# Authority and Lifecycle

This reference owns the Value Authority Graph, commercial invariants, lifecycle reconstruction, entitlement/consumption separation, authority lineage, and supersession reasoning.

## Value Authority Graph

For every material value path map:

```text
authority → evidence → interpretation → grant state → entitlement → enforcement → consumption
```

Identify what valuable state is reachable, who may grant it, what evidence authorizes it, what durable state is written, where access is enforced, and how value is consumed. Map client, application, database, administrator, queue, event, reconciliation, and external-authority boundaries.

## Invariants

- Commercial value must not exceed exact authorized entitlement.
- Payment-backed value requires corresponding authoritative payment state.
- A grant must bind to the correct account, customer, order, product, object, and quantity.
- One authority event must not create duplicate entitlement or quota.
- Revocation, expiry, refund, and downgrade must not be undone by stale evidence.
- Freshness and state transitions must not regress authoritative value.
- Consumption must not exceed effective entitlement.
- Reconciliation must not restore, misbind, or multiply value.

Derive policy-sensitive details from the context artifact. Do not impose a universal provider state machine.

## Entitlement and consumption

Model separately:

```text
grant → available entitlement → consumption → residual entitlement
```

Refund, cancellation, downgrade, or revocation does not automatically reverse consumed value. Use the recorded product policy and authority contract.

## Lifecycle and transition model

Derive states and transitions from implementation, schema, jobs, reconciliation, tests, product policy, and authoritative external contract where materially relevant. Record source evidence, authority, effective rule, entitlement effect, freshness rule, and replay/order rule. Include activation, trial, cancellation, expiry, delinquency/grace, refund, dispute, pause/resume, upgrade/downgrade, replacement, restoration, quota cycle, and reconciliation only when supported by evidence.

Do not assume payment failure immediately revokes value. Do not treat a provider state as product policy. Do not use missing application handling to declare an external state impossible.

## Authority lineage

Whenever incoming identity differs from current binding, partition it before judgment:

- `CURRENT`;
- `PRIOR / SUPERSEDED`;
- `GENUINELY NEW / NEVER-CURRENT`; or
- `UNKNOWN LINEAGE`.

Use current and historical identity fields, event ledgers, replacement markers, audit records, migrations, persisted prior IDs, and transition history where available. Do not invent lineage or merge materially different classes.

When identity differs, partition the branch structurally into `CURRENT`, `PRIOR_SUPERSEDED`, `GENUINELY_NEW`, or `UNKNOWN` lineage as applicable. Terminality does not erase lineage: once B validly supersedes A, A remains superseded across later inactive, expired, revoked, refunded, or terminal states. Rebinding requires an independent authoritative transition. A missing history distinction is a finding mechanism only when the security invariant requires it and the complete deterministic value path is established.

### Terminality Does Not Erase Lineage

Inactive, expired, revoked, refunded, cancelled, or terminal status changes activity; it does not erase that B superseded A. A remains prior/superseded after B becomes terminal unless an authoritative transition specifically restores A.

### Supersession Persistence Invariant

Once B validly supersedes A, A must not regain current grant authority solely because B later becomes non-effective or an active-current guard stops applying. Restoration requires independent evidence that specifically re-authorizes A.

### Rebind authorization

Acceptance eligibility is not rebind authority. Require an explicit new creation, replacement, migration, administrative, reconciliation, or restoration transition. A genuinely new object may be legitimate; a known prior object needs separate re-authorization.

If history is absent, ask whether the invariant requires distinguishing new from prior. Missing history alone is not a finding. It becomes a possible mechanism only when the application cannot distinguish stale prior authority and deterministically restores commercial value through a valid reachable input.

## Reconciliation, retry, and partial failure

Review webhook/event synchronization and reconciliation independently. Test stale state, missing objects, wrong bindings, repeated quota initialization, delayed retries, duplicate delivery, and event/reconciliation races. At every partial-failure boundary ask what privileged value survives and whether it remains authorized.

## Fail closed and enforce

Unknown identity, product, variant, signature, event, or impossible transition must not silently create paid value. A correct billing row is insufficient if downstream enforcement is absent; actual feature, quota, seat, export, storage, and API gates are part of the graph.
