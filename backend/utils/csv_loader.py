"""
Reusable CSV loading functions for PostgreSQL staging tables.
"""

from pathlib import Path
import pandas as pd

from backend.utils.logger import get_logger

logger = get_logger(__name__)


def validate_columns(df: pd.DataFrame, required_columns: list[str], file_name: str) -> None:
    """
    Check whether the CSV contains all required columns.
    """
    missing_columns = [col for col in required_columns if col not in df.columns]

    if missing_columns:
        raise ValueError(f"Missing columns in {file_name}: {missing_columns}")


def load_csv_to_table(
    csv_path: str,
    table_name: str,
    schema_name: str,
    required_columns: list[str],
    engine,
) -> None:
    """
    Load one CSV file into one PostgreSQL table.
    """
    file_path = Path(csv_path)

    if not file_path.exists():
        raise FileNotFoundError(f"CSV file not found: {csv_path}")

    logger.info("Reading file: %s", csv_path)

    df = pd.read_csv(file_path)

    validate_columns(df, required_columns, file_path.name)
    logger.info("Columns validated for %s", file_path.name)
    logger.info("Rows found in %s: %s", file_path.name, len(df))

    with engine.begin() as connection:
        connection.exec_driver_sql(f"TRUNCATE TABLE {schema_name}.{table_name};")

    logger.info("Cleared old data from %s.%s", schema_name, table_name)

    df.to_sql(
        name=table_name,
        con=engine,
        schema=schema_name,
        if_exists="append",
        index=False,
        method="multi",
    )

    logger.info("Loaded %s rows into %s.%s", len(df), schema_name, table_name)