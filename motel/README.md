# motel

Type a word. It lights up as a neon motel sign.

Every letter's on/off state, flicker timing, and tube color are drawn
deterministically from a hash of the word (FNV-1a seed, xorshift per field),
so the same word is the same sign on every machine. Beneath the word:
VACANCY, a room rate, and one deadpan note. About twenty common words
(motel, hotel, diner, friday, receipt, autogod, ...) get hand-tuned signs —
which letters are dead, the rate, the note — because the prose is the
product. Everything else is generated.

The joke is the burnt-out letters: dim, sagging, no glow. The default sign
is MOTEL with the O, T, and E dead — the O has been dead since 1974.

## Run

```
./run.sh            # http://127.0.0.1:8142
LAB_PORT=8199 ./run.sh
```

No server needed: `index.html` is one self-contained file (inline CSS+JS,
no fetch, no deps) and runs as-is from GitHub Pages at
https://jackdavisonpowell-eng.github.io/lab/motel/

## What it is

- single `index.html`, ~10 KB, stdlib-free
- `signFor(word)` is the whole product: pure function, exposed on
  `window.motel` for tests
- palette: night-sky blue-black with per-letter neon from six hand-picked
  two-color tube schemes; VACANCY is always classic sign red

## What I'd add

- a "photo mode" that renders the sign to a canvas for screenshots
- sound: a 60 Hz hum + random tick from the sputtering letters
- a sign for two words (MOTEL / DINER stacked)
