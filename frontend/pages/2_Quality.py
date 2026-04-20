"""
Quality dashboard page.
Shows defect trends and quality data table.
"""

import pandas as pd
import plotly.express as px
import streamlit as st

from services.data_loader import load_table

st.title("Quality Dashboard")

@st.cache_data
def get_data():
    return load_table("marts.mart_quality_trends")

df = get_data()

if df.empty:
    st.warning("No quality data found.")
else:
    df["inspection_date"] = pd.to_datetime(df["inspection_date"])

    st.subheader("Quality Trends Table")
    st.dataframe(df, use_container_width=True)

    st.subheader("Defect Rate Over Time")
    summary = (
        df.groupby("inspection_date", as_index=False)["defect_rate"]
        .mean()
        .sort_values("inspection_date")
    )
    fig1 = px.line(summary, x="inspection_date", y="defect_rate", markers=True)
    st.plotly_chart(fig1, use_container_width=True)

    st.subheader("Total Defects by Product")
    product_summary = (
        df.groupby("product_id", as_index=False)["total_defects"]
        .sum()
        .sort_values("total_defects", ascending=False)
    )
    fig2 = px.bar(product_summary, x="product_id", y="total_defects")
    st.plotly_chart(fig2, use_container_width=True)