# WIRE — the morning brief, read aloud

A tiny "radio" page. It takes the daily AUTOGOD brief
(`$AUTOGOD_VAULT/Inbox/AUTOGOD brief YYYY-MM-DD.md`) and plays it like a morning
broadcast: a typewriter types the text out word-by-word on a dark amber screen
while the browser's speech synthesis reads it aloud. If a **Northern English**
voice is installed it uses that; otherwise the best `en-GB` voice; otherwise it
runs in **typewriter-only** mode so it never goes silent.

It's a toy. It's the kind of thing nobody would bother to build — a radio
station that only broadcasts the agent's own daily report.

## Run it

```sh
cd /home/jack/lab/wire
./run.sh
# → http://127.0.0.1:8135/
```

Or by hand: `python3 server.py 8135`. Port **8135** (lab range 8100-8199).
No installs, no npm, stdlib only. Kill it with Ctrl-C or by PID.

## Controls

- **PLAY / PAUSE / STOP** — start, pause/resume, reset the broadcast.
- **SPEED** — 0.6×–1.6×, drives both the voice rate and the typewriter pace.
- **VOICE** — picks the speech voice; ranked Northern-English → en-GB → any en.
  Shows "typewriter only" if the browser has no voices.
- **BRIEF** — tune to any past brief by date (newest first).

## Notes / what I'd add

- The voice is the master clock; the typewriter chases it char-by-char via
  `speechSynthesis` `onboundary` events. If a voice fires no boundaries (some
  headless browsers), it falls back to a fixed chars/sec typewriter so it
  always moves.
- Add a "read only Failed + Patches" mode (the interesting part), or a
  per-line skip button.
- Briefs are read **read-only**; WIRE never writes to the vault.
