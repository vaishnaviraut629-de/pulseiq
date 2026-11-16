import streamlit as st
import duckdb
from pathlib import Path
import pandas as pd

st.set_page_config(page_title="Task 12 - Receivables", layout="wide")
st.title("Task 12: Invoices, Receivables and Cash Flow")
st.info("Open Statuses = SENT, OVERDUE, PARTIALLY_PAID - Only these are open")

db_path = str(Path(__file__).parent.parent / "pulseiq.duckdb")
con = duckdb.connect(db_path, read_only=True)

# 1. Total Open
total_open = con.execute("""
    SELECT SUM(balance_due) 
    FROM fact_invoice 
    WHERE status IN ('SENT','OVERDUE','PARTIALLY_PAID')
""").fetchone()[0]

st.metric("Total Open Receivables", f"Rs {total_open:,.0f}" if total_open else "Rs 0")

# 2. Aging Buckets
st.subheader("Aging Buckets")
aging = con.execute("""
    SELECT
      CASE
        WHEN days_past_due_at_cutoff BETWEEN 0 AND 30 THEN '0-30'
        WHEN days_past_due_at_cutoff BETWEEN 31 AND 60 THEN '31-60'
        WHEN days_past_due_at_cutoff BETWEEN 61 AND 90 THEN '61-90'
        ELSE '90+'
      END AS bucket,
      SUM(balance_due) AS amount
    FROM fact_invoice
    WHERE status IN ('SENT','OVERDUE','PARTIALLY_PAID')
    GROUP BY