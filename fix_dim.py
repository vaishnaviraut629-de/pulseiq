import duckdb
con = duckdb.connect('warehouse/pulseiq.duckdb')

con.execute("DROP TABLE IF EXISTS dim_account")
con.execute("""
CREATE TABLE dim_account AS 
SELECT DISTINCT 
CAST(account_code AS VARCHAR) as account_id,
CAST(account_code AS BIGINT) as account_code,
CASE 
 WHEN account_code >= 4000 AND account_code < 5000 THEN 'Revenue'
 WHEN account_code >= 5000 THEN 'Expense'
 ELSE 'Other'
END as account_type,
'N' as is_group
FROM fact_ledger
WHERE account_code IS NOT NULL
""")

con.execute("DROP TABLE IF EXISTS dim_vendor")
con.execute("""
CREATE TABLE dim_vendor AS 
SELECT DISTINCT 
CAST(vendor_id AS VARCHAR) as vendor_id,
CAST(vendor_id AS VARCHAR) as vendor_name 
FROM fact_expense WHERE vendor_id IS NOT NULL
""")

print("dim_account:", con.execute("SELECT * FROM dim_account LIMIT 10").fetchall())
print("Count:", con.execute("SELECT COUNT(*) FROM dim_account").fetchall())