# Task 18 - Self-Service Report

## 1. Live Link
Live Link: https://pulseiq-o5gndhpk8k9qbd2wmrk5o.streamlit.app/
GitHub Repo: https://github.com/vaishnaviraut629-de/pulseiq
Date: 19 Nov 2026

## 2. What User Can Do Without Help?
1. Department Filter badlu shakto - Chart aapoaap badalto
2. Page badlu shakto - Workforce, Attendance, Attrition, Payroll, Budget, PnL, AI Signals
3. KPI baghu shakto - Headcount = 81, Attrition = 12.5%
4. Safe Download karu shakto - Fakt Aggregate data

## 3. Filters Tested
| Filter | Result |
| :--- | :--- |
| Department = All | 81 employees disle |
| Department = Changed | Chart lagech badalla |
| Page = Attrition | Chart ughadla, No Error |

## 4. Safe Download
- Fakt `pulseiq_aggregate` table download hoto
- Name, Phone, Salary konacha hi disat nahi
- Raw Feed dashboard madhe nahi

## 5. Think For Yourself 

Q: A manager has a team of 3. Should they see attrition for their team? Decide and explain.

Ans: My decision is NO, we should not show attrition for a team of 3.

I thought about it like this. If the team has only 3 people and 1 person leaves, the dashboard will show attrition as 33.3%. That number looks very big and scary, but actually it is just 1 person. So the percentage is misleading. Manager will panic for no reason.

Second problem is privacy. In a team of 3, everyone knows who left. If we show attrition, cost, or reason, the manager will easily know who it was. That is not fair to that employee. We should not expose a single person like that.

So what I will do is, I will hide the attrition number when team size is less than 5. Instead of showing 33%, I will show "Data Hidden - Team Too Small" or I will show only company level attrition which is 12.5%. That way manager still gets an idea, but no single person is exposed.

In short, for small teams, showing exact attrition is wrong because it is both wrong in maths and wrong for privacy. So I will suppress it.