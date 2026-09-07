#!/usr/bin/env bash
# ABYSS — Subnautica progress tracker. Serves this directory on 127.0.0.1:8128.
set -euo pipefail
cd "$(dirname "$0")"
PORT="${LAB_PORT:-8128}"
echo "ABYSS → http://127.0.0.1:${PORT}/"
exec python3 -m http.server "${PORT}" --bind "${LAB_BIND:-127.0.0.1}"
