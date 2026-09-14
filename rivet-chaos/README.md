# RivetChaos

**Version:** `0.2.4` · **Status:** Methodology frozen; initial public release; released as part of the initial public Rivet family

RivetChaos is an adversarial behavioral review skill for established software repositories with an identifiable product/system contract. It examines how realistic confused, curious, chaotic, and limit-abusing behavior can challenge important product invariants. RivetChaos is discovery-only: it records evidence and remediation direction, but does not fix findings.

The canonical skill identifier is `rivet-chaos`, and its invocation is `$rivet-chaos`.

## What it reviews

RivetChaos is intended for repositories where the available evidence identifies the important:

- actors and trust boundaries;
- workflows and user-visible behavior;
- state and lifecycle transitions;
- ownership and authorization rules;
- business invariants;
- limits and resource boundaries;
- destructive, partial, and recovery behavior.

Documentation does not need to be exhaustive. Git history, complete test coverage, and a runnable runtime are helpful but not mandatory when repository evidence can establish the relevant contract.

## Adversarial lenses

- **CU — Confused User:** misunderstanding, stale UI, repeated actions, partial completion, recovery, and plausible input mistakes.
- **CR — Curious User:** alternate IDs or routes, hidden states, unusual sequencing, ownership exploration, and stale privileged actions.
- **CH — Chaos User:** concurrency, rapid repeats, retries, interruption, stale state, race conditions, and duplicate side effects.
- **LA — Limit-Abuse User:** quotas, batch/resource limits, expensive operations, rate limits, repeated entitlements, and authoritative enforcement.

These are adaptive lenses, not fixed scripts. The repository’s identifiable contract determines which scenarios matter.

## What it is not

RivetChaos is not:

- a general code linter;
- a static security scanner;
- a penetration-testing tool;
- a requirements-discovery tool for completely undocumented raw code;
- a remediation or triage skill;
- a generic fuzzing framework;
- a replacement for specialist security, performance, or architecture reviews.

## Review flow

```text
Minimum Review Baseline
→ Coverage Map
→ Broad Adversarial Discovery
→ Candidate Findings
→ Self-Challenge
→ Bounded Same-Mechanism Sibling Sweep
→ Adversarial Path Closure
→ Final Classification
→ Coverage Completion
```

Self-challenge is a precision filter applied after broad discovery. It checks relevant surrounding execution layers and compensating controls; it must not suppress relevant scenario generation.

## Outcomes

- `FINDING` — a concrete failure is supported by repository or runtime evidence.
- `ALREADY RESILIENT` — a meaningful adversarial scenario is blocked by sufficient controls.
- `UNVERIFIED` — the scenario is relevant, but material evidence is unavailable.
- `NOT APPLICABLE` — the scenario does not apply to the implementation.
- `INSUFFICIENT REVIEW BASELINE` — the repository does not expose enough identifiable contract to perform a meaningful review without inventing product intent.

## Findings and reports

Findings record the ID, severity, attempted behavior, expected invariant, actual behavior, evidence, impact, remediation direction, verification criteria, and relevant reachability, controls, overlap, and status information. Findings are not forced when evidence is insufficient or when controls preserve the invariant.

The required reports are created under `docs/reviews/personas/`:

```text
docs/reviews/personas/
├── 00-rivet-chaos-summary.md
├── 01-confused-user.md
├── 02-curious-user.md
├── 03-chaos-user.md
└── 04-limit-abuse-user.md
```

## Installation and minimal usage

Place this directory in the host’s supported skill directory and register it using that host’s supported skill-installation mechanism. This bundle does not prescribe a package manager or distribution service.

Use the canonical identifier `rivet-chaos` and invoke it with:

```text
$rivet-chaos Audit this repository.
```

## Scope and limitations

Repository evidence governs conclusions. Unknown product intent must not become a finding. Missing runtime execution does not prevent a statically proven defect or defense, while runtime-dependent scenarios may remain `UNVERIFIED`. Severity is based on practical reachable impact after compensating controls are considered. RivetChaos does not force findings.

## Package structure

```text
rivet-chaos/
├── SKILL.md
├── README.md
├── LICENSE
├── CHANGELOG.md
├── RELEASE_NOTES_0.2.2.md
├── RELEASE_NOTES_0.2.3.md
├── RELEASE_NOTES_0.2.4.md
├── assets/
│   └── report-template.md
├── evals/
│   └── evals.json
└── references/
    ├── evidence-rules.md
    └── persona-method.md
```

## Development status

RivetChaos `0.2.4` is methodology-frozen and is the initial public release, released as part of the initial public Rivet family. This refinement adds a mandatory adversarial path closure gate that preserves actor/object identity, cardinality, state transitions, and consequence support before a finding is confirmed. External usage and feedback are welcome. The API, report format, and methodology are frozen for version `0.2.4`.
