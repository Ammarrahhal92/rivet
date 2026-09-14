# RivetClose

**Version:** `0.1.1` · **Status:** Methodology frozen; release-ready; intended initial public release; not yet publicly published.

RivetClose performs evidence-based remediation and closure of canonical
`READY` findings produced by RivetTriage. It repairs the bounded defect,
verifies the restored invariant, and records auditable closure evidence.

## What it does not do

RivetClose does not perform broad discovery, canonical triage,
unrelated refactoring, or deployment. It does not redo Triage identity,
deduplication, provenance, or severity decisions.

## Input and workflow

The authoritative input is the current RivetTriage canonical register. Only
findings marked `READY` are admitted:

```text
READY admission
→ closure contract
→ bounded remediation
→ exact and invariant verification
→ fresh independent closure challenge
→ auditable closure reports
```

Public closure outcomes include `CLOSED VERIFIED`, `FIXED — VERIFICATION
INCOMPLETE`, `PARTIALLY REMEDIATED`, `NOT FIXED`, and the applicable blocked or
not-attempted states.

## Invocation

```text
$rivet-close Close the ready findings in this repository.
```

## Output

Closure reports are written under:

```text
docs/reviews/closure/
├── 00-rivet-close-summary.md
├── closure-register.md
├── verification-evidence.md
└── blocked-findings.md
```

## Rivet family

The current publication scope contains exactly four independently usable
skills:

```text
RivetChaos / RivetPay → RivetTriage → RivetClose
```

Chaos and Pay provide discovery/review material, Triage owns family-level
canonicalization and `READY` handoff, and Close owns bounded remediation and
verified closure. Pay remains optional and domain-specific.

## License

RivetClose is released under the [MIT License](LICENSE).
