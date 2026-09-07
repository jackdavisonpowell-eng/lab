#!/bin/sh
# TAPE — the AUTOGOD exchange.
# Read-only on $AUTOGOD_VAULT/AUTOGOD/journal; serves 127.0.0.1:8136.
cd "$(dirname "$0")"
exec python3 server.py
