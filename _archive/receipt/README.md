# receipt — the word bureau

Type any sentence and it prints a **thermal-paper receipt** that prices every
letter by its Scrabble value, itemized word by word, adds a **7% rarity
surcharge**, and shows a running **TOTAL DUE** that updates on every keystroke.

It is a showpiece: one self-contained `index.html`, no backend, no build, no
network. It runs from GitHub Pages as-is at
`https://jackdavisonpowell-eng.github.io/lab/receipt/`.

## run it

```sh
cd /home/jack/lab/receipt
./run.sh            # serves http://127.0.0.1:8102  (default)
./run.sh 9000       # or any other port
LAB_PORT=9000 ./run.sh
```

Or just open `index.html` directly — there is nothing to install.

## what it does

- Every letter is priced at its **official Scrabble value** (1–10).
- Words are itemized with a dotted leader to the word's price, like a real
  receipt.
- **Rare letters** (J Q X Z, plus the premium W K V) are flagged in red — they
  are what push the surcharge up, so you can see what is making you pay.
- `SUBTOTAL` + `RARITY SURCHARGE 7%` = `TOTAL DUE`, recomputed live.
- A big `TOTAL DUE` number sits in the counter readout, updating as you type.
- The receipt has a torn/perforated top and bottom edge, a dashed rule, a
  fake barcode, and a deterministic per-receipt code derived from your text
  (nothing leaves the page).
- The paper does a quick "print" flash on each keystroke.

## the math (verifiable)

`hello world` → letters h4 e1 l1 l1 o1 w4 o1 r1 l1 d2 = **$17.00** subtotal,
**$1.19** rarity surcharge (7%), **$18.19** total due.

## what I'd add

- A "print" button that opens a print stylesheet (paper only).
- A share-card export (render the receipt to a 1080px PNG) so the screenshot
  is one click, not a crop.
- A "most expensive sentence" leaderboard stored in `localStorage`.
- A currency toggle (the bureau accepts words in any unit).
