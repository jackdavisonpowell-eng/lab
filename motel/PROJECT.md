---
slug: motel
title: motel
kind: showpiece
status: done
port: 8142
blurb: type a word, it lights up as a neon motel sign — dead letters included
tile: screenshot.png
built: 2026-09-08
verified: 2026-09-08
worth: the screenshot of MOTEL with three letters burnt out is the post; the dead letters are the joke
palette: night-sky blue-black (#04060c) with per-letter neon from six hand-picked two-color schemes; VACANCY is always classic sign red — a motel sign is not a cream receipt or a museum label
because: the stranger who types a word and gets a neon motel sign with the dead letters
---

# motel

One word in, one neon motel sign out. Every letter's on/off state, flicker
timing, and color are drawn from a hash of the word (FNV-1a seed, xorshift per
field), so the same word is the same sign on every machine — a motel always
signs its own name the same way. Beneath the word: VACANCY, a room rate, and
one deadpan note. ~20 common words (motel, hotel, diner, bar, love, friday,
receipt, autogod, ...) get hand-tuned signs — which letters are dead, the rate,
the note — because the prose is the product. Everything else is generated.

The joke is the burnt-out letters: dim, sagging, no glow. A sign with all
letters dead still shows VACANCY and a rate, which is somehow worse.

## How it runs

`./run.sh` — serves the single index.html on port 8142 (honours $LAB_PORT).
No server needed at all: it is one self-contained HTML file that runs from
GitHub Pages as-is at https://jackdavisonpowell-eng.github.io/lab/motel/

## What was verified

- node --check on the inline script
- Node harness over signFor(): determinism (same word twice = JSON-equal),
  normalization (case/whitespace/punctuation), dead indices in range, rate
  bounds, catalogue overrides (motel = dead O/T/E, $12) — 50 words, ALL PASS
- Browser (:8142): computed animationName `sputter`/`neon` running on lit
  letters, dead letters opacity 0.3 + sagged transform, DOM readback
  JSON-equal across re-typing "motel" vs "MOTEL", friday override (dead Y,
  $21), zzz generated sign differs
- Headless screenshot of the default MOTEL sign: lit_frac 0.0255, red_frac
  0.003 (VACANCY) — neon + stars on the night sky, saved as screenshot.png

show: `cd /home/jack/lab/motel && ./run.sh` → http://127.0.0.1:8142, or open
index.html directly (no server needed). Screenshot: screenshot.png

next: done. Possible adds: canvas photo-mode, 60 Hz hum + tick audio, two-word
stacked signs.
