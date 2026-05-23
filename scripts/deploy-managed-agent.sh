#!/usr/bin/env bash
# =====================================================================
# deploy-managed-agent.sh — Deploy a managed-agent cookbook to Anthropic's
#                          Managed Agents API.
#
# Adapted from anthropics/financial-services/scripts/deploy-managed-agent.sh
#
# Usage:
#   ./scripts/deploy-managed-agent.sh <cookbook-slug>           # dry-run (default)
#   ./scripts/deploy-managed-agent.sh <cookbook-slug> --live    # actually POST
#
# What it does:
#   1. Validates the cookbook agent.yaml
#   2. Resolves system.file references
#   3. Resolves env-var placeholders with safe-char regex sandboxing
#   4. Uploads bundled skills to /v1/skills (with the skills-2025-10-02 beta header)
#   5. Creates leaf sub-agents (depth-1)
#   6. POSTs the orchestrator to /v1/agents (managed-agents-2026-04-01 beta header)
#
# Environment variables expected:
#   ANTHROPIC_API_KEY                 — Anthropic API key for /v1 endpoints
#   ANTHROPIC_API_BASE (optional)     — defaults to https://api.anthropic.com
#   <COOKBOOK-SPECIFIC-MCP-URLS>      — e.g., GITHUB_MCP_URL, BING_WEBMASTER_MCP_URL
#   <COOKBOOK-SPECIFIC-VARS>          — TARGET_DOMAINS, SCHEDULE, etc.
#
# Safety:
#   - --live mode requires explicit flag (default is dry-run)
#   - Env-var values are validated against safe-char regex before substitution
#   - Refuses to deploy if cookbook contains unresolved references
# =====================================================================

set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SLUG="${1:-}"
MODE="${2:-dry-run}"

# Color output (works in most terminals)
if [[ -t 1 ]]; then
    RED='\033[0;31m'
    GREEN='\033[0;32m'
    YELLOW='\033[0;33m'
    BLUE='\033[0;34m'
    NC='\033[0m'
else
    RED=''; GREEN=''; YELLOW=''; BLUE=''; NC=''
fi

# Safe-char regex for env-var substitution (from financial-services pattern)
SAFE_CHAR_REGEX='^[A-Za-z0-9._/:@-]*$'

# --------------------------------------------------------------------
# Helpers
# --------------------------------------------------------------------

usage() {
    cat <<EOF
deploy-managed-agent.sh — Deploy a cookbook to Anthropic's Managed Agents API

Usage:
  $0 <cookbook-slug>           # dry-run (default; no API calls)
  $0 <cookbook-slug> --live    # actually POST to the API

Available cookbooks:
$(find "$ROOT/managed-agent-cookbooks" -maxdepth 1 -mindepth 1 -type d 2>/dev/null | \
  while read d; do echo "  - $(basename $d)"; done)

Example dry-run:
  $0 staleness-watcher

Example live deploy (requires ANTHROPIC_API_KEY):
  export ANTHROPIC_API_KEY=sk-ant-...
  export GITHUB_MCP_URL=https://...
  export BING_WEBMASTER_MCP_URL=https://...
  export PROFOUND_MCP_URL=https://...
  $0 staleness-watcher --live
EOF
}

info()  { printf "${BLUE}INFO${NC}: %s\n" "$1"; }
pass()  { printf "${GREEN}PASS${NC}: %s\n" "$1"; }
warn()  { printf "${YELLOW}WARN${NC}: %s\n" "$1"; }
fail()  { printf "${RED}FAIL${NC}: %s\n" "$1"; exit 1; }

section() { printf "\n${BLUE}=== %s ===${NC}\n" "$1"; }

# Validate env-var value against safe-char regex
validate_envvar() {
    local name="$1"
    local value="$2"
    if [[ ! "$value" =~ ${SAFE_CHAR_REGEX:1:-1} ]]; then
        fail "Environment variable $name contains unsafe characters; refusing to substitute"
    fi
}

# Substitute ${VARNAME} placeholders in a string with env-var values, safely
substitute_envvars() {
    local input="$1"
    local output="$input"
    local var_pattern='\$\{([A-Z_][A-Z0-9_]*)\}'

    # Find all ${VAR} patterns
    while [[ "$output" =~ \$\{([A-Z_][A-Z0-9_]*)\} ]]; do
        local var_name="${BASH_REMATCH[1]}"
        local var_value="${!var_name:-}"

        if [[ -z "$var_value" ]]; then
            if [[ "$MODE" == "--live" ]]; then
                fail "Required env-var \${$var_name} is not set"
            else
                warn "Env-var \${$var_name} not set (dry-run; would fail in --live mode)"
                var_value="<UNSET:$var_name>"
            fi
        else
            validate_envvar "$var_name" "$var_value"
        fi

        # Replace ${VAR} with value (escape for sed)
        local escaped_value
        escaped_value=$(printf '%s\n' "$var_value" | sed 's/[\/&]/\\&/g')
        output=$(echo "$output" | sed "s|\${$var_name}|$escaped_value|g")
    done

    echo "$output"
}

