# Data Contracts - PulseIQ (Day 1)

Checked the data_contracts sheet and listed main contracts for 3 fact tables.

### 1. fact_payroll
- employee_id - should be int and not empty
- salary_amount - must be greater than 0, if negative then reject
- pay_date - should be in proper date format
- one employee can have multiple payroll entries but id should not be null

### 2. fact_task
- task_id - int, unique value
- hours_logged - value should be between 0 to 24 only
- status - only 4 status allowed: Done, In Progress, Pending, Blocked
- if status is different then mark as error

### 3. fact_leave
- leave_id - not null
- leave_type - only Sick, Casual, Earned, LOP is allowed
- leave_days - should be more than 0
- leave reason can be empty but type should be correct
