---
slug: clock
title: clock
kind: cli
status: **done**
blurb: the time, as sound (chord per second)
tile: 
built: 2026-09-02
verified: 2026-09-07
worth: half — no speaker on thebeast yet
palette: n/a — CLI/audio, no visual surface
show: ./run.sh --demo --out demo.wav  (demo.wav is checked in: three consecutive seconds, seconds voice climbs 413.9 -> 417.6 -> 421.4 Hz)
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
exits (no speaker needed) — that's the headless verification path. `--demo`
renders three consecutive seconds (with shimmer) to a .wav — the checked-in
`demo.wav` is the audible sample. `--tune` prints the three voice frequencies
for the current time. `--bpm` is a metronome: only the seconds voice, as a
short 0.12 s tick. `--shimmer` adds a quiet second harmonic (0.15 amp) to the
seconds voice so the tick is more audible over the sustained bass.

## verified (2026-09-07)
- `--once` renders valid WAVs: 44.1 kHz mono, 0.9 s, full-scale peaks.
- FFT of the steady middle of two adjacent seconds confirms the design:
  hours voice pinned at 88.9 Hz (bass), minutes at 166.7 Hz (mid), and the
  seconds voice shifts 238.9 Hz -> 241.7 Hz as the second ticks 5 -> 6.
- `--tune` prints the mapping (14:37:52 -> 88.5 / 179.0 / 413.9 Hz); matches
  the linear formulas in `voice_freqs()`.
- `--bpm` tick: 0.12 s, 44.1 kHz mono; Goertzel at the expected seconds
  frequency (413.9 Hz for ss=52) shows the design amplitude, control freq at
  ~0.
- `--shimmer`: Goertzel at 2x the seconds frequency (827.8 Hz) shows the
  added harmonic at ~43% of the fundamental, control freq still ~0.
- `--demo` renders 2.85 s (3 x 0.9 + 3 x 0.05 gaps); Goertzel across the three
  chords confirms the seconds voice climbs 413.9 -> 417.6 -> 421.4 Hz while
  the hours/minutes voices stay put.
- Live loop runs; on this headless box `aplay` reports "Host is down" (ALSA
  device idle/unplugged) but the code path is correct and swallows that
  error so the loop never crashes on a silent host.

## next
If resumed: (1) when a speaker is present, verify the live loop by ear and
note whether `--shimmer` is on or off by default; (2) consider a `--scale`
mode that snaps the three voices to a musical scale (e.g. C major pentatonic)
instead of linear Hz — the linear mapping has beats between voices that might
sound rough; (3) a `--loop N` flag to render N seconds to one .wav for
longer demos; (4) if the lab gets a browser-facing project, consider a tiny
Web Audio page that plays the same chord from the client clock (no aplay
needed).
