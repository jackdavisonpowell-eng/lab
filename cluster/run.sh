#!/usr/bin/env bash
# cluster — GR86-style digital gauge cluster, fake telemetry, demo mode.
# Serves this dir on 127.0.0.1:8124. Lab port range: 8100-8199.
cd "$(dirname "$0")"
exec python3 -m http.server ${LAB_PORT:-8124} --bind "${LAB_BIND:-127.0.0.1}"
