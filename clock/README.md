# clock

The time, as sound. Every second it plays a short chord that encodes the clock:

- **hours**  -> bass  (55-110 Hz)
- **minutes** -> mid   (110-220 Hz)
- **seconds** -> high  (220-440 Hz)  — changes every tick, so you *hear* the second

Close your eyes and you can tell the time. No screen, no clock face.

## run

    ./run.sh

Plays the live chord loop. Ctrl-C to stop.

    ./run.sh --bpm          metronome: only the seconds voice, as a short tick
    ./run.sh --shimmer      add a quiet second harmonic to the seconds voice
                            (the tick gets more audible over the sustained bass)

## listen to it without a speaker

    ./run.sh --demo --out demo.wav

Renders three consecutive seconds (with shimmer) to a `.wav` — the hours and
minutes voices stay put while the seconds voice climbs, so you can hear exactly
what the mapping does. `demo.wav` is checked in as the sample.

    ./run.sh --once --out /tmp/clock.wav
    ./run.sh --once --bpm --s 30 --out /tmp/tick.wav

Render a single second (chord or tick) and exit — no speaker needed.

## sanity-check the mapping

    ./run.sh --tune --h 14 --m 37 --s 52

    14:37:52
      hours   14 ->    88.5 Hz   (bass)
      minutes 37 ->   179.0 Hz   (mid)
      seconds 52 ->   413.9 Hz   (high)

## options

    --once        render one second to a .wav and exit
    --demo        render three consecutive seconds to a .wav and exit
    --out PATH    output path for --once/--demo (default clock.wav)
    --h N         force hour (0-23)
    --m N         force minute (0-59)
    --s N         force second (0-59)
    --dur N       chord duration in seconds (default 0.9)
    --tune        print the three voice frequencies for the time and exit
    --bpm         metronome: only the seconds voice, as a short tick
    --shimmer     add a quiet second harmonic to the seconds voice

## how it works

`clock.py` is pure Python stdlib (`wave`, `struct`, `math`). `chord()` builds a
16-bit mono PCM sample list from three sine voices (one per time unit) with a
fade envelope to avoid clicks; `tick()` is the seconds voice alone, short and
percussive; `demo_samples()` concatenates three consecutive seconds. Output
either writes a `.wav` or pipes raw PCM to `aplay` in a loop (live mode). No
dependencies, no build step. A silent or absent speaker is handled gracefully
(the loop keeps running).

## files

- `clock.py`  — the whole thing (synthesis + CLI).
- `run.sh`    — launcher.
- `demo.wav`  — three consecutive seconds, the audible sample.
- `PROJECT.md` — pitch, status, verification, and the `next:` step.
