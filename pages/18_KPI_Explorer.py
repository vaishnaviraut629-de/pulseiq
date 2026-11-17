import streamlit as st
import pandas as pd
import os

st.set_page_config(layout="wide")
st.title("Task 18: Self-Service KPI Explorer")
st.caption("Privacy Safe | Uses metric_dictionary.csv -> minimum_group_size")

CSV = "csv"

@st.cache_data
def load():
    emp = pd.read_csv(f"{CSV}/dim_employee.csv")
    dept = pd.read_csv(f"{CSV}/dim_department.csv")
    team = pd.read_csv(f"{CSV}/dim_team.csv")
    metric_dict = pd.read_csv(f"{CSV}/metric_dictionary.csv")
    payroll = pd.read_csv(f"{CSV}/fact_payroll.csv")
    headcount = pd.read_csv(f"{CSV}/fact_headcount_monthly.csv")
    return emp, dept, team, metric_dict, payroll, headcount

dim_emp, dim_dept, dim_team, metric_dict_df, fact_payroll, fact_head = load()

# Join for drill-down: Company -> Department -> Team
df_base = dim_emp.merge(dim_dept, on="dept_id", how="left").merge(dim_team, on="team_id", how="left")

st.sidebar.header("Login as Role (demo_users.csv)")
role = st.sidebar.selectbox("Select Role", ["ADMIN", "HR", "MANAGER", "EXECUTIVE"])
my_dept = st.sidebar.selectbox("Your Dept (if MANAGER)", dim_dept['dept_name'].unique())

# ---- 1. LIST METRICS & ROLE SAFETY ----
st.subheader("1. Metrics and Role-based Access")

metric_dict_df['minimum_group_size'] = pd.to_numeric(metric_dict_df['minimum_group_size'], errors='coerce').fillna(5)

def allowed_for_role(row, role):
    owner = str(row['owner_team'])
    metric = str(row['metric_name']).lower()
    if role == "ADMIN": 
        return True
    if role == "HR": 
        return "HR" in owner or "Payroll" in owner or "headcount" in metric
    if role == "MANAGER": 
        return "headcount" in metric or "attendance" in metric  # No payroll, no attrition
    if role == "EXECUTIVE": 
        return owner in ["Finance", "HR Analytics"] and "pay" not in metric
    return False

metric_dict_df['allowed_for_'+role] = metric_dict_df.apply(lambda r: allowed_for_role(r, role), axis=1)
allowed_metrics_df = metric_dict_df[metric_dict_df['allowed_for_'+role]]

st.write(f"**Role {role} can access {len(allowed_metrics_df)} metrics:**")
st.dataframe(allowed_metrics_df[['metric_id','metric_name','minimum_group_size','owner_team']], use_container_width=True)

# ---- 2. EXPLORER ----
c1, c2, c3 = st.columns(3)
with c1:
    sel_metric_name = st.selectbox("2. Choose Metric", allowed_metrics_df['metric_name'].tolist())
    sel_row = metric_dict_df[metric_dict_df['metric_name'] == sel_metric_name].iloc[0]
    MIN_GROUP = int(sel_row['minimum_group_size']) if sel_row['minimum_group_size'] >=5 else 5
with c2:
    dimension = st.selectbox("3. Choose Dimension", ["dept_name", "team_name"])
with c3:
    drill = st.selectbox("4. Drill Level", ["Company", "Department", "Team"])

st.info(f"Selected: **{sel_metric_name}** | Minimum Group Size Required = **{MIN_GROUP}** | Role = {role}")

# Filter for MANAGER
view_df = df_base.copy()
if role == "MANAGER":
    view_df = df_base[df_base['dept_name'] == my_dept]
    st.warning(f"MANAGER view: Only showing {my_dept} - {len(view_df)} employees")

# ---- 3. DRILL-DOWN + PRIVACY HIDE ----
st.divider()
st.subheader(f"Drill-down: {drill} by {dimension}")

if drill == "Company":
    n = len(view_df)
    if n < MIN_GROUP:
        st.error(f"🔒 Hidden - Group size {n} < required {MIN_GROUP} for '{sel_metric_name}'. Hidden to prevent privacy incident.")
    else:
        st.metric(f"Company - {sel_metric_name}", f"{n} records", f"Group Size OK: {n} >= {MIN_GROUP}")
else:
    group_col = "dept_name" if drill == "Department" else "team_name"
    grouped = view_df.groupby(group_col).size().reset_index(name="group_size")
    
    # Apply privacy rule
    grouped['status'] = grouped['group_size'].apply(lambda x: f"🔒 Hidden - Only {x} < {MIN_GROUP}" if x < MIN_GROUP else f"Visible ({x})")
    grouped['is_hidden'] = grouped['group_size'] < MIN_GROUP
    
    st.dataframe(grouped, use_container_width=True)
    
    safe = grouped[~grouped['is_hidden']]
    hidden = grouped[grouped['is_hidden']]
    
    if not safe.empty:
        st.bar_chart(safe.set_index(group_col)['group_size'])
        st.success(f"{len(safe)} groups are visible")
    if not hidden.empty:
        st.error(f"🔒 {len(hidden)} groups HIDDEN for privacy (size < {MIN_GROUP}): {', '.join(hidden[group_col].tolist())}")

# ---- 4. BREAK-IT NOTES ----
st.divider()
st.subheader("Think for Yourself")

st.markdown("""
**Q: A manager has a team of 3. Should they see attrition for their team?**

**My Answer:**

No, I think a manager should not see attrition for a team of 3.

The reason is, if there are only 3 people in a team and 1 person leaves, the attrition becomes 33%. The manager will easily know who left. This is a privacy problem.

In our metric_dictionary.csv, the minimum group size for attrition is 10. So we should hide the data if the group has less than 10 people.

Even if the person is the manager of that team, the rule should be same for everyone. We should show message like "Hidden - Need minimum 10 people" instead of showing the real data.
""")