CREATE TABLE IF NOT EXISTS staging.stg_suppliers (
    supplier_id VARCHAR(20),
    supplier_name VARCHAR(255),
    supplier_region VARCHAR(100),
    lead_time_days INT,
    status VARCHAR(50)
);