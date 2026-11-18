# Task 19: Metrics API

## Objective
Let anyone get the same 5 HR metrics from one place, in JSON format, so there is no confusion from different excels.

## What I Built
- **API File:** `api/main.py`
- **Framework:** FastAPI + Uvicorn
- **Format:** JSON
- **Live Link:** `http://127.0.0.1:8000/docs`
- **Total Endpoints:** 5

## Metrics Tested

| Endpoint | Value I Got | Source |
| --- | --- | --- |
| GET /metrics/headcount | 81 | `pulseiq_aggregate...` |
| GET /metrics/attrition-rate | 12.5 % | `pulseiq_aggregate...` |
| GET /metrics/avg-tenure | 3.2 years | `pulseiq_aggregate...` |
| GET /metrics/avg-pay | 85000 INR | `pulseiq_aggregate...` |
| GET /metrics/offer-accept-rate | 78 % | `pulseiq_aggregate...` |

**Dimensions:** None - API gives company level total only

## How To Run
```python
pip install fastapi uvicorn
uvicorn api.main:app --reload
```markdown
## What I Learned
API is like a waiter in a hotel. We ask for headcount, it brings headcount. We ask for avg-pay, it brings avg-pay.

Before this task, everyone could say different headcount number from different excel. Now API gives only one number - 81. So no fight about which number is correct.

I think this API will be useful for dashboard in next tasks. Dashboard will just call this API and show same numbers.

## Think For Yourself

### Q1. If someone changes a column name in raw feed, which metrics will break?
**Answer:**
It depends on which column is changed. All metrics will not break together, only that metric will break which uses that column.

I checked my lineage - which metric uses which column:

| If this column changes | These metrics will break | Why? |
| --- | --- | --- |
| employee_id | All 5 will break | Because I use employee_id to count people in all metrics |
| status / employment_status | headcount, attrition-rate | Because headcount counts only Active people, and attrition needs who left |
| joining_date / hire_date | avg-tenure | Because tenure is calculated from joining date to today |
| salary / monthly_pay | avg-pay | Because avg-pay is average of salary column only |
| offer_status | offer-accept-rate | Because it counts how many offers were Accepted vs total offers |

My thinking - Suppose someone changes `salary` to `pay`, then only avg-pay will break. Headcount will still work because headcount does not use salary. This is good because we will know exactly where problem is.

But if someone changes `employee_id`, then full API