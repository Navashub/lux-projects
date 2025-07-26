-- Creating dimension tables
CREATE TABLE dim_product (
    product_id SERIAL PRIMARY KEY,
    product_name VARCHAR(100),
    category VARCHAR(50)
);

CREATE TABLE dim_county (
    county_id SERIAL PRIMARY KEY,
    county_name VARCHAR(50),
    region VARCHAR(50)
);

CREATE TABLE dim_time (
    time_id SERIAL PRIMARY KEY,
    date DATE,
    month INT,
    year INT
);

-- Creating fact table
CREATE TABLE fact_prices (
    price_id SERIAL PRIMARY KEY,
    product_id INT REFERENCES dim_product(product_id),
    county_id INT REFERENCES dim_county(county_id),
    time_id INT REFERENCES dim_time(time_id),
    price FLOAT,
    unit VARCHAR(20)
);

-- Creating metadata table
CREATE TABLE metadata (
    metadata_id SERIAL PRIMARY KEY,
    source VARCHAR(100),
    update_date TIMESTAMP,
    record_count INT
);