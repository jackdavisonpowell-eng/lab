---
slug: tape
title: tape
kind: web-server
status: done
port: 8136
blurb: fake stock exchange of your machines
tile: screenshot.png
built: 2026-09-07
verified: 2026-09-07
worth: yes — the smartest weird one
palette: (not recorded — this one was built while the skill still mandated amber)
---
# TAPE

A fake stock exchange for Jack's machines and projects. FRD (FRIDAY) is up
on a green streak, ODYS (Odysseus) is delisted with the CT100, PANTH is
halted because it's a Proxmox host, and a scrolling ticker tape runs across
the top of the page. The stupid bit: prices are a deterministic random walk
seeded by REAL journal activity — every job line in
`$AUTOGOD_VAULT/AUTOGOD/journal/<date>.md` nudges the tickers it touches
(`done` pumps, `FAILED` dumps, timeouts are shrugs). Same journal, same
prices, no state, no writes. A right-hand "THE WIRE" column shows the last
120 journal events as market wires; clicking a ticker or a wire tag charts
its 24h tape.

White/amber monotone, big numbers, monospace, one word name. Local-only on
127.0.0.1:8136. Stdlib only.

## Market cap (added 2026-09-07)
Every ticker now carries a **MKT CAP** column = last × shares. The stupid
part: THE BEAST's share count is NOT fixed — it is the **live GPU power draw
in watts** from `nvidia-smi` (read-only, ~30ms, cached 15s). So TBEAST's
market cap is literally "price × how hard the GPUs are working right now,"
and it ticks as the box idles vs. works. A **GRID LOAD** meter under the
quotes shows real total watts + per-GPU breakdown. If `nvidia-smi` is absent
or wedged it degrades to 0W / "NO METER" and the server never crashes.

## Layout
- `server.py` — stdlib ThreadingHTTPServer; parses the journal, builds the
  seeded price series, reads live GPU power draw (`gpu_power()`, read-only
  `nvidia-smi`, 15s cache), serves `/`, `/api/quotes`, `/health`.
- `index.html` — the whole front end (inline CSS/JS).
- `run.sh` — starts it.

## Run
```
sh /home/jack/lab/tape/run.sh
# → http://127.0.0.1:8136
```

## Verified (2026-09-07, market-cap pass)
- `curl /health` = ok, `/api/quotes` returns 12 quotes each with
  `shares`/`mkt_cap`/`cap_live` + a `grid_load` block (watts + per-GPU).
- `node --check` on the inline script: clean.
- Node harness over the pure fns (fmtCap/fmtShares/quotesHTML/gridLoadHTML/
  headlineHTML) against a REAL /api/quotes payload: 23/23 PASS, including
  mkt_cap == last×shares for all 12, TBEAST live-dot + live-watts tooltip,
  per-GPU row count == grid_load.gpus, and the no-meter fallback.
- Drove the real UI in a browser: MKT CAP column present; TBEAST cap is
  amber with a pulsing live dot (computed color rgb(255,176,0)), FRD cap is
  white; GRID LOAD meter shows real total + 3 per-GPU rows; clicking TBEAST
  swaps the chart note to "MKT CAP = PRICE × LIVE GPU WATTS (…W RIGHT NOW)".
- Cap proven LIVE: API TBEAST shares=118 vs a fresh `nvidia-smi` total of
  121.7W (delta = the 15s cache), so the number tracks the real meter.
- run.sh works from a clean shell. Server killed by PID, port 8136
  confirmed free, no lingering process, curl refused.

## next:
(done — market cap from live GPU watts shipped. If revisiting: a buy/sell
button that plays a sound and logs a fake trade to the Wire, or an
"earnings call" that speaks a job's journal line aloud.)
