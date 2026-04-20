"""
Inventory and shipment dashboard page.
Shows inventory movement and shipment performance.
"""

import pandas as pd
import plotly.express as px
import streamlit as st

from services.data_loader import load_table

st.title("Inventory and Shipment Dashboard")

@st.cache_data
def get_data():
    inventory_df = load_table("marts.mart_inventory_health")
    shipment_df = load_table("marts.mart_shipment_performance")
    return inventory_df, shipment_df

inventory_df, shipment_df = get_data()

tab1, tab2 = st.tabs(["Inventory", "Shipments"])

with tab1:
    if inventory_df.empty:
        st.warning("No inventory data found.")
    else:
        inventory_df["movement_date"] = pd.to_datetime(inventory_df["movement_date"])

        st.subheader("Inventory Health Table")
        st.dataframe(inventory_df, use_container_width=True)

        summary = (
            inventory_df.groupby("movement_date", as_index=False)[["total_inbound", "total_outbound"]]
            .sum()
            .sort_values("movement_date")
        )

        fig = px.line(
            summary,
            x="movement_date",
            y=["total_inbound", "total_outbound"],
            markers=True,
        )
        st.plotly_chart(fig, use_container_width=True)

with tab2:
    if shipment_df.empty:
        st.warning("No shipment data found.")
    else:
        shipment_df["ship_date"] = pd.to_datetime(shipment_df["ship_date"])

        st.subheader("Shipment Performance Table")
        st.dataframe(shipment_df, use_container_width=True)

        trend = (
            shipment_df.groupby("ship_date", as_index=False)["on_time_rate"]
            .mean()
            .sort_values("ship_date")
        )

        fig = px.line(trend, x="ship_date", y="on_time_rate", markers=True)
        st.plotly_chart(fig, use_container_width=True)