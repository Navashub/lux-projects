from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import requests, psycopg2
from os import getenv
import logging

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2025, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

COINS = ["bitcoin", "ethereum", "tether", "binancecoin", "solana", "dogecoin", "tron",
         "cardano", "polkadot", "litecoin", "avalanche-2", "chainlink", "stellar", "uniswap", "monero"]

def fetch_and_store():
    url = f"https://api.coingecko.com/api/v3/simple/price"
    params = {
        'ids': ','.join(COINS),
        'vs_currencies': 'usd',
        'include_market_cap': 'true',
        'include_24hr_vol': 'true'
    }
    response = requests.get(url, params=params).json()

    conn = psycopg2.connect(
        dbname="your_db_name",
        user="your_user",
        password="your_password",
        host="localhost",
        port="5433"
    )
    cur = conn.cursor()

    for coin in COINS:
        data = response.get(coin, {})
        cur.execute("""
            INSERT INTO crypto_prices (coin_id, symbol, name, price_usd, market_cap, volume_24h)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            coin, coin[:4], coin.title(), 
            data.get('usd'), data.get('usd_market_cap'), data.get('usd_24h_vol')
        ))
    conn.commit()
    cur.close()
    conn.close()

with DAG("crypto_hourly_dag", default_args=default_args, schedule_interval='@hourly', catchup=False) as dag:
    extract_task = PythonOperator(
        task_id="extract_store_crypto_data",
        python_callable=fetch_and_store
    )
