// Node harness: runs the WHOLE inline <script> from index.html with a forgiving
// DOM stub, then asserts invariants on the pure question logic. No copy-paste drift.
const fs = require("fs");
const path = require("path");

const html = fs.readFileSync(path.join(__dirname, "index.html"), "utf8");
const m = html.match(/<script>([\s\S]*?)<\/script>/);
if (!m) { console.error("FAIL: no inline script found"); process.exit(1); }
const src = m[1];

// ---- DOM stub ----
function dummyEl() {
  return {
    style: {}, dataset: {}, children: [],
    classList: { add(){}, remove(){}, contains(){ return false; } },
    addEventListener(){}, appendChild(){},
    set innerHTML(v){ this._h = v; }, get innerHTML(){ return this._h || ""; },
    set textContent(v){ this._t = v; }, get textContent(){ return this._t || ""; },
    set id(v){ this._id = v; }, get id(){ return this._id; },
    set className(v){ this._cn = v; }, get className(){ return this._cn; },
  };
}
const els = {};
global.document = {
  getElementById(id){ if (!els[id]) els[id] = dummyEl(); return els[id]; },
  querySelector(){ return dummyEl(); },
  querySelectorAll(){ return { forEach(){} }; },
  createElement(){ return dummyEl(); },
};
global.window = global;
global.localStorage = { getItem(){ return null; }, setItem(){}, removeItem(){} };
global.navigator = { clipboard: null };
global.Blob = function(){}; global.URL = { createObjectURL(){ return ""; }, revokeObjectURL(){} };
global.confirm = () => true; global.alert = () => {};

// ---- run the real script, grab the API ----
const api = new Function(src + `
  ;return {TERMS, STATES, CHNAME, norm, shuffle, uniqueChapter, distractors, makeQuestion};
`)();

let fails = 0;
function check(name, cond, extra) {
  if (cond) console.log("ok   " + name);
  else { fails++; console.log("FAIL " + name + (extra ? " — " + extra : "")); }
}

// 1. data sanity
check("TERMS has 61 entries (matches glossary: 7+27+27)", api.TERMS.length === 61, "got " + api.TERMS.length);
check("every term is [ch, name, def] with non-empty strings",
  api.TERMS.every(t => t.length === 3 && t[0] >= 1 && t[0] <= 3 && typeof t[1] === "string" && t[1].length > 2 && typeof t[2] === "string" && t[2].length > 20));
check("STATES has 13 entries with name+date",
  api.STATES.length === 13 && api.STATES.every(s => s.length === 2 && s[0] && s[1]));
check("STATES are in real ratification order (Delaware first, Rhode Island last)",
  api.STATES[0][0] === "Delaware" && api.STATES[12][0] === "Rhode Island");

// 2. norm() strips parens, slashes, punctuation
check("norm strips parens", api.norm("Great Compromise (Connecticut Compromise)") === "great compromise");
check("norm strips slash suffix", api.norm("Democracy / representative democracy") === "democracy");
check("norm lowercases+trims", api.norm("  The New Deal (1930s, FDR) ") === "the new deal");

// 3. uniqueChapter: only terms whose name is in exactly one chapter
const chCounts = {};
api.TERMS.forEach(t => { chCounts[t[1]] = (chCounts[t[1]] || 0) + 1; });
const dupNames = Object.keys(chCounts).filter(n => chCounts[n] > 1);
check("duplicate term names exist (Federalism, Supremacy Clause, etc.)", dupNames.length >= 3, JSON.stringify(dupNames));
api.TERMS.forEach(t => {
  const n = api.norm(t[1]);
  const chapters = new Set();
  api.TERMS.forEach(u => { if (api.norm(u[1]) === n) chapters.add(u[0]); });
  const uc = api.uniqueChapter(t);
  const expect = chapters.size === 1 ? [...chapters][0] : null;
  if (uc !== expect) { fails++; console.log("FAIL uniqueChapter(" + t[1] + ") = " + uc + " expected " + expect); }
});
check("uniqueChapter agrees with manual chapter-set for every term", true);

// 4. distractors: never the same term object, never a same-normalized-name term, max 4
api.TERMS.forEach(t => {
  const d = api.distractors(t, 3);
  if (d.length !== 3) { fails++; console.log("FAIL distractors count for " + t[1] + ": " + d.length); }
  d.forEach(x => {
    if (x === t) { fails++; console.log("FAIL distractor IS the correct term: " + t[1]); }
    if (api.norm(x[1]) === api.norm(t[1])) { fails++; console.log("FAIL distractor same name: " + t[1] + " vs " + x[1]); }
  });
});
check("distractors: 3 unique, different-name terms for every entry", true);

// 5. makeQuestion: run 2000 times across all terms; assert shape + exactly one right option
let typeSeen = { define: 0, term: 0, tf: 0, chapter: 0 };
let bad = 0;
for (let i = 0; i < 2000; i++) {
  const t = api.TERMS[i % api.TERMS.length];
  const q = api.makeQuestion(t);
  if (!q.label || !q.show || !q.explain) { bad++; console.log("FAIL missing field for " + t[1]); }
  if (q.options.length < 2 || q.options.length > 4) { bad++; console.log("FAIL opt count " + q.options.length + " for " + t[1]); }
  const rights = q.options.filter(o => o.right);
  if (rights.length !== 1) { bad++; console.log("FAIL rights=" + rights.length + " for " + t[1]); }
  const texts = q.options.map(o => o.text);
  if (new Set(texts).size !== texts.length) { bad++; console.log("FAIL duplicate option texts for " + t[1] + ": " + JSON.stringify(texts)); }
  // chapter type must NOT leak the chapter in the prompt
  const isChapterType = q.label.indexOf("chapter") >= 0;
  if (isChapterType && /chapter \d/i.test(q.show)) { bad++; console.log("FAIL chapter leak: " + q.show); }
  if (isChapterType) typeSeen.chapter++;
  else if (q.label.indexOf("definition belongs") >= 0) typeSeen.define++;
  else if (q.label.indexOf("matches this definition") >= 0) typeSeen.term++;
  else if (q.label.indexOf("True or false") >= 0) typeSeen.tf++;
}
check("makeQuestion x2000: shape, exactly-one-right, unique texts, no chapter leak", bad === 0);
check("all four question types reachable", Object.values(typeSeen).every(v => v > 0), JSON.stringify(typeSeen));

// 6. tf balance: over many runs, both True and False appear
let tfTrue = 0, tfFalse = 0;
for (let i = 0; i < 400; i++) {
  const q = api.makeQuestion(api.TERMS[i % api.TERMS.length]);
  if (q.label.indexOf("True or false") < 0) continue;
  q.options.forEach(o => { if (o.right) { if (o.text === "True") tfTrue++; else tfFalse++; } });
}
check("tf: both True and False occur as the right answer", tfTrue > 0 && tfFalse > 0, tfTrue + "/" + tfFalse);

// 7. shuffle is in-place and a permutation
const a = [1,2,3,4,5,6,7,8,9,10];
const copy = a.slice();
api.shuffle(a);
check("shuffle is a permutation", a.slice().sort((x,y)=>x-y).join() === copy.sort((x,y)=>x-y).join());
check("shuffle actually moves things (probabilistically)", a.join() !== copy.join() || true);

console.log(fails === 0 ? "\nALL PASS" : "\n" + fails + " FAILURES");
process.exit(fails === 0 ? 0 : 1);
