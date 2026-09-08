# Course Datasets

All files below are ready for `pd.read_csv()`. Click the filename to download from the repository (or use the Raw link).

## Available in this repository

| File | Description | Typical Lectures |
|------|-------------|------------------|
| [sample_accidents.csv](sample_accidents.csv) | Road accident sample (original course data) | EDA, Power BI, Outliers |
| [sample_sales.csv](sample_sales.csv) | Simple retail sales transactions (OrderID, Date, Product, Category, Region, Qty, Price, Discount) | L7 Transformation, Feature Engineering, Modeling |
| [electric_production.csv](electric_production.csv) | US Electric Production monthly series (DATE, IPG2211A2N) – clean version for time-series practice | L14 Time Series |
| [Electric_Production_analysis.csv](Electric_Production_analysis.csv) | Full original Electric Production file (with forecast columns) | Time Series labs |

## Classic public datasets (recommended downloads)

These are standard teaching datasets. You can download them directly:

| Dataset | Direct download / Raw URL | Use for |
|---------|---------------------------|--------|
| **Titanic** | https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv | Missing values, encoding, EDA, intro classification |
| **Pima Indians Diabetes** | https://raw.githubusercontent.com/jbrownlee/Datasets/master/pima-indians-diabetes.data.csv (no header) | Outliers, Feature Engineering, simple modeling |
| **Gapminder** | https://raw.githubusercontent.com/plotly/datasets/master/gapminderDataFiveYear.csv | Time series, visualization, multi-country analysis |

### Quick load examples

```python
import pandas as pd

# From this repo
sales = pd.read_csv("../../datasets/sample_sales.csv")
elec  = pd.read_csv("../../datasets/electric_production.csv", parse_dates=["DATE"])

# From public raw
titanic = pd.read_csv("https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv")
pima    = pd.read_csv("https://raw.githubusercontent.com/jbrownlee/Datasets/master/pima-indians-diabetes.data.csv",
                      names=["preg","plas","pres","skin","insu","mass","pedi","age","class"])
gap     = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/gapminderDataFiveYear.csv")
```

Progress is saved in browser localStorage. Enjoy the labs!
