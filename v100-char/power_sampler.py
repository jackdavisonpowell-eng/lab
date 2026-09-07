#!/usr/bin/env python3
"""Sample V100 (gpu 0) power/clock/temp/throttle under live decode load.
Read-only: nvidia-smi queries only. Runs ~60s, one row per 0.3s."""
import subprocess, time, sys

DUR = float(sys.argv[1]) if len(sys.argv) > 1 else 60.0
OUT = sys.argv[2] if len(sys.argv) > 2 else "/tmp/v100_power.csv"

Q = "--query-gpu=power.draw,clocks.sm,temperature.gpu,utilization.gpu"
THR = "--query-gpu=clocks_event_reasons.active"

def q(args):
    try:
        return subprocess.run(["nvidia-smi", "-i", "0"] + args + ["--format=csv,noheader,nounits"],
                              capture_output=True, text=True, timeout=5).stdout.strip()
    except Exception as e:
        return f"ERR {e}"

rows = []
t0 = time.time()
with open(OUT, "w") as f:
    f.write("t,power_w,sm_mhz,temp_c,util_pct,throttle\n")
    while time.time() - t0 < DUR:
        p = q(["--query-gpu=power.draw,clocks.sm,temperature.gpu,utilization.gpu"])
        th = q(["--query-gpu=clocks_event_reasons.active"])
        parts = [x.strip() for x in p.split(",")]
        if len(parts) == 4:
            f.write(f"{time.time()-t0:.1f},{parts[0]},{parts[1]},{parts[2]},{parts[3]},{th.replace(',', ';')}\n")
            f.flush()
        time.sleep(0.3)

# summary
import statistics
data = [l.split(",") for l in open(OUT).read().splitlines()[1:] if len(l.split(",")) >= 5]
pw = [float(x[1]) for x in data if x[1].replace('.','',1).isdigit()]
sm = [int(x[2]) for x in data if x[2].isdigit()]
ut = [int(x[4]) for x in data if x[4].isdigit()]
th_active = [x[5] for x in data if x[5] and x[5] != "Not Active"]
print(f"samples={len(data)}")
print(f"power_w: min={min(pw):.1f} med={statistics.median(pw):.1f} max={max(pw):.1f}")
print(f"sm_mhz:  min={min(sm)} med={int(statistics.median(sm))} max={max(sm)}")
print(f"util_pct:min={min(ut)} med={int(statistics.median(ut))} max={max(ut)}")
print(f"throttle_active_events={len(th_active)}")
for t in sorted(set(th_active)):
    print("  THROTTLE:", t)
