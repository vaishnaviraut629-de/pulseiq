# Task 16 - Automated Report Builder and Release Candidate

**Objective:** Generate a monthly report pack with one command and package the app.

**Repo:** https://github.com/vaishnaviraut629-de/pulseiq
**Tag:** v1.0.0-rc1

## 1. One Command Report Pack
**Command for any month:**
`python phase-4/build_report.py --month YYYY-MM`

**Example:**
`python phase-4/build_report.py --month 2026-10`

**Output:** `reports/monthly_report_2026-10.xlsx` with 5 key tables/charts

## 2. 5 Key Sheets in Pack
1.  **Cover:** Shows Date Range (2026-10-01 to 2026-10-31) and Data Cut-off (2026-11-05 09:00 IST) - Stamp on top
2.  **Workforce:** Headcount by department table + bar chart
3.  **Attendance:** Monthly attendance % table + line chart
4.  **Attrition:** Leavers by department + trend chart
5.  **Payroll:** Total cost + department-wise cost chart

## 3. Clean-Machine Testing
Tested on clean folder (other laptop):
- `git clone https://github.com/vaishnaviraut629-de/pulseiq.git` - Success
- `python -m venv venv` + `pip install -r requirements.txt` - All pinned versions installed
- `python phase-4/build_report.py --month 2026-10` - Report generated in 3 sec
- `streamlit run app.py` - App runs
- **Notes:** No manual path needed, works anywhere.

## 4. Scheduling
File: `.github/workflows/monthly.yml`
Runs automatically on 1st of every month at 9 AM (`cron: '0 9 1 * *'`) + manual run allowed.

## 5. Packaging
- `requirements.txt` - All libs pinned with version (streamlit==1.35.0 etc)
- `README.md` - Has setup steps so anyone can run
- `v1.0.0-rc1` tag pushed to origin - Evidence in screenshot

## 6. Think for yourself: What would break if next month had a new department?

**Initial Problem:** My first code had hardcoded list: `departments = ['HR','Finance','IT','Operations']`. If 'Marketing' comes next month, it would be missing from report and totals would be wrong. Charts would be incomplete.

**Testing Failure:** I inserted dummy record `('Test','Marketing')` and ran report for 2026-11. Marketing data did not appear. Report was incomplete - proved the bug.

**Fix Applied:** Changed to dynamic query: `SELECT DISTINCT department FROM workforce WHERE department IS NOT NULL`. Now code fetches whatever is in DB. Added auto-color logic for charts.

**Final Test After Fix:** Ran again with Marketing dummy data. Marketing automatically appeared in all sheets, charts updated to 5 bars, totals corrected. No code change needed. Report is now future-proof for any new department, location, or role.

## 7. Reference Links
- python-pptx: https://github.com/scanny/python-pptx
- WeasyPrint: https://github.com/Kozea/WeasyPrint
- GitHub Actions starter workflows: https://github.com/actions/starter-workflows

## 8. Evidence
- Sample Report: `reports/monthly_report_2026-10.xlsx`
- Tag Proof: `git tag` shows v1.0.0-rc1, pushed
- Screenshot attached of report generation