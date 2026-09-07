---
slug: supernova
title: supernova
kind: web-static
status: done
port: 8138
blurb: Outer Wilds 22-min loop timer, the sun dies
tile: 
built: 2026-09-04
verified: 2026-09-07
worth: yes if you play OW
palette: (not recorded — this one was built while the skill still mandated amber)
---
# SUPERNOVA


## pitch
SUPERNOVA is a 22-minute loop timer for playing Outer Wilds, where the thing
you're timing yourself against is the sun itself. A single HTML file (no
dependencies, no installs) renders an ambient sun at the center of a starfield
that breathes slowly while you play. As the 22 minutes run down the sun grows
unstable — it shifts from calm amber to agitated red, its corona spikes, dust
starts drifting, a low 55 Hz drone swells — and at zero it goes nova: a white
flash, an expanding ring, the screen fading to black, "LOOP N" appearing, and
three soft offset bells ringing (a soft alarm, not a harsh one). Then the next
22-minute loop begins automatically. The loop count persists in localStorage.
It's the toy nobody would bother to build: a countdown where the countdown IS
the thing that kills you, and the alarm is the sun dying.

## how it runs
`./run.sh` → `python3 -m http.server 8127 --bind 127.0.0.1` from the project dir.
Open http://127.0.0.1:8127, click START. One file: index.html with inline
CSS/JS. Controls: START / HOLD / RESET / SOUND (the sound toggle also unlocks
the Web Audio context — browsers need one user gesture before audio plays).
Test with a short loop: http://127.0.0.1:8127/?seconds=90.

## verified (2026-09-04)
- `node --check` on the extracted inline script: SYNTAX OK.
- Loaded in a real browser: no runtime throw (re-ran the script in try/catch).
- Canvas animation proven live by sampling the center pixel twice ~2.5s apart
  (luminance 0 → 672, oscillates) and a lit-pixel fraction of 0.186 across a
  center band (the glow is actually on screen, not a static frame).
- Drove the real UI with ?seconds=3: countdown 00:03→00:00, phase
  CALM→GROWING UNSTABLE→nova (THE SUN IS GONE), loop counter incremented
  (LOOP 002→003), timer reset to 00:03 and auto-restarted, and the count
  persisted in localStorage. HOLD froze the countdown at a non-zero value;
  RESET snapped it back to full with the sun calm. Default page shows 22:00.
- Pure functions (fmt, phaseFor, loopLength, phaseParams, lerpC) asserted in a
  Node harness across boundary inputs: all passed.

## next
If resumed: (1) a count-UP "time until the sun goes nova" mode you can leave
open between loops; (2) a per-loop log of start/end timestamps in localStorage
so you can see how many loops you actually finished; (3) an optional deeper
bell an octave down for the final moment.
