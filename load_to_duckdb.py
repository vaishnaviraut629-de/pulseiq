import duckdb
import pandas as pd
from pathlib import Path

con = duckdb.connect('pulseiq.duckdb')
csv_folder = Path("csv")

for f in csv_folder.glob("*.csv"):
    table = f.stem.lower()
    df = pd.read_csv(f)
    con.execute(f"DROP TABLE IF EXISTS {table}")
    con.execute(f"CREATE TABLE {table} AS SELECT * FROM df")
    print(f"{table}: {len(df)} rows loaded")

print("--- pulseiq.duckdb ready ---")
con.close()