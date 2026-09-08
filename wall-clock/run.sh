#!/bin/sh
# wall-clock — a monotone clock in the side-wall's skin. Registered port: 8101.
#
# Usage: ./run.sh [port]      (default 8101)
# $LAB_PORT / $LAB_BIND also work; the positional port wins.
cd "$(dirname "$0")" || exit 1
PORT="${1:-${LAB_PORT:-8101}}"
exec python3 -m http.server "$PORT" --bind "${LAB_BIND:-127.0.0.1}"
