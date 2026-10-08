"""Check local resources, exact teaching calculations and execute Python labs independently.

Run from anywhere using the installed course requirements. Desktop tasks remain manual.
"""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import json,subprocess,sys,os,collections
import numpy as np,pandas as pd
import xml.etree.ElementTree as ET
R=Path(__file__).resolve().parents[1]
class Page(HTMLParser):
 def __init__(self):super().__init__();self.ids=[];self.refs=[];self.images=[]
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if 'id' in a:self.ids.append(a['id'])
  for attr in ['href','src']:
   if a.get(attr):self.refs.append(a[attr])
  if tag=='img':self.images.append(a)
pages={}
for path in R.rglob('*.html'):
 if '.git' in path.parts:continue
 page=Page();page.feed(path.read_text());pages[path.resolve()]=page
fail=[]
for path,page in pages.items():
 for ident,count in collections.Counter(page.ids).items():
  if count>1:fail.append(f'{path.relative_to(R)}: duplicate id {ident}')
 for ref in page.refs:
  url=urlsplit(ref)
  if url.scheme or url.netloc:continue
  if not url.path:
   if url.fragment and unquote(url.fragment) not in page.ids:fail.append(f'{path.relative_to(R)}: missing anchor {ref}')
   continue
  target=(path.parent/unquote(url.path)).resolve()
  if not target.exists():fail.append(f'{path.relative_to(R)}: missing {ref}')
  elif url.fragment and target in pages and unquote(url.fragment) not in pages[target].ids:fail.append(f'{path.relative_to(R)}: missing target anchor {ref}')
 for image in page.images:
  if not image.get('alt'):fail.append(f'{path.relative_to(R)}: image without alt {image.get("src")}')
assert not fail,'\n'.join(fail)
manifest=json.loads((R/'assets/visuals/manifest.json').read_text())
covered=set()
for item in manifest:
 ET.parse(R/'assets/visuals'/item['file'])
 assert all(item.get(k) for k in ['title','caption','alt','question','answer'])
 covered.update(item['lectures'])
assert covered==set(range(1,31))
assert len(json.loads((R/'assets/js/search-index.js').read_text().split('=',1)[1].strip().rstrip(';')))==30
sales=pd.read_csv(R/'datasets/sales_multiyear.csv',parse_dates=['OrderDate'])
assert len(sales)==4420 and sales.OrderID.nunique()==2192
assert not sales.duplicated(['OrderID','LineID']).any()
assert np.allclose(sales.NetRevenue,sales.Quantity*sales.UnitPrice*(1-sales.Discount))
assert np.allclose(sales.Profit,sales.NetRevenue-sales.TotalCost)
for key,file in [('ProductKey','dim_product.csv'),('CustomerKey','dim_customer.csv'),('RegionKey','dim_region.csv')]:
 dim=pd.read_csv(R/'datasets'/file);assert dim[key].is_unique
 assert sales[key].isin(dim[key]).all()
dates=pd.read_csv(R/'datasets/dim_date.csv',parse_dates=['Date']).Date
assert dates.is_unique and dates.diff().iloc[1:].eq(pd.Timedelta(days=1)).all()
assert sales.OrderDate.isin(dates).all()
ref=json.loads((R/'resources/reference_totals.json').read_text())['all']
assert np.isclose(sales.NetRevenue.sum(),ref['net_revenue_usd'])
assert ref['orders']==sales.OrderID.nunique()
x=np.array([10,20,30,40,100]);assert x.mean()==40 and x.var()==1000
assert np.isclose((120-x.min())/(x.max()-x.min()),11/9)
x=np.array([10,12,13,14,15,100]);assert np.isclose(x.mean(),164/6) and np.median(x)==13.5
assert np.allclose(np.percentile(x,[25,75],method='linear'),[12.25,14.75])
print(f'Static checks passed: {len(pages)} HTML pages, {len(manifest)} visuals; 30 lectures covered; dataset and exact-calculation checks passed.')
code_labs=0;manual_labs=0;code_cells=0
for path in sorted((R/'labs').glob('*.ipynb')):
 nb=json.loads(path.read_text());assert nb['nbformat']==4
 assert len({c['id'] for c in nb['cells']})==len(nb['cells'])
 cells=[''.join(c['source']) for c in nb['cells'] if c['cell_type']=='code']
 if not cells:manual_labs+=1;continue
 code_labs+=1;code_cells+=len(cells)
 runner='import matplotlib\nmatplotlib.use("Agg")\n'
 runner+='\n'.join(f'exec(compile({cell!r}, {str(path.name+":"+str(i+1))!r}, "exec"))' for i,cell in enumerate(cells))
 result=subprocess.run([sys.executable,'-c',runner],cwd=R,capture_output=True,text=True,timeout=120,env={**os.environ,'MPLBACKEND':'Agg'})
 assert result.returncode==0,f'{path.name}:\n{result.stderr}\n{result.stdout}'
 print('PASS',path.name)
print(f'Executed {code_cells} code cells in {code_labs} notebooks, each in a fresh Python process; {manual_labs} guided Desktop notebooks checked structurally only.')
