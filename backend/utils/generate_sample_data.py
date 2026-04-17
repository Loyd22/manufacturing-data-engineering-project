"""
This script generates fake manufacturing CSV files for our data engineering project.

What it creates:
- suppliers.csv
- production_orders.csv
- machine_logs.csv
- quality_inspections.csv
- inventory_movements.csv
- shipment_records.csv
- sales_orders.csv

Where it saves them:
- data/raw/

Why this is useful:
- We do not need to manually type hundreds of rows
- We can regenerate data anytime
- The project becomes easier to test and scale
"""

import csv
import random
from datetime import datetime, timedelta
from pathlib import Path


# ---------------------------------------------------------
# Helper settings
# ---------------------------------------------------------

# This creates the output folder path: data/raw
OUTPUT_DIR = Path("data/raw")

# Make sure the folder exists before saving files
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Set a fixed random seed so the generated data is repeatable
# This means if you run the script again, the random pattern stays consistent
random.seed(42)

# Start date for our fake data timeline
START_DATE = datetime(2026, 1, 1)


# ---------------------------------------------------------
# Helper functions
# ---------------------------------------------------------

def random_date(max_days: int = 90) -> str:
    """
    Return a random date string in YYYY-MM-DD format.

    max_days means how many days forward from START_DATE
    the random date can go.
    """
    random_days = random.randint(0, max_days)
    date_value = START_DATE + timedelta(days=random_days)
    return date_value.strftime("%Y-%m-%d")


