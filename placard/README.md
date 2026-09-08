# placard — the department of everyday things

Type any object — **spoon, key, sock, a dead battery, your own left shoe** — and
it is accessioned as a formal **museum placard**: a title in caps, a
deterministic **accession number**, a `c.` date, a material,
**"found under a cinema seat,"** dimensions in centimetres, and a **two-line
provenance** in deadpan curatorial prose.

It is a showpiece: one self-contained `index.html`, no backend, no build, no
network. It runs from GitHub Pages as-is at
`https://jackdavisonpowell-eng.github.io/lab/placard/`.

## run it

```sh
cd /home/jack/lab/placard
./run.sh            # serves http://127.0.0.1:8140  (default)
./run.sh 9000       # or any other port
LAB_PORT=9000 ./run.sh
```

Or just open `index.html` directly — there is nothing to install.

## what it does

- Type an object; the label re-renders on every keystroke.
- **Common objects** (spoon, key, sock, shoe, battery, cup, fork, ring, watch,
  pen, coin, button, glove, phone, book, umbrella, guitar, pillow, wallet) get a
  **hand-written** deadpan label — the prose is the product.
- **Anything else** gets a **generated** label: a deterministic year, material,
  find-spot, dimensions and two-line provenance, all derived from a hash of the
  word. The same object always gets the same label, on every machine — that is
  how a museum works.
- The **accession number** (`1994.117.42`), the `c.` date, the material, the
  dimensions, the **found** line and the provenance are all on the label,
  exactly like a real museum placard.
- The institution is the **DEPARTMENT OF EVERYDAY THINGS**, a museum that has
  permanently collected the objects you already own.
- The label does a small "pin" drop on each re-type. Nothing leaves the page.

## the label (verifiable)

`spoon` → **SPOON**, `c. 1994`, stainless steel, 11.2 × 2.4 cm,
accession **1994.284.24**, *"found under a cinema seat"*, provenance
"Recovered from the floor of the Odeon, 1994. / Gift of an anonymous seat."

## what I'd add

- A "print" button that opens a print stylesheet (the placard only).
- A share-card export (render the placard to a 1080px PNG) so the screenshot
  is one click, not a crop.
- A "most accessioned objects" leaderboard in `localStorage`.
- A second gallery: type the *room* and get the whole wall of labels.
