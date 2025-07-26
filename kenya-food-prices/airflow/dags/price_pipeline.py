from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import scripts.download_data as download
import scripts.clean_data as clean
import scripts.load_to_postgres as load

default_args = {
    'owner': 'data_engineer',
    'depends_on_past': False,
    'start_date': datetime(2025, 7, 1),
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'food_prices_pipeline',
    default_args=default_args,
    description='ETL pipeline for Kenya food prices',
    schedule_interval='@monthly',
)

get_task = PythonOperator(
    task_id='get_data',
    python_callable=download.download_knbs_data,
    dag=dag,
)

clean_task = PythonOperator(
    task_id='clean_data',
    python_callable=clean.clean_and_transform,
    dag=dag,
)

load_task = PythonOperator(
    task_id='load_data',
    python_callable=load.load_to_postgres,
    dag=dag,
)

get_task >> clean_task >> load_task