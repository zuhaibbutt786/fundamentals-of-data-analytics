"""Build complete teaching notebooks with local inputs and reference solutions."""
from pathlib import Path
import json
R=Path(__file__).resolve().parents[1];L=R/'labs'
def md(s):return {'cell_type':'markdown','metadata':{},'source':s.splitlines(True)}
def code(s):return {'cell_type':'code','metadata':{},'execution_count':None,'outputs':[],'source':s.splitlines(True)}
setup='''from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
ROOT = Path.cwd() if (Path.cwd() / "datasets").exists() else Path.cwd().parent
assert (ROOT / "datasets").exists(), "Run from the repository root or labs directory; in Colab upload/clone the repository first."
DATA = ROOT / "datasets"
'''
def build(file,title,goals,parts,exercise,solution=None,needs_setup=True):
 cells=[md(f'# {title}\n\n{goals}\n\n**Environment:** See ../requirements.txt and the labs index. Examples use bundled inputs; no internet is required after dependency installation. Synthetic data is for teaching only.' )]
 if needs_setup:cells.append(code(setup))
 for text,src in parts:
  cells.append(md(text))
  if src:cells.append(code(src))
 cells.append(md('## Student task\n'+exercise))
 if solution:cells.extend([md('## Reference solution\nTry the task before reading this cell.'),code(solution)])
 cells.append(md('## Interpretation and limitations\nRecord the dataset grain, units, assumptions, and a limitation in your submission. Explain one result rather than only submitting screenshots.'))

 for i,cell in enumerate(cells):cell['id']=f'cell-{i:03d}'
 obj={'cells':cells,'metadata':{'kernelspec':{'display_name':'Python 3','language':'python','name':'python3'},'language_info':{'name':'python','version':'3.11'}},'nbformat':4,'nbformat_minor':5}
 (L/file).write_text(json.dumps(obj,indent=1))
build('L2_Python_Basics_Comprehensive_Lab.ipynb','L2 supplement: Python foundations','Learn variables, lists, slicing, dictionaries, functions, loops, and simple assertions.', [('## Basic Python types and slicing','''records = [10, 20, 30, 40]
record = {"quantity": 3, "unit_price": 200}
def revenue(quantity, price):
    return quantity * price
print(records[1:3], revenue(record["quantity"], record["unit_price"]))
for value in records:
    if value >= 30:
        print("large", value)
assert revenue(3, 200) == 600''')], 'Write a function that returns net revenue after a fractional discount.', '''def net_revenue(quantity, price, discount):
    assert 0 <= discount <= 1
    return quantity * price * (1-discount)
assert net_revenue(3,200,.1) == 540
print(net_revenue(3,200,.1))''')
build('L3_Python_Data_Structures_Guide.ipynb','L3 supplement: Pandas and safe joins','Read tables, filter with .loc, clean strings, append compatible tables, and validate joins.', [('## Selection and string normalization','''sales = pd.read_csv(DATA / "sales_multiyear.csv", parse_dates=["OrderDate"])
print(sales.loc[sales["Quantity"] >= 5, ["OrderID", "Quantity"]].head())
print(pd.Series([" North ", "SOUTH"]).str.strip().str.title())'''),('## Join cardinality and row-count protection','''products = pd.read_csv(DATA / "dim_product.csv")
joined = sales[["OrderID","LineID","ProductKey"]].merge(products, on="ProductKey", how="left", validate="many_to_one", indicator=True)
assert len(joined) == len(sales)
assert joined["_merge"].eq("both").all()
print(joined.head())
appended = pd.concat([sales.iloc[:3],sales.iloc[3:6]],ignore_index=True)
assert len(appended) == 6''')], 'What would happen if the product dimension contained duplicate ProductKey values?', '''duplicate_dim = pd.concat([products,products.iloc[[0]]])
try:
    sales.merge(duplicate_dim,on="ProductKey",validate="many_to_one")
except pd.errors.MergeError as error:
    print("Expected validation failure:",error)''')
