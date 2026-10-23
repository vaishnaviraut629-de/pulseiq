import duckdb
import pathlib
base = pathlib.Path(__file__).parent.parent
db_path = base / "warehouse" / "pulseiq.duckdb"
con = duckdb.connect(str(db_path))
print("Creating KPI views...")
tables = [r[0] for r in con.execute("SHOW TABLES").fetchall()]
print(f"Tables found: {tables}")
con.execute("CREATE OR REPLACE VIEW kpi_attendance_rate AS SELECT * FROM fact_attendance_monthly")
print("Created view kpi_attendance_rate")
con.execute("CREATE OR REPLACE VIEW kpi_payroll_cost AS SELECT * FROM fact_payroll")
print("Created view kpi_payroll_cost")
con.execute("CREATE OR REPLACE VIEW kpi_leave_utilization AS SELECT * FROM fact_leave")
print("Created view kpi_leave_utilization")
con.execute("CREATE OR REPLACE VIEW kpi_anomaly_count AS SELECT * FROM fact_task")
print("Created view kpi_anomaly_count")
con.execute("CREATE OR REPLACE VIEW kpi_invoice_status AS SELECT * FROM fact_invoice")
print("Created view kpi_invoice_status")
con.close()
print("SUCCESS - All KPI views created")
