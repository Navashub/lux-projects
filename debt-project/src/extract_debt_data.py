import requests

def fetch_debt_data():
    url = "https://api.worldbank.org/v2/country/KE/indicator/DT.DOD.DECT.CD?format=json"
    params = {'date': '2010:2024'}
    response = requests.get(url, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception("Failed to fetch data from World Bank API")
