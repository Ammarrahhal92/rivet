# Changelog

## [0.2.4] - 2026-09-14

- Added a mandatory adversarial path closure gate before confirming findings.
- Added actor/object identity, cardinality, initial-state, transition, and consequence accounting.
- Added same-target versus distinct-target reasoning and a literal-execution counterfactual challenge.
- Extended the declarative eval corpus with focused path-closure and cardinality cases.

## [0.2.3] - 2026-09-13

- Added bounded same-mechanism sibling discovery with explicit trigger, stop, and independent-outcome rules.
- Added actor capability constraints and research-versus-reporting scope separation.
- Clarified that cross-persona recurrence is corroboration, not proof or severity escalation.
- Required the actor action → reachable mechanism → violated invariant → supported consequence reasoning path.
- Extended the declarative eval corpus with focused sibling, capability, scope, recurrence, and RivetTriage-boundary cases.

## [0.2.2] - 2026-09-06

- Clarified the established-contract repository scope.
- Added the lightweight Minimum Review Baseline and explicit coverage completion.
- Preserved broad adversarial discovery before post-discovery self-challenge.
- Strengthened execution-context validation, reachability, compensating-control, and impact-first severity guidance.
- Balanced the discovery/precision eval suite while retaining discovery-only behavior.

## [0.2.1]

- Added stronger false-positive defenses and execution-context tracing.
- Added reachability and blast-radius analysis.
- Tightened severity calibration.

## [0.2.0]

- Expanded concurrency, idempotency, and lifecycle analysis.
- Added partial-success and representation-boundary coverage.
- Improved resilience and `UNVERIFIED` handling.
- Broadened the use of repository evidence.

## [0.1.0]

- Initial RivetChaos package.
- Introduced the four personas and discovery-only workflow.
- Added evidence rules, five-report output structure, and the initial eval suite.
