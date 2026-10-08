"""Create a static resource hub, exact reference totals and a functional teaching report."""
from pathlib import Path
import json,html
import pandas as pd
R=Path(__file__).resolve().parents[1]; O=R/'resources'
sales=pd.read_csv(R/'datasets/sales_multiyear.csv',parse_dates=['OrderDate'])
def totals(df):
 revenue=round(float(df.NetRevenue.sum()),2);profit=round(float(df.Profit.sum()),2)
 return dict(lines=len(df),orders=int(df.OrderID.nunique()),customers=int(df.CustomerKey.nunique()),net_revenue_usd=revenue,total_cost_usd=round(float(df.TotalCost.sum()),2),profit_usd=profit,profit_margin=profit/revenue if revenue else None,average_order_value_usd=revenue/df.OrderID.nunique() if len(df) else None)
reference={'dataset':'sales_multiyear.csv','grain':'one order line','currency':'USD','synthetic':True,'seed':399,'all':totals(sales),'by_year':{str(year):totals(df) for year,df in sales.groupby(sales.OrderDate.dt.year)},'by_region':{region:totals(df) for region,df in sales.groupby('Region')}}
(O/'reference_totals.json').write_text(json.dumps(reference,indent=2)+'\n')
# Small self-contained report payload; compute DISTINCTCOUNT from OrderID at interaction time.
rows=[[r.OrderID,str(r.OrderDate.date()),r.Region,float(r.NetRevenue),float(r.Profit)] for r in sales.itertuples()]
(O/'retail-data.js').write_text('window.RETAIL_ROWS = '+json.dumps(rows,separators=(',',':'))+';\n')
def shell(title,body,scripts=''):
 return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{html.escape(title)} | Data Analytics</title><link rel="stylesheet" href="../assets/css/main.css"><style>main{{max-width:1050px;margin:2rem auto;padding:1rem}}.site-header{{position:static}}.resource-list a{{display:inline-block;padding:.5rem}}.kpis{{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:1rem}}.kpis p{{font-size:1.5rem;font-weight:700}}label{{margin-right:1rem}}select,button{{font:inherit;padding:.5rem}}#chart{{width:100%;height:auto}}th,td{{padding:.65rem}}table{{width:100%}}.resource-list{{line-height:1.7}}</style></head><body><a class="skip-link" href="#content">Skip to content</a><header class="site-header"><a href="../index.html">← Course home</a><a href="index.html">Resources</a><button id="themeToggle" aria-label="Toggle theme">Theme</button></header><main id="content"><h1>{title}</h1>{body}</main><script src="../assets/js/search-index.js"></script><script src="../assets/js/main.js"></script>{scripts}</body></html>'''
