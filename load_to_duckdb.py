import duckdb
import os

con = duckdb.connect('pulseiq.duckdb')

csv_folder = 'csv'
for file in os.listdir(csv_folder):
    if file.endswith('.csv'):
        table_name = file.replace('.csv','')
        path = os.path.join(csv_folder, file).replace('\\','/')
        try:
            con.execute(f"DROP TABLE IF EXISTS {table_name}")
            con.execute(f"CREATE TABLE {table_name} AS SELECT * FROM read_csv('{path}', AUTO_DETECT=TRUE)")
            print(f"Loaded {table_name}")
        except Exception as e:
            print(f"Failed {table_name}: {e}")

print("\nAll tables in DB:")
print(con.execute("SHOW TABLES").fetchdf().to_string())
con.close()