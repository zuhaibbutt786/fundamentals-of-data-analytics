(() => {
  'use strict';
  const year = document.getElementById('year'), region = document.getElementById('region');
  const dollars = new Intl.NumberFormat('en-US', {style:'currency', currency:'USD'});
  const number = new Intl.NumberFormat('en-US');
  function aggregate(rows) {
    const revenue = rows.reduce((a,r)=>a+r[3],0), profit = rows.reduce((a,r)=>a+r[4],0);
    return {revenue,profit,orders:new Set(rows.map(r=>r[0])).size,margin:revenue ? 100*profit/revenue : null};
  }
  function fields(label, a) { return [label,dollars.format(a.revenue),dollars.format(a.profit),a.margin===null?'N/A':a.margin.toFixed(2),number.format(a.orders)]; }
  function tableRow(values) { const tr=document.createElement('tr'); values.forEach((v,i)=>{const cell=document.createElement(i===0?'th':'td'); if(i===0)cell.scope='row'; cell.textContent=v;tr.append(cell);});return tr; }
  function render() {
    const filtered=window.RETAIL_ROWS.filter(r=>(year.value==='all'||r[1].startsWith(year.value))&&(region.value==='all'||r[2]===region.value));
    const all=aggregate(filtered);
    document.getElementById('revenue').textContent=dollars.format(all.revenue);
    document.getElementById('profit').textContent=dollars.format(all.profit);
    document.getElementById('margin').textContent=all.margin===null?'N/A':all.margin.toFixed(2)+'%';
    document.getElementById('orders').textContent=number.format(all.orders);
    document.getElementById('context').textContent=`Year: ${year.value}. Region: ${region.value}. ${number.format(filtered.length)} order lines.`;
    const regions=['North','South','East','West'].map(name=>({name,...aggregate(filtered.filter(r=>r[2]===name))}));
    const tbody=document.getElementById('rows');tbody.replaceChildren(...regions.map(r=>tableRow(fields(r.name,r))));
    const total=document.getElementById('total');total.replaceChildren(...tableRow(fields('Total',all)).children);
    const svg=document.getElementById('chart');svg.replaceChildren(); const ns='http://www.w3.org/2000/svg';
    function node(tag,attrs,text) { const el=document.createElementNS(ns,tag);Object.entries(attrs).forEach(([k,v])=>el.setAttribute(k,v));if(text)el.textContent=text;svg.append(el);return el; }
    node('rect',{width:900,height:380,fill:'white'});node('text',{x:170,y:30,fill:'#183153','font-size':18},'Net revenue (USD), zero baseline');
    const max=Math.max(1,...regions.map(r=>r.revenue));
    regions.forEach((r,i)=>{
      const y=65+i*70;node('text',{x:20,y:y+28,fill:'#183153','font-size':18},r.name);
      const bar=node('rect',{x:170,y,width:550*r.revenue/max,height:40,fill:'#2563eb',tabindex:0,role:'button','aria-label':`Filter ${r.name}: ${dollars.format(r.revenue)} revenue`});
      const select=()=>{region.value=r.name;render();region.focus();};bar.addEventListener('click',select);bar.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();select();}});
      node('text',{x:180+550*r.revenue/max,y:y+28,fill:'#183153','font-size':15},dollars.format(r.revenue));
    });node('line',{x1:170,x2:170,y1:55,y2:350,stroke:'#183153','stroke-width':2});node('text',{x:165,y:375,fill:'#183153','font-size':16},'0');
  }
  year.addEventListener('change',render);region.addEventListener('change',render);
  document.getElementById('reset').addEventListener('click',()=>{year.value='all';region.value='all';render();});render();
})();
