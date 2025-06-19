from sqlalchemy import create_engine
from config.db_config import get_db_engine

def load_data_to_postgres(df, table_name='external_debt'):
    engine = get_db_engine()
    df.to_sql(table_name, engine, if_exists='replace', index=False)
