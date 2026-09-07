---
slug: villeneuve
title: villeneuve
kind: web-static
status: done
port: 8132
blurb: one-button cinematic shot generator
tile: 
built: 2026-09-06
verified: 2026-09-07
worth: yes — photography class fuel
palette: (not recorded — this one was built while the skill still mandated amber)
---
# Villeneuve — shot generator

A one-button cinematic composition generator in the spirit of Denis
Villeneuve: brutalist mass, fog, silence, scale that swallows the subject.
Each "shot" is a card — scale, location, atmosphere, subject, light,
composition, a silence instruction, and a director's note. 5% of shots are
MASTER shots (amber frame): the ones that end the film. For photography or
art class: hit space, hold the frame, shoot it.

show: `cd /home/jack/lab/villeneuve && ./run.sh` → http://127.0.0.1:8132
(screenshot: shot.png in this dir — shot 0008, dark card, amber note)

Verified 2026-09-06: node --check clean; 1000-shot Node harness (fields from
pools, hold 6–30s, master 4.2%, toText 10 lines); live browser drive —
CUT button 0001→0007, Space key 0007→0008, holds in range. Server killed,
port 8132 confirmed free.

next: add a visible "hold" timer bar that drains over the shot's hold
seconds (pure CSS/JS, no deps) so the frame teaches you to wait; then add
share-card export (self-contained SVG 1080x1080, kicker pattern).
