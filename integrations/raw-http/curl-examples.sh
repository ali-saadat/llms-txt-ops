#!/usr/bin/env bash
# Raw curl examples for the A2A v1.0 server.
# Works from any tool / language that can speak HTTP — bash, JS fetch, Postman, etc.
#
# Override the endpoint via env-var:
#   A2A_URL=https://a2a.example.com bash curl-examples.sh
#
# For an authenticated server, also set:
#   A2A_BEARER=your-token bash curl-examples.sh

A2A_URL="${A2A_URL:-http://localhost:8000}"
A2A_BEARER="${A2A_BEARER:-}"

AUTH_HEADER=()
if [ -n "$A2A_BEARER" ]; then
    AUTH_HEADER=(-H "Authorization: Bearer $A2A_BEARER")
fi

echo "Using endpoint: $A2A_URL"
echo

# ----------------------------------------------------------------
# 1. Discover — fetch the Agent Card (no auth required for discovery)
# ----------------------------------------------------------------
echo "=== 1. Agent Card ==="
curl -s "$A2A_URL/.well-known/agent-card.json" | python3 -m json.tool | head -20
echo

# ----------------------------------------------------------------
# 2. Health check
# ----------------------------------------------------------------
echo "=== 2. Health ==="
curl -s "$A2A_URL/health"
echo
echo

# ----------------------------------------------------------------
# 3. message/send — synchronous request
# ----------------------------------------------------------------
echo "=== 3. message/send (advise skill) ==="
curl -s -X POST "$A2A_URL/a2a" \
    -H "Content-Type: application/json" \
    "${AUTH_HEADER[@]}" \
    -d '{
        "jsonrpc": "2.0",
        "id": "req-1",
        "method": "message/send",
        "params": {
            "message": {
                "role": "user",
                "parts": [{"kind": "text", "text": "Should I ship llms.txt for a marketing site?"}]
            },
            "metadata": {"skill": "advise"}
        }
    }' | python3 -m json.tool
echo

# ----------------------------------------------------------------
# 4. message/stream — SSE
# ----------------------------------------------------------------
echo "=== 4. message/stream (audit skill) — streamed output ==="
curl -s -N -X POST "$A2A_URL/a2a" \
    -H "Content-Type: application/json" \
    -H "Accept: text/event-stream" \
    "${AUTH_HEADER[@]}" \
    -d '{
        "jsonrpc": "2.0",
        "id": "req-2",
        "method": "message/stream",
        "params": {
            "message": {
                "role": "user",
                "parts": [{"kind": "text", "text": "Review my llms.txt"}]
            },
            "metadata": {"skill": "audit"}
        }
    }' | head -10
echo

# ----------------------------------------------------------------
# 5. tasks/list
# ----------------------------------------------------------------
echo "=== 5. tasks/list ==="
curl -s -X POST "$A2A_URL/a2a" \
    -H "Content-Type: application/json" \
    "${AUTH_HEADER[@]}" \
    -d '{
        "jsonrpc": "2.0",
        "id": "req-3",
        "method": "tasks/list",
        "params": {"limit": 5}
    }' | python3 -m json.tool | head -30
