CREATE TABLE IF NOT EXISTS food_prices (
    date DATE,
    admin1 VARCHAR(255),
    admin2 VARCHAR(255),
    market VARCHAR(255),
    market_id INT,
    latitude FLOAT,
    longitude FLOAT,
    category VARCHAR(255),
    commodity VARCHAR(255),
    commodity_id INT,
    unit VARCHAR(50),
    priceflag VARCHAR(50),
    pricetype VARCHAR(50),
    currency VARCHAR(10),
    price FLOAT,
    usdprice FLOAT
);

-- Dimension tables for star schema
CREATE TABLE IF NOT EXISTS dim_commodity (
    id SERIAL PRIMARY KEY,
    category VARCHAR(255),
    commodity VARCHAR(255),
    unit VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS dim_location (
    id SERIAL PRIMARY KEY,
    admin1 VARCHAR(255),
    admin2 VARCHAR(255),
    market VARCHAR(255)
);

-- Fact table
CREATE TABLE IF NOT EXISTS fact_prices (
    id SERIAL PRIMARY KEY,
    date DATE,
    commodity_id INT REFERENCES dim_commodity(id),
    location_id INT REFERENCES dim_location(id),
    price FLOAT,
    usdprice FLOAT,
    priceflag VARCHAR(50),
    pricetype VARCHAR(50),
    currency VARCHAR(10)
); 