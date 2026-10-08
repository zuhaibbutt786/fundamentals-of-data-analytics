from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from datetime import date
import json
P=Path(__file__).resolve().parents[1]/"assets/visuals"
P.mkdir(parents=True,exist_ok=True)
plt.rcParams.update({'font.family':'DejaVu Sans','svg.fonttype':'none','font.size':11})
N='#183153';B='#2563eb';T='#0f766e';A='#b7791f'
def table(ax,rows,labels,bbox,widths=None):
 tb=ax.table(cellText=rows,colLabels=labels,cellLoc='center',bbox=bbox,colWidths=widths);tb.auto_set_font_size(False);tb.set_fontsize(11)
 for (r,c),cell in tb.get_celld().items():
  cell.set_edgecolor('#d5dee8');cell.set_facecolor('#eef2f7' if r==0 else ('#f7fafc' if r%2 else 'white'))
  if r==0:cell.set_text_props(weight='bold',color=N)
 return tb
def start(name,sub,height=9):
 fig,ax=plt.subplots(figsize=(11,height));ax.axis('off');ax.set_xlim(0,1);ax.set_ylim(0,1)
 ax.text(0,1.01,name,fontsize=19,weight='bold',color=N);ax.text(0,.965,sub,fontsize=11,color='#526174');return fig,ax
def arrow(ax,a,b,label=None):
 ax.annotate('',xy=b,xytext=a,arrowprops={'arrowstyle':'->','color':N,'lw':2})
 if label:ax.text((a[0]+b[0])/2,(a[1]+b[1])/2+.02,label,ha='center',color=N,fontsize=10,bbox={'facecolor':'white','edgecolor':'none','pad':3})
def save(fig,name):
 for ext in ['svg']:fig.savefig(P/('l7-8-'+name+'.'+ext),bbox_inches='tight',dpi=170,facecolor='white')
 plt.close(fig)
x=np.array([10,20,30,40,100],dtype=float);mean=x.mean();var=x.var(ddof=0);sd=x.std(ddof=0);z=(x-mean)/sd;mm=(x-10)/90;logs=np.log1p(x)
assert mean==40 and var==1000
fig,ax=start('A · Same observations, different representations','Synthetic unitless values · standard deviation uses ddof = 0',11)
rows=[]
for v,m,s,l in zip(x,mm,z,logs):
 exactm={10:'0',20:'1/9',30:'2/9',40:'1/3',100:'1'}[int(v)]
 exactz={10:'−3/√10',20:'−2/√10',30:'−1/√10',40:'0',100:'6/√10'}[int(v)]
 rows.append([str(int(v)),exactm+'\n≈ '+f'{m:.6f}',exactz+'\n≈ '+f'{s:.6f}',f'ln({int(v)+1})\n≈ {l:.6f}'])
table(ax,rows,['Original x','Min–max','Standardized z','log1p(x)'],[0,.55,1,.35],[.16,.26,.29,.29])
ax.text(0,.48,'Computed parameters',color=N,weight='bold',fontsize=14)
ax.text(0,.43,'Mean = 40; population variance = 1000; SD = √1000 = 10√10.',color=N)
ax.text(0,.38,'Min–max = (x − 10)/90     z = (x − 40)/(10√10)     log1p(x) = ln(1 + x)',color=N)
# normalized axis coordinates demonstrate identical relative spacing under affine changes.
for y,lab,ticks in [(.28,'Original',['10','20','30','40','100']),(.18,'Standardized',['−3/√10','−2/√10','−1/√10','0','6/√10'])]:
 ax.text(0,y,lab,color=N,weight='bold');positions=.2+.75*mm
 ax.plot([.2,.95],[y,y],color='#c5cfdb');ax.scatter(positions,np.full(5,y),color=B if lab=='Original' else T,s=45,zorder=3)
 for pos,tick in zip(positions,ticks):ax.text(pos,y-.038,tick,ha='center',fontsize=9,color=N)
