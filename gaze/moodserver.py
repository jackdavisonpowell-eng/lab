#!/usr/bin/env python3
"""Tiny mood endpoint for testing ?poll= — cycles moods every 2s. Lab-only."""
import http.server, json, time

MOODS = ["idle", "happy", "thinking", "alert", "sad", "speaking"]
i = 0

class H(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        global i
        if self.path.startswith("/mood"):
            i = (i + 1) % len(MOODS)
            body = json.dumps({"mood": MOODS[i]})
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(body.encode())
        else:
            self.send_response(404); self.end_headers()
    def log_message(self, *a): pass

http.server.HTTPServer(("127.0.0.1", 8198), H).serve_forever()
