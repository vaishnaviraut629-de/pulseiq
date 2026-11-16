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
## Task 17: Release to Production - LIVE ✅
**Live Link:** https://pulseiq-o5qndhpk8k9qbdzwhmrk5o.streamlit.app/
**Status:** Anyone with link can open

### 1. Hosting Comparison Table
| Platform | Free RAM | Data Limit | Sleep Behaviour | Price |
|---|---|---|---|---|
| Streamlit Cloud | 1GB | 1GB | Sleeps after idle | Free |
| Render | 512MB | 500MB | Sleeps 15min | Free |
| Vercel | 100MB | 100MB | No sleep | Free |
**My Choice:** Streamlit Cloud. Reason: Free, Python sathi best, GitHub varun direct deploy. Sleep hoto pan MVP sathi ok. Real users aale tar $20 paid plan - normal business choice.

### 2. Think for Yourself (200MB Limit)
**Published:** `pulseiq_aggregates.parquet` (2.3KB) - Dept + Headcount only (11 rows)
**Left Out:** Raw employee data (Name, Email, Salary) - Privacy PII + Size limit cross hota.
Logic: Real company madhe Aggregates public, Raw data private DB madhe thevtat.

### 3. Secrets Management
No secrets in GitHub code. All settings in Streamlit Cloud Secrets Store. .env in .gitignore

### 4. Scheduled Refresh
Daily 9 AM IST - GitHub push -> Streamlit auto-redeploy

### 5. Testing as Stranger
Phone Test: PASS - Android var open hoto
Stranger Test: Friend la link pathavla - 5 sec madhe headcount shodhla without help - PASS

### Checklist
- [x] Link opens phone + stranger
- [x] Data cut-off shown: 2026-11-16 09:24
- [x] No secrets in repo
- [x] Hosting reason written