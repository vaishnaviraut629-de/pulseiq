June pay will stay in Sales cost.

Rule: JOIN by employee_key, not by employee_id.
Sales row has key=1 valid Jan-June.
Support row has key=2 valid July onwards.
June fact has key=1, so it counts in Sales. SCD Type 2 keeps history correct.

Orphan handling: 2 rows EMP-9001/9002 are fake IDs planted in source, mapped to employee_key = -1 Unknown and reported.