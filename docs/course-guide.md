# Course guide

This is an undergraduate teaching course with 30 lectures. The learning outcomes below are course guidance, not a claim of institutional accreditation or an official assessment policy.

| Outcome | Evidence |
|---|---|
| CLO-1: Design an analytics pipeline and frame a decision | Architecture, source inventory, business question and success criteria |
| CLO-2: Prepare, explore and validate data | Cleaning log, executable notebook, statistical interpretation and leakage-safe evaluation |
| CLO-3: Model and communicate analytics | Star schema, tested measures, accessible report and defensible recommendation |
| CLO-4: Apply ethics throughout the lifecycle | Permission, privacy, fairness and limitations statement |

## Suggested sequence

Use the lecture numbers as the sequence. The historical `week*` folders remain for stable links; their folder numbers do not enforce a timetable. At two lectures per teaching week the course takes 15 weeks.

1. L1–4: framing, architecture, acquisition and analytical thinking.
2. L5–10: quality, outliers, transformation, features, splitting and prediction.
3. L11–15: descriptive statistics, inference, SQL, time series and EDA.
4. L16–19: charts, design, advanced forms and dashboards.
5. L20–26: Power Query, interactions, modeling, DAX, time intelligence, performance and delivery.
6. L27–30: ethics, proposal, execution, QA and presentation.

## Prerequisites and setup

Basic algebra, percentages, tables and file handling are sufficient. Start with the Python foundations and Pandas notebooks before L5. Install Python 3.11 or later, create a virtual environment, and run `python -m pip install -r requirements.txt`. Start Jupyter or open the notebooks in VS Code. Run from the repository root or `labs/`; keep the datasets directory alongside labs. In Colab clone/upload the repository and install requirements first. Notebook outputs are intentionally cleared for students to execute.

Power BI labs are guided Desktop tasks. Install Power BI Desktop on a supported Windows environment. A browser-based teaching report is provided for exploring filters without Desktop. Service publishing, sharing and refresh depend on tenant permissions, account/licensing and connectivity; verify these in your own environment. A screenshot of a report does not prove refresh, security or correct DAX behavior.

## Suggested capstone rubric (adapt locally)

| Criterion | Weight | Review evidence |
|---|---:|---|
| Question and measurable decision | 10% | Audience, metric, denominator, scope |
| Acquisition, provenance and ethics | 15% | Source permissions, dictionary, privacy and limitations |
| Preparation and reproducibility | 20% | Raw retention, validation, decision log, executable steps |
| Analysis and evaluation | 20% | Correct statistical claims; baseline and held-out evaluation if predictive |
| Semantic model and report | 20% | Grain, key tests, reconciliation, accessible interactions |
| Communication and handover | 15% | Recommendation, uncertainty, refresh plan and reproducible delivery |

Submission: proposal, raw-source inventory, clean-data process, notebook, report file or browser report, measure definitions, QA checklist and short presentation. Evaluate predictive work only if the question calls for it. Synthetic accidents cannot support road-safety policy, and synthetic sales cannot support investment decisions.

## Reference documentation

- [scikit-learn: common pitfalls and leakage](https://scikit-learn.org/stable/common_pitfalls.html)
- [scikit-learn: cross-validation strategies](https://scikit-learn.org/stable/modules/cross_validation.html)
- [pandas: merging and join validation](https://pandas.pydata.org/docs/user_guide/merging.html)
- [SciPy statistical functions](https://docs.scipy.org/doc/scipy/reference/stats.html)
- [Microsoft: star schema guidance](https://learn.microsoft.com/en-us/power-bi/guidance/star-schema)
- [Microsoft: CALCULATE](https://learn.microsoft.com/en-us/dax/calculate-function-dax)
- [Microsoft: date tables](https://learn.microsoft.com/en-us/power-bi/guidance/model-date-tables)
- [Microsoft: row-level security](https://learn.microsoft.com/en-us/power-bi/enterprise/service-admin-rls)
- [Microsoft: Performance Analyzer](https://learn.microsoft.com/en-us/power-bi/create-reports/desktop-performance-analyzer)
