CREATE TABLE IF NOT EXISTS warehouse.dim_product (
    product_key SERIAL PRIMARY KEY,
    product_id VARCHAR(20) UNIQUE,
    product_name VARCHAR(100),
    product_category VARCHAR(100),
    product_line VARCHAR(100),
    is_active BOOLEAN
);

TRUNCATE TABLE warehouse.dim_product RESTART IDENTITY;

INSERT INTO warehouse.dim_product (
    product_id,
    product_name,
    product_category,
    product_line,
    is_active
)
SELECT DISTINCT
    product_id,
    'Product ' || product_id AS product_name,
    'General Category' AS product_category,
    'Main Product Line' AS product_line,
    TRUE AS is_active
FROM (
    SELECT product_id FROM staging.stg_production_orders
    UNION
    SELECT product_id FROM staging.stg_sales_orders
    UNION
    SELECT product_id FROM staging.stg_inventory_movements
) p
WHERE product_id IS NOT NULL;