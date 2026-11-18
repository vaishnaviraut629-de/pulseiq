# Data Lineage - PulseIQ

## Overview
This file shows where each number comes from, from raw table to dashboard.

## Lineage Diagram

```mermaid
flowchart LR
    A[Raw Feed - employees.csv] --> B[ETL - api/main.py]
    B --> C[Warehouse Table - pulseiq_aggregate]
    C --> D[Metric Views]
    D --> E[Dashboard]