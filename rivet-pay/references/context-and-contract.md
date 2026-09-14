# Context and Contract

This reference owns Phase 1. It builds the review context and policy contract without producing candidates, finding IDs, severity, remediation, or vulnerability verdicts.

## Context record

Record:

- repository, branch, revision, dirty state, and review mode;
- live-system scope and environment assumptions;
- commercial-value capabilities and enforcement locations;
- grant sources and authoritative systems;
- states, transitions, security-bearing predicates, and trust boundaries;
- provider-contract facts and their source;
- product-policy evidence and its confidence;
- contradictions, guarantees, unknowns, and open questions.

Do not discard inconvenient or conflicting evidence. A silent policy is not an affirmative policy.

## Product policy versus provider contract

Keep two evidence domains separate:

1. Product policy says what the reviewed product intends for access, grace, revocation, consumption, manual grants, recovery, and value limits.
2. Provider or external contract says what an external authority can produce, how identities and environments work, and what event or state semantics exist.

A provider-supported state establishes possible external input; it does not by itself establish immediate revocation, retained access, recovery policy, or a product invariant. If the product explicitly delegates policy to the external contract, record that delegation as evidence. Otherwise use policy states:

- `EXPLICIT`;
- `STRONGLY_RECONSTRUCTED`;
- `AMBIGUOUS`; or
- `UNSPECIFIED`.

A later judgment may not confirm a candidate that materially depends on `AMBIGUOUS` or `UNSPECIFIED` policy unless the judge proves the violated invariant is policy-independent.

## External-state applicability

Before a lifecycle or provider family can be considered not applicable, positively establish that the authoritative contract does not expose the state, the product/payment model cannot produce it, or the reviewed commercial capability does not exist. Missing handlers, normalizers, local rows, or tests are not proof.

When a provider fact materially affects applicability, event identity, ordering, freshness, environment/store/account separation, refund/dispute behavior, trial behavior, or delinquency semantics, record separately:

- repository-proven facts;
- authoritative external-contract facts; and
- unresolved facts.

Consult reliable external documentation read-only only when it changes classification. Do not invent provider behavior.

Provider facts must preserve material disagreement: use `ESTABLISHED` only when the relevant fact is resolved, `UNVERIFIED` when required evidence is absent, and `CONFLICTED` when authoritative sources materially disagree. A provider fact never automatically establishes a product-policy claim. A conflict that is irrelevant to a candidate's invariant need not block an otherwise independent judgment.

## Grant-source classification

Identify every legitimate grant source, including payment-backed, trial, administrative, promotional, migration/legacy, or another explicit source. A non-payment grant is not a payment bypass merely because no payment transaction exists. If commercial value lacks any defensible authority, record that as a context concern for later judgment rather than issuing a context-phase finding.

## Context artifact contract

`_rivetpay/context.json` and `_rivetpay/policy-contract.json` are factual inputs. They must be valid JSON objects and must not contain final outcome, finding, severity, or remediation fields. The policy contract mechanically separates required `product_policy_claims` from `provider_contract_facts`; product IDs use `POL-###` and provider facts use `PCF-###`. They may contain `unknowns`, `contradictions`, `assumptions`, `guarantees`, and `open_questions`. Provider facts never silently satisfy a product-policy dependency.

The context phase ends only when the reviewer can explain what is known, what is policy, what is external authority, and what remains unresolved. It does not decide whether any candidate is true.
