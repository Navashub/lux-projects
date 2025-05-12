from navas_etl import ApiExtractor, CsvLoader
import pandas as pd
import os
from dotenv import load_dotenv

# Load API key from .env
load_dotenv()
API_KEY = os.getenv('ALPHA_VANTAGE_API_KEY')

SYMBOL = "IBM"
OUTPUT_SIZE = "compact"

# Initialize extractor
extractor = ApiExtractor("https://www.alphavantage.co")

# Extract daily data
daily = extractor.extract(
    "query",
    params={
        "function": "TIME_SERIES_DAILY",
        "symbol": SYMBOL,
        "apikey": API_KEY,
        "outputsize": OUTPUT_SIZE
    }
)

# Extract weekly data
weekly = extractor.extract(
    "query",
    params={
        "function": "TIME_SERIES_WEEKLY",
        "symbol": SYMBOL,
        "apikey": API_KEY
    }
)

# Extract monthly data
monthly = extractor.extract(
    "query",
    params={
        "function": "TIME_SERIES_MONTHLY",
        "symbol": SYMBOL,
        "apikey": API_KEY
    }
)

def transform_av_data(raw_data):
    """Convert to a cleaned DataFrame"""
    ts_key = next((k for k in raw_data if "Time Series" in k), None)
    if not ts_key:
        raise ValueError("No 'Time Series' key found in data")

    df = pd.DataFrame(raw_data[ts_key]).T.reset_index()
    df = df.rename(columns={"index": "date"})
    df.columns = [col.split(". ")[-1] for col in df.columns]

    df["date"] = pd.to_datetime(df["date"])
    df[["open", "high", "low", "close"]] = df[["open", "high", "low", "close"]].astype("float64")
    df["volume"] = df["volume"].astype("int64")
    
    return df

# Transform each dataset
daily_df = transform_av_data(daily)
weekly_df = transform_av_data(weekly)
monthly_df = transform_av_data(monthly)

# Save to CSV
CsvLoader().load(daily_df, f"{SYMBOL}_daily.csv")
CsvLoader().load(weekly_df, f"{SYMBOL}_weekly.csv")
CsvLoader().load(monthly_df, f"{SYMBOL}_monthly.csv")

print("✅ All data saved successfully.")
