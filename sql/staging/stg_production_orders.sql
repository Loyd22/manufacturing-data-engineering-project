CREATE TABLE IF NOT EXISTS staging.stg_production_orders (
    production_order_id VARCHAR(20),
    production_date DATE,
    product_id VARCHAR(20),
    machine_id VARCHAR(20),
    supplier_id VARCHAR(20),
    quantity_planned INT,
    quantity_produced INT,
    shift VARCHAR(50),
    status VARCHAR(50)
);