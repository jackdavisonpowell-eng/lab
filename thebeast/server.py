#!/usr/bin/env python3
"""thebeast — a tiny read-only host dashboard server.

Serves index.html and a /stats JSON endpoint. Only reads nvidia-smi and /proc.
No deps beyond the Python 3 stdlib. Binds loopback only.
"""
import json
import os
import socket
import subprocess
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

HERE = os.path.dirname(os.path.abspath(__file__))
PORT = int(os.environ.get("THEBEAST_PORT", "8117"))
BIND = os.environ.get("LAB_BIND", "127.0.0.1")


def _read_uptime():
    try:
        with open("/proc/uptime") as f:
            return float(f.read().split()[0])
    except Exception:
        return 0.0


def _read_load():
    try:
        with open("/proc/loadavg") as f:
            parts = f.read().split()
            return [float(parts[0]), float(parts[1]), float(parts[2])]
    except Exception:
        return [0.0, 0.0, 0.0]


def _read_mem():
    out = {}
    try:
        with open("/proc/meminfo") as f:
            for line in f:
                key, _, rest = line.partition(":")
                val = rest.strip().split()
                if val and key in ("MemTotal", "MemAvailable"):
                    out[key] = int(val[0])
    except Exception:
        pass
    return out


def _cpu_usage():
    """Approximate overall CPU usage via a short /proc/stat sample."""
    def snap():
        with open("/proc/stat") as f:
            parts = f.readline().split()
        vals = list(map(int, parts[1:]))
        idle = vals[3] + vals[4]
        total = sum(vals)
        return idle, total
    try:
        i1, t1 = snap()
        time.sleep(0.15)
        i2, t2 = snap()
        dt = t2 - t1
        if dt <= 0:
            return 0.0
        return round(100.0 * (1.0 - (i2 - i1) / dt), 1)
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


def _f(x):
    try:
        return float(x)
    except Exception:
        return 0.0


def _procs():
    procs = []
    try:
        out = subprocess.run(
            ["ps", "-eo", "pid,pcpu,pmem,comm", "--sort=-pcpu"],
            capture_output=True, text=True, timeout=5)
        lines = out.stdout.strip().splitlines()
        for line in lines[1:6]:
            p = line.split(None, 3)
            if len(p) < 4:
                continue
            procs.append({"pid": int(p[0]), "cpu": _f(p[1]),
                          "mem": _f(p[2]), "cmd": p[3]})
    except Exception:
        pass
    return procs


def stats():
    mem = _read_mem()
    total = mem.get("MemTotal", 0)
    avail = mem.get("MemAvailable", 0)
    return {
        "ts": time.time(),
        "host": socket.gethostname(),
        "uptime_s": _read_uptime(),
        "load": _read_load(),
        "cpu": {"cores": os.cpu_count() or 0, "usage_pct": _cpu_usage()},
        "mem": {"total_kb": total, "available_kb": avail,
                "used_pct": round(100.0 * (1 - avail / total), 1) if total else 0.0},
        "gpus": _gpus(),
        "procs": _procs(),
    }


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
    srv = ThreadingHTTPServer((BIND, PORT), Handler)
    print(f"thebeast listening on http://{BIND}:{PORT}/", flush=True)
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
