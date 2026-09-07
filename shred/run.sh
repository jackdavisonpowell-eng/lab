#!/bin/sh
# shred — trick roulette. Serves the single HTML file on 127.0.0.1.
PORT="${LAB_PORT:-8137}"
cd "$(dirname "$0")"
exec python3 -m http.server "$PORT" --bind 127.0.0.1
