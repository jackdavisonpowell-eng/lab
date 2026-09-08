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
thing can be verified headless. `--tune` prints the three voice frequencies
for the current time so the mapping can be sanity-checked by ear. `--bpm`
switches to metronome mode: only the seconds voice, as a short tick.
"""

import argparse
import math
import struct
import subprocess
import sys
import time
import wave

SR = 44100  # sample rate
TICK_DUR = 0.12  # metronome tick length


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


def voice_freqs(hh, mm, ss):
    """The three voice frequencies (Hz) for a clock time."""
    fh = 55.0 + (110.0 - 55.0) * (hh / 23.0)
    fm = 110.0 + (220.0 - 110.0) * (mm / 59.0)
    fs = 220.0 + (440.0 - 220.0) * (ss / 59.0)
    return fh, fm, fs


def _env(n, fade=0.10):
    """Linear fade-in/out envelope (fraction `fade` at each end)."""
    env = [1.0] * n
    for i in range(n):
        t = i / n
        if t < fade:
            env[i] = t / fade
        elif t > 1.0 - fade:
            env[i] = (1.0 - t) / (1.0 - fade)
    return env


def _tone(freq, amp, n, env, sr=SR):
    """One sine voice, 16-bit PCM sample list."""
    out = [0] * n
    phase = 0.0
    step = 2.0 * math.pi * freq / sr
    for i in range(n):
        out[i] = _clip(int(32767 * amp * env[i] * math.sin(phase)))
        phase += step
    return out


def chord(hh, mm, ss, dur=0.9, sr=SR, shimmer=False):
    """Build the 16-bit PCM sample list for the given clock time.

    Three sine voices:
        hours   (0-23) -> 55..110 Hz   (bass)
        minutes (0-59) -> 110..220 Hz  (mid)
        seconds (0-59) -> 220..440 Hz  (high, changes each tick)
    A fade envelope avoids clicks. With `shimmer`, a quiet second harmonic
    of the seconds voice is added so the tick is more audible over the
    sustained bass.
    """
    fh, fm, fs = voice_freqs(hh, mm, ss)
    n = int(sr * dur)
    env = _env(n)
    mix = _tone(fh, 0.50, n, env, sr)            # hours bass
    mix = _add(mix, _tone(fm, 0.40, n, env, sr))  # minutes mid
    mix = _add(mix, _tone(fs, 0.35, n, env, sr))  # seconds high
    if shimmer:
        mix = _add(mix, _tone(2.0 * fs, 0.15, n, env, sr))
    return mix


def tick(ss, dur=TICK_DUR, sr=SR, shimmer=False):
    """Metronome tick: only the seconds voice, short and percussive."""
    fs = voice_freqs(0, 0, ss)[2]
    n = int(sr * dur)
    env = _env(n, fade=0.25)
    out = _tone(fs, 0.60, n, env, sr)
    if shimmer:
        out = _add(out, _tone(2.0 * fs, 0.15, n, env, sr))
    return out


def tune(hh, mm, ss):
    """Print the three voice frequencies for the given time."""
    fh, fm, fs = voice_freqs(hh, mm, ss)
    print(f"{hh:02d}:{mm:02d}:{ss:02d}")
    print(f"  hours   {hh:2d} -> {fh:7.1f} Hz   (bass)")
    print(f"  minutes {mm:2d} -> {fm:7.1f} Hz   (mid)")
    print(f"  seconds {ss:2d} -> {fs:7.1f} Hz   (high)")


def demo_samples(hh, mm, ss, dur=0.9, sr=SR):
    """Three consecutive seconds as chords (with shimmer), gap between them.

    The hours/minutes voices stay put while the seconds voice climbs —
    a self-describing sample of what clock sounds like.
    """
    gap = [0] * int(sr * 0.05)
    out = []
    for i in range(3):
        out.extend(chord(hh, mm, (ss + i) % 60, dur, sr=sr, shimmer=True))
        out.extend(gap)
    return out


def _pack(samples):
    return struct.pack("<%dh" % len(samples), *samples)


def render_wav(path, samples):
    data = _pack(samples)
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
    ap.add_argument("--tune", action="store_true",
                    help="print the three voice frequencies for the time and exit")
    ap.add_argument("--bpm", action="store_true",
                    help="metronome: only the seconds voice, as a short tick")
    ap.add_argument("--shimmer", action="store_true",
                    help="add a quiet second harmonic to the seconds voice")
    ap.add_argument("--demo", action="store_true",
                    help="render three consecutive seconds (with shimmer) to a .wav")
    args = ap.parse_args()

    now = time.localtime()
    hh = args.h if args.h is not None else now.tm_hour
    mm = args.m if args.m is not None else now.tm_min
    ss = args.s if args.s is not None else now.tm_sec

    if args.tune:
        tune(hh, mm, ss)
        return 0

    if args.demo:
        render_wav(args.out, demo_samples(hh, mm, ss, args.dur))
        print(f"wrote {args.out}  (demo: {hh:02d}:{mm:02d}:{ss:02d} +2s)")
        return 0

    if args.once:
        if args.bpm:
            samples = tick(ss, shimmer=args.shimmer)
        else:
            samples = chord(hh, mm, ss, args.dur, shimmer=args.shimmer)
        render_wav(args.out, samples)
        print(f"wrote {args.out}  ({hh:02d}:{mm:02d}:{ss:02d})")
        return 0

    if args.bpm:
        print(f"clock — metronome, {time.strftime('%H:%M:%S')}. Ctrl-C to stop.")
        try:
            while True:
                t = time.localtime()
                play_pcm(tick(t.tm_sec, shimmer=args.shimmer))
                time.sleep(max(0.05, 1.0 - TICK_DUR))
        except KeyboardInterrupt:
            print("\nstopped.")
        return 0

    print(f"clock — playing {time.strftime('%H:%M:%S')} as a chord. Ctrl-C to stop.")
    try:
        while True:
            t = time.localtime()
            play_pcm(chord(t.tm_hour, t.tm_min, t.tm_sec, args.dur,
                           shimmer=args.shimmer))
            time.sleep(max(0.05, 1.0 - args.dur))
    except KeyboardInterrupt:
        print("\nstopped.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
