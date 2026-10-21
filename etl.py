import duckdb, pandas as pd
con = duckdb.connect("pulseiq.duckdb")
tables = ["fact_payroll","fact_task","fact_leave","fact_ledger","fact_invoice"]
summary = []
for table in tables:
    df = con.execute(f"SELECT * FROM {table}").df()
    rows_in = len(df)
    bad = df.isna().any(axis=1)
    passed_df = df[~bad]
    q_df = df[bad].copy()
    if not q_df.empty:
        q_df["quarantine_reason"] = "NULL violates NOT NULL"
    con.execute(f"DROP TABLE IF EXISTS {table}_clean")
    con.execute(f"DROP TABLE IF EXISTS {table}_quarantine")
    con.execute(f"CREATE TABLE {table}_clean AS SELECT * FROM passed_df")
    if not q_df.empty:
        con.execute(f"CREATE TABLE {table}_quarantine AS SELECT * FROM q_df")
    else:
        con.execute(f"CREATE TABLE {table}_quarantine AS SELECT * FROM {table} WHERE 1=0")
    summary.append([table, rows_in, len(passed_df), rows_in-len(passed_df)])
    print(f"{table}: IN={rows_in} PASSED={len(passed_df)} QUAR={rows_in-len(passed_df)}")
summary_df = pd.DataFrame(summary, columns=["table_name","rows_in","rows_passed","rows_quarantined"])
con.execute("DROP TABLE IF EXISTS etl_summary")
con.execute("CREATE TABLE etl_summary AS SELECT * FROM summary_df")
print(summary_df)
con.close()