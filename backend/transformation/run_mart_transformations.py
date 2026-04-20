"""
Run all mart transformation SQL files.
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
    Run mart SQL files in order.
    """
    logger.info("Starting mart transformations")

    engine = get_engine()

    sql_files = [
        "sql/marts/mart_daily_production_summary.sql",
        "sql/marts/mart_quality_trends.sql",
        "sql/marts/mart_machine_downtime.sql",
        "sql/marts/mart_supplier_performance.sql",
        "sql/marts/mart_inventory_health.sql",
        "sql/marts/mart_shipment_performance.sql",
    ]

    try:
        for sql_file in sql_files:
            run_sql_file(engine, sql_file)
        logger.info("Mart transformations completed successfully")
    except Exception as error:
        logger.exception("Mart transformations failed: %s", error)
        raise


if __name__ == "__main__":
    main()