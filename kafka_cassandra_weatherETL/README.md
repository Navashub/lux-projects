
# 🌦️ Automated Weather Data Pipeline using Kafka and Cassandra

This project implements an automated ETL pipeline that fetches live weather data from OpenWeatherMap for African cities, streams it into **Apache Kafka**, and stores it in **Apache Cassandra** using Python.

---

## 📦 Tech Stack

- **Python 3.11**
- **Apache Kafka** (via Docker)
- **Apache Cassandra** (via Docker)
- **Confluent Kafka Python client**
- **DataStax Cassandra Python driver**
- **OpenWeatherMap API**

---

## ⚠️ Prerequisite: Python 3.11

The **Cassandra Python driver** (`cassandra-driver`) does **not support Python 3.12+** due to removal of `asyncore`.

✅ Solution: We use **Python 3.11** to ensure compatibility.

---

## 🚀 Project Setup

### 1. Clone the Repository

```bash
git clone https://github.com/Navashub/lux-projects/tree/main/kafka_cassandra_weatherETL
cd kafka_cassandra_weatherETL
```

---

### 2. Install Python 3.11 (if not already installed)

Download from: https://www.python.org/downloads/release/python-3110/

✅ Be sure to:
- Check **"Add Python to PATH"**
- Use **"Install for all users"**

---

### 3. Create and Activate Virtual Environment

```bash
py -3.11 -m venv myvenv311
myvenv311\Scripts\activate
```

---

### 4. Install Python Dependencies

```bash
pip install -r requirements.txt
```

Or manually:

```bash
pip install cassandra-driver confluent_kafka python-dotenv requests
```

---

### 5. Set Up `.env` File

Create a `.env` file in the root of your project:

```env
# Kafka
BOOTSTRAP_SERVERS=localhost:9092

# Cassandra
CASSANDRA_HOST=localhost

# OpenWeatherMap
WEATHER_API_KEY=your_openweather_api_key
```

---

## 🐳 Running Kafka & Cassandra with Docker

### 1. Start Docker Desktop

Ensure Docker Desktop is running.

### 2. Run Docker Compose

```bash
docker-compose up -d
```

This starts:

- ✅ Kafka (on port `9092`)
- ✅ Zookeeper (on port `2181`)
- ✅ Cassandra (on port `9042`)

### 3. Confirm the containers

```bash
docker ps
```

---

## 🧠 What the Scripts Do

- `weather_producer.py`:
  - Fetches weather data from OpenWeatherMap
  - Sends it to Kafka topic `weather_data`

- `weather_consumer.py`:
  - Subscribes to Kafka topic `weather_data`
  - Inserts the data into Cassandra table `navas_simple_weather`

---

## ▶️ Running the Pipeline

### 1. Run the Consumer First (Cassandra writer)

```bash
python weather_consumer.py
```

This connects to Cassandra and waits for weather data.

---

### 2. Run the Producer (Weather fetcher → Kafka)

```bash
python weather_producer.py
```

This sends weather data for 5 African cities to Kafka.

---

## 🔍 Verify Data in Cassandra

```bash
docker exec -it kafka_cassandra_weatheretl-cassandra-1 cqlsh
```

Then run:

```sql
USE weather_data;

SELECT * FROM navas_simple_weather;
```

You should see records like:

| city_name   | temperature | timestamp           | weather_main | weather_description |
|-------------|-------------|---------------------|---------------|----------------------|
| Nairobi     | 22.4        | 2025-06-15 10:12:48 | Clouds        | scattered clouds     |

---

## 🔁 Optional: Make Producer Run Every Hour

In `weather_producer.py`, replace the main function with:

```python
def produce_weather_data_loop():
    while True:
        for city in cities:
            data = fetch_weather_data(city)
            if data:
                producer.produce(topic, key=city, value=json.dumps(data), callback=delivery_report)
                producer.poll(0)
        producer.flush()
        logger.info("Waiting 1 hour before next fetch...")
        time.sleep(60 * 60)

if __name__ == "__main__":
    produce_weather_data_loop()
```

Now the producer runs forever, fetching new data every 1 hour.

---

## ✅ Summary

This project is a complete weather ETL pipeline that:

- Automates weather data ingestion
- Uses Kafka for streaming
- Uses Cassandra for scalable storage
- Can be extended to support alerts, analytics, and dashboards

---

## 📌 Credits

Built with ❤️ by [Navas Herbert](https://github.com/Navashub)
