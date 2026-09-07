---
slug: rain
title: rain
kind: web-static
status: done
port: 8121
blurb: vault note titles as matrix rain
tile:
built: 2026-09-05
verified: 2026-09-07
worth: maybe — pure aesthetic
palette: (not recorded — this one was built while the skill still mandated amber)
---
port: 8121

Pitch: The vault is 887 notes deep and nobody looks at it sideways. `rain`
renders the whole thing as an amber matrix-rain screensaver: each falling
stream is one real note title, head-glyph bright, tail fading into the dark.
Hovering a stream freezes it so you can read it; clicking catches the title
into a side ledger (last 14, numbered). It is the vault as weather.

Run: `sh run.sh` → http://127.0.0.1:8121/

Verified 2026-09-05: node --check clean; browser runtime-eval clean; canvas
pixel sampling shows live animation (lit fraction 0.2585→0.2416 over 2.5s);
space-pause dims HUD without clobbering it; click caught a real title into the
ledger ("User attends Georgia Southern College"). Port 8121 confirmed free
after kill.

show: cd /home/jack/lab/rain && sh run.sh → http://127.0.0.1:8121/

next: (if revisited) caught titles re-enter the rain as brighter "ghost"
streams; or a folder-filter mode (rain only College/ or only AUTOGOD/ titles).
