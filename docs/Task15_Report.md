# Task 15: Executive Company-Health Scorecard - Report

**File:** `pages/15_Executive_Scorecard.py`
**Dataset:** PulseIQ_Dataset.xlsx
**Month Used:** 2026-09

## 1. 8 KPIs List with Reason

I picked these 8 because founder needs Growth, Money and Risk in 2 mins.

1.  **Total Headcount - 441** - Source: M01 fact_headcount_monthly. To see company is growing or not.
2.  **Attrition Rate - 0.31%** - Source: M05 fact_headcount_monthly, target 1% from kpi_targets. If this goes up, we lose talent.
3.  **Absenteeism - 4.78%** - Source: M13 fact_attendance_monthly. Shows productivity issue.
4.  **Revenue per Employee - ₹2.23L** - Source: M15 fact_invoice. How much each person earns for company.
5.  **High-Risk Employees - 43** - Source: fact_attrition_risk where risk_band=High. These people may leave in 12 months.
6.  **Money at Risk - ₹32.9L** - Source: fact_anomaly money_at_risk. How much money is stuck due to anomalies.
7.  **Forecast Accuracy - 88%** - Source: fact_forecast. How good our planning is.
8.  **Cost per Employee - ₹1.25L** - Source: M10 fact_payroll. How much we spend per person.

All numbers come from metric_dictionary and fact tables only. I used @st.cache_data.

## 2. Target, Trend and Status

I used kpi_targets sheet for status.
- Attrition target is 1% monthly. My value 0.31% so Green.
- Attendance target is 94% (0.94). My value 95.22% (100-4.78) so Green.
- Trend I calculated MoM: (This Month - Last Month) / Last Month.

## 3. Design - One Page A4

I made 4 columns x 2 rows = 8 cards. Only st.metric used, no big charts.
It fits on one A4 page. I tested Ctrl+P. I added caption under each KPI with Target and Source so founder can trace it.

## 4. Traceability and Links

Each KPI has metric_id in caption like M01, M05. 
Left sidebar has all detailed pages - Workforce, Attendance, Attrition, Payroll Cost, AI Signals, Budget vs Actual, PnL. So founder can click for more detail.
Rule followed: If metric not in metric_dictionary, I did not add it.

## 5. Think for yourself: You may only show 5 KPIs. Which 3 do you remove and why?

This is my personal thinking.

**If I can show only 5, I will keep these 5:**
1. Total Headcount (441) - Basic growth number.
2. Attrition Rate (0.31%) - Main health indicator.
3. Revenue per Employee (₹2.23L) - Money efficiency.
4. High-Risk Employees (43) - Future problem.
5. Money at Risk (₹32.9L) - Current money problem.

These 5 cover everything - Growth, People, Money.

**Which 3 I will remove and why I removed them:**

**1. Absenteeism (4.78%) - I will remove this.**
Reason: This is daily level issue. 4.78% is not very high. And if someone is taking lot of leave, finally it will show in Attrition. So Attrition is more important than Absenteeism for founder. HR team can track absenteeism separately.

**2. Cost per Employee (₹1.25L) - I will remove this.**
Reason: Revenue per Employee already tells the story. If revenue is ₹2.23L and cost is ₹1.25L, we are making profit. So revenue per employee is enough for founder. Cost per employee is more for finance team to control, not for headline.

**3. Forecast Accuracy (88%) - I will remove this.**
Reason: This is for planning team. Founder cares more about real problems like 43 people at high risk and ₹32.9L money at risk. Forecast accuracy is good to know but not urgent like money at risk. Operations team can handle it.

So final thought: Founder wants to know - Are we growing? Are people staying? Are we making money? Is money safe? My 5 KPIs answer that.

## Completion Checklist

- [x] Fits on one page - Yes, 8 cards in grid
- [x] Each KPI traces to a metric view - Yes, M01, M05 etc in caption
- [x] Statuses follow kpi_targets - Yes, 1% attrition target used
- [x] Links work - Yes, sidebar has all pages
- [x] Month selector - Yes, 2026-09 selector

## Evidence and References

- Screenshot: docs/Evidence/Task15_Scorecard_Screenshot.png
I designed a scorecard an executive can read in two minutes.