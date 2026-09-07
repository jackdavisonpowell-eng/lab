---
slug: poise
title: poise
kind: web-static
status: done
port: 8134
blurb: ART-1100 balance playground
tile: screenshot.png
built: 2026-09-06
verified: 2026-09-07
worth: yes — maps to the C2 assignment
palette: (not recorded — this one was built while the skill still mandated amber)
---
      to read the balance of a real picture (maps straight onto the C2 assignment);
      then a one-line caption generator from the lookbook template.

# Pitch

A tiny canvas toy for ART-1100's **Balance** concept (Ch 2). Drag shapes onto a
canvas and the whole composition physically **tips under its visual weight** like
a seesaw, with live readouts of **symmetry**, **radial**, **net weight**, and
**tilt** — so you *feel* when it's balanced and can name which of the three formal
types you've made: symmetrical (mirrored masses), asymmetrical (unequal masses that
still resolve), or radial (mass ringing a center point). Visual weight follows the
course rule: size × value (dark weighs more) × saturation. Presets build each type
for you; it's a study aid for the C2 "Design Your Own Balance Artwork" assignment.

# What's here

- `index.html` — single-file app (inline CSS/JS, no deps, no runtime network).
- `run.sh` — serves the dir on 127.0.0.1:8134 via stdlib `http.server`.
- `test_poise.js` — Node harness over the real pure math (27 assertions: weight
  monotonic in size/value/sat; each preset yields its named balance type; empty /
  on-axis / off-center edge cases). Run: `node test_poise.js`.
- `README.md` — how to run and use it, plus what each readout means per Ch 2.
- `screenshot.png` — the running page.

# Verified (2026-09-06)

- `node --check` on the inline script: pass.
- `node test_poise.js`: 27/27 pass.
- Served over `http.server`, loaded in a browser, driven the real UI: all five
  presets produce the correct verdict + readouts (symmetric 0°/100% sym/50-50;
  asymmetric −6.4°/0% sym/82-18; radial 0°/84% radial/50-50; random; clear→EMPTY).
  Dragging the left circle to the right flipped it to ASYMMETRICAL +6.4°/6-94.
  Click-to-add drops a shape and reveals the size/value/sat sliders. Canvas
  pixel-sample shows shapes on screen; zero console JS errors.
