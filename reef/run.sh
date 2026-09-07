#!/usr/bin/env bash
# reef — the thebeast GPU tank. Run it in a real terminal.
cd "$(dirname "$0")"
exec python3 reef.py "$@"
