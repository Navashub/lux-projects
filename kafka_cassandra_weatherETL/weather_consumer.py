import json
import uuid
import os
from confluent_kafka import Consumer, KafkaError
from cassandra.cluster import Cluster
from dotenv import load_dotenv
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Kafka configuration
kafka_config = {
    "bootstrap.servers": "localhost:9092",
    "group.id": "weather_consumer_group",
    "auto.offset.reset": "earliest",
    "security.protocol": "PLAINTEXT",
}


# Cassandra configuration
cassandra_host = os.getenv('CASSANDRA_HOST')

# Connect to Cassandra
cluster = Cluster([cassandra_host])
session = None

def initialize_cassandra():
    """Initialize Cassandra connection and create keyspace/table if needed."""
    global session
    try:
        session = cluster.connect()

        # Create keyspace if it doesn't exist
        session.execute("""
            CREATE KEYSPACE IF NOT EXISTS weather_data
            WITH replication = {'class': 'SimpleStrategy', 'replication_factor': '1'}
            AND durable_writes = true;
        """)

        # Use the keyspace
        session.execute("USE weather_data")

        # Create table if it doesn't exist
        session.execute("""
            CREATE TABLE IF NOT EXISTS navas_simple_weather (
                id uuid PRIMARY KEY,
                city_name text,
                temperature float,
                timestamp timestamp,
                weather_description text,
                weather_main text
            );
        """)
        logger.info("Cassandra table ready")
        return True
    except Exception as e:
        logger.error(f"Cassandra initialization error: {e}")
        return False

def insert_weather_data(weather_data):
    """Insert weather data into Cassandra."""
    try:
        # Extract interesting fields
        city = weather_data["extracted_city"]
        temp = weather_data["main"]["temp"]
        timestamp = weather_data["dt"]
        weather_desc = weather_data["weather"][0]["description"]
        weather_main = weather_data["weather"][0]["main"]

        # Insert data into Cassandra
        query = """
            INSERT INTO navas_simple_weather (id, city_name, temperature, timestamp, weather_description, weather_main)
            VALUES (%s, %s, %s, toTimestamp(now()), %s, %s)
        """
        session.execute(query, (uuid.uuid4(), city, temp, weather_desc, weather_main))
        logger.info(f"Inserted weather for {city} at {timestamp}")
        return True
    except Exception as e:
        logger.error(f"Error inserting data: {e}")
        return False

def consume_weather_data():
    """Consume weather data from Kafka and store in Cassandra."""
    # Initialize Cassandra
    if not initialize_cassandra():
        return

    # Create Kafka consumer
    consumer = Consumer(kafka_config)
    consumer.subscribe(["weather_data"])

    logger.info("Subscribed to topic: weather_data")

    try:
        while True:
            msg = consumer.poll(1.0)

            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    continue
                else:
                    logger.error(f"Consumer error: {msg.error()}")
                    break
            try:
                weather_data = json.loads(msg.value())
                insert_weather_data(weather_data)
            except Exception as e:
                logger.error(f"Error processing message: {e}")

    except KeyboardInterrupt:
        logger.info("Stopping consumer")
    finally:
        consumer.close()
        cluster.shutdown()

if __name__ == "__main__":
    consume_weather_data()