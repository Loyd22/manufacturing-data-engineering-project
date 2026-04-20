"""
Production dashboard page.
Shows production metrics and production data table.
"""

import pandas as pd
import plotly.express as px
import streamlit as st

from services.data_loader import load_table

st.title("Production Dashboard")

@st.cache_data
def get_data():
    return load_table("marts.mart_daily_production_summary")

df = get_data()

if df.empty:
    st.warning("No production data found.")
else:
    df["production_date"] = pd.to_datetime(df["production_date"])

    st.subheader("Production Summary Table")
    st.dataframe(df, use_container_width=True)

    st.subheader("Daily Produced Quantity")
    fig1 = px.line(df, x="production_date", y="total_quantity_produced", markers=True)
    st.plotly_chart(fig1, use_container_width=True)

    st.subheader("Production Efficiency")
    fig2 = px.line(df, x="production_date", y="production_efficiency", markers=True)
    st.plotly_chart(fig2, use_container_width=True)