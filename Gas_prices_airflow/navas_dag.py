from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.bash import BashOperator 


default_args = {
    'owner':'navas',
    'start_date':datetime(2025,5,26),
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
    'depends_on_past': False
}

with DAG(
    dag_id = 'navas_gas_prices_pipleine',
    schedule_interval = '@daily',
    default_args=default_args,
    catchup = False
) as dag:
    
    
    venv_path = 'airflowenv/bin/activate'
    script_path = '/root/navas'
    run_script = BashOperator(
        task_id = 'run_script',
        bash_command = f'source{venv_path} && python3 {script_path}'
    )
    
run_script