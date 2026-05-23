#!/usr/bin/env bash
# =====================================================================
# CI validation script for llms.txt
#
# Usage:
#   ./validate.sh path/to/llms.txt [optional-expected-sha256-hash]
#
# Exits 0 on success, non-zero on validation failure.
#
# Designed to run in CI/CD pipelines before deploy. Catches:
#   - Encoding errors (UTF-8 check)
#   - BOM presence (should be absent)
#   - Spec-shape violations (must have exactly 1 H1)
#   - Size budget overflow (>50 KB warn, >200 KB fail)
#   - Dead URLs (4xx/5xx)
#   - Hash mismatch against pinned source-of-truth
#
# See knowledge/06-deployment.md for full operational context.
# =====================================================================

set -euo pipefail

FILE="${1:-llms.txt}"
EXPECTED_HASH="${2:-}"

# Color output (works in most CI environments)
if [[ -t 1 ]]; then
    RED='\033[0;31m'
    GREEN='\033[0;32m'
    YELLOW='\033[0;33m'
    NC='\033[0m'
else
    RED=''; GREEN=''; YELLOW=''; NC=''
fi

pass() { printf "${GREEN}PASS${NC}: %s\n" "$1"; }
warn() { printf "${YELLOW}WARN${NC}: %s\n" "$1"; }
fail() { printf "${RED}FAIL${NC}: %s\n" "$1"; exit 1; }

echo "================================================================"
echo "Validating: $FILE"
echo "================================================================"

# ---------- 1. File exists and is readable ----------

[ -r "$FILE" ] || fail "Cannot read $FILE"
pass "File exists and is readable"

# ---------- 1b. Non-markdown format check (anti-pattern #17) ----------

# Reject RTF, HTML, PDF, DOCX-zip, etc. via magic-byte inspection.
MAGIC=$(head -c 6 "$FILE" 2>/dev/null | xxd -p | tr -d '\n')
case "$MAGIC" in
    7b5c727466*)        # {\rtf
        fail "File is RTF, not markdown. Anti-pattern #17. Source must be plain markdown — see knowledge/07-failure-modes.md" ;;
    25504446*)          # %PDF
        fail "File is PDF, not markdown. Anti-pattern #17." ;;
    3c21444f*|3c68746d*|3c48746d*) # <!DO  <htm  <Htm
        fail "File appears to be HTML, not markdown. Anti-pattern #17." ;;
    504b0304*)          # PK\x03\x04 (zip; could be DOCX/XLSX/PPTX)
        fail "File looks like a zip / Office document, not markdown. Anti-pattern #17." ;;
esac
pass "File is not RTF/HTML/PDF/DOCX (magic-byte check)"

# ---------- 1c. PII / phone-number leakage check (anti-pattern #16) ----------

# Threshold-based: small files with a handful of contact patterns are fine
# (entity facts may list 1 corp phone). Bulk enumeration of phone numbers
# next to every URL is the failure mode.
# Note: grep -c exits 1 when no matches but still prints "0"; suppress error.
PHONE_HITS=$(grep -cE '\+?[0-9]{1,3}[-. ]?\(?[0-9]{3,4}\)?[-. ]?[0-9]{3,4}[-. ]?[0-9]{3,4}' "$FILE" 2>/dev/null || true)
PHONE_HITS="${PHONE_HITS:-0}"
if [[ "$PHONE_HITS" -gt 10 ]]; then
    fail "PII leakage detected: $PHONE_HITS phone-number patterns in file (anti-pattern #16). Strip vendor contact details; route to canonical vendor pages."
elif [[ "$PHONE_HITS" -gt 0 ]]; then
    warn "Found $PHONE_HITS phone-number pattern(s). Verify these are legitimate entity facts (corp contact) and not vendor-list leakage."
else
    pass "No phone-number patterns found (anti-pattern #16 not triggered)"
fi

# ---------- 2. UTF-8 encoding check (cross-platform: macOS BSD and Linux GNU) ----------

# Strategy: try `file -bi` (GNU/Linux format), fall back to `file -b` (BSD/macOS),
# fall back to a direct UTF-8 validity check via Python or iconv.

