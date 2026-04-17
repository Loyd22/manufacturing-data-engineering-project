"""
This script loads all raw CSV files into PostgreSQL staging tables.

Why this file exists:
- It acts as the main ingestion runner
- It calls the reusable loader function for each CSV
- It keeps the ingestion process organized
"""

from backend.utils.db import get_engine
from backend.utils.csv_loader import load_csv_to_table


def main() -> None:
    """
    Run all staging loads in order.
    """
    print("Starting staging ingestion process...")

    engine = get_engine()

    ingestion_jobs = [
        {
            "csv_path": "data/raw/suppliers.csv",
            "table_name": "stg_suppliers",
            "schema_name": "staging",
            "required_columns": [
                "supplier_id",
                "supplier_name",
                "supplier_region",
                "lead_time_days",
                "status",
            ],
        },
        {
            "csv_path": "data/raw/sales_orders.csv",
            "table_name": "stg_sales_orders",
            "schema_name": "staging",
            "required_columns": [
                "sales_order_id",
                "order_date",
                "product_id",
                "customer_region",
                "quantity_ordered",
            ],
        },
        {
            "csv_path": "data/raw/production_orders.csv",
            "table_name": "stg_production_orders",
            "schema_name": "staging",
            "required_columns": [
                "production_order_id",
                "production_date",
                "product_id",
                "machine_id",
                "supplier_id",
                "quantity_planned",
                "quantity_produced",
                "shift",
                "status",
            ],
        },
        {
            "csv_path": "data/raw/machine_logs.csv",
            "table_name": "stg_machine_logs",
            "schema_name": "staging",
            "required_columns": [
                "machine_log_id",
                "machine_id",
                "log_date",
                "uptime_minutes",
                "downtime_minutes",
                "downtime_reason",
            ],
        },
        {
            "csv_path": "data/raw/quality_inspections.csv",
            "table_name": "stg_quality_inspections",
            "schema_name": "staging",
            "required_columns": [
                "inspection_id",
                "production_order_id",
                "inspection_date",
                "defect_count",
                "inspected_units",
                "defect_type",
                "passed",
            ],
        },
        {
            "csv_path": "data/raw/inventory_movements.csv",
            "table_name": "stg_inventory_movements",
            "schema_name": "staging",
            "required_columns": [
                "movement_id",
                "product_id",
                "movement_date",
                "movement_type",
                "quantity",
                "warehouse_location",
            ],
        },
        {
            "csv_path": "data/raw/shipment_records.csv",
            "table_name": "stg_shipments",
            "schema_name": "staging",
            "required_columns": [
                "shipment_id",
                "sales_order_id",
                "supplier_id",
                "ship_date",
                "delivery_date",
                "promised_delivery_date",
                "shipment_status",
            ],
        },
    ]

    for job in ingestion_jobs:
        try:
            load_csv_to_table(
                csv_path=job["csv_path"],
                table_name=job["table_name"],
                schema_name=job["schema_name"],
                required_columns=job["required_columns"],
                engine=engine,
            )
        except Exception as error:
            print(f"Failed loading {job['csv_path']}: {error}")
            raise

    print("\nAll staging files loaded successfully.")


if __name__ == "__main__":
    main()