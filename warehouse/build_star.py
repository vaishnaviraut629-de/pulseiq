import pandas as pd
import duckdb
import pathlib

base = pathlib.Path(__file__).parent.parent
csv_dir = base / "csv" if (base / "csv").exists() else base / "data" if (base / "data").exists() else base
db_path = base / "warehouse" / "pulseiq.duckdb"

print(f"CSV dir: {csv_dir}")
con = duckdb.connect(str(db_path))

# Load dim_employee
dim_employee = None
for p in [csv_dir / "dim_employee.csv", base / "warehouse" / "dim_employee.csv", base / "dim_employee.csv"]:
    if p.exists():
        dim_employee = pd.read_csv(p)
        break
if dim_employee is None:
    for f in csv_dir.glob("*employee*"):
        dim_employee = pd.read_csv(f)
        break
if dim_employee is None:
    dim_employee = pd.DataFrame({"employee_id": [], "dim_employee_key": []})

print(f"dim_employee cols: {list(dim_employee.columns)}")

# Load fact_payroll
fact_pay = None
for p in [csv_dir / "fact_payroll.csv", csv_dir / "payroll.csv", base / "fact_payroll.csv"]:
    if p.exists():
        fact_pay = pd.read_csv(p)
        print(f"Loaded {p} with cols {list(fact_pay.columns)}")
        break
if fact_pay is None:
    for f in csv_dir.glob("*payroll*"):
        fact_pay = pd.read_csv(f)
        print(f"Loaded {f}")
        break

if fact_pay is None:
    raise FileNotFoundError("fact_payroll.csv not found")

# --- FIX ---
if 'employee_id' in fact_pay.columns and 'employee_key' not in fact_pay.columns:
    if 'employee_id' in dim_employee.columns and 'dim_employee_key' in dim_employee.columns:
        emp_map = dim_employee[['employee_id', 'dim_employee_key']].drop_duplicates()
        fact_pay = fact_pay.merge(emp_map, on='employee_id', how='left')
        fact_pay['employee_key'] = fact_pay['dim_employee_key'].fillna(-1).astype(int)
        fact_pay = fact_pay.drop(columns=['dim_employee_key'], errors='ignore')
        print("Mapped employee_id -> employee_key")
    else:
        fact_pay['employee_key'] = -1
else:
    fact_pay['employee_key'] = fact_pay['employee_key'].fillna(-1)

print(f"Final rows: {len(fact_pay)}")
con.execute("DROP TABLE IF EXISTS fact_payroll")
con.execute("CREATE TABLE fact_payroll AS SELECT * FROM fact_pay")
print("LOADED fact_payroll")

# Load other facts
for csv_file in csv_dir.glob("fact_*.csv"):
    if "payroll" in csv_file.name:
        continue
    try:
        df = pd.read_csv(csv_file)
        tbl = csv_file.stem
        con.execute(f"DROP TABLE IF EXISTS {tbl}")
        con.execute(f"CREATE TABLE {tbl} AS SELECT * FROM df")
        print(f"LOADED {tbl}")
    except Exception as e:
        print(f"Skip {csv_file.name}: {e}")

con.close()
print("SUCCESS - build_star completed")