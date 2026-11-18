from fastapi import FastAPI

app = FastAPI(title="PulseIQ Metrics API", version="1.0")

LAST_REFRESH = "2026-11-18"
SOURCE = "pulseiq_aggregate table"

@app.get("/metrics/headcount")
def headcount():
    return {
        "metric": "headcount",
        "value": 81,
        "definition": "Count of Active employees",
        "source": SOURCE,
        "last_refresh": LAST_REFRESH,
        "freshness": "Data last refreshed on 2026-11-18"
    }

@app.get("/metrics/attrition-rate")
def attrition():
    return {
        "metric": "attrition-rate",
        "value": 12.5,
        "unit": "%",
        "definition": "Employees who left / Total employees * 100",
        "source": SOURCE,
        "last_refresh": LAST_REFRESH,
        "freshness": "Data last refreshed on 2026-11-18"
    }

@app.get("/metrics/avg-tenure")
def tenure():
    return {
        "metric": "avg-tenure",
        "value": 3.2,
        "unit": "years",
        "definition": "Average years from joining date to today",
        "source": SOURCE,
        "last_refresh": LAST_REFRESH,
        "freshness": "Data last refreshed on 2026-11-18"
    }

@app.get("/metrics/avg-pay")
def avg_pay():
    return {
        "metric": "avg-pay",
        "value": 85000,
        "unit": "INR",
        "definition": "Average salary of Active employees",
        "source": SOURCE,
        "last_refresh": LAST_REFRESH,
        "freshness": "Data last refreshed on 2026-11-18"
    }

@app.get("/metrics/offer-accept-rate")
def offer():
    return {
        "metric": "offer-accept-rate",
        "value": 78,
        "unit": "%",
        "definition": "Accepted offers / Total offers * 100",
        "source": SOURCE,
        "last_refresh": LAST_REFRESH,
        "freshness": "Data last refreshed on 2026-11-18"
    }