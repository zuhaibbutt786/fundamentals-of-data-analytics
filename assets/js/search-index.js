window.COURSE_SEARCH_INDEX = [
  {
    "title": "Lecture 1: Modern Data Analytics Ecosystem",
    "url": "modules/week1/lecture1.html",
    "module": "Lecture 1",
    "keywords": "Frame a decision Write a stakeholder, decision, measurable outcome and analysis scope for declining orders.",
    "summary": "A 20% order decline describes a change; it does not identify its cause. Separate evidence from a hypothesis."
  },
  {
    "title": "Lecture 2: Designing a Data Pipeline",
    "url": "modules/week1/lecture2.html",
    "module": "Lecture 2",
    "keywords": "Defend the architecture Trace an invalid quantity from extraction to quarantine and correction. Identify where permissions, schema checks and lineage apply.",
    "summary": "Immutable raw storage retains the original record; correction creates a new processing version. ETL and ELT both require governance."
  },
  {
    "title": "Lecture 3: Data Acquisition Types & Storage",
    "url": "modules/week1/lecture3.html",
    "module": "Lecture 3",
    "keywords": "Acquire and join safely Use the local CSV/JSON/HTML examples and join ProductKey with validate=\"many_to_one\". Record source, retrieval date, permission, grain and types.",
    "summary": "A join must preserve the order-line count. A duplicated dimension key can inflate totals even when the code runs."
  },
  {
    "title": "Lecture 4: Analytical Thinking & Business Framing",
    "url": "modules/week2/lecture4.html",
    "module": "Lecture 4",
    "keywords": "Define a useful metric Calculate regional margin for 2024 Q1 as sum(Profit)/sum(NetRevenue). Specify the audience and the action a low margin would trigger.",
    "summary": "A ratio of totals weights transactions by revenue. An average of row margins answers a different question."
  },
  {
    "title": "Lecture 5: Data Quality & Profiling",
    "url": "modules/week3/lecture5.html",
    "module": "Lecture 5",
    "keywords": "Keep a cleaning decision log Profile dirty_sales.csv; remove exact duplicates, standardize region strings, coerce dates, quarantine impossible quantities/dates, and flag missing quantity before imputation.",
    "summary": "Keep raw inputs. The median baseline does not restore missing-data uncertainty. Compare results including and excluding imputed rows; predictive imputation must be fitted on training data."
  },
  {
    "title": "Lecture 6: Outliers & Noise Handling",
    "url": "modules/week3/lecture6.html",
    "module": "Lecture 6",
    "keywords": "Flag rather than automatically delete Compare the six-value example with the original five values and state the percentile convention. Identify the fences and observed whisker endpoints.",
    "summary": "For [10,12,13,14,15,100], linear Q1=12.25 and Q3=14.75; fences 8.5 and 18.5; whiskers 10 and 15. Statistical unusualness does not prove a data error."
  },
  {
    "title": "Lecture 7: Data Transformation",
    "url": "modules/week4/lecture7.html",
    "module": "Lecture 7",
    "keywords": "Separate fitting from transforming Reproduce all transformations of [10,20,30,40,100]. Fit the min–max scaler only once, then transform 120 without clipping.",
    "summary": "Population mean=40 and SD=10√10. The unseen scaled value is 11/9. Standardization changes location and scale, preserving shape rather than making a distribution normal."
  },
  {
    "title": "Lecture 8: Feature Engineering Basics",
    "url": "modules/week4/lecture8.html",
    "module": "Lecture 8",
    "keywords": "Define features and their availability Calculate the worked transaction and derive month/weekday from the assumed date 2024-01-08. Define the prediction timestamp before building historical features.",
    "summary": "Gross=600 USD; net=540; cost=360; profit=180; margin=1/3. Month=1; weekday=0 (Monday). Realized profit or later returns can leak future information."
  },
  {
    "title": "Lecture 9: Data Splitting & Validation",
    "url": "modules/week5/lecture9.html",
    "module": "Lecture 9",
    "keywords": "Match validation to the data structure Use stratification for independent class records, group splitting for repeated patients, and forward validation for dates. Verify groups do not overlap.",
    "summary": "A random split is unsuitable for evaluating future forecasting or new-patient generalization when related records cross partitions. Stratification alone does not solve these issues."
  },
  {
    "title": "Lecture 10: ML Basics & Insight Extraction",
    "url": "modules/week5/lecture10.html",
    "module": "Lecture 10",
    "keywords": "Evaluate a full predictive recipe Run the pipeline lab: imputation, polynomial features, scaling and regularized regression. Select settings using training-side folds and compare a baseline on the final held-out test.",
    "summary": "Every learned preprocessing step must be fitted inside each training fold. The degree-1/2/15 chart is a prespecified capacity demonstration, not permission to tune on test errors."
  },
  {
    "title": "Lecture 11: Descriptive Statistics Deep Dive",
    "url": "modules/week6/lecture11.html",
    "module": "Lecture 11",
    "keywords": "Report definitions and uncertainty Compute sample versus population standard deviation, adjusted versus unadjusted skewness, excess kurtosis and a mean confidence interval on the notebook’s stated examples.",
    "summary": "Common mean/median/mode orderings are heuristics, not theorems for every distribution. Zero skewness need not imply symmetry; kurtosis is about tail behavior, not simply peak height."
  },
  {
    "title": "Lecture 12: Correlation & Relationships",
    "url": "modules/week6/lecture12.html",
    "module": "Lecture 12",
    "keywords": "Choose the estimand before the test Run Welch independent means, paired differences, Mann–Whitney, chi-square and Fisher examples. Report effect direction, magnitude, confidence interval where appropriate, sample size and p-value.",
    "summary": "A p-value is not the probability the null is true. Rank tests compare distributions unless additional shift assumptions support a median interpretation; sparse counts may require exact methods."
  },
  {
    "title": "Lecture 13: Grouped Analysis",
    "url": "modules/week7/lecture13.html",
    "module": "Lecture 13",
    "keywords": "Learn SQL and aggregation together Run SQLite SELECT, WHERE, JOIN, GROUP BY, HAVING, CASE, a CTE and a window function in the lab. Reconcile grouped totals against Pandas and a pivot table.",
    "summary": "NULL comparisons use IS NULL, not = NULL. Joins can duplicate rows; check key cardinality and aggregation grain before interpreting totals."
  },
  {
    "title": "Lecture 14: Time Series Exploration",
    "url": "modules/week7/lecture14.html",
    "module": "Lecture 14",
    "keywords": "Respect temporal order Use the 397-observation monthly electric-production series. Sort dates, verify monthly coverage, compute trailing 12-month means and 12-month change, and inspect the trend/seasonality example.",
    "summary": "Trailing windows use past/current observations; centered windows and backward filling can expose future values. This lesson is descriptive; a forecast needs chronological validation and a naive baseline."
  },
  {
    "title": "Lecture 15: Mini Case Study — Complete EDA",
    "url": "modules/week8/lecture15.html",
    "module": "Lecture 15",
    "keywords": "Complete an EDA narrative Use accident_teaching.csv to inspect schema, missingness, duplicates, region/month counts and severity distribution. Deliver three observations with units and limitations.",
    "summary": "The 1800 records are generated for teaching. More incidents do not establish greater risk without exposure denominators such as traffic volume or distance traveled; association is not causation."
  },
  {
    "title": "Lecture 16: Foundations of Data Visualization",
    "url": "modules/week9/lecture16.html",
    "module": "Lecture 16",
    "keywords": "Choose an encoding for the question Use a bar for regional comparison and a line for ordered time. Compare the same four values with a pie and state what is lost.",
    "summary": "Bars normally need a zero baseline. Unordered regions should not be connected as a time trend. Avoid 3D distortions and label units, source and period."
  },
  {
    "title": "Lecture 17: Visualization Principles",
    "url": "modules/week9/lecture17.html",
    "module": "Lecture 17",
    "keywords": "Redesign for interpretation Redraw the before/after chart with a zero baseline, sensible ordering and one message. Test grayscale legibility and keyboard access to any controls.",
    "summary": "Use color plus labels or shapes. If using a truncated axis for a line chart, label it clearly and explain the focus; bar length must represent magnitude."
  },
  {
    "title": "Lecture 18: Advanced Charts",
    "url": "modules/week10/lecture18.html",
    "module": "Lecture 18",
    "keywords": "Check advanced chart semantics Reconcile the signed waterfall and calculate each funnel conversion. Compare regional trends using shared scales in small multiples.",
    "summary": "Waterfall: 100+20+15−10=125. Funnel: 30%, 40%, 50% stage rates and 6% overall for the same cohort. Choropleths usually need appropriate rates and geographic coverage, not raw population-driven counts."
  },
  {
    "title": "Lecture 19: Dashboard Thinking",
    "url": "modules/week10/lecture19.html",
    "module": "Lecture 19",
    "keywords": "Build a decision-oriented layout Explore the bundled retail report. Change Year and Region and verify cards, chart and table share the same context. Sketch a layout for a specific audience.",
    "summary": "Every KPI needs a definition, date window, units and denominator. The browser report is a working teaching example, not a Power BI screenshot."
  },
  {
    "title": "Lecture 20: Power BI Import & Model Prep",
    "url": "modules/week11/lecture20.html",
    "module": "Lecture 20",
    "keywords": "Shape data before loading Follow the Desktop lab: set data types; profile the complete dataset; merge a unique product dimension; append compatible yearly rows; unpivot a monthly table; document each step.",
    "summary": "CSV sources do not offer database query folding. Verify folding only for supported connectors and transformations. Preserve null indicators before replacement."
  },
  {
    "title": "Lecture 21: Power BI Visualization",
    "url": "modules/week11/lecture21.html",
    "module": "Lecture 21",
    "keywords": "Test interactions and delivery Test slicers, edit interactions, drillthrough and reset behavior. In your authorized Power BI workspace test refresh and View as role before sharing.",
    "summary": "A report is not a Service dashboard. Hiding columns or visuals is not security. Row-level security and workspace roles must be validated with realistic viewer permissions."
  },
  {
    "title": "Lecture 22: Data Modeling",
    "url": "modules/week12/lecture22.html",
    "module": "Lecture 22",
    "keywords": "Validate the star schema Import Sales and DimDate/DimProduct/DimCustomer/DimRegion. Use unique dimension keys with 1:* single-direction relationships; Date connects to OrderDate. Reconcile reference totals.",
    "summary": "One row is one order line. OrderID repeats, so order count is DISTINCTCOUNT(OrderID), not COUNTROWS. Use a continuous date table and mark it as the date table."
  },
  {
    "title": "Lecture 23: DAX Basics",
    "url": "modules/week12/lecture23.html",
    "module": "Lecture 23",
    "keywords": "Observe filter context Create the measures in resources/powerbi-measures.dax separately. Compare totals, category filters, KEEPFILTERS, REMOVEFILTERS and ALLSELECTED under region/category slicers.",
    "summary": "The four-line visual has sales 500 USD and 3 orders; North has 150 USD and 1 order. Measures respond to filter context; a calculated column is evaluated per row during model processing."
  },
  {
    "title": "Lecture 24: Advanced DAX & Time Intelligence",
    "url": "modules/week13/lecture24.html",
    "module": "Lecture 24",
    "keywords": "Test time intelligence across years Use the complete 2022–2024 dataset and marked date table. Compare YTD and previous-year totals, then contrast full-history and selected-period running totals with slicers.",
    "summary": "Clear ALL(DimDate), not just its Date column, when a cumulative measure should ignore Year/Month filters. Prior-year comparisons require comparable periods and explicit leap-day/calendar semantics."
  },
  {
    "title": "Lecture 25: Performance Optimization",
    "url": "modules/week13/lecture25.html",
    "module": "Lecture 25",
    "keywords": "Measure a performance change Use Performance Analyzer to record a baseline interaction, query duration and environment. Change one factor, repeat the same interaction and record the result.",
    "summary": "No measured performance values are invented here. Removing unused columns differs from hiding them; constrain cardinality and relationships before adding complex DAX."
  },
  {
    "title": "Lecture 26: Dashboard Design Project",
    "url": "modules/week13/lecture26.html",
    "module": "Lecture 26",
    "keywords": "Deliver a reconciled report Build the retail semantic model, apply all base measures and accessible interactions, and compare cards and annual totals to reference_totals.json. Document refresh and access.",
    "summary": "A passing screenshot is insufficient: test multiple filters, distinct order counts, margins, dates and security. The browser report supports exploration; Desktop is required to validate actual DAX."
  },
  {
    "title": "Lecture 27: Ethics & Project Proposal",
    "url": "modules/week14/lecture27.html",
    "module": "Lecture 27",
    "keywords": "Submit an ethical proposal Use the course-guide rubric to specify the problem, question, metric, data inventory, permission, privacy, method, validation and deliverables.",
    "summary": "Remove identifiers where possible, minimize collection, protect access and examine subgroup validity. State uncertainty and avoid implying observational association is causal."
  },
  {
    "title": "Lecture 28: Capstone Project Lab",
    "url": "modules/week14/lecture28.html",
    "module": "Lecture 28",
    "keywords": "Execute with checkpoints Keep a run log with source version, cleaning decisions, environment, key tests and unresolved questions. Review milestones against the proposal.",
    "summary": "A reproducible checkpoint includes code and inputs, not only outputs. Preserve evidence when scope changes; explain what the revised question can support."
  },
  {
    "title": "Lecture 29: Final Dashboard Completion",
    "url": "modules/week15/lecture29.html",
    "module": "Lecture 29",
    "keywords": "Perform QA before sharing Test join counts, duplicate keys, totals, blanks, slicer reset, keyboard navigation, narrow-screen readability, refresh and access roles. Ask a peer to reproduce one KPI.",
    "summary": "Technical correctness and usability are separate checks. Include uncertainty and source limitations in the report rather than concealing inconvenient exceptions."
  },
  {
    "title": "Lecture 30: Project Presentation & Viva",
    "url": "modules/week15/lecture30.html",
    "module": "Lecture 30",
    "keywords": "Tell a defensible analytical story Present problem → evidence → interpretation → recommendation → limitation → next action. Show the metric definition and demonstrate one interaction live.",
    "summary": "Separate observed facts from hypotheses, predictions and decisions. Supply reproducible files and a handover plan so the audience can verify the result."
  }
];
