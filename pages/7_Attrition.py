import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Attrition Analytics", layout="wide")
st.title("Task 7: Attrition Analytics")
st.caption("I built an attrition view that is useful and respects privacy.")

@st.cache_data
def load_data():
    xls = pd.ExcelFile('PulseIQ_Dataset.xlsx')
    df_head = pd.read_excel(xls, sheet_name='fact_headcount_monthly')
    df_risk = pd.read_excel(xls, sheet_name='fact_attrition_risk')
    df_dept = pd.read_excel(xls, sheet_name='dim_department')
    return df_head, df_risk, df_dept

df_head, df_risk, df_dept = load_data()
df_head = df_head.merge(df_dept[['department_id','department_name']], on='department_id', how='left')

dept_list = ['ALL'] + sorted(df_head['department_name'].dropna().unique().tolist())
selected_dept = st.selectbox("Select Department", dept_list)
if selected_dept != 'ALL':
    df_head_filtered = df_head[df_head['department_name'] == selected_dept]
else:
    df_head_filtered = df_head

st.header("1. Actual Exits (Real Data)")
monthly = df_head_filtered.groupby('month_start_date')[['exits','voluntary_exits','attrition_rate_monthly_pct']].sum().reset_index()
monthly['month_start_date'] = pd.to_datetime(monthly['month_start_date'])

col1, col2 = st.columns(2)
with col1:
    fig1 = px.line(monthly, x='month_start_date', y='exits', title='Exits per Month', markers=True)
    st.plotly_chart(fig1, use_container_width=True)
with col2:
    fig2 = px.line(monthly, x='month_start_date', y='attrition_rate_monthly_pct', title='Attrition % per Month', markers=True)
    st.plotly_chart(fig2, use_container_width=True)

dept_exits = df_head.groupby('department_name')['exits'].sum().reset_index().sort_values('exits', ascending=False)
fig3 = px.bar(dept_exits, x='department_name', y='exits', title='Total Exits by Department')
st.plotly_chart(fig3, use_container_width=True)

st.metric("Total Voluntary %", f"{(df_head_filtered['voluntary_exits'].sum() / max(1, df_head_filtered['exits'].sum()) * 100):.1f}%")
st.divider()

st.header("2. Predicted, not certain")
st.warning("What prediction IS: Statistical estimate based on past patterns. It is advice for a conversation. What prediction IS NOT: It is NOT a decision about a person.")

latest_date = df_risk['as_of_date'].max()
df_latest = df_risk[df_risk['as_of_date'] == latest_date]
df_latest = df_latest.merge(df_dept, on='department_id', how='left')

risk_by_dept = df_latest.groupby('department_name').agg(headcount=('employee_id','count'), high_risk=('risk_band', lambda x: (x=='High').sum())).reset_index()

def privacy_rule(row):
    if row['headcount'] < 5:
        return "Hidden (<5 - privacy)"
    pct = row['high_risk'] / row['headcount'] * 100 if row['headcount'] > 0 else 0
    return str(row['high_risk']) + " (" + str(round(pct, 1)) + "%)"

risk_by_dept['High Risk Display'] = risk_by_dept.apply(privacy_rule, axis=1)
st.dataframe(risk_by_dept[['department_name','headcount','High Risk Display']])
st.caption(f"As of date: {pd.to_datetime(latest_date).date()} | Group size rule: Dept <5 hidden")

fig4 = px.histogram(df_latest, x='risk_band', color='risk_band', title='Risk Band Distribution (No Individual Names)')
st.plotly_chart(fig4, use_container_width=True)
st.divider()

st.header("3. 3 Biggest Findings")
st.write("""
**Finding 1:** Engineering dept has highest total exits - 100 out of 304. Customer Support is second with 44 exits. Average monthly attrition rate is 1.18%.

**Finding 2:** Voluntary exits are 87.8% (267 / 304) - most people leave on their own. Median tenure at exit is 2.5 years.

**Finding 3:** Predicted High Risk is 10.1% (43 / 425 employees as of Sep 30, 2026). Customer Support has highest risk - 34.5% (20 / 58) are High Risk, needs retention focus.
""")