build('L3_Data_Acquisition_and_Scraping.ipynb','L3: Acquisition and structured extraction','Load local CSV/JSON and extract a local HTML table. This is a deterministic demonstration, not permission to scrape arbitrary sites.', [('## Load and profile a bundled source','''sales = pd.read_csv(DATA / "sample_sales.csv")
print(sales.shape, sales.dtypes, sales.head(), sep="\\n")'''),('## JSON records and nested fields','''import json
payload = '{"orders":[{"id":1,"customer":{"region":"North"},"qty":3}]}'
parsed = json.loads(payload)
flat = pd.json_normalize(parsed["orders"])
print(flat)'''),('## Parse an HTML table without a live website','''from io import StringIO
html = "<table><tr><th>Product</th><th>Price</th></tr><tr><td>Mouse</td><td>25</td></tr></table>"
table = pd.read_html(StringIO(html))[0]
assert table.loc[0,"Price"] == 25
print(table)'''),('## Responsible network acquisition',None)], 'Before a real HTTP request, document purpose, source permission, privacy, terms, rate limits, retries, and the availability of an official API. robots.txt is not legal authorization. Never commit credentials. Save raw responses and retrieval timestamps.')
build('L4_Analytical_Thinking_Practical_Lab.ipynb','L4: From a decision to a KPI','Define a decision, numerator, denominator, time window, and grain before calculating.', [('## A regional operations question','''sales = pd.read_csv(DATA / "sales_multiyear.csv",parse_dates=["OrderDate"])
period = sales.loc[sales.OrderDate.between("2024-01-01","2024-03-31")]
summary = period.groupby("Region").agg(net_revenue=("NetRevenue","sum"),profit=("Profit","sum"),orders=("OrderID","nunique"))
summary["margin"] = summary.profit / summary.net_revenue
print(summary.round(2))''')], 'Which region would you investigate? Separate a descriptive finding from a causal claim. Is margin per line equivalent to ratio of total profit to total revenue?', '''weighted_margin = period.Profit.sum()/period.NetRevenue.sum()
unweighted = (period.Profit/period.NetRevenue).mean()
print("Portfolio margin:",weighted_margin,"Mean line margin:",unweighted)''')
build('L5_Data_Quality_and_Profiling.ipynb','L5: Dirty data and missing-value flags','Profile a deliberately dirty synthetic extract. Preserve raw records, separate quarantine, and create indicators before imputation.', [('## Profile and identify issues','''raw = pd.read_csv(DATA / "dirty_sales.csv")
print(raw.isna().sum())
print("Exact duplicates:",raw.duplicated().sum())
assert raw.Quantity.isna().sum() == 1
assert raw.duplicated().sum() == 1'''),('## Clean without erasing the audit trail','''df = raw.drop_duplicates().copy()
df["Region"] = df.Region.str.strip().str.title()
df["OrderDate"] = pd.to_datetime(df.OrderDate,errors="coerce")
invalid = (df.Quantity < 0) | df.OrderDate.isna()
quarantine = df.loc[invalid].copy()
clean = df.loc[~invalid].copy()
clean["QuantityWasMissing"] = clean.Quantity.isna()
median = clean.Quantity.median()
clean["Quantity"] = clean.Quantity.fillna(median)
clean["GrossRevenue"] = clean.Quantity * clean.UnitPrice
clean["NetRevenue"] = clean.GrossRevenue * (1-clean.Discount)
clean["TotalCost"] = clean.Quantity * clean.UnitCost
clean["Profit"] = clean.NetRevenue-clean.TotalCost
assert clean.QuantityWasMissing.sum() == 1
assert clean.Quantity.eq(100).any()
print("Accepted",len(clean),"quarantined",len(quarantine),"median baseline",median)
print(clean.loc[clean.QuantityWasMissing,["OrderID","Quantity","QuantityWasMissing"]])'''),('## Missingness interpretation',None)], 'Explain why the indicator survives filling. Compare results without the imputed row. Do not claim MAR or MNAR is established by observed patterns. The median is a descriptive teaching baseline; prediction uses train-fitted imputers and inference needs uncertainty-aware methods.', '''print("Revenue sensitivity:",clean.NetRevenue.sum(),clean.loc[~clean.QuantityWasMissing,"NetRevenue"].sum())''')
build('L6_Outliers_and_Noise_Lab.ipynb','L6: Outliers and robust summaries','Use explicit analytical features and retain valid large transactions.', [('## Compute fences and actual whisker endpoints','''x = np.array([10,12,13,14,15,100],dtype=float)
q1,q3 = np.percentile(x,[25,75],method="linear")
iqr = q3-q1
low,high = q1-1.5*iqr,q3+1.5*iqr
inside=x[(x>=low)&(x<=high)]
print("Q1,Q3,IQR:",q1,q3,iqr,"fences",low,high,"whiskers",inside.min(),inside.max())
assert (q1,q3,low,high)==(12.25,14.75,8.5,18.5)
plt.boxplot(x,orientation="horizontal");plt.xlabel("Unitless value");plt.show()'''),('## Investigate a measurement, not an identifier','''df = pd.read_csv(DATA / "sales_multiyear.csv")
s = df["NetRevenue"]
q1,q3=s.quantile([.25,.75]);iqr=q3-q1
flags=(s<q1-1.5*iqr)|(s>q3+1.5*iqr)
print("Candidate lines:",flags.sum());print(df.loc[flags,["OrderID","Product","NetRevenue"]].head())''')], 'Compare mean and median with and without 100. Why does a flagged point still need domain review?', '''before=x[:-1]
print("Mean before/after:",before.mean(),x.mean())
print("Median before/after:",np.median(before),np.median(x))''')
build('L7_Data_Transformation_Lab.ipynb','L7: Scaling and encoding','Calculate transformations and verify train-fitted behavior.', [('## Exact example with ddof=0','''from sklearn.preprocessing import StandardScaler,MinMaxScaler,OrdinalEncoder,OneHotEncoder
x=np.array([10,20,30,40,100],dtype=float).reshape(-1,1)
z=StandardScaler().fit_transform(x)
scaler=MinMaxScaler().fit(x)
print(pd.DataFrame({"x":x.ravel(),"minmax":scaler.transform(x).ravel(),"z":z.ravel(),"log1p":np.log1p(x).ravel()}))
assert np.isclose(z.std(ddof=0),1)
assert np.isclose(scaler.transform([[120]])[0,0],11/9)
print("Unseen 120:",scaler.transform([[120]]))'''),('## Explicit categories and unknown input policy','''severity=OrdinalEncoder(categories=[["Low","Medium","High"]],handle_unknown="use_encoded_value",unknown_value=-1)
print(severity.fit_transform(np.array(["Low","High","Medium"]).reshape(-1,1)))
regions=OneHotEncoder(handle_unknown="ignore",sparse_output=False)
regions.fit(np.array(["North","South","East","West"]).reshape(-1,1))
print(regions.get_feature_names_out(),regions.transform([["North"],["Unknown"]]))
print("Unknown all-zero row needs monitoring; it does not mean a known region.")''')], 'Explain why standardization preserves shape. Compare population and sample SD on standardized values.', '''print(z.std(ddof=0),z.std(ddof=1))''')
build('L8_Feature_Engineering_Lab.ipynb','L8: Financial and temporal features','Derive features with documented formulas and prediction-time availability.', [('## Transaction features','''sale=pd.DataFrame({"Quantity":[3],"UnitPrice":[200],"Discount":[.10],"UnitCost":[120],"OrderDate":["2024-01-08"]})
sale["GrossRevenue"]=sale.Quantity*sale.UnitPrice
sale["NetRevenue"]=sale.GrossRevenue*(1-sale.Discount)
sale["TotalCost"]=sale.Quantity*sale.UnitCost
sale["Profit"]=sale.NetRevenue-sale.TotalCost
sale["ProfitMargin"]=sale.Profit/sale.NetRevenue
sale["OrderDate"]=pd.to_datetime(sale.OrderDate)
sale["Month"]=sale.OrderDate.dt.month
sale["Weekday"]=sale.OrderDate.dt.day_name()
assert sale.Profit.iloc[0]==180
print(sale.T)'''),('## Past-only customer feature','''df=pd.read_csv(DATA / "sales_multiyear.csv",parse_dates=["OrderDate"])
daily=df.groupby(["CustomerKey","OrderDate"],as_index=False).NetRevenue.sum().sort_values(["CustomerKey","OrderDate"])
daily["PreviousCustomerDayRevenue"]=daily.groupby("CustomerKey").NetRevenue.shift(1)
daily["PreviousObservedDate"]=daily.groupby("CustomerKey").OrderDate.shift(1)
assert (daily.PreviousObservedDate.dropna() < daily.loc[daily.PreviousObservedDate.notna(),"OrderDate"]).all()
print(daily.head())
# Previous observed customer day, not necessarily yesterday; excludes same-day information.
''')], 'Give one feature unavailable when predicting an order before checkout. Create price bands with explicit inclusive boundaries.', '''df["PriceBand"]=pd.cut(df.UnitPrice,[0,25,200,np.inf],labels=["Budget","Mid","Premium"],include_lowest=True)
print(df.PriceBand.value_counts())''')
build('L9_Splitting_and_Validation_Lab.ipynb','L9: Splitting and validation','Compare independent, stratified, grouped, and chronological partitions.', [('## Splits with explicit guarantees','''from sklearn.model_selection import train_test_split,GroupShuffleSplit,TimeSeriesSplit
ids=np.arange(40);labels=np.tile([0,0,0,1],10)
train,test=train_test_split(ids,test_size=.25,random_state=42,stratify=labels)
print("Class rates",labels[train].mean(),labels[test].mean())
groups=np.repeat(np.arange(10),4)
gtrain,gtest=next(GroupShuffleSplit(n_splits=1,test_size=.3,random_state=42).split(ids,groups=groups))
assert set(groups[gtrain]).isdisjoint(groups[gtest])
print("Train patients",np.unique(groups[gtrain]),"Test patients",np.unique(groups[gtest]))
for past,future in TimeSeriesSplit(n_splits=3).split(ids):
    assert past.max()<future.min()
    print("Past ends",past.max(),"future begins",future.min())''')], 'Why is a chronological split insufficient if rolling features include future observations? Why is stratification insufficient for repeated patients?')
