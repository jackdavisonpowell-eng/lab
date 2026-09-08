#!/bin/sh
# receipt — the word bureau. Serves the single-file showpiece.
# Registered port: 8102 (see /home/jack/lab/ports.json).
# NOTE: 8100 is the unregistered lab shelf server; 8101 is wall-clock.
#
# Usage: ./run.sh [port]      (default 8102)
# $LAB_PORT / $LAB_BIND also work; the positional port wins.
#
# #!/bin/sh + no `set -euo pipefail` (pipefail is bash-only; dash dies).
cd "$(dirname "$0")" || exit 1
PORT="${1:-${LAB_PORT:-8102}}"
exec python3 -m http.server "$PORT" --bind "${LAB_BIND:-127.0.0.1}"
