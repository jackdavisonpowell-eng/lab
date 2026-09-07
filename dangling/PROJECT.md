---
slug: dangling
title: dangling
kind: cli
status: done
blurb: text adventure inside thebeast
tile: 
built: 2026-09-04
verified: 2026-09-07
worth: yes — unique
palette: (not recorded — this one was built while the skill still mandated amber)
---
# DANGLING


## pitch
DANGLING is a terminal text adventure set inside thebeast. You are a leaked
object — allocated, never freed — a dangling reference that escaped into the
machine. The garbage collector waits at the EXIT. To be freed you crawl through
the beast's GPUs and services, and at every refcount door you must prove you
belong by stating a **true fact about thebeast**. Rooms are real (the i7-5820K,
the V100, the two P100s, FRIDAY's live brain, autogod's own llama-server, the
projector wall, the night lane) and every riddle is a real, verifiable fact from
the thebeast map — CPU model, GPU indices, service ports, the 200W governor, the
76C thermal-slowdown point, the fixed-speed shroud fan, the 3.8 night brain, the
08:00 hand-back. Single Python stdlib file, no installs, no network, no port.
It's the game nobody would bother to build: a dungeon crawler whose dungeons are
the machine you're running on, and whose keys are facts about it.

## how it runs
`./run.sh` → `python3 game.py`. One file. Rooms are a small graph; each edge is a
refcount door with a riddle + accepted answers + a hint. Type `go <room>` to
approach a door, then type the fact (or `answer <fact>` / `hint`). Reach the
EXIT and the GC reclaims you. `map` renders the whole beast from above with
visited/unseen state.

## verified (2026-09-04)
Ran a full winning path via piped stdin:
VOID→CPU (i7-5820k)→V100 (0)→PWR (200)→P100A (fixed)→P100B (two)→NIGHT (3.8)
→EXIT (08:00) — ended "F R E E D", rooms 8/11, steps 7, wrong 0, final score 160,
clean exit 0. Map renders all 11 rooms. Bare-typed facts auto-answer a pending
door. `NO_COLOR=1` strips ANSI when piped.

## next
If resumed: add a `live` mode — the `look` on each GPU room reads the *current*
nvidia-smi temp/power/util and weaves it into the description so the beast is
the real beast at that moment (read-only, no load). Then an `inventory` of
"facts you've proven" that doubles as a checklist of what you know about the
machine. Then a hard mode where wrong answers cost a "reference" and you can
dangle (die) if you run out.
