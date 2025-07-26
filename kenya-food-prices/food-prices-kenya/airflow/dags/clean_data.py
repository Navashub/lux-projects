# import pandas as pd
# import os

# def clean_data():
#     raw_path = 'data/raw/wfp_food_prices_ken.csv'
#     processed_path = '../../data/processed/cleaned_food_prices.csv'
#     df = pd.read_csv(raw_path, skiprows=[1])
#     # Basic cleaning
#     df = df.dropna(subset=['price', 'usdprice'])
#     df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')
#     # Normalize units or other cleaning as needed
#     df.to_csv(processed_path, index=False)
#     print("Data cleaned.")

# if __name__ == "__main__":
#     clean_data() 


import pandas as pd
import os

def clean_data():
    # Use absolute paths
    input_file = '/opt/airflow/data/raw/wfp_food_prices_ken.csv'
    output_dir = '/opt/airflow/data/processed'
    output_file = os.path.join(output_dir, 'cleaned_food_prices.csv')
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Check if input file exists
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"Input file not found: {input_file}")
    
    # Read the CSV file
    df = pd.read_csv(input_file)
    
    # Your cleaning logic here
    # Example cleaning steps:
    # df = df.dropna()  # Remove rows with missing values
    # df = df[df['price'] > 0]  # Remove rows with negative prices
    # Add your specific cleaning logic
    
    # Save the cleaned data
    df.to_csv(output_file, index=False)
    
    print(f"Data cleaned and saved to: {output_file}")
    print(f"Shape: {df.shape}")
    
    return output_file

if __name__ == "__main__":
    clean_data()