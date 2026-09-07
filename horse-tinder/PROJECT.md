---
slug: horse-tinder
title: horse-tinder
kind: web-static
status: done
port: 8123
blurb: swipe on procedurally generated horses
tile: screenshot.png
built: 2026-09-02
verified: 2026-09-07
worth: yes — 5 minutes of fun
palette: (not recorded — this one was built while the skill still mandated amber)
---
Pitch: Tinder, but the candidates are horses that do not exist. Each one is
generated on the fly — a jagged geometric head (SVG, seeded per horse so the
match screen can show the same face), a name like VELKEL, a title ("the
Unbothered", "of the Third Field"), six stats (HOOVES, FLAIR, CHAOS, GROOM,
VIBE, MOO), an italic one-line bio, and what it's "looking for". You swipe
left (NOPE) or right (MATCH) with drag, arrow keys, or buttons. Your own
horse is generated once per session with a dominant stat and an "into" stat;
matches happen when the candidate's dominant stat is one of yours, plus a
small random chance. The match screen shows both horses, the reason, and a
running count. Local high score of matches per night persists in localStorage.
White/amber monotone, Impact-italic, cut corners, no rounded anything.

next: polish pass — verify drag/swipe feel on a real screen, tune match
probability, add a "he remembered your bio" line to the match screen, and
consider a shareable match ticket (SVG download).
