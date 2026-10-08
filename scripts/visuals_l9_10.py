from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures,StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import json,csv
P=Path(__file__).resolve().parents[1]/"assets/visuals"
P.mkdir(parents=True,exist_ok=True)
plt.rcParams.update({'font.family':'DejaVu Sans','svg.fonttype':'none','font.size':11})
N='#183153';B='#2563eb';T='#0f766e';R='#b44444';A='#b7791f'
def save(fig,n):
 for ext in ['svg']:fig.savefig(P/('l9-10-'+n+'.'+ext),bbox_inches='tight',dpi=170,facecolor='white')
 plt.close(fig)
fig,axs=plt.subplots(4,1,figsize=(11,10));fig.suptitle('A · Match the split to the data structure',x=.12,ha='left',fontsize=19,weight='bold',color=N)
patterns=[('Random · independent records',['R'+str(i+1) for i in range(12)],[0,0,1,0,1,0,0,1,0,0,0,0],'Random assignment is appropriate only when records are independent.'),('Stratified · preserve class proportions',['0']*8+['1']*4,[0,0,1,0,0,1,0,0,0,1,0,0],'Example: train 6 class-0 + 3 class-1; test 2 class-0 + 1 class-1.'),('Grouped · keep patients separate',['P1']*3+['P2']*3+['P3']*3+['P4']*3,[0]*9+[1]*3,'All records from a patient remain in one split; group sizes can differ.'),('Chronological · past predicts future',['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'],[0]*9+[1]*3,'Train on earlier dates; evaluate later. Prevent look-ahead in features.')]
for ax,(head,labs,mask,note) in zip(axs,patterns):
 ax.axis('off');ax.set_xlim(-.7,12);ax.set_ylim(-.65,1.7);ax.text(-.5,1.25,head,color=N,weight='bold',fontsize=14)
 for i,(lab,split) in enumerate(zip(labs,mask)):
  ax.barh(.45,.8,left=i,color=T if split else B,height=.6,hatch='///' if split else None,edgecolor='white');ax.text(i+.4,.45,lab,ha='center',va='center',color='white',fontsize=10)
 ax.text(-.5,-.4,note,color=N,fontsize=10)
fig.text(.12,.025,'Blue = TRAIN · Teal = HELD-OUT TEST. Synthetic schematic; examples use 9 training and 3 test records.\nStratification does not prevent patient leakage or future-information leakage.',color=N,fontsize=10)
fig.subplots_adjust(top=.9,bottom=.13,hspace=.55);save(fig,'A_split_comparison')
fig,ax=plt.subplots(figsize=(10,13));ax.axis('off');ax.set_xlim(0,1);ax.set_ylim(0,1)
ax.text(0,1.01,'B · A safe predictive workflow',fontsize=19,weight='bold',color=N)
def box(x,y,s,c=N,w=14):ax.text(x,y,s,ha='center',va='center',fontsize=w,color=c,bbox={'boxstyle':'round,pad=.65','fc':'white','ec':c,'lw':1.8})
def arrow(a,b,c=N,dash=False):ax.annotate('',xy=b,xytext=a,arrowprops={'arrowstyle':'->','color':c,'lw':2,'linestyle':'--' if dash else '-'})
box(.5,.92,'Split using the correct strategy')
box(.25,.79,'Training partition',B);box(.76,.79,'Held-out test\nKeep untouched',T)
arrow((.47,.865),(.25,.825));arrow((.53,.865),(.76,.84))
box(.32,.66,'Training-side validation loop\nFit preprocessing on fold-training only\nTransform fold-training and validation\nTrain and compare candidates',B,w=12);arrow((.25,.765),(.30,.72))
box(.32,.51,'Choose recipe using validation\nRefit preprocessing on all training data',B,w=12);arrow((.32,.595),(.32,.555))
box(.32,.39,'Transform training → train final model',B,w=12);arrow((.32,.48),(.32,.425))
box(.70,.27,'Transform held-out test\nusing final training-fitted preprocessing',T,w=12);arrow((.32,.36),(.67,.31));arrow((.97,.74),(.97,.32),T)
box(.5,.14,'Predict and evaluate once\nReport held-out error and limitations',T,w=13);arrow((.68,.235),(.54,.185))
box(.78,.52,'LEAKAGE\nFit on test data',R,w=11);arrow((.74,.49),(.53,.52),R,True)
ax.text(.61,.58,'Do not use test values to fit\nimputers, scalers, or encoders.',color=R,fontsize=10)
arrow((.05,.095),(.14,.35),R,True)
ax.text(0,.065,'LEAKAGE: features built from future outcomes or later observations.',color=R,weight='bold',fontsize=11)
ax.text(0,.025,'Solid arrows = approved workflow. Red dashed arrow = prohibited leakage path.\nFuture-derived features are excluded before any training or evaluation.',color=N,fontsize=10)
save(fig,'B_safe_workflow')
# Prespecified models: compare capacity without test-guided tuning.
rng=np.random.default_rng(42)
x=np.linspace(-3,3,24);y=.7*x*x-.5*x+1+rng.normal(0,.65,len(x))
xt=rng.uniform(-3,3,400);yt=.7*xt*xt-.5*xt+1+rng.normal(0,.65,len(xt))
grid=np.linspace(-3,3,600);degrees=[1,2,15];results=[];preds=[]
for d in degrees:
 model=make_pipeline(PolynomialFeatures(d,include_bias=False),StandardScaler(),LinearRegression())
 model.fit(x[:,None],y)
 train_mse=float(np.mean((model.predict(x[:,None])-y)**2));test_mse=float(np.mean((model.predict(xt[:,None])-yt)**2));results.append({'degree':d,'train_mse':train_mse,'heldout_mse':test_mse});preds.append(model.predict(grid[:,None]))
