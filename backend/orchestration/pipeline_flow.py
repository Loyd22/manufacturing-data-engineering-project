"""
This file defines the main orchestration flow for the manufacturing data pipeline.

What this does:
- runs the staging ingestion step
- runs the warehouse transformation step
- runs the data quality checks
- runs the marts transformation step

Why this is useful:
- we no longer need to run every script manually
- the pipeline becomes easier to repeat
- this is closer to how real data pipelines are managed
"""

from prefect import flow, task

from backend.ingestion.load_all_staging import main as run_staging_ingestion
from backend.transformation.run_warehouse_transformations import main as run_warehouse_transformations
from backend.quality.run_quality_checks import main as run_quality_checks
from backend.transformation.run_mart_transformations import main as run_mart_transformations


@task(name="Load staging data")
def staging_task() -> None:
    """
    Run the CSV-to-staging ingestion step.
    """
    print("Starting staging ingestion...")
    run_staging_ingestion()
    print("Finished staging ingestion.")


@task(name="Build warehouse tables")
def warehouse_task() -> None:
    """
    Run the warehouse transformation step.
    """
    print("Starting warehouse transformations...")
    run_warehouse_transformations()
    print("Finished warehouse transformations.")


@task(name="Run data quality checks")
def quality_task() -> None:
    """
    Run the data quality checks step.
    """
    print("Starting quality checks...")
    run_quality_checks()
    print("Finished quality checks.")


@task(name="Build reporting marts")
def marts_task() -> None:
    """
    Run the marts transformation step.
    """
    print("Starting mart transformations...")
    run_mart_transformations()
    print("Finished mart transformations.")


@flow(name="manufacturing-operations-data-pipeline")
def manufacturing_pipeline_flow() -> None:
    """
    Main pipeline flow.

    This is the full order of the data pipeline:
    1. Load raw CSV files into staging
    2. Build warehouse tables
    3. Run quality checks
    4. Build reporting marts
    """
    staging_task()
    warehouse_task()
    quality_task()
    marts_task()

    print("Pipeline completed successfully.")


if __name__ == "__main__":
    manufacturing_pipeline_flow()