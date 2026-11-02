# Task 12: Invoices, Receivables and Cash Flow

**Open Statuses:** SENT, OVERDUE, PARTIALLY_PAID
These are the only statuses considered as open receivables. Mentioned on the page.

**Total Open Receivables:** ₹ 139,394,278
**Bucket Total:** ₹ 139,394,278
**Validation:** Match = True -> PASS

### Checklist
- [x] Buckets add up to total open receivables
- [x] Open statuses are written on the page
- [x] Slow-paying clients are named
- [x] Cash chart works

### What I Did
1. Created ageing buckets (0-30, 31-60, 61-90, 90+ days) using CASE in SQL
2. Calculated average days to pay per client to find slow payers
3. Listed clients with highest overdue amount for priority collection
4. Made cash in vs cash out chart month-wise from payment and expense tables

### Think for Yourself

### Think for Yourself

When I checked the data, I saw one big client is paying on time but always taking 75 days. 

For me this is a risk. Because even if our sales is good, cash will come very late. Then we have to manage our own payments from pocket, which is not good for business.

If I get chance to talk to finance team, I will ask them simple things - can we request this client to pay early, maybe we can give small discount? And also we should check if we are giving too much credit to only one client. Better to have many small clients than one big late paying client.

So collection needs to be more strict.
### Evidence
Task12_1.png - Total and Ageing Buckets
Task12_2.png - Cash flow and client tables