import duckdb
from datetime import datetime

con = duckdb.connect('pulseiq.duckdb')

con.execute("DROP TABLE IF EXISTS dq_results")
con.execute("""
CREATE TABLE dq_results (
  check_id VARCHAR,
  check_name VARCHAR,
  table_name VARCHAR,
  bad_rows INTEGER,
  status VARCHAR,
  run_time TIMESTAMP,
  severity VARCHAR
)
""")

checks = {
 "DQ-C03": ("Unique payroll rows", "fact_payroll", 
            "SELECT employee_id, date_key, COUNT(*) FROM fact_payroll GROUP BY 1,2 HAVING COUNT(*)>1", 
            "Critical"),
            
 "DQ-C04": ("No orphan employees", "fact_payroll", 
            "SELECT f.* FROM fact_payroll f LEFT JOIN dim_employee d ON f.employee_id=d.employee_id WHERE d.employee_id IS NULL", 
            "Critical"),
            
 "DQ-C06": ("Unpaid leave negative", "fact_payroll", 
            "SELECT * FROM fact_payroll WHERE lop_days < 0", 
            "Warning"),
            
 "DQ-C09": ("Task dates sensible", "fact_task", 
            "SELECT * FROM fact_task WHERE completed_date < started_date", 
            "Warning"),
            
 "DQ-C10": ("Leave dates sensible", "fact_leave", 
            "SELECT * FROM fact_leave WHERE end_date < start_date", 
            "Warning"),
            
 "DQ-C14": ("Minimum group size", "dim_employee", 
            "SELECT department_id, COUNT(*) FROM dim_employee GROUP BY 1 HAVING COUNT(*) < 3", 
            "Critical"),
}

print("--- Running DQ Checks ---")
for cid, (cname, tbl, sql, sev) in checks.items():
    bad = con.execute(sql).fetchall()
    cnt = len(bad)
    status = "FAIL" if cnt > 0 else "PASS"
    con.execute("INSERT INTO dq_results VALUES (?,?,?,?,?,?,?)", 
                (cid, cname, tbl, cnt, status, datetime.now(), sev))
    print(f"{cid}: {status} - bad_rows={cnt}")

df = con.execute("SELECT * FROM dq_results").fetchdf()
print("\nFinal Result:")
print(df.to_string())
con.close()