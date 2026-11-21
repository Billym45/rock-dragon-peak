#!/usr/bin/env bash
set -euo pipefail

python3 - <<'PYEOF'
import sys
from pathlib import Path

sys.path.insert(0, str(Path.home()))
from ai_rock_dragon_evolution import run_with_handshake

run_with_handshake(task="start_all_boot", energy="peak", cycles=1, log_to_ledger=True)
PYEOF

if [ -x "$HOME/test_peak_handshake.sh" ]; then
  echo "=== Handshake Test Suite ==="
  bash "$HOME/test_peak_handshake.sh"
fi

for script in "$HOME/spirit_monitor.py" "$HOME/builds/constant_pulse.py" "$HOME/builds/master.py"; do
  if [ -f "$script" ]; then
    echo "=== Running $(basename "$script") ==="
    python3 "$script"
  else
    echo "[skip] $script not found"
  fi
done
