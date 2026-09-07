# TAPE — The AUTOGOD Exchange

A fake stock market for Jack's machines and projects. FRD (FRIDAY) trades
on the day's work, ODYS (Odysseus) is delisted with the CT100, PANTH /
NITRO / MAXI are halted because they're not things you can trade, and a
scrolling ticker tape runs across the top.

The stupid bit: **prices are a deterministic random walk seeded by real
journal activity.** Every job line in `$AUTOGOD_VAULT/AUTOGOD/journal/<date>.md`
nudges the tickers it touches — `done` pumps, `FAILED` dumps, an `rc=124`
timeout is a shrug (dampened), and a long-running job moves the price more.
Same journal, same prices, every time. No state, no writes, read-only on the
journal. That's why GUIDE (study guides) is down ~20% right now: the math
study-guide failures are real and it's pricing them in.

## What's on the page
- **Ticker tape** — all 12 symbols scrolling, pauses on hover.
- **Quotes table** (left) — sym, last, 24h change, %, and **MKT CAP**.
  Click a row to chart it.
- **GRID LOAD** (under the quotes) — real live GPU power draw from
  `nvidia-smi`: total watts big, per-GPU breakdown below. This is the meter
  that drives THE BEAST's market cap.
- **Chart** (middle) — 24h SVG line + area, price grid, time labels,
  last-price dot. Big number up top.
- **The Wire** (right) — the last 120 journal events as market wires. Click a
  wire or one of its ticker tags to jump the chart to that symbol.

## The market cap
Every ticker has a market cap = last × shares. THE BEAST (TBEAST) is the
odd one: its **share count is the live GPU power draw in watts**, so its cap
is literally "price × how hard the GPUs are working right now" — it ticks as
the box idles vs. works (amber + pulsing dot marks it live). The other
tickers use fixed, arbitrary share counts. Read-only on `nvidia-smi`; if the
meter's missing it degrades to 0W / "NO METER" and nothing breaks.

White/amber monotone, monospace, big numbers, one-word name. Local-only.

## Run
```
sh /home/jack/lab/tape/run.sh
# → http://127.0.0.1:8136
```
Then open http://127.0.0.1:8136 in a browser. Refreshes every 15s.

## Files
- `server.py` — stdlib `ThreadingHTTPServer`. Parses the journal, builds the
  seeded price series, reads live GPU power draw (`gpu_power()`), serves `/`,
  `/api/quotes`, `/health`. No pip, no npm.
- `index.html` — the entire front end (inline CSS/JS).
- `run.sh` — starts it (port 8136, loopback).

## What I'd add
- A buy/sell button that does nothing but plays a sound and logs a fake trade
  to the Wire.
- Earnings calls: read a job's full text as the "press release" on click.