ax.text(0,.075,'Aligned relative spacing: standardization changes the origin and scale, not shape.',color=T,weight='bold')
ax.text(0,.03,'Standardized mean = 0 and variance = 1. Standardization does not make data normal.',color=A)
save(fig,'A_transformations')
fig,ax=start('B · An unseen value can exceed the fitted range','Fit on training values [10, 20, 30, 40, 100]; clipping is disabled',7)
table(ax,[['10','100','(x − 10)/90']],['Training minimum','Training maximum','Fitted transformation'],[0,.66,1,.2])
arrow(ax,(.5,.63),(.5,.5),'Apply unchanged to unseen data')
table(ax,[['120','(120 − 10)/90 = 11/9','1.222222…']],['Unseen x','Exact transformed value','Decimal representation'],[0,.29,1,.2],[.22,.48,.3])
ax.text(0,.2,'120 is greater than the training maximum of 100, so its scaled value exceeds 1.',color=T,weight='bold')
ax.text(0,.12,'Do not refit using the test observation. That would leak test information.',color=A)
ax.text(0,.045,'Optional clipping gives 1, but hides how far the observation lies beyond the training range.',color=N)
save(fig,'B_unseen_minmax')
fig,ax=start('C · Ordered categories versus unordered regions','Use explicit category meaning; integer codes do not create meaningful distances',10)
ax.text(0,.88,'Ordered severity: Low < Medium < High',fontsize=14,color=N,weight='bold')
table(ax,[['Low'],['Medium'],['High']],['Severity'],[0,.55,.3,.25])
arrow(ax,(.33,.675),(.55,.675),'Explicit mapping')
table(ax,[['Low','0'],['Medium','1'],['High','2']],['Category','Ordinal code'],[.58,.55,.42,.25])
ax.text(0,.49,'Codes preserve rank; equal severity gaps are not established by the coding.',color=A)
ax.text(0,.40,'Unordered regions: North, South, East, West',fontsize=14,color=N,weight='bold')
table(ax,[['North'],['South'],['East'],['West']],['Region'],[0,.12,.21,.23])
arrow(ax,(.23,.235),(.38,.235))
table(ax,[['North','1','0','0','0'],['South','0','1','0','0'],['East','0','0','1','0'],['West','0','0','0','1']],['Region','North','South','East','West'],[.40,.12,.60,.23])
ax.text(0,.055,'Arbitrary North=0, South=1, East=2, West=3 may imply order or distance to a model.',color=A)
ax.text(0,.01,'One-hot columns indicate membership. Handle unseen regions explicitly at inference.',color=N)
save(fig,'C_encoding')
fig,ax=start('D · A transaction becomes useful features','Synthetic sale · currency: USD · Discount is a fraction of gross revenue',12)
example_date=date(2024,1,8);assert example_date.strftime('%A')=='Monday'
table(ax,[['Quantity','3'],['UnitPrice','200 USD/unit'],['Discount','0.10 (10%)'],['UnitCost','120 USD/unit'],['OrderDate','2024-01-08 (assumed example)']],['Raw field','Value'],[0,.62,.95,.28],[.3,.65])
arrow(ax,(.475,.60),(.475,.51),'Apply documented feature formulas')
rows=[['Gross revenue','Quantity × UnitPrice','600 USD'],['Net revenue','Gross revenue × (1 − Discount)','540 USD'],['Total cost','Quantity × UnitCost','360 USD'],['Profit','Net revenue − Total cost','180 USD'],['Profit margin','Profit / Net revenue','1/3 = 33⅓%'],['Month','OrderDate.month','1 (January)'],['Weekday','OrderDate.weekday()','0 (Monday)']]
table(ax,rows,['Feature','Formula','Result'],[0,.12,1,.37],[.23,.48,.29])
ax.text(0,.075,'Assumptions: all units sold; no returns, tax, shipping, or other costs are included.',color=N,fontsize=10)
ax.text(0,.03,'Prediction-time caution: use only information available when the prediction is made.',color=A,weight='bold',fontsize=11)
ax.text(0,-.01,'Final profit, future sales, and later returns must not become inputs to an earlier prediction.',color=A,fontsize=10)
save(fig,'D_feature_engineering')
json.dump({'input':x.tolist(),'mean':float(mean),'variance_ddof0':float(var),'sd':float(sd),'minmax':mm.tolist(),'standardized':z.tolist(),'log1p':logs.tolist(),'unseen_120_scaled':11/9,'features':{'gross_revenue':600,'net_revenue':540,'total_cost':360,'profit':180,'margin':1/3,'example_date':'2024-01-08','month':1,'weekday':0}},open(P/'l7-8-calculations.json','w'),indent=2)

# Normalize editable text outputs for clean, portable Git patches.
for asset in P.glob("l7-8-*"):
 if asset.suffix in [".svg",".csv",".json"]:
  asset.write_text("\n".join(line.rstrip() for line in asset.read_text().splitlines())+"\n")
