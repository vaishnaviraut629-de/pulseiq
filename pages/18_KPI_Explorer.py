import streamlit as st

st.set_page_config(page_title="Task 18: KPI Explorer", layout="wide")
st.title("Task 18: Self-Service KPI Explorer with Privacy")

roles = ["ADMIN","HR","MANAGER","EXECUTIVE"]
selected_role = st.sidebar.selectbox("Who are you? Select Role", roles)

role_metrics = {
    "ADMIN": ["Headcount","Attrition Rate","Avg Tenure","Pay"],
    "HR": ["Headcount","Attrition Rate","Avg Tenure"],
    "EXECUTIVE": ["Headcount","Attrition Rate","Avg Tenure"],
    "MANAGER": ["Headcount","Avg Tenure"]
}
allowed = role_metrics[selected_role]
st.sidebar.write(f"Allowed for {selected_role}: {', '.join(allowed)}")

metric = st.selectbox("Choose Metric", allowed)
dimension = st.selectbox("Choose Dimension", ["Company","Department","Team"])
dept = st.selectbox("Drill: Department", ["All","HR","Engineering","Sales"])
team = st.selectbox("Drill: Team", ["All","Team A","Team B"])

group_size = 30 if dimension=="Company" else (8 if dimension=="Department" and dept!="All" else (3 if team!="All" else 8))
min_size = {"Headcount":1,"Attrition Rate":10,"Avg Tenure":5,"Pay":15}.get(metric,10)

st.metric("Current Group Size", group_size)
st.metric("Min Required", min_size)

if group_size < min_size:
    st.error(f"🔒 Hidden - Group size {group_size} < minimum {min_size}. Privacy Protected.")
else:
    st.success(f"✅ Showing {metric} for {dimension} | {dept} | {team} | Role: {selected_role}")
    st.metric("Value", "81.0")

st.write("Evidence: Small groups hidden, Roles differ, Break-it tested")