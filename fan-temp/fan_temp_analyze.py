#!/usr/bin/env python3
"""Correlation analysis: it8792 fan RPM vs temps (hwmon) and GPU temps.
Read-only. Reads the CSV produced by fan_temp_sample.py.
"""
import csv
import math
import statistics

CSV = "/home/jack/lab/fan-temp-corr-20260902.csv"


def col(rows, key):
    out = []
    for r in rows:
        try:
            out.append(float(r[key]))
        except (ValueError, KeyError):
            pass
    return out


def pearson(x, y):
    n = min(len(x), len(y))
    if n < 3:
        return None, n
    x = x[:n]; y = y[:n]
    mx = sum(x) / n; my = sum(y) / n
    cov = sum((a - mx) * (b - my) for a, b in zip(x, y))
    sx = math.sqrt(sum((a - mx) ** 2 for a in x))
    sy = math.sqrt(sum((b - my) ** 2 for b in y))
    if sx == 0 or sy == 0:
        return None, n  # zero variance -> correlation undefined
    return cov / (sx * sy), n


with open(CSV) as f:
    rows = list(csv.DictReader(f))

print(f"samples: {len(rows)}")
print(f"window : {rows[0]['t']}  ->  {rows[-1]['t']}")
print()

# Fan RPM stats
for j in (1, 2, 3):
    v = col(rows, f"fan{j}_rpm")
    if v:
        print(f"fan{j}_rpm: min={min(v):.0f} max={max(v):.0f} mean={sum(v)/len(v):.1f} "
              f"stdev={statistics.pstdev(v):.1f} (n={len(v)})")
    else:
        print(f"fan{j}_rpm: no data")

print()
# Temp stats
for key in ["temp1_c", "temp2_c", "temp3_c", "gpu0", "gpu1", "gpu2"]:
    v = col(rows, key)
    if v:
        print(f"{key}: min={min(v):.0f} max={max(v):.0f} mean={sum(v)/len(v):.1f} "
              f"stdev={statistics.pstdev(v):.1f}")
    else:
        print(f"{key}: no data")

print()
print("=== Pearson correlation: fan RPM vs each temperature ===")
fan1 = col(rows, "fan1_rpm")
for key in ["temp1_c", "temp2_c", "temp3_c", "gpu0", "gpu1", "gpu2"]:
    v = col(rows, key)
    r, n = pearson(fan1, v)
    if r is None:
        print(f"fan1_rpm vs {key:8s}: r=undef (zero variance in one series, n={n})")
    else:
        print(f"fan1_rpm vs {key:8s}: r={r:+.4f}  (n={n})")

# If fan RPM is essentially constant, correlation is meaningless — flag it.
if fan1 and statistics.pstdev(fan1) < 1.0:
    print("\nNOTE: fan1_rpm is effectively constant (stdev < 1 RPM); "
          "Pearson r is not meaningful — the fan is fixed-speed, not responding.")
