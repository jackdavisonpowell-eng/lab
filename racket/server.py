#!/usr/bin/env python3
"""LADDER — a tennis ladder for the court crew.

Stdlib only. Serves index.html on 127.0.0.1:8126 plus a tiny JSON API:
  GET  /api/state          -> {players, matches}
  POST /api/player         {name}              -> add player
  POST /api/match          {winner, loser}     -> record match, update ELO
  DELETE /api/player?id=N  -> remove player (and their matches)
State lives in state.json next to this file. ELO: K=32, start 1000.
"""
import json
import os
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs

HERE = os.path.dirname(os.path.abspath(__file__))
STATE_PATH = os.path.join(HERE, "state.json")
INDEX_PATH = os.path.join(HERE, "index.html")
PORT = 8126
BIND = os.environ.get("LAB_BIND", "127.0.0.1")
START_RATING = 1000
K = 32

_lock = threading.Lock()
_next_id = [1]


def _load():
    if os.path.exists(STATE_PATH):
        with open(STATE_PATH) as f:
            data = json.load(f)
        data.setdefault("players", [])
        data.setdefault("matches", [])
        data.setdefault("next_id", 1)
        return data
    return {"players": [], "matches": [], "next_id": 1}


def _save(state):
    tmp = STATE_PATH + ".tmp"
    with open(tmp, "w") as f:
        json.dump(state, f, indent=1)
    os.replace(tmp, STATE_PATH)


def _state_unlocked():
    """Snapshot WITHOUT taking the lock. Callers must hold it."""
    s = _load()
    players = sorted(s["players"], key=lambda p: -p["rating"])
    return {
        "players": players,
        "matches": list(reversed(s["matches"][-100:])),
        "next_id": s["next_id"],
    }


def elo_update(rw, rl):
    ew = 1.0 / (1.0 + 10 ** ((rl - rw) / 400.0))
    ew_new = rw + K * (1.0 - ew)
    el_new = rl + K * (0.0 - ew)
    return round(ew_new), round(el_new)


def api_add_player(name):
    with _lock:
        s = _load()
        name = (name or "").strip()
        if not name:
            return 400, {"error": "name required"}
        if any(p["name"].lower() == name.lower() for p in s["players"]):
            return 409, {"error": "player already exists"}
        p = {
            "id": s["next_id"],
            "name": name,
            "rating": START_RATING,
            "wins": 0,
            "losses": 0,
            "streak": 0,
        }
        s["next_id"] += 1
        s["players"].append(p)
        _save(s)
        return 200, {"player": p}


def api_record_match(winner_id, loser_id):
    with _lock:
        s = _load()
        by_id = {p["id"]: p for p in s["players"]}
        w = by_id.get(winner_id)
        l = by_id.get(loser_id)
        if w is None or l is None:
            return 404, {"error": "unknown player"}
        if w["id"] == l["id"]:
            return 400, {"error": "winner and loser must differ"}
        old_wr, old_lr = w["rating"], l["rating"]
        wr, lr = elo_update(old_wr, old_lr)
        w["rating"], w["wins"] = wr, w["wins"] + 1
        w["streak"] = abs(w["streak"]) + 1
        l["rating"], l["losses"] = lr, l["losses"] + 1
        l["streak"] = -(abs(l["streak"]) + 1)
        m = {
            "winner": w["id"],
            "loser": l["id"],
            "winner_name": w["name"],
            "loser_name": l["name"],
            "ts": int(time.time()),
            "delta": wr - old_wr,  # winner's rating swing
        }
        s["matches"].append(m)
        _save(s)
        return 200, {"match": m, "players": _state_unlocked()["players"]}


def api_delete_player(pid):
    with _lock:
        s = _load()
        before = len(s["players"])
        s["players"] = [p for p in s["players"] if p["id"] != pid]
        if len(s["players"]) == before:
            return 404, {"error": "unknown player"}
        s["matches"] = [
            m for m in s["matches"] if m["winner"] != pid and m["loser"] != pid
        ]
        _save(s)
        return 200, {"players": _state_unlocked()["players"]}


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def _json(self, code, obj):
        body = json.dumps(obj).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        u = urlparse(self.path)
        if u.path == "/api/state":
            with _lock:
                self._json(200, _state_unlocked())
        elif u.path in ("/", "/print"):
            with open(INDEX_PATH, "rb") as f:
                body = f.read()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        else:
            self._json(404, {"error": "not found"})

    def do_POST(self):
        u = urlparse(self.path)
        try:
            n = int(self.headers.get("Content-Length", 0))
            data = json.loads(self.rfile.read(n) or b"{}")
        except Exception:
            self._json(400, {"error": "bad json"})
            return
        if u.path == "/api/player":
            code, obj = api_add_player(data.get("name", ""))
            self._json(code, obj)
        elif u.path == "/api/match":
            try:
                code, obj = api_record_match(
                    int(data.get("winner")), int(data.get("loser"))
                )
            except (TypeError, ValueError):
                code, obj = 400, {"error": "winner/loser must be player ids"}
            self._json(code, obj)
        else:
            self._json(404, {"error": "not found"})

    def do_DELETE(self):
        u = urlparse(self.path)
        if u.path == "/api/player":
            q = parse_qs(u.query)
            try:
                code, obj = api_delete_player(int(q.get("id", ["0"])[0]))
            except ValueError:
                code, obj = 400, {"error": "bad id"}
            self._json(code, obj)
        else:
            self._json(404, {"error": "not found"})


if __name__ == "__main__":
    srv = ThreadingHTTPServer((BIND, PORT), Handler)
    print(f"ladder on http://{BIND}:{PORT}/")
    srv.serve_forever()
