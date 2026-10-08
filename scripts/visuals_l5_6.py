from pathlib import Path
import csv,json,statistics,zipfile
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
plt.rcParams.update({'font.family':'DejaVu Sans','svg.fonttype':'none','font.size':11})
OUT=Path(__file__).resolve().parents[1]/"assets/visuals"
OUT.mkdir(parents=True,exist_ok=True)
NAVY='#183153';BLUE='#2563eb';TEAL='#0f766e';AMBER='#b7791f';RED='#b44444'
def save(fig,name):
 fig.savefig(OUT/('l5-6-'+name+'.svg'),bbox_inches='tight',facecolor='white')
 plt.close(fig)
def title(ax,t,sub):
 ax.set_title(t,loc='left',fontsize=19,fontweight='bold',color=NAVY,pad=28)
 ax.text(0,1.02,sub,transform=ax.transAxes,color='#526174',fontsize=10)
rows=[['S01','North',2,50],['S02',' north ',3,40],['S03','South',None,30],['S04','East',-2,80],['S05','West',4,25],['S06','North',100,500],['S07','South',1,60],['S02',' north ',3,40]]
flags=['OK','Normalize region','Quantity missing','Invalid quantity','OK','Large; verified valid','OK','Exact duplicate of row 2']
clean=[]
median=statistics.median([r[2] for i,r in enumerate(rows) if i!=7 and r[2] is not None and r[2]>=0])
assert median==3
for i,r in enumerate(rows):
 if i in [3,7]:continue
 id,region,q,p=r;miss=q is None;q=median if miss else q
 clean.append([id,region.strip().title(),q,p,q*p,str(miss)])
fig,axs=plt.subplots(3,1,figsize=(11,15),gridspec_kw={'height_ratios':[4,3.5,3]})
for a in axs:a.axis('off')
title(axs[0],'A · Before and after data cleaning','Synthetic sales · currency: USD · one row per transaction')
def table(ax,data,cols,widths):
 t=ax.table(cellText=data,colLabels=cols,cellLoc='left',colLoc='left',colWidths=widths,bbox=[0,.04,1,.86]);t.auto_set_font_size(False);t.set_fontsize(10)
 for (r,c),cell in t.get_celld().items():
  cell.set_edgecolor('#d6dee8');cell.set_facecolor('#eef2f7' if r==0 else ('#f8fafc' if r%2 else 'white'))
  if r==0:cell.set_text_props(color=NAVY,weight='bold')
 return t
raw=[[i+1,r[0],repr(r[1]),'Missing' if r[2] is None else r[2],r[3],flags[i]] for i,r in enumerate(rows)]
t=table(axs[0],raw,['Row','Sale ID','Region (raw)','Qty','Unit price','Issue flag'],[.06,.1,.16,.1,.12,.46])
for r in [3,4,8]:
 for c in range(6):t[(r,c)].set_facecolor('#fff7df' if r!=4 else '#fff0f0')
axs[1].text(0,.98,'Cleaned analytical result · 6 accepted transactions',weight='bold',color=TEAL,fontsize=14)
table(axs[1],clean,['Sale ID','Region','Qty','Unit price','Revenue','Qty was missing'],[.12,.16,.08,.15,.17,.32])
axs[2].text(0,.97,'Decision log',weight='bold',color=NAVY,fontsize=14)
log=['Row 8: remove the exact duplicate; retain original row 2.', 'Rows 2 / 8: trim whitespace and normalize region to North.', 'Row 4: quarantine negative quantity; no verified correction is available.', 'Row 3: impute quantity = 3; preserve Qty was missing = True.', 'Median donors: accepted, unique observed quantities [2, 3, 4, 100, 1].', 'Row 6: retain verified large transaction; revenue = 100 × $500 = $50,000.', 'Preserve the eight raw records and this decision log for auditability.']
for i,s in enumerate(log):axs[2].text(0,.82-i*.105,s,color=RED if i==2 else NAVY,fontsize=11)
axs[2].text(0,.02,'Assumption: median imputation is a teaching baseline, not a universal remedy for missing data.',fontsize=10,color=AMBER)
fig.subplots_adjust(hspace=.25);save(fig,'A_data_cleaning')
with open(OUT/'l5-6-raw_sales.csv','w') as f:
 w=csv.writer(f);w.writerow(['SaleID','Region','Quantity','UnitPriceUSD']);w.writerows(rows)
with open(OUT/'l5-6-clean_sales.csv','w') as f:
 w=csv.writer(f);w.writerow(['SaleID','Region','Quantity','UnitPriceUSD','RevenueUSD','QuantityWasMissing']);w.writerows(clean)
# Mechanism diagrams: arrows encode dependence, not causal effects on income.
fig,axs=plt.subplots(3,1,figsize=(9,12))
def box(ax,x,y,label,color):
 ax.text(x,y,label,ha='center',va='center',fontsize=12,color=color,bbox=dict(boxstyle='round,pad=.7',fc='white',ec=color,lw=1.8))
