#!/usr/bin/env bash
# lapboard — sim-racing lap timer + delta board (second screen)
# Usage: ./run.sh [port]   (default 8125)
set -euo pipefail
cd "$(dirname "$0")"
export LAPBOARD_PORT="${1:-${LAB_PORT:-8125}}"
exec python3 server.py
