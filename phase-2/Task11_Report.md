# Task 11: Profit & Loss - Evidence

## Checklist
- [x] Totals tie to README headline - Revenue 80601695 / Expense 65615716 / Profit 14985979 / Margin 18.59%
- [x] Group accounts not double counted - WHERE LOWER(is_group)='n' used in v_pnl
- [x] Vendor and category charts correct - v_expense_by_category & v_top_vendor verified
- [x] 3 findings written

## Tie-out Table
| Metric | My P&L View | README Headline | Status |
| Revenue | 80601695 | 80601695 | ✅ Tied |
| Expense | 65615716 | 65615716 | ✅ Tied |
| Profit | 14985979 | 14985979 | ✅ Tied |

Logic: fact_ledger + dim_account joined, is_group='n' to avoid double counting.

## Screenshots
- docs/Evidence/Task11_1_ter...png - Terminal v_pnl proof
- docs/Evidence/Task11_2_pnl...png - Top KPI with month selector
- docs/Evidence/Task11_3_pnl...png - Expense by Category & Top Vendors

## 3 Findings
1. Overall margin 18.59% healthy but monthly fluctuation - expense spikes in some months.
2. Salaries/Subcontractor = 70%+ of total expense - main cost driver.
3. Top 3 vendors = 60%+ vendor spend - concentration risk, need diversification.

## Think for Yourself: Revenue grew but margin fell - 3 causes
1. Low-margin projects - Proof: project-wise margin from fact_ledger + dim_project (revenue-expense)/revenue
2. Vendor rate inflation - Proof: AVG amount per vendor per month from fact_expense trend
3. Bench cost / Unbilled - Proof: fact_attendance hours paid vs fact_ledger hours billed

Statement: I built a profit and loss view that ties to the books.
