#!/usr/bin/env python3
"""Refuse to publish Jack's data.

Runs over the files git is actually tracking, not the working tree, so a
gitignored file is out of scope by construction. Fails CLOSED: any hit, or any
error, and the push is blocked.

The rules are about DATA, not about names. thebeast, FRIDAY and AUTOGOD are
things Jack publishes on purpose; his note titles, his briefs, his coursework
files and his agent journals are not.
"""
import re, subprocess, sys, os

DENY = [
    ("personal-dataset", re.compile(r"(titles\.json|.*journal.*\.log|per-task\.md|media-picks)$"), "name"),
    ("vault-path",   re.compile(rb"(/data/vault|/home/jack/vault)"), "body"),
    ("tailnet-ip",   re.compile(rb"\b100\.(6[4-9]|[7-9]\d|1[01]\d|12[0-7])\.\d{1,3}\.\d{1,3}\b"), "body"),
    ("lan-ip",       re.compile(rb"\b192\.168\.\d{1,3}\.\d{1,3}\b"), "body"),
    ("gh-token",     re.compile(rb"gh[pousr]_[A-Za-z0-9]{20,}"), "body"),
    ("bearer",       re.compile(rb"(?i)(authorization|bearer)\s*[:=\"']*\s*[A-Za-z0-9_\-]{24,}"), "body"),
    ("tg-token",     re.compile(rb"\b\d{9,}:[A-Za-z0-9_\-]{30,}\b"), "body"),
    ("api-key",      re.compile(rb"(?i)(api[_-]?key|access[_-]?token|client[_-]?secret)\s*[:=]\s*[\"'][^\"']{12,}"), "body"),
    ("email",        re.compile(rb"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"), "body"),
    ("ssh-key",      re.compile(rb"BEGIN (RSA|OPENSSH|EC|DSA) PRIVATE KEY"), "body"),
]
BINARY = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".wav", ".mp3", ".ico", ".ttf", ".woff", ".woff2"}

files = subprocess.run(["git", "ls-files", "-z"], capture_output=True, check=True
                       ).stdout.decode().split("\0")
hits = []
# .bin/ is the scanner itself: its own rule strings would match.
for f in filter(None, files):
    if f.startswith(".bin/"):
        continue
    for rule, rx, where in DENY:
        if where == "name":
            if rx.search(os.path.basename(f)):
                hits.append((f, rule, os.path.basename(f)))
            continue
        if os.path.splitext(f)[1].lower() in BINARY or not os.path.exists(f):
            continue
        try:
            blob = open(f, "rb").read()
        except Exception as e:
            hits.append((f, "unreadable", str(e))); continue
        if b"\x00" in blob[:4096]:
            continue
        m = rx.search(blob)
        if m:
            hits.append((f, rule, m.group(0)[:70].decode("utf-8", "replace")))

if hits:
    print(f"{len(hits)} finding(s):", file=sys.stderr)
    for f, rule, sample in hits:
        print(f"  {f:44s} {rule:16s} {sample!r}", file=sys.stderr)
    sys.exit(1)
print(f"clean — {len([f for f in files if f])} tracked files scanned")
