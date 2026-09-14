# RivetChaos v0.2.2

RivetChaos v0.2.2 is the first pre-release and release-candidate-quality package of the adversarial behavioral review skill. It is intended for external usage and feedback while the project remains pre-1.0; it has not yet been publicly published.

## What it does

RivetChaos applies four adaptive adversarial lenses—Confused User, Curious User, Chaos User, and Limit-Abuse User—to established software repositories. It is discovery-only: it identifies evidence-backed findings and resilient behavior without modifying the reviewed system.

## What's notable in v0.2.2

- Coverage-first review of important contract surfaces.
- Clear scope for repositories with an identifiable product/system contract.
- Self-challenge applied after discovery as a precision filter.
- Execution-context-aware false-positive defense.
- Reachability-aware impact assessment.
- Impact-first severity calibration.
- Meaningful `ALREADY RESILIENT` and `UNVERIFIED` outcomes.

## Intended users

RivetChaos is intended for software teams, maintainers, reviewers, AI-assisted development workflows, and developers seeking adversarial behavioral review before release.

## Current limitations

- Requires an identifiable product/system contract.
- Is not a remediation tool or a replacement for specialist security reviews.
- Runtime-dependent scenarios may remain `UNVERIFIED`.
- Pre-1.0 behavior and report details may evolve.

## Installation / invocation

Place the bundle in the host’s supported skill directory and use the canonical identifier `rivet-chaos`. This package does not define a package manager or distribution mechanism.

Minimal invocation:

```text
$rivet-chaos Audit this repository.
```

## Release status

**Pre-release.** This package has not yet been publicly published. External feedback is welcome; this is not a stable 1.0 release.
