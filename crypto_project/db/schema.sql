CREATE TABLE IF NOT EXISTS crypto_prices (
    id SERIAL PRIMARY KEY,
    coin_id VARCHAR(50),
    symbol VARCHAR(10),
    name VARCHAR(50),
    timestamp TIMESTAMPTZ DEFAULT NOW(),
    price_usd NUMERIC,
    market_cap NUMERIC,
    volume_24h NUMERIC
);