build('L10_Predictive_Pipeline_Lab.ipynb','L10: A safe baseline and predictive pipeline','Use training-side CV for tuning, then one final test evaluation. Synthetic target is not a deployed medical or business score.', [('## Independent synthetic regression and untouched test partition','''from sklearn.model_selection import train_test_split,GridSearchCV,KFold
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler,PolynomialFeatures
from sklearn.linear_model import Ridge
from sklearn.dummy import DummyRegressor
from sklearn.metrics import mean_squared_error,mean_absolute_error
rng=np.random.default_rng(42)
x=rng.uniform(-3,3,240).reshape(-1,1)
y=.7*x[:,0]**2-.5*x[:,0]+1+rng.normal(0,.65,240)
X_train,X_test,y_train,y_test=train_test_split(x,y,test_size=.25,random_state=399)
pipe=Pipeline([("imputer",SimpleImputer()),("poly",PolynomialFeatures(include_bias=False)),("scale",StandardScaler()),("model",Ridge())])
search=GridSearchCV(pipe,{"poly__degree":[1,2,3],"model__alpha":[.01,1,10]},cv=KFold(5,shuffle=True,random_state=42),scoring="neg_mean_squared_error")
search.fit(X_train,y_train)
print("Chosen by training-only CV:",search.best_params_)
# GridSearchCV refits the chosen pipeline on all training rows.
baseline=DummyRegressor().fit(X_train,y_train)
for name,model in [("Baseline",baseline),("Chosen pipeline",search.best_estimator_)]:
    prediction=model.predict(X_test)
    print(name,"MSE",mean_squared_error(y_test,prediction),"MAE",mean_absolute_error(y_test,prediction))''')], 'Explain why each preprocessing component is inside the pipeline. Define MSE units. Report the final score without changing the recipe in response to the test result.')
