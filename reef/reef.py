#!/usr/bin/env python3
"""reef — a terminal ASCII aquarium where the fish are the GPUs.

More GPU load = faster fish. Samples nvidia-smi once a second (read-only).
Keys: q quit, f feed.
Flags: --frames N (exit after N frames), --fake (sine-wave fake loads),
       --load N (pin every GPU to N%), --seed N.
"""
import argparse
import math
import os
import random
import re
import select
import shutil
import subprocess
import sys
import time

IS_TTY = sys.stdout.isatty()
NO_COLOR = os.environ.get("NO_COLOR") is not None

AMBER = "38;5;215"
BRIGHT = "38;5;222"
DIM = "2"
WHITE = "37"

FPS = 20
FRAME = 1.0 / FPS


def paint(s, color=""):
    if NO_COLOR or not color:
        return s
    return "\x1b[%sm%s\x1b[0m" % (color, s)


def sample_gpus():
    """Read-only nvidia-smi poll. Returns [{'label','util'},...] or None."""
    try:
        out = subprocess.run(
            ["nvidia-smi",
             "--query-gpu=index,name,utilization.gpu",
             "--format=csv,noheader"],
            capture_output=True, text=True, timeout=2).stdout
    except Exception:
        return None
    gpus = []
    for line in out.strip().splitlines():
        parts = [p.strip() for p in line.split(",")]
        if len(parts) < 3:
            continue
        m = re.search(r"[A-Z]\d{3}", parts[1])
        label = m.group(0) if m else parts[1].split("-")[0]
        m = re.search(r"\d+", parts[2])
        util = int(m.group(0)) if m else 0
        gpus.append({"label": label, "util": util})
    return gpus or None


class Screen:
    def __init__(self, w, h):
        self.w, self.h = w, h
        self.g = [[(" ", "")] * w for _ in range(h)]
        self.prev = None

    def put(self, x, y, s, color=""):
        for i, ch in enumerate(s):
            xx = x + i
            if 0 <= y < self.h and 0 <= xx < self.w:
                self.g[y][xx] = (ch, color)
        end = x + len(s)
        if 0 <= y < self.h and 0 <= end < self.w:
            self.g[y][end] = ("\x00", "")

    def flush(self):
        out = []
        if self.prev is None:
            out.append("\x1b[2J\x1b[H")
        for i, row in enumerate(self.g):
            line = colorize(row, self.w)
            if self.prev is None or line != self.prev[i]:
                out.append("\x1b[%d;1H%s" % (i + 1, line))
        if out:
            sys.stdout.write("".join(out))
            sys.stdout.flush()
        self.prev = [colorize(row, self.w) for row in self.g]


def colorize(row, w):
    parts = []
    i, n = 0, len(row)
    while i < n:
        if row[i][0] == "\x00":
            break
        col = row[i][1]
        j = i
        while j < n and row[j][0] != "\x00" and row[j][1] == col:
            j += 1
        seg = "".join(c for c, _ in row[i:j])
        parts.append(paint(seg, col) if col else seg)
        i = j
    return "".join(parts)


class Fish:
    def __init__(self, gpu, big, w, h, rng):
        self.gpu = gpu
        self.big = big
        self.body = "oo" if big else "o"
        self.x = rng.uniform(2, max(3.0, w - 6))
        self.y = rng.uniform(2, max(3.0, h - 6))
        self.dir = rng.choice((1, -1))
        self.vy = rng.uniform(-0.4, 0.4)
        self.tail = 0
        self.tail_t = rng.uniform(0, 0.2)

    def step(self, dt, util, food, w, sand, rng):
        speed = 1.0 + (util / 100.0) * 25.0
        panic = util >= 90
        if panic:
            speed *= 1.6
        target = None
        for f in food:
            if f.alive and abs(f.x - self.x) < 12 and abs(f.y - self.y) < 12:
                target = f
                break
        if target is not None:
            dx = target.x - self.x
            self.dir = 1 if dx >= 0 else -1
            self.x += self.dir * speed * 1.5 * dt
            self.y += (1 if target.y >= self.y else -1) * speed * 0.9 * dt
        else:
            self.x += self.dir * speed * dt
            self.y += self.vy * dt
            if rng.random() < (0.004 if not panic else 0.08):
                self.vy = rng.uniform(-0.5, 0.5) * (3.0 if panic else 1.0)
            if rng.random() < (0.003 if not panic else 0.05):
                self.dir *= -1
        top, bot = 2, sand - 1
        if self.y < top:
            self.y, self.vy = top, abs(self.vy)
        if self.y > bot:
            self.y, self.vy = bot, -abs(self.vy)
        margin = len(self.body) + 1
        if self.x < 1:
            self.x, self.dir = 1.0, 1
        if self.x > w - margin:
            self.x, self.dir = float(w - margin), -1
        self.tail_t += dt * (1.0 + util / 100.0 * 9.0)
        if self.tail_t > 0.11:
            self.tail_t = 0.0
            self.tail ^= 1
        # eat
        mouth_x = self.x + self.dir * (len(self.body) / 2.0)
        for f in food:
            if f.alive and abs(f.x - mouth_x) < 1.6 and abs(f.y - self.y) < 1.2:
                f.alive = False
                f.spark_t = 0.35

    def draw(self, sc):
        y = int(round(self.y))
        x = int(round(self.x))
        if self.dir > 0:
            tail = "<" if self.tail == 0 else "-"
            sc.put(x, y, tail + self.body, BRIGHT if self.big else AMBER)
        else:
            tail = ">" if self.tail == 0 else "-"
            sc.put(x, y, self.body + tail, BRIGHT if self.big else AMBER)


