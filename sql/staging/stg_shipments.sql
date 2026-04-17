CREATE TABLE IF NOT EXISTS staging.stg_shipments (
    shipment_id VARCHAR(20),
    sales_order_id VARCHAR(20),
    supplier_id VARCHAR(20),
    ship_date DATE,
    delivery_date DATE,
    promised_delivery_date DATE,
    shipment_status VARCHAR(50)
);