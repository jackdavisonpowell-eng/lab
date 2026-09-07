#!/usr/bin/env python3
"""Significance + lag + load-transition analysis for fan-temp correlation."""
import csv
import math

CSV = "/home/jack/lab/fan-temp-corr-20260902.csv"


def col(rows, key):
    return [float(r[key]) for r in rows if r.get(key, "").strip() != ""]


def pearson(x, y):
    n = min(len(x), len(y))
    x, y = x[:n], y[:n]
    mx = sum(x) / n; my = sum(y) / n
    cov = sum((a - mx) * (b - my) for a, b in zip(x, y))
    sx = math.sqrt(sum((a - mx) ** 2 for a in x))
    sy = math.sqrt(sum((b - my) ** 2 for b in y))
    if sx == 0 or sy == 0:
        return None, n
    r = cov / (sx * sy)
    # t-test for significance of r
    if abs(r) >= 1:
        return r, n, float("inf")
    t = r * math.sqrt((n - 2) / (1 - r * r))
    return r, n, t


with open(CSV) as f:
    rows = list(csv.DictReader(f))

fan1 = col(rows, "fan1_rpm")
print("=== Significance (t-statistic; |t|>2.86 ~ p<0.01 for n=20) ===")
for key in ["temp1_c", "gpu0", "gpu2"]:
    v = col(rows, key)
    res = pearson(fan1, v)
    if res[0] is None:
        print(f"fan1 vs {key:8s}: r=undef")
    else:
        r, n, t = res
        print(f"fan1 vs {key:8s}: r={r:+.4f}  t={t:+.3f}  (n={n})")

print()
print("=== Load-transition structure (V100 gpu0 went hot->cool mid-window) ===")
# Split at the sample where gpu0 first drops below 60 (load ended)
gpu0 = col(rows, "gpu0")
split = next((i for i, t in enumerate(gpu0) if t < 60), len(gpu0))
hot = [f for f, g in zip(fan1, gpu0) if g >= 60]
cool = [f for f, g in zip(fan1, gpu0) if g < 60]
if hot and cool:
    mh = sum(hot) / len(hot); mc = sum(cool) / len(cool)
    print(f"hot phase  (gpu0>=60C, n={len(hot)}): fan mean={mh:.1f} RPM")
    print(f"cool phase (gpu0<60C,  n={len(cool)}): fan mean={mc:.1f} RPM")
    print(f"delta = {mc - mh:+.1f} RPM  "
          f"({(mc - mh) / mh * 100:+.2f}% of hot mean)")
    print(f"gpu0 hot mean={sum(g for g in gpu0 if g >= 60)/len([g for g in gpu0 if g>=60]):.1f}C "
          f"cool mean={sum(g for g in gpu0 if g < 60)/len([g for g in gpu0 if g<60]):.1f}C")

print()
print("=== Lag check: does fan lead/lag temp by 1 sample (30s)? ===")
for key in ["gpu0", "temp1_c"]:
    v = col(rows, key)
    # fan[t] vs temp[t-1] (fan responds to prior temp)
    r_lead, n, t_lead = pearson(fan1[1:], v[:-1])
    # fan[t] vs temp[t+1]
    r_lag, n, t_lag = pearson(fan1[:-1], v[1:])
    def fmt(x):
        return "undef" if x is None else f"{x:+.3f}"
    print(f"fan vs {key}: r(fan[t],temp[t-1])={fmt(r_lead)}  "
          f"r(fan[t],temp[t+1])={fmt(r_lag)}")

print()
print("=== Tach jitter: fan1 unique values ===")
from collections import Counter
print(Counter(fan1))
print(f"range={max(fan1)-min(fan1)} RPM over mean {sum(fan1)/len(fan1):.1f} "
      f"= {(max(fan1)-min(fan1))/(sum(fan1)/len(fan1))*100:.2f}%")
