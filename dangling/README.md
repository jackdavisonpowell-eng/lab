---
name: dangling
description: "DANGLING — a terminal text adventure set inside thebeast; rooms are the GPUs and services, every door is a refcount you satisfy by stating a real fact about the machine."
tags: [autogod, lab, game]
---

# DANGLING

A text adventure set inside thebeast. You are a leaked object — allocated,
never freed — a dangling reference that escaped into the machine. The garbage
collector waits at the EXIT. To be freed you crawl through the beast's GPUs and
services, and at every refcount door you must prove you belong by stating a
**true fact about thebeast**.

Rooms are real: the i7-5820K, the V100 (your card, 200W cap), the two P100s,
FRIDAY's live brain, autogod's own llama-server, the projector wall, the night
lane. Every riddle is a real, verifiable fact from the thebeast map — CPU model,
GPU indices, service ports, the 200W governor, the 76C thermal-slowdown point,
the fixed-speed shroud fan, the 3.8 night brain, the 08:00 hand-back.

## run it

    cd /home/jack/lab/dangling
    ./run.sh

No installs, no network, no port. It's a single Python stdlib file.

## commands

    look        describe the room you're in
    map         show the whole beast from above
    go <room>   move toward a room (may trigger a refcount door)
    answer <f>  answer the door that's asking (or just type the fact)
    hint        buy a hint (-10)
    score       your standing
    help        this
    quit        leave (dangling, unfreed)

Score: +10 per new room, -5 per wrong answer, -10 per hint. Reach the EXIT and
the garbage collector reclaims you — that's the win.

## what I'd add

- A `live` mode: the `look` on each GPU room reads the *current* nvidia-smi
  temp/power/util and weaves it into the description, so the beast is the real
  beast at that moment.
- An `inventory` of "facts you've proven" that doubles as a checklist of what
  you know about the machine.
- A harder mode where wrong answers cost a "reference" and you can dangle (die)
  if you run out.
