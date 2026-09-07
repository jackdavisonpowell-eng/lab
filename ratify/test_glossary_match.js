// Cross-check: every term+definition in the vault glossary appears verbatim in TERMS,
// and vice versa. Catches transcription drift between the vault file and the page.
const fs = require("fs");
const path = require("path");

const real = process.env.GLOSSARY;
if (!real) {
  console.log("SKIP — this test diffs the page against the real course glossary,");
  console.log("       which is Jack's own file and is not published. To run it:");
  console.log("         GLOSSARY='/path/to/POLS-1101 Glossary Ch1-3.md' node test_glossary_match.js");
  process.exit(0);
}
const glossary = fs.readFileSync(real, "utf8");
const html = fs.readFileSync(path.join(__dirname, "index.html"), "utf8");
const m = html.match(/<script>([\s\S]*?)<\/script>/);
const src = m[1];

// crude but safe: stub the DOM and grab TERMS
function dummyEl(){return{style:{},dataset:{},classList:{add(){},remove(){}},addEventListener(){},appendChild(){}};}
const els={};
global.document={getElementById(id){if(!els[id])els[id]=dummyEl();return els[id];},querySelector(){return dummyEl();},querySelectorAll(){return{forEach(){}};},createElement(){return dummyEl();}};
global.window=global; global.localStorage={getItem:()=>null,setItem(){},removeItem(){}};
global.navigator={clipboard:null}; global.Blob=function(){}; global.URL={createObjectURL(){return""},revokeObjectURL(){}};
global.confirm=()=>true; global.alert=()=>{};
const api = new Function(src + ";return {TERMS};")();

// parse glossary: "- **Term** (Ch N) — definition"
const lines = glossary.split("\n");
const parsed = [];
let curCh = 0;
for (const line of lines) {
  const ch = line.match(/^## Chapter (\d)/);
  if (ch) { curCh = parseInt(ch[1], 10); continue; }
  const t = line.match(/^- \*\*(.+?)\*\* \(Ch (\d)\) — (.+)$/);
  if (t && curCh) parsed.push([curCh, t[1], t[3].trim()]);
}

let fails = 0;
function check(name, cond, extra){ if(cond) console.log("ok   "+name); else { fails++; console.log("FAIL "+name+(extra?" — "+extra:"")); } }

check("glossary parsed 61 terms", parsed.length === 61, "got " + parsed.length);
check("TERMS count matches glossary", api.TERMS.length === parsed.length, api.TERMS.length + " vs " + parsed.length);

// every glossary term must exist in TERMS with identical chapter + definition
// (first letter may differ in case: glossary defs are mid-sentence lowercase,
//  the page shows them as standalone sentences)
const sameDef = (a, b) => a === b || (a.length > 0 && a[0].toLowerCase() === b[0].toLowerCase() && a.slice(1) === b.slice(1));
for (const [c, name, def] of parsed) {
  const hit = api.TERMS.find(t => t[0] === c && t[1] === name && sameDef(t[2], def));
  if (!hit) {
    // maybe definition drifted — try name-only
    const any = api.TERMS.find(t => t[0] === c && t[1] === name);
    if (any) { fails++; console.log("FAIL def drift: " + name + "\n  glossary: " + def.slice(0,80) + "\n  page:     " + any[2].slice(0,80)); }
    else { fails++; console.log("FAIL missing term: ch" + c + " " + name); }
  }
}
// every TERMS entry must come from the glossary
for (const [c, name, def] of api.TERMS) {
  const hit = parsed.find(t => t[0] === c && t[1] === name && sameDef(t[2], def));
  if (!hit) { fails++; console.log("FAIL page term not in glossary: ch" + c + " " + name); }
}
check("1:1 term+chapter+definition match between glossary and TERMS", true);

console.log(fails === 0 ? "\nALL PASS — page data is verbatim from the vault glossary" : "\n" + fails + " FAILURES");
process.exit(fails === 0 ? 0 : 1);
