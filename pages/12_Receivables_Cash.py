import streamlit as st
import pandas as pd
import plotly.express as px
import datetime

st.set_page_config(layout="wide")
st.title("💰 Task 12 - Receivables & Cash Flow")

@st.cache_data
def load_data():
    try:
        df = pd.read_csv("data/payroll_data.csv")
        return df
    except:
        return pd.DataFrame()

df = load_data()

if df.empty:
    st.warning("No data found. Upload payroll_data.csv in data folder")
else:
    # Dummy receivables for demo - replace with your actual logic
    st.subheader("Receivables Summary")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Open Receivables", "₹ 12.5 L")
    col2.metric("Overdue >30 Days", "₹ 3.2 L")
    col3.metric("Cash Inflow (This Month)", "₹ 8.1 L")

    # Sample chart
    st.subheader("Aging Buckets")
    aging_data = pd.DataFrame({
        "Bucket": ["0-30 Days", "31-60 Days", "61-90 Days", "90+ Days"],
        "Amount": [500000, 320000, 180000, 250000]
    })
    fig = px.bar(aging_data, x="Bucket", y="Amount", title="Receivables Aging")
    st.plotly_chart(fig, use_container_width=True)

    st.success("Task 12 Fixed! Syntax Error Solved!")

st.info("If you have actual receivables CSV, tell me column names - I will connect real data")