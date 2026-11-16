import streamlit as st
import pandas as pd
import os
from datetime import datetime

st.set_page_config(page_title="PulseIQ Live", layout="wide")
st.title("PulseIQ - Live Headcount Dashboard")

try:
    df = pd.read_parquet('data/pulseiq_aggregates.parquet')
    mtime = os.path.getmtime('data/pulseiq_aggregates.parquet')
    cutoff = datetime.fromtimestamp(mtime).strftime('%Y-%m-%d %H:%M')
    st.success(f"Data Cut-off Date: {cutoff} | Showing {len(df)} Departments")
    st.bar_chart(df.set_index('department_id'))
    st.dataframe(df)
except Exception as e:
    st.error(f"Error: {e}")

st.markdown("---")
st.caption("Hosting: Streamlit Cloud | Data: Aggregates only (2.3KB) | Raw DB not published due to 200MB limit")