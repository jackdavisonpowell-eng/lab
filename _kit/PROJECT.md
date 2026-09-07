---
slug: _kit
title: _kit
kind: web-static
status: done
port: 8110
blurb: the shared skin every lab web project starts from
tile:
built: 2026-09-07
verified: 2026-09-07
worth: the foundation — not a stranger-facing showpiece, but every future web project starts from this, so it compounds
palette: ember amber #ffb000 — the ONE amber, named, after six were invented across the fleet
---
port: 8110

Pitch: Twenty-one web projects each re-derived the same four things by hand —
a slightly-different amber, the italic display type and letter-spacing, the
DPR-correct canvas boilerplate, and the keydown handler. `_kit` is those
pieces, extracted once and made copy-paste ready: `base.css` (the skin,
overridable via :root vars), `snippets.md` (canvas / keydown / the 1080x1080
share-card SVG renderer from kicker / clipboard / data-fetch), a `run.sh`
template, and a live `index.html` demo of every class. Colour is still the
project's to choose (record it in `palette:`); the structure is not.

Run: `./run.sh` → http://127.0.0.1:8110/  (the kit's own demo)

Verified 2026-09-07:
- kit demo page served on 8110, canvas live (lit 0.0346), space-pause
  toggles running→paused→running, zero JS errors (browser console clean).
- rebuilt `rain` (smallest project, 4948→4520 bytes, −428) on the kit.
- proof of same behaviour: served visible text OLD vs NEW is byte-identical
  (['rain','rain ·','…','titles · caught','0','hover freezes a stream',
  'click catches the title','space pauses']); JS diff is exactly one line
  (`getElementById('hud')` → `querySelector('.hud')`, same element);
  effective CSS for #hud/#help/#caught resolves to the same values
  (the one real bug found and fixed: the `#help`→`.help` id/class mismatch
  that would have dropped the help text back to gray).
- rain rebuilt page: canvas live (lit ~0.33, 887 titles loaded), space-pause
  dims .hud (""→"0.35"→"1"), click-catch works (nc 0→1, ledger 0→1),
  zero JS errors.
- ports 8190/8191/8192 (test) and 8110 (kit) confirmed free after kill.

show: README.md

next: none
