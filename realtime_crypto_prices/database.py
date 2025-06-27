import psycopg2
import psycopg2.extras
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import logging
from config import DB_CONFIG

class DatabaseManager:
    def __init__(self):
        self.connection = None
        self.cursor = None
        
    def connect(self):
        """Establish connection to PostgreSQL database"""
        try:
            self.connection = psycopg2.connect(**DB_CONFIG)
            self.connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            self.cursor = self.connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            logging.info("Connected to PostgreSQL database")
            return True
        except psycopg2.Error as e:
            logging.error(f"Error connecting to PostgreSQL: {e}")
            return False
    
    def create_database_if_not_exists(self):
        """Create database if it doesn't exist"""
        try:
            # Connect to default postgres database to create our database
            temp_config = DB_CONFIG.copy()
            temp_config['database'] = 'postgres'
            temp_conn = psycopg2.connect(**temp_config)
            temp_conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            temp_cursor = temp_conn.cursor()
            
            # Check if database exists
            temp_cursor.execute(f"SELECT 1 FROM pg_database WHERE datname = '{DB_CONFIG['database']}'")
            exists = temp_cursor.fetchone()
            
            if not exists:
                temp_cursor.execute(f"CREATE DATABASE {DB_CONFIG['database']}")
                logging.info(f"Database '{DB_CONFIG['database']}' created successfully")
            else:
                logging.info(f"Database '{DB_CONFIG['database']}' already exists")
                
            temp_cursor.close()
            temp_conn.close()
            
        except psycopg2.Error as e:
            logging.error(f"Error creating database: {e}")
    
    def create_tables(self):
        """Create tables for storing crypto data"""
        try:
            create_table_query = """
            CREATE TABLE IF NOT EXISTS crypto_prices (
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
            
            CREATE INDEX IF NOT EXISTS idx_crypto_timestamp ON crypto_prices(timestamp);
            CREATE INDEX IF NOT EXISTS idx_crypto_symbol ON crypto_prices(symbol);
            CREATE INDEX IF NOT EXISTS idx_crypto_timestamp_symbol ON crypto_prices(timestamp, symbol);
            """
            
            self.cursor.execute(create_table_query)
            logging.info("Tables created successfully")
            
        except psycopg2.Error as e:
            logging.error(f"Error creating tables: {e}")
    
    def insert_crypto_data(self, data):
        """Insert crypto data into the database"""
        try:
            insert_query = """
            INSERT INTO crypto_prices (timestamp, symbol, price, open_price, high_price, low_price, volume)
            VALUES (%(timestamp)s, %(symbol)s, %(price)s, %(open_price)s, %(high_price)s, %(low_price)s, %(volume)s)
            ON CONFLICT (timestamp, symbol) 
            DO UPDATE SET 
                price = EXCLUDED.price,
                open_price = EXCLUDED.open_price,
                high_price = EXCLUDED.high_price,
                low_price = EXCLUDED.low_price,
                volume = EXCLUDED.volume
            """
            
            self.cursor.execute(insert_query, data)
            logging.debug(f"Inserted data for {data['symbol']} at {data['timestamp']}")
            
        except psycopg2.Error as e:
            logging.error(f"Error inserting data: {e}")
    
    def get_latest_prices(self, limit=10):
        """Get latest prices for all symbols"""
        try:
            query = """
            SELECT DISTINCT ON (symbol) 
                symbol, price, timestamp 
            FROM crypto_prices 
            ORDER BY symbol, timestamp DESC 
            LIMIT %s
            """
            
            self.cursor.execute(query, (limit,))
            return self.cursor.fetchall()
            
        except psycopg2.Error as e:
            logging.error(f"Error fetching latest prices: {e}")
            return []
    
    def close(self):
        """Close database connection"""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        logging.info("Database connection closed") 