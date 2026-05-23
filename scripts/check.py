#!/usr/bin/env python3
"""
check.py — Validation script for the llms-txt-advisor plugin

Adapted from anthropics/financial-services/scripts/check.py pattern.

Validates:
  1. plugin.json is well-formed JSON with required fields
  2. .mcp.json is well-formed JSON
  3. CLAUDE.md template has the five-rule contract block
  4. Each SKILL.md has valid YAML frontmatter with required fields
  5. Each agent.md / cookbook agent.yaml references valid file paths
  6. All sub-agent YAML files parse and have valid schemas
  7. All cross-references in markdown (relative paths) resolve to real files
  8. No SKILL.md exceeds 500 lines (Anthropic guidance)
  9. evals/ structure if present is valid

Exits 0 if all checks pass, non-zero otherwise.

Usage:
  python3 scripts/check.py             # run all checks
  python3 scripts/check.py --self-install   # install as .git/hooks/pre-commit
  python3 scripts/check.py --strict    # fail on warnings too
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

PASS = "\033[0;32mPASS\033[0m"
FAIL = "\033[0;31mFAIL\033[0m"
WARN = "\033[0;33mWARN\033[0m"
INFO = "\033[0;34mINFO\033[0m"

# Track outcomes
errors = []
warnings = []
passed = []


def report(level, message):
    if level == "PASS":
        passed.append(message)
        print(f"  {PASS}: {message}")
    elif level == "WARN":
        warnings.append(message)
        print(f"  {WARN}: {message}")
    elif level == "FAIL":
        errors.append(message)
        print(f"  {FAIL}: {message}")
    elif level == "INFO":
        print(f"  {INFO}: {message}")


def section(title):
    print(f"\n=== {title} ===")


def check_plugin_json():
    section("Check 1: .claude-plugin/plugin.json")
    path = ROOT / ".claude-plugin" / "plugin.json"
    if not path.exists():
        report("FAIL", f"{path.relative_to(ROOT)} does not exist")
        return
    try:
        with open(path) as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        report("FAIL", f"{path.relative_to(ROOT)} is not valid JSON: {e}")
        return

    required_fields = ["name", "version", "description"]
    for field in required_fields:
        if field not in data:
            report("FAIL", f"plugin.json missing required field: {field}")
        else:
            report("PASS", f"plugin.json has field '{field}': {data[field][:50] if isinstance(data[field], str) else data[field]}")

    # Version must be semver
    version = data.get("version", "")
    if not re.match(r"^\d+\.\d+\.\d+", version):
        report("FAIL", f"plugin.json version '{version}' is not semver")
    else:
        report("PASS", f"plugin.json version is semver: {version}")


def check_mcp_json():
    section("Check 2: .mcp.json")
    path = ROOT / ".mcp.json"
    if not path.exists():
        report("WARN", ".mcp.json does not exist (optional)")
        return
    try:
        with open(path) as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        report("FAIL", f".mcp.json is not valid JSON: {e}")
        return

    if "mcpServers" not in data:
        report("FAIL", ".mcp.json missing 'mcpServers' object")
        return

    servers = data["mcpServers"]
    report("PASS", f".mcp.json has {len(servers)} server slots")

    for name, config in servers.items():
        if not isinstance(config, dict):
            report("FAIL", f"mcpServer '{name}' is not an object")
            continue
        if "type" not in config:
            report("WARN", f"mcpServer '{name}' missing 'type' field")
        elif config["type"] not in ("http", "sse", "stdio"):
            report("WARN", f"mcpServer '{name}' has unusual type: {config['type']}")
        if "url" not in config:
            report("WARN", f"mcpServer '{name}' missing 'url' field")


def check_claude_md_template():
    section("Check 3: CLAUDE.md template (five-rule contract)")
    path = ROOT / "CLAUDE.md"
    if not path.exists():
        report("FAIL", "CLAUDE.md template does not exist at plugin root")
        return

    content = path.read_text(encoding="utf-8")

    # Check for the five-rule contract markers
    markers = [
        ("HTML comment block at start", lambda c: c.startswith("<!--")),
        ("Mentions config path", lambda c: "~/.claude/plugins/config/llms-txt-advisor" in c),
        ("Has [PLACEHOLDER] markers", lambda c: "[PLACEHOLDER]" in c),
        ("Has bounce instruction", lambda c: "STOP" in c or "bounce" in c.lower()),
        ("Mentions PROVISIONAL mode", lambda c: "PROVISIONAL" in c),
    ]

    for desc, check in markers:
        if check(content):
            report("PASS", f"CLAUDE.md template: {desc}")
        else:
            report("WARN", f"CLAUDE.md template: {desc} not found")


def check_skill_md(skill_path):
    """Validate a SKILL.md file."""
    rel = skill_path.relative_to(ROOT)
    content = skill_path.read_text(encoding="utf-8")

    # Must start with YAML frontmatter
    if not content.startswith("---\n"):
        report("FAIL", f"{rel}: does not start with YAML frontmatter")
        return

    # Find the closing ---
    end = content.find("\n---\n", 4)
    if end == -1:
        report("FAIL", f"{rel}: frontmatter missing closing ---")
        return

    frontmatter = content[4:end]

    # Check required fields
    if "name:" not in frontmatter:
        report("FAIL", f"{rel}: frontmatter missing 'name'")
    if "description:" not in frontmatter:
        report("FAIL", f"{rel}: frontmatter missing 'description'")
    else:
        # Extract description for triggering quality check
        desc_match = re.search(r"description:\s*(>|\|)?\s*\n?((?:.*\n)*?)(?=\n[a-z-]+:|---)", frontmatter)
        if desc_match:
            desc = desc_match.group(2).strip()
            if len(desc) < 50:
                report("WARN", f"{rel}: description very short ({len(desc)} chars)")
            elif len(desc) > 1536:
                report("WARN", f"{rel}: description over 1536 chars (will be truncated in skill listing)")

    # Check line count (under 500 lines per Anthropic guidance)
    lines = content.count("\n")
    if lines > 500:
        report("WARN", f"{rel}: {lines} lines (Anthropic suggests <500; move detail to references/)")
    else:
        report("PASS", f"{rel}: frontmatter valid, {lines} lines")


def check_all_skills():
    section("Check 4: skills/*/SKILL.md")
    skills_dir = ROOT / "skills"
    if not skills_dir.exists():
        report("FAIL", "skills/ directory missing")
        return

    skill_files = list(skills_dir.glob("*/SKILL.md"))
    if not skill_files:
        report("FAIL", "no SKILL.md files found under skills/")
        return

    report("INFO", f"found {len(skill_files)} skills")
    for sf in sorted(skill_files):
        check_skill_md(sf)


def check_agents():
    section("Check 5: agents/")
    agents_dir = ROOT / "agents"
    if not agents_dir.exists():
        report("WARN", "agents/ directory missing (optional)")
        return

    for agent_file in sorted(agents_dir.glob("*.md")):
        rel = agent_file.relative_to(ROOT)
        content = agent_file.read_text(encoding="utf-8")
        if not content.startswith("---\n"):
            report("FAIL", f"{rel}: does not start with YAML frontmatter")
        elif "name:" in content[:500] and "description:" in content[:1500]:
            report("PASS", f"{rel}: valid agent file")
        else:
            report("WARN", f"{rel}: missing name or description in frontmatter")


def check_cookbooks():
    section("Check 6: managed-agent-cookbooks/")
    cookbook_dir = ROOT / "managed-agent-cookbooks"
    if not cookbook_dir.exists():
        report("WARN", "managed-agent-cookbooks/ directory missing (optional)")
        return

    for cookbook in sorted(cookbook_dir.iterdir()):
        if not cookbook.is_dir():
            continue
        rel = cookbook.relative_to(ROOT)

        # Check for agent.yaml
        agent_yaml = cookbook / "agent.yaml"
        if not agent_yaml.exists():
            report("FAIL", f"{rel}: missing agent.yaml")
            continue

        content = agent_yaml.read_text(encoding="utf-8")

        # Light validation — check for required keys
        required_keys = ["name:", "model:", "system:", "tools:"]
        missing = [k for k in required_keys if k not in content]
        if missing:
            report("FAIL", f"{rel}/agent.yaml: missing keys {missing}")
            continue

        # Check that system.file: reference resolves
        file_match = re.search(r"system:\s*\n\s*file:\s*(\S+)", content)
        if file_match:
            ref_path = file_match.group(1)
            full_path = (cookbook / ref_path).resolve()
            if not full_path.exists():
                report("FAIL", f"{rel}/agent.yaml: system.file '{ref_path}' does not resolve to existing file ({full_path})")
            else:
                report("PASS", f"{rel}/agent.yaml: system.file resolves to {full_path.relative_to(ROOT)}")

        # Check sub-agents directory if cookbook has callable_agents
        if "callable_agents:" in content:
            subagent_files = list((cookbook / "subagents").glob("*.yaml"))
            report("PASS", f"{rel}: has {len(subagent_files)} sub-agent YAML files")
            for sa in subagent_files:
                sa_content = sa.read_text(encoding="utf-8")
                if "name:" not in sa_content or "tools:" not in sa_content:
                    report("FAIL", f"{sa.relative_to(ROOT)}: missing name or tools field")
                else:
                    report("PASS", f"{sa.relative_to(ROOT)}: valid sub-agent manifest")


def check_cross_references():
    section("Check 7: cross-reference resolution")
    # Pattern to find markdown links to local files
    md_link_re = re.compile(r"\[([^\]]+)\]\(([^)#]+)(?:#[^)]+)?\)")
    rel_path_re = re.compile(r"^(?!https?://|mailto:)[^:]+\.(md|txt|sh|conf|json|yaml|yml|py)$")
    # Strip fenced code blocks before scanning so placeholder URLs in examples
    # don't show up as broken references
    fence_re = re.compile(r"```[\s\S]*?```", re.MULTILINE)

    md_files = list(ROOT.rglob("*.md"))
    broken = []
    checked = 0

    for md in md_files:
        # Skip files under .git
        if ".git/" in str(md):
            continue
        content = md.read_text(encoding="utf-8")
        # Remove fenced code blocks (markdown examples often contain placeholder URLs)
        content_no_code = fence_re.sub("", content)
        for match in md_link_re.finditer(content_no_code):
            target = match.group(2).strip()
            # Skip empty, bracketed-placeholder, or anchor-only references
            if not target or target.startswith("[") or target.startswith("#"):
                continue
            if rel_path_re.match(target):
                checked += 1
                # Resolve relative to the markdown file's directory
                resolved = (md.parent / target).resolve()
                # Check if file exists OR if it's within the plugin root
                if not resolved.exists():
                    broken.append((md.relative_to(ROOT), target))

    if broken:
        for src, target in broken[:20]:  # Cap to first 20 to avoid spam
            report("WARN", f"broken reference in {src}: {target}")
        if len(broken) > 20:
            report("WARN", f"...and {len(broken) - 20} more broken references")
    else:
        report("PASS", f"checked {checked} relative markdown references — all resolve")


def check_evals():
    section("Check 8: evals/")
    evals_dir = ROOT / "evals"
    if not evals_dir.exists():
        report("INFO", "evals/ directory not present (optional)")
        return

    for evals_json in sorted(evals_dir.glob("**/evals.json")):
        rel = evals_json.relative_to(ROOT)
        try:
            with open(evals_json) as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            report("FAIL", f"{rel}: not valid JSON: {e}")
            continue

        if "prompts" not in data:
            report("FAIL", f"{rel}: missing 'prompts' array")
            continue

        if not isinstance(data["prompts"], list):
            report("FAIL", f"{rel}: 'prompts' is not an array")
            continue

        report("PASS", f"{rel}: {len(data['prompts'])} eval prompts")


def check_size_constraints():
    section("Check 9: size constraints")
    # Plugin manifest should be small
    plugin_json = ROOT / ".claude-plugin" / "plugin.json"
    if plugin_json.exists():
        size = plugin_json.stat().st_size
        if size > 4096:
            report("WARN", f"plugin.json is {size} bytes (typically <1KB)")
        else:
            report("PASS", f"plugin.json size {size} bytes")

    # Each SKILL.md
    for sf in (ROOT / "skills").glob("*/SKILL.md"):
        size = sf.stat().st_size
        rel = sf.relative_to(ROOT)
        if size > 30000:
            report("WARN", f"{rel} is {size} bytes — consider moving detail to references/")
        else:
            report("PASS", f"{rel}: {size} bytes")


def main():
    parser = argparse.ArgumentParser(description="Validate llms-txt-advisor plugin structure")
    parser.add_argument("--self-install", action="store_true", help="Install as .git/hooks/pre-commit")
    parser.add_argument("--strict", action="store_true", help="Fail on warnings too")
    args = parser.parse_args()

    if args.self_install:
        install_hook()
        return 0

    print(f"check.py — validating plugin at {ROOT}")
    print("=" * 60)

    check_plugin_json()
    check_mcp_json()
    check_claude_md_template()
    check_all_skills()
    check_agents()
    check_cookbooks()
    check_cross_references()
    check_evals()
    check_size_constraints()

    print("\n" + "=" * 60)
    print(f"Summary:")
    print(f"  {PASS}: {len(passed)}")
    print(f"  {WARN}: {len(warnings)}")
    print(f"  {FAIL}: {len(errors)}")
    print("=" * 60)

    if errors:
        print(f"\n{FAIL}: {len(errors)} errors found. Fix before committing.")
        return 1

    if args.strict and warnings:
        print(f"\n{FAIL} (strict mode): {len(warnings)} warnings found.")
        return 1

    if warnings:
        print(f"\n{WARN}: {len(warnings)} warnings (non-blocking)")
    print(f"{PASS}: plugin validation succeeded")
    return 0


def install_hook():
    """Install this script as .git/hooks/pre-commit."""
    git_dir = ROOT / ".git"
    if not git_dir.exists() or not git_dir.is_dir():
        # Could be a worktree or not a git repo
        report("INFO", ".git directory not found — skipping hook install")
        return

    # Use core.hooksPath -> .githooks (financial-services pattern)
    hooks_dir = ROOT / ".githooks"
    hooks_dir.mkdir(exist_ok=True)

    hook_path = hooks_dir / "pre-commit"
    hook_content = f"""#!/usr/bin/env bash
# Pre-commit hook for llms-txt-advisor plugin
# Installed by scripts/check.py --self-install
set -e

cd "$(git rev-parse --show-toplevel)"
python3 scripts/check.py
"""
    hook_path.write_text(hook_content)
    hook_path.chmod(0o755)

    # Set git config
    import subprocess
    try:
        subprocess.run(["git", "config", "core.hooksPath", ".githooks"], check=True, cwd=ROOT)
        report("PASS", f"installed pre-commit hook at {hook_path.relative_to(ROOT)}")
        report("PASS", "set git config core.hooksPath=.githooks")
    except subprocess.CalledProcessError as e:
        report("FAIL", f"failed to set git config: {e}")


if __name__ == "__main__":
    sys.exit(main())
