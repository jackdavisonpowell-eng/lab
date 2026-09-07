---
slug: cluster
title: cluster
kind: web-static
status: done
port: 8124
blurb: GR86 gauge cluster, DEMO + MANUAL drive
tile: screenshot.png
built: 2026-09-03
verified: 2026-09-07
worth: yes — it's your car
palette: (not recorded — this one was built while the skill still mandated amber)
---
# cluster


## pitch
A GR86-style digital gauge cluster as one web page: a big glowing tach dial
(0-8k, redline at 7300) with a sweeping needle, a giant italic gear readout,
a km/h number, coolant + fuel bars, a lap timer, and a GR86-style shift lamp
that blinks at 6500 and strobes at 7000. It's driven entirely by fake
telemetry: a DEMO mode loops through IDLE → LAUNCH → CRUISE → PUNCH →
BRAKE (with a rev-match blip on the downshift) → COAST, so the page is alive
the second it loads. Press M (or click the mode chip) for MANUAL mode:
hold SPACE to rev, 1-6 to shift, S to brake, R to reset. No framework, no
build step, no network: one HTML file with inline CSS/JS, served by
python3 -m http.server. White/amber monotone on near-black, big italic
numbers — the cockpit toy you open and watch rev itself.

## how it runs
./run.sh → http://127.0.0.1:8124/ (lab port 8124; 8120 breath, 8123 horse-tinder)
