CREATE TABLE IF NOT EXISTS warehouse.dim_date (
    date_key INT PRIMARY KEY,
    full_date DATE UNIQUE,
    day INT,
    month INT,
    quarter INT,
    year INT,
    week_number INT
);

TRUNCATE TABLE warehouse.dim_date;

INSERT INTO warehouse.dim_date (
    date_key,
    full_date,
    day,
    month,
    quarter,
    year,
    week_number
)
SELECT DISTINCT
    CAST(TO_CHAR(d.full_date, 'YYYYMMDD') AS INT) AS date_key,
    d.full_date,
    EXTRACT(DAY FROM d.full_date)::INT AS day,
    EXTRACT(MONTH FROM d.full_date)::INT AS month,
    EXTRACT(QUARTER FROM d.full_date)::INT AS quarter,
    EXTRACT(YEAR FROM d.full_date)::INT AS year,
    EXTRACT(WEEK FROM d.full_date)::INT AS week_number
FROM (
    SELECT production_date AS full_date FROM staging.stg_production_orders
    UNION
    SELECT log_date AS full_date FROM staging.stg_machine_logs
    UNION
    SELECT inspection_date AS full_date FROM staging.stg_quality_inspections
    UNION
    SELECT movement_date AS full_date FROM staging.stg_inventory_movements
    UNION
    SELECT ship_date AS full_date FROM staging.stg_shipments
    UNION
    SELECT delivery_date AS full_date FROM staging.stg_shipments
    UNION
    SELECT promised_delivery_date AS full_date FROM staging.stg_shipments
    UNION
    SELECT order_date AS full_date FROM staging.stg_sales_orders
) d
WHERE d.full_date IS NOT NULL;