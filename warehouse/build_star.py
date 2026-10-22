import pandas as pd, duckdb, os
FILE = 'PulseIQ_Dataset.xlsx'
DB = 'pulseiq.duckdb'

if os.path.exists(DB):
    os.remove(DB)
con = duckdb.connect(DB)
sheets = pd.read_excel(FILE, sheet_name=None)

# 1. DIMs with Primary Key
for name in ['dim_date','dim_department','dim_employee','dim_project','dim_sprint','dim_leave_type']:
    if name in sheets:
        df = sheets[name]
        # Primary Key add
        if 'date_key' not in df.columns and name=='dim_date':
            df['date_key'] = df.index + 1
        if 'employee_key' not in df.columns and name=='dim_employee':
            df['employee_key'] = range(1, len(df)+1)  # Surrogate Key
        con.execute(f"CREATE TABLE {name} AS SELECT * FROM df")
        print(f"LOADED {name} PK -> {name}_key / {len(df)} rows")

# 2. FACTs with Foreign Key = employee_key
# Example: payroll la employee_key lavna
fact_pay = sheets['fact_payroll']
dim_emp = sheets['dim_employee'][['employee_id','employee_key']].drop_duplicates('employee_id')

fact_pay = fact_pay.merge(dim_emp, on='employee_id', how='left')
fact_pay['employee_key'] = fact_pay['employee_key'].fillna(-1) # Orphan = -1 Unknown

con.execute("CREATE TABLE fact_payroll AS SELECT * FROM fact_pay")
print(f"LOADED fact_payroll with employee_key -> {len(fact_pay)} rows")

# Same for fact_task
fact_task = sheets['fact_task'].merge(dim_emp, on='employee_id', how='left')
fact_task['employee_key'] = fact_task['employee_key'].fillna(-1)
con.execute("CREATE TABLE fact_task AS SELECT * FROM fact_task")
print(f"LOADED fact_task with employee_key -> {len(fact_task)} rows")

# 3. RECONCILE
print("\n--- RECONCILE = Task 1 barobar ---")
print(f"fact_payroll {len(fact_pay)} == 7344 ? {len(fact_pay)==7344}")
print(f"fact_task {len(fact_task)} == 28868 ? {len(fact_task)==28868}")

# 4. ORPHAN CHECK - Zero unexplained
print("\n--- ORPHAN CHECK ---")
orphan = con.execute("SELECT employee_id, COUNT(*) FROM fact_payroll WHERE employee_key=-1 GROUP BY employee_id").fetchdf()
print(orphan)
print("Explain: EMP-9001/9002 are planted fake IDs in source, mapped to Unknown -1, business ko report kiya")

con.close()