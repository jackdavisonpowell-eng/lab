#!/usr/bin/env bash
# Horse Tinder — local-only. Binds 127.0.0.1:8123.
set -euo pipefail
cd "$(dirname "$0")"
PORT=${LAB_PORT:-8123}
echo "HORSE TINDER  ->  http://127.0.0.1:${PORT}/"
exec python3 -m http.server "$PORT" --bind "${LAB_BIND:-127.0.0.1}"
