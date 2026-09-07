#!/usr/bin/env python3
"""Parse autogod-brain journal for per-task perf: prompt size, prefill t/s,
decode t/s, TTFT proxy (prompt eval time), context depth, wall duration.
Correlate each task to the worker job running at that time (job type).
Outputs JSON + a markdown summary."""
import json, re
from datetime import datetime

BRAIN = "/home/jack/lab/v100-char/brain-journal-24h.log"
WORKER = "/home/jack/lab/v100-char/worker-journal-24h.log"
OUT_JSON = "/home/jack/lab/v100-char/tasks.json"
OUT_MD = "/home/jack/lab/v100-char/per-task.md"

def ts(line):
    m = re.match(r"(\w{3}) (\d{1,2}) (\d{2}):(\d{2}):(\d{2})", line)
    if not m:
        return None
    mon, d, h, mi, s = m.groups()
    return datetime(2026, {"Sep": 9}[mon], int(d), int(h), int(mi), int(s))

# ---- worker job windows
jobs = []
cur = None
for line in open(WORKER):
    t = ts(line)
    if t is None:
        continue
    m = re.search(r"job ([0-9a-f]{12}) \[([a-z-]+)\] (.*)", line)
    if m:
        jid, jtype, desc = m.groups()
        desc = desc.strip()[:100]
        if cur:
            jobs.append(cur)
        cur = {"id": jid, "type": jtype, "desc": desc, "start": t, "end": None}
    m2 = re.search(r"job ([0-9a-f]{12}) -> (\w+)", line)
    if m2 and cur and cur["id"] == m2.group(1):
        cur["end"] = t
        cur["status"] = m2.group(2)
        jobs.append(cur)
        cur = None
if cur:
    jobs.append(cur)

def job_at(t):
    best = None
    for j in jobs:
        if j["start"] and j["start"] <= t:
            if j["end"] and j["end"] < t:
                continue
            if best is None or j["start"] > best["start"]:
                best = j
    return best

# ---- brain tasks
tasks = []
cur = None
re_launch = re.compile(r"launch_slot_: id\s+\d+ \| task (\d+) \| processing task")
re_stop = re.compile(r"stop processing: n_tokens = (\d+)")
re_peval = re.compile(r"prompt eval time =\s+([\d.]+) ms /\s+(\d+) tokens")
re_eval = re.compile(r"eval time =\s+([\d.]+) ms /\s+(\d+) tokens")
re_tg = re.compile(r"n_decoded =\s+(\d+), tg =\s+([\d.]+) t/s")

for line in open(BRAIN):
    t = ts(line)
    if t is None:
        continue
    m = re_launch.search(line)
    if m:
        if cur:
            tasks.append(cur)
        cur = {"task": int(m.group(1)), "start": t, "stop": None,
               "prompt_ms": None, "prompt_tok": None,
               "eval_ms": None, "eval_tok": None,
               "tg_max": None, "n_tokens_stop": None}
        continue
    if cur is None:
        continue
    m = re_stop.search(line)
    if m:
        cur["stop"] = t
        cur["n_tokens_stop"] = int(m.group(1))
        continue
    m = re_peval.search(line)
    if m:
        cur["prompt_ms"] = float(m.group(1))
        cur["prompt_tok"] = int(m.group(2))
        continue
    m = re_eval.search(line)
    if m:
        cur["eval_ms"] = float(m.group(1))
        cur["eval_tok"] = int(m.group(2))
        continue
    m = re_tg.search(line)
    if m:
        tg = float(m.group(2))
        if cur["tg_max"] is None or tg > cur["tg_max"]:
            cur["tg_max"] = tg

if cur:
    tasks.append(cur)

# ---- derive
for k, task in enumerate(tasks):
    nxt = tasks[k+1]["start"] if k + 1 < len(tasks) else None
    end = task["stop"] or nxt
    task["duration_s"] = (end - task["start"]).total_seconds() if end else None
    task["pp_tps"] = (task["prompt_tok"] / (task["prompt_ms"] / 1000.0)
                      if task["prompt_ms"] and task["prompt_tok"] else None)
    task["decode_tps"] = (task["eval_tok"] / (task["eval_ms"] / 1000.0)
                          if task["eval_ms"] and task["eval_tok"] else None)
    task["ttft_s"] = task["prompt_ms"] / 1000.0 if task["prompt_ms"] else None
    j = job_at(task["start"])
    task["job"] = j["id"] if j else None
    task["job_type"] = j["type"] if j else None
    task["job_desc"] = j["desc"] if j else None

