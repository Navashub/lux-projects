import requests
import pandas as pd
import os
from dotenv import load_dotenv

def get_daily_data(symbol, api_key, outputsize='compact'):
    """
    Get free daily stock data from Alpha Vantage API (non-adjusted)
    
    Args:
        symbol (str): Stock ticker symbol (e.g., 'AAPL')
        api_key (str): Alpha Vantage API key
        outputsize (str): 'compact' (last 100 points) or 'full' (full history)
    
    Returns:
        pd.DataFrame: DataFrame with OHLC data or None if request fails
    """
    try:
        # Validate inputs
        if not api_key or not isinstance(api_key, str):
            raise ValueError("Invalid API key")
            
        # Make API request
        url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={api_key}&outputsize={outputsize}"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        # Check for API errors
        if 'Error Message' in data:
            print(f"API Error: {data['Error Message']}")
            return None
            
        if 'Note' in data:  # API limit note
            print(f"API Limit Note: {data['Note']}")
            return None
            
        if 'Time Series (Daily)' not in data:
            print("Unexpected API response format")
            print("Full response:", data)
            return None
        
        # Process successful response
        time_series = data['Time Series (Daily)']
        df = pd.DataFrame.from_dict(time_series, orient='index')
        
        # Convert columns to numeric
        cols = ['1. open', '2. high', '3. low', '4. close', '5. volume']
        df = df[cols]  # Only keep basic columns
        df[cols] = df[cols].apply(pd.to_numeric)
        
        # Rename columns
        df.columns = ['open', 'high', 'low', 'close', 'volume']
        df.index = pd.to_datetime(df.index)
        return df.sort_index()
        
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {str(e)}")
        return None
    except Exception as e:
        print(f"Error processing data: {str(e)}")
        return None

def main():
    # Load environment variables
    load_dotenv()
    api_key = os.getenv('ALPHA_VANTAGE_API_KEY')
    
    if not api_key:
        print("Error: API key not found in .env file")
        print("Please create a .env file with: ALPHA_VANTAGE_API_KEY=your_key_here")
        return
    
    print(f"Using API key: {api_key[:5]}...")  # Print first 5 chars for verification
    
    symbol = "AAPL"
    print(f"\nFetching daily data for {symbol}...")
    
    # Get data with error handling
    daily_data = get_daily_data(symbol, api_key, outputsize='compact')
    
    if daily_data is not None:
        print("\nSuccessfully retrieved data:")
        print(daily_data.head())
        
        # Save to CSV
        csv_file = f"{symbol}_daily.csv"
        daily_data.to_csv(csv_file)
        print(f"\nData saved to {csv_file}")
        
        # Basic analysis example
        print("\nRecent performance:")
        print(f"Last close: {daily_data.iloc[-1]['close']:.2f}")
        print(f"5-day range: {daily_data['close'].tail().min():.2f}-{daily_data['close'].tail().max():.2f}")
    else:
        print("\nFailed to retrieve data. Possible reasons:")
        print("- Invalid or missing API key")
        print("- API rate limit exceeded (5 calls/minute, 500/day)")
        print("- Network connectivity issues")
        print("- Alpha Vantage service unavailable")

if __name__ == "__main__":
    main()