#!/usr/bin/env python3
"""lapboard — sim-racing lap timer + delta board for a second screen.

Serves index.html plus a tiny lap API:
  GET  /laps       -> {"laps":[...], "live": {...}|null}
  POST /lap/start  -> begin a live lap (server timestamps it)
  POST /lap/finish -> finish it, append to laps.json

Laps live in laps.json next to this file:
  [{"t": 162.345, "d": [0.0, 5.0, ..., 162.345]}, ...]
  t = total lap time (s), d = cumulative-time samples (s) for delta matching.

Sector boundaries live in track.json (optional):
  {"sectors": [0.333, 0.667]}   # track-position fractions (0..1)
  The client shows per-sector deltas (S1/S2/S3) and the strip marks the
  boundaries. Both files are re-read on mtime change — no restart needed.

Delta model: d[] is cumulative time at equally-spaced track positions, so
the live delta is your clock vs the best lap's clock at the SAME position
(the server advances the live lap's position at a fixed rate via POST
/live/pos, one step per client render tick).

Last lap wins on file mtime (external editors / scripts can write laps.json
directly; the server re-reads when the file changes).
"""
import json
import os
import tempfile
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

PORT = int(os.environ.get("LAPBOARD_PORT", "8125"))
BIND = os.environ.get("LAB_BIND", "127.0.0.1")
HERE = os.path.dirname(os.path.abspath(__file__))
LAPS = os.path.join(HERE, "laps.json")
TRACK = os.path.join(HERE, "track.json")
INDEX = os.path.join(HERE, "index.html")

_lock = threading.Lock()
_live = None  # {"t0": monotonic, "pos": float} while a lap is running
_track_cache = None  # (mtime, sectors)
# live lap advances ~325 position samples over a full lap (matches the d[]
# density of a real exporter); client polls /live/pos once per render tick.
LIVE_STEP = 1.0 / 325.0


def _track():
    """Sector boundaries from track.json: {"sectors": [0.33, 0.67]} (track
    position fractions 0..1, sorted). Re-read when the file's mtime changes,
    so a track editor can drop new boundaries without a restart.
    Missing/invalid file -> no sectors.
    """
    global _track_cache
    try:
        mt = os.stat(TRACK).st_mtime
    except OSError:
        return []
    if _track_cache is None or _track_cache[0] != mt:
        secs = []
        try:
            with open(TRACK) as f:
                data = json.load(f)
            raw = data.get("sectors") if isinstance(data, dict) else data
            if isinstance(raw, list):
                secs = sorted(float(s) for s in raw if s is not None)
        except (OSError, ValueError, TypeError):
            secs = []
        _track_cache = (mt, secs)
    return _track_cache[1]


def _load():
    try:
        with open(LAPS) as f:
            data = json.load(f)
        if isinstance(data, list):
            return data
    except (OSError, ValueError):
        pass
    return []


def _save(laps):
    fd, tmp = tempfile.mkstemp(dir=HERE, prefix=".laps-", suffix=".json")
    with os.fdopen(fd, "w") as f:
        json.dump(laps, f, indent=1)
    os.chmod(tmp, 0o644)
    os.replace(tmp, LAPS)


def _state_unlocked():
    laps = _load()
    live = None
    if _live is not None:
        live = {"elapsed": time.monotonic() - _live["t0"], "pos": _live["pos"]}
    return {"laps": laps, "live": live, "sectors": _track()}


def state():
    with _lock:
        return _state_unlocked()


def start_lap():
    global _live
    with _lock:
        if _live is None:
            _live = {"t0": time.monotonic(), "pos": 0.0}
        return _state_unlocked()


def advance_pos():
    """Client render tick: nudge the live lap's position forward. No-op when
    idle. Returns the live state (pos + elapsed) for the client to render."""
    global _live
    with _lock:
        if _live is not None:
            _live["pos"] = min(1.0, _live["pos"] + LIVE_STEP)
        return _state_unlocked()


def finish_lap():
    global _live
    with _lock:
        if _live is None:
            return _state_unlocked()
        t = time.monotonic() - _live["t0"]
        _live = None
        laps = _load()
        laps.append({"t": round(t, 3), "d": [0.0, round(t, 3)]})
        _save(laps)
        return _state_unlocked()


def reset_best():
    with _lock:
        laps = _load()
        if not laps:
            return _state_unlocked()
        best = min(laps, key=lambda l: l["t"])
        laps.remove(best)
        _save(laps)
        return _state_unlocked()


def reset_all():
    global _live
    with _lock:
        _live = None
        _save([])
        return _state_unlocked()


class H(BaseHTTPRequestHandler):
    def _json(self, obj, code=200):
        body = json.dumps(obj).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path in ("/", "/index.html"):
            with open(INDEX, "rb") as f:
                body = f.read()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(body)
        elif self.path == "/laps":
            self._json(state())
        else:
            self._json({"error": "not found"}, 404)

    def do_POST(self):
        if self.path == "/lap/start":
            self._json(start_lap())
        elif self.path == "/lap/finish":
            self._json(finish_lap())
        elif self.path == "/lap/reset-best":
            self._json(reset_best())
        elif self.path == "/lap/reset":
            self._json(reset_all())
        elif self.path == "/live/pos":
            self._json(advance_pos())
        else:
            self._json({"error": "not found"}, 404)

    def log_message(self, *a):
        pass


if __name__ == "__main__":
    if not os.path.exists(LAPS):
        _save([])
    srv = ThreadingHTTPServer((BIND, PORT), H)
    print(f"lapboard on http://{BIND}:{PORT}/ (laps: {LAPS})")
    srv.serve_forever()
