---
name: horse-tinder-readme
description: "How to run and play Horse Tinder, the procedural horse-swiping toy."
tags: [autogod, lab]
---

# HORSE TINDER

Swipe left/right on procedurally generated horses. Single HTML file, no
dependencies, no network.

## Run

    cd /home/jack/lab/horse-tinder
    ./run.sh

Then open http://127.0.0.1:8123/ . The server binds 127.0.0.1 only. Kill it
with `pkill -f "http.server 8123"` when you're done.

## Play

- Drag the card left or right, or press ArrowLeft / ArrowRight, or click
  NOPE / MATCH.
- Your horse (top-left) is generated once per session: it has a dominant
  stat and an "into" stat.
- A candidate matches when its dominant stat is yours, plus a small random
  chance. The match screen shows both horses and why it worked.
- "best night" is your high score of matches in one session, saved in
  localStorage (per browser).

## Files

- `index.html` — everything (markup, CSS, JS, SVG generator)
- `run.sh` — python3 http.server on 127.0.0.1:8123

## What I'd add

- A shareable match ticket (download the match screen as SVG).
- A "he remembered your bio" line on the match screen.
- Rarity tiers for stat distributions (a 10/10 in two stats is a unicorn).
- Sound: a single low thud on NOPE, a single bell on MATCH.
