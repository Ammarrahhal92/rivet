#!/usr/bin/env python3
"""Deterministic artifact gate and renderer for RivetPay reviews.

The gate is standard-library-only. It validates structured review state and
never executes an application review or an agent.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import sys
from pathlib import Path
from typing import Any, Iterable

OUTCOMES = {"FINDING", "DEFENDED", "UNVERIFIED", "NOT_APPLICABLE", "INSUFFICIENT_EVIDENCE", "HARDENING_ONLY"}
LINEAGES = {"CURRENT", "PRIOR_SUPERSEDED", "GENUINELY_NEW", "UNKNOWN", "NOT_APPLICABLE"}
JUDGMENT_STATUSES = {"CONFIRMED", "NEEDS_REVIEW", "REJECTED", "DUPLICATE"}
POLICY_STATUSES = {"EXPLICIT", "STRONGLY_RECONSTRUCTED", "AMBIGUOUS", "UNSPECIFIED"}
PROVIDER_STATUSES = {"ESTABLISHED", "UNVERIFIED", "CONFLICTED"}
RESOLUTIONS = {"SATISFIED", "UNRESOLVED", "NOT_MATERIAL"}
PUBLIC_FINDING = re.compile(r"^RP-\d{3}$")
CANDIDATE_ID = re.compile(r"^RPC-\d{3}$")
BRANCH_ID = re.compile(r"^RPB-\d{3}$")
FAMILY_ID = re.compile(r"^RPF-\d{3}$")
LINEAGE_GROUP_ID = re.compile(r"^RPLG-\d{3}$")
POLICY_ID = re.compile(r"^POL-\d{3}$")
PROVIDER_ID = re.compile(r"^PCF-\d{3}$")
REGRESSION_ID = re.compile(r"^RPR-\d{3}$")
GENERATION_ID = re.compile(r"^GEN-\d{4}$")
FORBIDDEN_CANDIDATE_KEYS = {"severity", "finding_id", "verdict", "judgment", "final_verdict", "status", "outcome", "confirmed", "rejected", "duplicate_of", "remediation", "remediation_direction", "final_severity"}
REPORT_NAMES = ("00-rivet-pay-summary.md", "authority-state-map.md", "findings.md", "coverage-and-defenses.md")


class GateError(RuntimeError):
    """A deterministic validation failure with a stable category in its text."""


def fail(message: str, code: str = "E_SCHEMA") -> None:
    raise GateError(f"{code}: {message}")


def safe_child(base: Path, *parts: str) -> Path:
    """Return a path contained by base, rejecting traversal and absolute parts."""
    base = base.resolve()
    candidate = base.joinpath(*parts).resolve()
    try:
        candidate.relative_to(base)
    except ValueError as exc:
        fail(f"path escapes containment boundary: {candidate}", "E_PATH_CONTAINMENT")
        raise AssertionError from exc
    return candidate


def artifact_root(workdir: Path) -> Path:
    return safe_child(workdir, "_rivetpay")


def report_root(workdir: Path) -> Path:
    return safe_child(workdir, "docs", "reviews", "payments")


def json_dump(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def read_json(path: Path) -> Any:
    if not path.is_file():
        fail(f"missing JSON artifact {path}", "E_ARTIFACT_MISSING")
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        fail(f"invalid JSON in {path}: {exc}", "E_JSON_INVALID")


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json_dump(value), encoding="utf-8", newline="\n")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def relative_files(root: Path) -> list[str]:
    if not root.exists():
        return []
    return sorted(path.relative_to(root).as_posix() for path in root.rglob("*") if path.is_file())


def require_object(value: Any, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        fail(f"{label} must be a JSON object")
    return value


def require_list(value: Any, label: str) -> list[Any]:
    if not isinstance(value, list):
        fail(f"{label} must be a JSON array")
    return value


PLACEHOLDER_TEXT = {"", "unknown", "n/a", "na", "none", "null", "tbd", "todo", "unspecified", "not applicable", "-", "—"}


def meaningful_text(value: Any) -> bool:
    return isinstance(value, str) and value.strip().lower() not in PLACEHOLDER_TEXT


def meaningful_evidence(value: Any) -> bool:
    if not isinstance(value, list) or not value:
        return False
    return all(meaningful_text(item) for item in value)


def validate_finding_semantics(judgment: dict[str, Any], candidate: dict[str, Any]) -> None:
    """Require the canonical finding identity before CONFIRMED can be derived."""
    fields = (
        ("target_value", ("target_value",)),
        ("invariant", ("invariant",)),
        ("attack_path", ("attack_path", "violated_transition", "path")),
        ("authority", ("authority", "expected_authority", "grant_source", "authoritative_grant_source")),
        ("realized_value", ("realized_value", "unauthorized_result", "observed_result")),
    )
    for label, aliases in fields:
        if not any(meaningful_text(judgment.get(key)) for key in aliases):
            fail(f"confirmed {candidate['candidate_id']} requires meaningful {label}", "E_FINDING_SEMANTICS")
    evidence = judgment.get("evidence_basis", judgment.get("evidence"))
    if not meaningful_evidence(evidence):
        fail(f"confirmed {candidate['candidate_id']} requires non-placeholder evidence basis", "E_FINDING_SEMANTICS")
    if judgment.get("realized_value_status") != "ESTABLISHED":
        fail(f"confirmed {candidate['candidate_id']} requires established realized commercial value", "E_REALIZED_VALUE")
    if not meaningful_text(judgment.get("realized_value")):
        fail(f"confirmed {candidate['candidate_id']} requires a concrete realized value", "E_REALIZED_VALUE")
    value_path = judgment.get("value_path")
    if not isinstance(value_path, list) or len(value_path) < 2 or not meaningful_evidence(value_path):
        fail(f"confirmed {candidate['candidate_id']} requires a complete value path", "E_REALIZED_VALUE")


def id_ok(value: Any, pattern: re.Pattern[str]) -> bool:
    return isinstance(value, str) and bool(pattern.match(value))


def manifest_path(workdir: Path) -> Path:
    return safe_child(artifact_root(workdir), "manifest.json")


def load_manifest(workdir: Path) -> dict[str, Any]:
    return require_object(read_json(manifest_path(workdir)), "manifest")


def save_manifest(workdir: Path, manifest: dict[str, Any]) -> None:
    write_json(manifest_path(workdir), manifest)


def phase(workdir: Path) -> str:
    return str(load_manifest(workdir).get("phase"))


def set_phase(workdir: Path, value: str) -> None:
    manifest = load_manifest(workdir)
    manifest["phase"] = value
    active_record = active_generation_record(manifest)
    if active_record is not None:
        active_record["phase"] = value
    save_manifest(workdir, manifest)


def validate_policy_document(policy: dict[str, Any]) -> tuple[dict[str, dict[str, Any]], dict[str, dict[str, Any]]]:
    products = require_list(policy.get("product_policy_claims"), "policy-contract.product_policy_claims")
    providers = require_list(policy.get("provider_contract_facts"), "policy-contract.provider_contract_facts")
    product_map: dict[str, dict[str, Any]] = {}
    for raw in products:
        item = require_object(raw, "product policy claim")
        pid = item.get("id")
        if not id_ok(pid, POLICY_ID) or pid in product_map:
            fail(f"invalid or duplicate product policy ID {pid}", "E_POLICY_ID")
        if not all(isinstance(item.get(key), str) and item.get(key) for key in ("topic", "statement")):
            fail(f"product policy {pid} requires topic and statement", "E_POLICY_SCHEMA")
        if item.get("status") not in POLICY_STATUSES:
            fail(f"invalid product policy status for {pid}", "E_POLICY_SCHEMA")
        if not isinstance(item.get("delegated_to_provider"), bool):
            fail(f"product policy {pid} requires delegated_to_provider", "E_POLICY_SCHEMA")
        evidence = require_list(item.get("evidence"), f"product policy {pid}.evidence")
        contradictions = require_list(item.get("contradictions"), f"product policy {pid}.contradictions")
        if item["status"] == "STRONGLY_RECONSTRUCTED" and (len(evidence) < 2 or contradictions):
            fail(f"strongly reconstructed policy {pid} needs two evidence entries and no contradictions", "E_POLICY_EVIDENCE")
        if item["status"] == "EXPLICIT" and not evidence:
            fail(f"explicit policy {pid} needs evidence", "E_POLICY_EVIDENCE")
        product_map[pid] = item
    provider_map: dict[str, dict[str, Any]] = {}
    for raw in providers:
        item = require_object(raw, "provider contract fact")
        cid = item.get("id")
        if not id_ok(cid, PROVIDER_ID) or cid in provider_map:
            fail(f"invalid or duplicate provider fact ID {cid}", "E_PROVIDER_ID")
        if not all(isinstance(item.get(key), str) and item.get(key) for key in ("topic", "statement", "source_kind", "source")):
            fail(f"provider fact {cid} requires topic, statement, source_kind, and source", "E_PROVIDER_SCHEMA")
        if item.get("status") not in PROVIDER_STATUSES:
            fail(f"invalid provider fact status for {cid}", "E_PROVIDER_SCHEMA")
        require_list(item.get("evidence"), f"provider fact {cid}.evidence")
        conflicts = require_list(item.get("conflicts", []), f"provider fact {cid}.conflicts")
        if item["status"] == "CONFLICTED" and not conflicts:
            fail(f"conflicted provider fact {cid} must preserve the material conflict", "E_PROVIDER_CONFLICT")
        provider_map[cid] = item
    return product_map, provider_map


def validate_context_tree(root: Path) -> tuple[dict[str, Any], dict[str, dict[str, Any]], dict[str, dict[str, Any]]]:
    context = require_object(read_json(safe_child(root, "context.json")), "context")
    policy = require_object(read_json(safe_child(root, "policy-contract.json")), "policy-contract")
    if any(str(key).lower() in {"verdict", "severity", "finding_id", "remediation"} for key in context):
        fail("context contains final-only fields", "E_CONTEXT_FINAL_FIELD")
    if context.get("review_mode") not in {None, "READ-ONLY / DISCOVERY-ONLY"}:
        fail("context review_mode must preserve discovery-only mode", "E_SAFETY_MODE")
    products, providers = validate_policy_document(policy)
    return context, products, providers


def validate_context(workdir: Path) -> None:
    validate_context_tree(artifact_root(workdir))
    if manifest_path(workdir).is_file() and phase(workdir) == "CONTEXT":
        set_phase(workdir, "DISCOVERY")


def candidate_paths(root: Path) -> list[str]:
    paths = relative_files(safe_child(root, "candidates"))
    for relative in paths:
        name = Path(relative).name
        if not name.endswith(".json") or not id_ok(name[:-5], CANDIDATE_ID):
            fail(f"invalid candidate artifact name {relative}", "E_CANDIDATE_ID")
    return paths


def validate_discovery_tree(root: Path) -> tuple[dict[str, Any], list[dict[str, Any]], dict[str, Any]]:
    branches_doc = require_object(read_json(safe_child(root, "branches.json")), "branches")
    branches = require_list(branches_doc.get("branches"), "branches.branches")
    families = require_list(branches_doc.get("families"), "branches.families")
    family_map: dict[str, dict[str, Any]] = {}
    for raw in families:
        family = require_object(raw, "family")
        fid = family.get("id")
        if not id_ok(fid, FAMILY_ID) or fid in family_map:
            fail(f"invalid or duplicate family ID {fid}", "E_FAMILY_ID")
        if not isinstance(family.get("name"), str) or not isinstance(family.get("material"), bool):
            fail(f"family {fid} requires name and material", "E_FAMILY_SCHEMA")
        family_map[fid] = family
    branch_map: dict[str, dict[str, Any]] = {}
    for raw in branches:
        branch = require_object(raw, "branch")
        bid = branch.get("branch_id")
        if not id_ok(bid, BRANCH_ID) or bid in branch_map:
            fail(f"invalid or duplicate branch ID {bid}", "E_BRANCH_ID")
        if not isinstance(branch.get("material"), bool):
            fail(f"branch {bid} requires boolean material", "E_BRANCH_SCHEMA")
        fid = branch.get("family_id")
        if not id_ok(fid, FAMILY_ID) or fid not in family_map:
            fail(f"branch {bid} references unknown family {fid}", "E_FAMILY_UNKNOWN")
        if branch["material"]:
            lineage = branch.get("authority_lineage")
            if lineage not in LINEAGES:
                fail(f"material branch {bid} requires authority_lineage", "E_LINEAGE_REQUIRED")
            if not isinstance(branch.get("lineage_sensitive"), bool):
                fail(f"material branch {bid} requires lineage_sensitive", "E_LINEAGE_SCHEMA")
            if branch["lineage_sensitive"] and lineage == "NOT_APPLICABLE":
                fail(f"lineage-sensitive branch {bid} cannot be NOT_APPLICABLE", "E_LINEAGE_SCHEMA")
            group = branch.get("lineage_group")
            if group is not None and not id_ok(group, LINEAGE_GROUP_ID):
                fail(f"invalid lineage_group on {bid}", "E_LINEAGE_SCHEMA")
        branch_map[bid] = branch
    sensitive_groups: dict[str, set[str]] = {}
    for branch in branch_map.values():
        group = branch.get("lineage_group")
        if branch.get("material") and branch.get("lineage_sensitive") and group:
            seen = sensitive_groups.setdefault(group, set())
            lineage = branch["authority_lineage"]
            if lineage in seen:
                fail(f"lineage group {group} repeats lineage {lineage}", "E_LINEAGE_DUPLICATE")
            seen.add(lineage)
    for fid, family in family_map.items():
        if family["material"] and not any(branch["material"] and branch["family_id"] == fid for branch in branch_map.values()):
            fail(f"material family {fid} has no material branch", "E_FAMILY_EMPTY")
    candidates: dict[str, dict[str, Any]] = {}
    for relative in candidate_paths(root):
        candidate = require_object(read_json(safe_child(root, "candidates", relative)), relative)
        cid = candidate.get("candidate_id", candidate.get("id"))
        if not id_ok(cid, CANDIDATE_ID) or cid in candidates:
            fail(f"invalid or duplicate candidate ID {cid}", "E_CANDIDATE_ID")
        if any(str(key).lower() in FORBIDDEN_CANDIDATE_KEYS for key in candidate):
            fail(f"candidate {cid} contains top-level judgment/final field", "E_CANDIDATE_FINAL_FIELD")
        refs = candidate.get("branch_ids", [])
        if not isinstance(refs, list):
            fail(f"candidate {cid}.branch_ids must be an array", "E_CANDIDATE_SCHEMA")
        for bid in refs:
            if bid not in branch_map:
                fail(f"candidate {cid} references unknown branch {bid}", "E_BRANCH_UNKNOWN")
        for dep_key, pattern, code in (("policy_dependencies", POLICY_ID, "E_POLICY_UNKNOWN"), ("provider_dependencies", PROVIDER_ID, "E_PROVIDER_UNKNOWN")):
            deps = candidate.get(dep_key, [])
            if not isinstance(deps, list):
                fail(f"candidate {cid}.{dep_key} must be an array", "E_DEPENDENCY_SCHEMA")
            for dep in deps:
                item = require_object(dep, f"{cid} dependency")
                ref_key = "policy_id" if dep_key == "policy_dependencies" else "provider_fact_id"
                if not id_ok(item.get(ref_key), pattern):
                    fail(f"candidate {cid} has invalid {ref_key}", code)
                if not isinstance(item.get("material"), bool) or not isinstance(item.get("reason"), str) or not item["reason"]:
                    fail(f"candidate {cid} dependency requires material and reason", "E_DEPENDENCY_SCHEMA")
        candidates[cid] = candidate
    for branch in branch_map.values():
        refs = branch.get("candidate_ids", [])
        if not isinstance(refs, list):
            fail(f"branch {branch['branch_id']}.candidate_ids must be an array", "E_BRANCH_SCHEMA")
        for cid in refs:
            if cid not in candidates:
                fail(f"branch {branch['branch_id']} references unknown candidate {cid}", "E_CANDIDATE_UNKNOWN")
    return branches_doc, branches, {"families": family_map, "branches": branch_map, "candidates": candidates}


def validate_discovery(workdir: Path) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    doc, branches, _ = validate_discovery_tree(artifact_root(workdir))
    return doc, branches


def validate_dependency_references(structures: dict[str, Any], products: dict[str, dict[str, Any]], providers: dict[str, dict[str, Any]]) -> None:
    for cid, candidate in structures["candidates"].items():
        for dep in candidate.get("policy_dependencies", []):
            if dep["policy_id"] not in products:
                fail(f"candidate {cid} references unknown product policy {dep['policy_id']}", "E_POLICY_UNKNOWN")
        for dep in candidate.get("provider_dependencies", []):
            if dep["provider_fact_id"] not in providers:
                fail(f"candidate {cid} references unknown provider fact {dep['provider_fact_id']}", "E_PROVIDER_UNKNOWN")


def discovery_files(root: Path) -> list[str]:
    return ["context.json", "policy-contract.json", "branches.json", *[f"candidates/{p}" for p in candidate_paths(root)]]


def copy_tree_files(source_root: Path, target_root: Path, paths: Iterable[str]) -> None:
    for relative in paths:
        source = safe_child(source_root, *Path(relative).parts)
        target = safe_child(target_root, *Path(relative).parts)
        if not source.is_file():
            fail(f"missing snapshot source {relative}", "E_ARTIFACT_MISSING")
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)


def generation_root(generation_id: str, entries: list[dict[str, str]], candidate_ids: list[str], branch_ids: list[str]) -> str:
    rows = [f"generation_id={generation_id}"]
    rows.extend(f"{item['path']}:{item['sha256']}" for item in sorted(entries, key=lambda x: x["path"]))
    rows.append("candidate_ids=" + ",".join(sorted(candidate_ids)))
    rows.append("branch_ids=" + ",".join(sorted(branch_ids)))
    return hashlib.sha256(("\n".join(rows) + "\n").encode("utf-8")).hexdigest().upper()


def snapshot_entries(root: Path, paths: list[str]) -> list[dict[str, str]]:
    entries = []
    for relative in sorted(paths):
        path = safe_child(root, *Path(relative).parts)
        if not path.is_file():
            fail(f"missing frozen artifact {relative}", "E_FREEZE_MISSING")
        entries.append({"path": relative, "sha256": sha256(path)})
    return entries


def history_root(workdir: Path, generation_id: str) -> Path:
    return safe_child(artifact_root(workdir), "history", generation_id)


def history_generations(workdir: Path) -> list[str]:
    history = safe_child(artifact_root(workdir), "history")
    if not history.exists():
        return []
    values = []
    for path in history.iterdir():
        if path.is_dir():
            if not GENERATION_ID.match(path.name):
                fail(f"malformed history directory {path.name}", "E_HISTORY_MALFORMED")
            values.append(path.name)
    return sorted(values, key=lambda x: int(x[-4:]))


def validate_history(workdir: Path) -> None:
    manifest = load_manifest(workdir)
    generations = history_generations(workdir)
    numbers = [int(item[-4:]) for item in generations]
    if numbers != sorted(set(numbers)) or any(b != a + 1 for a, b in zip(numbers, numbers[1:])):
        fail("generation history is not unique and monotonically increasing", "E_HISTORY_SEQUENCE")
    for gid in generations:
        archive = history_root(workdir, gid)
        freeze = require_object(read_json(safe_child(archive, "freeze.json")), f"{gid} freeze")
        verify_archive(workdir, gid, freeze)
        record = next((item for item in manifest.get("generations", []) if isinstance(item, dict) and item.get("generation_id") == gid), None)
        if record is None or record.get("root_sha256") != freeze.get("root_sha256"):
            fail(f"manifest history binding is inconsistent for {gid}", "E_HISTORY_BINDING")
        reopen = safe_child(archive, "reopen.json")
        if reopen.is_file():
            record = require_object(read_json(reopen), f"{gid} reopen")
            if record.get("generation_id") != gid:
                fail(f"reopen record does not belong to {gid}", "E_HISTORY_REOPEN")
            next_generation = record.get("new_generation_id")
            if next_generation and next_generation != manifest.get("active_generation") and next_generation not in generations:
                fail(f"reopen record points to unknown generation {next_generation}", "E_HISTORY_REOPEN")
            previous = record.get("previous_generation_id")
            if previous and previous not in generations:
                fail(f"reopen record points to unknown generation {previous}", "E_HISTORY_REOPEN")
    active = manifest.get("active_generation")
    if active and not GENERATION_ID.match(str(active)):
        fail(f"invalid active generation {active}", "E_GENERATION_ID")


def verify_archive(workdir: Path, generation_id: str, freeze: dict[str, Any]) -> dict[str, Any]:
    if freeze.get("generation_id") != generation_id or not GENERATION_ID.match(str(generation_id)):
        fail(f"freeze generation mismatch for {generation_id}", "E_FREEZE_GENERATION")
    archive = history_root(workdir, generation_id)
    entries = require_list(freeze.get("files"), f"{generation_id}.freeze.files")
    expected_paths = set(discovery_files(archive))
    actual_paths = {item.get("path") for item in entries if isinstance(item, dict)}
    if actual_paths != expected_paths:
        fail(f"archived discovery set mismatch for {generation_id}", "E_FREEZE_SET")
    for raw in entries:
        item = require_object(raw, "freeze entry")
        relative = item.get("path")
        recorded = item.get("sha256")
        if not isinstance(relative, str) or not isinstance(recorded, str):
            fail("freeze entries require path and sha256", "E_FREEZE_SCHEMA")
        path = safe_child(archive, *Path(relative).parts)
        if not path.is_file() or sha256(path) != recorded:
            fail(f"archived frozen artifact mismatch {relative}", "E_FREEZE_MISMATCH")
    _, products, providers = validate_context_tree(archive)
    _, branches, structures = validate_discovery_tree(archive)
    validate_dependency_references(structures, products, providers)
    candidate_ids = sorted(structures["candidates"])
    branch_ids = sorted(branch["branch_id"] for branch in branches)
    expected_root = generation_root(generation_id, entries, candidate_ids, branch_ids)
    if freeze.get("root_sha256") != expected_root:
        fail(f"archived generation root mismatch for {generation_id}", "E_FREEZE_ROOT")
    return freeze


def active_generation_record(manifest: dict[str, Any]) -> dict[str, Any] | None:
    for record in manifest.get("generations", []):
        if isinstance(record, dict) and record.get("generation_id") == manifest.get("active_generation"):
            return record
    return None


def verify_freeze(workdir: Path) -> dict[str, Any]:
    manifest = load_manifest(workdir)
    active = manifest.get("active_generation")
    if not id_ok(active, GENERATION_ID):
        fail("no active frozen generation", "E_FREEZE_MISSING")
    validate_history(workdir)
    archive = history_root(workdir, active)
    archive_freeze = verify_archive(workdir, active, require_object(read_json(safe_child(archive, "freeze.json")), "archive freeze"))
    active_freeze_path = safe_child(artifact_root(workdir), "active-freeze.json")
    if not active_freeze_path.is_file() or read_json(active_freeze_path) != archive_freeze:
        fail("active freeze metadata differs from archived generation", "E_FREEZE_MISMATCH")
    record = active_generation_record(manifest)
    if not record or record.get("root_sha256") != archive_freeze.get("root_sha256"):
        fail("manifest generation/root binding differs from archive", "E_STALE_GENERATION")
    for relative in discovery_files(archive):
        active_path = safe_child(artifact_root(workdir), *Path(relative).parts)
        archived_path = safe_child(archive, *Path(relative).parts)
        if not active_path.is_file() or sha256(active_path) != sha256(archived_path):
            fail(f"active frozen artifact changed or disappeared: {relative}", "E_FREEZE_MISMATCH")
    if manifest.get("freeze_root_sha256") != archive_freeze.get("root_sha256"):
        fail("manifest freeze root is stale", "E_STALE_GENERATION")
    return archive_freeze


def freeze_discovery(workdir: Path) -> dict[str, Any]:
    manifest = load_manifest(workdir)
    if manifest.get("phase") != "DISCOVERY":
        fail(f"freeze requires DISCOVERY phase, current phase is {manifest.get('phase')}", "E_PHASE_TRANSITION")
    validate_context(workdir)
    _, branches, structures = validate_discovery_tree(artifact_root(workdir))
    _, products, providers = validate_context_tree(artifact_root(workdir))
    validate_dependency_references(structures, products, providers)
    existing_id = manifest.get("active_generation")
    if id_ok(existing_id, GENERATION_ID) and int(manifest.get("generation_number", 0)) > 0:
        number = int(manifest["generation_number"])
        generation_id = existing_id
    else:
        number = int(manifest.get("generation_number", 0)) + 1
        generation_id = f"GEN-{number:04d}"
    paths = discovery_files(artifact_root(workdir))
    entries = snapshot_entries(artifact_root(workdir), paths)
    root_hash = generation_root(generation_id, entries, sorted(structures["candidates"]), sorted(branch["branch_id"] for branch in branches))
    archive = history_root(workdir, generation_id)
    if archive.exists():
        fail(f"generation archive already exists {generation_id}", "E_GENERATION_EXISTS")
    copy_tree_files(artifact_root(workdir), archive, paths)
    freeze = {"schema_version": 2, "generation_id": generation_id, "root_sha256": root_hash, "files": entries}
    write_json(safe_child(archive, "freeze.json"), freeze)
    write_json(safe_child(artifact_root(workdir), "active-freeze.json"), freeze)
    manifest.update({"active_generation": generation_id, "generation_number": number, "freeze_root_sha256": root_hash, "phase": "FROZEN"})
    record = next((item for item in manifest.setdefault("generations", []) if item.get("generation_id") == generation_id), None)
    if record is None:
        manifest["generations"].append({"generation_id": generation_id, "generation_number": number, "root_sha256": root_hash, "phase": "FROZEN"})
    else:
        record.update({"generation_number": number, "root_sha256": root_hash, "phase": "FROZEN"})
    save_manifest(workdir, manifest)
    return freeze


def judgment_paths(workdir: Path) -> list[str]:
    paths = relative_files(safe_child(artifact_root(workdir), "judgments"))
    for relative in paths:
        name = Path(relative).name
        if not name.endswith(".json") or not id_ok(name[:-5], CANDIDATE_ID):
            fail(f"invalid judgment artifact name {relative}", "E_JUDGMENT_ID")
    return paths


def dependency_status(dep: dict[str, Any], judgment_deps: dict[str, dict[str, Any]], key: str, known: dict[str, dict[str, Any]], provider: bool) -> None:
    ref = dep[key]
    if ref not in known:
        fail(f"dependency {ref} does not resolve in its domain", "E_PROVIDER_UNKNOWN" if provider else "E_POLICY_UNKNOWN")
    resolution = judgment_deps.get(ref, {}).get("resolution")
    if resolution not in RESOLUTIONS:
        fail(f"missing dependency resolution for {ref}", "E_PROVIDER_UNRESOLVED" if provider else "E_POLICY_UNRESOLVED")
    if dep.get("material") and resolution == "SATISFIED":
        if provider and known[ref].get("status") != "ESTABLISHED":
            code = "E_PROVIDER_CONFLICT" if known[ref].get("status") == "CONFLICTED" else "E_PROVIDER_UNRESOLVED"
            fail(f"material provider fact {ref} is not established", code)
        if not provider and known[ref].get("status") in {"AMBIGUOUS", "UNSPECIFIED"}:
            fail(f"material policy {ref} is ambiguous/unspecified", "E_POLICY_AMBIGUOUS")


def validate_confirmed_evidence(judgment: dict[str, Any], candidate: dict[str, Any], products: dict[str, dict[str, Any]], providers: dict[str, dict[str, Any]]) -> None:
    required = ("invariant_status", "reachability_status", "value_consequence_status", "controls_challenged", "runtime_required", "runtime_evidence_available", "runtime_reason", "runtime_evidence", "policy_dependencies", "provider_dependencies", "evidence_matrix")
    for key in required:
        if key not in judgment:
            fail(f"confirmed {candidate['candidate_id']} missing {key}", "E_CONFIRMATION_SCHEMA")
    if judgment["invariant_status"] != "ESTABLISHED" or judgment["reachability_status"] != "ESTABLISHED" or judgment["value_consequence_status"] != "ESTABLISHED" or judgment["controls_challenged"] is not True:
        fail(f"confirmed {candidate['candidate_id']} lacks established invariant/path/value/control evidence", "E_CONFIRMATION_EVIDENCE")
    validate_finding_semantics(judgment, candidate)
    if judgment.get("severity") == "P1" and judgment.get("realized_value_status") != "ESTABLISHED":
        fail(f"P1 requires demonstrated material unauthorized commercial value for {candidate['candidate_id']}", "E_SEVERITY_VALUE")
    if not isinstance(judgment["runtime_required"], bool) or not isinstance(judgment["runtime_evidence_available"], bool) or not isinstance(judgment["runtime_reason"], str) or not isinstance(judgment["runtime_evidence"], list):
        fail(f"invalid runtime evidence matrix for {candidate['candidate_id']}", "E_RUNTIME_SCHEMA")
    if judgment["runtime_required"] and not judgment["runtime_evidence_available"]:
        fail(f"runtime evidence is required but unavailable for {candidate['candidate_id']}", "E_RUNTIME_REQUIRED")
    policy_deps = {item.get("policy_id"): item for item in require_list(judgment["policy_dependencies"], "judgment.policy_dependencies")}
    provider_deps = {item.get("provider_fact_id"): item for item in require_list(judgment["provider_dependencies"], "judgment.provider_dependencies")}
    independent = judgment.get("policy_independent_invariant") is True and isinstance(judgment.get("policy_independent_invariant_reason"), str) and bool(judgment.get("policy_independent_invariant_reason")) and bool(judgment.get("policy_independent_invariant_evidence"))
    for dep in candidate.get("policy_dependencies", []):
        if not (independent and dep.get("material") and products[dep["policy_id"]].get("status") in {"AMBIGUOUS", "UNSPECIFIED"}):
            dependency_status(dep, policy_deps, "policy_id", products, False)
        elif policy_deps.get(dep["policy_id"], {}).get("resolution") not in RESOLUTIONS:
            fail(f"missing dependency resolution for {dep['policy_id']}", "E_POLICY_UNRESOLVED")
        if dep.get("material") and products[dep["policy_id"]].get("status") in {"AMBIGUOUS", "UNSPECIFIED"} and not independent:
            fail(f"ambiguous material policy blocks confirmation for {candidate['candidate_id']}", "E_POLICY_AMBIGUOUS")
    for dep in candidate.get("provider_dependencies", []):
        dependency_status(dep, provider_deps, "provider_fact_id", providers, True)
    matrix = require_object(judgment["evidence_matrix"], "evidence_matrix")
    expected = {"invariant": "ESTABLISHED", "application_path": "ESTABLISHED", "value_consequence": "ESTABLISHED", "policy": {"SATISFIED", "NOT_MATERIAL"}, "provider": {"SATISFIED", "NOT_MATERIAL"}, "runtime": {"SATISFIED", "NOT_REQUIRED"}, "controls_challenged": True}
    for key, value in expected.items():
        actual = matrix.get(key)
        if isinstance(value, set):
            if actual not in value:
                fail(f"evidence matrix {key} is invalid for {candidate['candidate_id']}", "E_CONFIRMATION_EVIDENCE")
        elif actual != value:
            fail(f"evidence matrix {key} is invalid for {candidate['candidate_id']}", "E_CONFIRMATION_EVIDENCE")


def validate_duplicate_graph(judgments: dict[str, dict[str, Any]]) -> None:
    graph = {}
    for cid, judgment in judgments.items():
        if judgment.get("status") != "DUPLICATE":
            continue
        target = judgment.get("canonical_candidate_id")
        if target not in judgments or target == cid:
            fail(f"duplicate {cid} has invalid target {target}", "E_DUPLICATE_TARGET")
        if judgments[target].get("status") == "DUPLICATE":
            fail(f"duplicate {cid} points to another duplicate {target}", "E_DUPLICATE_CHAIN")
        graph[cid] = target
    for start in graph:
        visited: set[str] = set()
        node: str | None = start
        while node in graph:
            if node in visited:
                fail(f"duplicate cycle includes {node}", "E_DUPLICATE_CYCLE")
            visited.add(node)
            node = graph[node]


def validate_judgment(workdir: Path) -> dict[str, Any]:
    freeze = verify_freeze(workdir)
    archive = history_root(workdir, freeze["generation_id"])
    _, products, providers = validate_context_tree(archive)
    _, _, structures = validate_discovery_tree(archive)
    candidates = structures["candidates"]
    hashes = {Path(item["path"]).stem: item["sha256"] for item in freeze["files"] if item["path"].startswith("candidates/")}
    judgments: dict[str, dict[str, Any]] = {}
    for relative in judgment_paths(workdir):
        judgment = require_object(read_json(safe_child(artifact_root(workdir), "judgments", relative)), relative)
        cid = judgment.get("candidate_id")
        if cid not in candidates:
            fail(f"judgment references unknown candidate {cid}", "E_CANDIDATE_UNKNOWN")
        if cid in judgments:
            fail(f"duplicate judgment for candidate {cid}", "E_JUDGMENT_DUPLICATE")
        if judgment.get("generation_id") != freeze["generation_id"]:
            fail(f"judgment {cid} belongs to a stale generation", "E_STALE_GENERATION")
        if judgment.get("candidate_sha256") != hashes.get(cid):
            fail(f"judgment {cid} candidate hash does not match frozen bytes", "E_CANDIDATE_HASH")
        if judgment.get("freeze_root_sha256") != freeze["root_sha256"]:
            fail(f"judgment {cid} freeze root does not match", "E_FREEZE_ROOT")
        status = judgment.get("status")
        if status not in JUDGMENT_STATUSES:
            fail(f"invalid judgment status for {cid}", "E_JUDGMENT_STATUS")
        if any(key in judgment for key in ("finding_id", "final_finding_id")):
            fail(f"judgment {cid} hand-authors a public finding ID", "E_PUBLIC_ID_AUTHORING")
        if status == "CONFIRMED":
            if judgment.get("severity") not in {"P0", "P1", "P2", "P3"}:
                fail(f"confirmed candidate lacks valid severity {cid}", "E_SEVERITY_REQUIRED")
            validate_confirmed_evidence(judgment, candidates[cid], products, providers)
        elif "severity" in judgment:
            fail(f"non-confirmed candidate has severity {cid}", "E_SEVERITY_NONCONFIRMED")
        if status == "DUPLICATE" and judgment.get("canonical_candidate_id") not in candidates:
            fail(f"duplicate {cid} references missing canonical candidate", "E_DUPLICATE_TARGET")
        judgments[cid] = judgment
    if set(judgments) != set(candidates):
        fail(f"judgment coverage mismatch missing={sorted(set(candidates)-set(judgments))}", "E_JUDGMENT_MISSING")
    validate_duplicate_graph(judgments)
    if phase(workdir) == "FROZEN":
        set_phase(workdir, "JUDGMENT")
    return {"freeze": freeze, "candidates": candidates, "judgments": judgments, "products": products, "providers": providers}


def derive_family_status(outcomes: list[str]) -> str:
    if "FINDING" in outcomes:
        return "FINDINGS_CONFIRMED"
    if any(outcome in {"UNVERIFIED", "INSUFFICIENT_EVIDENCE"} for outcome in outcomes):
        return "PARTIAL"
    return "CLOSED"


def validate_coverage(workdir: Path, judgment_state: dict[str, Any]) -> dict[str, Any]:
    freeze = judgment_state["freeze"]
    coverage = require_object(read_json(safe_child(artifact_root(workdir), "coverage.json")), "coverage")
    if coverage.get("generation_id") != freeze["generation_id"]:
        fail("coverage belongs to a stale generation", "E_STALE_GENERATION")
    if coverage.get("freeze_root_sha256") != freeze["root_sha256"]:
        fail("coverage freeze root does not match", "E_FREEZE_ROOT")
    archive = history_root(workdir, freeze["generation_id"])
    _, branches, structures = validate_discovery_tree(archive)
    material = {branch["branch_id"]: branch for branch in branches if branch["material"]}
    rows = require_list(coverage.get("branches"), "coverage.branches")
    row_by_id: dict[str, dict[str, Any]] = {}
    for raw in rows:
        row = require_object(raw, "coverage branch")
        bid = row.get("branch_id")
        if bid not in material:
            fail(f"coverage references unknown/non-material branch {bid}", "E_BRANCH_UNKNOWN")
        if bid in row_by_id:
            fail(f"duplicate coverage branch {bid}", "E_BRANCH_DUPLICATE")
        if row.get("family_id") != material[bid]["family_id"]:
            fail(f"coverage family mismatch for {bid}", "E_FAMILY_UNKNOWN")
        if row.get("authority_lineage") != material[bid]["authority_lineage"]:
            fail(f"coverage lineage mismatch for {bid}", "E_LINEAGE_SCHEMA")
        if row.get("outcome") not in OUTCOMES:
            fail(f"invalid branch outcome for {bid}", "E_BRANCH_OUTCOME")
        refs = row.get("candidate_ids", [])
        if not isinstance(refs, list):
            fail(f"coverage candidate_ids must be an array for {bid}", "E_COVERAGE_SCHEMA")
        for cid in refs:
            if cid not in judgment_state["candidates"]:
                fail(f"coverage references unknown candidate {cid}", "E_CANDIDATE_UNKNOWN")
        row_by_id[bid] = row
    if set(row_by_id) != set(material):
        fail(f"coverage missing material branches {sorted(set(material)-set(row_by_id))}", "E_BRANCH_MISSING_OUTCOME")
    material_families = {fid: family for fid, family in structures["families"].items() if family["material"]}
    family_rows = require_list(coverage.get("families"), "coverage.families")
    family_by_id: dict[str, dict[str, Any]] = {}
    for raw in family_rows:
        item = require_object(raw, "coverage family")
        fid = item.get("family_id")
        if fid not in material_families or fid in family_by_id:
            fail(f"unknown or duplicate family {fid}", "E_FAMILY_UNKNOWN")
        branch_ids = item.get("branch_ids")
        expected_children = {bid for bid, branch in material.items() if branch["family_id"] == fid}
        if not isinstance(branch_ids, list) or set(branch_ids) != expected_children:
            fail(f"family {fid} does not enumerate exact material children", "E_FAMILY_CHILDREN")
        derived = derive_family_status([row_by_id[bid]["outcome"] for bid in branch_ids])
        if "outcome" in item and item["outcome"] != derived:
            fail(f"family {fid} has conflicting hand-authored outcome", "E_FAMILY_DERIVATION")
        family_by_id[fid] = {"family_id": fid, "name": material_families[fid]["name"], "branch_ids": sorted(branch_ids), "outcome": derived}
    if set(family_by_id) != set(material_families):
        fail(f"missing material family rows {sorted(set(material_families)-set(family_by_id))}", "E_FAMILY_MISSING")
    confirmed = {cid for cid, item in judgment_state["judgments"].items() if item["status"] == "CONFIRMED"}
    for cid in confirmed:
        if not any(cid in row.get("candidate_ids", []) and row["outcome"] == "FINDING" for row in row_by_id.values()):
            fail(f"confirmed candidate lacks FINDING branch {cid}", "E_CONFIRMED_NO_FINDING_BRANCH")
    for row in row_by_id.values():
        if row["outcome"] == "FINDING" and not any(cid in confirmed for cid in row.get("candidate_ids", [])):
            fail(f"FINDING branch lacks canonical confirmed candidate {row['branch_id']}", "E_FINDING_NO_CONFIRMED")
        if row["outcome"] == "FINDING" and any(judgment_state["judgments"][cid]["status"] != "CONFIRMED" for cid in row.get("candidate_ids", [])):
            fail(f"non-canonical candidate sources finding branch {row['branch_id']}", "E_FINDING_NONCANONICAL")
    return {"coverage": coverage, "branches": [row_by_id[bid] for bid in sorted(row_by_id)], "families": [family_by_id[fid] for fid in sorted(family_by_id)]}


def candidate_number(cid: str) -> int:
    return int(cid.split("-")[1])


def derive_final(workdir: Path, judgment_state: dict[str, Any], coverage_state: dict[str, Any]) -> dict[str, Any]:
    freeze = judgment_state["freeze"]
    judgments = judgment_state["judgments"]
    canonical = sorted((item for item in judgments.values() if item["status"] == "CONFIRMED"), key=lambda item: candidate_number(item["candidate_id"]))
    id_map = {item["candidate_id"]: f"RP-{index:03d}" for index, item in enumerate(canonical, 1)}
    confirmed = []
    for item in canonical:
        projected = dict(item)
        projected["finding_id"] = id_map[item["candidate_id"]]
        confirmed.append(projected)
    rows = coverage_state["branches"]
    unresolved = any(row["outcome"] in {"UNVERIFIED", "INSUFFICIENT_EVIDENCE"} for row in rows)
    context = read_json(safe_child(artifact_root(workdir), "context.json"))
    baseline_blocked = context.get("baseline_status") == "BLOCKED"
    coverage_status = "BLOCKED" if baseline_blocked else ("PARTIAL" if unresolved else "COMPLETE")
    verdict = "BLOCKED" if baseline_blocked else ("FINDINGS CONFIRMED" if confirmed else ("PASS" if coverage_status == "COMPLETE" else "PARTIAL"))
    outcome_totals = {outcome: 0 for outcome in sorted(OUTCOMES)}
    for row in rows:
        outcome_totals[row["outcome"]] += 1
    severity_totals = {severity: 0 for severity in ("P0", "P1", "P2", "P3")}
    for item in confirmed:
        severity_totals[item["severity"]] += 1
    statuses = {status: sum(1 for item in judgments.values() if item["status"] == status) for status in JUDGMENT_STATUSES}
    return {"schema_version": 2, "generation_id": freeze["generation_id"], "freeze_root_sha256": freeze["root_sha256"], "finding_verdict": "FINDINGS_CONFIRMED" if confirmed else "NO_CONFIRMED_FINDINGS", "coverage_status": coverage_status, "verdict": verdict, "finding_id_map": id_map, "candidate_totals": {"total": len(judgments), "confirmed": statuses["CONFIRMED"], "needs_review": statuses["NEEDS_REVIEW"], "rejected": statuses["REJECTED"], "duplicates": statuses["DUPLICATE"]}, "finding_totals": {"confirmed": len(confirmed)}, "severity_totals": severity_totals, "outcome_totals": outcome_totals, "confirmed_findings": confirmed, "branches": rows, "families": coverage_state["families"]}


def validate_structured(workdir: Path, check_final: bool = True) -> dict[str, Any]:
    validate_history(workdir)
    validate_context(workdir)
    verify_freeze(workdir)
    judgment_state = validate_judgment(workdir)
    coverage_state = validate_coverage(workdir, judgment_state)
    final = derive_final(workdir, judgment_state, coverage_state)
    final_path = safe_child(artifact_root(workdir), "final.json")
    if check_final and final_path.is_file() and read_json(final_path) != final:
        fail("final.json is inconsistent with regenerated structured state", "E_FINAL_TAMPERED")
    return {"judgment": judgment_state, "coverage": coverage_state, "final": final}


def scalar(value: Any) -> str:
    if value is None:
        return "unknown"
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False, sort_keys=True)
    return str(value)


def render_documents(workdir: Path, state: dict[str, Any]) -> dict[str, str]:
    final = state["final"]
    context = read_json(safe_child(artifact_root(workdir), "context.json"))
    policy = read_json(safe_child(artifact_root(workdir), "policy-contract.json"))
    summary = ["# RivetPay Summary", "", "## Verdict", "", f"- Overall verdict: `{final['verdict']}`", f"- Finding verdict: `{final['finding_verdict']}`", f"- Coverage status: `{final['coverage_status']}`", f"- Generation: `{final['generation_id']}`", "", "## Metadata", "", f"- Repository: `{scalar(context.get('repository'))}`", f"- Review mode: `{scalar(context.get('review_mode'))}`", "", "## Derived totals", "", f"- Candidate totals: {json.dumps(final['candidate_totals'], sort_keys=True)}", f"- Finding totals: {json.dumps(final['finding_totals'], sort_keys=True)}", f"- Severity totals: {json.dumps(final['severity_totals'], sort_keys=True)}", "", "## Confirmed findings", "", "| ID | Candidate | Severity | Title |", "|---|---|---|---|"]
    summary.extend(f"| {item['finding_id']} | {item['candidate_id']} | {item['severity']} | {scalar(item.get('title'))} |" for item in final["confirmed_findings"])
    if not final["confirmed_findings"]:
        summary.append("| — | — | — | None |")
    summary.extend(["", "## Policy/provider record", "", json.dumps(policy, ensure_ascii=False, indent=2, sort_keys=True), ""])
    authority = ["# RivetPay Authority / State Map", "", "## Context", "", json.dumps(context, ensure_ascii=False, indent=2, sort_keys=True), "", "## Policy and provider contract", "", json.dumps(policy, ensure_ascii=False, indent=2, sort_keys=True), "", "## Value Authority Graph", "", "```text", "authority → evidence → interpretation → grant state → entitlement → enforcement → consumption", "```", "", "## Material branches", ""]
    authority.extend(f"- `{row['branch_id']}` `{row.get('authority_lineage')}` → `{row['outcome']}`: {scalar(row.get('predicate', row.get('description')))}" for row in final["branches"])
    authority.append("")
    findings = ["# RivetPay Findings", ""]
    if not final["confirmed_findings"]:
        findings.append("No canonical confirmed findings.")
    for item in final["confirmed_findings"]:
        findings.extend([f"## {item['finding_id']} — {scalar(item.get('title'))}", "", f"- Candidate: `{item['candidate_id']}`", f"- Severity: `{item['severity']}`", f"- Target value: {scalar(item.get('target_value'))}", "", "### Invariant", "", scalar(item.get("invariant")), "", "### Path and evidence", "", scalar(item.get("path", item.get("attack_path"))), "", scalar(item.get("evidence")), ""])
    coverage = ["# RivetPay Coverage and Defenses", "", f"- Overall verdict: `{final['verdict']}`", f"- Coverage status: `{final['coverage_status']}`", "", "## Branch / outcome ledger", "", "| Branch | Family | Lineage | Outcome |", "|---|---|---|---|", *[f"| {row['branch_id']} | {row['family_id']} | {row['authority_lineage']} | {row['outcome']} |" for row in final["branches"]], "", "## Families", "", *[f"- `{family['family_id']}`: `{family['outcome']}` ({', '.join(family['branch_ids'])})" for family in final["families"]], "", "## Derived outcome totals", "", json.dumps(final["outcome_totals"], sort_keys=True), ""]
    return {REPORT_NAMES[0]: "\n".join(summary), REPORT_NAMES[1]: "\n".join(authority), REPORT_NAMES[2]: "\n".join(findings), REPORT_NAMES[3]: "\n".join(coverage)}


def finalize(workdir: Path) -> dict[str, Any]:
    if phase(workdir) not in {"FROZEN", "JUDGMENT", "FINALIZED"}:
        fail(f"finalize requires FROZEN or JUDGMENT phase, current phase is {phase(workdir)}", "E_PHASE_TRANSITION")
    state = validate_structured(workdir, check_final=False)
    write_json(safe_child(artifact_root(workdir), "final.json"), state["final"])
    set_phase(workdir, "FINALIZED")
    return state["final"]


def render(workdir: Path) -> None:
    if phase(workdir) != "FINALIZED":
        fail("render requires FINALIZED phase", "E_PHASE_TRANSITION")
    state = validate_structured(workdir)
    root = report_root(workdir)
    root.mkdir(parents=True, exist_ok=True)
    for name, content in render_documents(workdir, state).items():
        safe_child(root, name).write_text(content.rstrip() + "\n", encoding="utf-8", newline="\n")


def validate_reports(workdir: Path, state: dict[str, Any]) -> None:
    root = report_root(workdir)
    expected = render_documents(workdir, state)
    if sorted(relative_files(root)) != sorted(expected):
        fail("report tree is not the fixed projection", "E_REPORT_TREE")
    for name, content in expected.items():
        if safe_child(root, name).read_text(encoding="utf-8") != content.rstrip() + "\n":
            fail(f"report is not deterministic projection: {name}", "E_REPORT_TAMPERED")


def remove_active_state(workdir: Path) -> None:
    root = artifact_root(workdir)
    for path in safe_child(root, "judgments").rglob("*") if safe_child(root, "judgments").exists() else []:
        if path.is_file():
            path.unlink()
    for name in ("active-freeze.json", "coverage.json", "final.json"):
        path = safe_child(root, name)
        if path.exists():
            path.unlink()
    reports = report_root(workdir)
    for name in REPORT_NAMES:
        path = safe_child(reports, name)
        if path.exists():
            path.unlink()


def reopen_discovery(workdir: Path, reason: str) -> dict[str, Any]:
    if not isinstance(reason, str) or not reason.strip():
        fail("reopen-discovery requires a non-empty reason", "E_REOPEN_REASON")
    current_phase = phase(workdir)
    if current_phase not in {"FROZEN", "JUDGMENT", "FINALIZED"}:
        fail(f"reopen is not allowed from {current_phase}", "E_PHASE_TRANSITION")
    freeze = verify_freeze(workdir)
    manifest = load_manifest(workdir)
    old_id = freeze["generation_id"]
    number = int(manifest.get("generation_number", 0)) + 1
    new_id = f"GEN-{number:04d}"
    archive = history_root(workdir, old_id)
    source_judgments = safe_child(artifact_root(workdir), "judgments")
    if source_judgments.exists():
        copy_tree_files(artifact_root(workdir), archive, [f"judgments/{p}" for p in relative_files(source_judgments)])
    for name in ("coverage.json", "final.json"):
        source = safe_child(artifact_root(workdir), name)
        if source.is_file():
            shutil.copyfile(source, safe_child(archive, name))
    archived_branches = validate_discovery_tree(archive)[1]
    record = {"schema_version": 1, "generation_id": old_id, "new_generation_id": new_id, "previous_generation_id": None, "previous_root_sha256": freeze["root_sha256"], "reason": reason.strip(), "previous_phase": current_phase, "candidate_count": len([p for p in freeze["files"] if p["path"].startswith("candidates/")]), "branch_count": len(archived_branches)}
    write_json(safe_child(archive, "reopen.json"), record)
    remove_active_state(workdir)
    manifest.update({"active_generation": new_id, "generation_number": number, "freeze_root_sha256": None, "phase": "DISCOVERY"})
    manifest.setdefault("generations", []).append({"generation_id": new_id, "generation_number": number, "root_sha256": None, "phase": "DISCOVERY", "previous_generation_id": old_id})
    save_manifest(workdir, manifest)
    return {"previous_generation_id": old_id, "generation_id": new_id, "reason": reason.strip()}


def init(workdir: Path) -> None:
    root = artifact_root(workdir)
    root.mkdir(parents=True, exist_ok=True)
    safe_child(root, "candidates").mkdir(parents=True, exist_ok=True)
    safe_child(root, "judgments").mkdir(parents=True, exist_ok=True)
    safe_child(root, "history").mkdir(parents=True, exist_ok=True)
    defaults = {
        "context.json": {"schema_version": 2, "repository": str(workdir.resolve()), "branch": None, "revision": None, "dirty_state": None, "review_mode": "READ-ONLY / DISCOVERY-ONLY", "provider_grant_model": None, "live_system_scope": None, "baseline_status": "READY", "assumptions": [], "guarantees": [], "contradictions": [], "unknowns": [], "open_questions": []},
        "policy-contract.json": {"schema_version": 2, "product_policy_claims": [], "provider_contract_facts": [], "grant_authorities": [], "contradictions": [], "unknowns": [], "open_questions": []},
        "branches.json": {"schema_version": 2, "families": [], "branches": []},
        "manifest.json": {"schema_version": 2, "phase": "CONTEXT", "active_generation": None, "generation_number": 0, "freeze_root_sha256": None, "generations": []},
    }
    for name, value in defaults.items():
        path = safe_child(root, name)
        if not path.exists():
            write_json(path, value)


def validate_regression_corpus(package_root: Path) -> dict[str, Any]:
    eval_path = safe_child(package_root, "evals", "evals.json")
    if sha256(eval_path) != "07022C69D60EF795BC01CC098C2EFA9D52CCA42EFE4719BDC23175DABF127790":
        fail("methodology evals hash changed from the required 210-entry corpus", "E_EVALS_CHANGED")
    evals = read_json(eval_path)
    if not isinstance(evals, list) or len(evals) != 210:
        fail("methodology evals must remain the 210-entry corpus", "E_EVAL_COUNT")
    cases = require_list(read_json(safe_child(package_root, "evals", "regression-cases.json")), "regression cases")
    ids: set[str] = set()
    fixture_root = safe_child(package_root, "evals", "fixtures")
    for raw in cases:
        item = require_object(raw, "regression case")
        cid = item.get("id")
        if not id_ok(cid, REGRESSION_ID) or cid in ids:
            fail(f"invalid or duplicate regression case ID {cid}", "E_REGRESSION_ID")
        ids.add(cid)
        if not item.get("name") or not item.get("prompt") or item.get("provider") != "MockPay":
            fail(f"invalid regression case metadata {cid}", "E_REGRESSION_SCHEMA")
        relative = item.get("fixture_path")
        if not isinstance(relative, str):
            fail(f"missing fixture path {cid}", "E_REGRESSION_SCHEMA")
        fixture = safe_child(package_root, relative)
        try:
            fixture.relative_to(fixture_root)
        except ValueError:
            fail(f"fixture path escapes fixture root {relative}", "E_PATH_CONTAINMENT")
        if not fixture.is_dir() or not any(path.is_file() for path in fixture.rglob("*")):
            fail(f"fixture directory missing or empty {relative}", "E_REGRESSION_FIXTURE")
    return {"eval_count": len(evals), "case_count": len(cases), "case_ids": sorted(ids)}


def status(workdir: Path) -> dict[str, Any]:
    root = artifact_root(workdir)
    if not root.is_dir() or not manifest_path(workdir).is_file():
        result = {"initialized": False}
        print(json.dumps(result, indent=2, sort_keys=True))
        return result
    manifest = load_manifest(workdir)
    judgment_count = len(judgment_paths(workdir))
    counts = {name: 0 for name in ("CONFIRMED", "NEEDS_REVIEW", "REJECTED", "DUPLICATE")}
    if judgment_count and safe_child(root, "active-freeze.json").is_file():
        try:
            values = [item["status"] for item in validate_judgment(workdir)["judgments"].values()]
            counts = {name: values.count(name) for name in counts}
        except GateError:
            pass
    material = unresolved = family_count = 0
    coverage_status = None
    try:
        _, branches, structures = validate_discovery_tree(root)
        material = sum(1 for branch in branches if branch.get("material"))
        family_count = sum(1 for family in structures["families"].values() if family.get("material"))
        if safe_child(root, "coverage.json").is_file() and safe_child(root, "active-freeze.json").is_file():
            cov = validate_coverage(workdir, validate_judgment(workdir))
            unresolved = sum(1 for row in cov["branches"] if row["outcome"] in {"UNVERIFIED", "INSUFFICIENT_EVIDENCE"})
            coverage_status = "PARTIAL" if unresolved else "COMPLETE"
    except GateError:
        pass
    integrity = False
    if safe_child(root, "active-freeze.json").is_file():
        try:
            verify_freeze(workdir)
            integrity = True
        except GateError:
            pass
    result = {"initialized": True, "phase": manifest.get("phase"), "active_generation": manifest.get("active_generation"), "freeze_root_sha256": manifest.get("freeze_root_sha256"), "candidate_count": len(candidate_paths(root)), "judgment_count": judgment_count, "confirmed_count": counts["CONFIRMED"], "needs_review_count": counts["NEEDS_REVIEW"], "rejected_count": counts["REJECTED"], "duplicate_count": counts["DUPLICATE"], "material_branch_count": material, "unresolved_branch_count": unresolved, "family_count": family_count, "coverage_status": coverage_status, "overall_verdict": read_json(safe_child(root, "final.json")).get("verdict") if safe_child(root, "final.json").is_file() else None, "freeze_integrity": integrity, "reports": sorted(relative_files(report_root(workdir)))}
    print(json.dumps(result, indent=2, sort_keys=True))
    return result


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("init", "validate-context", "freeze-discovery", "reopen-discovery", "validate-judgment", "finalize", "render", "validate", "status", "validate-regression-corpus"))
    parser.add_argument("--workdir", type=Path, default=Path.cwd())
    parser.add_argument("--package-root", type=Path)
    parser.add_argument("--reason")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    try:
        workdir = args.workdir.resolve()
        if args.command == "init":
            init(workdir)
            print(json.dumps({"initialized": True, "workdir": str(workdir)}, sort_keys=True))
        elif args.command == "validate-context":
            validate_context(workdir)
            if phase(workdir) == "CONTEXT":
                set_phase(workdir, "DISCOVERY")
            print("context valid")
        elif args.command == "freeze-discovery":
            freeze = freeze_discovery(workdir)
            print(json.dumps({"generation_id": freeze["generation_id"], "root_sha256": freeze["root_sha256"], "frozen_files": len(freeze["files"])}, sort_keys=True))
        elif args.command == "reopen-discovery":
            print(json.dumps(reopen_discovery(workdir, args.reason or ""), sort_keys=True))
        elif args.command == "validate-judgment":
            state = validate_judgment(workdir)
            print(json.dumps({"generation_id": state["freeze"]["generation_id"], "judgments": len(state["judgments"])}, sort_keys=True))
        elif args.command == "finalize":
            final = finalize(workdir)
            print(json.dumps({"verdict": final["verdict"], "findings": final["finding_totals"]["confirmed"]}, sort_keys=True))
        elif args.command == "render":
            render(workdir)
            print("reports rendered")
        elif args.command == "validate":
            state = validate_structured(workdir)
            validate_reports(workdir, state)
            print(json.dumps({"valid": True, "verdict": state["final"]["verdict"]}, sort_keys=True))
        elif args.command == "status":
            status(workdir)
        elif args.command == "validate-regression-corpus":
            package_root = (args.package_root or Path(__file__).resolve().parents[1]).resolve()
            print(json.dumps(validate_regression_corpus(package_root), sort_keys=True))
        return 0
    except GateError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
