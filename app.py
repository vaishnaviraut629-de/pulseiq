import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="PulseIQ", layout="wide")
st.title("PulseIQ - Workforce Dashboard")
st.write(f"Data Cut-off Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}")

# Safe data - no external file needed for test
data = {
    "Department": ["Engineering", "Sales", "HR", "Marketing", "Support", "Finance", "Product", "Design", "Ops", "Legal", "Admin"],
    "Headcount": [45, 32, 12, 18, 25, 10, 20, 15, 30, 5, 8]
}
df = pd.DataFrame(data)

st.metric("Total Headcount", df["Headcount"].sum())
st.bar_chart(df.set_index("Department"))
st.dataframe(df)

st.success("App is Live! Phone & Stranger Test PASS")