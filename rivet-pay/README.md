# RivetPay

**Version:** `0.1.0` · **Status:** Methodology frozen; initial public release; released as part of the initial public Rivet family.

## Adversarial Payment & Entitlement Reviewer for Coding Agents

RivetPay is a provider-neutral Agent Skill for reviewing how software creates, changes, preserves, enforces, and consumes commercial value. It helps coding agents examine payment and entitlement behavior with source-aware, evidence-driven reasoning and deterministic review artifacts.

## What RivetPay is

RivetPay reviews commercial-value paths such as payments, subscriptions, one-time purchases, license-key activation, trials, administrative and promotional grants, refunds, disputes, quotas, credits, entitlement enforcement, lifecycle transitions, reconciliation, and provider event handling.

Its core principle is:

> Commercial value must never exist, persist, increase, restore, or be consumed beyond the exact entitlement authorized by its authoritative grant source.

For payment-backed value, there must be corresponding authoritative payment state.

## What RivetPay is not

RivetPay is not a payment-provider certification, a PCI assessment, a provider penetration test, or a guarantee of security or complete vulnerability detection. It does not make purchases, contact providers, change production state, or automatically remediate product code. A reported scenario still requires appropriate developer and runtime verification before remediation when external semantics matter.

## Core review model

RivetPay reconstructs the Value Authority Graph:

```text
authority → evidence → interpretation → grant state → entitlement → enforcement → consumption
```

The review separates entitlement from consumption, identifies security-bearing state and identity transitions, challenges replay and reconciliation behavior, and preserves uncertainty when provider or runtime facts are unavailable. Its structured gate validates generation/freeze integrity, candidate judgments, branch coverage, finalization, rendering, and tamper resistance.

## What it reviews

- payment-backed and non-payment grant paths;
- recurring and one-time commercial models;
- provider events, webhooks, refunds, disputes, cancellation, and dunning;
- license, seat, quota, credit, usage, and entitlement enforcement;
- lifecycle, replacement, restoration, freshness, replay, and reconciliation transitions;
- account, customer, order, and authority binding.

## Grant-source model

RivetPay does not assume every paid feature comes from a recurring subscription. It distinguishes payment-backed, trial, administrative, promotional, and migration/legacy grants, along with other explicitly documented sources. A legitimate non-payment grant is not a payment bypass merely because no payment transaction exists.

A repository with no implemented payment or commercial-entitlement domain is also a valid review result. RivetPay should record that boundary rather than fabricate payment findings.

## Finding / judgment outcomes

RivetPay should discover aggressively, classify conservatively, and state uncertainty explicitly. Judgments use the existing vocabulary:

- `FINDING` — a demonstrated current commercial-value invariant violation;
- `NEEDS_REVIEW` — judgment remains dependent on material unresolved evidence;
- `INSUFFICIENT_EVIDENCE` — the available record cannot establish the claim;
- `HARDENING_ONLY` — an improvement is useful without a demonstrated current violation;
- `DEFENDED` — the reviewed branch is protected within the evidence scope;
- `NOT_APPLICABLE` — positive contract or product-model evidence excludes the branch.

Findings may still contain provider- or runtime-dependent branches requiring developer verification. Uncertainty is retained rather than silently converted into a vulnerability.

RivetPay may consolidate duplicate candidates within its own review as local
candidate hygiene. This does not replace RivetTriage’s family-level,
cross-source canonical identity and deduplication.

## Installation

Copy the `rivet-pay` directory into the user's Codex skills directory:

```powershell
Copy-Item -Recurse -Force .\rivet-pay "$env:CODEX_HOME\skills\rivet-pay"
```

Use the equivalent path for a local Codex installation when `CODEX_HOME` is not set.

## Invocation

```text
$rivet-pay Review this repository.
```

## Review artifacts

The default workflow is discovery-only. It creates structured review artifacts under the reviewed repository's `_rivetpay/` directory and deterministic public reports under `docs/reviews/payments/`. Candidates survive discovery freeze; judgments, branch outcomes, canonical findings, and aggregate totals are validated before reports are rendered.

The [runtime specification](SPEC.md), [context and contract guidance](references/context-and-contract.md), [judgment guidance](references/judgment-and-evidence.md), and [artifact contract](references/reporting-and-artifacts.md) describe the maintained interfaces.

## Safety and scope

RivetPay reviews authorized repositories and controlled test systems only. It is discovery-only by default: it reviews, reconstructs authority and state, and reports findings; it does not automatically remediate product code. It does not deploy, mutate live customer state, rotate secrets, make purchases or refunds, or contact payment providers.

## Limitations

Source evidence can establish a dangerous code path without proving every external provider, deployment, database, scheduling, or production condition. Some branches may remain `NEEDS_REVIEW` or `INSUFFICIENT_EVIDENCE`. RivetPay does not replace provider documentation, application tests, or production-safe validation, and its results do not prove that every reported scenario is exploitable in production.

## Validation / benchmark status

Version 0.1.0 has been validated with the package's deterministic methodology checks, including 210 methodology evals, 112 unit tests, and 7 structural regression fixtures. Pre-release validation exercised RivetPay against multiple materially different commercial models to test portability, false-positive resistance, authority reconstruction, and non-applicable-domain handling, including recurring subscription plus quota lifecycle, one-time lifetime/license entitlement, and a repository with no implemented payment or commercial-entitlement domain. These are package validation claims, not independently packaged application-benchmark evidence, and they do not establish complete security.

## Rivet family context

RivetPay is the payment and commercial-entitlement discovery specialist in the current four-skill Rivet family. RivetChaos provides broad adversarial discovery; RivetTriage owns family-level canonicalization and current-state reconciliation; RivetClose owns bounded remediation and verified closure. Each skill remains independently usable, and Pay is domain-specific rather than mandatory for every repository. See [SOURCES.md](SOURCES.md) for the maintainer source inventory.

## License

RivetPay is released under the [MIT License](LICENSE).
