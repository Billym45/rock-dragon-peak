#!/usr/bin/env bash
set -euo pipefail

TASK="${1:-general_study}"
ENERGY="${2:-peak}"

log_stage() {
  printf '[%s] %-10s -> %s\n' "$(date '+%H:%M:%S')" "${1:-STAGE}" "${2:-}"
}

humor_check() {
  case "$1" in
    peak)   echo "Signal is clear. No dramatic excuses needed." ;;
    steady) echo "Cruising altitude. Keep the scope tight." ;;
    low)    echo "Battery's low—keep moves small and clean." ;;
    *)      echo "Custom state active. Staying sharp." ;;
  esac
}

select_mode() {
  case "$1" in
    peak)   echo "DEEP_BUILD" ;;
    steady) echo "STRUCTURED_ITERATION" ;;
    low)    echo "SMALL_WINS_AND_NOTES" ;;
    *)      echo "STRUCTURED_ITERATION" ;;
  esac
}

MODE="$(select_mode "$ENERGY")"
NOTE="$(humor_check "$ENERGY")"

log_stage "INIT" "task=$TASK | energy=$ENERGY | mode=$MODE"
log_stage "COURTESY" "$NOTE"
log_stage "HANDSHAKE" "ACK_ACTIVE | pid=$$ | status=READY"
log_stage "MOTION" "MOTION_ACTIVE | status=LIVE | mode=$MODE"
log_stage "EXECUTE" "1) Define target  2) Smallest check  3) Keep what works"
log_stage "PEAK_GUARD" "Trim noise early; log next step before stopping."
