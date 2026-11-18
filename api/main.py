from fastapi import FastAPI

app = FastAPI(title="PulseIQ Metrics API")

@app.get("/")
def home():
    return {"message": "PulseIQ API is running"}

@app.get("/metrics/headcount")
def headcount():
    return {
        "metric": "Headcount",
        "value": 81,
        "definition": "Total active employees",
        "source": "dim_employee",
        "last_refresh": "2026-11-18 09:00 IST",
        "freshness": "Refreshed daily at 9 AM"
    }

@app.get("/metrics/attrition-rate")
def attrition():
    return {
        "metric": "Attrition Rate",
        "value": 12.5,
        "unit": "%",
        "definition": "(Left in 12 months / Avg Headcount) * 100",
        "source": "fact_attrition",
        "last_refresh": "2026-11-18 09:00 IST",
        "freshness": "Refreshed daily at 9 AM"
    }

@app.get("/metrics/avg-tenure")
def tenure():
    return {
        "metric": "Avg Tenure",
        "value": 3.2,
        "unit": "years",
        "definition": "Average years since joining",
        "source": "dim_employee",
        "last_refresh": "2026-11-18 09:00 IST",
        "freshness": "Refreshed daily at 9 AM"
    }

@app.get("/metrics/avg-pay")
def pay():
    return {
        "metric": "Avg Pay",
        "value": 85000,
        "unit": "INR",
        "definition": "Average monthly salary",
        "source": "fact_pay",
        "last_refresh": "2026-11-18 09:00 IST",
        "freshness": "Refreshed monthly on 1st"
    }

@app.get("/metrics/offer-accept-rate")
def offer():
    return {
        "metric": "Offer Accept Rate",
        "value": 78,
        "unit": "%",
        "definition": "(Accepted / Made) * 100 in last 90 days",
        "source": "fact_offers",
        "last_refresh": "2026-11-18 09:00 IST",
        "freshness": "Refreshed daily at 9 AM"
    }