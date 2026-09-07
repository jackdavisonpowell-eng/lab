# lapboard

A sim-racing lap timer and delta display for a second screen. Big italic
numbers, amber on near-black, no pastel. It reads `laps.json` and shows:

- **LIVE** — the current lap's elapsed time, huge, ticking.
- **DELTA** — live delta vs the best lap, green when ahead, red when behind,
  recomputed every 150 ms from the best lap's cumulative-time samples.
- **BEST / LAST** — the fastest and most recent completed laps.
- **STRIP** — a full-lap cumulative-time chart: the best lap as a thin amber
  ghost line, the live (or last) lap drawn over it in green/red, with a
  moving dot so you can see *where* on the lap you're gaining or losing.

## run

    ./run.sh            # http://127.0.0.1:8125/
    ./run.sh 8130       # or any port

Open the page on the second screen (or `x11vnc` it / mirror it). Keys:

    space   start / finish a lap
    b       drop the best lap (reset the reference)
    r       reset all laps

## data

`laps.json` next to `server.py`:

    [ {"t": 161.095, "d": [0.0, 0.5, ..., 161.095]}, ... ]

`t` = total lap time in seconds, `d` = cumulative-time samples (seconds) for
delta matching. The server re-reads the file whenever its mtime changes, so an
external exporter (sim telemetry script, phone, whatever) can just write the
file — last lap wins, no restart needed. A finished live lap is appended with
a 2-point `d` (start/finish) — enough for total-time deltas; a real exporter
supplies the full sample curve.

## what I'd add

- **Sector splits** — `d` samples tagged with sector boundaries, three delta
  columns instead of one.
- **Telemetry ingest** — a WebSocket or `/telemetry` endpoint so a sim
  exporter (e.g. via a MoTeC/Motec-style UDP bridge) streams live samples and
  the strip draws the real lap shape, not a straight line.
- **Ghost audio** — a soft tick when you cross the best lap's time at each
  sample (ahead = high tick, behind = low).
- **Multi-car** — two live laps side by side (split-screen vs a friend).
