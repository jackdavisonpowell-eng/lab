# reef

A terminal ASCII aquarium where the fish **are** the GPUs. The tank is thebeast:
the V100 swims as a big bright fish, the two P100s as small amber ones.
`nvidia-smi` is polled once a second (read-only) and **more GPU load = faster
fish** — at 90%+ a school panics and darts. Bubbles rise faster under load,
seaweed sways harder, and a per-GPU util bar sits along the bottom.

## Run

```
./run.sh            # live thebeast GPUs
```

Keys: `q` quit, `f` feed (drops pellets; fish chase and eat them).

Needs a real TTY for the best experience (alternate screen + cbreak input).
Piped output still renders, just without key handling.

## Flags

```
--frames N   exit after N frames (smoke test)
--fake       three simulated GPUs on sine waves (no nvidia-smi needed)
--load N     pin every GPU to N% (see the panic at 90+)
--seed N     deterministic fish positions
```

Examples:

```
./run.sh --load 100    # full panic
./run.sh --fake        # demo on a laptop
```

## Tests

```
python3 test_reef.py
```

Headless, no TTY: asserts speed scales monotonically with load, panic beats
89%, feeding is actually eaten, rendering survives 40x12 terminals and all
load levels, and the tail flaps.

## What I'd add next

- Fish size by VRAM, species by architecture (V100 = eel, P100 = guppy).
- A "feed" that only works when a GPU is idle — the busy fish ignore pellets.
- Temperature as water color (dim blue → red at 85C+).
