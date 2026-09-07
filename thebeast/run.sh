#!/usr/bin/env bash
# thebeast — start the live host dashboard on loopback.
set -euo pipefail
cd "$(dirname "$0")"
exec python3 server.py
