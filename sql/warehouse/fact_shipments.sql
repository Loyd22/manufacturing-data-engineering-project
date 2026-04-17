CREATE TABLE IF NOT EXISTS warehouse.fact_shipments (
    shipment_key SERIAL PRIMARY KEY,
    shipment_id VARCHAR(20),
    sales_order_id VARCHAR(20),
    supplier_key INT,
    date_key INT,
    ship_date DATE,
    delivery_date DATE,
    promised_delivery_date DATE,
    shipment_status VARCHAR(50),
    delay_days INT,
    on_time_flag BOOLEAN
);

TRUNCATE TABLE warehouse.fact_shipments RESTART IDENTITY;

INSERT INTO warehouse.fact_shipments (
    shipment_id,
    sales_order_id,
    supplier_key,
    date_key,
    ship_date,
    delivery_date,
    promised_delivery_date,
    shipment_status,
    delay_days,
    on_time_flag
)
SELECT
    s.shipment_id,
    s.sales_order_id,
    ds.supplier_key,
    CAST(TO_CHAR(s.ship_date, 'YYYYMMDD') AS INT) AS date_key,
    s.ship_date,
    s.delivery_date,
    s.promised_delivery_date,
    s.shipment_status,
    GREATEST((s.delivery_date - s.promised_delivery_date), 0) AS delay_days,
    CASE
        WHEN s.delivery_date <= s.promised_delivery_date THEN TRUE
        ELSE FALSE
    END AS on_time_flag
FROM staging.stg_shipments s
LEFT JOIN warehouse.dim_supplier ds
    ON s.supplier_id = ds.supplier_id
WHERE s.shipment_id IS NOT NULL;