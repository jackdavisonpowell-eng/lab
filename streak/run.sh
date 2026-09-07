#!/bin/sh
# STREAK — pre-calculus drill trainer. Serves the single-file app on 127.0.0.1:8129.
cd "$(dirname "$0")"
exec python3 -m http.server ${LAB_PORT:-8129} --bind 127.0.0.1
