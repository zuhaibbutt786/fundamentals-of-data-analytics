# Fundamentals of Data Analytics

An undergraduate teaching course with 30 lectures, editable visual explanations, runnable Python labs and guided Power BI tasks. Static HTML/CSS/JavaScript, hosted on GitHub Pages.

[Live course](https://zuhaibbutt786.github.io/fundamentals-of-data-analytics/) · [Start here: setup and resources](resources/index.html) · [Course guide and capstone rubric](docs/course-guide.md)

## Included

- 39 editable SVG teaching visuals, computed numerical examples, captions, alt text and interpretation questions.
- 15 executable Python notebooks with local inputs and reference solutions, plus 3 guided Power BI notebooks.
- A reproducible synthetic retail case (2022–2024), dirty cleaning case, four dimensions and synthetic accident EDA case.
- Consistent [DAX measure definitions](resources/powerbi-measures.dax) and [Python reconciliation totals](resources/reference_totals.json).
- A [working retail teaching report](resources/retail-report.html) with year/region filters, KPI cards, chart/table and reset.
- Search covering all 30 lectures; keyboard-operable quizzes/flashcards, light/dark themes and explicit self-reported progress.

## Course structure

| Module | Focus | Lectures |
|---|---|---|
| 1 | Foundations, pipelines and analytical framing | 1–4 |
| 2 | Quality, preprocessing, features and prediction | 5–10 |
| 3 | Statistics, SQL, time series and EDA | 11–15 |
| 4 | Visualization, storytelling and Power BI preparation | 16–21 |
| 5 | Modeling, DAX and delivery | 22–26 |
| 6 | Ethics, proposal and capstone | 27–30 |

The four CLOs are course guidance, not an official institutional accreditation claim. Lecture numbers determine sequence; historical folder paths remain stable.

## Run and reproduce

Serve the repository root with `python -m http.server 8000`, then open `http://localhost:8000`. The static course needs no build step. Some original styling/fonts and math rendering use CDNs; downloadable inputs and notebook analysis are local after dependency installation.

Use Python 3.11+ and a virtual environment. Install `python -m pip install -r requirements.txt`, then run the notebooks from the root or `labs/`. See [visual generation commands](docs/visuals.md), [data dictionary and provenance](datasets/README.md), and [QA checklist](docs/qa-checklist.md).

Validation: `python scripts/validate_course.py`; JavaScript syntax: `node --check assets/js/main.js` and `node --check resources/retail-report.js`. Browser interaction checks: `node scripts/check_interactions.cjs` (dependency-free DOM fixtures, not full browser layout validation). Power BI Desktop/Service behavior still requires manual verification in a supported environment.

## Author

Zuhaib Hussain Butt · GIFT University

Reading progress is stored locally in your browser when storage is available. Completion is a self-report, not a mastery score. New sales/accident cases are synthetic and labeled throughout.

The existing launch-video creative plan remains in [brag/](brag/); video files were not present in the original repository.
