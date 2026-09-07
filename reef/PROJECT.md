---
slug: reef
title: reef
kind: cli
status: done
blurb: ASCII aquarium, fish = GPU load
tile: 
built: 2026-09-05
verified: 2026-09-07
worth: yes — 30 seconds of joy
palette: (not recorded — this one was built while the skill still mandated amber)
---
A terminal ASCII aquarium where the fish are thebeast's GPUs. nvidia-smi is
polled once a second; more load means faster fish — the V100 is a big bright
fish, the P100s are small amber ones, and at 90%+ a school panics and darts.
Bubbles and seaweed react to load too, with a per-GPU util bar along the
bottom. `f` drops pellets the fish chase and eat. Stdlib only, no port, no
deps. Verified: test_reef.py passes (speed scales 35x from 0%→100%, feeding,
panic, 40x12 render).

next: add species-by-architecture (V100 = eel, P100 = guppy) and
temperature-driven water color (dim blue → red at 85C+).