labs=''.join(f'<li><a href="../labs/{p.name}" download>{html.escape(p.stem.replace("_"," "))}</a></li>' for p in sorted((R/'labs').glob('*.ipynb')))
lectures=''.join(f'<li><a href="../{p.relative_to(R)}">Lecture {int(p.stem.replace("lecture",""))}</a></li>' for p in sorted((R/'modules').rglob('lecture*.html'),key=lambda p:int(p.stem.replace('lecture',''))))
body=f'''<p>Start with setup, then follow lectures in numeric order. Inputs and charts are reproducible. Predictive labs use training-only preprocessing and explicit validation.</p>
<section class="card"><h2>Setup and course expectations</h2><p>Use Python 3.11+ in a virtual environment. Run <code>python -m pip install -r requirements.txt</code> from the repository root. Open notebooks in Jupyter/VS Code and run all cells in order. In Colab clone/upload the repository before running. See the <a href="../docs/course-guide.md">course guide, learning outcomes and suggested capstone rubric</a>.</p><p>Power BI labs require Desktop in a supported Windows environment. Service sharing and refresh depend on your tenant/account. The runnable browser report below is available for conceptual practice.</p></section>
<section class="card"><h2>Shared case study</h2><p><strong>Synthetic sales:</strong> 2022–2024, USD, one order line per row. OrderID repeats across lines. Use DISTINCTCOUNT for orders and a ratio of totals for margin.</p><ul class="resource-list"><li><a href="../datasets/README.md">Data dictionary, sources, limitations and download index</a></li><li><a href="../datasets/sales_multiyear.csv" download>Multi-year sales</a> · <a href="../datasets/dirty_sales.csv" download>Dirty sales</a> · <a href="../datasets/accident_teaching.csv" download>Synthetic accidents</a></li><li>Dimensions: <a href="../datasets/dim_date.csv" download>Date</a>, <a href="../datasets/dim_product.csv" download>Product</a>, <a href="../datasets/dim_customer.csv" download>Customer</a>, <a href="../datasets/dim_region.csv" download>Region</a></li><li><a href="powerbi-measures.dax" download>Consistent DAX measures</a> · <a href="reference_totals.json">Computed reconciliation totals</a></li><li><a href="retail-report.html">Open the interactive retail teaching report</a></li></ul></section>
<section class="card"><h2>Notebook and guided labs</h2><p>Python labs include reference solutions. Desktop labs are procedural notebooks and require manual verification in Power BI. Outputs are cleared for students to execute.</p><ul class="resource-list">{labs}</ul></section>
<section class="card"><h2>Editable visual sources</h2><p><a href="../assets/visuals/manifest.json">Captions, alt text, questions and answers</a> · <a href="../docs/visuals.md">Generation commands and conventions</a></p><p>Each lecture embeds its visuals and offers the SVG download. Numerical values are computed from stated data, not generated illustrations.</p></section><section class="card"><h2>All lectures</h2><ol class="resource-list">{lectures}</ol></section>'''
(O/'index.html').write_text(shell('Course resources and setup',body))
body='''<p>A working browser report for the synthetic order-line case. This is a teaching implementation, not a Power BI screenshot or Service dashboard. Currency: USD. All rows represent generated transactions, not real business performance.</p>
<section class="card"><h2>Filter context</h2><label for="year">Year <select id="year"><option value="all">All years</option><option>2022</option><option>2023</option><option>2024</option></select></label><label for="region">Region <select id="region"><option value="all">All regions</option><option>North</option><option>South</option><option>East</option><option>West</option></select></label><button type="button" id="reset">Reset filters</button><p id="context" aria-live="polite"></p></section>
<div class="kpis"><section class="card"><h2>Net revenue</h2><p id="revenue"></p></section><section class="card"><h2>Profit</h2><p id="profit"></p></section><section class="card"><h2>Margin</h2><p id="margin"></p></section><section class="card"><h2>Distinct orders</h2><p id="orders"></p></section></div>
<section class="card"><h2>Which region needs investigation?</h2><p>Select a region in the chart or use the accessible region filter. Compare the revenue totals in the table, then investigate costs and mix; this chart does not explain causation.</p><svg id="chart" viewBox="0 0 900 380" role="img" aria-label="Regional net revenue bar chart; exact values in table below"></svg><div class="table-wrap"><table><caption>Regional totals under current filters</caption><thead><tr><th scope="col">Region</th><th scope="col">Net revenue (USD)</th><th scope="col">Profit (USD)</th><th scope="col">Margin (%)</th><th scope="col">Distinct orders</th></tr></thead><tbody id="rows"></tbody><tfoot><tr id="total"></tr></tfoot></table></div></section>
<section class="card"><h2>Definitions and limitations</h2><p>NetRevenue = Quantity × UnitPrice × (1 − Discount). Profit = NetRevenue − Quantity × UnitCost. Margin = sum(Profit)/sum(NetRevenue). Orders = number of unique OrderID values, not line count. Revenue/costs omit tax, shipping, returns and other expenses.</p><p>Raw values are summed before display rounding. Each synthetic order belongs to one region, so regional order counts reconcile. More general cross-category order counts may overlap and must not be summed blindly. <a href="reference_totals.json">Compare unfiltered values with the Python reference totals</a>.</p><details><summary>Interpretation question: Can average row margins replace the report margin?</summary><p>No. The report uses the ratio of total profit to total revenue; a row average weights each line equally.</p></details></section>'''
(O/'retail-report.html').write_text(shell('Retail analytics teaching report',body,'<script src="retail-data.js"></script><script src="retail-report.js"></script>'))
(O/'retail-report.js').write_text('''(() => {
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
''')
print(json.dumps(reference['all'],indent=2))