build('L11_Descriptive_Statistics_Lab.ipynb','L11: Shape, spread, and uncertainty','Summarize measurements rather than IDs; distinguish skewness conventions.', [('## Descriptive shape and skewness correction','''from scipy import stats
x=np.array([10,20,30,40,100],dtype=float)
m2=np.mean((x-x.mean())**2);m3=np.mean((x-x.mean())**3)
g1=m3/m2**1.5
G1=np.sqrt(len(x)*(len(x)-1))/(len(x)-2)*g1
assert np.isclose(G1,stats.skew(x,bias=False))
print("Unadjusted/adjusted skew",g1,G1)
print("Excess kurtosis",stats.kurtosis(x,fisher=True,bias=False))
sales=pd.read_csv(DATA / "sales_multiyear.csv")
print(sales[["Quantity","NetRevenue","Profit"]].agg(["mean","median","std","skew"]))'''),('## A mean confidence interval under stated assumptions','''rng=np.random.default_rng(11)
sample=rng.normal(50,8,40)
ci=stats.t.interval(.95,df=len(sample)-1,loc=sample.mean(),scale=stats.sem(sample))
print("Mean",sample.mean(),"95% CI",ci)
# Independent sample and approximately normal population for this small example.
''')], 'Explain why 95% confidence describes repeated sampling coverage, not a 95% probability assigned to this fixed population mean. Compare mean and median for revenue.')
build('L12_Correlation_Lab.ipynb','L12: Correlation and inference','Plot relationships; distinguish a statistical coefficient from causation and practical significance.', [('## Correlations of measurements','''from scipy import stats
sales=pd.read_csv(DATA / "sales_multiyear.csv")
num=sales[["Quantity","UnitPrice","Discount","NetRevenue"]]
print(num.corr(method="pearson"));print(num.corr(method="spearman"))
plt.scatter(sales.Quantity,sales.NetRevenue,alpha=.1);plt.xlabel("Quantity");plt.ylabel("Net revenue (USD)");plt.show()'''),('## Welch mean comparison; paired analysis; categorical association','''rng=np.random.default_rng(12)
a=rng.normal(20,3,35);b=rng.normal(23,6,40)
welch=stats.ttest_ind(a,b,equal_var=False)
diff=b.mean()-a.mean();se=np.sqrt(a.var(ddof=1)/len(a)+b.var(ddof=1)/len(b))
df=(a.var(ddof=1)/len(a)+b.var(ddof=1)/len(b))**2/((a.var(ddof=1)/len(a))**2/(len(a)-1)+(b.var(ddof=1)/len(b))**2/(len(b)-1))
ci=stats.t.interval(.95,df,loc=diff,scale=se)
print("Mean difference",diff,"95% Welch CI",ci,"p",welch.pvalue)
paired_before=rng.normal(20,4,30);paired_after=paired_before+rng.normal(2,2,30)
differences=paired_after-paired_before
print("Paired t-test",stats.ttest_rel(paired_after,paired_before))
print("Paired mean change",differences.mean(),"95% CI",stats.t.interval(.95,len(differences)-1,loc=differences.mean(),scale=stats.sem(differences)))
print("Paired standardized effect (dz)",differences.mean()/differences.std(ddof=1))
u=stats.mannwhitneyu(a,b)
print("Mann-Whitney distribution test",u,"probabilistic superiority a over b (half ties)",u.statistic/(len(a)*len(b)))
c=a.mean()+rng.normal(0,10,35)
print("Kruskal-Wallis distribution comparison",stats.kruskal(a,b,c))
counts=np.array([[20,5],[4,21]])
chi=stats.chi2_contingency(counts)
print("Expected counts",chi.expected_freq,"chi-square p",chi.pvalue)
print("Fisher exact",stats.fisher_exact([[1,8],[7,2]]))''')], 'State each test’s question and assumptions. Discuss independence, paired differences, rank/distribution versus mean questions, effect size, and multiple comparisons. A normality p-value alone is not a test-selection rule.')
build('L13_SQL_and_Aggregation_Lab.ipynb','L13: SQL and grouped analytics','Use a local SQLite database for joins, CASE, CTEs, NULL, aggregation, and windows.', [('## Same question in SQL and pandas','''import sqlite3
sales=pd.read_csv(DATA / "sales_multiyear.csv")
regions=pd.read_csv(DATA / "dim_region.csv")
con=sqlite3.connect(":memory:")
sales.to_sql("sales",con,index=False);regions.to_sql("regions",con,index=False)
query="""WITH regional AS (
 SELECT r.Region, SUM(s.NetRevenue) AS revenue,
 COUNT(DISTINCT s.OrderID) AS orders
 FROM sales s JOIN regions r ON s.RegionKey=r.RegionKey
 WHERE s.OrderDate >= '2024-01-01'
 GROUP BY r.Region
 HAVING SUM(s.NetRevenue) > 0
)
SELECT *, revenue/orders AS aov, RANK() OVER(ORDER BY revenue DESC) AS revenue_rank
FROM regional ORDER BY revenue_rank"""
print(pd.read_sql_query(query,con))
print(pd.read_sql_query("SELECT CASE WHEN Discount=0 THEN 'Full price' ELSE 'Discounted' END AS price_type, COUNT(*) AS lines FROM sales GROUP BY price_type",con))
print(pd.read_sql_query("SELECT COALESCE(NULL, 'Unknown') AS fallback, NULL IS NULL AS is_missing",con))'''),('## Grouped versus pivot layout','''print(sales.groupby(["Region","Category"]).NetRevenue.sum().head())
pivot=pd.pivot_table(sales,index="Region",columns="Category",values="NetRevenue",aggfunc="sum",fill_value=0,margins=True)
assert np.isclose(pivot.loc["All","All"],sales.NetRevenue.sum())
print(pivot)''')], 'Why can a join duplicate revenue? Explain SQL NULL versus zero. Add a monthly revenue CTE and a trailing three-row sum window.', '''q="""WITH monthly AS (SELECT substr(OrderDate,1,7) AS month,SUM(NetRevenue) AS revenue FROM sales GROUP BY month)
SELECT month,revenue,SUM(revenue) OVER(ORDER BY month ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) AS trailing_3_months FROM monthly"""
print(pd.read_sql_query(q,con).head())''')
build('L14_Time_Series_Lab.ipynb','L14: Calendar time and moving averages','Use the complete bundled electricity series; windows count observations, not arbitrary days.', [('## Monthly series and year-over-year comparison','''df=pd.read_csv(DATA / "electric_production.csv",parse_dates=["DATE"])
s=df.set_index("DATE")["IPG2211A2N"].sort_index()
assert s.index.is_unique
assert len(s)>24
monthly=s.resample("MS").mean()
ma=monthly.rolling(12,min_periods=12).mean()
plt.plot(monthly,label="Monthly index");plt.plot(ma,label="Trailing 12-month MA");plt.ylabel("Production index (source-defined base)");plt.legend();plt.show()
print(pd.DataFrame({"index":monthly,"prior_year":monthly.shift(12),"YoY":monthly.pct_change(12)}).tail())''')], 'Why are the first eleven complete-window moving averages missing? Why does a centered smoother leak future information in forecasting? Inspect seasonality over repeated years rather than claiming it from a few months.')
build('L15_EDA_Case_Study.ipynb','L15: EDA and exposure limitations','Combine grain checks, summaries, groups, and time analysis using synthetic accidents.', [('## Validate the grain and compare segments','''df=pd.read_csv(DATA / "accident_teaching.csv",parse_dates=["date"])
assert df.accident_id.is_unique
print(df[["vehicles","casualties"]].describe())
summary=df.groupby("region").agg(incidents=("accident_id","size"),casualties=("casualties","sum"))
summary["casualties_per_recorded_incident"]=summary.casualties/summary.incidents
print(summary)
series=df.set_index("date").resample("MS").casualties.sum()
series.plot(title="Synthetic monthly casualties");plt.ylabel("Casualties (count)");plt.show()''')], 'Write a descriptive finding and a limitation. Counts do not establish road danger: traffic volume, reporting coverage, and exposure denominators are absent. Do not infer causality or real policy recommendations from synthetic data.')
# Power BI notebooks are complete procedural guides; not fake executable Power BI environments.
for file,title,text in [
('L20_PowerBI_Power_Query_Lab.ipynb','L20: Power Query', '''1. Import sales_multiyear.csv with Transform Data. Profile the entire dataset rather than only the default first 1000 rows.
2. Set OrderDate to Date; IDs to text/whole number as appropriate; monetary columns to fixed decimal; Discount to decimal fraction.
3. Demonstrate Merge using dim_product.csv on ProductKey; ensure the product key is unique. Expand only needed columns.
4. Demonstrate Append by splitting 2022 and 2023 into identical-schema queries and appending them. Confirm combined row count.
5. Demonstrate Unpivot on a separate tiny January/February/Region table; one row becomes one region-month observation.
6. Use dirty_sales.csv separately: flag missing quantity before filling; remove the exact duplicate; quarantine invalid dates and negative quantities. Never silently replace errors with zero.
7. Add NetRevenue if not already supplied: [Quantity]*[UnitPrice]*(1-[Discount]).
8. Close & Apply. Rename the sales fact query Sales. See ../resources/powerbi-measures.dax for the complete measure set.
9. Query folding pushes compatible steps to a supported source. A local CSV does not provide database query folding; use View Native Query/diagnostics with a supported connector before claiming folding.
Deliver screenshots of named steps, before/after row counts, and the model. This file is a guide, not an executable Power BI report.'''),
('L22_PowerBI_Data_Modeling_Lab.ipynb','L22: Star schema', '''1. Load Sales from sales_multiyear.csv, DimProduct from dim_product.csv, DimCustomer from dim_customer.csv, DimRegion from dim_region.csv, and DimDate from dim_date.csv.
2. State grain: Sales contains one order line; (OrderID,LineID) is unique; OrderID can repeat.
3. Remove Product/Category/Region descriptors from the fact after retaining their keys. Hide technical foreign keys from report users; hiding does not reduce storage.
4. Set one-to-many relationships from unique dimension keys to Sales keys, single-direction dimension-to-fact filtering.
5. Connect DimDate[Date] to Sales[OrderDate]; dates must be Date type. Mark DimDate as the date table for classic time intelligence.
6. Verify the calendar contains every day from 2022-01-01 through 2024-12-31, not merely dates occurring in transactions.
7. Sort MonthName by Month. Keep Year and Month together for chronological reporting.
8. Test unmatched keys and blank members. Compare a region matrix to Python totals in resources/reference_totals.json.
Deliver a model screenshot and checks. No fabricated screenshots or measured performance claims are supplied.'''),
('L23_L24_PowerBI_DAX_Time_Intelligence_Lab.ipynb','L23–L24: DAX and time intelligence', '''1. Complete the L22 model, using Sales, DimDate, DimProduct, DimCustomer, DimRegion.
2. Copy the definitions from ../resources/powerbi-measures.dax in dependency order.
3. Test Total Sales, Order Count (DISTINCTCOUNT), Line Count (COUNTROWS), Profit, and Profit Margin.
4. Compare matrix totals to ../resources/reference_totals.json. Average order value uses distinct orders, not lines.
5. Add 2024 Year and Region slicers. Sales All Regions removes DimRegion filters but retains year and category filters. Sales Selected Regions uses ALLSELECTED for a selection-aware denominator.
6. Compare replacement of a Category slicer with KEEPFILTERS intersection.
7. Test Sales YTD, Sales PY, and YoY % for 2023 and 2024. For 2022, prior-year data is absent: BLANK is legitimate.
8. Full-history running total clears the entire date table. Selection-aware running total uses ALLSELECTED(DimDate). Explain their difference.
9. Test blank prior period, zero denominator, subtotals, and multi-selects. Report what you observed; do not assert native Power BI validation without opening Desktop.
Deliver screenshots and reconcile numbers with Python references.''')]:
 build(file,title,'Follow this guide in Power BI Desktop. A Python notebook viewer is used only to display the instructions.', [('## Worked procedural guide',None), (text,None)], 'Complete the steps and save your .pbix, screenshots, QA notes, and source definitions.',needs_setup=False)
print('Built',len(list(L.glob('*.ipynb'))),'notebooks')
