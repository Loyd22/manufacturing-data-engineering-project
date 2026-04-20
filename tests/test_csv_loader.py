"""
Tests for CSV loading utilities.

What we are testing:
- required column validation
- missing file handling

These tests help us catch simple pipeline problems early.
"""

from pathlib import Path

import pandas as pd
import pytest

from backend.utils.csv_loader import validate_columns, load_csv_to_table


def test_validate_columns_passes_when_all_columns_exist():
    """
    This test checks that validation passes
    when all required columns are present.
    """
    df = pd.DataFrame(
        {
            "supplier_id": ["SUP001"],
            "supplier_name": ["Supplier 1"],
            "status": ["active"],
        }
    )

    required_columns = ["supplier_id", "supplier_name", "status"]

    # This should not raise an error
    validate_columns(df, required_columns, "suppliers.csv")


def test_validate_columns_raises_error_when_column_is_missing():
    """
    This test checks that validation fails
    when one required column is missing.
    """
    df = pd.DataFrame(
        {
            "supplier_id": ["SUP001"],
            "supplier_name": ["Supplier 1"],
        }
    )

    required_columns = ["supplier_id", "supplier_name", "status"]

    with pytest.raises(ValueError, match="Missing columns"):
        validate_columns(df, required_columns, "suppliers.csv")


def test_load_csv_to_table_raises_file_not_found_for_missing_file():
    """
    This test checks that loading fails clearly
    when the CSV file does not exist.
    """
    fake_engine = None

    with pytest.raises(FileNotFoundError, match="CSV file not found"):
        load_csv_to_table(
            csv_path="data/raw/this_file_does_not_exist.csv",
            table_name="stg_suppliers",
            schema_name="staging",
            required_columns=["supplier_id", "supplier_name", "status"],
            engine=fake_engine,
        )