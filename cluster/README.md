# cluster

A GR86-style digital gauge cluster as a single web page. Open it and it revs
itself.

## what it is
- A big glowing tach dial (0-8000, redline at 7300) with a sweeping needle.
- A giant italic gear readout (N/1-6) on the right.
- A km/h number, coolant + fuel bars, a lap timer, and a boot/telemetry line.
- A GR86-style shift lamp that comes on at 5800, pulses at 6500, and strobes
  at 7000.

All of it is driven by fake telemetry. There is no car and no CAN bus — a
demo mode plays a scripted drive so the page is alive the second it loads.

## how to run
```
cd /home/jack/lab/cluster
./run.sh            # -> http://127.0.0.1:8124/
```
Then open http://127.0.0.1:8124/ . No build step, no framework, no network
beyond localhost. `run.sh` is just `python3 -m http.server 8124 --bind
127.0.0.1`.

## controls
- **DEMO** (default): it drives itself — IDLE → LAUNCH → CRUISE → PUNCH →
  BRAKE (rev-match blip on the downshift) → COAST, looping.
- **M** (or click the mode chip): switch to MANUAL.
- **SPACE / W**: hold to rev.
- **1-6** (or ↑ / ↓): shift.
- **S / X**: brake.
- **R**: reset to neutral idle.

## files
- `index.html` — everything (inline CSS + JS, one canvas + DOM HUD).
- `run.sh` — serves the dir on 127.0.0.1:8124.
- `PROJECT.md` — pitch + status + `next:` for a cold start.

## what I'd add next
- A subtle scanline / vignette pass for more cockpit grit.
- A fuel needle that actually tracks the bar, and a coolant redline warning.
- Real GR86 shift-light hysteresis (it should stay lit a beat past the blink
  band) and a "REV MATCH" flash tied to the demo downshift.
- Optional: a tiny WebAudio whine whose pitch follows rpm (off by default).
