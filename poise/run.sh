#!/usr/bin/env bash
# POISE — balance playground. Local-only, stdlib http.server.
# Serves this directory on 127.0.0.1:8134.
set -euo pipefail
cd "$(dirname "$0")"
PORT="${LAB_PORT:-8134}"
echo "POISE → http://127.0.0.1:${PORT}/"
exec python3 -m http.server "${PORT}" --bind "${LAB_BIND:-127.0.0.1}"
