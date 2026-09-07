#!/usr/bin/env bash
# DANGLING — a text adventure inside thebeast.
# Single-file Python stdlib game. No installs, no network, no port.
cd "$(dirname "$0")"
exec python3 game.py
