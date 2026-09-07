# ABYSS

A Subnautica progress tracker. Local-only, private, no deps.

## What it is
Track your Subnautica run from one page:

- **DEPTH** — set your max depth (meters). A vertical gauge plots it against the
  real zone bands (Sunset 0–200m → Deep 200–700m → Abyss 700–1500m → Dunes
  1500–2000m → Trench 2000–3000m → Lost River 3000m+). It reads the water
  pressure in atmospheres (≈1 atm per 10 m) and names the leviathan lurking at
  that depth.
- **BLUEPRINTS** — check off the blueprints you've found, grouped by
  Vehicles / Weapons / Tools, with per-group and overall counts.
- **BASE MODULES** — check off the base modules you've built (Structure / Systems).
- **Add your own** — type a blueprint or module name and hit ADD to extend either
  list; it saves with the rest.

Everything persists in the browser's `localStorage` (key `abyss-save-v1`). Reset
wipes it.

## How to run
```
cd /home/jack/lab/abyss
./run.sh
```
Then open http://127.0.0.1:8128/ in a browser. (run.sh starts a local
`python3 -m http.server` bound to 127.0.0.1 on port 8128; Ctrl-C to stop.)

## What I'd add next
- A progress ring / completion percentage for the whole run.
- A leviathan-encounter counter (log Ghost/Reaper/Sea Dragon sightings).
- Import/export the save as JSON (so a run survives a browser wipe).
- Editable blueprint/base lists persisted to the same save.
