# RivetTriage v0.1.1

## Evidence-lineage hardening

RivetTriage now records evidence origin and distinguishes independent,
derivative, shared-origin, and unknown-lineage evidence contributions.
Derivative and shared-origin artifacts remain fully accounted for but cannot
inflate independent corroboration. Current authoritative evidence remains
decisive for current-state reconciliation, and lineage remains separate from
finding identity, severity, and RivetClose readiness.

This release adds focused anti-source-laundering evaluation coverage. No new
canonicalization algorithm, runtime functionality, or external dependency is
introduced.

## Release state

The methodology is frozen and release-ready as the intended initial public
release. It has not yet been publicly published. Prior repository benchmark
validation was internal; benchmark artifacts are not packaged as independently
inspectable public evidence.
