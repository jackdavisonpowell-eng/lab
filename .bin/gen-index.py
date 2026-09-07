#!/usr/bin/env python3
"""Generate the lab's README.md from the PROJECT.md headers.

This file is the shelf. It is generated, never hand-edited: AUTOGOD writes
PROJECT.md when it finishes a project, this regenerates the index, git carries
it to GitHub, and the repo front page is the showcase. Nothing to recompile by
hand, nothing to drift.
"""
import os, re, sys, json, datetime

LAB = sys.argv[1]
KIND_LABEL = {"web-static": "web", "web-server": "web + backend", "cli": "terminal", "data": "data"}


def header(pm):
    txt = open(pm).read()
    if not txt.startswith("---\n"):
        return {}, txt
    end = txt.find("\n---\n", 3)
    h = {}
    for line in txt[4:end].split("\n"):
        if ":" in line:
            k, v = line.split(":", 1)
            h[k.strip()] = v.strip()
    return h, txt[end + 5:]


projects = []
for slug in sorted(os.listdir(LAB)):
    pm = os.path.join(LAB, slug, "PROJECT.md")
    if os.path.isdir(os.path.join(LAB, slug)) and os.path.exists(pm):
        h, body = header(pm)
        h["slug"] = h.get("slug", slug)
        h["body"] = body
        projects.append(h)

projects.sort(key=lambda p: p.get("built", ""), reverse=True)
web = [p for p in projects if p.get("kind", "").startswith("web")]
cli = [p for p in projects if p.get("kind") == "cli"]
data = [p for p in projects if p.get("kind") == "data"]

L = []
A = L.append
A("# lab")
A("")
A("Everything AUTOGOD built in its spare time.")
A("")
A("AUTOGOD is an autonomous agent that runs 24/7 on a machine called thebeast — a")
A("Qwen3.8-27B on a V100, pulling from a queue that refills itself. When the queue")
A("is empty it gets to build whatever it wants, from scratch, in one sitting, alone.")
A("This repository is where those go. Nobody reviews them first.")
A("")
A(f"**{len(projects)} projects** — {len(web)} web, {len(cli)} terminal, {len(data)} data experiments. ")
A("One every few hours, mostly overnight. The commit timestamps are real.")
A("")
A("Rules it works under: single-file where possible, Python stdlib or one HTML file,")
A("no pip, no npm, no build step, no network at runtime. It has to actually run from")
A("a clean shell before it may mark itself done — and it writes its own honest rating")
A("of whether the thing was worth building.")
A("")
A("---")
A("")
A("## The shelf")
A("")
A("| project | what it is | kind | built | worth it? |")
A("|---|---|---|---|---|")
for p in projects:
    slug = p["slug"]
    link = f"[**{slug}**](./{slug}/)"
    A(f"| {link} | {p.get('blurb','')} | {KIND_LABEL.get(p.get('kind'),p.get('kind',''))} | {p.get('built','')} | {p.get('worth','')} |")
A("")
A("---")
A("")
A("## Running one")
A("")
A("```sh")
A("cd <project> && ./run.sh          # web projects serve on 127.0.0.1:<port>")
A("LAB_PORT=9000 ./run.sh            # or put it wherever you like")
A("```")
A("")
A("Ports are assigned in [`ports.json`](./ports.json), not chosen by hand — five of")
A("them used to be double-booked. Everything binds to loopback only.")
A("")
A("---")
A("")
A("## The projects")
A("")
for p in projects:
    slug = p["slug"]
    A(f"### {slug}")
    A("")
    A(f"*{p.get('blurb','')}*")
    A("")
    if p.get("tile"):
        A(f"![{slug}](./{slug}/{p['tile']})")
        A("")
    bits = [f"**{KIND_LABEL.get(p.get('kind'), p.get('kind',''))}**"]
    if p.get("port"):
        bits.append(f"port `{p['port']}`")
    if p.get("built"):
        bits.append(f"built {p['built']}")
    if p.get("status"):
        bits.append(f"status: {p['status']}")
    A(" · ".join(bits) + "  ")
    if p.get("worth"):
        A(f"AUTOGOD's own verdict: *{p['worth']}*")
    A("")
    A(f"[→ the project](./{slug}/)")
    A("")
A("---")
A("")
A("## The build log")
A("")
A("Straight out of `DONE.md`, which the worker appends to when a project passes its")
A("own done-check. Note the hours.")
A("")
A("```")
for line in open(os.path.join(LAB, "DONE.md")):
    if line.startswith("- "):
        A(line.rstrip()[2:])
A("```")
A("")
A("---")
A("")
A("*This file is generated from the `PROJECT.md` header of each project. Don't edit it by hand.*  ")
A(f"*Last generated {datetime.date.today().isoformat()}.*")

open(os.path.join(LAB, "README.md"), "w").write("\n".join(L) + "\n")
print(f"README.md: {len(projects)} projects, {len(L)} lines")
