import requests
import os
import json
import time
from dotenv import load_dotenv
from kafka import KafkaProducer

load_dotenv()
API_KEY = os.getenv("API_KEY")

producer = KafkaProducer(
    bootstrap_servers = "localhost:9092",
    value_serializer = lambda v:json.dumps(v).encode('utf-8')
)


city = "Nairobi"
def getting_weather(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}"
    response =  requests.get(url)
    if response.status_code == 200:
        data = response.json()
        
        return {
            "city" : data['name'],
            "country" : data['sys']['country'],
            "description" : data['weather'][0]['description'],
            "temperature" : data['main']['temp']
        }
    else:
        print("Error fetching weather data")
        return None
    
while True:
    weather = getting_weather(city)
    if weather:
        producer.send("weather", value=weather)
        print("Produced: ", weather)
time.sleep(5)










