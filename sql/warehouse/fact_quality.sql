CREATE TABLE IF NOT EXISTS warehouse.fact_quality (
    quality_key SERIAL PRIMARY KEY,
    inspection_id VARCHAR(20),
    production_order_id VARCHAR(20),
    date_key INT,
    product_key INT,
    defect_count INT,
    inspected_units INT,
    defect_type VARCHAR(100),
    passed BOOLEAN
);

TRUNCATE TABLE warehouse.fact_quality RESTART IDENTITY;

INSERT INTO warehouse.fact_quality (
    inspection_id,
    production_order_id,
    date_key,
    product_key,
    defect_count,
    inspected_units,
    defect_type,
    passed
)
SELECT
    q.inspection_id,
    q.production_order_id,
    CAST(TO_CHAR(q.inspection_date, 'YYYYMMDD') AS INT) AS date_key,
    dp.product_key,
    q.defect_count,
    q.inspected_units,
    q.defect_type,
    q.passed
FROM staging.stg_quality_inspections q
LEFT JOIN staging.stg_production_orders p
    ON q.production_order_id = p.production_order_id
LEFT JOIN warehouse.dim_product dp
    ON p.product_id = dp.product_id
WHERE q.inspection_id IS NOT NULL;