
"""
This file contains small reusable UI helpers for KPI cards.

Why we separate it:
- Keeps the main dashboard pages cleaner
- Makes KPI display reusable
"""

import streamlit as st


def show_metric(label: str, value, help_text: str | None = None) -> None:
    """
    Display one KPI metric card.
    """
    st.metric(label=label, value=value, help=help_text)