json.dump({"jobs": jobs, "tasks": tasks}, open(OUT_JSON, "w"), indent=1, default=str)

def pct(xs, p):
    xs = sorted(x for x in xs if x is not None)
    if not xs:
        return None
    return xs[min(len(xs) - 1, int(p * len(xs)))]

def stats(xs):
    xs = [x for x in xs if x is not None]
    if not xs:
        return "n=0"
    return (f"n={len(xs)} med={pct(xs,.5):.1f} p90={pct(xs,.9):.1f} "
            f"min={min(xs):.1f} max={max(xs):.1f} mean={sum(xs)/len(xs):.1f}")

L = []
L.append("# Per-task performance, autogod-brain (Qwen3.8-27B Q4_K_M) on V100 @ 200 W cap")
L.append("")
L.append(f"window: {tasks[0]['start']} .. {tasks[-1]['stop'] or tasks[-1]['start']}   tasks: {len(tasks)}")
L.append("")
L.append("## overall")
L.append("")
L.append(f"decode t/s:      {stats([t['decode_tps'] for t in tasks])}")
L.append(f"prefill t/s:     {stats([t['pp_tps'] for t in tasks])}")
L.append(f"TTFT (prompt s): {stats([t['ttft_s'] for t in tasks])}")
L.append(f"prompt tokens:   {stats([t['prompt_tok'] for t in tasks])}")
L.append(f"decode tokens:   {stats([t['eval_tok'] for t in tasks])}")
L.append(f"wall duration s: {stats([t['duration_s'] for t in tasks])}")
L.append("")
L.append("## by job type")
L.append("")
for jtype in sorted(set(t["job_type"] or "?" for t in tasks)):
    sub = [t for t in tasks if (t["job_type"] or "?") == jtype]
    L.append(f"### {jtype}  ({len(sub)} tasks)")
    L.append(f"decode:      {stats([t['decode_tps'] for t in sub])}")
    L.append(f"prefill:     {stats([t['pp_tps'] for t in sub])}")
    L.append(f"ttft_s:      {stats([t['ttft_s'] for t in sub])}")
    L.append(f"prompt_tok:  {stats([t['prompt_tok'] for t in sub])}")
    L.append(f"decode_tok:  {stats([t['eval_tok'] for t in sub])}")
    L.append(f"duration_s:  {stats([t['duration_s'] for t in sub])}")
    L.append("")

L.append("## by context depth (n_tokens at stop)")
L.append("")
for lo, hi in [(0, 8000), (8000, 16000), (16000, 32000), (32000, 48000), (48000, 10**9)]:
    sub = [t for t in tasks if t["n_tokens_stop"] is not None and lo <= t["n_tokens_stop"] < hi]
    label = f"{lo//1000}k-{hi//1000}k" if hi < 10**9 else f"{lo//1000}k+"
    L.append(f"### ctx {label}")
    L.append(f"decode:      {stats([t['decode_tps'] for t in sub])}")
    L.append(f"prefill:     {stats([t['pp_tps'] for t in sub])}")
    L.append(f"ttft_s:      {stats([t['ttft_s'] for t in sub])}")
    L.append("")

L.append("## by epoch (server restart / config)")
L.append("")
epochs = [
    ("18:34-18:41 ctx32k", "2026-09-01T18:34:00", "2026-09-01T18:41:00"),
    ("18:41-18:59 ctx64k", "2026-09-01T18:41:00", "2026-09-01T18:59:00"),
    ("18:59-20:52 ctx64k", "2026-09-01T18:59:00", "2026-09-01T20:52:00"),
    ("20:52-00:49 ctx192k", "2026-09-01T20:52:00", "2026-09-02T00:49:00"),
    ("00:49-now ctx192k", "2026-09-02T00:49:00", "2026-09-02T23:59:00"),
]
for name, a, b in epochs:
    a = datetime.fromisoformat(a); b = datetime.fromisoformat(b)
    sub = [t for t in tasks if a <= t["start"] < b]
    L.append(f"### {name}")
    L.append(f"tasks: {len(sub)}")
    L.append(f"decode:      {stats([t['decode_tps'] for t in sub])}")
    L.append(f"prefill:     {stats([t['pp_tps'] for t in sub])}")
    L.append(f"ttft_s:      {stats([t['ttft_s'] for t in sub])}")
    L.append(f"prompt_tok:  {stats([t['prompt_tok'] for t in sub])}")
    L.append("")

open(OUT_MD, "w").write("\n".join(L))
print(f"tasks={len(tasks)} jobs={len(jobs)}")
print("\n".join(L[:30]))
