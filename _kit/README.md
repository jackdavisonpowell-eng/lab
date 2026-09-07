# _kit — the shared kit every lab web project starts from

One amber, one type system, one set of cut-corner chrome rules, and the
boilerplate that got rewritten in every one of the 21 projects before this
existed. Colour is still yours (see `palette:` in your PROJECT.md); the
structure is not.

## Start a project from the kit — five lines

```sh
cd /home/jack/lab
cp -r _kit <slug> && rm <slug>/snippets.md <slug>/index.html   # base.css + run.sh in
# 1. edit run.sh: set the <port> placeholder (lowest free in 8100-8199, see ports.json)
# 2. add "<slug>": <port> to /home/jack/lab/ports.json
# 3. write index.html — <link rel="stylesheet" href="base.css">, override :root vars,
#    paste the blocks you need from snippets.md (canvas / keydown / share-card)
# 4. write PROJECT.md FIRST (YAML header + pitch + next:), then README.md
# 5. ./run.sh, curl -s http://127.0.0.1:<port>/ | head -c 300, kill by PID
```

## What's in the kit

- **base.css** — the skin. `:root` vars (override per project), the display
  type (italic serif, big numbers), HUD/help corners, header rule, chips,
  cut-corner buttons, canvas rules. Letter-spacing comes from a fixed scale
  (`--ls-tight` … `--ls-mark`), not freestyle.
- **run.sh** — the template. `#!/bin/sh`, positional port with `$LAB_PORT` /
  `$LAB_BIND` fallbacks, `exec python3 -m http.server`. No `set -euo pipefail`
  (bash-only `pipefail` kills it under dash).
- **snippets.md** — copy-paste JS: DPR-correct canvas + resize + clamped-dt
  loop + trail-fade; keydown (tap keys and held keys); the 1080x1080
  share-card SVG renderer (from kicker) with wrap/esc/save; clipboard with
  fallback; data fetch with offline fixture.
- **index.html** — a live demo of every class in base.css. `./run.sh` serves
  it; it is also the reference for what the vars are supposed to look like.

## The one amber

`ember = #ffb000`. Six ambers were invented across the fleet before this
(`#ffb454`, `#ffbb5c`, `#ffaa3c`, `#ffb347`, `#ffb000`, `#ff8c1a`); they all
mean the same thing. `--accent` is the one to change if the subject is not
amber — a Subnautica tracker is not the same colour as a tennis ladder. Two
projects in a row with the same palette is a bug, not a house style.

## Rules that still apply (from the skill)

- Never hardcode Jack's vault: `os.environ.get("AUTOGOD_VAULT", ...)` /
  `$AUTOGOD_VAULT`, never a literal `$AUTOGOD_VAULT`.
- Never commit his data: read at runtime, ship a small synthetic fixture,
  `.gitignore` the real file. `rain/` is the worked example.
- Ports are assigned from `ports.json`, not chosen.
