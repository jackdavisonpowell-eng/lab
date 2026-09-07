#!/bin/sh
# seam — jeans cutting layout machine
# local-only, port 8127 (lab range 8100-8199)
cd "$(dirname "$0")"
exec python3 -m http.server ${LAB_PORT:-8127} --bind "${LAB_BIND:-127.0.0.1}"
