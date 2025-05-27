import http.client
import json
import pandas as pd
from sqlalchemy import create_engine

conn = http.client.HTTPSConnection("api.collectapi.com")

headers = {
    'content-type': "application/json",
    'authorization': "apikey 0DSo0ZEHWlDNCbqTHo3AT3:3OtfbBUm3m0IlzhwbPXKHE"
    }

conn.request("GET", "/gasPrice/stateUsaPrice?state=WA", headers=headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))

# Parse the JSON response
parsed_data = json.loads(data.decode("utf-8"))

# Extract the cities data from the parsed JSON
cities_data = parsed_data['result']['cities']


# Create a DataFrame from the cities data
df = pd.DataFrame(cities_data)

# drop column lowerName
df = df.drop(columns='lowerName')

#renaming 'name' columns
df = df.rename(columns={'name':'City'})


# Database connection parameters
user="postgres"
password="1234"
host="194.180.176.173"
port="5432"
database="postgres"


engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{database}')


# sending the DataFrame to PostgreSQL
df.to_sql( "navas_gas_prices", engine, if_exists='replace',index=False)