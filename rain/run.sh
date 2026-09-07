#!/bin/sh
# rain — amber matrix rain of vault note titles
cd "$(dirname "$0")"
# A clone has no real titles.json (it is Jack's vault, and gitignored).
[ -f titles.json ] || cp titles.sample.json titles.json
exec python3 -m http.server ${LAB_PORT:-8121} --bind 127.0.0.1
