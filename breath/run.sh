#!/usr/bin/env bash
# breath — thebeast breathes. Read-only: only reads nvidia-smi.
cd "$(dirname "$0")"
exec python3 server.py
