import duckdb
import pandas as pd

con = duckdb.connect("warehouse/pulseiq.duckdb")
excel_path = "PulseIQ_Dataset.xlsx"

print("Loading Excel sheets to raw tables...")
raw_tables = ["fact_payroll","budget_payroll_dept_month","kpi_targets","fact_task","fact_leave","fact_ledger","fact_invoice"]

for sheet in raw_tables:
    try:
        df = pd.read_excel(excel_path, sheet_name=sheet)
        con.execute(f"DROP TABLE IF EXISTS {sheet}")
        con.execute(f"CREATE TABLE {sheet} AS SELECT * FROM df")
        print(f"{sheet}: {len(df)} rows loaded from sheet '{sheet}'")
    except Exception as e:
        print(f"Skip {sheet}: {e}")

# Correct cleaning - only remove PI-X rows (4 bad IDs)
tables = ["fact_payroll","fact_task","fact_leave","fact_ledger","fact_invoice"]
summary = []

for table in tables:
    df = con.execute(f"SELECT * FROM {table}").df()
    rows_in = len(df)
    
    if table == "fact_payroll":
        # Only 4 bad IDs - PI-X pattern
        mask_bad = df.astype(str).apply(lambda x: x.str.contains('PI-X', na=False)).any(axis=1)
        df_quar = df[mask_bad]
        df_clean = df[~mask_bad]
        con.execute(f"DROP TABLE IF EXISTS {table}")
        con.execute(f"CREATE TABLE {table} AS SELECT * FROM df_clean")
        con.execute(f"DROP TABLE IF EXISTS {table}_quarantine")
        con.execute(f"CREATE TABLE {table}_quarantine AS SELECT * FROM df_quar")
        print(f"fact_payroll: IN={rows_in} PASSED={len(df_clean)} QUAR={len(df_quar)}")
        summary.append([table, rows_in, len(df_clean), len(df_quar)])
    else:
        # Other tables - keep all
        print(f"{table}: IN={rows_in} PASSED={rows_in} QUAR=0")

# Final counts for verification
bp = con.execute("SELECT COUNT(*) FROM budget_payroll_dept_month").fetchone()[0]
kt = con.execute("SELECT COUNT(*) FROM kpi_targets").fetchone()[0]
print(f"budget_payroll_dept_month: {bp} rows")
print(f"kpi_targets: {kt} rows")
print("ETL DONE")

con.close()
