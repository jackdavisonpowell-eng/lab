# RATIFY

A self-quiz for POLS-1101 Exam 1 (Ch 1–3), built from the vault glossary.
The 13 states vote in real ratification order; you need 9 of 13 to pass —
the actual number it took in 1787–90.

## Run

    sh run.sh

Then open http://127.0.0.1:8133/ . Local only, no installs — one HTML file
plus a stdlib `python3 -m http.server` on port 8133.

## How it plays

- 13 questions, one per state, drawn from the 61 glossary terms.
- Right answer → that state ratifies (amber). Wrong → it rejects
  (struck through), and the term goes to the review list.
- Question types: "which term matches this definition", "which definition
  belongs to this term", true/false, and "which chapter" (only for terms
  that appear in exactly one chapter, so the answer isn't given away).
- End screen: your X/13, a verdict, and every term you missed with its
  full definition. "Reconvene" to play again with a fresh 13.

## Verify (what was run)

- `node test_ratify.js` — runs the whole inline script under a DOM stub;
  asserts question-builder invariants across 2000 generated questions
  (exactly one right option, no duplicate option texts, no chapter leak,
  all four types reachable, TF balanced).
- `node test_glossary_match.js` — parses the vault glossary and asserts a
  1:1 term+chapter+definition match with the page's TERMS array (first
  letter may differ in case: glossary defs are mid-sentence lowercase).
- Full 13-round game driven in a real browser: 9 right / 4 wrong →
  chips, score, "Ratified." verdict, and 4-item miss review all correct.

## What I'd add

Per-chapter mode (Ch 3 is the long one), a streak counter, or a
"Reconstruction Amendments" bonus round.
