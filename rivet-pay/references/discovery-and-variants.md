# Discovery and Variants

This reference owns high-recall discovery, candidate persistence, security-bearing predicate inventory, and one-axis-at-a-time variant expansion. Discovery records allegations; it does not assign severity or final outcomes.

## Candidate discipline

For every plausible material path write a candidate artifact with:

- stable discovery ID `RPC-###`;
- title, hypothesis, target value, expected authority, and attacked evidence;
- exact source locations and reachable preconditions;
- root cause and exact seed;
- invariant under test;
- candidate expansion axes and stop reason;
- related material branch IDs.

Do not discard a candidate because it may be a false positive. Later judgment may confirm, reject, mark `NEEDS_REVIEW`, or deduplicate it. A duplicate remains persisted and points to its canonical candidate.

## Discovery seeds

Inspect, where present:

- client completion, redirects, and plan selection;
- event authenticity and semantic validation;
- replay, idempotency, ordering, retries, and reconciliation;
- account/customer/order/object binding;
- amount, quantity, product, variant, and tier mapping;
- activation, grace, cancellation, expiry, refund, dispute, recovery, replacement, and restoration;
- administrative, trial, promotional, migration, seed, and manual grant paths;
- quota initialization, reset, rollover, concurrent consumption, and downgrade residue;
- partial persistence, queue delivery, and downstream entitlement enforcement.

Ask how each edge of the Value Authority Graph could be forged, replayed, duplicated, reordered, misbound, stale, raced, or partially committed.

## Predicate coverage inventory

Inventory only implementation predicates that can materially change grant authority, identity, lifecycle, evidence acceptance, entitlement, quota, freshness, binding, retry, or commercial value. For each record control purpose, protected branch, opposite branch, value consequence, and authority consequence. Logging, metrics, presentation, and formatting conditions are not obligations.

If a security-bearing condition controls a defense, explicitly inspect its opposite branch. In compound conditions, vary the control-activation condition rather than generating every combination. Couple state-dependent predicates to the application-derived lifecycle model.

## Lineage-aware expansion

Whenever identity differs, create separate material branch rows for `CURRENT`, `PRIOR / SUPERSEDED`, `GENUINELY NEW / NEVER-CURRENT`, and `UNKNOWN LINEAGE` when evidence supports or leaves those possibilities open. Terminality does not erase supersession. A genuinely new object may be legitimate; a prior object requires explicit re-authorization.

## Root-cause variants

After a material seed:

1. state the root cause and exact seed;
2. list meaningful axes;
3. expand one axis at a time;
4. record new branch rows and candidates;
5. challenge compensating controls;
6. record why expansion stops.

Do not vary identity, lifecycle, timing, provider, grant source, and concurrency simultaneously without evidence that each axis changes authority or value. A branch discovered from implementation structure must be reviewed even if no catalog seed names it.

## Discovery output

`branches.json` is the complete material-branch inventory. It contains a registry of material families and each material row must include a stable branch ID, `family_id`, predicate/control, condition, authority identity/state, one `authority_lineage`, `lineage_sensitive`, candidate IDs, evidence questions, and materiality. A lineage-sensitive group is split into separate branch IDs for materially different lineage classes; it does not need every possible class. It contains no final verdict or severity. Candidates are allegations only: final/judgment fields are forbidden at the top level, while nested application state may use names such as `status`. Candidates and branch rows are append/update artifacts, not transient model notes.
