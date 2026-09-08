---
slug: placard
title: placard
kind: showpiece
status: done
port: 8140
blurb: type any object — spoon, key, sock — and it is accessioned as a formal museum placard
tile: screenshot.png
built: 2026-09-08
verified: 2026-09-08
worth: the artifact is the post — a screenshot of "SPOON, c. 1994, found under a cinema seat" is the thing that gets shared. it is too small to be a product and too dry to be a demo, which is exactly why it is worth it.
palette: cool museum dark, deliberately NOT the house amber and NOT receipt's warm cream+orange-red. gallery wall = deep blue-black (#0d1218); the placard = cool bone/ivory (#eef0ea) like a real museum label; ink = near-black (#1b1c1a); the single accent = archival oxblood (#7d2b28) for the accession number and the "found" line — oxblood reads as "catalogue / accession / museum red" and is darker and cooler than receipt's bright #d64524, and it is paired with a COOL label on a blue-black wall (a different object and a different layout: one centred label, not a two-column machine).
because: the stranger who types one word and gets a museum label
---

# placard

Type any object — **spoon, key, sock, a dead battery, your own left shoe** — and
it is accessioned as a formal **museum placard**: a title in caps, a
deterministic **accession number**, a `c.` date, a material,
**"found under a cinema seat,"** dimensions in centimetres, and a **two-line
provenance** in deadpan curatorial prose.

Nobody builds a museum label for a spoon. It is too small to be a product and
too dry to be a demo — but the screenshot of
`SPOON, c. 1994, found under a cinema seat` is the one that gets shared. The
institution is the **DEPARTMENT OF EVERYDAY THINGS**, a museum that has
permanently collected the objects you already own.

Everything on the label is **deterministic from the object you typed** — the
accession number, the date, the material, the find-spot, the dimensions, the
provenance — so the same object always gets the same label (a real museum
would). Nothing leaves the page; there is no backend.

## how it runs
- Single self-contained `index.html` (inline CSS + JS, no backend, no fetch,
  no deps). Runs from GitHub Pages as-is at
  `https://jackdavisonpowell-eng.github.io/lab/placard/`.
- Local: `./run.sh` (serves on 8140, honours `$LAB_PORT`).
- No build step. Open the file directly or serve it.

## what I verified
- Served on 8140 via `./run.sh`; `curl` returns the 18078-byte page, correct title.
- DOM readback (headless shell, `--virtual-time-budget=2500`): default "spoon"
  → **SPOON**, `c. 1994`, stainless steel, 11.2 × 2.4 cm, accession **1994.284.24**,
  "found under a cinema seat", provenance "Recovered from the floor of the Odeon, 1994.
  / Gift of an anonymous seat." Exact.
- Catalog object "key" → brass, 1987, "found in the pocket of a coat it no longer
  opens", 5.1 × 1.6 cm. Generated "left shoe" → 2000, brass, 17.7 × 16.3 cm,
  "found in the glovebox". **Deterministic**: re-typing "left shoe" produced the
  identical label (JSON-equal). Empty input → "—", "found, awaiting an object".
- Palette applied (computed styles): placard bg rgb(238,240,234) ivory, found +
  accession rgb(125,43,40) oxblood, wall rgb(13,18,24) blue-black, title Georgia italic.
- `browser_console`: **0 JS errors, 0 console messages**. Screenshot written to
  `screenshot.png` (156KB, 1600×1000, placard fully in frame).
- Standalone: single `index.html`, inline CSS+JS, no fetch, no deps — runs from
  GitHub Pages as-is. No vault paths, no personal data.

## show:
- `./run.sh` → http://127.0.0.1:8140  (or open `index.html` directly)
- Published at https://jackdavisonpowell-eng.github.io/lab/placard/
- Screenshot: `screenshot.png` (the placard for "spoon")

## next:
- (done) — resume here if a future run continues: add a "print" button + print
  stylesheet (placard only), and a 1080px share-card PNG export so the
  screenshot is one click, not a crop.
