CREATE TABLE IF NOT EXISTS warehouse.fact_production (
    production_key SERIAL PRIMARY KEY,
    production_order_id VARCHAR(20),
    date_key INT,
    product_key INT,
    machine_key INT,
    supplier_key INT,
    quantity_planned INT,
    quantity_produced INT,
    shift VARCHAR(50),
    status VARCHAR(50)
);

TRUNCATE TABLE warehouse.fact_production RESTART IDENTITY;

INSERT INTO warehouse.fact_production (
    production_order_id,
    date_key,
    product_key,
    machine_key,
    supplier_key,
    quantity_planned,
    quantity_produced,
    shift,
    status
)
SELECT
    s.production_order_id,
    CAST(TO_CHAR(s.production_date, 'YYYYMMDD') AS INT) AS date_key,
    dp.product_key,
    dm.machine_key,
    ds.supplier_key,
    s.quantity_planned,
    s.quantity_produced,
    s.shift,
    s.status
FROM staging.stg_production_orders s
LEFT JOIN warehouse.dim_product dp
    ON s.product_id = dp.product_id
LEFT JOIN warehouse.dim_machine dm
    ON s.machine_id = dm.machine_id
LEFT JOIN warehouse.dim_supplier ds
    ON s.supplier_id = ds.supplier_id
WHERE s.production_order_id IS NOT NULL;