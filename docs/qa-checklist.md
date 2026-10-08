# Course and capstone QA

## Automated checks

Run `python scripts/validate_course.py` to check internal links/anchors, duplicate HTML IDs, image alt text, SVG XML, lecture coverage, search coverage, date/dimension keys, financial formulas and reference totals. It executes every Python code cell in each runnable notebook in a fresh process; the three procedural Power BI notebooks are checked structurally. It does not claim Desktop or Power BI Service validation.

Run `node --check assets/js/main.js` and `node --check resources/retail-report.js`. The DOM-fixture interaction script (`node scripts/check_interactions.cjs`) additionally checks report totals, filters/reset, search from nested URLs, quiz keyboard operation, theme persistence and self-reported completion.

## Manual Desktop acceptance

1. Import the supplied Sales and four dimension tables; assign date, integer/key and currency types.
2. Confirm unique dimension keys and 1:* single-direction filtering. Mark the continuous DimDate date table.
3. Enter the DAX measures separately; compare unfiltered, year and region totals with `reference_totals.json`.
4. Confirm distinct orders differ from order-line counts; verify margin as the ratio of totals.
5. Check category replacement versus KEEPFILTERS, REMOVEFILTERS versus ALLSELECTED, and selected/full-history running totals under slicers.
6. Check YTD/prior-year dates, missing prior-year BLANK behavior and leap-day handling.
7. Test slicers, interactions, drillthrough, reset, keyboard/tab order, alt text and mobile layout.
8. Measure the same interaction before/after a performance change. Record hardware, dataset, cache conditions and measured duration.
9. In an authorized Service workspace test refresh and effective permissions/RLS as actual viewer roles. Hidden fields are not security.
10. Present source provenance, synthetic-data labels, assumptions, uncertainty and recommended next action.
