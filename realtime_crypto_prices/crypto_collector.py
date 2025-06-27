import json
import websocket
import pandas as pd
import logging
import threading
import time
from datetime import datetime, timezone
from database import DatabaseManager
from config import CRYPTO_ASSETS, BINANCE_WS_URL, COLLECTION_INTERVAL

class CryptoDataCollector:
    def __init__(self):
        self.db_manager = DatabaseManager()
        self.ws = None
        self.running = False
        self.data_buffer = {}
        self.last_insert_time = {}
        
        # Initialize database
        self.setup_database()
        
        # Setup WebSocket URL
        self.setup_websocket_url()
        
    def setup_database(self):
        """Initialize database connection and create tables"""
        self.db_manager.create_database_if_not_exists()
        if self.db_manager.connect():
            self.db_manager.create_tables()
        else:
            raise Exception("Failed to connect to database")
    
    def setup_websocket_url(self):
        """Setup WebSocket URL with crypto assets"""
        # Convert assets to lowercase and add kline_1m stream
        streams = [asset.lower() + '@kline_1m' for asset in CRYPTO_ASSETS]
        self.socket_url = BINANCE_WS_URL + '/'.join(streams)
        logging.info(f"WebSocket URL: {self.socket_url}")
    
    def on_message(self, ws, message):
        """Handle incoming WebSocket messages"""
        try:
            data = json.loads(message)
            self.process_crypto_data(data)
        except Exception as e:
            logging.error(f"Error processing message: {e}")
    
    def on_error(self, ws, error):
        """Handle WebSocket errors"""
        logging.error(f"WebSocket error: {error}")
    
    def on_close(self, ws, close_status_code, close_msg):
        """Handle WebSocket close"""
        logging.info("WebSocket connection closed")
        self.running = False
    
    def on_open(self, ws):
        """Handle WebSocket open"""
        logging.info("WebSocket connection opened")
        self.running = True
    
    def process_crypto_data(self, source):
        """Process crypto data from WebSocket"""
        try:
            # Extract data from WebSocket message
            kline_data = source['data']['k']
            symbol = source['data']['s']
            event_time = source['data']['E']
            
            # Convert timestamp to datetime
            timestamp = pd.to_datetime(event_time, unit='ms', utc=True)
            
            # Prepare data for database
            crypto_data = {
                'timestamp': timestamp,
                'symbol': symbol,
                'price': float(kline_data['c']),  # Close price
                'open_price': float(kline_data['o']),  # Open price
                'high_price': float(kline_data['h']),  # High price
                'low_price': float(kline_data['l']),   # Low price
                'volume': float(kline_data['v'])       # Volume
            }
            
            # Store in buffer
            self.data_buffer[symbol] = crypto_data
            
            # Check if we should insert data (every minute)
            current_time = datetime.now(timezone.utc)
            if symbol not in self.last_insert_time:
                self.last_insert_time[symbol] = current_time
                self.insert_data_to_db(crypto_data)
            else:
                time_diff = (current_time - self.last_insert_time[symbol]).total_seconds()
                if time_diff >= COLLECTION_INTERVAL:
                    self.insert_data_to_db(crypto_data)
                    self.last_insert_time[symbol] = current_time
            
            logging.info(f"Processed data for {symbol}: ${crypto_data['price']:.2f}")
            
        except Exception as e:
            logging.error(f"Error processing crypto data: {e}")
    
    def insert_data_to_db(self, data):
        """Insert data into database"""
        try:
            self.db_manager.insert_crypto_data(data)
            logging.info(f"Inserted {data['symbol']} data into database")
        except Exception as e:
            logging.error(f"Error inserting data to database: {e}")
    
    def start_data_collection(self):
        """Start the WebSocket connection and data collection"""
        logging.info("Starting crypto data collection...")
        
        websocket.enableTrace(False)
        self.ws = websocket.WebSocketApp(
            self.socket_url,
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close,
            on_open=self.on_open
        )
        
        # Start WebSocket in a separate thread
        self.ws.run_forever()
    
    def stop_data_collection(self):
        """Stop data collection"""
        logging.info("Stopping crypto data collection...")
        self.running = False
        if self.ws:
            self.ws.close()
        self.db_manager.close()
    
    def get_latest_data(self):
        """Get latest data from database"""
        return self.db_manager.get_latest_prices()
    
    def display_stats(self):
        """Display current statistics"""
        latest_data = self.get_latest_data()
        if latest_data:
            print("\n=== Latest Crypto Prices ===")
            for row in latest_data:
                print(f"{row['symbol']}: ${row['price']:.2f} (at {row['timestamp']})")
        else:
            print("No data available")

# Function to run the collector with graceful shutdown
def run_collector():
    """Run the crypto data collector with graceful shutdown"""
    collector = CryptoDataCollector()
    
    try:
        # Start data collection
        collector.start_data_collection()
        
    except KeyboardInterrupt:
        logging.info("Received interrupt signal, shutting down...")
        collector.stop_data_collection()
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        collector.stop_data_collection()

if __name__ == "__main__":
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    run_collector() 