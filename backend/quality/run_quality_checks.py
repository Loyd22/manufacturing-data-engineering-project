"""
This script runs all SQL data quality checks.

What it does:
- connects to PostgreSQL
- executes each SQL check file
- prints the result of each check
- shows whether any issues were found

Why this matters:
- it helps us verify that the data is trustworthy
- it makes the pipeline more production-style
"""

from pathlib import Path
import pandas as pd

from backend.utils.db import get_engine


def run_check_file(engine, sql_file_path: str) -> pd.DataFrame:
    """
    Run one SQL check file and return the results as a DataFrame.
    """
    path = Path(sql_file_path)

    if not path.exists():
        raise FileNotFoundError(f"SQL file not found: {sql_file_path}")

    print(f"\nRunning check file: {sql_file_path}")

    sql_text = path.read_text(encoding="utf-8")
    df = pd.read_sql(sql_text, engine)

    return df


def main() -> None:
    """
    Run all quality checks in sequence.
    """
    print("Starting data quality checks...")

    engine = get_engine()

    check_files = [
        "sql/checks/check_staging_production_orders.sql",
        "sql/checks/check_staging_quality.sql",
        "sql/checks/check_staging_inventory.sql",
        "sql/checks/check_staging_shipments.sql",
        "sql/checks/check_warehouse_fact_production.sql",
    ]

    total_issues = 0

    for check_file in check_files:
        df = run_check_file(engine, check_file)

        print(df.to_string(index=False))

        file_issues = int(df["issue_count"].sum())
        total_issues += file_issues

        if file_issues == 0:
            print("Result: PASS")
        else:
            print(f"Result: FOUND {file_issues} issue(s)")

    print("\nQuality check summary")
    print(f"Total issues found: {total_issues}")

    if total_issues == 0:
        print("All quality checks passed.")
    else:
        print("Some quality checks failed. Review the counts above.")


if __name__ == "__main__":
    main()