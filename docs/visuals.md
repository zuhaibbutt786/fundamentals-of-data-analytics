# Reproducing the teaching visuals

All 39 visuals are editable SVGs with real text. They are educational diagrams/charts rather than invented software screenshots. Each embedded figure has a caption, alt text, a student question and an answer. Its SVG opens at full size for zooming; mobile readers can also expand the text version of the diagram labels.

From the repository root after installing requirements:

```bash
python scripts/generate_datasets.py
python scripts/visuals_l5_6.py
python scripts/visuals_l7_8.py
python scripts/visuals_l9_10.py
python scripts/generate_visuals.py
python scripts/build_labs.py
python scripts/build_resources.py
python scripts/integrate_course.py
python scripts/validate_course.py
```

`correct_course.py` is a one-time migration of the original lessons, not part of normal regeneration. Regenerate derived assets after editing their scripts. Use a fresh checkout or preserve your work before rerunning the dataset generator.

## Conventions

- White/light figure backgrounds; navy structure, blue inputs, teal valid outputs, amber cautions and restrained red errors. Labels, line patterns and shapes carry meaning alongside color.
- Standardization uses population variance (`ddof=0`). Exact symbolic values accompany rounded decimals for the five-value transformation example.
- Boxplot quartiles use NumPy linear percentiles (Hyndman–Fan type 7); fences are thresholds, while whiskers terminate at actual observations within fences.
- Synthetic regression uses seed 42 and a quadratic mean with Gaussian noise SD 0.65. Degrees 1, 2 and 15 are fixed before evaluation and use the same 24 training observations. The 400 held-out observations are generated independently. Training and held-out MSE are calculated, not selected manually. Axis clipping is disclosed.
- Other chart seeds, units and assumptions are in their generator/caption. Synthetic accidents and sales are instructional examples; population claims require real, appropriately sourced data and suitable designs.
- The ETL/ELT comparison uses the same operational database and warehouse. Transformation location differs; governance and raw-history retention are possible in both.
- The retail report is functional HTML/JavaScript; it is labeled as a teaching implementation rather than Power BI UI. Actual Desktop performance, sharing and DAX execution require manual validation.

The manifest at `assets/visuals/manifest.json` maps assets to lectures and stores the caption, alt text and interpretation question/answer. Companion CSV/JSON files preserve the cleaning example and regression calculations.
