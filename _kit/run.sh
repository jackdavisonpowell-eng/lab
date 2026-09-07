#!/bin/sh
# _kit — the shared skin. This run.sh serves the kit's own demo (index.html)
# so you can see every base.css class live. Registered port: 8110.
#
# Usage: ./run.sh [port]      (default 8110)
# $LAB_PORT / $LAB_BIND also work; the positional port wins.
#
# When you START A NEW PROJECT, copy this file and change the default port
# to the one you took from /home/jack/lab/ports.json (lowest free in 8100-8199).
# Keep the #!/bin/sh + no-`set -euo pipefail` shape (pipefail is bash-only; dash dies).
cd "$(dirname "$0")" || exit 1
PORT="${1:-${LAB_PORT:-8110}}"
exec python3 -m http.server "$PORT" --bind "${LAB_BIND:-127.0.0.1}"
