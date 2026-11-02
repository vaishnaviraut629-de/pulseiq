import streamlit as st
import duckdb
import plotly.express as px

st.set_page_config(layout="wide")
st.title("📊 Task 11: Profit & Loss - README Tied")

con = duckdb.connect('pulseiq.duckdb', read_only=True)

# Load P&L
df = con.execute("SELECT * FROM v_pnl ORDER BY month").df()
df['profit'] = df['revenue'] - df['expense']
df['margin_pct'] = (df['profit'] / df['revenue'] * 100).round(2)

# KPI Row
m = st.selectbox("Select Month", df['month'].tolist(), index=len(df)-1)
row = df[df['month'] == m].iloc[0]

c1, c2, c3, c4 = st.columns(4)
c1.metric("Revenue", f"₹{row['revenue']:,.0f}")
c2.metric("Expense", f"₹{row['expense']:,.0f}")
c3.metric("Profit", f"₹{row['profit']:,.0f}")
c4.metric("Margin %", f"{row['margin_pct']}%")

# Main Chart - README Tie
st.subheader("Revenue vs Expense vs Profit (Month-wise)")
fig = px.line(df, x='month', y=['revenue','expense','profit'], markers=True)
fig.update_layout(xaxis_tickangle=-45)
st.plotly_chart(fig, use_container_width=True)

# Table
st.dataframe(df.sort_values('month', ascending=False), use_container_width=True)

col1, col2 = st.columns(2)
with col1:
    st.subheader("Expense by Category")
    exp_df = con.execute("SELECT * FROM v_expense_by_category").df()
    st.plotly_chart(px.bar(exp_df, x='total', y='category', orientation='h'), use_container_width=True)
    st.dataframe(exp_df, use_container_width=True)

with col2:
    st.subheader("Top 10 Vendors")
    ven_df = con.execute("SELECT * FROM v_top_vendor").df()
    st.plotly_chart(px.bar(ven_df, x='total', y='vendor_name', orientation='h'), use_container_width=True)
    st.dataframe(ven_df, use_container_width=True)

st.success("Task 11 Complete - P&L ties to fact_ledger + dim_account (is_group='n' filter applied)")