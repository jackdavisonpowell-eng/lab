# _kit/snippets.md — copy-paste blocks

These are the pieces that got rewritten in every project. Copy them, change
the constants, done. They assume base.css is linked and the :root vars exist.

## 1. Canvas boilerplate (DPR-correct, resize-safe)

The full-screen canvas with devicePixelRatio scaling. `W`/`H` are CSS pixels;
draw in CSS pixels, the transform handles the rest.

```js
var cv = document.getElementById('cv');
var ctx = cv.getContext('2d');
var W = 0, H = 0;

function resize(){
  var dpr = window.devicePixelRatio || 1;
  W = window.innerWidth;
  H = window.innerHeight;
  cv.width = Math.round(W * dpr);
  cv.height = Math.round(H * dpr);
  cv.style.width = W + 'px';
  cv.style.height = H + 'px';
  ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  // re-measure anything font-dependent here (charW, charH, cols, rows...)
}
window.addEventListener('resize', resize);
resize();
```

Animation loop with a clamped dt (tab-switch safe):

```js
var last = 0;
function frame(ts){
  requestAnimationFrame(frame);
  var dt = Math.min(0.05, (ts - last) / 1000);
  last = ts;
  // draw(dt)
}
requestAnimationFrame(function(ts){ last = ts; frame(ts); });
```

Fade-to-bg trick for trails (rain, supernova): instead of clearRect, paint
the background at low alpha every frame:

```js
ctx.fillStyle = 'rgba(10,10,8,0.16)';   // = --bg at 16%
ctx.fillRect(0, 0, W, H);
```

## 2. Keydown handler

One listener, a switch on `e.key`, guard `e.repeat` for held keys,
`e.preventDefault()` only when you actually consume the key.

```js
document.addEventListener('keydown', function(e){
  if (e.key === ' ' || e.key === 'Enter') { e.preventDefault(); next(); }
  else if (e.key === 'c' || e.key === 'C') copy();
  else if (e.key === 's' || e.key === 'S') save();
  else if (e.key >= '1' && e.key <= '9') { /* filter slot */ }
});
```

For held-key games (cluster: throttle/brake), track state in an object and
clear it on keyup:

```js
var keys = {};
document.addEventListener('keydown', function(e){
  var k = e.key.toLowerCase();
  if (k === ' ' || k === 'w') { keys.thr = true; e.preventDefault(); }
  else if (k === 's' || k === 'x') { keys.brk = true; e.preventDefault(); }
});
document.addEventListener('keyup', function(e){
  var k = e.key.toLowerCase();
  if (k === ' ' || k === 'w') keys.thr = false;
  if (k === 's' || k === 'x') keys.brk = false;
});
```

## 3. Share-card SVG renderer (from kicker)

One function, two outputs: the same string is injected into the page AND
downloaded as a self-contained 1080x1080 .svg. No fonts, no external refs —
system stacks only, so it renders identically anywhere.

