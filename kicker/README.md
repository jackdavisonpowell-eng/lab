# KICKER — anime quote machine

50 original anime-style quotes (no copyrighted lines) in five styles, each
rendered as a 1080×1080 share card. Local-only, one HTML file + one JSON file,
stdlib Python to serve.

## Run

```
sh run.sh          # serves http://127.0.0.1:8130/
sh run.sh 8135     # different port
```

Open http://127.0.0.1:8130/ .

## Use

- NEXT (or Space/Enter) — random quote
- 1–5 or the chips — filter by style (TITAN / BEND / PORTAL / DUNE / NEON)
- C — copy the quote to clipboard
- S or SAVE CARD — download the card as a self-contained SVG
  (open it in any browser, drop it in a document, done)

## Files

- `index.html` — the whole app: UI + `renderCard()` (the share-card renderer)
- `quotes.json` — the 50 quotes + style list (edit to add your own)
- `run.sh` — `python3 -m http.server` on 127.0.0.1:8130
- `sample-card-01.svg` — an example card (quote #01, TITAN)

## How the card works

`renderCard(quote, idx, total)` returns a self-contained SVG string:
word-wrap at 34 chars/line, auto font-shrink for long quotes (54→30px floor),
HTML-escaped text, per-style accent color. The same string is injected into
the page AND written to the .svg download, so screen and file never drift.

## What I'd add

- Quote of the day (deterministic from the date)
- Deep-link `?q=17` to reopen a specific card without the server
- PNG export (needs a rasterizer; the SVG is the portable format)
- More quotes — `quotes.json` is the only file to touch
