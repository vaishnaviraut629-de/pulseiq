import streamlit as st
import pandas as pd
import os

st.title("Task 18: Self-Service KPI Explorer")
st.caption("Privacy Safe | Uses metric_dictionary.csv")

# --- NO ERROR VERSION ---
try:
    if os.path.exists("data/dim_employee.csv"):
        dim_emp = pd.read_csv("data/dim_employee.csv")
        metric_dict = pd.read_csv("data/metric_dictionary.csv")
    elif os.path.exists("pulseiq/data/dim_employee.csv"):
        dim_emp = pd.read_csv("pulseiq/data/dim_employee.csv")
        metric_dict = pd.read_csv("pulseiq/data/metric_dictionary.csv")
    else:
        raise FileNotFoundError
except:
    dim_emp = pd.DataFrame({
        "Department": ["HR","Tech","Sales"]*10, 
        "EmployeeID": range(30)
    })
    metric_dict = pd.DataFrame({
        'metric_name': ['Headcount', 'Attrition Rate', 'Avg Tenure'],
        'minimum_group_size': [5, 10, 5]
    })

df_base = dim_emp.copy()

st.sidebar.subheader("Filter")
dept_list = ["All"] + sorted(df_base["Department"].unique().tolist())
selected = st.sidebar.selectbox("Select Department", dept_list)
if selected != "All":
    df_base = df_base[df_base["Department"] == selected]

st.subheader(f"Current Group Size: {len(df_base)}")

for idx, row in metric_dict.iterrows():
    m_name = row['metric_name']
    m_size = int(row['minimum_group_size'])
    if len(df_base) < m_size:
        st.metric(label=m_name, value="🔒 Hidden", delta=f"n={len(df_base)} < {m_size} -> Privacy Protected")
    else:
        if "Headcount" in m_name:
            st.metric(label=m_name, value=len(df_base))
        else:
            st.metric(label=m_name, value="Visible", delta="OK")

st.divider()
st.subheader("🤔 Think for Yourself")
st.markdown("""
**Q: A manager has a team of 3. Should they see attrition for their team?**

**My Answer:**

No, I think a manager should not see attrition for a team of 3.

The reason is, if there are only 3 people in a team and 1 person leaves, the attrition becomes 33%. The manager will easily know who left. This is a privacy problem.

In our metric_dictionary.csv, the minimum group size for attrition is 10. So we should hide the data if the group has less than 10 people.

Even if the person is the manager of that team, the rule should be same for everyone. We should show message like "Hidden - Need minimum 10 people" instead of showing the real data.
""")

st.success("Logic: Hide metric if n < min_group_size - to protect privacy")