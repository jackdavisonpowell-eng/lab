# MANIFEST

The cargo manifest for your dorm move-in. A packing checklist that isn't just a
list — it's a **manifest** you can text to your roommate, then **diff** against
theirs to find what you're both buying and what nobody's got.

## Run

```
./run.sh
```

Opens http://127.0.0.1:8128/ (local-only, private, no installs, no network).
Single HTML file — `index.html` — with inline CSS/JS. State lives in
`localStorage`, so it survives reloads on this machine.

## What it does

- **Holds** (categories): Bedding, Kitchen, Cleaning, Electronics, Furniture,
  Toiletries, Decor, Misc. Add/remove holds, add items to any hold.
- **State per item**: `have` / `need` / `buy` — tap to flip. Live tallies up top.
- **Export**: a round-trippable text manifest (`# MANIFEST <you>` / `## <hold>` /
  `[state] item`). Copy to clipboard or download as `.txt`.
- **Import**: paste a manifest back in — yours from another device, or a
  roommate's. Replaces the current list.
- **Roommate diff**: paste your roommate's manifest and it reports
  - **duplicates** — you're both getting it (one of you can stop),
  - **gaps** — standard dorm-kit items *nobody's* got (trash can, desk lamp,
    shower caddy, extension cord, …),
  - **only you / only them** — the clean split.

## The "nobody would bother" bit

A plain packing list is a to-do. MANIFEST treats the move-in as a **joint
shipment**: the whole point is the *roommate diff* — the overlap you'd otherwise
discover on move-in day, and the gaps you'd both assume the other covered.
The export format is deliberately dumb text so it survives a group chat.

## What I'd add (not yet)

- A "who's buying what" split so the diff can say *you* buy the lamp, *them* the
  trash can — turn the gap list into an assignment.
- A shared link / paste-in-the-URL so you don't have to copy-paste between
  phones (still local: encode the manifest in the URL hash).
- Per-item cost estimate so the manifest doubles as a budget.