def write_csv(filename: str, fieldnames: list[str], rows: list[dict]) -> None:
    """
    Save a list of dictionary rows into a CSV file.

    filename: output file name
    fieldnames: the column names
    rows: list of row dictionaries
    """
    file_path = OUTPUT_DIR / filename

    with open(file_path, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Created: {file_path} ({len(rows)} rows)")


# ---------------------------------------------------------
# Master ID lists
# ---------------------------------------------------------

# Create 100 products: PROD001 to PROD100
PRODUCT_IDS = [f"PROD{i:03d}" for i in range(1, 101)]

# Create 10 machines: MCH001 to MCH010
MACHINE_IDS = [f"MCH{i:03d}" for i in range(1, 11)]

# Create 20 suppliers: SUP001 to SUP020
SUPPLIER_IDS = [f"SUP{i:03d}" for i in range(1, 21)]

# Some reusable values to make the data more realistic
SUPPLIER_REGIONS = ["NCR", "CALABARZON", "Central Luzon", "Cebu", "Davao"]
SHIFTS = ["morning", "evening", "night"]
PRODUCTION_STATUS = ["completed", "completed", "completed", "delayed"]
DOWNTIME_REASONS = ["maintenance", "setup", "breakdown", "power_issue", "inspection"]
DEFECT_TYPES = ["scratch", "alignment", "dimension", "dent", "surface_issue"]
WAREHOUSE_LOCATIONS = ["WH-A", "WH-B", "WH-C"]
SHIPMENT_STATUS = ["delivered", "delivered", "delivered", "delayed"]
CUSTOMER_REGIONS = ["NCR", "CALABARZON", "Cebu", "Davao", "Iloilo"]


# ---------------------------------------------------------
# 1. Generate suppliers.csv
# ---------------------------------------------------------

def generate_suppliers() -> None:
    """
    Create supplier master data.
    """
    rows = []

    for i, supplier_id in enumerate(SUPPLIER_IDS, start=1):
        rows.append(
            {
                "supplier_id": supplier_id,
                "supplier_name": f"Supplier {i}",
                "supplier_region": random.choice(SUPPLIER_REGIONS),
                "lead_time_days": random.randint(3, 14),
                "status": random.choice(["active", "active", "active", "inactive"]),
            }
        )

    fieldnames = [
        "supplier_id",
        "supplier_name",
        "supplier_region",
        "lead_time_days",
        "status",
    ]

    write_csv("suppliers.csv", fieldnames, rows)


# ---------------------------------------------------------
# 2. Generate sales_orders.csv
# ---------------------------------------------------------

def generate_sales_orders(num_rows: int = 500) -> list[str]:
    """
    Create fake sales orders.

    Returns:
        A list of created sales order IDs so other files can use them.
    """
    rows = []
    sales_order_ids = []

    for i in range(1, num_rows + 1):
        sales_order_id = f"SO{i:04d}"
        sales_order_ids.append(sales_order_id)

        rows.append(
            {
                "sales_order_id": sales_order_id,
                "order_date": random_date(),
                "product_id": random.choice(PRODUCT_IDS),
                "customer_region": random.choice(CUSTOMER_REGIONS),
                "quantity_ordered": random.randint(50, 500),
            }
        )

    fieldnames = [
        "sales_order_id",
        "order_date",
        "product_id",
        "customer_region",
        "quantity_ordered",
    ]

    write_csv("sales_orders.csv", fieldnames, rows)
    return sales_order_ids


# ---------------------------------------------------------
# 3. Generate production_orders.csv
# ---------------------------------------------------------

def generate_production_orders(num_rows: int = 1000) -> list[str]:
    """
    Create fake production orders.

    Returns:
        A list of created production order IDs so quality data can use them.
    """
    rows = []
    production_order_ids = []

    for i in range(1, num_rows + 1):
        production_order_id = f"PO{i:04d}"
        production_order_ids.append(production_order_id)

        quantity_planned = random.randint(100, 1000)

        # quantity_produced should usually be <= quantity_planned
        quantity_produced = random.randint(
            max(0, quantity_planned - 120),
            quantity_planned
        )

        rows.append(
            {
                "production_order_id": production_order_id,
                "production_date": random_date(),
                "product_id": random.choice(PRODUCT_IDS),
                "machine_id": random.choice(MACHINE_IDS),
                "supplier_id": random.choice(SUPPLIER_IDS),
                "quantity_planned": quantity_planned,
                "quantity_produced": quantity_produced,
                "shift": random.choice(SHIFTS),
                "status": random.choice(PRODUCTION_STATUS),
            }
        )

    fieldnames = [
        "production_order_id",
        "production_date",
        "product_id",
        "machine_id",
        "supplier_id",
        "quantity_planned",
        "quantity_produced",
        "shift",
        "status",
    ]

    write_csv("production_orders.csv", fieldnames, rows)
    return production_order_ids


# ---------------------------------------------------------
# 4. Generate machine_logs.csv
# ---------------------------------------------------------

def generate_machine_logs(num_rows: int = 1000) -> None:
    """
    Create fake machine logs.

    We keep uptime + downtime within a realistic shift/day range.
    """
    rows = []

    for i in range(1, num_rows + 1):
        uptime_minutes = random.randint(300, 480)
        downtime_minutes = random.randint(0, 180)

        rows.append(
            {
                "machine_log_id": f"ML{i:04d}",
                "machine_id": random.choice(MACHINE_IDS),
                "log_date": random_date(),
                "uptime_minutes": uptime_minutes,
                "downtime_minutes": downtime_minutes,
                "downtime_reason": random.choice(DOWNTIME_REASONS),
            }
        )

    fieldnames = [
        "machine_log_id",
        "machine_id",
        "log_date",
        "uptime_minutes",
        "downtime_minutes",
        "downtime_reason",
    ]

    write_csv("machine_logs.csv", fieldnames, rows)


# ---------------------------------------------------------
# 5. Generate quality_inspections.csv
# ---------------------------------------------------------

def generate_quality_inspections(
    production_order_ids: list[str],
    num_rows: int = 500
) -> None:
    """
    Create fake quality inspections tied to production orders.
    """
    rows = []

    for i in range(1, num_rows + 1):
        inspected_units = random.randint(50, 200)
        defect_count = random.randint(0, min(25, inspected_units))

        rows.append(
            {
                "inspection_id": f"QI{i:04d}",
                "production_order_id": random.choice(production_order_ids),
                "inspection_date": random_date(),
                "defect_count": defect_count,
                "inspected_units": inspected_units,
                "defect_type": random.choice(DEFECT_TYPES),
                "passed": "true" if defect_count <= 10 else "false",
            }
        )

    fieldnames = [
        "inspection_id",
        "production_order_id",
        "inspection_date",
        "defect_count",
        "inspected_units",
        "defect_type",
        "passed",
    ]

    write_csv("quality_inspections.csv", fieldnames, rows)


# ---------------------------------------------------------
# 6. Generate inventory_movements.csv
# ---------------------------------------------------------

def generate_inventory_movements(num_rows: int = 500) -> None:
    """
    Create fake inventory movement data.
    """
    rows = []

    for i in range(1, num_rows + 1):
        rows.append(
            {
                "movement_id": f"INV{i:04d}",
                "product_id": random.choice(PRODUCT_IDS),
                "movement_date": random_date(),
                "movement_type": random.choice(["IN", "OUT"]),
                "quantity": random.randint(20, 600),
                "warehouse_location": random.choice(WAREHOUSE_LOCATIONS),
            }
        )

    fieldnames = [
        "movement_id",
        "product_id",
        "movement_date",
        "movement_type",
        "quantity",
        "warehouse_location",
    ]

    write_csv("inventory_movements.csv", fieldnames, rows)


# ---------------------------------------------------------
# 7. Generate shipment_records.csv
# ---------------------------------------------------------

def generate_shipment_records(
    sales_order_ids: list[str],
    num_rows: int = 500
) -> None:
    """
    Create fake shipment records tied to sales orders.

    Some shipments are on time, some are delayed.
    """
    rows = []

    for i in range(1, num_rows + 1):
        ship_base = START_DATE + timedelta(days=random.randint(0, 90))
        ship_date = ship_base
        promised_delivery_date = ship_date + timedelta(days=random.randint(1, 7))

        # Some deliveries are late on purpose
        late_days = random.choice([0, 0, 0, 1, 2, 3])
        delivery_date = promised_delivery_date + timedelta(days=late_days)

        shipment_status = "delivered" if late_days == 0 else "delayed"

        rows.append(
            {
                "shipment_id": f"SH{i:04d}",
                "sales_order_id": random.choice(sales_order_ids),
                "supplier_id": random.choice(SUPPLIER_IDS),
                "ship_date": ship_date.strftime("%Y-%m-%d"),
                "delivery_date": delivery_date.strftime("%Y-%m-%d"),
                "promised_delivery_date": promised_delivery_date.strftime("%Y-%m-%d"),
                "shipment_status": shipment_status,
            }
        )

    fieldnames = [
        "shipment_id",
        "sales_order_id",
        "supplier_id",
        "ship_date",
        "delivery_date",
        "promised_delivery_date",
        "shipment_status",
    ]

    write_csv("shipment_records.csv", fieldnames, rows)


# ---------------------------------------------------------
# Main function
# ---------------------------------------------------------

def main() -> None:
    """
    Run all generators in the correct order.
    """
    print("Generating sample manufacturing data...")

    generate_suppliers()
    sales_order_ids = generate_sales_orders()
    production_order_ids = generate_production_orders()
    generate_machine_logs()
    generate_quality_inspections(production_order_ids)
    generate_inventory_movements()
    generate_shipment_records(sales_order_ids)

    print("Done. All CSV files were created inside data/raw/")


# This runs the script only when you execute this file directly
if __name__ == "__main__":
    main()