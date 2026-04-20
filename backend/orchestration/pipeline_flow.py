"""
Main orchestration flow for the manufacturing data pipeline.
"""

from prefect import flow, task

from backend.ingestion.load_all_staging import main as run_staging_ingestion
from backend.transformation.run_warehouse_transformations import main as run_warehouse_transformations
from backend.quality.run_quality_checks import main as run_quality_checks
from backend.transformation.run_mart_transformations import main as run_mart_transformations
from backend.utils.logger import get_logger

logger = get_logger(__name__)


@task(name="Load staging data")
def staging_task() -> None:
    logger.info("Starting staging ingestion task")
    run_staging_ingestion()
    logger.info("Finished staging ingestion task")


@task(name="Build warehouse tables")
def warehouse_task() -> None:
    logger.info("Starting warehouse transformation task")
    run_warehouse_transformations()
    logger.info("Finished warehouse transformation task")


@task(name="Run data quality checks")
def quality_task() -> None:
    logger.info("Starting quality checks task")
    run_quality_checks()
    logger.info("Finished quality checks task")


@task(name="Build reporting marts")
def marts_task() -> None:
    logger.info("Starting mart transformation task")
    run_mart_transformations()
    logger.info("Finished mart transformation task")


@flow(name="manufacturing-operations-data-pipeline")
def manufacturing_pipeline_flow() -> None:
    """
    Full pipeline flow.
    """
    logger.info("Pipeline flow started")

    staging_task()
    warehouse_task()
    quality_task()
    marts_task()

    logger.info("Pipeline flow completed successfully")


if __name__ == "__main__":
    manufacturing_pipeline_flow()