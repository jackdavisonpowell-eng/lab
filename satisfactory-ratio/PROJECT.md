---
slug: satisfactory-ratio
title: satisfactory-ratio
kind: web-static
status: done
port: 8131
blurb: Satisfactory T7 production-ratio calc
tile: screenshot.png
built: 2026-09-04
verified: 2026-09-07
worth: yes if you play Satisfactory
palette: (not recorded — this one was built while the skill still mandated amber)
---
# RATIO — Satisfactory production-ratio calculator

Pick a Phase 4 / Tier 7 target item and a production rate. RATIO expands the full
recipe tree and tells you, per minute: how many of each machine you must run, and
how much of each base resource (ore, concrete, etc.) the whole line consumes.
Hardcoded recipes I'm sure of are computed; the rest are marked `unknown` and
shown as gaps.

Verified 2026-09-04: `node --check` clean; Node harness ran the page's real
`solve()` across 8 input sets (24 assertions, all pass — iron plate, steel beam,
electric motor fully resolve; mk.4/mk.5 correctly flag their unknown ingredient);
form driven in a browser (electric motor @100 → machines 1.67/1.25/1.25/1.67, base
iron ore 400 / coal 200 / copper ore 300, no gaps); `run.sh` works from a clean
shell (launched from /tmp, serves on 8131). Port 8131 freed after.

## next:
Add the real Tier 7 recipes from the wiki so the Mk.5 chain resolves fully —
`alclad aluminum sheet` and `encased industrial beam` (plus their ingredients)
into the `RECIPES` object in `index.html`. Then add per-machine overclock
multipliers and a summed power-draw (W) column.
