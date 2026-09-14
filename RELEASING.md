# Releasing Rivet

Rivet packages version independently. A package release should preserve the package directory as an independently installable skill and use the package's existing current release notes as the source for release content.

## Current intended release names

| Package | Intended tag | Recommended release title |
| --- | --- | --- |
| RivetChaos | `rivet-chaos-v0.2.4` | RivetChaos v0.2.4 |
| RivetPay | `rivet-pay-v0.1.0` | RivetPay v0.1.0 |
| RivetTriage | `rivet-triage-v0.1.1` | RivetTriage v0.1.1 |
| RivetClose | `rivet-close-v0.1.1` | RivetClose v0.1.1 |

Release notes should be derived from each package's existing current release-note file. The tags and releases above are intended names only; this local publication build creates none of them.

## Release checklist

- [ ] Verify the package version and canonical invocation.
- [ ] Run the package's existing tests and evals.
- [ ] Verify the package copy matches the frozen release package.
- [ ] Verify no `__pycache__`, `.pyc`, or `.pyo` files remain.
- [ ] Verify privacy and secret hygiene.
- [ ] Verify README and current release notes.
- [ ] Verify the package LICENSE and root licensing metadata.
- [ ] Create the package-specific prefixed tag.
- [ ] Create the package-specific GitHub Release.

## Initial public publication

The initial public transition for the current four-skill family is complete. Current package documents use durable release-state wording: each version is methodology-frozen and released as part of the initial public Rivet family.

Future package releases should update only the relevant current-state documentation as part of their own release process.
