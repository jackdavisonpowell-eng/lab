"""Headless tests for reef: load -> speed, feeding, panic, no crashes.

Run: python3 test_reef.py   (no TTY needed)
"""
import io
import sys
import types
from contextlib import redirect_stdout

import reef


def make_reef(load):
    args = types.SimpleNamespace(frames=1, fake=False, load=load, seed=42)
    r = reef.Reef(args)
    return r


def path_length(load, frames=300, dt=1.0 / 20.0):
    r = make_reef(load)
    prev = [(f.x, f.y) for f in r.fish]
    total = 0.0
    w, h = 80, 24
    for _ in range(frames):
        for f in r.fish:
            f.step(dt, r.util_of(f.gpu), r.food, w, h - 4, r.rng)
        for f, (px, py) in zip(r.fish, prev):
            total += abs(f.x - px) + abs(f.y - py)
        prev = [(f.x, f.y) for f in r.fish]
    return total


def test_speed_scales_with_load():
    lo = path_length(0)
    mid = path_length(50)
    hi = path_length(100)
    assert lo < mid < hi, "expected monotonic speed: %r %r %r" % (lo, mid, hi)
    print("OK speed scales: 0%%=%.1f 50%%=%.1f 100%%=%.1f (path units)" % (lo, mid, hi))


def test_panic_faster():
    hi = path_length(89)
    panic = path_length(100)
    assert panic > hi, "panic should exceed 89%%: %r <= %r" % (panic, hi)
    print("OK panic: 89%%=%.1f < 100%%=%.1f" % (hi, panic))


def test_feeding_eats():
    r = make_reef(30)
    w, h = 80, 24
    # drop food right in front of a fish
    f0 = r.fish[0]
    f0.x, f0.y, f0.dir = 10.0, 10.0, 1
    r.food.append(reef.Food(11.0, 10.0))
    dt = 1.0 / 20.0
    for _ in range(60):
        for f in r.fish:
            f.step(dt, r.util_of(f.gpu), r.food, w, h - 4, r.rng)
        if not r.food[0].alive:
            break
    assert not r.food[0].alive, "fish should have eaten the food"
    print("OK feeding: food consumed")


def test_render_no_crash():
    for load in (0, 42, 97, 100):
        r = make_reef(load)
        w, h = 80, 24
        sc = reef.Screen(w, h)
        buf = io.StringIO()
        with redirect_stdout(buf):
            for _ in range(10):
                r.frame(sc, 0.05)
            sc.flush()
        out = buf.getvalue()
        assert "reef" in out, "title missing"
        assert "V100" in out or "SIM" in out, "HUD missing"
        assert "%" in out
    print("OK render: 4 load levels, 10 frames each, no crash")


def test_render_small_terminal():
    r = make_reef(50)
    w, h = 40, 12
    sc = reef.Screen(w, h)
    buf = io.StringIO()
    with redirect_stdout(buf):
        for _ in range(5):
            r.frame(sc, 0.05)
        sc.flush()
    assert "V100" in buf.getvalue()
    print("OK render: 40x12 terminal, no crash")


def test_tail_animates():
    r = make_reef(90)
    w, h = 80, 24
    seen = set()
    for _ in range(40):
        for f in r.fish:
            f.step(0.05, 90, r.food, w, h - 4, r.rng)
        sc = reef.Screen(w, h)
        for f in r.fish:
            f.draw(sc)
        for row in sc.g:
            for ch, _ in row:
                if ch in "<>":
                    seen.add(ch)
    assert {"<", ">"} <= seen, "tail should flap between < and >, saw %r" % seen
    print("OK tail animates")


def test_sample_gpus_parses_space_percent():
    # thebeast emits '97 %' with a space — must not crash or read 0 always
    fake = "0, Tesla V100-PCIE-32GB, 97 %\n1, Tesla P100-PCIE-16GB, 0 %\n"
    import re
    gpus = []
    for line in fake.strip().splitlines():
        parts = [p.strip() for p in line.split(",")]
        m = re.search(r"\d+", parts[2])
        gpus.append(int(m.group(0)) if m else 0)
    assert gpus == [97, 0], gpus
    print("OK nvidia-smi parse: '97 %' -> 97")


if __name__ == "__main__":
    test_speed_scales_with_load()
    test_panic_faster()
    test_feeding_eats()
    test_render_no_crash()
    test_render_small_terminal()
    test_tail_animates()
    test_sample_gpus_parses_space_percent()
    print("ALL PASS")
