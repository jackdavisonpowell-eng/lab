# Villeneuve — shot generator

Random cinematic composition prompts in the Villeneuve register: fog,
sodium light, brutalist mass, silence as a character. One card at a time.
Each card has a HOLD time (6–30 s) — the shot you should wait for.

## Run

    ./run.sh

then open http://127.0.0.1:8132

## Use

- SPACE (or the CUT button) — next shot
- PRINT — copies the shot as plain text to the clipboard
- 5% of shots are MASTER shots (amber frame, "the shot that ends the film")

Single HTML file, no dependencies. Port 8132, bound to 127.0.0.1.

## What I'd add

- A visible hold-timer bar that drains over the shot's hold seconds.
- Share-card export: self-contained SVG 1080x1080 (kicker pattern).
- A "streak" mode: 10 shots, one must be a MASTER.
