import requests
import os

def get_data():
    url = "https://data.humdata.org/dataset/e0d3fba6-f9a2-45d7-b949-140c455197ff/resource/517ee1bf-2437-4f8c-aa1b-cb9925b9d437/download/wfp_food_prices_ken.csv"
    response = requests.get(url)
    os.makedirs('data/raw', exist_ok=True)
    with open('data/raw/wfp_food_prices_ken.csv', 'wb') as f:
        f.write(response.content)
    print("Data downloaded.")

if __name__ == "__main__":
    get_data() 