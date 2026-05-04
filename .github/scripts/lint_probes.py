#!/usr/bin/env python3
"""Lint all probe YAMLs for schema compliance.

Validates per SCHEMA.md:
- Required fields present
- id globally unique
- mappings has all 4 keys
- judge_rubric_path resolves
- prompts non-empty list

Exits 0 on success, 1 on any failure.
"""
from __future__ import annotations

import sys
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
PROBES_DIR = REPO_ROOT / "probes"
RUBRICS_DIR = REPO_ROOT / "rubrics"

REQUIRED_FIELDS = {"id", "name", "attack_class", "target_class", "severity", "prompts", "mappings", "judge"}
REQUIRED_MAPPING_KEYS = {"atlas", "owasp_llm", "nist_ai_rmf", "eu_ai_act"}
REQUIRED_JUDGE_KEYS = {"model", "rubric_path"}


def main() -> int:
    if not PROBES_DIR.is_dir():
        print(f"ERROR: probes/ directory not found at {PROBES_DIR}", file=sys.stderr)
        return 1

    errors: list[str] = []
    seen_ids: dict[str, Path] = {}

    for yaml_path in sorted(PROBES_DIR.glob("**/*.yaml")):
        rel = yaml_path.relative_to(REPO_ROOT)
        try:
            doc = yaml.safe_load(yaml_path.read_text())
        except yaml.YAMLError as e:
            errors.append(f"{rel}: malformed YAML: {e}")
            continue
        if not isinstance(doc, dict):
            errors.append(f"{rel}: top-level must be a mapping (got {type(doc).__name__})")
            continue

        # Required fields
        missing = REQUIRED_FIELDS - set(doc.keys())
        if missing:
            errors.append(f"{rel}: missing required fields: {sorted(missing)}")
            continue

        # id uniqueness
        probe_id = doc["id"]
        if probe_id in seen_ids:
            errors.append(f"{rel}: id {probe_id!r} duplicates {seen_ids[probe_id]}")
        else:
            seen_ids[probe_id] = rel

        # mappings
        mappings = doc.get("mappings")
        if not isinstance(mappings, dict):
            errors.append(f"{rel}: mappings must be a mapping")
        else:
            missing_keys = REQUIRED_MAPPING_KEYS - set(mappings.keys())
            if missing_keys:
                errors.append(f"{rel}: mappings missing keys: {sorted(missing_keys)}")
            for key in REQUIRED_MAPPING_KEYS & set(mappings.keys()):
                if not isinstance(mappings[key], list):
                    errors.append(f"{rel}: mappings.{key} must be a list (got {type(mappings[key]).__name__})")

        # attack_class non-empty list
        attack_class = doc.get("attack_class")
        if not isinstance(attack_class, list) or len(attack_class) == 0:
            errors.append(f"{rel}: attack_class must be a non-empty list")

        # prompts non-empty list
        prompts = doc.get("prompts")
        if not isinstance(prompts, list) or len(prompts) == 0:
            errors.append(f"{rel}: prompts must be a non-empty list")

        # judge nested object with model + rubric_path
        judge = doc.get("judge")
        if not isinstance(judge, dict):
            errors.append(f"{rel}: judge must be a mapping with model + rubric_path")
        else:
            missing_judge = REQUIRED_JUDGE_KEYS - set(judge.keys())
            if missing_judge:
                errors.append(f"{rel}: judge missing keys: {sorted(missing_judge)}")

            # judge.rubric_path resolves
            rubric_path_str = judge.get("rubric_path", "")
            if rubric_path_str:
                rel_rubric = rubric_path_str
                if rel_rubric.startswith("rubrics/"):
                    rel_rubric = rel_rubric[len("rubrics/"):]
                full_path = RUBRICS_DIR / rel_rubric
                if not full_path.is_file():
                    errors.append(f"{rel}: judge.rubric_path {rubric_path_str!r} does not resolve to file at {full_path}")

    if errors:
        print(f"❌ {len(errors)} probe lint errors:", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 1
    print(f"✅ Linted {len(seen_ids)} probes; all valid.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
