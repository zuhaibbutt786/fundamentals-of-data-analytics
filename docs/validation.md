# Validation record

Validated on 2026-10-08 with Python 3.12.14, NumPy 2.3.5, Pandas 2.2.3, SciPy 1.17.0, scikit-learn 1.8.0 and Matplotlib 3.10.8. `requirements.txt` expresses supported dependency ranges rather than a guarantee that future versions produce byte-identical SVG metadata or regression floating-point values.

- Static checks passed for 33 HTML pages: local links and anchors, duplicate IDs and image alt text.
- All 39 SVGs parsed; the manifest covers all 30 lectures and includes captions, alt text and student interpretation questions/answers. Representative rendered figures were visually reviewed.
- Search index contains all 30 lectures. Existing lecture URLs are preserved.
- Sales formulas, composite grain, unique dimension keys, referential integrity, continuous date coverage and reference totals passed.
- Exact transformation and boxplot example checks passed.
- All 48 Python code cells in 15 notebooks executed successfully, with a fresh process per notebook. Outputs remain cleared for learners. Three Power BI notebooks are procedural and were checked structurally, not executed in Desktop.
- JavaScript syntax checks passed. Dependency-free DOM-fixture tests passed for year/region report totals, keyboard chart filtering, reset, nested search URLs, focus restoration, keyboard quiz/flashcard behavior, theme/completion persistence, namespaced quiz progress and storage unavailability.
- Semantic section nesting and `git diff --check` passed.

## Limits

DOM fixtures exercise behavior, not complete browser rendering. Full browser layout, assistive-technology behavior and a mobile-device review remain manual checks. Power BI Desktop DAX execution, performance timings, Service publishing, refresh and effective RLS permissions require verification in a supported environment; these have not been claimed as tested. Original external CDN/public-dataset availability is not guaranteed. Synthetic sales and accidents cannot support real-world business, clinical or policy conclusions.

## Useful reconciliation result

Full synthetic sales: 4,420 order lines; 2,192 distinct orders; net revenue 3,523,690.75 USD; total cost 2,355,588.00 USD; profit 1,168,102.75 USD. Profit margin is approximately 33.14997918%. The JSON reference provides all/year/region checks without display rounding.
