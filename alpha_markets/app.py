import requests
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('ALPHA_VANTAGE_API_KEY')


def get_daily_data(symbol, api_key, outputsize='compact'):
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={api_key}&outputsize={outputsize}"
    
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        
        if 'Time Series (Daily)' not in data:
            print("Error:", data.get('Note', 'Unknown API error'))
            return None
            
        df = pd.DataFrame(data['Time Series (Daily)']).T
        df = df.rename(columns={
            '1. open': 'open',
            '2. high': 'high', 
            '3. low': 'low',
            '4. close': 'close',
            '5. volume': 'volume'
        }).astype(float)
        
        df.index = pd.to_datetime(df.index)
        return df.sort_index()
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return None
    
if api_key:
    print("Fetching AAPL daily data...")
    aapl_data = get_daily_data("AAPL", api_key)
    
    if aapl_data is not None:
        print("\nSuccess! First 5 rows:")
        print(aapl_data.head())
    else:
        print("\nFailed to retrieve data")
else:
    print("Error: ALPHA_VANTAGE_API_KEY not found in .env file")