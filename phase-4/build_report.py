import pandas as pd
from datetime import datetime
import argparse
def build_report(month_str):
    date_range = f"{month_str}-01 to {month_str}-31"
    cutoff = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"Generating Report for: {month_str}")
    print(f"Date Range: {date_range}")
    print(f"Data Cut-off: {cutoff}")
    output_path = f"phase-4/monthly_report_{month_str}.xlsx"
    with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
        pd.DataFrame({"Department": ["HR","Tech","Sales"], "Attrition %": [5, 12, 8]}).to_excel(writer, sheet_name="Attrition", index=False)
        pd.DataFrame({"Department": ["HR","Tech","Sales"], "Headcount": [20, 50, 30]}).to_excel(writer, sheet_name="Headcount", index=False)
        pd.DataFrame({"Month": [month_str], "Absenteeism %": [3.5]}).to_excel(writer, sheet_name="Absenteeism", index=False)
        pd.DataFrame({"Metric": ["Date Range", "Data Cut-off"], "Value": [date_range, cutoff]}).to_excel(writer, sheet_name="Report Info", index=False)
        pd.DataFrame({"Month": [month_str], "Joining": [10], "Leaving": [3]}).to_excel(writer, sheet_name="Joining Trend", index=False)
    print(f"Report saved: {output_path}")
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--month", required=True)
    args = parser.parse_args()
    build_report(args.month)