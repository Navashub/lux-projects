from airflow import DAG
from airflow.providers.http.hooks.http import HttpHook
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.decorators import task
from datetime import datetime, timedelta
import requests
import json

# Configuration
POSTGRES_CONN_ID = 'crypto_postgres'
API_CONN_ID = 'coinmarketcap_api'

# Top 10 cryptocurrencies by market cap (you can modify this list)
CRYPTO_SYMBOLS = ['BTC', 'ETH', 'BNB', 'XRP', 'ADA', 'DOGE', 'MATIC', 'SOL', 'DOT', 'LTC']

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2025, 6, 2),
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

## DAG
with DAG(dag_id='crypto_etl_pipeline',
         default_args=default_args,
         schedule='@hourly',  # Run every hour for crypto data
         catchup=False) as dag:

    @task()
    def extract_crypto_data():
        """Extract cryptocurrency data from CoinMarketCap API."""
        
        # Use the HTTP hook to get connection details from airflow connections
        http_hook = HttpHook(http_conn_id=API_CONN_ID, method='GET')
        
        # Build the API endpoint for latest quotes
        # CoinMarketCap API endpoint for latest cryptocurrency quotes
        symbols_str = ','.join(CRYPTO_SYMBOLS)
        endpoint = f'/v1/cryptocurrency/quotes/latest?symbol={symbols_str}&convert=USD'
        
        # Set headers (API key will be in the connection extra field)
        headers = {
            'Accept': 'application/json',
            'Accept-Encoding': 'deflate, gzip'
        }
        
        # Make the request via the HTTP hook
        response = http_hook.run(endpoint, headers=headers)
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to fetch crypto data: {response.status_code} - {response.text}")

    @task()
    def transform_crypto_data(crypto_data):
        """Transform the extracted cryptocurrency data."""
        
        transformed_data = []
        
        # Extract data from the API response
        if 'data' in crypto_data:
            for symbol in CRYPTO_SYMBOLS:
                if symbol in crypto_data['data']:
                    coin_data = crypto_data['data'][symbol]
                    quote_data = coin_data['quote']['USD']
                    
                    transformed_record = {
                        'symbol': coin_data['symbol'],
                        'name': coin_data['name'],
                        'price': quote_data['price'],
                        'market_cap': quote_data['market_cap'],
                        'volume_24h': quote_data['volume_24h'],
                        'percent_change_1h': quote_data['percent_change_1h'],
                        'percent_change_24h': quote_data['percent_change_24h'],
                        'percent_change_7d': quote_data['percent_change_7d'],
                        'circulating_supply': coin_data['circulating_supply'],
                        'total_supply': coin_data['total_supply'],
                        'max_supply': coin_data['max_supply'],
                        'cmc_rank': coin_data['cmc_rank'],
                        'last_updated': quote_data['last_updated']
                    }
                    transformed_data.append(transformed_record)
        
        return transformed_data

    @task()
    def load_crypto_data(transformed_data):
        """Load transformed cryptocurrency data into PostgreSQL."""
        
        pg_hook = PostgresHook(postgres_conn_id=POSTGRES_CONN_ID)
        conn = pg_hook.get_conn()
        cursor = conn.cursor()
        
        # Create table if it doesn't exist
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS crypto_data (
            id SERIAL PRIMARY KEY,
            symbol VARCHAR(10) NOT NULL,
            name VARCHAR(100) NOT NULL,
            price DECIMAL(20, 8),
            market_cap BIGINT,
            volume_24h BIGINT,
            percent_change_1h DECIMAL(10, 4),
            percent_change_24h DECIMAL(10, 4),
            percent_change_7d DECIMAL(10, 4),
            circulating_supply BIGINT,
            total_supply BIGINT,
            max_supply BIGINT,
            cmc_rank INTEGER,
            last_updated TIMESTAMP,
            inserted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)
        
        # Insert transformed data into the table
        for record in transformed_data:
            cursor.execute("""
            INSERT INTO crypto_data (
                symbol, name, price, market_cap, volume_24h, 
                percent_change_1h, percent_change_24h, percent_change_7d,
                circulating_supply, total_supply, max_supply, cmc_rank, last_updated
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
            """, (
                record['symbol'],
                record['name'],
                record['price'],
                record['market_cap'],
                record['volume_24h'],
                record['percent_change_1h'],
                record['percent_change_24h'],
                record['percent_change_7d'],
                record['circulating_supply'],
                record['total_supply'],
                record['max_supply'],
                record['cmc_rank'],
                record['last_updated']
            ))
        
        # Commit the transaction
        conn.commit()
        cursor.close()
        
        print(f"Successfully loaded {len(transformed_data)} cryptocurrency records")

    # DAG workflow - ETL Pipeline
    crypto_raw_data = extract_crypto_data()
    transformed_crypto_data = transform_crypto_data(crypto_raw_data)
    load_crypto_data(transformed_crypto_data)