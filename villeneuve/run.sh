#!/bin/sh
# Villeneuve — shot generator. Serves index.html on 127.0.0.1:8132.
cd "$(dirname "$0")"
exec python3 -m http.server ${LAB_PORT:-8132} --bind 127.0.0.1
