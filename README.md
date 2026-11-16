# PulseIQ - HR Analytics

## Setup Steps
1. Clone repo:
   git clone https://github.com/vaishnaviraut629-de/pulseiq.git
   cd pulseiq
2. Install libraries:
   pip install -r requirements.txt
3. Run monthly report for any month:
   python phase-4/build_report.py --month 2026-10
4. Run app:
   streamlit run app.py

## Libraries Pinned
duckdb==1.1.3
pandas==2.2.3
openpyxl==3.1.5
streamlit==1.38.0

## Report Pack
5 sheets: Cover (Date Range + Cut-off), Workforce, Attendance, Attrition, Payroll
Report generated with one command.

## Live Link
Will add in Task 17 after deployment