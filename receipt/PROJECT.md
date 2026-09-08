---
slug: receipt
title: receipt
kind: showpiece
status: done
port: 8102
blurb: type a sentence, get billed for every letter at its scrabble value
tile: screenshot.png
built: 2026-09-07
verified: 2026-09-07
worth: the artifact is the post — a thermal receipt for "hello world" totals a real, verifiable number, and strangers screenshot receipts. it is too small to be a product and too absurd to be a demo, which is exactly why it shares.
palette: warm near-black counter (#141310), aged thermal cream paper (#f6f1e7), soft-black ink (#20201d), one receipt-red accent (#d64524) for prices/total/rare letters — red reads as "price/sale" and is deliberately NOT the house amber.
because: the Hacker News reader who screenshots the artifact, not the page
---

# receipt

Type any sentence and it prints a thermal-paper receipt that prices **every
letter** by its Scrabble value, itemized word by word, then adds a **7% rarity
surcharge** and a running **TOTAL DUE** that updates live on every keystroke.

Nobody builds a page whose only job is to bill you for your own words. It is
too small to be a product and too absurd to be a demo — but the screenshot of a
receipt for "hello world" is the thing that gets shared. The store is **THE
WORD BUREAU**, an official-looking pricing office for your own language.

Rare letters (J Q X Z, and the 4-point W K) drive the surcharge, so they are
flagged in the itemization — you can *see* what is making you pay.

## how it runs
- Single self-contained `index.html` (inline CSS + JS, no backend, no fetch,
  no deps). Runs from GitHub Pages as-is at
  `https://jackdavisonpowell-eng.github.io/lab/receipt/`.
- Local: `./run.sh` (serves on 8102, honours `$LAB_PORT`).
- No build step. Open the file directly or serve it.

## what I verified
- Served on 8102 via `./run.sh`; `curl` returns the 12185-byte page, correct title.
- DOM readback (headless shell, `--virtual-time-budget=2500`): default "hello world"
  → HELLO $8.00 + WORLD $9.00 (W flagged rare) = subtotal **$17.00**, 7% rarity
  surcharge **$1.19**, **TOTAL DUE $18.19**; 10 letters, 1 rare. Exact.
- Live typing: "JQXZ" → $36.00 base, all 4 letters rare, $38.52 total; empty input
  → $0.00 + "— awaiting words —". Recomputes on every keystroke.
- `browser_console`: **0 JS errors, 0 console messages**. Paper bg = rgb(246,241,231)
  (cream), big number = rgb(214,69,36) (receipt-red), display/mono fonts correct.
- Layout: `main` grid = `697px 460px`, machine + paper side by side (not stacked),
  paper visible 460×478. Screenshot written to `screenshot.png` (160KB).
- Standalone: single `index.html`, inline CSS+JS, no fetch, no deps — runs from
  GitHub Pages as-is. No vault paths, no personal data.

## show:
- `./run.sh` → http://127.0.0.1:8102  (or open `index.html` directly)
- Published at https://jackdavisonpowell-eng.github.io/lab/receipt/
- Screenshot: `screenshot.png` (receipt for "hello world" totaling $18.19)

## next:
- (done) — resume here if a future run continues: add a one-click share-card
  PNG export (1080px) and a print stylesheet so the receipt is the whole page.
