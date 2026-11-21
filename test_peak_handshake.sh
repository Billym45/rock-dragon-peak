#!/usr/bin/env bash
set -euo pipefail

BASH_SCRIPT="${1:-$HOME/gemini_peak_alg.sh}"
PY_SCRIPT="${2:-$HOME/ai_rock_dragon_evolution.py}"

echo "=== [1/3] Checking files ==="
test -x "$BASH_SCRIPT" && echo "OK: executable $BASH_SCRIPT" || { echo "FAIL: $BASH_SCRIPT missing or not executable"; exit 1; }
test -f "$PY_SCRIPT" && echo "OK: found $PY_SCRIPT" || { echo "FAIL: $PY_SCRIPT missing"; exit 1; }

echo "=== [2/3] Testing Bash handshake output ==="
BASH_OUT="$("$BASH_SCRIPT" "handshake_test" "peak")"
echo "$BASH_OUT"
echo "$BASH_OUT" | grep -q "HANDSHAKE.*ACK_ACTIVE" && echo "OK: Bash emitted ACK_ACTIVE" || { echo "FAIL: missing ACK_ACTIVE"; exit 1; }

echo "=== [3/3] Running ai_rock_dragon_evolution.py ==="
python3 "$PY_SCRIPT"
echo "PASS: Test completed cleanly."
