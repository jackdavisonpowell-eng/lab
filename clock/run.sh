#!/usr/bin/env bash
# clock — the time, as sound. Plays the current clock as a chord, re-synthesized
# every second (hours=bass, minutes=mid, seconds=high). Ctrl-C to stop.
#
# Headless / no speaker? Use --once to render a .wav instead:
#   ./run.sh --once --out /tmp/clock.wav
set -euo pipefail
cd "$(dirname "$0")"
exec python3 clock.py "$@"
