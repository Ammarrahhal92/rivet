# Judgment and Evidence

This reference owns independent candidate judgment, evidence sufficiency, false-positive control, finding admission, and severity. Treat each frozen candidate as an allegation and reopen the cited source.

## Judgment boundary

For every frozen candidate:

- validate root cause, source semantics, reachability, and complete value path;
- validate invariant and grant source;
- separate product-policy and provider-contract dependencies;
- classify authority lineage independently;
- determine whether runtime evidence is materially required;
- challenge middleware, signatures, semantic validation, constraints, transactions, idempotency, reconciliation, enforcement, and queue controls;
- deduplicate only when the defect is truly the same.

Write one judgment per candidate with status `CONFIRMED`, `NEEDS_REVIEW`, `REJECTED`, or `DUPLICATE`. Only `CONFIRMED` may receive P0–P3 severity and a public `RP-###` finding ID.

## Evidence Sufficiency Gate

Classify required evidence as:

- contract/invariant evidence;
- deterministic application semantics;
- external/authority-contract evidence; or
- runtime reproduction.

Before downgrading because evidence is unavailable, state the exact unresolved fact and ask whether its opposite resolution could invalidate the candidate. If no, the gap is supportive only. If yes, use `NEEDS_REVIEW` and a coverage outcome of `UNVERIFIED` or `INSUFFICIENT EVIDENCE` as appropriate.

A blocked test suite is an assurance limitation, not an automatic blocker. Existing tests are evidence, not authority merely because they exist. Provider fixtures are not required for a source-provable branch when the external input class is established and runtime cannot change the deterministic transition.

## Deterministic Source Proof Rule

Runtime reproduction is unnecessary for confirmation when:

1. the expected invariant is established;
2. valid or materially possible input/state is established;
3. the current path is reachable;
4. source/database semantics deterministically establish the transition;
5. unauthorized entitlement/value follows through enforcement or consumption; and
6. compensating controls are challenged.

Trace evidence → accepted mutation → authoritative state → entitlement/value → enforcement/consumption. Static suspicion alone is insufficient. Runtime is materially required for deployment configuration, nondeterministic scheduling, unavailable database isolation/transaction behavior, external responses, hardware/process behavior, or provider facts not established by reliable contract evidence.

## Realized-Value Gate

Separate a suspicious upstream condition from an unauthorized commercial result. A `FINDING` requires a complete evidence path from valid or reachable authority input through accepted mutation and authoritative state to a concrete paid entitlement, retained or restored access, tier/quota/credit increase, duplicated fulfillment, reuse across accounts/orders, or another realized commercial-value consequence. A second object, retry, timeout, or intermediate row is not that consequence unless the product/provider contract and application semantics establish the downstream transition. Confirmed judgments must record `realized_value_status: ESTABLISHED`, a meaningful `realized_value`, and a structured `value_path`. Deterministic source/database semantics can establish the path; runtime reproduction is not a veto when it cannot change it.

## Product-Policy Ambiguity Gate

If confirmation depends on a product-policy decision, the referenced policy claim must be `EXPLICIT` or otherwise sufficiently established. `AMBIGUOUS` and `UNSPECIFIED` policy block confirmation unless the judgment explicitly records a policy-independent invariant with its reason and evidence. Provider capability does not answer local policy. Preserve legitimate administrative, manual, trial, promotional, migration, and legacy grant sources.

## Provider-Contract Conflict Gate

Provider facts are structured separately from product policy and may be `ESTABLISHED`, `UNVERIFIED`, or `CONFLICTED`. Preserve material conflicts between authoritative sources rather than selecting the interpretation that yields a finding. A material conflicted fact cannot satisfy a confirmed judgment dependency; an irrelevant conflict does not block a provider-independent finding.

## Policy and lineage controls

Provider capability does not establish local policy. A materially policy-dependent candidate cannot be confirmed when policy is ambiguous or unspecified unless the invariant is policy-independent. For differing identity, distinguish current, prior/superseded, genuinely new, and unknown lineage. A prior object remains superseded across terminality and can return only through explicit re-authorization. Missing lineage history is a finding mechanism only when the invariant requires the distinction and the omission deterministically permits stale value restoration.

Administrative/manual value requires both reachable mutation and proof that the actor is outside intended authority. Permission names do not establish intent. A broader administrative authority may subsume narrower permissions. Resolve contradictions with the authority model before confirmation.

## Finding Admission Gate

Confirm only when all are established:

- material value/entitlement at risk;
- expected authority and invariant;
- reachable attack path or deterministic bad transition;
- current implementation mechanism;
- challenged compensating controls;
- concrete unauthorized value/state/consumption consequence; and
- independently justified severity.

Record an evidence matrix: invariant, application path, unauthorized value, external fact required/established, runtime materially required/available, and controls challenged. A runtime test is not required when no material claim depends on it. Do not admit a finding merely because a provider supports a state, an identity differs, a branch exists, or a test is missing.

Before confirmation, the canonical judgment must also carry meaningful, non-placeholder `target_value`, `invariant`, `attack_path`, `authority`, `realized_value`, `evidence_basis`, and `value_path` fields. Null, empty, `unknown`, `n/a`, `unspecified`, and equivalent placeholders are invalid. P1 is downstream of this gate and requires demonstrated material unauthorized commercial value; severity cannot substitute for evidence.

## Judgment output

Use `NEEDS_REVIEW` when a material provider, runtime, policy, authority, or lineage fact remains unresolved. Confirmed judgments require generation ID, frozen candidate SHA-256, freeze-root SHA-256, invariant/path/value evidence, explicit policy/provider resolutions, runtime fields, and a structured evidence matrix. Runtime is required only when the claim materially depends on runtime facts; deterministic source proof can otherwise confirm. Use `REJECTED` for disproven or non-violating candidates, and `DUPLICATE` only with a direct canonical non-duplicate candidate reference. Do not delete rejected or duplicate candidates. Public `RP-###` IDs are generated later and must not be authored here.
