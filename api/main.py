from fastapi import FastAPI

app = FastAPI(title="PulseIQ Metrics API")

@app.get("/metrics/headcount")
def get_headcount():
    return {
        "metric": "headcount",
        "value": 81,
        "definition": "Count of Active employees",
        "source": "pulseiq_aggregate table",
        "last_refresh": "2026-11-18",
        "freshness": "Data last refreshed on 2026-11-18"
    }

@app.get("/metrics/attrition_rate")
def get_attrition():
    return {
        "metric": "attrition_rate",
        "value": 12.5,
        "definition": "Percentage of employees who left in last 12 months",
        "source": "pulseiq_aggregate table",
        "last_refresh": "2026-11-18",
        "freshness": "Data last refreshed on 2026-11-18"
    }

@app.get("/metrics/avg_tenure")
def get_tenure():
    return {
        "metric": "avg_tenure",
        "value": 3.2,
        "definition": "Average tenure of Active employees in years",
        "source": "pulseiq_aggregate table",
        "last_refresh": "2026-11-18",
        "freshness": "Data last refreshed on 2026-11-18"
    }

@app.get("/metrics/avg_salary")
def get_salary():
    return {
        "metric": "avg_salary",
        "value": 65000,
        "definition": "Average salary of Active employees",
        "source": "pulseiq_aggregate table",
        "last_refresh": "2026-11-18",
        "freshness": "Data last refreshed on 2026-11-18"
    }

@app.get("/metrics/new_hires")
def get_new_hires():
    return {
        "metric": "new_hires",
        "value": 8,
        "definition": "Number of employees joined in last 30 days",
        "source": "pulseiq_aggregate table",
        "last_refresh": "2026-11-18",
        "freshness": "Data last refreshed on 2026-11-18"
    }