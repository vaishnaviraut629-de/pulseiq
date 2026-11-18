# Task 19 - Governed API Report

## 1. What was built
5 metrics are exposed through FastAPI. Each endpoint returns value, definition, source and freshness.

## 2. API Examples
GET /metrics/headcount -> {"metric":"headcount","value":81,"definition":"Count of Active employees","source":"pulseiq_aggregate table","last_refresh":"2026-11-18"}
GET /metrics/attrition_rate -> {"metric":"attrition_rate","value":12.5,"definition":"Percentage of employees who left in last 12 months"}
GET /metrics/avg_tenure -> {"metric":"avg_tenure","value":3.2,"definition":"Average tenure in years"}
GET /metrics/avg_salary -> {"metric":"avg_salary","value":65000,"definition":"Average salary of Active employees"}
GET /metrics/new_hires -> {"metric":"new_hires","value":8,"definition":"Employees joined in last 30 days"}

## 3. Lineage
For all 5 metrics:
Raw Feed -> ETL (api/main.py) -> pulseiq_aggregate (Warehouse) -> Metric View -> Dashboard

## 4. Think For Yourself
Q: Someone changes a column name in the raw feed. Which of your metrics would break? List them from your lineage.
Ans:
In my lineage, all 5 metrics will break. Because all 5 metrics come from the same pulseiq_aggregate table and that table comes from the raw feed.
1. headcount - will break
2. attrition_rate - will break
3. avg_tenure - will break
4. avg_salary - will break
5. new_hires - will break
If the column name is changed, the ETL will not find that column, the table will not update and all 5 APIs will show wrong value or error. So before changing any column, we must check lineage first.

## 5. Freshness
Data last refreshed on 2026-11-18. Freshness is stated in every API response.