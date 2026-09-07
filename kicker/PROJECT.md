---
slug: kicker
title: kicker
kind: web-static
status: done
port: 8130
blurb: anime quote machine, 1080×1080 SVG share cards
tile: screenshot.png
built: 2026-09-05
verified: 2026-09-07
worth: yes — same bloodline as villeneuve
palette: (not recorded — this one was built while the skill still mandated amber)
---
# KICKER — anime quote machine

An anime quote machine for Jack's taste: 50 original quotes (no copyrighted
lines) in five styles — TITAN (Attack on Titan weight), BEND (Avatar
bending-philosophy), PORTAL (Rick-and-Morty cosmic snark), DUNE (desert
mystique), NEON (Blade Runner noir). Each quote renders as a 1080×1080
share card: dark, amber, italic serif quote, tribal chevrons, corner notches,
big italic number. One renderer (`renderCard`) drives both the on-screen card
and the downloadable self-contained SVG file — the card you save is the card
you see. Space = next, 1–5 = style filter, C = copy, S = save.

Built 2026-09-05. Verified: Node harness over all 50 quotes (wrap/escape/
auto-shrink invariants, 0 fails), live browser drive (next/filter/keyboard/
save all close the loop), canvas pixel-sample proves the card paints.

next: add a "quote of the day" (deterministic pick from the date) and a
share-URL that deep-links to a specific quote (?q=17) so a card can be
reopened without the server.
