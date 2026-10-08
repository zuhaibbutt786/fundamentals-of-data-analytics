/* Dependency-free DOM-fixture smoke checks; not a substitute for browser layout QA. */
const fs = require('fs'), vm = require('vm'), assert = require('assert'), path = require('path');
const root = path.resolve(__dirname, '..');
class Element {
  constructor(tag, attrs={}) { this.tagName=tag;this.attrs={};this.dataset={};this.children=[];this.events={};this.textContent='';this.innerHTML='';this.style={};this.value='';this.checked=false;this.classes=new Set();this.classList={add:(...c)=>c.forEach(x=>this.classes.add(x)),remove:(...c)=>c.forEach(x=>this.classes.delete(x)),contains:c=>this.classes.has(c),toggle:(c,force)=>{const next=force===undefined?!this.classes.has(c):force;next?this.classes.add(c):this.classes.delete(c);return next;}};Object.entries(attrs).forEach(([k,v])=>this.setAttribute(k,v)); }
  setAttribute(k,v) {this.attrs[k]=String(v);if(k==='id')this.id=v;if(k==='class')this.classes=new Set(String(v).split(' '));if(k.startsWith('data-'))this.dataset[k.slice(5).replace(/-([a-z])/g,(_,c)=>c.toUpperCase())]=v;}
  getAttribute(k){return this.attrs[k]??null;} removeAttribute(k){delete this.attrs[k];}
  append(...els){els.forEach(el=>{if(el.parentElement){el.parentElement.children=el.parentElement.children.filter(c=>c!==el);}el.parentElement=this;el.ownerDocument=this.ownerDocument;this.children.push(el);});}
  before(el){const p=this.parentElement;el.parentElement=p;el.ownerDocument=this.ownerDocument;p.children.splice(p.children.indexOf(this),0,el);}
  appendChild(el){this.append(el);return el;}
  prepend(el){el.parentElement=this;el.ownerDocument=this.ownerDocument;this.children.unshift(el);}
  replaceChildren(...els){this.children=[];this.append(...els);}
  addEventListener(type,fn){(this.events[type]??=[]).push(fn);}
  dispatch(type,extra={}){const e={target:this,key:'',preventDefault(){this.prevented=true;},...extra};(this.events[type]??[]).forEach(fn=>fn.call(this,e));}
  click(){this.dispatch('click');} focus(){this.ownerDocument.activeElement=this;}
  matches(s){if(s.startsWith('#'))return this.id===s.slice(1);if(s.startsWith('.'))return s.slice(1).split('.').every(c=>this.classes.has(c));if(s.startsWith('['))return this.getAttribute(s.slice(1,-1))!==null;if(s.includes('[')){const [tag,a]=s.split('[');return this.tagName===tag&&this.getAttribute(a.slice(0,-1))!==null;}return this.tagName===s;}
  querySelectorAll(selector){const options=selector.split(',').map(s=>s.trim()),hits=[];function visit(el){for(const child of el.children){if(options.some(s=>child.matches(s)))hits.push(child);visit(child);}}visit(this);return hits;}
  querySelector(selector){return this.querySelectorAll(selector)[0]??null;}
  closest(s){let e=this;while(e){if(e.matches(s))return e;e=e.parentElement;}return null;}
  contains(el){return el===this||this.children.some(c=>c.contains(el));}
}
function environment(url, storage=new Map(), blocked=false) {
  const doc = new Element('document');doc.ownerDocument=doc;doc.documentElement=new Element('html');doc.head=new Element('head');doc.body=new Element('body');doc.append(doc.documentElement);doc.documentElement.append(doc.head,doc.body);doc.documentElement.scrollHeight=1000;doc.readyState='complete';doc.currentScript={src:'https://example.test/course/assets/js/main.js'};
  doc.createElement=tag=>{const el=new Element(tag);el.ownerDocument=doc;return el;};doc.createElementNS=(_,tag)=>doc.createElement(tag);doc.getElementById=id=>doc.querySelector('#'+id);
  doc.activeElement=doc.body;
  const location=new URL(url),ctx={console,URL,Intl,Set,Map,document:doc,location,setTimeout:fn=>fn(),matchMedia:()=>({matches:false}),localStorage:{getItem:k=>{if(blocked)throw Error('storage unavailable');return storage.get(k)??null;},setItem:(k,v)=>{if(blocked)throw Error('storage unavailable');storage.set(k,v);}}};ctx.window=ctx;ctx.scrollY=0;ctx.innerHeight=800;ctx.innerWidth=1200;ctx.addEventListener=()=>{};vm.createContext(ctx);
  const add=(tag,attrs,parent=doc.body)=>{const el=doc.createElement(tag);Object.entries(attrs).forEach(([k,v])=>el.setAttribute(k,v));parent.append(el);return el;};
  return {doc,ctx,add,run:file=>vm.runInContext(fs.readFileSync(path.join(root,file),'utf8'),ctx,{filename:file})};
}
const references=JSON.parse(fs.readFileSync(path.join(root,'resources/reference_totals.json'),'utf8'));
const report=environment('https://example.test/course/resources/retail-report.html');
for(const id of ['year','region','reset','context','revenue','profit','margin','orders','chart','rows','total'])report.add(id==='chart'?'svg':'div',{id});
report.doc.getElementById('year').value='all';report.doc.getElementById('region').value='all';report.run('resources/retail-data.js');report.run('resources/retail-report.js');
function verifyReport(ref) {const dollars=new Intl.NumberFormat('en-US',{style:'currency',currency:'USD'});assert.equal(report.doc.getElementById('revenue').textContent,dollars.format(ref.net_revenue_usd));assert.equal(report.doc.getElementById('orders').textContent,new Intl.NumberFormat('en-US').format(ref.orders));assert.equal(report.doc.getElementById('profit').textContent,dollars.format(ref.profit_usd));assert.equal(report.doc.getElementById('margin').textContent,(ref.profit_margin*100).toFixed(2)+'%');}
verifyReport(references.all);
for(const [year,ref] of Object.entries(references.by_year)){report.doc.getElementById('year').value=year;report.doc.getElementById('year').dispatch('change');verifyReport(ref);}
report.doc.getElementById('reset').click();verifyReport(references.all);
for(const [region,ref] of Object.entries(references.by_region)){report.doc.getElementById('region').value=region;report.doc.getElementById('region').dispatch('change');verifyReport(ref);}
report.doc.getElementById('reset').click();
const bar=report.doc.getElementById('chart').querySelector('[role]');bar.dispatch('keydown',{key:'Enter'});verifyReport(references.by_region.North);report.doc.getElementById('reset').click();verifyReport(references.all);
const store=new Map();
function lesson(url,blocked=false){const env=environment(url,store,blocked),{add,doc,run}=env;add('button',{id:'themeToggle'});add('button',{id:'searchBtn'});const overlay=add('div',{id:'searchOverlay'}),box=add('div',{class:'search-box'},overlay);add('input',{id:'searchInput'},box);add('div',{id:'searchResults'},box);add('input',{id:'lectureComplete','data-complete-lecture':'5'});const quiz=add('div',{id:'q1',class:'quiz-card','data-answer':'b'});add('p',{},quiz).textContent='Which answer?';for(const v of ['a','b'])add('div',{class:'quiz-option','data-value':v},quiz);add('div',{class:'quiz-feedback'},quiz);const card=add('div',{class:'flashcard'});add('div',{class:'flashcard-front'},card);add('div',{class:'flashcard-back'},card);run('assets/js/search-index.js');run('assets/js/main.js');return env;}
const lesson5=lesson('https://example.test/course/modules/week3/lecture5.html');
lesson5.doc.getElementById('searchBtn').focus();lesson5.doc.getElementById('searchBtn').click();assert.equal(lesson5.doc.activeElement.id,'searchInput');const input=lesson5.doc.getElementById('searchInput');input.value='DAX';input.dispatch('input');assert(lesson5.doc.getElementById('searchResults').querySelectorAll('a').some(a=>a.getAttribute('href')==='https://example.test/course/modules/week12/lecture23.html'));lesson5.doc.getElementById('searchClose').click();assert.equal(lesson5.doc.activeElement.id,'searchBtn');
const option=lesson5.doc.querySelectorAll('.quiz-option')[1];option.dispatch('keydown',{key:' '});assert.equal(option.getAttribute('aria-checked'),'true');lesson5.ctx.checkQuiz('q1');assert(lesson5.doc.querySelector('.quiz-feedback').textContent.startsWith('Correct'));
lesson5.doc.querySelector('.flashcard').dispatch('keydown',{key:'Enter'});assert.equal(lesson5.doc.querySelector('.flashcard-back').getAttribute('aria-hidden'),'false');
lesson5.doc.getElementById('themeToggle').click();assert.equal(store.get('da-theme'),'dark');const check=lesson5.doc.getElementById('lectureComplete');check.checked=true;check.dispatch('change');assert(JSON.parse(store.get('da-course-progress'))['lecture-5']);
const lesson6=lesson('https://example.test/course/modules/week3/lecture6.html');assert.equal(lesson6.doc.documentElement.getAttribute('data-theme'),'dark');assert(lesson6.doc.getElementById('lectureComplete').checked);assert.equal(Object.keys(JSON.parse(store.get('da-course-progress'))).filter(k=>k.endsWith(':q1')).length,1);assert.equal(lesson6.doc.querySelectorAll('.quiz-option').some(o=>o.classList.contains('selected')),false);
lesson('https://example.test/course/modules/week3/lecture5.html',true);
console.log('PASS: report totals (all / 3 years / 4 regions), chart keyboard filter, reset, nested search URL, search focus restore, keyboard quiz/flashcard, theme/completion persistence, namespaced progress and unavailable storage. DOM fixtures; full browser layout checks remain manual.');
