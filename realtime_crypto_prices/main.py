import logging
import signal
import sys
from crypto_collector import CryptoDataCollector

def signal_handler(sig, frame):
    """Handle interrupt signals gracefully"""
    print('\nShutting down gracefully...')
    sys.exit(0)

def main():
    """Main entry point for the crypto data collection system"""
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('crypto_collector.log'),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    # Register signal handler for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    print("🚀 Starting Realtime Crypto Price Collector")
    print("=" * 50)
    print("Monitoring: BTC, ETH, BNB")
    print("Database: PostgreSQL")
    print("Collection Interval: Every 1 minute")
    print("Press Ctrl+C to stop")
    print("=" * 50)
    
    # Initialize and start the collector
    collector = CryptoDataCollector()
    
    try:
        # Display initial stats
        collector.display_stats()
        
        # Start data collection
        collector.start_data_collection()
        
    except KeyboardInterrupt:
        logging.info("Received interrupt signal, shutting down...")
        collector.stop_data_collection()
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        collector.stop_data_collection()
        sys.exit(1)

if __name__ == "__main__":
    main()
