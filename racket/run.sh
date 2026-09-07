#!/bin/sh
# LADDER — tennis ladder for the court crew.
# Serves on 127.0.0.1:8126. Stdlib only, state in state.json next to this file.
cd "$(dirname "$0")" || exit 1
exec python3 server.py
