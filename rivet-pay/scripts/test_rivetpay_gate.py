#!/usr/bin/env python3
"""Explicit architecture tests for the deterministic RivetPay gate."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import rivetpay_gate as gate  # noqa: E402


class GateTests(unittest.TestCase):
    def write_review_files(self, root: Path, *, policy_status: str = "EXPLICIT", provider_status: str = "ESTABLISHED", lineage: str = "CURRENT", lineage_sensitive: bool = False, second_branch: bool = False, candidate_deps: bool = False, provider_material: bool = True) -> None:
        gate.init(root)
        policy = {"schema_version": 2, "product_policy_claims": [], "provider_contract_facts": [], "grant_authorities": [], "contradictions": [], "unknowns": [], "open_questions": []}
        if candidate_deps:
            policy["product_policy_claims"] = [{"id": "POL-001", "topic": "grant policy", "statement": "grant is allowed", "status": policy_status, "delegated_to_provider": False, "evidence": ["contract", "usage"] if policy_status == "STRONGLY_RECONSTRUCTED" else (["contract"] if policy_status == "EXPLICIT" else []), "contradictions": []}]
            policy["provider_contract_facts"] = [{"id": "PCF-001", "topic": "external state", "statement": "state is valid", "status": provider_status, "source_kind": "OFFICIAL_PROVIDER", "source": "contract", "evidence": ["contract"], "conflicts": ["source disagreement"] if provider_status == "CONFLICTED" else []}]
        gate.write_json(gate.safe_child(root, "_rivetpay", "policy-contract.json"), policy)
        families = [{"id": "RPF-001", "name": "synthetic family", "material": True}]
        branches = [{"branch_id": "RPB-001", "family_id": "RPF-001", "predicate": "authority_guard", "condition": "current state", "authority_lineage": lineage, "lineage_sensitive": lineage_sensitive, "lineage_group": "RPLG-001" if lineage_sensitive else None, "material": True, "candidate_ids": ["RPC-001"]}]
        if second_branch:
            branches.append({"branch_id": "RPB-002", "family_id": "RPF-001", "predicate": "authority_guard", "condition": "terminal state", "authority_lineage": "GENUINELY_NEW", "lineage_sensitive": True, "lineage_group": "RPLG-001", "material": True, "candidate_ids": ["RPC-002"]})
        gate.write_json(gate.safe_child(root, "_rivetpay", "branches.json"), {"schema_version": 2, "families": families, "branches": branches})
        candidate = {"candidate_id": "RPC-001", "title": "Synthetic deterministic value violation", "hypothesis": "valid input reaches unauthorized value", "target_value": "synthetic entitlement", "expected_authority": "synthetic authority", "invariant": "value requires exact authority", "attack_path": "valid authority evidence -> state mutation -> paid capability", "realized_value": "unauthorized paid capability", "realized_value_status": "ESTABLISHED", "root_cause": "weak binding", "exact_seed": "valid input reaches grant", "source_evidence": ["app/handler"], "branch_ids": ["RPB-001"]}
        if candidate_deps:
            candidate["policy_dependencies"] = [{"policy_id": "POL-001", "material": True, "reason": "policy determines claim"}]
            candidate["provider_dependencies"] = [{"provider_fact_id": "PCF-001", "material": provider_material, "reason": "provider state determines reachability"}]
        gate.write_json(gate.safe_child(root, "_rivetpay", "candidates", "RPC-001.json"), candidate)
        if second_branch:
            candidate2 = dict(candidate, candidate_id="RPC-002", title="Second candidate", branch_ids=["RPB-002"], policy_dependencies=[], provider_dependencies=[])
            gate.write_json(gate.safe_child(root, "_rivetpay", "candidates", "RPC-002.json"), candidate2)

    def make_review(self, root: Path, *, status: str = "CONFIRMED", outcome: str = "FINDING", policy_status: str = "EXPLICIT", provider_status: str = "ESTABLISHED", lineage: str = "CURRENT", lineage_sensitive: bool = False, candidate_deps: bool = False, second_branch: bool = False, provider_material: bool = True) -> dict:
        self.write_review_files(root, policy_status=policy_status, provider_status=provider_status, lineage=lineage, lineage_sensitive=lineage_sensitive, candidate_deps=candidate_deps, second_branch=second_branch, provider_material=provider_material)
        gate.validate_context(root)
        freeze = gate.freeze_discovery(root)
        for cid in ("RPC-001", "RPC-002") if second_branch else ("RPC-001",):
            candidate_path = gate.safe_child(root, "_rivetpay", "history", freeze["generation_id"], "candidates", f"{cid}.json")
            judgment = {"candidate_id": cid, "generation_id": freeze["generation_id"], "candidate_sha256": gate.sha256(candidate_path), "freeze_root_sha256": freeze["root_sha256"], "status": status}
            if status == "CONFIRMED":
                judgment.update({"severity": "P1", "title": "Synthetic finding", "target_value": "synthetic entitlement", "invariant": "value requires exact authority", "attack_path": "valid authority evidence -> state mutation -> paid capability", "authority": "synthetic authority", "realized_value": "unauthorized paid capability", "realized_value_status": "ESTABLISHED", "value_path": ["accepted evidence", "persisted grant", "paid capability"], "evidence_basis": ["app/handler", "entitlement enforcement"], "invariant_status": "ESTABLISHED", "reachability_status": "ESTABLISHED", "value_consequence_status": "ESTABLISHED", "controls_challenged": True, "runtime_required": False, "runtime_evidence_available": False, "runtime_reason": "deterministic source proof", "runtime_evidence": [], "policy_dependencies": [{"policy_id": "POL-001", "material": True, "resolution": "SATISFIED", "evidence": ["policy"]}] if candidate_deps else [], "provider_dependencies": [{"provider_fact_id": "PCF-001", "material": True, "resolution": "SATISFIED", "evidence": ["provider"]}] if candidate_deps else [], "evidence_matrix": {"invariant": "ESTABLISHED", "application_path": "ESTABLISHED", "value_consequence": "ESTABLISHED", "policy": "SATISFIED" if candidate_deps else "NOT_MATERIAL", "provider": "SATISFIED" if candidate_deps else "NOT_MATERIAL", "runtime": "NOT_REQUIRED", "controls_challenged": True}})
            gate.write_json(gate.safe_child(root, "_rivetpay", "judgments", f"{cid}.json"), judgment)
        rows = []
        for bid, cid, row_outcome in (("RPB-001", "RPC-001", outcome), ("RPB-002", "RPC-002", "DEFENDED")) if second_branch else (("RPB-001", "RPC-001", outcome),):
            rows.append({"branch_id": bid, "family_id": "RPF-001", "authority_lineage": lineage if bid == "RPB-001" else "GENUINELY_NEW", "outcome": row_outcome, "candidate_ids": [cid], "evidence_required": ["source"], "evidence_available": ["source"], "missing_material_evidence": []})
        gate.write_json(gate.safe_child(root, "_rivetpay", "coverage.json"), {"schema_version": 2, "generation_id": freeze["generation_id"], "freeze_root_sha256": freeze["root_sha256"], "branches": rows, "families": [{"family_id": "RPF-001", "branch_ids": [row["branch_id"] for row in rows]}]})
        return freeze

    def assert_gate_error(self, fn) -> None:
        with self.assertRaises(gate.GateError):
            fn()

    def test_A_valid_review_passes(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); self.make_review(root); self.assertEqual(gate.finalize(root)["verdict"], "FINDINGS CONFIRMED")

    def test_B_missing_judgment_fails(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); self.write_review_files(root); gate.validate_context(root); gate.freeze_discovery(root); self.assert_gate_error(lambda: gate.validate_judgment(root))

    def test_C_missing_material_branch_outcome_fails(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); self.make_review(root); c = gate.read_json(gate.safe_child(root, "_rivetpay", "coverage.json")); c["branches"] = []; gate.write_json(gate.safe_child(root, "_rivetpay", "coverage.json"), c); self.assert_gate_error(lambda: gate.validate_structured(root))

    def test_D_frozen_candidate_modification_fails(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); self.make_review(root); p = gate.safe_child(root, "_rivetpay", "candidates", "RPC-001.json"); p.write_text(p.read_text() + "\n", encoding="utf-8"); self.assert_gate_error(lambda: gate.validate_judgment(root))

    def test_E_frozen_candidate_deletion_fails(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); self.make_review(root); gate.safe_child(root, "_rivetpay", "candidates", "RPC-001.json").unlink(); self.assert_gate_error(lambda: gate.validate_judgment(root))

    def test_F_missing_duplicate_target_fails(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); self.make_review(root, status="DUPLICATE"); p = gate.safe_child(root, "_rivetpay", "judgments", "RPC-001.json"); j = gate.read_json(p); j["canonical_candidate_id"] = "RPC-999"; gate.write_json(p, j); self.assert_gate_error(lambda: gate.validate_judgment(root))

    def test_G1_duplicate_self_reference_fails(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); self.make_review(root, status="DUPLICATE"); p = gate.safe_child(root, "_rivetpay", "judgments", "RPC-001.json"); j = gate.read_json(p); j["canonical_candidate_id"] = "RPC-001"; gate.write_json(p, j); self.assert_gate_error(lambda: gate.validate_judgment(root))

    def test_G2_duplicate_two_node_cycle_fails(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); self.make_review(root, status="DUPLICATE", second_branch=True); self._set_duplicate(root, "RPC-001", "RPC-002"); self._set_duplicate(root, "RPC-002", "RPC-001"); self.assert_gate_error(lambda: gate.validate_judgment(root))

    def test_G3_duplicate_longer_cycle_fails(self):
        self.assert_gate_error(lambda: gate.validate_duplicate_graph({"A": {"status": "DUPLICATE", "canonical_candidate_id": "B"}, "B": {"status": "DUPLICATE", "canonical_candidate_id": "C"}, "C": {"status": "DUPLICATE", "canonical_candidate_id": "A"}}))

    def test_G4_duplicate_to_duplicate_chain_fails(self):
        self.assert_gate_error(lambda: gate.validate_duplicate_graph({"A": {"status": "DUPLICATE", "canonical_candidate_id": "B"}, "B": {"status": "DUPLICATE", "canonical_candidate_id": "C"}, "C": {"status": "CONFIRMED"}}))

    def _set_duplicate(self, root, cid, target):
        p = gate.safe_child(root, "_rivetpay", "judgments", f"{cid}.json"); j = gate.read_json(p); j["canonical_candidate_id"] = target; gate.write_json(p, j)

    def _write_dup(self, root, f, cid, target):
        path = gate.safe_child(root, "_rivetpay", "history", f["generation_id"], "candidates", f"{cid}.json")
        if not path.exists():
            j = {"candidate_id": cid, "title": cid, "branch_ids": ["RPB-001"], "policy_dependencies": [], "provider_dependencies": []}; gate.write_json(path, j)
        gate.write_json(gate.safe_child(root, "_rivetpay", "judgments", f"{cid}.json"), {"candidate_id": cid, "generation_id": f["generation_id"], "candidate_sha256": gate.sha256(path), "freeze_root_sha256": f["root_sha256"], "status": "DUPLICATE", "canonical_candidate_id": target})

    def _add_candidate_and_dup(self, root, f, cid, target):
        self._write_dup(root, f, cid, target)

    def test_H_confirmed_without_severity_fails(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); self.make_review(root); p = gate.safe_child(root, "_rivetpay", "judgments", "RPC-001.json"); j = gate.read_json(p); del j["severity"]; gate.write_json(p, j); self.assert_gate_error(lambda: gate.validate_judgment(root))

    def test_I_nonconfirmed_with_severity_fails(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); self.make_review(root, status="REJECTED"); p = gate.safe_child(root, "_rivetpay", "judgments", "RPC-001.json"); j = gate.read_json(p); j["severity"] = "P1"; gate.write_json(p, j); self.assert_gate_error(lambda: gate.validate_judgment(root))

    def test_J_ambiguous_policy_confirmed_fails(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); self.make_review(root, policy_status="AMBIGUOUS", candidate_deps=True); self.assert_gate_error(lambda: gate.validate_judgment(root))

    def test_K_policy_independent_binding_can_pass(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); self.make_review(root, policy_status="AMBIGUOUS", candidate_deps=True); p = gate.safe_child(root, "_rivetpay", "judgments", "RPC-001.json"); j = gate.read_json(p); j.update({"policy_independent_invariant": True, "policy_independent_invariant_reason": "binding violation is independent", "policy_independent_invariant_evidence": ["binding"]}); gate.write_json(p, j); self.assertEqual(gate.validate_judgment(root)["judgments"]["RPC-001"]["status"], "CONFIRMED")

    def test_L_unresolved_provider_confirmed_fails(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); self.make_review(root, provider_status="UNVERIFIED", candidate_deps=True); self.assert_gate_error(lambda: gate.validate_judgment(root))

    def test_M_runtime_required_unavailable_blocks(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); self.make_review(root); p = gate.safe_child(root, "_rivetpay", "judgments", "RPC-001.json"); j = gate.read_json(p); j["runtime_required"] = True; gate.write_json(p, j); self.assert_gate_error(lambda: gate.validate_judgment(root))

    def test_N_runtime_not_required_source_proof_passes(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); self.make_review(root); self.assertEqual(gate.validate_judgment(root)["judgments"]["RPC-001"]["status"], "CONFIRMED")

    def _mutate_confirmed(self, root, **changes):
        p = gate.safe_child(root, "_rivetpay", "judgments", "RPC-001.json")
        judgment = gate.read_json(p)
        judgment.update(changes)
        gate.write_json(p, judgment)

    def test_precision_A_confirmed_unknown_target_value_fails(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); self.make_review(root); self._mutate_confirmed(root, target_value="unknown"); self.assert_gate_error(lambda: gate.validate_judgment(root))

    def test_precision_B_confirmed_unknown_invariant_fails(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); self.make_review(root); self._mutate_confirmed(root, invariant="unknown"); self.assert_gate_error(lambda: gate.validate_judgment(root))

    def test_precision_C_confirmed_empty_required_semantics_fail(self):
        for field in ("target_value", "invariant", "attack_path", "authority", "realized_value", "evidence_basis"):
            with self.subTest(field=field), tempfile.TemporaryDirectory() as d:
                root = Path(d); self.make_review(root); self._mutate_confirmed(root, **{field: None if field == "realized_value" else ([] if field == "evidence_basis" else "")}); self.assert_gate_error(lambda: gate.validate_judgment(root))

    def test_precision_D_upstream_state_without_realized_value_not_confirmed(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); self.make_review(root); self._mutate_confirmed(root, realized_value_status="UNESTABLISHED", realized_value="second checkout object", value_path=["timeout", "second checkout"]); self.assert_gate_error(lambda: gate.validate_judgment(root))

    def test_precision_E_deterministic_complete_value_path_can_confirm(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); self.make_review(root); self.assertEqual(gate.validate_judgment(root)["judgments"]["RPC-001"]["status"], "CONFIRMED")

    def test_precision_F_ambiguous_policy_dependent_candidate_not_confirmed(self):
        self.test_J_ambiguous_policy_confirmed_fails()

    def test_precision_G_explicit_policy_supports_confirmation(self):
        self.test_explicit_policy_evidence_satisfies()

    def test_precision_H_policy_independent_candidate_can_confirm(self):
        self.test_K_policy_independent_binding_can_pass()

    def test_precision_I_conflicted_material_provider_fact_blocks(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); self.make_review(root, provider_status="CONFLICTED", candidate_deps=True); self.assert_gate_error(lambda: gate.validate_judgment(root))

    def test_precision_J_irrelevant_provider_conflict_does_not_block(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); self.make_review(root, provider_status="CONFLICTED", candidate_deps=True, provider_material=False); self.assertEqual(gate.validate_judgment(root)["judgments"]["RPC-001"]["status"], "CONFIRMED")

    def test_precision_K_suspicious_intermediate_without_value_is_blocked(self):
        self.test_precision_D_upstream_state_without_realized_value_not_confirmed()

    def test_precision_L_mismatch_to_entitlement_chain_can_confirm(self):
        self.test_N_runtime_not_required_source_proof_passes()

    def test_precision_M_P1_without_realized_value_fails(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); self.make_review(root); self._mutate_confirmed(root, realized_value_status="UNESTABLISHED"); self.assert_gate_error(lambda: gate.validate_judgment(root))

    def test_precision_N_nonconfirmed_final_severity_fails(self):
        self.test_I_nonconfirmed_with_severity_fails()

    def test_precision_O_renderer_cannot_emit_placeholder_finding(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); self.make_review(root); self._mutate_confirmed(root, target_value="unknown"); self.assert_gate_error(lambda: gate.finalize(root))

    def test_precision_P_public_findings_are_canonical_and_unique(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); self.make_review(root); final = gate.finalize(root); gate.render(root); findings = gate.safe_child(root, "docs", "reviews", "payments", "findings.md").read_text(encoding="utf-8"); self.assertEqual(final["finding_totals"]["confirmed"], 1); self.assertEqual(findings.count("## RP-001"), 1); self.assertNotIn("No canonical confirmed findings", findings)

    def test_precision_Q_admin_manual_grant_is_not_payment_bypass_by_itself(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); self.make_review(root, status="REJECTED", outcome="DEFENDED"); self.assertEqual(gate.finalize(root)["verdict"], "PASS")

    def test_precision_R_provider_not_connected_remains_non_vulnerability(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); self.make_review(root, status="REJECTED", outcome="NOT_APPLICABLE"); self.assertEqual(gate.finalize(root)["verdict"], "PASS")

    def test_precision_S_generation_reopen_freeze_and_tamper_protections_remain(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); self.make_review(root); gate.reopen_discovery(root, "precision regression"); self.assertEqual(gate.phase(root), "DISCOVERY"); self.assertEqual(gate.freeze_discovery(root)["generation_id"], "GEN-0002")

    def test_O_confirmed_without_finding_branch_fails(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); self.make_review(root, outcome="DEFENDED"); self.assert_gate_error(lambda: gate.validate_coverage(root, gate.validate_judgment(root)))

    def test_P_finding_without_confirmed_candidate_fails(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); self.make_review(root, status="REJECTED", outcome="FINDING"); self.assert_gate_error(lambda: gate.validate_coverage(root, gate.validate_judgment(root)))

    def test_Q_rejected_candidate_cannot_be_finding(self): self.test_P_finding_without_confirmed_candidate_fails()

    def test_R_duplicate_persists_without_duplicate_public_finding(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); self.write_review_files(root, second_branch=True); gate.validate_context(root); f = gate.freeze_discovery(root); self._write_confirmed(root, f, "RPC-001"); self._write_dup(root, f, "RPC-002", "RPC-001"); gate.write_json(gate.safe_child(root, "_rivetpay", "coverage.json"), {"generation_id": f["generation_id"], "freeze_root_sha256": f["root_sha256"], "branches": [{"branch_id": "RPB-001", "family_id": "RPF-001", "authority_lineage": "CURRENT", "outcome": "FINDING", "candidate_ids": ["RPC-001"]}, {"branch_id": "RPB-002", "family_id": "RPF-001", "authority_lineage": "GENUINELY_NEW", "outcome": "DEFENDED", "candidate_ids": []}], "families": [{"family_id": "RPF-001", "branch_ids": ["RPB-001", "RPB-002"]}]}); self.assertEqual(gate.finalize(root)["finding_totals"]["confirmed"], 1)

    def _write_confirmed(self, root, f, cid):
        path = gate.safe_child(root, "_rivetpay", "history", f["generation_id"], "candidates", f"{cid}.json"); gate.write_json(gate.safe_child(root, "_rivetpay", "judgments", f"{cid}.json"), {"candidate_id": cid, "generation_id": f["generation_id"], "candidate_sha256": gate.sha256(path), "freeze_root_sha256": f["root_sha256"], "status": "CONFIRMED", "severity": "P1", "target_value": "synthetic entitlement", "invariant": "value requires exact authority", "attack_path": "accepted evidence -> persisted grant -> paid capability", "authority": "synthetic authority", "realized_value": "unauthorized paid capability", "realized_value_status": "ESTABLISHED", "value_path": ["accepted evidence", "persisted grant", "paid capability"], "evidence_basis": ["source", "enforcement"], "invariant_status": "ESTABLISHED", "reachability_status": "ESTABLISHED", "value_consequence_status": "ESTABLISHED", "controls_challenged": True, "runtime_required": False, "runtime_evidence_available": False, "runtime_reason": "source", "runtime_evidence": [], "policy_dependencies": [], "provider_dependencies": [], "evidence_matrix": {"invariant": "ESTABLISHED", "application_path": "ESTABLISHED", "value_consequence": "ESTABLISHED", "policy": "NOT_MATERIAL", "provider": "NOT_MATERIAL", "runtime": "NOT_REQUIRED", "controls_challenged": True}})

    def test_S_partial_coverage_cannot_pass(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); self.make_review(root, status="REJECTED", outcome="UNVERIFIED"); self.assertEqual(gate.finalize(root)["verdict"], "PARTIAL")

    def test_T_findings_confirmed_plus_partial_is_valid(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); self.make_review(root, outcome="FINDING", second_branch=True); p = gate.safe_child(root, "_rivetpay", "judgments", "RPC-002.json"); j = gate.read_json(p); j["status"] = "REJECTED"; j.pop("severity", None); gate.write_json(p, j); c = gate.read_json(gate.safe_child(root, "_rivetpay", "coverage.json")); c["branches"][1]["outcome"] = "UNVERIFIED"; c["branches"][1]["candidate_ids"] = []; gate.write_json(gate.safe_child(root, "_rivetpay", "coverage.json"), c); final = gate.finalize(root); self.assertEqual(final["verdict"], "FINDINGS CONFIRMED"); self.assertEqual(final["coverage_status"], "PARTIAL")

    def test_U_tampered_counts_fail(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); self.make_review(root); gate.finalize(root); p = gate.safe_child(root, "_rivetpay", "final.json"); f = gate.read_json(p); f["finding_totals"]["confirmed"] = 99; gate.write_json(p, f); self.assert_gate_error(lambda: gate.validate_structured(root))

    def test_V_findings_renderer_includes_canonical(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); self.make_review(root); gate.finalize(root); gate.render(root); self.assertIn("RP-001", gate.safe_child(root, "docs", "reviews", "payments", "findings.md").read_text())

    def test_findings_renderer_includes_every_canonical_confirmed_finding(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); self.make_review(root, second_branch=True); p = gate.safe_child(root, "_rivetpay", "coverage.json"); c = gate.read_json(p); c["branches"][1]["outcome"] = "FINDING"; c["branches"][1]["candidate_ids"] = ["RPC-002"]; gate.write_json(p, c); gate.finalize(root); gate.render(root); findings = gate.safe_child(root, "docs", "reviews", "payments", "findings.md").read_text(); self.assertIn("RP-001", findings); self.assertIn("RP-002", findings)

    def test_W_renderer_deterministic(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); self.make_review(root); gate.finalize(root); gate.render(root); a = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in gate.report_root(root).iterdir()}; gate.render(root); b = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in gate.report_root(root).iterdir()}; self.assertEqual(a, b)

    def test_X_path_containment_blocks_outside(self):
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(gate.GateError): gate.safe_child(gate.report_root(Path(d)), "..", "outside.md")

    def test_Y_frozen_candidate_id_disappearance_fails(self): self.test_E_frozen_candidate_deletion_fails()

    def test_Z1_invalid_branch_reference_fails(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); self.write_review_files(root); p = gate.safe_child(root, "_rivetpay", "candidates", "RPC-001.json"); c = gate.read_json(p); c["branch_ids"] = ["RPB-999"]; gate.write_json(p, c); gate.validate_context(root); self.assert_gate_error(lambda: gate.freeze_discovery(root))

    def test_Z2_invalid_policy_reference_fails(self): self._invalid_dependency("policy_dependencies", "policy_id", "POL-999")
    def test_Z3_invalid_provider_reference_fails(self): self._invalid_dependency("provider_dependencies", "provider_fact_id", "PCF-999")
    def _invalid_dependency(self, field, key, value):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); self.write_review_files(root); p = gate.safe_child(root, "_rivetpay", "candidates", "RPC-001.json"); c = gate.read_json(p); c[field] = [{key: value, "material": True, "reason": "x"}]; gate.write_json(p, c); gate.validate_context(root); self.assert_gate_error(lambda: gate.freeze_discovery(root))

    def test_Z4_invalid_family_reference_fails(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); self.write_review_files(root); p = gate.safe_child(root, "_rivetpay", "branches.json"); b = gate.read_json(p); b["branches"][0]["family_id"] = "RPF-999"; gate.write_json(p, b); gate.validate_context(root); self.assert_gate_error(lambda: gate.freeze_discovery(root))

    def test_candidate_top_level_final_field_ban_is_exact(self):
        fields = ("status", "outcome", "confirmed", "severity", "finding_id", "verdict", "duplicate_of", "final_verdict", "remediation_direction")
        for field in fields:
            with self.subTest(field=field), tempfile.TemporaryDirectory() as d:
                root = Path(d); self.write_review_files(root); p = gate.safe_child(root, "_rivetpay", "candidates", "RPC-001.json"); c = gate.read_json(p); c[field] = "x"; gate.write_json(p, c); self.assert_gate_error(lambda: gate.validate_discovery(root))

    def test_nested_application_status_is_allowed(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); self.write_review_files(root); p = gate.safe_child(root, "_rivetpay", "candidates", "RPC-001.json"); c = gate.read_json(p); c["observed_state"] = {"status": "inactive"}; gate.write_json(p, c); self.assertEqual(len(gate.validate_discovery(root)[1]), 1)

    def test_generation_first_freeze_is_GEN0001(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); self.write_review_files(root); gate.validate_context(root); self.assertEqual(gate.freeze_discovery(root)["generation_id"], "GEN-0001")

    def test_generation_second_freeze_without_reopen_fails(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); self.write_review_files(root); gate.validate_context(root); gate.freeze_discovery(root); self.assert_gate_error(lambda: gate.freeze_discovery(root))

    def test_reopen_requires_reason(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); self.make_review(root); self.assert_gate_error(lambda: gate.reopen_discovery(root, ""))

    def test_reopen_archives_and_increments_generation(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); self.make_review(root); result = gate.reopen_discovery(root, "new candidate"); self.assertEqual(result["generation_id"], "GEN-0002"); self.assertTrue(gate.safe_child(root, "_rivetpay", "history", "GEN-0001", "reopen.json").is_file())

    def test_reopen_removes_active_judgment_coverage_final(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); self.make_review(root); gate.finalize(root); gate.reopen_discovery(root, "reopen"); self.assertFalse(gate.safe_child(root, "_rivetpay", "final.json").exists()); self.assertFalse(gate.safe_child(root, "_rivetpay", "coverage.json").exists()); self.assertEqual(gate.relative_files(gate.safe_child(root, "_rivetpay", "judgments")), [])

    def test_reopen_archives_prior_derived_state(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); self.make_review(root); gate.finalize(root); gate.reopen_discovery(root, "archive complete generation"); archive = gate.safe_child(root, "_rivetpay", "history", "GEN-0001"); self.assertTrue(gate.safe_child(archive, "judgments", "RPC-001.json").is_file()); self.assertTrue(gate.safe_child(archive, "coverage.json").is_file()); self.assertTrue(gate.safe_child(archive, "final.json").is_file())

    def test_archived_candidate_bytes_remain_unchanged_after_reopen(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); self.make_review(root); archived = gate.safe_child(root, "_rivetpay", "history", "GEN-0001", "candidates", "RPC-001.json").read_bytes(); gate.reopen_discovery(root, "editable next generation"); active = gate.safe_child(root, "_rivetpay", "candidates", "RPC-001.json"); active.write_bytes(active.read_bytes() + b"new-generation-edit"); self.assertEqual(gate.safe_child(root, "_rivetpay", "history", "GEN-0001", "candidates", "RPC-001.json").read_bytes(), archived)

    def test_stale_generation_judgment_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); self.make_review(root); old = gate.read_json(gate.safe_child(root, "_rivetpay", "judgments", "RPC-001.json")); gate.reopen_discovery(root, "new candidate"); gate.freeze_discovery(root); gate.write_json(gate.safe_child(root, "_rivetpay", "judgments", "RPC-001.json"), old); self.assert_gate_error(lambda: gate.validate_judgment(root))

    def test_wrong_candidate_hash_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); self.make_review(root); p = gate.safe_child(root, "_rivetpay", "judgments", "RPC-001.json"); j = gate.read_json(p); j["candidate_sha256"] = "0" * 64; gate.write_json(p, j); self.assert_gate_error(lambda: gate.validate_judgment(root))

    def test_wrong_root_hash_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); self.make_review(root); p = gate.safe_child(root, "_rivetpay", "judgments", "RPC-001.json"); j = gate.read_json(p); j["freeze_root_sha256"] = "0" * 64; gate.write_json(p, j); self.assert_gate_error(lambda: gate.validate_judgment(root))

    def test_coverage_wrong_generation_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); self.make_review(root); p = gate.safe_child(root, "_rivetpay", "coverage.json"); c = gate.read_json(p); c["generation_id"] = "GEN-0002"; gate.write_json(p, c); self.assert_gate_error(lambda: gate.validate_structured(root))

    def test_final_wrong_generation_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); self.make_review(root); gate.finalize(root); p = gate.safe_child(root, "_rivetpay", "final.json"); f = gate.read_json(p); f["generation_id"] = "GEN-0002"; gate.write_json(p, f); self.assert_gate_error(lambda: gate.validate_structured(root))

    def test_freeze_metadata_rewrite_cannot_legitimize_change(self): self.test_D_frozen_candidate_modification_fails()
    def test_freeze_rewrite_exploit_fails_against_archived_generation(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); self.make_review(root); candidate = gate.safe_child(root, "_rivetpay", "candidates", "RPC-001.json"); candidate.write_text(candidate.read_text() + "changed", encoding="utf-8"); active = gate.read_json(gate.safe_child(root, "_rivetpay", "active-freeze.json")); active["files"][3]["sha256"] = gate.sha256(candidate); active["root_sha256"] = gate.generation_root(active["generation_id"], active["files"], ["RPC-001"], ["RPB-001"]); gate.write_json(gate.safe_child(root, "_rivetpay", "active-freeze.json"), active); self.assert_gate_error(lambda: gate.validate_judgment(root))
    def test_history_sequence_validation_passes(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); self.make_review(root); gate.reopen_discovery(root, "reopen"); self.assertIsNone(gate.validate_history(root))
    def test_malformed_history_fails(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); self.make_review(root); gate.safe_child(root, "_rivetpay", "history", "bad").mkdir(); self.assert_gate_error(lambda: gate.validate_history(root))

    def test_synthetic_generation_reopen_requires_fresh_all_candidate_judgments(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); self.make_review(root); old_judgment = gate.read_json(gate.safe_child(root, "_rivetpay", "judgments", "RPC-001.json")); gate.reopen_discovery(root, "candidate discovered during judgment")
            branches_path = gate.safe_child(root, "_rivetpay", "branches.json"); branches = gate.read_json(branches_path); branches["branches"].append({"branch_id": "RPB-002", "family_id": "RPF-001", "predicate": "new_authority", "condition": "new", "authority_lineage": "GENUINELY_NEW", "lineage_sensitive": True, "lineage_group": "RPLG-002", "material": True, "candidate_ids": ["RPC-002"]}); gate.write_json(branches_path, branches)
            gate.write_json(gate.safe_child(root, "_rivetpay", "candidates", "RPC-002.json"), {"candidate_id": "RPC-002", "title": "new candidate", "branch_ids": ["RPB-002"], "policy_dependencies": [], "provider_dependencies": []}); f2 = gate.freeze_discovery(root)
            gate.write_json(gate.safe_child(root, "_rivetpay", "judgments", "RPC-001.json"), old_judgment); self.assert_gate_error(lambda: gate.validate_judgment(root)); gate.safe_child(root, "_rivetpay", "judgments", "RPC-001.json").unlink(); self._write_confirmed(root, f2, "RPC-001"); self._write_rejected(root, f2, "RPC-002"); self._write_coverage_two(root, f2); self.assertEqual(gate.finalize(root)["generation_id"], "GEN-0002")

    def _write_rejected(self, root, f, cid):
        path = gate.safe_child(root, "_rivetpay", "history", f["generation_id"], "candidates", f"{cid}.json")
        gate.write_json(gate.safe_child(root, "_rivetpay", "judgments", f"{cid}.json"), {"candidate_id": cid, "generation_id": f["generation_id"], "candidate_sha256": gate.sha256(path), "freeze_root_sha256": f["root_sha256"], "status": "REJECTED"})

    def _write_coverage_two(self, root, f):
        gate.write_json(gate.safe_child(root, "_rivetpay", "coverage.json"), {"generation_id": f["generation_id"], "freeze_root_sha256": f["root_sha256"], "branches": [{"branch_id": "RPB-001", "family_id": "RPF-001", "authority_lineage": "CURRENT", "outcome": "FINDING", "candidate_ids": ["RPC-001"]}, {"branch_id": "RPB-002", "family_id": "RPF-001", "authority_lineage": "GENUINELY_NEW", "outcome": "DEFENDED", "candidate_ids": []}], "families": [{"family_id": "RPF-001", "branch_ids": ["RPB-001", "RPB-002"]}]})

    def test_material_branch_missing_lineage_fails(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); self.write_review_files(root); p = gate.safe_child(root, "_rivetpay", "branches.json"); b = gate.read_json(p); del b["branches"][0]["authority_lineage"]; gate.write_json(p, b); gate.validate_context(root); self.assert_gate_error(lambda: gate.freeze_discovery(root))
    def test_invalid_lineage_enum_fails(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); self.write_review_files(root, lineage="BAD"); gate.validate_context(root); self.assert_gate_error(lambda: gate.freeze_discovery(root))
    def test_lineage_sensitive_not_applicable_fails(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); self.write_review_files(root, lineage="NOT_APPLICABLE", lineage_sensitive=True); gate.validate_context(root); self.assert_gate_error(lambda: gate.freeze_discovery(root))
    def test_prior_lineage_is_structural(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); self.write_review_files(root, lineage="PRIOR_SUPERSEDED"); gate.validate_context(root); f = gate.freeze_discovery(root); self.assertEqual(gate.validate_discovery_tree(gate.safe_child(root, "_rivetpay", "history", f["generation_id"]))[2]["branches"]["RPB-001"]["authority_lineage"], "PRIOR_SUPERSEDED")
    def test_genuine_new_sibling_is_separate(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); self.write_review_files(root, second_branch=True, lineage_sensitive=True); self.assertEqual(len(gate.validate_discovery_tree(gate.artifact_root(root))[1]), 2)
    def test_duplicate_lineage_group_class_fails(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); self.write_review_files(root, second_branch=True, lineage_sensitive=True); p = gate.safe_child(root, "_rivetpay", "branches.json"); b = gate.read_json(p); b["branches"][1]["authority_lineage"] = "CURRENT"; gate.write_json(p, b); self.assert_gate_error(lambda: gate.validate_discovery(root))
    def test_lineage_group_need_not_contain_all_classes(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); self.write_review_files(root, lineage_sensitive=True); self.assertEqual(len(gate.validate_discovery(root)[1]), 1)

    def test_missing_family_id_fails(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); self.write_review_files(root); p = gate.safe_child(root, "_rivetpay", "branches.json"); b = gate.read_json(p); del b["branches"][0]["family_id"]; gate.write_json(p, b); self.assert_gate_error(lambda: gate.validate_discovery(root))
    def test_unknown_family_id_fails(self): self.test_Z4_invalid_family_reference_fails()
    def test_material_family_without_branch_fails(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); self.write_review_files(root); p = gate.safe_child(root, "_rivetpay", "branches.json"); b = gate.read_json(p); b["branches"] = []; gate.write_json(p, b); gate.validate_context(root); self.assert_gate_error(lambda: gate.freeze_discovery(root))
    def test_family_finding_status_is_derived(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); self.make_review(root); self.assertEqual(gate.validate_coverage(root, gate.validate_judgment(root))["families"][0]["outcome"], "FINDINGS_CONFIRMED")
    def test_family_unresolved_status_is_derived(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); self.make_review(root, status="REJECTED", outcome="UNVERIFIED"); self.assertEqual(gate.validate_coverage(root, gate.validate_judgment(root))["families"][0]["outcome"], "PARTIAL")
    def test_all_closed_family_is_closed(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); self.make_review(root, status="REJECTED", outcome="DEFENDED"); self.assertEqual(gate.validate_coverage(root, gate.validate_judgment(root))["families"][0]["outcome"], "CLOSED")
    def test_conflicting_family_status_fails(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); self.make_review(root); p = gate.safe_child(root, "_rivetpay", "coverage.json"); c = gate.read_json(p); c["families"][0]["outcome"] = "CLOSED"; gate.write_json(p, c); self.assert_gate_error(lambda: gate.validate_structured(root))

    def test_public_id_first_is_RP001(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); self.make_review(root); self.assertEqual(gate.finalize(root)["finding_id_map"], {"RPC-001": "RP-001"})
    def test_public_ids_sorted_by_candidate(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); self.make_review(root, second_branch=True); p = gate.safe_child(root, "_rivetpay", "judgments", "RPC-002.json"); j = gate.read_json(p); j["status"] = "REJECTED"; j.pop("severity", None); gate.write_json(p, j); final = gate.finalize(root); self.assertEqual(final["finding_id_map"], {"RPC-001": "RP-001"})
    def test_rejected_duplicate_needs_review_do_not_consume_id(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); self.make_review(root); self.assertNotIn("finding_id", gate.read_json(gate.safe_child(root, "_rivetpay", "judgments", "RPC-001.json")))
    def test_rerun_finalization_preserves_mapping(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); self.make_review(root); a = gate.finalize(root)["finding_id_map"]; b = gate.finalize(root)["finding_id_map"]; self.assertEqual(a, b)
    def test_hand_authored_finding_id_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); self.make_review(root); p = gate.safe_child(root, "_rivetpay", "judgments", "RPC-001.json"); j = gate.read_json(p); j["finding_id"] = "RP-001"; gate.write_json(p, j); self.assert_gate_error(lambda: gate.validate_judgment(root))

    def test_policy_arrays_required(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); self.write_review_files(root); p = gate.safe_child(root, "_rivetpay", "policy-contract.json"); x = gate.read_json(p); del x["product_policy_claims"]; gate.write_json(p, x); self.assert_gate_error(lambda: gate.validate_context(root))
    def test_policy_ids_unique(self): self._duplicate_policy_or_provider("product_policy_claims")
    def test_provider_ids_unique(self): self._duplicate_policy_or_provider("provider_contract_facts")
    def _duplicate_policy_or_provider(self, key):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); self.write_review_files(root, candidate_deps=True); p = gate.safe_child(root, "_rivetpay", "policy-contract.json"); x = gate.read_json(p); x[key].append(dict(x[key][0])); gate.write_json(p, x); self.assert_gate_error(lambda: gate.validate_context(root))
    def test_cross_domain_reference_fails(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); self.write_review_files(root, candidate_deps=True); p = gate.safe_child(root, "_rivetpay", "candidates", "RPC-001.json"); x = gate.read_json(p); x["policy_dependencies"][0]["policy_id"] = "PCF-001"; gate.write_json(p, x); self.assert_gate_error(lambda: gate.validate_discovery(root))
    def test_strong_policy_one_evidence_fails(self): self._policy_status_evidence("STRONGLY_RECONSTRUCTED", ["one"])
    def test_strong_policy_contradictions_fail(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); self.write_review_files(root, candidate_deps=True); p = gate.safe_child(root, "_rivetpay", "policy-contract.json"); x = gate.read_json(p); x["product_policy_claims"][0].update(status="STRONGLY_RECONSTRUCTED", evidence=["a", "b"], contradictions=["conflict"]); gate.write_json(p, x); self.assert_gate_error(lambda: gate.validate_context(root))
    def _policy_status_evidence(self, status, evidence):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); self.write_review_files(root, candidate_deps=True); p = gate.safe_child(root, "_rivetpay", "policy-contract.json"); x = gate.read_json(p); x["product_policy_claims"][0].update(status=status, evidence=evidence); gate.write_json(p, x); self.assert_gate_error(lambda: gate.validate_context(root))
    def test_explicit_policy_evidence_satisfies(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); self.make_review(root, candidate_deps=True); self.assertEqual(gate.validate_judgment(root)["judgments"]["RPC-001"]["status"], "CONFIRMED")
    def test_unspecified_policy_blocks(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); self.make_review(root, policy_status="UNSPECIFIED", candidate_deps=True); self.assert_gate_error(lambda: gate.validate_judgment(root))
    def test_policy_independent_binding_requires_reason(self): self.test_J_ambiguous_policy_confirmed_fails()

    def test_provider_established_passes(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); self.make_review(root, candidate_deps=True); self.assertEqual(gate.validate_judgment(root)["judgments"]["RPC-001"]["status"], "CONFIRMED")
    def test_provider_unverified_blocks(self): self.test_L_unresolved_provider_confirmed_fails()
    def test_nonmaterial_provider_does_not_block(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); self.make_review(root, provider_status="UNVERIFIED", candidate_deps=True); p = gate.safe_child(root, "_rivetpay", "candidates", "RPC-001.json"); c = gate.read_json(p); c["provider_dependencies"][0]["material"] = False; gate.write_json(p, c); self.assert_gate_error(lambda: gate.validate_judgment(root))
    def test_missing_provider_id_fails(self): self.test_Z3_invalid_provider_reference_fails()
    def test_runtime_required_available_passes(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); self.make_review(root); p = gate.safe_child(root, "_rivetpay", "judgments", "RPC-001.json"); j = gate.read_json(p); j.update(runtime_required=True, runtime_evidence_available=True, runtime_evidence=["integration"], evidence_matrix={**j["evidence_matrix"], "runtime": "SATISFIED"}); gate.write_json(p, j); self.assertEqual(gate.validate_judgment(root)["judgments"]["RPC-001"]["status"], "CONFIRMED")
    def test_missing_runtime_fields_fail(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); self.make_review(root); p = gate.safe_child(root, "_rivetpay", "judgments", "RPC-001.json"); j = gate.read_json(p); del j["runtime_required"]; gate.write_json(p, j); self.assert_gate_error(lambda: gate.validate_judgment(root))

    def test_final_tampered_severity_totals_fail(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); self.make_review(root); gate.finalize(root); p = gate.safe_child(root, "_rivetpay", "final.json"); x = gate.read_json(p); x["severity_totals"]["P1"] = 0; gate.write_json(p, x); self.assert_gate_error(lambda: gate.validate_structured(root))
    def test_final_tampered_coverage_status_fail(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); self.make_review(root); gate.finalize(root); p = gate.safe_child(root, "_rivetpay", "final.json"); x = gate.read_json(p); x["coverage_status"] = "PARTIAL"; gate.write_json(p, x); self.assert_gate_error(lambda: gate.validate_structured(root))
    def test_final_tampered_mapping_fail(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); self.make_review(root); gate.finalize(root); p = gate.safe_child(root, "_rivetpay", "final.json"); x = gate.read_json(p); x["finding_id_map"] = {}; gate.write_json(p, x); self.assert_gate_error(lambda: gate.validate_structured(root))
    def test_final_regeneration_restores_canonical(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); self.make_review(root); gate.finalize(root); p = gate.safe_child(root, "_rivetpay", "final.json"); x = gate.read_json(p); x["finding_totals"]["confirmed"] = 99; gate.write_json(p, x); gate.finalize(root); self.assertEqual(gate.read_json(p)["finding_totals"]["confirmed"], 1)

    def test_cli_synthetic_lifecycle_gen1_reopen_gen2(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); self.make_review(root); cli = Path(__file__).with_name("rivetpay_gate.py"); result = subprocess.run([sys.executable, "-X", "utf8", "-B", str(cli), "reopen-discovery", "--workdir", str(root), "--reason", "new candidate"], capture_output=True, text=True); self.assertEqual(result.returncode, 0, result.stderr); self.assertEqual(json.loads(result.stdout)["generation_id"], "GEN-0002")

    def test_cli_full_synthetic_pipeline_and_report_hashes(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); self.write_review_files(root); cli = Path(__file__).with_name("rivetpay_gate.py")
            for command in ("init", "validate-context", "freeze-discovery"):
                result = subprocess.run([sys.executable, "-X", "utf8", "-B", str(cli), command, "--workdir", str(root)], capture_output=True, text=True); self.assertEqual(result.returncode, 0, result.stderr)
            f = gate.verify_freeze(root); self._write_confirmed(root, f, "RPC-001")
            gate.write_json(gate.safe_child(root, "_rivetpay", "coverage.json"), {"generation_id": f["generation_id"], "freeze_root_sha256": f["root_sha256"], "branches": [{"branch_id": "RPB-001", "family_id": "RPF-001", "authority_lineage": "CURRENT", "outcome": "FINDING", "candidate_ids": ["RPC-001"]}], "families": [{"family_id": "RPF-001", "branch_ids": ["RPB-001"]}]})
            for command in ("validate-judgment", "finalize", "render", "validate", "status"):
                result = subprocess.run([sys.executable, "-X", "utf8", "-B", str(cli), command, "--workdir", str(root)], capture_output=True, text=True); self.assertEqual(result.returncode, 0, result.stderr)
            first = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in gate.report_root(root).iterdir()}; subprocess.run([sys.executable, "-X", "utf8", "-B", str(cli), "render", "--workdir", str(root)], check=True, capture_output=True, text=True); second = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in gate.report_root(root).iterdir()}; self.assertEqual(first, second)

    def test_regression_corpus_has_seven_cases_and_eval_corpus_210(self):
        result = gate.validate_regression_corpus(Path(__file__).resolve().parents[1]); self.assertEqual(result["eval_count"], 210); self.assertEqual(result["case_count"], 7)


if __name__ == "__main__":
    unittest.main(verbosity=2)
