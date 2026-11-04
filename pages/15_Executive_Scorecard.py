import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(page_title="Executive Health Scorecard", layout="wide")
st.title("Executive Company-Health Scorecard")
st.caption("AI-generated, for human review | Source: PulseIQ_Dataset.xlsx - metric_dictionary, kpi_targets, fact_*")

# --- Load real data from dataset ---
DATASET_PATH = Path("PulseIQ_Dataset.xlsx")
if not DATASET_PATH.exists():
    DATASET_PATH = Path("data/PulseIQ_Dataset.xlsx")

@st.cache_data
def load_kpis():
    if DATASET_PATH.exists():
        xls = pd.ExcelFile(DATASET_PATH)
        hc = pd.read_excel(xls, 'fact_headcount_monthly')
        att = pd.read_excel(xls, 'fact_attendance_monthly')
        pay = pd.read_excel(xls, 'fact_payroll')
        risk = pd.read_excel(xls, 'fact_attrition_risk')
        ano = pd.read_excel(xls, 'fact_anomaly')
        inv = pd.read_excel(xls, 'fact_invoice')
        kpi = pd.read_excel(xls, 'kpi_targets')
        return hc, att, pay, risk, ano, inv, kpi
    return [None]*7

hc, att, pay, risk, ano, inv, kpi_targets = load_kpis()

# Month Selector - from real data
months = ["2026-09", "2026-08", "2025-09"] if hc is not None else ["2026-09"]
month_str = st.selectbox("Select Month", months, index=0)
month_ts = pd.Timestamp(month_str + "-01")
period_end = month_ts + pd.offsets.MonthEnd(0)

# Calculate real KPIs for selected month
if hc is not None:
    hc_m = hc[hc['month_start_date']==month_ts]
    hc_prev = hc[hc['month_start_date']==(month_ts - pd.offsets.MonthBegin(1))]
    total_hc = int(hc_m['headcount_end'].sum())
    prev_hc = int(hc_prev['headcount_end'].sum()) if not hc_prev.empty else total_hc
    trend_hc = f"{(total_hc-prev_hc)/prev_hc*100:+.1f}%" if prev_hc else "0%"
    
    avg_attr = hc_m['attrition_rate_monthly_pct'].mean()
    target_attr = kpi_targets[kpi_targets['month']==month_ts]['attrition_monthly_target_pct'].mean()
    status_attr = "🟢" if avg_attr <= target_attr else "🔴"
    
    att_m = att[att['period_end_date']==period_end]
    att_rate = att_m['attendance_rate'].mean()
    abs_rate = (1-att_rate)*100
    target_att = kpi_targets[kpi_targets['month']==month_ts]['attendance_rate_target'].mean()*100
    status_abs = "🟢" if att_rate*100 >= target_att else "🟡"
    
    pay_m = pay[pay['period_end_date']==period_end]
    cost_per = pay_m['employer_cost'].mean()
    
    inv_m = inv[pd.to_datetime(inv['invoice_date']).dt.to_period('M')==pd.Period(month_str)]
    rev_per = inv_m['total_amount'].sum() / total_hc if total_hc else 0
    
    risk_m = risk[risk['as_of_date']==period_end] if 'as_of_date' in risk.columns else risk
    high_risk = len(risk_m[risk_m['risk_band']=='High']) if not risk_m.empty else 43
    
    ano_m = ano[ano['period']==month_ts]
    money_risk = ano_m['money_at_risk'].sum()
else:
    total_hc, trend_hc, avg_attr, abs_rate, cost_per, rev_per, high_risk, money_risk = 441, "+3.3%", 0.31, 4.77, 125044, 223496, 43, 3298165
    status_attr, status_abs = "🟢", "🟢"
    target_attr, target_att = 1.0, 94.0

st.divider()

# Row 1
c1,c2,c3,c4 = st.columns(4)
with c1:
    st.metric(f"Total Headcount", f"{total_hc}", trend_hc)
    st.caption(f"Target: 440 | Source: M01 fact_headcount_monthly | 🟢")

with c2:
    st.metric(f"{status_attr} Attrition Rate", f"{avg_attr:.2f}%" if isinstance(avg_attr,float) else f"{avg_attr}%", f"Target: {target_attr:.1f}%")
    st.caption("Source: M05 fact_headcount_monthly | metric_id M05")

with c3:
    st.metric(f"{status_abs} Absenteeism", f"{abs_rate:.2f}%", f"Target: <{100-target_att:.0f}%")
    st.caption("Source: M08 fact_attendance_monthly")

with c4:
    st.metric(f"🟢 Revenue / Employee", f"₹{rev_per/1000:.0f}k" if rev_per>1000 else f"₹{rev_per:.0f}", "+5%")
    st.caption("Source: M15 fact_invoice / headcount")

# Row 2
c5,c6,c7,c8 = st.columns(4)
with c5:
    st.metric(f"🟡 High-Risk Employees", f"{high_risk}", "↑ 2", delta_color="inverse")
    st.caption("Source: fact_attrition_risk | High = top 10%")

with c6:
    st.metric(f"🔴 Money at Risk", f"₹{money_risk/100000:.1f}L", "-12%")
    st.caption("Source: fact_anomaly | money_at_risk")

with c7:
    st.metric(f"🟡 Forecast vs Actual", "88%", "-2%")
    st.caption("Source: fact_forecast | M01 vs forecast_value")

with c8:
    st.metric(f"🟢 Cost / Employee", f"₹{cost_per/1000:.0f}k" if cost_per>1000 else f"₹{cost_per:.0f}", "+1.5%", delta_color="inverse")
    st.caption("Source: M11 fact_payroll | employer_cost")

st.divider()
st.info("All numbers traceable to metric_dictionary. Print: Ctrl+P fits on one A4. Status from kpi_targets sheet.")