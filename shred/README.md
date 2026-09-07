# shred

A skateboarding trick roulette. One HTML file, zero dependencies,
local-only.

## what it is

Press space (or the SPIN button) and three slot reels spin —
TRICK × STANCE × SPOT — and land on a call:

    cork 540 flip × switch × 12-stair

Go do the trick. Come back. Log it:

    l  = landed
    b  = bailed

It keeps score:

- landed streak / best streak / bail streak (big italic numbers)
- HEAT — an exponentially weighted meter over your last 14 outcomes
  (weight 1.25^i). Lands push it toward "shred", bails decay it to
  "cold". Bail = screen shake.
- per-trick table: landed / bailed / rate% for every trick you've
  attempted, sorted by attempts. A trick with 2+ bails and 0 lands
  gets flagged WRECKED.

All stats live in localStorage (`shred.stats.v1`) — close the tab,
come back tomorrow, your heat is still cold. RESET STATS (bottom right)
wipes it.

## how to run

    cd /home/jack/lab/shred
    ./run.sh            # http://127.0.0.1:8126/
    ./run.sh 8130       # or any port

Open the URL in a browser. That's it.

## keys

    space  spin the reels
    l      log landed
    b      log bailed

## what i'd add

- session mode: a graded N-spin session (7/10 = "solid") with history
- difficulty tiers (street/park/vert) that weight the reels and bonus
  heat for harder tiers
- WebAudio oscillator clicks per reel step + a thump on bail
- an SVG deck that flips when you spin switch
