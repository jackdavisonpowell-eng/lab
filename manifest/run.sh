#!/usr/bin/env bash
# MANIFEST — dorm move-in cargo manifest.
# Serves the single-file app on 127.0.0.1:8139. Local-only, private.
set -euo pipefail
cd "$(dirname "$0")"
PORT="${LAB_PORT:-8139}"
echo "MANIFEST -> http://127.0.0.1:${PORT}/"
exec python3 -m http.server "${PORT}" --bind 127.0.0.1
