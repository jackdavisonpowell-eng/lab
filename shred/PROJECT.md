---
slug: shred
title: shred
kind: web-static
status: done
port: 8137
blurb: skate trick roulette + heat meter
tile: screenshot.png
built: 2026-09-03
verified: 2026-09-07
worth: yes — fun toy
palette: (not recorded — this one was built while the skill still mandated amber)
---
# shred


## pitch
A skateboarding trick roulette. Three slot-machine reels — TRICK × STANCE ×
SPOT — spin on spacebar and land on a call like "cork 540 flip × switch ×
12-stair". You go do the trick (or don't), come back, and log landed or
bailed. It tracks your landed streak, best streak, bail streak, and a
decaying "heat" meter (exponentially weighted last-14 outcomes) that drops
from "shred" to "cold" as you bail. A per-trick table accumulates
landed/bailed/rate per trick, and flags a trick as WRECKED after two
straight bails. Everything lives in localStorage. Amber on near-black,
italic big numbers, CRT scanlines — same bloodline as breath/lapboard.
One HTML file, zero dependencies.

## how it runs
`./run.sh [port]` (default 8126) serves the single index.html via
`python3 -m http.server` on 127.0.0.1. Keys: space = spin, l = landed,
b = bailed. localStorage key `shred.stats.v1` holds {landed, bailed,
streak, best, bailstreak, results (last 200 1/0s), tricks:{name:{l,b}}}.
Heat = exp-weighted (1.25^i) fraction of landed over the last 14 results.

## verified (2026-09-03)
- node --check on the extracted inline script: pass.
- Served on 127.0.0.1:8126, drove the real UI in a browser: spin landed
  reels on the exact announced trick/stance/spot (reel math verified by
  reading the .mid item text), log landed/bailed updated streaks + best +
  heat bar, per-trick table rows appeared, localStorage round-tripped,
  bail shake fired, reset cleared. Server killed, port 8126 free.

## next
If resumed: (1) session mode — a "session" of N spins with a pass/fail
grade at the end (e.g. 7/10 = "solid"), stored as a session list in
localStorage; (2) trick difficulty tiers (street/park/vert) that weight
the reels and give heat bonus for landing harder tiers; (3) sound —
WebAudio click per reel step + a bass thump on bail, no assets,
oscillator-only; (4) "the board" — a small SVG deck that flips on a
successful spin (switch stance flips it).
