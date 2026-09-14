# Verification Evidence

Record only evidence actually executed or directly established.

| Finding | Layer/type | Command / test / scenario | Expected | Observed | Result | Notes |
|---|---|---|---|---|---|---|
| RT-XXX | Pre-fix | | | | REPRODUCED / DETERMINISTICALLY ESTABLISHED / NOT SAFELY REPRODUCIBLE | |
| RT-XXX | Layer 1 — exact regression | | | | PASS / FAIL / BLOCKED | |
| RT-XXX | Layer 2 — invariant | | | | PASS / FAIL / BLOCKED | |
| RT-XXX | Fix challenge | | | | PASS / FAIL / BLOCKED | |
| RT-XXX | Layer 3 — relevant suite | | | | PASS / FAIL / BLOCKED | |
| RT-XXX | Layer 4 — broader validation | | | | PASS / FAIL / BLOCKED | |

## Failure attribution

| Command/test | Failure | Attribution | Finding impact |
|---|---|---|---|
| | | PRE-EXISTING FAILURE / REMEDIATION-INTRODUCED FAILURE / UNRELATED/UNRESOLVED | |

## Verification discipline

- Do not record commands that were not run.
- Do not report mock evidence as live-provider evidence.
- Do not report serial coverage as concurrency proof.
- Do not report repository-only changes as deployed production closure.
