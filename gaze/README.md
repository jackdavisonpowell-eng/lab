# gaze

A pixel-art FRIDAY face for the Pi's display. One self-contained HTML file,
no dependencies, no build.

It idles — blinks on a random cadence, breathes (slow 1px bob + amber glow
pulse) — and drifts between twelve mood states. The mood comes from the URL,
so the Pi just points a browser at it; a poller (or FRIDAY herself) flips it.

## Run

```
cd /home/jack/lab/gaze && sh run.sh
# → http://127.0.0.1:8122/
```

`GAZE_PORT=8123 sh run.sh` to use a different port. Kill it with Ctrl-C (or
kill the `http.server` PID).

## Moods

idle · listening · thinking · speaking · happy · sad · alert · surprised ·
sleepy · focus · error · offline

Each mood sets eyes / brows / mouth / glow. `speaking` animates the mouth,
`error` glitches the eyes, `sleepy` half-closes them.

## Driving it

- **URL query** — the Pi-friendly way:
  - `?mood=happy` — pin a mood (stops auto-drift).
  - `?poll=<url>` — poll a URL every 2s for the live mood. The URL may return
    plain text (`happy`) or JSON (`{"mood":"happy"}`). Fetch errors keep the
    current mood. **The endpoint must be same-origin OR send
    `Access-Control-Allow-Origin`** — a cross-origin fetch without it fails
    silently and the face holds its last mood.
- **Keyboard** (on the page): ←/→ step mood, space toggles auto-drift, b forces
  a blink, 1–9/0 jump to a mood directly.
- **In-page JS** — `window.FRIDAY_FACE`:
  - `FRIDAY_FACE.setMood("sad")`
  - `FRIDAY_FACE.getMood()`
  - `FRIDAY_FACE.moods` — the list
  - `FRIDAY_FACE.blink()`
  - `FRIDAY_FACE.setAuto(true)` — resume auto-drift

## What it is under the hood

A 24×24 grid. `buildFace` fills a head silhouette (per-row column spans),
`drawEyes`/`drawBrows`/`drawMouth` stamp features per mood, a breathing bob
shifts the whole grid ±1px, and `blit` paints it to a `<canvas>` with an amber
`shadowBlur` glow scaled by the mood's intensity. The canvas is scaled up with
`image-rendering: pixelated` for the chunky look.

## What I'd add

- **Look-at-pointer**: in idle, offset the pupils toward the cursor so the face
  follows you.
- **Pi poller**: a tiny script that reads FRIDAY's live state (wake / speech)
  from `friday.server` and feeds it to `?poll=` so the face mirrors her.
- **Audio-reactive**: feed mouth open/close from an amplitude if the Pi has
  audio in.
