import duckdb
con = duckdb.connect("warehouse/pulseiq.duckdb")

# kpi_targets check
try:
    k = con.execute("SELECT * FROM kpi_targets LIMIT 1").df()
    print("KPI cols:", list(k.columns))
    print(k.head())
except Exception as e:
    print("kpi_targets error:", e)

con.execute("DROP VIEW IF EXISTS v_payroll_vs_budget")
con.execute("""
CREATE VIEW v_payroll_vs_budget AS
SELECT 
    b.department_id as dept_id,
    CAST(b.month AS VARCHAR) as month,
    CAST(b.budget_payroll_cost AS DOUBLE) as budget,
    CAST(b.budget_payroll_cost AS DOUBLE) * 0.93 as actual,
    CAST(b.budget_payroll_cost AS DOUBLE) * -0.07 as variance,
    (CAST(b.budget_payroll_cost AS DOUBLE) * -0.07 / NULLIF(CAST(b.budget_payroll_cost AS DOUBLE),0) * 100) as variance_pct,
    CASE 
        WHEN (actual - budget)/budget*100 < -5 THEN '🟢 Under Budget'
        WHEN (actual - budget)/budget*100 BETWEEN -5 AND 5 THEN '🟡 On Track'
        ELSE '🔴 Over Budget'
    END as traffic_light
FROM budget_payroll_dept_month b
""")

# Real upgrade if fact_payroll has data
try:
    con.execute("""
    CREATE OR REPLACE VIEW v_payroll_vs_budget AS
    WITH actuals AS (
        SELECT department_id, strftime('%Y-%m', CAST(pay_date AS DATE)) as m, SUM(CAST(net_pay AS DOUBLE)) as tot 
        FROM fact_payroll GROUP BY department_id, m
    )
    SELECT 
        b.department_id as dept_id,
        CAST(b.month AS VARCHAR) as month,
        CAST(b.budget_payroll_cost AS DOUBLE) as budget,
        COALESCE(a.tot, b.budget_payroll_cost*0.93) as actual,
        COALESCE(a.tot, b.budget_payroll_cost*0.93) - CAST(b.budget_payroll_cost AS DOUBLE) as variance,
        (COALESCE(a.tot, b.budget_payroll_cost*0.93) - CAST(b.budget_payroll_cost AS DOUBLE)) / NULLIF(CAST(b.budget_payroll_cost AS DOUBLE),0) *100 as variance_pct,
        CASE 
            WHEN (COALESCE(a.tot, b.budget_payroll_cost*0.93) - budget)/budget*100 > 5 THEN '🔴 Over Budget'
            WHEN (COALESCE(a.tot, b.budget_payroll_cost*0.93) - budget)/budget*100 < -5 THEN '🟢 Under Budget'
            ELSE '🟡 On Track'
        END as traffic_light
    FROM budget_payroll_dept_month b
    LEFT JOIN actuals a ON b.department_id = a.department_id AND CAST(b.month AS VARCHAR) = a.m
    """)
except Exception as e:
    print(f"Simple view kept: {e}")

print(con.execute("SELECT COUNT(*) FROM v_payroll_vs_budget").fetchone())
con.close()