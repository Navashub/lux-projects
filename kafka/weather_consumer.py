import json
from kafka import KafkaConsumer

consumer = KafkaConsumer(
    "weather",
    bootstrap_servers="localhost:9092",
    auto_offset_reset = "earliest",
    enable_auto_commit = True,
    value_deserializer = lambda m: json.loads(m.decode('utf-8'))  
)

print("Listening for weather data")

for message in consumer:
    weather = message.value
    print(f"{weather['city']}")
