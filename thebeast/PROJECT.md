---
slug: thebeast
title: thebeast
kind: web-server
status: done
port: 8117
blurb: live host dashboard (GPU/CPU/RAM/proc feed)
tile: screenshot.png
built: 2026-09-01
verified: 2026-09-07
worth: yes — the flagship
palette: (not recorded — this one was built while the skill still mandated amber)
---
# thebeast


## pitch
thebeast is the machine that runs all day on its own GPU. This project is a single
self-contained web page — a live, terminal-styled dashboard of *this* host: per-GPU
temperature / VRAM / utilization / power, CPU load, RAM, uptime, and a live
"what's chewing the machine" process feed. It's the thing nobody bothers to build:
open one page and watch the beast breathe in real time. No framework, no build step,
one Python stdlib server + one HTML file.

## how it runs
`./run.sh` starts a tiny stdlib http.server on 127.0.0.1:8117 that serves index.html
and a `/stats` JSON endpoint (nvidia-smi + /proc). The page polls /stats every 2s.
Read-only on the host — it only *reads* nvidia-smi and /proc, never touches the brain.

## verified (2026-09-01)
Ran it: server bound 127.0.0.1:8117, `/stats` returned live JSON (host THEBEAST,
3 GPUs — V100 awake 71C/29GB VRAM, 2 P100s asleep; load, RAM 78%, top procs), `/`
served the 6.5KB page. Confirmed in a real browser via DOM: 3 GPU cards with filled
util/vram/temp bars + awake/asleep lamps, system card (host/uptime/load/ram), and a
5-row process feed all populated live. Screenshot saved to screenshot.png. Server
shut down after (no service left running).

## next
If resumed: add a rolling sparkline history of the V100's utilization + temp
(keep last ~120 samples in JS, draw on a <canvas>), a per-GPU "time awake" counter,
and a "beast mood" line derived from aggregate load (e.g. "idling / chewing /
roaring"). Optional: a /stats?history=1 endpoint that returns the last N samples
from a small in-memory ring buffer so sparklines survive page refreshes.
