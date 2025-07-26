import pandas as pd
import os

def clean_data():
    raw_path = 'data/raw/wfp_food_prices_ken.csv'
    processed_path = '../../data/processed/cleaned_food_prices.csv'
    df = pd.read_csv(raw_path, skiprows=[1])
    # Basic cleaning
    df = df.dropna(subset=['price', 'usdprice'])
    df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')
    # Normalize units or other cleaning as needed
    df.to_csv(processed_path, index=False)
    print("Data cleaned.")

if __name__ == "__main__":
    clean_data() 