#!/usr/bin/env python3
"""
sync.py — Skill synchronization for the llms-txt-advisor plugin

Adapted from anthropics/financial-services/scripts/sync-agent-skills.py pattern.

In the financial-services pattern, agents are self-contained: they bundle a
synced copy of every skill they need from vertical-plugins/. sync.py uses
shutil.copytree to propagate updates from the source to all agent bundles.

In our current plugin, skills are not duplicated (single source of truth in
skills/). This script:
  1. Validates the plugin has no drift (currently a no-op since no duplicates)
  2. Sets up scaffolding to add agent bundles in the future
  3. Auto-bumps plugin.json version on detected changes (optional)

Usage:
  python3 scripts/sync.py             # validate (no drift in current layout)
  python3 scripts/sync.py --version-bump  # patch-bump plugin.json version
  python3 scripts/sync.py --add-agent-bundle <name>  # scaffold a new agent bundle
"""

import argparse
import json
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = ROOT / "skills"
AGENT_BUNDLES_DIR = ROOT / "agent-bundles"  # Future: where bundled agent copies live


def list_skills():
    """Return list of (skill_name, path) tuples for all canonical skills."""
    if not SKILLS_DIR.exists():
        return []
    return [(p.name, p) for p in sorted(SKILLS_DIR.iterdir()) if p.is_dir() and (p / "SKILL.md").exists()]


def sync_drift_check():
    """Check for drift between source-of-truth skills and any agent bundles."""
    print("=== Drift check ===")

    if not AGENT_BUNDLES_DIR.exists():
        print(f"  INFO: {AGENT_BUNDLES_DIR.relative_to(ROOT)} does not exist — no agent bundles to sync")
        print("  INFO: skills/ is the single source of truth (current layout)")
        return 0

    skills = {name: path for name, path in list_skills()}
    drift_count = 0

    for bundle in sorted(AGENT_BUNDLES_DIR.iterdir()):
        if not bundle.is_dir():
            continue
        bundle_skills_dir = bundle / "skills"
        if not bundle_skills_dir.exists():
            continue

        for bundle_skill in bundle_skills_dir.iterdir():
            if not bundle_skill.is_dir():
                continue
            name = bundle_skill.name
            if name not in skills:
                print(f"  WARN: {bundle.name}/skills/{name} has no source-of-truth in skills/")
                continue

            source = skills[name]
            # Compare directory tree contents
            if not directories_equal(source, bundle_skill):
                print(f"  FAIL: drift detected: {bundle.name}/skills/{name} differs from skills/{name}")
                drift_count += 1

    if drift_count == 0:
        print("  PASS: no drift detected")
        return 0

    print(f"\n  {drift_count} drift(s) detected. Run with --sync to fix.")
    return 1


def directories_equal(dir_a, dir_b):
    """Compare two directories byte-for-byte."""
    files_a = sorted([p.relative_to(dir_a) for p in dir_a.rglob("*") if p.is_file()])
    files_b = sorted([p.relative_to(dir_b) for p in dir_b.rglob("*") if p.is_file()])
    if files_a != files_b:
        return False
    for rel in files_a:
        if (dir_a / rel).read_bytes() != (dir_b / rel).read_bytes():
            return False
    return True


def do_sync():
    """Copy source-of-truth skills into all agent bundles."""
    print("=== Sync ===")

    if not AGENT_BUNDLES_DIR.exists():
        print("  INFO: no agent-bundles/ directory — nothing to sync")
        return 0

    skills = {name: path for name, path in list_skills()}
    synced_count = 0

    for bundle in sorted(AGENT_BUNDLES_DIR.iterdir()):
        if not bundle.is_dir():
            continue
        bundle_skills_dir = bundle / "skills"
        if not bundle_skills_dir.exists():
            bundle_skills_dir.mkdir(parents=True)

        # For each skill referenced in the bundle (by directory presence), sync it
        for skill_marker in bundle_skills_dir.iterdir():
            if not skill_marker.is_dir():
                continue
            name = skill_marker.name
            if name not in skills:
                print(f"  WARN: {bundle.name}/skills/{name} has no source — skipping")
                continue

            source = skills[name]
            print(f"  SYNC: skills/{name} → {bundle.name}/skills/{name}")
            shutil.rmtree(skill_marker)
            shutil.copytree(source, skill_marker)
            synced_count += 1

    print(f"\n  Synced {synced_count} skill(s)")
    return 0


