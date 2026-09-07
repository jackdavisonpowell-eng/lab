#!/usr/bin/env python3
"""
clock — the time, as sound.

Every second it synthesizes a short chord whose three voices encode the clock:

    hours   -> low  voice  (bass)
    minutes -> mid  voice
    seconds -> high voice  (this one changes every tick, so you HEAR the second)

No clock, no screen: close your eyes and you can tell the time.

Pure Python stdlib (wave + struct + math) for synthesis, piped to `aplay`.
`--once` renders a single second to a .wav file (no speaker needed) so the
thing can be verified headless.
"""

import argparse
import math
import struct
import subprocess
import sys
import time
import wave

SR = 44100  # sample rate


def _clip(v):
    if v > 32767:
        return 32767
    if v < -32768:
        return -32768
    return v


def _add(a, b):
    """Add two 16-bit PCM sample lists element-wise with clipping."""
    n = min(len(a), len(b))
    return [_clip(a[i] + b[i]) for i in range(n)]


def _scale(buf, factor):
    return [_clip(int(v * factor)) for v in buf]


def chord(hh, mm, ss, dur=0.9, sr=SR):
    """Build the 16-bit PCM sample list for the given clock time.

    Three sine voices:
        hours   (0-23) -> 55..110 Hz   (bass)
        minutes (0-59) -> 110..220 Hz  (mid)
        seconds (0-59) -> 220..440 Hz  (high, changes each tick)
    A raised-cosine-ish envelope avoids clicks.
    """
    fh = 55.0 + (110.0 - 55.0) * (hh / 23.0)
    fm = 110.0 + (220.0 - 110.0) * (mm / 59.0)
    fs = 220.0 + (440.0 - 220.0) * (ss / 59.0)

    n = int(sr * dur)
    # envelope: fade in first 10%, fade out last 10%
    env = [1.0] * n
    for i in range(n):
        t = i / n
        if t < 0.10:
            env[i] = t / 0.10
        elif t > 0.90:
            env[i] = (1.0 - t) / 0.10

    def voiced(freq, amp):
        out = [0] * n
        phase = 0.0
        step = 2.0 * math.pi * freq / sr
        for i in range(n):
            out[i] = _clip(int(32767 * amp * env[i] * math.sin(phase)))
            phase += step
        return out

    mix = voiced(fh, 0.50)            # hours bass
    mix = _add(mix, voiced(fm, 0.40))  # minutes mid
    mix = _add(mix, voiced(fs, 0.35))  # seconds high
    return mix


def _pack(samples):
    return struct.pack("<%dh" % len(samples), *samples)


def render_wav(path, hh, mm, ss, dur=0.9):
    data = _pack(chord(hh, mm, ss, dur))
    with wave.open(path, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(data)
    return path


def play_pcm(samples):
    """Pipe raw 16-bit mono PCM to aplay. A silent/absent speaker is fine."""
    try:
        p = subprocess.Popen(
            ["aplay", "-q", "-f", "S16_LE", "-r", str(SR), "-c", "1", "-"],
            stdin=subprocess.PIPE,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        p.stdin.write(_pack(samples))
        p.stdin.close()
        p.wait(timeout=5)
    except (OSError, subprocess.TimeoutExpired):
        pass


def main():
    ap = argparse.ArgumentParser(description="the time, as sound")
    ap.add_argument("--once", action="store_true",
                    help="render the current second to a .wav and exit (no speaker)")
    ap.add_argument("--out", default="clock.wav", help="output path for --once")
    ap.add_argument("--h", type=int, help="force hour (0-23)")
    ap.add_argument("--m", type=int, help="force minute (0-59)")
    ap.add_argument("--s", type=int, help="force second (0-59)")
    ap.add_argument("--dur", type=float, default=0.9, help="chord duration seconds")
    args = ap.parse_args()

    now = time.localtime()
    hh = args.h if args.h is not None else now.tm_hour
    mm = args.m if args.m is not None else now.tm_min
    ss = args.s if args.s is not None else now.tm_sec

    if args.once:
        render_wav(args.out, hh, mm, ss, args.dur)
        print(f"wrote {args.out}  ({hh:02d}:{mm:02d}:{ss:02d})")
        return 0

    print(f"clock — playing {time.strftime('%H:%M:%S')} as a chord. Ctrl-C to stop.")
    try:
        while True:
            t = time.localtime()
            play_pcm(chord(t.tm_hour, t.tm_min, t.tm_sec, args.dur))
            time.sleep(max(0.05, 1.0 - args.dur))
    except KeyboardInterrupt:
        print("\nstopped.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
