# RivetClose v0.1.1

## Release state

The RivetClose methodology is frozen and release-ready as the intended initial
public release. It has not yet been publicly published.

## What RivetClose does

RivetClose consumes canonical `READY` findings from RivetTriage, performs
bounded evidence-based remediation, verifies the restored invariant, and
records auditable closure evidence.

It is not a discovery skill, a second triage pass, a generic autonomous fixer,
or a deployment workflow.

## What's notable in v0.1.1

- Fresh Independent Closure Challenge before verified closure.
- Portable logically separate fallback when an isolated reviewer is
  unavailable.
- Demonstrated equivalent-path bypasses prevent `CLOSED VERIFIED`.
- Speculation alone does not block closure.
- Legitimate behavior preservation remains required.

## Validation materials

The package contains 75 declarative evaluation cases. No external benchmark
claim is made by this release note.

## Invocation

```text
$rivet-close Close the ready findings in this repository.
```

## Output

Closure reports are written under `docs/reviews/closure/`.