fig,axs=plt.subplots(3,1,figsize=(10,14),sharex=True,sharey=True)
labels=['Underfitting · linear model (degree 1)','Appropriate capacity · quadratic (degree 2)','Overfitting · flexible polynomial (degree 15)']
for ax,label,res,pred in zip(axs,labels,results,preds):
 ax.scatter(x,y,color=B,s=32,label='Same 24 training observations',zorder=3);ax.plot(grid,.7*grid**2-.5*grid+1,color='#748294',ls='--',label='Known synthetic mean');ax.plot(grid,pred,color=T,lw=2,label='Fitted model')
 ax.set_title(label,loc='left',fontsize=14,weight='bold',color=N);ax.text(.03,.96,f'Training MSE = {res["train_mse"]:.4f}\nHeld-out MSE = {res["heldout_mse"]:.4f}',transform=ax.transAxes,va='top',bbox={'fc':'white','ec':'#d6dee8'},color=N);ax.set_ylabel('Synthetic target y');ax.set_ylim(-2,12);ax.grid(alpha=.18);ax.legend(loc='upper right',fontsize=9)
axs[-1].set_xlabel('Synthetic predictor x');fig.suptitle('C · Model capacity and generalization',x=.125,ha='left',fontsize=19,weight='bold',color=N)
fig.text(.125,.025,'Seed 42 · y = 0.7x² − 0.5x + 1 + noise; noise SD = 0.65.\n400 independent held-out observations; MSE = mean squared error (squared target units).\nDegrees were specified before evaluation. This capacity demonstration is not a tuning procedure.\nDisplayed y-axis is fixed at [−2, 12]; extreme curve segments may extend outside it.',fontsize=10,color=N)
fig.subplots_adjust(top=.92,bottom=.15,hspace=.3);save(fig,'C_regression_capacity')
json.dump(results,open(P/'l9-10-metrics.json','w'),indent=2)
for name,xx,yy in [('training_data.csv',x,y),('heldout_data.csv',xt,yt)]:
 with open(P/('l9-10-'+name),'w') as f:
  w=csv.writer(f);w.writerow(['x','y']);w.writerows(zip(xx,yy))
print(json.dumps(results))

# Normalize editable text outputs for clean, portable Git patches.
for asset in P.glob("l9-10-*"):
 if asset.suffix in [".svg",".csv",".json"]:
  asset.write_text("\n".join(line.rstrip() for line in asset.read_text().splitlines())+"\n")
