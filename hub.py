#!/usr/bin/env python3
"""LAB HUB — starts every web project in the lab and puts one index in front of them.

The projects each serve themselves on their own port from ports.json, but they
default to 127.0.0.1 and nothing ever started them, so on a headless box they
were unreachable by anyone including Jack. The hub supervises them with
LAB_BIND=0.0.0.0 and serves an index at :8100.

Stdlib only, single file, no build step — same rules the projects work under.
"""
import html
import json
import os
import re
import signal
import subprocess
import sys
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

HERE = os.path.dirname(os.path.abspath(__file__))
PORT = int(os.environ.get("LAB_HUB_PORT", "8100"))
BIND = os.environ.get("LAB_BIND", "0.0.0.0")
CHILD_BIND = os.environ.get("LAB_CHILD_BIND", "0.0.0.0")

PORTS = json.load(open(os.path.join(HERE, "ports.json")))

# The README's shelf table is the curated description of every project,
# including AUTOGOD's own verdict on whether it was worth building. Reuse it
# rather than inventing a second source of truth that will drift.
ROW = re.compile(
    r"^\|\s*\[\*\*(?P<name>[^*]+)\*\*\]\([^)]*\)\s*\|"
    r"\s*(?P<what>[^|]*)\|\s*(?P<kind>[^|]*)\|"
    r"\s*(?P<built>[^|]*)\|\s*(?P<worth>[^|]*)\|"
)


def shelf():
    meta = {}
    try:
        for line in open(os.path.join(HERE, "README.md")):
            m = ROW.match(line.strip())
            if m:
                d = m.groupdict()
                meta[d["name"].strip()] = {k: v.strip() for k, v in d.items()}
    except OSError:
        pass
    return meta


class Child:
    """One lab project, kept alive."""

    def __init__(self, name, port):
        self.name, self.port = name, port
        self.proc = None
        self.starts = 0
        self.last_error = ""

    @property
    def alive(self):
        return self.proc is not None and self.proc.poll() is None

    def start(self):
        d = os.path.join(HERE, self.name)
        run = os.path.join(d, "run.sh")
        if not os.path.isfile(run):
            self.last_error = "no run.sh"
            return
        env = dict(os.environ)
        env["LAB_BIND"] = CHILD_BIND
        env["LAB_PORT"] = str(self.port)
        try:
            # Run it through its own shebang: half the projects are #!/bin/sh
            # and half are #!/usr/bin/env bash using `set -o pipefail`, which
            # dash rejects. All 24 run.sh carry the exec bit.
            cmd = [run] if os.access(run, os.X_OK) else ["/bin/bash", run]
            self.proc = subprocess.Popen(
                cmd, cwd=d, env=env,
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                start_new_session=True)
            self.starts += 1
            self.last_error = ""
        except Exception as e:            # a broken project must not kill the hub
            self.last_error = str(e)

    def stop(self):
        if self.alive:
            try:
                os.killpg(os.getpgid(self.proc.pid), signal.SIGTERM)
            except Exception:
                pass


CHILDREN = [Child(n, p) for n, p in sorted(PORTS.items())]


def supervise():
    while True:
        for c in CHILDREN:
            if not c.alive and c.last_error != "no run.sh":
                c.start()
        time.sleep(10)


CSS = """
:root{--bg:#0b0b0c;--fg:#e8e6e3;--dim:#8a8681;--amber:#ffb000;--line:#232326}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--fg);
  font:14px/1.55 ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;padding:2.2rem 1.4rem}
.wrap{max-width:1000px;margin:0 auto}
h1{font-size:1.5rem;letter-spacing:.16em;text-transform:uppercase;margin:0 0 .2rem;
  font-style:italic;color:var(--amber)}
.sub{color:var(--dim);margin:0 0 2rem;font-size:.82rem}
table{width:100%;border-collapse:collapse}
th{text-align:left;font-size:.68rem;letter-spacing:.14em;text-transform:uppercase;
  color:var(--dim);font-weight:500;padding:0 .7rem .6rem;border-bottom:1px solid var(--line)}
td{padding:.62rem .7rem;border-bottom:1px solid var(--line);vertical-align:top}
tr:hover td{background:#141416}
a.p{color:var(--amber);text-decoration:none;font-weight:600}
a.p:hover{text-decoration:underline}
.what{color:var(--fg)}
.kind,.built{color:var(--dim);font-size:.8rem;white-space:nowrap}
.dot{display:inline-block;width:7px;height:7px;border-radius:50%;margin-right:.5rem}
.up{background:#3ddc84}.down{background:#4a4a4e}
.off{color:var(--dim)}
.note{margin-top:2rem;color:var(--dim);font-size:.76rem;border-top:1px solid var(--line);
  padding-top:1rem}
@media(max-width:640px){.kind,.built{display:none}}
"""


def page(host):
    meta = shelf()
    up = sum(1 for c in CHILDREN if c.alive)
    rows = []
    for c in CHILDREN:
        m = meta.get(c.name, {})
        cls = "up" if c.alive else "down"
        url = f"http://{host}:{c.port}/"
        if c.alive:
            link = f'<a class="p" href="{html.escape(url)}">{html.escape(c.name)}</a>'
        else:
            reason = c.last_error or "not running"
            link = (f'<span class="p off">{html.escape(c.name)}</span> '
                    f'<span class="kind">({html.escape(reason)})</span>')
        rows.append(
            f'<tr><td><span class="dot {cls}"></span>{link}</td>'
            f'<td class="what">{html.escape(m.get("what",""))}</td>'
            f'<td class="kind">{html.escape(m.get("kind",""))}</td>'
            f'<td class="built">{html.escape(m.get("built",""))}</td></tr>')

    return f"""<!doctype html><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>THE LAB</title><style>{CSS}</style>
<div class="wrap">
<h1>The Lab</h1>
<p class="sub">Everything AUTOGOD built in its spare time &middot;
{up} of {len(CHILDREN)} serving &middot; thebeast</p>
<table>
<tr><th>project</th><th>what it is</th><th>kind</th><th>built</th></tr>
{''.join(rows)}
</table>
<p class="note">Terminal projects (clock, dangling, reef) have no web front end &mdash;
ssh in and run them. The hub restarts any project that dies, every 10s.</p>
</div>"""


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Link back through whatever hostname the browser used, so the index
        # works over the LAN and over Tailscale without being told which.
        host = (self.headers.get("Host") or f"{BIND}:{PORT}").rsplit(":", 1)[0]
        if self.path.startswith("/status"):
            body = json.dumps({c.name: {"port": c.port, "up": c.alive,
                                        "starts": c.starts} for c in CHILDREN},
                              indent=1).encode()
            ctype = "application/json"
        else:
            body = page(host).encode()
            ctype = "text/html; charset=utf-8"
        self.send_response(200)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *a):
        pass


def main():
    threading.Thread(target=supervise, daemon=True).start()

    def bye(*_):
        for c in CHILDREN:
            c.stop()
        sys.exit(0)

    signal.signal(signal.SIGTERM, bye)
    signal.signal(signal.SIGINT, bye)
    srv = ThreadingHTTPServer((BIND, PORT), Handler)
    print(f"lab hub on http://{BIND}:{PORT}/  ({len(CHILDREN)} projects)", flush=True)
    srv.serve_forever()


if __name__ == "__main__":
    main()
