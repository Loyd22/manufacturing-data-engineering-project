CREATE TABLE IF NOT EXISTS marts.mart_shipment_performance (
    ship_date DATE,
    supplier_id VARCHAR(20),
    total_shipments BIGINT,
    on_time_shipments BIGINT,
    delayed_shipments BIGINT,
    on_time_rate NUMERIC(10,4)
);

TRUNCATE TABLE marts.mart_shipment_performance;

INSERT INTO marts.mart_shipment_performance (
    ship_date,
    supplier_id,
    total_shipments,
    on_time_shipments,
    delayed_shipments,
    on_time_rate
)
SELECT
    d.full_date AS ship_date,
    ds.supplier_id,
    COUNT(f.shipment_id) AS total_shipments,
    SUM(CASE WHEN f.on_time_flag = TRUE THEN 1 ELSE 0 END) AS on_time_shipments,
    SUM(CASE WHEN f.on_time_flag = FALSE THEN 1 ELSE 0 END) AS delayed_shipments,
    CASE
        WHEN COUNT(f.shipment_id) = 0 THEN 0
        ELSE ROUND(
            SUM(CASE WHEN f.on_time_flag = TRUE THEN 1 ELSE 0 END)::NUMERIC /
            COUNT(f.shipment_id)::NUMERIC,
            4
        )
    END AS on_time_rate
FROM warehouse.fact_shipments f
LEFT JOIN warehouse.dim_date d
    ON f.date_key = d.date_key
LEFT JOIN warehouse.dim_supplier ds
    ON f.supplier_key = ds.supplier_key
GROUP BY d.full_date, ds.supplier_id
ORDER BY d.full_date, ds.supplier_id;