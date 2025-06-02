from airflow import DAG
from airflow.providers.http.hooks.http import HttpHook
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.decorators import task
from datetime import datetime, timedelta
import requests
import json


# Latitude and longitude for the location
LATITUDE = '1.2921'
LONGITUDE = '36.8219'

POSTGRES_CONN_ID = 'postgres_default'
API_CONN_ID = 'open_meteo_api'

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2025, 6, 2),
}

## DAG
with DAG(dag_id='weather_etl_pipleine',
         default_args=default_args,
         schedule='@daily',
         catchup=False) as dag:
    
    @task()
    def extract_weather_data():
        """Extract weather data from Open Meteo API."""
        
        # Use the HTTP hook to get CONNECTIION details from airflow connections
        http_hook = HttpHook(http_conn_id=API_CONN_ID, method='GET')
        
        ## Build the API endpoint
        ## Url = https://api.open-meteo.com
        ## Url = https://api.open-meteo.com/v1/forecast?latitude=51.5074&longitude=-0.1278&current_weather=true
        endpoint = f'/v1/forecast?latitude={LATITUDE}&longitude={LONGITUDE}&current_weather=true'
        
        
        # Make the request via the HTTP hook
        response = http_hook.run(endpoint)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to fetch weather data: {response.status_code}")
        
    @task()
    def transform_weather_data(weather_data):
        """Transform the extracted weather data."""
        current_weather = weather_data['current_weather']
        transformed_data = {
            'latitude': LATITUDE,
            'longitude': LONGITUDE,
            'temperature': current_weather['temperature'],
            'windspeed': current_weather['windspeed'],
            'winddirection': current_weather['winddirection'],
            'weathercode': current_weather['weathercode']
            
        }
        return transformed_data
        
        
    @task()
    def load_weather_data(transform_data):
        """Load transfrormed data into PostgreSQL."""
        pg_hook = PostgresHook(postgres_conn_id=POSTGRES_CONN_ID)
        conn = pg_hook.get_conn()
        cursor = conn.cursor()
        
        # Create table if it doesnt exist
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS weather_data (
            latitude FLOAT,
            longitude FLOAT,
            temperature FLOAT,
            windspeed FLOAT,
            winddirection FLOAT,
            weathercode INT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)
        
        
        # Instert transformed data into the table
        cursor.execute("""
        INSERT INTO weather_data (latitude, longitude, temperature, windspeed, winddirection, weathercode)
        VALUES (%s, %s, %s, %s, %s, %s);
        """, (
            transform_data['latitude'],
            transform_data['longitude'],
            transform_data['temperature'],
            transform_data['windspeed'],
            transform_data['winddirection'],
            transform_data['weathercode']
        ))
        # Commit the transaction
        conn.commit()   
        cursor.close()
        
    # DAG workflow - ETL Pipleine
    weather_data = extract_weather_data()
    transformed_data = transform_weather_data(weather_data)
    load_weather_data(transformed_data)
    
    