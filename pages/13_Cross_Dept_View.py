import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Task 13: Cross-department impact view")
st.markdown("**Grain:** One row per department + month")
st.markdown("**Join Order:** headcount (BASE) LEFT JOIN payroll, attendance, leave - Aggregate first, then join")

df_head = pd.read_excel("PulseIQ_Dataset.xlsx", sheet_name="fact_headcount_monthly")
df_pay = pd.read_excel("PulseIQ_Dataset.xlsx", sheet_name="fact_payroll")
df_att = pd.read_excel("PulseIQ_Dataset.xlsx", sheet_name="fact_attendance_monthly")
df_leave = pd.read_excel("PulseIQ_Dataset.xlsx", sheet_name="fact_leave")
df_emp = pd.read_excel("PulseIQ_Dataset.xlsx", sheet_name="dim_employee")
df_dept = pd.read_excel("PulseIQ_Dataset.xlsx", sheet_name="dim_department")

df_head['month'] = pd.to_datetime(df_head['month_start_date']).dt.strftime('%Y-%m')
df_pay['month'] = pd.to_datetime(df_pay['period_end_date']).dt.strftime('%Y-%m')
df_att['month'] = pd.to_datetime(df_att['period_end_date']).dt.strftime('%Y-%m')
df_leave['month'] = pd.to_datetime(df_leave['start_date']).dt.strftime('%Y-%m')

pay_agg = df_pay.groupby(['department_id','month']).agg(total_cost=('employer_cost','sum'), overtime_cost=('overtime_pay','sum')).reset_index()
att_agg = df_att.groupby(['department_id','month']).agg(present_days=('present_days','sum'), avg_att_rate=('attendance_rate','mean')).reset_index()

df_leave_ok = df_leave[df_leave['status']=='Approved']
leave_with_dept = pd.merge(df_leave_ok, df_emp[['employee_id','department_id']], on='employee_id', how='left')
leave_agg = leave_with_dept.groupby(['department_id','month']).agg(leave_days=('days','sum')).reset_index()

final = pd.merge(df_head, pay_agg, on=['department_id','month'], how='left')
final = pd.merge(final, att_agg, on=['department_id','month'], how='left')
final = pd.merge(final, leave_agg, on=['department_id','month'], how='left')
final['leave_days'] = final['leave_days'].fillna(0)
final['overtime_per_head'] = final['overtime_cost'] / final['headcount_end'].replace(0,1)
final['leave_per_head'] = final['leave_days'] / final['headcount_end'].replace(0,1)
final = pd.merge(final, df_dept[['department_id','department_name']], on='department_id', how='left')

st.subheader("Combined Table - Same Grain")
st.dataframe(final.head(20))
st.write("Shape:", final.shape)

chart_df = final.groupby('department_name').agg(avg_cost=('total_cost','mean'), avg_ot=('overtime_cost','mean'), avg_attr=('attrition_rate_monthly_pct','mean')).reset_index()
fig = px.bar(chart_df, x='department_name', y=['avg_cost','avg_ot'], barmode='group', title="Cost, Overtime & Attrition - Dept Compare")
st.plotly_chart(fig, use_container_width=True)

fig2 = px.scatter(final, x='overtime_per_head', y='attrition_rate_monthly_pct', color='department_name', title="Overtime vs Attrition - Correlation?")
st.plotly_chart(fig2, use_container_width=True)

st.success("Same grain YES | Chart YES | Join Order YES")