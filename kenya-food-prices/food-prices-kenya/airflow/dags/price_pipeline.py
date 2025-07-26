# from airflow import DAG
# from airflow.operators.python import PythonOperator
# from datetime import datetime
# import sys
# import os

# sys.path.append('D:\lux-projects\kenya-food-prices\food-prices-kenya\airflow\scripts')
# from get_data import get_data
# from clean_data import clean_data
# from load_data import load_data

# default_args = {
#     'owner': 'airflow',
#     'start_date': datetime(2025, 7, 1),
#     'retries': 1,
# }

# dag = DAG('price_pipeline', default_args=default_args, schedule_interval='@monthly')

# t1 = PythonOperator(
#     task_id='get_data',
#     python_callable=get_data,
#     dag=dag,
# )

# t2 = PythonOperator(
#     task_id='clean_data',
#     python_callable=clean_data,
#     dag=dag,
# )

# t3 = PythonOperator(
#     task_id='load_data',
#     python_callable=load_data,
#     dag=dag,
# )

# t1 >> t2 >> t3 



from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

# Import directly since files are in the same directory
from get_data import get_data
from clean_data import clean_data
from load_data import load_data

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2025, 7, 1),
    'retries': 1,
}

dag = DAG(
    'price_pipeline',
    default_args=default_args,
    schedule='@monthly'
)

t1 = PythonOperator(
    task_id='get_data',
    python_callable=get_data,
    dag=dag,
)

t2 = PythonOperator(
    task_id='clean_data',
    python_callable=clean_data,
    dag=dag,
)

t3 = PythonOperator(
    task_id='load_data',
    python_callable=load_data,
    dag=dag,
)

t1 >> t2 >> t3