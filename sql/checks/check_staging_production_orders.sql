SELECT 'missing_production_order_id' AS check_name, COUNT(*) AS issue_count
FROM staging.stg_production_orders
WHERE production_order_id IS NULL

UNION ALL

SELECT 'negative_quantity_planned' AS check_name, COUNT(*) AS issue_count
FROM staging.stg_production_orders
WHERE quantity_planned < 0

UNION ALL

SELECT 'negative_quantity_produced' AS check_name, COUNT(*) AS issue_count
FROM staging.stg_production_orders
WHERE quantity_produced < 0

UNION ALL

SELECT 'produced_greater_than_planned' AS check_name, COUNT(*) AS issue_count
FROM staging.stg_production_orders
WHERE quantity_produced > quantity_planned

UNION ALL

SELECT 'duplicate_production_order_id' AS check_name, COUNT(*) AS issue_count
FROM (
    SELECT production_order_id
    FROM staging.stg_production_orders
    WHERE production_order_id IS NOT NULL
    GROUP BY production_order_id
    HAVING COUNT(*) > 1
) dup;