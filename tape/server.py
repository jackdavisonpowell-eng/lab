#!/usr/bin/env python3
"""TAPE — the AUTOGOD exchange.

A fake stock market for Jack's machines and projects. Prices are a
deterministic random walk seeded by REAL journal activity: every job
line in $AUTOGOD_VAULT/AUTOGOD/journal/<date>.md nudges the tickers it
touches. Same journal, same prices — no state, no writes, read-only.

Stdlib only. Serves index.html + /api/quotes on 127.0.0.1:8136.
"""
import hashlib
import json
import math
import os
import random
import re
import subprocess
import sys
import threading
import time
from datetime import datetime, timedelta
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

VAULT = os.environ.get("AUTOGOD_VAULT", os.path.expanduser("~/vault"))
JOURNAL_DIR = os.path.join(VAULT, "AUTOGOD", "journal")
PORT = 8136
TICK_MIN = 15
HORIZON_H = 24

# symbol -> (display name, status)
TICKERS = [
    ("FRD", "FRIDAY", "OPEN"),
    ("TBEAST", "THE BEAST", "OPEN"),
    ("ODYS", "ODYSSEUS", "DELISTED"),
    ("PANTH", "PANTHEON", "SUSPENDED"),
    ("NITRO", "NITRO", "SUSPENDED"),
    ("MAXI", "MAXIMUS", "SUSPENDED"),
    ("WIRE", "MORNING WIRE", "OPEN"),
    ("QUEUE", "THE QUEUE", "OPEN"),
    ("GUIDE", "STUDY GUIDES", "OPEN"),
    ("LAB", "THE LAB", "OPEN"),
    ("CURATE", "CURATE", "OPEN"),
    ("MEAS", "MEASURE", "OPEN"),
]
SUSPENDED = {s for s, _, st in TICKERS if st != "OPEN"}
SUSPENDED_PRICE = {
    "ODYS": 13.37,
    "PANTH": 42.00,
    "NITRO": 69.00,
    "MAXI": 31.41,
}

# shares outstanding per ticker. THE BEAST is the odd one: its share
# count is NOT fixed — it is the live GPU power draw (watts) from
# nvidia-smi, so its market cap is literally "price x how hard the GPUs
# are working right now." The rest are arbitrary fun numbers.
SHARES = {
    "FRD": 1_200_000,
    "TBEAST": None,  # = live watts, filled in at quote time
    "ODYS": 133_700,
    "PANTH": 4_200_000,
    "NITRO": 6_900,
    "MAXI": 3_141_500,
    "WIRE": 8_136,
    "QUEUE": 9_999,
    "GUIDE": 3_140,
    "LAB": 4_096,
    "CURATE": 4_500,
    "MEAS": 2_718,
}
# ticker -> which machine's GPUs it draws power from (for the cap source)
POWER_SOURCE = {"TBEAST": "THE BEAST"}

# --- live GPU power draw (read-only, THE BEAST's market cap is this) ---
_power_cache = {"t": 0.0, "total": 0.0, "gpus": []}
_power_lock = threading.Lock()


def gpu_power():
    """Total live GPU power draw (watts) from nvidia-smi, read-only.

    Fast (~30ms), cached for 15s so the page refresh doesn't re-shell.
    Tolerant: no nvidia-smi, no GPUs, or a wedged driver returns 0.0 and
    an empty list — the server never crashes on the meter.
    """
    now = time.time()
    with _power_lock:
        if now - _power_cache["t"] < 15 and _power_cache["total"] is not None:
            return _power_cache["total"], _power_cache["gpus"]
    gpus = []
    total = 0.0
    try:
        out = subprocess.run(
            ["nvidia-smi", "--query-gpu=name,power.draw",
             "--format=csv,noheader,nounits"],
            capture_output=True, text=True, timeout=5,
        )
        for line in out.stdout.splitlines():
            parts = [p.strip() for p in line.split(",")]
            if len(parts) < 2:
                continue
            name = parts[0]
            m = re.search(r"[\d.]+", parts[1])
            watts = float(m.group(0)) if m else 0.0
            gpus.append({"name": name, "watts": round(watts, 1)})
            total += watts
    except (OSError, subprocess.SubprocessError, ValueError):
        gpus, total = [], 0.0
    with _power_lock:
        _power_cache["t"] = now
        _power_cache["total"] = round(total, 1)
        _power_cache["gpus"] = gpus
    return round(total, 1), gpus

