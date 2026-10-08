"""Reproducible synthetic teaching data. Never interpret as real business evidence."""
from pathlib import Path
import numpy as np
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]
D=ROOT/'datasets';D.mkdir(exist_ok=True)
rng=np.random.default_rng(399)
products=pd.DataFrame({'ProductKey':[1,2,3,4],'Product':['Laptop','Chair','Notebook','Mouse'],'Category':['Electronics','Furniture','Stationery','Electronics'],'UnitPrice':[800.,150.,5.,25.],'UnitCost':[500.,90.,2.,12.]})
regions=pd.DataFrame({'RegionKey':[1,2,3,4],'Region':['North','South','East','West']})
customers=pd.DataFrame({'CustomerKey':range(1,81),'Segment':['Consumer' if i%3 else 'Business' for i in range(1,81)]})
rows=[];oid=0
for date in pd.date_range('2022-01-01','2024-12-31'):
 for _ in range(2):
  oid+=1;region=int(rng.integers(1,5));customer=int(rng.integers(1,81))
  for line in range(1,int(rng.integers(2,5))):
   p=products.iloc[int(rng.integers(0,4))];q=int(rng.integers(1,7));discount=float(rng.choice([0,.05,.10,.15]));gross=round(q*p.UnitPrice,2);net=round(gross*(1-discount),2);cost=round(q*p.UnitCost,2)
   rows.append([f'O{oid:05d}',line,date.strftime('%Y-%m-%d'),int(p.ProductKey),customer,region,p.Product,p.Category,regions.iloc[region-1].Region,q,p.UnitPrice,discount,p.UnitCost,gross,net,cost,round(net-cost,2)])
cols=['OrderID','LineID','OrderDate','ProductKey','CustomerKey','RegionKey','Product','Category','Region','Quantity','UnitPrice','Discount','UnitCost','GrossRevenue','NetRevenue','TotalCost','Profit']
sales=pd.DataFrame(rows,columns=cols);sales.to_csv(D/'sales_multiyear.csv',index=False)
products.to_csv(D/'dim_product.csv',index=False);regions.to_csv(D/'dim_region.csv',index=False);customers.to_csv(D/'dim_customer.csv',index=False)
dates=pd.DataFrame({'Date':pd.date_range('2022-01-01','2024-12-31')});dates['Year']=dates.Date.dt.year;dates['Month']=dates.Date.dt.month;dates['MonthName']=dates.Date.dt.month_name();dates['Quarter']=dates.Date.dt.quarter;dates.to_csv(D/'dim_date.csv',index=False,date_format='%Y-%m-%d')
dirty=sales.iloc[:60].copy();dirty.loc[1,'Quantity']=np.nan;dirty.loc[3,'Quantity']=-2;north_indices=dirty.index[dirty.Region.eq('North')].tolist();dirty.loc[north_indices[0],'Region']=' north ';dirty.loc[north_indices[1],'Region']='NORTH';dirty.loc[6,'OrderDate']='not-a-date';dirty.loc[7,'Quantity']=100;dirty.loc[7,'GrossRevenue']=dirty.loc[7,'Quantity']*dirty.loc[7,'UnitPrice'];dirty.loc[7,'NetRevenue']=dirty.loc[7,'GrossRevenue']*(1-dirty.loc[7,'Discount']);dirty.loc[7,'TotalCost']=dirty.loc[7,'Quantity']*dirty.loc[7,'UnitCost'];dirty.loc[7,'Profit']=dirty.loc[7,'NetRevenue']-dirty.loc[7,'TotalCost'];dirty.loc[[1,3],['GrossRevenue','NetRevenue','TotalCost','Profit']]=np.nan;dirty=pd.concat([dirty,dirty.iloc[[2]]],ignore_index=True);dirty.to_csv(D/'dirty_sales.csv',index=False)
records=[]
for i in range(1800):
 date=pd.Timestamp('2022-01-01')+pd.Timedelta(days=int(rng.integers(0,1096)));vehicles=int(rng.integers(1,5));cas=int(rng.poisson(.5+vehicles*.3))
 records.append([f'A{i+1:05d}',date.strftime('%Y-%m-%d'),str(rng.choice(regions.Region)),str(rng.choice(['Clear','Rain','Fog'])),str(rng.choice(['Urban','Rural','Motorway'])),int(rng.choice([30,40,60,70])),vehicles,cas,'Serious' if cas>=3 else 'Slight'])
pd.DataFrame(records,columns=['accident_id','date','region','weather','road_type','speed_limit','vehicles','casualties','severity']).sort_values('date').to_csv(D/'accident_teaching.csv',index=False)
print(f'Generated {len(sales)} sales lines, {sales.OrderID.nunique()} orders; 61 dirty lines; 1800 accident records.')
