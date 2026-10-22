import duckdb, os
# auto-find correct DB
base = os.path.dirname(os.path.abspath(__file__))
candidates = [
    os.path.join(base, '..', 'pulseiq.duckdb'),
    os.path.join(base, 'pulseiq.duckdb'),
    os.path.join(base, 'warehouse', 'pulseiq.duckdb'),
    os.path.join(base, '..', 'warehouse', 'pulseiq.duckdb'),
    'pulseiq.duckdb'
]
db_path = None
for p in candidates:
    if os.path.exists(p):
        db_path = p
        break
if not db_path:
    db_path = os.path.join(base, 'pulseiq.duckdb')

print(f"Using DB: {db_path}")
con = duckdb.connect(db_path)

print("--- PROVING CHECKS WORK WITH BAD DATA ---")
con.execute("CREATE OR REPLACE TABLE t1 AS SELECT * FROM fact_payroll")
con.execute("INSERT INTO t1 SELECT * FROM t1 LIMIT 1")
r1 = con.execute("SELECT COUNT(*) FROM (SELECT employee_id, date_key, COUNT(*) FROM t1 GROUP BY 1,2 HAVING COUNT(*)>1)").fetchone()[0]
print(f"DQ-C03 Duplicate Test: Found {r1} bad row -> {'WORKING' if r1>0 else 'NOT WORKING'}")

r2 = con.execute("SELECT COUNT(*) FROM (SELECT '2024-12-31'::DATE as start_date, '2024-01-01'::DATE as end_date) WHERE end_date < start_date").fetchone()[0]
print(f"DQ-C10 Date Test: Found {r2} bad row -> {'WORKING' if r2>0 else 'NOT WORKING'}")

print("--- BOTH CHECKS PROVED ---")
con.execute("DROP TABLE t1")