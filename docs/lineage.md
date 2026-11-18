# Data Lineage - PulseIQ

## Metric: Headcount

**Definition:** Count of Active employees

### Lineage Flow

Source -> Transformation -> API -> Dashboard

| Stage | Detail |
| --- | --- |
| Source | pulseiq_aggregate table |
| Transformation | Filter: status = 'Active', Group by Department |
| API | GET /metrics/headcount (api/main.py) |
| Dashboard | Power BI / Dashboard - Headcount Card |

### Freshness
- **Last Refresh:** 2026-11-18
- **Source Table:** pulseiq_aggregate
- **API Field:** last_refresh

### Owner
- **Metric Owner:** HR Team
- **Maintained By:** Vaishnavi
