# Task 18: Self-Service KPI Explorer with Privacy

## Objective
Let a user choose a metric and a dimension, drill from company to department to team, and never reveal small groups.

## What I Built
- **Explorer Page:** `pages/18_KPI_Explorer.py`
- **Roles:** ADMIN, HR, MANAGER, EXECUTIVE (from `demo_users.csv`)
- **Drill-down:** Company (n=30) -> Department (n=8) -> Team (n=3)
- **Live Link:** `pulseiq-o5qndhp8k9qbdzwhmrk5o.streamlit.app/KPI_Explorer`

## Metrics & Dimensions Allowed

| Role | Allowed Metrics | Safe Reason |
| :--- | :--- | :--- |
| ADMIN | Headcount, Attrition Rate, Avg Tenure, Pay | Full access |
| HR | Headcount, Attrition Rate, Avg Tenure | No Pay |
| EXECUTIVE | Headcount, Attrition Rate, Avg Tenure | Strategic only |
| MANAGER | Headcount, Avg Tenure | Team only, no sensitive |

**Dimensions:** Company, Department, Team

## Privacy Logic - Minimum Group Size

```python
MIN_GROUP_SIZE = {
  "Headcount": 1,
  "Attrition Rate": 10,
  "Avg Tenure": 5,
  "Pay": 15
}

if current_group_size < MIN_GROUP_SIZE[metric]:
    st.error(f"🔒 Hidden - Group size {current_group_size} < minimum {MIN_GROUP_SIZE[metric]}. Privacy Protected.")
else:
    show_kpi(value)
    ## Think For Yourself

**Q: A manager has a team of 3. Should they see attrition for their team?**

**My Answer: No, they should not see it.**

Actually first I thought yes, manager should see his own team data. But then I thought about privacy.

If team is only 3 people and 1 person leaves, attrition shows 33%. In small team everyone knows who left. So it is indirectly telling who resigned. That is personal information.

Also if team is 3, if we show pay also, we can guess whose pay is what. So it is risky.

In my app I set minimum 10 for attrition. So for team of 3, I hide it and show message "Hidden - group too small". Manager can see company level or department level attrition but not his own team of 3.

I think this is correct because one privacy bug can expose someone. Better to hide than to leak.

So my decision: Hide attrition for team of 3.