ENC_RAW=""
if command -v file >/dev/null 2>&1; then
    ENC_RAW=$(file -bi "$FILE" 2>/dev/null | grep -oE 'charset=[a-zA-Z0-9-]+' || echo "")
    if [[ -z "$ENC_RAW" ]]; then
        # BSD file -bi returns "regular file" — use -b for human-readable encoding info
        FB_OUT=$(file -b "$FILE" 2>/dev/null || echo "")
        if echo "$FB_OUT" | grep -qiE "UTF-8|ASCII"; then
            ENC_RAW="charset=utf-8"
        fi
    fi
fi

# Final fallback: validate UTF-8 directly via Python or iconv
if [[ -z "$ENC_RAW" ]]; then
    if command -v python3 >/dev/null 2>&1; then
        if python3 -c "open('$FILE','rb').read().decode('utf-8')" 2>/dev/null; then
            ENC_RAW="charset=utf-8"
        fi
    elif command -v iconv >/dev/null 2>&1; then
        if iconv -f UTF-8 -t UTF-8 "$FILE" >/dev/null 2>&1; then
            ENC_RAW="charset=utf-8"
        fi
    fi
fi

case "$ENC_RAW" in
    charset=utf-8|charset=us-ascii)
        pass "Encoding is $ENC_RAW"
        ;;
    *)
        fail "Could not confirm UTF-8 encoding. Re-save as UTF-8 without BOM and ensure 'file', python3, or iconv is installed."
        ;;
esac

# ---------- 3. BOM check (UTF-8 BOM is 3 bytes: EF BB BF) ----------

BOM=$(head -c 3 "$FILE" | xxd -p | tr -d '\n')
if [[ "$BOM" == "efbbbf" ]]; then
    fail "BOM detected at file start. Re-save as UTF-8 WITHOUT BOM."
fi
pass "No BOM at file start"

# ---------- 4. Exactly one H1 ----------

H1_COUNT=$(grep -c "^# " "$FILE" || true)
if [[ "$H1_COUNT" != "1" ]]; then
    fail "Expected exactly 1 H1 heading (# ...), found $H1_COUNT. Spec requires a single H1 as the project name."
fi
pass "Single H1 heading present"

# ---------- 5. Size budget ----------

SIZE=$(wc -c < "$FILE" | tr -d ' ')

if [[ "$SIZE" -gt 204800 ]]; then
    fail "File size $SIZE bytes exceeds 200 KB hard limit. Apply URL-pattern technique to high-cardinality sections."
fi

if [[ "$SIZE" -gt 51200 ]]; then
    warn "File size $SIZE bytes exceeds 50 KB target. Consider tightening curation."
else
    pass "File size $SIZE bytes (within 50 KB target)"
fi

# ---------- 6. Link extraction and validation ----------

echo "Extracting URLs..."
# Exclude markdown special chars (backtick, paren, brace, bracket, quote) and whitespace
# Also strip trailing punctuation that's likely sentence-end rather than URL-end (. , ;)
URLS=$(grep -oE 'https?://[^)`'"'"'"<>{}[:space:]]+' "$FILE" \
       | sed -E 's/[.,;:]+$//' \
       | sort -u)
URL_COUNT=$(echo "$URLS" | grep -c '^http' || true)

if [[ "$URL_COUNT" -lt 1 ]]; then
    warn "No URLs found in file. Is this intentional?"
else
    pass "Found $URL_COUNT unique URLs"
fi

# ---------- 7. URL liveness check (parallel curl) ----------

