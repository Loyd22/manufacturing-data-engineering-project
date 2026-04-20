"""
Run all warehouse transformation SQL files.
"""

from pathlib import Path

from backend.utils.db import get_engine
from backend.utils.logger import get_logger

logger = get_logger(__name__)


def run_sql_file(engine, sql_file_path: str) -> None:
    """
    Read one SQL file and execute it.
    """
    path = Path(sql_file_path)

    if not path.exists():
        raise FileNotFoundError(f"SQL file not found: {sql_file_path}")

    logger.info("Running SQL file: %s", sql_file_path)

    sql_text = path.read_text(encoding="utf-8")

    with engine.begin() as connection:
        connection.exec_driver_sql(sql_text)

    logger.info("Finished SQL file: %s", sql_file_path)


def main() -> None:
    """
    Run warehouse SQL files in the correct order.
    """
    logger.info("Starting warehouse transformations")

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

    try:
        for sql_file in sql_files:
            run_sql_file(engine, sql_file)
        logger.info("Warehouse transformations completed successfully")
    except Exception as error:
        logger.exception("Warehouse transformations failed: %s", error)
        raise


if __name__ == "__main__":
    main()