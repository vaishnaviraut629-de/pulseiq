# Think 10: Hiring Freeze Fairness

**Q: Budget was never updated after hiring freeze, how to compare fairly?**

So normally we do Budget vs Actual. But if hiring freeze happened, actual payroll goes down because no new hiring. Budget is still old high value. So it will show we saved money, but actually it's fake saving.

What I think is fair:
- We should make adjusted budget. Like Budget * 0.85
- Why 0.85? Because almost 15% positions were frozen, so budget should also reduce 15%
- Then we can calculate 2 variances:
    1. Normal Variance = Actual - Original Budget
    2. Adjusted Variance = Actual - (Budget*0.85) -> this is fair

Also for KPI, task completion target was 80% before, but with less people it should be 68% (80*0.85). Attendance 94% target we can keep same.

In my dashboard I added both columns, so manager can see fair picture.

Formula I used: Adjusted Budget = Budget * 0.85