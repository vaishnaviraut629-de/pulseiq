# Task 17 - Release to Production
**Date: 16 Nov 2026**
**By: Vaishnavi Raut**

Live Link: https://pulseiq-o5qndhpk8k9qbdzwhmrk5o.streamlit.app/
GitHub Repo: https://github.com/vaishnaviraut629-de/pulseiq

### What I did
In this task I published my dashboard live. Before it was only on my laptop, now anyone with link can open it.

### Hosting Comparison - Why I chose Streamlit
I checked 3 platforms:

| Platform | Free Limit | Data Size | Sleep? | Price |
|---|---|---|---|---|
| Streamlit Cloud | 1GB RAM | 1GB | Yes, sleeps when idle | Free |
| Render | 512MB | 500MB | Yes, after 15 min | Free |
| Vercel | 100MB | 100MB | No sleep | Free |

I selected Streamlit Community Cloud because it is free and easy for python apps. It directly deploys from GitHub. Yes it sleeps but for my college project it is okay. If in future real users face issue due to sleep, then taking $20 paid plan is normal business decision. That is cheap.

Reference: I took reference from Streamlit official github - https://github.com/streamlit/streamlit

### Data - What I Published
Platform has 200MB file limit. My original warehouse was very big (>500MB) with employee names, email, salary.

So I exported only aggregates to parquet file.
File: pulseiq_aggregates.parquet
Size: 2.3 KB only
Content: Department Name and Headcount - 11 rows only

Think Yourself Answer:
Q: What do you publish and what do you leave out?
Ans: I published only aggregates because it is small, fast, and under limit. I left out raw data like Name, Email, Salary because it is private PII data and also big in size. In real company also they publish only summary, not raw private data.

### Secrets
I did not put any password or API key in my code. I put all settings in Streamlit Secrets Store. My .env file is in .gitignore so it will not go to GitHub. I checked repo, no secrets.

### Scheduled Refresh
Refresh time: Daily 9 AM IST
How: When I push to GitHub, Streamlit auto redeploys and data updates.
Data cut-off date is shown on dashboard top: 2026-11-16 10:10

### Testing
1. Phone Test: I opened link on my phone. It opened and graph was visible. Screenshot I have added in Evidence folder.
2. Stranger Test: I sent link to my friend. I asked him to find headcount without my help. He found it in 5 seconds. So PASS.

### Checklist (as per task)
- [x] Link opens on phone and for stranger - Done
- [x] Data cut-off date shown - Done - 2026-11-16 10:10
- [x] No secrets in repo - Done
- [x] Hosting choice and reason written - Done

### Evidence
1. Live Link: https://pulseiq-o5qndhpk8k9qbdzwhmrk5o.streamlit.app/
2. Screenshot: Attached in Evidence/phone_test.jpg
3. GitHub Link: https://github.com/vaishnaviraut629-de/pulseiq

Finally I can say: I released an analytics product to the internet.

### How real companies do it
I read note - free plans can sleep. If pause hurts users, small paid plan is normal. My decision: For now free is okay, later if users increase I will pay.