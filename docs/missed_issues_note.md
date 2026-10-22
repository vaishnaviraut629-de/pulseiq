---
# Missed Issues Note - Day 3

## Issues missed on Day 2 that were fixed on Day 3

### 1. KPI Target Join Missing
- **Issue:** Day 2 chya KPI views madhe target value (kpi_targets.csv) join navta, fakt actual hota.
- **Fix:** Day 3 la `build_kpi_views.py` madhe LEFT JOIN kele kpi_targets var, target vs actual % calculate kela.
- **Evidence:** `06_kpi_views.png`

### 2. No Business Logic for Payroll Cost
- **Issue:** fact_payroll madhe total_cost = basic + allowances hota pan business rule - "overtime is paid 1.5x" - miss hota.
- **Fix:** KPI view madhe CASE WHEN logic add kela for overtime calculation.

### 3. Star Schema Documentation Missing
- **Issue:** Day 2 la star_schema.md madhe fakt table names hote, relationships clear navte.
- **Fix:** Day 3 la proper diagram + FK relationships + grain definition lihile.
- **File:** `docs/star_schema.md`

### 4. Dashboard Filter Issue
- **Issue:** Day 2 cha data raw hota, date filter chukat hota.
- **Fix:** dim_date la is_weekend, is_month_end flags add kele, dashboard sathi.

All Day 2 gaps closed on Day 3.