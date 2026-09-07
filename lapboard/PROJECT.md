---
slug: lapboard
title: lapboard
kind: web-server
status: done
port: 8125
blurb: sim-racing lap timer + delta strip
tile: screenshot.png
built: 2026-09-07
verified: 2026-09-07
worth: yes if you sim
palette: (not recorded — this one was built while the skill still mandated amber)
---
# lapboard


## pitch
A sim-racing lap timer and delta board for a second screen. You open it,
press space, and a huge italic number ticks up as your lap runs. Beside it,
a live delta vs your best lap turns green when you're ahead and red when
you're behind — recomputed every 150 ms against the best lap's
cumulative-time samples, so you can see *where on the lap* you're losing
time, not just the total. Below, a full-lap strip draws the best lap as a
thin amber ghost line and your live lap over it in green/red, with a moving
dot. Best and last laps sit under the big number. Amber on near-black,
tabular numerals, no pastel — built for a wall of a sim rig, not a laptop.
Laps live in a plain `laps.json` the server re-reads on mtime change, so an
external telemetry exporter can just write the file — no restart, no
protocol. One Python stdlib server + one HTML file, local-only.

## how it runs
`./run.sh [port]` (default 8125) starts `server.py` (stdlib
http.server, 127.0.0.1). Endpoints: `GET /laps`, `POST /lap/start`,
`POST /lap/finish`, `POST /lap/reset-best`, `POST /lap/reset`. The page
polls `/laps` every 150 ms. Keys: space = start/finish, b = drop best lap,
r = reset all. `laps.json` format: `[{"t": 161.095, "d": [0.0, 0.5, ...,
161.095]}, ...]` — `t` total seconds, `d` cumulative-time samples for delta
matching. A server-finished lap gets a 2-point `d`; a real exporter supplies
the full curve.

## verified (2026-09-03)
Ran it: server bound 127.0.0.1:8125, `GET /laps` returned the seed data (5
laps, best 161.095). `node --check` on the extracted inline script passed;
re-thrown in a browser try/catch with NO runtime error. DOM in idle: best
2:41.095, last 2:41.449, delta +0:00.354 (red/behind), "lap 5". Drove the
real UI with dispatched Space keydowns: lap started (state → recording,
live lamp on, live ticking 1.365 → 3.464 s, delta live vs best), second
Space finished it (lap 6, last 0:03.502, back to idle). Canvas strip
sampled via getImageData: 3.86% of pixels lit, brightest pixel at
[875,28] — the curve is on screen. API tested end-to-end over curl:
start/finish appends, reset-best drops the min, an external write to
laps.json is picked up on the next poll (mtime reload), reset clears.
Server killed after; port 8125 confirmed free.

## next
If resumed: (1) sector splits — tag `d` samples with sector boundaries and
show three delta columns (S1/S2/S3) under the main delta; (2) telemetry
ingest — a `/telemetry` POST or WebSocket so a sim exporter streams live
samples and the strip draws the real lap shape instead of the 2-point
straight line a manual start/finish produces; (3) ghost audio — a soft tick
when crossing each best-lap sample (high when ahead, low when behind);
(4) multi-car — two live laps side by side for split-screen vs a friend.
