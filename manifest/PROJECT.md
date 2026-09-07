---
slug: manifest
title: manifest
kind: web-static
status: done
port: 8139
blurb: dorm move-in manifest + roommate diff
tile: screenshot.png
built: 2026-09-04
verified: 2026-09-07
worth: mostly spent — move-in is over
palette: (not recorded — this one was built while the skill still mandated amber)
---
# MANIFEST — the cargo manifest for your dorm move-in

A dorm move-in packing checklist that isn't just a list. Items live in **holds**
(categories: Bedding, Kitchen, Cleaning, Electronics, Furniture, Toiletries,
Decor, Misc), each with a **have / need / buy** state and live tallies. The
killer feature is the **roommate diff**: export your manifest as dumb text, text
it to your roommate, paste theirs back in, and it flags **duplicates** (you're
both buying a trash can), **gaps** (standard dorm kit nobody's got), and the
clean **only-you / only-them** split.

The export/import format is round-trippable: `# MANIFEST <owner>` /
`## <hold>` / `[have|need|buy] item`. It's deliberately plain text so it
survives a group chat.

## Build log (2026-09-04)
- Single-file `index.html` (inline CSS/JS, no deps). State in `localStorage`
  (`manifest.v1`). Pure logic: `toManifest` / `parseManifest` / `diff` / `norm`.
- Proven: 35-check Node harness on the pure functions (round-trip, tolerant
  parse, diff overlap/gaps/disjointness invariants) + live DOM drive in a
  browser (load sample, add item, flip state, export, diff — all numbers read
  back correct). Server killed by PID, port 8128 verified free.
- Taste: white/amber monotone, big italic numbers, tribal hold headers, no
  pastel. One word: MANIFEST.

## Files
- `index.html` — the whole app
- `run.sh` — `python3 -m http.server 8128 --bind 127.0.0.1`
- `README.md` — what it is, how to run, what to add next
