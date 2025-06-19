import os
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

def get_db_engine():
    db_url = os.getenv("DATABASE_URL")
    return create_engine(db_url)
