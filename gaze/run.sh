#!/bin/sh
# gaze — FRIDAY pixel face. Serves the page on 127.0.0.1:8122.
#
#   sh run.sh                    # serve, auto mood drift (default)
#   GAZE_PORT=8122 sh run.sh     # different port
#
# Mood is set via URL query params (the page, not the server):
#   http://127.0.0.1:8122/?mood=happy     pin a mood
#   http://127.0.0.1:8122/?poll=URL       live mood from a URL (text or {"mood":"x"})
#
# Moods: idle listening thinking speaking happy sad alert surprised sleepy focus error off
cd "$(dirname "$0")" || exit 1
PORT="${LAB_PORT:-8122}"
exec python3 -m http.server "$PORT" --bind 127.0.0.1
