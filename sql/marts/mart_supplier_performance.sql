CREATE TABLE IF NOT EXISTS marts.mart_supplier_performance (
    supplier_id VARCHAR(20),
    supplier_name VARCHAR(255),
    total_shipments BIGINT,
    late_shipments BIGINT,
    on_time_rate NUMERIC(10,4),
    average_delay_days NUMERIC(10,2)
);

TRUNCATE TABLE marts.mart_supplier_performance;

INSERT INTO marts.mart_supplier_performance (
    supplier_id,
    supplier_name,
    total_shipments,
    late_shipments,
    on_time_rate,
    average_delay_days
)
SELECT
    ds.supplier_id,
    ds.supplier_name,
    COUNT(f.shipment_id) AS total_shipments,
    SUM(CASE WHEN f.on_time_flag = FALSE THEN 1 ELSE 0 END) AS late_shipments,
    CASE
        WHEN COUNT(f.shipment_id) = 0 THEN 0
        ELSE ROUND(
            SUM(CASE WHEN f.on_time_flag = TRUE THEN 1 ELSE 0 END)::NUMERIC /
            COUNT(f.shipment_id)::NUMERIC,
            4
        )
    END AS on_time_rate,
    ROUND(AVG(COALESCE(f.delay_days, 0))::NUMERIC, 2) AS average_delay_days
FROM warehouse.fact_shipments f
LEFT JOIN warehouse.dim_supplier ds
    ON f.supplier_key = ds.supplier_key
GROUP BY ds.supplier_id, ds.supplier_name
ORDER BY ds.supplier_id;