CREATE TABLE IF NOT EXISTS staging.stg_sales_orders (
    sales_order_id VARCHAR(20),
    order_date DATE,
    product_id VARCHAR(20),
    customer_region VARCHAR(100),
    quantity_ordered INT
);