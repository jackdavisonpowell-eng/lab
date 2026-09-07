#!/usr/bin/env python3
"""WIRE — the morning brief, read aloud.

Stdlib-only HTTP server. Serves:
  GET /            the radio page (index.html, same dir)
  GET /briefs      JSON list of available briefs (newest first)
  GET /brief       JSON {date, file, size, text} — latest by default,
                   ?date=YYYY-MM-DD to pick one.

Briefs live at $AUTOGOD_VAULT/Inbox/AUTOGOD brief YYYY-MM-DD.md (read-only).
"""
import os
import json
import re
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse, parse_qs

BRIEF_DIR = Path(os.environ.get("AUTOGOD_VAULT", os.path.expanduser("~/vault"))) / "Inbox"
BRIEF_RE = re.compile(r"^AUTOGOD brief (\d{4}-\d{2}-\d{2})\.md$")
HERE = Path(__file__).resolve().parent
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8135


def brief_index():
    out = []
    if BRIEF_DIR.is_dir():
        for p in BRIEF_DIR.iterdir():
            m = BRIEF_RE.match(p.name)
            if m and p.is_file():
                out.append({"date": m.group(1), "file": p.name,
                            "size": p.stat().st_size})
    out.sort(key=lambda x: x["date"], reverse=True)
    return out


def get_brief(date=None):
    idx = brief_index()
    if not idx:
        return None
    entry = idx[0]
    if date:
        entry = next((e for e in idx if e["date"] == date), None)
        if entry is None:
            return None
    text = (BRIEF_DIR / entry["file"]).read_text(encoding="utf-8")
    return {"date": entry["date"], "file": entry["file"],
            "size": entry["size"], "text": text}


class Handler(BaseHTTPRequestHandler):
    server_version = "WIRE/1.0"

    def _send(self, code, body, ctype):
        data = body.encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        u = urlparse(self.path)
        q = parse_qs(u.query)
        if u.path == "/":
            try:
                self._send(200, (HERE / "index.html").read_text("utf-8"),
                           "text/html; charset=utf-8")
            except OSError:
                self._send(500, "index.html missing", "text/plain")
        elif u.path == "/briefs":
            self._send(200, json.dumps(brief_index()), "application/json")
        elif u.path == "/brief":
            b = get_brief(q.get("date", [None])[0])
            if b is None:
                self._send(404, json.dumps({"error": "no such brief"}),
                           "application/json")
            else:
                self._send(200, json.dumps(b), "application/json")
        else:
            self._send(404, "not found", "text/plain")

    def log_message(self, fmt, *args):
        sys.stderr.write("wire: " + (fmt % args) + "\n")


def main():
    srv = ThreadingHTTPServer(("127.0.0.1", PORT), Handler)
    sys.stderr.write(f"wire: on air at http://127.0.0.1:{PORT}/ "
                     f"(briefs from {BRIEF_DIR})\n")
    srv.serve_forever()


if __name__ == "__main__":
    main()
