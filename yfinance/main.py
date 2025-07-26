import os
import yfinance as yf
import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime, timedelta


DATABASE_URL = os.getenv("DATABASE_URL", "postgres://avnadmin:AVNS_Jvib48pYtaFIOeAPq2z@my-postgres-db-navashub.f.aivencloud.com:12378/defaultdb?sslmode=require")
SYMBOLS = ["BTC-USD", "ETH-USD", "SOL-USD"] 


def fetch_crypto_data(symbols, days=5*365):
    """Fetch historical data for cryptocurrencies"""
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)

    data = yf.download(
        symbols,
        start=start_date.strftime("%Y-%m-%d"),
        end=end_date.strftime("%Y-%m-%d"),
        group_by="ticker"
    )

    return data


def store_data_in_db(data, db_url):
    """Store data in PostgreSQL database"""
    # Check if DATABASE_URL is properly configured

    engine = create_engine(db_url)
    
    # Handle both single and multi-symbol data structures
    if hasattr(data.columns, 'levels') and len(data.columns.levels) > 0:
        # Multi-symbol data
        for symbol in data.columns.levels[0]:
            df = data[symbol].copy()
            df['symbol'] = symbol.replace("-USD", "")
            df.reset_index(inplace=True)
            df.to_sql(
                'crypto_prices_1a',
                engine,
                if_exists='append',
                index=False,
                schema='recur'
            )
            print(f"Data for {symbol} stored successfully")
    else:
        # Single symbol data
        df = data.copy()
        df['symbol'] = SYMBOLS[0].replace("-USD", "")
        df.reset_index(inplace=True)
        df.to_sql(
            'crypto_prices_1a',
            engine,
            if_exists='append',
            index=False,
            schema='recur'
        )
        print(f"Data for {SYMBOLS[0]} stored successfully")

def main():
    print("🚀 Starting crypto data fetch...")
    
    # Fetch data
    crypto_data = fetch_crypto_data(SYMBOLS)
    print(f"✅ Successfully fetched data for {len(SYMBOLS)} symbols")

    # Store data in db
    store_data_in_db(crypto_data, DATABASE_URL)

    print("✅ Process completed successfully")


if __name__ == "__main__":
    main()