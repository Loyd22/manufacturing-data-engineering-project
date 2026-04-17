SELECT 'missing_movement_id' AS check_name, COUNT(*) AS issue_count
FROM staging.stg_inventory_movements
WHERE movement_id IS NULL

UNION ALL

SELECT 'negative_inventory_quantity' AS check_name, COUNT(*) AS issue_count
FROM staging.stg_inventory_movements
WHERE quantity < 0

UNION ALL

SELECT 'invalid_movement_type' AS check_name, COUNT(*) AS issue_count
FROM staging.stg_inventory_movements
WHERE movement_type NOT IN ('IN', 'OUT')

UNION ALL

SELECT 'duplicate_movement_id' AS check_name, COUNT(*) AS issue_count
FROM (
    SELECT movement_id
    FROM staging.stg_inventory_movements
    WHERE movement_id IS NOT NULL
    GROUP BY movement_id
    HAVING COUNT(*) > 1
) dup;