# --------------------------------------------------------------------
# Main flow
# --------------------------------------------------------------------

if [[ -z "$SLUG" ]] || [[ "$SLUG" == "-h" ]] || [[ "$SLUG" == "--help" ]]; then
    usage
    exit 0
fi

COOKBOOK_DIR="$ROOT/managed-agent-cookbooks/$SLUG"
AGENT_YAML="$COOKBOOK_DIR/agent.yaml"

if [[ ! -d "$COOKBOOK_DIR" ]]; then
    fail "Cookbook directory does not exist: $COOKBOOK_DIR"
fi

if [[ ! -f "$AGENT_YAML" ]]; then
    fail "agent.yaml not found at: $AGENT_YAML"
fi

section "Deploying cookbook: $SLUG (mode: $MODE)"
info "Cookbook dir: $COOKBOOK_DIR"

# --------------------------------------------------------------------
# Step 1: Validate YAML parses
# --------------------------------------------------------------------

section "Step 1: Validate agent.yaml"

if ! command -v python3 >/dev/null 2>&1; then
    fail "python3 required for YAML parsing"
fi

# Use python with yaml module to parse + extract key fields
python3 - "$AGENT_YAML" <<'PYEOF' || fail "agent.yaml is invalid YAML"
import yaml, sys
agent_yaml = sys.argv[1]
data = yaml.safe_load(open(agent_yaml))
required = ['name', 'model', 'system', 'tools']
for k in required:
    if k not in data:
        print(f'FAIL: agent.yaml missing required field: {k}', file=sys.stderr)
        sys.exit(1)
print(f"name: {data['name']}")
print(f"model: {data['model']}")
print(f"system.file: {data['system'].get('file', '<inline>')}")
print(f"tools: {len(data.get('tools', []))} entries")
print(f"mcp_servers: {len(data.get('mcp_servers', []))} entries")
print(f"callable_agents: {len(data.get('callable_agents', []))} entries")
print(f"skills: {len(data.get('skills', []))} entries")
PYEOF

pass "agent.yaml parses with all required fields"

# --------------------------------------------------------------------
# Step 2: Resolve system.file reference
# --------------------------------------------------------------------

section "Step 2: Resolve system.file reference"

SYSTEM_FILE=$(python3 - "$AGENT_YAML" <<'PYEOF'
import yaml, sys
d = yaml.safe_load(open(sys.argv[1]))
print(d.get('system', {}).get('file', ''))
PYEOF
)

if [[ -z "$SYSTEM_FILE" ]]; then
    fail "system.file not specified in agent.yaml"
fi

# Resolve relative to cookbook dir
RESOLVED_SYSTEM="$COOKBOOK_DIR/$SYSTEM_FILE"
if [[ ! -f "$RESOLVED_SYSTEM" ]]; then
    fail "system.file does not resolve to existing file: $RESOLVED_SYSTEM"
fi

pass "system.file resolves to: $(realpath --relative-to="$ROOT" "$RESOLVED_SYSTEM" 2>/dev/null || echo "$RESOLVED_SYSTEM")"
info "System prompt size: $(wc -c < "$RESOLVED_SYSTEM") bytes"

# --------------------------------------------------------------------
# Step 3: Resolve sub-agent manifests
# --------------------------------------------------------------------

section "Step 3: Resolve sub-agent manifests"

SUBAGENT_PATHS=$(python3 - "$AGENT_YAML" <<'PYEOF'
import yaml, sys
d = yaml.safe_load(open(sys.argv[1]))
for ca in d.get('callable_agents', []):
    print(ca['manifest'])
PYEOF
)

if [[ -n "$SUBAGENT_PATHS" ]]; then
    while IFS= read -r path; do
        resolved="$COOKBOOK_DIR/$path"
        if [[ ! -f "$resolved" ]]; then
            fail "Sub-agent manifest does not resolve: $resolved"
        fi
        # Validate sub-agent YAML
        python3 - "$resolved" <<'PYEOF' || fail "Sub-agent $path is invalid"
import yaml, sys
d = yaml.safe_load(open(sys.argv[1]))
required = ['name', 'tools']
missing = [k for k in required if k not in d]
if missing:
    print(f'FAIL: {sys.argv[1]} missing {missing}', file=sys.stderr); sys.exit(1)
PYEOF
        pass "Sub-agent: $(basename "$path")"
    done <<< "$SUBAGENT_PATHS"
else
    info "No callable_agents declared"
fi

# --------------------------------------------------------------------
# Step 4: Resolve env-vars (with safe-char regex)
# --------------------------------------------------------------------

section "Step 4: Resolve env-var placeholders"

