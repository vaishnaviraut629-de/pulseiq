import duckdb
con = duckdb.connect('warehouse/pulseiq.duckdb')

con.execute("""
CREATE OR REPLACE VIEW v_pnl AS
SELECT 
    CAST(strftime(CAST(entry_date AS DATE), '%Y-%m') AS VARCHAR) as month,
    SUM(CASE WHEN a.account_type='Revenue' THEN l.credit ELSE 0 END) as revenue,
    SUM(CASE WHEN a.account_type='Expense' THEN l.debit ELSE 0 END) as expense
FROM fact_ledger l 
JOIN dim_account a ON CAST(l.account_code AS VARCHAR)=a.account_id
WHERE a.is_group='N'
GROUP BY 1
ORDER BY 1
""")

con.execute("""
CREATE OR REPLACE VIEW v_expense_by_category AS
SELECT CAST(category_account AS VARCHAR) as category, SUM(total_amount) as total 
FROM fact_expense GROUP BY 1 ORDER BY total DESC
""")

con.execute("""
CREATE OR REPLACE VIEW v_top_vendor AS
SELECT v.vendor_name, SUM(e.total_amount) as total 
FROM fact_expense e JOIN dim_vendor v ON CAST(e.vendor_id AS VARCHAR)=v.vendor_id 
GROUP BY 1 ORDER BY total DESC LIMIT 10
""")

print("SUCCESS - v_pnl created")
print(con.execute("SELECT * FROM v_pnl").fetchall())