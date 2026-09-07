---
slug: gaze
title: gaze
kind: web-server
status: done
port: 8122
blurb: pixel FRIDAY face, 12 moods, for the Pi
tile: screenshot.png
built: 2026-09-07
verified: 2026-09-07
worth: yes — has a real deployment target
palette: (not recorded — this one was built while the skill still mandated amber)
---
# FRIDAY — gaze

A 24×24 pixel-art FRIDAY face that sits on the Pi's display and *lives*: it
blinks on a random cadence, breathes (a slow 1px bob + an amber glow pulse),
and drifts between twelve mood states — idle, listening, thinking, speaking,
happy, sad, alert, surprised, sleepy, focus, error, offline. The whole thing is
one self-contained HTML file (no deps, no build) that reads its mood from the
URL, so the Pi just points a browser at it and a small poller (or FRIDAY
herself) can flip it by hitting `?mood=happy` or `?poll=<url>`.

The point is the *face*, not the plumbing: a small, sharp, amber-on-black
presence that makes a wall of Pi feel like something is looking at you.

## Contract
- `?mood=<name>` — pin a mood (stops auto-drift).
- `?poll=<url>` — poll a URL every 2s for the live mood (plain text or `{"mood":"x"}`).
- `window.FRIDAY_FACE` — `{ setMood, getMood, moods, blink, setAuto }` for a page to drive it in-process.
- Keyboard: ←/→ step mood, space toggles auto-drift, b forces a blink, 1–9/0 direct.

## Run
```
cd /home/jack/lab/gaze && sh run.sh
# → http://127.0.0.1:8122/
```

## next:
Wire up the Pi end-to-end: a tiny poller that reads FRIDAY's current mood
(wake-word / speech state from friday.server) and hits the page with ?poll=, so
the face actually mirrors what she's doing. Then add a "look-at-pointer"
eyeball (pupil offsets toward the cursor) for the idle state.