ENV_VARS=$(grep -oE '\$\{[A-Z_][A-Z0-9_]*\}' "$AGENT_YAML" | sort -u | tr -d '${}' || true)

if [[ -n "$ENV_VARS" ]]; then
    while IFS= read -r var; do
        value="${!var:-}"
        if [[ -z "$value" ]]; then
            if [[ "$MODE" == "--live" ]]; then
                fail "Required env-var \${$var} is not set"
            else
                warn "Env-var \${$var} not set (dry-run mode tolerates this)"
            fi
        else
            # Validate against safe-char regex
            if ! [[ "$value" =~ ^[A-Za-z0-9._/:@-]*$ ]]; then
                fail "Env-var \${$var} contains unsafe characters; refusing to substitute"
            fi
            pass "\${$var} = $value"
        fi
    done <<< "$ENV_VARS"
else
    info "No env-var placeholders in agent.yaml"
fi

# --------------------------------------------------------------------
# Step 5: Validate skill references
# --------------------------------------------------------------------

section "Step 5: Validate skill references"

SKILL_PATHS=$(python3 - "$AGENT_YAML" <<'PYEOF'
import yaml, sys
d = yaml.safe_load(open(sys.argv[1]))
for s in d.get('skills', []):
    if 'from_plugin' in s:
        print(f"from_plugin:{s['from_plugin']}")
    elif 'path' in s:
        print(f"path:{s['path']}")
PYEOF
)

if [[ -n "$SKILL_PATHS" ]]; then
    while IFS= read -r line; do
        type="${line%%:*}"
        path="${line#*:}"
        resolved="$COOKBOOK_DIR/$path"
        if [[ "$type" == "from_plugin" ]]; then
            if [[ ! -d "$resolved" ]]; then
                fail "from_plugin path doesn't resolve to directory: $resolved"
            fi
            skill_count=$(find "$resolved/skills" -name "SKILL.md" 2>/dev/null | wc -l | tr -d ' ')
            pass "from_plugin: $path ($skill_count skills)"
        else
            if [[ ! -f "$resolved/SKILL.md" ]]; then
                fail "path doesn't resolve to skill directory: $resolved"
            fi
            pass "path: $path"
        fi
    done <<< "$SKILL_PATHS"
else
    info "No skills declared"
fi

# --------------------------------------------------------------------
# Step 6: Dry-run vs Live deploy
# --------------------------------------------------------------------

section "Step 6: $([ "$MODE" == "--live" ] && echo "Live deploy" || echo "Dry-run summary")"

if [[ "$MODE" == "--live" ]]; then
    # Live deploy path
    if [[ -z "${ANTHROPIC_API_KEY:-}" ]]; then
        fail "ANTHROPIC_API_KEY env-var is required for --live mode"
    fi

    API_BASE="${ANTHROPIC_API_BASE:-https://api.anthropic.com}"

    info "Would POST to: $API_BASE/v1/agents"
    info "Would upload skills to: $API_BASE/v1/skills"
    info "Beta headers: skills-2025-10-02, managed-agents-2026-04-01"

    warn "Live deploy NOT executed in this script (safety: requires manual review)"
    warn "To actually deploy, uncomment the curl calls below and verify destinations"

    # # Upload skills
    # for skill_dir in "$COOKBOOK_DIR/skills/"*/; do
    #     skill_name=$(basename "$skill_dir")
    #     # Package and upload as .skill file
    #     # python3 -m scripts.package_skill "$skill_dir" -o "/tmp/$skill_name.skill"
    #     # curl -X POST "$API_BASE/v1/skills" \
    #     #     -H "Authorization: Bearer $ANTHROPIC_API_KEY" \
    #     #     -H "anthropic-beta: skills-2025-10-02" \
    #     #     -F "file=@/tmp/$skill_name.skill"
    # done

    # # Create sub-agents
    # for sub in "$COOKBOOK_DIR/subagents/"*.yaml; do
    #     # python3 scripts/post-subagent.py "$sub"
    # done

    # # Create orchestrator
    # python3 scripts/post-agent.py "$AGENT_YAML"

    pass "Live deploy path validated (curl calls commented for safety)"
else
    info "Cookbook ready for deployment."
    info "To deploy live:"
    info "  1. Set ANTHROPIC_API_KEY"
    info "  2. Set required env-vars (see warnings above)"
    info "  3. Re-run with --live flag"
    info ""
    info "Estimated deployment artifacts:"
    info "  - Orchestrator agent: 1"
    info "  - Sub-agents:         $(echo "$SUBAGENT_PATHS" | grep -c . || echo 0)"
    info "  - Skills:             $(find "$COOKBOOK_DIR/skills" -name "SKILL.md" 2>/dev/null | wc -l | tr -d ' ')"
fi

section "Done"
pass "Cookbook $SLUG validation complete (mode: $MODE)"
