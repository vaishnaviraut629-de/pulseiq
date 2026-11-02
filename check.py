import pandas as pd, duckdb
xls = pd.ExcelFile('PulseIQ_Dataset.xlsx')
con = duckdb.connect('pulseiq.duckdb')

for name in ['dim_account', 'dim_vendor', 'fact_expense']:
    df = pd.read_excel(xls, sheet_name=name)
    df.columns = [c.strip().lower().replace(' ','_') for c in df.columns]
    con.execute(f"DROP TABLE IF EXISTS {name}")
    con.execute(f"CREATE TABLE {name} AS SELECT * FROM df")

print("Creating Views... FINAL FIX")

con.execute("""
CREATE OR REPLACE VIEW v_pnl AS
SELECT 
  d.year_month as month,
  SUM(CASE WHEN LOWER(a.account_type) LIKE '%income%' THEN -l.signed_amount_debit_positive ELSE 0 END) as revenue,
  SUM(CASE WHEN LOWER(a.account_type) LIKE '%expense%' THEN l.signed_amount_debit_positive ELSE 0 END) as expense
FROM fact_ledger l
JOIN dim_account a ON l.account_code = a.account_code
JOIN dim_date d ON l.date_key = d.date_key
WHERE LOWER(a.is_group) = 'n'
GROUP BY 1 ORDER BY 1
""")

con.execute("""
CREATE OR REPLACE VIEW v_expense_by_category AS
SELECT a.account_name as category, SUM(l.signed_amount_debit_positive) as total
FROM fact_ledger l JOIN dim_account a ON l.account_code=a.account_code
WHERE LOWER(a.account_type) LIKE '%expense%' AND LOWER(a.is_group) = 'n'
GROUP BY 1 ORDER BY total DESC
""")

con.execute("""
CREATE OR REPLACE VIEW v_top_vendor AS
SELECT v.vendor_name, SUM(e.total_amount) as total
FROM fact_expense e JOIN dim_vendor v ON e.vendor_id = v.vendor_id
GROUP BY 1 ORDER BY total DESC LIMIT 10
""")

print(con.execute("SELECT * FROM v_pnl ORDER BY month").df().to_string())
print("\nVIEWS READY! Task 11 Done")