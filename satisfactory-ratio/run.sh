#!/usr/bin/env bash
# RATIO — Satisfactory production-ratio calculator
# Serves the single-file app on 127.0.0.1:8131 (lab port range 8100-8199).
set -euo pipefail
cd "$(dirname "$0")"
PORT=${LAB_PORT:-8131}
echo "RATIO → http://127.0.0.1:${PORT}/"
exec python3 -m http.server "${PORT}" --bind "${LAB_BIND:-127.0.0.1}"
