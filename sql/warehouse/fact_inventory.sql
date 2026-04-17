CREATE TABLE IF NOT EXISTS warehouse.fact_inventory (
    inventory_key SERIAL PRIMARY KEY,
    movement_id VARCHAR(20),
    date_key INT,
    product_key INT,
    movement_type VARCHAR(10),
    quantity INT,
    warehouse_location VARCHAR(50)
);

TRUNCATE TABLE warehouse.fact_inventory RESTART IDENTITY;

INSERT INTO warehouse.fact_inventory (
    movement_id,
    date_key,
    product_key,
    movement_type,
    quantity,
    warehouse_location
)
SELECT
    i.movement_id,
    CAST(TO_CHAR(i.movement_date, 'YYYYMMDD') AS INT) AS date_key,
    dp.product_key,
    i.movement_type,
    i.quantity,
    i.warehouse_location
FROM staging.stg_inventory_movements i
LEFT JOIN warehouse.dim_product dp
    ON i.product_id = dp.product_id
WHERE i.movement_id IS NOT NULL;