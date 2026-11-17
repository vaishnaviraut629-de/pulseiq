import streamlit as st
import pandas as pd
import os

st.title("Task 18: Self-Service KPI Explorer")
st.caption("Privacy Safe | Uses metric_dictionary.csv")

# FIX FOR PATH - works on both local and Streamlit Cloud
def load_csv(file_name):
    possible_paths = [
        f"data/{file_name}",
        f"../data/{file_name}",
        file_name,
        f"/mount/src/pulseiq/data/{file_name}"
    ]
    for p in possible_paths:
        if os.path.exists(p):
            return pd.read_csv(p)
    # last try
    return pd.read_csv(f"data/{file_name}")

try:
    dim_emp = load_csv("dim_employee.csv")
    metric_dict = load_csv("metric_dictionary.csv")
except Exception as e:
    st.error(f"CSV not found, creating dummy. Error: {e}")
    dim_emp = pd.DataFrame({"Department": ["HR","Tech","Sales"]*10, "EmployeeID": range(30)})
    metric_dict = pd.DataFrame({
        'metric_name': ['Headcount', 'Attrition Rate', 'Avg Tenure'],
        'minimum_group_size': [5, 10, 5]
    })

df_base = dim_emp.copy()

dept_col = None
for c in ['Department', 'dept_name', 'department', 'Dept']:
    if c in df_base.columns:
        dept_col = c
        break

if dept_col:
    selected = st.sidebar.selectbox(f"Select {dept_col}", ["All"] + sorted(df_base[dept_col].dropna().unique().tolist()))
    if selected != "All":
        df_base = df_base[df_base[dept_col] == selected]

st.subheader(f"Current Group Size: {len(df_base)}")

for idx, row in metric_dict.iterrows():
    metric_name = row['metric_name'] if 'metric_name' in row else row[0]
    min_size = int(row['minimum_group_size']) if 'minimum_group_size' in row else 5
    if len(df_base) < min_size:
        st.metric(label=metric_name, value="🔒 Hidden", delta=f"n={len(df_base)} < {min_size}")
    else:
        if "Headcount" in str(metric_name):
            st.metric(label=metric_name, value=len(df_base))
        else:
            st.metric(label=metric_name, value="OK")

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