class Bubble:
    def __init__(self, x, y, rng):
        self.x = x
        self.y = y
        self.phase = rng.uniform(0, 6.28)
        self.alive = True

    def step(self, dt, util, t, top):
        self.y -= (2.0 + util / 100.0 * 4.0) * dt
        self.x += math.sin(t * 3 + self.phase) * 0.03
        if self.y <= top:
            self.alive = False

    def draw(self, sc):
        sc.put(int(round(self.x)), int(round(self.y)), "\u00b7", DIM)


class Food:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.alive = True
        self.spark_t = 0.0

    def step(self, dt, sand):
        if self.alive:
            self.y += 1.5 * dt
            if self.y >= sand - 1:
                self.alive = False
        elif self.spark_t > 0:
            self.spark_t -= dt

    def draw(self, sc):
        if self.alive:
            sc.put(int(round(self.x)), int(round(self.y)), "*", AMBER)
        elif self.spark_t > 0:
            sc.put(int(round(self.x)), int(round(self.y)), "+", BRIGHT)


class Reef:
    def __init__(self, args):
        self.args = args
        self.rng = random.Random(args.seed)
        self.t = 0.0
        self._last = None
        self.last_sample = -10.0
        self.gpus = []
        self.fish = []
        self.bubbles = []
        self.food = []
        self.weeds = []
        self.rock_xs = []
        self._sample()
        self._populate()

    def _sample(self):
        if self.args.fake:
            self.gpus = []
            tf = self.t + 0.5
            for i in range(3):
                u = int(50 + 45 * math.sin(tf * (0.3 + 0.07 * i) + 2.1 * i))
                self.gpus.append({"label": "SIM%d" % i, "util": max(0, u)})
        elif self.args.load is not None:
            real = sample_gpus() or []
            if not real:
                real = [{"label": "GPU%d" % i} for i in range(3)]
            self.gpus = [dict(g, util=self.args.load) for g in real]
        else:
            real = sample_gpus()
            self.gpus = real if real else [
                {"label": "SIM0", "util": int(50 + 45 * math.sin(self.t * 0.3))},
                {"label": "SIM1", "util": int(50 + 45 * math.sin(self.t * 0.2 + 2))},
            ]

    def _populate(self):
        for i, g in enumerate(self.gpus):
            big = "V" in g["label"] or "A" in g["label"]
            n = 2
            for _ in range(n):
                self.fish.append(Fish(i, big, 80, 30, self.rng))
        w = shutil.get_terminal_size((80, 24)).columns
        for _ in range(5):
            self.weeds.append({
                "x": self.rng.randint(3, max(4, w - 4)),
                "h": self.rng.randint(3, 6),
                "phase": self.rng.uniform(0, 6.28),
            })
        for _ in range(4):
            self.rock_xs.append(self.rng.randint(2, max(3, w - 3)))

    def util_of(self, i):
        return self.gpus[i]["util"] if i < len(self.gpus) else 0

    def frame(self, sc, dt):
        t = self.t
        w, h = sc.w, sc.h
        n_hud = min(len(self.gpus), 3)
        sand = h - 1 - n_hud
        top = 2
        if sand <= top + 2:
            sand, top = h - 1, 2

        for i, g in enumerate(self.gpus):
            util = g["util"]
            if self.rng.random() < 0.01 + util / 100.0 * 0.12 and len(self.bubbles) < 70:
                self.bubbles.append(Bubble(
                    self.rng.uniform(2, w - 2), float(sand - 1), self.rng))
        for b in self.bubbles:
            b.step(dt, self.util_of(0), t, top)
        self.bubbles = [b for b in self.bubbles if b.alive]
        for f in self.food:
            f.step(dt, sand)
        self.food = [f for f in self.food if f.alive or f.spark_t > 0]
        for fi in self.fish:
            fi.step(dt, self.util_of(fi.gpu), self.food, w, sand, self.rng)

        # --- draw ---
        sc.put(0, 0, paint("reef \u2014 thebeast GPU tank", DIM)
               + "    " + paint("q quit \u00b7 f feed", DIM))
        # sand
        for x in range(w):
            ch = "\u00b7" if x % 2 == 0 else " "
            sc.put(x, sand, ch, DIM)
        for rx in self.rock_xs:
            if 0 <= rx < w - 1:
                sc.put(rx, sand, "_", WHITE)
                sc.put(rx + 1, sand, "_", WHITE)
        # weeds sway harder with load
        amp = 0.4 + self.util_of(0) / 100.0 * 1.6
        freq = 1.0 + self.util_of(0) / 100.0 * 2.0
        for wd in self.weeds:
            for k in range(wd["h"]):
                dx = int(round(math.sin(t * freq + wd["phase"] + k * 0.6) * amp * (k / 3.0 + 0.3)))
                sc.put(wd["x"] + dx, sand - 1 - k, "|", DIM)
        for b in self.bubbles:
            b.draw(sc)
        for f in self.food:
            f.draw(sc)
        for fi in self.fish:
            fi.draw(sc)
        # HUD
        for i, g in enumerate(self.gpus[:n_hud]):
            u = g["util"]
            bar_w = 20
            fill = int(round(u / 100.0 * bar_w))
            bar = "\u2588" * fill + "\u2591" * (bar_w - fill)
            col = BRIGHT if u >= 90 else AMBER
            row = " %-5s [%s] %3d%%" % (g["label"], bar, u)
            sc.put(0, h - n_hud + i, row, col)

    def feed(self, w):
        for _ in range(3):
            self.food.append(Food(self.rng.uniform(3, w - 3), 2.0))

    def run(self):
        old = None
        if IS_TTY:
            import termios
            import tty
            old = termios.tcgetattr(sys.stdin)
            tty.setcbreak(sys.stdin)
        import signal
        stop = {"v": False}

        def _sig(_s, _f):
            stop["v"] = True
        signal.signal(signal.SIGTERM, _sig)
        signal.signal(signal.SIGINT, _sig)
        try:
            sys.stdout.write("\x1b[?1049h\x1b[?25l")
            sys.stdout.flush()
            frame_no = 0
            while not stop["v"]:
                t0 = time.time()
                dt = min(0.1, t0 - (self._last or t0))
                self._last = t0
                self.t += dt
                if self.t - self.last_sample >= 1.0:
                    self.last_sample = self.t
                    self._sample()
                w, h = shutil.get_terminal_size((80, 24))
                sc = Screen(w, h)
                self.frame(sc, dt)
                sc.flush()
                frame_no += 1
                key = poll_key()
                if key == "q":
                    break
                if key == "f":
                    self.feed(w)
                if self.args.frames and frame_no >= self.args.frames:
                    break
                time.sleep(max(0.0, FRAME - (time.time() - t0)))
        finally:
            sys.stdout.write("\x1b[?25l\x1b[0m\x1b[?1049l")
            sys.stdout.flush()
            if old is not None:
                import termios
                termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old)


def poll_key():
    try:
        r, _, _ = select.select([sys.stdin], [], [], 0)
    except Exception:
        return None
    if not r:
        return None
    try:
        data = os.read(0, 64)
    except OSError:
        return "q"
    if not data:
        return "q"
    for b in data:
        ch = chr(b)
        if ch in "qQ" or ch == "\x03":
            return "q"
        if ch == "f":
            return "f"
    return None


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--frames", type=int, default=None)
    ap.add_argument("--fake", action="store_true")
    ap.add_argument("--load", type=int, default=None, metavar="N")
    ap.add_argument("--seed", type=int, default=None)
    args = ap.parse_args()
    if args.load is not None:
        args.load = max(0, min(100, args.load))
    Reef(args).run()


if __name__ == "__main__":
    main()
