import streamlit as st
import duckdb

st.set_page_config(page_title="Task 12 - Receivables", layout="wide")
st.title("Task 12: Invoices, Receivables and Cash Flow")
st.info("Open Statuses = SENT, OVERDUE, PARTIALLY_PAID - Only these are open")

db_path = 'C:/Users/yadnya/Desktop/pulseiq/warehouse/pulseiq.duckdb'
con = duckdb.connect(db_path, read_only=True)

# 1. Total Open
total_open = con.execute("""
SELECT SUM(balance_due) 
FROM fact_invoice 
WHERE status IN ('SENT','OVERDUE','PARTIALLY_PAID')
""").fetchone()[0]
st.metric("Total Open Receivables", f"₹ {total_open:,.0f}")

# 2. Buckets
aging = con.execute("""
SELECT 
  CASE 
    WHEN days_past_due_at_cutoff BETWEEN 0 AND 30 THEN '0-30 days'
    WHEN days_past_due_at_cutoff BETWEEN 31 AND 60 THEN '31-60 days'
    WHEN days_past_due_at_cutoff BETWEEN 61 AND 90 THEN '61-90 days'
    WHEN days_past_due_at_cutoff > 90 THEN '90+ days'
    ELSE 'Not Due'
  END as bucket,
  SUM(balance_due) as amount
FROM fact_invoice
WHERE status IN ('SENT','OVERDUE','PARTIALLY_PAID')
GROUP BY 1
""").df()

bucket_total = aging['amount'].sum()
st.write(f"Bucket Total = ₹ {bucket_total:,.0f} | Total Open = ₹ {total_open:,.0f} | Match: {abs(bucket_total-total_open) < 1}")
st.subheader("Ageing Buckets")
st.bar_chart(aging.set_index('bucket'))

# 3. Avg Days to Pay
st.subheader("Average Days to Pay by Client")
days_df = con.execute("""
SELECT client_id, AVG(days_to_pay) as avg_days_to_pay
FROM fact_invoice 
WHERE status='PAID' AND days_to_pay IS NOT NULL
GROUP BY 1 ORDER BY avg_days_to_pay DESC LIMIT 10
""").df()
st.dataframe(days_df, use_container_width=True)

# 4. Most Overdue
st.subheader("Clients with Most Overdue Money")
overdue = con.execute("""
SELECT client_id, SUM(balance_due) as total_due
FROM fact_invoice 
WHERE status='OVERDUE'
GROUP BY 1 ORDER BY total_due DESC LIMIT 10
""").df()
st.dataframe(overdue, use_container_width=True)

# 5. Cash In vs Cash Out - FIXED
st.subheader("Cash In vs Cash Out by Month")
cash_in = con.execute("""
SELECT DATE_TRUNC('month', CAST(payment_date AS DATE))::DATE as month, SUM(amount) as cash_in 
FROM fact_invoice_payment GROUP BY 1 ORDER BY 1
""").df()

cash_out = con.execute("""
SELECT DATE_TRUNC('month', CAST(expense_date AS DATE))::DATE as month, SUM(total_amount) as cash_out 
FROM fact_expense GROUP BY 1 ORDER BY 1
""").df()

cash = cash_in.merge(cash_out, on='month', how='outer').fillna(0).sort_values('month')
cash['month_str'] = cash['month'].astype(str)
st.line_chart(cash.set_index('month_str')[['cash_in','cash_out']])
st.dataframe(cash, use_container_width=True)