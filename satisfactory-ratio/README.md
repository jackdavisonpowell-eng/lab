---
name: satisfactory-ratio
description: Satisfactory Phase 4 / Tier 7 production-ratio calculator — pick a target item + rate, get machine counts and base-resource demand.
tags: [autogod, lab]
---

# RATIO

A Satisfactory **production-ratio calculator** for Phase 4 / Tier 7 recipes.
Pick a target item and a production rate (items/min). RATIO walks the full
recipe tree and reports:

- **Production lines** — how many of each machine you must run (exact ratio; round up).
- **Base-resource demand** — how much ore / concrete / petroleum the whole line
  consumes per minute, after fully expanding every intermediate item.
- **Unknown gaps** — items whose recipe I haven't hardcoded, flagged so you know
  where the chain breaks.

## Run

```
cd /home/jack/lab/satisfactory-ratio
./run.sh          # → http://127.0.0.1:8131/
```

Single HTML file, no installs, no network. Local-only.

## What's hardcoded

**Known recipes** (sure of these): iron plate, copper plate, steel ingot, coal
coke, concrete, wire, screw, plastic, rubber, polymer, reinforced iron plate,
steel beam, modular frame, electric motor, **conveyor belt Mk.4**, **conveyor
belt Mk.5**.

**Base resources** (mined, no recipe): iron ore, copper ore, coal, limestone,
silicon, quartz, petroleum, salt, bauxite, catalyst.

**Unknown** (deliberate gaps): alclad aluminum sheet, encased industrial beam,
and anything deeper. Add a recipe to the `RECIPES` object in `index.html` to
close a gap.

## How the math works

A machine at 1× makes `60 / cycle_time` items per minute. For a target `T` at
rate `R`, the solver computes `machines[T] = R / capacity(T)`, then for each
ingredient `I` of `T` recurses with `need(I) = (R / out(T)) * in(T, I)`. Base
resources accumulate their `need`; unknown items land in the gaps table.

## What I'd add next

- Real Tier 7 recipes (alclad aluminum sheet, encased industrial beam) from the
  wiki so the Mk.5 chain resolves fully.
- Overclock / underclock multipliers per machine.
- Power draw per machine (W), summed.
- A "closest whole-machine" suggestion and a total cost in base ore.
