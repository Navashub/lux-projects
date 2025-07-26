
# import requests
# import os
# from datetime import datetime

# def download_knbs_data():
#     # URL for food price dataset from Kenya Open Data Portal
#     # Example dataset: Consumer Price Index (CPI) or food price data
#     # Replace with specific dataset URL after exploring https://kenya.opendataforafrica.org/
#     url = "https://kenya.opendataforafrica.org/api/data?dataset=consumer-price-index"
#     output_dir = "data/raw"
#     os.makedirs(output_dir, exist_ok=True)
    
#     headers = {
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
#     }
#     response = requests.get(url, headers=headers)
    
#     if response.status_code == 200:
#         file_path = f"{output_dir}/food_prices_{datetime.now().strftime('%Y%m')}.csv"
#         with open(file_path, 'wb') as f:
#             f.write(response.content)
#         return file_path
#     else:
#         raise Exception(f"Failed to download bandage: {response.status_code}")



import os
import shutil
from datetime import datetime

def download_knbs_data():
    try:
        # Path to manually downloaded file in Downloads folder
        source_file = "C:/Users/navas/Downloads/wfp_food_prices_ken.csv"
        output_dir = "data/raw"
        os.makedirs(output_dir, exist_ok=True)
        
        # Destination path with timestamp
        file_path = f"{output_dir}/food_prices_{datetime.now().strftime('%Y%m')}.csv"
        
        print(f"Copying file from {source_file} to {file_path}")
        if not os.path.exists(source_file):
            raise FileNotFoundError(f"Source file not found: {source_file}")
        
        shutil.copy(source_file, file_path)
        print(f"Copy successful! File saved to {file_path}")
        return file_path
    except Exception as e:
        print(f"Error in download_knbs_data: {str(e)}")
        raise

if __name__ == "__main__":
    download_knbs_data()