#!/bin/sh
# KICKER — anime quote machine. Serves the lab on 127.0.0.1:8130.
# Usage: sh run.sh [port]   (default 8130)
PORT="${LAB_PORT:-8130}"
cd "$(dirname "$0")" || exit 1
exec python3 -m http.server "$PORT" --bind 127.0.0.1
