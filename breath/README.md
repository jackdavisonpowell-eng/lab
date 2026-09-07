# breath — thebeast breathes

A full-screen visual where the machine's three GPUs are drawn as concentric
amber lungs that breathe.

- **Temperature sets the tempo.** A cool GPU (30C) breathes slowly and deeply
  (~9.5s per cycle); a hot one (80C) gasps fast (~2.2s).
- **Utilisation sets the fire.** An idle ring glows faint amber; a working GPU
  burns bright and swells.
- A tribal tick ring marks the perimeter, a background ember brightens with
  aggregate heat, and a core blinks at the center.
- A minimal HUD (top-right) lists each GPU's temp / util / power with an awake
  lamp; bottom-left shows a mood line (IDLE / CHEWING / ROARING); bottom-right
  shows the aggregate heat as a big italic number.

It is **read-only**: the server only calls `nvidia-smi --query-gpu` and reads
nothing else. It never touches FRIDAY's brain or generates any load.

## run it

```
cd /home/jack/lab/breath
./run.sh            # -> http://127.0.0.1:8120/
```

Open http://127.0.0.1:8120/ in a browser on thebeast. It binds loopback only,
so it's private. Stop it with Ctrl-C (or `pkill -f "python3 server.py"`).

The page polls `/stats` every 2s and animates the canvas at 60fps. No
frameworks, no build step — one Python stdlib server + one HTML file.

## files
- `server.py` — stdlib `http.server`, serves the page + `/stats` (nvidia-smi).
- `index.html` — the whole visual: CSS + canvas animation + HUD, inline.
- `run.sh` — starts the server on 127.0.0.1:8120.
- `screenshot.png` — what it looks like.

## what I'd add
Phase-lock the lungs into a staggered inhale wave; a "held breath" state for a
warm-but-idle GPU; a heat shimmer above 70C; and a per-GPU temp sparkline fed by
a small in-memory history ring buffer on the server.
