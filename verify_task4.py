import duckdb
con = duckdb.connect('pulseiq.duckdb')

print("---METRIC CATALOG---")
print(con.execute('SELECT metric_id, metric_name, min_group_size FROM metric_catalog').fetchdf().to_string())

print("\n---PRIVACY PROOF D00---")
print(con.execute("SELECT * FROM M01_Headcount WHERE department_id='D00' LIMIT 3").fetchdf().to_string())
