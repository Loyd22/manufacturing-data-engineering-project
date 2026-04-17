CREATE TABLE IF NOT EXISTS marts.mart_inventory_health (
    movement_date DATE,
    product_id VARCHAR(20),
    total_inbound BIGINT,
    total_outbound BIGINT,
    net_movement BIGINT
);

TRUNCATE TABLE marts.mart_inventory_health;

INSERT INTO marts.mart_inventory_health (
    movement_date,
    product_id,
    total_inbound,
    total_outbound,
    net_movement
)
SELECT
    d.full_date AS movement_date,
    dp.product_id,
    SUM(CASE WHEN f.movement_type = 'IN' THEN f.quantity ELSE 0 END) AS total_inbound,
    SUM(CASE WHEN f.movement_type = 'OUT' THEN f.quantity ELSE 0 END) AS total_outbound,
    SUM(CASE WHEN f.movement_type = 'IN' THEN f.quantity ELSE 0 END) -
    SUM(CASE WHEN f.movement_type = 'OUT' THEN f.quantity ELSE 0 END) AS net_movement
FROM warehouse.fact_inventory f
LEFT JOIN warehouse.dim_date d
    ON f.date_key = d.date_key
LEFT JOIN warehouse.dim_product dp
    ON f.product_key = dp.product_key
GROUP BY d.full_date, dp.product_id
ORDER BY d.full_date, dp.product_id;