def add_agent_bundle(name):
    """Create scaffolding for a new agent bundle."""
    print(f"=== Adding agent bundle: {name} ===")

    AGENT_BUNDLES_DIR.mkdir(exist_ok=True)
    bundle_dir = AGENT_BUNDLES_DIR / name
    if bundle_dir.exists():
        print(f"  FAIL: {bundle_dir.relative_to(ROOT)} already exists")
        return 1

    bundle_dir.mkdir()
    (bundle_dir / "skills").mkdir()
    (bundle_dir / ".claude-plugin").mkdir()

    # Write plugin.json
    plugin_json = {
        "name": name,
        "version": "0.1.0",
        "description": f"Agent bundle: {name}",
        "author": {"name": "llms-txt-advisor"}
    }
    (bundle_dir / ".claude-plugin" / "plugin.json").write_text(json.dumps(plugin_json, indent=2))

    # Write README
    readme = f"""# Agent Bundle: {name}

This agent bundle is self-contained. It vendors copies of skills it depends on
from the canonical `skills/` directory at plugin root. Use `scripts/sync.py`
to keep this bundle in sync with the source-of-truth.

## Bundled skills

(Add skills here by creating subdirectories under `./skills/` matching the
canonical skill names from `../../skills/`. Then run:

    python3 ../../scripts/sync.py --sync

to populate them.)
"""
    (bundle_dir / "README.md").write_text(readme)

    print(f"  PASS: created {bundle_dir.relative_to(ROOT)}")
    print(f"  Next: create subdirectories under {bundle_dir.relative_to(ROOT)}/skills/ for each skill to bundle, then run --sync")
    return 0


def version_bump():
    """Patch-bump plugin.json version."""
    print("=== Version bump ===")

    plugin_json_path = ROOT / ".claude-plugin" / "plugin.json"
    if not plugin_json_path.exists():
        print(f"  FAIL: {plugin_json_path.relative_to(ROOT)} does not exist")
        return 1

    with open(plugin_json_path) as f:
        data = json.load(f)

    current = data.get("version", "0.0.0")
    match = re.match(r"^(\d+)\.(\d+)\.(\d+)(.*)$", current)
    if not match:
        print(f"  FAIL: current version '{current}' is not semver")
        return 1

    major, minor, patch, suffix = match.groups()
    new_patch = int(patch) + 1
    new_version = f"{major}.{minor}.{new_patch}{suffix}"

    data["version"] = new_version
    with open(plugin_json_path, "w") as f:
        json.dump(data, f, indent=2)
        f.write("\n")

    print(f"  PASS: bumped version {current} → {new_version}")
    return 0


def main():
    parser = argparse.ArgumentParser(description="Sync skills across agent bundles")
    parser.add_argument("--sync", action="store_true", help="Copy source-of-truth skills into agent bundles")
    parser.add_argument("--check", action="store_true", help="Check for drift (default action)")
    parser.add_argument("--version-bump", action="store_true", help="Patch-bump plugin.json version")
    parser.add_argument("--add-agent-bundle", metavar="NAME", help="Scaffold a new agent bundle")
    args = parser.parse_args()

    print(f"sync.py — managing plugin at {ROOT}")
    print()

    if args.add_agent_bundle:
        return add_agent_bundle(args.add_agent_bundle)

    if args.version_bump:
        return version_bump()

    if args.sync:
        return do_sync()

    # Default: check for drift
    return sync_drift_check()


if __name__ == "__main__":
    sys.exit(main())
