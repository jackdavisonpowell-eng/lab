# LADDER

A tennis ladder for a friend group. Add players, record matches, watch the
board re-rank itself on ELO, print it, tape it to the wall.

Dark page, amber ink, big italic numbers. No framework, no build step, no
account. Python stdlib only.

## run it

```sh
cd /home/jack/lab/racket
./run.sh
# -> http://127.0.0.1:8126/
```

Stop it with Ctrl-C. State lives in `state.json` next to the code — delete
that file to start a fresh ladder.

## use it

- **Add a player** — type a name, hit add (or Enter). Starts at 1000.
- **Record a match** — pick the winner and the loser in the two dropdowns,
  hit record. Ratings move (ELO, K=32), records and streaks update, the
  ladder re-sorts, the match lands in the feed.
- **Strike a name** — the little x on a row removes the player and their
  matches (asks first).
- **Print the ladder** — the button opens the browser print dialog with a
  clean white-on-black version (form controls hidden, date stamped). Pick
  "Save as PDF" if you want to keep it.

## how the numbers work

Standard ELO. Expected score `E = 1 / (1 + 10^((R_loser - R_winner)/400))`,
rating moves by `K * (result - E)` with K=32. Two equal players: +16/-16.
A win for the lower-rated player swings a bit more than that; a loss for
the higher-rated one swings a bit less. Streaks are signed: `^3` is a
three-match win run, `v3` a three-match loss run.

## files

- `server.py` — the whole backend: HTTP server, JSON API, ELO, state I/O.
- `index.html` — the whole frontend: page, styles, print sheet, JS.
- `run.sh` — starts it.
- `state.json` — created on first write; the players and matches.
- `screenshot.png` — what it looks like.

## what i'd add next

Head-to-head history (click two names), a "challenge" rule where the #1 is
the standing target, CSV export, and a per-player color chip that survives
printing.
