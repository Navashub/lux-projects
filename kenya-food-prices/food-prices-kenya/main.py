import pandas as pd

def main():
    df = pd.read_csv('data/processed/cleaned_food_prices.csv')
    print("Sample Data:")
    print(df.head())
    print("\nAverage Price by Commodity:")
    print(df.groupby('commodity')['price'].mean())

if __name__ == "__main__":
    main() 