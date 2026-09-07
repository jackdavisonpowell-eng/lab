# SUPERNOVA

A 22-minute loop timer for playing Outer Wilds, with an ambient sun that
grows unstable as the loop runs down and goes nova when it hits zero.

## what it is

One HTML file, no dependencies. The sun sits at the center of a starfield
and breathes slowly. As the timer runs:

- **22:00 – 6:36 remaining (calm)** — slow amber breathing, faint corona,
  a low 55 Hz drone under everything.
- **6:36 – 1:54 remaining (agitated)** — the sun shifts red, the corona
  spikes, dust starts drifting, a rising swell builds.
- **last 1:54 (final)** — fast flicker, red vignette closing in, the swell
  peaks.
- **0:00** — the sun goes nova: white flash, expanding ring, everything
  fades to black, "LOOP N" appears, and three soft offset bells ring
  (no harsh alarm). Then the next 22-minute loop starts automatically.

Loop count persists in localStorage. Controls: START / HOLD / RESET /
SOUND (the sound toggle also unlocks the Web Audio context — browsers
require one user gesture before audio can play).

## how to run

    cd /home/jack/lab/supernova
    ./run.sh

Then open http://127.0.0.1:8127 in a browser. Click START.

To test with a shorter loop (e.g. 90 seconds):
http://127.0.0.1:8127/?seconds=90

## what I'd add

- A "time until the sun goes nova" mode that counts *up* from when you
  start playing, so you can leave it open between loops.
- A per-loop log of when each loop started/ended (localStorage), so you
  can see how many loops you actually finished.
- Optional: a second, deeper bell an octave down for the final moment.
