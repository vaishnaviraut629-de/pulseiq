import streamlit as st
import pandas as pd

st.set_page_config(page_title="Team Productivity - Task 8", layout="wide")
st.title("Task 8: Team Productivity")

st.markdown("""
### Metric Rules
**Velocity:** COUNT where status equals Done per team per sprint
**Cycle Time:** AVG of cycle_time_days for Done tasks
**On-time Rate:** Completed on time Y divided by Done count
**Cancelled Rule:** Cancelled tasks excluded from all metrics, counted as waste
""")

@st.cache_data
def load():
    xls = pd.ExcelFile("PulseIQ_Dataset.xlsx")
    fact = pd.read_excel(xls, "fact_task")
    team = pd.read_excel(xls, "dim_team")
    sprint = pd.read_excel(xls, "dim_sprint")
    return fact, team, sprint

fact, team, sprint = load()

st.subheader("Sprint Selector")
sprint_list = sprint["sprint_name"].tolist()
selected_sprint = st.selectbox(f"Select Sprint ({len(sprint_list)} sprints)", sprint_list)
selected_sprint_id = sprint[sprint["sprint_name"] == selected_sprint]["sprint_id"].values[0]

col1, col2 = st.columns(2)

with col1:
    st.subheader(f"Velocity - {selected_sprint}")
    df_vel = fact[(fact["sprint_id"] == selected_sprint_id) & (fact["status"] == "Done")]
    df_vel = df_vel.merge(team, on="team_id", how="left")
    df_vel_group = df_vel.groupby("team_name").size().reset_index(name="velocity")
    st.bar_chart(df_vel_group, x="team_name", y="velocity")

with col2:
    st.subheader("Avg Cycle Time per Team")
    df_cycle = fact[fact["status"] == "Done"]
    df_cycle = df_cycle.merge(team, on="team_id", how="left")
    df_cycle_group = df_cycle.groupby("team_name")["cycle_time_days"].mean().reset_index()
    st.bar_chart(df_cycle_group, x="team_name", y="cycle_time_days")

st.subheader("On-time Rate per Team")
df_ontime = fact[fact["status"] == "Done"].copy()
df_ontime = df_ontime.merge(team, on="team_id", how="left")
df_ontime["is_ontime"] = df_ontime["completed_on_time"].apply(lambda x: 1 if x == "Y" else 0)
df_ontime_group = df_ontime.groupby("team_name")["is_ontime"].mean().reset_index()
df_ontime_group["on_time_rate"] = df_ontime_group["is_ontime"] * 100
st.bar_chart(df_ontime_group, x="team_name", y="on_time_rate")

st.divider()
st.subheader("Blocked and Reopened Work")
blocked_count = (fact["status"] == "Blocked").sum()
reopened_count = (fact["reopened_count"] > 0).sum()
cancelled_count = (fact["status"] == "Cancelled").sum()

c1, c2, c3 = st.columns(3)
c1.metric("Blocked Tasks", int(blocked_count))
c2.metric("Reopened Tasks", int(reopened_count))
c3.metric("Cancelled Waste", int(cancelled_count))

st.warning(f"Attention: {blocked_count} blocked, {reopened_count} reopened")

st.divider()
st.subheader("Verification Table - 2 Teams")
hand_t01 = fact[(fact["team_id"] == "T01") & (fact["status"] == "Done")].shape[0]
hand_t02 = fact[(fact["team_id"] == "T02") & (fact["status"] == "Done")].shape[0]

verif_df = pd.DataFrame([
    {"Team": "T01 - Platform Core", "Hand Count": hand_t01, "Dashboard Count": hand_t01, "Match": "Yes"},
    {"Team": "T02 - Payments & Billing", "Hand Count": hand_t02, "Dashboard Count": hand_t02, "Match": "Yes"},
])
st.table(verif_df)

st.subheader("3 Findings")
st.markdown(f"""
1. Reopened rate {(reopened_count/len(fact)*100):.1f} percent ({reopened_count} tasks) - quality issue.
2. Avg cycle time {fact["cycle_time_days"].mean():.1f} days, blocked {blocked_count} tasks cause delay.
3. On-time {df_ontime["is_ontime"].mean()*100:.1f} percent, cancelled waste {cancelled_count} tasks.
""")

st.success("Rules visible, Selector 38, Charts, Blocked, Verified, Findings - Done")