# seam.

A cutting layout machine for custom jeans.

Enter your measurements — waist, hip, inseam, outseam, leg opening, ease —
pick a fabric width (30/44/58 in) and whether you want turned cuffs. It
drafts the pattern pieces from the measurements, lays them out on a strip of
fabric at real width (grainline included), and tells you how many yards to
buy, computed from the actual packed layout.

## Run

    sh run.sh

Then open http://127.0.0.1:8127 . Local only; nothing is saved.

## What it does

- Pattern drafting: rise = outseam − inseam (front −1.5, back +0.5), leg
  width from hip/4 + ease, 3/4 in seam allowance added to cut sizes.
- Shelf packing: pieces run with the grain; the waistband may rotate across
  the width if it is too long to fit lengthwise.
- Yardage = packed fabric length, rounded up to the nearest 1/4 yd.
- Print view (button or Ctrl+P) hides the form and gives a clean layout +
  piece table for the cutting table.

## What it is not

An estimate from formulas, not a commercial pattern. No dart placement, no
gusset curves, no pocket bag. Buy 1/4 yd extra if the denim is patterned.

## Ideas not built yet

- Fabric swatch picker (oz + color) that tints the layout.
- Cut-list export (one line per piece, with a scissors count).
- A "second pair" toggle — two pairs on one bolt, yardage for both.
