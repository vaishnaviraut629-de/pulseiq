# Think Day 3 - Reflection

## What I built today?
Built KPI views (attendance_rate, avg_work_hours, leave_utilization, payroll_cost) with target vs actual logic. Connected star schema to BI layer.

## What was the hardest bug?
KPI target join - kpi_targets.csv madhe date_key format 'YYYY-MM' hota pan dim_date madhe 'YYYY-MM-DD'. Join fail hot hota, 0 rows yet hote. Fix: `substr(date_key, 1, 7)` ne join kela.

## Proof that KPI logic works?
Ran `SELECT * FROM kpi_attendance_rate LIMIT 5` - target 95% vs actual 92.3% shows correctly. Screenshot: `06_kpi_views.png`

## What will I do next?
Final dashboard in PowerBI + final GitHub push + Evidence folder complete.