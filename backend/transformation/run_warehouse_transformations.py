"""
This script runs all warehouse transformation SQL files.

What it does:
- connects to PostgreSQL
- opens each SQL file
- executes it in the correct order

Why this is useful:
- we do not have to run many SQL files manually
- the transformation step becomes repeatable
"""

from pathlib import Path

from backend.utils.db import get_engine


def run_sql_file(engine, sql_file_path: str) -> None:
    """
    Read one SQL file and execute it.
    """
    path = Path(sql_file_path)

    if not path.exists():
        raise FileNotFoundError(f"SQL file not found: {sql_file_path}")

    print(f"Running: {sql_file_path}")

    sql_text = path.read_text(encoding="utf-8")

    with engine.begin() as connection:
        connection.exec_driver_sql(sql_text)

    print(f"Finished: {sql_file_path}")


def main() -> None:
    """
    Run warehouse SQL transformations in the correct order.
    """
    print("Starting warehouse transformations...")

    engine = get_engine()

    sql_files = [
        "sql/warehouse/dim_supplier.sql",
        "sql/warehouse/dim_machine.sql",
        "sql/warehouse/dim_product.sql",
        "sql/warehouse/dim_date.sql",
        "sql/warehouse/fact_production.sql",
        "sql/warehouse/fact_quality.sql",
        "sql/warehouse/fact_inventory.sql",
        "sql/warehouse/fact_shipments.sql",
        "sql/warehouse/fact_machine_logs.sql",
    ]

    for sql_file in sql_files:
        run_sql_file(engine, sql_file)

    print("Warehouse transformations completed successfully.")


if __name__ == "__main__":
    main()