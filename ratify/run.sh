#!/bin/sh
# RATIFY — POLS 1101 Ch 1-3 ratification quiz. Serves on 127.0.0.1:8133.
cd "$(dirname "$0")"
exec python3 -m http.server ${LAB_PORT:-8133} --bind "${LAB_BIND:-127.0.0.1}"
