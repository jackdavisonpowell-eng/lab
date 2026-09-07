---
slug: abyss
title: abyss
kind: web-static
status: done
port: 8128
blurb: Subnautica depth/blueprint tracker
tile: screenshot.png
built: 2026-09-05
verified: 2026-09-07
worth: yes if you play it
palette: (not recorded — this one was built while the skill still mandated amber)
---
# ABYSS


## Pitch
A Subnautica progress tracker that feels like the game. A vertical depth gauge
shows your max depth against the real zone bands (Sunset → Deep → Abyss → Dunes →
Trench → Lost River), reads the pressure in atmospheres (≈1 atm per 10 m), and
names the leviathan lurking at that depth. Below it, two checklists — blueprints
found and base modules built — with per-group and overall progress, plus a field
to add your own entries. Everything saves to the browser's localStorage, so it's
private and local: open the page, track your run, close the tab. White/amber
monotone, sharp italic, bioluminescent particles drifting up from the dark.

## Verified (2026-09-05)
- Depth math: 34 node assertions pass (zone boundaries, lurk lookup, pressure,
  marker pct, clamp at 0/4000, group progress, no dupes).
- UI driven in browser: set depth 2500 → zone "The Trench", 251 atm, Reaper
  lurk, marker 62.5%; check blueprint + base module; add/remove custom entry;
  reset wipes; localStorage persists (abyss-save-v1); canvas particles animate
  (region lit count oscillates 41–65 over 2s).
- run.sh serves HTTP 200 from a clean shell; port 8128 freed after.

## next:
Add leviathan-encounter counter (log Ghost/Reaper/Sea Dragon sightings) and
import/export the save as JSON so a run survives a browser wipe.

## notes
- Port 8128 (lab range 8100-8199, was free on 2026-09-05).
- Single index.html, inline CSS/JS, no deps. run.sh = python3 -m http.server.
- Data (zones, blueprint/base lists) is curated in the JS at the top of
  index.html; Jack can edit it or use the in-page "add" field for gaps.
