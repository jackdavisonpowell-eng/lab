#!/usr/bin/env python3
"""Controlled power-limit A/B on the autogod brain (:11466, same model/flags).
Runs an identical probe at 200 W and 250 W, samples power/clock/throttle under
each, and ALWAYS restores the limit to 200 W at the end (even on error).
The probe prompt is varied per run (different repeat count) so the KV cache is
cold each time -> measures real prefill + decode, not cache hits.
Read-only on the running system: only nvidia-smi -pl changes, and it's restored.
"""
import json, subprocess, time, urllib.request, sys, statistics

BASE = "http://127.0.0.1:11466/v1/chat/completions"
OUT = "/home/jack/lab/v100-char/ab_results.json"
SAMPLER = "/home/jack/lab/v100-char/power_sampler.py"
RESTORE = 200  # the running config

def set_pl(w):
    subprocess.run(["sudo", "-n", "nvidia-smi", "-i", "0", "-pl", str(w)],
                   capture_output=True, text=True, timeout=10)
    got = subprocess.run(["nvidia-smi", "-i", "0",
                          "--query-gpu=power.limit", "--format=csv,noheader,nounits"],
                         capture_output=True, text=True, timeout=10).stdout.strip()
    print(f"set_pl {w} -> actual {got}")
    return got

def probe(repeat_n):
    sysp = "You are a precise counter. " * repeat_n
    body = {"model": "autogod",
            "messages": [{"role": "system", "content": sysp},
                         {"role": "user", "content": "Count from 1 to 300, one number per line, no other text."}],
            "max_tokens": 300, "temperature": 0.7, "stream": False}
    req = urllib.request.Request(BASE, data=json.dumps(body).encode(),
                                 headers={"Content-Type": "application/json"})
    t0 = time.time()
    with urllib.request.urlopen(req, timeout=180) as r:
        d = json.loads(r.read())
    wall = time.time() - t0
    u = d.get("usage", {})
    return {"prompt_tokens": u.get("prompt_tokens"),
            "completion_tokens": u.get("completion_tokens"),
            "cached_tokens": (u.get("prompt_tokens_details") or {}).get("cached_tokens"),
            "wall_s": round(wall, 3)}

def gpu_temp():
    try:
        return int(subprocess.run(["nvidia-smi", "-i", "0", "--query-gpu=temperature.gpu",
                                   "--format=csv,noheader,nounits"],
                                  capture_output=True, text=True, timeout=5).stdout.strip())
    except Exception:
        return 0

def run_phase(pl, tag, sampler_out):
    print(f"\n===== PHASE {tag} @ {pl} W =====")
    set_pl(pl)
    time.sleep(3)
    # start sampler in background for the duration of the 3 probes
    proc = subprocess.Popen(["python3", SAMPLER, "70", sampler_out])
    time.sleep(2)
    results = []
    for i, rep in enumerate([1200, 1300, 1400]):
        tmp = gpu_temp()
        if pl >= 250 and tmp >= 85:
            print(f"  THERMAL GUARD: {tmp} C >= 85, aborting 250W phase after run{i}")
            break
        r = probe(rep)
        r["run"] = i
        r["temp_before_c"] = tmp
        results.append(r)
        print(f"  run{i} (temp {tmp}C): {r}")
        time.sleep(4)
    proc.wait(timeout=90)
    # read sampler summary
    ssum = subprocess.run(["python3", "-c",
        "import statistics as s;d=[l.split(',') for l in open('%s').read().splitlines()[1:] if len(l.split(','))>=5];pw=[float(x[1]) for x in d if x[1].replace('.','',1).isdigit()];sm=[int(x[2]) for x in d if x[2].isdigit()];th=[x[5] for x in d if x[5] and x[5]!='Not Active'];print(f'power_med={s.median(pw):.1f} power_max={max(pw):.1f} sm_med={int(s.median(sm))} sm_max={max(sm)} throttle_events={len(th)} throttle_types={sorted(set(th))}')" % sampler_out],
        capture_output=True, text=True, timeout=20).stdout.strip()
    print(f"  sampler: {ssum}")
    return {"pl": pl, "tag": tag, "probes": results, "sampler": ssum}

def main():
    out = {}
    try:
        out["phase_200"] = run_phase(200, "200W", "/tmp/ab_200.csv")
        time.sleep(8)  # let clocks/temps settle between phases
        out["phase_250"] = run_phase(250, "250W", "/tmp/ab_250.csv")
    finally:
        print("\n===== RESTORE 200 W =====")
        out["restored_pl"] = set_pl(RESTORE)
        time.sleep(2)
        final = subprocess.run(["nvidia-smi", "-i", "0", "--query-gpu=power.limit,temperature.gpu,clocks.sm",
                                "--format=csv,noheader"], capture_output=True, text=True).stdout.strip()
        out["final_state"] = final
        print("final:", final)
    json.dump(out, open(OUT, "w"), indent=1)
    print(f"\nwrote {OUT}")
    print(json.dumps(out, indent=1))

if __name__ == "__main__":
    main()
