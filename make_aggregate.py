import duckdb
import pandas as pd
import os

con = duckdb.connect('warehouse/pulseiq.duckdb')

# The correct columns are department_id and headcount_end
# Your table does not have 'department' or 'headcount' columns
df = con.execute("""
    SELECT 
        department_id, 
        SUM(headcount_end) as headcount 
    FROM fact_headcount_monthly 
    GROUP BY department_id
""").df()

print(df)

os.makedirs('data', exist_ok=True)
df.to_parquet('data/pulseiq_aggregates.parquet')

print("Done! File created: data/pulseiq_aggregates.parquet")
con.close()