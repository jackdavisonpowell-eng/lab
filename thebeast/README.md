# thebeast

A live, terminal-styled dashboard of *this* machine. Open one page and watch the
GPUs breathe: per-GPU temp / VRAM / utilization / power, CPU load, RAM, uptime, and
a live feed of the top processes chewing the machine.

It's read-only — the page's server only *reads* `nvidia-smi` and `/proc`. It never
touches FRIDAY's brain, never starts/stops anything, never binds a public port.

## run

    ./run.sh

Then open http://127.0.0.1:8117/ in a browser on the same host (or port-forward).

- `server.py`  — stdlib http.server: serves `index.html` and a `/stats` JSON endpoint.
- `index.html` — the page. Polls `/stats` every 2s, renders the dashboard.
- `run.sh`     — starts the server on 127.0.0.1:8117 (kill it with Ctrl-C).

No dependencies beyond Python 3 stdlib. No installs, no build step.

## the endpoint

`GET /stats` returns JSON:

    {
      "host": "...", "uptime_s": ..., "load": [1,5,15],
      "cpu": {"cores": 12, "usage_pct": ...},
      "mem": {"total_kb": ..., "available_kb": ...},
      "gpus": [ {"name","temp_c","mem_used_mb","mem_total_mb","util_pct","power_w"} ],
      "procs": [ {"pid","cpu","mem","cmd"} ]
    }
