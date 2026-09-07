---
slug: seam
title: seam
kind: web-static
status: done
port: 8127
blurb: jeans cutting-layout machine
tile: screenshot.png
built: 2026-09-03
verified: 2026-09-07
worth: yes — real utility
palette: (not recorded — this one was built while the skill still mandated amber)
---
A cutting layout machine for custom jeans. Enter waist, hip, inseam, outseam,
leg opening, ease and fabric width; it drafts every pattern piece (front/back
legs as trapezoids, yoke, pockets, waistband, fly, cuffs), shelf-packs them
onto a real-width fabric strip with a grainline, and reports yardage from the
ACTUAL packed layout — not a lookup table. White/amber on black, print view
for the cutting table.

Verified 2026-09-03: node --check clean; draft+pack run in a Node harness
across 5 input sets (30/44/58 in, big/small, cuffs on/off) with no overflow or
within-shelf overlap; real form driven in-browser (fabric width 44→30 in, hip
38→40) and yardage/viewBox updated correctly (2.75 yd @44 in, 4 yd @30 in).
4 stacked shelf bands, all 13 labels inside their pieces.

next: add a fabric-swatch picker (denim oz + color) that tints the SVG, and a
"cut list" export (one line per piece, with a scissors count) so Jack can cut
from the printout without the table.