if [[ "$URL_COUNT" -gt 0 ]] && [[ "${SKIP_URL_CHECK:-0}" != "1" ]]; then
    echo "Checking URL liveness (max 10s per URL, parallelism 8)..."

    BAD_URLS=""
    # shellcheck disable=SC2034
    while IFS= read -r url; do
        # Use HEAD first, fall back to GET if HEAD returns 405 (some servers reject HEAD)
        CODE=$(curl -sLI -o /dev/null -w "%{http_code}" --max-time 10 "$url" 2>/dev/null || echo "000")
        if [[ "$CODE" == "405" ]] || [[ "$CODE" == "000" ]]; then
            # Retry with GET
            CODE=$(curl -sL -o /dev/null -w "%{http_code}" --max-time 10 "$url" 2>/dev/null || echo "000")
        fi
        FIRST_CHAR="${CODE:0:1}"
        if [[ "$FIRST_CHAR" != "2" ]]; then
            BAD_URLS="${BAD_URLS}\n  $url [$CODE]"
        fi
    done < <(echo "$URLS")

    if [[ -n "$BAD_URLS" ]]; then
        printf "Bad URLs (non-2xx):${BAD_URLS}\n"
        fail "Found dead or broken URLs. Fix or remove them."
    fi
    pass "All URLs return 2xx"
else
    warn "Skipped URL liveness check (set SKIP_URL_CHECK=0 to enable)"
fi

# ---------- 8. Optional SHA-256 hash verification ----------

if [[ -n "$EXPECTED_HASH" ]]; then
    if command -v shasum >/dev/null 2>&1; then
        ACTUAL_HASH=$(shasum -a 256 "$FILE" | awk '{print $1}')
    elif command -v sha256sum >/dev/null 2>&1; then
        ACTUAL_HASH=$(sha256sum "$FILE" | awk '{print $1}')
    else
        warn "Neither shasum nor sha256sum found; skipping hash check"
        ACTUAL_HASH=""
    fi

    if [[ -n "$ACTUAL_HASH" ]]; then
        if [[ "$ACTUAL_HASH" != "$EXPECTED_HASH" ]]; then
            fail "SHA-256 mismatch:\n  Expected: $EXPECTED_HASH\n  Actual:   $ACTUAL_HASH"
        fi
        pass "SHA-256 hash matches pinned source"
    fi
fi

# ---------- 9. Spec-shape parse (optional, requires llms_txt2ctx) ----------

if command -v llms_txt2ctx >/dev/null 2>&1; then
    if llms_txt2ctx --check "$FILE" >/dev/null 2>&1; then
        pass "llms_txt2ctx parse successful"
    else
        warn "llms_txt2ctx parse failed (file may have spec quirks)"
    fi
else
    warn "llms_txt2ctx not installed; skipped spec-shape parse (pip install llms-txt)"
fi

# ---------- 10. Common anti-pattern checks ----------

# Check for marketing-speak red flags
if grep -qiE "revolutionize|cutting-edge|industry-leading|empowering|world-class|best-in-class" "$FILE"; then
    warn "Marketing-speak detected in descriptions. Replace with literal 'what's on the page' language."
fi

# Check for "robots.txt confusion" — User-agent: directives
if grep -qE "^User-agent:" "$FILE"; then
    fail "User-agent: directives detected. llms.txt is NOT robots.txt — it has no concept of user-agent rules. Move blocking rules to robots.txt."
fi

# Check for absurd description length (likely paragraphs in descriptions)
if grep -E "^- \[" "$FILE" | awk -F': ' 'length($2) > 300' | head -1 | grep -q .; then
    warn "Some descriptions exceed 300 characters. Trim to ~100-150 chars for retrieval-decision usefulness."
fi

# Check Optional section is the right name (case-sensitive per spec)
if grep -qE "^## (optional|OPTIONAL|Optional Section)" "$FILE" && ! grep -qE "^## Optional$" "$FILE"; then
    warn "Found a section that may be intended as Optional but doesn't match the spec name '## Optional' exactly. Parsers won't recognize it."
fi

# ---------- Done ----------

echo "================================================================"
printf "${GREEN}All checks passed.${NC} File size: $SIZE bytes. URLs: $URL_COUNT.\n"

# Print SHA-256 for record-keeping
if command -v shasum >/dev/null 2>&1; then
    HASH=$(shasum -a 256 "$FILE" | awk '{print $1}')
    echo "SHA-256: $HASH"
    echo "Pin this hash in your deployment ticket for post-deploy verification."
fi

echo "================================================================"
