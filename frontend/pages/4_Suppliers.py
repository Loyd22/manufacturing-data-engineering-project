"""
Supplier dashboard page.
Shows supplier shipment performance.
"""

import plotly.express as px
import streamlit as st

from services.data_loader import load_table

st.title("Supplier Performance Dashboard")

@st.cache_data
def get_data():
    return load_table("marts.mart_supplier_performance")

df = get_data()

if df.empty:
    st.warning("No supplier data found.")
else:
    st.subheader("Supplier Performance Table")
    st.dataframe(df, use_container_width=True)

    st.subheader("Supplier On-Time Rate")
    fig1 = px.bar(
        df.sort_values("on_time_rate", ascending=False),
        x="supplier_name",
        y="on_time_rate",
    )
    st.plotly_chart(fig1, use_container_width=True)

    st.subheader("Average Delay Days by Supplier")
    fig2 = px.bar(
        df.sort_values("average_delay_days", ascending=False),
        x="supplier_name",
        y="average_delay_days",
    )
    st.plotly_chart(fig2, use_container_width=True)