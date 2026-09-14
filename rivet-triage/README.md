# RivetTriage

**Version:** `0.1.1` · **Status:** Methodology frozen; initial public release; released as part of the initial public Rivet family.

RivetTriage is the post-discovery reconciliation stage of the Rivet review flow:

```text
RivetChaos / RivetPay → RivetTriage → RivetClose
```

Invoke it with:

```text
$rivet-triage Triage this repository.
```

## What it does

RivetTriage accepts current review findings and relevant historical, remediation, closure, or issue context. It:

- inventories every source finding and preserves source accounting;
- establishes defect identity from operation, invariant, mechanism, affected boundary, behavior, and remediation class;
- identifies exact duplicates, partial overlaps, related-distinct findings, independent findings, and unresolved relationships;
- verifies whether a source claim survives current implementation, invariant, behavior, controls, and reachability checks before admitting it as a current finding;
- assigns canonical `RT-*` findings with current-state status and provenance;
- reconciles severity from current reachable impact, with bounded real defects defaulting to `P3` unless material `P2` evidence is independently justified;
- records unresolved candidates when identity, contract, or current state cannot be established; and
- prepares findings for RivetClose with explicit handoff readiness.

RivetTriage owns family-level canonical identity and deduplication. Any
candidate-level hygiene performed inside a discovery skill remains local to
that review and does not replace Triage’s cross-source canonical register.

Primary inputs may include RivetChaos or RivetPay reports, another explicit review report, issue or audit documents supplied as current inputs, and clearly identified historical or remediation context. The resulting reports belong under `docs/reviews/triage/`.

## What it does not do

RivetTriage does not perform broad new discovery, rerun discovery/review skills, or replace specialist review. It does not remediate product code, configuration, tests, infrastructure, deployment, or data. It does not merge findings by title, subsystem, severity, reviewer count, or shared remediation direction, and it does not treat historical closure language as current proof.

## Outputs

The canonical register records the supported claim, invariant, current evidence, reachability, controls, impact, severity basis, source mappings, provenance, current-state verification, remediation direction, and RivetClose handoff state. Every source finding is accounted for, including findings that are rejected, fixed, stale, unverified, superseded, or left unresolved.

See [SKILL.md](SKILL.md) for the complete operating rules.
