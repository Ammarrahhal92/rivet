# Rivet

Rivet is a family of independently installable agent skills for adversarial review, specialized commercial-authority review, canonical triage, and evidence-based remediation and closure.

The current publication scope contains exactly four skills:

```text
RivetChaos ─┐
            ├─> RivetTriage ─> RivetClose
RivetPay ───┘
```

## Family roles

| Skill | Responsibility |
| --- | --- |
| [RivetChaos](rivet-chaos/README.md) | Broad persona-driven adversarial discovery. |
| [RivetPay](rivet-pay/README.md) | Specialized payment, grant, entitlement, quota, license, and commercial-value review. |
| [RivetTriage](rivet-triage/README.md) | Post-discovery normalization, canonical finding identity, deduplication, provenance, current-state reconciliation, severity reconciliation, and READY handoff. |
| [RivetClose](rivet-close/README.md) | Bounded remediation, regression verification, and evidence-based closure of canonical READY findings. |

The packages are methodology-frozen and released as the initial public Rivet family.

## Independent use

The four skills do not always need to run together.

- Use RivetChaos independently for broad adversarial behavioral discovery.
- Use RivetPay when payment, subscription, license, entitlement, quota, credits, trials, commercial access, or grant authority exists. Pay is not required for non-commercial repositories.
- Use RivetTriage when findings from Chaos, Pay, or another explicit review source need to become one current canonical register.
- Use RivetClose when canonical READY findings are ready for bounded remediation and verification.

Chaos does not have to precede Pay. Pay does not replace Triage. Close consumes canonical READY findings from Triage.

## Current release matrix

| Skill | Version | Invocation | State |
| --- | --- | --- | --- |
| RivetChaos | 0.2.4 | `$rivet-chaos Audit this repository.` | Methodology-frozen; release-ready |
| RivetPay | 0.1.0 | `$rivet-pay Review this repository.` | Methodology-frozen; release-ready |
| RivetTriage | 0.1.1 | `$rivet-triage Triage this repository.` | Methodology-frozen; release-ready |
| RivetClose | 0.1.1 | `$rivet-close Close the ready findings in this repository.` | Methodology-frozen; release-ready |

## When to use which skill

- Use RivetChaos when broad adversarial behavioral review is needed and misuse, workflow, concurrency, lifecycle, or edge-case discovery matters.
- Use RivetPay when the repository has commercial authority or entitlement behavior such as payments, subscriptions, licenses, quotas, credits, trials, or grants.
- Use RivetTriage when several review outputs need normalization, reconciliation, and one canonical current-state register.
- Use RivetClose when canonical READY findings need bounded remediation and evidence-based verification.

## Installation

Each package is independently installable as a Codex skill. Copy the package directory you need into the generic Codex skills destination:

```text
~/.codex/skills/
```

For example:

```text
rivet-chaos/  →  ~/.codex/skills/rivet-chaos/
rivet-pay/    →  ~/.codex/skills/rivet-pay/
```

Install only the packages relevant to the review. Each package remains independently copyable and installable.

## Output locations

- RivetChaos: `docs/reviews/personas/`
- RivetPay: `docs/reviews/payments/` and structured `_rivetpay/` artifacts where applicable
- RivetTriage: `docs/reviews/triage/`
- RivetClose: `docs/reviews/closure/`

## Validation evidence

The packages include methodology and evaluation evidence appropriate to each skill:

- RivetChaos: 35 declarative eval cases
- RivetPay: 210 methodology evals, 112 unit tests, and 7 regression fixtures
- RivetTriage: 56 declarative eval cases
- RivetClose: 75 declarative eval cases

These counts are package validation evidence, not proof that a reviewed application is secure or defect-free. They do not represent independently packaged public application-benchmark artifacts.

## License

Rivet is distributed under the [MIT License](LICENSE). Each package also carries its own MIT [LICENSE](rivet-chaos/LICENSE) so that packages remain independently distributable.
