# Crypto Price Collector Setup Guide

## Prerequisites

1. **PostgreSQL Database** - Make sure you have PostgreSQL installed and running
2. **Python 3.11+** - This project requires Python 3.11 or higher

## Installation Steps

### 1. Install Dependencies

```bash
# Install UV (if not already installed)
pip install uv

# Install project dependencies
uv sync
```

### 2. Database Setup

#### Option A: Create Database Manually
```sql
-- Connect to PostgreSQL as superuser
psql -U postgres

-- Create database and user
CREATE DATABASE crypto_prices;
CREATE USER crypto_user WITH PASSWORD 'your_secure_password';
GRANT ALL PRIVILEGES ON DATABASE crypto_prices TO crypto_user;
```

#### Option B: Let the application create the database
The application will automatically create the database if it doesn't exist (requires PostgreSQL superuser privileges).

### 3. Environment Configuration

Create a `.env` file in the project root:

```bash
# PostgreSQL Database Configuration
DB_HOST=localhost
DB_PORT=5432
DB_NAME=crypto_prices
DB_USER=crypto_user
DB_PASSWORD=your_secure_password

# Optional: Set log level
LOG_LEVEL=INFO

# Optional: Set collection interval in seconds (default: 60)
COLLECTION_INTERVAL=60
```

### 4. Database Schema

The application automatically creates the following table structure:

```sql
CREATE TABLE crypto_prices (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP WITH TIME ZONE NOT NULL,
    symbol VARCHAR(20) NOT NULL,
    price DECIMAL(20, 8) NOT NULL,
    open_price DECIMAL(20, 8),
    high_price DECIMAL(20, 8),
    low_price DECIMAL(20, 8),
    volume DECIMAL(20, 8),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(timestamp, symbol)
);
```

## Running the Application

### Start Data Collection

```bash
# Using UV (recommended)
uv run main.py

# Or using Python directly
python main.py
```

### Test Database Connection

```python
# Test script
from database import DatabaseManager

db = DatabaseManager()
db.create_database_if_not_exists()
if db.connect():
    db.create_tables()
    print("Database setup successful!")
    latest_data = db.get_latest_prices()
    print("Latest data:", latest_data)
    db.close()
else:
    print("Database connection failed!")
```

## Monitored Cryptocurrencies

- **BTC/USDT** - Bitcoin
- **ETH/USDT** - Ethereum  
- **BNB/USDT** - Binance Coin

## Data Collection Details

- **Source**: Binance WebSocket API
- **Stream**: 1-minute kline data
- **Frequency**: Data stored every 1 minute
- **Data Points**: Open, High, Low, Close prices + Volume

## Grafana Visualization Setup

### 1. Install Grafana

```bash
# Ubuntu/Debian
sudo apt-get install -y software-properties-common
sudo add-apt-repository "deb https://packages.grafana.com/oss/deb stable main"
wget -q -O - https://packages.grafana.com/gpg.key | sudo apt-key add -
sudo apt-get update
sudo apt-get install grafana

# Start Grafana
sudo systemctl start grafana-server
sudo systemctl enable grafana-server
```

### 2. Configure PostgreSQL Data Source

1. Open Grafana (default: http://localhost:3000)
2. Login with admin/admin
3. Go to Configuration > Data Sources
4. Add PostgreSQL data source with your database credentials

### 3. Sample Queries for Dashboards

```sql
-- Latest prices for all cryptocurrencies
SELECT 
    timestamp,
    symbol,
    price
FROM crypto_prices 
WHERE timestamp >= NOW() - INTERVAL '1 hour'
ORDER BY timestamp DESC;

-- Price trends over time
SELECT 
    timestamp,
    symbol,
    price,
    volume
FROM crypto_prices 
WHERE timestamp >= NOW() - INTERVAL '24 hours'
ORDER BY timestamp;

-- Average price by hour
SELECT 
    DATE_TRUNC('hour', timestamp) as hour,
    symbol,
    AVG(price) as avg_price,
    MIN(price) as min_price,
    MAX(price) as max_price
FROM crypto_prices 
WHERE timestamp >= NOW() - INTERVAL '24 hours'
GROUP BY hour, symbol
ORDER BY hour;
```

## Troubleshooting

### Common Issues

1. **Database Connection Failed**
   - Check PostgreSQL is running: `sudo systemctl status postgresql`
   - Verify credentials in `.env` file
   - Ensure database exists

2. **WebSocket Connection Issues**
   - Check internet connection
   - Verify Binance API is accessible
   - Check firewall settings

3. **Permission Errors**
   - Ensure user has proper database privileges
   - Check file permissions for log files

### Logs

- Application logs are written to `crypto_collector.log`
- Use `tail -f crypto_collector.log` to monitor in real-time

## Production Deployment

### Using Systemd (Linux)

Create `/etc/systemd/system/crypto-collector.service`:

```ini
[Unit]
Description=Crypto Price Collector
After=network.target postgresql.service

[Service]
Type=simple
User=your_user
WorkingDirectory=/path/to/your/project
ExecStart=/path/to/your/project/.venv/bin/python main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable crypto-collector
sudo systemctl start crypto-collector
```

### Using Docker

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY . .

RUN pip install uv
RUN uv sync

CMD ["uv", "run", "main.py"]
```

## Support

If you encounter any issues, check the logs and ensure all prerequisites are met. The application includes comprehensive error handling and logging to help troubleshoot problems. 