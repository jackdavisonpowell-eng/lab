#!/bin/sh
# WIRE — morning brief radio. Serves http://127.0.0.1:8135/
cd "$(dirname "$0")"
exec python3 server.py ${LAB_PORT:-8135}
