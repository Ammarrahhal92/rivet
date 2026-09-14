# RivetPay v0.1.0

## Release state

RivetPay v0.1.0 is the methodology-frozen initial public release, released as
part of the initial public Rivet family.

## What RivetPay does

RivetPay is a provider-neutral Agent Skill for adversarial review of payment, billing, grant, quota, license, seat, order, and entitlement authority. It traces commercial value from authority and evidence through entitlement enforcement and consumption.

## Major capabilities

- Value Authority Graph analysis.
- Multiple legitimate grant-source models, including payment-backed, trial, administrative, promotional, and migration/legacy grants.
- Lifecycle, identity, replacement, refund, dispute, reconciliation, quota, and consumption review.
- Separate product-policy and provider-contract evidence.
- High-recall discovery with conservative judgment and deterministic artifact validation.
- Generation-bound freeze, canonical findings, deterministic reports, and tamper detection.

## Intended users

Developers, security reviewers, coding agents, and engineering teams reviewing payment or commercial-entitlement behavior in authorized repositories and controlled test systems.

## Basic invocation

```text
$rivet-pay Review this repository.
```

## Important limitations

RivetPay is discovery-only by default and does not remediate product code or modify production state. Source proof may not establish external provider behavior, deployment configuration, database scheduling, or other runtime facts. Some branches may remain `NEEDS_REVIEW` or `INSUFFICIENT_EVIDENCE`; results should be verified before remediation where external semantics matter.

## Validation summary

Version 0.1.0 passed the package's deterministic validation suite, including 112 unit tests, 210 methodology evals, and 7 structural regression fixtures. Pre-release validation exercised multiple materially different commercial models, including recurring subscription with quota lifecycle, one-time lifetime/license entitlement, and a repository without an implemented payment or commercial-entitlement domain. This validation does not guarantee security or complete vulnerability detection.

## Known boundaries

- Source evidence may establish a dangerous code path without proving every external runtime or provider condition.
- Some branches may remain `NEEDS_REVIEW` or `INSUFFICIENT_EVIDENCE`.
- Findings should be verified before remediation when external semantics matter.
- RivetPay does not replace provider documentation, application tests, or production-safe validation.

## Upgrade notes

This is the initial public release. There are no prior public-version migration
requirements.
