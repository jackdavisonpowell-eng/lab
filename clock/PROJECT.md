---
slug: clock
title: clock
kind: cli
status: **building**
blurb: the time, as sound (chord per second)
tile: 
built: 
verified: 2026-09-07
worth: half — no speaker on thebeast yet
palette: (not recorded — this one was built while the skill still mandated amber)
---
# clock


## pitch
clock is the time, as sound. Every second it synthesizes a short chord whose
three voices encode the clock: hours -> bass (55-110 Hz), minutes -> mid
(110-220 Hz), seconds -> high (220-440 Hz). The seconds voice changes every
tick, so you can *hear* the second go by. No clock, no screen: close your eyes
and you can tell the time. Pure Python stdlib (wave/struct/math) for synthesis,
piped to `aplay`. The thing nobody bothers to build: a clock you listen to.

## how it runs
`./run.sh` runs `clock.py`, which in a loop renders the current second's chord
and pipes 16-bit mono PCM to `aplay`. `--once` renders one second to a .wav and
exits (no speaker needed) — that's the headless verification path.

## verified (2026-09-02)
- `--once` renders valid WAVs: 44.1 kHz mono, 0.9 s, full-scale peaks.
- FFT of the steady middle of two adjacent seconds confirms the design:
  hours voice pinned at 88.9 Hz (bass), minutes at 166.7 Hz (mid), and the
  seconds voice shifts 238.9 Hz -> 241.7 Hz as the second ticks 5 -> 6.
- Live loop runs; on this headless box `aplay` reports "Host is down" (ALSA
  device idle/unplugged) but the code path is correct and now swallows that
  error so the loop never crashes on a silent host.

## next
If resumed: (1) add a `--tune` mode that prints the three voice frequencies for
the current time so Jack can sanity-check the mapping by ear; (2) a `--bpm`
"metronome" variant that only plays the seconds voice as a tick (pure time-
keeping, no chord); (3) an optional second-harmonic shimmer on the seconds voice
so the tick is more audible over the sustained bass. (4) When a speaker is
present, verify the live loop by ear and drop a short demo .wav into the folder.
