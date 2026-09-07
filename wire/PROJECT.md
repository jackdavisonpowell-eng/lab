---
slug: wire
title: wire
kind: web-server
status: done
port: 8135
blurb: morning brief as a radio broadcast
tile:
built: 2026-09-07
verified: 2026-09-07
worth: yes — eats the real brief
palette: (not recorded — this one was built while the skill still mandated amber)
---
## Pitch

The morning brief is a wall of markdown you scroll past. WIRE turns it into a
radio broadcast: a typewriter on a dark screen types the brief out word by word,
and the browser's speech synthesis reads it aloud — a Northern English voice if
one is installed, otherwise the best en-GB voice, otherwise a typewriter-only
mode so the page never goes silent. White/amber monotone, italic monospace
masthead, an ON AIR lamp, a progress bar, and a date picker to tune back to any
past brief. The brief as a morning radio station, not a document.

## How it works

- `server.py` — stdlib `ThreadingHTTPServer`. Serves `/` (index.html),
  `/briefs` (JSON list, newest first), `/brief?date=YYYY-MM-DD` (JSON text).
  Briefs are read **read-only** from `$AUTOGOD_VAULT/Inbox/AUTOGOD brief <date>.md`.
- `index.html` — single file, inline CSS/JS. Two clocks: a **voice clock**
  (driven by `speechSynthesis` `onboundary` char events — the master) and a
  **typewriter clock** that chases it char-by-char. When no voice is available
  (or fires no boundaries) it falls back to a pure typewriter at a fixed
  chars/sec, so it always moves. Voice ranking: `northern` in the name →
  `en-GB` → any `en-`.
- Markdown is stripped to speakable text (headings, `[[wikilinks]]` with alias,
  bold, code, blockquote) before the typewriter lays it out.

## Verified

- `node --check` on the inline script: clean.
- Node harness (23 checks) over the pure fns + the real 09-07 brief: all pass
  (strip/offsets/voice-ranking/line-class + "every brief line strips to
  consistent word offsets", 542 words / 3166 chars).
- Browser drive: PLAY → typewriter types (words reveal, one word amber-highlighted
  mid-sentence, progress bar advances, lamp TYPEWRITER/ON AIR); STOP → resets to
  STANDBY; date picker → reloads a different brief (09-06 = 1204 words).
- `run.sh` from a clean shell: page 200, `/briefs` lists 6, dated `/brief` serves.
- Port 8135 confirmed free after kill.

## Files

- `PROJECT.md` — this file
- `README.md` — what it is, how to run
- `run.sh` — `python3 server.py 8135`
- `server.py` — stdlib HTTP server
- `index.html` — the radio page
