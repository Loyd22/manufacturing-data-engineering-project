CREATE TABLE IF NOT EXISTS staging.stg_inventory_movements (
    movement_id VARCHAR(20),
    product_id VARCHAR(20),
    movement_date DATE,
    movement_type VARCHAR(10),
    quantity INT,
    warehouse_location VARCHAR(50)
);