def arrow(ax,a,b):ax.annotate('',xy=b,xytext=a,arrowprops={'arrowstyle':'->','color':NAVY,'lw':1.8})
for ax in axs:ax.axis('off');ax.set_xlim(0,1);ax.set_ylim(0,1)
axs[0].set_title('B · Why patient income is missing',loc='left',color=NAVY,fontsize=19,weight='bold',pad=25)
axs[0].text(0,1.03,'Illustrative mechanisms · arrows show reporting dependence',fontsize=10,color='#526174')
for ax,head in zip(axs,['MCAR · Random loss','MAR · Depends on observed age','MNAR · Depends on unreported income']):ax.text(0,.9,head,color=NAVY,weight='bold',fontsize=14)
box(axs[0],.22,.62,'Random record loss',BLUE);box(axs[0],.76,.62,'Income not reported',AMBER);arrow(axs[0],(.43,.62),(.57,.62))
axs[0].text(.02,.23,'Loss is unrelated to observed age and true income.\nExample: a random transmission failure removes income entries.',color=NAVY,fontsize=11)
box(axs[1],.22,.62,'Observed age',BLUE);box(axs[1],.76,.62,'Income reporting',AMBER);arrow(axs[1],(.4,.62),(.57,.62))
axs[1].text(.02,.23,'Example: older patients report income less often.\nWithin a fixed age, reporting probability does not depend on income.',color=NAVY,fontsize=11)
box(axs[2],.22,.62,'True income\n(unobserved if missing)',BLUE);box(axs[2],.76,.62,'Income reporting',AMBER);arrow(axs[2],(.46,.62),(.57,.62))
axs[2].text(.02,.23,'Example: high-income patients report income less often,\neven after accounting for observed age.',color=NAVY,fontsize=11)
fig.text(.1,.025,'A heatmap shows missingness patterns; it cannot establish MAR versus MNAR.\nThese examples specify mechanisms rather than diagnose a real dataset.',fontsize=11,color=RED)
fig.subplots_adjust(hspace=.35,bottom=.1);save(fig,'B_missingness_mechanisms')
# Numerical charts and boxplot calculations.
a=np.array([10,12,13,14,15]);b=np.append(a,100)
def boxstats(x):
 q1,q2,q3=np.percentile(x,[25,50,75],method='linear');iqr=q3-q1;lo=q1-1.5*iqr;hi=q3+1.5*iqr;inside=x[(x>=lo)&(x<=hi)]
 return dict(q1=float(q1),med=float(q2),q3=float(q3),whislo=float(min(inside)),whishi=float(max(inside)),fliers=list(map(float,x[(x<lo)|(x>hi)])),lower_fence=float(lo),upper_fence=float(hi))
s=boxstats(b);assert s['q1']==12.25 and s['q3']==14.75 and s['whishi']==15
fig,axs=plt.subplots(3,1,figsize=(10,12),gridspec_kw={'height_ratios':[2,2,3]})
for ax,x,heading,meanlabel,medlabel in zip(axs[:2],[a,b],['Original: [10, 12, 13, 14, 15]','Append 100: [10, 12, 13, 14, 15, 100]'],['Mean = 64/5 = 12.8','Mean = 164/6 = 82/3 = 27⅓'],['Median = 13','Median = (13 + 14)/2 = 13.5']):
 ax.scatter(x,np.zeros(len(x)),s=75,color=BLUE,zorder=3,label='Observations');ax.axvline(x.mean(),color=RED,lw=2,label=meanlabel);ax.axvline(np.median(x),color=TEAL,lw=2,ls='--',label=medlabel)
 ax.set_xlim(0,110);ax.set_ylim(-.4,.6);ax.set_yticks([]);ax.set_title(heading,loc='left',color=NAVY,fontsize=13,weight='bold');ax.set_xlabel('Value (unitless)');ax.legend(loc='upper right',fontsize=10)
 for spine in ['left','right','top']:ax.spines[spine].set_visible(False)
ax=axs[2];ax.bxp([s],positions=[1],vert=False,showfliers=True,patch_artist=True,boxprops={'facecolor':'#e6f7f3','edgecolor':TEAL},medianprops={'color':TEAL,'linewidth':2},flierprops={'marker':'o','markerfacecolor':RED,'markeredgecolor':RED},widths=.3)
for v,l in [(s['lower_fence'],'Lower fence 8.5'),(s['upper_fence'],'Upper fence 18.5')]:ax.axvline(v,color=AMBER,ls=':',lw=2,label=l)
ax.set_xlim(0,110);ax.set_ylim(.4,1.7);ax.set_yticks([]);ax.set_xlabel('Value (unitless)');ax.set_title('Separate boxplot · augmented data',loc='left',color=NAVY,fontsize=14,weight='bold');ax.legend(loc='upper right',fontsize=10)
ax.text(.02,.05,'Q1 = 12.25; median = 13.5; Q3 = 14.75; IQR = 2.5\nActual whisker endpoints: 10 and 15. Outlier: 100.',transform=ax.transAxes,color=NAVY,fontsize=11,bbox={'facecolor':'white','edgecolor':'none','alpha':1})
fig.suptitle('C · One extreme observation shifts the mean',x=.125,ha='left',color=NAVY,fontsize=19,weight='bold')
fig.text(.125,.025,'Convention: NumPy linear percentiles (Hyndman–Fan type 7).\nFences = Q1 − 1.5×IQR and Q3 + 1.5×IQR; whiskers end at observed values within fences.',fontsize=10,color=NAVY)
fig.subplots_adjust(hspace=.75,top=.90,bottom=.12);save(fig,'C_mean_median_boxplot')
json.dump({'original_mean':64/5,'augmented_mean':164/6,'original_median':13,'augmented_median':13.5,'augmented_boxplot':s},open(OUT/'l5-6-calculations.json','w'),indent=2)

# Normalize editable text outputs for clean, portable Git patches.
for asset in OUT.glob("l5-6-*"):
 if asset.suffix in [".svg",".csv",".json"]:
  asset.write_text("\n".join(line.rstrip() for line in asset.read_text().splitlines())+"\n")