# job type -> tickers it moves
TYPE_TOUCHES = {
    "lab": ["LAB", "WIRE"],
    "prospect": ["QUEUE"],
    "measure": ["MEAS"],
    "curate": ["CURATE"],
    "task": ["TBEAST"],
    "study_guide": ["GUIDE"],
    "build": ["TBEAST"],
    "verify": ["TBEAST"],
    "brief": ["WIRE"],
}

# machine mentions in the job text -> ticker
MENTIONS = [
    (re.compile(r"\bfriday\b", re.I), "FRD"),
    (re.compile(r"\bthebeast\b|\bthe beast\b", re.I), "TBEAST"),
    (re.compile(r"\bpantheon\b", re.I), "PANTH"),
    (re.compile(r"\bnitro\b", re.I), "NITRO"),
    (re.compile(r"\bmaximus\b", re.I), "MAXI"),
    (re.compile(r"\bct106\b|\bct 106\b|\bjellyfin\b|\bradarr\b|\bsonarr\b", re.I), "PANTH"),
    (re.compile(r"\bodysseus\b", re.I), "ODYS"),
    (re.compile(r"\bwire\b", re.I), "WIRE"),
    (re.compile(r"\blab\b", re.I), "LAB"),
    (re.compile(r"\bqueue\b", re.I), "QUEUE"),
    (re.compile(r"\bmeasure\b", re.I), "MEAS"),
    (re.compile(r"\bcurate\b|\bmedia-picks\b", re.I), "CURATE"),
    (re.compile(r"\bstudy guide\b|\bstudy_guide\b", re.I), "GUIDE"),
]

LINE_RE = re.compile(
    r"^(\d{2}:\d{2})\s+\[(\w+)\]\s+(done|FAILED|interrupted)"
    r"(?:\s+(?:rc=(\d+)\s+)?(?:in|after)\s+(\d+)s)?\s+—\s+(.*)$"
)


def parse_journal():
    """All journal lines -> event dicts, oldest first."""
    events = []
    if not os.path.isdir(JOURNAL_DIR):
        return events
    for fname in sorted(os.listdir(JOURNAL_DIR)):
        m = re.match(r"^(\d{4}-\d{2}-\d{2})\.md$", fname)
        if not m:
            continue
        date = m.group(1)
        path = os.path.join(JOURNAL_DIR, fname)
        try:
            with open(path, "r", encoding="utf-8", errors="replace") as f:
                lines = f.read().splitlines()
        except OSError:
            continue
        for line in lines:
            lm = LINE_RE.match(line.strip())
            if not lm:
                continue
            hhmm, jtype, status, rc, secs, text = lm.groups()
            hh, mm = hhmm.split(":")
            secs = int(secs) if secs else None
            ts = datetime.strptime(f"{date} {hh}:{mm}", "%Y-%m-%d %H:%M")
            touches = set(TYPE_TOUCHES.get(jtype, []))
            for rx, sym in MENTIONS:
                if rx.search(text):
                    touches.add(sym)
            events.append({
                "ts": ts,
                "type": jtype,
                "status": status,
                "rc": rc,
                "secs": int(secs) if secs else None,
                "text": text.strip()[:220],
                "touches": sorted(touches),
            })
    events.sort(key=lambda e: e["ts"])
    return events


def _seeded(sym, ts):
    h = int(hashlib.md5(f"{sym}|{ts.isoformat()}".encode()).hexdigest()[:8], 16)
    return random.Random(h)


