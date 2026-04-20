"""
Run all SQL data quality checks.
"""

from pathlib import Path
import pandas as pd

from backend.utils.db import get_engine
from backend.utils.logger import get_logger

logger = get_logger(__name__)


def run_check_file(engine, sql_file_path: str) -> pd.DataFrame:
    """
    Run one SQL check file and return the results.
    """
    path = Path(sql_file_path)

    if not path.exists():
        raise FileNotFoundError(f"SQL file not found: {sql_file_path}")

    logger.info("Running check file: %s", sql_file_path)

    sql_text = path.read_text(encoding="utf-8")
    df = pd.read_sql(sql_text, engine)

    return df


def main() -> None:
    """
    Run all quality checks in sequence.
    """
    logger.info("Starting data quality checks")

    engine = get_engine()

    check_files = [
        "sql/checks/check_staging_production_orders.sql",
        "sql/checks/check_staging_quality.sql",
        "sql/checks/check_staging_inventory.sql",
        "sql/checks/check_staging_shipments.sql",
        "sql/checks/check_warehouse_fact_production.sql",
    ]

    total_issues = 0

    try:
        for check_file in check_files:
            df = run_check_file(engine, check_file)

            print(df.to_string(index=False))

            file_issues = int(df["issue_count"].sum())
            total_issues += file_issues

            if file_issues == 0:
                logger.info("PASS: %s", check_file)
            else:
                logger.warning("FOUND %s issue(s) in %s", file_issues, check_file)

        logger.info("Quality check summary | Total issues found: %s", total_issues)

        if total_issues == 0:
            logger.info("All quality checks passed")
        else:
            logger.warning("Some quality checks failed")
    except Exception as error:
        logger.exception("Quality checks failed: %s", error)
        raise


if __name__ == "__main__":
    main()