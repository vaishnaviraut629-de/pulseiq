import streamlit as st
import pandas as pd
import plotly.express as px

st.title("💰 Task 12 - Receivables & Cash Flow")

# Dummy data - CSV nasla tari chalel!
st.subheader("Receivables Summary")
col1, col2, col3 = st.columns(3)
col1.metric("Total Open Receivables", "₹ 12.5 L", "+5%")
col2.metric("Overdue >30 Days", "₹ 3.2 L", "-2%")
col3.metric("Cash Inflow (This Month)", "₹ 8.1 L", "+12%")

st.subheader("Aging Buckets")
aging_data = pd.DataFrame({
    "Bucket": ["0-30 Days", "31-60 Days", "61-90 Days", "90+ Days"],
    "Amount": [500000, 320000, 180000, 250000]
})
fig = px.bar(aging_data, x="Bucket", y="Amount", color="Bucket", title="Receivables Aging")
st.plotly_chart(fig, use_container_width=True)

st.subheader("Cash Flow Trend")
cash_data = pd.DataFrame({
    "Month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
    "Inflow": [6.5, 7.2, 6.8, 8.1, 7.5, 9.0],
    "Outflow": [5.0, 5.5, 5.8, 6.0, 5.9, 6.2]
})
fig2 = px.line(cash_data, x="Month", y=["Inflow", "Outflow"], markers=True, title="Cash Flow Trend")
st.plotly_chart(fig2, use_container_width=True)

st.success("✅ Task 12 Working! No CSV needed!")