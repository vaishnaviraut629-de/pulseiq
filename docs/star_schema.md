# Task 2 - Star Schema Warehouse

## ER Diagram
```mermaid
erDiagram
    dim_employee ||--o{ fact_payroll : employee_key
    dim_date ||--o{ fact_payroll : date_key
    dim_department ||--o{ fact_payroll : dept
    dim_employee ||--o{ fact_task : employee_key
    dim_sprint ||--o{ fact_task : sprint

    dim_employee {
        int employee_key PK
        string employee_id
        string dept
    }
    fact_payroll {
        string payroll_item_id PK
        int employee_key FK
        float employer_cost
    }
    fact_task {
        string task_id PK
        int employee_key FK
        int story_points
    }
```

## Keys
- PK: dim_employee.employee_key (Surrogate Key - SCD Type 2)
- FK: fact_payroll.employee_key = -1 for Unknown

## Reconcile Proof (Task1 = Task2)
- fact_payroll 7344 rows == source
- fact_task 28868 rows == source
- fact_leave 3441 rows == source

## Orphan Check
- 2 rows EMP-9001/9002 are planted fake IDs in source Excel
- Mapped to employee_key = -1 Unknown
- Explained and reported to business

## History Rule
JOIN by employee_key not employee_id. So June pay stays in Sales even if person moves to Support in July.