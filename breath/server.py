#!/usr/bin/env python3
"""breath — thebeast breathes. A tiny read-only server.

Serves index.html (a full-screen breathing amber visual) and a /stats JSON
endpoint. Only reads nvidia-smi. No deps beyond the Python 3 stdlib.
Binds loopback only.
"""
import json
import os
import socket
import subprocess
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

HERE = os.path.dirname(os.path.abspath(__file__))
PORT = int(os.environ.get("BREATH_PORT", "8120"))


def _f(x):
    try:
        return float(x)
    except Exception:
        return 0.0


def _gpus():
    gpus = []
    try:
        out = subprocess.run(
            ["nvidia-smi",
             "--query-gpu=name,temperature.gpu,memory.used,memory.total,utilization.gpu,power.draw",
             "--format=csv,noheader,nounits"],
            capture_output=True, text=True, timeout=5)
        for line in out.stdout.strip().splitlines():
            p = [x.strip() for x in line.split(",")]
            if len(p) < 6:
                continue
            gpus.append({
                "name": p[0],
                "temp_c": _f(p[1]),
                "mem_used_mb": _f(p[2]),
                "mem_total_mb": _f(p[3]),
                "util_pct": _f(p[4]),
                "power_w": _f(p[5]),
            })
    except Exception:
        pass
    return gpus


def stats():
    return {"host": socket.gethostname(), "gpus": _gpus()}


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def _send(self, code, body, ctype):
        data = body.encode() if isinstance(body, str) else body
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        path = self.path.split("?", 1)[0]
        if path in ("/", "/index.html"):
            try:
                with open(os.path.join(HERE, "index.html"), "rb") as f:
                    self._send(200, f.read(), "text/html; charset=utf-8")
            except Exception:
                self._send(500, "index.html missing", "text/plain")
        elif path == "/stats":
            self._send(200, json.dumps(stats()), "application/json")
        else:
            self._send(404, "not found", "text/plain")


def main():
    srv = ThreadingHTTPServer(("127.0.0.1", PORT), Handler)
    print(f"breath listening on http://127.0.0.1:{PORT}/", flush=True)
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
