# Task 13 - Cross Dept Impact View

### 1. Grain and Join Logic
- **Grain:** department_id + month (2020-01 to 2025-12)
- **Total Rows:** 821 rows, 20 columns
- **Join Order:** headcount as BASE (LEFT JOIN) -> payroll agg, attendance agg, leave agg
- **Logic:** Aggregate First, Then Join. To avoid row multiplication, all daily/hourly data was summed to monthly level before joining.

### 2. Vault Comparison
- **Reference File:** `04_Validation_Vault/dept_month_summary.xlsx`
- **Comparison:**
    - total_cost: <2% difference. Reason: I used employer_cost, vault reference used gross + employer contribution.
    - total_leave_days: 0% difference. Both filtered for Approved leaves only.
    - overtime_hours: Exact match.
- **Status:** Matches reference or differences explained.

### 3. Charts Evidence
- **Screenshot 1:** `Task13_01_SameGrain_CombinedTable_821x20.png` - Shows final combined table with same grain.
- **Screenshot 2:** `Task13_02_Dept_Cost_OT_BarChart.png` - Engineering and Operations have highest avg cost and overtime.
- **Screenshot 3:** `Task13_03_Overtime_vs_Attrition_Scatter.png` - Shows correlation between overtime and attrition.

### 4. Think For Yourself - Key Question

**Q: Overtime is high where attrition is high. Does overtime cause attrition? What else could explain it?**

**Ans:** No, not directly. The chart shows correlation, not causation. Both OT and attrition are high at the same time, but overtime is not the root cause.

The main underlying factor is understaffing. When a team has fewer members than required, the existing staff has to work extra hours, which leads to high overtime. Over time, this workload causes burnout and employees leave.

Other possible reasons are poor management, low salary hike, frequent night shifts, and lack of promotion.

So, overtime is a symptom of less staffing, not the actual cause of attrition. To reduce attrition, the focus should be on hiring adequate staff, not just reducing overtime hours.