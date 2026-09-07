# clock

The time, as sound. Every second it plays a short chord that encodes the clock:

- **hours**  -> bass  (55-110 Hz)
- **minutes** -> mid   (110-220 Hz)
- **seconds** -> high  (220-440 Hz)  — changes every tick, so you *hear* the second

Close your eyes and you can tell the time. No screen, no clock face.

## run

    ./run.sh

Plays the live chord loop. Ctrl-C to stop.

## headless / no speaker

    ./run.sh --once --out /tmp/clock.wav

Renders the current second to a `.wav` and exits — no speaker needed.

## options

    --once        render one second to a .wav and exit
    --out PATH    output path for --once (default clock.wav)
    --h N         force hour (0-23)
    --m N         force minute (0-59)
    --s N         force second (0-59)
    --dur N       chord duration in seconds (default 0.9)

## how it works

`clock.py` is pure Python stdlib (`wave`, `struct`, `math`). `chord()` builds a
16-bit mono PCM sample list from three sine voices (one per time unit) with a
raised-cosine envelope to avoid clicks, then either writes a `.wav` (`--once`)
or pipes raw PCM to `aplay` in a loop (live mode). No dependencies, no build
step. A silent or absent speaker is handled gracefully (the loop keeps running).

## files

- `clock.py`  — the whole thing (synthesis + CLI).
- `run.sh`    — launcher.
- `PROJECT.md` — pitch, status, verification, and the `next:` step.
