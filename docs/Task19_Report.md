# Task 19 - Governed API Report

**Metric:** headcount
**Value:** 81
**Definition:** Count of Active employees
**Source:** pulseiq_aggregate table
**Last Refresh:** 2026-11-18
**Freshness:** Data last refreshed on 2026-11-18
**Owner:** HR Team
**Maintained By:** Vaishnavi

## 1. What was built
Endpoint: `GET /metrics/headcount`

The API now returns not only the value, but also governance information like definition, source and freshness:

{"metric":"headcount","value":81,"definition":"Count of Active employees","source":"pulseiq_aggregate table","last_refresh":"2026-11-18","freshness":"Data last refreshed on 2026-11-18"}

## 2. Lineage
pulseiq_aggregate -> API (api/main.py) -> Dashboard
Full lineage is in `docs/lineage.md`

## 3. Think For Yourself

**Q: Someone changes a column name in the raw feed. Which of your metrics would break? List them from your lineage.**

**Ans:**
In my lineage, I have only one metric which is headcount.

So if someone changes a column name in the raw feed, my headcount metric will break. Because my headcount comes from pulseiq_aggregate table and that table comes from the raw feed.

If the column name is changed, the code will not understand which column to take. Then the table will not update properly and API will show wrong value or give error.

So before changing any column name, we should first check lineage and see which metric is using that column, then change it in both places.

**1. headcount - WILL BREAK**

Reason: This metric depends on the `pulseiq_aggregate` table