def price_series(events, sym, now):
    """Price per TICK_MIN from first event to now.

    Every journal event that touches sym contributes a move:
    done -> up, FAILED/interrupted -> down, sized by a seeded RNG
    (stable across reloads) and the job's runtime. Ticks between
    events get a tiny seeded drift so the line is alive, not stepped.
    """
    if not events:
        return [], []
    t0 = events[0]["ts"].replace(second=0, microsecond=0)
    if t0 > now:
        t0 = now.replace(second=0, microsecond=0)
    n = int((now - t0).total_seconds() // (TICK_MIN * 60)) + 1
    stamps = [t0 + timedelta(minutes=TICK_MIN * i) for i in range(n)]
    if stamps[-1] < now:
        stamps.append(now)

    if sym in SUSPENDED:
        base = SUSPENDED_PRICE[sym]
        pts = []
        for st in stamps:
            r = _seeded(sym, st)
            pts.append(round(base + (r.random() - 0.5) * 0.06, 2))
        return stamps, pts

    # bucket moves per tick index
    moves = {}
    for ev in events:
        if sym not in ev["touches"]:
            continue
        idx = int((ev["ts"] - t0).total_seconds() // (TICK_MIN * 60))
        r = _seeded(sym, ev["ts"])
        if ev["status"] == "done":
            sign = 1.0
        else:
            sign = -1.0
        mag = 0.4 + r.random() * 1.6
        if ev["secs"]:
            mag *= 1.0 + min(ev["secs"] / 3600.0, 2.0) * 0.25
        if ev["status"] == "FAILED" and ev["rc"] == "124":
            mag *= 0.6  # a timeout is a shrug, not a crash
        moves[idx] = moves.get(idx, 0.0) + sign * mag

    pts = []
    price = 100.0
    for i, st in enumerate(stamps):
        price += moves.get(i, 0.0)
        r = _seeded(sym, st)
        price += (r.random() - 0.5) * 0.05  # idle drift
        price = max(price, 1.0)
        pts.append(round(price, 2))
    return stamps, pts


def _idx_at(stamps, dt):
    if dt <= stamps[0]:
        return 0
    if dt >= stamps[-1]:
        return len(stamps) - 1
    # binary search
    lo, hi = 0, len(stamps) - 1
    while lo < hi:
        mid = (lo + hi) // 2
        if stamps[mid] < dt:
            lo = mid + 1
        else:
            hi = mid
    return lo


def build_quotes(events, now):
    total_watts, gpus = gpu_power()
    quotes = []
    for sym, name, status in TICKERS:
        stamps, pts = price_series(events, sym, now)
        if not pts:
            continue
        last = pts[-1]
        # shares: THE BEAST's are live GPU watts, everything else is fixed
        shares = SHARES.get(sym)
        if shares is None:
            shares = int(round(total_watts)) or 1
        mkt_cap = last * shares
        day_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        if day_start >= stamps[0]:
            prev = pts[_idx_at(stamps, day_start)]
        else:
            prev = pts[0]
        chg = last - prev
        pct = (chg / prev * 100.0) if prev else 0.0
        # sparkline: last 24h, downsampled to ~96 points
        cut = now - timedelta(hours=HORIZON_H)
        s0 = _idx_at(stamps, cut)
        sp_stamps, sp_pts = stamps[s0:], pts[s0:]
        step = max(1, len(sp_pts) // 96)
        spark = [sp_pts[i] for i in range(0, len(sp_pts), step)]
        quotes.append({
            "sym": sym,
            "name": name,
            "status": status,
            "last": last,
            "chg": round(chg, 2),
            "pct": round(pct, 2),
            "shares": shares,
            "mkt_cap": mkt_cap,
            "cap_live": sym in POWER_SOURCE,
            "spark": spark,
            "stamps": [s.isoformat() for s in sp_stamps],
            "pts": sp_pts,
        })
    news = [
        {
            "t": e["ts"].strftime("%m-%d %H:%M"),
            "type": e["type"],
            "status": e["status"],
            "rc": e["rc"],
            "secs": e["secs"],
            "text": e["text"],
            "touches": e["touches"],
        }
        for e in events[-120:]
    ][::-1]
    return {
        "now": now.isoformat(),
        "quotes": quotes,
        "news": news,
        "grid_load": {"watts": total_watts, "gpus": gpus},
    }


_cache = {"key": None, "data": None}
_lock = threading.Lock()


def get_quotes():
    with _lock:
        now = datetime.now()
        key = (now.strftime("%Y-%m-%d %H:%M"),)
        if _cache["key"] == key and _cache["data"]:
            return _cache["data"]
        events = parse_journal()
        data = build_quotes(events, now)
        _cache["key"] = key
        _cache["data"] = data
        return data


class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        pass

    def _send(self, code, body, ctype):
        if isinstance(body, str):
            body = body.encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        path = self.path.split("?", 1)[0]
        if path == "/":
            with open(os.path.join(os.path.dirname(__file__), "index.html"),
                      "rb") as f:
                self._send(200, f.read(), "text/html; charset=utf-8")
        elif path == "/api/quotes":
            data = get_quotes()
            self._send(200, json.dumps(data), "application/json")
        elif path == "/health":
            self._send(200, "ok", "text/plain")
        else:
            self._send(404, "not on the tape", "text/plain")


def main():
    srv = ThreadingHTTPServer(("127.0.0.1", PORT), Handler)
    print(f"TAPE exchange open on http://127.0.0.1:{PORT}", flush=True)
    srv.serve_forever()


if __name__ == "__main__":
    sys.exit(main())
