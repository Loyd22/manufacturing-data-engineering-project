SELECT 'missing_shipment_id' AS check_name, COUNT(*) AS issue_count
FROM staging.stg_shipments
WHERE shipment_id IS NULL

UNION ALL

SELECT 'delivery_before_ship_date' AS check_name, COUNT(*) AS issue_count
FROM staging.stg_shipments
WHERE delivery_date < ship_date

UNION ALL

SELECT 'promised_before_ship_date' AS check_name, COUNT(*) AS issue_count
FROM staging.stg_shipments
WHERE promised_delivery_date < ship_date

UNION ALL

SELECT 'duplicate_shipment_id' AS check_name, COUNT(*) AS issue_count
FROM (
    SELECT shipment_id
    FROM staging.stg_shipments
    WHERE shipment_id IS NOT NULL
    GROUP BY shipment_id
    HAVING COUNT(*) > 1
) dup;