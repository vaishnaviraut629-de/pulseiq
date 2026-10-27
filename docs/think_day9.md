How would you tell a finance head that 4 rows in the data were wrong? Write 3 calm sentences.
### Think Day 9: Payroll data had 4 bad rows. How to tell Finance Head?

Here's how I think about it:

Raw payroll looks great on paper - say 7344 rows total. But if 4 of those are wrong, that's Rs 4,10,967.46 extra cost coming in. So your actual clean total is only for 7340 rows. And those 4 wrong rows are worse than normal errors. They create double counting, trust issues, and you end up matching the wrong total twice.

The 4 rows were PI-X0001, PI-X0002 as duplicates and PI-X0003, PI-X0004 as orphans. PI-X0001 and PI-X0002 were same employee paid twice for same run_id. That's classic double-counting. PI-X0003 and PI-X0004 were for EMP-9001 and EMP-9002 which are not even in dim_employee. So they are invalid.

Clean data is 7340 rows with correct totals. So it actually matches exactly with validation answer key. No noise, no mismatch. Finance is happier, audit is less stressed, and what you ship stays correct.

For me, health is not just speed. It's sustainable accuracy + trust.

A payroll with wrong rows usually has underlying issues:
- No proper unique constraint on employee + run_id
- Too much rushing to close month end
- No foreign key check with employee master
- Maybe validation is skipped to hit deadline

So raw data is fast but fragile. Clean data is slower but stable.

My decision: I'd pick clean 7340 rows as final any day.

If I had to fix payroll, I'd tell them to add unique key, add foreign key, limit manual edits, and track reconciliation as a first-class metric, not just total cost.

Final communication to Finance Head:
During reconciliation I noticed four rows were incorrect, two were paid twice for the same month and two were for employees not in our master, totaling Rs 4,10,967.46. I have excluded those rows and now our totals are matching exactly with the validation sheet. The final report is ready for your review and I have not shown any individual salary details.