#!/bin/sh
# motel — serves the single-file neon sign on an assigned port.
cd "$(dirname "$0")"
exec python3 -m http.server "${LAB_PORT:-8142}" --bind 127.0.0.1
