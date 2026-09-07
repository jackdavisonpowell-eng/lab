---
slug: racket
title: racket
kind: web-server
status: done
port: 8126
blurb: tennis ladder, real ELO, print view
tile: screenshot.png
built: 2026-09-03
verified: 2026-09-07
worth: yes if the crew uses it
palette: (not recorded — this one was built while the skill still mandated amber)
---
# ladder


## pitch
LADDER is a tennis ladder for the court crew. Add names, record who beat
who, and the board re-ranks itself live on real ELO (K=32, start 1000) with
win/loss records and streak marks (a ^3 is a three-match run). One page,
dark and amber, big italic rating numbers, a tribal tick rule under the
title — the kind of thing a friend group would actually print and tape to
the clubhouse wall, because the "print the ladder" button exists for
exactly that. No framework, no build step, no account: one Python stdlib
server, one HTML file, state in a single state.json next to the code.
Local-only, private, the sensible app nobody would bother to build.

## how it runs
`./run.sh` starts a stdlib ThreadingHTTPServer on 127.0.0.1:8126 that serves
index.html plus a tiny JSON API (add player, record match, delete player,
state). The page fetches /api/state on load and after every action; the
ladder table re-sorts by rating client-side from the server's ranked list.
ELO: expected score 1/(1+10^((rl-rw)/400)), K=32. Streaks are signed
(+ = win run, - = loss run). Print view is a @media print stylesheet —
white on black, form controls hidden, a date line stamped in.

## verified (2026-09-03)
Ran it: server bound 127.0.0.1:8126, page served. Exercised the API with
curl: add 3 players (dup name -> 409), 3 matches (winner==loser -> 400),
ELO verified by hand (equal ratings: +16/-16; 1001 vs 984: +17/-17, the
underdog win swings slightly more). Then drove the REAL UI in a browser
(reloaded first so listeners registered once): typed a name, clicked ADD
(Miguel appeared on the ladder), set the winner/loser dropdowns, clicked
RECORD — ladder re-ranked (Miguel 1016, Sam dropped to 985), match feed
grew to 4, no console errors, and the inline script re-thrown in a
try/catch threw nothing. Server killed after; port confirmed free.
state.json currently holds that demo crew (Priya/Sam/Jack/Miguel) so a
first run has something on the board.

## next
If resumed: (1) head-to-head — a click on any two names shows their
history and who's ahead, the thing a ladder crew actually argues about;
(2) a "challenge" mode where the #1 is the one who has to play next
(standard ladder rules: top of the board is the target); (3) CSV export
button next to print, for people who keep the real record in a spreadsheet;
(4) per-player color chip that carries through print so the wall copy reads
at a glance.
