---
slug: breath
title: breath
kind: web-server
status: done
port: 8120
blurb: the machine's GPUs as breathing lungs
tile: screenshot.png
built: 2026-09-02
verified: 2026-09-07
worth: yes — best screensaver here
palette: (not recorded — this one was built while the skill still mandated amber)
---
# breath


## pitch
thebeast breathes. A full-screen, single-page visual where the machine's three
GPUs are drawn as concentric amber lungs. Each GPU's temperature sets the *tempo*
of its breath (30C = a slow 9.5s cycle, 80C = a fast 2.2s gasp) and its
utilisation sets the *fire* (how hot and bright the ring burns). A tribal tick
ring marks the perimeter, a soft ember fills the background in proportion to
aggregate heat, and a core blinks at the center. A minimal HUD shows per-GPU
temp/util/power with awake lamps, a mood line (IDLE / CHEWING / ROARING) and the
aggregate heat as a big italic number. It's the "open one page and watch the
machine breathe" toy, taken to its literal limit. No framework, no build step:
one Python stdlib server + one HTML file, read-only on the host (only reads
nvidia-smi, never touches the brain).

## how it runs
`./run.sh` starts a tiny stdlib http.server on 127.0.0.1:8120 that serves
index.html and a `/stats` JSON endpoint (nvidia-smi only). The page polls /stats
every 2s; the canvas animates at 60fps with a shaped breath curve (quick inhale,
brief hold, long slow exhale). Each GPU gets its own lung ring, outermost = gpu 0.

## verified (2026-09-02)
Ran it: server bound 127.0.0.1:8120, `/stats` returned live JSON (host THEBEAST,
3 GPUs — V100 ~71C awake, 2 P100s ~34C asleep). Loaded the page in a real browser:
inline script re-thrown in a try/catch with NO error, zero console/JS errors, GPU
HUD populated (V100 lamp on, P100s off, mood IDLE, aggregate 50C). Sampled canvas
pixels: 92% of the frame is lit amber, brightest pixel dead-center, and the center
pixel's luminance oscillated over 2.5s (240->251->246) proving the breath loop is
live, not a static frame. Screenshot saved to screenshot.png. Server shut down
after (no service left running).

## next
If resumed: (1) let the breath *phase-lock* — offset each lung's phase by its
index so they inhale in a staggered wave instead of all in sync; (2) add a
"hold breath" pause when a GPU is awake but util=0 (the V100 sitting warm at
55W idle); (3) a subtle screen-space heat shimmer when aggregate temp > 70C;
(4) a /stats history ring buffer (last ~120 samples) so the HUD can draw a tiny
temp sparkline under each GPU row.
