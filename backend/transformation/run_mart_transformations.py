"""
This script runs all mart transformation SQL files.

What it does:
- connects to PostgreSQL
- reads each mart SQL file
- executes them in order

Why this matters:
- marts become easy to refresh
- dashboard tables can be rebuilt anytime
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
    Run all mart SQL files in order.
    """
    print("Starting mart transformations...")

    engine = get_engine()

    sql_files = [
        "sql/marts/mart_daily_production_summary.sql",
        "sql/marts/mart_quality_trends.sql",
        "sql/marts/mart_machine_downtime.sql",
        "sql/marts/mart_supplier_performance.sql",
        "sql/marts/mart_inventory_health.sql",
        "sql/marts/mart_shipment_performance.sql",
    ]

    for sql_file in sql_files:
        run_sql_file(engine, sql_file)

    print("Mart transformations completed successfully.")


if __name__ == "__main__":
    main()