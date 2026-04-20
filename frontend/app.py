"""
Main Streamlit dashboard home page.

What this page does:
- shows the dashboard title
- loads core marts tables
- displays top KPI cards
- displays overview charts

This is the first page users will see.
"""

import pandas as pd
import plotly.express as px
import streamlit as st

from components.metrics import show_metric
from services.data_loader import load_table


# Set the browser tab title and dashboard layout
st.set_page_config(
    page_title="Manufacturing Operations Dashboard",
    page_icon="🏭",
    layout="wide",
)

st.title("🏭 Manufacturing Operations Dashboard")
st.caption("Streamlit dashboard powered by PostgreSQL marts tables")


@st.cache_data
def get_data():
    """
    Load overview tables once and cache them
    so the app becomes faster after the first load.
    """
    production_df = load_table("marts.mart_daily_production_summary")
    quality_df = load_table("marts.mart_quality_trends")
    machine_df = load_table("marts.mart_machine_downtime")
    supplier_df = load_table("marts.mart_supplier_performance")
    shipment_df = load_table("marts.mart_shipment_performance")

    return production_df, quality_df, machine_df, supplier_df, shipment_df


production_df, quality_df, machine_df, supplier_df, shipment_df = get_data()

# Convert date columns to proper datetime for cleaner charts
if not production_df.empty:
    production_df["production_date"] = pd.to_datetime(production_df["production_date"])

if not quality_df.empty:
    quality_df["inspection_date"] = pd.to_datetime(quality_df["inspection_date"])

if not shipment_df.empty:
    shipment_df["ship_date"] = pd.to_datetime(shipment_df["ship_date"])


# -----------------------------
# KPI Section
# -----------------------------
st.subheader("Executive Overview")

col1, col2, col3, col4 = st.columns(4)

total_produced_units = int(production_df["total_quantity_produced"].sum()) if not production_df.empty else 0
total_planned_units = int(production_df["total_quantity_planned"].sum()) if not production_df.empty else 0
avg_supplier_on_time = float(supplier_df["on_time_rate"].mean()) if not supplier_df.empty else 0
total_defects = int(quality_df["total_defects"].sum()) if not quality_df.empty else 0

with col1:
    show_metric("Total Produced Units", f"{total_produced_units:,}")

with col2:
    show_metric("Total Planned Units", f"{total_planned_units:,}")

with col3:
    show_metric("Avg Supplier On-Time Rate", f"{avg_supplier_on_time:.2%}")

with col4:
    show_metric("Total Defects", f"{total_defects:,}")


# -----------------------------
# Charts Section
# -----------------------------
chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.markdown("### Daily Produced Quantity")

    if not production_df.empty:
        fig = px.line(
            production_df,
            x="production_date",
            y="total_quantity_produced",
            markers=True,
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No production data available.")

with chart_col2:
    st.markdown("### Defect Rate Over Time")

    if not quality_df.empty:
        quality_summary = (
            quality_df.groupby("inspection_date", as_index=False)["defect_rate"]
            .mean()
            .sort_values("inspection_date")
        )

        fig = px.line(
            quality_summary,
            x="inspection_date",
            y="defect_rate",
            markers=True,
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No quality data available.")


bottom_col1, bottom_col2 = st.columns(2)

with bottom_col1:
    st.markdown("### Supplier On-Time Rate")

    if not supplier_df.empty:
        fig = px.bar(
            supplier_df.sort_values("on_time_rate", ascending=False),
            x="on_time_rate",
            y="supplier_name",
            orientation="h",
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No supplier data available.")

with bottom_col2:
    st.markdown("### Average Machine Downtime Percentage")

    if not machine_df.empty:
        machine_summary = (
            machine_df.groupby("machine_id", as_index=False)["downtime_percentage"]
            .mean()
            .sort_values("downtime_percentage", ascending=False)
        )

        fig = px.bar(
            machine_summary,
            x="machine_id",
            y="downtime_percentage",
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No machine data available.")


st.markdown("---")
st.write("Use the left sidebar to open the detailed dashboard pages.")