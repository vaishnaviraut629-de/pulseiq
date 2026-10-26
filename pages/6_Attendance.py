import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Task 6: Attendance and Leave Trends")

path = "../PulseIQ_Dataset.xlsx"
try:
    att = pd.read_excel(path, sheet_name="fact_attendance_monthly")
except:
    path = "PulseIQ_Dataset.xlsx"
    att = pd.read_excel(path, sheet_name="fact_attendance_monthly")

leave = pd.read_excel(path, sheet_name="fact_leave")
dim_date = pd.read_excel(path, sheet_name="dim_date")

att['period_end_date'] = pd.to_datetime(att['period_end_date'])

# Dept filter
dept = st.selectbox("Department", ["ALL"] + sorted(att['department_id'].unique().tolist()))
if dept != "ALL":
    att_f = att[att['department_id']==dept]
else:
    att_f = att

# 1. Attendance Rate
monthly = att_f.groupby(att_f['period_end_date'].dt.to_period('M').astype(str))['attendance_rate'].mean().reset_index()
fig1 = px.line(monthly, x='period_end_date', y='attendance_rate', markers=True, title="Attendance Rate by Month")
fig1.add_annotation(x="2025-10", y=0.93, text="Oct 2025: 3 Holidays")
fig1.add_annotation(x="2026-01", y=0.93, text="Jan 2026: 3 Holidays")
st.plotly_chart(fig1)

# 2. Late + OT
monthly2 = att_f.groupby(att_f['period_end_date'].dt.to_period('M').astype(str)).agg(Late=('late_arrivals','sum'), OT=('overtime_hours','sum')).reset_index()
fig2 = px.bar(monthly2, x='period_end_date', y=['Late','OT'], barmode='group')
st.plotly_chart(fig2)

# 3. Leave by Type
leave['start_date'] = pd.to_datetime(leave['start_date'])
leave_g = leave[leave['status']=='Approved'].groupby([leave['start_date'].dt.to_period('M').astype(str), 'leave_type_code'])['days'].sum().reset_index()
fig3 = px.bar(leave_g, x='start_date', y='days', color='leave_type_code', title="Leave by Type")
st.plotly_chart(fig3)

# 4. Heatmap
pivot = att.pivot_table(index='department_id', columns=att['period_end_date'].dt.to_period('M').astype(str), values='attendance_rate')
st.dataframe(pivot)

st.subheader("3 Insights")
st.write("""
1. **May 2026 - 92.67% lowest**: D10 83.6%, D08 85.2%
2. **Jan 2026 - 93.12% dip**: 3 holidays + 19 working days only, not a crisis
3. **Dec 2025 - OT 787 hrs**: 51% above avg, year-end workload
""")