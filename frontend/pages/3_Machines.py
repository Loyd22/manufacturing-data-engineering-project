"""
Machines dashboard page.
Shows downtime and machine performance.
"""

import pandas as pd
import plotly.express as px
import streamlit as st

from services.data_loader import load_table

st.title("Machine Performance Dashboard")

@st.cache_data
def get_data():
    return load_table("marts.mart_machine_downtime")

df = get_data()

if df.empty:
    st.warning("No machine data found.")
else:
    df["log_date"] = pd.to_datetime(df["log_date"])

    st.subheader("Machine Downtime Table")
    st.dataframe(df, use_container_width=True)

    st.subheader("Downtime Percentage by Machine")
    machine_summary = (
        df.groupby("machine_id", as_index=False)["downtime_percentage"]
        .mean()
        .sort_values("downtime_percentage", ascending=False)
    )
    fig1 = px.bar(machine_summary, x="machine_id", y="downtime_percentage")
    st.plotly_chart(fig1, use_container_width=True)

    st.subheader("Downtime Trend Over Time")
    trend = (
        df.groupby("log_date", as_index=False)["downtime_percentage"]
        .mean()
        .sort_values("log_date")
    )
    fig2 = px.line(trend, x="log_date", y="downtime_percentage", markers=True)
    st.plotly_chart(fig2, use_container_width=True)