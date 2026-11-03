import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.title("Task 14: AI Signals Dashboard")
st.markdown("### AI-generated, for human review")

xls = pd.ExcelFile('PulseIQ_Dataset.xlsx')
anom = pd.read_excel(xls, 'fact_anomaly')
fc = pd.read_excel(xls, 'fact_forecast')
risk = pd.read_excel(xls, 'fact_attrition_risk')

try:
    head = pd.read_excel(xls, 'fact_headcount_monthly')
except:
    head = pd.DataFrame()

# 1. ANOMALIES
st.subheader("1. Anomalies by Type - Money at Risk")
st.caption("AI-generated, for human review")

agg = anom.groupby('reason_code')['money_at_risk'].sum().reset_index()
agg = agg.sort_values('money_at_risk', ascending=False)
fig1 = px.bar(agg, x='reason_code', y='money_at_risk', text_auto=',.0f')
st.plotly_chart(fig1, use_container_width=True)
st.info("Plain Note: Highest risk on top. Check it first.")
st.dataframe(agg)

# 2. FORECAST
st.subheader("2. Forecast vs Actual with Confidence Band")
st.caption("AI-generated, for human review")

fc['forecast_month'] = pd.to_datetime(fc['forecast_month'])
fc = fc.sort_values('forecast_month')

fig2 = go.Figure()
fig2.add_trace(go.Scatter(x=fc['forecast_month'], y=fc['forecast_value'], name='Forecast', mode='lines+markers'))
fig2.add_trace(go.Scatter(x=fc['forecast_month'], y=fc['upper_80'], name='Upper', line=dict(width=0), showlegend=False))
fig2.add_trace(go.Scatter(x=fc['forecast_month'], y=fc['lower_80'], name='Confidence Band', fill='tonexty', fillcolor='rgba(100,100,255,0.2)', line=dict(width=0)))

# Add actuals if available
if not head.empty:
    # find date column safely
    date_col = None
    for c in head.columns:
        if 'month' in c.lower() or 'date' in c.lower():
            date_col = c
            break
    if date_col is None:
        date_col = head.columns[0]
    
    head[date_col] = pd.to_datetime(head[date_col], errors='coerce')
    # count headcount
    actual = head.groupby(date_col).size().reset_index(name='actual_value')
    fig2.add_trace(go.Scatter(x=actual[date_col], y=actual['actual_value'], name='Actual', mode='lines+markers'))

st.plotly_chart(fig2, use_container_width=True)
st.info("Plain Note: Forecast is an estimate, not a promise. Wide band = low confidence.")

# 3. ERROR TABLE
st.subheader("3. Forecast Error Table")
st.dataframe(fc[['forecast_month','forecast_value','lower_80','upper_80']])
st.warning("Think: 12% error - good? Check if seasonal/festival month. If normal month, 12% is high.")

# 4. ATTRITION
st.subheader("4. Attrition Risk")
st.caption("AI-generated, for human review")
st.dataframe(risk.sort_values('risk_score_12m', ascending=False).head(10))