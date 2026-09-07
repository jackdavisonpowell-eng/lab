// Node harness: run the WHOLE inline script with a forgiving DOM stub,
// grab the pure math fns, assert invariants across the presets.
const fs = require('fs');
const html = fs.readFileSync('/home/jack/lab/poise/index.html','utf8');
const src = html.match(/<script>([\s\S]*?)<\/script>/)[1];

// DOM stub
const dummyEl = () => ({
  style:{}, classList:{toggle(){},add(){},remove(){}},
  setAttribute(){}, getAttribute(){return null;},
  addEventListener(){}, innerHTML:'', textContent:'',
  getContext(){ return new Proxy({}, {get:()=> (typeof arguments[1]==='function')?arguments[1]:(()=>{})}); },
});
const document = {
  getElementById: () => dummyEl(),
  querySelector: () => dummyEl(),
  querySelectorAll: () => [],
  createElement: () => dummyEl(),
};
const window = global;
window.addEventListener = () => {};
window.removeEventListener = () => {};
const requestAnimationFrame = () => {};
const script = src.replace(/^"use strict";/m,'');
const api = new Function('document','window','requestAnimationFrame',
  script + '\nreturn {shapeWeight,symmetryScore,radialScore,computeReadout,verdict};')
  (document, window, requestAnimationFrame);
const {shapeWeight,computeReadout} = api;
const W=800,H=600,Cx=W/2,Cy=H/2;

let pass=0, fail=0;
function check(name, cond){ if(cond){pass++;} else {fail++; console.log('FAIL: '+name);} }

// --- weight is monotonic in size, value, sat ---
const base={type:'circle',x:100,y:100,size:40,value:0.5,sat:0.5};
check('weight>0', shapeWeight(base)>0);
check('bigger size -> heavier', shapeWeight({...base,size:80})>shapeWeight({...base,size:20}));
check('darker -> heavier', shapeWeight({...base,value:1})>shapeWeight({...base,value:0}));
check('saturated -> heavier', shapeWeight({...base,sat:1})>shapeWeight({...base,sat:0}));
// all shapes have positive weight and area
for(const t of ['circle','square','triangle','diamond','bar']){
  check('area>0 '+t, shapeWeight({type:t,x:0,y:0,size:30,value:0.5,sat:0.5})>0);
}

// --- symmetric preset: high symmetry, near-zero tilt, verdict SYMMETRICAL ---
const sym=[
 {type:'circle',x:Cx-160,y:300,size:72,value:0.85,sat:0.9},
 {type:'circle',x:Cx+160,y:300,size:72,value:0.85,sat:0.9},
 {type:'bar',x:Cx,y:300,size:42,value:0.5,sat:0.6},
];
let r=computeReadout(sym,W,H);
check('sym symmetry>=0.9', r.symmetry>=0.9);
check('sym tilt~0', Math.abs(r.tilt)<1);
check('sym verdict SYMMETRICAL', r.verdict==='SYMMETRICAL');
check('sym net ~50/50', Math.abs(r.leftW-r.rightW)<1);

// --- asymmetric preset: low symmetry, verdict ASYMMETRICAL, big dark mass on one side ---
const asym=[
 {type:'triangle',x:170,y:310,size:98,value:0.95,sat:0.85},
 {type:'circle',x:520,y:240,size:34,value:0.12,sat:0.2},
 {type:'circle',x:610,y:330,size:28,value:0.15,sat:0.25},
 {type:'diamond',x:560,y:410,size:26,value:0.2,sat:0.3},
];
r=computeReadout(asym,W,H);
check('asym symmetry<0.4', r.symmetry<0.4);
check('asym verdict ASYMMETRICAL', r.verdict==='ASYMMETRICAL');
check('asym left heavier (big dark mass left)', r.leftW>r.rightW);

// --- radial preset: high radial, verdict RADIAL ---
const rad=[];
for(let i=0;i<6;i++){const a=i/6*Math.PI*2;
  rad.push({type:'diamond',x:Cx+Math.cos(a)*150,y:Cy+Math.sin(a)*150,size:34,value:0.7,sat:0.8});}
rad.push({type:'circle',x:Cx,y:Cy,size:30,value:0.9,sat:0.9});
r=computeReadout(rad,W,H);
check('radial radial>=0.6', r.radial>=0.6);
check('radial verdict RADIAL', r.verdict==='RADIAL');

// --- empty canvas ---
r=computeReadout([],W,H);
check('empty tilt 0', r.tilt===0);
check('empty verdict EMPTY', r.verdict==='EMPTY');
check('empty symmetry 0', r.symmetry===0);
check('empty radial 0', r.radial===0);

// --- single shape on axis: perfectly symmetric, no tilt ---
r=computeReadout([{type:'circle',x:Cx,y:300,size:50,value:0.6,sat:0.6}],W,H);
check('on-axis symmetry 1.0', r.symmetry===1);
check('on-axis tilt ~0', Math.abs(r.tilt)<0.01);
check('on-axis verdict SYMMETRICAL', r.verdict==='SYMMETRICAL');

// --- a lone off-center shape tips toward it ---
r=computeReadout([{type:'circle',x:650,y:300,size:50,value:0.6,sat:0.6}],W,H);
check('right-heavy tips right', r.tilt>0);
check('right-heavy leftW 0', r.leftW===0);

console.log('\n'+pass+' passed, '+fail+' failed');
process.exit(fail?1:0);
