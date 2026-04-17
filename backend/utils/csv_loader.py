"""
This file contains reusable functions for loading CSV files
into PostgreSQL staging tables.

Why we separate this:
- So one loading function can be reused for many CSV files
- Keeps the main ingestion script clean
"""

from pathlib import Path
import pandas as pd


def validate_columns(df: pd.DataFrame, required_columns: list[str], file_name: str) -> None:
    """
    Check whether the CSV contains all required columns.

    If any required column is missing, raise an error.
    """
    missing_columns = [col for col in required_columns if col not in df.columns]

    if missing_columns:
        raise ValueError(
            f"Missing columns in {file_name}: {missing_columns}"
        )


def load_csv_to_table(
    csv_path: str,
    table_name: str,
    schema_name: str,
    required_columns: list[str],
    engine,
) -> None:
    """
    Load one CSV file into one PostgreSQL table.

    Steps:
    1. Read the CSV
    2. Validate columns
    3. Clear old data in the target table
    4. Insert the new rows
    """
    file_path = Path(csv_path)

    if not file_path.exists():
        raise FileNotFoundError(f"CSV file not found: {csv_path}")

    print(f"\nReading file: {csv_path}")

    # Read the CSV into a pandas DataFrame
    df = pd.read_csv(file_path)

    # Validate the CSV structure before loading
    validate_columns(df, required_columns, file_path.name)

    print(f"Columns validated: {file_path.name}")
    print(f"Rows found: {len(df)}")

    # Clear the old staging data first
    with engine.begin() as connection:
        connection.exec_driver_sql(f"TRUNCATE TABLE {schema_name}.{table_name};")

    print(f"Cleared old data from {schema_name}.{table_name}")

    # Load new data into PostgreSQL
    df.to_sql(
        name=table_name,
        con=engine,
        schema=schema_name,
        if_exists="append",
        index=False,
        method="multi",
    )

    print(f"Loaded {len(df)} rows into {schema_name}.{table_name}")