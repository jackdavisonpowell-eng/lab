#!/bin/sh
# SUPERNOVA — 22-minute Outer Wilds loop timer.
# Serves the page on 127.0.0.1:8138 (lab port range 8100-8199).
cd "$(dirname "$0")" || exit 1
exec python3 -m http.server ${LAB_PORT:-8138} --bind "${LAB_BIND:-127.0.0.1}"