```js
function esc(s){
  return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;')
    .replace(/"/g,'&quot;').replace(/'/g,'&#39;');
}

/* Wrap text into lines of at most maxChars chars, word-boundary. */
function wrapText(text, maxChars){
  var words = String(text).split(/\s+/), lines = [], line = '';
  for (var i = 0; i < words.length; i++) {
    var w = words[i];
    if (line && (line + ' ' + w).length > maxChars) { lines.push(line); line = w; }
    else line = line ? line + ' ' + w : w;
  }
  if (line) lines.push(line);
  return lines;
}

/* 1080x1080 card. accent = any hex; the rest is the house chrome. */
function renderCard(text, accent, idx, total){
  var lines = wrapText(text, 34);
  var fs = 54, maxH = 470;
  while (lines.length * (fs * 1.45) > maxH && fs > 30) fs -= 2;
  var lineH = fs * 1.45, blockH = lines.length * lineH;
  var y0 = 600 - blockH / 2 + fs * 0.35;
  var tspans = '';
  for (var i = 0; i < lines.length; i++)
    tspans += '<tspan x="540" y="' + (y0 + i * lineH).toFixed(1) + '">' + esc(lines[i]) + '</tspan>';
  var num = String(idx).replace(/\D/g,''), pad = num.length < 2 ? '0' + num : num;

  return '<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="1080" viewBox="0 0 1080 1080">' +
    '<rect width="1080" height="1080" fill="#0b0b0b"/>' +
    /* corner notches */
    '<path d="M0 64 L64 0 L1080 0 L1080 1016 L1016 1080 L0 1080 Z" fill="none" stroke="' + accent + '" stroke-width="3"/>' +
    '<path d="M0 96 L96 0 L1080 0" fill="none" stroke="#2a2a2a" stroke-width="1"/>' +
    '<path d="M1080 984 L984 1080 L0 1080" fill="none" stroke="#2a2a2a" stroke-width="1"/>' +
    /* chevrons, top-left */
    '<path d="M64 150 L104 110 L144 150" fill="none" stroke="' + accent + '" stroke-width="4"/>' +
    '<path d="M64 190 L104 150 L144 190" fill="none" stroke="' + accent + '" stroke-width="4" opacity="0.55"/>' +
    '<path d="M64 230 L104 190 L144 230" fill="none" stroke="' + accent + '" stroke-width="4" opacity="0.3"/>' +
    /* wordmark — replace SLUG + tagline */
    '<text x="90" y="120" font-family="ui-monospace, Menlo, Consolas, monospace" font-size="30" letter-spacing="14" fill="#f2f0ea">SLUG</text>' +
    '<text x="90" y="152" font-family="ui-monospace, Menlo, Consolas, monospace" font-size="15" letter-spacing="6" fill="#6b6b6b">TAGLINE</text>' +
    /* the text */
    '<text text-anchor="middle" font-family="Georgia, \'Times New Roman\', serif" font-style="italic" font-size="' + fs + '" fill="#f2f0ea">' + tspans + '</text>' +
    /* divider */
    '<line x1="440" y1="850" x2="640" y2="850" stroke="#2a2a2a" stroke-width="2"/>' +
    '<path d="M540 838 L552 850 L540 862 L528 850 Z" fill="' + accent + '"/>' +
    /* big number */
    '<text x="470" y="985" text-anchor="end" font-family="Georgia, \'Times New Roman\', serif" font-style="italic" font-size="110" fill="' + accent + '">' + pad + '</text>' +
    '<text x="500" y="985" font-family="ui-monospace, Menlo, Consolas, monospace" font-size="30" letter-spacing="4" fill="#6b6b6b">/ ' + total + '</text>' +
    '</svg>';
}

/* Download it. Same string as the on-screen one. */
function saveCard(svg, filename){
  var blob = new Blob([svg], { type: 'image/svg+xml' });
  var url = URL.createObjectURL(blob);
  var a = document.createElement('a');
  a.href = url; a.download = filename;
  document.body.appendChild(a); a.click(); document.body.removeChild(a);
  setTimeout(function(){ URL.revokeObjectURL(url); }, 1000);
}
```

## 4. Clipboard with fallback

```js
function copyText(text, onDone){
  function done(){ onDone && onDone(); }
  if (navigator.clipboard && navigator.clipboard.writeText)
    navigator.clipboard.writeText(text).then(done, function(){ fallbackCopy(text); done(); });
  else { fallbackCopy(text); done(); }
}
function fallbackCopy(text){
  var ta = document.createElement('textarea');
  ta.value = text; ta.style.position = 'fixed'; ta.style.opacity = '0';
  document.body.appendChild(ta); ta.select();
  try { document.execCommand('copy'); } catch (e) {}
  document.body.removeChild(ta);
}
```

## 5. Data fetch with a graceful offline fallback

Projects ship a fixture (`.sample.json` / inline default) so a clone with no
real data still runs. `rain` is the worked example (see its run.sh).

```js
fetch('titles.json').then(function(r){ return r.json(); }).then(function(t){
  start(t);
}).catch(function(){
  start([/* inline fixture */]);
});
```
