import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Database configuration
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': os.getenv('DB_PORT', '5432'),
    'database': os.getenv('DB_NAME', 'crypto_prices'),
    'user': os.getenv('DB_USER', 'postgres'),
    'password': os.getenv('DB_PASSWORD', 'password')
}

# Crypto assets to monitor
CRYPTO_ASSETS = ['BTCUSDT', 'ETHUSDT', 'BNBUSDT']

# WebSocket URL
BINANCE_WS_URL = "wss://stream.binance.com:9443/stream?streams="

# Data collection interval (in seconds)
COLLECTION_INTERVAL = 60  # 1 minute 