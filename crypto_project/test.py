from pycoingecko import CoinGeckoAPI
from datetime import datetime
import pandas as pd

cg = CoinGeckoAPI()

def get_coin_list():
    """Get list of supported coins with their IDs"""
    return cg.get_coins_list()

def get_supported_vs_currencies():
    """Get list of supported vs currencies"""
    return cg.get_supported_vs_currencies()

def fetch_crypto_data(coin_ids, vs_currency='usd'):
    """
    Fetch market data for multiple cryptocurrencies using pycoingecko
    Returns list of dictionaries with relevant data
    """
    try:
        # Get market data
        data = cg.get_coins_markets(
            vs_currency=vs_currency,
            ids=coin_ids,
            price_change_percentage='1h,24h,7d'
        )
        
        # Transform data to our desired format
        formatted_data = []
        for coin in data:
            formatted_data.append({
                'coin_id': coin['id'],
                'symbol': coin['symbol'],
                'name': coin['name'],
                'current_price': coin['current_price'],
                'market_cap': coin['market_cap'],
                'total_volume': coin['total_volume'],
                'price_change_1h': coin['price_change_percentage_1h_in_currency'],
                'price_change_24h': coin['price_change_percentage_24h_in_currency'],
                'price_change_7d': coin['price_change_percentage_7d_in_currency'],
                'last_updated': datetime.fromtimestamp(coin['last_updated'] / 1000),
                'image': coin['image']
            })
            
        return formatted_data
        
    except Exception as e:
        print(f"Error fetching data from CoinGecko: {e}")
        return []

def get_historical_data(coin_id, vs_currency='usd', days=30):
    """
    Get historical market data including price, market cap, and volume
    Returns a pandas DataFrame
    """
    try:
        data = cg.get_coin_market_chart_by_id(
            id=coin_id,
            vs_currency=vs_currency,
            days=days
        )
        
        # Process prices
        prices = pd.DataFrame(data['prices'], columns=['timestamp', 'price'])
        prices['timestamp'] = pd.to_datetime(prices['timestamp'], unit='ms')
        prices.set_index('timestamp', inplace=True)
        
        # Process market caps
        market_caps = pd.DataFrame(data['market_caps'], columns=['timestamp', 'market_cap'])
        market_caps.set_index('timestamp', inplace=True)
        
        # Process total volumes
        total_volumes = pd.DataFrame(data['total_volumes'], columns=['timestamp', 'total_volume'])
        total_volumes.set_index('timestamp', inplace=True)
        
        # Combine all data
        df = pd.concat([prices, market_caps, total_volumes], axis=1)
        df.index.name = 'date'
        
        return df
        
    except Exception as e:
        print(f"Error fetching historical data for {coin_id}: {e}")
        return pd.DataFrame()
    
if __name__ == "__main__":
    # Get list of coins and print a few
    coin_list = get_coin_list()
    print("Sample coin list:")
    print(coin_list[:5])  # Show first 5 coin entries

    # Get supported vs currencies and print
    vs_currencies = get_supported_vs_currencies()
    print("\nSupported vs currencies:")
    print(vs_currencies[:10])  # Show first 10 supported currencies

    # Choose a few popular coins
    coins_to_fetch = ['bitcoin', 'ethereum', 'cardano']

    # Fetch current market data
    print("\nFetching current market data...")
    market_data = fetch_crypto_data(coins_to_fetch)
    for coin in market_data:
        print(coin)

    # Fetch historical data for bitcoin for the past 7 days
    print("\nFetching historical data for Bitcoin (7 days)...")
    historical_df = get_historical_data('bitcoin', days=7)
    print(historical_df.head())  # Print first few rows
