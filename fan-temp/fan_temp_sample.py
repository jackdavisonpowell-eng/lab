#!/usr/bin/env python3
"""Sample it8792 fan RPMs + temps and GPU temps every 30s. Read-only."""
import csv
import json
import subprocess
import time
from datetime import datetime, timezone

HW = "/sys/class/hwmon/hwmon2"
N = 20          # samples
INTERVAL = 30   # seconds


def read(path):
    try:
        with open(path) as f:
            return f.read().strip()
    except Exception:
        return ""


def gpu_temps():
    try:
        out = subprocess.run(
            ["nvidia-smi", "--query-gpu=index,temperature.gpu",
             "--format=csv,noheader,nounits"],
            capture_output=True, text=True, timeout=10)
        rows = [r.split(",") for r in out.stdout.strip().splitlines() if r.strip()]
        return {f"gpu{i}": int(t) for i, t in rows}
    except Exception:
        return {}


out_path = "/home/jack/lab/fan-temp-corr-20260902.csv"
rows = []
t0 = time.time()
for i in range(N):
    ts = datetime.now(timezone.utc).isoformat()
    row = {"t": ts, "i": i}
    for j in (1, 2, 3):
        row[f"fan{j}_rpm"] = read(f"{HW}/fan{j}_input")
        row[f"temp{j}_c"] = read(f"{HW}/temp{j}_input")
    row.update({k: v for k, v in gpu_temps().items()})
    rows.append(row)
    if i < N - 1:
        time.sleep(INTERVAL)

with open(out_path, "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    w.writeheader()
    w.writerows(rows)

print(json.dumps({"rows": len(rows), "elapsed_s": round(time.time() - t0, 1),
                  "path": out_path}))
