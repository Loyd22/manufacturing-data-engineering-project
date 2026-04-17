# Data Model Design

## 1. Database Schema Layers

This project uses a layered database design to separate raw input, cleaned core data, and reporting outputs.

### raw
Purpose:
- optional landing layer for untouched raw data
- keeps original source-level structure if needed

### staging
Purpose:
- stores raw CSV data after loading into PostgreSQL
- used for initial validation and transformation
- tables remain close to source structure

### warehouse
Purpose:
- stores cleaned, standardized, and structured data
- contains dimension tables and fact tables
- acts as the main source of truth

### marts
Purpose:
- stores final business-ready reporting tables
- used directly by dashboards and BI tools

---

## 2. Main Raw Files

The following CSV files will be ingested into the system:

- `production_orders.csv`
- `machine_logs.csv`
- `quality_inspections.csv`
- `inventory_movements.csv`
- `suppliers.csv`
- `shipment_records.csv`
- `sales_orders.csv`

---

## 3. Staging Tables

These tables store data loaded from CSV files.

### staging.stg_production_orders
Columns:
- production_order_id
- production_date
- product_id
- machine_id
- supplier_id
- quantity_planned
- quantity_produced
- shift
- status

### staging.stg_machine_logs
Columns:
- machine_log_id
- machine_id
- log_date
- uptime_minutes
- downtime_minutes
- downtime_reason

### staging.stg_quality_inspections
Columns:
- inspection_id
- production_order_id
- inspection_date
- defect_count
- inspected_units
- defect_type
- passed

### staging.stg_inventory_movements
Columns:
- movement_id
- product_id
- movement_date
- movement_type
- quantity
- warehouse_location

### staging.stg_suppliers
Columns:
- supplier_id
- supplier_name
- supplier_region
- lead_time_days
- status

### staging.stg_shipments
Columns:
- shipment_id
- sales_order_id
- supplier_id
- ship_date
- delivery_date
- promised_delivery_date
- shipment_status

### staging.stg_sales_orders
Columns:
- sales_order_id
- order_date
- product_id
- customer_region
- quantity_ordered

---

## 4. Warehouse Dimension Tables

Dimension tables store descriptive data used by fact tables.

### warehouse.dim_product
Columns:
- product_key
- product_id
- product_name
- product_category
- product_line
- is_active

### warehouse.dim_supplier
Columns:
- supplier_key
- supplier_id
- supplier_name
- supplier_region
- lead_time_days
- status

### warehouse.dim_machine
Columns:
- machine_key
- machine_id
- machine_name
- machine_type
- production_line
- is_active

### warehouse.dim_date
Columns:
- date_key
- full_date
- day
- month
- quarter
- year
- week_number

---

## 5. Warehouse Fact Tables

Fact tables store measurable business events.

### warehouse.fact_production
Columns:
- production_key
- production_order_id
- date_key
- product_key
- machine_key
- supplier_key
- quantity_planned
- quantity_produced
- shift
- status

### warehouse.fact_quality
Columns:
- quality_key
- inspection_id
- production_order_id
- date_key
- product_key
- defect_count
- inspected_units
- defect_type
- passed

### warehouse.fact_inventory
Columns:
- inventory_key
- movement_id
- date_key
- product_key
- movement_type
- quantity
- warehouse_location

### warehouse.fact_shipments
Columns:
- shipment_key
- shipment_id
- sales_order_id
- supplier_key
- date_key
- ship_date
- delivery_date
- promised_delivery_date
- shipment_status
- delay_days
- on_time_flag

### warehouse.fact_machine_logs
Columns:
- machine_log_key
- machine_log_id
- date_key
- machine_key
- uptime_minutes
- downtime_minutes
- downtime_reason

---

## 6. Reporting Mart Tables

These are the final business-ready tables for dashboards.

### marts.mart_daily_production_summary
Purpose:
- daily production totals and efficiency metrics

Main columns:
- production_date
- total_orders
- total_quantity_planned
- total_quantity_produced
- production_efficiency

### marts.mart_quality_trends
Purpose:
- defect trends over time by product or day

Main columns:
- inspection_date
- product_id
- total_defects
- total_inspected_units
- defect_rate

### marts.mart_machine_downtime
Purpose:
- machine downtime monitoring

Main columns:
- log_date
- machine_id
- total_uptime_minutes
- total_downtime_minutes
- downtime_percentage

### marts.mart_supplier_performance
Purpose:
- supplier delivery and performance tracking

Main columns:
- supplier_id
- supplier_name
- total_shipments
- late_shipments
- on_time_rate
- average_delay_days

### marts.mart_inventory_health
Purpose:
- inventory inflow and outflow analysis

Main columns:
- movement_date
- product_id
- total_inbound
- total_outbound
- net_movement

### marts.mart_shipment_performance
Purpose:
- shipment timing and delay analysis

Main columns:
- ship_date
- supplier_id
- total_shipments
- on_time_shipments
- delayed_shipments
- on_time_rate

---

## 7. High-Level Relationships

Main relationship flow:

- production orders connect to products, machines, and suppliers
- quality inspections connect to production orders
- inventory movements connect to products
- shipments connect to suppliers and sales orders
- machine logs connect to machines
- all fact tables connect to dim_date

---

## 8. Single Source of Truth Strategy

The warehouse layer is the main cleaned source of truth.

Rules:
- staging is for loaded source data
- warehouse is for cleaned structured data
- marts are for reporting and dashboards only

This separation helps make the pipeline easier to manage and more production-ready.