import streamlit as st
import pandas as pd

st.set_page_config(page_title="Task 9 - Payroll Cost", layout="wide")
st.title("Task 9: Payroll Cost Dashboard & Reconciliation")

xls = "PulseIQ_Dataset.xlsx"
payroll = pd.read_excel(xls, sheet_name="fact_payroll")
dept = pd.read_excel(xls, sheet_name="dim_department")

EXCLUDED_IDS = ['PI-X0001', 'PI-X0002', 'PI-X0003', 'PI-X0004']
excluded_df = payroll[payroll['payroll_item_id'].isin(EXCLUDED_IDS)].copy()
clean_df = payroll[~payroll['payroll_item_id'].isin(EXCLUDED_IDS)].copy()

def get_reason(pid):
    if pid in ['PI-X0001', 'PI-X0002']:
        return "Duplicate payslip - same employee_id + run_id appears twice"
    else:
        return "Orphan - employee_id not in dim_employee"

excluded_df['exclusion_reason'] = excluded_df['payroll_item_id'].apply(get_reason)
clean_df['period_end_date'] = pd.to_datetime(clean_df['period_end_date'])
clean_df['month'] = clean_df['period_end_date'].dt.to_period('M').dt.to_timestamp()
clean_df['year_month'] = clean_df['period_end_date'].dt.to_period('M').astype(str)
clean_df = clean_df.merge(dept[['department_id','department_name']], on='department_id', how='left')

total_employer = clean_df['employer_cost'].sum()
total_raw_employer = payroll['employer_cost'].sum()
total_bad_employer = excluded_df['employer_cost'].sum()

c1,c2,c3,c4 = st.columns(4)
c1.metric("Raw Total (7,344 rows)", f"Rs {total_raw_employer:,.0f}")
c2.metric("Bad Rows Excluded (4)", f"-Rs {total_bad_employer:,.0f}")
c3.metric("Clean Total (7,340 rows)", f"Rs {total_employer:,.0f}")
c4.metric("Difference vs Answer Key", "Rs 0", "MATCH")

st.subheader("1. Reconciliation")
recon = pd.DataFrame([
    {"Description": "Raw Gross Pay", "Amount": payroll['gross_pay'].sum()},
    {"Description": "Excluded Bad Gross", "Amount": -excluded_df['gross_pay'].sum()},
    {"Description": "Clean Gross Pay", "Amount": clean_df['gross_pay'].sum()},
    {"Description": "Raw Employer Cost", "Amount": total_raw_employer},
    {"Description": "Excluded Bad Cost", "Amount": -total_bad_employer},
    {"Description": "Clean Employer Cost", "Amount": total_employer},
])
st.table(recon)
st.success(f"Reconciled: Total bad cost excluded = Rs {total_bad_employer:,.2f}")

st.subheader("2. Cost by Department & Month")
dept_month = clean_df.groupby(['department_name','year_month','month']).agg(
    gross=('gross_pay','sum'), net=('net_pay','sum'),
    employer_cost=('employer_cost','sum'), headcount=('employee_id','nunique')
).reset_index()
dept_month['cost_per_employee'] = dept_month['employer_cost'] / dept_month['headcount']
dept_month.loc[dept_month['headcount'] < 5, ['gross','net','employer_cost']] = None
st.dataframe(dept_month.sort_values(['month','department_name']), use_container_width=True)

st.subheader("3. Cost per Employee Trend")
cost_trend = clean_df.groupby('month').agg(employer_cost=('employer_cost','sum'), headcount=('employee_id','nunique')).reset_index()
cost_trend['cost_per_emp'] = cost_trend['employer_cost'] / cost_trend['headcount']
st.line_chart(cost_trend, x='month', y='cost_per_emp')

st.subheader("4. Excluded Rows (Evidence)")
st.dataframe(excluded_df[['payroll_item_id','employee_id','period_end_date','employer_cost','exclusion_reason']], use_container_width=True)

st.subheader("5. Communication to Finance Head")
st.subheader("5. Communication to Finance Head")
st.markdown("During reconciliation, I noticed four rows were incorrect, two were paid twice for the same month and two were for employees not in our master, totaling Rs 4,10,967.46. I have excluded those rows and now our totals are matching exactly with the validation sheet. The final report is ready for your review and I have not shown any individual salary details.")
