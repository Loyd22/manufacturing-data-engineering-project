CREATE TABLE IF NOT EXISTS warehouse.dim_supplier (
    supplier_key SERIAL PRIMARY KEY,
    supplier_id VARCHAR(20) UNIQUE,
    supplier_name VARCHAR(255),
    supplier_region VARCHAR(100),
    lead_time_days INT,
    status VARCHAR(50)
);

TRUNCATE TABLE warehouse.dim_supplier RESTART IDENTITY;

INSERT INTO warehouse.dim_supplier (
    supplier_id,
    supplier_name,
    supplier_region,
    lead_time_days,
    status
)
SELECT DISTINCT
    supplier_id,
    supplier_name,
    supplier_region,
    lead_time_days,
    status
FROM staging.stg_suppliers
WHERE supplier_id IS NOT NULL;