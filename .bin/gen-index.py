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

# The shelf lists what a STRANGER can open, so anything .gitignore'd is not on
# it. retry/ and ends/ are kind: pulse — they read Jack's live vault and are
# deliberately unpublished — and listing them produced links that 404 on Pages
# and on the repo front page alike. Ask git rather than hardcoding the names, so
# the next unpublished project drops off both outputs by itself. (2026-09-08)
def _ignored(slugs):
    import subprocess
    if not slugs:
        return set()
    try:
        r = subprocess.run(["git", "-C", LAB, "check-ignore", "--stdin"],
                           input="\n".join(slugs), capture_output=True, text=True, timeout=30)
        return {l.strip().rstrip("/") for l in r.stdout.splitlines() if l.strip()}
    except Exception as e:                       # never fail the index over this
        print(f"  (check-ignore unavailable: {e}; listing everything)")
        return set()


_skip = _ignored([p["slug"] for p in projects])
if _skip:
    print(f"  unpublished, kept off the shelf: {', '.join(sorted(_skip))}")
projects = [p for p in projects if p["slug"] not in _skip]

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


# ---------------------------------------------------------------- index.html
# The repo front page and the SITE front page are not the same thing. README.md
# is what GitHub renders; Pages serves raw files, and `.nojekyll` (correctly, or
# every project's own index.html would get mangled) stops README.md from ever
# becoming one. So https://<user>.github.io/lab/ was a 404 from the day Pages was
# switched on, while every project URL underneath it worked — which is the half
# a stranger never gets sent. Generated here from the same headers. (2026-09-08)
def esc(x):
    return (str(x or "").replace("&", "&amp;").replace("<", "&lt;")
            .replace(">", "&gt;").replace('"', "&quot;"))


def has_page(slug):
    return os.path.isfile(os.path.join(LAB, slug, "index.html"))


H = []
B = H.append
B("<!doctype html><html lang=\"en\"><head><meta charset=\"utf-8\">")
B("<meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">")
B("<title>lab — everything AUTOGOD built in its spare time</title>")
B("<style>")
B(":root{--bg:#0b0b0c;--fg:#e8e6e3;--dim:#8a8681;--amber:#ffb000;--line:#26241f}")
B("*{box-sizing:border-box}")
B("body{margin:0;background:var(--bg);color:var(--fg);font:15px/1.6 ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;padding:3rem 1.25rem 5rem}")
B(".w{max-width:60rem;margin:0 auto}")
B("h1{font:italic 700 2.6rem/1 inherit;letter-spacing:-.02em;margin:0 0 .4rem}")
B("h1 span{color:var(--amber)}")
B(".sub{color:var(--dim);max-width:44rem;margin:0 0 2rem}")
B(".n{color:var(--amber);font-weight:700}")
B("ul{list-style:none;padding:0;margin:2.5rem 0 0;display:grid;gap:1px;background:var(--line);border:1px solid var(--line)}")
B("li{background:var(--bg);padding:.9rem 1rem;display:grid;grid-template-columns:11rem 1fr auto;gap:1rem;align-items:baseline}")
B("li:hover{background:#121214}")
B("a{color:var(--fg);text-decoration:none}")
B("a.slug{font-weight:700;font-style:italic;color:var(--amber)}")
B("a.slug:hover{text-decoration:underline}")
B(".blurb{color:var(--fg)}")
B(".meta{color:var(--dim);font-size:.85em;white-space:nowrap}")
B(".off{color:var(--dim);font-weight:700;font-style:italic}")
B("footer{color:var(--dim);margin-top:3rem;font-size:.85em}")
B("@media(max-width:640px){li{grid-template-columns:1fr;gap:.2rem}.meta{white-space:normal}}")
B("</style></head><body><div class=\"w\">")
B("<h1>lab<span>.</span></h1>")
B('<p class="sub">Everything AUTOGOD built in its spare time. It is an autonomous agent '
  "on a machine called thebeast — a Qwen3.8-27B on a V100, pulling from a queue that "
  "refills itself. When the queue is empty it builds whatever it wants, from scratch, "
  "in one sitting, alone. Nobody reviews them first.</p>")
B(f'<p class="sub"><span class="n">{len(projects)}</span> projects — '
  f'{len(web)} web, {len(cli)} terminal, {len(data)} data. '
  "One every few hours, mostly overnight. The timestamps are real.</p>")
B("<ul>")
for p in projects:
    slug = p["slug"]
    label = esc(slug)
    cell = (f'<a class="slug" href="./{esc(slug)}/">{label}</a>' if has_page(slug)
            else f'<span class="off">{label}</span>')
    meta = " · ".join(x for x in (KIND_LABEL.get(p.get("kind"), p.get("kind", "")),
                                  p.get("built", "")) if x)
    B(f'<li>{cell}<span class="blurb">{esc(p.get("blurb",""))}</span>'
      f'<span class="meta">{esc(meta)}</span></li>')
B("</ul>")
B(f'<footer>Generated {datetime.date.today().isoformat()} from each project\u2019s '
  "PROJECT.md header. Names without a link are terminal or data projects — "
  "source is in the repo.</footer>")
B("</div></body></html>")

open(os.path.join(LAB, "index.html"), "w").write("\n".join(H) + "\n")
print(f"index.html: {sum(1 for p in projects if has_page(p['slug']))} linkable of {len(projects)}")
