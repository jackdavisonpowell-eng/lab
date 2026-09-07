# rain

Amber-monotone matrix rain where every falling stream is a real note title
from the vault (887 of them, pulled from `titles.json`).

- head glyph: near-white amber
- body: amber, fading via the canvas trail
- hover a stream: it freezes so you can read the title
- click: catches the title into the numbered ledger (top-right, last 14)
- space: pause

## Run

    sh run.sh

then open http://127.0.0.1:8121/

No deps: one HTML file with inline CSS/JS, python3 stdlib http.server,
port 8121.

## Regenerating titles

    cd $AUTOGOD_VAULT
    find . -name '*.md' -not -path '*/.*' -printf '%f\n' \
      | sed 's/\.md$//' | sort -u > /home/jack/lab/rain/titles.json.tmp
    python3 -c "import json;json.dump(sorted(set(l.strip() for l in open('/home/jack/lab/rain/titles.json.tmp') if l.strip())),open('/home/jack/lab/rain/titles.json','w'),ensure_ascii=False)"

## Ideas (not done)

- caught titles re-enter the rain as brighter "ghost" streams
- a mode that only rains titles from a chosen folder (College, AUTOGOD...)
- sound: a low tick per stream recycle, very quiet
