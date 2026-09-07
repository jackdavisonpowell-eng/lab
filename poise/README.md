# POISE — balance playground

A tiny canvas toy for ART-1100's **Balance** concept (Ch 2). Drag shapes onto a
canvas and watch a live readout of **symmetry**, **radial**, **net weight**, and
**tilt** — the whole composition physically tips under its visual weight, like a
seesaw, so you *feel* when it's balanced.

It's a study aid for the C2 "Design Your Own Balance Artwork" assignment: play
with mass, value (dark weighs more), and placement until you can name which of
the three balance types you've made.

## Run

```
bash run.sh
```

Then open http://127.0.0.1:8134/  (local-only, nothing leaves the page).

## Use

- **Click empty canvas** to drop a shape with the current brush (circle / square /
  triangle / diamond / bar). **Drag** any shape to move it.
- **Select** a shape to edit its size, value (darkness), and saturation with the
  sliders. Dark + saturated shapes weigh more.
- **Presets** build each balance type for you: *Symmetric* (mirrored masses),
  *Asymmetric* (one big dark mass counterweighted by small light ones), *Radial*
  (masses ringing a center point). *Random* scatters shapes. *Clear* wipes.

## What the readouts mean (ART-1100 Ch 2)

- **Tilt** — the seesaw. Center of visual mass vs. the frame center. 0° = even.
- **Symmetry** — how much mass is mirrored across the vertical axis. High =
  *symmetrical (formal) balance*: stable, calm, static.
- **Radial** — how evenly mass radiates from the center point. High = *radial
  balance*: focused, organic.
- **Net weight** — the left/right mass split, the counterweight balance.
- **Verdict** — SYMMETRICAL / ASYMMETRICAL / RADIAL / TIPPING, the type you've made.
  *Asymmetrical (informal) balance* is the "one large dark shape vs. several small
  light ones that still resolve" case — low symmetry, near-zero tilt.

## What I'd add

- A "photo mode" that overlays your own image and lets you drop weight markers on
  it to read the balance of a real picture (maps straight onto the assignment).
- Export the composition as an SVG to paste into a caption.
- A "caption generator" that writes the template line from the lookbook:
  "<type> balance — <where the weight is> is counterweighted by <what balances it>."
