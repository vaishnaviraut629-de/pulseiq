import pandas as pd

xls = "PulseIQ_Dataset.xlsx"

payroll = pd.read_excel(xls, sheet_name="fact_payroll")
employee = pd.read_excel(xls, sheet_name="dim_employee")

# 1. Duplicate check
dup = payroll.groupby(['employee_id','run_id']).size().reset_index(name='cnt')
dup = dup[dup['cnt']>1]
print("Duplicate groups:")
print(dup)

# 2. Orphan check
orphan = payroll[~payroll['employee_id'].isin(employee['employee_id'])]
print("\nOrphan rows:")
print(orphan[['payroll_item_id','employee_id','period_end_date','employer_cost']])

# 3. Summary - SIMPLE LINES (no complex f-string)
total_bad_rows = len(dup) + len(orphan)
bad_cost = orphan['employer_cost'].sum()

print("\nTotal bad rows:", total_bad_rows)
print("Total bad cost:", bad_cost) # Get exact 4 payroll_item_ids to exclude
dup_rows = payroll[payroll.duplicated(subset=['employee_id','run_id'], keep='first')]
print("\nExact Duplicate PI-IDs to exclude (keep first, remove second):")
print(dup_rows[['payroll_item_id','employee_id','run_id','employer_cost']])

all_bad = pd.concat([dup_rows, orphan])
print("\nFinal 4 BAD IDs list:")
print(all_bad['payroll_item_id'].tolist())
print("\nTotal bad cost final:", all_bad['employer_cost'].sum())
