# Rivet

Open-source agent skills for adversarial code review, payment and entitlement security, canonical triage, and evidence-based remediation.

[Website](https://ammarrahhal92.github.io/rivet/) · [GitHub](https://github.com/Ammarrahhal92/rivet) · [Releases](https://github.com/Ammarrahhal92/rivet/releases) · [MIT License](LICENSE)

Rivet is a published, methodology-frozen family of four independently installable Codex skills. Use the relevant skill for the review surface; the four do not always need to run together.

```text
RivetChaos ─┐
            ├─> RivetTriage ─> RivetClose
RivetPay ───┘
```

## Quick start

```bash
git clone https://github.com/Ammarrahhal92/rivet.git
```

Copy the package directory you need into `~/.codex/skills/`. For example, copy `rivet-chaos/` and invoke it with:

```text
$rivet-chaos Audit this repository.
```

## Why Rivet?

- Discovery is separated from family-level canonical triage and bounded closure.
- Current evidence and explicit uncertainty remain visible instead of being silently converted to certainty.
- Commercial authority gets a specialized review path when it is relevant.
- Each skill remains independently copyable and installable.

## Family roles

| Skill | Responsibility |
| --- | --- |
| [RivetChaos](rivet-chaos/README.md) | Broad persona-driven adversarial discovery. |
| [RivetPay](rivet-pay/README.md) | Specialized payment, grant, entitlement, quota, license, and commercial-value review. |
| [RivetTriage](rivet-triage/README.md) | Post-discovery normalization, canonical finding identity, deduplication, provenance, current-state reconciliation, severity reconciliation, and READY handoff. |
| [RivetClose](rivet-close/README.md) | Bounded remediation, regression verification, and evidence-based closure of canonical READY findings. |

Chaos can be used independently. Pay is useful only when commercial authority exists and is not required for non-commercial repositories. Triage accepts Chaos, Pay, or other explicit review material. Close consumes canonical READY findings from Triage. Chaos does not have to precede Pay, and Pay does not replace Triage.

## Current published releases

| Skill | Version | Invocation | State |
| --- | --- | --- | --- |
| RivetChaos | 0.2.4 | `$rivet-chaos Audit this repository.` | Published; methodology-frozen |
| RivetPay | 0.1.0 | `$rivet-pay Review this repository.` | Published; methodology-frozen |
| RivetTriage | 0.1.1 | `$rivet-triage Triage this repository.` | Published; methodology-frozen |
| RivetClose | 0.1.1 | `$rivet-close Close the ready findings in this repository.` | Published; methodology-frozen |

## When to use which skill

- Use RivetChaos when broad adversarial behavioral review is needed and misuse, workflow, concurrency, lifecycle, or edge-case discovery matters.
- Use RivetPay when the repository has commercial authority or entitlement behavior such as payments, subscriptions, licenses, quotas, credits, trials, or grants.
- Use RivetTriage when several review outputs need normalization, reconciliation, and one canonical current-state register.
- Use RivetClose when canonical READY findings need bounded remediation and evidence-based verification.

## Installation

Each package is independently installable as a Codex skill. Copy the package directory you need into:

```text
~/.codex/skills/
```

For example:

```text
rivet-chaos/  →  ~/.codex/skills/rivet-chaos/
rivet-pay/    →  ~/.codex/skills/rivet-pay/
```

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

These counts are package validation artifacts, not a guarantee that reviewed applications are secure or defect-free. They do not represent independently packaged public application-benchmark artifacts.

## License and contribution

Rivet is distributed under the [MIT License](LICENSE). Each package also carries its own MIT [LICENSE](rivet-chaos/LICENSE) so packages remain independently distributable. See [CONTRIBUTING.md](CONTRIBUTING.md) and [RELEASING.md](RELEASING.md) for project guidance.
